import streamlit as st

from services.url_service import analyze_url


st.title("🌐 URL Security Checker")

url = st.text_input("Enter URL")


if st.button("Analyze URL"):

    result = analyze_url(url)

    st.write(result)