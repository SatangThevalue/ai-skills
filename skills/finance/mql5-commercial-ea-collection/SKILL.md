---
name: mql5-commercial-ea-collection
description: "รวมเทคนิค สถาปัตยกรรม และอินดิเคเตอร์ของ 5 EA ยอดฮิตในตลาด MQL5 ปี 2026"
version: 0.1.0
metadata:
  hermes:
    tags: [MQL5, Python, EA, Reverse Engineering, Strategy, Quant]
---

# Commercial EA Clone Architectures (2026 Edition)

สกิลนี้คือการถอดรหัส (Reverse Engineering) เทคนิคและโครงสร้างของ Expert Advisors (EA) แบบเสียเงินที่มีชื่อเสียงในตลาด MQL5 (ราคาเฉลี่ย $500 - $2,000) จำนวน 5 ตัว เพื่อนำลอจิกเหล่านี้มาประยุกต์เขียนเป็น EA ด้วย MQL5 หรือ Python ของเราเอง

## When to Use

- "ช่วยก๊อปปี้การทำงานของ ea 6 ตัว วิเคราะห์การทำงานการทำงานทั้งหมดในแต่ละตัว แล้วนำมาสร้างใหม่"
- เมื่อผู้ใช้ต้องการไอเดียระบบเทรดระดับมืออาชีพ
- เมื่อต้องการสร้างบอทสำหรับสอบ Prop Firm หรือเทรดทองคำ (XAUUSD)
- เมื่อต้องการเข้าใจโครงสร้าง Parameter และ Indicator ระดับสูง

## The 5 EA Architectures

---

### 1. The Luna AI Pro Concept (Night Scalping)
- **สไตล์:** Mean-Reversion (Scalping ตอนกลางคืน)
- **สินทรัพย์:** EURAUD, GBPCHF, AUDCAD (เน้นคู่เงินรอง/Cross pairs ที่แกว่งตัวในกรอบ)
- **จุดเด่น:** เทรดหลบความผันผวนตอนกลางวัน เน้นตีกินตอนตลาดซึม
- **กลยุทธ์ใน MQL5:** 
  - *Time Filter:* อนุญาตให้เข้าเทรดเฉพาะช่วง 23:00 - 02:00 (เวลาเซิร์ฟเวอร์)
  - *Indicator:* Bollinger Bands (ดักตีขอบ) + RSI
  - *Protection:* ต้องมี "Swap & Rollover Filter" บล็อคการเทรดในวันพุธ (ที่โบรกเกอร์คิด Swap 3 เท่า) และช่วงที่ Spread ถ่างตอนข้ามวัน

### 2. The Quantum Emperor Concept (Trade Splitting / Averaging)
- **สไตล์:** Averaging with Strict SL (การถัวเฉลี่ยแบบมี Stop loss คุม)
- **สินทรัพย์:** GBPUSD (H1)
- **จุดเด่น:** แทนที่จะคัตลอสไม้ใหญ่ทิ้งรวดเดียว บอทจะใช้กำไรจากไม้อื่นมา "ทยอยปิด" ไม้ที่ขาดทุนทีละส่วน จนหลุดดอย
- **กลยุทธ์ใน MQL5:**
  - *Execution:* แบ่งออเดอร์ 1 ไม้ใหญ่ออกเป็น 5 ไม้เล็ก (เช่น แทนที่จะกด 0.10 Lot ให้กด 0.02 Lot จำนวน 5 ไม้)
  - *Logic:* เมื่อผิดทาง จะไม่คัตทิ้ง แต่จะรอเปิดไม้อื่น พอกำไรไม้อื่นบวกเกิน 10$ จะสั่งปิดไม้อื่นพร้อมกับ "หั่น" ไม้ที่ติดลบทิ้งไป 1 ไม้ (0.02 Lot) ทำไปเรื่อยๆ จนหลุดดอย

### 3. The Gold Reaper Concept (Multi-Timeframe Breakout)
- **สไตล์:** Support/Resistance Breakout (เก็งกำไรตอนทะลุแนวรับแนวต้าน)
- **สินทรัพย์:** XAUUSD (H1)
- **จุดเด่น:** ไม่มาร์ติงเกล แต่มีระบบ Randomization เพื่อไม่ให้กองทุน Prop Firm จับได้ว่าก็อปปี้เทรด
- **กลยุทธ์ใน MQL5:**
  - *Indicator:* Donchian Channels หรือ Fractal เพื่อหาแนวรับแนวต้าน
  - *Prop Firm Anti-Ban:* สุ่มปรับค่า SL/TP เล็กน้อย (เช่น ±1-2 pips) ในฟังก์ชัน `OrderSend()`
  - *Friday Stop:* สั่งปิดทุกออเดอร์ตอน 20:00 วันศุกร์ ป้องกัน Gap เปิดกระโดดวันจันทร์

### 4. The Range Breakout Concept (Asian Session Filter)
- **สไตล์:** Volatility Breakout (ระเบิดกรอบเอเชีย)
- **สินทรัพย์:** XAUUSD, BTCUSD, US30
- **จุดเด่น:** ไม่ง้อ Indicator แต่ใช้วิธีจับ "พฤติกรรมตลาดตามเวลาโลก"
- **กลยุทธ์ใน MQL5:**
  - วาดกล่อง (หา High/Low) ในช่วงตลาด Asian Session (เช่น 00:00 - 08:00)
  - พอเข้าช่วง London Session (09:00 เป็นต้นไป) ถ้าราคาทะลุ High สั่ง BUY, ทะลุ Low สั่ง SELL
  - *Close Rule:* สั่งปิดออเดอร์ทุกไม้ตอนจบตลาด New York เพื่อหนีความผันผวน

### 5. The GoldBaron AI Concept (Trend Following + Prop Firm Scaling)
- **สไตล์:** Trend Following คำใหญ่ (ถือยาวข้ามวัน)
- **สินทรัพย์:** XAUUSD (H1)
- **จุดเด่น:** มีระบบ Dynamic Risk Management ที่ตั้ง Lot อัตโนมัติให้เหมาะกับ Drawdown Limit ของกองทุน
- **กลยุทธ์ใน MQL5:**
  - *Indicator:* Moving Average 3 เส้นตัดกัน (เช่น 20, 50, 200) เพื่อคอนเฟิร์มเทรนด์
  - *Position Sizing:* ถ้าตั้ง Lot เป็นค่าลบ (เช่น -0.5) หมายถึงให้บอทคำนวณ Leverage อัตโนมัติจาก Balance แบบทบต้น (Compounding)
  - *Volatility Filter:* ถ้าแท่งเทียนยาวผิดปกติ (ATR Spike) จะบล็อคคำสั่งซื้อ ป้องกันการเบรคหลอก (Fakeout)

## Blueprint for Your Custom MQ5 EA

หากต้องการผสมผสานจุดแข็งของทั้ง 5 EA นี้เข้าด้วยกัน (Ultimate EA) โครงสร้าง `Input Parameters` ควรเป็นดังนี้:

```cpp
input group "=== Risk & Prop Firm ==="
input double DailyDrawdownLimit = 4.5;    // หยุดบอทถ้าติดลบถึง -4.5% ต่อวัน
input bool   RandomizeSLTP      = true;   // สุ่มจุดปิดออเดอร์ ± 1-2 pips (หลบ Prop Firm จับผิด)
input bool   CloseFriday        = true;   // ปิดทุกออเดอร์วันศุกร์ (หลบ Gap)

input group "=== Session Filters ==="
input bool   TradeAsianRange    = false;  // เล่น Breakout ช่วงเข้าตลาดยุโรป
input bool   TradeNightScalp    = false;  // เล่น Mean Reversion ช่วงดึก

input group "=== Indicators & Logic ==="
input bool   UseVolatilityFilter= true;   // ห้ามเทรดตอนข่าวแรง (ATR Spike)
```

## Verification
- การนำเทคนิคเหล่านี้ไปเขียนโค้ด MQL5 ต้องระมัดระวังเรื่อง `TimeCurrent()` ให้ดี เพราะเทคนิคที่ใช้เรื่องเวลา (เช่น Night Scalping หรือ Asian Breakout) ต้องอ้างอิงจาก **เวลาของเซิร์ฟเวอร์โบรกเกอร์ (Server Time)** เสมอ ไม่ใช่เวลาของคอมพิวเตอร์ Local
- หากนำไปพัฒนาบน Python ให้ดึงเวลาแท่งเทียนที่เป็น UTC มาแปลงให้ตรงกับ Session นั้นๆ ก่อนคำนวณ Breakout เสมอ