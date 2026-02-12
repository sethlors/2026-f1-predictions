import streamlit as st
import pandas as pd
from datetime import date
from utils.data_helpers import (
    load_drivers,
    load_races,
    load_constructors,
    load_season_predictions,
    load_race_predictions,
)

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
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&family=Racing+Sans+One&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background: #0a0a0a !important;
    }

    /* Checkered flag pattern for hero background */
    .hero {
        position: relative;
        background: linear-gradient(135deg, #e10600 0%, #8b0000 50%, #1e1e1e 100%);
        border-radius: 20px;
        padding: 3.5rem 3rem;
        margin-bottom: 2rem;
        color: white;
        overflow: hidden;
        box-shadow: 0 20px 60px rgba(225, 6, 0, 0.3), 0 0 0 1px rgba(255,255,255,0.1) inset;
    }
    .hero::before {
        content: '';
        position: absolute;
        top: 0;
        right: 0;
        width: 200px;
        height: 200px;
        background: 
            repeating-conic-gradient(rgba(255,255,255,0.03) 0% 25%, transparent 0% 50%) 
            50% / 40px 40px;
        opacity: 0.4;
        pointer-events: none;
    }
    .hero::after {
        content: '';
        position: absolute;
        bottom: -50%;
        left: -10%;
        width: 120%;
        height: 100%;
        background: linear-gradient(90deg, transparent 0%, rgba(255,255,255,0.03) 50%, transparent 100%);
        transform: skewY(-3deg);
        pointer-events: none;
    }
    .hero h1 {
        font-size: 3.5rem;
        font-weight: 900;
        margin: 0 0 0.5rem 0;
        letter-spacing: -2px;
        text-shadow: 0 4px 20px rgba(0,0,0,0.5);
        position: relative;
        z-index: 1;
    }
    .hero .subtitle {
        font-size: 1.3rem;
        opacity: 0.9;
        margin-top: 0;
        font-weight: 600;
        position: relative;
        z-index: 1;
        text-shadow: 0 2px 10px rgba(0,0,0,0.3);
    }

    .stat-row {
        display: flex;
        gap: 1.25rem;
        margin-bottom: 2rem;
        flex-wrap: wrap;
    }
    .stat-card {
        flex: 1;
        min-width: 160px;
        background: linear-gradient(135deg, #1a1a1a 0%, #151515 100%);
        border: 1px solid rgba(225, 6, 0, 0.2);
        border-radius: 16px;
        padding: 1.75rem 1.5rem;
        color: white;
        text-align: center;
        position: relative;
        overflow: hidden;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 20px rgba(0,0,0,0.4);
    }
    .stat-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #e10600, #ff6347);
        opacity: 0;
        transition: opacity 0.3s;
    }
    .stat-card:hover {
        transform: translateY(-4px);
        border-color: rgba(225, 6, 0, 0.5);
        box-shadow: 0 8px 30px rgba(225, 6, 0, 0.3), 0 0 0 1px rgba(225,6,0,0.3) inset;
    }
    .stat-card:hover::before {
        opacity: 1;
    }
    .stat-card .stat-value {
        font-size: 2.5rem;
        font-weight: 900;
        background: linear-gradient(135deg, #e10600 0%, #ff6347 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        filter: drop-shadow(0 2px 8px rgba(225, 6, 0, 0.4));
    }
    .stat-card .stat-label {
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        opacity: 0.6;
        margin-top: 0.5rem;
        font-weight: 600;
    }

    .nav-cards {
        display: flex;
        gap: 1.5rem;
        margin-top: 1.5rem;
        flex-wrap: wrap;
    }
    .nav-card {
        flex: 1;
        min-width: 280px;
        background: linear-gradient(135deg, #1a1a1a 0%, #151515 100%);
        border: 1px solid #2a2a2a;
        border-radius: 18px;
        padding: 2.5rem 2rem;
        color: white;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
        box-shadow: 0 4px 20px rgba(0,0,0,0.4);
    }
    .nav-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #e10600, #ff6347, #e10600);
        transform: translateX(-100%);
        transition: transform 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .nav-card::after {
        content: '';
        position: absolute;
        bottom: 20px;
        right: 20px;
        width: 100px;
        height: 100px;
        background: radial-gradient(circle, rgba(225,6,0,0.1) 0%, transparent 70%);
        pointer-events: none;
        opacity: 0;
        transition: opacity 0.3s;
    }
    .nav-card:hover {
        border-color: rgba(225, 6, 0, 0.4);
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(225, 6, 0, 0.25);
    }
    .nav-card:hover::before {
        transform: translateX(0);
    }
    .nav-card:hover::after {
        opacity: 1;
    }
    .nav-card h3 {
        margin: 0 0 0.75rem 0;
        font-weight: 800;
        font-size: 1.35rem;
        letter-spacing: -0.5px;
    }
    .nav-card p {
        margin: 0;
        opacity: 0.7;
        font-size: 0.95rem;
        line-height: 1.6;
    }

    .countdown-bar {
        background: linear-gradient(135deg, #e10600 0%, #c70000 50%, #8b0000 100%);
        border-radius: 16px;
        padding: 1.5rem 2rem;
        color: white;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 2rem;
        flex-wrap: wrap;
        gap: 1rem;
        position: relative;
        overflow: hidden;
        box-shadow: 0 8px 30px rgba(225, 6, 0, 0.4), 0 0 0 1px rgba(255,255,255,0.1) inset;
    }
    .countdown-bar::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -10%;
        width: 200px;
        height: 200px;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: pulse 4s ease-in-out infinite;
    }
    @keyframes pulse {
        0%, 100% { transform: scale(1); opacity: 0.5; }
        50% { transform: scale(1.2); opacity: 0.8; }
    }
    .countdown-bar .race-name {
        font-weight: 800;
        font-size: 1.2rem;
        letter-spacing: -0.3px;
        position: relative;
        z-index: 1;
    }
    .countdown-bar .days-left {
        font-weight: 900;
        font-size: 1.5rem;
        background: rgba(255,255,255,0.2);
        padding: 0.3rem 1rem;
        border-radius: 8px;
        position: relative;
        z-index: 1;
        backdrop-filter: blur(10px);
    }

    .footer {
        text-align: center;
        opacity: 0.35;
        font-size: 0.8rem;
        margin-top: 4rem;
        padding-bottom: 1.5rem;
    }
    .footer a {
        transition: opacity 0.2s;
    }
    .footer a:hover {
        opacity: 1;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------
drivers_df = load_drivers()
races_df = load_races()
constructors_df = load_constructors()
season_df = load_season_predictions()
race_pred_df = load_race_predictions()

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
