---
name: ai-content-studio-architecture
description: Architecture and workflows for the Satang AI Studio multi-agent content generation platform.
version: 1.0.0
metadata:
  hermes:
    tags:
      - Next.js
      - FastAPI
      - LangGraph
      - Prefect
      - Multi-Agent
---

# Satang AI Studio Architecture

This skill documents the architecture, data models, and operational patterns for Satang AI Studio—an enterprise-grade, multi-tenant AI content automation platform with Human-in-the-Loop (HITL) capabilities.

## Tech Stack Overview

- **Frontend:** Next.js 16+ (App Router)
- **Backend:** FastAPI (Python 3.11+, Async)
- **Database:** PostgreSQL (with `asyncpg` and `psycopg-pool`)
- **AI Core:** LangGraph (Stateful workflow), LangChain, Local LLMs (via `cli-proxy-api`)
- **Orchestration:** Prefect 2.x (Background workers, Scheduling)
- **Infrastructure:** Docker Compose, Traefik (Reverse Proxy)

## Core Workflow (End-to-End)

The system operates through four distinct phases, coordinated between FastAPI, LangGraph, and Prefect:

1. **Phase 1: Input & Configuration (Drafting)**
   - The user creates a campaign (`/api/v1/campaigns`).
   - FastAPI creates a `CampaignJob` record in PostgreSQL (`status=DRAFTING`).
   - FastAPI spawns a background task (or Prefect flow) to trigger LangGraph.
   - LangGraph executes the `researcher` and `writer` nodes asynchronously.
   - The graph is configured with `interrupt_before=["human_approval"]`. Execution suspends here.
   - The graph state is persisted to PostgreSQL via `AsyncPostgresSaver`.
   - The job status updates to `WAITING_APPROVAL`.

2. **Phase 2: Human-in-the-Loop (HITL)**
   - The user views the generated draft and image prompts in the Next.js UI.
   - If **Rejected**: The user provides feedback. The job status reverts to `DRAFTING`, and the LangGraph state is updated. The graph is re-invoked, looping back to the `writer` node to apply the feedback.
   - If **Approved**: The user approves the draft (optionally setting a `scheduled_at` time). The job status advances to `FORMATTING`.

3. **Phase 3: Multi-Platform Formatting**
   - Upon approval, the background task resumes the LangGraph execution.
   - The `formatter` node generates platform-specific content (e.g., Facebook, Twitter) concurrently.
   - Once formatting completes, the job status updates to `SCHEDULED` (if a time was set) or `PUBLISHED`.

4. **Phase 4: Auto-Publishing (Orchestration)**
   - A dedicated Python worker (or Prefect task) continuously polls the database for jobs where `status=SCHEDULED` and `scheduled_at <= NOW()`.
   - The worker executes the publishing logic (e.g., calling social media APIs).
   - Upon success, the job status is marked as `PUBLISHED`.

## Database Schema Highlights

The system uses SQLAlchemy (Async) with the following core models:

- **`ClientProfile`:** Supports multi-tenancy. Stores `enable_researcher`, `require_human_approval` (allows bypassing HITL for auto-pilot clients), `brand_voice`, and `custom_prompts`.
- **`CampaignJob`:** Tracks the lifecycle of a content request. Includes `topic`, `persona_id`, `target_platforms`, `status` (Enum), `image_prompt`, and `scheduled_at`.
- **`UsageLog`:** Tracks token consumption (cost analytics). Integrated with `get_openai_callback()` in LangGraph nodes to capture `input_tokens` and `output_tokens` per step.

## Key Implementation Patterns & Pitfalls

### 1. LangGraph Async Postgres Checkpointer
When using `AsyncPostgresSaver` within a FastAPI application, it must be initialized and attached to the graph during the application's lifespan to ensure the async event loop is active.

```python
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from psycopg_pool import AsyncConnectionPool

@asynccontextmanager
async def lifespan(app: FastAPI):
    pool = AsyncConnectionPool(conninfo=DB_URL, max_size=20, kwargs={"autocommit": True, "prepare_threshold": 0})
    await pool.open() # IMPORTANT: Await pool.open() to avoid RuntimeWarnings about lazy initialization
    checkpointer = AsyncPostgresSaver(pool)
    await checkpointer.setup() # Creates the required checkpoint tables
    
    global content_graph
    content_graph = uncompiled_graph.compile(
        checkpointer=checkpointer,
        interrupt_before=["human_approval"]
    )
    yield
    await pool.close()
```

### 2. Prefect Integration within FastAPI
- **Circular Imports:** When integrating Prefect tasks with FastAPI and LangGraph, avoid importing the compiled `content_graph` directly into the Prefect worker module if the graph module also imports database models. This leads to circular dependency errors during Uvicorn startup. Instead, inject the graph instance or handle the invocation logic carefully to break the cycle.
- **Background Tasks vs. Prefect:** For rapid dev/MVP stages, `fastapi.BackgroundTasks` is sufficient to prevent thread-blocking during LLM calls (`.ainvoke()`). However, for production resilience and scheduled publishing, these tasks should be migrated to Prefect Flows/Tasks.

### 3. Docker Compose & Dependency Conflicts
- When building Python images for FastAPI + Prefect + LangChain, avoid strict version pinning (`==`) in `requirements.txt` unless absolutely necessary. Conflicts frequently arise between `starlette` versions required by `fastapi` and `prefect`. Use `>=` to allow `pip` to resolve the dependency graph.
- **Memory/Disk Management:** Complex pip installations (especially involving `psycopg-binary`, `grpcio`, etc.) can quickly consume significant disk space within the Docker overlay filesystem. If you encounter `no space left on device` during `docker compose build`, prune the builder and volumes (`docker builder prune -f`, `docker system prune -af --volumes`) before retrying.

### 4. Traefik Routing
When mapping a domain (e.g., `sais.satangthevalue.app`) to the Next.js and FastAPI containers:
- Ensure the `docker-compose.yml` networks block explicitly references the *actual* external Traefik network name (e.g., `traefik-public`), not a generic name like `web`.
- The `traefik.http.routers.<name>.entrypoints` and `traefik.http.routers.<name>.tls.certresolver` labels MUST match the configuration of the host Traefik instance (e.g., `traefik-publicsecure` and `leresolver`).
- Set `NEXT_PUBLIC_API_URL` to the public HTTPS domain so client-side React components avoid CORS issues.

### 5. Multi-Modal Generation
The `writer` node can be adapted to generate image generation prompts concurrently with the text draft. Pass the text draft through an LLM configured as a "Creative Director" to output a Midjourney-style prompt, and store this in the `CampaignJob.image_prompt` database column for the UI to display.

### 6. Video Automation Integration
To support Video Automation (Reels/Shorts/TikTok) in the Studio pipeline:
- The system must integrate a dedicated `Video Editing API` (e.g. FastAPI + MoviePy) that handles vertical 9:16 rendering.
- N8N automation or Prefect flows should pass `video_local_path` or `video_file` inputs directly to avoid `UploadFile` latency or `n8n timeout errors` during lengthy background rendering.
- Ensure the FastAPI server is configured with proper CPU lock (`asyncio.Lock()`) for heavy rendering tasks (`cpu_render_lock`), and GPU lock (`gpu_lock`) for TTS components to prevent Out-Of-Memory (OOM) errors.
- Include Advanced Audio Post-Processing (Pedalboard) for the AI voiceover to achieve studio quality before overlaying onto the video.