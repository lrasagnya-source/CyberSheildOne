"""
utils/helpers.py
-----------------
Small, generic helper functions shared across pages/services -
formatting, risk-level styling, timestamps, etc.
"""

from datetime import datetime


def now_iso() -> str:
    return datetime.utcnow().isoformat()


def format_timestamp(ts: str) -> str:
    """Convert an ISO timestamp string into a friendly display format."""
    if not ts:
        return "N/A"
    try:
        dt = datetime.fromisoformat(ts)
        return dt.strftime("%d %b %Y, %I:%M %p")
    except (ValueError, TypeError):
        return ts


def risk_level_color(risk_level: str) -> str:
    """Return a hex color associated with a risk level, for badges/charts."""
    mapping = {
        "LOW RISK": "#22c55e",
        "MEDIUM RISK": "#eab308",
        "HIGH RISK": "#f97316",
        "CRITICAL RISK": "#ef4444",
        "UNKNOWN": "#6b7280",
    }
    return mapping.get(risk_level.upper() if risk_level else "UNKNOWN", "#6b7280")


def risk_level_icon(risk_level: str) -> str:
    mapping = {
        "LOW RISK": "🟢",
        "MEDIUM RISK": "🟡",
        "HIGH RISK": "🟠",
        "CRITICAL RISK": "🔴",
        "UNKNOWN": "⚪",
    }
    return mapping.get(risk_level.upper() if risk_level else "UNKNOWN", "⚪")


def clamp(value: float, min_value: float = 0, max_value: float = 100) -> float:
    return max(min_value, min(max_value, value))


def severity_color(severity: str) -> str:
    mapping = {
        "LOW": "#22c55e",
        "MEDIUM": "#eab308",
        "HIGH": "#f97316",
        "CRITICAL": "#ef4444",
    }
    return mapping.get(severity.upper() if severity else "LOW", "#6b7280")
