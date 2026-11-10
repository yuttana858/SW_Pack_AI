"""SW Pack AI web app (phase C3).

  python -m webapp.app                      # http://127.0.0.1:8080 (dev sign-in, search-only without API key)
  SWPACK_AUTH_MODE=oidc python -m webapp.app

The page (webapp/static) talks to the JSON API below. Every API call needs a bearer token; the
engineer's plant comes from their identity (X-SWPack-Plant may only pick among granted plants).
"""
from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Literal

from fastapi import Depends, FastAPI, Header, HTTPException, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from assistant.checks import CITE
from kb.service import KnowledgeService, UserContext

from .auth import AuthConfig, AuthError, Authenticator, Identity
from .responders import Responder, make_responder
from .store import Store

ROOT = Path(__file__).resolve().parent.parent
STATIC = Path(__file__).resolve().parent / "static"


class AskIn(BaseModel):
    question: str = Field(min_length=1, max_length=8000)
    conversation_id: str | None = None
    effort: Literal["low", "medium", "high"] = "medium"


class FeedbackIn(BaseModel):
    message_id: str
    rating: Literal[-1, 1]
    comment: str | None = Field(default=None, max_length=4000)
    correction: str | None = Field(default=None, max_length=8000)
    target_ref: str | None = Field(default=None, max_length=300)


class DecisionIn(BaseModel):
    status: Literal["accepted", "rejected"]
    note: str | None = Field(default=None, max_length=4000)


class DevLoginIn(BaseModel):
    persona: str


def _jsonable(messages: list) -> list:
    out = []
    for m in messages:
        c = m["content"]
        if not isinstance(c, str):
            c = [b if isinstance(b, dict) else (b.to_dict() if hasattr(b, "to_dict") else b.model_dump(mode="json", exclude_none=True))
                 for b in c]
        out.append({"role": m["role"], "content": c})
    return out


def create_app(service: KnowledgeService, store: Store, auth: Authenticator, responder: Responder) -> FastAPI:
    app = FastAPI(title="SW Pack AI", docs_url=None, redoc_url=None)

    @app.exception_handler(AuthError)
    async def _auth_error(_: Request, e: AuthError):
        return JSONResponse({"error": str(e)}, status_code=e.status)

    def identity(authorization: str | None = Header(default=None)) -> Identity:
        return auth.authenticate(authorization)

    def plant_of(ident: Identity, x_swpack_plant: str | None) -> str | None:
        return Authenticator.choose_plant(ident, x_swpack_plant)

    def ctx_for(ident: Identity, plant: str | None) -> UserContext:
        role = "steward" if "steward" in ident.roles else "plant-admin" if "plant-admin" in ident.roles else \
            "engineer" if "engineer" in ident.roles else "viewer"
        return UserContext(user=ident.sub, plant=plant, role=role)

    def citations(text: str, ctx: UserContext) -> list[dict]:
        out = []
        for cid in dict.fromkeys(CITE.findall(text)):
            look = cid if service.index.read(cid) else f"card.{cid}" if service.index.read(f"card.{cid}") else None
            if look is None:                      # tolerate a shortened id if it matches exactly one chunk
                cands = [k for k in service.index.by_id if k.startswith(cid) or k.startswith(f"card.{cid}")]
                look = cands[0] if len(cands) == 1 else cid
            c = service.read(ctx, look)["result"]
            if "error" in c:
                out.append({"id": cid, "found": False})
            else:
                out.append({"id": cid, "found": True, "chunk_id": c["id"], "title": c["title"], "heading": c["heading"],
                            "kind": c["kind"], "confidence": c["confidence"], "status": c["status"], "path": c["path"]})
        return out

    # ---- public --------------------------------------------------------------------
    @app.get("/api/config")
    def config():
        return {"auth": auth.public_config(), "responder": responder.mode, "release_id": service.manifest.get("release_id")}

    @app.post("/api/dev/login")
    def dev_login(body: DevLoginIn):
        return {"token": auth.issue_dev_token(body.persona)}

    # ---- signed in -----------------------------------------------------------------
    @app.get("/api/me")
    def me(ident: Identity = Depends(identity)):
        return {**ident.public(), "can_propose": ident.can_propose, "responder": responder.mode,
                "release_id": service.manifest.get("release_id")}

    @app.post("/api/ask")
    def ask(body: AskIn, ident: Identity = Depends(identity), x_swpack_plant: str | None = Header(default=None)):
        plant = plant_of(ident, x_swpack_plant)
        ctx = ctx_for(ident, plant)
        if body.conversation_id:
            conv = store.conversation(body.conversation_id, ident.sub)
            if not conv:
                raise HTTPException(404, "conversation not found")
            if conv["plant"] != plant:
                raise HTTPException(409, "this conversation belongs to another plant; start a new conversation")
            cid, history = conv["id"], store.history(conv["id"])
        else:
            cid, history = store.create_conversation(ident.sub, plant, body.question), []
        r = responder.ask(body.question, ctx, history or None, body.effort)
        meta = {"citations": citations(r.answer, ctx), "warnings": r.warnings, "stop_reason": r.stop_reason,
                "release_id": r.release_id, "served_by": r.served_by, "usage": r.usage, "refusal": r.refusal,
                "effort": body.effort, "plant": plant, "mode": responder.mode,
                "tool_calls": [{"name": t.name, "input": t.input, "is_error": t.is_error} for t in r.tool_calls]}
        mid = store.save_turn(cid, ident.sub, body.question, r.answer, meta, _jsonable(r.messages))
        store.audit(ident.sub, "ask", {"conversation": cid, "message": mid, "plant": plant, "tools": len(r.tool_calls)})
        return {"conversation_id": cid, "message_id": mid, "answer": r.answer, **meta}

    @app.get("/api/conversations")
    def conversations(ident: Identity = Depends(identity)):
        return {"conversations": store.list_conversations(ident.sub)}

    @app.get("/api/conversations/{cid}")
    def conversation(cid: str, ident: Identity = Depends(identity)):
        conv = store.conversation(cid, ident.sub)
        if not conv:
            raise HTTPException(404, "conversation not found")
        return {"id": cid, "title": conv["title"], "plant": conv["plant"],
                "messages": [{"id": m["id"], "question": m["question"], "answer": m["answer"], **m["meta"]}
                             for m in store.messages(cid)]}

    @app.get("/api/chunk/{chunk_id:path}")
    def chunk(chunk_id: str, ident: Identity = Depends(identity), x_swpack_plant: str | None = Header(default=None)):
        res = service.read(ctx_for(ident, plant_of(ident, x_swpack_plant)), chunk_id)["result"]
        if "error" in res:
            raise HTTPException(404, res["error"])
        return res

    @app.post("/api/feedback")
    def feedback(body: FeedbackIn, ident: Identity = Depends(identity)):
        m = store.message(body.message_id)
        if not m or m["user_sub"] != ident.sub:
            raise HTTPException(404, "message not found")
        store.set_feedback(body.message_id, ident.sub, body.rating, body.comment)
        out = {"ok": True, "proposal_id": None}
        if body.correction:
            if not ident.can_propose:
                raise HTTPException(403, "your role cannot submit corrections")
            cites = (m.get("meta_json") and re.findall(r'"chunk_id": "([^"]+)"', m["meta_json"])) or []
            out["proposal_id"] = store.create_proposal(
                "correction", ident.sub, m["plant"],
                {"question": m["question"], "answer": m["answer"], "correction": body.correction, "comment": body.comment,
                 "cited_chunks": cites}, message_id=m["id"], target_ref=body.target_ref)
        store.audit(ident.sub, "feedback", {"message": body.message_id, "rating": body.rating, **out})
        return out

    def visible_proposals(ident: Identity, status: str | None) -> list[dict]:
        if "steward" in ident.roles:
            return store.proposals(status)
        if "plant-admin" in ident.roles:
            return store.proposals(status, list(ident.plants), include_global=False)
        return [p for p in store.proposals(status) if p["created_by"] == ident.sub]

    @app.get("/api/proposals")
    def proposals(status: str | None = "open", ident: Identity = Depends(identity)):
        return {"proposals": visible_proposals(ident, status)}

    @app.post("/api/proposals/{pid}/decision")
    def decide(pid: str, body: DecisionIn, ident: Identity = Depends(identity)):
        p = next((x for x in store.proposals(None) if x["id"] == pid), None)
        if not p:
            raise HTTPException(404, "proposal not found")
        allowed = "steward" in ident.roles or ("plant-admin" in ident.roles and p["plant"] in ident.plants)
        if not allowed:
            raise HTTPException(403, "only a data steward, or the plant admin for this plant, can decide")
        if p["status"] != "open":
            raise HTTPException(409, f"proposal already {p['status']}")
        r = store.decide(pid, ident.sub, body.status, body.note)
        store.audit(ident.sub, "decide", {"proposal": pid, "status": body.status})
        return {"proposal": {k: r[k] for k in ("id", "status", "decided_by", "decision_note")},
                "next_step": "Accepted corrections are applied to the corpus or data records by the steward "
                             "(data admin, phase C4); this decision is recorded in the audit log."}

    # ---- page ----------------------------------------------------------------------
    app.mount("/static", StaticFiles(directory=STATIC), name="static")

    @app.get("/")
    def index():
        return FileResponse(STATIC / "index.html")

    return app


def build_default_app() -> FastAPI:
    from kb.build import build  # noqa: PLC0415
    build_dir = ROOT / "build" / "kb"
    if not (build_dir / "index.json").exists():
        build(build_dir)
    service = KnowledgeService.load(build_dir)
    store = Store(os.environ.get("SWPACK_DB", ROOT / "build" / "webapp.db"))
    return create_app(service, store, Authenticator(AuthConfig.load()), make_responder(service))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(build_default_app(), host=os.environ.get("HOST", "127.0.0.1"), port=int(os.environ.get("PORT", "8080")))
