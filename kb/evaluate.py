#!/usr/bin/env python3
"""Retrieval evaluation: recall@k and MRR over an eval YAML.

  python -m kb.evaluate [--k 10] [--set evals/retrieval_seed.yaml] [--min-recall 0.9]
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

from .index import HybridIndex

ROOT = Path(__file__).resolve().parent.parent


def evaluate(index: HybridIndex, eval_path: Path, k: int = 10, embedder=None) -> dict:
    qs = yaml.safe_load(eval_path.read_text())["questions"]
    hits, rr, misses = 0, 0.0, []
    for item in qs:
        ids = [r["id"] for r in index.search(item["q"], k=k, embedder=embedder)]
        rank = next((i for i, cid in enumerate(ids) if any(cid.startswith(e) for e in item["expect"])), None)
        if rank is None:
            misses.append({"q": item["q"], "expect": item["expect"], "got": ids[:3]})
        else:
            hits += 1
            rr += 1 / (rank + 1)
    n = len(qs)
    return {"questions": n, "k": k, "recall_at_k": round(hits / n, 3), "mrr": round(rr / n, 3), "misses": misses}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--k", type=int, default=10)
    ap.add_argument("--set", type=Path, default=ROOT / "evals" / "retrieval_seed.yaml")
    ap.add_argument("--index", type=Path, default=ROOT / "build" / "kb" / "index.json")
    ap.add_argument("--min-recall", type=float, default=0.0)
    a = ap.parse_args()
    r = evaluate(HybridIndex.load(a.index), a.set, a.k)
    print(f"recall@{a.k} = {r['recall_at_k']}  MRR = {r['mrr']}  ({r['questions']} questions)")
    for m in r["misses"]:
        print(f"MISS  {m['q']}\n      expected {m['expect']}\n      got      {m['got']}")
    return 1 if r["recall_at_k"] < a.min_recall else 0


if __name__ == "__main__":
    sys.exit(main())
