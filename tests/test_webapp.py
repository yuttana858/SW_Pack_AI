import time
from pathlib import Path
from types import SimpleNamespace as NS

import jwt
import pytest
from cryptography.hazmat.primitives.asymmetric import rsa
from fastapi.testclient import TestClient

from kb.chunker import build_chunks
from kb.index import HybridIndex
from kb.service import KnowledgeService
from swdata import Store as DataStore
from webapp.app import create_app
from webapp.auth import AuthConfig, Authenticator, AuthError
from webapp.responders import AssistantResponder, SearchOnlyResponder
from webapp.store import Store

ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture(scope="module")
def service():
    return KnowledgeService(HybridIndex.build(build_chunks(ROOT)), {"release_id": "test"}, DataStore.from_dir(ROOT / "data"))


def scripted_client():
    def create(**kw):
        n = sum(1 for m in kw["messages"] if m["role"] == "assistant")
        usage = NS(input_tokens=10, output_tokens=5, cache_read_input_tokens=0, cache_creation_input_tokens=0)
        if n == 0:
            return NS(stop_reason="tool_use", model="claude-opus-5-5", stop_details=None, usage=usage, content=[
                NS(type="tool_use", id=f"t{len(kw['messages'])}", name="convert_units",
                   input={"kind": "ect", "value": 32, "to": "si"}, to_dict=lambda: {"type": "tool_use"})])
        return NS(stop_reason="end_turn", model="claude-opus-5-5", stop_details=None, usage=usage, content=[
            NS(type="text", text="32 ECT is 5.604 kN/m [kb.reference.units-and-conversions#edge-crush-and-line-load-lb-in-kn-m-kg].",
               to_dict=lambda: {"type": "text", "text": "..."})])
    return NS(beta=NS(messages=NS(create=create)))


def make(service, responder=None):
    auth = Authenticator(AuthConfig(mode="dev", dev_secret="test-secret-0123456789-abcdefghijklmnop"))
    app = create_app(service, Store(":memory:"), auth, responder or AssistantResponder(service, scripted_client()))
    c = TestClient(app)
    def login(persona):
        tok = c.post("/api/dev/login", json={"persona": persona}).json()["token"]
        return {"Authorization": f"Bearer {tok}"}
    return c, login


def test_requires_sign_in(service):
    c, _ = make(service)
    assert c.get("/api/me").status_code == 401
    assert c.post("/api/ask", json={"question": "x"}).status_code == 401
    assert c.get("/api/config").json()["auth"]["mode"] == "dev"
    assert c.get("/").status_code == 200


def test_ask_flow_with_citations_and_audit(service):
    c, login = make(service)
    h = login("engineer-a")
    assert c.get("/api/me", headers=h).json()["plants"] == ["example"]
    r = c.post("/api/ask", headers=h, json={"question": "Convert 32 ECT to kN/m"}).json()
    assert r["plant"] == "example" and r["tool_calls"][0]["name"] == "convert_units"
    assert r["citations"][0]["found"] and r["citations"][0]["title"].startswith("Units")
    r2 = c.post("/api/ask", headers=h, json={"question": "and 44 ECT?", "conversation_id": r["conversation_id"]}).json()
    conv = c.get(f"/api/conversations/{r['conversation_id']}", headers=h).json()
    assert [m["id"] for m in conv["messages"]] == [r["message_id"], r2["message_id"]]
    assert c.get("/api/conversations", headers=h).json()["conversations"][0]["id"] == r["conversation_id"]


def test_plant_enforcement(service):
    c, login = make(service)
    h = login("engineer-a")
    assert c.post("/api/ask", headers={**h, "X-SWPack-Plant": "other"}, json={"question": "x"}).status_code == 403
    v = login("viewer")
    r = c.post("/api/ask", headers=v, json={"question": "x"}).json()
    assert r["plant"] is None


def test_conversations_are_private(service):
    c, login = make(service)
    r = c.post("/api/ask", headers=login("engineer-a"), json={"question": "x"}).json()
    other = login("steward")
    assert c.get(f"/api/conversations/{r['conversation_id']}", headers=other).status_code == 404
    assert c.post("/api/feedback", headers=other, json={"message_id": r["message_id"], "rating": 1}).status_code == 404


def test_feedback_correction_and_review(service):
    c, login = make(service)
    eng, viewer = login("engineer-a"), login("viewer")
    r = c.post("/api/ask", headers=eng, json={"question": "x"}).json()
    fb = c.post("/api/feedback", headers=eng, json={"message_id": r["message_id"], "rating": -1, "comment": "wrong",
                                                    "correction": "Our plant uses 5.60 kN/m"}).json()
    pid = fb["proposal_id"]
    assert pid
    rv = c.post("/api/ask", headers=viewer, json={"question": "x"}).json()
    assert c.post("/api/feedback", headers=viewer, json={"message_id": rv["message_id"], "rating": -1,
                                                         "correction": "x"}).status_code == 403
    assert c.post(f"/api/proposals/{pid}/decision", headers=eng, json={"status": "accepted"}).status_code == 403
    pa = login("plant-admin")
    assert [p["id"] for p in c.get("/api/proposals", headers=pa).json()["proposals"]] == [pid]
    d = c.post(f"/api/proposals/{pid}/decision", headers=pa, json={"status": "accepted", "note": "ok"}).json()
    assert d["proposal"]["status"] == "accepted"
    assert c.post(f"/api/proposals/{pid}/decision", headers=login("steward"), json={"status": "rejected"}).status_code == 409


def test_chunk_endpoint_scoped(service):
    c, login = make(service)
    h = login("engineer-a")
    assert c.get("/api/chunk/card.lib.formula.mckee-simple", headers=h).json()["kind"] == "card"
    assert c.get("/api/chunk/nope", headers=h).status_code == 404


def test_search_only_mode(service):
    c, login = make(service, SearchOnlyResponder(service))
    r = c.post("/api/ask", headers=login("engineer-a"), json={"question": "ISTA 3A drop sequence"}).json()
    assert r["mode"] == "search-only" and "Search-only mode" in r["answer"] and r["citations"][0]["found"]


def test_dev_mode_refused_in_production(monkeypatch):
    monkeypatch.setenv("SWPACK_ENV", "production")
    monkeypatch.setenv("SWPACK_AUTH_MODE", "dev")
    with pytest.raises(RuntimeError):
        AuthConfig.load()


def test_oidc_token_verification_and_group_mapping():
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    pub = jwt.PyJWK.from_dict({**jwt.algorithms.RSAAlgorithm.to_jwk(key.public_key(), as_dict=True), "kid": "k1"})
    jwks = NS(get_signing_key_from_jwt=lambda token: pub)
    cfg = AuthConfig(mode="oidc", oidc={"issuer": "https://idp.test", "audience": "swpack", "client_id": "spa"},
                     role_groups={"g-eng": "engineer", "g-stew": "steward"}, plant_groups={"g-dal": "dallas"})
    a = Authenticator(cfg, jwk_client=jwks)
    now = int(time.time())
    claims = {"sub": "u1", "name": "Dana", "email": "d@x", "groups": ["g-eng", "g-dal", "g-other"],
              "iss": "https://idp.test", "aud": "swpack", "iat": now, "exp": now + 300}
    tok = jwt.encode(claims, key, algorithm="RS256", headers={"kid": "k1"})
    ident = a.authenticate(f"Bearer {tok}")
    assert ident.roles == {"viewer", "engineer"} and ident.plants == ("dallas",)
    bad = jwt.encode({**claims, "aud": "other"}, key, algorithm="RS256", headers={"kid": "k1"})
    with pytest.raises(AuthError):
        a.authenticate(f"Bearer {bad}")
    expired = jwt.encode({**claims, "exp": now - 10}, key, algorithm="RS256", headers={"kid": "k1"})
    with pytest.raises(AuthError, match="expired"):
        a.authenticate(f"Bearer {expired}")
