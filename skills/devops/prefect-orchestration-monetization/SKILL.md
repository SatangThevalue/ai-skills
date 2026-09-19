---
name: prefect-orchestration-monetization
description: "Schedule and monitor the Zero-Touch Monetization pipeline using Prefect, with Infisical and A2A integration."
version: 0.2.0
metadata:
  hermes:
    tags: [Prefect, Orchestration, Scheduling, Monetization, A2A, Infisical]
    related_skills: [shopee-affiliate-data-pipeline, llm-prompt-orchestration, thai-faceless-video-automation, agent-frameworks-integration, infisical-secrets-management]
---

# Prefect Orchestration for Monetization (Zero-Touch + A2A + Infisical)

This skill defines the methodology for orchestrating individual Python scripts (Scraping, AI Generation, Video Assembly) and other AI agents (via A2A) into a robust, scheduled pipeline using Prefect. 

**CRITICAL SECURITY RULE:** All Prefect flows and tasks MUST retrieve their secrets at runtime using `infisical run` or the `infisical-python` SDK. Hardcoding or using `.env` files is strictly prohibited.

## When to Use
- Scheduling daily video creation or trading tasks.
- Coordinating complex multi-agent workflows (e.g., Prefect tells an A2A agent to research, then passes the result to a video assembly script).
- Handling retries and alerting on failure.

## Prerequisites
- Prefect Server running locally (`http://127.0.0.1:4200`).
- Infisical Vault running locally (`http://100.115.66.121:8080`) with a valid Machine Identity token.

## How to Run
Create a master `.py` file containing Prefect `@flow` and `@task` decorators. Execute it by wrapping the command in the Infisical CLI.
```bash
infisical run --env=prod --domain http://100.115.66.121:8080 -- python master_flow.py
```

## Quick Reference
- Local UI: `http://localhost:4200`
- Task decorator: `@task(retries=3, retry_delay_seconds=10)`
- Flow decorator: `@flow(name="Daily TikTok Affiliate Pipeline")`

## Procedure

### 1. Integrating Prefect with A2A (Agent-to-Agent)
Prefect can act as the "Master Scheduler", triggering A2A calls to other AI agents. Since A2A requests often require Bearer Tokens, these tokens MUST be fetched from Infisical.

```python
import os
import requests
from prefect import task, flow

@task(retries=2, retry_delay_seconds=5)
def delegate_to_research_agent(topic: str):
    # Retrieve the A2A Peer Token injected by Infisical CLI
    a2a_token = os.getenv("A2A_RESEARCHER_TOKEN")
    if not a2a_token:
        raise ValueError("Missing A2A token in environment. Was this run with infisical?")
        
    peer_url = "http://research-box.local:9900/api/v1/message"
    
    headers = {
        "Authorization": f"Bearer {a2a_token}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "message": f"Research trending products for {topic}",
        "contextId": "daily-research-01"
    }
    
    print(f"🤖 Sending A2A request to Research Agent...")
    res = requests.post(peer_url, json=payload, headers=headers)
    res.raise_for_status()
    
    # Return the agent's response to be used by the next Prefect task
    return res.json().get("reply")
```

### 2. Wrap Functions in Tasks
Convert existing python functions (like video assembly) into Prefect Tasks.
```python
@task
def create_video(script: str):
    # Calls logic from thai-faceless-video-automation
    # Any API keys needed (e.g., for external TTS) must be read via os.getenv()
    tts_api_key = os.getenv("API_TTS_SECRET")
    print("Video rendering...")
    return "/tmp/final_video.mp4"
```

### 3. Define the Flow Structure
Ensure data passes sequentially between tasks.
```python
@flow(name="Content Factory Pipeline via A2A", log_prints=True)
def run_daily_automation():
    # 1. Prefect asks an external AI agent to do research
    research_data = delegate_to_research_agent("smart watches")
    
    # 2. Assemble the video using the research
    video_path = create_video(research_data)
    
    print(f"✅ Pipeline complete! Output at {video_path}")

if __name__ == "__main__":
    # Local execution for testing
    run_daily_automation()
```

### 4. Deploying the Flow with Infisical (Scheduling)
When deploying a Prefect flow to run automatically, the background worker MUST also be wrapped in Infisical so it has access to secrets when it wakes up to run the job.

**Start the Prefect Worker:**
```bash
# The worker process itself is wrapped in Infisical
infisical run --env=prod --domain http://100.115.66.121:8080 -- prefect worker start -p my-pool
```

## Pitfalls
- **Missing Secrets in Background Jobs:** If you test the script manually with `infisical run` but your Prefect background worker was started *without* `infisical run`, the scheduled jobs will fail with `NoneType` errors when trying to read `os.getenv()`. Always wrap the worker process.
- **State Passing:** Tasks should return JSON-serializable data. Passing complex objects (like active database connections) between tasks will cause serialization errors.
- **A2A Timeouts:** A2A requests to other LLM agents can take 60-120 seconds. Ensure your `requests.post(..., timeout=120)` explicitly handles long wait times so Prefect doesn't incorrectly flag it as a network failure.

## Verification
Open the Prefect Dashboard (`http://127.0.0.1:4200`) and verify that the flow appears in the "Flow Runs" tab and executed successfully with a Green status.