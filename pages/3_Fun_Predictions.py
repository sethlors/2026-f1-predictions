import streamlit as st
from datetime import date
from utils.constants import USERS
from utils.data_helpers import load_fun_predictions, insert_fun_prediction, delete_fun_prediction
from utils.styles import inject_styles
from utils.ui_helpers import render_navbar, render_page_header, render_section_header, render_divider, render_footer, render_toast, render_empty_state

st.set_page_config(page_title="Fun Predictions", page_icon="", layout="wide")
inject_styles()
st.markdown(render_navbar("fun"), unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
st.markdown(
    render_page_header(
        "Fun Predictions",
        "Hot takes, wild guesses, and bold calls for the season.",
    ),
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Form
# ---------------------------------------------------------------------------
col_user, _ = st.columns([1, 2])
with col_user:
    user = st.selectbox("User", USERS, key="fun_user")

prediction_text = st.text_area(
    "Your prediction",
    placeholder="e.g. Bearman scores a podium before Round 5...",
    key="fun_text",
)

btn_col, _ = st.columns([3, 1])
with btn_col:
    submit = st.button("Submit Prediction", type="primary", use_container_width=True)

if submit:
    if not prediction_text.strip():
        st.markdown(render_toast("Prediction can't be empty.", "error"), unsafe_allow_html=True)
    else:
        new_row = {
            "user": user,
            "prediction": prediction_text.strip(),
            "date_created": date.today().strftime("%m/%d/%Y"),
        }
        insert_fun_prediction(new_row)
        st.markdown(render_toast("Prediction submitted!", "success"), unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Display all fun predictions (newest first, 3 across)
# ---------------------------------------------------------------------------
st.markdown(render_divider(accent=True), unsafe_allow_html=True)
st.markdown(render_section_header("All Predictions"), unsafe_allow_html=True)

df = load_fun_predictions()

if df.empty:
    st.markdown(render_empty_state("No fun predictions yet — drop your hot takes here."), unsafe_allow_html=True)
else:
    df_display = df.iloc[::-1].reset_index()
    # Use Supabase 'id' if available, otherwise fall back to original DataFrame index
    id_col = "id" if "id" in df.columns else "index"

    rows_of_cards = [
        df_display.iloc[i : i + 3] for i in range(0, len(df_display), 3)
    ]

    for card_row in rows_of_cards:
        cols = st.columns(3)
        for col_idx, (_, row) in enumerate(card_row.iterrows()):
            with cols[col_idx]:
                st.markdown(
                    f"""
                    <div class="fun-card">
                        <div class="fun-text">{row['prediction']}</div>
                        <div class="fun-meta">
                            <span class="fun-user">{row['user']}</span>
                            <span>{row['date_created']}</span>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                st.markdown('<div class="trash-btn">', unsafe_allow_html=True)
                if st.button("Delete", key=f"del_fun_{row[id_col]}"):
                    delete_fun_prediction(row[id_col])
                    st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)

st.markdown(render_footer(), unsafe_allow_html=True)
