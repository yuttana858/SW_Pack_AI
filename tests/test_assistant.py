import json
from pathlib import Path
from types import SimpleNamespace as NS

import pytest

from assistant.agent import AgentConfig, Assistant
from assistant.checks import check_answer
from assistant.tools import ALL_TOOLS, ToolLog
from kb.chunker import build_chunks
from kb.index import HybridIndex
from kb.service import KnowledgeService, UserContext
from swdata import Store

ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture(scope="module")
def service():
    return KnowledgeService(HybridIndex.build(build_chunks(ROOT)), {"release_id": "test"}, Store.from_dir(ROOT / "data"))


def text(t): return NS(type="text", text=t)
def call(i, name, inp): return NS(type="tool_use", id=i, name=name, input=inp)
def resp(stop, *blocks, model="claude-opus-5-5", details=None):
    return NS(stop_reason=stop, content=list(blocks), model=model, stop_details=details,
              usage=NS(input_tokens=100, output_tokens=20, cache_read_input_tokens=80, cache_creation_input_tokens=0))


class FakeClient:
    def __init__(self, script):
        self.script, self.calls = list(script), []
        self.beta = NS(messages=NS(create=self._create))

    def _create(self, **kw):
        self.calls.append({**kw, "messages": list(kw["messages"])})
        return self.script.pop(0)


MCKEE = {"model": "mckee_simple", "ect_n_per_mm": 5.604, "length_mm": 400, "width_mm": 300, "depth_mm": 300,
         "caliper_mm": 4.0, "dx_n_mm": None, "dy_n_mm": None}


def test_tool_loop_and_grounded_answer(service):
    client = FakeClient([
        resp("tool_use", text("Searching."), call("t1", "kb_search", {"query": "McKee", "k": 3, "kinds": None, "material_families": None}),
             call("t2", "box_compression", MCKEE)),
        resp("end_turn", text("Predicted BCT is 2462 N (553 lbf) [lib.formula.mckee-simple].")),
    ])
    r = Assistant(service, client).ask("BCT of a 400x300x300 RSC, 32 ECT C flute?", UserContext(plant="a"))
    assert r.stop_reason == "end_turn" and "2462" in r.answer and r.used_calculator
    second = client.calls[1]["messages"]
    assert second[-1]["role"] == "user" and [x["tool_use_id"] for x in second[-1]["content"]] == ["t1", "t2"]
    assert "Engineer context — plant: a" in client.calls[0]["messages"][0]["content"]
    # 553 lbf was never converted with convert_units, so the grounding check must flag it
    assert r.warnings == ["number 553 is not traceable to a tool result or retrieved text"]


def test_converted_number_is_grounded(service):
    client = FakeClient([
        resp("tool_use", call("t1", "box_compression", MCKEE)),
        resp("tool_use", call("t2", "convert_units", {"kind": "force", "value": 2462.3, "to": "us"})),
        resp("end_turn", text("Predicted BCT is 2462 N (553.6 lbf) [lib.formula.mckee-simple].")),
    ])
    r = Assistant(service, client).ask("BCT?", UserContext())
    assert r.warnings == [], r.warnings


def test_ungrounded_number_and_unknown_citation_flagged():
    log = [ToolLog("box_compression", {}, {"value": 2462.3, "formula": "lib.formula.mckee-simple"}, False)]
    w = check_answer("BCT 2462 N, roughly 3150 N wet [lib.formula.mckee-simple] [kb.fake.doc#x]", log)
    assert any("3150" in x for x in w) and any("kb.fake.doc#x" in x for x in w)
    assert not any("2462" in x for x in w)


def test_request_shape(service):
    client = FakeClient([resp("end_turn", text("No data in the knowledge base."))])
    Assistant(service, client, AgentConfig(effort="high")).ask("hi", UserContext())
    kw = client.calls[0]
    assert kw["model"] == "claude-opus-5-5" and kw["output_config"] == {"effort": "high"}
    assert kw["fallbacks"] == "default" and kw["betas"] == ["server-side-fallback-2026-07-01"]
    assert kw["system"][0]["cache_control"] == {"type": "ephemeral"} and "PACK AI" in kw["system"][0]["text"]
    assert "thinking" not in kw and "temperature" not in kw and "tool_choice" not in kw
    names = [t["name"] for t in kw["tools"]]
    assert "lookup_record" not in names and {"kb_search", "kb_read", "kb_resolve", "box_compression"} <= set(names)


def test_refusal(service):
    client = FakeClient([resp("refusal", details=NS(category="cyber", explanation="x"))])
    r = Assistant(service, client).ask("q", UserContext())
    assert r.stop_reason == "refusal" and r.refusal["category"] == "cyber" and r.answer == ""


def test_max_tokens_does_not_run_tools(service):
    client = FakeClient([resp("max_tokens", call("t1", "box_compression", MCKEE))])
    r = Assistant(service, client).ask("q", UserContext())
    assert r.stop_reason == "max_tokens" and r.tool_calls == []


def test_tool_errors_are_returned_with_is_error(service):
    client = FakeClient([resp("tool_use", call("t1", "kb_read", {"chunk_id": "nope"})), resp("end_turn", text("Not found."))])
    Assistant(service, client).ask("q", UserContext())
    tr = client.calls[1]["messages"][-1]["content"][0]
    assert tr["is_error"] is True and "no chunk" in json.loads(tr["content"])["result"]["error"]


def test_scope_cannot_be_widened_by_the_model(service):
    client = FakeClient([resp("tool_use", call("t1", "kb_resolve", {"record_type": "allowance_table", "filter_key": None,
                                                                     "filter_value": None, "approved_only": False})),
                         resp("end_turn", text("ok"))])
    r = Assistant(service, client).ask("q", UserContext(plant="a"))
    assert "plant" not in ALL_TOOLS[2]["input_schema"]["properties"]
    assert r.tool_calls[0].output["result"]["record"]["scope"] == "global"


def test_max_turns_guard(service):
    loop = [resp("tool_use", call(f"t{i}", "convert_units", {"kind": "length", "value": 1, "to": "si"})) for i in range(3)]
    r = Assistant(service, FakeClient(loop), AgentConfig(max_turns=3)).ask("q", UserContext())
    assert r.stop_reason == "max_turns" and r.warnings


def test_history_is_append_only(service):
    client = FakeClient([resp("end_turn", text("first")), resp("end_turn", text("second"))])
    a = Assistant(service, client)
    r1 = a.ask("q1", UserContext())
    r2 = a.ask("q2", UserContext(), history=r1.messages)
    assert r2.messages[: len(r1.messages)] == r1.messages
    assert r2.messages[len(r1.messages)] == {"role": "user", "content": "q2"}
