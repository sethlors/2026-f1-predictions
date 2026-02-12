import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Season Predictions", page_icon="", layout="wide")

# ---------------------------------------------------------------------------
# CSS
# ---------------------------------------------------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    .page-header {
        background: linear-gradient(135deg, #e10600 0%, #1e1e1e 60%);
        border-radius: 14px;
        padding: 2rem 2.5rem;
        margin-bottom: 1.5rem;
        color: white;
    }
    .page-header h1 { font-size: 2.2rem; font-weight: 900; margin: 0; letter-spacing: -0.5px; }
    .page-header p  { opacity: 0.8; margin: 0.25rem 0 0 0; }

    .form-card {
        background: #1e1e1e;
        border: 1px solid #333;
        border-radius: 14px;
        padding: 1.75rem;
        color: white;
        margin-bottom: 1.5rem;
    }
    .form-card h3 { margin: 0 0 0.25rem 0; font-weight: 700; }
    .form-card .form-hint { opacity: 0.55; font-size: 0.88rem; margin-bottom: 1rem; }

    .pred-grid {
        display: flex;
        gap: 1rem;
        flex-wrap: wrap;
    }
    .pred-card {
        flex: 1;
        min-width: 250px;
        background: #1e1e1e;
        border: 1px solid #333;
        border-radius: 14px;
        padding: 1.5rem;
        color: white;
        text-align: center;
    }
    .pred-card .user-name {
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        opacity: 0.6;
    }
    .pred-card .pick-label {
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        opacity: 0.5;
        margin-top: 1rem;
    }
    .pred-card .pick-value {
        font-size: 1.15rem;
        font-weight: 700;
        color: #e10600;
        margin-top: 0.15rem;
    }

    .team-badge {
        display: inline-block;
        padding: 2px 10px;
        border-radius: 6px;
        font-size: 0.78rem;
        font-weight: 600;
        color: white;
        margin-left: 6px;
        vertical-align: middle;
    }

    /* Red trash-can delete button */
    .trash-btn {
        display: flex;
        justify-content: flex-end;
        margin-top: -2.8rem;
        margin-bottom: 1.2rem;
        padding-right: 0.75rem;
    }
    .trash-btn button {
        background: transparent !important;
        border: none !important;
        color: #e10600 !important;
        font-size: 0.95rem !important;
        padding: 0.1rem 0.4rem !important;
        min-height: 0 !important;
        line-height: 1 !important;
        opacity: 0.35;
        transition: opacity 0.15s;
        cursor: pointer;
    }
    .trash-btn button:hover {
        opacity: 1;
        background: transparent !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

USERS = ["Seth", "Colin"]
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

TEAM_COLORS = {
    "McLaren": "#FF8700", "Mercedes": "#00D2BE", "Red Bull": "#1E41FF",
    "Ferrari": "#DC0000", "Williams": "#005AFF", "Racing Bulls": "#2B4562",
    "Aston Martin": "#006F62", "Haas": "#B6BABD", "Audi": "#C0C0C0",
    "Alpine": "#0090FF", "Cadillac": "#FFD700",
}


def load_drivers():
    return pd.read_csv(os.path.join(DATA_DIR, "drivers.csv"))


def load_constructors():
    return pd.read_csv(os.path.join(DATA_DIR, "constructors.csv"))


def load_season_predictions():
    return pd.read_csv(os.path.join(DATA_DIR, "season_predictions.csv"))


def save_season_predictions(df: pd.DataFrame):
    df.to_csv(os.path.join(DATA_DIR, "season_predictions.csv"), index=False)


def driver_with_team(name: str, drivers_df: pd.DataFrame) -> str:
    """Return 'Name  (Team)' for display."""
    row = drivers_df[drivers_df["Driver Name"] == name]
    if row.empty:
        return name
    team = row.iloc[0]["Driver Team"]
    return f"{name}  —  {team}"


# ---------------------------------------------------------------------------
# UI
# ---------------------------------------------------------------------------

# Header
st.markdown(
    """
    <div class="page-header">
        <h1>Season Predictions</h1>
    </div>
    """,
    unsafe_allow_html=True,
)

drivers_df = load_drivers()
constructors_df = load_constructors()
season_df = load_season_predictions()

driver_names = drivers_df["Driver Name"].tolist()
constructor_names = constructors_df["Team Name"].tolist()

# Build display labels:  "Name  —  Team"
driver_display = [driver_with_team(d, drivers_df) for d in driver_names]

# --- Form card ---
st.markdown(
    '<div class="form-card"><h3>Make Your Pick</h3>'
    '<div class="form-hint">Select a user and choose your drivers.</div></div>',
    unsafe_allow_html=True,
)

col_user, _ = st.columns([1, 2])
with col_user:
    user = st.selectbox("User", USERS, key="season_user")

# Pre-fill
existing = season_df[season_df["user"] == user]
default_driver_idx = 0
default_constructor_idx = 0
if not existing.empty:
    row = existing.iloc[0]
    if row["drivers_champion"] in driver_names:
        default_driver_idx = driver_names.index(row["drivers_champion"])
    if row["constructors_champion"] in constructor_names:
        default_constructor_idx = constructor_names.index(row["constructors_champion"])

col1, col2 = st.columns(2)
with col1:
    driver_idx = st.selectbox(
        "Drivers' Champion",
        range(len(driver_names)),
        format_func=lambda i: driver_display[i],
        index=default_driver_idx,
        key="season_driver",
    )
    drivers_champion = driver_names[driver_idx]

with col2:
    constructors_champion = st.selectbox(
        "Constructors' Champion",
        constructor_names,
        index=default_constructor_idx,
        key="season_constructor",
    )

st.markdown("")
submit_season = st.button("Submit Season Prediction", type="primary", use_container_width=True)

if submit_season:
    season_df = load_season_predictions()
    mask = season_df["user"] == user
    new_row = {
        "user": user,
        "drivers_champion": drivers_champion,
        "constructors_champion": constructors_champion,
    }
    if mask.any():
        for col, val in new_row.items():
            season_df.loc[mask, col] = val
    else:
        season_df = pd.concat([season_df, pd.DataFrame([new_row])], ignore_index=True)
    save_season_predictions(season_df)
    st.success(f"Season prediction saved for **{user}**!")

# ---------------------------------------------------------------------------
# Display current predictions as styled cards
# ---------------------------------------------------------------------------
st.markdown("---")
st.markdown("### Current Predictions")

season_df = load_season_predictions()

if season_df.empty:
    st.info("No season predictions yet — be the first!")
else:
    season_df_display = season_df.reset_index()  # keeps original index for deletion
    
    # Calculate number of columns needed
    num_cards = len(season_df_display)
    cols = st.columns(num_cards)
    
    for col_idx, (_, row) in enumerate(season_df_display.iterrows()):
        with cols[col_idx]:
            driver_team = ""
            d_row = drivers_df[drivers_df["Driver Name"] == row["drivers_champion"]]
            if not d_row.empty:
                driver_team = d_row.iloc[0]["Driver Team"]
            team_color = TEAM_COLORS.get(driver_team, "#555")
            cons_color = TEAM_COLORS.get(row["constructors_champion"], "#555")

            st.markdown(
                f"""
                <div class="pred-card">
                    <div class="user-name">{row['user']}</div>
                    <div class="pick-label">Drivers' Champion</div>
                    <div class="pick-value">{row['drivers_champion']}
                        <span class="team-badge" style="background:{team_color}">{driver_team}</span>
                    </div>
                    <div class="pick-label">Constructors' Champion</div>
                    <div class="pick-value" style="color:{cons_color}">{row['constructors_champion']}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            trash_icon = "\u2715"  # small X mark
            st.markdown('<div class="trash-btn">', unsafe_allow_html=True)
            if st.button(trash_icon, key=f"del_season_{row['index']}"):
                season_df = load_season_predictions()
                season_df = season_df.drop(index=row["index"]).reset_index(drop=True)
                save_season_predictions(season_df)
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
