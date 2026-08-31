---
name: quant-trading-standard-framework
description: "มาตรฐานการดำเนินงานเชิง Quant สำหรับสินทรัพย์ทุกประเภท ครอบคลุม 17 Phases ตั้งแต่ Data ถึง MLOps Auto-Retraining"
---

# Quant Trading Standard Framework

Framework ฉบับนี้ออกแบบสำหรับบทบาท **Head of Quant Research / MLOps Architect / Project Manager** เพื่อใช้เป็น "มาตรฐานกลาง" สำหรับการพัฒนาระบบเทรดในทุกสินทรัพย์ (Forex, Stocks, Crypto, Indices, Commodity, Bond) บน Platform เดียวกัน

---

## 🛑 4 กฎเหล็กพื้นฐาน (The 4 Golden Rules)
1. **AI ≠ กลยุทธ์:** `Data + Research + Risk + Execution + Monitoring = กลยุทธ์`
2. **ห้ามใช้โมเดลโดยไม่มี Baseline:** ทุกโมเดลต้องทดสอบชนะระบบพื้นฐานก่อน (เช่น Buy & Hold, EMA Cross, RSI, Donchian)
3. **No Data Leakage 100%:** ข้อมูลอนาคตห้ามหลุดเข้ามาในอดีตตอนสร้าง Feature หรือ Label
4. **Reproducibility:** ทุกโมเดลต้องระบุ Dataset Version, Feature Version, Label Version, Model Version เพื่อย้อนกลับมาตรวจสอบและทำซ้ำได้

---

## 📈 The 17 Phases of Quant Research Lifecycle

### Phase 1: Market Research
ศึกษาพฤติกรรมสินทรัพย์ก่อนทำโมเดล
- **Forex:** Session, Spread, News Impact
- **Crypto:** 24/7 Market, Funding Rate, Fear & Greed
- **Stocks:** Market Open, Earning Reports, Sector Rotation

### Phase 2: Data Engineering
- **Sources:** MT5, Polygon, Yahoo Finance, CCXT, FRED, TradingEconomics, NewsAPI
- **Data Standard:** ทุก Source ต้องแปลงให้อยู่ในฟอร์แมตกลาง `symbol, timestamp, open, high, low, close, volume, spread`

### Phase 3: Data Quality
ทุก Dataset ต้องผ่านการตรวจสอบ:
- Missing Value < 1%, Duplicate = 0%, Timestamp Gap ไม่มีช่องว่าง, และเก็บ Outlier Report

### Phase 4: Feature Engineering & Governance
- **กลุ่ม Feature:** Price, Trend, Momentum, Volatility, Market Structure, Time, Regime, Macro
- **Feature Governance:** ทุก Feature ต้องบันทึก `Name, Version, Description, Owner, Created Date`

### Phase 5: Label Engineering
เป้าหมายที่ AI จะใช้เรียนรู้ (แนะนำวิธี *Triple Barrier*)
- **Label Governance:** ต้องมี Version, Definition, Parameters (เช่น `LB_V3: TP=30, SL=20, TTL=12H`)

### Phase 6: Feature Selection
`150 Features` ➔ `Variance Filter` ➔ `Correlation Filter` ➔ `Mutual Information` ➔ `RFE` ➔ `SHAP` ➔ `40 Features`

### Phase 7: Model Development
- **Baseline:** Logistic Regression, Random Forest
- **Candidate:** LightGBM, XGBoost, CatBoost
- **Advanced:** Transformer, TFT, LSTM

### Phase 8: Hyperparameter Optimization (HPO)
ใช้ Optuna โดยมี Objective เป็น **Profit Factor, Sharpe, Sortino** (ไม่ใช่ Accuracy)

### Phase 9: Walk Forward Testing
ห้ามใช้ Random Split ต้องใช้ Walk Forward เท่านั้น (Train 2020-2022 / Test 2023)
- **Minimum Acceptance:** PF > 1.5, Sharpe > 1.5, Drawdown < 15%

### Phase 10: Market Regime Detection
Model ต้องรู้สภาวะตลาดก่อน (Bull Trend, Bear Trend, Range, High/Low Volatility) แล้วเลือกรัน Strategy ที่เหมาะสม

### Phase 11: Portfolio Construction & Position Sizing
- **Portfolio:** ไม่คิดทีละสินทรัพย์ ให้คิด Portfolio Risk (Correlation, Exposure)
- **Position Sizing:** ไม่ใช้ Fixed Lot แนะนำให้ประยุกต์ใช้แบบผสมผสาน (1% Risk + Volatility Adjusted + Confidence Score) *(ดูสูตรคำนวณและวิธีออกแบบ Sizing Engine เจาะลึกได้ที่สกิล `quant-risk-sizing-drift-engine`)*

### Phase 12: Execution Layer
โมเดลห้ามยิง Order ตรง ต้องผ่าน **Risk Engine** และตรวจสอบ Spread, Slippage, Liquidity ก่อน *(ศึกษา กฎ 7 ข้อของ Risk Engine ได้ที่สกิล `quant-risk-sizing-drift-engine`)*

### Phase 13: Risk Management (Kill Switches)
- **Daily Loss:** -3% (หยุดระบบ)
- **Max Drawdown:** -10% (หยุดระบบ)
- **Consecutive Loss:** เสีย 10 ครั้งติด (หยุดระบบ)
- **Exposure Limit:** ถือครองไม่เกิน 20% ต่อสินทรัพย์

### Phase 14: Model Registry (MLflow)
บันทึกทุกอย่างลง MLflow: Dataset, Features, Labels, Hyperparameters, Metrics, Artifacts

### Phase 15: Deployment
ห้ามเอาขึ้น Production ตรง ๆ ต้องผ่าน: `Research` ➔ `Staging` ➔ `Paper Trade (30 วัน)` ➔ `Production`

### Phase 16: Monitoring
- **Data:** Missing Data, Feature Drift, Concept Drift *(วิธีการวัดผล Population Stability Index (PSI) แบบสถาบัน สามารถดูได้ที่สกิล `quant-risk-sizing-drift-engine`)*
- **Model:** Accuracy, Confidence, Prediction Distribution
- **Trading:** PF, Sharpe, Drawdown, Win Rate

### Phase 17: Retraining
ตั้งค่าเงื่อนไขให้เทรนใหม่เมื่อ: `PSI > 0.25`, `PF ลดลง 20%`, หรือ `Sharpe < 1`

---

## 📑 Quant Checklist (Gold Standard)

ทุกโมเดลต้องมีเอกสารอธิบาย Source/Version ของ Data, Feature, Model, และ Deployment
**Checklist อนุมัติระบบ:**
- [ ] **Data:** Standard Symbol, UTC Time, Missing/Duplicate Checked
- [ ] **Feature:** Feature Version, Feature Registry, Unit Tested
- [ ] **Label:** Label Registry, Label Version
- [ ] **Model:** Baseline Comparison, Optuna Tuning, Walk Forward Tested
- [ ] **Validation:** Sharpe/PF/Drawdown ผ่านเกณฑ์ Minimum Acceptance
- [ ] **Deployment:** ONNX Validation, Paper Trading, Rollback Plan
- [ ] **Monitoring:** Data Drift, Concept Drift, Trading Metrics

> **The Gold Standard Quant Workflow:**
> `Market Data` → `Data Validation` → `Feature Eng.` → `Feature Selection` → `Label Eng.` → `LightGBM` → `Optuna` → `Walk Forward` → `Regime Analysis` → `Portfolio Construction` → `Risk Engine` → `MLflow` → `ONNX` → `Paper Trading` → `Production` → `Monitoring` → `Drift Detection` → `Retraining`