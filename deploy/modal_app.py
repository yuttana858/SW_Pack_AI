"""Modal deployment for the swpack-kb knowledge service (phase C1).

NOT DEPLOYED YET: requires the company's Modal workspace. When ready:

    modal deploy deploy/modal_app.py                       # web endpoint + functions
    modal run deploy/modal_app.py::build_index              # build a release into the Volume
    modal run deploy/modal_app.py::retrieval_eval           # recall@k on evals/retrieval_seed.yaml

Layout on the `swpack-kb` Volume:
    /kb/releases/<release_id>/index.json, manifest.json
    /kb/CURRENT                         -> text file holding the active release id (atomic swap)

Access: the endpoint uses Modal proxy auth (requires_proxy_auth=True), so only callers with a
Modal proxy token (Modal-Key / Modal-Secret headers) reach it. Per-user SSO identity and plant
scope replace the environment-variable context in phase C3.
Secrets (modal.Secret "swpack-kb"): VOYAGE_API_KEY only if the voyage embedder is used.
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
    .pip_install("mcp>=2.3,<3", "uvicorn>=0.30")
    .env({"PYTHONPATH": APP_DIR})
    .add_local_dir(str(REPO / "corpus"), f"{APP_DIR}/corpus")
    .add_local_dir(str(REPO / "data"), f"{APP_DIR}/data")
    .add_local_dir(str(REPO / "rag"), f"{APP_DIR}/rag")
    .add_local_dir(str(REPO / "schemas"), f"{APP_DIR}/schemas")
    .add_local_dir(str(REPO / "evals"), f"{APP_DIR}/evals")
    .add_local_python_source("kb", "packcalc", "swdata", "agent", "mcp_server")
)
volume = modal.Volume.from_name("swpack-kb", create_if_missing=True)
app = modal.App("swpack-kb", image=image)


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
