"""Knowledge base ingestion and retrieval (RAG) using ChromaDB."""

import hashlib
from pathlib import Path
from typing import Any

import chromadb
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings

from ..config.settings import settings

_SUPPORTED_EXTENSIONS = {
    ".txt", ".md", ".py", ".js", ".ts", ".json",
    ".pdf", ".csv", ".yaml", ".yml",
}


class KnowledgeBase:
    """Ingests documents and exposes a semantic search interface.

    Uses ChromaDB as the vector store and OpenAI Embeddings for encoding.
    Documents are split into overlapping chunks before indexing.
    """

    def __init__(self) -> None:
        """Initialise the knowledge base."""
        self._embeddings = OpenAIEmbeddings(
            model="text-embedding-3-small",
            api_key=settings.openai_api_key,
        )
        self._splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
        )
        self._client = chromadb.PersistentClient(path=settings.chroma_persist_dir)
        self._collection = self._client.get_or_create_collection(
            name=settings.chroma_collection_knowledge,
            metadata={"hnsw:space": "cosine"},
        )

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def ingest_file(self, file_path: str) -> int:
        """Load, split and index a single file into the knowledge base.

        Args:
            file_path: Path to the file to ingest.

        Returns:
            The number of chunks indexed.

        Raises:
            ValueError: If the file extension is not supported.
            FileNotFoundError: If the file does not exist.
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Fayl topilmadi: '{file_path}'")
        ext = path.suffix.lower()
        if ext not in _SUPPORTED_EXTENSIONS:
            raise ValueError(f"Qo'llab-quvvatlanmaydigan fayl turi: '{ext}'")

        docs = self._load_file(path)
        chunks = self._splitter.split_documents(docs)
        if not chunks:
            return 0

        ids: list[str] = []
        embeddings: list[list[float]] = []
        documents: list[str] = []
        metadatas: list[dict[str, Any]] = []

        for chunk in chunks:
            chunk_id = hashlib.sha256(
                (str(path) + chunk.page_content).encode()
            ).hexdigest()
            emb = self._embeddings.embed_query(chunk.page_content)
            ids.append(chunk_id)
            embeddings.append(emb)
            documents.append(chunk.page_content)
            metadatas.append({"source": str(path), "extension": ext})

        self._collection.upsert(
            ids=ids,
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas,
        )
        return len(chunks)

    def ingest_directory(self, directory_path: str) -> dict[str, int]:
        """Ingest all supported files from a directory.

        Args:
            directory_path: Path to the directory to scan.

        Returns:
            A dict mapping each file path to the number of chunks indexed.
        """
        base = Path(directory_path)
        results: dict[str, int] = {}
        for file_path in base.rglob("*"):
            if file_path.is_file() and file_path.suffix.lower() in _SUPPORTED_EXTENSIONS:
                try:
                    count = self.ingest_file(str(file_path))
                    results[str(file_path)] = count
                except Exception as exc:  # noqa: BLE001
                    results[str(file_path)] = -1
                    print(f"⚠️  '{file_path}' yuklanmadi: {exc}")
        return results

    def query(self, question: str, k: int = 5) -> list[dict[str, Any]]:
        """Run a semantic search over the knowledge base.

        Args:
            question: The query string.
            k: Number of results to return.

        Returns:
            A list of dicts with ``content``, ``source`` and ``score`` keys.
        """
        try:
            n = min(k, self._collection.count())
            if n == 0:
                return []
            embedding = self._embeddings.embed_query(question)
            results = self._collection.query(
                query_embeddings=[embedding],
                n_results=n,
                include=["documents", "metadatas", "distances"],
            )
            output: list[dict[str, Any]] = []
            for doc, meta, dist in zip(
                results["documents"][0],
                results["metadatas"][0],
                results["distances"][0],
            ):
                output.append(
                    {
                        "content": doc,
                        "source": meta.get("source", ""),
                        "score": round(1 - dist, 4),
                    }
                )
            return output
        except Exception:  # noqa: BLE001
            return []

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _load_file(self, path: Path) -> list:
        """Return LangChain Document objects for the given file."""
        ext = path.suffix.lower()
        if ext == ".pdf":
            from langchain_community.document_loaders import PyPDFLoader
            return PyPDFLoader(str(path)).load()
        if ext == ".md":
            from langchain_community.document_loaders import UnstructuredMarkdownLoader
            return UnstructuredMarkdownLoader(str(path)).load()
        from langchain_community.document_loaders import TextLoader
        return TextLoader(str(path), encoding="utf-8").load()
