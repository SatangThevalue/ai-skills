---
name: settrade-adaptive-survival-bot
description: "Deploy an adaptive algorithmic trading bot for Thai stocks."
version: 0.1.0
metadata.hermes.tags:
  - Algorithmic Trading
  - Settrade Open API
  - Python
  - Quantitative Finance
---

# Adaptive Survival Trading Bot (SET)

Deploys a production-ready, multi-timeframe algorithmic trading bot (`AdaptiveSurvivalSystemV4`) connected to the Settrade Open API Sandbox. It scans the Thai stock market (SET Universe), analyzes 1W/1D/1H trends (Confluence), applies dynamic risk management (Board Lot sizing, Commission adjustment, Consecutive loss multipliers), and executes Market Orders automatically during SET operational hours.

## When to Use

* When deploying an automated stock scanner and trader for the Thai market.
* When needing a framework for volatility-adjusted position sizing and Drawdown recovery.
* When setting up a headless trading cronjob that respects Thai market hours and random open/close intervals.

## Prerequisites

* Python 3.8+ with `yfinance` and `settrade-v2` (`uv pip install yfinance settrade-v2==2.2.1`).
* Settrade Open API Application ID and Secret (Sandbox or Production).
* Equity Account number (`satang-E`) and PIN (`000000`).

## How to Run

Invoke the main runner script via the `terminal` tool. For autonomous execution, schedule it using the `cronjob` tool.

## Quick Reference

* Settrade Sandbox Auth Endpoint: `https://developer.settrade.com/api/openapi/auth/login`
* SET Morning Open: `10:00` - `12:30` (Random Pre-open: `09:55`-`10:00`)
* SET Afternoon Open: `14:30` - `16:30` (Random Pre-open: `14:25`-`14:30`)
* YFinance SET Suffix: `.BK` (e.g., `PTT.BK`)

## Procedure

1. **Deploy the System Scripts:**
   Write the core logic (`adaptive_survival_system_v4.py`) and the execution runner (`sandbox_runner.py`) into the `~/.hermes/scripts/` directory using the `skill_manage` tool (action `write_file`).

2. **Configure Credentials:**
   Edit the configuration section in `sandbox_runner.py` using `patch` to insert your specific `APP_ID` and `APP_SECRET`.

3. **Test the Execution Loop:**
   Run the bot manually via the `terminal` tool to verify auth, portfolio sync, and market scanning.
   ```bash
   ~/.hermes/hermes-agent/venv/bin/python ~/.hermes/scripts/sandbox_runner.py
   ```

4. **Schedule the Autonomous Bot:**
   Use the `cronjob` tool to schedule the bot to run periodically during SET market hours (e.g., every 30 minutes, Mon-Fri).
   ```json
   {
     "action": "create",
     "name": "settrade-sandbox-auto-trade",
     "schedule": "*/30 10-16 * * 1-5",
     "script": "sandbox_runner.py",
     "no_agent": true
   }
   ```

## Pitfalls

* **Market Price (MP-MKT) Validity:** When placing `MP-MKT` (Market Order) via the Settrade API, you CANNOT use `validity_type="Day"`. The Stock Exchange of Thailand (SET) rules mandate that market orders must be executed immediately or cancelled. You must pair `price_type="MP-MKT"` with `validity_type="FOK"` (Fill or Kill) or `validity_type="IOC"` (Immediate or Cancel). Using "Day" will cause the broker to reject the order (Error: "Cannot place Market order when validity is not FOK/IOC").
* **Time Decay in DW:** This specific algorithm relies on underlying price trends. Do NOT feed Derivative Warrants (DW) ticker data directly into the bot; their price degrades via time decay, corrupting MACD/EMA signals. Analyze the underlying stock instead.
* **YFinance Data Latency:** YFinance free tier may have slight delays or missing tickers compared to real-time Settrade WebSocket data.
* **Repainting:** If evaluated intraday, Daily indicators (like Daily MACD) can repaint until the market closes at 16:30. The bot's 1H timeframe mitigates this, but be aware of mid-day signal reversals.
* **Random Open/Close:** The SET uses random opening (09:55-10:00, 14:25-14:30) and closing (16:35-16:40) times. Firing Market Orders (`MP-MKT`) during these Pre-open/Pre-close phases can result in unfavorable execution prices. The runner script blocks execution during these precise windows.

## Verification

The terminal execution or cronjob output will display `✅ ล็อกอิน Settrade Sandbox สำเร็จ!`, followed by the current Cash Balance, a list of Top Picks, and an execution summary (Buy/Sell/Hold).