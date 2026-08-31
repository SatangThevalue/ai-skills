---
name: satang-ai-gateway
description: "Satang AI: Integration patterns for FastAPI Gateway, Better-Auth, and Prefect."
---

# Satang AI Integration: Workflow and Pitfalls

## 1. Monorepo Integration Strategy
- **Root Directory Strategy:** Always run Python modules from the project root (`satang-ai-monorepo`) with `export PYTHONPATH=.`.
- **Import convention:** Use absolute imports from root, e.g., `from apps.backend_gateway.core.database import engine`.
- **Deployment:** Use `docker-compose` at the root, mapping paths via volume mounts in `docker-compose.yml`.

## 2. Authentication Flow (Better-Auth + FastAPI)
- **Shared DB:** Both Next.js (Better-Auth) and FastAPI point to the same PostgreSQL DB.
- **Session Verification:** FastAPI reads the `session` table directly for stateless validation.
- **Pitfall:** Ensure `DATABASE_URL` uses `asyncpg` for FastAPI's async compatibility.

## 3. Webhook Hub
- **Pattern:** Use a Dispatcher pattern in `webhooks/router.py`.
- **Security:** Verify signatures in `processors/<platform>.py` before executing any logic.
- **Async Execution:** Always offload processing to Prefect flows via `run_deployment` to prevent Gateway timeouts.

## 4. Troubleshooting
- **ModuleNotFoundError:** Ensure `__init__.py` exists in every subfolder of `apps/` and `packages/`.
- **DB Connection:** If connection fails, check `pg_isready` and ensure `POSTGRES_DB` name matches in `.env`.
