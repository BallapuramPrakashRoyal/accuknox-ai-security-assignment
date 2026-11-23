"""CSV User Importer with Row-by-Row Validation, Deduplication, and Transactions."""

import csv
import logging
import os
import sqlite3
from typing import Any, Dict, List, Optional, Tuple

from user_database import UserDatabase
from validator import validate_user_row

logger = logging.getLogger(__name__)


class CSVUserImporter:
    """Imports user data from CSV into SQLite with transactional integrity."""

    def __init__(self, db: UserDatabase):
        self.db = db

    def import_csv(self, csv_filepath: str) -> Dict[str, Any]:
        """Process CSV file, validate records, and persist valid unique entries.
        
        Args:
            csv_filepath: Absolute or relative path to target CSV file.
            
        Returns:
            Dictionary containing comprehensive execution metrics.
        """
        if not os.path.exists(csv_filepath):
            raise FileNotFoundError(f"Target CSV file not found: {csv_filepath}")

        # Ensure database and table exist
        self.db.init_db()

        total_rows = 0
        inserted_rows = 0
        duplicate_rows = 0
        invalid_rows = 0
        failed_insertions = 0
        rejection_details: List[Dict[str, Any]] = []

        # In-memory tracking of seen emails within the current batch to catch intra-CSV duplicates
        seen_emails_in_batch = set()

        logger.info(f"Starting CSV import from file: {csv_filepath}")

        with open(csv_filepath, mode="r", encoding="utf-8-sig") as csv_file:
            reader = csv.DictReader(csv_file)

            # Validate header presence
            headers = [h.strip().lower() for h in (reader.fieldnames or [])]
            if "name" not in headers or "email" not in headers:
                raise ValueError(
                    f"CSV header validation failed. Required columns 'Name' and 'Email' not found in: {reader.fieldnames}"
                )

            # Open a single database transaction connection
            with self.db.get_connection() as conn:
                for row_idx, raw_row in enumerate(reader, start=1):
                    total_rows += 1

                    # 1. Row-level validation
                    is_valid, clean_row, error_reason = validate_user_row(raw_row, row_idx)
                    if not is_valid:
                        invalid_rows += 1
                        rejection_details.append({
                            "row": row_idx,
                            "type": "INVALID_ROW",
                            "reason": error_reason,
                            "raw_data": raw_row
                        })
                        continue

                    email = clean_row["email"]
                    name = clean_row["name"]

                    # 2. Check intra-batch duplicate
                    if email in seen_emails_in_batch:
                        duplicate_rows += 1
                        rejection_details.append({
                            "row": row_idx,
                            "type": "DUPLICATE_EMAIL",
                            "reason": f"Duplicate email '{email}' encountered within CSV batch",
                            "raw_data": raw_row
                        })
                        continue

                    # 3. Check persistent database duplicate
                    cursor = conn.execute("SELECT 1 FROM users WHERE email = ? COLLATE NOCASE LIMIT 1", (email,))
                    if cursor.fetchone():
                        duplicate_rows += 1
                        rejection_details.append({
                            "row": row_idx,
                            "type": "DUPLICATE_EMAIL",
                            "reason": f"Email '{email}' already exists in SQLite database",
                            "raw_data": raw_row
                        })
                        continue

                    # 4. Attempt parameterized insertion inside transaction savepoint
                    try:
                        cursor = conn.execute(
                            "INSERT INTO users (name, email) VALUES (?, ?)",
                            (name, email)
                        )
                        if cursor.rowcount > 0:
                            inserted_rows += 1
                            seen_emails_in_batch.add(email)
                        else:
                            duplicate_rows += 1
                    except sqlite3.IntegrityError as exc:
                        duplicate_rows += 1
                        rejection_details.append({
                            "row": row_idx,
                            "type": "INTEGRITY_ERROR",
                            "reason": f"SQLite IntegrityError: {exc}",
                            "raw_data": raw_row
                        })
                    except sqlite3.Error as exc:
                        failed_insertions += 1
                        rejection_details.append({
                            "row": row_idx,
                            "type": "DATABASE_ERROR",
                            "reason": f"SQLite Execution error: {exc}",
                            "raw_data": raw_row
                        })

                # Commit all successful operations atomically
                conn.commit()

        summary = {
            "csv_file": csv_filepath,
            "total_rows_processed": total_rows,
            "successfully_inserted_rows": inserted_rows,
            "duplicate_rows": duplicate_rows,
            "invalid_rows": invalid_rows,
            "failed_insertions": failed_insertions,
            "rejections": rejection_details
        }

        logger.info(
            f"Import finished: {inserted_rows}/{total_rows} inserted, "
            f"{duplicate_rows} duplicates, {invalid_rows} invalid, {failed_insertions} failed."
        )
        return summary
