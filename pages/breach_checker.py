import streamlit as st

from services.breach_service import check_email


st.title("📧 Email Breach Checker")

st.write(
    "Check whether your email appears in our breach database."
)


email = st.text_input(
    "Enter your email address"
)


if st.button("🔍 Check Email"):

    if not email.strip():

        st.warning("Please enter an email address.")

    else:

        result = check_email(email)

        # Save score for dashboard
        st.session_state["email_score"] = result["security_score"]

        if result["breached"]:

            st.error("🚨 Email Found in Breach")

        else:

            st.success("✅ No Breach Found")

        st.metric(
            "Email Security Score",
            f"{result['security_score']}/100"
        )

        st.info(
            result["message"]
        )