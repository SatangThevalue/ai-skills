---
name: personal-finance-and-investment
description: Guide for personal finance management, asset allocation, and algorithmic trading portfolio risk control.
version: 1.0.0
author: Tonthong
license: MIT
metadata:
  hermes:
    tags: [finance, investment, trading, asset-allocation]
    related_skills: [thai-finance-legal-guide, stocks, excel-author, 3-statement-model, comps-analysis, dcf-model, lbo-model, merger-model, evm, solana, hyperliquid]
---

# Personal Finance and Investment Guide

## Overview
This skill provides a structured framework for managing personal finances, tracking progress toward a 150,000 THB/month income goal, allocating assets, and maintaining strict risk control in algorithmic trading (Forex XAUUSD, Crypto, Stocks).

## When to Use
- When reviewing financial goals and monthly savings/income.
- When designing or adjusting asset allocation strategies.
- When formulating risk management parameters for automated trading bots (MQL5/Python).
- When assessing compliance with Thai financial regulations (referencing `thai-finance-legal-guide`).

## Financial Management Strategy

### 1. Income & Cash Flow Tracking
- **Target Tracking:** Actively track progress toward the 150,000 THB/month threshold. Categorize income into Active (freelance, job) and Passive/Systematic (trading systems, content monetization, digital products like `soundbridgehub`).
- **Emergency Fund:** Maintain 6-12 months of fixed living expenses in high-yield savings accounts or liquid assets before scaling up high-risk investments.
- **Budgeting (50/30/20 Rule):**
  - **50% Needs:** Living expenses, rent, utilities.
  - **30% Wants:** Dining out (garlic fried chicken thigh!), entertainment.
  - **20% Savings & Investment:** Transferred immediately upon income receipt.

### 2. Asset Allocation Framework
- **Core Portfolio (Low-to-Medium Risk):**
  - Mutual funds (passive index tracking).
  - Dividend-paying stocks.
  - Government bonds or fixed income.
- **Satellite Portfolio (High Risk / Active):**
  - Automated trading systems (Forex XAUUSD, BTC, SET stocks).
  - Individual growth stocks.
  - Crypto asset holdings.
  - Max allocation for the Satellite Portfolio: 30% of total investable assets.
  - *Tooling & Execution:* Utilize the `stocks` skill (`python3 ~/.hermes/skills/finance/stocks/scripts/stocks_client.py`) for global quotes, historical OHLCV data, crypto, and commodity prices (e.g. `GC=F` for gold). Use `evm` and `solana` for on-chain asset tracking. Use `hyperliquid` for perpetual and derivatives market data.
  - *Quantitative Analysis:* For equity valuation and corporate finance tasks, leverage `dcf-model`, `comps-analysis`, `3-statement-model`, `lbo-model`, and `merger-model` in tandem with `excel-author` to produce structured Excel artifacts.

### 3. Automated Trading Risk Control Rules
- **Capital Preservation:** Never risk more than 1-2% of account equity on a single trade.
- **Portfolio Correlation:** Ensure trading systems running on different assets (e.g., XAUUSD vs. BTC) do not have highly correlated entry signals.
- **Drawdown Limiters:** Implement hard daily and weekly drawdown limits in code (e.g., max 5% daily drawdown) that trigger automatic script shutdown/cooldown.
- **System Backtesting:** Ensure all MQL5/Python trading bots have completed walk-forward analysis and multi-year backtests (including 2020-2026 data) before going live.

## Common Pitfalls
1. **Overleveraging in Algorithmic Trading:** Fusing trading system development with emotional manual overrides. Maintain a strict separation.
2. **Ignoring Tax Implications:** Check tax brackets and allowances (e.g., SSF/RMF/ThaiESG, trading tax rules in Thailand).
3. **Neglecting Cash Flow for System Expenses:** Keep infrastructure costs (VPS for trading bots, hosting, database) accounted for separately from personal savings.

## Verification Checklist
- [ ] Financial goals are reviewed monthly.
- [ ] Satellite portfolio risk parameters (drawdown, leverage) are checked and verified.
- [ ] Tax allowances and deductions are reviewed quarterly.
- [ ] Automated trading logs are monitored for execution anomalies.
