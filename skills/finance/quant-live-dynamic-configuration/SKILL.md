---
name: quant-live-dynamic-configuration
description: "Architecture for dynamically loading Python-generated JSON configs (Thresholds, Features) directly into MQL5 EAs."
version: 0.1.0
metadata.hermes.tags: [MQL5, ONNX, Architecture, Config]
---

# Dynamic Configuration Loading for MQL5

To eliminate human error during model updates, MQL5 Expert Advisors should dynamically load model thresholds, feature counts, and risk parameters directly from JSON configuration files exported by the Python training pipeline.

## When to Use
- When deploying new ONNX model versions to MT5.
- When the number of features (`NUM_FEATURES`) changes between model iterations.
- When signal thresholds (`buy_threshold`, `sell_threshold`) are optimized and changed in Python.

## Prerequisites
- The `JAson.mqh` library installed in `MQL5/Include/`.
- Exported JSON configs (`model_config.json`, `feature_order.json`) alongside the `.onnx` file.

## Procedure

1. **Python Export Phase:** Ensure the training pipeline exports configurations along with the `.onnx` model.
   ```python
   # Example output: EURUSD_model_config_v1.0.json
   {
     "buy_threshold": 0.60,
     "sell_threshold": 0.40,
     "atr_sl": 1.5,
     "atr_tp": 3.0
   }
   ```

2. **MQL5 EA Definition:** Remove hardcoded constants like `#define NUM_FEATURES`. Declare dynamic variables:
   ```mql5
   #include <JAson.mqh> 
   
   int num_features = 0;
   double buy_threshold = 0.5;
   double sell_threshold = 0.5;
   ```

3. **MQL5 Loading Logic (OnInit):** Parse the JSON files to configure the EA.
   ```mql5
   CJAVal config;
   string config_data = ReadFile(InpConfigPath);
   if(config.Deserialize(config_data)) {
      buy_threshold = config["buy_threshold"].ToDbl();
      sell_threshold = config["sell_threshold"].ToDbl();
   }
   
   CJAVal feature_order;
   string feature_data = ReadFile(InpFeaturePath);
   if(feature_order.Deserialize(feature_data)) {
      num_features = feature_order["features"].Size();
   }
   ```

4. **Dynamic Array Allocation (OnTick):** Resize the feature array based on the loaded count before running ONNX inference.
   ```mql5
   float features[];
   ArrayResize(features, num_features);
   ```

## Pitfalls
- **Missing JSON Library:** MT5 cannot parse JSON natively without external libraries like `JAson.mqh`.
- **Path Issues:** If the EA cannot find the JSON files in `MQL5/Files/`, it will fail to load constraints and must halt execution (`INIT_FAILED`).
- **Data Types:** Ensure the Python export saves numbers clearly so `JAson.mqh` can parse them via `.ToDbl()`.

## Verification
In the MT5 Experts Log, look for the dynamic loading confirmation:
`Loaded Feature Order | Detected 38 Features.`
`Loaded Config | Buy: 0.60 | Sell: 0.40 | SL: 1.5x | TP: 3.0x`
EOF
