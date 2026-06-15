"""Document loading + ChromaDB-backed persistent indexing pipeline."""
from __future__ import annotations

import logging
from dataclasses import dataclass, field
from pathlib import Path

import chromadb
from llama_index.core import (
    SimpleDirectoryReader,
    StorageContext,
    VectorStoreIndex,
)
from llama_index.core.node_parser import SentenceSplitter
from llama_index.vector_stores.chroma import ChromaVectorStore

from .config import Settings, get_settings
from .models import configure_llama_settings

log = logging.getLogger(__name__)

SUPPORTED_EXTENSIONS: frozenset[str] = frozenset(
    {".pdf", ".md", ".markdown", ".txt", ".docx"}
)


@dataclass
class IndexBuildReport:
    files_indexed: int = 0
    nodes_created: int = 0
    files: list[str] = field(default_factory=list)
    skipped: list[str] = field(default_factory=list)


def _chroma_client(settings: Settings) -> chromadb.PersistentClient:
    return chromadb.PersistentClient(path=str(settings.storage_dir))


def _filter_supported(data_dir: Path) -> tuple[list[Path], list[str]]:
    supported: list[Path] = []
    skipped: list[str] = []
    for p in sorted(data_dir.rglob("*")):
        if not p.is_file() or p.name.startswith("."):
            continue
        if p.name == "_sources_index.json":
            continue
        if p.suffix.lower() in SUPPORTED_EXTENSIONS:
            supported.append(p)
        else:
            skipped.append(str(p.relative_to(data_dir)))
    return supported, skipped


def _drop_collection(client: chromadb.PersistentClient, name: str) -> None:
    try:
        client.delete_collection(name)
        log.info("Deleted existing collection '%s'", name)
    except Exception as exc:  # chromadb raises NotFoundError / ValueError across versions
        log.debug("delete_collection('%s') skipped: %s", name, exc)


def build_index(rebuild: bool = False) -> IndexBuildReport:
    """Build (or rebuild) the persistent ChromaDB-backed vector index."""
    settings = get_settings()
    configure_llama_settings()

    files, skipped = _filter_supported(settings.data_dir)
    report = IndexBuildReport(skipped=skipped)
    if not files:
        log.warning("No supported files found in %s", settings.data_dir)
        return report

    client = _chroma_client(settings)
    if rebuild:
        _drop_collection(client, settings.collection_name)

    collection = client.get_or_create_collection(settings.collection_name)
    vector_store = ChromaVectorStore(chroma_collection=collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    log.info("Loading %d file(s) from %s", len(files), settings.data_dir)
    reader = SimpleDirectoryReader(
        input_files=[str(p) for p in files],
        filename_as_id=True,
    )
    documents = reader.load_data()

    splitter = SentenceSplitter(
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
    )
    nodes = splitter.get_nodes_from_documents(documents)
    log.info("Created %d chunk node(s); embedding…", len(nodes))

    VectorStoreIndex(
        nodes=nodes,
        storage_context=storage_context,
        show_progress=True,
    )

    report.files_indexed = len({d.metadata.get("file_name") for d in documents if d.metadata.get("file_name")})
    if report.files_indexed == 0:
        report.files_indexed = len(files)
    report.nodes_created = len(nodes)
    report.files = [str(p.relative_to(settings.data_dir)) for p in files]
    log.info("Indexing complete: %d files / %d chunks", report.files_indexed, report.nodes_created)
    return report


def load_index() -> VectorStoreIndex | None:
    """Load the persistent index if it exists and is non-empty, else None."""
    settings = get_settings()
    configure_llama_settings()

    client = _chroma_client(settings)
    try:
        collection = client.get_collection(settings.collection_name)
    except Exception:
        return None
    if collection.count() == 0:
        return None
    vector_store = ChromaVectorStore(chroma_collection=collection)
    return VectorStoreIndex.from_vector_store(vector_store=vector_store)


def index_stats() -> dict[str, object]:
    """Return a lightweight snapshot of the current index."""
    settings = get_settings()
    client = _chroma_client(settings)
    try:
        collection = client.get_collection(settings.collection_name)
        count = collection.count()
    except Exception:
        count = 0
    return {
        "collection": settings.collection_name,
        "chunks": count,
        "storage_dir": str(settings.storage_dir),
        "data_dir": str(settings.data_dir),
    }
