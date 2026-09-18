# MT5 ONNX Basics (Inference Engine)

MT5 natively supports loading ONNX (Open Neural Network Exchange) models directly inside EAs, Indicators, or Scripts. This eliminates the need for a running Python backend during live trading, significantly reducing latency.

## Key Concepts
- **Inference Only:** MT5 does NOT train models. Training must be done in Python (PyTorch, TensorFlow, Scikit-Learn, LightGBM, XGBoost) and exported to `.onnx`.
- **Core API Functions:**
  - `OnnxCreate()` / `OnnxCreateFromBuffer()`: Load the model from file or buffer.
  - `OnnxSetInputShape()` / `OnnxSetOutputShape()`: Define tensor shapes (required before running).
  - `OnnxRun()`: Execute the prediction.
  - `OnnxRelease()`: Free memory and resources.
- **Common Use Cases:** 
  1. Price Prediction (Up/Down in next N hours).
  2. Signal Classification (Buy/Sell/Hold based on technical indicators).
  3. Risk Management (Dynamic Lot Sizing/SL/TP based on volatility).
  4. Market Regime Detection (Trend vs Range).
- **Advantages over Sockets:** Extremely low latency, fully supports Backtesting in Strategy Tester, easy VPS deployment (just deploy `.ex5` and `.onnx`), and supports hardware acceleration (CUDA GPU via flags).
- **Critical Limitations:** 
  - Massive models (LLMs, large Transformers) consume too much RAM/CPU and may crash the MT5 terminal. Prefer LightGBM, XGBoost, or small MLPs/CNNs.
  - Preprocessing in MQL5 **MUST exactly match** the Python training preprocessing (e.g., Z-score standardization). If normalization differs, outputs will be wildly incorrect.