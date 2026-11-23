"""CLI Runner for Task 1: Book API Retrieval & Normalized SQLite Storage."""

import argparse
import logging
import os
import sys
from typing import List, Dict, Any

from api_client import BookAPIClient
from book_database import BookDatabase

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("Task1_Main")


def format_table(records: List[Dict[str, Any]]) -> str:
    """Format book records into an aligned ASCII table."""
    if not records:
        return "No records found in database."

    headers = ["ID", "Title", "Author(s)", "Year", "ISBN"]
    col_widths = {
        "ID": 4,
        "Title": 38,
        "Author(s)": 30,
        "Year": 6,
        "ISBN": 15
    }

    sep = "+" + "+".join(["-" * (w + 2) for w in col_widths.values()]) + "+"
    header_line = "| " + " | ".join([h.ljust(col_widths[h]) for h in headers]) + " |"
    lines = [sep, header_line, sep]

    for r in records:
        b_id = str(r.get("id", ""))
        title = str(r.get("title", ""))
        if len(title) > col_widths["Title"]:
            title = title[: col_widths["Title"] - 3] + "..."
        authors = str(r.get("authors") or r.get("author") or "Unknown Author")
        if len(authors) > col_widths["Author(s)"]:
            authors = authors[: col_widths["Author(s)"] - 3] + "..."
        year = str(r.get("publication_year") or "N/A")
        isbn = str(r.get("isbn") or "N/A")
        if len(isbn) > col_widths["ISBN"]:
            isbn = isbn[: col_widths["ISBN"] - 3] + "..."

        row_str = (
            f"| {b_id.ljust(col_widths['ID'])} "
            f"| {title.ljust(col_widths['Title'])} "
            f"| {authors.ljust(col_widths['Author(s)'])} "
            f"| {year.ljust(col_widths['Year'])} "
            f"| {isbn.ljust(col_widths['ISBN'])} |"
        )
        lines.append(row_str)

    lines.append(sep)
    return "\n".join(lines)


def run_pipeline(
    query: str = "cybersecurity",
    limit: int = 8,
    db_path: str = "books.db",
    allow_fallback: bool = False
) -> None:
    """Execute end-to-end extraction, storage, and presentation."""
    print("=" * 85)
    print(" ACCUKNOX TASK 1: REST API RETRIEVAL & NORMALIZED SQLITE STORAGE")
    print(f" Target Query: '{query}' | Record Limit: {limit} | Database: '{db_path}'")
    print(f" Mode: {'OFFLINE FALLBACK ALLOWED' if allow_fallback else 'LIVE API DEFAULT (Requires Internet)'}")
    print("=" * 85)

    # 1. Initialize Normalized Database
    db = BookDatabase(db_path=db_path)
    db.init_db()

    # 2. Fetch Books from REST API
    client = BookAPIClient()
    try:
        books, source_label = client.fetch_books(query=query, limit=limit, allow_fallback=allow_fallback)
        print(f"\n[+] DATA SOURCE: [{source_label}]")
        print(f"[+] Retrieved {len(books)} records.")
    except ConnectionError as exc:
        print(f"\n[!] NETWORK ERROR: {exc}")
        print("[!] Note: To test in an isolated offline environment, use the --offline flag.")
        sys.exit(1)

    # 3. Store Books into SQLite Database with Deduplication
    summary = db.insert_books_batch(books)
    print(f"[+] Storage Summary:")
    print(f"    - Processed in batch:  {summary['total_processed']}")
    print(f"    - Newly inserted:      {summary['inserted']}")
    print(f"    - Existing handled:    {summary['duplicates']}")
    print(f"    - Total unique books:  {db.get_book_count()}")
    print(f"    - Total unique authors:{db.get_author_count()}")

    # 4. Query and Display Stored Records
    all_books = db.get_all_books()
    print(f"\n[+] Stored Books in Database (Total: {len(all_books)}):")
    print(format_table(all_books))
    print("[✓] Task 1 completed successfully.\n")


def main() -> None:
    repo_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    default_db = os.path.join(repo_root, "outputs", "books.db")

    parser = argparse.ArgumentParser(description="Fetch books from REST API and store into normalized SQLite.")
    parser.add_argument("--query", type=str, default="cybersecurity", help="Book topic query (default: cybersecurity)")
    parser.add_argument("--limit", type=int, default=8, help="Number of records to fetch (default: 8)")
    parser.add_argument("--db", type=str, default=default_db, help="SQLite database path (default: outputs/books.db)")
    parser.add_argument("--offline", action="store_true", help="Explicitly enable offline reference dataset if network is unavailable")
    args = parser.parse_args()

    run_pipeline(query=args.query, limit=args.limit, db_path=args.db, allow_fallback=args.offline)


if __name__ == "__main__":
    main()
