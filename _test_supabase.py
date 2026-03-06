"""Test Supabase connection and create tables if needed."""
import sys
from supabase import create_client

URL = "https://qjhzpfvgmjxtxnwemxgd.supabase.co"
KEY = "sb_publishable_xFMGIBmViJ3eKRYB5CFIxg_cP12JqSt"

try:
    sb = create_client(URL, KEY)
    print("Client created OK")
except Exception as e:
    print(f"Client creation failed: {e}")
    sys.exit(1)

# Try to query a table to see if it exists
try:
    resp = sb.table("season_predictions").select("*").limit(1).execute()
    print(f"season_predictions exists, rows: {len(resp.data)}")
except Exception as e:
    print(f"season_predictions query failed: {e}")
    print("You need to run supabase_schema.sql in the Supabase SQL Editor!")

try:
    resp = sb.table("race_predictions").select("*").limit(1).execute()
    print(f"race_predictions exists, rows: {len(resp.data)}")
except Exception as e:
    print(f"race_predictions query failed: {e}")

try:
    resp = sb.table("fun_predictions").select("*").limit(1).execute()
    print(f"fun_predictions exists, rows: {len(resp.data)}")
except Exception as e:
    print(f"fun_predictions query failed: {e}")

