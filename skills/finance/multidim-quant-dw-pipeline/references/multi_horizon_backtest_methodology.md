# Multi-Horizon Backtesting & Capital Preservation Methodology

Framework for validating quantitative DW trading pipelines across multiple time horizons (1 to 90 days) with strict Money Management (1% capital risk).

---

## 1. Multi-Horizon Testing Matrix (1 to 90 Days)

Backtesting over multiple rolling horizons evaluates consistency across market regimes:
- **Ultra-short (1–5 Days):** Tests micro-momentum and immediate reaction to volume surges.
- **Short (7–10 Days):** Tests swing continuation and resistance retests.
- **Medium (20–40 Days):** Captures multi-week sector rotations and earnings cycles.
- **Long (50–90 Days):** Exposes cumulative Time Decay (Theta drag) on DW contracts and tests regime filter endurance.

---

## 2. Quantitative Verification Metrics

| Metric | Target | Formula / Logic |
| :--- | :---: | :--- |
| **Max Single Loss** | $\le 1.0\%$ (500 THB) | Hard Stop Loss: $\text{Loss} = (\text{Entry} - \text{SL}) \times \text{Volume}$ |
| **Max Drawdown (MDD)** | $< 10.0\%$ | $\max(0, (\text{Peak Equity} - \text{Current Equity}) / \text{Capital})$ |
| **Profit Factor** | $\ge 1.5$ | $\sum \text{Gross Profits} / |\sum \text{Gross Losses}|$ |
| **Expected Value (EV)** | $> 0$ | $(\text{Win Rate} \times \text{Avg Win}) - (\text{Loss Rate} \times \text{Avg Loss})$ |
| **MM Compliance** | 100% | Verified if every loss $\le 500$ THB and volume $\le 25\%$ capital outlay |

---

## 3. Empirical Insights from SET DW Testing

1. **The Call-Only Drawdown Trap:**
   - In consolidating or downward-trending markets, long-only Call DW strategies experience persistent theta decay.
   - **Remedy:** The Market Regime filter must aggressively downgrade signals (e.g. $0.70\times$ multiplier) during non-bullish regimes, forcing the pipeline into **Silent Mode (100% Cash)** to preserve capital.

2. **MFE / MAE Diagnostics:**
   - **MAE < 5%:** Confirms breakouts were clean and stop losses were not triggered by market noise.
   - **MFE significantly higher than realized return:** Indicates profit-taking was too late or trailing stops failed to lock in the peak.

3. **Zero-Token Pipeline Performance:**
   - Pre-caching fundamental metrics (P/E, ROE) in PostgreSQL and executing parallel technical/volume scans via 4-worker thread pools achieves $\approx 0.5$–$0.7$ seconds per ticker, completely eliminating LLM token costs during routine scans.
