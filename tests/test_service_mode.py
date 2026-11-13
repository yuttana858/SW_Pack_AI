"""Service (proxy) mode for SWIS and session memory across turns and restarts."""
from pathlib import Path
from types import SimpleNamespace as NS

import pytest
from fastapi.testclient import TestClient

from assistant.prompt import system_prompt
from kb.chunker import build_chunks
from kb.index import HybridIndex
from kb.service import KnowledgeService
from swdata import Store as DataStore
from webapp.app import create_app
from webapp.auth import AuthConfig, Authenticator
from webapp.responders import AssistantResponder
from webapp.store import Store

ROOT = Path(__file__).resolve().parent.parent
KEY = "k" * 40
USER = {"X-Service-Key": KEY, "X-User-Id": "aad-123", "X-User-Name": "Jane Engineer",
        "X-User-Plants": "example", "X-User-Roles": "engineer,superuser"}


@pytest.fixture(scope="module")
def service():
    return KnowledgeService(HybridIndex.build(build_chunks(ROOT)), {"release_id": "t"}, DataStore.from_dir(ROOT / "data"))


class RecordingClient:
    """Scripted Claude stand-in that records every request's messages."""
    def __init__(self):
        self.requests = []
        self.beta = NS(messages=NS(create=self.create))

    def create(self, **kw):
        self.requests.append(list(kw["messages"]))
        n = len(self.requests)
        return NS(stop_reason="end_turn", model="claude-opus-5-5", stop_details=None,
                  usage=NS(input_tokens=1, output_tokens=1, cache_read_input_tokens=0, cache_creation_input_tokens=0),
                  content=[NS(type="text", text=f"answer {n}", to_dict=lambda n=n: {"type": "text", "text": f"answer {n}"})])


def make(service, monkeypatch, db=":memory:", client=None):
    monkeypatch.setenv("SWPACK_AUTH_MODE", "proxy")
    monkeypatch.setenv("PACKAI_SERVICE_KEY", KEY)
    monkeypatch.setenv("SWPACK_AUTH_CONFIG", "/nonexistent")
    client = client or RecordingClient()
    app = create_app(service, Store(db), Authenticator(AuthConfig.load()), AssistantResponder(service, client))
    return TestClient(app), client


def test_service_key_and_user_required(service, monkeypatch):
    c, _ = make(service, monkeypatch)
    assert c.get("/api/me").status_code == 401
    assert c.get("/api/me", headers={**USER, "X-Service-Key": "wrong"}).status_code == 401
    assert c.get("/api/me", headers={"X-Service-Key": KEY}).status_code == 400
    me = c.get("/api/me", headers=USER).json()
    assert me["name"] == "Jane Engineer" and me["plants"] == ["example"]
    assert set(me["roles"]) == {"viewer", "engineer"}          # unknown role "superuser" ignored


def test_proxy_mode_needs_a_strong_key(monkeypatch):
    monkeypatch.setenv("SWPACK_AUTH_MODE", "proxy")
    monkeypatch.setenv("PACKAI_SERVICE_KEY", "short")
    with pytest.raises(RuntimeError):
        AuthConfig.load()


def test_second_question_keeps_the_conversation(service, monkeypatch):
    c, client = make(service, monkeypatch)
    r1 = c.post("/api/ask", headers=USER, json={"question": "BCT for a 400x300x300 RSC in 32 ECT C flute?"}).json()
    r2 = c.post("/api/ask", headers=USER, json={"question": "And at 90 %RH?", "conversation_id": r1["conversation_id"]}).json()
    assert r2["conversation_id"] == r1["conversation_id"]
    second = client.requests[1]
    assert second[0]["content"].endswith("BCT for a 400x300x300 RSC in 32 ECT C flute?")
    assert second[1]["role"] == "assistant" and second[-1] == {"role": "user", "content": "And at 90 %RH?"}
    conv = c.get(f"/api/conversations/{r1['conversation_id']}", headers=USER).json()
    assert [m["question"] for m in conv["messages"]] == ["BCT for a 400x300x300 RSC in 32 ECT C flute?", "And at 90 %RH?"]


def test_conversation_survives_restart(service, monkeypatch, tmp_path):
    db = tmp_path / "sessions.db"
    c1, _ = make(service, monkeypatch, db=db)
    cid = c1.post("/api/ask", headers=USER, json={"question": "first"}).json()["conversation_id"]
    c2, client2 = make(service, monkeypatch, db=db)            # new process, same storage
    c2.post("/api/ask", headers=USER, json={"question": "second", "conversation_id": cid})
    assert client2.requests[0][0]["content"].endswith("first") and client2.requests[0][-1]["content"] == "second"


def test_users_cannot_see_each_others_sessions(service, monkeypatch):
    c, _ = make(service, monkeypatch)
    cid = c.post("/api/ask", headers=USER, json={"question": "mine"}).json()["conversation_id"]
    other = {**USER, "X-User-Id": "aad-999"}
    assert c.get(f"/api/conversations/{cid}", headers=other).status_code == 404
    assert c.post("/api/ask", headers=other, json={"question": "x", "conversation_id": cid}).status_code == 404


def test_assistant_is_named_swis(monkeypatch):
    system_prompt.cache_clear()
    assert system_prompt().startswith("You are SWIS, the PACK AI packaging-engineering assistant")
    monkeypatch.setenv("SWPACK_ASSISTANT_NAME", "Pack Buddy")
    system_prompt.cache_clear()
    assert system_prompt().startswith("You are Pack Buddy,")
    system_prompt.cache_clear()


def test_store_backup_restore_roundtrip(tmp_path):
    s = Store(tmp_path / "live.db")
    cid = s.create_conversation("u", "p", "title")
    s.save_turn(cid, "u", "q", "a", {}, [{"role": "user", "content": "q"}])
    s.backup_to(tmp_path / "durable.db")
    restored = Store(tmp_path / "durable.db")
    assert restored.history(cid) == [{"role": "user", "content": "q"}]
