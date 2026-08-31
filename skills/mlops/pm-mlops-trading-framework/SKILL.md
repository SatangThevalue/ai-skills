---
name: pm-mlops-trading-framework
description: "Project Management framework and strict governance rules for building an end-to-end MLOps AI Trading Platform (MT5 + ONNX)."
prerequisites: ["MLOps fundamentals", "Algorithmic trading concepts", "MT5/MQL5 architecture"]
---

# PM MLOps Trading Framework

กรอบการบริหารจัดการโปรเจกต์ (Project Management Framework) สำหรับการสร้าง **AI Trading Platform** แบบครบวงจร (Data Pipeline + ML Training + ONNX Registry + MT5 Auto Trading + Monitoring) โดยเน้นการควบคุมความเสี่ยงอย่างเข้มงวด (Capital, Data Leakage, Model Risk, Infrastructure Risk, Operational Risk)

## 1. Project Charter

### 🎯 Vision
สร้างระบบอัตโนมัติแบบ End-to-End: **Research → Train → Validate → Deploy → Monitor**

### 📊 Goals
| Category | Metric | Target |
| :--- | :--- | :--- |
| **Business** | Profit Factor | > 1.5 |
| | Sharpe Ratio | > 1.2 |
| | Max Drawdown | < 15% |
| | Win Rate | > 40% |
| **Technical** | Model Retraining | Automated |
| | Deploy Time | < 10 นาที |
| | Rollback Time | < 1 นาที |
| | Inference Latency| < 50ms |

## 2. Requirements Definition

### ⚙️ Functional Requirements (FR)
- **FR-001 Data Collection:** ดึงข้อมูลจาก MT5 (Tick, OHLCV, Indicator) ได้
- **FR-002 Feature Generator:** สร้าง Indicator อัตโนมัติ (เช่น RSI, MACD, ATR, EMA, Volatility)
- **FR-003 Model Training:** รองรับ LightGBM, XGBoost, CatBoost
- **FR-004 HPO:** รองรับการทำ Hyperparameter Optimization ด้วย Optuna
- **FR-005 Validation:** ต้องทำ Walk Forward Testing (Rolling Window Validation) ทุกครั้ง
- **FR-006 Model Registry:** บันทึก Model Version, Training Date, Feature List, Metrics
- **FR-007 Export ONNX:** แปลงและส่งออกไฟล์ `model.onnx` อัตโนมัติ
- **FR-008 MT5 Deployment:** สามารถ Deploy EA พร้อมโมเดล ONNX ได้
- **FR-009 Monitoring Dashboard:** แสดงผล Profit, Drawdown, Accuracy, และ Model Drift

### 🚀 Non-Functional Requirements (NFR)
- **Performance:** Prediction (Inference) < 50ms
- **Availability:** Uptime 99.9%
- **Recovery (RTO):** < 15 นาที
- **Security:** จัดการ Secrets ด้วยเครื่องมือมาตรฐาน (เช่น Infisical)

## 3. Team Structure & Responsibilities

| Role | Responsibilities |
| :--- | :--- |
| **PM** | Roadmap, Risk, Budget |
| **Data Engineer** | ETL, Feature Store, PostgreSQL |
| **Data Scientist** | Research, Feature Engineering, Training |
| **MLOps Engineer** | MLflow, Model Registry, Deployment Pipeline |
| **Quant** | Strategy, Risk Management, Validation |
| **MQL5 Developer** | EA Development, ONNX Runtime Integration, Execution |

## 4. Architecture Blueprint (5 Layers)

1. **Layer 1: Data** → MT5 → Collector → PostgreSQL
2. **Layer 2: Processing** → Prefect → Feature Pipeline
3. **Layer 3: Training** → LightGBM → Optuna → MLflow
4. **Layer 4: Deployment** → Export ONNX → Model Registry → MT5 EA
5. **Layer 5: Monitoring** → ML Monitoring, Prometheus, Grafana

## 5. ⚠️ Strict Data Governance (Critical)

กฎเหล็กสำหรับการจัดการข้อมูลเพื่อป้องกัน Data Leakage และ Overfitting:

1. **ห้ามใช้ข้อมูลอนาคต (No Future Data):** ห้ามสร้าง Feature ที่มองเห็นอนาคต เช่น `EMA(t+1)`
2. **ห้าม Random Split:** การแบ่งข้อมูลต้องใช้ **Walk Forward** (Time-series split) เท่านั้น
3. **Pipeline Consistency:** Feature Pipeline ระหว่าง **Training** และ **Production** ต้องเหมือนกัน 100%
4. **Feature Order Lock:** ลำดับของ Features ต้องล็อกให้ตรงกัน (เช่น Train: RSI, ATR, EMA → Production ต้องป้อนเรียง RSI, ATR, EMA ตามลำดับเป๊ะ)
5. **Dataset Versioning:** ต้องเก็บเวอร์ชันของ Dataset ทุกครั้งที่มีการ Train (Dataset V1, V2, V3, ...)

## 6. Training Rules & Thresholds

- **Baseline Requirement:** ต้องมีโมเดล Baseline เสมอ (เช่น Buy & Hold, EMA Cross, RSI Strategy)
- **Victory Condition:** AI Model **ต้องชนะ Baseline** หากไม่ผ่านเกณฑ์ให้ Reject ทันที
- **Minimum Acceptable Metrics:**
  - Accuracy > 55%
  - Profit Factor > 1.3
  - Sharpe Ratio > 1.0
  - Max Drawdown < 20%

## 7. Walk Forward Policy

นโยบายการทดสอบความเสถียรของโมเดลข้ามช่วงเวลา:
- **Production Approval:** โมเดลต้องสอบผ่านอย่างน้อย **5 Walk Forward Windows** (เช่น 2020→21, 2021→22, 2022→23, 2023→24, 2024→25)
- **Stability Constraint:** ทุก Window ต้องทำกำไรได้ **ไม่น้อยกว่า 60%** ของจำนวนช่วงทดสอบทั้งหมด

## 8. Deployment Policy

- **Model Promotion Pipeline:** โมเดลต้องผ่าน Pipeline ตามลำดับอย่างเคร่งครัด
  `Research → Staging → Paper Trade → Production`
- ❌ **ห้ามข้ามขั้นตอน:** ห้าม Deploy จาก Research ขึ้น Production โดยตรงเด็ดขาด