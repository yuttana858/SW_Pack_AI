from pathlib import Path
from urllib.parse import parse_qs, unquote, urlparse

import httpx
import pytest
from fastapi.testclient import TestClient

from kb.chunker import build_chunks
from kb.index import HybridIndex
from kb.service import KnowledgeService
from swdata import Store as DataStore
from webapp.app import create_app
from webapp.auth import AuthConfig, Authenticator
from webapp.responders import SearchOnlyResponder
from webapp.store import Store

ROOT = Path(__file__).resolve().parent.parent
SECRET = "s" * 40


def github_mock(member_state="active", teams=("swpack-stewards", "plant-dallas")):
    def handler(req: httpx.Request) -> httpx.Response:
        u = str(req.url)
        if u.startswith("https://github.com/login/oauth/access_token"):
            return httpx.Response(200, json={"access_token": "gho_test"})
        assert req.headers["Authorization"] == "Bearer gho_test"
        if u.endswith("/user"):
            return httpx.Response(200, json={"id": 42, "login": "dana", "name": "Dana Eng", "email": None})
        if "/user/memberships/orgs/swis" in u:
            return httpx.Response(200 if member_state else 404, json={"state": member_state} if member_state else {})
        if "/user/teams" in u:
            return httpx.Response(200, json=[{"slug": t, "organization": {"login": "SWIS"}} for t in teams] +
                                  [{"slug": "elsewhere", "organization": {"login": "other-org"}}])
        return httpx.Response(404)
    return httpx.Client(transport=httpx.MockTransport(handler))


def make(http, monkeypatch):
    for k, v in {"SWPACK_AUTH_MODE": "github", "SWPACK_GITHUB_ORG": "swis", "GITHUB_CLIENT_ID": "cid",
                 "GITHUB_CLIENT_SECRET": "csecret", "SWPACK_SESSION_SECRET": SECRET,
                 "SWPACK_PUBLIC_URL": "https://swis--pack-ai.modal.run", "SWPACK_AUTH_CONFIG": "/nonexistent"}.items():
        monkeypatch.setenv(k, v)
    cfg = AuthConfig.load()
    cfg.github.update(team_roles={"swpack-stewards": "steward"}, team_plants={"plant-dallas": "dallas"})
    svc = KnowledgeService(HybridIndex.build(build_chunks(ROOT)), {"release_id": "t"}, DataStore([]))
    return TestClient(create_app(svc, Store(":memory:"), Authenticator(cfg), SearchOnlyResponder(svc), github_http=http),
                      base_url="https://swis--pack-ai.modal.run", follow_redirects=False)


def login(c):
    r = c.get("/auth/github/login")
    assert r.status_code == 302
    q = parse_qs(urlparse(r.headers["location"]).query)
    assert q["scope"] == ["read:user user:email read:org"] and q["client_id"] == ["cid"]
    assert q["redirect_uri"] == ["https://swis--pack-ai.modal.run/auth/github/callback"]
    return q["state"][0]


def fragment(r):
    return dict(x.split("=", 1) for x in urlparse(r.headers["location"]).fragment.split("&"))


def test_member_signs_in_with_team_roles_and_plants(monkeypatch):
    c = make(github_mock(), monkeypatch)
    assert c.get("/api/config").json()["auth"] == {"mode": "github", "login_url": "/auth/github/login", "org": "swis"}
    state = login(c)
    r = c.get("/auth/github/callback", params={"code": "abc", "state": state})
    token = fragment(r)["session"]
    me = c.get("/api/me", headers={"Authorization": f"Bearer {token}"}).json()
    assert me["name"] == "Dana Eng" and set(me["roles"]) == {"viewer", "engineer", "steward"} and me["plants"] == ["dallas"]


def test_non_member_refused(monkeypatch):
    c = make(github_mock(member_state=None), monkeypatch)
    r = c.get("/auth/github/callback", params={"code": "abc", "state": login(c)})
    assert "not an active member" in unquote(fragment(r)["error"])


def test_pending_invitation_refused(monkeypatch):
    c = make(github_mock(member_state="pending"), monkeypatch)
    r = c.get("/auth/github/callback", params={"code": "abc", "state": login(c)})
    assert "error" in fragment(r)


def test_state_from_another_browser_refused(monkeypatch):
    c = make(github_mock(), monkeypatch)
    state = login(c)
    c.cookies.clear()
    r = c.get("/auth/github/callback", params={"code": "abc", "state": state})
    assert "different browser" in unquote(fragment(r)["error"])


def test_tampered_state_and_cancel(monkeypatch):
    c = make(github_mock(), monkeypatch)
    login(c)
    assert "error" in fragment(c.get("/auth/github/callback", params={"code": "abc", "state": "x.y.z"}))
    assert "cancelled" in unquote(fragment(c.get("/auth/github/callback", params={"error": "access_denied"}))["error"])


def test_config_requires_settings(monkeypatch):
    monkeypatch.setenv("SWPACK_AUTH_MODE", "github")
    monkeypatch.setenv("SWPACK_AUTH_CONFIG", "/nonexistent")
    for k in ("SWPACK_GITHUB_ORG", "GITHUB_CLIENT_ID", "GITHUB_CLIENT_SECRET", "SWPACK_PUBLIC_URL", "SWPACK_SESSION_SECRET"):
        monkeypatch.delenv(k, raising=False)
    with pytest.raises(RuntimeError, match="github sign-in needs"):
        AuthConfig.load()
