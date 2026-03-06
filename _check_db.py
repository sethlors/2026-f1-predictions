"""Create Supabase tables using the service key from secrets.toml."""
import sys
import os

# We need to read secrets.toml ourselves (not via st.secrets since we're not in Streamlit)
secrets_path = os.path.join(os.path.dirname(__file__), ".streamlit", "secrets.toml")

url = None
key = None
with open(secrets_path) as f:
    for line in f:
        line = line.strip()
        if line.startswith("SUPABASE_URL"):
            url = line.split("=", 1)[1].strip().strip('"')
        elif line.startswith("SUPABASE_KEY"):
            key = line.split("=", 1)[1].strip().strip('"')

if not url or not key:
    print("ERROR: Could not read SUPABASE_URL and SUPABASE_KEY from .streamlit/secrets.toml")
    sys.exit(1)

print(f"URL: {url}")
print(f"Key: {key[:25]}...")

from supabase import create_client
sb = create_client(url, key)

# Read the SQL schema
with open(os.path.join(os.path.dirname(__file__), "supabase_schema.sql")) as f:
    sql = f.read()

# Execute via Supabase RPC (raw SQL) - we need to use the REST API
# Supabase anon key can't run raw SQL. Print instructions instead.
print()
print("=" * 60)
print("Tables need to be created in the Supabase SQL Editor.")
print("Go to: https://supabase.com/dashboard → SQL Editor")
print("Paste the contents of supabase_schema.sql and click Run.")
print("=" * 60)
print()

# Try to check if tables already exist by querying them
tables = ["season_predictions", "race_predictions", "fun_predictions"]
for table in tables:
    try:
        resp = sb.table(table).select("*").limit(0).execute()
        print(f"  ✅ {table} - exists")
    except Exception as e:
        if "PGRST205" in str(e):
            print(f"  ❌ {table} - NOT FOUND (needs to be created)")
        else:
            print(f"  ⚠️  {table} - error: {e}")

