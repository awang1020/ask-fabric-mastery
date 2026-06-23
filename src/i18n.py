"""Lightweight EN/FR translations for the Streamlit UI."""
from __future__ import annotations

TRANSLATIONS: dict[str, dict[str, str]] = {
    "en": {
        # branding
        "brand": "Ask Fabric Mastery",
        "subbrand": "RAG assistant",
        # hero
        "hero_title": "Ask anything about Microsoft Fabric and Power BI",
        "hero_subtitle": "Answers sourced from the Fabric Mastery newsletter.",
        "hero_subtitle_empty": "Drop a newsletter file into the data folder, then build the index to get started.",
        # example prompts
        "ex_arch_title": "Medallion architecture",
        "ex_arch_prompt": "How should I structure the Bronze, Silver, and Gold layers in Fabric?",
        "ex_sec_title": "Fine-grained security",
        "ex_sec_prompt": "How do RLS, CLS, and OLS work together in Fabric?",
        "ex_cicd_title": "CI/CD",
        "ex_cicd_prompt": "How do I industrialise DEV \u2192 TEST \u2192 PROD deployments in Fabric?",
        "ex_capacity_title": "Capacity Units",
        "ex_capacity_prompt": "How do I optimise my Fabric Capacity Unit consumption?",
        # chat
        "ask_placeholder": "Ask anything about Fabric\u2026",
        "thinking": "Searching the archive\u2026",
        "cannot_answer": "I cannot answer this from the Fabric Mastery newsletter archive.",
        # sources
        "sources": "Sources",
        "view_post": "Open post",
        "page": "page",
        "score": "score",
        # sidebar
        "settings": "Settings",
        "language": "Language",
        "index": "Index",
        "index_chunks": "Indexed chunks",
        "build_index": "Build index",
        "rebuild_index": "Rebuild index",
        "indexing": "Indexing\u2026 this can take a couple of minutes.",
        "index_built": "Index built \u2014 {files} file(s), {chunks} chunk(s).",
        "no_files": "No supported files (.pdf, .md, .txt, .docx) found in {dir}.",
        "skipped_files": "Skipped (unsupported)",
        "clear_chat": "Clear conversation",
        "data_dir": "Data folder",
        "collection": "Collection",
        # status / errors
        "no_index": "No vector index yet. Build it from the sidebar to start asking questions.",
        "config_error": "Configuration error: {err}",
        "config_hint": "Copy `.env.example` to `.env` and fill in your Azure OpenAI credentials.",
        "error": "Error: {err}",
        "footer": "Powered by Azure OpenAI + LlamaIndex \u00b7 Grounded RAG \u00b7 {n} sources indexed",
        # safety: auth + rate limit
        "auth_title": "Private preview",
        "auth_subtitle": "This assistant is reserved for Fabric Mastery readers. The access code is at the top of the latest newsletter edition — paste it once and start asking questions.",
        "auth_password_label": "Access code",
        "auth_submit": "Unlock",
        "auth_invalid": "Invalid access code. The code is published at the top of the latest Fabric Mastery edition.",
        "rate_limited": "You\u2019ve asked {n} questions in the last {window_min} minutes. Please wait about {retry} seconds before the next one.",
        "visit_newsletter": "Read the newsletter",
    },
    "fr": {
        "brand": "Ask Fabric Mastery",
        "subbrand": "assistant RAG",
        "hero_title": "Posez vos questions sur Microsoft Fabric & Power BI",
        "hero_subtitle": "R\u00e9ponses sourc\u00e9es de la newsletter Fabric Mastery.",
        "hero_subtitle_empty": "D\u00e9posez un fichier de newsletter dans le dossier de donn\u00e9es, puis construisez l'index pour d\u00e9marrer.",
        "ex_arch_title": "Architecture Medallion",
        "ex_arch_prompt": "Comment structurer Bronze, Silver et Gold dans Fabric\u00a0?",
        "ex_sec_title": "S\u00e9curit\u00e9 fine",
        "ex_sec_prompt": "Comment fonctionnent RLS, CLS et OLS dans Fabric\u00a0?",
        "ex_cicd_title": "CI/CD",
        "ex_cicd_prompt": "Comment industrialiser le d\u00e9ploiement DEV \u2192 TEST \u2192 PROD dans Fabric\u00a0?",
        "ex_capacity_title": "Capacity Units",
        "ex_capacity_prompt": "Comment optimiser ma consommation de Capacity Units sur Fabric\u00a0?",
        "ask_placeholder": "Posez votre question sur Fabric\u2026",
        "thinking": "Recherche dans les archives\u2026",
        "cannot_answer": "Je ne peux pas r\u00e9pondre \u00e0 partir des archives de la newsletter Fabric Mastery.",
        "sources": "Sources",
        "view_post": "Ouvrir l'article",
        "page": "page",
        "score": "score",
        "settings": "Param\u00e8tres",
        "language": "Langue",
        "index": "Index",
        "index_chunks": "Fragments index\u00e9s",
        "build_index": "Construire l'index",
        "rebuild_index": "Reconstruire l'index",
        "indexing": "Indexation en cours\u2026 cela peut prendre quelques minutes.",
        "index_built": "Index construit \u2014 {files} fichier(s), {chunks} fragment(s).",
        "no_files": "Aucun fichier pris en charge (.pdf, .md, .txt, .docx) dans {dir}.",
        "skipped_files": "Ignor\u00e9s (non pris en charge)",
        "clear_chat": "Effacer la conversation",
        "data_dir": "Dossier des donn\u00e9es",
        "collection": "Collection",
        "no_index": "Aucun index vectoriel pour l'instant. Construisez-le depuis la barre lat\u00e9rale pour commencer.",
        "config_error": "Erreur de configuration\u00a0: {err}",
        "config_hint": "Copiez `.env.example` vers `.env` puis renseignez vos identifiants Azure OpenAI.",
        "error": "Erreur\u00a0: {err}",
        "footer": "Propuls\u00e9 par Azure OpenAI + LlamaIndex \u00b7 RAG strict \u00b7 {n} sources index\u00e9es",
        # safety: auth + rate limit
        "auth_title": "Acc\u00e8s r\u00e9serv\u00e9 aux lecteurs",
        "auth_subtitle": "Cet assistant est r\u00e9serv\u00e9 aux lecteurs de la newsletter Fabric Mastery. Le code d\u2019acc\u00e8s se trouve en haut de la derni\u00e8re \u00e9dition \u2014 collez-le ici pour commencer.",
        "auth_password_label": "Code d\u2019acc\u00e8s",
        "auth_submit": "D\u00e9verrouiller",
        "auth_invalid": "Code d\u2019acc\u00e8s invalide. Vous le trouverez en haut de la derni\u00e8re \u00e9dition de la newsletter Fabric Mastery.",
        "rate_limited": "Vous avez pos\u00e9 {n}\u00a0questions ces {window_min}\u00a0minutes. Patientez environ {retry}\u00a0secondes avant la prochaine.",
        "visit_newsletter": "Lire la newsletter",
    },
}


def t(language: str, key: str, **kwargs: object) -> str:
    lang = "fr" if (language or "").lower().startswith("fr") else "en"
    template = TRANSLATIONS[lang].get(key) or TRANSLATIONS["en"].get(key, key)
    return template.format(**kwargs) if kwargs else template
