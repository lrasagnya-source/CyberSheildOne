def calculate_privacy_score(answers):

    score = 100

    if not answers["mfa"]:
        score -= 20

    if answers["password_reuse"]:
        score -= 20

    if answers["location_sharing"]:
        score -= 15

    if answers["public_wifi"]:
        score -= 15

    if answers["tracking"]:
        score -= 15

    return max(score, 0)