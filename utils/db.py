"""Supabase client singleton."""
from __future__ import annotations

import streamlit as st

try:
    from supabase import create_client, Client  # type: ignore[import-untyped]

    _HAS_SUPABASE = True
except ImportError:
    _HAS_SUPABASE = False
    Client = None  # type: ignore[assignment,misc]


_client: "Client | None" = None
_client_checked: bool = False


def get_client() -> "Client | None":
    """Return a shared Supabase client, or *None* if secrets are missing."""
    global _client, _client_checked
    if _client_checked:
        return _client
    if not _HAS_SUPABASE:
        _client_checked = True
        return None
    try:
        url: str = st.secrets["SUPABASE_URL"]
        key: str = st.secrets["SUPABASE_KEY"]
    except (KeyError, FileNotFoundError):
        _client_checked = True
        return None
    _client = create_client(url, key)
    _client_checked = True
    return _client

