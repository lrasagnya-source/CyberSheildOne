WEIGHTS = {
    "password": 0.20,
    "email": 0.20,
    "phishing": 0.20,
    "web": 0.20,
    "privacy": 0.20
}


def calculate_cyber_health_score(
    password,
    email,
    phishing,
    web,
    privacy,
    qr
):

    score = (

        password * 0.20 +

        email * 0.15 +

        phishing * 0.20 +

        web * 0.20 +

        privacy * 0.15 +

        qr * 0.10

    )

    return round(score)


def calculate_risk_level(score):

    if score >= 80:
        return "LOW"
    elif score >= 60:
        return "MEDIUM"
    elif score >= 40:
        return "HIGH"
    else:
        return "CRITICAL"


def get_highest_risk(scores):

    return min(scores, key=scores.get)