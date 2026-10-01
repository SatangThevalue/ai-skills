# Two-Way DW Trading: Mathematical & Execution Architecture

This document defines the mathematical models, risk formulas, and execution rules for trading both Call and Put Derivative Warrants (DW) on the Stock Exchange of Thailand (SET).

---

## 1. Core Philosophy: Asymmetric Risk on Both Sides

In traditional equity trading, going short requires borrowing shares (SBL) or trading TFEX futures, which exposes the account to unlimited loss potential or margin calls.
By contrast, trading **Call and Put DWs** provides directional asymmetry:

| Strategy | Market Expectation | Instrument | Underlying Movement | DW Price Movement | Max Downside Risk |
| :--- | :--- | :--- | :---: | :---: | :--- |
| **Bullish Trend** | Price Up | **Buy CALL DW** | $P_{\text{underlying}} \uparrow$ | $P_{\text{DW}} \uparrow$ (Gain) | Bounded to Premium Paid |
| **Bearish Breakdown** | Price Down | **Buy PUT DW** | $P_{\text{underlying}} \downarrow$ | $P_{\text{DW}} \uparrow$ (Gain) | Bounded to Premium Paid |

> **Key Rule:** The quantitative engine ALWAYS acts as a **Buyer** (Long Call or Long Put). It never writes (sells to open) warrants. Thus, catastrophic risk is mathematically capped.

---

## 2. Signal Generation & Directional Thresholds

### Bullish Confluence (Routes to Call DW)
*   Price > EMA20 > EMA50 > EMA200
*   RSI(14) between 50.0 and 65.0 (Healthy trend momentum)
*   MACD > Signal Line and Histogram > 0
*   Volume Ratio vs 20-day SMA $\ge 1.3\times$ on green bars
*   Trigger: `Final Score >= 70.0%` $\rightarrow$ Signal `BUY` or `STRONG_BUY`

### Bearish Breakdown (Routes to Put DW)
*   Price < EMA20 < EMA50 (or breaking down below major support)
*   RSI(14) $\le 40.0$ (Strong downward velocity)
*   MACD < Signal Line and Histogram < 0
*   Volume Ratio vs 20-day SMA $\ge 1.3\times$ on red bars (Distribution)
*   Trigger: `Final Score >= 70.0%` $\rightarrow$ Signal `SELL` or `STRONG_SELL`

---

## 3. Mathematical Mapping: Underlying to DW

Let:
*   $P_0$ = Underlying Entry Price
*   $SL_u$ = Underlying Stop Loss Price
*   $TP_u$ = Underlying Take Profit Price
*   $DW_0$ = DW Base Entry Price
*   $G$ = Effective Gearing of the DW
*   $T_u$ = Underlying Tick Size (per SET rules)
*   $T_{dw}$ = DW Tick Size (0.01 THB for prices $< 2.00$ THB)

### Call DW Mapping ($SL_u < P_0 < TP_u$)
*   Underlying Loss: $\Delta P_{sl} = P_0 - SL_u$
*   Underlying Gain: $\Delta P_{tp} = TP_u - P_0$
*   DW Stop Loss:
    $$SL_{dw} = \max\left(0.01, DW_0 \cdot \left[1 - \left(\frac{\Delta P_{sl}}{P_0} \cdot G\right)\right]\right)$$
*   DW Take Profit:
    $$TP_{dw} = DW_0 \cdot \left[1 + \left(\frac{\Delta P_{tp}}{P_0} \cdot G\right)\right]$$

### Put DW Mapping ($TP_u < P_0 < SL_u$)
*   Underlying Loss (Adverse Move Up): $\Delta P_{sl} = SL_u - P_0$
*   Underlying Gain (Favorable Drop Down): $\Delta P_{tp} = P_0 - TP_u$
*   DW Stop Loss:
    $$SL_{dw} = \max\left(0.01, DW_0 \cdot \left[1 - \left(\frac{\Delta P_{sl}}{P_0} \cdot G\right)\right]\right)$$
*   DW Take Profit:
    $$TP_{dw} = DW_0 \cdot \left[1 + \left(\frac{\Delta P_{tp}}{P_0} \cdot G\right)\right]$$

> **Crucial Invariant:** For both Call and Put DWs, because we are the **buyer**, $SL_{dw} < DW_0 < TP_{dw}$ holds true at all times.

---

## 4. Money Management: 1.0% Fixed Risk Sizing

For an account capital $C$ (e.g. 50,000 THB):
1.  **Risk Budget:**
    $$R_{\text{budget}} = C \times 0.01 = 500\text{ THB}$$
2.  **Risk per Share (including 1-tick slippage buffer):**
    $$R_{\text{share}} = (DW_0 - SL_{dw}) + 0.01\text{ THB}$$
3.  **Volume (Board Lot rounded to 100 shares):**
    $$V = \left\lfloor \frac{R_{\text{budget}}}{R_{\text{share}}} \cdot \frac{1}{100} \right\rfloor \times 100$$
4.  **Portfolio Heat Constraint:**
    $$\text{Total Outlay} = V \cdot DW_0 \le C \times 0.25$$
    If $V \cdot DW_0 > C \times 0.25$, reduce volume so total capital committed to a single warrant never exceeds 25%.
5.  **Concurrent Position Cap:**
    Maximum 3 open positions at any time (Total portfolio risk $\le 3\%$).
