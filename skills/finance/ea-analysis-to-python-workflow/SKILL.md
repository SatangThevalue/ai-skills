---
name: ea-analysis-to-python-workflow
description: "Reverse-engineer commercial MT5 EAs into Python quantitative strategies."
version: 0.1.0
metadata:
  hermes:
    tags: [MT5, Python, EA, Reverse Engineering, Quantitative]
---

# EA Analysis to Python Workflow

Extracts trading logic, core indicators, and risk management parameters from commercial Expert Advisor (EA) descriptions (like MQL5 market listings) and translates them into Python-based mathematical models. It does NOT decompile `.ex5` files; it relies on text extraction, deduction of underlying statistical concepts (e.g., mapping "Sync Rate" to Pearson Correlation), and scaffolding the architecture for a Python-to-MT5 execution loop.

## When to Use

- "ช่วยค้นหาข้อมูล และวิเคราะห์อัลกอริทึมของ [MQL5 Market URL]"
- "ต้องใช้อินดิเคเตอร์ตัวไหนบ้าง สร้างสกิลได้เลย"
- When converting a proprietary trading concept (e.g., FarmedHedge) into an open Python strategy.

## Prerequisites

- URL to the EA documentation, MQL5 market page, or YouTube review.
- Python data science stack (`pandas`, `numpy`) for strategy modeling.

## How to Run

1. Use `web_extract` on the provided EA URL.
2. Use `web_search` to find secondary sources, reviews, or forum discussions about the EA's mechanics.
3. Synthesize the commercial terms into standard quantitative terms (e.g., "Farm Index" -> Z-Score of Spread).
4. Use the `skill_manage` tool to write the logic into a reusable Python template.

## Quick Reference

- **Pair Trading (Statistical Arbitrage):** Trade diverging correlated assets.
- **Sync Rate (Correlation):** `df['Close_A'].rolling(window=N).corr(df['Close_B'])`
- **Farm Index (Z-Score):** `(Spread - Spread_Mean) / Spread_Std`
- **Mean Reversion:** Take profit when Z-Score returns to ~0.

## Procedure

1. **Extract EA Documentation**
   Use the `web_extract` tool on the target URL to capture the developer's description, recommended settings, and entry/exit conditions.
   ```python
   # Example Hermes tool call
   web_extract(urls=["https://www.mql5.com/en/market/product/162186"])
   ```

2. **Deconstruct the Logic**
   Identify the core mechanisms:
   - What triggers an entry? (e.g., Index > 200)
   - What filters the entry? (e.g., Correlation > 70%)
   - How is the exit managed? (e.g., Index returns to 50, or Stop Loss at 400)

3. **Translate to Quantitative Python**
   Map the commercial terms to standard pandas/numpy functions. Create a Python class that calculates these metrics. (Reference the `python-pair-trading-mt5` skill for the exact Pair Trading implementation).

4. **Draft the Architecture**
   Determine how the Python logic will connect to MT5. Refer to the `eamt5-python-architecture` skill to decide between Direct API Polling, REST API Microservices, or ONNX export.

## Pitfalls

- **Marketing vs Reality:** EA descriptions often use proprietary buzzwords (e.g., "Wind Gauge", "Harvest Time Bar"). You must deduce the underlying math (e.g., Momentum, Volume spikes, Z-Score) rather than trying to find a library that implements the buzzword.
- **Hidden Filters:** Commercial EAs often hide their smoothing functions or lag filters. A raw Z-score implementation in Python might generate more noise than the commercial EA.
- **Execution Latency:** Pair trading requires simultaneous execution of two legs. A direct Python `mt5.order_send` loop fires sequentially, introducing "Leg Risk" (slippage between the two orders). 

## Verification

The workflow is successful when you have produced a Python class capable of receiving two Pandas DataFrames, calculating the derived indicators (Correlation, Z-Score), and returning a definitive "BUY", "SELL", or "WAIT" signal based on the EA's documented thresholds.