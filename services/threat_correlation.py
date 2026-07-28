# services/threat_correlation.py


def detect_combined_threats(scores):

    threats = []

    password_score = scores.get("password", 100)
    email_score = scores.get("email", 100)
    phishing_score = scores.get("phishing", 100)
    web_score = scores.get("web", 100)
    privacy_score = scores.get("privacy", 100)
    qr_score = scores.get("qr", 100)

    # Account compromise risk
    if email_score < 50 and password_score < 60:

        threats.append({
            "severity": "HIGH",
            "title": "Account Compromise Risk",
            "message": (
                "Your email may be exposed and your password "
                "security is weak. Change your password immediately."
            )
        })

    # Phishing attack chain
    if phishing_score < 50 and web_score < 50:

        threats.append({
            "severity": "HIGH",
            "title": "Phishing Attack Risk",
            "message": (
                "Suspicious messages and unsafe websites were detected."
            )
        })

    # QR phishing risk
    if qr_score < 50 and web_score < 50:

        threats.append({
            "severity": "HIGH",
            "title": "QR Phishing Risk",
            "message": (
                "A QR code may lead to a potentially dangerous website."
            )
        })

    # Privacy exposure
    if privacy_score < 50:

        threats.append({
            "severity": "MEDIUM",
            "title": "Privacy Exposure",
            "message": (
                "Your privacy settings indicate increased exposure."
            )
        })

    # Weak password
    if password_score < 50:

        threats.append({
            "severity": "MEDIUM",
            "title": "Weak Password Security",
            "message": (
                "Improve your password security and avoid password reuse."
            )
        })

    return threats