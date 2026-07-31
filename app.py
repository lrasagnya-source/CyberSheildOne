"""
app.py
------
CyberShield ONE - Entry point.

Handles:
- App-wide page config + dark cybersecurity theme
- Database initialization (creates SQLite file/schema on first run)
- Authentication: Register / Login / Logout
- Session-state based access control
- Sidebar navigation to feature pages (Streamlit multipage app)

Run with:
    streamlit run app.py

Note on multipage navigation:
CyberShield ONE uses Streamlit's native `pages/` directory feature.
Every file in pages/ is auto-registered as a page. app.py itself
acts as the gatekeeper: unauthenticated users only ever see the
Login/Register screen, no matter which page they try to open,
because every page in pages/ calls `require_login()` from this
file (imported) before rendering anything.
"""

import streamlit as st
from utils.styles import apply_custom_styles

from database.db import init_db
from database.models import create_user, get_user_by_email, email_exists
from utils.security import hash_password, verify_password
from utils.validators import (
    is_valid_email,
    is_valid_name,
    password_meets_minimum_requirements,
    passwords_match,
)


# ---------------------------------------------------------------------
# PAGE CONFIG + THEME
# ---------------------------------------------------------------------

st.set_page_config(
    page_title="CyberShield ONE",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_custom_styles()


# ---------------------------------------------------------------------
# DB INIT (idempotent)
# ---------------------------------------------------------------------

init_db()

# ---------------------------------------------------------------------
# SESSION STATE
# ---------------------------------------------------------------------

def init_session_state():
    defaults = {
        "authenticated": False,
        "user_id": None,
        "user_name": None,
        "user_email": None,
        "auth_mode": "Login",  # "Login" or "Register"
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def require_login():
    """
    Call this at the top of every page in pages/*.py.
    Stops rendering (st.stop) if the user is not authenticated.
    """
    init_session_state()
    if not st.session_state.get("authenticated"):
        st.warning("🔒 Please log in to access CyberShield ONE.")
        st.info("Go to the main app page (CyberShield ONE) in the sidebar to log in.")
        st.stop()


def logout():
    for key in ["authenticated", "user_id", "user_name", "user_email"]:
        st.session_state[key] = False if key == "authenticated" else None


# ---------------------------------------------------------------------
# AUTH FORMS
# ---------------------------------------------------------------------

def render_login_form():
    with st.form("login_form", clear_on_submit=False):
        email = st.text_input("Email", placeholder="you@example.com")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Log In", use_container_width=True)

    if submitted:
        if not is_valid_email(email):
            st.error("Please enter a valid email address.")
            return
        if not password:
            st.error("Please enter your password.")
            return

        user = get_user_by_email(email)
        if not user or not verify_password(password, user["password_hash"]):
            st.error("Invalid email or password.")
            return

        st.session_state.authenticated = True
        st.session_state.user_id = user["id"]
        st.session_state.user_name = user["name"]
        st.session_state.user_email = user["email"]
        st.success(f"Welcome back, {user['name']}! Redirecting to your dashboard...")
        st.switch_page("pages/dashboard.py")


def render_register_form():
    with st.form("register_form", clear_on_submit=False):
        name = st.text_input("Full Name", placeholder="Jane Doe")
        email = st.text_input("Email", placeholder="you@example.com")
        password = st.text_input("Password", type="password",
                                  help="At least 8 characters, with uppercase, lowercase, and a number.")
        confirm_password = st.text_input("Confirm Password", type="password")
        submitted = st.form_submit_button("Create Account", use_container_width=True)

    if submitted:
        if not is_valid_name(name):
            st.error("Please enter your full name (2-100 characters).")
            return
        if not is_valid_email(email):
            st.error("Please enter a valid email address.")
            return
        if email_exists(email):
            st.error("An account with this email already exists. Please log in instead.")
            return
        ok, msg = password_meets_minimum_requirements(password)
        if not ok:
            st.error(msg)
            return
        if not passwords_match(password, confirm_password):
            st.error("Passwords do not match.")
            return

        password_hash = hash_password(password)  # never store plain text
        user_id = create_user(name=name.strip(), email=email.strip(), password_hash=password_hash)

        st.session_state.authenticated = True
        st.session_state.user_id = user_id
        st.session_state.user_name = name.strip()
        st.session_state.user_email = email.strip().lower()
        st.success("Account created successfully! Redirecting to your dashboard...")
        st.switch_page("pages/dashboard.py")


# ---------------------------------------------------------------------
# MAIN ENTRY
# ---------------------------------------------------------------------

def main():
    init_session_state()

    st.markdown(
        "<div class='cs-title'>🛡️ CyberShield ONE</div>"
        "<div class='cs-subtitle'>AI-Powered Personal Cyber Health Platform</div>",
        unsafe_allow_html=True,
    )
    st.caption(
        "⚠️ CyberShield ONE evaluates and improves your personal cyber-security "
        "posture. It is an awareness and risk-scoring tool - it is **not** an "
        "antivirus and does not guarantee protection from every cyberattack."
    )
    st.divider()

    if st.session_state.authenticated:
        st.success(f"You're logged in as **{st.session_state.user_name}**.")
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("Go to Dashboard →", use_container_width=True):
                st.switch_page("pages/dashboard.py")
        with col2:
            if st.button("Log Out", use_container_width=True):
                logout()
                st.rerun()
        return

    left, right = st.columns([1, 1.2])

    with left:
        st.subheader("Get Started")
        mode = st.radio("Choose an option", ["Login", "Register"], horizontal=True,
                         index=0 if st.session_state.auth_mode == "Login" else 1)
        st.session_state.auth_mode = mode
        st.write("")
        if mode == "Login":
            render_login_form()
        else:
            render_register_form()

    with right:
        st.markdown(
            """
            <div class="cs-card">
                <h4>What CyberShield ONE Checks</h4>
                <ul>
                    <li>🔑 Password Health</li>
                    <li>📧 Email Breach Exposure</li>
                    <li>🎣 Phishing Email Detection (ML)</li>
                    <li>🌐 Suspicious URL / Website Detection (ML)</li>
                    <li>📷 QR Code Safety Scanning</li>
                    <li>🕵️ Privacy Habits</li>
                </ul>
                <p>All results feed a single, personalized <b>Cyber Health Score</b>,
                a Threat Correlation Engine, and adaptive recommendations.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )


if __name__ == "__main__":
    main()
