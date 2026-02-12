import streamlit as st
import pandas as pd
import os
from datetime import date

st.set_page_config(page_title="Fun Predictions", page_icon="", layout="wide")

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

    .fun-card {
        background: #2a2a2a;
        border: 1px solid #444;
        border-top: 4px solid #e10600;
        border-radius: 4px;
        padding: 1.25rem 1.5rem;
        color: white;
        min-height: 160px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        box-shadow: 2px 3px 8px rgba(0,0,0,0.3);
    }
    .fun-card .fun-text {
        font-size: 1rem;
        font-weight: 600;
        line-height: 1.5;
        margin-bottom: 0.75rem;
        flex: 1;
    }
    .fun-card .fun-meta {
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: 0.75rem;
        opacity: 0.5;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .fun-card .fun-user {
        color: #e10600;
        font-weight: 700;
        opacity: 1;
    }

    /* Red trash-can delete button — pulled into card bottom-right */
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
FUN_PATH = os.path.join(DATA_DIR, "fun_predictions.csv")

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_fun_predictions() -> pd.DataFrame:
    return pd.read_csv(FUN_PATH)


def save_fun_predictions(df: pd.DataFrame):
    df.to_csv(FUN_PATH, index=False)


# ---------------------------------------------------------------------------
# UI
# ---------------------------------------------------------------------------

st.markdown(
    """
    <div class="page-header">
        <h1>Fun Predictions</h1>
        <p>Hot takes, wild guesses, and bold calls.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

col_user, _ = st.columns([1, 2])
with col_user:
    user = st.selectbox("User", USERS, key="fun_user")

prediction_text = st.text_area(
    "Your prediction",
    placeholder="e.g. Bearman scores a podium before Round 5...",
    key="fun_text",
)

btn_col1, btn_col2 = st.columns([3, 1])
with btn_col1:
    submit = st.button("Submit Prediction", type="primary", use_container_width=True)

if submit:
    if not prediction_text.strip():
        st.error("Prediction can't be empty.")
    else:
        df = load_fun_predictions()
        new_row = {
            "user": user,
            "prediction": prediction_text.strip(),
            "date_created": date.today().strftime("%m/%d/%Y"),
        }
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        save_fun_predictions(df)
        st.success("Prediction submitted!")

# ---------------------------------------------------------------------------
# Display all fun predictions as sticky-note cards (newest first, 3 across)
# ---------------------------------------------------------------------------
st.markdown("---")
st.markdown("### All Predictions")

df = load_fun_predictions()

if df.empty:
    st.info("No fun predictions yet — drop your hot takes here.")
else:
    # Show newest first — use original index as a stable ID for deletion
    df_display = df.iloc[::-1].reset_index()  # keeps original index in "index" col

    # 3-column grid
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
                trash_icon = "\u2715"  # small X mark
                st.markdown('<div class="trash-btn">', unsafe_allow_html=True)
                if st.button(trash_icon, key=f"del_fun_{row['index']}"):
                    df = load_fun_predictions()
                    df = df.drop(index=row["index"]).reset_index(drop=True)
                    save_fun_predictions(df)
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
