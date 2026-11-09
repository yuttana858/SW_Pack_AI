#!/usr/bin/env python3
"""Build the knowledge index and release manifest.

  python -m kb.build [--out build/kb] [--embedder voyage]

Writes <out>/index.json and <out>/manifest.json. The manifest pins what an answer was built from:
git commit, corpus file hashes, data record versions, packcalc version, index format, embedder.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import subprocess
from collections import Counter
from pathlib import Path

import yaml

import packcalc

from .chunker import build_chunks
from .embedders import get_embedder
from .index import HybridIndex

ROOT = Path(__file__).resolve().parent.parent
INDEX_FORMAT = "swpack-kb-index/1"


def _git(*args: str) -> str | None:
    try:
        return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def manifest(chunks, embedder_name: str | None) -> dict:
    corpus = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()[:16]
              for p in sorted((ROOT / "corpus").rglob("*.md"))}
    records = {}
    for p in sorted((ROOT / "data").rglob("*.yaml")):
        if "_example" in p.parts or p.name.startswith("_"):
            continue
        r = yaml.safe_load(p.read_text())
        records[r["id"]] = {"version": r["version"], "status": r["status"], "scope": r["scope"]}
    body = {"corpus": corpus, "records": records, "packcalc": packcalc.__version__, "index_format": INDEX_FORMAT,
            "embedder": embedder_name}
    release_id = hashlib.sha256(json.dumps(body, sort_keys=True).encode()).hexdigest()[:12]
    return {"release_id": release_id, "built_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
            "git_commit": _git("rev-parse", "HEAD"), "git_dirty": bool(_git("status", "--porcelain")),
            "chunks": len(chunks), "chunk_kinds": dict(Counter(c.kind for c in chunks)),
            "record_status": dict(Counter(v["status"] for v in records.values())), **body}


def build(out: Path, embedder_name: str | None = None) -> dict:
    chunks = build_chunks(ROOT)
    embedder = get_embedder(embedder_name)
    ix = HybridIndex.build(chunks, embedder)
    out.mkdir(parents=True, exist_ok=True)
    ix.save(out / "index.json")
    m = manifest(chunks, embedder.name if embedder else None)
    (out / "manifest.json").write_text(json.dumps(m, indent=2))
    return m


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=ROOT / "build" / "kb")
    ap.add_argument("--embedder", default=None, help="none (default) | voyage | sentence-transformers")
    a = ap.parse_args()
    m = build(a.out, a.embedder)
    print(f"release {m['release_id']}: {m['chunks']} chunks {m['chunk_kinds']}, records {m['record_status']}, "
          f"embedder {m['embedder']} -> {a.out}")


if __name__ == "__main__":
    main()
