def analyze_password(password):

    score = 0
    recommendations = []

    if len(password) >= 8:
        score += 20
    else:
        recommendations.append("Use at least 8 characters.")

    if any(c.isupper() for c in password):
        score += 20
    else:
        recommendations.append("Add uppercase letters.")

    if any(c.islower() for c in password):
        score += 20
    else:
        recommendations.append("Add lowercase letters.")

    if any(c.isdigit() for c in password):
        score += 20
    else:
        recommendations.append("Add numbers.")

    if any(not c.isalnum() for c in password):
        score += 20
    else:
        recommendations.append("Add special characters.")

    if score >= 80:
        strength = "Strong"
    elif score >= 50:
        strength = "Medium"
    else:
        strength = "Weak"

    return {
        "score": score,
        "strength": strength,
        "recommendations": recommendations
    }