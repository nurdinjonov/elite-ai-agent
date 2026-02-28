"""Long-term vector memory backed by ChromaDB and OpenAI Embeddings."""

import uuid
from datetime import datetime, timezone
from typing import Any

import chromadb
from langchain_openai import OpenAIEmbeddings

from ..config.settings import settings


class LongTermMemory:
    """Persists and retrieves memories using ChromaDB vector store.

    Each memory is stored with a UUID, timestamp and optional metadata so
    that the agent can perform semantic recall across sessions.
    """

    def __init__(self) -> None:
        """Initialise the ChromaDB client and OpenAI Embeddings."""
        self._embeddings = OpenAIEmbeddings(
            model="text-embedding-3-small",
            api_key=settings.openai_api_key,
        )
        self._client = chromadb.PersistentClient(path=settings.chroma_persist_dir)
        self._collection = self._client.get_or_create_collection(
            name=settings.chroma_collection_memory,
            metadata={"hnsw:space": "cosine"},
        )

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def store_memory(
        self,
        content: str,
        memory_type: str = "general",
        metadata: dict[str, Any] | None = None,
    ) -> str:
        """Persist a memory entry in the vector store.

        Args:
            content: The text content to store.
            memory_type: A label categorising the memory (e.g. "fact", "task").
            metadata: Optional extra key-value pairs to attach to the entry.

        Returns:
            The UUID assigned to the stored memory.
        """
        memory_id = str(uuid.uuid4())
        combined_meta: dict[str, Any] = {
            "memory_type": memory_type,
            "timestamp": datetime.now(tz=timezone.utc).isoformat(),
        }
        if metadata:
            combined_meta.update(metadata)

        embedding = self._embeddings.embed_query(content)
        self._collection.add(
            ids=[memory_id],
            embeddings=[embedding],
            documents=[content],
            metadatas=[combined_meta],
        )
        return memory_id

    def recall(self, query: str, k: int = 5) -> list[dict[str, Any]]:
        """Retrieve the *k* most semantically similar memories.

        Args:
            query: The search query string.
            k: Number of results to return.

        Returns:
            A list of dicts with keys ``content``, ``metadata`` and ``score``.
        """
        try:
            embedding = self._embeddings.embed_query(query)
            results = self._collection.query(
                query_embeddings=[embedding],
                n_results=min(k, self._collection.count()),
                include=["documents", "metadatas", "distances"],
            )
            memories: list[dict[str, Any]] = []
            for doc, meta, dist in zip(
                results["documents"][0],
                results["metadatas"][0],
                results["distances"][0],
            ):
                memories.append(
                    {
                        "content": doc,
                        "metadata": meta,
                        "score": round(1 - dist, 4),
                    }
                )
            return memories
        except Exception:
            return []

    def recall_as_text(self, query: str, k: int = 5) -> str:
        """Return recalled memories formatted as a human-readable string.

        Args:
            query: The search query string.
            k: Number of results to return.

        Returns:
            A formatted multi-line string, or an empty string if nothing found.
        """
        memories = self.recall(query, k)
        if not memories:
            return ""
        lines: list[str] = []
        for i, mem in enumerate(memories, start=1):
            ts = mem["metadata"].get("timestamp", "")
            lines.append(f"{i}. [{ts}] {mem['content']} (score: {mem['score']})")
        return "\n".join(lines)
