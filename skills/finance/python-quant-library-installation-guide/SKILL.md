---
name: python-quant-library-installation-guide
description: "คู่มือการติดตั้ง 15 Library Stack แบบแบ่ง 3 Phases (Research, Training, Production) และ Workflow สำหรับระบบ AI Trading"
---

# Python Quant Library Installation & Workflow Guide

การขึ้นระบบ AI Trading ระดับโปรดักชั่น ไม่ควรติดตั้งทุก Library พร้อมกันในวันแรก แต่ควรแบ่งออกเป็น 3 Phases เพื่อลดปัญหา Dependency และให้ง่ายต่อการ Debug:
`Phase 1: Research Environment` → `Phase 2: Training & MLOps` → `Phase 3: Production Deployment`

---

## 0. เตรียม Python Environment

แนะนำให้ใช้ **Python 3.11**
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux / WSL
python3 -m venv .venv
source .venv/bin/activate

# อัปเดตพื้นฐาน
pip install --upgrade pip setuptools wheel
```

---

## 1. Phase 1: Research Environment (ฐานราก)

กลุ่มนี้ใช้สำหรับการจัดการข้อมูล ทำ Data Analysis และเก็บ Data
```bash
pip install numpy pandas polars pyarrow scipy duckdb matplotlib seaborn plotly
```

**Workflow:** `MT5 Data` → `DuckDB` → `Polars` → `Data Analysis` → `Feature Engineering`
- **Polars:** ทำงานเร็วกว่า Pandas แนะนำให้ใช้เป็นหลักในการทำ Feature Engineering, Join, Aggregation
- **DuckDB:** เก็บ OHLCV, Features, Backtest Results แบบ Data Lake (`bronze/`, `silver/`, `gold/`) แทนไฟล์ Excel

---

## 2. Phase 2: Data Collection & Feature Engineering

เตรียมข้อมูลจาก MT5 และสกัดฟีเจอร์ด้วย `pandas-ta`
```bash
pip install MetaTrader5 pandas-ta
```

**Workflow:** `MT5` → `Polars DataFrame` → `pandas-ta (Indicators)` → `Feature Store`
- ใช้สร้าง RSI, MACD, ATR, ADX, Bollinger, EMA
- **⚠️ เทคนิคสำคัญ:** ห้ามส่ง EMA20 หรือ EMA50 ตรง ๆ เข้าโมเดล แต่ต้องสร้างเป็น `EMA_GAP` หรือ `EMA_SLOPE` เสมอ (ดูรายละเอียดที่สกิล `quant-feature-design-document`)

---

## 3. Phase 3: Feature Selection & Model Training (แกนกลาง ML)

กรองฟีเจอร์ที่ไม่จำเป็นออก และเทรนโมเดลตัวหลัก
```bash
pip install scikit-learn lightgbm
```

**Workflow:** `120 Features` → `Correlation Filter` → `Mutual Information` → `RFE` → `60 Features` → `LightGBM`
- **Correlation Filter:** ลบฟีเจอร์ที่เหมือนกัน (corr > 0.95)
- **LightGBM:** เริ่มที่ `learning_rate=0.03`, `max_depth=6`, `num_leaves=64`
- **⚠️ ข้อควรระวัง:** อย่าประเมินผลด้วย *Accuracy* อย่างเดียว ให้ดู *Profit Factor, Sharpe, Drawdown* เป็นหลัก

---

## 4. Phase 4: Hyperparameter Optimization & Validation

หาพารามิเตอร์ที่ดีที่สุดด้วย Optuna และเช็คการ Overfit ด้วย Walk Forward
```bash
pip install optuna quantstats empyrical
```

**Workflow:** `LightGBM` → `Optuna` → `Walk Forward (Time Series Split)` → `QuantStats`
- **Optuna:** เริ่มต้น `n_trials=100`, โปรดักชั่น `n_trials=300-500` (ให้ Optimize ด้วยโจทย์ Maximize Sharpe Ratio แทน Accuracy)
- **Walk Forward:** (เช่น Train 2020-2022 -> Test 2023, จากนั้นเลื่อน Train 2021-2023 -> Test 2024)

---

## 5. Phase 5: Explainability (XAI) & Experiment Tracking

ตอบคำถามว่าโมเดลกด BUY เพราะอะไร และเก็บประวัติการเทรน
```bash
pip install shap mlflow
```

**Workflow:** `Model` → `SHAP` → `Feature Ranking` → `MLflow Model Registry`
- **SHAP:** ดูสัดส่วนความสำคัญ (เช่น RSI 25%, ATR 20%, ADX 15%) แล้วนำมาตัดฟีเจอร์ที่ไม่มีประโยชน์ออก
- **MLflow:** บันทึก Parameters, Metrics, Artifacts, Models (เปรียบเทียบ Sharpe Ratio ระหว่าง Model_V1 กับ V2 ได้)

---

## 6. Phase 6: Orchestration, ONNX & Production

แปลงโมเดลส่งเข้า MT5 และสร้างระบบ MLOps อัตโนมัติ
```bash
pip install onnx onnxruntime onnxmltools skl2onnx prefect evidently prometheus-client loguru pydantic-settings
```

**Workflow:** `Prefect` → `LightGBM` → `ONNX` → `MT5 EA` → `Evidently` → `Retrain`
- **ONNX:** ต้องทดสอบผ่าน `onnxruntime` ก่อนส่งเข้า MT5 เสมอ
- **Prefect:** จัดตารางเวลา (เช่น 02:00 Fetch Data, 02:30 Train, 03:00 Validate)
- **Evidently:** ใช้ตรวจ Data Drift หากค่า `PSI > 0.25` ให้สั่ง Trigger Retraining อัตโนมัติ
- **Loguru / Pydantic-Settings:** ใช้จัดการ Config (`dev.yaml`, `prod.yaml`) และระบบ Logging ที่ดีกว่ามาตรฐาน

---

## 🔄 ภาพรวม Workflow ของระบบ AI Trading แบบ End-to-End

```text
MT5 → MetaTrader5 (API) → DuckDB (Lake) → Polars (Processing)
     ↓
Feature Engineering (pandas-ta) → Feature Selection (sklearn)
     ↓
LightGBM (Training) ↔ Optuna (Tuning)
     ↓
Walk Forward (Validation) → QuantStats (Metrics)
     ↓
SHAP (Explainability) → MLflow (Registry)
     ↓
ONNX Export → MT5 EA (Execution)
     ↓
Evidently (Monitoring) → Auto Retrain (Prefect)
```

---

## 🎓 ลำดับการศึกษาที่แนะนำ (Learning Path)

หากจะศึกษาและทำความเข้าใจทั้งหมดนี้ ควรเรียนตามลำดับ 11 ขั้นตอน:
1. **Polars** (จัดการข้อมูล)
2. **Pandas-TA** (สร้างฟีเจอร์)
3. **Scikit-Learn** (คัดกรอง / วัลลิเดท)
4. **LightGBM** (เครื่องยนต์หลัก)
5. **Optuna** (จูนพารามิเตอร์)
6. **QuantStats** (วัดผลทางการเงิน)
7. **SHAP** (ตีความผลลัพธ์)
8. **MLflow** (จัดเก็บโมเดล)
9. **ONNX** (เชื่อม MT5)
10. **Prefect** (ระบบอัตโนมัติ)
11. **Evidently** (มอนิเตอร์และ Drift)

> *ถ้าเข้าใจ 11 ตัวนี้จริง คุณจะสามารถสร้างระบบ AI Trading แบบครบวงจร ตั้งแต่ Data → Train → Optimize → Deploy → Monitor → Retrain ได้ในระดับ Production ของจริง*