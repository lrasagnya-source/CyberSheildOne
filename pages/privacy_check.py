import streamlit as st

from services.privacy_service import calculate_privacy_score


st.title("🔒 Privacy Check")

mfa = st.checkbox("I use Multi-Factor Authentication")

password_reuse = st.checkbox("I reuse passwords")

location_sharing = st.checkbox("I frequently share my location")

public_wifi = st.checkbox("I frequently use public Wi-Fi")

tracking = st.checkbox("I allow extensive browser tracking")


if st.button("Calculate Privacy Score"):

    answers = {
        "mfa": mfa,
        "password_reuse": password_reuse,
        "location_sharing": location_sharing,
        "public_wifi": public_wifi,
        "tracking": tracking
    }

    score = calculate_privacy_score(answers)

    # Save the privacy score for the dashboard
    st.session_state["privacy_score"] = score

    st.metric(
        "Privacy Score",
        f"{score}/100"
    )