# services/breach_service.py

# Demo breach database for testing
DEMO_BREACHED_EMAILS = [
    "test@example.com",
    "demo@gmail.com",
    "hacked@example.com"
]


def check_email(email):

    # Clean the email entered by the user
    email = email.strip().lower()

    # Check whether email exists in demo breach database
    if email in DEMO_BREACHED_EMAILS:

        return {
            "breached": True,
            "security_score": 20,
            "message": "This email was found in a known demo data breach."
        }

    else:

        return {
            "breached": False,
            "security_score": 100,
            "message": "No breach was found in the demo database."
        }