"""CLI Driver for Task 2: Student Score Processing and Visualization."""

import argparse
import logging
import os
import sys

from mock_api import MockStudentServer, get_default_student_data
from score_analyzer import StudentScoreAnalyzer

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("Task2_Main")


def run_pipeline(api_url: str = None, output_png: str = None) -> None:
    """Execute student score retrieval, validation, statistics, and visualization."""
    repo_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    if output_png is None:
        output_png = os.path.join(repo_root, "outputs", "student_scores_barchart.png")

    print("=" * 85)
    print(" ACCUKNOX TASK 2: STUDENT SCORE PROCESSING & VISUALIZATION PIPELINE")
    print(f" Target Output Image: '{output_png}'")
    print("=" * 85)
    print("\n[IMPLEMENTATION NOTE / DOCUMENTED ASSUMPTION]")
    print("Since no student-score API endpoint was provided in the problem statement,")
    print("I created a local REST API serving synthetic student test scores to demonstrate")
    print("the complete data retrieval, numerical validation, and analysis workflow.")

    server = None
    analyzer = StudentScoreAnalyzer()

    try:
        # Step 1: Start local mock API if no external URL provided
        if not api_url:
            print("\n[+] Starting Local Student REST API Server (Python http.server)...")
            server = MockStudentServer(host="127.0.0.1", port=8089)
            api_url = server.start()

        # Step 2: Fetch student scores
        print(f"[+] Fetching student score dataset from: {api_url}")
        raw_records = analyzer.fetch_scores_from_api(api_url)
        print(f"    - Received raw payload containing {len(raw_records)} records.")

        # Step 3: Validate and clean records
        print("\n[+] Validating numerical score ranges and student identifiers...")
        df, validation = analyzer.clean_and_validate_data(raw_records)
        print(f"    - Total records received: {validation['total_records']}")
        print(f"    - Valid records retained: {validation['valid_records']}")
        print(f"    - Invalid records dropped: {validation['invalid_records']}")
        for rejected in validation["rejection_log"]:
            print(f"      * [DROPPED] Record ID: {rejected['record'].get('id')} - Reason: {rejected['reason']}")

        # Step 4: Calculate statistical metrics
        print("\n[+] Calculating statistical metrics across student scores:")
        stats = analyzer.calculate_statistics(df)
        print("-" * 55)
        print(f"  • Student Count:         {stats['count']}")
        print(f"  • Class Average (Mean):  {stats['mean_score']:.2f}")
        print(f"  • Median Score:          {stats['median_score']:.2f}")
        print(f"  • Standard Deviation:    {stats['std_deviation']:.2f}")
        print(f"  • Minimum Score:         {stats['min_score']:.2f} ({stats['lowest_performer']})")
        print(f"  • Maximum Score:         {stats['max_score']:.2f} ({stats['top_performer']})")
        print("-" * 55)

        # Step 5: Render and save Matplotlib visualization
        print("\n[+] Generating clean Matplotlib bar chart visualization...")
        saved_path = analyzer.generate_bar_chart(df, output_png, title="Student Performance")
        # Also sync to assignment_1/outputs if directory exists
        sub_out = os.path.join(repo_root, "assignment_1", "outputs", "student_scores_barchart.png")
        if os.path.exists(os.path.dirname(sub_out)) and os.path.abspath(output_png) != os.path.abspath(sub_out):
            import shutil
            shutil.copy2(saved_path, sub_out)
        print(f"[✓] Visualization successfully written to: {saved_path}")
        print("[✓] Task 2 completed successfully.\n")

    finally:
        if server:
            server.stop()


def main() -> None:
    parser = argparse.ArgumentParser(description="Process student scores and generate visualization.")
    parser.add_argument("--url", type=str, default=None, help="REST API endpoint for student scores (defaults to local mock server)")
    parser.add_argument("--output", type=str, default=None, help="Output PNG path for generated bar chart")
    args = parser.parse_args()

    run_pipeline(api_url=args.url, output_png=args.output)


if __name__ == "__main__":
    main()
