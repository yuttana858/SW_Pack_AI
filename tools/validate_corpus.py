#!/usr/bin/env python3
"""Validate corpus/ Markdown files against the schema in corpus/README.md.

Checks per file:
  - YAML front-matter present with required keys and allowed enum values
  - unique `id` across the corpus
  - every [S#] tag used in the body is declared in `sources`
  - every declared source has a title and url (or is marked as a standard)
  - at least one `##` section (chunkable)
Warnings (non-fatal): declared sources never cited, VERIFY markers count.

Usage: python tools/validate_corpus.py [corpus_dir]
Exit code 1 if any error.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

REQUIRED = ["id", "title", "domain", "tags", "applies_to", "confidence", "status", "last_reviewed", "sources"]
CONFIDENCE = {"reference", "industry-typical", "derived", "supplier-certified"}
STATUS = {"draft", "reviewed", "approved"}
CITE = re.compile(r"\[(S\d+)(?:[,;]\s*S?\d+)*\]")
CITE_ALL = re.compile(r"S\d+")


def split_front_matter(text: str):
    if not text.startswith("---"):
        return None, text
    end = text.find("\n---", 3)
    if end == -1:
        return None, text
    return yaml.safe_load(text[3:end]), text[end + 4 :]


def cited_ids(body: str) -> set[str]:
    ids: set[str] = set()
    for m in re.finditer(r"\[([^\[\]]*\bS\d+[^\[\]]*)\]", body):
        ids.update(CITE_ALL.findall(m.group(1)))
    return ids


def main(root: Path) -> int:
    errors, warnings, seen = [], [], {}
    files = sorted(p for p in root.rglob("*.md") if p.name not in ("README.md", "INDEX.md"))
    for path in files:
        rel = path.relative_to(root)
        try:
            fm, body = split_front_matter(path.read_text(encoding="utf-8"))
        except yaml.YAMLError as e:
            errors.append(f"{rel}: invalid YAML front-matter ({e})")
            continue
        if not isinstance(fm, dict):
            errors.append(f"{rel}: missing front-matter")
            continue
        for key in REQUIRED:
            if key not in fm:
                errors.append(f"{rel}: missing key '{key}'")
        if fm.get("confidence") not in CONFIDENCE:
            errors.append(f"{rel}: confidence '{fm.get('confidence')}' not in {sorted(CONFIDENCE)}")
        if fm.get("status") not in STATUS:
            errors.append(f"{rel}: status '{fm.get('status')}' not in {sorted(STATUS)}")
        if fm.get("confidence") == "supplier-certified" and "company" not in rel.parts:
            errors.append(f"{rel}: supplier-certified content must live under company/")
        fid = fm.get("id")
        if fid in seen:
            errors.append(f"{rel}: duplicate id '{fid}' (also {seen[fid]})")
        seen[fid] = rel

        declared = {}
        for s in fm.get("sources") or []:
            if not isinstance(s, dict) or "id" not in s:
                errors.append(f"{rel}: malformed source entry {s!r}")
                continue
            declared[s["id"]] = s
            if not s.get("title"):
                errors.append(f"{rel}: source {s['id']} has no title")
            if not s.get("url") and not s.get("standard"):
                warnings.append(f"{rel}: source {s['id']} has no url")
        used = cited_ids(body)
        for missing in sorted(used - declared.keys(), key=lambda x: int(x[1:])):
            errors.append(f"{rel}: cites {missing} but it is not declared in sources")
        for unused in sorted(declared.keys() - used, key=lambda x: int(x[1:]) if x[1:].isdigit() else 0):
            warnings.append(f"{rel}: source {unused} declared but never cited")
        if not re.search(r"^## ", body, re.M):
            errors.append(f"{rel}: no '## ' sections to chunk on")
        n_verify = body.count("VERIFY")
        if n_verify:
            warnings.append(f"{rel}: {n_verify} VERIFY marker(s) need engineer review")

    print(f"Checked {len(files)} files: {len(errors)} error(s), {len(warnings)} warning(s)")
    for e in errors:
        print("ERROR  ", e)
    for w in warnings:
        print("WARN   ", w)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(Path(sys.argv[1] if len(sys.argv) > 1 else "corpus")))
