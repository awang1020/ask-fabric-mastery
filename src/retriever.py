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


def build_postprocessors(settings: Settings | None = None) -> list:
    s = settings or get_settings()
    procs: list = [SimilarityPostprocessor(similarity_cutoff=s.similarity_cutoff)]
    if s.use_llm_rerank:
        # Imported lazily so environments that never enable rerank do not pay the import cost.
        from llama_index.core.postprocessor import LLMRerank

        from .models import build_llm

        procs.append(LLMRerank(top_n=s.rerank_top_n, llm=build_llm(s)))
    return procs
