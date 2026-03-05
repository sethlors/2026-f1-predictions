import streamlit as st
import pandas as pd
from datetime import date
from utils.styles import inject_styles
from utils.data_helpers import (
    load_drivers,
    load_races,
    load_constructors,
    load_season_predictions,
    load_race_predictions,
    load_fun_predictions,
)
from utils.ui_helpers import (
    render_navbar,
    render_hero,
    render_countdown,
    render_stat_cards,
    render_nav_cards,
    render_section_header,
    render_race_calendar,
    render_divider,
    render_footer,
)

st.set_page_config(
    page_title="2026 F1 Predictions",
    page_icon="",
    layout="wide",
)

inject_styles()
st.markdown(render_navbar("home"), unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------
drivers_df = load_drivers()
races_df = load_races()
constructors_df = load_constructors()
season_df = load_season_predictions()
race_pred_df = load_race_predictions()
fun_pred_df = load_fun_predictions()

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
        countdown_text = "Race Day!"
    elif days_left == 1:
        countdown_text = "1 day away"
    else:
        countdown_text = f"{days_left} days away"
    st.markdown(
        render_countdown(next_race["Race Name"], countdown_text),
        unsafe_allow_html=True,
    )

# ---------------------------------------------------------------------------
# Hero
# ---------------------------------------------------------------------------
st.markdown(
    render_hero("2026 F1 Predictions", "Track your championship picks with friends"),
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Stats row
# ---------------------------------------------------------------------------
total_predictions = len(season_df) + len(race_pred_df) + len(fun_pred_df)
st.markdown(
    render_stat_cards([
        (len(drivers_df), "Drivers"),
        (len(constructors_df), "Teams"),
        (len(races_df), "Races"),
        (total_predictions, "Predictions"),
    ]),
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Navigation cards
# ---------------------------------------------------------------------------
st.markdown(
    render_nav_cards([
        ("", "Season Predictions",
         "Pick your full <strong>Drivers'</strong> and <strong>Constructors' Championships</strong> for 2026.",
         "/Season_Predictions"),
        ("", "Race Predictions",
         "Predict the <strong>P1 – P22</strong> finishing order for every Grand Prix.",
         "/Race_Predictions"),
        ("", "Fun Predictions",
         "Hot takes, wild guesses, and bold calls for the season.",
         "/Fun_Predictions"),
    ]),
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Race Calendar
# ---------------------------------------------------------------------------
st.markdown(render_section_header("2026 Race Calendar"), unsafe_allow_html=True)
st.markdown(render_race_calendar(races_df), unsafe_allow_html=True)

st.markdown(render_footer(), unsafe_allow_html=True)
