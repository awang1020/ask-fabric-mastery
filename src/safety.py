"""Lightweight in-process safety controls for the public RAG UI.

Two layers are exposed:

1. ``require_password`` — optional shared-secret gate. When ``APP_PASSWORD``
   is set, visitors must type the password before they can ask anything.
   This is intentionally *not* per-user auth: it is a cheap anti-bot /
   anti-scraper layer suitable for a newsletter audience.

2. ``check_rate_limit`` — session-scoped sliding-window rate limiter.
   Caps how many questions a single Streamlit session can ask in a window,
   protecting AOAI token spend against a tab left open with auto-refresh
   or a curious user mashing the example cards.

Both helpers store their state in ``st.session_state`` and degrade safely
(open) when configuration is missing.
"""
from __future__ import annotations

import os
import secrets
import time
from dataclasses import dataclass

import streamlit as st

from src.i18n import t


_PASSWORD_KEY = "_auth_ok"
_RATE_KEY = "_question_timestamps"


@dataclass(frozen=True)
class RateLimit:
    max_questions: int
    window_seconds: int


def _expected_password() -> str | None:
    pwd = os.getenv("APP_PASSWORD", "").strip()
    return pwd or None


def require_password(language: str) -> bool:
    """Block rendering until the visitor has typed the shared password.

    Returns True when the page is unlocked (no password configured, or the
    user has authenticated successfully) and False while the gate is shown.
    """
    expected = _expected_password()
    if expected is None:
        return True
    if st.session_state.get(_PASSWORD_KEY) is True:
        return True

    st.markdown(
        '<div class="afm-hero" style="margin-top:6rem;">'
        f'<h1>{t(language, "auth_title")}</h1>'
        f'<p>{t(language, "auth_subtitle")}</p>'
        '</div>',
        unsafe_allow_html=True,
    )

    with st.form("afm-password-gate", clear_on_submit=False):
        pwd = st.text_input(
            t(language, "auth_password_label"),
            type="password",
            autocomplete="current-password",
        )
        submitted = st.form_submit_button(
            t(language, "auth_submit"), use_container_width=True
        )

    if submitted:
        # Constant-time compare — avoid trivial timing oracles.
        if secrets.compare_digest(pwd, expected):
            st.session_state[_PASSWORD_KEY] = True
            st.rerun()
        else:
            st.error(t(language, "auth_invalid"))
    return False


def _rate_limit_config() -> RateLimit:
    return RateLimit(
        max_questions=int(os.getenv("RATE_LIMIT_MAX_QUESTIONS", "20") or 20),
        window_seconds=int(os.getenv("RATE_LIMIT_WINDOW_SECONDS", "900") or 900),
    )


def check_rate_limit(language: str) -> tuple[bool, int]:
    """Return ``(allowed, retry_after_seconds)``.

    The caller should drop the question and surface the message to the
    user when ``allowed`` is False. Each successful call records the
    current timestamp.
    """
    cfg = _rate_limit_config()
    now = time.time()
    history: list[float] = st.session_state.setdefault(_RATE_KEY, [])
    cutoff = now - cfg.window_seconds
    history[:] = [ts for ts in history if ts >= cutoff]
    if len(history) >= cfg.max_questions:
        retry = int(cfg.window_seconds - (now - history[0])) + 1
        st.warning(
            t(
                language,
                "rate_limited",
                n=cfg.max_questions,
                window_min=cfg.window_seconds // 60,
                retry=retry,
            )
        )
        return False, retry
    history.append(now)
    return True, 0
