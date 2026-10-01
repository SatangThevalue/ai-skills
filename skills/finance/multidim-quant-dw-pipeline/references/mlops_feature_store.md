# MLOps Telemetry & Triple Barrier Feature Store

This document details the schema, lifecycle, and extraction methods for collecting training data and labels during live or simulated DW trading.

## Schema Architecture: `finance_db.ml_training_dataset`

Every opened paper or live position initiates a record in this table with status `ACTIVE`. Upon trade conclusion, it is enriched with excursion metrics, duration, and target labels, transitioning to `COMPLETED`.

| Column | Type | Description |
| :--- | :--- | :--- |
| `id` | SERIAL PRIMARY KEY | Unique dataset sample index |
| `timestamp` | TIMESTAMP | Signal timestamp at order entry |
| `asset_name` | VARCHAR(50) | Underlying stock symbol (e.g. `PTT`) |
| `dw_symbol` | VARCHAR(50) | DW contract symbol (e.g. `PTT01C2608A`) |
| `features` | JSONB | Flattened matrix of all fundamental, technical, and volume metrics |
| `market_regime` | VARCHAR(20) | Detected regime state (`SUPER_BULL`, `BULL`, `REBOUND`, `BEARISH`) |
| `model_version` | VARCHAR(50) | Active scoring model tag (e.g. `v1.0_multidim`) |
| `predicted_score` | NUMERIC | Composite confidence score at entry (0–100) |
| `target_entry` | NUMERIC | Intended entry price on DW |
| `actual_fill` | NUMERIC | Executed fill price from broker |
| `peak_price` | NUMERIC | Highest DW price observed while holding |
| `trough_price` | NUMERIC | Lowest DW price observed while holding |
| `mfe_pct` | NUMERIC | Maximum Favorable Excursion: `((peak - entry) / entry) * 100` |
| `mae_pct` | NUMERIC | Maximum Adverse Excursion: `((entry - trough) / entry) * 100` |
| `triple_barrier_label` | INT | `+1` (Take Profit hit), `-1` (Stop Loss hit), `0` (Timeout / Breakdown) |
| `realized_pnl` | NUMERIC | Net realized profit or loss in THB |
| `holding_duration_secs` | INT | Trade lifespan from entry to exit in seconds |
| `loss_cause` | VARCHAR(50) | Attribution tag for losing trades (e.g. `INDICATOR_BREAKDOWN`) |
| `status` | VARCHAR(20) | `ACTIVE` during trade, `COMPLETED` when closed and labeled |

---

## Metric Diagnostics

1. **Maximum Adverse Excursion (MAE):**
   - Measures downside volatility tolerated before a win or loss.
   - High MAE on winning trades indicates stop losses are appropriately placed.
   - Low MAE on losing trades reveals false breakouts where price immediately collapsed.

2. **Maximum Favorable Excursion (MFE):**
   - Measures maximum unrealized profit attained before closing.
   - If MFE significantly outpaces final realized return, take-profit thresholds or trailing stops are lagging.

3. **Triple Barrier Labeling (de Prado):**
   - Standardizes time-series returns into discrete classification targets for supervised machine learning:
     - **Upper Barrier:** $+2.5 \times \text{ATR}$ (or DW equivalent) $\rightarrow$ `+1`
     - **Lower Barrier:** $-1.5 \times \text{ATR}$ (or 1% portfolio risk stop) $\rightarrow$ `-1`
     - **Vertical Barrier:** Technical breakdown or max holding window $\rightarrow$ `0`

---

## Python Dataset Export for LightGBM / Optuna

To convert the PostgreSQL database records directly into feature ($X$) and target ($y$) training sets:

```python
import psycopg2
import pandas as pd

def load_training_dataset(db_params: dict) -> tuple[pd.DataFrame, pd.Series]:
    conn = psycopg2.connect(**db_params)
    cur = conn.cursor()
    cur.execute("""
        SELECT features, triple_barrier_label
        FROM finance_db.ml_training_dataset
        WHERE status = 'COMPLETED';
    """)
    rows = cur.fetchall()
    conn.close()

    if not rows:
        return pd.DataFrame(), pd.Series()

    features_list = [r[0] for r in rows]
    labels_list = [r[1] for r in rows]

    X = pd.json_normalize(features_list)
    y = pd.Series(labels_list, name="target")
    return X, y
```
