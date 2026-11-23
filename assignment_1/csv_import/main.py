"""CLI Driver for Task 3: CSV User Import into SQLite."""

import argparse
import logging
import os
import sys

from user_database import UserDatabase
from importer import CSVUserImporter

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("Task3_Main")


def run_pipeline(csv_file: str, db_file: str) -> None:
    """Execute end-to-end CSV parsing, validation, and SQLite import."""
    print("=" * 80)
    print(" ACCUKNOX TASK 3: CSV DATA IMPORT INTO SQLITE PIPELINE")
    print(f" Source File: '{csv_file}' | Database: '{db_file}'")
    print("=" * 80)

    db = UserDatabase(db_path=db_file)
    importer = CSVUserImporter(db)

    metrics = importer.import_csv(csv_file)

    print("\n" + "=" * 50)
    print("        IMPORT EXECUTION METRICS SUMMARY")
    print("=" * 50)
    print(f"  • Total Rows Processed:       {metrics['total_rows_processed']}")
    print(f"  • Successfully Inserted Rows: {metrics['successfully_inserted_rows']}")
    print(f"  • Duplicate Rows:             {metrics['duplicate_rows']}")
    print(f"  • Invalid Rows:               {metrics['invalid_rows']}")
    print(f"  • Failed Insertions:          {metrics['failed_insertions']}")
    print("=" * 50)

    if metrics["rejections"]:
        print("\n[!] Detailed Row Rejection Audit Log:")
        for r in metrics["rejections"]:
            print(f"    - Row {r['row']} [{r['type']}]: {r['reason']}")

    # Display final database contents
    all_users = db.get_all_users()
    print(f"\n[+] Verified SQLite Database Records (Total: {len(all_users)}):")
    header_str = f"| {'ID'.ljust(4)} | {'Name'.ljust(25)} | {'Email'.ljust(35)} | {'Status'.ljust(8)} |"
    sep = "-" * len(header_str)
    print(sep)
    print(header_str)
    print(sep)
    for u in all_users:
        u_id = str(u["id"]).ljust(4)
        name = u["name"][:25].ljust(25)
        email = u["email"][:35].ljust(35)
        status = str(u.get("status", "ACTIVE")).ljust(8)
        print(f"| {u_id} | {name} | {email} | {status} |")
    print(sep)
    print("[✓] Task 3 completed successfully.\n")


def main() -> None:
    repo_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    default_csv = os.path.join(repo_root, "assignment_1", "data", "sample_users_mixed.csv")
    default_db = os.path.join(repo_root, "outputs", "users.db")

    parser = argparse.ArgumentParser(description="Import users from CSV into SQLite.")
    parser.add_argument("--csv", type=str, default=default_csv, help="Path to input CSV file")
    parser.add_argument("--db", type=str, default=default_db, help="Path to SQLite database file")
    args = parser.parse_args()

    run_pipeline(args.csv, args.db)


if __name__ == "__main__":
    main()
