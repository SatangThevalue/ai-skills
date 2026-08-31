---
name: python-quant-mlops-stack
description: "Python Library Stack และ MLOps Architecture สำหรับระบบ AI Trading / Quant Platform ระดับ Enterprise"
---

# Python Library Stack & MLOps Architecture สำหรับ AI Trading

ในฐานะ Tech Lead/PM การสร้างระบบไม่ควรติดตั้งทุกอย่างตั้งแต่วันแรก แต่ควรแบ่ง Library ออกเป็น Layer ตามสถาปัตยกรรม เพื่อควบคุมความซับซ้อนและลด Technical Debt

**Workflow:**
`Data Collection` → `Feature Engineering` → `Training (LightGBM)` → `Hyperparameter Tuning` → `Validation` → `Experiment Tracking` → `Model Registry` → `ONNX Export` → `MT5 Deployment` → `Monitoring` → `Retraining`

---

## 1. Core Python (Data Manipulation)
พื้นฐานสำหรับการจัดการข้อมูลขนาดใหญ่และ Vectorized calculation
- **`polars`**: แนะนำเป็นหลัก เร็วกว่าเมื่อข้อมูลระดับล้านแถว
- **`pandas`**: แนะนำเป็นรอง
- **`numpy`**, **`pyarrow`**, **`scipy`**

## 2. Data Collection
- **`MetaTrader5`**: ดึง Tick, OHLCV, Spread, Account Info, Position
- **`sqlalchemy`**, **`psycopg2-binary`**: สำหรับ PostgreSQL
- **`duckdb`**: สำหรับ Research (เหมาะกับงาน Quant เพราะ Query เร็วมาก)

## 3. Feature Engineering
- **`ta`**, **`pandas-ta`**: สร้าง Technical Indicators อัตโนมัติ (RSI, MACD, ATR, BBANDS)
- **`scipy`**, **`statsmodels`**: สำหรับ Statistics (ADF Test, Stationarity, Rolling Regression)
- **`category-encoders`**: สำหรับ Feature Encoding

## 4. Machine Learning (Core)
นี่คือหัวใจของระบบ
- **`lightgbm`**: Gradient Boosting Framework ตัวหลักที่เหมาะมากสำหรับ Tabular Data
- **`scikit-learn`**: สำหรับ Baseline models (Logistic Regression, Random Forest, Extra Trees)
- **`xgboost`**, **`catboost`**: Option เสริมสำหรับทำ Ensemble ภายหลัง

## 5. Hyperparameter Tuning
- **`optuna`**: ตัวที่แนะนำที่สุด มี Integration กับ LightGBM สำหรับปรับ Hyperparameter อัตโนมัติ (เช่น max_depth, num_leaves, learning_rate, feature_fraction, bagging_fraction)

## 6. Validation & Metrics
- **`scikit-learn`**: ใช้ `TimeSeriesSplit` สำหรับ Time Series CV
- **`empyrical`**: คำนวณ Financial Metrics (Sharpe, Sortino, Calmar, Drawdown)
- **`quantstats`**: สร้างรายงาน Trade Analysis และ Portfolio Metrics

## 7. Explainable AI (XAI)
สำคัญมาก!
- **`shap`**: ใช้ดูว่า Feature ไหนมีผลต่อ Decision (เช่น ตัดสินใจจาก RSI 20%, ATR 15%, EMA Gap 10%)

## 8. Experiment Tracking
สิ่งที่ "ต้องมี" สำหรับ MLOps
- **`mlflow`**: เก็บ Model, Metrics, Parameters, Artifacts (เทียบได้เลยว่า Version 1 ได้ Sharpe 0.9 ส่วน Version 2 ได้ 1.5) มี Integration สำหรับ LightGBM โดยตรง

## 9. Model Registry
- **`mlflow`** (ใช้ตัวเดียวจบได้) หรือ **`bentoml`** (ถ้าขยายระบบใหญ่)

## 10. ONNX Export
ต้องมีสำหรับการส่งออกไป MT5
- **`onnx`**: สร้างไฟล์ `model.onnx`
- **`onnxruntime`**: ทดสอบ Prediction ก่อนส่งเข้า MT5
- **`skl2onnx`**: แปลง Scikit-Learn เป็น ONNX
- **`onnxmltools`**: แปลง LightGBM / XGBoost เป็น ONNX

## 11. Workflow Automation
- **`prefect`**: ควบคุม ETL, Training, Validation, Deployment ทั้งหมด
- *ตัวอย่าง:* ทุกตี 2 Fetch Data → Generate Features → Train → Validate → MLflow

## 12. Monitoring
- **`grafanalib`**: สำหรับสร้าง Dashboard
- **`prometheus-client`**: เก็บ Prediction Count, Latency, Sharpe, Drawdown

## 13. Data Drift Monitoring
สำคัญมากในตลาดเงิน
- **`evidently`**: ใช้ตรวจ Data Drift, Feature Drift, Target Drift (เช่น ถ้าระบุว่า RSI Distribution Changed จะทำการ Alert)

## 14. Retraining Automation
- ใช้ **`prefect`** + **`evidently`** + **`mlflow`** ร่วมกัน
- *Flow:* Drift Detected → Trigger Training → Validation → Deploy Candidate → Paper Trade

## 15. API Layer (อนาคต)
ถ้าจะสร้าง Platform ของตัวเอง
- **`fastapi`**, **`uvicorn`**, **`pydantic`**: สร้าง Model Registry API, Monitoring API, Feature API

## 16. Configuration & Secret Management
ห้าม Hardcode เด็ดขาด
- **`python-dotenv`**, **`pydantic-settings`**: จัดการ Config
- **`infisical-python`**: จัดการ Secret

## 17. Logging & Testing
- **`loguru`**: แนะนำให้ใช้แทน logging มาตรฐาน
- **`pytest`**, **`pytest-cov`**: สำหรับ Unit Test และ Coverage

---

## Production Package List
ถ้าจะสร้างจริง เริ่มจากชุดนี้:
```bash
pip install numpy pandas polars pyarrow scipy MetaTrader5 sqlalchemy psycopg2-binary duckdb ta lightgbm scikit-learn optuna shap quantstats empyrical mlflow onnx onnxruntime onnxmltools skl2onnx prefect evidently fastapi uvicorn python-dotenv pydantic-settings loguru pytest
```

---

## การจัดลำดับความสำคัญ (Phased Rollout)

### Phase 1 (MVP)
**ต้องมี:** `MetaTrader5`, `Polars`, `LightGBM`, `Scikit-Learn`, `Optuna`, `ONNX`, `onnxruntime`

### Phase 2 (Production)
**เพิ่ม:** `MLflow`, `Prefect`, `QuantStats`, `SHAP`

### Phase 3 (Professional Quant Platform)
**เพิ่ม:** `Evidently`, `Grafana`, `Prometheus`, `FastAPI`, `Feature Store`

> **สรุปสำหรับสาย Big Data / MLOps:** 
> สำหรับโปรเจกต์นี้ (Big Data + Prefect + MLflow + MT5 + ONNX) **6 Library หลักที่ต้องลงทุนศึกษาให้ลึกที่สุด** คือ `LightGBM`, `Optuna`, `MLflow`, `ONNX Runtime`, `Prefect`, และ `Evidently` เพราะนี่คือแกนกลางของระบบทั้งหมด
