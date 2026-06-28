---
name: research-backed-investing
description: Use when designing asset allocation frameworks, developing algorithmic trading strategies, or selecting investment vehicles across Stocks, Mutual Funds, Forex, and Crypto using academic research-backed methodologies.
version: 1.0.0
author: Tonthong
license: MIT
metadata:
  hermes:
    tags: [finance, research, stocks, mutual-funds, forex, crypto, trading-strategies]
    related_skills: [personal-finance-and-investment, thai-finance-legal-guide]
---

# Research-Backed Investment Strategies

## Overview
This skill consolidates key academic research papers and empirical methodologies across four major asset classes (Stocks, Mutual Funds, Forex, and Cryptocurrencies) into actionable portfolio construction and trading system rules. It bridges the gap between quantitative academic literature and live portfolio management.

## When to Use
- Designing asset allocation strategies for long-term wealth.
- Formulating factor-based stock selection algorithms.
- Developing FX systematic trading strategies (Carry Trade and Momentum).
- Optimizing cryptocurrency portfolios while managing extreme tail-risk and estimation errors.
- Triaging mutual fund selections based on fee structures and active/passive dynamics.

## 1. Stock Market (ตลาดหุ้น)

### Empirical Foundation
*   **Fama-French Three-Factor Model (1993)** & **Five-Factor Model (2015)**: Stock returns are driven by specific risk factors rather than just market risk (CAPM). The five factors are:
    1.  *Market Risk (Mkt-RF)*: Overall market premium.
    2.  *Size (SMB - Small Minus Big)*: Small-cap stocks historically outperform large-cap stocks.
    3.  *Value (HML - High Minus Low)*: Stocks with high book-to-market ratios (value stocks) outperform growth stocks.
    4.  *Profitability (RMW - Robust Minus Weak)*: Companies with robust operating profitability yield higher returns.
    5.  *Investment (CMA - Conservative Minus Aggressive)*: Companies that invest conservatively yield higher returns than those investing aggressively.
*   **Modern Portfolio Theory (MPT - Markowitz, 1952)**: Diversification minimizes portfolio variance for a target expected return.

### Implementation Guidelines
*   **Factor Tilts**: Tilt equity portfolios toward SMB (size), HML (value), and RMW (high quality) factors rather than index-weighting alone.
*   **Systematic Screening (Python/SET)**:
    *   Sort universe by EV/EBITDA or P/B (HML proxy).
    *   Filter out stocks in the bottom quartile of Return on Invested Capital (ROIC) or Operating Margin (RMW proxy).
    *   Limit exposure to companies with high capital expenditures growth (CMA proxy).

---

## 2. Mutual Funds (กองทุนรวม)

### Empirical Foundation
*   **Carhart Four-Factor Model (1997) ("On Persistence in Mutual Fund Performance")**: Demystifies mutual fund performance persistence. Key findings:
    1.  Common risk factors (including momentum/UMD) and differences in expense ratios/transaction costs explain almost all persistence in mutual fund returns.
    2.  No evidence of significant stock-picking ability among fund managers after accounting for fees.
    3.  Funds with high performance in the past year often continue to perform well due to short-term momentum, but long-term persistence (beyond 1-2 years) is non-existent.
*   **Bogle's Cost Matter Hypothesis (CMH)**: Passive low-cost index funds outperform active mutual funds over long horizons because active fees eat up compound interest.

### Implementation Guidelines
*   **Core-Satellite Selection**:
    *   **Core Portfolio**: Use low-cost index mutual funds (tracking SET50, S&P 500, or MSCI World) with expense ratios $< 0.5\%$ and tracking errors $< 0.1\%$.
    *   **Active Screening**: If selecting active mutual funds, screen out any fund in the bottom half of performance or those with expense ratios $> 1.5\%$.
    *   **Avoid "Past Winners" Trap**: Do not purchase an active fund solely because it was the top-performing fund last year; mean reversion is academically proven to degrade performance.

---

## 3. Forex Market (ตลาดแลกเปลี่ยนเงินตรา)

### Empirical Foundation
*   **Lustig, Roussanov, & Verdelhan (2011) ("Common Risk Factors in Currency Markets")**: Explains the currency carry trade premium.
    1.  Uncovered Interest Parity (UIP) systematically fails.
    2.  High interest rate currencies (investment currencies) yield positive excess returns but are highly sensitive to global market volatility risk and suffer from tail/crash risk.
    3.  Low interest rate currencies (funding currencies, e.g., JPY, USD historically) act as safe havens and appreciate during global equity market selloffs.
*   **Menkhoff, Sarno, Schmeling, & Schrimpf (2012)**: Global foreign exchange volatility is a key priced risk factor in the cross-section of currency returns.

### Implementation Guidelines
*   **Systematic Carry Trade Execution**:
    *   Long currencies in the highest interest rate quartile; Short currencies in the lowest interest rate quartile.
    *   **Risk Limiter**: Implement a global equity market volatility (VIX proxy) filter. If global volatility spikes, liquidate or hedge carry trade positions to avoid sudden crash risks (unwinding).
*   **FX Momentum / Trend-Following**:
    *   Measure 3-month to 12-month momentum on G10 currency pairs.
    *   Trade in the direction of the momentum, but adjust position size inversely to currency-specific historical volatility (volatility sizing).

---

## 4. Cryptocurrencies (คริปโตเคอเรนซี)

### Empirical Foundation
*   **Platanakis & Urquhart (2019) ("Portfolio management with cryptocurrencies: The role of estimation risk")**:
    1.  Standard Mean-Variance Optimization (MPT) performs poorly with cryptocurrencies due to estimation risk (highly volatile returns lead to unstable weights).
    2.  The **Black-Litterman model** and portfolio models with **Variance-Based Constraints (VBCs)** significantly outperform standard MPT out-of-sample.
    3.  Downside risk measures (e.g., maximizing the **Sortino Ratio** rather than Sharpe Ratio) are vital because cryptocurrency return distributions are highly non-normal (fat-tailed, high kurtosis, negatively skewed during crashes).

### Implementation Guidelines
*   **Portfolio Construction**:
    *   Avoid classic Mean-Variance Optimization for portfolios containing crypto assets.
    *   Use **Black-Litterman** where "market equilibrium" is the starting point, and adjust using quantitative views (e.g., onchain metrics, network growth).
    *   Set maximum exposure constraints (e.g., max 5% of total portfolio to crypto) to mitigate estimation risk.
*   **Risk Metric Focus**:
    *   Optimize parameters targeting the **Sortino Ratio** (using downside deviation) or **Conditional Value at Risk (CVaR)** instead of standard volatility (Standard Deviation).

---

## Common Pitfalls
1.  **Overestimating Factor Persistence**: Assuming historical factor premiums (like SMB or Value) will always outpace the market in the short term. Prepare for decade-long factor underperformance.
2.  **UIP False Assumptions**: Relying on economic theory that exchange rates will adjust to offset interest differentials; they do not in the short-to-medium term.
3.  **Applying Normal Distribution to Crypto**: Assuming standard deviations represent true risk parameters for BTC/ETH. Always model tail risk and maximum drawdown constraints.
4.  **Transaction Costs Ignore**: Over-trading momentum strategies in Forex or small-cap stocks where bid-ask spreads and swap rates erode all alpha.

## Verification Checklist
- [ ] Equity factor screening includes Value (P/B, P/E), Quality (ROIC/margin), and Size limits.
- [ ] Active mutual funds checked against passive equivalents for total expense ratio (TER) and tracking error.
- [ ] FX trading scripts incorporate a global market volatility (VIX/global equity) emergency exit condition.
- [ ] Crypto allocation limits are hardcoded (e.g., maximum 5%) and optimized using downside risk metrics (Sortino Ratio/CVaR) instead of standard MPT.