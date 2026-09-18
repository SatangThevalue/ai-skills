---
name: asset-specific-quant-pipeline
description: "Build and deploy asset-specific AI trading pipelines."
version: 0.1.0
metadata:
  hermes:
    tags: [Quant, MLOps, MQL5, Python, Trading]
---

# Asset-Specific Quant Pipeline

This skill outlines the architecture and procedure for building Asset-Specific MLOps pipelines connecting Python (LightGBM/ONNX) to MetaTrader 5 (MQL5). It provides solutions for hardware-constrained VPS environments, avoids the "one-size-fits-all" trap by separating strategies based on asset classes (Fiat, Crypto, Gold), and uses FastAPI gateways to bypass MT5 limitations for alternative data (News/Macro).

## When to Use
- Designing quantitative trading architectures linking Python and MT5.
- Exporting machine learning models (LightGBM) to ONNX for MQL5 Expert Advisors.
- Optimizing resource-heavy training loops on a limited VPS.
- Integrating ForexFactory news or macro-economic data (Bond Yields) without MT5 WebRequest blockers.
- Troubleshooting strategies that fail due to market noise or spread (e.g., Gold, Crypto, 15m timeframes).

## Prerequisites
- Python environment managed via `uv` (recommended Python 3.12+).
- Python libraries: `yfinance`, `pandas_ta`, `lightgbm`, `onnxmltools`, `fastapi`, `uvicorn`, `loguru`.
- MT5 terminal with `JAson.mqh` installed in `MQL5/Include/`.

## How to Run
- Use the `terminal` tool with `background=true` for heavy training pipelines.
- Use `write_file` to author MQL5 EA scripts and Python FastAPI gateways.
- Use `patch` to adjust dynamic JSON configurations or feature inputs.

## Quick Reference
- **Stable Fiat (EURUSD, USDCHF):** Price Action + Mean Reversion/Trend. High success on 1H/1D timeframes.
- **Volatile Fiat (GBPUSD, USDJPY):** Fails on intraday noise. Requires Macro Yield Spreads (US10Y) or strict Time Filters (Asian Session 22:00-06:00).
- **Gold (XAUUSD):** Fails on standard indicators. Requires HMM Regime Detection, Real Yields, Volatility Breakout Stop Orders, and Hard News Filters.
- **Crypto (BTCUSD):** Fails on standard risk. Requires Asymmetric TP/SL (TP 4.0 ATR / SL 1.5 ATR), Volatility Target Sizing, and Orderbook/Funding Rate alternative data.

## Procedure

1. **Bypass VPS Hardware Constraints**
   Heavy parallel processing (e.g., Prefect orchestrators) will cause SQLite locks and CPU timeouts on a small VPS. 
   - Disable daemon overhead: `export PREFECT_API_URL=""`.
   - Run loops sequentially using `ThreadPoolTaskRunner(max_workers=1)`.
   - Execute via the `terminal` tool in the background using `nohup` or `background=true` with output redirected to a log file.

2. **Asset-Specific Feature Engineering**
   Do not use the same indicators for all assets.
   - *Fiat:* `rsi14`, `ema_gap`.
   - *Gold:* Fractional Differencing, `us10y_diff`, `dxy_ret`.
   - *Crypto:* Volatility Normalization (`close / atr`), Binance `fundingRate`.

3. **Train and Export ONNX Artifacts**
   Train the LightGBM model and export the "4 Pillars of Export":
   - `model.onnx`: The inference engine.
   - `feature_order.json`: Strict array mapping to prevent feature mismatch.
   - `model_config.json`: Dynamic thresholds (e.g., `buy_threshold: 0.65`) and Risk Multipliers.
   - `scaler.json`: For preprocessing normalization.

4. **Deploy FastAPI Gateways for Alternative Data**
   Do NOT hardcode MT5 to scrape the web (avoids IP bans and timezone mismatches).
   - Create a Python FastAPI server (`news_api_server.py`) that fetches ForexFactory XML or Macro Data once per day/hour.
   - Convert all times to UTC.
   - Expose endpoints like `http://localhost:8000/news?symbol=EURUSD`.

5. **Author MQL5 Smart Expert Advisors**
   Design EA variants tailored to the asset:
   - *Core EA:* Standard execution loading dynamic JSON thresholds (`ArrayResize` based on `feature_order.json`).
   - *Asian Ranger EA:* Mean-reversion with strict Time Filters (`Hour() >= 22 || Hour() < 6`).
   - *XAU Sniper EA:* Places `BuyStop` / `SellStop` pending orders at `0.5 ATR` instead of Market Orders. Uses Step Trailing Stops.
   - *News Filter Logic:* EA calls the FastAPI gateway. If `safe == false`, block trading 30 mins before/after news.

## Pitfalls
- **Timezone Mismatch (Data Drift):** Never pass time or news countdowns into the ONNX model training. Python server time (UTC) and Broker time (UTC+2/+3) differ. Handle time dynamically inside MQL5 (`TimeCurrent() - TimeGMT()`).
- **Spread Eaten on Low Timeframes:** Timeframes like 15m generate hundreds of trades but net returns turn negative due to spread costs. Use Meta-Labeling (secondary model predicting trade success) or scale up to 1H/4H.
- **Crypto Fixed Lots:** Using fixed 1% risk on crypto causes -80% drawdowns. Use Volatility Target Sizing (Inverse ATR).
- **Statistical Arbitrage Trap:** Cointegration (P-Value) can fail rapidly. Do not run Pair Trading (e.g., EURUSD vs GBPUSD) without real-time dynamic P-Value checks, otherwise spread divergence will wipe the account.

## Verification
1. Verify the ONNX package: Ensure `.onnx` and `.json` exist in `models/production/`.
2. Verify API Gateway: Use `terminal` to run `curl -s "http://localhost:8000/news?symbol=EURUSD"`. It should return a JSON object with `"safe": true/false`.
3. Verify EA Load: Check MT5 Experts log for `ONNX System Ready. Model requires X features.`