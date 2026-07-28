# services/phishing_service.py

import re


# Words commonly found in phishing messages
SUSPICIOUS_KEYWORDS = [
    "urgent",
    "immediately",
    "verify your account",
    "verify account",
    "click here",
    "claim your prize",
    "you have won",
    "winner",
    "free prize",
    "password",
    "confirm your account",
    "account suspended",
    "account blocked",
    "bank",
    "otp",
    "login",
    "security alert",
    "limited time",
    "act now"
]


def analyze_message(message):

    message = message.strip().lower()

    if not message:

        return {
            "is_phishing": False,
            "risk_score": 0,
            "security_score": 100,
            "confidence": 0,
            "reasons": [
                "No message was entered."
            ]
        }

    risk_score = 0
    reasons = []

    # Check suspicious keywords
    found_keywords = []

    for keyword in SUSPICIOUS_KEYWORDS:

        if keyword in message:

            found_keywords.append(keyword)

    if found_keywords:

        risk_score += min(
            len(found_keywords) * 8,
            40
        )

        reasons.append(
            "Suspicious keywords detected: "
            + ", ".join(found_keywords)
        )

    # Check for URLs
    urls = re.findall(
        r"https?://\S+|www\.\S+",
        message
    )

    if urls:

        risk_score += 25

        reasons.append(
            "Message contains a website link."
        )

    # Check urgency
    urgency_words = [
        "urgent",
        "immediately",
        "act now",
        "within 24 hours",
        "last chance"
    ]

    urgency_found = any(
        word in message
        for word in urgency_words
    )

    if urgency_found:

        risk_score += 15

        reasons.append(
            "Message uses urgent or threatening language."
        )

    # Check for money/prize-related content
    financial_words = [
        "money",
        "prize",
        "lottery",
        "reward",
        "cash",
        "won"
    ]

    if any(
        word in message
        for word in financial_words
    ):

        risk_score += 15

        reasons.append(
            "Message contains suspicious prize or financial content."
        )

    # Limit risk score
    risk_score = min(
        risk_score,
        100
    )

    # Convert risk score to security score
    security_score = 100 - risk_score

    # Determine result
    if risk_score >= 60:

        is_phishing = True

        confidence = risk_score

        status = "PHISHING"

    elif risk_score >= 30:

        is_phishing = False

        confidence = risk_score

        status = "SUSPICIOUS"

    else:

        is_phishing = False

        confidence = 100 - risk_score

        status = "LEGITIMATE"

    return {

        "is_phishing": is_phishing,

        "status": status,

        "risk_score": risk_score,

        "security_score": security_score,

        "confidence": confidence,

        "reasons": reasons
    }