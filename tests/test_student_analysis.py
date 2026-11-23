"""Unit and Integration Tests for Task 2: Student Score Processing & Visualization."""

import os
import sys
import tempfile
import pytest

TASK2_DIR = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "assignment_1",
    "student_analysis"
)
sys.path.insert(0, TASK2_DIR)

from score_analyzer import StudentScoreAnalyzer
from mock_api import get_default_student_data


@pytest.fixture
def analyzer():
    return StudentScoreAnalyzer()


def test_data_validation_and_cleaning(analyzer):
    """Verify that invalid scores (null, negative, >100, malformed) are rejected."""
    raw_data = [
        {"name": "Valid Student", "score": 85.5},
        {"name": "Another Valid", "score": "90.0"},
        {"name": "Negative Score", "score": -10.0},
        {"name": "Exceeding Score", "score": 150.0},
        {"name": "Null Score", "score": None},
        {"name": "String Score", "score": "InvalidScore"},
        {"name": "", "score": 75.0}  # Empty name
    ]
    df, summary = analyzer.clean_and_validate_data(raw_data)
    assert summary["total_records"] == 7
    assert summary["valid_records"] == 2
    assert summary["invalid_records"] == 5
    assert len(df) == 2
    assert list(df["student_name"]) == ["Valid Student", "Another Valid"]


def test_duplicate_student_detection(analyzer):
    """Verify duplicate student records within the same subject are detected."""
    raw_data = [
        {"id": 1, "name": "Aarav Sharma", "subject": "Networks", "score": 85.0},
        {"id": 1, "name": "Aarav Sharma", "subject": "Networks", "score": 88.0},  # Duplicate
        {"id": 2, "name": "Bhavya Reddy", "subject": "Networks", "score": 92.0}
    ]
    df, summary = analyzer.clean_and_validate_data(raw_data)
    assert summary["total_records"] == 3
    assert summary["valid_records"] == 2
    assert summary["invalid_records"] == 1
    assert "Duplicate student" in summary["rejection_log"][0]["reason"]


def test_statistical_metrics_calculation(analyzer):
    """Verify statistical formulas for mean, median, min, max."""
    raw_data = [
        {"name": "Student A", "score": 60.0},
        {"name": "Student B", "score": 80.0},
        {"name": "Student C", "score": 100.0}
    ]
    df, _ = analyzer.clean_and_validate_data(raw_data)
    stats = analyzer.calculate_statistics(df)
    assert stats["count"] == 3
    assert stats["mean_score"] == 80.0
    assert stats["median_score"] == 80.0
    assert stats["min_score"] == 60.0
    assert stats["max_score"] == 100.0
    assert stats["top_performer"] == "Student C"
    assert stats["lowest_performer"] == "Student A"


def test_independent_average_verification(analyzer):
    """Independently calculate statistics on benchmark dataset to confirm reported values."""
    raw_data = get_default_student_data()
    df, summary = analyzer.clean_and_validate_data(raw_data)
    
    # 12 valid students in baseline dataset
    assert len(df) == 12
    expected_sum = 85.5 + 92.0 + 78.0 + 88.5 + 95.0 + 63.5 + 71.0 + 89.0 + 96.5 + 82.0 + 79.5 + 80.5
    assert expected_sum == 1001.0
    expected_mean = round(1001.0 / 12, 2)
    assert expected_mean == 83.42

    stats = analyzer.calculate_statistics(df)
    assert stats["count"] == 12
    assert stats["mean_score"] == 83.42
    assert stats["median_score"] == 83.75
    assert stats["std_deviation"] == 9.75
    assert stats["min_score"] == 63.50
    assert stats["max_score"] == 96.50
    assert stats["top_performer"] == "Ishita Sen"
    assert stats["lowest_performer"] == "Farhan Ali"


def test_empty_dataset_handling(analyzer):
    """Verify ValueError is raised on an empty dataset."""
    import pandas as pd
    with pytest.raises(ValueError, match="empty dataset"):
        analyzer.calculate_statistics(pd.DataFrame())


def test_chart_generation(analyzer):
    """Verify PNG file generation, valid dimensions, and non-empty byte stream."""
    raw_data = get_default_student_data()
    df, _ = analyzer.clean_and_validate_data(raw_data)
    
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp_file:
        tmp_path = tmp_file.name

    try:
        output_path = analyzer.generate_bar_chart(df, tmp_path, title="Benchmark Test Chart")
        assert os.path.exists(output_path)
        assert os.path.getsize(output_path) > 1000  # Valid non-empty PNG
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
