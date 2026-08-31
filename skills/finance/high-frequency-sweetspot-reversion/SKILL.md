---
name: high-frequency-sweetspot-reversion
description: "สูตรลับการปรับจูน Indicator เพื่อหา Sweet Spot (Win Rate ~70% + เทรดถี่) สำหรับ Daily Cashflow"
version: 0.1.0
metadata:
  hermes:
    tags: [Python, Backtest, Optimization, Mean Reversion, Sweet Spot, Cashflow]
---

# High Frequency Sweet Spot Reversion

สกิลนี้สาธิตวิธีการเขียนระบบ Backtest กลยุทธ์ Mean Reversion โดยใช้ `Backtesting.py` และการเขียน **Custom Objective Function** (การสร้างสมการเป้าหมายให้ AI) เพื่อค้นหาจุดสมดุล (Sweet Spot) ที่สามารถทำ Win Rate ได้สูงในระดับปลอดภัย (~70%) ในขณะที่ยังคงความถี่ในการเปิดออเดอร์ (High Frequency) เพื่อปั๊มกระแสเงินสดรายวัน (Daily Cashflow) ได้อย่างต่อเนื่อง

## When to Use

- "ใช่ปรับให้เหลือแค่ 70% ได้ไหม"
- "หาค่า Sweet Spot ของกลยุทธ์ Mean Reversion"
- เมื่อผู้ใช้ต้องการบอทที่มีความสมดุลระหว่าง Win Rate กับ จำนวนครั้งที่เทรด (Frequency)
- เมื่อต้องการสร้างบอทสไตล์ Scalping แบบรายวัน (Day Trade)

## Quick Reference

- **เป้าหมาย:** สั่ง AI ให้ `maximize=custom_objective`
- **Custom Objective:** บังคับ Win Rate ไว้ที่ `65% - 80%` และเน้นหาตัวที่ `Return * log(Trades)` สูงที่สุด
- **Indicator Stack:** Bollinger Bands (กางขอบ 1.8-2.2) + RSI (Oversold 30/35) + ADX (<25/30)
- **ผลลัพธ์ที่ได้:** Win Rate ลดลงมาเหลือประมาณ 56-70% แต่จำนวนครั้งที่เทรดเพิ่มขึ้นมหาศาล (เช่น 110 ครั้งใน 2 เดือน)

## Procedure (The Sweet Spot Logic)

เมื่อเราไม่ต้องการ Win Rate 100% (ที่ 2 ปีเทรดแค่ 4 ครั้ง) เราต้องคลายความเข้มงวดของระบบลง เพื่อให้เข้าเทรดได้ง่ายขึ้น โดยปรับดังนี้:

### 1. การคลายความเข้มงวดของ Indicator (Loosening Filters)
เปลี่ยนจากกราฟ H1 กลับมาใช้กราฟ **15 นาที (M15)** และปรับเงื่อนไขให้ยืดหยุ่นขึ้น:

```python
# 1. กรองเทรนด์: ขยับ ADX Limit จาก 20 เป็น 25 หรือ 30 (ยอมให้มีเทรนด์อ่อนๆ ได้)
if ADX > 25: return

# 2. กรองกรอบราคา: ขยับขอบ BB ลงมาแคบขึ้น (Deviation 1.8 - 2.2)
if Price < Lower_BB_1_8:

# 3. กรองความตึง: RSI ไม่ต้องรอต่ำ 15 ให้แค่ 30-35 ก็เข้าได้เลย
    if RSI(14) < 30:
        BUY()
```

### 2. การสร้างสมการเป้าหมายให้ AI (Custom Objective)
ในไลบรารี `Backtesting.py` เราไม่จำเป็นต้องเลือกแค่ `maximize='Win Rate [%]'` หรือ `maximize='Return [%]'` อย่างเดียว เราสามารถสร้างฟังก์ชันบังคับ AI ได้เอง:

```python
def custom_objective(stats):
    wr = stats['Win Rate [%]']
    trades = stats['# Trades']
    ret = stats['Return [%]']
    
    # บังคับว่า Win Rate ต้องอยู่ระหว่าง 65% ถึง 80% และต้องเทรดมากกว่า 10 ครั้ง
    if wr < 65 or wr > 80 or trades < 10:
        return -100 # ถ้าไม่ตรงเงื่อนไข ตัดคะแนนทิ้งไปเลย
        
    # ถ้าผ่านเงื่อนไข ให้เลือกตัวที่ (กำไร x จำนวนครั้งที่เทรด) สูงสุด
    return ret * np.log(trades if trades > 1 else 1)

# ตอนรัน optimize เรียกใช้ฟังก์ชันนี้
stats = bt.optimize(..., maximize=custom_objective)
```

## ผลลัพธ์จากการ Optimization เชิงลึก (EURUSD M15, 60 วันล่าสุด)

เมื่อเราคลายเงื่อนไข และสั่งให้ AI ค้นหาด้วยสมการใหม่ (เปรียบเทียบจากตัวเลือก 48 รูปแบบ) พบว่าชุด Parameter "Sweet Spot" ที่ปั๊ม Cashflow ได้ดีที่สุดในช่วงที่ผ่านมาคือ:

- `n=15` (Period ของ BB และค่าเฉลี่ย)
- `dev=1.8` (ขอบ BB แคบลงมาก ทำให้ราคาแตะขอบบ่อยขึ้น)
- `adx_limit=25` (ยอมให้ตลาดมีเทรนด์อ่อนๆ ได้)
- `rsi_oversold=30` / `rsi_overbought=65` (เข้าเทรดง่ายขึ้น)

### Trade-off ที่เกิดขึ้น (สิ่งที่ได้ vs สิ่งที่เสียไป)

*   **สิ่งที่ได้ (Frequency):** บอทสามารถจับจังหวะเทรดได้ถึง **110 ครั้ง ภายในเวลาเพียง 60 วัน** (เฉลี่ยเทรดเกือบทุกวัน วันละ 2-3 รอบ) เหมาะกับการทำ Cashflow
*   **สิ่งที่เสีย (Accuracy & Profit):** Win Rate ตกลงมาอยู่ที่ระดับประมาณ **56%** (AI พยายามดันให้ถึง 65% ตามเป้าหมายแล้ว แต่สภาวะตลาด 2 เดือนล่าสุดนี้เอาไม่อยู่จริงๆ) ประกอบกับพอร์ตโดนค่าธรรมเนียม (Commission) กัดกินไปถึง 219 ดอลลาร์ ทำให้ผลตอบแทนสุทธิออกมาราวๆ เสมอตัว (-0.17%)

## Pitfalls (หลุมพรางของ High Frequency)

- **Commission & Spread:** ศัตรูที่น่ากลัวที่สุดของการเทรดถี่ๆ (Scalping) ไม่ใช่ตลาด แต่เป็น "ค่าธรรมเนียมของโบรกเกอร์" ยิ่งคุณเทรดบ่อย โบรกเกอร์ยิ่งรวย ระบบนี้จึงจะเวิร์กก็ต่อเมื่อคุณใช้บัญชีประเภท **Zero Spread หรือ Raw Spread** (ค่าคอมฯ ต่ำมากๆ) เท่านั้น
- **Market Noise:** การลงมาเล่นใน Timeframe M15 คุณจะเจอกับความผันผวนหลอกๆ (Whipsaw) จำนวนมาก ซึ่งทำให้ชน Stop loss ได้ง่ายกว่ากราฟใหญ่

## Verification
เมื่อใช้การตั้งค่าแบบ Sweet Spot ผู้ใช้งานควรจะต้องนำผลลัพธ์ไปทดสอบ (Forward Test) ใน Demo Account ของโบรกเกอร์ที่จะใช้งานจริงเสียก่อน เพื่อดูว่า Commission และ Slippage จริงในตลาด กระทบกับกลยุทธ์นี้มากน้อยเพียงใด