---
name: thailand-monetization-playbooks
description: Detailed execution methods and concrete examples for the 4 pillars of Thai monetization (Faceless Media, LINE Agents, Quant Trading, DaaS).
---
# Execution Playbooks: Thailand Monetization (2026-2027)

This skill provides the technical blueprint and concrete examples for implementing the 4 core Zero-Touch monetization pillars in Thailand. Designed for tight VPS constraints and highly automated workflows.

## Pillar 1: Automated "Faceless" Media
**The Method:** 
1. Use `n8n` to orchestrate data collection (e.g., RSS, API, Scraping).
2. Pass data to an LLM to generate structured, hook-heavy scripts.
3. Generate voice using Thai TTS APIs (or local models).
4. Use `Faster-Whisper` to generate `.ass` subtitles.
5. Use raw `FFmpeg` complex filters (to save RAM) to stitch background videos, images, audio, and subtitles together.
6. Auto-upload via platform APIs.

**Concrete Examples:**
*   **Example 1: TikTok Shop Affiliate Reviewer**
    *   *Flow:* Scrape top 10 trending items on Shopee/TikTok. LLM writes a 45-second script ("3 เหตุผลที่ต้องซื้อ..."). Download product images. Use FFmpeg `zoompan` to create a slideshow video. Merge with TTS and lo-fi background music. Auto-post with the affiliate link in the description.
*   **Example 2: YouTube Long-form "Sleep" Podcasts (Horror / Dhamma)**
    *   *Flow:* LLM generates a 10,000-word ghost story set in Thai provinces or Buddhist teachings. Chunk text, send to TTS. Stitch into a 1-hour audio file. Loop a dark, ambient 10-second video clip using FFmpeg `-stream_loop -1`. Add large Thai subtitles. Monetize via YouTube AdSense.

## Pillar 2: B2B AI Agents on LINE OA (Micro-SaaS)
**The Method:**
1. Set up a `FastAPI` webhook to receive LINE Messaging API events.
2. Verify the LINE signature.
3. Route text/images to a `LangGraph` state machine.
4. Use `AsyncPostgresSaver` to remember user context across sessions.
5. Use Tools (Function Calling) to trigger external APIs (SlipOK, Google Calendar).

**Concrete Examples:**
*   **Example 1: The "Mae-Kha" (Online Seller) Checkout Agent**
    *   *Flow:* User asks "มีสีแดงไหม?". Agent checks database inventory and replies "มีครับ กดสั่งได้เลย". User uploads a bank transfer slip. Agent uses the SlipOK API to verify the QR code, amount, and receiver. Once verified, Agent updates the DB, sends a confirmation LINE message, and pushes an order to the packing dashboard.
*   **Example 2: 24/7 Dental Clinic Receptionist**
    *   *Flow:* Patient asks "ดัดฟันราคาเท่าไหร่?". Agent uses RAG to pull pricing. User asks to book for Saturday. Agent calls Google Calendar API tool to check slots, proposes 10:00 AM, and registers the booking into the system. Subscriptions sold to clinics at 990 THB/month.

## Pillar 3: Quant Trading & Algo Systems
**The Method:**
1. Run `cronjob` schedules on the VPS.
2. Fetch market data using `yfinance` (US Stocks), `ccxt` (Crypto), or `Settrade API` (Thai SET/DW).
3. Compute signals using `pandas-ta` (must drop NaNs).
4. Execute trades based on strict risk management (1% risk per trade).
5. Log trade metadata to `MLflow` and send a Telegram notification.

**Concrete Examples:**
*   **Example 1: Settrade DW Daily Mean Reversion**
    *   *Flow:* At 10:30 AM daily, fetch top 5 most liquid Call/Put DWs. Calculate Bollinger Bands. If the underlying SET50 drops below the lower band (oversold), place a Fill-Or-Kill (FOK) order for the Call DW. Exit trade when price reverts to the SMA-20.
*   **Example 2: Crypto Delta-Neutral Funding Arbitrage**
    *   *Flow:* Monitor Hyperliquid (Perps) and Binance (Spot). When the funding rate for SOL-PERP is highly positive (longs pay shorts), the bot buys $1,000 of SOL Spot and simultaneously shorts $1,000 of SOL-PERP. The price risk cancels out (Delta Neutral), and the bot safely collects the funding fee yield every 8 hours.

## Pillar 4: DaaS (Data-as-a-Service) & Web Scraping
**The Method:**
1. Write `Playwright` (for JS-heavy sites) or `BeautifulSoup` scrapers.
2. Clean and validate extracted data strictly using `Pydantic`.
3. Store in `PostgreSQL`.
4. Build a `FastAPI` layer with API Key authentication and tiered rate limits (Redis).

**Concrete Examples:**
*   **Example 1: Thai Real Estate Arbitrage Radar**
    *   *Flow:* Scrape DDproperty/Hipflat nightly. Calculate the average price per square meter for specific BTS/MRT zones. Flag listings that are 20% below the moving average (distressed sales). Package this feed into an API and sell monthly access to real estate flippers and investors.
*   **Example 2: Government Procurement (e-GP) Alert System**
    *   *Flow:* Scrape the Thai government's e-GP website daily for new bidding projects. Allow SME clients to register keywords (e.g., "ติดตั้งเครื่องปรับอากาศ", "ซ่อมบำรุง"). When a matching project is posted, instantly send an alert via LINE Notify/Telegram to the client so they can bid first.