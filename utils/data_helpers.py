"""Data loading and saving utilities.

When Supabase credentials are configured (via `st.secrets`), all data is
persisted in Supabase tables.  Otherwise the module falls back to local CSV files
so the app stays runnable during local development.
"""
from __future__ import annotations

import os
import pandas as pd

from utils.db import get_client

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")

# ---------------------------------------------------------------------------
# Reference data (Supabase with CSV fallback)
# ---------------------------------------------------------------------------

def load_drivers() -> pd.DataFrame:
    """Load drivers data from Supabase or CSV fallback."""
    sb = get_client()
    if sb is not None:
        resp = sb.table("drivers").select("*").execute()
        if resp.data:
            df = pd.DataFrame(resp.data)
            df = df.rename(columns={
                "driver_name": "Driver Name",
                "driver_number": "Driver Number",
                "driver_team": "Driver Team",
            })
            return df
    return pd.read_csv(os.path.join(DATA_DIR, "drivers.csv"))


def load_constructors() -> pd.DataFrame:
    """Load constructors data from Supabase or CSV fallback."""
    sb = get_client()
    if sb is not None:
        resp = sb.table("constructors").select("*").execute()
        if resp.data:
            df = pd.DataFrame(resp.data)
            df = df.rename(columns={
                "team_name": "Team Name",
                "team_color": "Team Color",
            })
            return df
    return pd.read_csv(os.path.join(DATA_DIR, "constructors.csv"))


def load_races() -> pd.DataFrame:
    """Load races data from Supabase or CSV fallback."""
    sb = get_client()
    if sb is not None:
        resp = sb.table("races").select("*").execute()
        if resp.data:
            df = pd.DataFrame(resp.data)
            df = df.rename(columns={
                "round_number": "Round Number",
                "race_name": "Race Name",
                "race_date": "Race Date",
            })
            return df
    return pd.read_csv(os.path.join(DATA_DIR, "races.csv"))


# =========================================================================
# Season predictions
# =========================================================================

def load_season_predictions() -> pd.DataFrame:
    sb = get_client()
    if sb is not None:
        resp = sb.table("season_predictions").select("*").execute()
        if resp.data:
            return pd.DataFrame(resp.data)
        # Return empty DF with expected columns
        cols = ["id", "user"] + [f"D{i}" for i in range(1, 23)] + [f"C{i}" for i in range(1, 12)]
        return pd.DataFrame(columns=cols)
    return pd.read_csv(os.path.join(DATA_DIR, "season_predictions.csv"))


def save_season_predictions(df: pd.DataFrame) -> None:
    """Save the full season predictions DataFrame (CSV fallback only)."""
    sb = get_client()
    if sb is not None:
        # For Supabase we prefer the row-level helpers below.
        # This full-DF save is only used by the CSV path.
        pass
    else:
        df.to_csv(os.path.join(DATA_DIR, "season_predictions.csv"), index=False)


def upsert_season_prediction(row: dict) -> None:
    """Insert or update a single season prediction row keyed on ``user``."""
    sb = get_client()
    if sb is not None:
        sb.table("season_predictions").upsert(row, on_conflict="user").execute()
    else:
        # CSV path: load → upsert in-memory → save
        df = pd.read_csv(os.path.join(DATA_DIR, "season_predictions.csv"))
        mask = df["user"] == row["user"]
        if mask.any():
            for k, v in row.items():
                df.loc[mask, k] = v
        else:
            df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
        df.to_csv(os.path.join(DATA_DIR, "season_predictions.csv"), index=False)


def delete_season_prediction(user: str) -> None:
    """Delete a season prediction by user name."""
    sb = get_client()
    if sb is not None:
        sb.table("season_predictions").delete().eq("user", user).execute()
    else:
        df = pd.read_csv(os.path.join(DATA_DIR, "season_predictions.csv"))
        df = df[df["user"] != user].reset_index(drop=True)
        df.to_csv(os.path.join(DATA_DIR, "season_predictions.csv"), index=False)


# =========================================================================
# Race predictions
# =========================================================================

def load_race_predictions() -> pd.DataFrame:
    sb = get_client()
    if sb is not None:
        resp = sb.table("race_predictions").select("*").execute()
        if resp.data:
            return pd.DataFrame(resp.data)
        cols = ["id", "race", "user"] + [f"P{i}" for i in range(1, 23)]
        return pd.DataFrame(columns=cols)
    return pd.read_csv(os.path.join(DATA_DIR, "race_predictions.csv"))


def save_race_predictions(df: pd.DataFrame) -> None:
    """Save the full race predictions DataFrame (CSV fallback only)."""
    sb = get_client()
    if sb is None:
        df.to_csv(os.path.join(DATA_DIR, "race_predictions.csv"), index=False)


def upsert_race_prediction(row: dict) -> None:
    """Insert or update a single race prediction keyed on ``(race, user)``."""
    sb = get_client()
    if sb is not None:
        sb.table("race_predictions").upsert(row, on_conflict="race,user").execute()
    else:
        df = pd.read_csv(os.path.join(DATA_DIR, "race_predictions.csv"))
        mask = (df["race"] == row["race"]) & (df["user"] == row["user"])
        if mask.any():
            for k, v in row.items():
                df.loc[mask, k] = v
        else:
            df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
        df.to_csv(os.path.join(DATA_DIR, "race_predictions.csv"), index=False)


def delete_race_prediction(race: str, user: str) -> None:
    """Delete a race prediction by race name + user."""
    sb = get_client()
    if sb is not None:
        sb.table("race_predictions").delete().eq("race", race).eq("user", user).execute()
    else:
        df = pd.read_csv(os.path.join(DATA_DIR, "race_predictions.csv"))
        df = df[~((df["race"] == race) & (df["user"] == user))].reset_index(drop=True)
        df.to_csv(os.path.join(DATA_DIR, "race_predictions.csv"), index=False)


# =========================================================================
# Fun predictions
# =========================================================================

def load_fun_predictions() -> pd.DataFrame:
    sb = get_client()
    if sb is not None:
        resp = sb.table("fun_predictions").select("*").execute()
        if resp.data:
            return pd.DataFrame(resp.data)
        return pd.DataFrame(columns=["id", "user", "prediction", "date_created"])
    return pd.read_csv(os.path.join(DATA_DIR, "fun_predictions.csv"))


def save_fun_predictions(df: pd.DataFrame) -> None:
    """Save the full fun predictions DataFrame (CSV fallback only)."""
    sb = get_client()
    if sb is None:
        df.to_csv(os.path.join(DATA_DIR, "fun_predictions.csv"), index=False)


def insert_fun_prediction(row: dict) -> None:
    """Insert a single fun prediction."""
    sb = get_client()
    if sb is not None:
        sb.table("fun_predictions").insert(row).execute()
    else:
        df = pd.read_csv(os.path.join(DATA_DIR, "fun_predictions.csv"))
        df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
        df.to_csv(os.path.join(DATA_DIR, "fun_predictions.csv"), index=False)


def delete_fun_prediction(prediction_id: int) -> None:
    """Delete a fun prediction by its id (Supabase PK) or index (CSV fallback)."""
    sb = get_client()
    if sb is not None:
        sb.table("fun_predictions").delete().eq("id", prediction_id).execute()
    else:
        df = pd.read_csv(os.path.join(DATA_DIR, "fun_predictions.csv"))
        df = df.drop(index=prediction_id).reset_index(drop=True)
        df.to_csv(os.path.join(DATA_DIR, "fun_predictions.csv"), index=False)
