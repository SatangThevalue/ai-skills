---
name: market-regime-detection-quant
description: "สถาปัตยกรรมและเทคนิคการสร้าง Market Regime Detection สำหรับระบบ AI Trading เพื่อแก้ปัญหาโมเดลขาดทุนเมื่อสภาวะตลาดเปลี่ยน"
---

# Market Regime Detection ใน Quant Trading

Market Regime Detection (การตรวจจับสภาวะตลาด) เป็นหนึ่งในแนวคิดที่สำคัญที่สุดของ Quant Trading สาเหตุที่ AI Trading จำนวนมากล้มเหลว ไม่ใช่เพราะโมเดลไม่ดี แต่เป็นเพราะ **"ตลาดเปลี่ยน แต่โมเดลไม่เปลี่ยน"** 

ไม่มี Strategy ไหนชนะทุกสภาวะตลาด เช่น EMA Crossover ทำกำไรได้ดีใน Trending Market แต่ขาดทุนยับเยินใน Sideway Market ดังนั้น "ก่อนใช้โมเดล ต้องรู้ก่อนว่าตลาดอยู่ Regime ไหน"

---

## 5 Regime หลักที่ใช้ในตลาดการเงิน (Framework แนะนำ)

แทนที่จะแบ่งแค่ Trend กับ Range ขอแนะนำให้แบ่ง Regime ออกเป็น 5 กลุ่ม:

1. **R1 = Strong Uptrend:** ADX > 30, EMA20 > EMA50 > EMA200, RSI > 60
2. **R2 = Strong Downtrend:** ADX > 30, EMA20 < EMA50 < EMA200, RSI < 40
3. **R3 = Sideway:** ADX < 20, BB Width ต่ำ, EMA Flat
4. **R4 = High Volatility:** ATR Ratio > 1.5, BB Width สูง, Volume Spike
5. **R5 = Low Volatility:** ATR Ratio < 0.7, BB Width ต่ำ, Volume ต่ำ

---

## 4 ระดับของการสร้าง Regime Detection

### Level 1: Rule-Based (ง่ายที่สุด)
ใช้ Indicator พื้นฐานกำหนดตายตัว
- `ADX > 25` = Trend
- `ADX < 20` = Range
- `ATR > ATR_Mean` = High Volatility
- *ข้อดี:* ง่าย, เร็ว, อธิบายได้ / *ข้อเสีย:* แข็งทื่อเกินไป ปรับตัวไม่ได้

### Level 2: Statistical Regime
ใช้สถิติ เช่น Rolling Standard Deviation ของ Volatility หรือ Return แล้วแบ่งกลุ่ม (เช่น High Vol vs Low Vol)

### Level 3: Clustering (Machine Learning)
ใช้ Unsupervised Learning เช่น **KMeans**, **Gaussian Mixture Model (GMM)**, หรือ **HDBSCAN**
- ใส่ Feature (ATR, RSI, ADX, Return, Volume) ปล่อยให้ AI แบ่งกลุ่มเอง
- *ผลลัพธ์:* Cluster 1 = Trend, Cluster 2 = Sideway, Cluster 3 = High Vol

### Level 4: Hidden Markov Model (HMM) - ระดับ Quant Fund
ใช้ HMM ค้นหา Hidden State จากพฤติกรรมของราคา (เรามองไม่เห็น Regime โดยตรง แต่เห็นราคาเคลื่อนไหว)
- *ผลลัพธ์:* AI จะประเมิน State A (Trend), State B (Range), State C (Crash) ออกมาเป็นความน่าจะเป็นแบบ Real-time

---

## Architecture การวางระบบที่แนะนำ

ระบบ AI ทั่วไปมักเป็น: `Price` → `LightGBM` → `Signal` (พังง่าย)
**ระบบที่แนะนำควรเป็น:**

```text
Price
 ↓
Regime Detector
 ↓
 ├─ Trend Model (Model_Trend.onnx)
 ├─ Range Model (Model_Range.onnx)
 └─ High Vol Model (Model_HighVol.onnx)
 ↓
 Signal
```

### Feature ที่แนะนำสำหรับ Regime Detector (25 ตัวที่ควรเริ่มทำ V1)

หากต้องสร้าง V1 แนะนำให้ใช้ Indicator ตาม "หน้าที่" ของมัน (Trend + Volatility + Momentum + Market Structure + Liquidity) ดังนี้:

**Group 1: Trend Indicators (ใช้วัดความแข็งแกร่ง)**
- `ADX14`, `ADX21` (ADX < 20 = Range, ADX > 40 = Very Strong Trend)
- `EMA20`, `EMA50`, `EMA200`
- `EMA20-EMA50 Gap`, `EMA50-EMA200 Gap` (ถ้าเรียงตัวสวย = Strong Trend)

**Group 2: Volatility Indicators (สำคัญมากในการจับ Regime)**
- `ATR14`, `ATR50`
- `ATR Ratio` (ATR14 / ATR100) -> >1.5 = High Vol, <0.7 = Low Vol
- `BB Width` (ขยาย = Market Expansion, หด = Market Compression)

**Group 3: Momentum Indicators**
- `RSI14`, `RSI28` (RSI > 60 = Bullish Momentum, < 40 = Bearish Momentum)
- `MACD`, `MACD Histogram` (Histogram เพิ่ม = Momentum Strengthening)

**Group 4: Market Structure (คนส่วนใหญ่มองข้าม)**
- `HH / HL / LH / LL` (Higher High / Higher Low) 

**Group 5: Volume (ใน Forex ใช้ Tick Volume แทน)**
- `Volume Ratio` (current_volume / avg_50_volume) -> >1.5 = High Participation

**Group 6: Multi Timeframe Regime (มีประโยชน์มาก)**
- `H1 RSI`, `H4 RSI`, `D1 RSI`
- `H1 ADX`, `H4 ADX`, `D1 ADX`

---

## 5 ตัวท็อปที่สำคัญที่สุด (Top 5 Priority)

ถ้าต้องเลือกแค่ 5 ตัวแรกสำหรับ Regime Detection แนะนำ:
1. **ADX(14):** จับความแข็งแกร่งของ Trend ได้ดีที่สุด
2. **ATR Ratio:** จับ Volatility ได้ชัดเจน
3. **EMA20-EMA50 Gap:** บอกทิศทางและกำลังของเทรนด์
4. **Bollinger Band Width:** จับการบีบตัวและระเบิดของราคา
5. **Volume Ratio:** จับความสนใจและการเข้ามาของรายใหญ่ (Participation)

เพราะ 5 ตัวนี้รวมความสำคัญครบทั้ง Trend, Volatility และ Participation ซึ่งเพียงพอสำหรับสร้าง V1 ที่ใช้งานได้จริงก่อนขยับไปทำ HMM ในอนาคต

---

## วิธีวัดผล Regime Detector

อย่าวัดที่ Classification Accuracy ของการทาย Regime แต่อย่างเดียว ให้วัด **"Model Performance แยกตาม Regime"** (เช่น Profit Factor)

| Regime | Profit Factor |
|----------|-------------|
| Trend | 2.1 |
| Range | 1.7 |
| High Vol | 1.5 |

> ถ้าระบบรวมกันได้ PF = 1.2 แต่พอแยก Regime แล้วดึงเฉพาะโมเดลที่ถูกจังหวะมาใช้ จน PF รวมขึ้นเป็น 1.8 แสดงว่า Regime Detector มีประโยชน์จริง

---

## Roadmap การพัฒนา Regime Detection

- **Version 1:** `Rule-Based` (ADX + ATR)
- **Version 2:** `KMeans` (หา Regime อัตโนมัติด้วย Unsupervised Learning)
- **Version 3:** `Hidden Markov Model (HMM)` (ระดับสถาบัน)
- **Version 4:** `Regime-specific LightGBM` (แยก 1 โมเดล ต่อ 1 Regime ชัดเจน)
- **Version 5:** `Meta Model` (AI เรียนรู้และเลือกเองว่าจะน้ำหนักไปทางโมเดลไหน)

---

## ลำดับความสำคัญในการออกแบบระบบ MT5 + ONNX

เมื่อจะสร้างระบบจริง โครงสร้างที่ Quant ขาดไม่ได้คือ:
`Market Data` → `Regime Detector` → `Feature Gen` → `LightGBM Ensemble` → `Risk Engine` → `Position Sizing` → `Execution`

**Priority ที่ควรทำตามลำดับ:**
1. Feature Engineering
2. Train LightGBM
3. Walk Forward Testing
4. Risk Engine
5. Position Sizing
6. **Market Regime Detection**
7. Ensemble Model
8. Auto Retraining

> เมื่อคุณทำมาถึงข้อ 6 (Regime Detection) ผลลัพธ์มักก้าวกระโดดอย่างชัดเจน เพราะระบบ "รู้ว่าตัวเองควรใช้กลยุทธ์ไหนในตลาดแบบใด" แทนที่จะดันทุรังใช้โมเดลเดียวกับทุกสภาวะตลาด