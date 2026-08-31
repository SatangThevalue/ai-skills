---
name: langgraph-fastapi-hitl
description: Architecture and implementation guide for building Human-in-the-Loop (HITL) workflows with LangGraph and FastAPI, including business patterns (HITL vs HOTL).
---

# LangGraph + FastAPI HITL Architecture & Business Patterns

## Core Business Patterns (HITL vs. HOTL)

When designing AI oversight, choose the right pattern based on risk vs. volume:

### 1. Human-in-the-Loop (HITL) - Synchronous Approval
*   **How it works:** AI processes data -> System flags output -> Human approves/corrects -> AI learns from feedback.
*   **Characteristics:** Synchronous, pre-decision approval. The AI advises; the human executes.
*   **Best For:** High-stakes, ambiguous, regulated decisions (e.g., healthcare diagnostics, financial approvals, legal review).
*   **Risk Profile:** Lower decision risk, higher operational delay.

### 2. Human-on-the-Loop (HOTL) - Asynchronous Supervision
*   **How it works:** AI executes autonomously -> System sends alerts/metrics -> Humans monitor for drift/risk -> Humans intervene/override when thresholds breach.
*   **Characteristics:** Asynchronous, exception-based intervention. Requires robust monitoring infrastructure.
*   **Best For:** High-volume, routine, time-sensitive tasks (e.g., fraud detection, high-speed content moderation, automated trading).
*   **Risk Profile:** Higher automated risk, lower delay.

## Design Principles for HITL Systems

1.  **Confidence Scoring & Dynamic Routing:** The AI must output a confidence score. High confidence (>95%) can be auto-approved (HOTL), medium confidence (75-95%) routes to human review (HITL), and low confidence falls back to manual processes.
2.  **Rich Review Interfaces:** Dashboards must show full context (original input alongside AI output), highlight specific changes, and capture structured feedback (not just a binary approve/reject).
3.  **Continuous Learning Loop:** Feedback must not be siloed. Capture natural language feedback to improve prompts, retrieval strategies (RAG), or fine-tune models (Agent Learning from Human Feedback - ALHF).
4.  **Mitigate Vigilance Decay:** Prevent "rubber-stamping" by limiting batch sizes, rotating reviewers, and using risk-based routing rather than reviewing every single output.

---

## Overview
When building Human-in-the-Loop (HITL) AI workflows using LangGraph and exposing them via FastAPI, the architecture must support asynchronous non-blocking execution, durable state persistence, and stateless API endpoints.

## Core Principles

1.  **Async Everywhere**: All Python code (FastAPI routes, SQLAlchemy ORM, LangChain model invocations) MUST use `async/await`. Avoid synchronous blocking calls (`.invoke()`) which will freeze the FastAPI server. Use `.ainvoke()`, `.aget_state()`, and `.aupdate_state()`.
2.  **Durable Checkpointers**: Do not use `MemorySaver` in production as state is lost on server restart. Use a database-backed checkpointer like `AsyncPostgresSaver` from `langgraph-checkpoint-postgres`.
3.  **Background Tasks**: API endpoints triggering AI work must return immediately (e.g., HTTP 202 Accepted) and delegate the LangGraph execution to `fastapi.BackgroundTasks` or an orchestrator like Prefect.

## Implementation Details

### 1. Dependencies
Requires `langgraph`, `langgraph-checkpoint-postgres`, `psycopg[binary]`, and `psycopg-pool`.

### 2. FastAPI Lifespan and Postgres Pool
Initialize the database connection pool and the LangGraph checkpointer during the FastAPI application lifespan. Use `await pool.open()` to avoid `RuntimeWarning` in modern `psycopg_pool`.

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from psycopg_pool import AsyncConnectionPool

DB_URL = "postgresql://user:pass@host:5432/dbname"
pool = None
checkpointer = None
content_graph = None # Your compiled graph

@asynccontextmanager
async def lifespan(app: FastAPI):
    global pool, checkpointer, content_graph
    pool = AsyncConnectionPool(
        conninfo=DB_URL,
        max_size=20,
        kwargs={"autocommit": True, "prepare_threshold": 0},
    )
    await pool.open() # Fixes RuntimeWarning: opening the async pool in the constructor is deprecated
    checkpointer = AsyncPostgresSaver(pool)
    await checkpointer.setup() # Ensure tables exist

    
    # Compile graph with the checkpointer and interrupt points
    content_graph = uncompiled_graph.compile(
        checkpointer=checkpointer,
        interrupt_before=["human_approval"]
    )
    yield
    await pool.close()

app = FastAPI(lifespan=lifespan)
```

### 3. Asynchronous Graph Execution (Triggering)
Generate a unique `thread_id` (e.g., UUID) for each workflow instance. Pass the execution to a background task.

```python
import uuid
from fastapi import BackgroundTasks

async def run_ai_task(thread_id: str, input_data: dict):
    config = {"configurable": {"thread_id": thread_id}}
    await content_graph.ainvoke(input_data, config=config)

@app.post("/jobs", status_code=202)
async def create_job(background_tasks: BackgroundTasks):
    job_id = str(uuid.uuid4())
    input_data = {"key": "value"} # Initial state
    background_tasks.add_task(run_ai_task, job_id, input_data)
    return {"job_id": job_id}
```

### 4. Checking Status and Reading State
Read the current state to check if the graph is waiting at the interrupt point.

```python
@app.get("/jobs/{job_id}")
async def get_job_status(job_id: str):
    config = {"configurable": {"thread_id": job_id}}
    state_snapshot = await content_graph.aget_state(config)
    
    if not state_snapshot:
        return {"error": "Not found"}
        
    current_state = state_snapshot.values
    # Check if the next node is the interrupt point
    is_waiting = len(state_snapshot.next) > 0 and "human_approval" in state_snapshot.next
    
    return {"status": "waiting" if is_waiting else "processing", "data": current_state}
```

### 5. Approving and Resuming (HITL)
Update the graph state based on human input, then resume execution as a background task.

```python
async def resume_ai_task(thread_id: str):
    config = {"configurable": {"thread_id": thread_id}}
    await content_graph.ainvoke(None, config=config)

@app.post("/jobs/{job_id}/approve", status_code=202)
async def approve_job(job_id: str, action: str, background_tasks: BackgroundTasks):
    config = {"configurable": {"thread_id": job_id}}
    
    # Update the state with the human decision
    await content_graph.aupdate_state(
        config,
        {"approval_status": action} # Update specific state keys
    )
    
    # Resume the graph in the background
    background_tasks.add_task(resume_ai_task, job_id)
    return {"message": "Job resumed"}
```

## Pitfalls
-   **Forgetting to setup the Checkpointer**: Failing to call `await checkpointer.setup()` will result in `UndefinedTable` errors when the graph tries to save state.
-   **Compiling graph outside async loop**: The `AsyncPostgresSaver` must be instantiated and the graph compiled within an active asyncio event loop (e.g., inside the FastAPI lifespan function), otherwise you will encounter event loop attachment errors. Build the graph definition synchronously, but compile it asynchronously.
-   **Dependency Conflicts**: When installing LangGraph and FastAPI, watch for conflicting Starlette requirements (often caused by older versions of Prefect or other orchestration tools). Use `>=` in `requirements.txt` and allow the resolver to find a compatible set.
-   **Prefect + SQLAlchemy Circular Imports**: When moving from raw FastAPI `BackgroundTasks` to Prefect tasks (`@task`), circular imports often occur if the Prefect task module imports the compiled LangGraph object back from the FastAPI main file. **Fix**: Do not import `content_graph` directly into the Prefect tasks. Pass the `job_id` and initialize/invoke the graph directly within the worker, or use Dependency Injection.
-   **Prefect `pool.open()` RuntimeWarning**: When using `psycopg_pool.AsyncConnectionPool` with SQLAlchemy inside FastAPI `lifespan()`, newer versions throw a `RuntimeWarning` if the pool is opened via the constructor implicitly. **Fix**: Create the pool without opening it immediately, then explicitly `await pool.open()` inside the `lifespan` block before passing it to `AsyncPostgresSaver`.