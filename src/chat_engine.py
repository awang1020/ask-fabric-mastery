"""Grounded chat engine: ContextChatEngine wired with strict system prompts."""
from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from llama_index.core import VectorStoreIndex
from llama_index.core.chat_engine import ContextChatEngine
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.core.schema import NodeWithScore

from .config import get_settings
from .models import build_llm
from .prompts import CONTEXT_TEMPLATE, get_system_prompt
from .retriever import build_postprocessors, build_retriever

log = logging.getLogger(__name__)

SOURCES_INDEX_FILENAME = "_sources_index.json"
_sources_index_cache: dict[str, dict[str, str]] | None = None

# Strip YAML front-matter (--- ... ---) and leading markdown headings/whitespace
# so the UI snippet starts with actual prose, not metadata noise.
import re  # noqa: E402

_FRONT_MATTER_RE = re.compile(r"^---\s*\n.*?\n---\s*\n", flags=re.DOTALL)
_HEADING_RE = re.compile(r"^(#{1,6}\s+.*$|=+\s*$)", flags=re.MULTILINE)

# Patterns we treat as obvious prompt-injection / jailbreak attempts.
# When the user input matches any of these, we short-circuit BEFORE calling
# the LLM and return the canonical refusal line. This is a cheap defence in
# depth on top of the system prompt itself.
_JAILBREAK_RE = re.compile(
    r"""(?ix)
    (?:
        ignore\s+(?:all\s+|the\s+|your\s+|previous\s+)*(?:prior|previous|above|prompt|instructions?|rules?)
      | disregard\s+(?:all|the|your|previous|prior)?\s*(?:instructions?|rules?|prompt)
      | (?:forget|oublie|ignore[zr]?)\s+(?:tes|tout(?:es)?|les)?\s*(?:instructions?|consignes?|r[ee]gles?|prompts?)
      | (?:system|syst[\u00e8e]me)\s+prompt
      | reveal\s+(?:your|the)?\s*(?:system\s+)?(?:prompt|instructions?)
      | r[\u00e9e]v[\u00e8e]le[zr]?\s+(?:ton|le)?\s*(?:prompt|system|consigne|instructions?)
      | (?:tu\s+es\s+maintenant|you\s+are\s+now|act\s+as|pretend\s+to\s+be|joue\s+(?:le\s+r[\u00f4o]le|au\s+r[\u00f4o]le))
      | (?:do\s+anything\s+now|\bDAN\b|developer\s+mode|mode\s+d[\u00e9e]veloppeur)
      | jailbreak
      | bypass\s+(?:the|your|all)?\s*(?:safety|filters?|rules?|restrictions?)
      | switch\s+(?:to\s+)?(?:another|admin|root|god)\s+mode
    )
    """,
)


def looks_like_jailbreak(text: str) -> bool:
    """Return True when the query matches a known injection / override pattern."""
    if not text:
        return False
    return bool(_JAILBREAK_RE.search(text))


def _clean_snippet(raw: str, length: int = 220) -> str:
    text = _FRONT_MATTER_RE.sub("", raw or "")
    text = _HEADING_RE.sub("", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text[:length]


def _load_sources_index() -> dict[str, dict[str, str]]:
    """Load (and cache) the {filename: {title, url, date, ...}} side-table from ingest."""
    global _sources_index_cache  # noqa: PLW0603
    if _sources_index_cache is not None:
        return _sources_index_cache
    path: Path = get_settings().data_dir / SOURCES_INDEX_FILENAME
    if not path.exists():
        _sources_index_cache = {}
        return _sources_index_cache
    try:
        _sources_index_cache = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        log.warning("Could not parse %s: %s", path.name, exc)
        _sources_index_cache = {}
    return _sources_index_cache


def refresh_sources_index() -> None:
    """Force re-read on next access (call after rebuilding the index)."""
    global _sources_index_cache  # noqa: PLW0603
    _sources_index_cache = None


@dataclass
class Source:
    file_name: str
    page: str | None
    score: float | None
    snippet: str
    title: str | None = None
    url: str | None = None
    date: str | None = None

    @classmethod
    def from_node(cls, node: NodeWithScore) -> "Source":
        meta = node.node.metadata or {}
        file_name = (
            meta.get("file_name")
            or meta.get("file_path")
            or meta.get("filename")
            or "unknown"
        )
        file_name = Path(str(file_name)).name  # always basename for display
        page = meta.get("page_label")
        idx = _load_sources_index().get(file_name, {})
        return cls(
            file_name=file_name,
            page=str(page) if page is not None else None,
            score=float(node.score) if node.score is not None else None,
            snippet=_clean_snippet(node.node.get_content() or ""),
            title=idx.get("title"),
            url=idx.get("url"),
            date=idx.get("date"),
        )


@dataclass
class ChatTurn:
    answer: str
    sources: list[Source]
    raw_response: Any | None = None


def build_chat_engine(index: VectorStoreIndex, language: str = "en") -> ContextChatEngine:
    settings = get_settings()
    retriever = build_retriever(index, settings)
    postprocessors = build_postprocessors(settings)
    llm = build_llm(settings)
    memory = ChatMemoryBuffer.from_defaults(token_limit=4096, llm=llm)
    return ContextChatEngine.from_defaults(
        retriever=retriever,
        llm=llm,
        memory=memory,
        node_postprocessors=postprocessors,
        system_prompt=get_system_prompt(language),
        context_template=CONTEXT_TEMPLATE,
    )


def _refusal(language: str) -> str:
    if (language or "").lower().startswith("fr"):
        return (
            "Je ne peux pas r\u00e9pondre \u00e0 partir des archives de la "
            "newsletter Fabric Mastery. Posez-moi plut\u00f4t une question sur "
            "Microsoft Fabric ou Power BI."
        )
    return (
        "I cannot answer this from the Fabric Mastery newsletter archive. "
        "Ask me about Microsoft Fabric or Power BI instead."
    )


def ask(engine: ContextChatEngine, query: str, language: str = "en") -> ChatTurn:
    """Run a single query through the chat engine and capture sources.

    Sources are de-duplicated by URL (falling back to filename) so the UI only
    surfaces distinct posts even when multiple chunks of the same article match.
    If ``query`` looks like a prompt-injection / jailbreak attempt, the LLM is
    bypassed and the canonical refusal line is returned instead.
    """
    if looks_like_jailbreak(query):
        return ChatTurn(answer=_refusal(language), sources=[], raw_response=None)

    response = engine.chat(query)

    seen: set[str] = set()
    sources: list[Source] = []
    for node in (getattr(response, "source_nodes", None) or []):
        src = Source.from_node(node)
        key = src.url or src.file_name
        if key in seen:
            continue
        seen.add(key)
        sources.append(src)

    answer = str(response).strip()
    # LlamaIndex returns the literal string "Empty Response" when every node
    # is filtered out by the similarity cutoff. That happens for off-topic
    # questions (no chunk is close enough). Surface the canonical refusal.
    if not answer or answer.lower() == "empty response" or not sources:
        return ChatTurn(answer=_refusal(language), sources=[], raw_response=response)

    return ChatTurn(answer=answer, sources=sources, raw_response=response)
