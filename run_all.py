"""End-to-end Orchestration Script for Assignment 1 Tasks 1, 2, and 3."""

import argparse
import os
import subprocess
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TASK1_MAIN = os.path.join(BASE_DIR, "assignment_1", "api_books", "main.py")
TASK2_MAIN = os.path.join(BASE_DIR, "assignment_1", "student_analysis", "main.py")
TASK3_MAIN = os.path.join(BASE_DIR, "assignment_1", "csv_import", "main.py")
OUTPUTS_DIR = os.path.join(BASE_DIR, "outputs")
CSV_FILE = os.path.join(BASE_DIR, "assignment_1", "data", "sample_users_mixed.csv")

PYTHON_EXE = sys.executable


def run_command(cmd, desc):
    print("\n" + "=" * 85)
    print(f" >>> EXECUTING {desc} <<<")
    print("=" * 85)
    result = subprocess.run(cmd, capture_output=False, text=True)
    if result.returncode != 0:
        print(f"[!] {desc} failed with returncode {result.returncode}")
        sys.exit(result.returncode)


def main():
    parser = argparse.ArgumentParser(description="Run all AccuKnox Assignment 1 pipelines.")
    parser.add_argument("--offline", action="store_true", help="Explicitly enable offline reference dataset for Task 1 in network-restricted environments")
    args = parser.parse_args()

    # 1. Run Task 1
    books_db = os.path.join(OUTPUTS_DIR, "books.db")
    task1_cmd = [PYTHON_EXE, TASK1_MAIN, "--query", "cybersecurity", "--limit", "8", "--db", books_db]
    if args.offline:
        task1_cmd.append("--offline")

    run_command(task1_cmd, "TASK 1: REST API RETRIEVAL & NORMALIZED SQLITE STORAGE")

    # 2. Run Task 2
    chart_png = os.path.join(OUTPUTS_DIR, "student_scores_barchart.png")
    run_command(
        [PYTHON_EXE, TASK2_MAIN, "--output", chart_png],
        "TASK 2: STUDENT SCORE PROCESSING & VISUALIZATION"
    )

    # 3. Run Task 3
    users_db = os.path.join(OUTPUTS_DIR, "users.db")
    run_command(
        [PYTHON_EXE, TASK3_MAIN, "--csv", CSV_FILE, "--db", users_db],
        "TASK 3: CSV DATA IMPORT INTO SQLITE"
    )

    print("\n" + "=" * 85)
    print(" [✓] ALL THREE ASSIGNMENT 1 PIPELINES COMPLETED SUCCESSFULLY!")
    print("=" * 85)


if __name__ == "__main__":
    main()
