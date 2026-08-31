---
name: satang-ai-gateway-dev
description: "Development guide for the Satang AI Monorepo: FastAPI Gateway, Better-Auth integration, and Prefect orchestration."
---

# Satang AI Gateway Development

This skill governs the development of the Satang AI system, a monorepo containing:
- **apps/frontend**: Next.js 16+ using Better-Auth. Enforce a Feature-Sliced Design (Mini-app approach) under `src/features/<module>/` to keep functional domains decoupled without needing multiple Next.js apps/subdomains.
- **apps/backend-gateway**: FastAPI, SQLModel, ABAC (Casbin).
- **packages/shared-models**: SQLModel schemas shared between Next.js and FastAPI.
- **packages/prefect-flows**: Orchestration for heavy-duty AI/Trading tasks.

## Core Principles
1. **Shared Database**: FastAPI Gateway accesses the Better-Auth `user` and `session` tables directly.
2. **Frontend Architecture**: Use Feature-Sliced Design (Mini-app approach) in Next.js, isolating modules under `apps/frontend/src/features/<module-name>` to keep the Monorepo strictly decoupled.
3. **Payment Gateway**: Default to Beam Checkout for Thai payment gateway integrations. Handle webhooks in FastAPI to update subscriptions.
4. **Gateway Pattern**: Use FastAPI as an API Gateway for validation and audit logging before triggering Prefect flows.
5. **Async Everything**: FastAPI is async-only. All blocking/heavy code must be delegated to Prefect.
6. **LINE Integration**: Configure webhooks using `linebot.v3.messaging` and return `{"status": "ok"}` on successful parsing. Send a loading animation (`show_loading_animation`) immediately upon receiving a message, before doing any heavy AI processing, to prevent user frustration. Use Flex Messages (`FlexMessage`, `FlexContainer`) for rich responses like receipts. Handle non-financial chatter gracefully by ignoring it and not writing garbage to the DB.
7. **AI Routing & Parsing**: Avoid complex LangChain `PromptTemplate` features when possible. Rely on direct API calls using hardcoded strings to local models via the CLI proxy (e.g. `http://localhost:42869/v1/chat/completions`) for maximum stability. When enforcing predefined categories, pass the allowed list within the prompt string and implement a safe fallback in code.
8. **LINE Messaging API Blob**: Use `MessagingApiBlob.get_message_content(message_id)` to retrieve image bytes from LINE. Encode these bytes to base64 before passing them to the AI vision model payload.
9. **Telemetry**: Log AI inference latency, token usage, and estimated cost to the database to support business analytics and monitoring.
6. **Audit Logging**: Every API request must be recorded in `audit_logs`.
7. **ABAC/RBAC Integration**: เมื่อต้องการควบคุมสิทธิ์การเข้าถึงทรัพยากร ให้ใช้ Casbin ควบคู่กับฐานข้อมูล เพื่อความยืดหยุ่นและการจัดการที่ปรับเปลี่ยนผ่านหน้าเว็บได้โดยไม่ต้องแก้ไขโค้ด
8. **Webhook Dispatching**: ใช้ Dispatcher Pattern แยกตาม Platform (LINE, Settrade) และทำ Signature Validation ในระดับ Middleware/Processor ก่อนประมวลผล
9. **LINE Webhook UX**: สำหรับ LINE Webhook ที่ต้องใช้ AI ให้ใช้ `showLoadingAnimation` หน่วงเวลากลับไปก่อน (เช่น 30 วิ) และส่ง HTTP 200 OK ทันที เพื่อไม่ให้ Timeout จากนั้นโยนงานเข้า Background Task แล้วค่อยส่งผลลัพธ์ด้วย Flex Message
10. **Local LLM via CLI Proxy**: See `templates/langchain-cli-proxy.py` for connecting LangChain to the local Hermes CLI proxy API.

See `references/satangthebank_schema.md` for a concrete MVP ledger schema implementation.

**Architecture Patterns**: See `references/saas_architecture_patterns.md` for standard multi-tenant Next.js URL structures, CORS/Env setup, and quota-based modular database design.
See `references/docker_compose_production.md` for pitfalls and workarounds when containerizing the stack.

## Setup
### Local Development
1. Install UV: `curl -LsSf https://astral.sh/uv/install.sh | sh`
2. Configure pnpm workspace:
   ```yaml
   packages:
     - 'apps/*'
     - 'packages/*'
   ```
3. Initialize the backend with UV: `cd apps/backend && uv venv && source .venv/bin/activate && uv pip install fastapi uvicorn sqlmodel asyncpg`
4. Initialize the frontend with Next.js/Tailwind/Better-Auth using pnpm in `apps/frontend`.
5. Set environment: `DATABASE_URL` for PostgreSQL.

## Pitfalls
- **ModuleNotFoundError**: Always ensure PYTHONPATH includes the Monorepo root. Use `PYTHONPATH=$PYTHONPATH:$(pwd)`. Ensure all subdirectories have `__init__.py`.
- **Database Port Conflicts**: When developing locally, ensure the PostgreSQL port (e.g., 5432) doesn't conflict with other running Traefik/Postgres instances. If 5432 is in use, remap the compose port to 5433 (e.g. `5433:5432`) and update the `DATABASE_URL` accordingly.
- **Traefik and Native Host Routing**: If moving a containerized service (like FastAPI) to run natively on the host for debugging, Traefik will return `502 Bad Gateway` if the rule still points to the container name. Update Traefik's dynamic `loadBalancer.servers.url` to the host gateway IP (e.g., `10.0.0.1:8000` or `10.0.2.1:8000`).
- **Sync/Async Mixed**: Never run sync code in FastAPI async endpoints. Use `run_in_threadpool` (or `await asyncio.to_thread()`) for light tasks, and Prefect for heavy tasks.
- **LangChain Blocking Event Loop**: Synchronous AI calls (like `chain.invoke()`) block the FastAPI worker thread, causing severe latency. Always wrap them in `await asyncio.to_thread(chain.invoke, inputs)` to maintain throughput.
- **Better-Auth Integration**: FastAPI reads `session` tokens from the same DB as Next.js; treat these tables as Read-only from the FastAPI side. Ensure SQLModel definitions match the Better-Auth schema exactly (User, Session). Next.js Route handler in Better-Auth v1.6.23+ requires using `toNextJsHandler` from `better-auth/next-js` with `auth.handler`, not `toNextRouteHandler` from `better-auth/next`.
- **Audit Logging**: Every API request must be logged by a Middleware to the `audit_logs` table.
- **Webhook Pattern**: Webhooks must be processed via a Dispatcher -> Prefect Flow to ensure latency requirements (e.g., 2s for LINE) are met. Example: LINE webhook -> FastAPI validates signature -> Fast response -> Prefect handles OCR/NLP.
- **ABAC/RBAC**: Implement authorization checks (e.g., `check_owner`) inside FastAPI dependencies to enforce resource-level access policies fetched from the DB at runtime.
- **LangChain Prompt Template JSON Formatting**: When specifying a JSON schema or dict structure inside a LangChain prompt template, curly braces `{` and `}` are treated as template inputs by default. Ensure all literal curly braces are escaped by doubling them (e.g., `{{` and `}}`), otherwise LangChain will raise an `InvalidPromptInput` error stating variables are missing.
- **Docker vs Host Database Networking**: In Docker Compose environments, referencing database hosts using internal service names (like `satangthebank-db`) works within the Docker network, but fails when running backend processes natively on the host (Native/Host mode). Ensure configuration supports dynamic host resolution or falls back to `localhost`/`127.0.0.1` when resolving database connections outside Docker networking.
- **Host Native vs Docker Deployments**: Docker compose for the full stack (web, api, db) often faces memory starvation on small VMs resulting in crashes or 502 Bad Gateway via Traefik. For more stable deployments, consider a Host Native approach: run PostgreSQL in Docker, but run Next.js and FastAPI natively using PM2/nohup, relying on Traefik for port forwarding. When deploying full stack via Docker Compose, be aware of `pnpm install` failing with `ERR_PNPM_ABORTED_REMOVE_MODULES_DIR_NO_TTY` in the Next.js `Dockerfile`. Fix this by setting `ENV CI=true` and `RUN pnpm config set confirmModulesPurge false` before installation. Also, Next.js Dockerfiles in a Monorepo must copy the `node_modules` from the root workspace, not just the app-level `node_modules`, to avoid `MODULE_NOT_FOUND` errors.
