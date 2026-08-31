---
name: prefect-orchestration
description: Set up and manage Prefect workflows, task queues, and auto-publishing pipelines.
---

# Prefect Orchestration

This skill provides best practices and troubleshooting steps for working with Prefect (version 2.16+) as a task orchestrator, specifically within Docker Compose environments.

## Docker Compose Setup

When setting up Prefect inside a Docker Compose network alongside other services (like FastAPI and PostgreSQL), be mindful of the following configurations:

1. **Port Binding:** Use `--host 0.0.0.0` when starting the Prefect server in Docker so it is accessible to other containers and the host machine.
   ```yaml
   prefect-server:
     image: prefecthq/prefect:2.16-python3.11
     command: prefect server start --host 0.0.0.0
     ports:
       - "4200:4200"
   ```

2. **API URL Resolution:** Configure `PREFECT_API_URL` so that services *inside* the Docker network can reach the server. Avoid using `localhost` or `127.0.0.1` for internal communication.
   ```yaml
   environment:
     - PREFECT_API_URL=http://prefect-server:4200/api
   ```

3. **Database Backend:** Prefect 2.16+ uses SQLite by default. For MVP or development, you can omit `PREFECT_API_DATABASE_CONNECTION_URL`. If you provide a PostgreSQL connection URL, ensure it is formatted correctly for sync drivers (e.g., `postgresql+asyncpg` might cause issues if Prefect expects a sync driver internally depending on the specific setup; standard `postgresql://` is safer for the Prefect server itself).

## Task Execution and Circular Imports

When integrating Prefect `@task` and `@flow` decorators with external systems like LangGraph or FastAPI:

1.  **Avoid Circular Imports:** If your tasks need access to a compiled LangGraph object or a database connection pool initialized in FastAPI's `lifespan`, **do not** import them directly at the top level of your task file if it causes a circular dependency. Instead, pass necessary IDs (like `job_id`) into the task and re-initialize or retrieve the necessary objects within the task itself, or use Dependency Injection.
2.  **SQLite Concurrency Limits:** If Prefect server crashes with `sqlite3.OperationalError: database is locked`, it's buckling under async concurrency. **Fix**: Do NOT use the default SQLite backend for a production Prefect server running alongside heavy async jobs. Set `PREFECT_API_DATABASE_CONNECTION_URL` to point to a PostgreSQL database.
3.  **Conflicting Package Versions with FastAPI/LangChain**: Prefect often pins Starlette or other dependencies that conflict with FastAPI or LangChain. **Fix:** Use `>=` instead of `==` in `requirements.txt` to let pip resolve a compatible version across all three frameworks.
- **Async Tasks:** Prefect fully supports `async def` tasks. Ensure you `await` them properly within your flows.

## Auto-Publishing Patterns

To implement auto-publishing or cron-like scheduling without relying on complex Prefect Deployments initially:

1. **Background Workers:** Create a standalone Python script (e.g., `auto_publisher.py`) that runs an infinite `asyncio.sleep` loop.
2. **Database Polling:** Have the worker query the database (e.g., PostgreSQL via SQLAlchemy) for jobs where `status == 'SCHEDULED'` and `scheduled_at <= datetime.now(timezone.utc)`.
3. **Execution:** Process the jobs, update the status to `PUBLISHED`, and commit the transaction.
4. **Docker Integration:** Run this worker as a separate service in `docker-compose.yml`:
   ```yaml
   auto_publisher:
     build: ./backend
     command: python -m app.workers.auto_publisher
     depends_on:
       - postgres
   ```

## Disk Space Management

Prefect, FastAPI, and Next.js builds can quickly consume disk space on constrained VPS environments.
- Monitor space with `df -h`.
- Aggressively clean up Docker using `docker system prune -af --volumes` and `docker builder prune -af` if you encounter `no space left on device` errors during `docker compose build`.