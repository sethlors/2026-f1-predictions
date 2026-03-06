import streamlit as st
from utils.constants import (
    USERS,
    DRIVER_POSITIONS,
    CONSTRUCTOR_POSITIONS,
    PLACEHOLDER,
    TEAM_COLORS,
)
from utils.data_helpers import (
    load_drivers,
    load_constructors,
    load_season_predictions,
    upsert_season_prediction,
    delete_season_prediction,
)
from utils.styles import inject_styles
from utils.ui_helpers import (
    driver_with_team,
    pos_class,
    render_navbar,
    render_page_header,
    render_section_header,
    render_divider,
    render_timing_tower,
    render_podium,
    render_footer,
    render_toast,
    render_empty_state,
)

st.set_page_config(page_title="Season Predictions", page_icon="", layout="wide")
inject_styles()
st.markdown(render_navbar("season"), unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
st.markdown(
    render_page_header(
        "Season Predictions",
        "Predict the full Drivers' and Constructors' Championships for 2026.",
    ),
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------
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
    for pos in DRIVER_POSITIONS:
        st.session_state[f"season_driver_{pos}"] = prefilled_drivers.get(pos, PLACEHOLDER)
    for pos in CONSTRUCTOR_POSITIONS:
        st.session_state[f"season_constructor_{pos}"] = prefilled_constructors.get(pos, PLACEHOLDER)
    st.session_state[state_key] = user

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def get_selected_drivers(exclude_pos: str) -> set[str]:
    selected = set()
    for p in DRIVER_POSITIONS:
        if p == exclude_pos:
            continue
        val = st.session_state.get(f"season_driver_{p}", PLACEHOLDER)
        if val != PLACEHOLDER:
            selected.add(val)
    return selected


def get_selected_constructors(exclude_pos: str) -> set[str]:
    selected = set()
    for p in CONSTRUCTOR_POSITIONS:
        if p == exclude_pos:
            continue
        val = st.session_state.get(f"season_constructor_{p}", PLACEHOLDER)
        if val != PLACEHOLDER:
            selected.add(val)
    return selected


def calculate_constructor_standings_from_drivers() -> list[str]:
    team_positions: dict[str, list[int]] = {}
    for i, pos in enumerate(DRIVER_POSITIONS):
        driver = st.session_state.get(f"season_driver_{pos}", PLACEHOLDER)
        if driver != PLACEHOLDER and driver in driver_teams:
            team = driver_teams[driver]
            team_positions.setdefault(team, []).append(i + 1)
    team_scores = {}
    for team, positions in team_positions.items():
        positions.sort()
        team_scores[team] = sum(positions[:2])
    return [team for team, _ in sorted(team_scores.items(), key=lambda x: x[1])]


def auto_populate_constructors():
    constructor_order = calculate_constructor_standings_from_drivers()
    if len(constructor_order) >= len(CONSTRUCTOR_POSITIONS):
        filled = sum(
            1 for pos in CONSTRUCTOR_POSITIONS
            if st.session_state.get(f"season_constructor_{pos}", PLACEHOLDER) != PLACEHOLDER
        )
        if filled < len(CONSTRUCTOR_POSITIONS) / 2:
            for i, pos in enumerate(CONSTRUCTOR_POSITIONS):
                if i < len(constructor_order):
                    st.session_state[f"season_constructor_{pos}"] = constructor_order[i]


# ---------------------------------------------------------------------------
# Championships Side-by-Side
# ---------------------------------------------------------------------------
col_drivers, col_constructors = st.columns(2)

# --- Drivers' Championship ---
with col_drivers:
    st.markdown(
        '<div class="championship-section"><h3>Drivers\' Championship</h3>'
        '<div class="championship-body">',
        unsafe_allow_html=True,
    )

    driver_selections: dict[str, str] = {}

    for i, pos in enumerate(DRIVER_POSITIONS):
        pc = pos_class(i + 1)
        already_taken = get_selected_drivers(pos)
        current_val = st.session_state.get(f"season_driver_{pos}", PLACEHOLDER)

        available = [d for d in driver_names if d not in already_taken or d == current_val]
        options = [PLACEHOLDER] + available
        display_options = [PLACEHOLDER] + [driver_with_team(d, drivers_df) for d in available]

        idx = options.index(current_val) if current_val in options else 0

        col_label, col_select = st.columns([0.2, 4], gap="small")
        with col_label:
            st.markdown(
                f'<div style="padding-top:0.45rem"><span class="pos-label {pc}">P{i+1}</span></div>',
                unsafe_allow_html=True,
            )
        with col_select:
            chosen = st.selectbox(
                f"Driver Position {i+1}",
                options,
                format_func=lambda v, _o=options, _d=display_options: _d[_o.index(v)],
                key=f"season_driver_{pos}",
                label_visibility="collapsed",
            )
        driver_selections[pos] = chosen

    st.markdown("")
    if st.button("Submit Drivers' Championship", type="primary", use_container_width=True, key="submit_drivers"):
        empty_slots = [p for p, v in driver_selections.items() if v == PLACEHOLDER]
        if empty_slots:
            st.markdown(render_toast(f"Missing: {', '.join(empty_slots)}. Fill every position.", "error"), unsafe_allow_html=True)
        else:
            vals = list(driver_selections.values())
            dupes = {d for d in vals if vals.count(d) > 1}
            if dupes:
                st.markdown(render_toast(f"Duplicate drivers: {', '.join(sorted(dupes))}.", "error"), unsafe_allow_html=True)
            else:
                # Build the full row, preserving existing constructor picks
                existing_df = load_season_predictions()
                existing_row = existing_df[existing_df["user"] == user]
                full_row = {"user": user, **driver_selections}
                if not existing_row.empty:
                    for pos in CONSTRUCTOR_POSITIONS:
                        full_row[pos] = existing_row.iloc[0].get(pos, PLACEHOLDER)
                else:
                    for pos in CONSTRUCTOR_POSITIONS:
                        full_row[pos] = PLACEHOLDER
                upsert_season_prediction(full_row)
                st.markdown(render_toast(f"Drivers' Championship saved for {user}!", "success"), unsafe_allow_html=True)

    st.markdown("</div></div>", unsafe_allow_html=True)

# --- Constructors' Championship ---
with col_constructors:
    st.markdown(
        '<div class="championship-section"><h3>Constructors\' Championship</h3>'
        '<div class="championship-body">',
        unsafe_allow_html=True,
    )

    col_auto, _ = st.columns([1, 1])
    with col_auto:
        if st.button("Auto-calculate from Drivers", use_container_width=True, key="auto_constructors"):
            auto_populate_constructors()
            st.rerun()

    st.markdown("")

    constructor_selections: dict[str, str] = {}
    for i, pos in enumerate(CONSTRUCTOR_POSITIONS):
        pc = pos_class(i + 1)
        already_taken = get_selected_constructors(pos)
        current_val = st.session_state.get(f"season_constructor_{pos}", PLACEHOLDER)

        available = [c for c in constructor_names if c not in already_taken or c == current_val]
        options = [PLACEHOLDER] + available

        idx = options.index(current_val) if current_val in options else 0

        col_label, col_select = st.columns([0.2, 4], gap="small")
        with col_label:
            st.markdown(
                f'<div style="padding-top:0.45rem"><span class="pos-label {pc}">P{i+1}</span></div>',
                unsafe_allow_html=True,
            )
        with col_select:
            chosen = st.selectbox(
                f"Constructor Position {i+1}",
                options,
                key=f"season_constructor_{pos}",
                label_visibility="collapsed",
            )
        constructor_selections[pos] = chosen

    st.markdown("")
    if st.button("Submit Constructors' Championship", type="primary", use_container_width=True, key="submit_constructors"):
        empty_slots = [p for p, v in constructor_selections.items() if v == PLACEHOLDER]
        if empty_slots:
            st.markdown(render_toast(f"Missing: {', '.join(empty_slots)}. Fill every position.", "error"), unsafe_allow_html=True)
        else:
            vals = list(constructor_selections.values())
            dupes = {c for c in vals if vals.count(c) > 1}
            if dupes:
                st.markdown(render_toast(f"Duplicate constructors: {', '.join(sorted(dupes))}.", "error"), unsafe_allow_html=True)
            else:
                # Build the full row, preserving existing driver picks
                existing_df = load_season_predictions()
                existing_row = existing_df[existing_df["user"] == user]
                full_row = {"user": user}
                if not existing_row.empty:
                    for pos in DRIVER_POSITIONS:
                        full_row[pos] = existing_row.iloc[0].get(pos, PLACEHOLDER)
                else:
                    for pos in DRIVER_POSITIONS:
                        full_row[pos] = PLACEHOLDER
                for pos in CONSTRUCTOR_POSITIONS:
                    full_row[pos] = constructor_selections[pos]
                upsert_season_prediction(full_row)
                st.markdown(render_toast(f"Constructors' Championship saved for {user}!", "success"), unsafe_allow_html=True)

    st.markdown("</div></div>", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Display current predictions
# ---------------------------------------------------------------------------
st.markdown(render_divider(accent=True), unsafe_allow_html=True)
st.markdown(render_section_header("Current Predictions"), unsafe_allow_html=True)

season_df = load_season_predictions()

if season_df.empty:
    st.markdown(render_empty_state("No season predictions yet — be the first!"), unsafe_allow_html=True)
else:
    for _, pred_row in season_df.iterrows():
        pred_user = pred_row["user"]

        # Build driver values
        driver_vals = {}
        driver_list = []
        for pos in DRIVER_POSITIONS:
            val = pred_row.get(pos, "")
            if val and val != PLACEHOLDER:
                driver_vals[pos] = val
                driver_list.append(val)

        # Build constructor values
        constructor_vals = {}
        for pos in CONSTRUCTOR_POSITIONS:
            val = pred_row.get(pos, "")
            if val and val != PLACEHOLDER:
                constructor_vals[pos] = val

        # Podium visualization (drivers)
        if len(driver_list) >= 3:
            st.markdown(
                render_podium(driver_list[:3], driver_teams),
                unsafe_allow_html=True,
            )

        # Side-by-side timing towers
        col_d, col_c = st.columns(2)
        with col_d:
            st.markdown(
                render_timing_tower(
                    user=pred_user,
                    positions=DRIVER_POSITIONS,
                    pos_values=driver_vals,
                    driver_teams=driver_teams,
                    championship_label="Drivers",
                    placeholder=PLACEHOLDER,
                ),
                unsafe_allow_html=True,
            )
        with col_c:
            st.markdown(
                render_timing_tower(
                    user=pred_user,
                    positions=CONSTRUCTOR_POSITIONS,
                    pos_values=constructor_vals,
                    driver_teams=driver_teams,
                    championship_label="Constructors",
                    placeholder=PLACEHOLDER,
                ),
                unsafe_allow_html=True,
            )

        # Delete button
        st.markdown('<div class="trash-btn">', unsafe_allow_html=True)
        if st.button("Delete prediction", key=f"del_season_{pred_user}"):
            delete_season_prediction(pred_user)
            del_key = f"_season_init_{pred_user}"
            if del_key in st.session_state:
                del st.session_state[del_key]
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown(render_divider(), unsafe_allow_html=True)

st.markdown(render_footer(), unsafe_allow_html=True)
