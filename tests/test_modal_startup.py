"""The Modal web() startup path, run locally with the Volume simulated."""
import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

import deploy.modal_app as m
from kb.build import build
from webapp.passwords import hash_password

ROOT = Path(__file__).resolve().parent.parent


class FakeVolume:
    commits = 0
    def reload(self): pass
    def commit(self): FakeVolume.commits += 1


@pytest.fixture()
def vol(tmp_path, monkeypatch):
    rel = build(tmp_path / "kb" / "releases" / "r1")
    (tmp_path / "kb" / "CURRENT").write_text("r1")
    monkeypatch.setattr(m, "VOL_PATH", str(tmp_path / "kb"))
    monkeypatch.setattr(m, "APP_DIR", str(ROOT))
    monkeypatch.setattr(m, "volume", FakeVolume())
    monkeypatch.setenv("SWPACK_DB", str(tmp_path / "local" / "sessions.db"))
    for k, v in {"SWPACK_ENV": "production", "SWPACK_AUTH_MODE": "password", "PACKAI_ADMIN_USER": "yuttana",
                 "PACKAI_ADMIN_PASSWORD_HASH": hash_password("a-long-test-password"), "SWPACK_SESSION_SECRET": "s" * 40,
                 "ANTHROPIC_API_KEY": "none", "SWPACK_AUTH_CONFIG": str(ROOT / "webapp" / "auth.yaml")}.items():
        monkeypatch.setenv(k, v)
    return tmp_path


def raw_web():
    return m.web._raw_f_          # the undecorated function body Modal runs in the container


def login(c):
    return {"Authorization": "Bearer " + c.post("/api/login", json={"username": "yuttana", "password": "a-long-test-password"}).json()["token"]}


def test_normal_start_and_sessions_survive_restart(vol):
    c = TestClient(raw_web()())
    assert c.get("/healthz").json()["ok"] is True and c.get("/").status_code == 200
    h = login(c)
    cid = c.post("/api/ask", headers=h, json={"question": "C flute take-up factor"}).json()["conversation_id"]
    assert (vol / "kb" / "sessions.db").exists() and FakeVolume.commits >= 1
    c2 = TestClient(raw_web()())                         # container restart: restore from the Volume backup
    conv = c2.get(f"/api/conversations/{cid}", headers=login(c2)).json()
    assert [x["question"] for x in conv["messages"]] == ["C flute take-up factor"]


def test_bad_secret_reports_instead_of_crash_looping(vol, monkeypatch):
    monkeypatch.setenv("PACKAI_ADMIN_PASSWORD_HASH", "plain-text-password")
    c = TestClient(raw_web()())
    r = c.get("/")
    assert r.status_code == 503 and "PACKAI_ADMIN_PASSWORD_HASH" in r.json()["reason"]
    assert "plain-text-password" not in json.dumps(r.json())


def test_unreadable_backup_is_set_aside(vol):
    (vol / "kb" / "sessions.db").write_bytes(b"this is not a sqlite database at all" * 10)
    c = TestClient(raw_web()())
    assert c.get("/healthz").status_code == 200
    assert list((vol / "kb").glob("sessions.unreadable-*.db"))
