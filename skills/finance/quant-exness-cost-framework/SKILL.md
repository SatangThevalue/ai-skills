---
name: quant-exness-cost-framework
description: Framework for calculating and storing All-In Transaction Costs (Spread, Commission, Swap, Slippage) for Exness in Quant Trading Backtests and Risk Engines.
category: finance
---

# Transaction Cost Framework สำหรับ Exness (Quant Trading)

สำหรับการสร้าง Backtest Engine, Risk Engine และ Position Sizing Engine ที่แม่นยำ จำเป็นต้องคำนวณ Transaction Cost แบบ **"All-in Cost"** ห้ามคำนวณเพียงแค่ Spread เท่านั้น ต้นทุนหลักมี 4 ส่วน:
1. Spread
2. Commission
3. Swap
4. Slippage

## 1. Exness Account Types & Fee Structures

| Account Type | Commission | Spread Characteristics | Use Case / Notes |
| :--- | :--- | :--- | :--- |
| **Standard** | $0 | 0.2 - 0.3 pips (เริ่มต้น) | ต้นทุนแฝงอยู่ใน Spread ทั้งหมด |
| **Pro** | $0 | ~0.1 pips (เริ่มต้น) | Spread ต่ำกว่า Standard |
| **Raw Spread** | ~$3.5/lot/side ($7 RT) | ≈ 0 pips | นิยมที่สุดสำหรับ AI/Algo Trading |
| **Zero** | $0.05 - $8/side (Dynamic) | 0 pips (ใน 30 คู่สกุลเงินหลัก) | ค่าคอมมิชชันแปรผันตาม Instrument |

## 2. All-In Trading Cost Calculation

**สูตรหลัก:**
`Total Cost = Spread Cost + Commission + Swap + Slippage`

### วิธีคำนวณแต่ละส่วน:
*   **Spread Cost:** `Spread (pips) × Pip Value × Lot Size`
    *   *ตัวอย่าง:* EURUSD Spread 1 pip, 1 Lot, Pip Value $10 -> Cost = $10
*   **Commission:** ตามประเภทบัญชี (Raw Spread = $7 per round turn lot)
*   **Swap:** เปลี่ยนแปลงตลอดเวลาขึ้นอยู่กับ Symbol, Direction, และ Day (ควรดึงข้อมูล long_swap, short_swap รายวันเก็บไว้ใน DB)
*   **Slippage:** `Slippage (pips) × Pip Value × Lot Size`
    *   *ตัวอย่าง:* Signal Buy @ 1.10000, Fill จริง @ 1.10015 -> Slippage 1.5 pips -> 1.5 * $10 = $15 Cost

## 3. PostgreSQL Database Architecture

แนะนำให้แยกการเก็บข้อมูลและต้นทุนอย่างละเอียดในระบบฐานข้อมูล:

### Table: `spreads_history`
ใช้เก็บข้อมูลความผันผวนของ Spread (สำคัญสำหรับ Market Regime & Session Analysis)
*   `symbol`
*   `timestamp`
*   `spread`
*   `session` (e.g., Asian, London, New York)

### Table: `executions`
ใช้เก็บคุณภาพการ Execute ของบัญชีจริง
*   `symbol`
*   `signal_price` (ราคาที่ Algorithm สั่ง)
*   `fill_price` (ราคาที่ Broker จับคู่ให้จริง)
*   `slippage` (คำนวณจากส่วนต่าง)

### Table: `execution_costs`
รวมค่าใช้จ่ายทุกส่วนของแต่ละไม้
*   `symbol`
*   `account_type`
*   `timestamp`
*   `spread` / `commission` / `swap` / `slippage` (Raw metrics)
*   `spread_cost` / `commission_cost` / `swap_cost` / `slippage_cost` (Monetary metrics)
*   `total_cost` (All-in Cost)

## 4. V1 Backtest Conservative Assumptions (EURUSD)

หากเพิ่งเริ่มพัฒนาและยังไม่มีข้อมูล Spread/Slippage จริง ให้ใช้ค่า Conservative Assumption สำหรับ EURUSD ดังนี้:

*   **Standard Account:** Spread = 1.2 pips, Commission = $0, Slippage = 0.2 pips
*   **Raw Spread Account:** Spread = 0.2 pips, Commission = $7/lot, Slippage = 0.2 pips
*   **Pro Account:** Spread = 0.7 pips, Commission = $0, Slippage = 0.2 pips

*ข้อควรระวัง: ต้องอัปเดตและทำ Calibrate ค่าเหล่านี้ด้วยข้อมูลจริงที่เก็บจาก MT5 (Database: `executions` และ `spreads_history`) ในภายหลัง*

## 5. Cost-adjusted KPIs

ในการวัดผลระบบ Trading ห้ามวัดแค่ `Gross Profit` ระบบควร Report Metrics เหล่านี้เสมอ:
*   `Gross Profit`
*   `Net Profit` (Gross Profit - Total Cost)
*   `Cost Ratio` (Total Cost / Gross Profit) -> *ชี้วัดว่ากลยุทธ์ทำเงินให้ Broker หรือให้เรา*
*   `Average Spread` (ตาม Session)
*   `Average Slippage` (เพื่อประเมิน Execution Quality ของ Broker)