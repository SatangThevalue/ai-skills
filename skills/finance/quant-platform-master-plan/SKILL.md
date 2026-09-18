---
name: quant-platform-master-plan
description: "แผนแม่บท (Master Project Plan) 16 Phases ในการสร้าง AI Quant Trading Platform ระดับ MLOps"
---

# Master Project Plan: AI Quant Trading Platform
**(MT5 + Python + LightGBM + ONNX + Prefect + MLflow)**

แผนแม่บทฉบับนี้ออกแบบสำหรับระยะเวลา 6-8 เดือน โดยเป้าหมายคือการสร้างระบบที่ข้ามขีดจำกัดจากการเป็นแค่ "AI Bot" ไปสู่ "Quant Trading Platform + MLOps" อย่างเต็มรูปแบบ

---

## 🏗️ Phase 0-8: MUST HAVE (โครงสร้างพื้นฐานและโมเดล)

**Phase 0: Foundation & Architecture (2 สัปดาห์)**
- กำหนดมาตรฐาน: Architecture Diagram, Git/Docker, UTC Time, Naming Standard (Asset/Feature)

**Phase 1: Data Platform (3-4 สัปดาห์)**
- เชื่อมต่อ: MT5, Yahoo Finance, CCXT, FRED, TradingEconomics
- ฐานข้อมูล: `market_ohlcv`, `market_ticks`, `economic_events`
- *KPI:* Data Completeness > 99%, Duplicate = 0%

**Phase 2: Feature Store (4 สัปดาห์)**
- สร้าง Feature Registry: 100+ Features แบ่งหมวด Price, Trend, Momentum, Volatility, Regime, Macro
- *Checklist:* Feature Contract, Feature Version, Unit Testing

**Phase 3: Label Engineering (1 สัปดาห์)**
- สร้างเป้าหมายให้ AI: `Direction (V1)`, `Future Return (V2)`, `Triple Barrier (V3)`

**Phase 4: Baseline Research (2 สัปดาห์)**
- สร้างเกณฑ์มาตรฐานด้วย Logistic Regression หรือ Random Forest ก่อนไปใช้ LightGBM

**Phase 5: Feature Selection (2 สัปดาห์)**
- กรองจาก 100 เหลือ 30-50 Features ด้วย: `Correlation` ➔ `Mutual Information` ➔ `RFE` ➔ `SHAP`

**Phase 6: Model Training (3 สัปดาห์)**
- ใช้ LightGBM + Optuna และ Tracking ทุกอย่างลง MLflow (เก็บ Parameters, Metrics, Artifacts)

**Phase 7: Walk Forward Validation (3 สัปดาห์ - *หัวใจหลัก*)**
- รัน Rolling Windows ตรวจสอบความเสถียร (Stability Analysis)
- *KPI:* PF > 1.5, Sharpe > 1.5, DD < 15%, PF Std < 0.2

**Phase 8: ONNX Deployment Pipeline (2 สัปดาห์)**
- Export 3 ไฟล์หลัก: `model.onnx`, `feature_order.json`, `model_config.json`
- *KPI:* Python Prediction vs ONNX Prediction ตรงกัน > 99.9%

---

## 🚀 Phase 9-12: PRODUCTION READY (การเทรดจริงบน MT5)

**Phase 9: MT5 Integration (4 สัปดาห์)**
- เขียน MQL5 แยกเลเยอร์: Feature Engine, ONNX Runtime, Signal Layer, Logging

**Phase 10: Position Sizing Engine (2 สัปดาห์)**
- สูตรคำนวณ Lot: `(Base Risk % × Confidence × Regime) ÷ ATR`

**Phase 11: Risk Engine (3 สัปดาห์)**
- ด่านสกัดความเสี่ยง: Daily Loss, Drawdown, Spread Filter, News Filter, Exposure Limit

**Phase 12: Execution Engine (3 สัปดาห์)**
- บริหารออเดอร์: Smart Entry, Smart Exit (Trailing Stop, Partial Close, Scale Out)

---

## 🏢 Phase 13-16: QUANT PLATFORM (สเกลระดับกองทุน)

**Phase 13: Monitoring Platform (3 สัปดาห์)**
- ตรวจสอบ Data Drift (PSI) และ Concept Drift (NannyML / Champion vs Challenger)

**Phase 14: Portfolio Engine (4 สัปดาห์)**
- จัดการเงินทุน (Capital Allocation), เช็ค Correlation Matrix เพื่อป้องกันการอมความเสี่ยงซ้ำซ้อน

**Phase 15: Regime Detection & Strategy Router (4 สัปดาห์)**
- แบ่งสภาวะตลาด (Trend, Range, Volatility) แล้วส่งคำสั่งให้โมเดลเฉพาะทางทำงาน (Trend Model / Mean Reversion)

**Phase 16: Auto Retraining (2 สัปดาห์)**
- ตั้ง Trigger: หาก `PSI > 0.25` **AND** `PF Drop > 20%` ระบบจะสั่งเทรนตัวเองใหม่ผ่าน Prefect Pipeline พร้อมมีแผน Rollback

**Phase 17 (Advanced/V4): Meta-Labeling & Microstructure (Optional/Next Step)**
- สร้างโมเดล 2 ชั้น (Base Model + Meta Model) คัดกรองออเดอร์ขยะสำหรับรันเทรดในกราฟ 15m/30m
- ดึงข้อมูล Alternative Data (เช่น Funding Rates, Market Microstructure) และ Time-of-Day Features สำหรับแก้ปัญหา BTC และ GOLD

---

## 📊 Executive KPI Dashboard (เป้าหมายสูงสุด)

- **Data:** Completeness > 99%, Duplicate = 0%, Missing < 1%
- **Trading:** Profit Factor > 1.5, Sharpe > 1.5, Drawdown < 15%, Win Rate > 40%
- **Model:** WFA Passed, Drift Controlled, Explainability Available (SHAP)
- **Production:** Uptime > 99%, Prediction Latency < 100 ms, Rollback Available

> **ลำดับความสำคัญของ PM (Top 10 Priority):**
> 1. Data Platform  ➔  2. Feature Store  ➔  3. Walk Forward Validation  ➔  4. ONNX Integration  ➔  5. Position Sizing  ➔  6. Risk Engine  ➔  7. Execution Engine  ➔  8. Monitoring  ➔  9. Portfolio Engine  ➔  10. Strategy Router