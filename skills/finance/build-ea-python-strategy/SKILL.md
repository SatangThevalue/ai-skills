---
name: build-ea-python-strategy
description: "Guidelines and architecture for building Expert Advisors using Python and MT5."
version: 0.1.0
metadata:
  hermes:
    tags: [MT5, Python, EA, Quantitative, Architecture]
---

# Building Expert Advisors with Python and MT5

This skill captures the essential workflow for transitioning trading concepts into programmatic Expert Advisors (EAs) by combining MetaTrader 5's execution capabilities with Python's data-science ecosystem (pandas, scikit-learn). It focuses on architectural choices, strict data handling rules, and preventing common quantitative errors like look-ahead bias.

## When to Use

- "ช่วยหาบทความเกี่ยวกับการสร้าง EA MT5 ให้หน่อย"
- "สอนเขียน EA MT5 Python"
- When starting a new quantitative trading project bridging MT5 and Python.

## Prerequisites

- MetaTrader 5 terminal installed.
- Python `venv` with: `pip install MetaTrader5 pandas numpy scikit-learn skl2onnx pytz`
- A quantitative hypothesis to test (e.g., trend following vs. mean reversion).

## Quick Reference

- **Satang's Python Brain + MT5 Muscle:** See `references/satang-architecture-principles.md` for the strict risk-managed architecture layout preferred for modern Python/MT5 bridging.
- **Timezone Rule:** MT5 stores all times in UTC. Python `datetime` objects MUST be explicitly timezone-aware (`pytz.timezone("Etc/UTC")`) before fetching data.
- **Data Splitting:** Never use `train_test_split(shuffle=True)` on time-series data. Split chronologically to avoid future leakage.
- **ONNX Export:** Use `skl2onnx` to package trained Python models for native execution inside MQL5 EAs.

## Architectural Approaches

1. **Python Brain + MT5 Muscle (Direct Execution with Risk Controller):** Python loops continuously (or cron-based polling), fetching prices via `mt5.copy_rates_from_pos()`. It runs ML inference (e.g., XGBoost, LSTM) and calculates features (pandas-ta). An explicit Python Risk Manager class acts as a gatekeeper before `mt5.order_send()`, enforcing "Satang's Rules" (No Martingale, ATR Sizing, Break-even SL, Max Daily Drawdown). *Best for sophisticated ML/DL pipelines using Colab for training and lightweight local inference.*
2. **Asynchronous Microservices:** MQL5 EA monitors ticks and sends HTTP requests (or ZeroMQ) to a Python Flask API. Python runs the ML model and returns BUY/SELL JSON payloads. EA handles SL/TP execution natively. *Best for robustness.*
3. **ONNX Native Inference:** Python downloads historical data, trains an ML model (e.g., RandomForest, LSTM), and exports an `.onnx` file. The MQL5 EA loads the `.onnx` file directly onto the chart and executes without Python running. *Best for High-Frequency Trading (HFT) and backtesting in MT5 Strategy Tester.*

## Procedure (Data to ONNX Pipeline)

1. **Strict UTC Data Ingestion:**
   ```python
   import MetaTrader5 as mt5, pandas as pd, pytz
   from datetime import datetime
   mt5.initialize()
   utc = pytz.timezone("Etc/UTC")
   rates = mt5.copy_rates_range("EURUSD", mt5.TIMEFRAME_H1, datetime(2020,1,1, tzinfo=utc), datetime.now(utc))
   df = pd.DataFrame(rates)
   df['time'] = pd.to_datetime(df['time'], unit='s')
   ```

2. **Feature Engineering & Transformation:**
   Avoid standard indicators; calculate *second-order derivatives* (differences of differences) to capture market acceleration.
   ```python
   df['close_diff'] = df['close'].diff()
   df['acceleration'] = df['close_diff'].diff()
   # Filter out features with target correlation < 0.02
   ```

3. **Chronological Model Training:**
   ```python
   # DO NOT SHUFFLE!
   split_idx = int(len(df) * 0.9)
   train, test = df.iloc[:split_idx], df.iloc[split_idx:]
   ```

4. **ONNX Export:**
   ```python
   from skl2onnx import convert_sklearn
   from skl2onnx.common.data_types import FloatTensorType
   initial_type = [("float_input", FloatTensorType([None, X_train.shape[1]]))]
   onnx_model = convert_sklearn(model, initial_types=initial_type)
   with open("model.onnx", "wb") as f:
       f.write(onnx_model.SerializeToString())
   ```

## Pitfalls

- **Timezone Drift:** Forgetting to convert Python's local datetime to UTC before passing it to MT5 functions will silently shift your data, destroying the geometry of your analysis.
- **Look-ahead Bias:** Calculating indicators over the entire dataset *before* splitting train/test allows future data to bleed into past calculations (e.g., using `.rolling().mean()` on the whole dataframe instead of isolated sets).
- **Execution Latency:** If using Python directly to send trades (Approach 1), network latency or script crashes can leave positions unprotected. Always attach `sl` and `tp` inside the `MqlTradeRequest` payload so the broker server holds the risk parameters.

## Verification

The workflow is successful when you can pull raw `copy_rates_range` data, transform it, train an ML model, and execute either an `order_send()` via Python or successfully load an `.onnx` model into the MT5 Strategy Tester.