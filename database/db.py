"""
database/db.py
--------------
Central SQLite connection handling for CyberShield ONE.

Responsibilities:
- Create/open the SQLite database file.
- Execute the schema on first run.
- Provide a single `get_connection()` helper used across the app.

No business logic lives here - only connection + initialization.
"""

import os
import sqlite3
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # python-dotenv is optional at import time; .env is still read
    # gracefully by os.environ if the variable is set another way.
    pass

BASE_DIR = Path(__file__).resolve().parent.parent
DEFAULT_DB_PATH = BASE_DIR / "database" / "cybershield.db"
SCHEMA_PATH = BASE_DIR / "database" / "schema.sql"

DB_PATH = Path(os.environ.get("DATABASE_PATH", DEFAULT_DB_PATH))
if not DB_PATH.is_absolute():
    DB_PATH = BASE_DIR / DB_PATH


def get_connection() -> sqlite3.Connection:
    """
    Return a SQLite connection with foreign keys enabled and
    row factory set so rows behave like dictionaries.
    """
    conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """
    Create the database file (if needed) and apply schema.sql.
    Safe to call multiple times - uses CREATE TABLE IF NOT EXISTS.
    """
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = get_connection()
    try:
        with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
            schema_sql = f.read()
        conn.executescript(schema_sql)
        conn.commit()
    finally:
        conn.close()


def dict_from_row(row: sqlite3.Row) -> dict:
    """Convert a sqlite3.Row into a plain dict (helper for reuse)."""
    if row is None:
        return {}
    return {key: row[key] for key in row.keys()}


if __name__ == "__main__":
    # Allows: python database/db.py  -> quick manual init/test
    init_db()
    print(f"Database initialized at: {DB_PATH}")
