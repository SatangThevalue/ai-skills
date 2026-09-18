---
name: quant-concept-drift-position-sizing
description: "เจาะลึกความสัมพันธ์ระดับสถาบัน: Market Regime, Concept Drift, Position Sizing, Risk Engine และ Walk Forward Validation (Top 5 Quant Platform)"
---

# ระบบ 5 แกนหลักเพื่อความอยู่รอดของ Quant Model (Top 5 Quant Platform)

การสร้าง AI หรือ Quant Model ที่มีแม่นยำแค่ 55-60% ก็สามารถรอดและทำกำไรใน Production ได้ หากมี 5 เสาหลักนี้ทำงานร่วมกันอย่างเป็นระบบ:

1. **Walk Forward Validation**
2. **Risk Engine**
3. **Position Sizing**
4. **Concept Drift Monitoring**
5. **Execution Engine**

---

## 1. Monitor Concept Drift อย่างไร?

ก่อนอื่นต้องแยกประเภทของการเปลี่ยนแปลงข้อมูลก่อน:

### Data Drift
เป็นการตรวจสอบว่า **Distribution (การกระจายตัวของข้อมูล) เปลี่ยนไหม?**
เช่น ในอดีตค่าเฉลี่ยของ RSI อยู่ที่ 50 แต่ปัจจุบันขยับไปที่ 70

*   **เครื่องมือวัดผล:** PSI (Population Stability Index), KS Test, Jensen Shannon Divergence

### Concept Drift (อันตรายที่สุด)
เป็นการตรวจสอบว่า **ความสัมพันธ์ระหว่าง Feature กับ Target เปลี่ยนไหม?**
เช่น 
*   **อดีต:** เมื่อ RSI > 70 ทิศทางราคาจะปรับตัว "ลง"
*   **ปัจจุบัน:** เมื่อ RSI > 70 ทิศทางราคากลับปรับตัว "ขึ้นต่อ"

---

### เครื่องมือที่แนะนำในการทำ Monitoring

#### 1. Evidently (⭐⭐⭐⭐⭐ แนะนำมากที่สุด)
*   **ติดตั้ง:** `pip install evidently`
*   **ใช้ตรวจ:** Data Drift, Target Drift, Prediction Drift
*   **ข้อดี:** Dashboard สวยงาม, Integration ง่าย, ใช้ร่วมกับ MLflow ได้ดีเยี่ยม

#### 2. NannyML (⭐⭐⭐⭐⭐)
*   **เครื่องมือที่ออกแบบมาเพื่อ Concept Drift โดยเฉพาะ**
*   **ติดตั้ง:** `pip install nannyml`
*   **ความสามารถหลัก:** สามารถตรวจ Performance Degradation ได้ล่วงหน้า แม้จะยังไม่มี Label หรือผลเฉลยจริงเกิดขึ้น
*   **เหมาะกับ:** สินทรัพย์อย่าง Forex, Stocks, Crypto ที่ต้องรอผลลัพธ์ในอนาคต

#### 3. Custom Champion-Challenger (ใช้งานจริงบ่อยที่สุด)
*   **แนวคิด:** เปรียบเทียบ **Production Model (Champion)** VS **Latest Model (Challenger)**
*   **ตัวชี้วัด:** เปรียบเทียบ Profit Factor (PF), Sharpe Ratio, Expected Value อย่างต่อเนื่อง
*   **Promotion Rule:** หาก New Model ทำผลงานได้ดีกว่าคงที่ตลอดระยะเวลา 3-4 Walk Forward Window ถึงจะ Promote ขึ้นเป็น Production Model

### Dashboard Concept Drift ที่ควรมี
ควรติดตาม Metric เหล่านี้:
1. RSI PSI
2. ATR PSI
3. Volume PSI
4. Prediction Distribution
5. Trade Win Rate
6. Profit Factor
7. Sharpe Ratio

> **🚨 Trigger Retrain Alert:** 
> ควรสั่ง Retrain เมื่อค่า **PSI > 0.25** และ **Profit Factor ลดลง > 20%** พร้อมกัน

---

## 2. Risk Engine (ด่านสุดท้าย)

นี่คือด่านสุดท้ายในการคัดกรองคำสั่งซื้อขาย ก่อนส่ง Order เข้าสู่ Execution Engine และ Broker ตาม Architecture ดังนี้:

`ONNX (Signal)` → `Position Sizing` → **`Risk Engine`** → `Execution` → `Broker`

### กฎการคัดกรองคำสั่งของ Risk Engine
*   **Rule 1: Daily Loss Limit** (จำกัดขาดทุนรายวัน) เช่น หากกำหนดไว้ที่ 3% ของทุน 100,000 = ถ้าขาดทุนถึง 3,000 ให้ **STOP TRADING**
*   **Rule 2: Max Drawdown** เช่น 10% หาก Equity Peak = 120,000 แล้ว Current Equity ลดลงเหลือ 107,000 (DD = 10.8%) ให้ **Disable New Trade** ทันที
*   **Rule 3: Spread Filter** ตรวจจับความห่างของ Spread เช่น ค่าเฉลี่ย 12 Points หากปัจจุบัน 40 Points ให้ **Reject Trade**
*   **Rule 4: News Filter** หลีกเลี่ยงความผันผวนจากข่าวสำคัญ เช่น ก่อนข่าว NFP, CPI, FOMC ให้งดเปิด Order อย่างน้อย 60 นาที
*   **Rule 5: Correlation Risk** ป้องกันความเสี่ยงพอร์ตกระจุกตัว (Portfolio Exposure) เช่น การถือ EURUSD, GBPUSD, AUDUSD ในฝั่ง BUY พร้อมกัน หมายความว่ามีความเสี่ยงในหน้า Long USD สูงมาก 
*   **Rule 6: Max Open Trades** จำกัดจำนวนไม้ที่เปิดพร้อมกัน เช่น ตั้งไว้ 10 ไม้ หากเกินให้ **Reject**

> **💡 แนะนำเพิ่มเติม: การให้ Risk Score (0-100)**
> นำค่า Spread, Volatility, Exposure, และ Drawdown มาประมวลผล หาก **Risk Score = 90** ให้ตั้งสถานะเป็น **NO TRADE**

---

## 3. Position Sizing (ควรเปิดกี่ Lot?)

การคำนวณจำนวน Lot ที่เหมาะสม **ไม่แนะนำให้ใช้ Fixed Lot** แต่ควรใช้สมการแบบผสม:

**`Fixed Risk` + `ATR (Volatility)` + `ML Confidence`**

### Step-by-Step Sizing

*   **Step 1: กำหนดความเสี่ยง**
    *   ทุน = 100,000 | Risk = 1% | เสียได้ = 1,000
*   **Step 2: การใช้ ATR Stop**
    *   เช่น ATR = 20 pip | กำหนด SL = 1.5 × ATR | SL สุดท้าย = 30 pip
*   **Step 3: หา Lot Size เบื้องต้น (Base Lot)**
    *   **สูตร:** `Lot = Risk Amount / (SL × Pip Value)`
    *   ตัวอย่าง: `1000 / (30 × 50) = 0.67 Lot`
*   **Step 4: Confidence Adjustment (ปรับตามระดับความมั่นใจของโมเดล ONNX)**
    *   ONNX มั่นใจ 0.55 -> ลด 50% (0.5x)
    *   ONNX มั่นใจ 0.88 -> เพิ่ม 20% (1.2x)
    *   *Mapping Table ตัวอย่าง:*
        *   50-60% = 0.5x
        *   60-70% = 0.8x
        *   70-80% = 1.0x
        *   80-90% = 1.2x
        *   90%+ = 1.5x

**Position Sizing Formula ขั้นสุดท้าย:**
> `Final Lot` = `Base Risk Lot` × `Confidence Factor` ÷ `ATR Ratio`

---

## 4. Walk Forward Validation (สำคัญที่สุดใน Quant)

*   **กฎเหล็ก:** ห้ามใช้ `Random Split` (Train/Test Split แบบสุ่ม) ในอนุกรมเวลา (Time Series) เด็ดขาด
*   **หลักการ:** ต้องเป็นการเลื่อน Window ไปข้างหน้าตามเวลาจริง เพื่อจำลองสภาพการนำไปเทรดในตลาดสด (Live Trading Simulation) ให้สมจริงที่สุด