import streamlit as st
import pandas as pd
from datetime import date
from utils.constants import USERS
from utils.data_helpers import load_fun_predictions, save_fun_predictions
from utils.styles import COMMON_STYLES
from utils.ui_helpers import render_page_header

st.set_page_config(page_title="Fun Predictions", page_icon="", layout="wide")

# ---------------------------------------------------------------------------
# CSS
# ---------------------------------------------------------------------------
st.markdown(COMMON_STYLES, unsafe_allow_html=True)
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
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: repeating-linear-gradient(
            45deg,
            transparent,
            transparent 20px,
            rgba(255,255,255,0.02) 20px,
            rgba(255,255,255,0.02) 40px
        );
        pointer-events: none;
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

    .fun-card {
        background: linear-gradient(135deg, #1a1a1a 0%, #151515 100%);
        border: 1px solid #2a2a2a;
        border-top: 4px solid #e10600;
        border-radius: 12px;
        padding: 1.5rem 1.75rem;
        color: white;
        min-height: 180px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        box-shadow: 0 6px 25px rgba(0,0,0,0.5), 0 0 0 1px rgba(225,6,0,0.1) inset;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    .fun-card::before {
        content: '';
        position: absolute;
        top: -100%;
        left: -100%;
        width: 300%;
        height: 300%;
        background: radial-gradient(circle, rgba(225,6,0,0.05) 0%, transparent 70%);
        transition: all 0.5s;
        pointer-events: none;
    }
    .fun-card:hover {
        transform: translateY(-4px) rotate(0.5deg);
        box-shadow: 0 12px 35px rgba(225, 6, 0, 0.25), 0 0 0 1px rgba(225,6,0,0.2) inset;
        border-color: rgba(225, 6, 0, 0.3);
    }
    .fun-card:hover::before {
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
    }
    .fun-card .fun-text {
        font-size: 1.05rem;
        font-weight: 600;
        line-height: 1.6;
        margin-bottom: 1rem;
        flex: 1;
        position: relative;
    }
    .fun-card .fun-meta {
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: 0.7rem;
        opacity: 0.45;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 600;
        position: relative;
    }
    .fun-card .fun-user {
        color: #e10600;
        font-weight: 800;
        opacity: 1;
        text-shadow: 0 1px 4px rgba(225, 6, 0, 0.4);
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

# Data will be loaded using utility functions


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
