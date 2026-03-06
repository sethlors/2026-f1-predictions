"""Data loading and saving utilities — Supabase only."""
from __future__ import annotations

import streamlit as st
import pandas as pd

from utils.db import get_client


def _require_client():
    """Return the Supabase client or stop with an error."""
    sb = get_client()
    if sb is None:
        st.error("Supabase is not configured. Set SUPABASE_URL and SUPABASE_KEY in secrets.")
        st.stop()
    return sb


# ---------------------------------------------------------------------------
# Reference data
# ---------------------------------------------------------------------------

def load_drivers() -> pd.DataFrame:
    sb = _require_client()
    resp = sb.table("drivers").select("*").execute()
    df = pd.DataFrame(resp.data) if resp.data else pd.DataFrame(columns=["Driver Name", "Driver Number", "Driver Team"])
    return df.rename(columns={
        "driver_name": "Driver Name",
        "driver_number": "Driver Number",
        "driver_team": "Driver Team",
    })


def load_constructors() -> pd.DataFrame:
    sb = _require_client()
    resp = sb.table("constructors").select("*").execute()
    df = pd.DataFrame(resp.data) if resp.data else pd.DataFrame(columns=["Team Name", "Team Color"])
    return df.rename(columns={
        "team_name": "Team Name",
        "team_color": "Team Color",
    })


def load_races() -> pd.DataFrame:
    sb = _require_client()
    resp = sb.table("races").select("*").execute()
    df = pd.DataFrame(resp.data) if resp.data else pd.DataFrame(columns=["Round Number", "Race Name", "Race Date"])
    return df.rename(columns={
        "round_number": "Round Number",
        "race_name": "Race Name",
        "race_date": "Race Date",
    })


# =========================================================================
# Season predictions
# =========================================================================

def load_season_predictions() -> pd.DataFrame:
    sb = _require_client()
    resp = sb.table("season_predictions").select("*").execute()
    if resp.data:
        return pd.DataFrame(resp.data)
    cols = ["id", "user"] + [f"D{i}" for i in range(1, 23)] + [f"C{i}" for i in range(1, 12)]
    return pd.DataFrame(columns=cols)


def upsert_season_prediction(row: dict) -> None:
    """Insert or update a single season prediction row keyed on ``user``."""
    sb = _require_client()
    try:
        sb.table("season_predictions").upsert(row, on_conflict="user").execute()
    except Exception as e:
        st.error(f"Database write failed: {e}")


def delete_season_prediction(user: str) -> None:
    sb = _require_client()
    sb.table("season_predictions").delete().eq("user", user).execute()


# =========================================================================
# Race predictions
# =========================================================================

def load_race_predictions() -> pd.DataFrame:
    sb = _require_client()
    resp = sb.table("race_predictions").select("*").execute()
    if resp.data:
        return pd.DataFrame(resp.data)
    cols = ["id", "race", "user"] + [f"P{i}" for i in range(1, 23)]
    return pd.DataFrame(columns=cols)


def upsert_race_prediction(row: dict) -> None:
    """Insert or update a single race prediction keyed on ``(race, user)``."""
    sb = _require_client()
    try:
        sb.table("race_predictions").upsert(row, on_conflict="race,user").execute()
    except Exception as e:
        st.error(f"Database write failed: {e}")


def delete_race_prediction(race: str, user: str) -> None:
    sb = _require_client()
    sb.table("race_predictions").delete().eq("race", race).eq("user", user).execute()


# =========================================================================
# Fun predictions
# =========================================================================

def load_fun_predictions() -> pd.DataFrame:
    sb = _require_client()
    resp = sb.table("fun_predictions").select("*").execute()
    if resp.data:
        return pd.DataFrame(resp.data)
    return pd.DataFrame(columns=["id", "user", "prediction", "date_created"])


def insert_fun_prediction(row: dict) -> None:
    sb = _require_client()
    try:
        sb.table("fun_predictions").insert(row).execute()
    except Exception as e:
        st.error(f"Database write failed: {e}")


def delete_fun_prediction(prediction_id: int) -> None:
    sb = _require_client()
    sb.table("fun_predictions").delete().eq("id", prediction_id).execute()
