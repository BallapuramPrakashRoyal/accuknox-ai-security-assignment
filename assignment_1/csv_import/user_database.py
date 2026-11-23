"""SQLite Database Handler for Task 3: User Storage & Deduplication."""

import logging
import os
import sqlite3
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class UserDatabase:
    """Manages SQLite user table creation, queries, and atomic inserts."""

    def __init__(self, db_path: str = "users.db", schema_path: Optional[str] = None):
        self.db_path = db_path
        if schema_path is None:
            schema_path = os.path.join(os.path.dirname(__file__), "schema.sql")
        self.schema_path = schema_path

    def get_connection(self) -> sqlite3.Connection:
        """Create and return a configured connection."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    def init_db(self) -> None:
        """Initialize the users table from schema.sql."""
        if not os.path.exists(self.schema_path):
            raise FileNotFoundError(f"Schema file not found at: {self.schema_path}")

        with open(self.schema_path, "r", encoding="utf-8") as f:
            script = f.read()

        with self.get_connection() as conn:
            conn.executescript(script)
            conn.commit()
        logger.info(f"Initialized user database schema at: {self.db_path}")

    def insert_user(self, name: str, email: str) -> bool:
        """Insert a single user using parameterized SQL."""
        query = "INSERT OR IGNORE INTO users (name, email) VALUES (?, ?)"
        with self.get_connection() as conn:
            cursor = conn.execute(query, (name.strip(), email.strip().lower()))
            conn.commit()
            return cursor.rowcount > 0

    def email_exists(self, email: str) -> bool:
        """Check whether email already exists in database."""
        query = "SELECT 1 FROM users WHERE email = ? COLLATE NOCASE LIMIT 1"
        with self.get_connection() as conn:
            cursor = conn.execute(query, (email.strip().lower(),))
            return cursor.fetchone() is not None

    def get_all_users(self) -> List[Dict[str, Any]]:
        """Retrieve all users ordered by creation date."""
        query = "SELECT id, name, email, status, created_at FROM users ORDER BY id ASC"
        with self.get_connection() as conn:
            cursor = conn.execute(query)
            return [dict(row) for row in cursor.fetchall()]

    def get_user_count(self) -> int:
        """Return total count of stored users."""
        with self.get_connection() as conn:
            cursor = conn.execute("SELECT COUNT(*) AS total FROM users")
            row = cursor.fetchone()
            return row["total"] if row else 0
