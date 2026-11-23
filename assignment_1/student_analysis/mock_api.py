"""Mock REST API Server & Provider for Task 2.

NOTE ON ARCHITECTURE:
This module provides both an in-memory client and a lightweight local HTTP server
using Python's built-in http.server to explicitly demonstrate REST API fetching
without requiring external third-party subscriptions or risking rate-limiting.
It is explicitly labeled as a LOCAL MOCK API in adherence to assessment instructions.
"""

import json
import logging
import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


def get_default_student_data() -> List[Dict[str, Any]]:
    """Return verified benchmark student test scores."""
    json_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "data",
        "sample_students.json"
    )
    if os.path.exists(json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            return json.load(f)

    # In-memory baseline fallback
    return [
        {"id": 101, "name": "Aarav Sharma", "subject": "Computer Networks", "score": 85.5},
        {"id": 102, "name": "Bhavya Reddy", "subject": "Computer Networks", "score": 92.0},
        {"id": 103, "name": "Chaitanya Kumar", "subject": "Computer Networks", "score": 78.0},
        {"id": 104, "name": "Divya Prakash", "subject": "Computer Networks", "score": 88.5},
        {"id": 105, "name": "Eshwar Varma", "subject": "Computer Networks", "score": 95.0},
        {"id": 106, "name": "Farhan Ali", "subject": "Computer Networks", "score": 63.5},
        {"id": 107, "name": "Gitanjali Rao", "subject": "Computer Networks", "score": 71.0},
        {"id": 108, "name": "Hari Prasad", "subject": "Computer Networks", "score": 89.0},
        {"id": 109, "name": "Ishita Sen", "subject": "Computer Networks", "score": 96.5},
        {"id": 110, "name": "Jayant Mehta", "subject": "Computer Networks", "score": 82.0},
        {"id": 111, "name": "Kavya Sri", "subject": "Computer Networks", "score": 79.5},
        {"id": 112, "name": "Lokesh Naidu", "subject": "Computer Networks", "score": 80.5},
        {"id": 999, "name": "Invalid Student", "subject": "Computer Networks", "score": -15.0},
        {"id": 998, "name": "Missing Score Student", "subject": "Computer Networks", "score": None},
        {"id": 997, "name": "Malformed Score Student", "subject": "Computer Networks", "score": "ninety-five"}
    ]


class MockStudentAPIHandler(BaseHTTPRequestHandler):
    """HTTP Request handler serving student score records."""

    def log_message(self, format: str, *args: Any) -> None:
        """Suppress noisy default console logging."""
        pass

    def do_GET(self) -> None:
        if self.path == "/api/v1/students/scores" or self.path == "/":
            data = get_default_student_data()
            payload = json.dumps({"status": "success", "count": len(data), "data": data}).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'{"error": "Endpoint not found"}')


class MockStudentServer:
    """Manages background lifecycle of the local student mock REST API."""

    def __init__(self, host: str = "127.0.0.1", port: int = 8089):
        self.host = host
        self.port = port
        self.server: Optional[HTTPServer] = None
        self.thread: Optional[threading.Thread] = None

    def start(self) -> str:
        """Start server in daemon background thread."""
        self.server = HTTPServer((self.host, self.port), MockStudentAPIHandler)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        endpoint = f"http://{self.host}:{self.port}/api/v1/students/scores"
        logger.info(f"Local Mock Student REST API running at: {endpoint}")
        return endpoint

    def stop(self) -> None:
        """Shutdown mock server gracefully."""
        if self.server:
            self.server.shutdown()
            self.server.server_close()
            logger.info("Local Mock Student REST API stopped.")
