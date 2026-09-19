---
name: free-api-python-monetization-stack
description: "100 free Python libraries and APIs for TTS, AI, scraping, finance, and automation."
version: 1.0.0
metadata:
  hermes:
    tags: [Open-Source, Python, API, Automation, Monetization]
---

# 100 Free Python Libraries & APIs for Monetization

This skill is a master index of 100 completely free, open-source Python libraries and APIs (available on GitHub/PyPI) mapped to specific monetization workflows. It is designed to help developers build Zero-Touch automation pipelines without incurring monthly SaaS or API costs.

## When to Use
- When planning a new automation project and looking for free tool alternatives.
- When you need to bypass paid APIs (like OpenAI, ElevenLabs, Apify).
- When expanding the monetization stack for trading, media generation, or data scraping.

## Prerequisites
- Python 3.8+ (preferably managed via `uv`).
- A Linux VPS for 24/7 background execution.

## How to Run
Use `uv pip install <library_name>` via the `terminal` tool to install any of the listed packages.

## The 100 Monetization Libraries (Categorized)

### 🎙️ 1. TTS, Audio & Speech Recognition (Audio Automation)
1. **`edge-tts`** - Free Microsoft Edge Neural voices (Best for Thai Faceless Videos).
2. **`gTTS`** - Google Translate TTS (Free, no API key, robotic voice).
3. **`faster-whisper`** - Free OpenAI Whisper model for CPU (Karaoke subtitles).
4. **`pyttsx3`** - Offline text-to-speech conversion.
5. **`bark`** - Suno's open-source text-to-audio model (Requires GPU).
6. **`meloTTS`** - High-quality multi-lingual TTS by MyShell.
7. **`SpeechRecognition`** - Library for performing speech recognition, with support for offline models.
8. **`pydub`** - Audio manipulation (cutting, joining, volume adjustments).
9. **`librosa`** - Music and audio analysis (beat detection for syncing video).
10. **`pedalboard`** - Spotify's library for adding studio-quality audio effects (EQ, Reverb).

### 🤖 2. AI & Machine Learning (Zero-Cost LLMs)
11. **`g4f` (GPT4Free)** - Access GPT-4 / Claude API endpoints for free via reverse engineering.
12. **`ollama`** - Run Llama 3, Mistral, and other LLMs locally on your VPS/PC.
13. **`llama.cpp`** - C++ port of LLaMA model for CPU inference.
14. **`transformers`** - HuggingFace's core library for all NLP tasks.
15. **`huggingface_hub`** - Download free open-source models.
16. **`langchain`** - Building applications with LLMs through composability.
17. **`llama-index`** - Data framework for connecting custom data sources to LLMs (RAG).
18. **`litellm`** - Call all LLM APIs using the OpenAI format.
19. **`outlines`** - Guided text generation (force local LLMs to output strict JSON).
20. **`sentence-transformers`** - Free text embeddings for vector databases.

### 🕷️ 3. Web Scraping & Data Extraction (DaaS)
21. **`playwright`** - Modern browser automation (bypasses many simple anti-bots).
22. **`beautifulsoup4`** - Classic HTML parsing and data extraction.
23. **`scrapy`** - Fast, high-level web crawling framework for large-scale data extraction.
24. **`yt-dlp`** - Ultimate YouTube / Video downloader and metadata scraper.
25. **`facebook-scraper`** - Scrape Facebook public pages without API keys.
26. **`instaloader`** - Download pictures (or metadata) from Instagram.
27. **`tweepy`** - Twitter API client (Free tier allows reading public tweets).
28. **`requests-html`** - HTML Parsing for Humans (with JS support).
29. **`httpx`** - Next-generation HTTP client (async, faster than requests).
30. **`feedparser`** - Parse RSS and Atom feeds (great for news aggregator bots).

### 🎬 4. Video, Image & Media Generation (Faceless Channels)
31. **`ffmpeg-python`** - Python bindings for FFmpeg (Core video rendering).
32. **`moviepy`** - Video editing via Python (good for prototyping).
33. **`Pillow` (PIL)** - Image processing, generating text overlays safely.
34. **`opencv-python` (cv2)** - Computer vision, auto-cropping, face detection.
35. **`rembg`** - AI tool to remove image backgrounds automatically.
36. **`diffusers`** - HuggingFace library for Stable Diffusion (Image generation).
37. **`controlnet_aux`** - Auxiliary models for Stable Diffusion ControlNet.
38. **`Wand`** - MagickWand API binding for Python (ImageMagick).
39. **`face_recognition`** - Recognize and manipulate faces from Python.
40. **`mediapipe`** - Google's ML solutions for face/hand tracking (great for Vtubers).

### 📈 5. Finance, Crypto & Algorithmic Trading
41. **`yfinance`** - Free Yahoo Finance market data downloader.
42. **`pandas-ta`** - 130+ Technical Analysis indicators (RSI, MACD) for pandas DataFrames.
43. **`ccxt`** - Cryptocurrency trading library supporting 100+ exchanges.
44. **`ta-lib`** - Widely used technical analysis library (C-based, extremely fast).
45. **`tvDatafeed`** - Unofficial TradingView data scraper (real-time data without API keys).
46. **`alpha_vantage`** - Stock API wrapper (Free tier available).
47. **`binance-python`** - Official Binance API wrapper.
48. **`investpy`** - Financial data extraction from Investing.com.
49. **`settrade-v2`** - Thai Stock Market API (Free Sandbox available for algo-trading).
50. **`pyalgotrade`** - Event-driven algorithmic trading Python library.

### 💾 6. Database & High-Speed Data Processing
51. **`asyncpg`** - Extremely fast async PostgreSQL client.
52. **`sqlite3`** - Built-in, zero-configuration database (good for local caching).
53. **`redis-py`** - Redis client for caching and pub/sub messaging.
54. **`motor`** - Async driver for MongoDB.
55. **`supabase`** - Python client for Supabase (Open source Firebase alternative, generous free tier).
56. **`firebase-admin`** - Google Firebase SDK (Free tier).
57. **`minio`** - S3-compatible object storage (Self-hosted for free video storage).
58. **`duckdb`** - In-process SQL OLAP database (super fast data analytics).
59. **`polars`** - Blazing fast DataFrame library written in Rust (pandas alternative).
60. **`pandas`** - The standard data manipulation and analysis library.

### ⚙️ 7. Task Orchestration & Automation
61. **`prefect`** - Modern workflow orchestration (Zero-touch pipeline brain).
62. **`celery`** - Distributed task queue (Industry standard).
63. **`apscheduler`** - Advanced Python Scheduler (Cron-like execution).
64. **`schedule`** - Python job scheduling for humans.
65. **`rq`** - Simple job queues for Python backed by Redis.
66. **`pyautogui`** - Cross-platform GUI automation (Mouse/Keyboard control).
67. **`pynput`** - Control and monitor input devices.
68. **`watchdog`** - Python API to monitor file system events.
69. **`n8n`** - (Node-based, but integrable) Self-hosted workflow automation.
70. **`airflow`** - Apache Airflow (Heavy-duty orchestration).

### 🌐 8. Web Frameworks & Dashboards
71. **`fastapi`** - High-performance async API framework.
72. **`streamlit`** - The fastest way to build custom ML/Data web apps.
73. **`gradio`** - Build UIs for machine learning models instantly.
74. **`flask`** - Micro web framework.
75. **`django`** - Batteries-included web framework.
76. **`uvicorn`** - Lightning-fast ASGI server.
77. **`pydantic`** - Data parsing and validation using Python type hints.
78. **`aiohttp`** - Asynchronous HTTP client/server.
79. **`dash`** - Analytical Web Apps for Python.
80. **`nicegui`** - Create web-based UI with Python.

### 💬 9. Social Media & Messaging Bots
81. **`line-bot-sdk`** - Official LINE Messaging API SDK (Essential for Thai market).
82. **`python-telegram-bot`** - Create Telegram bots (Great for system alerts).
83. **`discord.py`** - API wrapper for Discord.
84. **`slack_sdk`** - Slack API client.
85. **`praw`** - Python Reddit API Wrapper (Great for scraping story content).
86. **`pyrogram`** - Telegram MTProto API Client (Control user accounts).
87. **`mastodon.py`** - Mastodon API wrapper.
88. **`twitchio`** - Async bot framework for Twitch.
89. **`google-api-python-client`** - Access Google Sheets/Drive for free DB alternatives.
90. **`notion-client`** - Official Notion API client (Use Notion as a CMS/DB).

### 🛡️ 10. DevOps, Utilities & Anti-Ban
91. **`uv`** - An extremely fast Python package installer and resolver written in Rust.
92. **`playwright-stealth`** - Stealth plugin for Playwright to avoid bot detection.
93. **`fake-useragent`** - Up-to-date simple useragent faker with real world database.
94. **`cloudscraper`** - Bypass Cloudflare's anti-bot page (Useful for web scraping).
95. **`python-dotenv`** - Reads key-value pairs from a `.env` file.
96. **`loguru`** - Python logging made (stupidly) simple.
97. **`rich`** - Beautiful formatting in the terminal (colors, tables, progress bars).
98. **`tqdm`** - Fast, Extensible Progress Meter.
99. **`docker-py`** - Manage Docker containers from Python.
100. **`pytest`** - Framework for writing scalable tests.

## Pitfalls
- **API Changes:** Unofficial scrapers (like `facebook-scraper` or `yt-dlp`) break when platforms change their HTML. Always pin your versions but be ready to update (`uv pip install -U <pkg>`) when they fail.
- **TOS Violations:** Libraries like `g4f` (GPT4Free) operate in a gray area. They are great for prototyping but should not be relied upon for mission-critical production APIs.
- **Resource Limits:** Just because a library is free doesn't mean it's lightweight. `playwright`, `moviepy`, and `diffusers` can easily crash a low-RAM VPS.

## Verification
To verify the availability of any library, invoke the terminal tool and run `uv pip install <library_name>`.