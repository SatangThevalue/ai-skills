---
name: forex-exness-backtesting
description: "การทดสอบสภาพแวดล้อมเสมือนจริงของ Exness (Free Swap) บน Python"
version: 0.1.0
metadata:
  hermes:
    tags: [Forex, Exness, Backtest, Python, Broker]
---

# Exness Virtual Environment Backtesting

สกิลนี้อธิบายวิธีการตั้งค่า Library `backtesting.py` เพื่อจำลองสภาพแวดล้อม (Simulation) ของโบรกเกอร์ยอดนิยมอย่าง Exness ซึ่งมีจุดเด่นเรื่องบัญชี **Extended Swap-Free** (ถือข้ามคืนฟรีดอกเบี้ย) เพื่อตรวจสอบว่ากลยุทธ์ Mean Reversion สามารถทำกำไรในโลกความจริงได้หรือไม่

## When to Use

- "จำลองบนสภาพแวดล้อม Exness"
- "รัน Backtest แบบสมจริง (มี Spread, ไม่มี Swap)"
- เมื่อต้องการตรวจสอบว่าระบบเทรดใช้งานได้จริงบนโบรกเกอร์ที่ผู้ใช้เลือกหรือไม่

## Quick Reference

- **Timeframe ที่เหมาะสม:** H1 หรือ H4 (หลบ Noise และ Spread)
- **ทุนเริ่มต้นที่เหมาะสม:** $100 - $500
- **ค่าธรรมเนียมบัญชี Standard (EURUSD):** Spread เฉลี่ย 1.0 pips (commission=0.00010)
- **Swap:** 0.00 (อนุญาตให้ถือข้ามคืนได้โดยไม่เจ็บตัว)

## Procedure (การจำลอง Exness บน Python)

### 1. การตั้งค่า Spread & Commission
ในการใช้งาน `backtesting.py` เราไม่สามารถตั้งค่า "Spread" แยกได้โดยตรง แต่เราจะรวมมันเข้าไปในค่า `commission`
- **Exness Standard Account:** EURUSD spread เฉลี่ยอยู่ที่ 10 points (หรือ 1 pip)
- **การแปลงเป็น Commission:** ให้ตั้งค่า `commission = 0.00010` (หรือทศนิยมตำแหน่งที่ 4 ตาม pip size)

```python
from backtesting import Backtest

# จำลองบัญชี $100 Leverage 1:500
bt = Backtest(
    data, 
    MyStrategy, 
    cash=100, 
    margin=1/500, 
    commission=0.00010, # เท่ากับ Spread 1 pips
    trade_on_close=False
)
```

### 2. การประยุกต์กลยุทธ์เข้ากับ Free-Swap
จุดเด่นที่แข็งแกร่งที่สุดของ Exness คือ **Free Swap** แปลว่าเราสามารถ **"ทนลาก (ถือออเดอร์ข้ามคืน)"** ได้โดยไม่โดนโบรกเกอร์เก็บดอกเบี้ยรายวัน (ซึ่งปกติเป็นศัตรูร้ายของการติดดอย)

ดังนั้น หากใช้โบรกเกอร์นี้ เราสามารถ:
- **ขยาย Stop Loss (SL) ให้กว้างขึ้น:** จากเดิม 1.5 ATR ให้ยืดเป็น **3.0 ATR** เพื่อสู้กับเทรนด์และให้กราฟมีพื้นที่กลับตัว
- **ขยับ Timeframe (TF):** เปลี่ยนจาก M15 (ที่ต้องรีบเทรดรีบปิดก่อนข้ามคืน) ไปเป็น **H1** (ถือออเดอร์ 1-3 วันได้สบายๆ)

## Pitfalls (สิ่งที่ผลลัพธ์จาก Backtest สอนเรา)

แม้จะใช้สภาพแวดล้อมที่เป็นใจที่สุด (กราฟ H1 เพื่อหนี Spread, ขยาย SL, และไม่คิดดอกเบี้ยข้ามคืน) แต่การทำ Backtest ย้อนหลัง 1 ปีด้วยกลยุทธ์ Mean Reversion คลาสสิก ยังคงพบว่า **"ขาดทุน (-10%)"** 

**ทำไมถึงขาดทุน?**
1. **The Drawdown Trap:** พอร์ตขนาด 100$ เมื่อโดนลากจนชน SL กว้างๆ (3.0 ATR) ในกราฟ H1 จะสูญเสียเงินก้อนใหญ่ในไม้เดียว ทำให้ Max Drawdown ร่วงลงไปถึง -31%
2. **Win Rate สู้ Risk/Reward ไม่ได้:** แม้ Win Rate จะสูงถึง 56% แต่กำไรตอนชนเส้นกลาง (Take Profit) ของกราฟ H1 นั้นน้อยกว่าระยะขาดทุนตอนโดนเทรนด์ลาก (Stop Loss)

## Verification
- หากผู้ใช้จะนำอัลกอริทึมนี้ไปทำเงินจริง การใช้กลยุทธ์ "Bollinger Band + RSI" แบบพื้นฐาน (Vanilla Strategy) บนคู่ EURUSD **ยังไม่สามารถอยู่รอดได้ในระยะยาว**
- ต้องเพิ่ม "ฟิลเตอร์" หรือ "ตัวกรองโครงสร้างราคา (Price Action Confirmation)" เช่น คอนเฟิร์มการกลับตัวด้วยแท่งเทียน Pinbar หรือ Engulfing ก่อนเข้าเทรด เพื่อลดจำนวนครั้งที่แพ้ลงให้ได้อีก