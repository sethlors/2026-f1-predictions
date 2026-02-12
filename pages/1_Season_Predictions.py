import streamlit as st
import pandas as pd
from utils.constants import (
    USERS,
    DRIVER_POSITIONS,
    CONSTRUCTOR_POSITIONS,
    PLACEHOLDER,
)
from utils.data_helpers import (
    load_drivers,
    load_constructors,
    load_season_predictions,
    save_season_predictions,
)
from utils.styles import COMMON_STYLES, SEASON_PREDICTIONS_STYLES, PREDICTION_CARD_STYLES
from utils.ui_helpers import driver_with_team, pos_class, render_page_header

st.set_page_config(page_title="Season Predictions", page_icon="", layout="wide")

# ---------------------------------------------------------------------------
# CSS
# ---------------------------------------------------------------------------
st.markdown(COMMON_STYLES, unsafe_allow_html=True)
st.markdown(SEASON_PREDICTIONS_STYLES, unsafe_allow_html=True)
st.markdown(PREDICTION_CARD_STYLES, unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# UI
# ---------------------------------------------------------------------------

# Header
st.markdown(
    render_page_header(
        "Season Predictions",
        "Predict the full Drivers' and Constructors' Championships for 2026."
    ),
    unsafe_allow_html=True,
)

drivers_df = load_drivers()
constructors_df = load_constructors()
season_df = load_season_predictions()

driver_names = drivers_df["Driver Name"].tolist()
constructor_names = constructors_df["Team Name"].tolist()
driver_teams = dict(zip(drivers_df["Driver Name"], drivers_df["Driver Team"]))

# --- User selector ---
col_user, _ = st.columns([1, 2])
with col_user:
    user = st.selectbox("User", USERS, key="season_user")

# --- Pre-fill logic ---
existing = season_df[season_df["user"] == user]
prefilled_drivers: dict[str, str] = {}
prefilled_constructors: dict[str, str] = {}
if not existing.empty:
    row = existing.iloc[0]
    for pos in DRIVER_POSITIONS:
        val = str(row.get(pos, ""))
        if val in driver_names:
            prefilled_drivers[pos] = val
    for pos in CONSTRUCTOR_POSITIONS:
        val = str(row.get(pos, ""))
        if val in constructor_names:
            prefilled_constructors[pos] = val

# ---------------------------------------------------------------------------
# Initialize session-state selections (once per user)
# ---------------------------------------------------------------------------
state_key = f"_season_init_{user}"
if st.session_state.get(state_key) != user:
    # Reset all position keys in session state
    for pos in DRIVER_POSITIONS:
        widget_key = f"season_driver_{pos}"
        if pos in prefilled_drivers:
            st.session_state[widget_key] = prefilled_drivers[pos]
        else:
            st.session_state[widget_key] = PLACEHOLDER
    for pos in CONSTRUCTOR_POSITIONS:
        widget_key = f"season_constructor_{pos}"
        if pos in prefilled_constructors:
            st.session_state[widget_key] = prefilled_constructors[pos]
        else:
            st.session_state[widget_key] = PLACEHOLDER
    st.session_state[state_key] = user

# ---------------------------------------------------------------------------
# Build the set of already-selected drivers/constructors (for filtering)
# ---------------------------------------------------------------------------
def get_selected_drivers(exclude_pos: str) -> set[str]:
    """Return drivers currently selected in other positions."""
    selected = set()
    for p in DRIVER_POSITIONS:
        if p == exclude_pos:
            continue
        val = st.session_state.get(f"season_driver_{p}", PLACEHOLDER)
        if val != PLACEHOLDER:
            selected.add(val)
    return selected


def get_selected_constructors(exclude_pos: str) -> set[str]:
    """Return constructors currently selected in other positions."""
    selected = set()
    for p in CONSTRUCTOR_POSITIONS:
        if p == exclude_pos:
            continue
        val = st.session_state.get(f"season_constructor_{p}", PLACEHOLDER)
        if val != PLACEHOLDER:
            selected.add(val)
    return selected

# ---------------------------------------------------------------------------
# Championships Side-by-Side
# ---------------------------------------------------------------------------
col_drivers, col_constructors = st.columns(2)

# ---------------------------------------------------------------------------
# Drivers' Championship
# ---------------------------------------------------------------------------
with col_drivers:
    st.markdown('<div class="championship-section"><h3>Drivers\' Championship</h3><div class="championship-body">', unsafe_allow_html=True)

    driver_selections: dict[str, str] = {}

    for i, pos in enumerate(DRIVER_POSITIONS):
        pc = pos_class(i + 1)
        
        # Drivers available for this slot
        already_taken = get_selected_drivers(pos)
        current_val = st.session_state.get(f"season_driver_{pos}", PLACEHOLDER)
        
        available = [d for d in driver_names if d not in already_taken or d == current_val]
        options = [PLACEHOLDER] + available
        display_options = [PLACEHOLDER] + [driver_with_team(d, drivers_df) for d in available]
        
        # Determine current index
        if current_val in options:
            idx = options.index(current_val)
        else:
            idx = 0
        
        col_label, col_select = st.columns([0.2, 4], gap="small")
        with col_label:
            position_num = i + 1
            st.markdown(
                f'<div style="padding-top:0.45rem"><span class="pos-label {pc}">P{position_num}</span></div>',
                unsafe_allow_html=True,
            )
        with col_select:
            chosen = st.selectbox(
                f"Driver Position {position_num}",
                options,
                format_func=lambda v, _opts=options, _disp=display_options: _disp[_opts.index(v)],
                index=idx,
                key=f"season_driver_{pos}",
                label_visibility="collapsed",
            )
        driver_selections[pos] = chosen

    # --- Submit Drivers' Championship ---
    st.markdown("")
    submit_drivers = st.button("Submit Drivers' Championship", type="primary", use_container_width=True, key="submit_drivers")

    if submit_drivers:
        driver_chosen_list = list(driver_selections.values())
        
        # Check for empty slots
        empty_driver_slots = [p for p, v in driver_selections.items() if v == PLACEHOLDER]
        
        if empty_driver_slots:
            st.error(f"Missing driver selections: **{', '.join(empty_driver_slots)}**. Every position must have a driver.")
        else:
            # Duplicate check (should be impossible with filtering, but just in case)
            driver_dupes = set([d for d in driver_chosen_list if driver_chosen_list.count(d) > 1 and d != PLACEHOLDER])
            
            if driver_dupes:
                st.error(f"Duplicate drivers: **{', '.join(sorted(driver_dupes))}**. Each driver must appear exactly once.")
            else:
                season_df = load_season_predictions()
                mask = season_df["user"] == user
                new_row = {"user": user, **driver_selections}
                if mask.any():
                    for col_name, val in driver_selections.items():
                        season_df.loc[mask, col_name] = val
                else:
                    # Need to create full row with placeholders for constructors
                    full_row = {"user": user, **driver_selections}
                    for pos in CONSTRUCTOR_POSITIONS:
                        full_row[pos] = PLACEHOLDER
                    season_df = pd.concat([season_df, pd.DataFrame([full_row])], ignore_index=True)
                save_season_predictions(season_df)
                st.success(f"Drivers' Championship prediction saved for **{user}**!")
    
    st.markdown('</div></div>', unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Constructors' Championship
# ---------------------------------------------------------------------------
with col_constructors:
    st.markdown('<div class="championship-section"><h3>Constructors\' Championship</h3><div class="championship-body">', unsafe_allow_html=True)

    constructor_selections: dict[str, str] = {}
    for i, pos in enumerate(CONSTRUCTOR_POSITIONS):
        pc = pos_class(i + 1)
        
        # Constructors available for this slot
        already_taken = get_selected_constructors(pos)
        current_val = st.session_state.get(f"season_constructor_{pos}", PLACEHOLDER)
        
        available = [c for c in constructor_names if c not in already_taken or c == current_val]
        options = [PLACEHOLDER] + available
        
        # Determine current index
        if current_val in options:
            idx = options.index(current_val)
        else:
            idx = 0
        
        col_label, col_select = st.columns([0.2, 4], gap="small")
        with col_label:
            position_num = i + 1
            st.markdown(
                f'<div style="padding-top:0.45rem"><span class="pos-label {pc}">P{position_num}</span></div>',
                unsafe_allow_html=True,
            )
        with col_select:
            chosen = st.selectbox(
                f"Constructor Position {position_num}",
                options,
                index=idx,
                key=f"season_constructor_{pos}",
                label_visibility="collapsed",
            )
        constructor_selections[pos] = chosen

    # --- Submit Constructors' Championship ---
    st.markdown("")
    submit_constructors = st.button("Submit Constructors' Championship", type="primary", use_container_width=True, key="submit_constructors")

    if submit_constructors:
        constructor_chosen_list = list(constructor_selections.values())
        
        # Check for empty slots
        empty_constructor_slots = [p for p, v in constructor_selections.items() if v == PLACEHOLDER]
        
        if empty_constructor_slots:
            st.error(f"Missing constructor selections: **{', '.join(empty_constructor_slots)}**. Every position must have a constructor.")
        else:
            # Duplicate check (should be impossible with filtering, but just in case)
            constructor_dupes = set([c for c in constructor_chosen_list if constructor_chosen_list.count(c) > 1 and c != PLACEHOLDER])
            
            if constructor_dupes:
                st.error(f"Duplicate constructors: **{', '.join(sorted(constructor_dupes))}**. Each constructor must appear exactly once.")
            else:
                season_df = load_season_predictions()
                mask = season_df["user"] == user
                new_row = {"user": user, **constructor_selections}
                if mask.any():
                    for col_name, val in constructor_selections.items():
                        season_df.loc[mask, col_name] = val
                else:
                    # Need to create full row with placeholders for drivers
                    full_row = {"user": user}
                    for pos in DRIVER_POSITIONS:
                        full_row[pos] = PLACEHOLDER
                    for pos in CONSTRUCTOR_POSITIONS:
                        full_row[pos] = constructor_selections[pos]
                    season_df = pd.concat([season_df, pd.DataFrame([full_row])], ignore_index=True)
                save_season_predictions(season_df)
            st.success(f"Constructors' Championship prediction saved for **{user}**!")
    
    st.markdown('</div></div>', unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Display current predictions
# ---------------------------------------------------------------------------
st.markdown("---")
st.markdown("### Current Predictions")

season_df = load_season_predictions()

if season_df.empty:
    st.info("No season predictions yet — be the first!")
else:
    season_df_display = season_df.reset_index()  # keeps original index for deletion
    display_cols = st.columns(len(season_df_display))
    
    for idx, (_, pred_row) in enumerate(season_df_display.iterrows()):
        with display_cols[idx]:
            # Drivers' Championship
            html = f'<div class="user-col-header">{pred_row["user"]} — Drivers</div>'
            for i, pos in enumerate(DRIVER_POSITIONS, 1):
                driver = pred_row.get(pos, "")
                if driver and driver != PLACEHOLDER:
                    team = driver_teams.get(driver, "")
                    color = TEAM_COLORS.get(team, "#555")
                    pc = pos_class(i)
                    html += (
                        f'<div class="result-row">'
                        f'<span class="result-pos"><span class="pos-label {pc}">P{i}</span></span>'
                        f'<span class="result-driver">{driver}</span>'
                        f'<span class="result-team" style="color:{color}; opacity:1;">{team}</span>'
                        f'</div>'
                    )
            
            # Constructors' Championship
            html += f'<div class="user-col-header" style="margin-top:1.5rem;">{pred_row["user"]} — Constructors</div>'
            for i, pos in enumerate(CONSTRUCTOR_POSITIONS, 1):
                constructor = pred_row.get(pos, "")
                if constructor and constructor != PLACEHOLDER:
                    color = TEAM_COLORS.get(constructor, "#555")
                    pc = pos_class(i)
                    html += (
                        f'<div class="result-row">'
                        f'<span class="result-pos"><span class="pos-label {pc}">P{i}</span></span>'
                        f'<span class="result-driver" style="color:{color}; opacity:1;">{constructor}</span>'
                        f'</div>'
                    )
            
            st.markdown(html, unsafe_allow_html=True)
            
            trash_icon = "\u2715"  # small X mark
            st.markdown('<div class="trash-btn">', unsafe_allow_html=True)
            if st.button(trash_icon, key=f"del_season_{pred_row['index']}"):
                season_df = load_season_predictions()
                season_df = season_df.drop(index=pred_row["index"]).reset_index(drop=True)
                save_season_predictions(season_df)
                # Clear the session-state init key so dropdowns reset on rerun
                state_key_del = f"_season_init_{pred_row['user']}"
                if state_key_del in st.session_state:
                    del st.session_state[state_key_del]
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
