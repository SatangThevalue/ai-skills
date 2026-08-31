---
name: mql5-onnx-architecture-th
description: "คู่มือและโครงสร้างสถาปัตยกรรม การนำโมเดล AI (ML/DL) มาใช้งานบน MetaTrader 5 ผ่าน ONNX สำหรับสาย AI/Big Data"
---

# การทำงานของ MQL5 / MT5 กับโมเดล ONNX (AI, ML, DL)

MetaTrader 5 (MT5) และภาษา MQL5 สามารถโหลดโมเดล Machine Learning หรือ Deep Learning ที่ถูกแปลงเป็นไฟล์ `.onnx` แล้วรันได้โดยตรงภายใน EA (Expert Advisor), Indicator หรือ Script โดยไม่ต้องเปิด Python ควบคู่กันขณะเทรดจริง

**ONNX (Open Neural Network Exchange)** เป็นมาตรฐานกลางสำหรับแลกเปลี่ยนโมเดล AI ระหว่าง Framework ต่าง ๆ เช่น PyTorch, TensorFlow / Keras, Scikit-Learn, LightGBM, XGBoost เมื่อ Export เป็น `.onnx` แล้วสามารถนำเข้า MT5 ได้เลย

## โครงสร้างการทำงาน (Workflow)

```text
Historical Data
       ↓
Train Model (Python) -> [ PyTorch / TensorFlow / LightGBM ]
       ↓
Export → model.onnx
       ↓
MT5 (MQL5)
       ↓
OnnxCreate() / OnnxRun()
       ↓
Prediction
       ↓
Buy / Sell Signal
```

MT5 มี API ONNX ในตัวสำหรับการโหลด รัน และปิดโมเดล:
- `OnnxCreate()`, `OnnxCreateFromBuffer()`
- `OnnxSetInputShape()`, `OnnxSetOutputShape()`
- `OnnxRun()`
- `OnnxRelease()`

---

## ตัวอย่าง Use Cases

1. **Price Prediction:** โมเดลเรียนรู้จาก Open, High, Low, Close, Volume เพื่อทำนายทิศทางราคาในอนาคต (Price ↑ หรือ Price ↓) แล้วเปิด Order อัตโนมัติ
2. **Signal Classification:** ใช้ Indicator (RSI, MACD, ATR, EMA) เป็น Input ให้ Neural Network เพื่อทำนายสถานะ BUY, SELL หรือ HOLD
3. **Risk Management:** โมเดลคำนวณ Lot Size, Stop Loss, Take Profit อัตโนมัติตามความผันผวน (Volatility) แทนการกำหนดค่าคงที่
4. **Market Regime Detection:** จำแนกสภาวะตลาด (TREND, RANGE, BREAKOUT) เพื่อสลับกลยุทธ์อัตโนมัติ (เช่น สลับจาก Trend Strategy เป็น Mean Reversion)

---

## ข้อดีของ ONNX บน MT5

1. **ไม่ต้องใช้ Python Runtime:** ลด Latency และเพิ่มความเสถียร (MT5 -> ONNX Runtime -> Prediction ทันที)
2. **Backtest ได้ใน Strategy Tester:** สามารถทดสอบโมเดล AI ย้อนหลังหลายปีได้ภายใน MT5 โดยตรง
3. **Deploy ง่าย:** แค่ส่งไฟล์ `EA.ex5` และ `model.onnx` ไปรันบน VPS ได้เลย โดยไม่ต้องติดตั้ง Python หรือ Packages ให้ยุ่งยาก
4. **รองรับ GPU:** MetaQuotes รองรับ CUDA GPU สำหรับ ONNX Runtime โดยมี Flag ให้เลือกประมวลผลบน GPU หรือ CPU ได้

---

## ข้อจำกัดที่ต้องระวัง

1. **MT5 ใช้สำหรับ Inference เท่านั้น:** MT5 ไม่ได้ใช้สำหรับ AI Training การ Train ต้องทำใน Python (PyTorch, TensorFlow, Scikit-Learn) แล้วค่อย Export เป็น ONNX
2. **โมเดลขนาดใหญ่อาจทำงานช้า:** โมเดลที่กินทรัพยากรสูง เช่น Large LSTM, Transformer, LLM อาจทำให้กิน RAM และ CPU สูง นิยมใช้โมเดลขนาดเล็กถึงกลางสำหรับระบบเทรดจริง เช่น MLP, Small CNN/LSTM, XGBoost, LightGBM
3. **การทำ Preprocessing ต้องตรงกัน:** การทำ Data Normalization (เช่น `(X-mean)/std`) ตอนรันใน MT5 ต้องใช้วิธีและพารามิเตอร์เดียวกับตอนที่ Train โมเดลเป๊ะ ๆ มิฉะนั้นผลลัพธ์จะผิดเพี้ยน

---

## สรุปแนวทางสำหรับสาย AI / Big Data (Best Practices)

สำหรับนักพัฒนาสาย Data Science / AI แนวทางที่นิยมและคุ้มค่าที่สุดในงานเทรดจริง:

1. **Feature Engineering (Python):** สร้าง Feature ทางเทคนิค เช่น RSI, MACD, ATR, VWAP
2. **Machine Learning / Deep Learning:** Train ข้อมูลด้วย XGBoost, LightGBM (หรือ Deep Learning สำหรับโมเดลขนาดเล็ก)
3. **Export & Deploy:** Export โมเดลเป็น ONNX
4. **MQL5 Integration:** ใช้ MQL5 เรียกผ่าน `OnnxRun()`
5. **Backtesting:** ทำ Walk Forward Backtesting ภายใน Strategy Tester ของ MT5

---

## 4 Metrics หลักที่ต้องให้ความสำคัญ

ในการประเมินโมเดลเทรด **Trading Metrics สำคัญกว่า Classification Metrics (Accuracy)**

**Classification Metrics:** (สำหรับประเมิน Model ขั้นต้น)
- Accuracy, F1 Score, Precision, Recall, AUC

**Trading Metrics:** (สำหรับประเมินระบบเทรดจริง - สำคัญมาก)
- **Profit Factor:** ควร > 1.5 (Gross Profit / Gross Loss)
- **Sharpe Ratio:** ควร > 1.5
- **Max Drawdown:** ควร < 20%
- **Win Rate:** ไม่จำเป็นต้องสูง (เช่น 45% ก็เทรดได้ถ้า Profit Factor สูง)
- **Expected Value**

---

## เทคนิคการทำ Walk Forward & Validation

- **Rolling Window:** ใช้เทคนิค Walk Forward เช่น Train 2 ปี Test 3 เดือน แล้วเลื่อน (Roll) ไปเรื่อย ๆ เพื่อทดสอบความเสถียรของโมเดล
- **Ensemble Models (โหวตติ้ง):** แทนที่จะใช้ LightGBM ตัวเดียว ให้ใช้ LightGBM + XGBoost + CatBoost แล้วให้โมเดลโหวตกัน (เช่น 2 BUY 1 SELL = BUY)

---

## ข้อควรระวังตอน Export เป็น ONNX

เมื่อทำการ Export โมเดล (LightGBM -> ONNX -> `model.onnx`) **ห้ามเก็บแค่โมเดลเปล่า ๆ** สิ่งที่ต้องเก็บคู่กันเสมอ:
1. `model.onnx`
2. `feature_order.json` (ลำดับ Feature สำคัญมาก ถ้าตอน Train เป็น `[RSI, ATR, EMA]` แต่ตอนรันส่ง `[ATR, RSI, EMA]` ผลจะพังทันที)
3. `scaler.pkl` (หรือไฟล์พารามิเตอร์ของ Normalizer)
4. `metadata.json`

---

## เทคนิคเพิ่มประสิทธิภาพบน MT5 (Filters & Thresholds)

EA ต้องมี Pipeline เดียวกับ Python 100% แต่สามารถเพิ่ม Filter เหล่านี้เพื่อลด False Signal ได้:

1. **Threshold Trading:** แทนที่จะใช้ Prob > 0.5 ให้ตั้งค่าเป็น:
   - Prob > 0.7 = BUY
   - Prob < 0.3 = SELL
   - ช่วงกลาง 0.3-0.7 = HOLD
2. **Confidence Filter:** หากโมเดลแยก Class ชัดเจน (เช่น BUY=0.89, SELL=0.11) ให้เทรด แต่ถ้าก้ำกึ่ง (เช่น BUY=0.52, SELL=0.48) งดเทรด
3. **ATR Filter:** งดเทรดเมื่อ ATR ต่ำเกินไป (สภาวะตลาด Sideway)
4. **Spread Filter:** งดเทรดเมื่อ Spread ถ่างมากกว่าปกติ (เช่น > Average Spread x 2)
5. **News Filter:** เชื่อม Economic Calendar งดเทรดก่อนข่าวแดง 30-60 นาที (เช่น NFP, CPI, FOMC)

---

## สถาปัตยกรรมระดับมืออาชีพ (Pro Architecture)

```text
MT5 Data
   ↓
PostgreSQL
   ↓
Feature Pipeline
   ↓
LightGBM
   ↓
Optuna
   ↓
Walk Forward
   ↓
MLflow
   ↓
ONNX
   ↓
MT5 EA
   ↓
Monitoring
```

**สูตรเริ่มต้นทำโปรเจกต์จริง:**
- **Dataset:** EURUSD, GBPUSD, XAUUSD (ย้อนหลัง 5-10 ปี)
- **Features:** 80-120 Features
- **Model:** LightGBM
- **Validation:** Walk Forward
- **Optimization:** Optuna
- **Deployment:** ONNX + MT5 EA
- **Monitoring:** Profit Factor, Sharpe Ratio, Drawdown, Prediction Accuracy, Feature Drift

> **สรุป:** ถ้าทำครบ Pipeline นี้ได้จริง คุณจะได้ระบบในระดับใกล้เคียง Quant Research Workflow มากกว่าระบบ "AI Trading" ทั่วไปที่มักมีเพียง LSTM + Buy/Sell โดยไม่มี Validation และ Monitoring ที่เข้มงวด

---

## Roadmap สำหรับการทำระบบแบบมืออาชีพ (Project Phases & Timeline)

### Phase 1: MVP (Minimum Viable Product)
**เป้าหมาย:** ระบบ LightGBM + ONNX + MT5 ที่รันได้จริง
**ใช้เวลา:** 8-12 สัปดาห์
- Data Pipeline (2 สัปดาห์)
- Feature Engineering (2 สัปดาห์)
- Train Model (1 สัปดาห์)
- Walk Forward Testing (1 สัปดาห์)
- Export ONNX (1 สัปดาห์)
- MT5 EA Integration (2-3 สัปดาห์)

### Phase 2: Production (MLOps Integration)
**เป้าหมาย:** เพิ่มความเสถียรด้วยระบบ Monitoring และ Retraining
**ใช้เวลา:** เพิ่มอีก 2-3 เดือน
- นำ MLflow เข้ามาจัดการ Experiment Tracking
- สร้างระบบ Monitoring (Grafana)
- เขียน Script สำหรับ Auto Retrain

### Phase 3: Quant Platform (Advanced Scale)
**เป้าหมาย:** เทรดหลายสินทรัพย์ (Multi-Asset) และใช้โมเดลขั้นสูง
**ใช้เวลา:** เพิ่มอีก 3-6 เดือน
- ทำ Feature Store แบบรวมศูนย์
- ใช้ระบบ Model Registry
- เพิ่ม Market Regime Detection
- พัฒนาระบบ Ensemble Models
- ขยายไปเทรด EURUSD, GBPUSD, XAUUSD, US30 พร้อมกัน

---

## KPI ระดับมืออาชีพ (เมื่อระบบนิ่งแล้วควรวัดผลรายวัน)

หากต้องการทำเป็น **"AI Trading Platform"** เต็มรูปแบบ ระบบจะต้องบรรลุค่า KPI เหล่านี้:
- **Profit Factor:** > 1.5
- **Sharpe Ratio:** > 1.5
- **Max Drawdown:** < 15%
- **Prediction Drift:** < Threshold ที่ตั้งไว้
- **Data Drift:** < Threshold ที่ตั้งไว้
- **Model Retraining Frequency:** <= 1 เดือน (หรือเร็วกว่านั้นเมื่อพบ Drift)
- **Rollback Time (MTTR):** < 5 นาที (กู้คืนระบบกลับโมเดลเวอร์ชันเก่าได้อย่างรวดเร็ว)

---

## กฎเหล็ก 5 ข้อสำหรับการนำ AI ขึ้นเทรดจริง (Production Rules)

ความล้มเหลวของ AI Trading กว่า 80% ไม่ได้เกิดจากโมเดลไม่เก่ง แต่เกิดจาก Data Leakage, Overfitting, และไม่มีระบบควบคุมความเสี่ยง หากจะสร้างระบบระดับมืออาชีพ **ห้ามละเมิดกฎ 5 ข้อนี้เด็ดขาด:**

1. **No Data Leakage:** ข้อมูลในอนาคตต้องไม่หลุดไปปนในอดีตตอนสร้าง Feature หรือทำ Normalization
2. **Walk Forward Only:** การประเมินผลต้องใช้ Walk Forward Testing เท่านั้น ห้ามใช้ Train/Test Split ธรรมดา
3. **Risk Engine Before Execution:** ห้าม AI ส่ง Order ตรง ต้องผ่าน Risk Engine กรองก่อนเสมอ (ดูหัวข้อ 9)
4. **Paper Trading Before Production:** ต้องรัน Paper Trading (Forward Test) อย่างน้อย 30 วันก่อนใช้เงินจริง และเมื่อเริ่มใช้เงินจริงให้เริ่มที่ 1% Position Size ก่อนเสมอ
5. **Monitoring + Rollback Must Exist:** ต้องมีระบบมอนิเตอร์หลัง Deploy (Drift, PnL) และมีแผน Rollback กลับไปใช้โมเดลเวอร์ชันก่อนหน้าหากเกิดปัญหา

---

## 9. Risk Management Engine (จุดชี้เป็นชี้ตาย)

AI ห้ามส่ง Order โดยตรง แต่ต้องส่งผ่าน Risk Engine ก่อนเสมอ:
- **Daily Loss Limit:** เช่น ติดลบถึง -3% หยุดเทรดทั้งวัน
- **Max Drawdown:** เช่น Drawdown ถึง 10% หยุดระบบ (Kill Switch) ทันที
- **Consecutive Loss:** เช่น เทรดเสีย 10 ครั้งติด หยุดระบบทันที
- **Spread Protection:** ถ้าราคา Spread > Threshold (เช่น ข่าวออก) ไม่ให้เทรด
- **Slippage Protection:** ถ้า Slippage > Threshold ให้ยกเลิก Order (Cancel)

---

## 10. MLOps Requirements (การจัดการวงจรชีวิตโมเดล)

- **Experiment Tracking:** ใช้ MLflow เก็บข้อมูล Parameters, Metrics, และ Models ทุกครั้งที่ Train
- **Model Registry:** ทุกโมเดลที่ใช้งานต้องมี `Model ID`, `Version`, `Dataset Version`, `Feature Version`, และ `Training Date` ชัดเจน
- **Retraining Strategy:** ต้องตั้งระบบ Retrain โมเดลอัตโนมัติ (เช่น ทุกสิ้นเดือน) หรือทำทันทีเมื่อตรวจพบว่า Data/Feature Drift สูงเกินไป

---

## 11. Monitoring Requirements

- **Trading Monitoring:** ติดตาม PnL, Profit Factor, Drawdown, และ Win Rate แบบ Real-time
- **Model Monitoring:** ดูการกระจายตัวของคำทำนาย (Prediction Distribution), ค่าความมั่นใจ (Confidence Score)
- **Data Monitoring:** ติดตาม Data Drift, Feature Drift, และตรวจสอบว่ามี Missing Value โผล่มาหรือไม่ตอนเทรดจริง

---

## 12. Incident Response (Runbook สำหรับแก้ปัญหาเฉพาะหน้า)

- **Model Failure:** Rollback กลับไปใช้โมเดลตัวก่อนหน้าทันที
- **MT5 Failure:** สลับไปรันบน Backup VPS
- **Data Failure:** หยุดเทรด (Freeze Trading) ทันที จนกว่าจะแก้ไข Data Source เสร็จ
- **Drift Detected:** แจ้งเตือน และสั่งรัน Retraining Pipeline ใหม่

---

## Definition of Done (DoD) ก่อนขึ้น Production

ก่อนจะนำโมเดลใด ๆ ไปเทรดเงินจริง ต้องเช็คลิสต์ว่าผ่านสิ่งเหล่านี้แล้ว:
- [x] Feature Review
- [x] Code Review
- [x] Backtest Review
- [x] Walk Forward Validation
- [x] Paper Trading (30 วัน)
- [x] Risk Review (Risk Engine เปิดใช้งาน)
- [x] ONNX Export Validation
- [x] MT5 Integration Test
- [x] Monitoring Setup (Grafana / MLflow ทำงานอยู่)
- [x] Rollback Tested
- [x] Disaster Recovery Tested (ทดสอบย้าย VPS)

### 1. Beginner (ความยาก 3/10)
เหมาะสำหรับเริ่มต้นและทำความเข้าใจ Pipeline
- **Features:** OHLCV + RSI + MACD + ATR
- **Model:** LightGBM
- **Deployment:** ONNX -> MT5

### 2. Intermediate (ความยาก 6/10)
- **Features:** OHLCV + 50-100 Technical Features
- **Model:** LightGBM + Optuna (Hyperparameter Tuning)
- **Deployment:** ONNX -> MT5

### 3. Advanced (ความยาก 10/10)
- **Features:** Multi Timeframe (H1 + H4 + D1) + Feature Store
- **Model:** Transformer + Ensemble Models
- **Validation:** Walk Forward Testing
- **Deployment:** ONNX -> MT5 Cluster

---

## MT5 Deployment Pipeline & Risk Management

การนำโมเดลไปใช้งานจริง (Phase 7) ไม่ใช่แค่การรันโมเดล แต่ต้องมีระบบจัดการความเสี่ยง (Risk Management Layer) ครอบอยู่เสมอ

```text
Feature Calculation
       ↓
Normalize (ต้องเหมือนตอน Train)
       ↓
OnnxRun()
       ↓
Prediction
       ↓
Risk Check (Max Position, Max Drawdown, Max Daily Loss, Spread, News Filter)  <-- ขาดไม่ได้!
       ↓
Order Execute
```

---

## Technology Stack สำหรับ Data Scientist / Big Data

| Layer | Tool |
|---------|--------|
| **Data Collection** | MT5 API, Python |
| **Storage** | PostgreSQL, DuckDB |
| **Feature Engineering** | Pandas, Polars |
| **Machine Learning** | LightGBM, XGBoost |
| **Deep Learning** | PyTorch |
| **Experiment Tracking** | MLflow |
| **Workflow** | Prefect |
| **Model Registry** | MLflow |
| **Export** | ONNX |
| **Deployment** | MQL5 |
| **Monitoring** | Grafana |

---

## Roadmap 6 เดือน (สำหรับผู้เริ่มต้น)

| เดือน | เป้าหมาย |
|---------|----------|
| **1** | Data Collection, ทำความเข้าใจ OHLCV |
| **2** | Feature Engineering, สร้าง Technical Indicators |
| **3** | Train LightGBM และทำ Walk Forward Testing |
| **4** | Export ONNX, รัน Paper Trading และสร้าง EA เบื้องต้น |
| **5** | Setup Monitoring (MLflow, Optuna) |
| **6** | นำขึ้นเทรดจริงด้วย MT5, ทำระบบ Auto Retraining และขยายไป Multi-Asset (EURUSD, XAUUSD ฯลฯ) |

> **คำแนะนำสุดท้าย:** ถ้าต้องการ "ระบบทำเงินจริง" อย่าเพิ่งเริ่มจาก Deep learning ที่ซับซ้อนอย่าง LSTM หรือ Transformer ให้เริ่มจาก: **Feature Engineering + LightGBM + Walk Forward Testing + ONNX + MT5** นี่คือแนวทางที่ให้ผลลัพธ์ดีที่สุดต่อเวลา ทรัพยากร และลด Overfitting ในตลาดที่มี Noise สูงได้ดีที่สุด

แนวทางนี้ช่วยให้สามารถสร้าง "AI Trading Bot" ที่ทำงานได้อย่างรวดเร็ว รองรับการทำ Backtest ที่แม่นยำ และจัดการกับข้อมูลที่มี Noise สูงในตลาดการเงิน (เช่น Forex) ได้อย่างมีประสิทธิภาพ
