---
name: ea-dashboard-architecture
description: "สถาปัตยกรรมและพารามิเตอร์สำหรับสร้าง Dashboard และระบบตั้งค่า EA (Python/MT5)"
version: 0.1.0
metadata:
  hermes:
    tags: [MT5, Python, EA, Dashboard, Parameters, Architecture]
---

# EA Dashboard & Parameter Architecture

สกิลนี้อธิบายโครงสร้างของ "หน้าตั้งค่า (Input Parameters)" และ "หน้าปัดแสดงผล (Dashboard)" สำหรับบอทเทรดระดับมืออาชีพ (เช่น แนว Scalping/Grid) ที่เขียนด้วย Python MT5 โดยรวบรวมตัวแปรที่จำเป็น ตัวกรองข่าว และการจัดการเวลาเซิร์ฟเวอร์ เพื่อให้บอทมีความทนทาน (Robust) เมื่อนำไปรันในสภาพแวดล้อมจริง

## When to Use

- "ช่วยวิเคราะห์ สร้างหน้าตั้งค่า พารามิเตอร์,เดชบอร์ด ควรมีตัวแปรใดบ้าง"
- เมื่อต้องการออกแบบ UI หรือ Configuration File สำหรับบอทเทรด
- เมื่อต้องการวางระบบป้องกันข่าว (News Filter) และจัดการเวลา (Time Management)

## Quick Reference

- **Config Format:** แนะนำให้ใช้ `.json` หรือ `.yaml` สำหรับ Python Bot
- **News Filter:** ใช้ ATR Spike Detection (ปลอดภัยกว่าเชื่อม API ข่าว)
- **Time Sync:** ต้องเช็ค `mt5.symbol_info_session_trade()` เสมอ

## 1. โครงสร้างหน้าตั้งค่า (Input Parameters)

หากเขียนด้วย Python ตัวแปรเหล่านี้ควรอยู่ในไฟล์ `config.json` หรือถูกประกาศไว้ด้านบนของ Script เพื่อให้ผู้ใช้งาน (User) ปรับแก้ได้ง่าย แบ่งเป็น 5 หมวดหมู่:

### 1.1 Core Trading Setup (การตั้งค่าหลัก)
- `Symbol`: "XAUUSD" (คู่เงิน/สินทรัพย์ที่เทรด)
- `Timeframe`: 1 (หมายถึง M1 สำหรับ Scalping)
- `Magic_Number`: 123456 (เพื่อไม่ให้บอทไปยุ่งกับออเดอร์ของบอทตัวอื่น หรือที่คนกดมือ)

### 1.2 Risk & Money Management (การบริหารเงิน)
- `Base_Lot`: 0.01 (หลอดเริ่มต้น)
- `Lot_Multiplier`: 1.5 (กรณีเปิดไม้ Grid แก้งาน ไม้ต่อไปจะเป็น 0.01 -> 0.015)
- `Max_Grid_Levels`: 5 (จำนวนไม้สูงสุดที่จะเปิดแก้พอร์ต ถ้าเกินนี้ยอมคัตทิ้ง)
- `Daily_Target_USD`: 50.0 (กำไรถึงเป้าต่อวันแล้วหยุดทำงาน)
- `Daily_StopLoss_USD`: 150.0 (ขาดทุนถึงเป้าต่อวันแล้วหยุดทำงาน)

### 1.3 Execution Parameters (เงื่อนไขการยิงออเดอร์)
- `Grid_Distance_Pips`: 30 (ระยะห่างขั้นต่ำก่อนเปิดไม้ย้ำ)
- `Take_Profit_Pips`: 20 (เป้าหมายกำไร)
- `Use_Trailing_Stop`: True (เปิด/ปิดระบบล็อคกำไร)
- `Trailing_Start_Pips`: 15 (เริ่มขยับ SL บังหน้าทุนเมื่อกำไรถึงระยะนี้)
- `Trailing_Step_Pips`: 5 (ขยับ SL ตามไปทีละ 5 pips)

### 1.4 Protection Filters (ด่านป้องกันพอร์ต)
- `Max_Spread_Points`: 30 (ถ้าโบรกเกอร์ถ่าง Spread เกิน 30 points ห้ามยิงออเดอร์)
- `News_Filter_Enabled`: True (เปิด/ปิดระบบหลบข่าว)
- `Pause_After_Shock_Minutes`: 30 (ถ้าเจอข่าวแรง ให้บอทหยุดพักกี่นาที)

## 2. โครงสร้างหน้าปัดแสดงผล (Dashboard / Logs)

บอท Python ไม่มีหน้าต่างกราฟิกเหมือน EA MQL5 ดังนั้น Dashboard จึงควรถูกพิมพ์ออกมาทาง Console (Terminal) หรือยิงแจ้งเตือนเข้า LINE/Telegram/Discord โดยควรแสดงข้อมูลดังนี้ ทุกๆ N นาที:

### ข้อมูลที่ต้องแสดงบน Dashboard:
1. **Account Status:** Balance, Equity, Free Margin, Margin Level (%)
2. **Daily Performance:** P/L วันนี้ (Current Daily Profit vs Daily Target)
3. **Current Positions:** จำนวนไม้ที่เปิดอยู่ (Buy X ไม้ / Sell Y ไม้), Floating P/L ปัจจุบัน, Lot สะสมรวม
4. **System Status:** แจ้งเตือนสภาวะตลาด (เช่น "Market: Normal", "Market: Shock/News", "Spread: High")

## 3. ตัวกรองการเข้าเทรด (Indicators & Logic)

สำหรับบอท Scalping XAUUSD M1 แนะนำให้ใช้ Indicator ชุดนี้:
- **Bollinger Bands (Period=20, Dev=2.5):** ใช้หาจุดที่ราคากระชากแรงผิดปกติ (Overextended)
- **RSI (Period=14):** ใช้ยืนยันโมเมนตัม (Oversold < 30, Overbought > 70)
- **ATR (Period=14):** ใช้เป็นไม้บรรทัดวัดความผันผวน เพื่อคำนวณระยะ Grid และ News Filter

*Logic (Selective Grid):* เมื่อราคาหลุดขอบล่าง BB + RSI < 30 = ยิง BUY. หากผิดทาง จะไม่ยิงไม้สองทันที แต่จะรอให้ราคาร่วงลงไปมากกว่า `Grid_Distance` + เกิดสัญญาณ Oversold อีกครั้ง ถึงจะยิงไม้สอง (นี่คือที่มาของคำว่า Selective Grid)

## 4. การจัดการปัญหาเวลาเซิร์ฟเวอร์ (Server Time Management)

ปัญหาคลาสสิกของ MT5 Python คือ "เวลาบนคอมพิวเตอร์เรา" ไม่ตรงกับ "เวลาของ Server โบรกเกอร์" (ซึ่งมักใช้เวลา GMT+2 หรือ GMT+3)

**วิธีการจัดการที่ถูกต้องใน Python:**
1. ไม่ใช้ `datetime.now()` ของคอมพิวเตอร์ในการคำนวณแท่งเทียน
2. ต้องเช็คเวลาเปิด-ปิดตลาดของโบรกเกอร์ด้วยฟังก์ชัน:
   ```python
   sym_info = mt5.symbol_info("XAUUSD")
   # เช็คเวลาเริ่ม/จบ session ของวันนั้น
   # mt5.symbol_info_session_trade("XAUUSD", day_of_week)
   ```
3. ดึงเวลาเซิร์ฟเวอร์ล่าสุดจาก Tick data เสมอ:
   ```python
   tick = mt5.symbol_info_tick("XAUUSD")
   server_time = pd.to_datetime(tick.time, unit='s')
   ```

## 5. การป้องกันข่าว (News Filter Architecture)

แทนที่จะใช้ API ปฏิทินข่าว (ForexFactory) ซึ่งยุ่งยากและมักจะดีเลย์ แนะนำให้ใช้ **Volatility Breakout (ATR Spike)** เป็นตัวจับข่าวสดๆ บนกราฟ:

*แนวคิด:* เมื่อมีข่าวใหญ่ (เช่น Non-Farm) ราคาจะกระชากแรงผิดปกติในแท่งเดียว
*   คำนวณ `ATR(15)` ของกราฟ M1 (ค่าเฉลี่ยการแกว่ง 15 นาทีที่ผ่านมา)
*   นำความยาวแท่งเทียนปัจจุบัน (High - Low) มาเทียบกับ ATR
*   หาก `(High - Low) > ATR * 3.0` แสดงว่าเกิดข่าวกระชาก (News Shock)
*   **Action:** บอทเปลี่ยนสถานะเป็น `PAUSED` และหยุดยิงออเดอร์ใหม่ไปอีก 30 นาที (รอจนกว่าตลาดย่อยข่าวเสร็จ)

## Verification
เมื่อนำ Blueprint นี้ไปเขียนเป็น Python Script จะต้องสามารถแปลง `config.json` ให้เป็นตัวแปรในคลาสเทรดได้ และมีฟังก์ชัน `print_dashboard()` ที่ทำงานทุกๆ 5 นาที เพื่อรายงานสถานะพอร์ตและ Daily Profit สรุปให้ผู้ใช้งานทราบ