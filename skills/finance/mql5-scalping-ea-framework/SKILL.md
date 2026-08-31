---
name: mql5-scalping-ea-framework
description: "Framework and MQL5 template for building a robust XAUUSD Scalping EA."
version: 0.1.0
metadata:
  hermes:
    tags: [MQL5, EA, MetaTrader5, Scalping, Trading]
---

# MQL5 Scalping EA Framework

This skill distills the architecture required to build a professional-grade MetaTrader 5 Expert Advisor (EA) in native MQL5 (without Python). It provides the blueprint for handling high-frequency scalping (M1 timeframe) on XAUUSD, including input parameter grouping, a live on-chart dashboard, daily profit/loss limits, and an ATR-based news filter to pause trading during extreme volatility.

## When to Use

- "ช่วยแปลงเป็น ea mt5 ไม่ใช้ python แล้ว"
- When the user needs a native MQL5 skeleton for a commercial-style trading robot.
- To implement Risk Management (Daily Limits) and News Filtering directly in MQL5.

## Prerequisites

- MetaTrader 5 Terminal installed on a Windows machine (or via Wine/Docker).
- Access to the MetaEditor IDE (press F4 in MT5) to compile `.mq5` files.

## How to Run

1. Use the `terminal` tool to write the MQL5 template to a file (e.g., `~/ScalpingEA.mq5`).
2. The user must manually copy this `.mq5` file to their MT5 `MQL5/Experts/` folder.
3. The user opens MetaEditor, compiles the file (F7), and attaches it to an XAUUSD M1 chart.

## Quick Reference

- **Input Groups:** Use `input group "Name"` to organize the settings panel visually.
- **Daily Limits:** Track `startOfDayBalance = AccountInfoDouble(ACCOUNT_BALANCE)` on a new day.
- **News Filter (ATR Spike):** `if(current_candle > ATR * 3.0) { pause_trading(); }`
- **Dashboard:** Use `Comment("...")` to render real-time text on the upper-left of the chart.

## Procedure

1. **Scaffold the Architecture**
   Create the `.mq5` file using the `terminal` tool. The structure must include standard MQL5 includes for ease of execution:
   ```cpp
   #include <Trade\Trade.mqh>
   #include <Trade\PositionInfo.mqh>
   #include <Trade\SymbolInfo.mqh>
   #include <Trade\AccountInfo.mqh>
   ```

2. **Define Input Parameters**
   Group variables so they look professional in the EA properties window:
   ```cpp
   input group "=== 2. Risk & Money Management ==="
   input double   InpDailyTargetUSD    = 50.0;
   input double   InpDailyStopLossUSD  = 150.0;
   ```

3. **Implement the Daily Reset Logic**
   Inside `OnTick()`, detect when a new day begins (Server Time) to reset the baseline balance for daily profit calculations:
   ```cpp
   static int lastDay = -1;
   MqlDateTime dt;
   TimeCurrent(dt);
   if(dt.day != lastDay) {
      startOfDayBalance = AccountInfoDouble(ACCOUNT_BALANCE);
      lastDay = dt.day;
   }
   ```

4. **Implement the ATR News Filter**
   Rather than polling external economic calendars (which can lag or break), detect "News Shocks" directly from price action. Compare the current candle's length to the ATR. If it exceeds a multiplier (e.g., 3x), pause the EA:
   ```cpp
   double currentCandleLength = symInfo.High() - symInfo.Low();
   if(currentCandleLength > (atr[0] * 3.0)) {
       pauseUntilTime = TimeCurrent() + (30 * 60); // Pause for 30 mins
   }
   ```

5. **Draw the Dashboard**
   Use `Comment()` at the end of `OnTick()` to render the current Equity, Daily P/L, and the System Status (Running or Paused).

## Pitfalls

- **Point vs Pip Calculation:** XAUUSD usually has 2 or 3 decimal places. You must normalize calculations using `_Point` and check `_Digits` to ensure SL/TP distances are calculated correctly across different brokers.
- **Comment() Overwriting:** If another indicator or script uses the `Comment()` function on the same chart, it will overwrite the EA's dashboard.
- **Backtesting M1 Data:** Testing an M1 scalper with "Open Prices Only" or "1 Minute OHLC" modeling will yield wildly inaccurate results. Users must use "Every tick based on real ticks" in the Strategy Tester.

## Verification

If successfully compiled and attached to an MT5 chart, the upper-left corner of the chart will display a multi-line text dashboard showing "Equity", "Daily P/L", and "Status: RUNNING", and the EA inputs window will feature cleanly separated sections.