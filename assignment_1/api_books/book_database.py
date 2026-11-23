"""SQLite Database Handler for Task 1: Normalized Book & Author Storage."""

import logging
import os
import sqlite3
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


class BookDatabase:
    """Manages SQLite database connections, schema execution, and normalized book-author operations."""

    def __init__(self, db_path: str = "books.db", schema_path: Optional[str] = None):
        self.db_path = db_path
        if schema_path is None:
            schema_path = os.path.join(os.path.dirname(__file__), "schema.sql")
        self.schema_path = schema_path

    def get_connection(self) -> sqlite3.Connection:
        """Create and return a configured SQLite connection with foreign keys enabled."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    def init_db(self) -> None:
        """Initialize normalized database tables and indexes from schema.sql."""
        if not os.path.exists(self.schema_path):
            raise FileNotFoundError(f"Schema file not found at: {self.schema_path}")

        with open(self.schema_path, "r", encoding="utf-8") as f:
            schema_script = f.read()

        with self.get_connection() as conn:
            conn.executescript(schema_script)
            # Ensure openlibrary_key exists if database was created with an earlier schema version
            cursor = conn.execute("PRAGMA table_info(books)")
            cols = [row["name"] for row in cursor.fetchall()]
            if "openlibrary_key" not in cols:
                conn.execute("ALTER TABLE books ADD COLUMN openlibrary_key TEXT")
                conn.execute("CREATE INDEX IF NOT EXISTS idx_books_ol_key ON books(openlibrary_key)")
            conn.commit()
        logger.info(f"Initialized normalized SQLite database at: {self.db_path}")

    def get_or_create_author(self, conn: sqlite3.Connection, author_name: str) -> int:
        """Retrieve existing author ID or insert a new author record."""
        clean_name = (author_name or "Unknown Author").strip()
        
        cursor = conn.execute("SELECT id FROM authors WHERE name = ? COLLATE NOCASE", (clean_name,))
        row = cursor.fetchone()
        if row:
            return int(row["id"])

        cursor = conn.execute("INSERT INTO authors (name) VALUES (?)", (clean_name,))
        return cursor.lastrowid

    def insert_book(
        self,
        title: str,
        authors: List[str],
        publication_year: Optional[int],
        isbn: Optional[str] = None,
        openlibrary_key: Optional[str] = None
    ) -> Tuple[bool, Optional[int]]:
        """Insert a book and associate its authors via the book_authors junction table.
        
        Where available, prefers stable Open Library key identifier for book identity,
        falling back to (title, publication_year).
        
        Returns:
            Tuple of (is_new_insertion: bool, book_id: Optional[int])
        """
        clean_title = (title or "").strip()
        if not clean_title:
            logger.warning("Skipping insertion: Book title cannot be empty.")
            return False, None

        if not authors:
            authors = ["Unknown Author"]

        with self.get_connection() as conn:
            try:
                # 1. Check if book already exists (by openlibrary_key first if present, then title + pub_year)
                existing = None
                if openlibrary_key:
                    cursor = conn.execute(
                        "SELECT id FROM books WHERE openlibrary_key = ?",
                        (openlibrary_key,)
                    )
                    existing = cursor.fetchone()

                if not existing:
                    cursor = conn.execute(
                        "SELECT id FROM books WHERE title = ? AND publication_year IS ?",
                        (clean_title, publication_year)
                    )
                    existing = cursor.fetchone()

                if existing:
                    book_id = int(existing["id"])
                    # Link any newly identified authors
                    for author_name in authors:
                        author_id = self.get_or_create_author(conn, author_name)
                        conn.execute(
                            "INSERT OR IGNORE INTO book_authors (book_id, author_id) VALUES (?, ?)",
                            (book_id, author_id)
                        )
                    conn.commit()
                    return False, book_id

                # 2. Insert new book record
                cursor = conn.execute(
                    "INSERT INTO books (title, publication_year, isbn, openlibrary_key) VALUES (?, ?, ?, ?)",
                    (clean_title, publication_year, isbn, openlibrary_key)
                )
                book_id = cursor.lastrowid

                # 3. Associate all authors in junction table
                for author_name in authors:
                    author_id = self.get_or_create_author(conn, author_name)
                    conn.execute(
                        "INSERT OR IGNORE INTO book_authors (book_id, author_id) VALUES (?, ?)",
                        (book_id, author_id)
                    )

                conn.commit()
                return True, book_id

            except sqlite3.Error as exc:
                logger.error(f"Database error inserting book '{clean_title}': {exc}")
                conn.rollback()
                raise

    def insert_books_batch(self, books: List[Dict[str, Any]]) -> Dict[str, int]:
        """Insert multiple books within a single atomic database transaction."""
        inserted_count = 0
        duplicate_count = 0

        with self.get_connection() as conn:
            try:
                for b in books:
                    title = (b.get("title") or "").strip()
                    if not title:
                        continue

                    raw_authors = b.get("authors")
                    if isinstance(raw_authors, list):
                        authors = raw_authors
                    elif isinstance(b.get("author"), str):
                        authors = [b.get("author")]
                    else:
                        authors = ["Unknown Author"]

                    pub_year = b.get("publication_year")
                    isbn = b.get("isbn")
                    ol_key = b.get("openlibrary_key")

                    # Check for duplicate by openlibrary_key first, then title + pub_year
                    existing = None
                    if ol_key:
                        cursor = conn.execute(
                            "SELECT id FROM books WHERE openlibrary_key = ?",
                            (ol_key,)
                        )
                        existing = cursor.fetchone()

                    if not existing:
                        cursor = conn.execute(
                            "SELECT id FROM books WHERE title = ? AND publication_year IS ?",
                            (title, pub_year)
                        )
                        existing = cursor.fetchone()

                    if existing:
                        duplicate_count += 1
                        book_id = int(existing["id"])
                    else:
                        cursor = conn.execute(
                            "INSERT INTO books (title, publication_year, isbn, openlibrary_key) VALUES (?, ?, ?, ?)",
                            (title, pub_year, isbn, ol_key)
                        )
                        book_id = cursor.lastrowid
                        inserted_count += 1

                    # Associate authors
                    for author_name in authors:
                        author_id = self.get_or_create_author(conn, author_name)
                        conn.execute(
                            "INSERT OR IGNORE INTO book_authors (book_id, author_id) VALUES (?, ?)",
                            (book_id, author_id)
                        )

                conn.commit()
                logger.info(
                    f"Batch complete: {inserted_count} new books stored, "
                    f"{duplicate_count} existing books handled."
                )
            except sqlite3.Error as exc:
                logger.error(f"Transaction failed during batch insertion: {exc}")
                conn.rollback()
                raise

        return {
            "total_processed": len(books),
            "inserted": inserted_count,
            "duplicates": duplicate_count
        }

    def get_all_books(self) -> List[Dict[str, Any]]:
        """Retrieve all books joined with all their authors via the junction table."""
        query = """
            SELECT 
                b.id,
                b.title,
                COALESCE(GROUP_CONCAT(a.name, ', '), 'Unknown Author') AS authors,
                b.publication_year,
                b.isbn,
                b.created_at
            FROM books b
            LEFT JOIN book_authors ba ON b.id = ba.book_id
            LEFT JOIN authors a ON ba.author_id = a.id
            GROUP BY b.id
            ORDER BY b.publication_year DESC NULLS LAST, b.title ASC
        """
        with self.get_connection() as conn:
            cursor = conn.execute(query)
            rows = cursor.fetchall()
            return [dict(row) for row in rows]

    def get_book_count(self) -> int:
        """Return total count of unique books."""
        with self.get_connection() as conn:
            cursor = conn.execute("SELECT COUNT(*) AS total FROM books")
            row = cursor.fetchone()
            return row["total"] if row else 0

    def get_author_count(self) -> int:
        """Return total count of unique authors."""
        with self.get_connection() as conn:
            cursor = conn.execute("SELECT COUNT(*) AS total FROM authors")
            row = cursor.fetchone()
            return row["total"] if row else 0
