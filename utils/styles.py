"""Shared CSS injection for the F1 Predictions app."""
import os
import streamlit as st

_CSS_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "style.css")


@st.cache_resource
def _load_css() -> str:
    """Read the global stylesheet once and cache it."""
    with open(_CSS_PATH) as f:
        return f.read()


def inject_styles() -> None:
    """Inject the global CSS into the current page."""
    st.markdown(f"<style>{_load_css()}</style>", unsafe_allow_html=True)
