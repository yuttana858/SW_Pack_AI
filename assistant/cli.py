#!/usr/bin/env python3
"""Ask the SW Pack AI assistant from the terminal (uses the Claude API; each question costs credit).

  python -m assistant.cli "What ECT do I need for ...?" --plant dallas
  python -m assistant.cli --chat --plant dallas          # multi-turn session
"""
from __future__ import annotations

import argparse
import json
import sys

from kb.service import KnowledgeService, UserContext

from .agent import AgentConfig, AgentResult, Assistant


def show(r: AgentResult, verbose: bool) -> None:
    print(r.answer or f"[no answer: {r.stop_reason}]")
    print(f"\n— release {r.release_id} · {len(r.tool_calls)} tool call(s) · stop {r.stop_reason}"
          + (f" · served by {r.served_by}" if r.served_by else ""))
    for w in r.warnings:
        print(f"⚠ {w}")
    if r.refusal:
        print(f"⚠ declined: {r.refusal}")
    if verbose:
        for t in r.tool_calls:
            print(f"  · {t.name} {json.dumps(t.input)}{'  [error]' if t.is_error else ''}")
        print(f"  usage {r.usage}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("question", nargs="?")
    ap.add_argument("--plant")
    ap.add_argument("--machine")
    ap.add_argument("--families", default="")
    ap.add_argument("--effort", default="medium", choices=["low", "medium", "high", "xhigh", "max"])
    ap.add_argument("--chat", action="store_true")
    ap.add_argument("-v", "--verbose", action="store_true")
    a = ap.parse_args()
    ctx = UserContext(user="cli", plant=a.plant, machine=a.machine, families=tuple(f for f in a.families.split(",") if f))
    bot = Assistant(KnowledgeService.load(), config=AgentConfig(effort=a.effort))
    if not a.chat:
        if not a.question:
            ap.error("give a question or use --chat")
        show(bot.ask(a.question, ctx), a.verbose)
        return 0
    history = None
    while True:
        try:
            q = input("\nyou> ").strip()
        except EOFError:
            return 0
        if q in ("", "exit", "quit"):
            return 0
        r = bot.ask(q, ctx, history)
        history = r.messages
        show(r, a.verbose)


if __name__ == "__main__":
    sys.exit(main())
