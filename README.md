# AccuKnox AI Security Engineer Trainee Assessment — Technical Submission

> 📄 **Primary Deliverable:** **[Download Master Assessment Report (PDF)](docs/Ballapuram_Prakash_Royal_AccuKnox_Assignment.pdf)**

**Candidate:** Ballapuram Prakash Royal  
**Education:** B.Tech in Computer Science and Technology (2026), CGPA: 9.15/10, Madanapalle Institute of Technology & Science (MITS)  
**Target Role:** AI Security Engineer Trainee (AccuKnox)  
**Research Publication:** [IEEE Xplore Digital Library — Document 11518386](https://ieeexplore.ieee.org/document/11518386)  
**GitHub Profile:** [https://github.com/BallapuramPrakashRoyal](https://github.com/BallapuramPrakashRoyal)  
**Assessment PDF:** [`docs/Ballapuram_Prakash_Royal_AccuKnox_Assignment.pdf`](docs/Ballapuram_Prakash_Royal_AccuKnox_Assignment.pdf)

---

## 1. Executive Summary

This repository contains the complete, verified engineering deliverables for the **AccuKnox AI Security Engineer Trainee** assessment.

The submission covers three core assignment areas:

1. **Assignment 1 — Python & Database Engineering:**
   - **Task 1 (REST API & SQLite):** Live Open Library REST API book retrieval with normalized 3NF SQLite schema (`authors`, `books` with `openlibrary_key`, and `book_authors` junction table), parameterized SQL queries, deduplication, and formatted ASCII display. An explicit offline reference mode is supported for air-gapped environments.
   - **Task 2 (Data Processing & Visualization):** Automated HTTP student score retrieval, robust data cleaning (filtering nulls, negatives, and non-numeric entries), accurate statistical analysis (Mean: **83.42**, Median: **83.75**, Sample Std Dev: **9.75**, Population Std Dev: **9.34**), and a publication-quality 300 DPI Matplotlib bar chart with benchmark dashed lines.
   - **Task 3 (CSV Import Pipeline):** Robust CSV data ingestion with practical regex email validation, case-insensitive normalization, atomic database transactions (`BEGIN...COMMIT / ROLLBACK`), and rejected row audit logging.
   - **Existing Codebase Links:** Traceable architectural references to production-grade Python and database implementations in [FlowPilot AI](https://github.com/BallapuramPrakashRoyal/FlowPilotAI) (asynchronous DAG execution engine in `runner.py` / `dag.py` and relational schemas in `models.py`).

2. **Assignment 2 — AI, Deep Learning & LLM Systems:**
   - **Confirmed Self-Assessment:** Technical competency self-rating of **B (Can code under supervision)** across Artificial Intelligence, Machine Learning, Deep Learning, and Large Language Models.
   - **Enterprise LLM Chatbot Architecture:** Multi-tier architectural design detailing 7 core components (Client Interface, API Gateway & Rate Limiter, Ingestion/Pre-processor, LLM Inference Engine, Security Guardrails, Context & Memory Store, Monitoring & Observability) alongside optional modular extensions (RAG retriever, sandboxed tool execution, multi-agent orchestrator).
   - **AI Cybersecurity Defense-in-Depth:** Practical defense controls mitigating prompt injection, jailbreaks, training data leakage, insecure output handling, denial of service, and supply chain vulnerabilities, with explicit boundaries (access control and tool authorization enforced outside the LLM context) and full lifecycle data protection across embedding generation, inference, and logging.
   - **Vector Database Engineering:** Mathematical analysis of similarity metrics (Cosine similarity, Cosine distance $1 - \text{cosine similarity}$, Euclidean L2, Dot Product), approximate nearest neighbor indexing (HNSW hierarchical proximity graph vs. IVFFlat inverted file), vector storage sizing (~3.072 GB raw storage for 500,000 float32 1,536-dimensional vectors), and trade-off evaluation recommending PostgreSQL with `pgvector` for an internal enterprise security knowledge assistant.

3. **Assignment 3 — Research & Engineering Project (IMLPTS):**
   - Architectural deep-dive into the *Intelligent Multi-Layer Penetration Testing System Using Hybrid AI Models* (IEEE Document 11518386).
   - Multi-tier model coordination combining Random Forest (network vulnerability classification), Bidirectional LSTM (HTTP payload sequence analysis), and Deep Q-Network (Gymnasium reinforcement learning attack path selection).
   - Direct explanation of why combining these models presented genuine technical and evaluation challenges.

---

## 2. Published Directory Structure

```
accuknox-ai-security-assignment/
├── docs/
│   └── Ballapuram_Prakash_Royal_AccuKnox_Assignment.pdf  # Master assessment report (PDF)
├── README.md                                          # Technical overview and execution guide
├── requirements.txt                                   # Python dependencies
├── run_all.py                                         # Master orchestrator for all 3 tasks
├── .gitignore                                         # Git ignore rules
│
├── assignment_1/                                      # Python & Database Engineering
│   ├── api_books/
│   │   ├── api_client.py                              # REST API client (live default, offline mode)
│   │   ├── book_database.py                           # SQLite 3NF relational operations & deduplication
│   │   ├── main.py                                    # CLI driver & ASCII table formatter
│   │   └── schema.sql                                 # Relational schema (authors, books, book_authors)
│   ├── student_analysis/
│   │   ├── mock_api.py                                # HTTP mock REST server serving student scores
│   │   ├── score_analyzer.py                          # Data validation, statistics, & chart generation
│   │   └── main.py                                    # CLI driver & statistical reporter
│   ├── csv_import/
│   │   ├── importer.py                                # CSV parser & atomic transaction manager
│   │   ├── user_database.py                           # SQLite user storage & queries
│   │   ├── validator.py                               # Regex email validation & name checks
│   │   ├── main.py                                    # CLI driver & metrics reporter
│   │   └── schema.sql                                 # User table schema with unique constraints
│   ├── data/
│   │   ├── sample_students.json                       # Source student score dataset (15 records)
│   │   └── sample_users_mixed.csv                     # Sample user CSV (valid, duplicates, malformed)
│   ├── code_links.md                                  # Links to existing complex code in FlowPilot AI
│   └── requirements.txt                               # Task-level dependency reference
│
├── assignment_2/                                      # AI, ML, Deep Learning & LLMs
│   ├── self_assessment.md                             # Confirmed technical ratings & competencies
│   ├── llm_chatbot_architecture.md                    # Core architecture, data flow & security controls
│   └── vector_database_analysis.md                    # Metrics math, indexing algorithms & pgvector
│
├── assignment_3/                                      # Proudest Project (IMLPTS)
│   ├── project_overview.md                            # Comprehensive IMLPTS hybrid AI engineering
│   └── technical_challenges.md                        # Technical challenges and model coordination
│
├── outputs/                                           # Visualizations & Generated Artifacts
│   ├── student_scores_barchart.png                    # Matplotlib bar chart generated by Task 2
│   └── .gitkeep                                       # Directory preservation
│
└── tests/                                             # Automated Test Suite (20 unit & integration tests)
    ├── test_api_books.py                              # Tests for Task 1
    ├── test_student_analysis.py                       # Tests for Task 2
    └── test_csv_import.py                             # Tests for Task 3
```

---

## 3. Installation & Setup

### Prerequisites
- Python 3.10+ (Verified on Python 3.13)
- Git 2.40+

### Setup Instructions
```bash
# 1. Clone repository
git clone https://github.com/BallapuramPrakashRoyal/accuknox-ai-security-assignment.git
cd accuknox-ai-security-assignment

# 2. Create and activate a virtual environment
python -m venv .venv

# On Windows (PowerShell):
.venv\Scripts\Activate.ps1
# On Linux / macOS:
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt
```

---

## 4. Execution Commands

All scripts can be executed directly from the repository root directory.

### Run All Three Tasks Sequentially
```bash
# Live API mode (default):
python run_all.py

# Offline reference mode (for air-gapped or restricted networks):
python run_all.py --offline
```

### Run Tasks Individually

#### Task 1: REST API Retrieval & Normalized SQLite Storage
```bash
# Live execution against Open Library API:
python assignment_1/api_books/main.py --query "cybersecurity" --limit 5

# Offline mode using reference dataset:
python assignment_1/api_books/main.py --offline --limit 5
```

#### Task 2: Student Score Processing & Visualization
```bash
python assignment_1/student_analysis/main.py
```
*Note:* Automatically starts a local HTTP mock server, validates 15 raw records, drops 3 invalid entries, calculates verified statistics, and renders the Matplotlib chart at `outputs/student_scores_barchart.png`.

#### Task 3: CSV User Import into SQLite
```bash
python assignment_1/csv_import/main.py
```
*Note:* Ingests `assignment_1/data/sample_users_mixed.csv`, validates email syntax with case-insensitive normalization, rejects batch and database duplicates within an atomic transaction, and logs rejected rows.

---

## 5. Automated Test Results

The test suite contains **20 comprehensive unit and integration tests** covering API failure handling, schema migrations, junction tables, data cleaning, statistical accuracy, regex email validation, and SQL injection safety.

Run the test suite with:
```bash
pytest tests/ -v
```

### Verified Test Run Output
```
============================= test session starts =============================
platform win32 -- Python 3.13.17, pytest-9.2.0, pluggy-1.7.0
rootdir: accuknox-ai-security-assignment
collected 20 items

tests/test_api_books.py::test_schema_initialization PASSED               [  5%]
tests/test_api_books.py::test_insert_book_with_multiple_authors PASSED   [ 10%]
tests/test_api_books.py::test_duplicate_book_handling PASSED             [ 15%]
tests/test_api_books.py::test_batch_insertion_and_deduplication PASSED   [ 20%]
tests/test_api_books.py::test_sql_injection_safe_parameterization PASSED [ 25%]
tests/test_api_books.py::test_api_client_parsing_with_missing_fields PASSED [ 30%]
tests/test_api_books.py::test_api_timeout_error_handling PASSED          [ 35%]
tests/test_api_books.py::test_api_http_error_handling PASSED             [ 40%]
tests/test_api_books.py::test_api_malformed_json_handling PASSED         [ 45%]
tests/test_csv_import.py::test_name_validation PASSED                    [ 50%]
tests/test_csv_import.py::test_email_validation_standard PASSED          [ 55%]
tests/test_csv_import.py::test_sql_injection_safe_parameterization_in_csv PASSED [ 60%]
tests/test_csv_import.py::test_csv_import_pipeline_and_deduplication PASSED [ 65%]
tests/test_csv_import.py::test_missing_csv_header PASSED                 [ 70%]
tests/test_student_analysis.py::test_data_validation_and_cleaning PASSED [ 75%]
tests/test_student_analysis.py::test_duplicate_student_detection PASSED  [ 80%]
tests/test_student_analysis.py::test_statistical_metrics_calculation PASSED [ 85%]
tests/test_student_analysis.py::test_independent_average_verification PASSED [ 90%]
tests/test_student_analysis.py::test_empty_dataset_handling PASSED       [ 95%]
tests/test_student_analysis.py::test_chart_generation PASSED             [100%]

============================= 20 passed in 5.30s ==============================
```

---

## 6. Sample Execution Outputs

### Task 1: Stored Books in Normalized SQLite
```
+------+--------------------------------------------------+----------------------------+--------+
| ID   | Title                                            | Author(s)                  | Year   |
+------+--------------------------------------------------+----------------------------+--------+
| 1    | Cybersecurity For Dummies                        | Joseph Steinberg           | 2019   |
| 2    | Cybersecurity: A Very Short Introduction         | David Stupples             | 2022   |
| 3    | Transformational Security Awareness              | Perry Carpenter            | 2019   |
| 4    | The Cybersecurity Playbook                       | Allison Cerra              | 2019   |
| 5    | Practical Cybersecurity Architecture             | Ed Moyle, Diana Kelley     | 2020   |
+------+--------------------------------------------------+----------------------------+--------+
```

### Task 2: Student Score Statistics (Single Source of Truth)
```
--------------------------------------------------
  • Total Raw Records Received: 15
  • Valid Records Retained:    12
  • Corrupted Records Dropped: 3 (1 negative, 1 null, 1 non-numeric string)
--------------------------------------------------
  • Student Count:             12
  • Sum of Scores:             1001.00
  • Class Average (Mean):      83.42
  • Median Score:              83.75
  • Sample Standard Deviation: 9.75
  • Population Std Deviation:  9.34
  • Minimum Score:             63.50 (Farhan Ali)
  • Maximum Score:             96.50 (Ishita Sen)
--------------------------------------------------
```

### Task 3: CSV User Import Metrics & Rejection Log
```
==================================================
        IMPORT EXECUTION METRICS SUMMARY
==================================================
  • Total Rows Processed:       15
  • Successfully Inserted Rows: 8
  • Duplicate Rows:             2
  • Invalid Rows:               5
  • Failed Insertions:          0
==================================================
Rejected Row Log:
  - Row 8  [DUPLICATE_EMAIL]: Duplicate email 'prakash.royal@example.com' within batch
  - Row 9  [DUPLICATE_EMAIL]: Duplicate email 'aarav.sharma@example.com' within batch
  - Row 10 [INVALID_ROW]: Name cannot be empty or whitespace
  - Row 11 [INVALID_ROW]: Invalid email format: 'not-an-email-at-all'
  - Row 12 [INVALID_ROW]: Email cannot be empty or whitespace
  - Row 13 [INVALID_ROW]: Consecutive or leading/trailing dots: 'user@@domain..com'
  - Row 14 [INVALID_ROW]: Invalid email format: 'user name@domain.com'
```

---

## 7. Assignment 3 — Research & Engineering Project (IMLPTS)

**Project Title:** Intelligent Multi-Layer Penetration Testing System Using Hybrid AI Models (IMLPTS)  
**IEEE Xplore Publication:** [Document 11518386](https://ieeexplore.ieee.org/document/11518386)

### Why This Project Was Challenging:
1. Integrating Random Forest, BiLSTM, and Deep Q-Network models was challenging because each model performs a different role within the penetration-testing workflow.
2. The system required coordinating vulnerability classification and reinforcement-learning-based decision-making across multiple security assessment stages.
3. Evaluating the combined framework was more complex than evaluating individual models because their outputs had to work together to support the overall security assessment.

---

## 8. Assumptions & Limitations

1. **REST API Rate Limiting & Network Resilience:** The Open Library REST API is an open public endpoint without guaranteed uptime. An automatic retry mechanism with exponential backoff and an explicit offline fallback mode ensure test reliability.
2. **Student API Protocol:** Since no public mock student endpoint was specified, an embedded Python `http.server` mock REST API was implemented to demonstrate end-to-end HTTP payload retrieval and response handling.
3. **Email Validation Scope:** Email validation enforces standard RFC-compliant structural rules using practical regular expressions rather than performing live SMTP/DNS handshakes, avoiding false rejections of valid intranet/internal corporate domains.
4. **Vector Database Scalability:** For the hypothetical 500,000-chunk knowledge assistant, PostgreSQL with `pgvector` was selected because the raw vector footprint (~3.072 GB) comfortably fits in standard enterprise memory profiles without the operational complexity of managing a separate distributed vector database cluster.

---

## 9. Candidate Verification & Existing Codebase

- **Candidate:** Ballapuram Prakash Royal
- **Degree:** B.Tech in Computer Science and Technology (2026), CGPA 9.15/10, MITS
- **FlowPilot AI Repository:** [https://github.com/BallapuramPrakashRoyal/FlowPilotAI](https://github.com/BallapuramPrakashRoyal/FlowPilotAI)
- **IMLPTS Research Publication:** [https://ieeexplore.ieee.org/document/11518386](https://ieeexplore.ieee.org/document/11518386)
- **LinkedIn / Contact:** Available on candidate profile and master report.
