"""Single-user password login (interim until Azure SSO) plus service-key callers on the same app."""
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from kb.chunker import build_chunks
from kb.index import HybridIndex
from kb.service import KnowledgeService
from swdata import Store as DataStore
from webapp.app import create_app
from webapp.auth import AuthConfig, Authenticator
from webapp.passwords import hash_password, verify_password
from webapp.responders import SearchOnlyResponder
from webapp.store import Store

ROOT = Path(__file__).resolve().parent.parent
PW = "a-long-test-password"
HASH = hash_password(PW)
KEY = "v" * 40


@pytest.fixture(scope="module")
def service():
    return KnowledgeService(HybridIndex.build(build_chunks(ROOT)), {"release_id": "t"}, DataStore([]))


def make(service, monkeypatch, service_key=KEY):
    env = {"SWPACK_AUTH_MODE": "password", "PACKAI_ADMIN_USER": "Yuttana", "PACKAI_ADMIN_PASSWORD_HASH": HASH,
           "SWPACK_SESSION_SECRET": "s" * 40, "PACKAI_ADMIN_PLANTS": "example", "SWPACK_AUTH_CONFIG": "/nonexistent"}
    for k, v in env.items():
        monkeypatch.setenv(k, v)
    if service_key:
        monkeypatch.setenv("PACKAI_SERVICE_KEY", service_key)
    else:
        monkeypatch.delenv("PACKAI_SERVICE_KEY", raising=False)
    return TestClient(create_app(service, Store(":memory:"), Authenticator(AuthConfig.load()), SearchOnlyResponder(service)))


def test_hashing():
    assert verify_password(PW, HASH) and not verify_password("a-long-test-passworD", HASH)
    assert hash_password(PW) != HASH                       # salted
    with pytest.raises(ValueError):
        hash_password("short")


def test_login_and_session(service, monkeypatch):
    c = make(service, monkeypatch)
    assert c.get("/api/config").json()["auth"] == {"mode": "password"}
    tok = c.post("/api/login", json={"username": "yuttana", "password": PW}).json()["token"]
    h = {"Authorization": f"Bearer {tok}"}
    me = c.get("/api/me", headers=h).json()
    assert me["name"] == "Yuttana" and set(me["roles"]) >= {"engineer", "steward"} and me["plants"] == ["example"]
    r1 = c.post("/api/ask", headers=h, json={"question": "C flute take-up factor"}).json()
    r2 = c.post("/api/ask", headers=h, json={"question": "and B flute?", "conversation_id": r1["conversation_id"]}).json()
    assert r2["conversation_id"] == r1["conversation_id"]


def test_wrong_credentials_same_message(service, monkeypatch):
    c = make(service, monkeypatch)
    a = c.post("/api/login", json={"username": "yuttana", "password": "wrong-password-123"})
    b = c.post("/api/login", json={"username": "someone", "password": PW})
    assert a.status_code == b.status_code == 401 and a.json() == b.json()


def test_rate_limit(service, monkeypatch):
    c = make(service, monkeypatch)
    for _ in range(5):
        assert c.post("/api/login", json={"username": "yuttana", "password": "nope-nope-nope"}).status_code == 401
    assert c.post("/api/login", json={"username": "yuttana", "password": PW}).status_code == 429


def test_service_key_works_alongside(service, monkeypatch):
    c = make(service, monkeypatch)
    hdr = {"X-Service-Key": KEY, "X-User-Id": "svc-user", "X-User-Roles": "engineer"}
    assert c.get("/api/me", headers=hdr).json()["name"] == "svc-user"
    assert c.get("/api/me", headers={**hdr, "X-Service-Key": "x" * 40}).status_code == 401
    c2 = make(service, monkeypatch, service_key=None)                 # no key configured: header ignored, login needed
    assert c2.get("/api/me", headers=hdr).status_code == 401


def test_bad_config_refused(monkeypatch):
    monkeypatch.setenv("SWPACK_AUTH_MODE", "password")
    monkeypatch.setenv("SWPACK_AUTH_CONFIG", "/nonexistent")
    monkeypatch.setenv("PACKAI_ADMIN_USER", "u")
    monkeypatch.setenv("PACKAI_ADMIN_PASSWORD_HASH", "plaintext-password")
    monkeypatch.setenv("SWPACK_SESSION_SECRET", "s" * 40)
    with pytest.raises(RuntimeError, match="PACKAI_ADMIN_PASSWORD_HASH"):
        AuthConfig.load()
    monkeypatch.setenv("PACKAI_ADMIN_PASSWORD_HASH", HASH)
    monkeypatch.setenv("SWPACK_SESSION_SECRET", "short")
    with pytest.raises(RuntimeError, match="SWPACK_SESSION_SECRET"):
        AuthConfig.load()
