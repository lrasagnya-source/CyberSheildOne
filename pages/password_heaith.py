import streamlit as st

from services.password_service import analyze_password


st.title("🔑 Password Health Checker")

password = st.text_input(
    "Enter password for temporary analysis",
    type="password"
)

if st.button("Analyze Password"):

    if password:

        result = analyze_password(password)

        # Save the password score for the dashboard
        st.session_state["password_score"] = result["score"]

        st.metric(
            "Password Score",
            f"{result['score']}/100"
        )

        st.write(
            f"Strength: **{result['strength']}**"
        )

        for recommendation in result["recommendations"]:
            st.warning(recommendation)

        st.info(
            "Your actual password is not stored."
        )