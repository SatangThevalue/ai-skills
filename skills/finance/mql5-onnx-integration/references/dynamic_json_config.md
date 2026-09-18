# Dynamic JSON Configuration for ONNX EAs

Instead of hardcoding `#define NUM_FEATURES` and signal thresholds in MQL5, dynamically load them from JSON files generated during the Python ONNX export phase. This prevents feature-mismatch crashes when model versions change.

## Implementation Details
1. **Python Export**: Alongside `model.onnx`, export `feature_order.json` (array of feature names) and `model_config.json` (buy/sell thresholds, risk parameters).
2. **MQL5 Loading (using JAson.mqh)**:
   - Read `feature_order.json` to count the keys, then use `ArrayResize(features, num_features)`.
   - Read `model_config.json` to set `buy_threshold` and `sell_threshold`.
3. **Benefits**: The EA becomes a standalone execution engine. You can upgrade models by simply replacing the `.onnx` and `.json` files in `MQL5/Files/` without recompiling the `.mq5` code.