"""Split the corpus and data cards into retrieval chunks with metadata.

Corpus files split at `## ` headings (one chunk per section); a section longer than
MAX_CHARS splits again at `### `. Each chunk keeps its document title and heading path,
the citations it uses (resolved to source title/url), and the filter metadata:
tier, scope, material_family, confidence, status, domain, tags.
"""
from __future__ import annotations

import hashlib
import re
from dataclasses import asdict, dataclass, field
from pathlib import Path

import yaml

MAX_CHARS = 6000
FAMILY_FROM_APPLIES = {
    "corrugated": "corrugated", "folding-carton": "folding-carton", "cushioning": "foam", "pallet": "multi",
    "rigid": "rigid-box", "flexible": "flexible", "honeycomb": "honeycomb", "paper-tube": "paper-tube",
    "molded-pulp": "molded-pulp", "formed-fibre": "formed-fibre", "solid-board": "solid-board",
}
SKIP = {"README.md", "INDEX.md"}


@dataclass
class Chunk:
    id: str
    doc_id: str
    kind: str                      # corpus | card
    title: str                     # document title
    heading: str                   # section heading path, "A > B"
    text: str
    path: str
    tier: str = "L0"
    scope: str = "global"
    material_family: list[str] = field(default_factory=list)
    confidence: str = ""
    status: str = ""
    domain: str = ""
    tags: list[str] = field(default_factory=list)
    citations: list[dict] = field(default_factory=list)
    record_id: str | None = None
    record_version: str | None = None

    def to_dict(self) -> dict:
        return asdict(self)


def _slug(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:60]


def _split_front_matter(text: str) -> tuple[dict, str]:
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    return yaml.safe_load(text[3:end]) or {}, text[end + 4:]


def _sections(body: str, level: str) -> list[tuple[str, str]]:
    """Return (heading, text) pairs split at headings of `level` ('## ' or '### ')."""
    pat = re.compile(rf"^{re.escape(level)}(.+)$", re.M)
    hits = list(pat.finditer(body))
    out = []
    if hits and body[: hits[0].start()].strip():
        out.append(("", body[: hits[0].start()].strip()))
    for i, m in enumerate(hits):
        end = hits[i + 1].start() if i + 1 < len(hits) else len(body)
        out.append((m.group(1).strip(), body[m.start():end].strip()))
    return out or [("", body.strip())]


def _citations(text: str, sources: dict[str, dict]) -> list[dict]:
    ids = []
    for m in re.finditer(r"\[([^\[\]]*\bS\d+[^\[\]]*)\]", text):
        for sid in re.findall(r"S\d+", m.group(1)):
            if sid not in ids:
                ids.append(sid)
    return [{"id": s, "title": sources[s].get("title", ""), "url": sources[s].get("url", ""),
             "publisher": sources[s].get("publisher", "")} for s in ids if s in sources]


def _families(fm: dict) -> list[str]:
    if fm.get("material_family"):
        v = fm["material_family"]
        return v if isinstance(v, list) else [v]
    fam = [FAMILY_FROM_APPLIES.get(a, a) for a in fm.get("applies_to") or []]
    return sorted(set(fam)) or ["multi"]


def chunk_corpus_file(path: Path, root: Path) -> list[Chunk]:
    fm, body = _split_front_matter(path.read_text(encoding="utf-8"))
    sources = {s["id"]: s for s in fm.get("sources") or [] if isinstance(s, dict) and "id" in s}
    doc_id, title = fm.get("id", path.stem), fm.get("title", path.stem)
    meta = dict(tier="L0", scope="global", material_family=_families(fm), confidence=fm.get("confidence", ""),
                status=fm.get("status", ""), domain=fm.get("domain", ""), tags=list(fm.get("tags") or []))
    chunks, seen = [], set()
    for heading, text in _sections(body, "## "):
        if not text or heading.lower().startswith("research log"):
            continue                                  # research logs are for reviewers, not answers
        parts = [(heading, text)]
        if len(text) > MAX_CHARS:
            subs = _sections(text, "### ")
            parts = [(heading if not h else f"{heading} > {h}", t) for h, t in subs]
        for h, t in parts:
            cid = f"{doc_id}#{_slug(h) or 'intro'}"
            if cid in seen:
                cid += "-" + hashlib.sha1(t.encode()).hexdigest()[:6]
            seen.add(cid)
            chunks.append(Chunk(id=cid, doc_id=doc_id, kind="corpus", title=title, heading=h or title, text=t,
                                path=str(path.relative_to(root)), citations=_citations(t, sources), **meta))
    return chunks


def chunk_card(path: Path, root: Path) -> Chunk:
    fm, body = _split_front_matter(path.read_text(encoding="utf-8"))
    title = next((l[2:].strip() for l in body.splitlines() if l.startswith("# ")), fm["record_id"])
    return Chunk(id=fm["id"], doc_id=fm["record_id"], kind="card", title=title, heading=title, text=body.strip(),
                 path=str(path.relative_to(root)), tier=fm["tier"], scope=fm["scope"],
                 material_family=[fm.get("material_family") or "corrugated"], confidence=fm["confidence"],
                 status=fm["status"], domain=fm["record_type"], tags=[fm["record_type"]],
                 citations=[{"id": r, "title": r, "url": "", "publisher": ""} for r in fm.get("source_refs") or []],
                 record_id=fm["record_id"], record_version=fm["record_version"])


def build_chunks(root: Path) -> list[Chunk]:
    chunks = []
    for p in sorted((root / "corpus").rglob("*.md")):
        if p.name not in SKIP:
            chunks += chunk_corpus_file(p, root)
    for p in sorted((root / "rag" / "cards").glob("*.md")):
        chunks.append(chunk_card(p, root))
    return chunks
