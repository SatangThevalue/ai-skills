---
name: dw-trading-thailand-strategy
description: "คู่มือเทคนิคและการเลือกซื้อ DW (Derivative Warrants) ในประเทศไทย"
version: 0.1.0
metadata:
  hermes:
    tags: [DW, Trading, Settrade, Strategy, Thailand]
---

# DW Trading Strategy in Thailand

This skill outlines the complete top-down approach and essential metrics required to trade Derivative Warrants (DW) effectively on the Stock Exchange of Thailand (SET). It covers market analysis, underlying stock selection, DW specification filtering, price mapping, and execution constraints. It does NOT provide executable Python scripts, but rather the business logic required to build or evaluate a DW trading bot.

## When to Use

- "วิเคราะห์ลำดับขั้นตอนในการซื้อขาย dw"
- "หาข้อมูล ข้อควรระวัง DW"
- "เทรด DW ต้องดูอะไรบ้าง"
- When building or reviewing the trading logic for a DW automated bot.

## Prerequisites

- Access to Settrade Open API (or equivalent broker API) for execution.
- Real-time market data access (MQTT or API) to monitor the underlying stock.
- The DW issuer's pricing table (ตารางราคา DW) for price mapping.

## Quick Reference

- **Underlying (หุ้นแม่):** The stock the DW tracks (e.g., PTT).
- **Time to Maturity:** Must be > 1 - 1.5 months.
- **Effective Gearing:** Target range 3.0x - 6.0x.
- **Sensitivity (Tick):** Target range 0.8 - 1.2.
- **Moneyness:** Select ATM (At-the-Money) or slightly OTM.

## Procedure

1. **Global & Macro Analysis**
   Check global indices (Dow Jones, Nasdaq, Nikkei) and commodities. Ensure the global sentiment aligns with the intended DW direction (Call/Put) to avoid fighting strong macro trends.

2. **Underlying Stock Selection**
   Filter for SET50/SET100 stocks. Analyze the *underlying stock's* technical chart (e.g., ADX > 25) to confirm a strong, clear trend. Avoid sideways markets where Time Decay will erode DW value.

3. **DW Filtering**
   For the chosen underlying, select a specific DW based on:
   - **Time to Maturity:** > 1.5 months to minimize rapid Time Decay.
   - **Effective Gearing:** 3x to 6x.
   - **Sensitivity (Tick):** ~1.0 (so 1 tick of the underlying = 1 tick of the DW).

4. **Price Mapping (ตารางราคา)**
   Determine the Entry, Stop Loss (SL), and Take Profit (TP) prices on the *underlying stock*. Map these exactly to the corresponding DW prices using the issuer's DW price table. NEVER use technical indicators directly on the DW chart.

5. **Execution**
   Use the `terminal` tool to run the bot. Send orders to the SET matching the mapped DW prices. Use `Limit Order` for passive entry or `MP-MKT` with `FOK / IOC` validity for aggressive entry.

## Pitfalls

- **Market Maker (MM) Pulls Bids:** During high volatility or near open/close, the MM may temporarily remove bids. If the bot detects widened spreads, it must suspend Market Orders.
- **Weekend / Holiday Risk:** Time Decay includes non-trading days. Holding DWs over long weekends causes immediate value loss upon market open.
- **No Averaging Down (ห้ามถัวเฉลี่ยขาลง):** Averaging down a losing DW position compounds losses via both adverse underlying price movement and continuous Time Decay. Execute strict Stop Loss.
- **Dividend Effect (XD):** When the underlying stock goes XD, its price drops. DW issuers adjust the DW terms to compensate, but a bot reading pure price data might trigger a false Stop Loss. Code must account for XD dates.

## Verification

Review the bot's configuration or logic flow to ensure technical indicators (EMA, RSI, MACD) are calculated on the underlying stock (`PTT.BK`), while execution calls target the specific DW symbol (`PTT01C2405A`).