---
name: ai-telemetry-and-billing
description: "Implement database telemetry to track LLM token usage, latency, and estimated costs."
version: 0.1.0
metadata:
  hermes:
    tags:
      - Analytics
      - Telemetry
      - Database
      - Cost Optimization
---

# AI Telemetry and Billing Analytics

This skill provides a pattern for capturing AI model usage metrics (tokens, latency, cost) alongside standard application data. It is crucial for estimating production costs (e.g. Gemini, OpenAI APIs), identifying bottlenecks (latency tracking), and understanding user behavior across multimodal requests (text vs image).

## When to Use
- When the user asks to log, track, or analyze LLM token usage and costs.
- When transitioning an AI app to production and needing visibility into API expenses per user.
- When optimizing prompts and needing hard data on `prompt_tokens` vs `completion_tokens`.

## Prerequisites
- A PostgreSQL (or similar SQL) database.
- An application executing API requests to an LLM endpoint that returns standard `usage` blocks (e.g. OpenAI format).

## Quick Reference
- Standard cost formula (e.g. Gemini 1.5 Flash): `(prompt_tokens / 1M * 0.075) + (completion_tokens / 1M * 0.30)`

## Procedure

1. **Create the Telemetry Schema:**
   Add a tracking table to your database.
   ```sql
   CREATE TABLE IF NOT EXISTS ai_usage_log (
       id SERIAL PRIMARY KEY,
       user_identifier TEXT, -- e.g., line_user_id
       model_name TEXT NOT NULL,
       prompt_tokens INTEGER DEFAULT 0,
       completion_tokens INTEGER DEFAULT 0,
       total_tokens INTEGER DEFAULT 0,
       latency_ms INTEGER DEFAULT 0,
       cost_estimated DOUBLE PRECISION DEFAULT 0.0,
       request_type TEXT NOT NULL, -- e.g., 'text' or 'image'
       status TEXT DEFAULT 'success',
       created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT (NOW() AT TIME ZONE 'utc')
   );
   ```

2. **Intercept Metrics at the API Call Level:**
   Wrap the LLM request to track latency and extract the `usage` block.
   ```python
   import time
   
   start_time = time.time()
   response = requests.post(url, json=payload)
   latency_ms = int((time.time() - start_time) * 1000)
   
   resp_json = response.json()
   usage = resp_json.get("usage", {})
   
   # Attach telemetry metadata to your returned result
   telemetry = {
       "model": resp_json.get("model", "unknown-model"),
       "prompt_tokens": usage.get("prompt_tokens", 0),
       "completion_tokens": usage.get("completion_tokens", 0),
       "total_tokens": usage.get("total_tokens", 0),
       "latency_ms": latency_ms,
       "request_type": "text" # or "image"
   }
   ```

3. **Calculate Cost and Persist:**
   Where the main application processes the AI result, calculate the cost based on the active model's pricing and save the log entry.
   ```python
   cost_est = (telemetry["prompt_tokens"] / 1_000_000 * 0.075) + (telemetry["completion_tokens"] / 1_000_000 * 0.30)
   
   log_entry = AiUsageLog(
       line_user_id=user_id,
       model_name=telemetry["model"],
       prompt_tokens=telemetry["prompt_tokens"],
       completion_tokens=telemetry["completion_tokens"],
       total_tokens=telemetry["total_tokens"],
       latency_ms=telemetry["latency_ms"],
       cost_estimated=cost_est,
       request_type=telemetry["request_type"],
       status="success"
   )
   session.add(log_entry)
   session.commit()
   ```

## Verification
Run a simple aggregation query to confirm data is logging correctly:
```bash
invoke terminal: docker exec db_container psql -U user -d db -c "SELECT SUM(cost_estimated) AS total_ai_cost_usd, SUM(total_tokens) AS token_used FROM ai_usage_log;"
```

## Scheduled Quota Warnings and Expiration (Cron Integration)

When running production AI platforms, a background cron job should check billing usage and warn users (e.g. at 80% usage) or manage membership downgrades when active periods expire.

### 1. Warning and Expiration Checker Script Pattern
Write a scheduled script (e.g. `cron_quota_warning.py`) to query database tables for active subscriptions and aggregate usage logs:

```python
import asyncio
from datetime import datetime
from sqlmodel import Session, select, func
# Import your engine, UserSubscription, LineAccount/AppUser, and AiUsageLog models

async def check_and_warn_quotas():
    now = datetime.utcnow()
    start_of_month = datetime(now.year, now.month, 1)
    
    with Session(engine) as session:
        # Fetch active subscriptions
        subscriptions = session.exec(
            select(UserSubscription).where(
                (UserSubscription.expires_at == None) | (UserSubscription.expires_at > now)
            )
        ).all()
        
        for sub in subscriptions:
            # 1. Check monthly request/token quotas
            plan = sub.plan_tier or "free"
            max_requests = 50 if plan == "free" else 500  # Example limits
            
            usage_stmt = select(
                func.count(AiUsageLog.id), 
                func.sum(AiUsageLog.total_tokens)
            ).where(
                AiUsageLog.line_user_id == sub.line_user_id,
                AiUsageLog.created_at >= start_of_month,
                AiUsageLog.status == "success"
            )
            usage_res = session.exec(usage_stmt).first()
            requests_used = usage_res[0] if usage_res and usage_res[0] else 0
            
            # Send warning if usage is >= 80% and we haven't hit 100%
            if max_requests and (requests_used >= max_requests * 0.8) and (requests_used < max_requests):
                percent = int((requests_used / max_requests) * 100)
                send_push_notification(sub.line_user_id, f"⚠️ You have used {percent}% of your monthly AI quota.")
                
            # 2. Check Expiration Warning (e.g., 3 days before expiration)
            if sub.expires_at:
                days_left = (sub.expires_at - now).days
                if days_left == 3:
                    send_push_notification(sub.line_user_id, f"⏳ Your package expires in 3 days. Please renew.")

if __name__ == "__main__":
    asyncio.run(check_and_warn_quotas())
```

### 2. Execution in Containerized Environments
If your API runs inside a Docker container (e.g. `satangthebank-api`), copy the script inside the container (or use volume mounts) and trigger it via host-level crontab/Hermes scheduler using `docker exec`:

```bash
# Update/Register the Hermes cron job command
hermes cron edit <job_id> --workdir "/absolute/path/to/project-root" --prompt "docker exec -i satangthebank-api python3 /app/src/cron_quota_warning.py"
```

This prevents path mismatches between host execution and the isolated database/API network environment.