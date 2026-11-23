"""Student Score Processing, Statistical Analysis, and Matplotlib Visualization.

Implementation Note & Assumption:
Since no public student-score API endpoint was provided in the problem statement,
a local REST API (mock_api.py) serving synthetic student test scores was created to
demonstrate the complete HTTP data retrieval, data validation, and analysis workflow.
"""

import logging
import os
import tempfile
from typing import Any, Dict, List, Optional, Tuple
import requests

# Ensure Matplotlib operates reliably in headless environments without GUI popups
os.environ.setdefault("MPLCONFIGDIR", os.path.join(tempfile.gettempdir(), "mpl_cache"))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

logger = logging.getLogger(__name__)


class StudentScoreAnalyzer:
    """Fetches student score data, validates numerical values, and generates visualizations."""

    def __init__(self, timeout: int = 5):
        self.timeout = timeout

    def fetch_scores_from_api(self, api_url: str) -> List[Dict[str, Any]]:
        """Fetch student scores from external or local REST API endpoint."""
        logger.info(f"Connecting to REST API endpoint: {api_url}")
        try:
            resp = requests.get(api_url, timeout=self.timeout)
            resp.raise_for_status()
            data = resp.json()
            if isinstance(data, dict) and "data" in data:
                return data["data"]
            elif isinstance(data, list):
                return data
            else:
                raise ValueError(f"Unexpected JSON structure received from API: {type(data)}")
        except requests.exceptions.RequestException as exc:
            logger.error(f"API communication failure: {exc}")
            raise

    def clean_and_validate_data(self, raw_records: List[Dict[str, Any]]) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """Validate, sanitize, and convert raw records into a clean Pandas DataFrame.
        
        Validation rules:
        - Student name must be non-empty string.
        - Score must be a valid numeric float between 0.0 and 100.0.
        - Missing or malformed values are tracked and dropped from statistical calculation.
        - Duplicate student records within the same subject are tracked and deduplicated.
        """
        valid_records = []
        invalid_records = []
        seen_students = set()

        for item in raw_records:
            name = item.get("name")
            raw_score = item.get("score")
            subject = item.get("subject", "Computer Networks")
            student_id = item.get("id")

            # Validate name
            if not name or not isinstance(name, str) or not name.strip():
                invalid_records.append({"record": item, "reason": "Missing or empty student name"})
                continue

            cleaned_name = name.strip()

            # Validate numerical score
            if raw_score is None:
                invalid_records.append({"record": item, "reason": "Score is null/None"})
                continue

            try:
                numeric_score = float(raw_score)
            except (ValueError, TypeError):
                invalid_records.append({"record": item, "reason": f"Non-numeric score value: '{raw_score}'"})
                continue

            # Check logical bounds
            if numeric_score < 0.0 or numeric_score > 100.0:
                invalid_records.append({"record": item, "reason": f"Score {numeric_score} outside valid range [0, 100]"})
                continue

            # Check duplicate student within the same subject
            dedup_key = (student_id or cleaned_name.lower(), subject.lower())
            if dedup_key in seen_students:
                invalid_records.append({"record": item, "reason": f"Duplicate student score entry for '{cleaned_name}'"})
                continue

            seen_students.add(dedup_key)
            valid_records.append({
                "student_id": student_id,
                "student_name": cleaned_name,
                "subject": subject.strip(),
                "score": round(numeric_score, 2)
            })

        df = pd.DataFrame(valid_records)
        validation_summary = {
            "total_records": len(raw_records),
            "valid_records": len(valid_records),
            "invalid_records": len(invalid_records),
            "rejection_log": invalid_records
        }
        logger.info(
            f"Data validation complete: {len(valid_records)} valid rows retained, "
            f"{len(invalid_records)} invalid rows rejected."
        )
        return df, validation_summary

    def calculate_statistics(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Compute statistical metrics from validated student scores."""
        if df.empty:
            raise ValueError("Cannot calculate statistics on an empty dataset.")

        scores = df["score"]
        stats = {
            "count": int(scores.count()),
            "mean_score": round(float(scores.mean()), 2),
            "median_score": round(float(scores.median()), 2),
            "std_deviation": round(float(scores.std()), 2) if len(scores) > 1 else 0.0,
            "min_score": round(float(scores.min()), 2),
            "max_score": round(float(scores.max()), 2),
            "top_performer": df.loc[scores.idxmax()]["student_name"],
            "top_performer_score": float(scores.max()),
            "lowest_performer": df.loc[scores.idxmin()]["student_name"],
            "lowest_performer_score": float(scores.min()),
        }
        return stats

    def generate_bar_chart(
        self,
        df: pd.DataFrame,
        output_png_path: str,
        title: str = "Student Test Score Performance"
    ) -> str:
        """Render a clean, readable Matplotlib bar chart and save as PNG.
        
        Features:
        - Sorted bars for clear visual comparison.
        - Dual-color differentiation (above average vs below average).
        - Prominent dashed threshold line indicating class mean score.
        - Data labels on top of bars.
        - Clear title, axes, and legend.
        """
        if df.empty:
            raise ValueError("Cannot generate chart from an empty DataFrame.")

        # Ensure output directory exists safely
        try:
            os.makedirs(os.path.dirname(os.path.abspath(output_png_path)), exist_ok=True)
        except OSError:
            pass

        # Sort students by score descending for readability
        sorted_df = df.sort_values(by="score", ascending=False).reset_index(drop=True)
        mean_score = sorted_df["score"].mean()

        # Clean color scheme: dark slate blue and forest green
        colors = ["#1b5e20" if s >= mean_score else "#0d47a1" for s in sorted_df["score"]]

        fig, ax = plt.subplots(figsize=(11, 6), dpi=300)

        bars = ax.bar(
            sorted_df["student_name"],
            sorted_df["score"],
            color=colors,
            width=0.55,
            edgecolor="#263238",
            linewidth=0.75,
            zorder=3
        )

        # Draw Class Average Line
        ax.axhline(
            y=mean_score,
            color="#c62828",
            linestyle="--",
            linewidth=1.75,
            label=f"Class Average: {mean_score:.2f}",
            zorder=4
        )

        # Data value annotations directly above bars
        for bar in bars:
            height = bar.get_height()
            ax.annotate(
                f"{height:.1f}",
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 4),
                textcoords="offset points",
                ha="center",
                va="bottom",
                fontsize=9,
                fontweight="bold",
                color="#212121"
            )

        subject_name = sorted_df["subject"].iloc[0] if "subject" in sorted_df else "Assessment"
        ax.set_title(f"{title} ({subject_name})", fontsize=13, fontweight="bold", pad=14)
        ax.set_xlabel("Student Name", fontsize=10, fontweight="bold", labelpad=8)
        ax.set_ylabel("Test Score (0 – 100)", fontsize=10, fontweight="bold", labelpad=8)
        ax.set_ylim(0, 110)

        ax.set_xticks(range(len(sorted_df)))
        ax.set_xticklabels(sorted_df["student_name"], rotation=30, ha="right", fontsize=9)

        ax.yaxis.grid(True, linestyle=":", alpha=0.5, color="#90a4ae", zorder=0)
        ax.set_axisbelow(True)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

        ax.legend(loc="upper right", frameon=True, facecolor="#ffffff", edgecolor="#cfd8dc", fontsize=9.5)

        plt.tight_layout()
        plt.savefig(output_png_path, dpi=300)
        plt.close(fig)
        logger.info(f"Bar chart successfully saved to: {output_png_path}")
        return output_png_path
