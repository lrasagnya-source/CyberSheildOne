import streamlit as st


def apply_custom_styles():

    st.markdown(
        """
        <style>

        .stApp {
            background-color: #0b0f19;
            color: #e5e7eb;
        }

        section[data-testid="stSidebar"] {
            background-color: #0f1420;
        }

        .cs-card {
            background-color: #131a2b;
            border: 1px solid #1f2937;
            border-radius: 14px;
            padding: 18px;
            margin-bottom: 14px;
        }

        .cs-title {
            font-size: 1.6rem;
            font-weight: 700;
            color: #38bdf8;
        }

        .cs-subtitle {
            color: #9ca3af;
        }

        .stButton button {
            background-color: #2563eb;
            color: white;
            border-radius: 8px;
        }

        </style>
        """,
        unsafe_allow_html=True
    )