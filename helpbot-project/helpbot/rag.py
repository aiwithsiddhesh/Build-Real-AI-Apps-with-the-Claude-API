from __future__ import annotations

import logging
import os
from pathlib import Path
from typing import TYPE_CHECKING

import numpy as np
from numpy.typing import NDArray

if TYPE_CHECKING:
    pass

log = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Chunking
# ---------------------------------------------------------------------------
def chunk_by_section(text: str) -> list[str]:
    """Split a markdown document at every H2 header (## ...)."""
    raw = text.split("\n## ")
    chunks: list[str] = []
    for i, section in enumerate(raw):
        section = section.strip()
        if not section:
            continue
        # The first split chunk may already start with ##; the rest don't.
        if i > 0:
            section = "## " + section
        chunks.append(section)
    return chunks


# ---------------------------------------------------------------------------
# Vector store — cosine similarity
# ---------------------------------------------------------------------------
class VectorStore:
    def __init__(self) -> None:
        self._vectors: list[NDArray[np.float32]] = []
        self._docs: list[str] = []

    def add(self, vector: list[float], text: str) -> None:
        self._vectors.append(np.array(vector, dtype=np.float32))
        self._docs.append(text)

    def search(self, query_vector: list[float], top_k: int = 3) -> list[str]:
        if not self._vectors:
            return []
        q = np.array(query_vector, dtype=np.float32)
        q_norm = np.linalg.norm(q)
        scores = [
            float(np.dot(q, v) / (q_norm * np.linalg.norm(v) + 1e-10))
            for v in self._vectors
        ]
        top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)
        return [self._docs[i] for i in top_indices[:top_k]]


# ---------------------------------------------------------------------------
# BM25 keyword store
# ---------------------------------------------------------------------------
class BM25Store:
    def __init__(self) -> None:
        self._docs: list[str] = []
        self._bm25 = None

    def index(self, docs: list[str]) -> None:
        from rank_bm25 import BM25Okapi  # optional dep, imported lazily

        self._docs = docs
        self._bm25 = BM25Okapi([doc.lower().split() for doc in docs])

    def search(self, query: str, top_k: int = 3) -> list[str]:
        if self._bm25 is None:
            return []
        scores: NDArray[np.float32] = self._bm25.get_scores(query.lower().split())
        top_indices = scores.argsort()[-top_k:][::-1]
        return [self._docs[i] for i in top_indices]


# ---------------------------------------------------------------------------
# RAG index — owns both stores, built once at startup
# ---------------------------------------------------------------------------
class RAGIndex:
    def __init__(self) -> None:
        self._vector_store = VectorStore()
        self._bm25_store = BM25Store()
        self._ready = False

    @property
    def ready(self) -> bool:
        return self._ready

    def build(self, policy_path: str | Path, voyage_api_key: str) -> None:
        path = Path(policy_path)
        if not path.exists():
            log.warning("Policy file not found at '%s'. RAG disabled.", path)
            return

        try:
            import voyageai  # optional dep

            client = voyageai.Client(api_key=voyage_api_key)
            chunks = chunk_by_section(path.read_text(encoding="utf-8"))
            if not chunks:
                log.warning("Policy file produced no chunks. RAG disabled.")
                return

            log.info("Embedding %d policy chunks via Voyage AI…", len(chunks))
            embeddings: list[list[float]] = client.embed(
                texts=chunks, model="voyage-3"
            ).embeddings

            for chunk, vector in zip(chunks, embeddings):
                self._vector_store.add(vector, chunk)
            self._bm25_store.index(chunks)

            self._ready = True
            log.info("RAG index ready (%d chunks).", len(chunks))

        except Exception:
            log.exception("Failed to build RAG index. RAG disabled.")

    def search(self, query: str, voyage_api_key: str, top_k: int = 2) -> list[str]:
        if not self._ready:
            return []

        try:
            import voyageai

            client = voyageai.Client(api_key=voyage_api_key)
            query_vector: list[float] = client.embed(
                texts=[query], model="voyage-3"
            ).embeddings[0]

            semantic = self._vector_store.search(query_vector, top_k=top_k)
            keyword = self._bm25_store.search(query, top_k=top_k)

            # Reciprocal Rank Fusion
            scores: dict[str, float] = {}
            for rank, doc in enumerate(semantic):
                scores[doc] = scores.get(doc, 0.0) + 1.0 / (rank + 1)
            for rank, doc in enumerate(keyword):
                scores[doc] = scores.get(doc, 0.0) + 1.0 / (rank + 1)

            return sorted(scores, key=scores.__getitem__, reverse=True)[:top_k]

        except Exception:
            log.exception("RAG search failed.")
            return []
