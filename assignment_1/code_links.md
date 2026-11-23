# Assignment 1: Existing Python and Database Code Links

**Candidate:** Ballapuram Prakash Royal  
**Role Target:** AI Security Engineer Trainee (AccuKnox)  

---

## 1. Most Complex Python Code Written

### Direct GitHub Reference
- **Repository:** [FlowPilotAI](https://github.com/BallapuramPrakashRoyal/FlowPilotAI)
- **Primary Link:** [`FlowPilotAI/backend/app/engine/runner.py` (Commit df0f775)](https://github.com/BallapuramPrakashRoyal/FlowPilotAI/blob/df0f775710d3c0edac7edb954a973a24f58e0955/backend/app/engine/runner.py)
- **Supporting File:** [`FlowPilotAI/backend/app/engine/dag.py` (Commit df0f775)](https://github.com/BallapuramPrakashRoyal/FlowPilotAI/blob/df0f775710d3c0edac7edb954a973a24f58e0955/backend/app/engine/dag.py)

### Technical Description of Implementation
In `backend/app/engine/runner.py` and `dag.py`, I implemented an asynchronous workflow execution engine:
- **Graph Resolution:** Evaluates computational graph structures representing workflow steps, resolving execution order based on node dependencies.
- **Cycle Detection:** Checks for circular dependencies during graph validation before execution begins.
- **State Handling:** Coordinates execution states (`PENDING`, `RUNNING`, `WAITING_APPROVAL`, `COMPLETED`, `FAILED`) across asynchronous tasks using Python's `asyncio` library.
- **Retry Logic:** Implements step-level retry mechanisms with configurable exponential backoff to handle transient step failures.
- **Task Dispatching:** Passes execution payloads to Celery background workers for longer-running tasks.

---

## 2. Most Complex Database Code Written

### Direct GitHub Reference
- **Repository:** [FlowPilotAI](https://github.com/BallapuramPrakashRoyal/FlowPilotAI)
- **Primary Link:** [`FlowPilotAI/backend/app/database/models.py` (Commit df0f775)](https://github.com/BallapuramPrakashRoyal/FlowPilotAI/blob/df0f775710d3c0edac7edb954a973a24f58e0955/backend/app/database/models.py)
- **Supporting File (RAG Vector Queries):** [`FlowPilotAI/backend/app/ai/rag/service.py` (Commit df0f775)](https://github.com/BallapuramPrakashRoyal/FlowPilotAI/blob/df0f775710d3c0edac7edb954a973a24f58e0955/backend/app/ai/rag/service.py)

### Technical Description of Implementation
In `backend/app/database/models.py` and `backend/app/ai/rag/service.py`, I implemented relational schemas and vector query integration using SQLAlchemy 2.0 (async):
- **Relational Schema Design:** Designed 12+ relational models (including `User`, `Workspace`, `WorkflowVersion`, `IntegrationCredential`, `ExecutionNode`, `KnowledgeBase`, and `DocumentChunk`) with foreign key constraints, cascading deletes (`ondelete="CASCADE"`), and compound unique constraints (such as `(workspace_id, user_id)`).
- **Workspace-Isolated Vector Retrieval:** In `app/ai/rag/service.py`, implemented vector search queries that enforce multi-tenant isolation by joining `DocumentChunk`, `Document`, and `KnowledgeBase` tables before evaluating cosine vector similarity, ensuring users cannot query documents outside their assigned workspace.
- **Schema Migrations:** Integrated Alembic migration scripts (`backend/alembic/versions`) to track and apply database schema changes in development and test environments.
