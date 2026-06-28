---
name: satang-project-suite
description: Develop and deploy Thanapol's custom AI and trading projects.
version: 0.1.0
metadata:
  hermes:
    tags:
      - Next.js
      - FastAPI
      - Trading
      - Computer-Vision
      - Voice-Cloning
---

# Thanapol's Project Suite Development Guide

This guide provides procedures for developing, deploying, and maintaining the portfolio projects of Thanapol Nanthakaset (Satang), covering soundbridgehub, automated trading systems, YOLO flower detection, and voice cloning.

## When to Use
- When writing code or configuring infrastructure for the `soundbridgehub` MP3 e-commerce platform.
- When developing automated trading bots for Forex (XAUUSD), Crypto (BTC), or Stocks using SETTRADE API.
- When implementing YOLO models for flower detection or configuring Voice Cloning/TTS services.

## Prerequisites
- Next.js project layout with `better-auth` and a PostgreSQL database setup.
- Python environment managed via `uv` with `fastapi`, `ultralytics` (YOLO), and `prefect` installed.
- SETTRADE API credentials and MetaTrader 5 (MQL5) environment access.

## How to Run
- Execute testing, compilation, and deployment commands using the `terminal` tool.
- Apply database migrations and code changes using `patch` or `write_file` tools.

## Quick Reference
- Run next.js dev: `pnpm dev`
- Run FastAPI server: `uvicorn main:app --reload`
- Trigger Prefect workflow: `prefect flow-run execute`

## Procedure

### 1. Soundbridgehub Development (Next.js + better-auth + PostgreSQL)
1. Initialize/navigate to the Next.js e-commerce repository.
2. Verify the PostgreSQL connection and run Better-Auth migration:
   ```bash
   pnpx better-auth generate
   ```
3. Set up the local environment variables for JWT and authentication in `.env.local`:
   ```env
   BETTER_AUTH_SECRET=your_jwt_secret_here
   BETTER_AUTH_URL=http://localhost:3000
   DATABASE_URL=postgresql://user:pass@localhost:5432/soundbridgehub
   ```

### 2. Automated Trading Systems (SETTRADE + Python + MQL5)
1. Set up a secure Python environment using `uv` to handle market execution scripts.
2. Integrate SETTRADE API for Thai stocks or MQL5 script loops for XAUUSD/BTC.
3. Schedule ingestion and execution pipelines using Prefect:
   ```python
   # pipeline.py
   from prefect import flow
   @flow
   def execute_trading_strategy():
       # Fetch data & place order logic
       pass
   ```

### 3. YOLO Flower Detection & CV (FastAPI + YOLO)
1. Install OpenCV and Ultralytics under `uv`:
   ```bash
   uv pip install ultralytics opencv-python fastapi uvicorn
   ```
2. Build a FastAPI endpoint to receive image uploads and run inference:
   ```python
   # main.py
   from fastapi import FastAPI, UploadFile
   from ultralytics import YOLO
   app = FastAPI()
   model = YOLO("yolov8n.pt") # Edible flower model
   @app.post("/predict")
   async def predict(file: UploadFile):
       # Run inference and return classes
       pass
   ```

## Pitfalls
- **MQL5 execution**: MQL5 requires a Windows/Wine environment to run MetaEditor/Terminal. Ensure scripts bridge data correctly via socket/REST to the Python controller if running on Linux.
- **Better-Auth Cookie domain**: Ensure `BETTER_AUTH_URL` matches host headers to avoid session dropouts.

## Verification
Verify database connectivity and check the API server status:
```bash
curl -I http://localhost:8000/health
```
