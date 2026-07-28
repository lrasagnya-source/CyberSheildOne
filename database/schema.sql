-- =========================================================
-- CyberShield ONE - SQLite Schema
-- =========================================================

PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS users (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    name          TEXT NOT NULL,
    email         TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    created_at    TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS security_scores (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id         INTEGER NOT NULL,
    password_score  REAL NOT NULL DEFAULT 0,
    email_score     REAL NOT NULL DEFAULT 0,
    phishing_score  REAL NOT NULL DEFAULT 0,
    web_score       REAL NOT NULL DEFAULT 0,
    privacy_score   REAL NOT NULL DEFAULT 0,
    overall_score   REAL NOT NULL DEFAULT 0,
    risk_level      TEXT NOT NULL DEFAULT 'UNKNOWN',
    created_at      TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS security_events (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id      INTEGER NOT NULL,
    event_type   TEXT NOT NULL,
    severity     TEXT NOT NULL DEFAULT 'LOW',
    description  TEXT NOT NULL,
    created_at   TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS recommendations (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id        INTEGER NOT NULL,
    category       TEXT NOT NULL,
    priority       TEXT NOT NULL DEFAULT 'MEDIUM',
    recommendation TEXT NOT NULL,
    status         TEXT NOT NULL DEFAULT 'OPEN',
    created_at     TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS privacy_checks (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id     INTEGER NOT NULL,
    score       REAL NOT NULL DEFAULT 0,
    answers_json TEXT,
    created_at  TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS quiz_results (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id         INTEGER NOT NULL,
    score           REAL NOT NULL DEFAULT 0,
    total_questions INTEGER NOT NULL DEFAULT 0,
    created_at      TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_scores_user       ON security_scores (user_id);
CREATE INDEX IF NOT EXISTS idx_events_user        ON security_events (user_id);
CREATE INDEX IF NOT EXISTS idx_recommendations_user ON recommendations (user_id);
CREATE INDEX IF NOT EXISTS idx_privacy_user       ON privacy_checks (user_id);
CREATE INDEX IF NOT EXISTS idx_quiz_user          ON quiz_results (user_id);
