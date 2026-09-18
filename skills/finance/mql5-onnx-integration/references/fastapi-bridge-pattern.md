# FastAPI Bridge Pattern for MT5

**Context:** MT5 (MQL5) has limitations when fetching alternative data (Macroeconomics, ForexFactory News Calendar) directly via `WebRequest` due to Broker Timezone mismatches, Rate Limits (IP bans), and rigid synchronous execution.

**The Pattern:**
Decouple the data fetching from MT5 by creating a lightweight Python FastAPI Gateway.
1. **Python FastAPI (Gateway):** Runs on the VPS, fetches data (e.g., Yahoo Finance, ForexFactory XML) infrequently to avoid rate limits, and caches the result. It handles complex logic like timezone normalization (converting EST to UTC) and heavy macro calculations.
2. **MQL5 EA (Client):** Uses `WebRequest()` to call the local FastAPI endpoint (`http://127.0.0.1:8000/data`) before executing a trade. It parses the JSON response using the `JAson.mqh` library.

**Dynamic JSON Configuration:**
Never hardcode `buy_threshold`, `sell_threshold`, or `num_features` in MQL5 when integrating with ML pipelines. Export a `model_config.json` and `feature_order.json` alongside the `.onnx` file during Python training. The MQL5 EA should read these JSONs at `OnInit()` to dynamically allocate array sizes (`ArrayResize(features, num_features)`) and apply signal thresholds. This prevents fatal feature mismatches when the Python model is updated.