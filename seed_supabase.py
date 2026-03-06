"""Seed Supabase tables with CSV reference data.

Reads credentials from .streamlit/secrets.toml and uploads drivers,
constructors, and races data from the data/ directory into Supabase.

Usage:
    python seed_supabase.py
"""
from __future__ import annotations

import os
import sys

import pandas as pd

# ---------------------------------------------------------------------------
# Read Supabase credentials from .streamlit/secrets.toml
# ---------------------------------------------------------------------------
SECRETS_PATH = os.path.join(os.path.dirname(__file__), ".streamlit", "secrets.toml")

url: str | None = None
key: str | None = None

try:
    with open(SECRETS_PATH) as f:
        for line in f:
            line = line.strip()
            if line.startswith("SUPABASE_URL"):
                url = line.split("=", 1)[1].strip().strip('"')
            elif line.startswith("SUPABASE_KEY"):
                key = line.split("=", 1)[1].strip().strip('"')
except FileNotFoundError:
    print(f"ERROR: {SECRETS_PATH} not found.")
    print("Create .streamlit/secrets.toml with SUPABASE_URL and SUPABASE_KEY.")
    sys.exit(1)

if not url or not key:
    print("ERROR: Could not read SUPABASE_URL and SUPABASE_KEY from secrets.")
    sys.exit(1)

from supabase import create_client

sb = create_client(url, key)
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def upsert_table(table_name: str, df: pd.DataFrame, conflict_col: str) -> None:
    """Upsert a DataFrame into a Supabase table."""
    rows = df.to_dict(orient="records")
    if not rows:
        print(f"  ⚠️  {table_name}: no data to upload")
        return
    resp = sb.table(table_name).upsert(rows, on_conflict=conflict_col).execute()
    print(f"  ✅ {table_name}: upserted {len(rows)} rows")


# ---------------------------------------------------------------------------
# Seed reference data
# ---------------------------------------------------------------------------
print("Seeding reference data...")

# Drivers
drivers = pd.read_csv(os.path.join(DATA_DIR, "drivers.csv"))
drivers.columns = ["driver_name", "driver_number", "driver_team"]
upsert_table("drivers", drivers, "driver_name")

# Constructors
constructors = pd.read_csv(os.path.join(DATA_DIR, "constructors.csv"))
constructors.columns = ["team_name", "team_color"]
upsert_table("constructors", constructors, "team_name")

# Races
races = pd.read_csv(os.path.join(DATA_DIR, "races.csv"))
races.columns = ["round_number", "race_name", "race_date"]
upsert_table("races", races, "round_number")

# ---------------------------------------------------------------------------
# Seed prediction data (if any rows exist in CSVs)
# ---------------------------------------------------------------------------
print("\nSeeding prediction data...")

# Season predictions
sp = pd.read_csv(os.path.join(DATA_DIR, "season_predictions.csv"))
if not sp.empty:
    upsert_table("season_predictions", sp, "user")
else:
    print("  ⏭  season_predictions: CSV is empty, skipping")

# Race predictions
rp = pd.read_csv(os.path.join(DATA_DIR, "race_predictions.csv"))
if not rp.empty:
    upsert_table("race_predictions", rp, "race,user")
else:
    print("  ⏭  race_predictions: CSV is empty, skipping")

# Fun predictions
fp = pd.read_csv(os.path.join(DATA_DIR, "fun_predictions.csv"))
if not fp.empty:
    # Fun predictions are append-only; insert new ones
    rows = fp.to_dict(orient="records")
    sb.table("fun_predictions").insert(rows).execute()
    print(f"  ✅ fun_predictions: inserted {len(rows)} rows")
else:
    print("  ⏭  fun_predictions: CSV is empty, skipping")

print("\n✅ Done! Your data is now in Supabase.")
