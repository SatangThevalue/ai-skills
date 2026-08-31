---
name: prefect-quant-orchestration
description: "สถาปัตยกรรม MLOps สำหรับ Quant Trading โดยใช้ Prefect เป็น Orchestrator ผสาน Data Sources, MLflow, ONNX และ MT5 เข้าด้วยกัน"
---

# สถาปัตยกรรมระบบนิเวศน์ Prefect ใน Quant Trading

ข้อผิดพลาดสำคัญของนักพัฒนาคือการใช้ Prefect แค่แทน Cron Job (`Cron -> Run Script`) ซึ่งเสียของมาก ในโปรเจกต์ AI Trading ระดับโปรดักชั่น **Prefect ควรเป็น "ระบบประสาทส่วนกลาง" (Orchestrator)** ที่ทำหน้าที่ควบคุม Data Pipeline, Feature Pipeline, Training Pipeline, Deployment Pipeline, Monitoring Pipeline และ Retraining Pipeline ทั้งหมด

---

## 1. ภาพรวมสถาปัตยกรรม (The Nervous System)

```text
                Prefect
                    │
 ┌──────────────────┼──────────────────┐
 │                  │                  │
 ▼                  ▼                  ▼
Data Flow      Training Flow      Monitoring Flow
 │                  │                  │
 ▼                  ▼                  ▼
APIs          LightGBM          Drift Check
 ▼                  ▼                  ▼
Feature       Optuna            Alert
 ▼                  ▼                  ▼
Storage       MLflow            Retrain
 ▼                  ▼                  ▼
Feature Store Model Registry    Deploy
```

---

## 2. แหล่งข้อมูล (Data Sources) ที่แนะนำนอกเหนือจาก MT5
การใช้ราคา (Price) เดี่ยวๆ มักไม่พอ ควรมี Alternative Data ด้วย:

### 2.1 ตลาดการเงิน (Financial Data)
- **`yfinance`**: ข้อมูลฟรีและครอบคลุมสุด (Forex, Stocks, Crypto) เหมาะทำ Research
- **`polygon-api-client`**: สาย Production ที่นิ่งและแม่นยำกว่า Yahoo
- **`ccxt`**: สำหรับดึงข้อมูล Crypto จาก Exchange ชั้นนำ (Binance, Bybit) พร้อมกัน

### 2.2 ข้อมูลเศรษฐกิจ (Macro & Calendar) - สำคัญมาก
- **`tradingeconomics`**: ดึงเวลาเกิดข่าว CPI, NFP, GDP, Interest Rate
  - *Feature ที่ได้:* `hours_to_next_nfp`, `high_impact_news_flag`
- **`fredapi`**: ข้อมูล Macro ระดับชาติ
  - *Feature ที่ได้:* `us_10y_yield`, `fed_funds_rate`, `yield_spread`

### 2.3 ความเชื่อมั่นและข่าว (Sentiment & News)
- **`newsapi-python`** หรือ **`GDELT`**: ใช้นับจำนวนข่าว (news_count) หรือดึงความเห็นตลาด
- **Alternative.me**: API สำหรับ Crypto Fear & Greed Index

---

## 3. สถาปัตยกรรม Flow ย่อยใน Prefect (The Flows)

ควรแยก Flow หน้าที่ใครหน้าที่มัน:

### 1. Data Collection Flow (ดึงข้อมูล)
`Yahoo/Polygon/FRED` → `Raw Storage (PostgreSQL/DuckDB)`
```python
@flow
def collect_data_flow():
    market_data()
    economic_data()
    news_data()
    save_raw_data()
```

### 2. Feature Flow (สกัดและเก็บฟีเจอร์)
`Raw` → `RSI/ATR/ADX` → `Feature Store`
```python
@flow
def feature_flow():
    load_raw()
    create_features()
    validate()
    save_feature_store()
```

### 3. Training Flow (เทรนและทดสอบ)
`Feature Store` → `LightGBM` → `Optuna` → `Walk Forward`
```python
@flow
def training_flow():
    load_features()
    feature_selection()
    train_model()
    validate_model()
```

### 4. Deployment Flow (แปลงเป็น ONNX ส่ง MT5)
`LightGBM` → `ONNX` → `MT5` (ถ้ารัน `validate_onnx()` ไม่ผ่าน สั่ง Deploy Fail ทันที)
```python
@flow
def deploy_flow():
    export_onnx()
    validate_onnx()
    push_model()
```

### 5. Monitoring & Retraining Flow (ตรวจ Drift และซ่อมแซมตัวเอง)
`Prediction` → `Drift Check` → `Alert/Retrain`
- ตรวจจับโดย `Evidently` หากเจอ Drift (`PSI > 0.25`) หรือกำไรพอร์ตแย่ลง (`Sharpe < 1`) จะทริกเกอร์ `retrain_flow()` ทันที
```python
@flow
def monitor_flow():
    check_drift()
    check_performance()
    send_alert()
    
    if drift_detected or sharpe < 1:
        retrain_flow()
```

---

## 4. Scheduling Strategies (การจัดตารางเวลา)

- **ทุก 1 ชั่วโมง:** `Collect Data` (ดึงข้อมูลล่าสุด)
- **ทุกวัน:** `Feature Update` (อัปเดตฟีเจอร์ใหม่)
- **ทุกสัปดาห์:** `Retrain Candidate` (เทรนโมเดลสำรองเตรียมไว้)
- **ทุกเดือน:** `Production Model Evaluation` (ประเมินโมเดลหลักที่ใช้อยู่ว่าหมดสภาพหรือยัง)

---

## 5. การทำงานร่วมกันระหว่าง Prefect กับ Tools อื่นๆ

- **Prefect + MLflow:** รันเทรนเสร็จให้ Prefect ยิงเข้า MLflow ทันที *(ดูโครงสร้างและวิธีเก็บ Metadata/Metrics ระดับสถาบันลง MLflow ได้ที่สกิล `mlflow-quant-tracking-guide`)* ถ้าเจอว่า Model_V2 ได้ Sharpe 1.6 (ดีกว่า V1 ที่ได้ 1.2) Prefect จะ Promote โมเดล V2 เข้า Registry อัตโนมัติ
- **Prefect + PostgreSQL:** คุม Schema กลาง ได้แก่ `raw_market_data`, `features`, `predictions`, `trades`, `model_metrics`, `drift_reports` *(ดูการออกแบบ Table ทั้งหมดได้ที่สกิล `quant-database-architecture`)*
- **Prefect + Evidently:** เป็นหน้าด่านรับ Live Data เข้าไปเช็ค Data Drift เพื่อเป็นตัวจุดระเบิด (Trigger) สั่งเทรนใหม่

---

## 🚀 Roadmap การพัฒนา Platform (ฉบับสมบูรณ์)

- **Phase 1 (Data):** `Prefect + Yahoo Finance + DuckDB + Polars` (เป้าหมาย: Data Pipeline นิ่ง)
- **Phase 2 (Training):** `LightGBM + Optuna + MLflow` (เป้าหมาย: Training Pipeline รันได้)
- **Phase 3 (Deploy):** `ONNX + MT5` (เป้าหมาย: Deployment Pipeline ทำงานร่วมกันได้)
- **Phase 4 (Macro & Alt Data):** `TradingEconomics + FRED + Evidently` (เป้าหมาย: เพิ่ม Regime Detection และตรวจจับ Data Drift)
- **Phase 5 (Automation):** `Auto Retrain + Auto Deploy` (เป้าหมาย: Self-improving AI Trading Platform)

> **สรุป:** ถ้าจะทำสเกลโปรเจกต์นี้ให้สุด ให้ทุก Library ทำงานผ่าน Prefect Flows ทั้งหมด เพื่อให้ระบบตรวจสอบย้อนหลังได้, สั่ง Retry ได้เวลาแครช, ตั้ง Schedule ได้, และทำ Automation ได้ตั้งแต่ Data ไปจนถึง Retrain อย่างแท้จริง

*(ดูตัวอย่างการเขียนโค้ดสำหรับสร้าง Pipeline พวกนี้ทั้งหมดได้ที่สกิล `prefect-quant-pipeline-implementation`)*