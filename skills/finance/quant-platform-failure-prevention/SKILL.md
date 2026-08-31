---
name: quant-platform-failure-prevention
description: Quant PM checklist for preventing AI trading system failures (Python to MQL5 via ONNX).
---
# Quant Trading Platform Failure Prevention Guide

**Core Philosophy:** "AI Trading systems rarely fail because of weak models; they fail because the surrounding infrastructure is fragile."

Use this guide as a **Deployment Checklist** before moving any Quant/AI strategy from Python Research to MT5 Production. 

## 1. Data Risks
| Risk | Symptoms & Impact | Prevention & Solution |
| :--- | :--- | :--- |
| **Data Leakage** | Backtest looks perfect, production fails instantly (e.g., target `shift(-5)` leaks into features). | ✅ Use historical data only.<br>✅ Strict Walk-Forward validation.<br>✅ Code Review & Feature Audit. |
| **Timestamp Misalignment** | Python in UTC, MT5 in Broker Time -> Features/News timing completely wrong. | ✅ Store EVERYTHING in UTC in DB (PostgreSQL).<br>✅ Convert Timezone ONLY at presentation/execution layer. |
| **Missing Candles** | Gaps in timeframes distort ATR, RSI, and Returns. | ✅ Implement Data Quality Checks prior to training pipeline. |
| **Duplicate Data** | API retries insert duplicate rows. | ✅ PostgreSQL `UNIQUE(symbol, timeframe, timestamp)` constraint. |

## 2. Feature Engineering Risks
| Risk | Symptoms & Impact | Prevention & Solution |
| :--- | :--- | :--- |
| **Feature Drift** | Model trained on ATR Mean = 1.0, Production sees ATR Mean = 3.2. | ✅ PSI Monitoring & Data Drift Dashboards (Evidently).<br>✅ Automated Alerts. |
| **Feature Mismatch** | #1 cause of ONNX failure. Python logic (ATR14/ATR100) != MQL5 logic (ATR14/ATR50). | ✅ Feature Registry & Feature Contracts.<br>✅ `feature_order.json`.<br>✅ Unit Tests comparing Python vs MQL5 outputs. |
| **Scaling Mismatch** | Python uses `RobustScaler`, MQL5 uses raw values. Predictions break. | ✅ Always export and apply `scaler.json` in MT5. |

## 3. Label (Target) Risks
- **Label Leakage:** Target variables accidentally included as training features. **Fix:** Strict Label Registry and Feature Review.
- **Label Instability:** Changing definitions (e.g., Future Return vs. Triple Barrier) breaks comparability. **Fix:** Version control labels (e.g., `LB_V1`, `LB_V2`).

## 4. Model Risks
- **Overfitting:** 92% Win-rate in Train, 48% in Live. **Fix:** Walk-Forward Optimization, `TimeSeriesSplit`, strict Optuna Constraints, prioritize Simplicity.
- **Hyperparameter Over-Optimization:** Optuna memorizing data over 1000 trials. **Fix:** Select based on PF Mean/Std Dev across folds, not just the absolute "Best Trial".
- **Regime Dependency:** Model works in Trend, bleeds in Range. **Fix:** Implement a Market Regime Detector and Strategy Router.

## 5. ONNX Pipeline Risks
- **Wrong Feature Order:** Train order (RSI, ADX, ATR) != Inference order (ADX, RSI, ATR). **Fix:** Use `feature_order.json` to enforce strict ordering before prediction.
- **Version Mismatch:** Exported ONNX v17, but MT5 supports v15. **Fix:** Integrate an ONNX Compatibility Test in the CI/CD pipeline.

## 6. MQL5 Execution Risks
- **Invalid Features (NaN/Inf):** Division by zero in real-time. **Fix:** Call `MathIsValidNumber()` on EVERY feature before passing to the ONNX model.
- **Indicator Handle Failures:** `iATR()` returns `INVALID_HANDLE`. **Fix:** Implement robust Fallbacks (e.g., `NO TRADE` condition).

## 7. Market Execution Risks
- **Spread Explosion:** Spread widens from 1 to 30 during news. **Fix:** Strict Spread Filter.
- **Slippage:** Signal at 1.1000, filled at 1.1015. **Fix:** Enforce Max Slippage limits and Market Condition Filters.
- **Partial Fills:** Orders not fully executed. **Fix:** State machine to track order states and handle partial fill logic appropriately.