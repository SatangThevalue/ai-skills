---
name: langgraph-development
description: Best practices for building and tracing AI agents with LangGraph, Deep Agents, and MLflow.
---

# LangChain Ecosystem & AI Gateway Development

This skill provides comprehensive patterns for building, orchestrating, and tracking AI agents using the modern LangChain ecosystem (LangChain, LangGraph, Langflow, Deep Agents) alongside MLflow for tracing and AI Gateway management.

## 🏗️ Environment Setup (Latest Official ecosystem)
Prefer using `uv` for fast virtual environment creation:
```bash
uv venv
source .venv/bin/activate
# Install core ecosystem (latest stable versions)
uv pip install langchain langchain-core langchain-openai
uv pip install langgraph langgraph-checkpoint langgraph-checkpoint-postgres langgraph-sdk
uv pip install langflow
uv pip install mlflow
```

## 1. LangChain & LangGraph (Stateful Agents)
LangGraph is the official framework for building stateful, multi-actor applications (Agents).
- **Nodes & Edges:** Define `StateGraph(State)`. Nodes are Python functions taking `State` and returning state updates. Edges define the flow (conditional routing).
- **Checkpointers (Memory):** For persistent memory (Human-in-the-Loop, time-travel), you MUST use a checkpointer like `MemorySaver` (testing) or `AsyncPostgresSaver` (production).
- **Async Execution:** For production (FastAPI/Web), ALWAYS use `.ainvoke()`, `.astream()`, `.aget_state()` to prevent blocking threads.

**Human-in-the-Loop (HITL) Pattern:**
```python
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from psycopg_pool import AsyncConnectionPool

# In FastAPI Lifespan or async init:
pool = AsyncConnectionPool(conninfo=DB_URL, max_size=20)
await pool.open()
checkpointer = AsyncPostgresSaver(pool)
await checkpointer.setup()

# Compile with interrupt
graph = builder.compile(checkpointer=checkpointer, interrupt_before=["human_approval_node"])

# Resume after approval
await graph.aupdate_state(config, {"approval_status": "approved"})
await graph.ainvoke(None, config=config)
```

## 2. MLflow & AI Gateway (Tracing & Management)
MLflow provides two core functionalities for LangChain:
1. **Tracing (Autologging):** Logs agent thoughts, tool calls, and token usage automatically.
   - Run: `mlflow ui --host 0.0.0.0 --port 5000`
   - Code: `import mlflow; mlflow.langchain.autolog()` BEFORE graph compilation.
2. **AI Gateway (MLflow Deployments / Gateway):** A unified proxy to manage credentials, rate limits, and routing across multiple LLM providers (OpenAI, Anthropic, local models).
   - Set `MLFLOW_GATEWAY_URI` in the environment.
   - Access models securely without hardcoding API keys in the app.

## 3. Token Tracking
To track cost and tokens across LangGraph nodes, use `get_openai_callback`:
```python
from langchain_community.callbacks.manager import get_openai_callback

async def llm_node(state):
    with get_openai_callback() as cb:
        response = await llm.ainvoke(prompt)
        # cb.total_tokens, cb.total_cost available here for DB logging
```

## 4. Langflow (Visual Builder)
Langflow is a UI for LangChain/LangGraph.
- Start server: `langflow run --host 0.0.0.0 --port 7860` (Always use `terminal(background=true)` for this).
- It generates Python code or provides an API endpoint to integrate the visual flow into your backend.

## 5. Deep Agents Framework
`deepagents` is LangChain's opinionated harness built on top of LangGraph.
- **Quickstart:** Use `from deepagents import create_deep_agent` to instantiate an agent with built-in planning and delegation.
- Any custom LangGraph `CompiledStateGraph` can be passed as a tool/sub-agent into a Deep Agent.

## ⚠️ Pitfalls & Constraints
- **Docker Dependency Conflicts:** Be cautious with exact version pins (e.g., `==`) in `requirements.txt` when mixing FastAPI, Starlette, and Prefect. Prefer `>=` to allow `pip` to resolve dependency conflicts automatically.
- **FastAPI Thread Blocking:** Never run synchronous LangGraph `invoke()` calls directly in a FastAPI endpoint handler without pushing them to a background task or using `ainvoke()`, as this will block the server under load. Always use `.ainvoke()` and push generation work to a background task (e.g. `fastapi.BackgroundTasks` or Prefect/Celery) so the API can respond `202 Accepted` immediately.
- **Prefect Orchestration Integration**: When placing Prefect behind a proxy or inside a Docker compose network, make sure to configure `PREFECT_API_URL` properly so that internal services can resolve it. For Docker Compose with Prefect 2.x, use `--host 0.0.0.0` when starting the server to avoid network binding issues (`prefect server start --host 0.0.0.0`). Avoid using `AsyncConnectionPool` warnings during initialization by awaiting `pool.open()` instead of letting it lazily open. Note that Prefect 2.16+ requires SQLite by default, so omitting `PREFECT_API_DATABASE_CONNECTION_URL` simplifies initial Docker Compose setup. See the `prefect-orchestration` skill for more details.
- **Prefect Worker Circular Imports:** When wrapping LangGraph invocations in Prefect `@task`s, do not import the compiled `content_graph` directly at the module level if the graph depends on the same database models or tasks. This causes a circular import error on startup. Pass the graph instance or run the invocation indirectly from FastAPI.
- **Traefik Network Connectivity:** When exposing services via Traefik labels in `docker-compose.yml`, explicitly set the network to the name of the external Traefik network (e.g., `traefik-public`) rather than just `web`. Ensure `external: true` is set for that network block, and that entrypoints (`traefik-publicsecure`) and certresolvers match the Traefik host configuration.
- **Docker Compose Dependencies:** Ensure `depends_on` lists required services, and for internal communication, use `extra_hosts` with `host.docker.internal:host-gateway` to allow containers to reach host ports (e.g., `cli-proxy-api`).
- **Next.js Docker Port Collisions:** Next.js uses port 3000 by default. If this port is already allocated on the host, explicitly map it to an alternate port in `docker-compose.yml` (e.g., `3001:3000`) and ensure any `.env` files point to the correct port.
- **PostgreSQL Port Collisions:** If `5432` is already in use on the host, map the Docker container to an alternate port like `5433:5432` in `docker-compose.yml`.
- **Long-running Services:** When starting UI servers like `langflow run`, `mlflow ui`, or FastAPI `uvicorn`, ALWAYS use the terminal tool with `background=true` and `notify_on_complete=true`. Running them in the foreground will hang the terminal tool and result in a timeout error.
- **Host Binding on VPS:** When exposing UIs (MLflow, Langflow) on a remote VPS, explicitly bind to `0.0.0.0` (e.g., `--host 0.0.0.0`) so they are accessible externally, rather than defaulting to localhost.