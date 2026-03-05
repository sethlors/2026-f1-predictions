import streamlit as st
from utils.constants import USERS, PLACEHOLDER, TEAM_COLORS
from utils.data_helpers import load_drivers, load_races, load_race_predictions, upsert_race_prediction, delete_race_prediction
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

st.set_page_config(page_title="Race Predictions", page_icon="", layout="wide")
inject_styles()
st.markdown(render_navbar("race"), unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
NUM_POSITIONS = 22
POSITIONS = [f"P{i}" for i in range(1, NUM_POSITIONS + 1)]

# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
st.markdown(
    render_page_header(
        "Race Predictions",
        "Predict the full finishing order for each Grand Prix.",
    ),
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------
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
# Initialize session-state (once per user+race combo)
# ---------------------------------------------------------------------------
state_key = f"_race_init_{user}_{selected_race}"
if st.session_state.get(state_key) != (user, selected_race):
    for pos in POSITIONS:
        st.session_state[f"race_{pos}"] = prefilled.get(pos, PLACEHOLDER)
    st.session_state[state_key] = (user, selected_race)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def get_selected_drivers(exclude_pos: str) -> set[str]:
    selected = set()
    for p in POSITIONS:
        if p == exclude_pos:
            continue
        val = st.session_state.get(f"race_{p}", PLACEHOLDER)
        if val != PLACEHOLDER:
            selected.add(val)
    return selected

# ---------------------------------------------------------------------------
# Position dropdowns
# ---------------------------------------------------------------------------
st.markdown(render_section_header("Predicted Finishing Order"), unsafe_allow_html=True)

selections: dict[str, str] = {}

for i, pos in enumerate(POSITIONS):
    pc = pos_class(i + 1)
    already_taken = get_selected_drivers(pos)
    current_val = st.session_state.get(f"race_{pos}", PLACEHOLDER)

    available = [d for d in driver_names if d not in already_taken or d == current_val]
    options = [PLACEHOLDER] + available
    display_options = [PLACEHOLDER] + [driver_with_team(d, drivers_df) for d in available]

    idx = options.index(current_val) if current_val in options else 0

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
            format_func=lambda v, _o=options, _d=display_options: _d[_o.index(v)],
            index=idx,
            key=f"race_{pos}",
            label_visibility="collapsed",
        )
    selections[pos] = chosen

# --- Submit ---
st.markdown("")
if st.button("Submit Race Prediction", type="primary", use_container_width=True):
    chosen_list = list(selections.values())
    empty_slots = [p for p, v in selections.items() if v == PLACEHOLDER]

    if empty_slots:
        st.markdown(render_toast(f"Missing: {', '.join(empty_slots)}. Fill every position.", "error"), unsafe_allow_html=True)
    else:
        dupes = {d for d in chosen_list if chosen_list.count(d) > 1}
        if dupes:
            st.markdown(render_toast(f"Duplicate drivers: {', '.join(sorted(dupes))}.", "error"), unsafe_allow_html=True)
        else:
            new_row = {"race": selected_race, "user": user, **selections}
            upsert_race_prediction(new_row)
            st.markdown(render_toast(f"Prediction for {selected_race} saved for {user}!", "success"), unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Display predictions for selected race
# ---------------------------------------------------------------------------
st.markdown(render_divider(accent=True), unsafe_allow_html=True)
st.markdown(render_section_header(f"Predictions — {selected_race}"), unsafe_allow_html=True)

race_pred_df = load_race_predictions()
filtered = race_pred_df[race_pred_df["race"] == selected_race]

if filtered.empty:
    st.markdown(render_empty_state("No predictions yet for this race."), unsafe_allow_html=True)
else:
    for idx, (_, pred_row) in enumerate(filtered.iterrows()):
        pred_user = pred_row["user"]

        # Build position values
        pos_values = {}
        driver_list = []
        for pos in POSITIONS:
            val = pred_row.get(pos, "")
            if val and val != PLACEHOLDER:
                pos_values[pos] = val
                driver_list.append(val)

        # Podium visualization
        if len(driver_list) >= 3:
            st.markdown(
                render_podium(driver_list[:3], driver_teams),
                unsafe_allow_html=True,
            )

        # Timing tower
        st.markdown(
            render_timing_tower(
                user=pred_user,
                positions=POSITIONS,
                pos_values=pos_values,
                driver_teams=driver_teams,
                championship_label="Race Result",
                placeholder=PLACEHOLDER,
            ),
            unsafe_allow_html=True,
        )

        st.markdown('<div class="trash-btn">', unsafe_allow_html=True)
        if st.button("Delete prediction", key=f"del_race_{idx}"):
            delete_race_prediction(selected_race, pred_row["user"])
            del_key = f"_race_init_{pred_row['user']}_{selected_race}"
            if del_key in st.session_state:
                del st.session_state[del_key]
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown(render_divider(), unsafe_allow_html=True)

st.markdown(render_footer(), unsafe_allow_html=True)
