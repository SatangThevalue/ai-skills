# Satang AI Studio Architecture

Enterprise AI Content Automation pipeline designed for multi-tenant (Agency) use with Human-in-the-loop (HITL).

## Tech Stack
- **Frontend:** Next.js 16+ (App Router, Tailwind, Zod) - Role-based UI (Admin vs Client Post Simulator)
- **Backend:** FastAPI (Python 3.11+, SQLAlchemy Async, Pydantic v2)
- **Database:** PostgreSQL (Multi-tenant IAM, Billing/Usage tracking, JSONB metadata)
- **Orchestration:** Prefect (Task Queue & Cron Scheduling)
- **AI Core:** LangGraph (State Machine), LangChain, Deep Agent
- **Integrations:** FastMCP (Tools)

## Core Architectural Patterns
1. **HITL via LangGraph Checkpointer**: 
   - Agent drafts content -> LangGraph interrupts state (`PostgresSaver`) -> FastAPI returns pending status to UI.
   - Client approves/edits -> FastAPI resumes graph -> Agent forks formatting for specific platforms (Parallel processing).
2. **Orchestration**:
   - Prefect handles background processing of LangGraph tasks to ensure the FastAPI server never blocks threads while waiting for LLM completions.
3. **Database Constraints**:
   - Usage logs capture input/output tokens strictly for billing accuracy.
   - All Python DB calls use `asyncpg` and SQLAlchemy Async.

## Pitfalls & Workarounds
1. **Dependency Conflict (FastAPI + Prefect)**:
   - `fastapi` (e.g., 0.109.2) and older `prefect` (e.g., 2.14.2) versions have strict, conflicting bounds on `starlette`. 
   - **Fix:** Use `prefect>=2.16.0` alongside `fastapi>=0.109.2` to resolve the Starlette dependency collision.
2. **Docker Postgres Port Collision**:
   - The VPS host often runs an existing Postgres instance on port 5432. Map the dockerized Postgres to `5433:5432` in `docker-compose.yml` to avoid binding errors on `docker compose up`.