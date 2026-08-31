---
name: prefect-monetization-orchestration
description: Blueprint for replacing n8n and simple cronjobs with Prefect 2.x/3.x for enterprise-grade, code-based orchestration of Thai monetization pipelines.
---
# Prefect Orchestration for Monetization Pipelines

While `n8n` is great for rapid API stitching and `cronjob` is simple for time-based triggers, they struggle with complex state management, retries, conditional branching, and distributed execution. For robust, Python-native "Zero-Touch" monetization pipelines (Media, Trading, Scraping), **Prefect** is the enterprise-grade choice.

## 1. Why Prefect over n8n & Cron?
- **100% Python Native:** No visual spaghetti code. You write standard Python, decorate it with `@task` and `@flow`, and Prefect handles the rest.
- **State Management & Retries:** If a trading API times out, Prefect automatically retries with exponential backoff.
- **Concurrency & Scaling:** Prefect can fan-out (run 10 video renderings concurrently) and fan-in (wait for all to finish before uploading).
- **Observability:** Provides a beautiful dashboard to monitor pipeline health, logs, and execution history without manually tailing VPS logs.

## 2. Prefect Architecture for the 4 Pillars

### A. Pillar 1: Automated "Faceless" Media
Replacing n8n webhook/scheduler with a Prefect Flow.
```python
from prefect import flow, task
import asyncio

@task(retries=3, retry_delay_seconds=60)
def generate_script(topic: str):
    # LLM logic here
    return script_text

@task
def generate_tts_and_subtitles(script_text: str):
    # TTS & Faster-Whisper logic
    return audio_file, ass_file

@task
def render_video_ffmpeg(audio_file, ass_file, background_video):
    # Raw FFmpeg subprocess call
    return output_video

@task
def upload_to_youtube(video_path):
    # API upload logic
    pass

@flow(name="Faceless Video Pipeline")
def media_pipeline(topic: str = "เรื่องลี้ลับในไทย"):
    script = generate_script(topic)
    audio, subs = generate_tts_and_subtitles(script)
    video = render_video_ffmpeg(audio, subs, "bg.mp4")
    upload_to_youtube(video)

# To schedule:
# media_pipeline.serve(name="daily_video", cron="0 18 * * *")
```

### B. Pillar 3: Quant Trading (Replacing Cron)
Standard `cron` fails silently. If the Settrade API rejects a login, cron dies and you don't know until you check the logs. Prefect provides alerts and retries.
```python
from prefect import flow, task
from datetime import timedelta

@task(retries=5, retry_delay_seconds=5) # Handle network hiccups
def fetch_market_data():
    pass

@task
def compute_signals(data):
    pass

@task
def execute_trade(signals):
    pass

@flow(name="Settrade DW Algo", timeout_seconds=600)
def quant_trading_flow():
    data = fetch_market_data()
    signals = compute_signals(data)
    if signals.has_trade():
        execute_trade(signals)

# Run every 5 minutes during market hours
# quant_trading_flow.serve(name="intraday_bot", cron="*/5 10-16 * * 1-5")
```

### C. Pillar 4: DaaS (Web Scraping)
Prefect's **Mapping (Fan-out)** feature is perfect for scraping multiple pages concurrently.
```python
from prefect import flow, task

@task
def get_target_urls(category):
    return ["url1", "url2", "url3", "url4", "url5"] # Returns list of 100+ URLs

@task
def scrape_page(url):
    # Playwright logic here
    return extracted_data

@task
def save_to_db(all_data):
    # Pydantic validation & Postgres insert
    pass

@flow(name="Real Estate Scraper")
def scraping_flow():
    urls = get_target_urls("condos")
    
    # .map() runs the task concurrently for every item in the list!
    scraped_data_list = scrape_page.map(urls) 
    
    save_to_db(scraped_data_list)
```

## 3. VPS Deployment Strategy (Zero-Touch)
To run this on a tight VPS (like the SatangTheBank server):
1. **Local Server:** Run Prefect Server locally via Docker Compose (SQLite backend is default and uses minimal RAM). `prefect server start --host 0.0.0.0`
2. **Workers/Pools:** Start a local Prefect Worker `prefect worker start --pool "default-agent-pool"`.
3. **Deployments:** Use `prefect deploy` to register the code with the local server. The worker will pick up the scheduled runs and execute them.

## 4. Agent Instructions & Constraints
- **Avoid Global State:** Prefect tasks run concurrently or in isolated processes. Do not rely on global variables (`bot_state = {}`) to pass data between tasks. Always return data from one task and pass it as an argument to the next.
- **Async Playwright:** When using Playwright inside Prefect, ensure you are using the `async` version of Playwright and `async def` for tasks, or run synchronous Playwright in a separate subprocess, as Prefect's event loop can conflict with Playwright's if mismanaged.
- **Timeouts:** ALWAYS set `timeout_seconds` on `@task` and `@flow` decorators for scraping and trading to prevent hanging zombie processes from eating up VPS RAM.