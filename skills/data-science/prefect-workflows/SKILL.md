---
name: prefect-workflows
description: Design, monitor, and run data orchestrations with Prefect.
version: 0.1.0
metadata:
  hermes:
    tags:
      - Prefect
      - Orchestration
      - Python
      - MLOps
---

# Data Orchestration with Prefect

Build, run, and orchestrate Python data pipelines and workflow processes using the Prefect framework.

## When to Use
- When deploying data integration, extraction, or ML model training steps.
- When scheduling tasks and monitoring failures in workflow execution.
- When replacing cron jobs with dynamic, failure-tolerant pipelines.

## Prerequisites
- A Python environment managed by `uv`.
- Prefect package installed: `uv pip install prefect`.

## How to Run
- Run pipeline invocations and start Prefect worker pools using the `terminal` tool.

## Quick Reference
- Install: `uv pip install prefect`
- Run local server dashboard: `prefect server start`
- Execute flow: `python flow.py`

## Procedure

1. **Write a Prefect Flow**
   Define tasks and a main flow inside a Python script (e.g., `pipeline.py`):
   ```python
   from prefect import flow, task
   
   @task
   def extract_data():
       return [1, 2, 3]
   
   @task
   def process_data(data):
       return [x * 2 for x in data]
   
   @flow(name="My First Flow")
   def main_flow():
       data = extract_data()
       result = process_data(data)
       print(f"Processed: {result}")
   
   if __name__ == "__main__":
       main_flow()
   ```

2. **Execute the Flow**
   Run the script directly via uv virtual environment:
   ```bash
   python pipeline.py
   ```

3. **Start the Prefect Server for Monitoring**
   Launch the dashboard to monitor task states:
   ```bash
   prefect server start
   ```

## Pitfalls
- **Spelling Mismatch**: Ensure you use `prefect` (correct spelling) instead of "perfect" when calling CLI binaries or importing.
- **SQLite Database Locks**: Local Prefect server uses SQLite by default. Avoid writing heavily concurrent logs to prevent locks.

## Verification
Verify the Prefect CLI is active:
```bash
prefect version
```
