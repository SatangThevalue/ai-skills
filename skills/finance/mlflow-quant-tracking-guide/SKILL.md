---
name: mlflow-quant-tracking-guide
description: "คู่มือการออกแบบ MLflow Tracking, Naming Convention และ Artifacts สำหรับ AI Quant Trading ระดับสถาบัน"
---

# MLflow สำหรับ Quant Trading (Trading Research Memory)

สำหรับ MLOps Architect และ Quant PM **MLflow ไม่ใช่แค่ที่เก็บไฟล์ `model.pkl` หรือ `accuracy`** แต่คือ "Trading Research Memory" ขององค์กร 

ในโปรเจกต์ AI Trading เราต้องสามารถย้อนกลับไปตอบคำถามได้เสมอว่า: *โมเดลไหนกำไรดีสุด? ใช้ Feature อะไร? Dataset เวอร์ชันไหน? Profit Factor เท่าไร?*

---

## 1. เป้าหมายของ MLflow ในโปรเจกต์นี้
MLflow ต้องเก็บข้อมูล 12 มิติให้ครบวงจร:
1. Experiment, 2. Dataset, 3. Features, 4. Labels, 5. Parameters, 6. Metrics, 7. Models, 8. ONNX, 9. Backtest, 10. Walk Forward, 11. Deployment, 12. Production Monitoring

---

## 2. โครงสร้างและ Naming Convention

### โครงสร้างระดับโปรเจกต์ (Project Structure)
แบ่งระดับโฟลเดอร์ให้ชัดเจน:
`Trading Platform` -> `EURUSD` (Trend, Range, Ensemble) -> `XAUUSD`

### ชื่อ Experiment (Experiment Name)
**Format:** `ASSET_MODEL_TARGET_VERSION`
**ตัวอย่าง:**
- `EURUSD_LGBM_DIRECTION_V1`
- `XAUUSD_LGBM_REGIME_V2`

### ชื่อการทดลอง (Run Name) - สำคัญมาก
**Format:** `DATE_SYMBOL_TIMEFRAME_FEATURESET`
**ตัวอย่าง:** `20260831_EURUSD_H1_FS_V1`

---

## 3. การออกแบบ Tag (Tag Design)
อย่ามองข้าม Tag เด็ดขาด ใช้สำหรับ Query ดูข้อมูลย้อนหลัง:
```json
{
    "symbol": "EURUSD",
    "timeframe": "H1",
    "market": "Forex",
    "model": "LightGBM",
    "feature_version": "FS_V2",
    "label_version": "LB_V3",
    "dataset_version": "DS_V5",
    "researcher": "Thanapon",
    "stage": "Research"
}
```

---

## 4. Metadata ที่ต้อง Track ทุกครั้ง

### Dataset & Feature & Label Version
- **Dataset:** `{"rows": 500000, "start_date": "2020-01-01", "end_date": "2026-01-01"}` (เช่น `DS_EURUSD_H1_2020_2026_V1`)
- **Feature Version:** `FS_V1`
- **Label Version:** เช่น `LB_V2` (อ้างอิงเป้าหมาย เช่น Triple Barrier TP=30, SL=20, HOURS=12)

### Hyperparameters (LightGBM & Optuna)
ต้อง log ค่าที่ใช้จริงทั้งหมด: `learning_rate`, `num_leaves`, `max_depth`, `feature_fraction`
สำหรับ Optuna ให้เก็บ `trial_count` และ `best_sharpe` เพิ่มเติม

### Feature Selection Tracking
ให้เก็บจำนวน Feature ที่รอดชีวิตจาก Funnel เสมอ เพื่อวิเคราะห์ภายหลัง:
`initial_features=126` -> `corr_filtered=88` -> `mi_selected=60` -> `shap_selected=42`

---

## 5. Metric ที่ต้อง Log (Trading > Classification)

ห้ามสนใจแค่ Classification Metrics (Accuracy, F1, AUC) แต่ต้อง Log **Trading Metrics** ให้ครบ:

```python
mlflow.log_metrics({
    "profit_factor": 1.82,
    "sharpe": 1.65,
    "sortino": 2.11,
    "drawdown": 9.3,
    "win_rate": 46.2,
    "expected_value": 8.2
})
```

### Walk Forward Tracking (หัวใจสำคัญ)
ถ้าแบ่ง Walk Forward เป็น 4 Window ให้ Log แยกรายตัว และ Log ค่าสถิติรวม:
- `wf1_pf`, `wf2_pf`, `wf3_pf`, `wf4_pf`
- **`mean_pf=1.73`**, **`std_pf=0.08`** (ค่าความเสถียร)

---

## 6. สิ่งที่ต้องโยนเข้า Artifacts (หลักฐานการวิจัย)

ทุกๆ การรัน 1 ครั้ง ต้องโยนไฟล์เหล่านี้เก็บเป็น Artifacts:
1. `model.pkl` (โมเดลต้นฉบับ)
2. **`model.onnx`** (โมเดลสำหรับ MT5)
3. **`selected_features.json`** (รายชื่อ Feature ที่เข้ารอบ)
4. `feature_importance.csv`
5. **`shap_summary.png`**
6. **`backtest_report.html`** (จาก QuantStats)
7. `walkforward_report.html`
8. `confusion_matrix.png`
9. `dataset_profile.json`

---

## 7. Model Registry & Promotion Policy

โมเดลทั้งหมดต้องผ่านท่อ (Pipeline) ต่อไปนี้ตามลำดับ (ห้ามลัดขั้นตอน):
**`Research`** ➔ **`Staging`** ➔ **`PaperTrade`** ➔ **`Production`** ➔ **`Archived`**

---

## 8. Monitoring & Drift Tracking

สร้าง Experiment แยกชื่อ `PRODUCTION_MONITORING` เพื่อ Track โมเดลที่รันอยู่จริง
- เก็บ Trading Log: `daily_profit`, `daily_drawdown`, `weekly_sharpe`, `monthly_pf`
- เก็บ Drift Log (รายวัน): **`psi_score`**, `feature_drift_count`, `concept_drift_score` 
*(ตัวอย่าง: หาก `psi_score = 0.31` ให้ระบบ Trigger Retrain ทันที)*

---

## ✅ Checklist ทุกครั้งที่ Training (The Gold Standard Run)

ก่อนจบการรัน 1 ครั้ง ต้องมั่นใจว่าใน MLflow มีข้อมูลเหล่านี้ครบ:
- [ ] Dataset / Feature / Label Version
- [ ] Hyperparameters
- [ ] Feature Count & Selected Features list
- [ ] Classification Metrics
- [ ] Trading Metrics (PF, Sharpe, Drawdown)
- [ ] Walk Forward Metrics (รวมถึงค่า Mean/Std)
- [ ] SHAP Report (รูปภาพ)
- [ ] Feature Importance (CSV)
- [ ] Backtest Report (HTML)
- [ ] **ONNX File (สำคัญที่สุดสำหรับการนำไปใช้)**
- [ ] Production Readiness Score

> **บทสรุป:** หากคุณเก็บข้อมูล MLflow ตามโครงสร้างนี้ คุณจะสามารถย้อนกลับไปทำซ้ำ (Reproduce) ได้ 100% ว่าโมเดลนี้ใช้อะไร ทำไมถึงแม่นยำ ซึ่งเป็นมาตรฐานการทำงานของทีม Quant และ MLOps ระดับโลก