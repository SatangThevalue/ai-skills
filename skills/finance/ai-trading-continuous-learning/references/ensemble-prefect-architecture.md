# Production Quant Trading Architecture (Hybrid + Prefect)

## 1. The 5-Model Ensemble Scoring
Instead of relying on a single LightGBM model, use a weighted ensemble combining multiple dimensions. Crucially, apply a **Market Regime Multiplier** as a final filter to slash scores during false setups:
- **Price Action**: Support/Resistance, Breakouts.
- **Indicators**: RSI, MACD, EMA.
- **Volume/Micro-structure**: Order book pressure, tick-level spikes.
- **Machine Learning**: Probability forecasting (LightGBM/ONNX).
- **Market Regime (The Filter)**: Uses HMM/ATR to detect Trend vs Range. If the regime contradicts the strategy (e.g., breakout strategy in a ranging market), slash the final score (e.g., x0.5).

## 2. Hybrid Data Ingestion & Concurrency
When scaling to 100+ assets (e.g., SET100), querying API data for full historical candles on every tick exceeds rate limits.
- **Hybrid Strategy**: Query historical candles (T-100 to T-1) from a local PostgreSQL database, and only query the **Live Tick (T-0)** from the Broker API. Concatenate them in memory.
- **Prefect Concurrency**: Do not use `asyncio.gather` for blocking broker APIs. Use Prefect's `ThreadPoolTaskRunner` to batch requests dynamically.
```python
from prefect import flow, task
from prefect.task_runners import ThreadPoolTaskRunner

@task
def process_asset(asset: str):
    pass # Fetch hybrid data, score, and execute

@flow(task_runner=ThreadPoolTaskRunner(max_workers=5)) # Limits to 5 concurrent API requests
def scan_market(universe):
    futures = [process_asset.submit(asset["name"]) for asset in universe if is_market_open(asset)]
    for f in futures: f.result()
```

## 3. Position Sizing with Slippage Buffer
Always include a slippage/spread buffer in the denominator when calculating risk-based position size. This prevents losses from exceeding the rigid 1% threshold during rapid market orders:
```python
def calculate_position_size(capital: float, entry: float, sl: float, risk_pct: float = 0.01) -> float:
    risk_amount = capital * risk_pct
    risk_per_share = abs(entry - sl)
    
    # Pad risk with estimated slippage (e.g. +1 tick)
    adjusted_risk_per_share = risk_per_share + 0.25 
    
    size = risk_amount / adjusted_risk_per_share
    return round(size, 2)
```

## 4. Telemetry and Optuna Registry
Do not hardcode model weights. Read them from a database `model_registry` to allow live-updating without restarting the orchestrator. Save every evaluated signal above a certain threshold (e.g., >=75%) into a `paper_trade_log` database table, capturing the raw sub-scores (PA, ML, IND, VOL) before the regime multiplier. This telemetry data is required for future Optuna optimization passes.