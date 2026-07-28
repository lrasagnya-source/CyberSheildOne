# services/recommendation_engine.py


def generate_recommendations(scores):

    recommendations = []


    password_score = scores.get(
        "password",
        0
    )

    email_score = scores.get(
        "email",
        0
    )

    phishing_score = scores.get(
        "phishing",
        0
    )

    web_score = scores.get(
        "web",
        0
    )

    privacy_score = scores.get(
        "privacy",
        0
    )

    qr_score = scores.get(
        "qr",
        0
    )


    # Password recommendations

    if password_score < 50:

        recommendations.append({

            "priority": "HIGH",

            "category": "Password Security",

            "message": (
                "Your password security is weak. "
                "Use a strong and unique password "
                "and avoid reusing passwords."
            )

        })


    elif password_score < 75:

        recommendations.append({

            "priority": "MEDIUM",

            "category": "Password Security",

            "message": (
                "Improve your password strength "
                "and consider using a password manager."
            )

        })


    # Email breach recommendations

    if email_score < 50:

        recommendations.append({

            "priority": "HIGH",

            "category": "Email Security",

            "message": (
                "Your email may be exposed in a data breach. "
                "Change passwords associated with this email "
                "and enable MFA."
            )

        })


    # Phishing recommendations

    if phishing_score < 50:

        recommendations.append({

            "priority": "HIGH",

            "category": "Phishing Protection",

            "message": (
                "Be careful with suspicious emails and messages. "
                "Do not click unknown links or share sensitive information."
            )

        })


    # Web recommendations

    if web_score < 50:

        recommendations.append({

            "priority": "HIGH",

            "category": "Web Security",

            "message": (
                "Avoid suspicious websites and verify URLs "
                "before entering passwords or personal information."
            )

        })


    # Privacy recommendations

    if privacy_score < 50:

        recommendations.append({

            "priority": "MEDIUM",

            "category": "Privacy",

            "message": (
                "Improve your privacy settings, reduce tracking, "
                "and avoid sharing unnecessary personal information."
            )

        })


    # QR recommendations

    if qr_score < 50:

        recommendations.append({

            "priority": "HIGH",

            "category": "QR Security",

            "message": (
                "Avoid scanning suspicious QR codes. "
                "Always verify the destination URL before opening it."
            )

        })


    # General recommendation

    if len(recommendations) == 0:

        recommendations.append({

            "priority": "LOW",

            "category": "Overall Security",

            "message": (
                "Your current cyber security posture looks good. "
                "Continue monitoring your security regularly."
            )

        })


    return recommendations