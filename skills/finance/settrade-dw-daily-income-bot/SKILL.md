---
name: settrade-dw-daily-income-bot
description: "Deploy an automated DW trading bot using Settrade Open API."
version: 0.1.0
metadata:
  hermes:
    tags: [Settrade, Trading, DW, Cronjob, Python]
---

# Settrade DW Daily Income Bot

Deploys a complete execution loop connecting a survival-first trading engine to the Settrade Open API (Sandbox) for automated DW (Derivative Warrants) trading. It handles portfolio syncing, global macro checks (VIX), technical analysis on underlying stocks, dynamic position sizing, and scheduled execution via cron. It does NOT implement direct MarketData subscriptions due to Sandbox restrictions, falling back to simulated DW prices for position sizing when necessary.

## When to Use

- The user wants to trade DWs automatically.
- A request to build a "daily income bot" for the Thai stock market.
- "สร้างอัลกอริทึมเทรดให้หน่อย dw"

## Prerequisites

- Settrade Open API credentials securely stored in `~/.settrade.env` (APP_ID, APP_SECRET).
- Python environment with `settrade-v2`, `pandas`, `yfinance`, and `pytz` installed.
- Target DW symbols updated to currently active series (e.g., `PTT01C2412A`).

## How to Run

1. Use the `terminal` tool to copy the script template to `~/.hermes/scripts/dw_daily_income_bot.py`.
2. Schedule the bot using the `cronjob` tool.

## Quick Reference

- **Config Path:** `~/.settrade.env`
- **Global Macro Filter:** VIX > 25 triggers "RISK_OFF" (suspend CALL buys).
- **Trend Filter:** ADX > 25 required to enter trades (avoids sideways/Time Decay).
- **Execution:** `price_type="MP-MKT"`, `validity_type="FOK"`.
- **Sizing Rule:** `min(max_cap_allowed, max_risk_allowed)`.

## Procedure

1. **Deploy the Script**
   Use the `terminal` tool to write the DW trading script:
   ```bash
   cp ~/.hermes/skills/finance/settrade-dw-daily-income-bot/scripts/dw_bot_template.py ~/.hermes/scripts/dw_daily_income_bot.py
   ```

2. **Verify Environment Variables**
   Ensure the `~/.settrade.env` file exists and is populated with the correct API credentials.
   ```bash
   cat ~/.settrade.env
   ```

3. **Schedule the Cron Job**
   Schedule the script to run during Thai market hours using the `cronjob` tool:
   Call `cronjob(action="create", name="dw-daily-income-bot", schedule="*/30 10-16 * * 1-5", script="dw_daily_income_bot.py", no_agent=True)`

4. **Monitor Execution**
   Verify the bot's logic and API connectivity by triggering a manual run:
   ```bash
   python3 ~/.hermes/scripts/dw_daily_income_bot.py
   ```

## Pitfalls

- **Sandbox MarketData Inactivity:** The Settrade Sandbox often returns `User is inactive` for `MarketData` API calls (like `get_quote_symbol`), especially outside core trading hours. The script includes a fallback mock price to allow position sizing calculations to proceed for testing purposes.
- **Underlying vs DW Symbols:** `yfinance` does not support Thai DW symbols. Technical analysis (EMA, ADX, RSI) MUST be performed on the underlying stock (`PTT.BK`), while execution (`place_order`) targets the DW symbol (`PTT01C2412A`).
- **Market Hours Enforcement:** `MP-MKT` with `FOK` validity will be rejected if sent outside market open hours. The script includes an `is_market_open()` check (timezone: `Asia/Bangkok`) to gracefully exit if the market is closed or on a lunch break.

## Verification

Check the most recent output of the script to ensure it logged into Settrade, checked the VIX, and evaluated the underlying stocks without crashing.
```bash
python3 ~/.hermes/scripts/dw_daily_income_bot.py
```