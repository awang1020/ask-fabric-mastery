"""Azure OpenAI LLM + embedding model factories and global LlamaIndex wiring.

Authentication priority:
  1. ``AZURE_OPENAI_API_KEY`` if set in the environment.
  2. Otherwise Entra ID via ``DefaultAzureCredential`` (Azure CLI login,
     managed identity, env vars, etc.) — required when the tenant has
     ``disableLocalAuth=true`` on the Cognitive Services account.
"""
from __future__ import annotations

from llama_index.core import Settings as LlamaSettings
from llama_index.embeddings.azure_openai import AzureOpenAIEmbedding
from llama_index.llms.azure_openai import AzureOpenAI

from .config import Settings, get_settings

_AAD_SCOPE = "https://cognitiveservices.azure.com/.default"
_credential_cache: object | None = None


def _token_provider():
    """Return a callable that produces a fresh Entra ID bearer token.

    Uses a deterministic chain so dev machines do not get tripped up by an
    unrelated Azure Arc / Connected Machine managed identity:
      1. AzureCliCredential       (the user's `az login` session)
      2. EnvironmentCredential    (SP creds in env vars, e.g. CI)
      3. ManagedIdentityCredential (in Azure-hosted runtime)
    """
    from azure.identity import (
        AzureCliCredential,
        ChainedTokenCredential,
        EnvironmentCredential,
        ManagedIdentityCredential,
        get_bearer_token_provider,
    )

    global _credential_cache  # noqa: PLW0603
    if _credential_cache is None:
        _credential_cache = ChainedTokenCredential(
            AzureCliCredential(),
            EnvironmentCredential(),
            ManagedIdentityCredential(),
        )
    return get_bearer_token_provider(_credential_cache, _AAD_SCOPE)


def _auth_kwargs(settings: Settings) -> dict:
    if settings.azure_openai_api_key:
        return {"api_key": settings.azure_openai_api_key}
    return {"azure_ad_token_provider": _token_provider(), "use_azure_ad": True}


def build_llm(settings: Settings | None = None) -> AzureOpenAI:
    s = settings or get_settings()
    return AzureOpenAI(
        model=s.azure_openai_chat_model,
        deployment_name=s.azure_openai_chat_deployment,
        azure_endpoint=s.azure_openai_endpoint,
        api_version=s.azure_openai_api_version,
        temperature=s.temperature,
        max_tokens=s.max_tokens,
        **_auth_kwargs(s),
    )


def build_embed_model(settings: Settings | None = None) -> AzureOpenAIEmbedding:
    s = settings or get_settings()
    return AzureOpenAIEmbedding(
        model=s.azure_openai_embedding_model,
        deployment_name=s.azure_openai_embedding_deployment,
        azure_endpoint=s.azure_openai_endpoint,
        api_version=s.azure_openai_api_version,
        **_auth_kwargs(s),
    )


def configure_llama_settings() -> None:
    """Wire Azure OpenAI models into LlamaIndex's global Settings.

    Must be called before any indexing or querying so that
    `VectorStoreIndex` and friends pick up the right embedding model.
    """
    s = get_settings()
    LlamaSettings.llm = build_llm(s)
    LlamaSettings.embed_model = build_embed_model(s)
