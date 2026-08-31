---
name: mt5-farmed-hedge-yield-strategy
description: Analysis and reverse-engineering of the MQL5 'Farmed Hedge Yield II' market-neutral hedging strategy, adapted for survival-first principles.
tags: [trading, mt5, forex, hedging, market-neutral, mql5, algorithmic-trading]
version: 1.0.0
---

# Farmed Hedge Yield II Strategy Analysis

This skill documents the mechanics, risk profile, and reverse-engineered logic of the MQL5 signal "Farmed Hedge Yield II" by Tanapisit Tepawarapruek, with adaptations for survival-first algorithmic trading.

## 1. Core Concept & Logic
- **Framework**: 100% Algorithmic, Market-Neutral (Statistical Arbitrage / Correlation Hedging).
- **Directional Split**: Perfectly balanced (49.97% Long / 50.03% Short), reducing directional market risk.
- **Asset Class**: Forex Cross Pairs with mean-reverting characteristics (AUDCAD, GBPAUD, EURAUD, EURJPY, AUDJPY).
- **Frequency**: High (Avg 90 trades/week, 95% time in market).
- **Holding Period**: Intraday to Swing (Avg 24 hours).
- **Win Rate**: ~55%, Profit Factor: 1.39.

## 2. Reverse-Engineered Mechanics
Based on the trading statistics, the strategy likely employs:
1. **Correlation Hedging (Pairs Trading)**: Trading historically correlated cross pairs against each other to capture mean reversion spreads.
2. **Bi-directional Grid / Mean Reversion**: Opening both long and short positions to capture ranging volatility, relying heavily on the mean-reverting nature of CAD, AUD, and GBP cross pairs.
3. **Strict Lot Sizing**: The author dictates a strict linear sizing rule of **$400–$500 per 0.01 lot**.

## 3. Vulnerabilities & Risk Profile (Warning)
- **Severe Drawdown (55.49%)**: Despite the "market-neutral" claim, the floating drawdown is high. This implies the strategy holds onto un-hedged floating losses until the market reverts (a common flaw in standard Grid or pure correlation arbitrage when structural breaks occur).
- **Margin Pressure**: Max deposit load hit **46.50%**, indicating that during deep drawdown phases, the system uses significant margin to maintain or average into positions.
- **Platform Flags**: MQL5 frequently flagged this signal for "High drawdown (30%-39%)" and "Too much growth (high risk)", signifying periods lacking hard risk limitation.

## 4. Adaptation for 'Survival-First' Philosophy
Given your preference for **Drawdown protection and Survival-first algorithms**, the base mechanics of this signal are too risky. However, the conceptual framework can be upgraded:

### A. Implementing Hard Equity Stops
- The original system lacks risk limitation on the portfolio level.
- **Upgrade**: Implement a global `Portfolio Equity Stop` at 15-20%. If the market-neutral spread diverges beyond this, cut all positions. Survival > Yield.

### B. Dynamic Position Sizing (ATR-based)
- The original uses static $400/0.01 lot.
- **Upgrade**: Size the hedge dynamically based on the volatility (ATR) of the paired assets. If AUDCAD is highly volatile, its lot size should dynamically shrink compared to a less volatile pair in the hedge basket.

### C. Cointegration over Correlation
- **Upgrade**: Do not rely purely on standard correlation (which breaks down during news). Use Statistical Cointegration (e.g., Engle-Granger test in Python) to ensure the spread between the selected cross pairs is stationary and highly probable to revert.

### D. Time-of-Day / News Filtering
- **Upgrade**: Cross pairs can suffer from massive spread widening during major central bank announcements. Implement a filter to flatten the portfolio before high-impact news.