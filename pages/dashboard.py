import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

from utils.styles import apply_custom_styles

from services.risk_engine import (
    calculate_cyber_health_score,
    calculate_risk_level,
    get_highest_risk
)

from services.recommendation_engine import (
    generate_recommendations
)

from services.threat_correlation import (
    detect_combined_threats
)


# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="CyberShield ONE Dashboard",
    page_icon="🛡️",
    layout="wide"
)


# =====================================================
# APPLY PROFESSIONAL THEME
# =====================================================

apply_custom_styles()


# =====================================================
# LOGIN CHECK
# =====================================================

if not st.session_state.get("authenticated", False):

    st.warning("🔒 Please login to access the dashboard.")

    st.stop()


# =====================================================
# HEADER
# =====================================================

col1, col2 = st.columns([4, 1])


with col1:

    st.title("🛡️ CyberShield ONE")

    st.caption(
        "AI-Powered Personal Cyber Security Health Monitor"
    )


with col2:

    st.write("")

    if st.button(
        "🚪 Logout",
        use_container_width=True
    ):

        st.session_state.authenticated = False
        st.session_state.user_id = None
        st.session_state.user_name = None
        st.session_state.user_email = None

        st.switch_page("app.py")


st.divider()


# =====================================================
# GET SCORES FROM SESSION STATE
# =====================================================

scores = {

    "password": st.session_state.get(
        "password_score",
        0
    ),

    "email": st.session_state.get(
        "email_score",
        0
    ),

    "phishing": st.session_state.get(
        "phishing_score",
        0
    ),

    "web": st.session_state.get(
        "web_score",
        0
    ),

    "privacy": st.session_state.get(
        "privacy_score",
        0
    ),

    "qr": st.session_state.get(
        "qr_score",
        0
    )

}


# =====================================================
# CALCULATE CYBER HEALTH SCORE
# =====================================================
health_score = calculate_cyber_health_score(
    scores["password"],
    scores["email"],
    scores["phishing"],
    scores["web"],
    scores["privacy"],
    scores["qr"]
)




risk_level = calculate_risk_level(
    health_score
)


highest_risk = get_highest_risk(
    scores
)


# =====================================================
# MAIN HEALTH SCORE
# =====================================================

st.subheader("🛡️ Overall Cyber Health")


gauge = go.Figure(

    go.Indicator(

        mode="gauge+number",

        value=health_score,

        title={
            "text": "Cyber Health Score"
        },

        gauge={

            "axis": {
                "range": [0, 100]
            },

            "bar": {
                "thickness": 0.3
            },

            "steps": [

                {
                    "range": [0, 40]
                },

                {
                    "range": [40, 70]
                },

                {
                    "range": [70, 100]
                }

            ]

        }

    )

)


gauge.update_layout(

    height=320,

    margin=dict(

        l=20,

        r=20,

        t=50,

        b=20

    )

)


st.plotly_chart(

    gauge,

    use_container_width=True

)


# =====================================================
# RISK SUMMARY
# =====================================================

summary_col1, summary_col2, summary_col3 = st.columns(3)


with summary_col1:

    st.metric(

        "🛡️ Cyber Health",

        f"{health_score}/100"

    )


with summary_col2:

    st.metric(

        "⚠️ Risk Level",

        risk_level

    )


with summary_col3:

    st.metric(

        "🚨 Highest Risk",

        highest_risk.title()

    )


if health_score >= 80:

    st.success(

        "🟢 Your cybersecurity health is strong."

    )

elif health_score >= 50:

    st.warning(

        "🟠 Your cybersecurity health needs improvement."

    )

else:

    st.error(

        "🔴 Your cybersecurity risk is high. "
        "Immediate action is recommended."

    )


# =====================================================
# SECURITY CATEGORY SCORES
# =====================================================

st.subheader("📊 Security Category Scores")


col1, col2, col3 = st.columns(3)


with col1:

    st.metric(

        "🔑 Password Health",

        f"{scores['password']}/100"

    )


with col2:

    st.metric(

        "📧 Email Security",

        f"{scores['email']}/100"

    )


with col3:

    st.metric(

        "🎣 Phishing Protection",

        f"{scores['phishing']}/100"

    )


col4, col5, col6 = st.columns(3)


with col4:

    st.metric(

        "🌐 Web Security",

        f"{scores['web']}/100"

    )


with col5:

    st.metric(

        "🔒 Privacy",

        f"{scores['privacy']}/100"

    )


with col6:

    st.metric(

        "📷 QR Security",

        f"{scores['qr']}/100"

    )


# =====================================================
# SECURITY ANALYSIS CHART
# =====================================================

st.subheader("📈 Security Category Analysis")


chart_data = {

    "Category": [

        "Password",

        "Email",

        "Phishing",

        "Web",

        "Privacy",

        "QR"

    ],

    "Score": [

        scores["password"],

        scores["email"],

        scores["phishing"],

        scores["web"],

        scores["privacy"],

        scores["qr"]

    ]

}


fig = px.bar(

    chart_data,

    x="Category",

    y="Score",

    range_y=[0, 100],

    text="Score"

)


fig.update_traces(

    textposition="outside"

)


fig.update_layout(

    height=400,

    yaxis_title="Security Score",

    xaxis_title="Security Category",

    showlegend=False

)


st.plotly_chart(

    fig,

    use_container_width=True

)


# =====================================================
# ACTIVE THREATS
# =====================================================

st.subheader("🚨 Active Threats")


try:

    threats = detect_combined_threats(
        scores
    )


    if threats:

        for threat in threats:

            if threat["severity"] == "HIGH":

                st.error(

                    f"🔴 **{threat['title']}**\n\n"
                    f"{threat['message']}"

                )

            else:

                st.warning(

                    f"🟠 **{threat['title']}**\n\n"
                    f"{threat['message']}"

                )

    else:

        st.success(

            "✅ No major combined threats detected."

        )


except Exception:

    st.info(

        "ℹ️ Threat correlation will appear "
        "after enough security checks are completed."

    )


# =====================================================
# PERSONALIZED RECOMMENDATIONS
# =====================================================

st.subheader("🤖 Personalized Recommendations")


recommendations = generate_recommendations(

    scores

)


if recommendations:

    for recommendation in recommendations:

        st.info(

            f"**{recommendation['priority']} - "
            f"{recommendation['category']}**\n\n"

            f"{recommendation['message']}"

        )

else:

    st.success(

        "🎉 No immediate recommendations. "
        "Your security posture looks good!"

    )


# =====================================================
# FOOTER
# =====================================================

st.divider()


st.caption(

    "CyberShield ONE | Personal Cyber Security "
    "Health Monitoring Platform"

)