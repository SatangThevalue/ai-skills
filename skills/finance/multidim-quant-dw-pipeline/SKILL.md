---
name: multidim-quant-dw-pipeline
description: "Execute multi-dimensional quant screening and DW trading."
version: 0.3.0
metadata:
  hermes:
    tags: [Quant, Trading, Prefect, PostgreSQL, DW]
---

# Multi-Dimensional Quant DW Pipeline

This skill orchestrates an automated quantitative trading and paper simulation engine that evaluates securities across three decoupled dimensions (Fundamental, Technical, and Volume), enforcing strict 1% portfolio risk management on Derivative Warrants (DW). It executes as a zero-token Prefect flow using PostgreSQL for state, rate-limited thread pools for parallel screening, and Prefect notification blocks for curated alerts.

## When to Use
- When deploying an automated multi-dimensional stock scanner and DW execution engine.
- When screening securities without incurring LLM token costs (100% deterministic Python compute).
- When filtering high-conviction signals (Score >= 75%) with automatic silent mode when market conditions are adverse.
- When managing paper DW positions (entry, TP, SL, indicator breakdown exits) with portfolio heat limits.

## Prerequisites
- PostgreSQL running with schema `finance_db` on host `100.115.66.121:5432` (or localhost).
- Prefect Server running on `http://100.115.66.121:4200/api` (Prefect v3.8.x).
- Python 3.10+ virtual environment with dependencies: `pip install "prefect>=3.8.0" yfinance psycopg2-binary sqlmodel python-dotenv beautifulsoup4`.
- Systemd daemon `satang-quant-runner.service` running `serve_quant_engine.py` for 24/7 background scheduled execution.
- Prefect block `telegram-satang-alerts` created from `CustomWebhookNotificationBlock`.
- Environment variables in `/home/thaieasyvps/satang-workspace/.env`:
  ```env
  DB_URL="postgresql://admin:super_...2026@100.115.66.121:5432/satang_vault"
  PREFECT_API_URL="http://100.115.66.121:4200/api"
  SETTRADE_APP_ID="rWrJLgVKDgkTd38y"
  SETTRADE_APP_SECRET="LXW7..."
  ```

## How to Run
Execute the Prefect orchestration pipeline through the `terminal` tool:
```bash
PREFECT_API_URL="http://100.115.66.121:4200/api" \
PYTHONPATH="/home/thaieasyvps/satang-workspace/apps/quant" \
/home/thaieasyvps/satang-workspace/.venv/bin/python /home/thaieasyvps/satang-workspace/apps/quant/prefect_quant_flow.py
```

## Quick Reference
- Master Flow: `apps/quant/prefect_quant_flow.py`
- Autonomous Runner: `apps/quant/serve_quant_engine.py` (served via `flow.serve()` on Prefect v3)
- Systemd Service: `/etc/systemd/system/satang-quant-runner.service` (24/7 autonomous daemon)
- Fundamental Analyzer: `apps/quant/fundamental_analyzer.py` (Daily DB cache, 20% weight)
- Technical Analyzer: `apps/quant/technical_analyzer.py` (EMA/RSI/MACD/ATR, 40% weight)
- Volume Analyzer: `apps/quant/volume_analyzer.py` (VSA, Volume vs SMA20, 40% weight)
- DW Selector & MM: `apps/quant/dw_selector_and_mm.py` (Two-way Call/Put, 1% risk sizing, Board Lot rounding)
- Exact Tick Scraper: `apps/quant/dw_price_table_scraper.py` (DW01/DW13 table scraper + SET tick step)
- Settrade Order Dispatcher: `apps/quant/settrade_order_dispatcher.py` (Sandbox Equity `satang-E` Limit orders & reconciliation)
- Settrade Realtime Streamer: `apps/quant/settrade_realtime_streamer.py` (MQTT price & order stream)
- Paper Position Manager: `apps/quant/paper_position_manager.py` (Auto open/close, MFE/MAE tracking)
- Two-Way DW Guide: `references/two_way_dw_trading.md` (Call & Put DW mathematical mapping)
- MLOps Telemetry Guide: `references/mlops_feature_store.md` (JSONB features, Triple Barrier, ML export)
- Multi-Horizon Backtesting: `references/multi_horizon_backtest_methodology.md` (1-90 day testing, MM compliance)
- Notification Block: `CustomWebhookNotificationBlock.load("telegram-satang-alerts")`
- Primary Tables: `trading_universe`, `fundamental_evaluations`, `technical_evaluations`, `volume_evaluations`, `composite_signals`, `algo_positions`, `paper_trade_log`, `ml_training_dataset`, `backtest_results`

## Procedure

1. **Daily Fundamental Caching (Intraday Optimization):**
   Before calling external APIs, inspect `finance_db.fundamental_evaluations` where `evaluation_date = CURRENT_DATE`. If present, reuse the record immediately. Fetch from `yfinance` only once per symbol per day to eliminate API quota consumption.

2. **Bounded Parallel Technical & Volume Scan:**
   Run evaluations concurrently using an internal `ThreadPoolExecutor(max_workers=4)`. Never spawn uncapped threads; 3 to 5 workers provide sub-second throughput per ticker (~0.5s/sym) while staying below exchange rate limits and avoiding HTTP 429 errors.

3. **Two-Way Scoring (Call & Put DWs):**
   - **Bullish Evaluation:** Measures Price > EMA20 > EMA50 > EMA200, RSI 50-65, MACD > 0, Bullish volume. High score ($\ge 70\%$) triggers `BUY` (Routes to **Call DW**).
   - **Bearish Evaluation:** Measures Price < EMA20 < EMA50, RSI < 45 breakdown, MACD histogram < 0, Heavy volume selling. High score ($\ge 70\%$) triggers `SELL` (Routes to **Put DW** to profit from market decline).
   - In both cases, the trader **BUYS** the DW (Long Call or Long Put). Downside risk is strictly bounded to the DW premium paid.

4. **Exact Tick Mapping & Position Sizing:**
   - Query `dw_catalog` for matching Call or Put DW where days to expiry $\ge 30$ and effective gearing is 3.5x to 5.5x.
   - Use `DWPriceTableScraper.map_ticks()` to map underlying entry, SL, and TP into exact DW prices via issuer tables or SET tick rules.
   - For Put DWs, underlying SL is *above* entry and TP is *below* entry, but DW SL is always *below* DW Entry:
     $$\text{Volume} = \left\lfloor \frac{\text{Capital} \times 0.01}{(\text{DW Entry} - \text{DW SL}) + 0.01} \cdot \frac{1}{100} \right\rfloor \times 100$$
   - Enforce Portfolio Heat limit ($\le 25\%$ total capital outlay, max 3 positions).

5. **Sandbox Order Dispatching & Reconciliation:**
   - Execute limit orders using `Investor.Equity(account_no="satang-E").place_order(pin="000000", side="Buy", price_type="Limit", validity_type="Day")`.
   - Track returned `orderNo` and update order status in `finance_db.trade_journal` via `reconcile_orders()`.

6. **Prefect v3 Autonomous Daemon:**
   - Serve the flow using `flow.serve(name="satang-dw-quant-scanner-v3", cron="*/3 10-16 * * 1-5")`.
   - Maintain 24/7 background execution via systemd daemon `/etc/systemd/system/satang-quant-runner.service`.

7. **Filtering and Consolidated Notifications:**
   - Filter evaluations strictly for $\text{Final Score} \ge 75.0\%$.
   - Sort descending.
   - **Silent Mode:** If no symbol qualifies, terminate without sending messages (zero notification spam).
   - If qualified, format a single consolidated leaderboard (Top 1 to 3) and dispatch via `CustomWebhookNotificationBlock.load("telegram-satang-alerts")`.

## Pitfalls
- **SET DW Board:** In Thailand SET, Derivative Warrants (DW) trade on the **Equity board** (`satang-E`). Calling `Investor.Derivatives(account_no="satang-D").place_order()` for a DW will fail; use `Investor.Equity(account_no="satang-E")`.
- **Order OSS Spreads:** Settrade rejects orders if the limit price exceeds 10 spreads from last price. Ensure limit prices match the valid trading band.
- **Prefect v3 Runner Deployment:** In Prefect v3, do not use deprecated `Deployment.build_from_flow()` or client-side schemas that conflict with the server API. Use `flow.serve()` to simultaneously register, poll, and execute scheduled runs.
- **Market Hours Simulation:** Settrade Sandbox returns "User is inactive" outside 10:00-16:30 BKK time. Maintain simulation mode in testing to evaluate pipelines off-hours.
- **DW Direct Analysis Fallacy:** Never apply technical indicators to DW price charts due to decay and low volume. Always compute indicators on the underlying equity (e.g. `PTT.BK`) and map exit levels to the DW.

## Verification
Run a verification query via the `terminal` tool to verify recorded signals and paper trading status in PostgreSQL:
```bash
python3 -c "
import psycopg2
conn = psycopg2.connect('postgresql://admin:super_...2026@100.115.66.121:5432/satang_vault')
cur = conn.cursor()
cur.execute('SELECT count(*) FROM finance_db.composite_signals WHERE timestamp::date = CURRENT_DATE;')
print('Today Composite Signals:', cur.fetchone()[0])
cur.execute('SELECT count(*) FROM finance_db.algo_positions;')
print('Total Algo Positions Recorded:', cur.fetchone()[0])
conn.close()
"
```
Output will report integer counts confirming active database telemetry.