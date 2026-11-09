"""Hybrid retrieval index: BM25 keyword search + optional dense embeddings, fused with RRF.

BM25 runs everywhere (no model download) and is strong on packaging codes and numbers:
FEFCO 0201, TAPPI T 839, ISO 3037, 32 ECT, BC flute. A dense embedder (Voyage API or a
self-hosted model on a Modal GPU) can be plugged in via the `Embedder` protocol; results
are fused with reciprocal-rank fusion. Filters apply before ranking.
"""
from __future__ import annotations

import json
import math
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Iterable, Protocol, Sequence

from .chunker import Chunk

STOP = set("""a an and are as at be by for from has have in into is it its of on or that the this to was were will with
what which how why when where who does do can should would could i we you your our their there than then them these those
not no but if so such""".split())
CODE_JOIN = [  # normalise common code spellings so "T839", "T 839" and "t-839" match
    (re.compile(r"\b(tappi\s*)?t[\s-]?(\d{3})\b", re.I), r"t\2"),
    (re.compile(r"\biso[\s-]?(\d{3,5})\b", re.I), r"iso\1"),
    (re.compile(r"\bastm[\s-]?d[\s-]?(\d{3,4})\b", re.I), r"d\1"),
    (re.compile(r"\bd[\s-](\d{3,4})\b", re.I), r"d\1"),
    (re.compile(r"\bista[\s-]?(\d[a-z]?)\b", re.I), r"ista\1"),
    (re.compile(r"\b(\d{2,3})[\s-]?ect\b", re.I), r"\1ect"),
    (re.compile(r"\bfefco[\s-]?(\d{4})\b", re.I), r"\1"),
]


def tokenize(text: str) -> list[str]:
    t = text.lower()
    for pat, rep in CODE_JOIN:
        t = pat.sub(rep, t)
    toks = re.findall(r"[a-z0-9]+(?:\.[0-9]+)?", t)
    return [w for w in toks if w not in STOP and (len(w) > 1 or w.isdigit())]


class Embedder(Protocol):
    name: str

    def embed(self, texts: Sequence[str], kind: str) -> list[list[float]]: ...   # kind: "document" | "query"


def _matches(c: dict, filters: dict | None) -> bool:
    if not filters:
        return True
    for key, want in filters.items():
        if want in (None, [], ""):
            continue
        have = c.get(key)
        want_set = set(want) if isinstance(want, (list, tuple, set)) else {want}
        have_set = set(have) if isinstance(have, list) else {have}
        if key == "material_family":
            have_set |= {"multi"} if "multi" in have_set else set()
            if not (have_set & want_set or "multi" in have_set):
                return False
        elif not have_set & want_set:
            return False
    return True


class HybridIndex:
    K1, B = 1.4, 0.72
    FIELD_BOOST = {"title": 2, "heading": 3}

    def __init__(self, chunks: list[dict], embedder_name: str | None = None, vectors: list[list[float]] | None = None):
        self.chunks = chunks
        self.embedder_name, self.vectors = embedder_name, vectors
        self.tf: list[Counter] = []
        df: Counter = Counter()
        for c in chunks:
            toks = tokenize(c["text"]) + tokenize(c["title"]) * self.FIELD_BOOST["title"] \
                + tokenize(c["heading"]) * self.FIELD_BOOST["heading"] + tokenize(" ".join(c.get("tags") or []))
            tf = Counter(toks)
            self.tf.append(tf)
            df.update(tf.keys())
        n = len(chunks)
        self.idf = {t: math.log(1 + (n - d + 0.5) / (d + 0.5)) for t, d in df.items()}
        self.lengths = [sum(tf.values()) for tf in self.tf]
        self.avgdl = sum(self.lengths) / max(n, 1)
        self.by_id = {c["id"]: i for i, c in enumerate(chunks)}

    @classmethod
    def build(cls, chunks: Iterable[Chunk], embedder: Embedder | None = None) -> "HybridIndex":
        dicts = [c.to_dict() for c in chunks]
        vecs = embedder.embed([f"{c['title']} — {c['heading']}\n{c['text']}" for c in dicts], "document") if embedder else None
        return cls(dicts, embedder.name if embedder else None, vecs)

    # --- persistence ---------------------------------------------------------------
    def save(self, path: Path) -> None:
        path.write_text(json.dumps({"chunks": self.chunks, "embedder": self.embedder_name, "vectors": self.vectors}))

    @classmethod
    def load(cls, path: Path) -> "HybridIndex":
        d = json.loads(path.read_text())
        return cls(d["chunks"], d.get("embedder"), d.get("vectors"))

    # --- search --------------------------------------------------------------------
    def _bm25(self, q: list[str], allowed: set[int]) -> list[tuple[int, float]]:
        scores = defaultdict(float)
        for t in set(q):
            idf = self.idf.get(t)
            if idf is None:
                continue
            for i in allowed:
                f = self.tf[i].get(t)
                if f:
                    scores[i] += idf * f * (self.K1 + 1) / (f + self.K1 * (1 - self.B + self.B * self.lengths[i] / self.avgdl))
        return sorted(scores.items(), key=lambda x: -x[1])

    def _dense(self, qv: list[float], allowed: set[int]) -> list[tuple[int, float]]:
        def cos(a, b):
            na, nb = math.sqrt(sum(x * x for x in a)), math.sqrt(sum(x * x for x in b))
            return sum(x * y for x, y in zip(a, b)) / (na * nb or 1)
        return sorted(((i, cos(qv, self.vectors[i])) for i in allowed), key=lambda x: -x[1])

    def search(self, query: str, k: int = 8, filters: dict | None = None, embedder: Embedder | None = None,
               rrf_k: int = 60) -> list[dict]:
        allowed = {i for i, c in enumerate(self.chunks) if _matches(c, filters)}
        ranked = self._bm25(tokenize(query), allowed)
        if embedder and self.vectors and embedder.name == self.embedder_name:
            dense = self._dense(embedder.embed([query], "query")[0], allowed)[: max(50, k * 5)]
            fused = defaultdict(float)
            for lst in (ranked[: max(50, k * 5)], dense):
                for rank, (i, _) in enumerate(lst):
                    fused[i] += 1 / (rrf_k + rank + 1)
            ranked = sorted(fused.items(), key=lambda x: -x[1])
        out = []
        for i, score in ranked[:k]:
            c = self.chunks[i]
            out.append({"id": c["id"], "score": round(score, 4), "kind": c["kind"], "title": c["title"],
                        "heading": c["heading"], "confidence": c["confidence"], "status": c["status"],
                        "tier": c["tier"], "scope": c["scope"], "material_family": c["material_family"],
                        "path": c["path"], "snippet": c["text"][:400]})
        return out

    def read(self, chunk_id: str) -> dict | None:
        i = self.by_id.get(chunk_id)
        return None if i is None else self.chunks[i]
