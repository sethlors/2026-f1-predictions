import streamlit as st
import pandas as pd
import os
from datetime import date

st.set_page_config(
    page_title="2026 F1 Predictions",
    page_icon="",
    layout="wide",
)

# ---------------------------------------------------------------------------
# Custom CSS
# ---------------------------------------------------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .hero {
        background: linear-gradient(135deg, #e10600 0%, #1e1e1e 60%);
        border-radius: 16px;
        padding: 3rem 2.5rem;
        margin-bottom: 2rem;
        color: white;
    }
    .hero h1 {
        font-size: 3rem;
        font-weight: 900;
        margin: 0 0 0.25rem 0;
        letter-spacing: -1px;
    }
    .hero .subtitle {
        font-size: 1.2rem;
        opacity: 0.85;
        margin-top: 0;
    }

    .stat-row {
        display: flex;
        gap: 1rem;
        margin-bottom: 1.5rem;
        flex-wrap: wrap;
    }
    .stat-card {
        flex: 1;
        min-width: 160px;
        background: #1e1e1e;
        border: 1px solid #333;
        border-radius: 12px;
        padding: 1.25rem 1.5rem;
        color: white;
        text-align: center;
    }
    .stat-card .stat-value {
        font-size: 2rem;
        font-weight: 900;
        color: #e10600;
    }
    .stat-card .stat-label {
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        opacity: 0.7;
        margin-top: 0.25rem;
    }

    .nav-cards {
        display: flex;
        gap: 1.25rem;
        margin-top: 1rem;
        flex-wrap: wrap;
    }
    .nav-card {
        flex: 1;
        min-width: 260px;
        background: #1e1e1e;
        border: 1px solid #333;
        border-radius: 14px;
        padding: 2rem 1.75rem;
        color: white;
        transition: border-color 0.2s, transform 0.2s;
    }
    .nav-card:hover {
        border-color: #e10600;
        transform: translateY(-2px);
    }
    .nav-card h3 {
        margin: 0 0 0.5rem 0;
        font-weight: 700;
    }
    .nav-card p {
        margin: 0;
        opacity: 0.7;
        font-size: 0.95rem;
        line-height: 1.5;
    }

    .countdown-bar {
        background: linear-gradient(90deg, #e10600 0%, #ff6347 100%);
        border-radius: 12px;
        padding: 1rem 1.5rem;
        color: white;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1.5rem;
        flex-wrap: wrap;
        gap: 0.5rem;
    }
    .countdown-bar .race-name {
        font-weight: 700;
        font-size: 1.1rem;
    }
    .countdown-bar .days-left {
        font-weight: 900;
        font-size: 1.3rem;
    }

    .footer {
        text-align: center;
        opacity: 0.4;
        font-size: 0.8rem;
        margin-top: 3rem;
        padding-bottom: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

drivers_df = pd.read_csv(os.path.join(DATA_DIR, "drivers.csv"))
races_df = pd.read_csv(os.path.join(DATA_DIR, "races.csv"))
constructors_df = pd.read_csv(os.path.join(DATA_DIR, "constructors.csv"))
season_df = pd.read_csv(os.path.join(DATA_DIR, "season_predictions.csv"))
race_pred_df = pd.read_csv(os.path.join(DATA_DIR, "race_predictions.csv"))

# ---------------------------------------------------------------------------
# Next-race countdown
# ---------------------------------------------------------------------------
today = date.today()
races_df["_date"] = pd.to_datetime(races_df["Race Date"], format="%m/%d/%Y")
future_races = races_df[races_df["_date"].dt.date >= today]

if not future_races.empty:
    next_race = future_races.iloc[0]
    days_left = (next_race["_date"].date() - today).days
    if days_left == 0:
        countdown_text = "Today!"
    elif days_left == 1:
        countdown_text = "1 day away"
    else:
        countdown_text = f"{days_left} days away"
    st.markdown(
        f"""
        <div class="countdown-bar">
            <span class="race-name">Next Race: {next_race['Race Name']}</span>
            <span class="days-left">{countdown_text}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ---------------------------------------------------------------------------
# Hero
# ---------------------------------------------------------------------------
st.markdown(
    """
    <div class="hero">
        <h1>2026 F1 Predictions</h1>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Stats row
# ---------------------------------------------------------------------------
num_drivers = len(drivers_df)
num_teams = len(constructors_df)
num_races = len(races_df)
total_preds = len(season_df) + len(race_pred_df)

st.markdown(
    f"""
    <div class="stat-row">
        <div class="stat-card">
            <div class="stat-value">{num_drivers}</div>
            <div class="stat-label">Drivers</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">{num_teams}</div>
            <div class="stat-label">Teams</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">{num_races}</div>
            <div class="stat-label">Races</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">{total_preds}</div>
            <div class="stat-label">Predictions Made</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Navigation cards
# ---------------------------------------------------------------------------
st.markdown(
    """
    <div class="nav-cards">
        <div class="nav-card">
            <h3>Season Predictions</h3>
            <p>Pick your <strong>Drivers'</strong> and <strong>Constructors' Champions</strong> for the 2026 season.</p>
        </div>
        <div class="nav-card">
            <h3>Race Predictions</h3>
            <p>Predict the full <strong>P1 – P22</strong> finishing order for every Grand Prix.</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("")
st.info("Use the **sidebar** to navigate to a prediction page.")

st.markdown(
    '<div class="footer">Built by <a href="https://github.com/sethlors" target="_blank" style="color:inherit; text-decoration:underline;">sethlors</a> and the <a href="https://claude.com/product/claude-code" target="_blank" style="color:inherit; text-decoration:underline;">gpu bots</a> · 2026 F1 Predictions Tracker</div>',
    unsafe_allow_html=True,
)
