from pathlib import Path

import pytest
import yaml

from assistant.agent import AgentResult
from assistant.tools import ToolLog
from evals.run_answers import grade
from kb.chunker import build_chunks

ROOT = Path(__file__).resolve().parent.parent
ITEMS = {i["id"]: i for i in yaml.safe_load((ROOT / "evals/answers_seed.yaml").read_text())["questions"]}


def result(answer, tools=(), warnings=()):
    return AgentResult(answer=answer, stop_reason="end_turn", tool_calls=[ToolLog(t, {}, {}, False) for t in tools],
                       warnings=list(warnings), messages=[], release_id="t")


def test_every_citation_prefix_exists():
    ids = [c.id for c in build_chunks(ROOT)] + [f"lib.formula.{p.stem}" for p in (ROOT / "data/library/formulas").glob("*.yaml")]
    for item in ITEMS.values():
        for p in item.get("must_cite", []):
            assert any(i.startswith(p) for i in ids), f"{item['id']}: no chunk id starts with {p}"


def test_grader_pass_and_fail():
    good = result("BCT ≈ 2462 N [lib.formula.mckee-simple]; McKee tends to over-predict, confirm by ASTM D642.",
                  tools=["box_compression"])
    assert grade(ITEMS["bct-mckee-basic"], good) == []
    bad = result("BCT is about 2,900 N.", warnings=["number 2,900 is not traceable"])
    fails = grade(ITEMS["bct-mckee-basic"], bad)
    assert any("did not call" in f for f in fails) and any("missing value 2462" in f for f in fails)
    assert any("grounding warning" in f for f in fails)


def test_no_data_grading():
    assert grade(ITEMS["no-data-pet"], result("That is not covered in the knowledge base.")) == []
    assert grade(ITEMS["no-data-pet"], result("PET melts at about 260 °C.")) != []
