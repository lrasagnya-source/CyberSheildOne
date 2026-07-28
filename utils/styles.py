import streamlit as st
from utils.styles import apply_custom_styles


def apply_custom_styles():

    st.markdown(
        """
        <style>

        /* =========================
           MAIN BACKGROUND
        ========================= */

        .stApp {

            background:
                radial-gradient(
                    circle at 10% 10%,
                    rgba(0, 180, 255, 0.12),
                    transparent 30%
                ),

                radial-gradient(
                    circle at 90% 90%,
                    rgba(0, 120, 255, 0.10),
                    transparent 30%
                ),

                linear-gradient(
                    135deg,
                    #06111f 0%,
                    #0b1d31 50%,
                    #06101c 100%
                );

            color: #ffffff;

        }


        /* =========================
           SIDEBAR
        ========================= */

        section[data-testid="stSidebar"] {

            background:
                linear-gradient(
                    180deg,
                    #071522,
                    #0b2438
                );

            border-right:
                1px solid
                rgba(0, 200, 255, 0.20);

        }


        /* =========================
           HEADINGS
        ========================= */

        h1 {

            color: #00d9ff !important;

            font-weight: 700;

        }


        h2 {

            color: #8be9fd !important;

        }


        h3 {

            color: #b8f3ff !important;

        }


        /* =========================
           GLASS METRIC CARDS
        ========================= */

        div[data-testid="stMetric"] {

            background:
                rgba(
                    255,
                    255,
                    255,
                    0.07
                );

            border:
                1px solid
                rgba(
                    0,
                    217,
                    255,
                    0.25
                );

            border-radius: 16px;

            padding: 18px;

            box-shadow:
                0 8px 32px
                rgba(0, 0, 0, 0.25);

            backdrop-filter: blur(10px);

        }


        /* Metric label */

        div[data-testid="stMetricLabel"] {

            color: #b8d9e8 !important;

        }


        /* Metric value */

        div[data-testid="stMetricValue"] {

            color: #00d9ff !important;

        }


        /* =========================
           BUTTONS
        ========================= */

        .stButton > button {

            background:
                rgba(
                    0,
                    217,
                    255,
                    0.10
                );

            color: #00d9ff;

            border:
                1px solid
                #00d9ff;

            border-radius: 10px;

            padding: 8px 20px;

            transition: 0.3s;

        }


        .stButton > button:hover {

            background: #00d9ff;

            color: #06111f;

            box-shadow:
                0 0 15px
                rgba(0, 217, 255, 0.5);

        }


        /* =========================
           INPUT FIELDS
        ========================= */

        input,
        textarea {

            background-color:
                rgba(
                    255,
                    255,
                    255,
                    0.08
                ) !important;

            color: white !important;

            border:
                1px solid
                rgba(
                    0,
                    217,
                    255,
                    0.30
                ) !important;

            border-radius: 8px !important;

        }


        /* =========================
           SELECTBOX
        ========================= */

        div[data-baseweb="select"] > div {

            background-color:
                rgba(
                    255,
                    255,
                    255,
                    0.08
                );

            border:
                1px solid
                rgba(
                    0,
                    217,
                    255,
                    0.30
                );

        }


        /* =========================
           ALERT BOXES
        ========================= */

        div[data-testid="stAlert"] {

            border-radius: 12px;

            backdrop-filter: blur(8px);

        }


        /* =========================
           DATAFRAME / TABLE
        ========================= */

        div[data-testid="stDataFrame"] {

            border-radius: 12px;

            overflow: hidden;

        }


        /* =========================
           HORIZONTAL LINE
        ========================= */

        hr {

            border-color:
                rgba(
                    0,
                    217,
                    255,
                    0.20
                );

        }


        </style>
        """,

        unsafe_allow_html=True
    )