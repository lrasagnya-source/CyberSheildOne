def analyze_url(url):
    return {
        "status": "SAFE",
        "risk_score": 10,
        "message": f"URL analyzed: {url}",
        "reasons": []
    }