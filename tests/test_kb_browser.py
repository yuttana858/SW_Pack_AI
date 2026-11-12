"""Knowledge-base browsing API and user preferences."""
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from kb.chunker import Chunk, build_chunks
from kb.index import HybridIndex
from kb.service import KnowledgeService
from swdata import Store as DataStore
from webapp.app import create_app
from webapp.auth import AuthConfig, Authenticator
from webapp.responders import SearchOnlyResponder
from webapp.store import Store

ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture(scope="module")
def client():
    chunks = build_chunks(ROOT) + [Chunk(id="card.plant.secret", doc_id="plant.secret", kind="card", title="Other plant board",
                                         heading="Other plant board", text="secret", path="x", tier="L3", scope="plant:elsewhere",
                                         material_family=["corrugated"], confidence="measured", status="approved", domain="board_material")]
    svc = KnowledgeService(HybridIndex.build(chunks), {"release_id": "t"}, DataStore([]))
    app = create_app(svc, Store(":memory:"), Authenticator(AuthConfig(mode="dev", dev_secret="d" * 40)), SearchOnlyResponder(svc))
    c = TestClient(app)
    tok = c.post("/api/dev/login", json={"persona": "engineer-a"}).json()["token"]
    c.headers["Authorization"] = f"Bearer {tok}"
    return c


def test_document_list_covers_corpus_and_library(client):
    docs = client.get("/api/kb/documents").json()["documents"]
    ids = {d["id"] for d in docs}
    assert "kb.performance.box-compression" in ids and "lib.formula.mckee-simple" in ids
    assert "plant.secret" not in ids                                     # other plant's data hidden
    corpus = [d for d in docs if d["kind"] == "corpus"]
    assert len(corpus) == 28 and sum(d["sections"] for d in docs) >= 370
    assert {d["group"] for d in docs if d["kind"] == "card"} == {"library"}


def test_document_reading_order_and_references(client):
    d = client.get("/api/kb/documents/kb.performance.box-compression").json()
    headings = [s["heading"] for s in d["sections"]]
    assert headings.index("Simplified McKee formula") < headings.index("Urbanik–Frank (2006) model and refit of McKee to world-wide data")
    assert d["references"] and all(r["title"] for r in d["references"])
    assert client.get("/api/kb/documents/plant.secret").status_code == 404
    assert client.get("/api/kb/documents/nope").status_code == 404


def test_search_points_to_documents(client):
    res = client.get("/api/kb/search", params={"q": "ISTA 3A drop sequence"}).json()["results"]
    assert res[0]["doc_id"] == "kb.testing.distribution-testing"
    assert client.get("/api/kb/search", params={"q": "  "}).json()["results"] == []


def test_theme_preference_persists_and_validates(client):
    assert client.get("/api/prefs").json()["theme"] == "system"
    assert client.put("/api/prefs", json={"theme": "dark"}).json()["theme"] == "dark"
    assert client.get("/api/prefs").json()["theme"] == "dark"
    assert client.put("/api/prefs", json={"theme": "purple"}).status_code == 422
