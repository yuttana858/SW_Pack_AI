#!/usr/bin/env python3
"""Render data/ records into Markdown "data cards" for the RAG index (rag/cards/).

Numbers in cards come only from the structured records, so the assistant's retrieved text
can never drift from the data the calculators and Auto3D use. Cards are generated: never
hand-edit them. CI runs `--check` to fail when cards are stale.

Usage:
  python tools/generate_cards.py            # (re)write rag/cards/
  python tools/generate_cards.py --check    # exit 1 if any card is missing or stale
"""
from __future__ import annotations

import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
DATA, OUT = ROOT / "data", ROOT / "rag" / "cards"
SCOPE_TEXT = {"global": "all plants", "company": "company-wide"}


def fmt(v) -> str:
    if v is None:
        return ""
    if isinstance(v, float):
        return f"{v:g}"
    if isinstance(v, (list, tuple)):
        return " – ".join(fmt(x) for x in v) if len(v) == 2 and all(isinstance(x, (int, float)) for x in v) else ", ".join(fmt(x) for x in v)
    if isinstance(v, dict):
        return "; ".join(f"{k}: {fmt(x)}" for k, x in v.items())
    return str(v).replace("|", "/").replace("\n", " ")


def table(rows: list[dict], skip=("cite",)) -> list[str]:
    if not rows:
        return []
    cols = [c for c in dict.fromkeys(k for r in rows for k in r) if c not in skip]
    out = ["| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
    out += ["| " + " | ".join(fmt(r.get(c)) for c in cols) + " |" for r in rows]
    return out


def body(rec: dict) -> list[str]:
    t = rec["type"]
    if t == "formula":
        f = rec["formula"]
        lines = ["```", f["expression"], "```", ""]
        lines += table([{"symbol": v["symbol"], "meaning": v["meaning"], "SI": v["si_unit"], "US": v.get("us_unit", "")} for v in f["variables"]])
        lines += ["", f"**Valid for:** {f.get('validity', '')}", "", f"**Limitations:** {f.get('limitations', '')}",
                  "", f"**Calculator:** `{f['implementation']}` (tested against the corpus worked examples). "
                      "Always compute with the calculator rather than by hand."]
        return lines
    if t == "allowance_table":
        return [f"Convention: `{rec['convention']}` (inside = score − k_s·t; outside = score + (k_o − k_s)·t, per [L, W, H]).", ""] + table(rec["rows"])
    if t in ("factor_set",):
        return [f"Kind: **{rec['factors']['kind']}**", ""] + table(rec["factors"]["rows"])
    if t == "grade_table":
        return [f"System: **{rec['table']['system']}**", ""] + table(rec["table"]["rows"])
    if t == "tolerance_spec":
        tol = rec["tolerances"]
        return [f"Applies to: {tol['applies_to']}. Dimension basis: {tol.get('basis', 'n/a')}.", ""] + table(tol["rows"])
    if t in ("flute_profile", "box_style", "board_material", "machine_spec", "plant", "test_result"):
        key = {"flute_profile": "flute", "box_style": "style", "board_material": "board", "machine_spec": "machine",
               "plant": "plant", "test_result": "test"}[t]
        payload = dict(rec[key])
        lines = table([{"field": k, "value": v} for k, v in payload.items() if k != "cite"])
        if t == "board_material" and rec.get("auto3d"):
            lines += ["", "Auto3D board record:", ""] + table([{"field": k, "value": v} for k, v in rec["auto3d"].items()])
        return lines
    return ["```yaml", yaml.safe_dump(rec, sort_keys=False, allow_unicode=True).strip(), "```"]


def render(rec: dict, path: Path) -> str:
    scope = rec["scope"]
    where = SCOPE_TEXT.get(scope, scope.replace("plant:", "plant ").replace("machine:", "machine "))
    fm = {
        "id": f"card.{rec['id']}", "record_id": rec["id"], "record_type": rec["type"], "record_version": rec["version"],
        "tier": rec["tier"], "scope": scope, "status": rec["status"], "confidence": rec["confidence"],
        "source_refs": rec.get("provenance", {}).get("sources", []), "generated_from": str(path.relative_to(ROOT)),
    }
    lines = ["---", yaml.safe_dump(fm, sort_keys=False, allow_unicode=True).strip(), "---", "",
             f"# {rec.get('title') or rec['id']}", "",
             f"> Data card generated from `{fm['generated_from']}` v{rec['version']}. Tier {rec['tier']}, applies to {where}. "
             f"Status **{rec['status']}**, confidence **{rec['confidence']}**. Do not edit; change the record instead.", ""]
    if rec.get("notes"):
        lines += [f"**Notes:** {fmt(rec['notes'])}", ""]
    lines += ["## Values", ""] + body(rec)
    refs = fm["source_refs"]
    if refs:
        lines += ["", "## Sources", ""] + [f"- `{r}`" for r in refs]
    return "\n".join(lines) + "\n"


def main(check: bool) -> int:
    expected = {}
    for path in sorted(DATA.rglob("*.yaml")):
        if "_example" in path.parts or path.name.startswith("_"):
            continue
        rec = yaml.safe_load(path.read_text())
        expected[OUT / f"{rec['id']}.md"] = render(rec, path)
    stale = [p for p, txt in expected.items() if not p.exists() or p.read_text() != txt]
    orphans = [p for p in OUT.glob("*.md") if p not in expected] if OUT.exists() else []
    if check:
        for p in stale:
            print("STALE  ", p.relative_to(ROOT))
        for p in orphans:
            print("ORPHAN ", p.relative_to(ROOT))
        print(f"{len(expected)} cards: {len(stale)} stale, {len(orphans)} orphan")
        return 1 if stale or orphans else 0
    OUT.mkdir(parents=True, exist_ok=True)
    for p, txt in expected.items():
        p.write_text(txt)
    for p in orphans:
        p.unlink()
    print(f"wrote {len(expected)} cards to {OUT.relative_to(ROOT)} ({len(orphans)} orphans removed)")
    return 0


if __name__ == "__main__":
    sys.exit(main("--check" in sys.argv))
