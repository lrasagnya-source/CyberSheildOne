import re
from urllib.parse import urlparse

# Common suspicious words
SUSPICIOUS_KEYWORDS = [
    "login",
    "verify",
    "verification",
    "secure",
    "account",
    "update",
    "confirm",
    "bank",
    "paypal",
    "password",
    "wallet",
    "prize",
    "free",
    "urgent",
    "alert"
]

# Common URL shorteners
SHORTENERS = [
    "bit.ly",
    "tinyurl.com",
    "t.co",
    "goo.gl",
    "is.gd",
    "cutt.ly"
]


def detect_fake_url(url):
    """
    Analyze a URL and return a risk score and reasons.
    """

    result = {
        "url": url,
        "is_suspicious": False,
        "risk_score": 0,
        "risk_level": "Low",
        "reasons": []
    }

    # Add scheme if missing
    if not url.startswith(("http://", "https://")):
        url = "http://" + url

    try:
        parsed = urlparse(url)
        domain = parsed.netloc.lower()
        path = parsed.path.lower()

        if not domain:
            result["is_suspicious"] = True
            result["risk_score"] = 100
            result["risk_level"] = "High"
            result["reasons"].append("Invalid URL")
            return result

        # 1. HTTP instead of HTTPS
        if parsed.scheme == "http":
            result["risk_score"] += 15
            result["reasons"].append("Uses HTTP instead of HTTPS")

        # 2. IP address instead of domain
        if re.match(r"^\d{1,3}(\.\d{1,3}){3}$", domain):
            result["risk_score"] += 30
            result["reasons"].append("Uses an IP address instead of a domain name")

        # 3. URL shortener
        if domain in SHORTENERS:
            result["risk_score"] += 25
            result["reasons"].append("Uses a URL shortening service")

        # 4. Suspicious keywords
        full_url = (domain + path).lower()

        found_keywords = [
            word for word in SUSPICIOUS_KEYWORDS
            if word in full_url
        ]

        if found_keywords:
            result["risk_score"] += min(len(found_keywords) * 8, 30)
            result["reasons"].append(
                "Contains suspicious keywords: "
                + ", ".join(found_keywords)
            )

        # 5. Excessive subdomains
        if domain.count(".") >= 3:
            result["risk_score"] += 15
            result["reasons"].append("Contains an unusually large number of subdomains")

        # 6. @ symbol
        if "@" in url:
            result["risk_score"] += 30
            result["reasons"].append("Contains '@' which can hide the actual destination")

        # 7. Very long URL
        if len(url) > 100:
            result["risk_score"] += 10
            result["reasons"].append("URL is unusually long")

        # 8. Suspicious characters
        if "%" in url:
            result["risk_score"] += 5
            result["reasons"].append("Contains URL-encoded characters")

        # Limit score
        result["risk_score"] = min(result["risk_score"], 100)

        # Risk level
        if result["risk_score"] >= 60:
            result["risk_level"] = "High"
            result["is_suspicious"] = True

        elif result["risk_score"] >= 30:
            result["risk_level"] = "Medium"
            result["is_suspicious"] = True

        else:
            result["risk_level"] = "Low"
            result["is_suspicious"] = False

        return result

    except Exception as e:
        result["is_suspicious"] = True
        result["risk_score"] = 100
        result["risk_level"] = "High"
        result["reasons"].append("Unable to parse URL")

        return result


# Test
if __name__ == "__main__":

    test_urls = [
        "https://google.com",
        "http://secure-account-verification-login.example.com/verify",
        "http://192.168.1.10/login",
        "https://bit.ly/abc123"
    ]

    for url in test_urls:
        result = detect_fake_url(url)

        print("\nURL:", result["url"])
        print("Risk Score:", result["risk_score"])
        print("Risk Level:", result["risk_level"])
        print("Suspicious:", result["is_suspicious"])

        if result["reasons"]:
            print("Reasons:")
            for reason in result["reasons"]:
                print(" -", reason)