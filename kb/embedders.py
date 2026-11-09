"""Dense embedders (optional). The index works with BM25 alone; plug one in for semantic recall.

- voyage: Voyage AI API (`pip install voyageai`, VOYAGE_API_KEY). Easiest to operate.
- sentence-transformers: self-hosted open model, intended for a Modal GPU function so documents
  never leave the company's Modal account. Model name via SWPACK_EMBED_MODEL.
Both are imported lazily so the core package has no heavy dependencies.
"""
from __future__ import annotations

import os
from typing import Sequence


class VoyageEmbedder:
    def __init__(self, model: str = os.environ.get("SWPACK_VOYAGE_MODEL", "voyage-3.5")):
        import voyageai  # noqa: PLC0415
        self.client, self.model, self.name = voyageai.Client(), model, f"voyage:{model}"

    def embed(self, texts: Sequence[str], kind: str) -> list[list[float]]:
        out = []
        for i in range(0, len(texts), 64):
            out += self.client.embed(list(texts[i:i + 64]), model=self.model, input_type=kind).embeddings
        return out


class SentenceTransformerEmbedder:
    def __init__(self, model: str = os.environ.get("SWPACK_EMBED_MODEL", "BAAI/bge-base-en-v1.5")):
        from sentence_transformers import SentenceTransformer  # noqa: PLC0415
        self.model, self.name = SentenceTransformer(model), f"st:{model}"

    def embed(self, texts: Sequence[str], kind: str) -> list[list[float]]:
        prefix = "Represent this sentence for searching relevant passages: " if kind == "query" else ""
        return self.model.encode([prefix + t for t in texts], normalize_embeddings=True).tolist()


def get_embedder(name: str | None):
    if not name or name == "none":
        return None
    if name == "voyage":
        return VoyageEmbedder()
    if name == "sentence-transformers":
        return SentenceTransformerEmbedder()
    raise ValueError(f"unknown embedder {name!r}")
