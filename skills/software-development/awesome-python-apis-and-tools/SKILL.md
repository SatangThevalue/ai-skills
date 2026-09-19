---
name: awesome-python-apis-and-tools
description: "100+ Free Python libraries and APIs for scalable automation, AI, and monetization."
version: 1.0.0
metadata:
  hermes:
    tags: [Python, API, Automation, Open-Source, Free, Monetization]
    related_skills: [free-api-python-monetization-stack]
---

# 100+ Free Python Libraries & APIs (The Ultimate Developer Arsenal)

This skill catalogues an expansive list of 100+ free, open-source Python libraries, frameworks, and public APIs available on GitHub and PyPI. This list is categorized by use case, specifically focusing on tools that enable developers to build scalable businesses, automations, and AI tools with zero initial capital.

## When to Use
- Brainstorming tech stacks for new automation projects.
- Looking for alternatives to paid SaaS platforms (e.g., Stripe, AWS, OpenAI).
- Exploring new areas for Data-as-a-Service (DaaS) or Micro-SaaS.

## Prerequisites
- A local or VPS Python environment.
- Use `uv pip install <library>` to fetch these packages.

## The 100+ Free Tools & APIs

### 🗣️ 1. Advanced Audio & Voice (TTS / STT / Processing)
1. **`coqui-ai/TTS`** - Deep learning toolkit for Text-to-Speech (High quality, can clone voices locally).
2. **`VITS`** - Conditional Variational Autoencoder with Adversarial Learning for End-to-End TTS.
3. **`pytube`** - Lightweight, dependency-free Python library for downloading YouTube Videos (good for extracting audio).
4. **`demucs`** - Music source separation (extract vocals, drums, bass from any song).
5. **`spleeter`** - Deezer's source separation library (another vocal remover).
6. **`audiocraft`** - Meta's library for audio generation (MusicGen, AudioGen).
7. **`pysndfx`** - Apply audio effects (reverb, chorus, pitch shift) easily.
8. **`speechmatics-python`** - STT API wrapper (generous free tier).
9. **`pyAudioAnalysis`** - Audio feature extraction, classification, and segmentation.
10. **`mutagen`** - Read and write audio tags (metadata manipulation).

### 👁️ 2. Computer Vision & Image Generation (Free / Local)
11. **`EasyOCR`** - Ready-to-use OCR with 80+ supported languages (including Thai).
12. **`pytesseract`** - Python wrapper for Google's Tesseract-OCR Engine.
13. **`face_alignment`** - 2D and 3D Face alignment library build using PyTorch.
14. **`DeepFace`** - Lightweight face recognition and facial attribute analysis (age, gender, emotion).
15. **`imageio`** - Read and write a wide range of image data (including animated GIFs).
16. **`rembg`** - Tool to remove images background (runs locally).
17. **`InvokeAI`** - Stable Diffusion implementation with a great local WebUI/API.
18. **`ComfyUI`** - The most powerful and modular node-based GUI for Stable Diffusion (Python backend).
19. **`sam` (Segment Anything)** - Meta's model to cut out any object in any image.
20. **`ultralytics`** - YOLOv8 for real-time object detection and image segmentation.

### 🧠 3. Alternative AI & NLP (No OpenAI Key Required)
21. **`vLLM`** - High-throughput and memory-efficient LLM serving engine (Run your own API).
22. **`CTransformers`** - Python bindings for GGML models (Run LLaMA on CPU).
23. **`instructor`** - Structured extraction in Python using LLMs (force Pydantic outputs).
24. **`semantic-kernel`** - Microsoft's SDK to integrate LLMs into apps.
25. **`haystack`** - End-to-end NLP framework for building search and QA systems (RAG).
26. **`spacy`** - Industrial-strength Natural Language Processing (fast NLP, NER).
27. **`nltk`** - The Natural Language Toolkit (classic text processing).
28. **`textblob`** - Simplified text processing (sentiment analysis).
29. **`gensim`** - Topic modeling for humans (Word2Vec).
30. **`pythainlp`** - Thai Natural Language Processing library (Essential for Thai text tokenization).

### 🌐 4. Public APIs (No Auth or Free Tier)
31. **`PokeAPI`** - All the Pokémon data you'll ever need (Great for practicing API integration).
32. **`OpenWeatherMap API`** - Weather data (Free tier available).
33. **`CoinGecko API`** - Free cryptocurrency price, volume, and market data (No key needed for basic usage).
34. **`Jikan API`** - Unofficial MyAnimeList API.
35. **`SpaceX API`** - Open Source REST API for SpaceX launch, rocket, core, capsule, starlink, launchpad, and mission data.
36. **`REST Countries`** - Get information about countries via a RESTful API.
37. **`TheCatAPI` / `TheDogAPI`** - Pictures of cats/dogs (Free tier).
38. **`Open Food Facts API`** - Free and open database of food products.
39. **`NewsAPI`** - Search worldwide news with code (Free for developers).
40. **`ExchangeRate-API`** - Free currency conversion API.

### 🕵️‍♂️ 5. Advanced Scraping & Browser Automation
41. **`DrissionPage`** - A tool combines web browser automation and requests (bypasses Cloudflare better than Selenium).
42. **`selenium-wire`** - Extends Selenium to intercept and inspect network requests.
43. **`pyppeteer`** - Unofficial Python port of Puppeteer (Headless Chrome).
44. **`mechanicalsoup`** - A Python library for automating interaction with websites.
45. **`fake-useragent`** - Up to date simple useragent faker.
46. **`proxybroker`** - Finds public proxies and checks them.
47. **`newspaper3k`** - Article scraping & curation (extracts title, text, authors from news sites).
48. **`trafilatura`** - Fast Web scraping, text extraction, and HTML parsing.
49. **`twint`** - An advanced Twitter scraping & OSINT tool (No API key needed, though currently fighting Twitter updates).
50. **`snscrape`** - A social networking service scraper (Twitter, Facebook, VK, Instagram).

### 💰 6. Financial, Trading & E-commerce Tools
51. **`freqtrade`** - Free, open-source crypto trading bot framework.
52. **`vectorbt`** - Find your trading edge, using the fastest backtesting engine for Python.
53. **`backtrader`** - Python Backtesting library for trading strategies.
54. **`pyfolio`** - Portfolio and risk analytics in Python.
55. **`ccxt`** - Cryptocurrency trading library (connects to 100+ exchanges).
56. **`stripe-python`** - Stripe API client (Free to integrate, takes a cut of sales).
57. **`paypal-checkout-serversdk`** - PayPal checkout SDK.
58. **`shopee-python`** - Unofficial/Community wrappers for Shopee Open API.
59. **`lazop-sdk-python`** - Lazada Open Platform SDK.
60. **`omise-python`** - Omise Payment Gateway (Popular in Thailand).

### 🗄️ 7. Database, Data Engineering & Storage
61. **`sqlmodel`** - SQL databases in Python, designed for simplicity, compatibility, and robustness (Combines SQLAlchemy + Pydantic).
62. **`tinydb`** - A lightweight document oriented database optimized for your happiness.
63. **`chromadb`** - The open-source AI-native database (Vector DB for RAG).
64. **`qdrant-client`** - Vector search engine client.
65. **`peewee`** - A small, expressive orm.
66. **`dbt-core`** - Data build tool.
67. **`great_expectations`** - Always know what to expect from your data.
68. **`boto3`** - Amazon Web Services (AWS) SDK for Python (Integrates with free tiers or self-hosted MinIO).
69. **`gspread`** - Google Spreadsheets Python API (Use GSheets as a free database).
70. **`pyarrow`** - Cross-language development platform for in-memory analytics.

### 🏗️ 8. Web Frameworks & UI (Build DaaS/SaaS)
71. **`litestar`** - Light, flexible and extensible ASGI API framework.
72. **`sanic`** - Async Python 3.7+ web server and web framework.
73. **`reflex`** - Web apps in pure Python (formerly Pynecone).
74. **`flet`** - Build interactive multi-platform apps in Python (Flutter backend).
75. **`pywebio`** - Write interactive web app in script way.
76. **`panel`** - High-level app and dashboarding solution for Python.
77. **`jinja2`** - Very fast and expressive template engine.
78. **`httpx`** - Next generation HTTP client.
79. **`beautifulsoup4`** - Screen-scraping library.
80. **`flask-cors`** - A Flask extension for handling Cross Origin Resource Sharing (CORS).

### 🛠️ 9. System, Security & Network
81. **`psutil`** - Cross-platform lib for process and system monitoring.
82. **`paramiko`** - SSH2 protocol library.
83. **`fabric`** - High level SSH command execution.
84. **`scapy`** - Interactive packet manipulation program & library.
85. **`cryptography`** - Package designed to expose cryptographic recipes and primitives.
86. **`passlib`** - Comprehensive password hashing framework.
87. **`python-nmap`** - Python bind for nmap network scanner.
88. **`sh`** - Python subprocess replacement (Call bash commands like python functions).
89. **`watchdog`** - Monitor file system events.
90. **`schedule`** - Python job scheduling for humans.

### 📊 10. Data Viz, Reporting & Utilities
91. **`plotly`** - Interactive graphing library.
92. **`seaborn`** - Statistical data visualization.
93. **`matplotlib`** - The standard plotting library.
94. **`reportlab`** - The proven industry standard PDF generating solution.
95. **`weasyprint`** - Visual rendering engine for HTML and CSS that can export to PDF.
96. **`python-docx`** - Create and update Microsoft Word (.docx) files.
97. **`openpyxl`** - A Python library to read/write Excel 2010 xlsx/xlsm files.
98. **`pydantic-settings`** - Settings management using Pydantic.
99. **`pendulum`** - Python datetimes made easy.
100. **`icecream`** - Never use `print()` to debug again (beautiful debug printing).

## Verification
You can install and test any of these libraries via the `terminal` tool using `uv pip install <library-name>`. For APIs, you can use the `requests` library to fetch JSON data.