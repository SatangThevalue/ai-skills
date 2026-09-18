---
name: mql5-onnx-production-architecture
description: "สถาปัตยกรรมการออกแบบ MQL5 (MT5 EA) ระดับ Production สำหรับรัน ONNX Model (แยก Inference ออกจาก Training)"
---

# MQL5 ONNX Production Architecture

สถาปัตยกรรมและโครงสร้างโค้ดสำหรับเขียน MQL5 (EA) ระดับ Production โดยมีหัวใจสำคัญคือ:
**"Python = Training Engine, MT5 = Inference & Execution Engine"**
ห้ามเอาตรรกะการเทรน หรือการคำนวณที่ซับซ้อนมาฝังใน MT5 โมเดลมีหน้าที่แค่บอกความน่าจะเป็น (Probability) ส่วนการตัดสินใจเปิดออเดอร์ต้องผ่านการคัดกรองจากชั้นอื่นๆ ใน EA อีกหลายด่าน

---

## 📦 1. สิ่งที่ต้อง Export จาก Python (ห้าม Export แค่โมเดล!)

การนำ AI ลง MT5 ที่ถูกต้อง ต้องดึงไฟล์จาก Python มา 4 ไฟล์เสมอ:
1. **`model.onnx`:** ตัวโมเดล (เช่น LightGBM, XGBoost, RandomForest) ที่ถูกแปลงแล้ว
2. **`feature_order.json`:** ลำดับของ Feature ที่เข้าโมเดล (MT5 ต้องคำนวณและเรียง `float[]` ให้ตรงกัน 100%) หรืออาจอยู่ในไฟล์ metadata รวม
3. **`feature_registry.json` / `feature_metadata.json`:** เก็บ Metadata เช่น ค่า Mean/Std (สำหรับ StandardScaler) หรือค่า Min/Max ของแต่ละฟีเจอร์, Formula, Dtype เพื่อให้ MT5 ทำ Normalize ข้อมูลได้ตรงกับตอน Train 100%
4. **`model_config.json`:** เก็บ Metadata (เช่น Model Version, Signal Threshold)

---

## 🏗️ 2. MQL5 Modular Architecture

ใน MQL5 ห้ามเขียนทุกอย่างรวมกันใน `OnTick()` ต้องแยกออกเป็น 7 Layers:

```text
EA (Expert Advisor)
│
├── Data Layer       (อ่านราคา OHLC, Tick Volume, Spread)
├── Feature Layer    (สกัด RSI, ADX, ATR, BB_WIDTH ให้เหมือน Python 100%)
├── ONNX Layer       (โหลด model.onnx -> คืนค่า Prediction 0.0 - 1.0)
├── Signal Layer     (แปลง 0.84 = BUY, 0.12 = SELL)
├── Risk Layer       (เช็ค Drawdown, Spread, ข่าว)
├── Execution Layer  (สั่ง Market Order, คำนวณ TP/SL)
└── Monitor Layer    (Logging ค่า Prediction และ Trade)
```

### The Signal Layer (จุดสับสวิตช์ความแม่นยำ)
ห้ามใช้ `0.5` เป็นเส้นแบ่ง Buy/Sell เด็ดขาด หรือให้ Output ออกมาเป็น Action BUY/SELL ตรงๆ ควรให้ Output เป็น Probability เสมอ แล้วตัดสินใจด้วย Threshold:
- `Prediction > 0.75` ➔ **BUY**
- `Prediction < 0.25` ➔ **SELL**
- `0.25 - 0.75` ➔ **NO TRADE**

---

## ⚙️ 3. การออกแบบ MT5 Settings (Inputs)

EA ระดับสถาบันต้องมี Parameter ให้ปรับครบ 6 หมวดหลัก (สามารถนำไปเขียนเป็น `input` หรือ `sinput` ใน MQL5 ได้เลย):

### 1. กลุ่ม Model & Signal
- `ModelPath`: `model.onnx`
- `EnableONNX`: `true`
- `BuyThreshold`: `0.75`
- `SellThreshold`: `0.25`

### 2. กลุ่ม Position Sizing & ATR
- `RiskPercent`: `1.0` (เสี่ยง 1% ของทุน)
- `UseATRSizing`: `true`
- `ATRPeriod`: `14`
- `ATRMultiplierSL`: `1.5` (SL = 1.5 ATR)
- `ATRMultiplierTP`: `3.0` (TP = 3.0 ATR)

### 3. กลุ่ม Risk Engine (Kill Switches)
- `MaxDailyLoss`: `3%`
- `MaxDrawdown`: `10%`
- `MaxSpread`: `30`
- `MaxConsecutiveLoss`: `5`

### 4. กลุ่ม Session & News Filter
- `TradeLondon` / `TradeNewYork` / `TradeAsia`: `true/false`
- `EnableNewsFilter`: `true`
- `MinutesBeforeNews`: `60`
- `MinutesAfterNews`: `30`

### 5. กลุ่ม Regime (สับสวิตช์ตามสภาวะ)
- `EnableRegime`: `true`
- `TrendOnly` / `RangeOnly`: `true/false`

### 6. กลุ่ม Portfolio
- `MaxExposure`: `20%` (ห้ามถือครองสินทรัพย์รวมเกิน)
- `MaxSymbolExposure`: `5%`

---

## 🔒 4. Trade Execution Logic (ลอจิกการเข้าเทรดจริง)

### การคัดกรองความน่าจะเป็น (Feature Validation & Signal Logic)

ก่อนรัน Predict ให้มั่นใจว่าข้อมูลไม่พังเด็ดขาด **(ถ้า Feature หาย ห้ามเติม 0 สุ่มสี่สุ่มห้า):**
- ตรวจสอบ `ArraySize(features) != 8` (ขนาดอาร์เรย์ต้องตรงกับตอน Train เป๊ะ)
- ตรวจหาค่า `NaN`, `INF`, `Missing` ก่อนส่งเข้า ONNX เสมอ (ถ้ามีให้ทิ้ง `return;` ทันที)

**แนวทางการทำ Data Cleaning (Quant Professional):**
- **ฝั่ง Training (Python):** `NaN` ➔ ทิ้ง (Drop), `INF` ➔ Replace เป็น `NaN` แล้ว Drop, `Outlier` ➔ Winsorize (บีบค่าให้อยู่ในกรอบ)
- **ฝั่ง MQL5:** `Create Features` ➔ `Validate Features` ➔ `Scaling` ➔ `ONNX` ➔ `Prediction` *(ดูตัวอย่างโค้ด MQL5 สำหรับ Feature Validation และ RobustScaler ได้ที่สกิล `quant-data-cleaning-and-scaling`)*

เมื่อรัน `OnnxRun()` แล้วได้ค่าความน่าจะเป็น `prob_buy` ออกมา เราจะไม่ให้ ONNX ตัดสินใจเปิดออเดอร์เอง ให้สับสวิตช์ความแม่นยำที่ **Signal Layer**:

```cpp
if(prob_buy > 0.75) {
   Signal = BUY;
} else if(prob_buy < 0.25) {
   Signal = SELL;
} else {
   Signal = NO_TRADE;
}
```

และออเดอร์จะถูกยิงเข้าโบรคเกอร์ได้ **ต้องผ่านครบทุกเงื่อนไขความเสี่ยง (AND) เท่านั้น:**

```text
Prediction Signal Passed (BUY / SELL)
   AND
Spread < 30 (Risk Layer)
   AND
No News (News Filter)
   AND
Risk Engine Passed (ยังไม่ชน Daily Loss / Drawdown limit)
```

---

## 📉 5. ข้อมูลและฟีเจอร์ (The Data Contract)

จุดที่พลาดกันมากที่สุดคือการคิดว่า Export Model ไปแล้วใช้งานได้เลย

**Rule สำคัญ:** Feature ใน MT5 ต้องคำนวณด้วย Logic เดียวกับ Feature ใน Python 100% ห้ามใช้ Indicator จากต่าง Source ที่คำนวณไม่เหมือนกัน

### Feature Layers
- **Layer 1 Raw Data:** Open, High, Low, Close, Volume, Spread (ดึงจาก MT5)
- **Layer 2 Indicators:** EMA20, EMA50, RSI14, ATR14, ADX14 (สร้างให้เหมือน Python)
- **Layer 3 Derived Features:** `EMA20_50_GAP`, `ATR_RATIO`, `RSI_DISTANCE`, `TREND_SCORE` (แนะนำให้ส่ง Feature แบบนี้เข้าโมเดล แทนที่จะส่ง Indicator เปล่าๆ)
- **Layer 4 Normalization:** สำคัญมาก ต้อง Normalize ด้วยค่าจากตอน Train (เช่น Export ค่า Mean, Std จาก StandardScaler) ตัวอย่าง JSON: `{"atr_ratio": {"mean":1.05, "std":0.21}}`

**Input ของ ONNX** ไม่ควรเป็น OHLC ตรงๆ แต่ควรเป็น Feature Vector เช่น:
`[ atr_ratio, volume_ratio, bb_width, trend_score ]` -> `[ -0.0021, 0.0043, 67.5, 1.32 ]`

### การจัดการการคำนวณฟีเจอร์
- **V1:** คำนวณทุกอย่าง (RSI, ATR, ADX, Returns) ใน MT5 เอง (ง่ายที่สุด)
- **V2:** เพิ่ม Config File (เช่น `feature_order.json`) ให้ MT5 อ่านและจัดเรียงฟีเจอร์ให้ตรงตามลำดับ
- **V3:** สร้าง Shared Feature Engine (เช่น สร้าง Script Python เพื่อ Generate MQL5 Code อัตโนมัติจาก Spec `feature_registry.json` ที่ระบุ formula, dtype, order)

---

## 📈 6. Logging ที่ EA ต้องทำ (เพื่อใช้วิเคราะห์ Data Drift)

- **ทุก Prediction:** `timestamp, model_version, prediction, rsi, adx, atr, spread, signal`
- **ทุก Order:** `entry, sl, tp, atr, confidence, position_size`

---

## 🚀 7. Roadmap การปล่อย EA (Versioning)

คำแนะนำที่ดีที่สุดสำหรับ Quant Architect คือ **อย่าเพิ่งทำท่ายากตั้งแต่วันแรก** เริ่มต้นง่าย ๆ เพื่อป้องกัน Feature Mismatch ระหว่าง Python กับ MT5 แล้วค่อยเพิ่มความซับซ้อน:

- **การจัดการกับ Infrastructure:** ห้ามรัน MT5 บน Linux Docker (WINE Overhead) การพยายามจำลอง WINE บน Docker เพื่อรัน MT5 จะทำให้เกิดคอขวดทรัพยากร (กิน RAM หนักและเพิ่ม Latency การเทรด) ให้ใช้สถาปัตยกรรม **"แยกเซิร์ฟเวอร์ (Separation of Concerns)"**: วาง Python/MLOps Pipeline ไว้บน Linux VPS และนำไฟล์ `.onnx` ไปใส่ในโปรแกรม MT5 ที่ติดตั้งบน Windows VPS แยกต่างหาก

- **EA V1 (MVP):** `LightGBM` + `No Scaler (ไม่ทำ Normalize)` + `Feature Validation` + `ONNX` + `Simple Signal Threshold`
- **EA V2 (Smart Standalone EA):** 
  - นำ `RobustScaler` มาใช้ (เพิ่ม Scaler config) + `30-50 Features` + `Regime Detection` + `ATR Position Sizing`
  - ให้ EA โหลดข้อมูลการตั้งค่าแบบ Dynamic จาก JSON (เช่น โหลด Threshold และจำนวน Features จาก `model_config.json` และ `feature_order.json`) โดยตรง เพื่อปิดช่องโหว่ Human Error ตอนอัปเดตโมเดล
  - ใส่ **Standalone News Filter** ฝังในตัว EA ให้ยิง API ดึงปฏิทินข่าวด้วยตัวเอง แล้วจัดการเวลา `TimeCurrent() - TimeGMT()` เพื่อเลี่ยงความผันผวนช่วงข่าวแรงๆ โดยไม่ต้องพึ่งเซิร์ฟเวอร์หลังบ้าน
  - *แนะนำ:* ให้ลองสร้าง Feature Version ใหม่เทียบกันใน MLflow (เช่น `FS_V1=No Scaler` เทียบกับ `FS_V2=RobustScaler`) จะพิจารณาอัปเกรดเป็น RobustScaler ก็ต่อเมื่อผล Walk Forward ยืนยันชัดเจนว่า **Sharpe, Profit Factor, Drawdown, และ Stability** มีค่าดีกว่า V1 เท่านั้น (อย่าใช้เพียงเพราะเขาบอกว่าเป็น Best Practice ทั่วไป)
- **V3 (ระดับสถาบัน):** `Portfolio Engine` + `Correlation Engine` + `Strategy Router`
- **V4 (Advanced):** `Meta-Labeling (Two-Stage Model)` + `Time-of-Day/Session Filters` + `Alternative Data (Funding Rates)` สำหรับสินทรัพย์ปราบเซียนอย่างกราฟ 15m, GOLD, และ BTC

---

## 🏆 The Ultimate Final Architecture 

เพื่อให้ภาพทั้งหมดของการสับเปลี่ยนระหว่าง Python (Training) ไปสู่ MT5 (Execution) สมบูรณ์แบบ นี่คือสถาปัตยกรรมที่ Quant Architect แนะนำ:

```text
======================================
               PYTHON
======================================
Raw Data
    ↓
Feature Engineering
    ↓
LightGBM
    ↓
Optuna
    ↓
MLflow
    ↓
Export
    │
    ├── model.onnx
    ├── feature_order.json
    ├── scaler.json
    └── model_config.json

======================================
               MT5
======================================
OHLCV
    ↓
Feature Engine
    ↓
Normalization
    ↓
ONNX Runtime
    ↓
Probability (e.g., 0.85)
    ↓
Signal Threshold Filter
    ↓
Risk Engine
    ↓
Position Sizing (ATR + Confidence)
    ↓
Execution Engine
    ↓
Order
```

> **บทสรุป:** การใช้ **ONNX Runtime ภายใน MQL5 โดยตรง** ดีกว่าการใช้ Python API เชื่อมเข้า MT5 มาก เพราะเสถียร, Latency ต่ำ, Deploy ง่าย (โยนไฟล์เข้า VPS จบเลย) และเหมาะกับระบบ `LightGBM + Optuna + MLflow + MT5` ที่เราออกแบบมาตั้งแต่ต้นมากที่สุดครับ