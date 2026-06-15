"""Retrieval logic: vector retriever + similarity post-processing."""
from __future__ import annotations

from llama_index.core import VectorStoreIndex
from llama_index.core.postprocessor import SimilarityPostprocessor
from llama_index.core.retrievers import VectorIndexRetriever

from .config import Settings, get_settings


def build_retriever(
    index: VectorStoreIndex, settings: Settings | None = None
) -> VectorIndexRetriever:
    s = settings or get_settings()
    return VectorIndexRetriever(index=index, similarity_top_k=s.top_k)


def build_postprocessors(settings: Settings | None = None) -> list[SimilarityPostprocessor]:
    s = settings or get_settings()
    return [SimilarityPostprocessor(similarity_cutoff=s.similarity_cutoff)]
