"""Unit and Integration Tests for Task 1: Book API Retrieval & Normalized SQLite Storage."""

import os
import sys
import tempfile
import unittest.mock as mock
import pytest
import requests

TASK1_DIR = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "assignment_1",
    "api_books"
)
sys.path.insert(0, TASK1_DIR)

from api_client import BookAPIClient
from book_database import BookDatabase


@pytest.fixture
def temp_db():
    """Create a temporary SQLite database for test isolation."""
    import gc
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    db = BookDatabase(db_path=path)
    db.init_db()
    yield db
    del db
    gc.collect()
    try:
        if os.path.exists(path):
            os.remove(path)
    except OSError:
        pass


def test_schema_initialization(temp_db):
    """Verify tables and indexes are created properly."""
    with temp_db.get_connection() as conn:
        cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row["name"] for row in cursor.fetchall()]
        assert "authors" in tables
        assert "books" in tables
        assert "book_authors" in tables


def test_insert_book_with_multiple_authors(temp_db):
    """Verify that normalized many-to-many author relationship stores multiple authors."""
    inserted, b_id = temp_db.insert_book(
        title="Computer Systems Security",
        authors=["William Stallings", "Lawrie Brown"],
        publication_year=2018,
        isbn="9780134794105"
    )
    assert inserted is True
    assert b_id is not None

    all_books = temp_db.get_all_books()
    assert len(all_books) == 1
    # Both authors should appear in the concatenated authors string
    assert "William Stallings" in all_books[0]["authors"]
    assert "Lawrie Brown" in all_books[0]["authors"]
    assert temp_db.get_author_count() == 2


def test_duplicate_book_handling(temp_db):
    """Verify identical book records are deduplicated without crashing."""
    inserted1, _ = temp_db.insert_book(
        title="Malware Analysis Guide",
        authors=["Michael Sikorski"],
        publication_year=2012
    )
    assert inserted1 is True

    # Attempt to insert duplicate
    inserted2, _ = temp_db.insert_book(
        title="Malware Analysis Guide",
        authors=["Michael Sikorski"],
        publication_year=2012
    )
    assert inserted2 is False
    assert temp_db.get_book_count() == 1


def test_batch_insertion_and_deduplication(temp_db):
    """Verify atomic batch book insertion and metrics calculation."""
    sample_books = [
        {"title": "Book A", "authors": ["Author One"], "publication_year": 2018},
        {"title": "Book B", "authors": ["Author Two"], "publication_year": 2019},
        {"title": "Book A", "authors": ["Author One"], "publication_year": 2018},  # Duplicate
        {"title": "", "authors": ["Author Three"], "publication_year": 2020}       # Empty title
    ]
    summary = temp_db.insert_books_batch(sample_books)
    assert summary["total_processed"] == 4
    assert summary["inserted"] == 2
    assert summary["duplicates"] == 1
    assert temp_db.get_book_count() == 2


def test_sql_injection_safe_parameterization(temp_db):
    """Verify malicious SQL payloads in book titles are safely escaped."""
    malicious_title = "Safe Book'); DROP TABLE books;--"
    inserted, b_id = temp_db.insert_book(
        title=malicious_title,
        authors=["Adversarial Author"],
        publication_year=2024
    )
    assert inserted is True
    # Table must still exist and contain the book
    books = temp_db.get_all_books()
    assert len(books) == 1
    assert books[0]["title"] == malicious_title


def test_api_client_parsing_with_missing_fields():
    """Verify parser handles documents with missing author or year."""
    client = BookAPIClient()
    mock_docs = [
        {
            "title": "Clean Architecture",
            "author_name": ["Robert C. Martin"],
            "first_publish_year": 2017,
            "isbn": ["9780134494166"]
        },
        {
            "title": "Anonymous Treatise"
            # Missing author_name, first_publish_year, isbn
        }
    ]
    parsed = client._parse_api_response(mock_docs, limit=5)
    assert len(parsed) == 2
    assert parsed[0]["authors"] == ["Robert C. Martin"]
    assert parsed[1]["authors"] == ["Unknown Author"]
    assert parsed[1]["publication_year"] is None


def test_api_timeout_error_handling():
    """Verify client handles API timeout properly."""
    client = BookAPIClient(timeout=1)
    with mock.patch.object(client.session, "get", side_effect=requests.exceptions.Timeout("Request timed out")):
        # In default mode (allow_fallback=False), should raise ConnectionError
        with pytest.raises(ConnectionError, match="Failed to connect"):
            client.fetch_books(query="cybersecurity", limit=3, allow_fallback=False)

        # In fallback mode (allow_fallback=True), should return fallback dataset cleanly
        books, source = client.fetch_books(query="cybersecurity", limit=3, allow_fallback=True)
        assert len(books) == 3
        assert "OFFLINE_FALLBACK" in source


def test_api_http_error_handling():
    """Verify client handles HTTP 500 error properly."""
    client = BookAPIClient()
    mock_resp = mock.Mock()
    mock_resp.raise_for_status.side_effect = requests.exceptions.HTTPError("500 Server Error")
    with mock.patch.object(client.session, "get", return_value=mock_resp):
        with pytest.raises(ConnectionError):
            client.fetch_books(query="cybersecurity", limit=3, allow_fallback=False)


def test_api_malformed_json_handling():
    """Verify client handles invalid non-JSON payload properly."""
    client = BookAPIClient()
    mock_resp = mock.Mock()
    mock_resp.raise_for_status.return_value = None
    mock_resp.json.side_effect = ValueError("Invalid JSON string")
    with mock.patch.object(client.session, "get", return_value=mock_resp):
        with pytest.raises(ValueError, match="Malformed JSON"):
            client.fetch_books(query="cybersecurity", limit=3, allow_fallback=False)
