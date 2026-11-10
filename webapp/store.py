"""SQLite persistence for the web app: conversations, answers, feedback, proposals, audit.

One file (SWPACK_DB, default build/webapp.db; on Modal a Volume path). Conversation history is
stored append-only, exactly as the agent returned it, so the next turn can replay it unchanged.
Swap for Postgres in phase C4 by re-implementing this class.
"""
from __future__ import annotations

import json
import sqlite3
import threading
import time
import uuid
from pathlib import Path
from typing import Any

SCHEMA = """
CREATE TABLE IF NOT EXISTS conversations (
  id TEXT PRIMARY KEY, user_sub TEXT NOT NULL, plant TEXT, title TEXT, created REAL, updated REAL,
  history_json TEXT NOT NULL DEFAULT '[]');
CREATE TABLE IF NOT EXISTS messages (
  id TEXT PRIMARY KEY, conversation_id TEXT NOT NULL REFERENCES conversations(id), user_sub TEXT NOT NULL,
  question TEXT NOT NULL, answer TEXT, meta_json TEXT, created REAL);
CREATE TABLE IF NOT EXISTS feedback (
  id TEXT PRIMARY KEY, message_id TEXT NOT NULL REFERENCES messages(id), user_sub TEXT NOT NULL,
  rating INTEGER NOT NULL, comment TEXT, created REAL, UNIQUE(message_id, user_sub));
CREATE TABLE IF NOT EXISTS proposals (
  id TEXT PRIMARY KEY, kind TEXT NOT NULL, status TEXT NOT NULL DEFAULT 'open', plant TEXT,
  message_id TEXT, target_ref TEXT, body_json TEXT NOT NULL, created_by TEXT NOT NULL, created REAL,
  decided_by TEXT, decided REAL, decision_note TEXT);
CREATE TABLE IF NOT EXISTS audit (
  id INTEGER PRIMARY KEY AUTOINCREMENT, ts REAL, user_sub TEXT, action TEXT, detail_json TEXT);
CREATE INDEX IF NOT EXISTS conv_user ON conversations(user_sub, updated);
CREATE INDEX IF NOT EXISTS prop_status ON proposals(status, plant);
"""


def _id() -> str:
    return uuid.uuid4().hex[:16]


class Store:
    def __init__(self, path: str | Path):
        Path(path).parent.mkdir(parents=True, exist_ok=True) if str(path) != ":memory:" else None
        self.db = sqlite3.connect(str(path), check_same_thread=False)
        self.db.row_factory = sqlite3.Row
        self.db.executescript(SCHEMA)
        self.lock = threading.Lock()

    def _x(self, sql: str, args: tuple = ()) -> sqlite3.Cursor:
        with self.lock, self.db:
            return self.db.execute(sql, args)

    def audit(self, user: str, action: str, detail: dict) -> None:
        self._x("INSERT INTO audit(ts,user_sub,action,detail_json) VALUES (?,?,?,?)",
                (time.time(), user, action, json.dumps(detail, default=str)))

    # ---- conversations -------------------------------------------------------------
    def create_conversation(self, user: str, plant: str | None, title: str) -> str:
        cid, now = _id(), time.time()
        self._x("INSERT INTO conversations(id,user_sub,plant,title,created,updated) VALUES (?,?,?,?,?,?)",
                (cid, user, plant, title[:120], now, now))
        return cid

    def conversation(self, cid: str, user: str) -> dict | None:
        r = self._x("SELECT * FROM conversations WHERE id=? AND user_sub=?", (cid, user)).fetchone()
        return dict(r) if r else None

    def list_conversations(self, user: str, limit: int = 50) -> list[dict]:
        rows = self._x("SELECT id,title,plant,updated FROM conversations WHERE user_sub=? ORDER BY updated DESC LIMIT ?",
                       (user, limit)).fetchall()
        return [dict(r) for r in rows]

    def history(self, cid: str) -> list:
        r = self._x("SELECT history_json FROM conversations WHERE id=?", (cid,)).fetchone()
        return json.loads(r["history_json"]) if r else []

    def save_turn(self, cid: str, user: str, question: str, answer: str, meta: dict, history: list) -> str:
        old = self.history(cid)
        if history[: len(old)] != old:
            raise ValueError("conversation history must be append-only")
        mid, now = _id(), time.time()
        self._x("INSERT INTO messages(id,conversation_id,user_sub,question,answer,meta_json,created) VALUES (?,?,?,?,?,?,?)",
                (mid, cid, user, question, answer, json.dumps(meta, default=str), now))
        self._x("UPDATE conversations SET history_json=?, updated=? WHERE id=?", (json.dumps(history, default=str), now, cid))
        return mid

    def messages(self, cid: str) -> list[dict]:
        rows = self._x("SELECT id,question,answer,meta_json,created FROM messages WHERE conversation_id=? ORDER BY created", (cid,))
        return [{**dict(r), "meta": json.loads(r["meta_json"] or "{}")} for r in rows.fetchall()]

    def message(self, mid: str) -> dict | None:
        r = self._x("SELECT m.*, c.plant FROM messages m JOIN conversations c ON c.id=m.conversation_id WHERE m.id=?", (mid,)).fetchone()
        return dict(r) if r else None

    # ---- feedback & proposals ------------------------------------------------------
    def set_feedback(self, mid: str, user: str, rating: int, comment: str | None) -> None:
        self._x("INSERT INTO feedback(id,message_id,user_sub,rating,comment,created) VALUES (?,?,?,?,?,?) "
                "ON CONFLICT(message_id,user_sub) DO UPDATE SET rating=excluded.rating, comment=excluded.comment",
                (_id(), mid, user, rating, comment, time.time()))

    def create_proposal(self, kind: str, user: str, plant: str | None, body: dict, message_id: str | None = None,
                        target_ref: str | None = None) -> str:
        pid = _id()
        self._x("INSERT INTO proposals(id,kind,plant,message_id,target_ref,body_json,created_by,created) VALUES (?,?,?,?,?,?,?,?)",
                (pid, kind, plant, message_id, target_ref, json.dumps(body), user, time.time()))
        return pid

    def proposals(self, status: str | None = None, plants: list[str] | None = None, include_global: bool = True) -> list[dict]:
        rows = [dict(r) for r in self._x("SELECT * FROM proposals ORDER BY created DESC").fetchall()]
        out = []
        for r in rows:
            if status and r["status"] != status:
                continue
            if plants is not None and not (r["plant"] in plants or (include_global and r["plant"] is None)):
                continue
            out.append({**r, "body": json.loads(r["body_json"])})
        return out

    def decide(self, pid: str, user: str, status: str, note: str | None) -> dict | None:
        self._x("UPDATE proposals SET status=?, decided_by=?, decided=?, decision_note=? WHERE id=? AND status='open'",
                (status, user, time.time(), note, pid))
        r = self._x("SELECT * FROM proposals WHERE id=?", (pid,)).fetchone()
        return dict(r) if r else None
