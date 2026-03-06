"""Supabase client singleton.

Returns ``None`` when credentials are not configured (local dev / CSV fallback).
"""
from __future__ import annotations

import streamlit as st

try:
    from supabase import create_client, Client  # type: ignore[import-untyped]

    _HAS_SUPABASE = True
except ImportError:
    _HAS_SUPABASE = False
    Client = None  # type: ignore[assignment,misc]


@st.cache_resource
def get_client() -> "Client | None":
    """Return a shared Supabase client, or *None* if secrets are missing."""
    if not _HAS_SUPABASE:
        return None
    try:
        url: str = st.secrets["SUPABASE_URL"]
        key: str = st.secrets["SUPABASE_KEY"]
    except (KeyError, FileNotFoundError):
        return None
    return create_client(url, key)

