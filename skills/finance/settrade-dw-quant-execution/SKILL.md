---
name: settrade-dw-quant-execution
description: "Execute DW trading strategies via Settrade Open API."
version: 0.1.0
metadata:
  hermes:
    tags: [Quant, DW, Settrade, Python, Algorithmic-Trading]
---

# Settrade DW Quant Execution

This skill provides the architectural logic for deploying a quantitative trading engine targeting Derivative Warrants (DW) using the Settrade Open API (Python SDK v2). It explicitly decouples market data sourcing (yfinance for underlying, Settrade for DW ticks) from execution (Settrade limit orders), embedding strict risk management (1% max loss) and state tracking (PostgreSQL).

## When to Use
- When deploying an automated Python trading bot for the Thai stock market.
- When calculating Position Sizing and Hard Stop Loss for DW instruments.
- When designing continuous-learning pipelines (MLOps) for trading.
- When the user asks to "trade DW using Settrade Sandbox".

## Prerequisites
- `settrade-v2` installed (`pip install settrade-v2`).
- A PostgreSQL database for state tracking (schema: `finance_db`).
- Settrade Open API credentials stored in `.env` (App ID, Secret, Broker ID, App Code, PIN).

## How to Run
Invoke execution scripts via the `terminal` tool. Run them in a virtual environment (`source .venv/bin/activate`). Do not use `background=true` for tests, but require it for production daemon loops.

## Quick Reference
- Underlying Graph: `yfinance.download(symbol+".BK")`
- DW Live Price: `market.get_quote_symbol(dw_symbol)`
- DW Tick Mapping: Extract tables from DW issuer websites (e.g. DW13).
- Execution: `deri.place_order(..., price_type='Limit', validity_type='Day')`
- Risk Formula: `Position = (Capital * 1%) / (Entry Price - SL Price + Slippage)`

## Procedure

1. **Sourcing Data (Hybrid Strategy):**
   Use `yfinance` to pull historical OHLCV data for the *Underlying Asset* (e.g., PTT.BK) to feed the scoring models (Price Action, Indicators, ML). Do not run indicators on DW charts due to Time Decay and false volume.

2. **Scoring Engine (Ensemble Voting):**
   Combine multiple models (e.g., PA, Indicators, Volume, ML) into a final Confidence Score. Apply a *Market Regime Multiplier* (e.g., 0.5x if ranging) to discount signals that contradict current market conditions.

3. **Filtering DW Instruments:**
   If Score >= 75%, select a DW. Ensure:
   - Call/Put matches signal direction.
   - Time to Maturity > 30 days.
   - Moneyness is near ATM to slightly OTM.
   - Effective Gearing is moderate (4x - 6x).

4. **Tick Mapping & Position Sizing:**
   Map the Underlying's Entry/SL prices to DW prices using the issuer's price table.
   Calculate position size limiting risk to 1% of total capital, factoring in a 1-tick slippage buffer.

5. **Execution (Settrade Sandbox):**
   Connect using `settrade_v2.Investor`. Use the `Derivatives` module (or `Equity` if classified as stock) to place a `Limit` order. Do not use Market (`MP`) with a `Day` validity.

6. **Exit Strategies:**
   - *Hard Stop:* Execute immediately if DW price hits mapped SL (-1%).
   - *Indicator Breakdown:* Exit if Underlying asset breaks trend (e.g., MACD cross down).
   - *Trailing Stop:* Engage only if Confidence Score rises >= 85%.

7. **Telemetry & Paper Trading:**
   Log all signals and executed trades to a PostgreSQL database (`paper_trade_log`) to enable Walk Forward Validation and future Optuna hyperparameter tuning.

## Pitfalls
- **API Rate Limits:** Executing a 100-asset scan simultaneously will trigger rate limits. Use a task runner (e.g. Prefect) with concurrency limits (Batching) to throttle requests.
- **Sandbox Hours:** Settrade Sandbox is only fully functional during actual market hours (10:00-16:30 BKK). Out-of-hours requests yield "User is inactive" errors from the `MarketData` module.
- **Account Type:** Connection requires `Investor`, not `MarketRep` for standard sandbox trading accounts.

## Verification
Run a Python script invoking `Investor(...).Derivatives(account_no=...).get_account_info()` via the `terminal` tool to verify the Settrade connection and credit line.