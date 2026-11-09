import asyncio
import json
from pathlib import Path

import pytest

from kb.chunker import Chunk, build_chunks
from kb.evaluate import evaluate
from kb.index import HybridIndex, tokenize
from kb.service import KnowledgeService, UserContext
from swdata import Store

ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture(scope="module")
def chunks():
    return build_chunks(ROOT)


@pytest.fixture(scope="module")
def index(chunks):
    return HybridIndex.build(chunks)


def test_chunks_unique_and_clean(chunks):
    ids = [c.id for c in chunks]
    assert len(ids) == len(set(ids))
    assert not any(c.heading.lower().startswith("research log") for c in chunks)
    assert all(len(c.text) <= 9000 for c in chunks)


def test_citations_resolved(chunks):
    c = next(c for c in chunks if c.id.startswith("kb.performance.box-compression#simplified-mckee"))
    assert c.citations and all(x["title"] for x in c.citations)


def test_code_tokenisation():
    assert "t839" in tokenize("TAPPI T 839") and "t839" in tokenize("T-839")
    assert "iso3037" in tokenize("ISO 3037") and "32ect" in tokenize("32 ECT") and "0201" in tokenize("FEFCO 0201")


def test_retrieval_seed_recall(index):
    r = evaluate(index, ROOT / "evals" / "retrieval_seed.yaml", k=10)
    assert r["recall_at_k"] >= 0.9, r["misses"]


def _plant_chunk(scope, text):
    return Chunk(id=f"card.{scope}.x", doc_id="x", kind="card", title="Secret board", heading="Secret board",
                 text=text, path="x", tier="L3", scope=scope, material_family=["corrugated"], confidence="measured",
                 status="approved")


def test_plant_scope_isolation(chunks):
    extra = [_plant_chunk("plant:a", "zebraboard caliper 4.1 mm"), _plant_chunk("plant:b", "zebraboard caliper 3.7 mm")]
    ix = HybridIndex.build(list(chunks) + extra)
    svc = KnowledgeService(ix, {"release_id": "test"}, Store([]))
    got_a = [h["scope"] for h in svc.search(UserContext(plant="a"), "zebraboard")["result"]]
    assert got_a == ["plant:a"]
    assert svc.search(UserContext(), "zebraboard")["result"] == []
    assert "error" in svc.read(UserContext(plant="a"), "card.plant:b.x")["result"]


def test_family_filter(index):
    svc = KnowledgeService(index, {"release_id": "t"}, Store([]))
    hits = svc.search(UserContext(), "density", families=["molded-pulp"])["result"]
    assert all({"molded-pulp", "multi"} & set(h["material_family"]) for h in hits)


def test_mcp_server_tools_are_read_only(index):
    from mcp_server.server import create_server
    svc = KnowledgeService(index, {"release_id": "t"}, Store.from_dir(ROOT / "data"))
    server = create_server(svc, UserContext())

    async def go():
        tools = await server.list_tools()
        assert {t.name for t in tools} == {"kb_search", "kb_read", "kb_resolve", "calc_list", "calc", "kb_release"}
        assert all(t.annotations.read_only_hint for t in tools)
        res = await server.call_tool("calc", {"calculator": "convert_units", "arguments": {"kind": "ect", "value": 32, "to": "si"}})
        return json.loads(res.content[0].text)

    out = asyncio.run(go())
    assert out["result"]["value"] == pytest.approx(5.604, abs=1e-3)
