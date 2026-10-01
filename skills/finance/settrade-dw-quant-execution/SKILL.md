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
- Detailed scoring formulas & DB schema: `references/multidim_scoring_and_mm.md`
- Order Dispatcher & Lifecycle: `references/settrade_order_lifecycle.md`
- Underlying Graph: `yfinance.download(symbol+".BK")`
- DW Live Price: `market.get_quote_symbol(dw_symbol)`
- DW Tick Mapping: Extract tables from DW issuer websites (e.g. DW13).
- Execution: `equity.place_order(pin="000000", side="Buy", symbol=dw_sym, volume=vol, price=price, price_type="Limit", validity_type="Day")`
- Risk Formula: `Position = (Capital * 1%) / (Entry Price - SL Price + Slippage)`

## Procedure

1. **Sourcing Data (Hybrid Strategy):**
   Use `yfinance` to pull historical OHLCV data for the *Underlying Asset* (e.g., PTT.BK) to feed the scoring models. Note: Thai stocks require `.BK` suffix, while crypto tickers require `-USD` (never append `.BK` to crypto). Do not run indicators on DW charts due to Time Decay and false volume.

2. **Scoring Engine (Multi-Dimensional Voting):**
   Evaluate three decoupled dimensions:
   - **Fundamental (20%):** P/E, P/BV, ROE, D/E, Profit Margins.
   - **Technical (40%):** EMA 20/50/200 trend alignment, RSI 14 sweet spot (50-65), MACD crossover.
   - **Volume (40%):** 20-day SMA volume surge ratio and VSA expansion pattern.
   Apply a *Market Regime Multiplier* (0.7x - 1.0x) to penalize trend-following signals in ranging/bearish regimes. Refer to `references/multidim_scoring_and_mm.md` for the exact rubric.

3. **Filtering DW Instruments:**
   If Score >= 70%, select a DW. Ensure:
   - Call/Put matches signal direction.
   - Time to Maturity > 30 days.
   - Moneyness is near ATM to slightly OTM.
   - Effective Gearing is moderate (3.5x - 5.5x).

4. **Tick Mapping & Position Sizing:**
   Map the Underlying's Entry/SL prices to DW prices using the issuer's price table.
   Calculate position size limiting risk to 1% of total capital, factoring in a 1-tick slippage buffer, rounded down to SET Board Lots (multiples of 100 shares), capped at 25% max portfolio outlay.

5. **Execution (Settrade Sandbox):**
   Connect using `settrade_v2.Investor`. In Thailand SET, **Derivative Warrants (DW) trade exclusively on the Equity board**. Use `inv.Equity(account_no="satang-E")` (never Derivatives `satang-D`). Place a `Limit` order specifying numeric price, multiple of 100 shares, and `validity_type="Day"`. Do not use Market (`MP-MKT`) with `Day`.

6. **Exit Strategies:**
   - *Hard Stop:* Execute immediately if DW price hits mapped SL (-1%).
   - *Indicator Breakdown:* Exit if Underlying asset breaks trend (e.g., MACD cross down).
   - *Trailing Stop:* Engage only if Confidence Score rises >= 85%.

7. **Telemetry & Paper Trading:**
   Log all signals and executed trades to PostgreSQL tables (`finance_db.composite_signals`, `finance_db.paper_trade_log`, `finance_db.algo_positions`, `finance_db.ml_training_dataset`) to enable Walk Forward Validation and future Optuna hyperparameter tuning.

## Pitfalls
- **SET DW Account Type:** Derivative Warrants (DW) must be traded via `investor.Equity(account_no="satang-E")`. The Derivatives account (`satang-D`) is reserved for TFEX futures/options and will reject DW equity symbols.
- **Settrade Order Spread Guard (OSS):** Placing limit orders exceeding 10 spreads from the last traded price triggers `[OSS] Order price exceeds 10 spread(s) from last price` rejection. Ensure price is within 10 spreads.
- **Floor / Ceiling Enforced:** Orders outside the day's floor/ceiling return `Price should between X to Y`.
- **Order Syntax:** Side must be title-cased (`"Buy"` or `"Sell"`). Volume must be a multiple of 100 (Board Lot). PIN is `000000` for Sandbox.
- **Prefect Version Compatibility:** Prefect 2.x uses `SequentialTaskRunner()` or `ConcurrentTaskRunner()`, whereas Prefect 3.x uses `ThreadPoolTaskRunner()`. Do not mix versions. Pin `anyio<4.0.0` on Prefect 2.20 to avoid `GatherTaskGroup` abstract class errors.
- **API Rate Limits:** Executing a 100-asset scan simultaneously will trigger rate limits. Use thread pools bounded to 3-5 workers.
- **Symbol Formatting:** `yfinance` rejects symbols with wrong extensions (e.g., `BTCUSD.BK`). Ensure symbol resolution maps Thai stocks to `.BK` and crypto to `-USD`.
- **Sandbox Hours:** Settrade Sandbox returns "User is inactive" outside 10:00-16:30 BKK time for `MarketData`. However, `Equity.place_order()` accepts limit orders even outside hours, staging them as `Offline order` (`status: OF`).
- **Account Type:** Connection requires `Investor`, not `MarketRep` for standard sandbox trading accounts.

## Verification
Run a Python script invoking `Investor(...).Equity(account_no="satang-E").get_account_info()` via the `terminal` tool to verify the Settrade connection and credit line (`10,000,000.0 THB`).