#!/usr/bin/env python3
"""Run the answer-quality eval against the live Claude API.

  python -m evals.run_answers --dry-run            # show the plan and an approximate cost, no API calls
  python -m evals.run_answers --limit 5            # run the first 5 questions
  python -m evals.run_answers                      # run all; writes evals/results/<timestamp>/

Every run spends API credit: get approval before running it. Grading is programmatic (see the
header of the eval YAML). Results: per-question pass/fail with reasons, transcripts of tool
calls, token usage, and the knowledge release id.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path

import yaml

from assistant.agent import AgentConfig, AgentResult, Assistant
from assistant.checks import CITE, NUM
from kb.service import KnowledgeService, UserContext

ROOT = Path(__file__).resolve().parent.parent
NO_DATA = re.compile(r"(not (?:covered|in|available in) the knowledge base|knowledge base (?:does not|doesn't)|"
                     r"no (?:data|information|record)|not (?:covered|available)|outside (?:the|my) (?:scope|knowledge))", re.I)
# Rough planning numbers per question (input incl. cache reads, output) for the cost estimate.
EST_IN, EST_OUT, PRICE_IN, PRICE_OUT, PRICE_CACHE = 60_000, 2_500, 4.0, 20.0, 0.20


def grade(item: dict, r: AgentResult) -> list[str]:
    fails = []
    called = {t.name for t in r.tool_calls}
    for need in item.get("must_call", []):
        if not set(need.split("|")) & called:
            fails.append(f"did not call {need}")
    nums = [float(m.group(1).replace(",", "")) for m in NUM.finditer(CITE.sub("", r.answer))]
    nums += [float(x) for x in re.findall(r"(?<![\w.])\d(?:\.\d+)?(?![\w.])", r.answer)]
    for v in item.get("values", []):
        tol = max(abs(v["value"]) * v.get("tol_pct", 0) / 100, 1e-9)
        if not any(abs(n - v["value"]) <= tol for n in nums):
            fails.append(f"missing value {v['value']} (±{v.get('tol_pct', 0)} %)")
    if item.get("must_cite"):
        cites = CITE.findall(r.answer)
        if not any(c.startswith(p) for c in cites for p in item["must_cite"]):
            fails.append(f"no citation starting with {item['must_cite']}")
    low = r.answer.lower()
    for phrase in item.get("must_mention", []):
        if not any(p.lower() in low for p in phrase.split("|")):
            fails.append(f"does not mention {phrase!r}")
    if item.get("no_data"):
        if not NO_DATA.search(r.answer):
            fails.append("should say the knowledge base does not cover this")
        if r.used_calculator:
            fails.append("used a calculator on an out-of-scope question")
    if len(r.warnings) > item.get("max_warnings", 0):
        fails.append(f"{len(r.warnings)} grounding warning(s): {r.warnings}")
    if r.stop_reason not in ("end_turn", "stop_sequence"):
        fails.append(f"stop_reason {r.stop_reason}")
    return fails


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--set", type=Path, default=ROOT / "evals" / "answers_seed.yaml")
    ap.add_argument("--limit", type=int)
    ap.add_argument("--effort", default="medium")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    items = yaml.safe_load(a.set.read_text())["questions"][: a.limit]
    est = len(items) * (EST_IN * (0.3 * PRICE_IN + 0.7 * PRICE_CACHE) + EST_OUT * PRICE_OUT) / 1e6
    print(f"{len(items)} questions, effort {a.effort}; rough cost estimate ${est:.2f} (claude-opus-5-5 list prices)")
    if a.dry_run:
        return 0
    service = KnowledgeService.load()
    bot = Assistant(service, config=AgentConfig(effort=a.effort))
    out_dir = ROOT / "evals" / "results" / dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    out_dir.mkdir(parents=True)
    rows, passed, usage = [], 0, {}
    for item in items:
        r = bot.ask(item["q"], UserContext(plant=item.get("plant")))
        fails = grade(item, r)
        passed += not fails
        for k, v in r.usage.items():
            usage[k] = usage.get(k, 0) + v
        rows.append({"id": item["id"], "pass": not fails, "fails": fails, "answer": r.answer, "warnings": r.warnings,
                     "tools": [{"name": t.name, "input": t.input, "is_error": t.is_error} for t in r.tool_calls],
                     "usage": r.usage, "served_by": r.served_by, "stop_reason": r.stop_reason})
        print(f"{'PASS' if not fails else 'FAIL'}  {item['id']}" + ("" if not fails else f"  {fails}"))
    summary = {"release_id": service.manifest["release_id"], "questions": len(items), "passed": passed,
               "pass_rate": round(passed / len(items), 3), "effort": a.effort, "usage": usage}
    (out_dir / "results.json").write_text(json.dumps({"summary": summary, "rows": rows}, indent=2, default=str))
    print(json.dumps(summary, indent=2))
    return 0 if summary["pass_rate"] >= 0.85 else 1


if __name__ == "__main__":
    sys.exit(main())
