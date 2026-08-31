---
name: quantum-omnigold-architecture
description: "สถาปัตยกรรมและกลยุทธ์การเทรดทองคำ (XAUUSD) เลียนแบบ Quantum OmniGold EA"
version: 0.1.0
metadata:
  hermes:
    tags: [MT5, MQL5, EA, XAUUSD, Prop Firm, Architecture]
---

# Quantum OmniGold Architecture (Clone Blueprint)

สกิลนี้วิเคราะห์และถอดรหัส (Reverse Engineering) สถาปัตยกรรมของ EA ระดับพรีเมียม (Quantum OmniGold) ที่ถูกออกแบบมาเพื่อเทรดทองคำ (XAUUSD) และสอบกองทุน (Prop Firm) โดยเฉพาะ จุดเด่นคือความปลอดภัยสูง "No Grid, No Martingale" ทุกออเดอร์เป็นอิสระและมีการจัดการความเสี่ยงในตัวเอง

## When to Use

- "ช่วย วิเคราะห์และจัดเรียง เพื่อนำไปสร้าง mq5 เพื่อไปทดสอบ full loop"
- เมื่อต้องการสร้างบอทเทรดทองคำ (XAUUSD) ที่ปลอดภัยสำหรับสอบ Prop Firm
- เมื่อต้องการวาง Logic แบบ Multi-indicator (ZigZag + MA + Stochastic)

## Quick Reference

- **Core Indicators:** `ZigZag` (Price Action/Structure), `Moving Average` (Trend), `Stochastic` (Momentum).
- **Execution Style:** 1 Trade = 1 Life (No Grid). Always has SL.
- **Trade Management:** 2 TP Levels + Adaptive Trailing Stop.
- **Risk Profiles:** Adjustable from "Very Low" (Prop Firm) to "Growth".

## โครงสร้างและตรรกะการเทรด (The Execution Loop)

เพื่อนำไปเขียนเป็น MQL5 (Full Loop) ต้องจัดเรียงตรรกะการทำงาน (Logic Flow) ให้ทำงานตามลำดับดังนี้:

### 1. Risk Management Module (การคัดกรองความเสี่ยง)
ด่านแรกสุดของ `OnTick()` ต้องป้องกันพอร์ตพัง:
- **Prop Firm Mode (Very Low Risk):** กำหนด `Max_Daily_Drawdown` (เช่น -4%). ถ้ายอด Equity ต่ำกว่าเกณฑ์ ให้ปิดออเดอร์และหยุดการทำงานทันที
- **Spread Filter:** ทองคำผันผวนสูง หาก Spread ปัจจุบันสูงกว่าค่าเฉลี่ยที่ตั้งไว้ ห้ามยิงออเดอร์

### 2. Trend Confirmation (ด่านจับเทรนด์ภาพใหญ่)
- **Indicator:** `Moving Average` (เช่น EMA 50 หรือ EMA 200)
- **Logic:** 
  - ถ้าราคาปัจจุบัน > EMA = อนุญาตให้หาจังหวะ BUY เท่านั้น
  - ถ้าราคาปัจจุบัน < EMA = อนุญาตให้หาจังหวะ SELL เท่านั้น

### 3. Price Action Structure (ด่านจับโครงสร้างราคา)
ใช้เพื่อหาราคาแนวรับ-แนวต้านที่ชัดเจน ลดสัญญาณหลอก
- **Indicator:** `ZigZag`
- **Logic:** บอทจะใช้ยอด (High) และฐาน (Low) ของ ZigZag ล่าสุดเป็นจุดอ้างอิง
  - *Setup (Buy):* ต้องเกิดจุด Higher Low (ฐานยกสูงขึ้น)
  - *Setup (Sell):* ต้องเกิดจุด Lower High (ยอดต่ำลง)

### 4. Momentum Trigger (ด่านสับไกยิง)
หลังจากผ่านด่านเทรนด์และด่านโครงสร้างแล้ว จะรอการย่อตัว (Pullback) เพื่อเข้าซื้อในราคาที่ดีที่สุด
- **Indicator:** `Stochastic Oscillator` (เช่น ค่า 5,3,3 หรือ 14,3,3)
- **Logic:** 
  - *Entry Buy:* เมื่อเส้น %K ตัด %D ขึ้น ในโซน Oversold (< 20)
  - *Entry Sell:* เมื่อเส้น %K ตัด %D ลง ในโซน Overbought (> 80)

### 5. Position Management (การจัดการออเดอร์แบบมืออาชีพ)
นี่คือส่วนที่ทำให้ EA ตัวนี้ผ่านกองทุนและทำกำไรได้ยั่งยืน (Win rate สูง, Drawdown ต่ำ)
- **One Independent Position:** อนุญาตให้มีออเดอร์เปิดอยู่แค่ 1 ไม้เสมอ (ห้ามตีกริด ห้ามถัว)
- **Predefined Stop Loss (SL):** วาง SL ทันทีที่ยิงออเดอร์ โดยอิงจากสวิงต่ำสุด/สูงสุดของ ZigZag หรือใช้ ATR
- **Dual Take Profit (2 TP Levels):**
  - เมื่อราคาไปถึง *TP 1* (เช่น 1:1 Risk-Reward) -> ทำการ Partial Close ปิดทำกำไรครึ่งนึง (0.5x Lot) และเลื่อน SL มาบังทุน (Break-Even)
  - ส่วนที่เหลือปล่อยรันไปหา *TP 2* (เช่น 1:3 Risk-Reward) หรือใช้ **Adaptive Trailing Stop** เลื่อน SL ตามราคาไปเรื่อยๆ จนกว่ากราฟจะย้อนมากิน

## Verification for MQL5 Implementation
ก่อนนำไปคอมไพล์ใน MQL5 ต้องมั่นใจว่าโค้ดมีระบบ `Partial Close` และ `Trailing Stop` ที่แยกการทำงานออกจากฟังก์ชันส่งคำสั่ง (Execution) และมีการเช็ค `PositionsTotal() == 0` เสมอก่อนหาจุดเข้าใหม่ เพื่อคงคอนเซปต์ "No Grid"