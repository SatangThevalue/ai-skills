---
name: python-quant-mlops-stack
description: "สถาปัตยกรรม Python Library Stack สำหรับ AI Trading & Quant Platform เต็มรูปแบบ ตั้งแต่ Data Collection ถึง Auto Retraining"
---

# สถาปัตยกรรม MLOps สำหรับ Quant Trading

คู่มือนี้สรุปชุดเครื่องมือ (Library Stack) ที่ครอบคลุมวงจรชีวิตของการทำ AI Trading บน MetaTrader 5 (MT5) โดยเน้นเครื่องมือที่ **Production Ready, รองรับ MLOps, รองรับ Quant Trading และขยายระบบได้ในอนาคต**

---

## 🏗️ Architecture ภาพรวม

```text
┌─────────────────┐
│ MT5 Data        │
└────────┬────────┘
         ▼
┌─────────────────┐
│ DuckDB / Postgre│
└────────┬────────┘
         ▼
┌─────────────────┐
│ Feature Engine  │
└────────┬────────┘
         ▼
┌─────────────────┐
│ LightGBM / Optuna│
└────────┬────────┘
         ▼
┌─────────────────┐
│ Walk Forward    │
│ Validation      │
└────────┬────────┘
         ▼
┌─────────────────┐
│ MLflow          │
│ Model Registry  │
└────────┬────────┘
         ▼
┌─────────────────┐
│ ONNX            │
└────────┬────────┘
         ▼
┌─────────────────┐
│ MT5 EA          │
└────────┬────────┘
         ▼
┌─────────────────┐
│ Monitoring      │
│ Drift Detection │
└─────────────────┘
```

---

## 🛠️ Python Libraries ตาม Layers

### 1. Data Collection & Database Layer
- **`MetaTrader5`**: ตัวดึงข้อมูลหลัก (OHLCV, Tick Data, Positions, Orders) [ความสำคัญ: 10/10] *(หมายเหตุ: แพ็กเกจ Python รันได้เฉพาะบน Windows เท่านั้น หากรันบน Linux VPS ต้องใช้เทคนิครัน EA/Inference บน Windows แล้วเทรนโมเดลบน Linux)*
- **`duckdb`**: ฐานข้อมูลแบบ In-memory ที่เร็วมาก เหมาะกับงาน Research (รองรับ SQL และ Parquet)
- **`psycopg2-binary`, `sqlalchemy`**: สำหรับต่อ PostgreSQL เพื่อเก็บ Features, Trades, Models ในสเกลใหญ่ *(ดูการออกแบบ Schema ระดับสถาบันได้ที่สกิล `quant-database-architecture`)*

### 2. Data Processing Layer
- **`polars`**: 🔥 *แนะนำแทน Pandas* ทำงานเร็วกว่า 5-20 เท่า, กิน RAM น้อยกว่า, รองรับ Lazy Query
- **`pyarrow`**: รูปแบบการจัดเก็บข้อมูล Columnar Storage (Parquet) ที่เร็วและมีประสิทธิภาพสูง

### 3. Feature Engineering Layer
- **`pandas-ta`**: สร้าง Technical Indicators รวดเร็ว (RSI, ATR, MACD, ADX, CCI)
- **`ta-lib`**: (ทางเลือก) เร็วมากและมีมายาวนาน แต่ติดตั้งยากกว่านิดหน่อย

### 4. Statistical & Regime Features
- **`scipy`**: สร้าง Z-Score, Hypothesis Test, สถิติพื้นฐาน
- **`statsmodels`**: การทำ ADF Test, Cointegration, ทดสอบ Stationarity
- **`hmmlearn`**: ใช้สร้าง Hidden Markov Model สำหรับประเมิน **Market Regime** (Trend, Range, Volatility)
- **`scikit-learn`**: ใช้ Clustering (KMeans, DBSCAN, GaussianMixture) หา Regime แบบ Unsupervised

### 5. Machine Learning Layer
- **`lightgbm`**: 🔥 *เครื่องยนต์หลัก* เหมาะกับงาน Tabular data มากที่สุด (Classification, Regression, Ranking) [ความสำคัญ: 10/10]
- **`scikit-learn`**: สิ่งที่ขาดไม่ได้ (Pipelines, Scalers, Metrics, Feature Selection)

### 6. Hyperparameter Optimization Layer
- **`optuna`**: Bayesian Optimization ยอดฮิต 
  - *Beginner:* `n_trials=50`
  - *Production:* `n_trials=300`
  - *Quant Level:* `n_trials=1000+`

### 7. Validation & Evaluation Layer
- **`scikit-learn`**: ใช้ `TimeSeriesSplit` ป้องกัน Data Leakage ในอนาคต
- **`quantstats`**: สร้าง HTML Reports, หา Sharpe, Sortino, Calmar, Drawdown
- **`empyrical`**: ตัวช่วยคำนวณ Profit Factor และ Risk Metrics ระดับกองทุน

### 8. Explainable AI (XAI) & Feature Selection
- **`shap`**: 🔥 *สำคัญมาก* ใช้หา Feature Importance แบบลึก และอธิบายได้ว่า "ทำไมถึงกด BUY" (เช่น เพราะ RSI ต่ำ + ATR สูง)
- **`scikit-learn`**: `SelectFromModel`, `Mutual Information`, `RFE`

### 9. Experiment Tracking & MLOps
- **`mlflow`**: เก็บบันทึก Model V1 vs V2, เปรียบเทียบ Sharpe Ratio, ดูพารามิเตอร์ และใช้เป็น Model Registry
- *(ดูคู่มือการออกแบบ Naming Convention และการ Tracking ด้วย MLflow เชิงลึกได้ที่สกิล `mlflow-quant-tracking-guide`)*

### 10. Workflow Orchestration
- **`prefect`**: ตั้งเวลาและร้อยเรียงท่อ (Fetch Data → Generate Features → Train → Validate → MLflow Deploy)
- *(ดูสถาปัตยกรรมและเวิร์กโฟลว์การใช้ Prefect แบบจัดเต็มได้ที่สกิล `prefect-quant-orchestration`)*

### 11. ONNX Deployment Layer
- **`onnx`**, **`onnxruntime`**: ทดสอบ Inference ด้วย Python ก่อนส่งเข้า MT5
- **`skl2onnx`**, **`onnxmltools`**: แปลง LightGBM ให้เป็นไฟล์ `.onnx`

### 12. Monitoring & Retraining
- **`evidently`**: ตรวจจับ Data Drift, Feature Drift, Target Drift (ถ้า PSI > 0.25 ให้สั่ง Alert และ Retrain อัตโนมัติ)

### 13. System & Utilities
- **`loguru`**: การทำ Logging ที่ดีกว่า `logging` มาตรฐานหลายเท่า
- **`pydantic-settings`**: จัดการ Configuration (ML Config, Database Config) โดยไม่ Hardcode
- **`pytest`**: ขาดไม่ได้สำหรับ Unit Test (เขียน Test ให้ครอบคลุมทุก Feature)
- **`plotly`, `seaborn`**: การทำ Visualization

---

## 🚀 Requirement Packages & Installation Guide

*(ดูคู่มือการแบ่งเฟสติดตั้ง และ Workflow การทำงานร่วมกันระหว่างไลบรารีอย่างละเอียดได้ที่สกิล `python-quant-library-installation-guide`)*

### Stage 1: MVP (Minimum Viable Product)
```bash
uv pip install MetaTrader5 polars numpy pyarrow lightgbm scikit-learn optuna pandas-ta onnx onnxruntime onnxmltools quantstats shap duckdb mlflow prefect loguru
```

### Stage 2: Production v2 (เพิ่มความเสถียร & ฐานข้อมูล)
```bash
uv pip install evidently statsmodels empyrical plotly postgresql sqlalchemy psycopg2-binary pydantic-settings
```

### Stage 3: Quant Platform (ระดับสถาบัน)
```bash
uv pip install hmmlearn feature-engine feast prometheus-client fastapi redis
```

---

## 🏆 The "Top 10" Core Libraries

ถ้าต้องโฟกัสแค่ 10 Library ที่เป็นกระดูกสันหลังของระบบ AI Trading ให้เชี่ยวชาญก่อน แนะนำ:

1. **`MetaTrader5`** (Data)
2. **`Polars`** (Data Processing)
3. **`LightGBM`** (Training)
4. **`Scikit-Learn`** (Validation / Metrics)
5. **`Optuna`** (Tuning)
6. **`MLflow`** (Experiment Tracking)
7. **`ONNX Runtime`** (Deployment)
8. **`Prefect`** (Workflow Automation)
9. **`SHAP`** (Explainability)
10. **`Evidently`** (Monitoring / Drift Detection)

*(10 ตัวนี้ครอบคลุมวงจรชีวิตทั้งหมด ตั้งแต่ดึงข้อมูล เทรนโมเดล ดีพลอย และมอนิเตอร์)*

---

## 🔗 อ่านเพิ่มเติมเกี่ยวกับชิ้นส่วนต่างๆ ของสถาปัตยกรรม
- **สถาปัตยกรรมการต่อ MT5 กับ ONNX แบบเจาะลึก:** `mql5-onnx-architecture-th`
- **การออกแบบฟีเจอร์ Quant (11 Stages):** `quant-feature-design-document`
- **โค้ดสกัดฟีเจอร์และ Feature Selection Pipeline:** `python-quant-feature-pipeline`
- **ระบบ Market Regime Detection:** `market-regime-detection-quant`