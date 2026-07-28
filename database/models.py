"""
database/models.py
-------------------
Data-access functions (simple "model" layer) for CyberShield ONE.

Every function opens its own short-lived connection via db.get_connection()
and closes it before returning. This keeps Streamlit's rerun-heavy
execution model simple and avoids shared-connection threading issues.

No password hashing or business logic beyond simple CRUD lives here -
that belongs in utils/security.py and the services/ layer.
"""

from datetime import datetime
from typing import Optional
import json

from database.db import get_connection, dict_from_row


# ---------------------------------------------------------------------
# USERS
# ---------------------------------------------------------------------

def create_user(name: str, email: str, password_hash: str) -> int:
    """Insert a new user. Returns the new user's id."""
    conn = get_connection()
    try:
        cur = conn.execute(
            "INSERT INTO users (name, email, password_hash, created_at) "
            "VALUES (?, ?, ?, ?)",
            (name, email.lower().strip(), password_hash, datetime.utcnow().isoformat()),
        )
        conn.commit()
        return cur.lastrowid
    finally:
        conn.close()


def get_user_by_email(email: str) -> Optional[dict]:
    conn = get_connection()
    try:
        row = conn.execute(
            "SELECT * FROM users WHERE email = ?", (email.lower().strip(),)
        ).fetchone()
        return dict_from_row(row) if row else None
    finally:
        conn.close()


def get_user_by_id(user_id: int) -> Optional[dict]:
    conn = get_connection()
    try:
        row = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
        return dict_from_row(row) if row else None
    finally:
        conn.close()


def email_exists(email: str) -> bool:
    return get_user_by_email(email) is not None


# ---------------------------------------------------------------------
# SECURITY SCORES
# ---------------------------------------------------------------------

def insert_security_score(user_id: int, password_score: float, email_score: float,
                           phishing_score: float, web_score: float, privacy_score: float,
                           overall_score: float, risk_level: str) -> int:
    conn = get_connection()
    try:
        cur = conn.execute(
            """INSERT INTO security_scores
               (user_id, password_score, email_score, phishing_score,
                web_score, privacy_score, overall_score, risk_level, created_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (user_id, password_score, email_score, phishing_score, web_score,
             privacy_score, overall_score, risk_level, datetime.utcnow().isoformat()),
        )
        conn.commit()
        return cur.lastrowid
    finally:
        conn.close()


def get_latest_score(user_id: int) -> Optional[dict]:
    conn = get_connection()
    try:
        row = conn.execute(
            "SELECT * FROM security_scores WHERE user_id = ? "
            "ORDER BY created_at DESC, id DESC LIMIT 1",
            (user_id,),
        ).fetchone()
        return dict_from_row(row) if row else None
    finally:
        conn.close()


def get_score_history(user_id: int, limit: int = 30) -> list:
    conn = get_connection()
    try:
        rows = conn.execute(
            "SELECT * FROM security_scores WHERE user_id = ? "
            "ORDER BY created_at ASC LIMIT ?",
            (user_id, limit),
        ).fetchall()
        return [dict_from_row(r) for r in rows]
    finally:
        conn.close()


# ---------------------------------------------------------------------
# SECURITY EVENTS
# ---------------------------------------------------------------------

def log_security_event(user_id: int, event_type: str, severity: str, description: str) -> int:
    conn = get_connection()
    try:
        cur = conn.execute(
            """INSERT INTO security_events (user_id, event_type, severity, description, created_at)
               VALUES (?, ?, ?, ?, ?)""",
            (user_id, event_type, severity, description, datetime.utcnow().isoformat()),
        )
        conn.commit()
        return cur.lastrowid
    finally:
        conn.close()


def get_recent_events(user_id: int, limit: int = 15) -> list:
    conn = get_connection()
    try:
        rows = conn.execute(
            "SELECT * FROM security_events WHERE user_id = ? "
            "ORDER BY created_at DESC LIMIT ?",
            (user_id, limit),
        ).fetchall()
        return [dict_from_row(r) for r in rows]
    finally:
        conn.close()


# ---------------------------------------------------------------------
# RECOMMENDATIONS
# ---------------------------------------------------------------------

def add_recommendation(user_id: int, category: str, priority: str, recommendation: str) -> int:
    conn = get_connection()
    try:
        cur = conn.execute(
            """INSERT INTO recommendations (user_id, category, priority, recommendation, status, created_at)
               VALUES (?, ?, ?, ?, 'OPEN', ?)""",
            (user_id, category, priority, recommendation, datetime.utcnow().isoformat()),
        )
        conn.commit()
        return cur.lastrowid
    finally:
        conn.close()


def get_recommendations(user_id: int, status: Optional[str] = None) -> list:
    conn = get_connection()
    try:
        if status:
            rows = conn.execute(
                "SELECT * FROM recommendations WHERE user_id = ? AND status = ? "
                "ORDER BY created_at DESC",
                (user_id, status),
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT * FROM recommendations WHERE user_id = ? ORDER BY created_at DESC",
                (user_id,),
            ).fetchall()
        return [dict_from_row(r) for r in rows]
    finally:
        conn.close()


def update_recommendation_status(rec_id: int, status: str) -> None:
    conn = get_connection()
    try:
        conn.execute("UPDATE recommendations SET status = ? WHERE id = ?", (status, rec_id))
        conn.commit()
    finally:
        conn.close()


# ---------------------------------------------------------------------
# PRIVACY CHECKS
# ---------------------------------------------------------------------

def save_privacy_check(user_id: int, score: float, answers: dict) -> int:
    conn = get_connection()
    try:
        cur = conn.execute(
            """INSERT INTO privacy_checks (user_id, score, answers_json, created_at)
               VALUES (?, ?, ?, ?)""",
            (user_id, score, json.dumps(answers), datetime.utcnow().isoformat()),
        )
        conn.commit()
        return cur.lastrowid
    finally:
        conn.close()


def get_latest_privacy_check(user_id: int) -> Optional[dict]:
    conn = get_connection()
    try:
        row = conn.execute(
            "SELECT * FROM privacy_checks WHERE user_id = ? "
            "ORDER BY created_at DESC LIMIT 1",
            (user_id,),
        ).fetchone()
        return dict_from_row(row) if row else None
    finally:
        conn.close()


# ---------------------------------------------------------------------
# QUIZ RESULTS
# ---------------------------------------------------------------------

def save_quiz_result(user_id: int, score: float, total_questions: int) -> int:
    conn = get_connection()
    try:
        cur = conn.execute(
            """INSERT INTO quiz_results (user_id, score, total_questions, created_at)
               VALUES (?, ?, ?, ?)""",
            (user_id, score, total_questions, datetime.utcnow().isoformat()),
        )
        conn.commit()
        return cur.lastrowid
    finally:
        conn.close()


def get_latest_quiz_result(user_id: int) -> Optional[dict]:
    conn = get_connection()
    try:
        row = conn.execute(
            "SELECT * FROM quiz_results WHERE user_id = ? "
            "ORDER BY created_at DESC LIMIT 1",
            (user_id,),
        ).fetchone()
        return dict_from_row(row) if row else None
    finally:
        conn.close()
