---
name: prefect-zero-touch-blueprint
description: Enterprise architecture, strict coding standards, fallback rules, and Dockerized setup for the Zero-Touch Monetization suite using Prefect.
---
# Prefect Zero-Touch Development Blueprint

This skill defines the strict architectural rules, default fallbacks, and Dockerized infrastructure for the `zero-touch-prefect` monetization suite. It ensures scalable, resilient, and observable Python pipelines on a constrained VPS.

## 1. Environment & Architecture
- **Root Directory:** `/home/thaieasyvps/zero-touch-prefect`
- **Repository:** `SatangThevalue/zero-touch-prefect`
- **Package Manager:** `uv`
- **Docker Compose:** The project includes a `docker-compose.yml` to spin up the Prefect Server (SQLite backed) bound to port 4200.

### Required Environment Variables (`.env`)
```bash
PREFECT_API_URL="http://127.0.0.1:4200/api"
PREFECT_LOGGING_LEVEL="INFO" # Switch to DEBUG for troubleshooting
APP_ENV="production" # or "staging"
WORKSPACE_ROOT="/home/thaieasyvps/zero-touch-prefect"
TELEGRAM_BOT_TOKEN="your_token"
TELEGRAM_CHAT_ID="your_chat_id"
```

## 2. Strict Naming Conventions
- **File Naming:** `{SEQ_ID}-{category}-{task_name}.py`
  - *Example:* `001-media-tiktok-affiliate.py`, `002-line-clinic-agent.py`, `003-quant-settrade-dw.py`
- **Prefect Tags:** Mandatory on all `@flow` decorators for UI filtering.
  - *Pillars:* `"P1-Media"`, `"P2-LINE"`, `"P3-Quant"`, `"P4-DaaS"`
  - *Operations:* `"cron-daily"`, `"intraday"`, `"critical"`, `"webhook"`

## 3. Strict Coding Rules & Default Fallbacks (The Fail-Safe Guardrails)
Whenever generating or updating a pipeline, the following rules MUST be applied if the user does not specify otherwise:

1. **Retries (Network Guard):**
   - API/Web Scraping: `@task(retries=3, retry_delay_seconds=10)`
   - Trading (Settrade/Crypto): `@task(retries=5, retry_delay_seconds=2)`
2. **Timeouts (Anti-Zombie Guard):**
   - ALL flows must have a timeout. 
   - Media rendering: `@flow(timeout_seconds=3600)` (1 Hour)
   - Trading/General: `@flow(timeout_seconds=600)` (10 Minutes)
3. **Logging (Observability Guard):**
   - **NEVER use `print()`.**
   - Use `from prefect import get_run_logger`.
   - `logger = get_run_logger()` inside tasks.
   - Use `logger.info()` for milestones, `logger.error()` for exceptions.
4. **Error Alerting (Notification Guard):**
   - Critical failures (e.g., API auth failure, DB crash) must trigger a Telegram alert. Use a dedicated `send_telegram_alert(msg)` task in the `except` block of the main flow.
5. **Idempotency (Data Guard):**
   - Pipelines must be able to run twice without duplicating data or orders. Use `cache_key_fn` in Prefect or check DB existence before inserting.
6. **Concurrency/Rate Limits:**
   - Always respect 3rd-party API rate limits (e.g., LINE API). Use `asyncio.sleep()` or Prefect's concurrency limits when fanning out.

## 4. Dockerization & API Health Check
The project root must contain a `docker-compose.yml` to run the Prefect server locally, ensuring it restarts automatically if the VPS reboots.

### `docker-compose.yml` Standard
```yaml
version: "3.9"
services:
  prefect-server:
    image: prefecthq/prefect:2-python3.11
    command: prefect server start --host 0.0.0.0
    ports:
      - "4200:4200"
    restart: always
    volumes:
      - prefect-data:/root/.prefect
    environment:
      - PREFECT_API_URL=http://127.0.0.1:4200/api

volumes:
  prefect-data:
```

### Automated Health Check (Verification)
To verify if the infrastructure is healthy via Python, use this standard script:
```python
import requests
import os

def check_prefect_health():
    api_url = os.getenv("PREFECT_API_URL", "http://127.0.0.1:4200/api")
    health_endpoint = f"{api_url}/health"
    try:
        response = requests.get(health_endpoint, timeout=5)
        if response.status_code == 200:
            print("✅ Prefect Server is Healthy and Online.")
            return True
        else:
            print(f"❌ Prefect Server returned status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to connect to Prefect API: {e}")
        return False

if __name__ == "__main__":
    check_prefect_health()
```