# 🏎️ 2026 F1 Predictions

A Streamlit app for tracking Formula 1 season & race predictions with friends.

## Features

- **Season Predictions** — Pick your full Drivers' and Constructors' Championship standings
- **Race Predictions** — Predict the P1–P22 finishing order for every Grand Prix
- **Fun Predictions** — Hot takes, wild guesses, and bold calls
- **Persistent storage** — Supabase (PostgreSQL) in production, CSV fallback for local dev

## Quick Start (Local)

```bash
pip install -r requirements.txt
streamlit run Home.py
```

No database setup needed locally — predictions save to CSV files in `data/`.

## Deploy to Streamlit Community Cloud

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io) and connect your repo
3. Set up Supabase (see below) and add secrets in the Streamlit Cloud dashboard

## Supabase Setup

1. Create a free project at [supabase.com](https://supabase.com)
2. Open the **SQL Editor** and run the contents of [`supabase_schema.sql`](supabase_schema.sql)
3. Go to **Project Settings → API** and copy your **Project URL** and **anon/public key**
4. Create `.streamlit/secrets.toml` (see `.streamlit/secrets.toml.example`):

```toml
SUPABASE_URL = "https://your-project-id.supabase.co"
SUPABASE_KEY = "your-anon-public-key"
```

5. On Streamlit Community Cloud, paste the same values into **App Settings → Secrets**

## Project Structure

```
Home.py                  # Landing page
pages/
  1_Season_Predictions.py
  2_Race_Predictions.py
  3_Fun_Predictions.py
assets/
  style.css              # Global stylesheet
utils/
  constants.py           # Users, team colors, position config
  data_helpers.py        # Load/save with Supabase + CSV fallback
  db.py                  # Supabase client singleton
  styles.py              # CSS injection
  ui_helpers.py          # Reusable HTML component renderers
data/
  drivers.csv            # Static reference data
  constructors.csv
  races.csv
  season_predictions.csv # Local CSV fallback
  race_predictions.csv
  fun_predictions.csv
```

## Adding Users

Edit `USERS` in `utils/constants.py`:

```python
USERS = ["Seth", "Colin", "NewFriend"]
```

---

Built by [sethlors](https://github.com/sethlors) · 2026 F1 Predictions Tracker
