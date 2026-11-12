"""Modal deployment for PACK AI (app "pack-ai" in workspace "swis").

SWIS API:     https://swis--pack-ai.modal.run          (function api, label "pack-ai", proxy auth)
MCP endpoint: https://swis--pack-ai-mcp-http.modal.run/mcp

NOT DEPLOYED YET: requires the company's Modal workspace. When ready:

    modal deploy deploy/modal_app.py                       # web endpoint + functions
    modal run deploy/modal_app.py::build_index              # build a release into the Volume
    modal run deploy/modal_app.py::retrieval_eval           # recall@k on evals/retrieval_seed.yaml

Layout on the `pack-ai-kb` Volume:
    /kb/releases/<release_id>/index.json, manifest.json
    /kb/CURRENT                         -> text file holding the active release id (atomic swap)

Access: the endpoint uses Modal proxy auth (requires_proxy_auth=True), so only callers with a
Modal proxy token (Modal-Key / Modal-Secret headers) reach it. Per-user SSO identity and plant
scope replace the environment-variable context in phase C3.
Secrets: modal.Secret "pack-ai-kb" holds VOYAGE_API_KEY (only if the voyage embedder is used);
modal.Secret "anthropic" holds ANTHROPIC_API_KEY for the assistant (`ask`).
"""
from __future__ import annotations

from pathlib import Path

import modal

REPO = Path(__file__).resolve().parent.parent
APP_DIR = "/app"
VOL_PATH = "/kb"

image = (
    modal.Image.debian_slim(python_version="3.12")
    .pip_install_from_requirements(str(REPO / "requirements.txt"))
    .pip_install("mcp>=2.3,<3", "uvicorn>=0.30", "anthropic>=2.8", "fastapi>=0.115", "pyjwt[crypto]>=2.9", "httpx>=0.27")
    .env({"PYTHONPATH": APP_DIR, "SWPACK_AUTH_CONFIG": f"{APP_DIR}/webapp/auth.yaml"})
    .add_local_dir(str(REPO / "corpus"), f"{APP_DIR}/corpus")
    .add_local_dir(str(REPO / "data"), f"{APP_DIR}/data")
    .add_local_dir(str(REPO / "rag"), f"{APP_DIR}/rag")
    .add_local_dir(str(REPO / "schemas"), f"{APP_DIR}/schemas")
    .add_local_dir(str(REPO / "evals"), f"{APP_DIR}/evals")
    .add_local_python_source("kb", "packcalc", "swdata", "agent", "mcp_server", "assistant", "webapp")
    .add_local_dir(str(REPO / "webapp" / "static"), f"{APP_DIR}/webapp/static")
    .add_local_file(str(REPO / "webapp" / "auth.yaml"), f"{APP_DIR}/webapp/auth.yaml")
)
volume = modal.Volume.from_name("pack-ai-kb", create_if_missing=True)
app = modal.App("pack-ai", image=image)


def _current_dir() -> Path:
    rel = (Path(VOL_PATH) / "CURRENT").read_text().strip()
    return Path(VOL_PATH) / "releases" / rel


@app.function(volumes={VOL_PATH: volume}, timeout=1800)
def build_index(embedder: str | None = None) -> dict:
    """Build a release from the files baked into the image and make it CURRENT."""
    from kb.build import build  # noqa: PLC0415

    tmp = Path(VOL_PATH) / "releases" / "_building"
    manifest = build(tmp, embedder)
    final = Path(VOL_PATH) / "releases" / manifest["release_id"]
    if final.exists():
        import shutil  # noqa: PLC0415
        shutil.rmtree(tmp)
    else:
        tmp.rename(final)
    (Path(VOL_PATH) / "CURRENT").write_text(manifest["release_id"])
    volume.commit()
    return {k: manifest[k] for k in ("release_id", "git_commit", "chunks", "record_status", "embedder")}


@app.function(volumes={VOL_PATH: volume})
def retrieval_eval(k: int = 10) -> dict:
    from kb.evaluate import evaluate  # noqa: PLC0415
    from kb.index import HybridIndex  # noqa: PLC0415

    return evaluate(HybridIndex.load(_current_dir() / "index.json"), Path(APP_DIR) / "evals" / "retrieval_seed.yaml", k)


@app.function(volumes={VOL_PATH: volume}, min_containers=0, scaledown_window=600)
@modal.concurrent(max_inputs=32)
@modal.asgi_app(requires_proxy_auth=True)
def mcp_http():
    """swpack-kb MCP server over streamable HTTP at /mcp."""
    from mcp.server.transport_security import TransportSecuritySettings  # noqa: PLC0415

    from kb.service import KnowledgeService  # noqa: PLC0415
    from mcp_server.server import context_from_env, create_server  # noqa: PLC0415

    volume.reload()
    service = KnowledgeService.load(_current_dir(), Path(APP_DIR) / "data")
    server = create_server(service, context_from_env())
    # Modal terminates TLS and enforces proxy auth in front of this app; host-header checks are
    # done by Modal's routing, so DNS-rebinding protection (meant for localhost servers) is off.
    return server.streamable_http_app(stateless_http=True, json_response=True,
                                      transport_security=TransportSecuritySettings(enable_dns_rebinding_protection=False))


@app.function(volumes={VOL_PATH: volume}, secrets=[modal.Secret.from_name("anthropic")], timeout=900)
def ask(question: str, plant: str | None = None, machine: str | None = None, effort: str = "medium",
        history: list | None = None) -> dict:
    """Assistant core (phase C2). Called by the web front end (phase C3) through the Modal SDK.
    Returns the answer, warnings, tool-call audit log and release id. History must be passed back
    unchanged on the next turn (append-only)."""
    from assistant.agent import AgentConfig, Assistant  # noqa: PLC0415
    from kb.service import KnowledgeService, UserContext  # noqa: PLC0415

    volume.reload()
    service = KnowledgeService.load(_current_dir(), Path(APP_DIR) / "data")
    r = Assistant(service, config=AgentConfig(effort=effort)).ask(question, UserContext(plant=plant, machine=machine), history)
    return {"answer": r.answer, "warnings": r.warnings, "stop_reason": r.stop_reason, "release_id": r.release_id,
            "served_by": r.served_by, "usage": r.usage, "refusal": r.refusal,
            "tool_calls": [{"name": t.name, "input": t.input, "is_error": t.is_error} for t in r.tool_calls],
            "history": [m if isinstance(m["content"], str) else
                        {"role": m["role"], "content": [b if isinstance(b, dict) else b.model_dump() for b in m["content"]]}
                        for m in r.messages]}


@app.function(volumes={VOL_PATH: volume}, secrets=[modal.Secret.from_name("anthropic"), modal.Secret.from_name("pack-ai-api")],
              max_containers=1, scaledown_window=900, timeout=900)
@modal.concurrent(max_inputs=16)
@modal.asgi_app(label="pack-ai", requires_proxy_auth=True)
def api():
    """PACK AI service for SWIS (and later the PACK AI page): conversations with session memory,
    knowledge search/read and calculators. See docs/SWIS-INTEGRATION.md.

    Access needs BOTH a Modal proxy token (Modal-Key / Modal-Secret headers) and the PACK AI service
    key (X-Service-Key). The caller has already signed the user in (Azure SSO) and passes X-User-Id,
    X-User-Name, X-User-Email, X-User-Plants and X-User-Roles.

    Secret "pack-ai-api": SWPACK_ENV=production, SWPACK_AUTH_MODE=proxy, PACKAI_SERVICE_KEY, and
    optionally SWPACK_ASSISTANT_NAME (default SWIS). Secret "anthropic": ANTHROPIC_API_KEY (the
    placeholder "none" keeps search-only mode).

    Session memory lives in SQLite on the Volume; every mutating request commits the Volume so
    conversations survive restarts and redeploys. max_containers=1 keeps SQLite safe; move to
    Postgres before scaling out.
    """
    import os  # noqa: PLC0415

    from kb.service import KnowledgeService  # noqa: PLC0415
    from webapp.app import create_app  # noqa: PLC0415
    from webapp.auth import AuthConfig, Authenticator  # noqa: PLC0415
    from webapp.responders import make_responder  # noqa: PLC0415
    from webapp.store import Store  # noqa: PLC0415

    volume.reload()
    service = KnowledgeService.load(_current_dir(), Path(APP_DIR) / "data")
    store = Store(os.environ.get("SWPACK_DB", f"{VOL_PATH}/sessions.db"))
    fastapi_app = create_app(service, store, Authenticator(AuthConfig.load()), make_responder(service))

    @fastapi_app.middleware("http")
    async def persist_after_writes(request, call_next):
        response = await call_next(request)
        if request.method in ("POST", "PUT", "PATCH", "DELETE") and response.status_code < 400:
            volume.commit()                     # make session memory durable
        return response

    return fastapi_app
