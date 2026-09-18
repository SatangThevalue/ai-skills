---
name: prefect-orchestration
description: Set up and manage Prefect workflows, task queues, and auto-publishing pipelines.
---

# Prefect Orchestration

This skill provides best practices and troubleshooting steps for working with Prefect (version 2.16+) as a task orchestrator, specifically within Docker Compose environments.

## Docker Compose Setup

When setting up Prefect inside a Docker Compose network alongside other services (like FastAPI and PostgreSQL), be mindful of the following configurations:

14. **Port Binding Security:** Use `--host 0.0.0.0` when starting the Prefect server in Docker so it is accessible to other containers. **Crucially, bind the exposed port strictly to localhost** (`127.0.0.1:4200:4200`) to prevent unauthorized internet access to your orchestrator.
15.    ```yaml
16.    prefect-server:
17.      image: prefecthq/prefect:2.16-python3.11
18.      command: prefect server start --host 0.0.0.0
19.      ports:
20.        - "127.0.0.1:4200:4200"
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

## 5. Offline / Local Mode Constraints (VPS Hardware Limits)

When running Prefect flows on constrained VPS hardware (e.g., 2 vCPUs, < 1GB available RAM), attempting to run the default Prefect daemon and SQLite backend simultaneously with heavy data/ML tasks (like LightGBM training loops) often causes system-wide hangups:

- **The Error:** `sqlite3.OperationalError: database is locked` cascading into `RuntimeError: Timed out while attempting to connect to ephemeral Prefect API server.`
- **The Cause:** Prefect attempts to boot an ephemeral API server to handle telemetry and tracking. The heavy I/O of parallel training tasks chokes SQLite and the VPS CPU, causing the ephemeral server to time out.
- **The Fix:**
  1. **Disable Ephemeral Server:** Hard-disable the API and telemetry in your script before importing Prefect or running the flow:
     ```python
     os.environ["PREFECT_API_URL"] = ""
     os.environ["PREFECT_LOCAL_STORAGE_PATH"] = os.path.join(os.getcwd(), ".prefect")
     os.environ["PREFECT_LOGGING_LEVEL"] = "WARNING" # or ERROR to reduce I/O
     ```
  2. **Force Sequential Execution:** Prevent parallel task execution to save RAM and SQLite locks by overriding the flow's task runner:
     ```python
     from prefect.task_runners import ThreadPoolTaskRunner
     
     @flow(name="Constrained Flow", task_runner=ThreadPoolTaskRunner(max_workers=1))
     def my_heavy_flow():
         # Tasks run sequentially
     ```
  3. **Rate Limiting:** If tasks hit external APIs (like `yfinance`), use Prefect's built-in rate limiting inside the loop to slow down the queue:
     ```python
     from prefect.concurrency.sync import rate_limit
     
     for item in items:
         rate_limit("yahoo_api", occupy=1)
         run_task(item)
     ```