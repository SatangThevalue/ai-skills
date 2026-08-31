---
name: mql5-acd-cs-architecture
description: "โครงสร้างและอัลกอริทึมของ EA แบบ Adaptive Context-Driven (ACD-CS) บน MT5"
version: 0.1.0
metadata:
  hermes:
    tags: [MQL5, EA, MT5, Architecture, Market Regime]
---

# Adaptive Context-Driven Correlation System (ACD-CS) Architecture

สกิลนี้สรุปแนวคิดและโครงสร้างของ Expert Advisor (EA) บน MQL5 ที่ไม่ได้ใช้แค่สัญญาณ Technical (เช่น ตัดเส้น EMA แล้วเข้าเทรด) แต่ใช้ **"การประเมินบริบทของตลาด (Context-Driven)"** เป็นหัวใจหลักในการคัดกรองสัญญาณ โดยแบ่งเป็นระบบให้คะแนน (Scoring System) และตัวกรอง 4 ชั้นก่อนถึงขั้นตอนการเข้าเทรด

## When to Use

- เมื่อผู้ใช้ขอให้ "วิเคราะห์โค้ด EA" หรือ "อธิบายโครงสร้าง EA MQL5"
- เมื่อต้องการสร้างบอท MT5 / Python ที่มีระบบตรวจจับสภาวะตลาด (Market Regime)
- เมื่อต้องการวางระบบตัวกรองข่าว (Event Filter) โดยไม่ใช้ปฏิทินเศรษฐกิจ

## Quick Reference

- **Regime Detection:** ใช้ `ADX` แบ่งตลาดเป็น Balanced, Transition, Trend, Shock.
- **Event Filter:** ใช้สัดส่วน `ATR(M15) / ATR_AVG(M15) > 2.0` เป็นตัวแทนของข่าวกระชาก
- **Liquidity Check:** สกัดการเข้าเทรดเมื่อ Spread ถ่างเกินกำหนด (`Spread > Max_Spread_Pips`).
- **Scoring Engine:** ใช้ระบบสะสมคะแนนจากบริบทต่างๆ (ถ้าคะแนน < `Min_Score` จะไม่เข้าเทรด).

## โครงสร้างอัลกอริทึม (The 6-Step Execution Pipeline)

โค้ดนี้แสดงถึงสถาปัตยกรรมระดับมืออาชีพ โดยใช้โครงสร้าง `OnTick()` เป็น Pipeline ที่มีด่านสกัด 6 ขั้นตอน:

### 1. Session Context (ด่านคัดกรองเวลา)
- **แนวคิด:** ห้ามบอททำงานในสภาพแวดล้อมที่คาดเดาไม่ได้ (เช่น นอกเวลาทำการหลัก หรือช่วงพักเที่ยง/ข้ามคืน)
- **กลไก:** ใช้ `TimeHour(TimeTradeServer())` เช็คชั่วโมงของฝั่งเซิร์ฟเวอร์ (เช่น ให้เทรดเฉพาะ 07:00 - 20:00)

### 2. Market Regime (ด่านคัดกรองสภาวะตลาด)
- **แนวคิด:** กลยุทธ์ Mean-Reversion จะพังทลายถ้าตลาดกำลังมีเทรนด์รุนแรง
- **กลไก:** ใช้ **ADX (H1)** ควบคู่กับ **ATR (H1)** เป็นตัวแบ่งโซน:
  - `ATR ปัจจุบัน > (ATR เฉลี่ย * 2)` = **SHOCK** (แพนิก)
  - `ADX > 30` = **TREND** (เทรนด์ชัด)
  - `ADX > 20` = **TRANSITION** (กำลังเปลี่ยนเทรนด์)
  - `ที่เหลือ` = **BALANCED** (ไซด์เวย์)
- *ผลลัพธ์:* ระบบอนุญาตให้ใช้กลยุทธ์ Mean-Reversion เฉพาะตอนตลาดเป็น Balanced หรือ Transition เท่านั้น

### 3. Event / Volatility Check (ด่านคัดกรองข่าว)
- **แนวคิด:** หลีกเลี่ยงความเสี่ยงจากข่าว (News) โดยไม่ต้องง้อ API ปฏิทินเศรษฐกิจ (ซึ่งมักจะพังหรือดีเลย์)
- **กลไก (Behavior-Based):** ใช้ `ATR(M15)` เทียบกับ `ATR_AVG(M15)`
  - ถ้าราคากระชากแรงกะทันหัน (`Ratio > 2.0`) ระบบจะถือว่าเป็น "เหตุการณ์ (Event-driven)" และตีค่า impact เป็น `0.0` (สั่งหยุดเทรดทันที)

### 4. Liquidity Check (ด่านกรองสภาพคล่อง)
- **แนวคิด:** ป้องกันการถูกกินส่วนต่าง (Spread) ในช่วงที่สภาพคล่องต่ำ (เช่น ตอนข้ามวัน หรือช่วงประกาศข่าว)
- **กลไก:** เอา `Ask - Bid / Point` ถ้าเกินค่า `Max_Spread_Pips` ที่ตั้งไว้ บอทจะหยุดทำงาน

### 5. Signal & Scoring Engine (ระบบให้คะแนน)
- **แนวคิด:** เปลี่ยนจากระบบ Binary (True/False) มาเป็น "เกรดความน่าจะเป็น" (Probability Score)
- **กลไก:** นำผลลัพธ์จากด่านที่ 1-3 มาคำนวณสะสมคะแนน เช่น ถ้าได้ Session ดี (+25) + ตลาด Balanced (+25) + ... ถ้ารวมแล้วคะแนนถึง `Min_Score` (เช่น 65) ถึงจะอนุมัติการส่งคำสั่ง

### 6. Execution (การลงมือทำ)
- เมื่อผ่านทั้ง 5 ด่าน จะทำการเช็คออเดอร์ค้าง (เช่น `PositionsTotal() == 0`) เพื่อป้องกันการยิงซ้ำ (Over-trading) แล้วถึงเรียกฟังก์ชัน `OpenTrade()`

## Pitfalls (จุดอ่อนหรือข้อจำกัดของโค้ดชุดนี้)

- **Hardcoded Session Hours:** การ Fix ตัวเลขเวลาไว้ในโค้ด (เช่น `hour >= 7 && hour <= 20`) อาจมีปัญหากับโบรกเกอร์ที่มีการปรับเวลา Daylight Saving Time (DST) หรือ Server Time Offset ไม่ตรงกับตลาดจริง. (ควรทำเป็นตัวแปร Input)
- **ATR Array Management:** ฟังก์ชัน `iATR` ที่ใส่พารามิเตอร์ 4 ตัว (เช่น `iATR(_Symbol, PERIOD_H1, ATR_Period, 20)`) อาจไม่ใช่ Standard Signature ใน MQL5 ดั้งเดิม ซึ่งปกติจะต้องสร้าง Handle ก่อนใน `OnInit()` แล้วใช้ `CopyBuffer()` เพื่อดึงข้อมูลอดีตมาหาค่าเฉลี่ย
- **Incomplete Code:** โค้ดยังขาดส่วนการจัดการ Risk (การนำ `PipValue` ไปคำนวณ `LotSize`) และขาดฟังก์ชัน `OpenTrade()` อย่างเป็นทางการ

## Verification
- โค้ดแนวคิดนี้สามารถประยุกต์ไปใช้ใน Python ได้ทันที โดยแปลงจาก `OnTick()` เป็น Loop รายนาที, ใช้ `yfinance` หรือ `pandas_ta` หา ATR/ADX, และใช้ `datetime.now()` หา Session.