import streamlit as st
import pandas as pd
from utils.constants import USERS, PLACEHOLDER
from utils.data_helpers import load_drivers, load_races, load_race_predictions, save_race_predictions
from utils.styles import COMMON_STYLES, PREDICTION_CARD_STYLES
from utils.ui_helpers import pos_class, render_page_header

st.set_page_config(page_title="Race Predictions", page_icon="", layout="wide")

# ---------------------------------------------------------------------------
# CSS
# ---------------------------------------------------------------------------
st.markdown(COMMON_STYLES, unsafe_allow_html=True)
st.markdown(PREDICTION_CARD_STYLES, unsafe_allow_html=True)
st.markdown(
    """
    <style>

    .page-header {
        background: linear-gradient(135deg, #e10600 0%, #8b0000 50%, #1e1e1e 100%);
        border-radius: 18px;
        padding: 2.5rem 3rem;
        margin-bottom: 2rem;
        color: white;
        box-shadow: 0 12px 40px rgba(225, 6, 0, 0.35), 0 0 0 1px rgba(255,255,255,0.08) inset;
        position: relative;
        overflow: hidden;
    }
    .page-header::before {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        height: 100px;
        background: linear-gradient(90deg, transparent 0%, rgba(255,255,255,0.02) 50%, transparent 100%);
        transform: skewY(-2deg);
    }
    .page-header h1 { 
        font-size: 2.5rem; 
        font-weight: 900; 
        margin: 0; 
        letter-spacing: -1px;
        text-shadow: 0 2px 10px rgba(0,0,0,0.3);
        position: relative;
    }
    .page-header p { 
        opacity: 0.85; 
        margin: 0.4rem 0 0 0;
        font-size: 1.05rem;
        font-weight: 500;
        position: relative;
    }

    .pos-label {
        display: inline-block;
        width: 40px;
        text-align: center;
        font-weight: 800;
        font-size: 0.8rem;
        border-radius: 8px;
        padding: 3px 0;
        margin-right: 6px;
        color: white;
        box-shadow: 0 2px 8px rgba(0,0,0,0.3);
        transition: transform 0.2s;
    }
    .pos-label:hover { transform: scale(1.05); }
    .pos-gold   { background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%); color: #1e1e1e; box-shadow: 0 2px 12px rgba(255,215,0,0.5); }
    .pos-silver { background: linear-gradient(135deg, #E8E8E8 0%, #C0C0C0 100%); color: #1e1e1e; box-shadow: 0 2px 12px rgba(192,192,192,0.5); }
    .pos-bronze { background: linear-gradient(135deg, #CD7F32 0%, #8B4513 100%); color: white; box-shadow: 0 2px 12px rgba(205,127,50,0.4); }
    .pos-points { background: linear-gradient(135deg, #2d6a4f 0%, #1b4332 100%); box-shadow: 0 2px 10px rgba(45,106,79,0.4); }
    .pos-rest   { background: linear-gradient(135deg, #444 0%, #2a2a2a 100%); }

    .user-col-header {
        font-weight: 800;
        font-size: 1.1rem;
        padding: 1rem 0 0.5rem 0;
        border-bottom: 3px solid #e10600;
        margin-bottom: 0.75rem;
        letter-spacing: -0.3px;
        background: linear-gradient(90deg, rgba(225,6,0,0.1) 0%, transparent 100%);
        padding-left: 0.5rem;
        border-radius: 4px 4px 0 0;
    }
    .result-row {
        display: flex;
        align-items: center;
        padding: 6px 10px;
        border-radius: 8px;
        margin-bottom: 3px;
        font-size: 0.9rem;
        transition: background 0.2s;
        border: 1px solid transparent;
    }
    .result-row:nth-child(odd) { background: rgba(255,255,255,0.02); }
    .result-row:hover { 
        background: rgba(225,6,0,0.08); 
        border-color: rgba(225,6,0,0.2);
    }
    .result-pos {
        width: 40px;
        font-weight: 800;
        flex-shrink: 0;
        margin-right: 1rem;
    }
    .result-driver { 
        flex: 1;
        font-weight: 600;
    }
    .result-team {
        font-size: 0.75rem;
        opacity: 0.6;
        padding-left: 10px;
        font-weight: 600;
    }
    .team-dot {
        display: inline-block;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        margin-right: 6px;
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

# Data will be loaded using utility functions
NUM_POSITIONS = 22
POSITIONS = [f"P{i}" for i in range(1, NUM_POSITIONS + 1)]


def driver_with_team(name: str, drivers_df: pd.DataFrame) -> str:
    row = drivers_df[drivers_df["Driver Name"] == name]
    if row.empty:
        return name
    return f"{name}  —  {row.iloc[0]['Driver Team']}"


# ---------------------------------------------------------------------------
# UI
# ---------------------------------------------------------------------------

st.markdown(
    """
    <div class="page-header">
        <h1>Race Predictions</h1>
        <p>Predict the full finishing order for each Grand Prix.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

drivers_df = load_drivers()
races_df = load_races()
race_pred_df = load_race_predictions()

driver_names = drivers_df["Driver Name"].tolist()
driver_teams = dict(zip(drivers_df["Driver Name"], drivers_df["Driver Team"]))

race_labels = races_df.apply(
    lambda r: f"{r['Round Number']}  —  {r['Race Name']}", axis=1
).tolist()
race_name_list = races_df["Race Name"].tolist()

# --- Selectors ---
sel_col1, sel_col2 = st.columns([1, 2])
with sel_col1:
    user = st.selectbox("User", USERS, key="race_user")
with sel_col2:
    selected_label = st.selectbox("Race", race_labels, key="race_select")

selected_race = race_name_list[race_labels.index(selected_label)]

# --- Pre-fill logic ---
existing = race_pred_df[
    (race_pred_df["race"] == selected_race) & (race_pred_df["user"] == user)
]
prefilled: dict[str, str] = {}
if not existing.empty:
    row = existing.iloc[0]
    for pos in POSITIONS:
        val = str(row.get(pos, ""))
        if val in driver_names:
            prefilled[pos] = val

# ---------------------------------------------------------------------------
# Initialise session-state selections (once per user+race combo)
# ---------------------------------------------------------------------------
state_key = f"_race_init_{user}_{selected_race}"
if st.session_state.get(state_key) != (user, selected_race):
    # Reset all position keys in session state
    for pos in POSITIONS:
        widget_key = f"race_{pos}"
        if pos in prefilled:
            st.session_state[widget_key] = prefilled[pos]
        else:
            st.session_state[widget_key] = PLACEHOLDER
    st.session_state[state_key] = (user, selected_race)

# ---------------------------------------------------------------------------
# Build the set of already-selected drivers (for filtering)
# ---------------------------------------------------------------------------
def get_selected_drivers(exclude_pos: str) -> set[str]:
    """Return drivers currently selected in other positions."""
    selected = set()
    for p in POSITIONS:
        if p == exclude_pos:
            continue
        val = st.session_state.get(f"race_{p}", PLACEHOLDER)
        if val != PLACEHOLDER:
            selected.add(val)
    return selected

# --- Position dropdowns — single-column vertical list ---
st.markdown("### Predicted Finishing Order")

selections: dict[str, str] = {}

for i, pos in enumerate(POSITIONS):
    pc = pos_class(i + 1)

    # Drivers available for this slot = all drivers minus those picked elsewhere
    already_taken = get_selected_drivers(pos)
    current_val = st.session_state.get(f"race_{pos}", PLACEHOLDER)

    available = [d for d in driver_names if d not in already_taken or d == current_val]
    options = [PLACEHOLDER] + available
    display_options = [PLACEHOLDER] + [driver_with_team(d, drivers_df) for d in available]

    # Determine current index
    if current_val in options:
        idx = options.index(current_val)
    else:
        idx = 0

    col_label, col_select = st.columns([0.1, 4], gap="small")
    with col_label:
        st.markdown(
            f'<div style="padding-top:0.45rem"><span class="pos-label {pc}">{pos}</span></div>',
            unsafe_allow_html=True,
        )
    with col_select:
        chosen = st.selectbox(
            pos,
            options,
            format_func=lambda v, _opts=options, _disp=display_options: _disp[_opts.index(v)],
            index=idx,
            key=f"race_{pos}",
            label_visibility="collapsed",
        )
    selections[pos] = chosen

# --- Submit ---
st.markdown("")
submit_race = st.button("Submit Race Prediction", type="primary", use_container_width=True)

if submit_race:
    chosen_list = list(selections.values())

    # Check for empty slots
    empty_slots = [p for p, v in selections.items() if v == PLACEHOLDER]
    if empty_slots:
        st.error(
            f"Missing selections for: **{', '.join(empty_slots)}**. "
            "Every position must have a driver."
        )
    else:
        # Duplicate check (should be impossible with filtering, but just in case)
        if len(set(chosen_list)) != len(chosen_list):
            seen: set[str] = set()
            dupes: set[str] = set()
            for d in chosen_list:
                if d in seen:
                    dupes.add(d)
                seen.add(d)
            st.error(
                f"Duplicate drivers: **{', '.join(sorted(dupes))}**. "
                "Each driver must appear exactly once."
            )
        else:
            race_pred_df = load_race_predictions()
            mask = (race_pred_df["race"] == selected_race) & (
                race_pred_df["user"] == user
            )
            new_row = {"race": selected_race, "user": user, **selections}
            if mask.any():
                for col_name, val in new_row.items():
                    race_pred_df.loc[mask, col_name] = val
            else:
                race_pred_df = pd.concat(
                    [race_pred_df, pd.DataFrame([new_row])], ignore_index=True
                )
            save_race_predictions(race_pred_df)
            st.success(f"Prediction for **{selected_race}** saved for **{user}**!")

# ---------------------------------------------------------------------------
# Display predictions for selected race
# ---------------------------------------------------------------------------
st.markdown("---")
st.markdown(f"### Predictions for {selected_race}")

race_pred_df = load_race_predictions()
filtered = race_pred_df[race_pred_df["race"] == selected_race]

if filtered.empty:
    st.info("No predictions yet for this race.")
else:
    filtered_display = filtered.reset_index()  # keeps original index for deletion
    display_cols = st.columns(len(filtered_display))
    for idx, (_, pred_row) in enumerate(filtered_display.iterrows()):
        with display_cols[idx]:
            html = f'<div class="user-col-header">{pred_row["user"]}</div>'
            for i, pos in enumerate(POSITIONS, 1):
                driver = pred_row.get(pos, "")
                team = driver_teams.get(driver, "")
                color = TEAM_COLORS.get(team, "#555")
                pc = pos_class(i)
                html += (
                    f'<div class="result-row">'
                    f'<span class="result-pos"><span class="pos-label {pc}">{pos}</span></span>'
                    f'<span class="result-driver">{driver}</span>'
                    f'<span class="result-team" style="color:{color}; opacity:1;">{team}</span>'
                    f'</div>'
                )
            st.markdown(html, unsafe_allow_html=True)
            
            trash_icon = "\u2715"  # small X mark
            st.markdown('<div class="trash-btn">', unsafe_allow_html=True)
            if st.button(trash_icon, key=f"del_race_{pred_row['index']}"):
                race_pred_df = load_race_predictions()
                race_pred_df = race_pred_df.drop(index=pred_row["index"]).reset_index(drop=True)
                save_race_predictions(race_pred_df)
                # Clear the session-state init key so dropdowns reset on rerun
                state_key_del = f"_race_init_{pred_row['user']}_{selected_race}"
                if state_key_del in st.session_state:
                    del st.session_state[state_key_del]
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
