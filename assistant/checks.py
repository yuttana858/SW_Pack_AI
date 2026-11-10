"""Post-answer grounding checks. They never change the answer; they produce warnings the UI shows
and the eval scores. Two checks:

1. Citations: every [id] cited must have been retrieved (kb_search/kb_read/kb_resolve) or be a
   formula id returned by a calculator in this turn.
2. Numbers: every number with engineering precision in the answer must appear (within 0.5 %)
   in some tool output or retrieved text, otherwise it may have come from the model's memory.
"""
from __future__ import annotations

import json
import re
from typing import Iterable

from .tools import ToolLog

CITE = re.compile(r"\[((?:kb|card|lib)\.[A-Za-z0-9_.:#/\-]+)\]")
NUM = re.compile(r"(?<![\w.])(-?\d{1,3}(?:,\d{3})+(?:\.\d+)?|-?\d+\.\d+|-?\d{2,})(?![\w.])")
IGNORE_INTS = set(range(0, 13))         # small counts ("2 pallets", "step 3") are not engineering values


def _walk(obj, out: list[str]) -> None:
    if isinstance(obj, dict):
        for v in obj.values():
            _walk(v, out)
    elif isinstance(obj, list):
        for v in obj:
            _walk(v, out)
    elif obj is not None:
        out.append(str(obj))


def evidence(log: Iterable[ToolLog]) -> tuple[set[str], list[float], str]:
    ids: set[str] = set()
    texts: list[str] = []
    for t in log:
        res = t.output.get("result", t.output) if isinstance(t.output, dict) else t.output
        items = res if isinstance(res, list) else [res]
        for it in items:
            if isinstance(it, dict):
                for key in ("id", "record_id", "formula"):
                    if isinstance(it.get(key), str):
                        ids.add(it[key])
                if isinstance(it.get("record"), dict) and it["record"].get("id"):
                    ids.add(it["record"]["id"])
        _walk(t.output, texts)
        texts.append(json.dumps(t.input))
    blob = "\n".join(texts)
    nums = []
    for m in NUM.finditer(blob):
        try:
            nums.append(float(m.group(1).replace(",", "")))
        except ValueError:
            pass
    nums += [float(x) for x in re.findall(r"-?\d+\.\d+|-?\d+", blob) if len(x) < 20]
    return ids, nums, blob


def check_answer(text: str, log: list[ToolLog]) -> list[str]:
    ids, nums, _ = evidence(log)
    warnings = []
    for cid in dict.fromkeys(CITE.findall(text)):
        base = cid.split("#")[0]
        card_like = {cid, cid.removeprefix("card."), f"card.{cid}"}
        if not (card_like & ids or any(i.startswith(cid) or cid.startswith(i) for i in ids if "#" in i or i.startswith("lib."))
                or (base.startswith("kb.") and any(i.startswith(base) for i in ids) and "#" not in cid)):
            warnings.append(f"cited {cid} but it was not retrieved in this answer")
    for m in NUM.finditer(CITE.sub("", text)):
        raw = m.group(1).replace(",", "")
        try:
            v = float(raw)
        except ValueError:
            continue
        if v.is_integer() and int(v) in IGNORE_INTS:
            continue
        if not any(abs(v - n) <= max(abs(n) * 0.005, 0.005) for n in nums):
            warnings.append(f"number {m.group(1)} is not traceable to a tool result or retrieved text")
    return warnings
