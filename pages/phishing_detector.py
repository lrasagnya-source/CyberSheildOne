# pages/phishing_detector.py

import streamlit as st

from services.phishing_service import analyze_message


st.title("🤖 AI Phishing Detector")

st.write(
    "Paste an email, SMS, or message to check for phishing indicators."
)


message = st.text_area(
    "Paste your message here",
    height=250,
    placeholder=(
        "Example: Your account has been suspended. "
        "Click here immediately to verify your account."
    )
)


if st.button("🔍 Analyze Message"):

    if not message.strip():

        st.warning(
            "Please enter a message to analyze."
        )

    else:

        result = analyze_message(message)

        # Save phishing security score for dashboard
        st.session_state["phishing_score"] = (
            result["security_score"]
        )

        st.session_state["phishing_risk_score"] = (
            result["risk_score"]
        )

        st.subheader("Analysis Result")

        # Display result
        if result["status"] == "PHISHING":

            st.error(
                "🚨 PHISHING DETECTED"
            )

        elif result["status"] == "SUSPICIOUS":

            st.warning(
                "⚠️ SUSPICIOUS MESSAGE"
            )

        else:

            st.success(
                "✅ MESSAGE APPEARS LEGITIMATE"
            )

        # Display scores
        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Risk Score",
                f"{result['risk_score']}/100"
            )

        with col2:

            st.metric(
                "Security Score",
                f"{result['security_score']}/100"
            )

        with col3:

            st.metric(
                "Confidence",
                f"{result['confidence']}%"
            )

        # Display reasons
        st.subheader("🔎 Detection Indicators")

        if result["reasons"]:

            for reason in result["reasons"]:

                st.write(
                    f"• {reason}"
                )

        else:

            st.write(
                "No major suspicious indicators were detected."
            )

        st.info(
            "The message content is analyzed temporarily "
            "and is not stored by this module."
        )