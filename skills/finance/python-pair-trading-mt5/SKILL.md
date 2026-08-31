---
name: python-pair-trading-mt5
description: "สถาปัตยกรรมและสมการสร้างบอท Pair Trading (Statistical Arbitrage) บน MT5 ด้วย Python"
version: 0.1.0
metadata:
  hermes:
    tags: [MT5, Python, EA, Pair Trading, Arbitrage, Quantitative]
---

# สถาปัตยกรรมบอท Pair Trading บน MT5 ด้วย Python

สกิลนี้อธิบายแก่นของการสร้างบอทประเภท **Pair Trading (Statistical Arbitrage / Mean Reversion)** ซึ่งเป็นกลยุทธ์ที่ใช้หลักการทางสถิติเพื่อหากำไรจากส่วนต่างของสินทรัพย์ 2 ตัวที่ปกติมีความสัมพันธ์กัน (Correlation) แต่เกิดความคลาดเคลื่อนชั่วคราว (Divergence) สกิลนี้ครอบคลุม Indicator ที่ต้องใช้, สมการคำนวณ, และโครงสร้างโค้ด Python สำหรับดึงข้อมูลและยิงออเดอร์เข้า MT5

## When to Use

- "ต้องการสร้างบอท Pair Trading แบบ FarmedHedge"
- "หา Indicator ที่ใช้จับคู่เงิน (Correlation / Z-Score)"
- "การสร้างบอท Arbitrage หรือ Mean Reversion ใน Python"

## Quick Reference

- **Indicator 1: Pearson Correlation (Rolling)** — วัดความสัมพันธ์ (Sync Rate) ต้อง > 0.70 หรือ 70%
- **Indicator 2: Spread Z-Score** — วัดความถ่างของราคา (Farm Index)
  - `Z-Score > +2.0` = สินทรัพย์ A แพงไป (SELL A, BUY B)
  - `Z-Score < -2.0` = สินทรัพย์ A ถูกไป (BUY A, SELL B)
  - `Z-Score เข้าใกล้ 0` = จุด Take Profit

## การเตรียม Indicators และสมการคณิตศาสตร์ (The Math)

ในการทำ Pair Trading บน Python เราไม่ต้องใช้ Indicator ทั่วไปอย่าง RSI หรือ MACD แต่เราต้องสร้าง **Statistical Indicators** ของเราเองด้วย `pandas` และ `numpy`:

### 1. การหาความสัมพันธ์ (Rolling Correlation)
แทนค่าฟังก์ชัน "Sync Rate" วัดว่าสินทรัพย์ A และ B เคลื่อนไหวไปทางเดียวกันหรือไม่ในช่วง $N$ แท่งเทียนที่ผ่านมา (เช่น 50 แท่งของกราฟ H1)
```python
import pandas as pd

# สมมติ df มี column 'close_A' และ 'close_B'
df['Correlation'] = df['close_A'].rolling(window=50).corr(df['close_B'])
```
*เงื่อนไขการเทรด:* `df['Correlation'] > 0.70` (มีความสัมพันธ์กันสูง)

### 2. การหาระยะห่าง หรือ สเปรด (Spread & Hedge Ratio)
คำนวณส่วนต่างระหว่างสองสินทรัพย์ โดยปรับสัดส่วนความผันผวน (Hedge Ratio) มักใช้ OLS (Ordinary Least Squares) หรือคำนวณสัดส่วนธรรมดา:
```python
# หาระยะห่างพื้นฐาน
df['Spread'] = df['close_A'] - df['close_B']
```

### 3. การคำนวณ Z-Score (The Entry/Exit Signal)
แทนค่าฟังก์ชัน "Farm Index" เพื่อแปลงค่า Spread ให้อยู่ในรูปแบบค่ามาตรฐานที่วัดได้ว่า "ห่างจากค่าเฉลี่ยปกติไปกี่เปอร์เซ็นต์/กี่ SD"
```python
window = 50
spread_mean = df['Spread'].rolling(window=window).mean()
spread_std = df['Spread'].rolling(window=window).std()

# สมการ Z-Score: (ค่าปัจจุบัน - ค่าเฉลี่ย) / ค่าเบี่ยงเบนมาตรฐาน
df['Z_Score'] = (df['Spread'] - spread_mean) / spread_std
```

## สถาปัตยกรรมการเทรด (Trading Logic Architecture)

ระบบจะจับคู่ 2 สินทรัพย์ (ตัวอย่าง: `EURUSD` และ `GBPUSD`) และเฝ้าดูค่า Z-Score:

1. **ENTRY SHORT SPREAD (Z-Score ทะลุ +2.0):**
   - ความหมาย: Spread กว้างเกินไป (EURUSD แพงกว่าปกติเมื่อเทียบกับ GBPUSD)
   - *Action:* ยิงคำสั่ง **SELL EURUSD** และ **BUY GBPUSD** พร้อมกัน (Lot เท่ากันหรือตามอัตราส่วน)

2. **ENTRY LONG SPREAD (Z-Score หลุด -2.0):**
   - ความหมาย: Spread แคบเกินไป (EURUSD ถูกกว่าปกติเมื่อเทียบกับ GBPUSD)
   - *Action:* ยิงคำสั่ง **BUY EURUSD** และ **SELL GBPUSD** พร้อมกัน

3. **TAKE PROFIT (Mean Reversion):**
   - *Action:* เมื่อ `Z-Score` วิ่งกลับมาเข้าใกล้ `0` (เช่น -0.5 ถึง +0.5) ให้ยิงคำสั่งปิดออเดอร์ทั้ง 2 ตัวทิ้งทันที รับกำไรจากส่วนต่าง

4. **STOP LOSS (Risk Management):**
   - *Action:* หาก `Z-Score` ถ่างออกไปรุนแรงจนทะลุ ±4.0 หรือ `Correlation` ร่วงหลุด 0.5 (แปลว่าความสัมพันธ์พังทลาย หุ้นสองตัวไม่วิ่งตามกันแล้ว) ให้ Cut Loss ออเดอร์ทั้งหมดเพื่อป้องกันพอร์ตแตก

## ข้อควรระวังในการทำ Pair Trading (Pitfalls)

- **Leg Risk:** ขาของออเดอร์อาจเข้าไม่พร้อมกัน (Slippage) หากใช้ `mt5.order_send` ให้ยิงขาที่สภาพคล่องต่ำกว่าก่อนเสมอ หรือเขียนระบบ Retry
- **Timeframe:** Pair Trading เป็นกลยุทธ์กินรอบความผันผวน ควรใช้ Timeframe ตั้งแต่ **H1, H4, หรือ D1** ขึ้นไป การใช้ M1 หรือ M5 มักเจอปัญหา Noise และค่าคอมมิชชั่น/Spread ของโบรกเกอร์กินกำไรหมด
- **Swap / Rollover:** การถือออเดอร์ข้ามคืน (2 ขา) จะโดนค่า Swap สองเด้ง หากถือแช่นานเกินไป ค่า Swap จะกินกำไรส่วนต่างหมด ควรมี Time-based Stop Loss

## Verification

หากต้องการนำไปเขียนโค้ด ให้ดูไฟล์ `templates/pair_trading_engine.py` ในสกิลนี้ ซึ่งแสดงโครงสร้างคลาส Python ในการจัดการ 2 สินทรัพย์ คำนวณ Z-Score และยิงคำสั่งขนานผ่าน `mt5linux`