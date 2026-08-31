---
name: forex-profitability-framework
description: "กรอบความคิดและหลักการเชิงปริมาณ (Quant) เพื่อทำกำไรอย่างยั่งยืนในตลาด Forex"
version: 0.1.0
metadata:
  hermes:
    tags: [Forex, Trading, Risk Management, Quantitative, Strategy]
---

# Forex Profitability Framework

This skill outlines the four core pillars of sustainable profitability in the Forex market from a Quantitative/Algorithmic trading perspective. It shifts the focus from "predicting direction" to "managing probability and survival." It does NOT provide a holy-grail trading script, but rather the business logic and risk parameters required to build a resilient Expert Advisor (EA) or Python trading bot.

## When to Use

- "แล่วเราจะทำกำไรจากตลาด forex ได้อย่างไร"
- "ช่วยแนะนำวิธีบริหารความเสี่ยง Forex"
- When evaluating if a proposed trading algorithm has a statistical edge.
- When designing the Money Management module of a new EA.

## Quick Reference

- **Rule 1: Risk per Trade** <= 1% to 2% of total equity.
- **Rule 2: Risk:Reward (R:R)** >= 1:1.5 to 1:2.
- **Trend Filter:** ADX > 25 (Trend Following), ADX < 20 (Mean Reversion).
- **Automation:** Execute via MQL5 EA or Python to eliminate human psychology.

## Procedure (The 4 Pillars of Forex Profitability)

### 1. Statistical Edge (ความได้เปรียบทางสถิติ)
A trading system must be proven mathematically, not emotionally.
- **Backtesting:** Code the strategy in Python or MQL5 and run it over 3-5 years of historical data to determine the Win Rate and Maximum Drawdown.
- **Contextual Strategies:**
  - *Trend Following:* Use when ADX > 25. Ride the momentum (e.g., EMA crossovers).
  - *Mean Reversion:* Use when ADX < 20. Trade the ranges (e.g., Bollinger Bands limits).
  - *Statistical Arbitrage (Pair Trading):* Exploit pricing inefficiencies between highly correlated assets.

### 2. Money & Risk Management (การบริหารเงินทุน)
The most critical pillar. Focus on survival (what you lose), not just profit (what you win).
- **The 1-2% Rule:** Position sizing must ensure that a hit Stop Loss (SL) deducts no more than 1% to 2% of the total account equity. 
  - *Formula:* `Lot Size = (Account Equity * Risk%) / (Stop Loss in Points * Point Value)`
- **Risk to Reward Ratio (R:R):** Always target an R:R of at least 1:1.5 or 1:2. With a 1:2 R:R, a system only needs a 40% win rate to be profitable.

### 3. Context & Filters (รู้ว่าตอนไหนไม่ควรเทรด)
A good algorithm rejects trades more often than it takes them.
- **News/Event Filter:** Pause the bot during major macroeconomic announcements (e.g., Non-Farm Payrolls, FOMC). Spreads widen and slippage destroys SL/TP calculations. (See the `mql5-acd-cs-architecture` skill for ATR-based shock detection).
- **Liquidity Filter:** Avoid trading during the rollover period (New York close / Asian open) when spreads are artificially wide and price action is random.

### 4. Automation (ตัดอารมณ์มนุษย์ด้วย EA/Bot)
Human psychology (fear and greed) destroys statistical edges.
- **Fear:** Holding losing positions ("Let Loss Run") or averaging down.
- **Greed:** Closing winning positions too early ("Cut Profit Short").
- **Solution:** Translate the edge, risk management, and filters into a Python script (via `MetaTrader5` library) or an MQL5 Expert Advisor. Let the machine execute 100% of the strategy.

## Pitfalls

- **Over-optimization (Curve Fitting):** Tweak parameters until backtests look perfect, only for the bot to fail immediately in forward testing (live markets). Always use Out-of-Sample testing.
- **Martingale / Grid Systems:** Strategies that double down on losing trades will eventually blow up the account during a strong, unidirectional trend. 
- **Ignoring Spread & Commission:** Backtesting without accounting for real-world spreads and broker commissions will drastically overstate potential profits, especially on lower timeframes (M1, M5).

## Verification

Review the proposed algorithmic logic (e.g., a Python script). It passes verification if it contains explicit functions for calculating Position Size based on a strict % Risk, and includes filters that prevent execution during low liquidity or high volatility shocks.