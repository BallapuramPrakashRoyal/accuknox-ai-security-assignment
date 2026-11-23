"""Unit and Integration Tests for Task 3: CSV User Import into SQLite."""

import os
import sqlite3
import sys
import tempfile
import unittest.mock as mock
import pytest

TASK3_DIR = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "assignment_1",
    "csv_import"
)
sys.path.insert(0, TASK3_DIR)

from user_database import UserDatabase
from importer import CSVUserImporter
from validator import validate_name, validate_email, validate_user_row


@pytest.fixture
def temp_db():
    import gc
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    db = UserDatabase(db_path=path)
    db.init_db()
    yield db
    del db
    gc.collect()
    try:
        if os.path.exists(path):
            os.remove(path)
    except OSError:
        pass


def test_name_validation():
    ok, val, err = validate_name("Prakash Royal")
    assert ok is True
    assert val == "Prakash Royal"

    ok, _, err = validate_name("")
    assert ok is False
    assert "empty" in err.lower()

    ok, _, err = validate_name("A")
    assert ok is False
    assert "at least 2" in err.lower()

    ok, _, err = validate_name("User<script>")
    assert ok is False
    assert "invalid characters" in err.lower()


def test_email_validation_standard():
    ok, val, err = validate_email("prakash.royal@example.com")
    assert ok is True
    assert val == "prakash.royal@example.com"

    # Case normalization to lowercase
    ok, val, err = validate_email("PRAKASH.ROYAL@EXAMPLE.COM")
    assert ok is True
    assert val == "prakash.royal@example.com"

    # Malformed emails
    ok, _, err = validate_email("invalid-email-address")
    assert ok is False

    ok, _, err = validate_email("user@domain..com")
    assert ok is False

    ok, _, err = validate_email("user @domain.com")
    assert ok is False


def test_sql_injection_safe_parameterization_in_csv(temp_db):
    """Verify malicious SQL payloads in name and email are safely parameterized."""
    importer = CSVUserImporter(temp_db)
    csv_content = """Name,Email
Robert'); DROP TABLE users;--,robert.drop@example.com
"""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False, encoding="utf-8") as f:
        f.write(csv_content)
        temp_csv = f.name

    try:
        metrics = importer.import_csv(temp_csv)
        assert metrics["total_rows_processed"] == 1
        # Robert'); DROP TABLE... has invalid characters for our name validator
        assert metrics["invalid_rows"] == 1
        assert temp_db.get_user_count() == 0
    finally:
        if os.path.exists(temp_csv):
            os.remove(temp_csv)


def test_csv_import_pipeline_and_deduplication(temp_db):
    """Test importing a CSV with valid records, intra-batch duplicates, and malformed rows."""
    importer = CSVUserImporter(temp_db)
    csv_content = """Name,Email
Alice Johnson,alice.j@example.com
Bob Smith,bob.s@example.com
Charlie Brown,charlie.b@example.com
Alice Johnson,ALICE.J@EXAMPLE.COM
,missing.name@example.com
Invalid Email,not-an-email
Duplicate User,bob.s@example.com
"""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False, encoding="utf-8") as f:
        f.write(csv_content)
        temp_csv = f.name

    try:
        metrics = importer.import_csv(temp_csv)
        assert metrics["total_rows_processed"] == 7
        assert metrics["successfully_inserted_rows"] == 3
        assert metrics["duplicate_rows"] == 2
        assert metrics["invalid_rows"] == 2
        assert metrics["failed_insertions"] == 0
        assert temp_db.get_user_count() == 3

        # Re-importing same file: all previously valid rows are identified as duplicates
        metrics_second = importer.import_csv(temp_csv)
        assert metrics_second["successfully_inserted_rows"] == 0
        assert metrics_second["duplicate_rows"] == 5
        assert metrics_second["invalid_rows"] == 2
        assert temp_db.get_user_count() == 3
    finally:
        if os.path.exists(temp_csv):
            os.remove(temp_csv)


def test_missing_csv_header(temp_db):
    """Verify ValueError is raised if required headers are absent."""
    importer = CSVUserImporter(temp_db)
    csv_content = """User,Contact
Alice,alice@example.com
"""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False, encoding="utf-8") as f:
        f.write(csv_content)
        temp_csv = f.name

    try:
        with pytest.raises(ValueError, match="CSV header validation failed"):
            importer.import_csv(temp_csv)
    finally:
        if os.path.exists(temp_csv):
            os.remove(temp_csv)
