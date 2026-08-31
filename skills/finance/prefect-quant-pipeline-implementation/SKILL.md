---
name: prefect-quant-pipeline-implementation
description: "คู่มือการเขียนโค้ดและขึ้นระบบ Prefect Orchestration สำหรับ Quant Trading (ต่อยอดกับ MLflow, PostgreSQL, Optuna, ONNX)"
---

# ภาคปฏิบัติ: การสร้าง Quant Pipeline ด้วย Prefect

นี่คือคู่มือภาคปฏิบัติที่เจาะลึกการเขียนโค้ดและสร้างระบบ MLOps Platform โดยใช้ **Prefect เป็นแกนหลัก (Nervous System)** คุมทุกอย่างตั้งแต่การดึงข้อมูลไปจนถึง Auto-Retraining 

*(สำหรับภาพรวมและสถาปัตยกรรม อ่านได้ที่สกิล `prefect-quant-orchestration`)*

---

## 1. การเตรียมสภาพแวดล้อม (Environment)

**ติดตั้ง Prefect:**
```bash
pip install prefect
```

**เริ่ม Prefect Server (สำหรับ Local Development):**
```bash
prefect server start
```
*ระบบจะเปิด API Server, Database, และ Dashboard ให้ที่ `http://127.0.0.1:4200`*

---

## 2. โครงสร้างโปรเจกต์ระดับโปรดักชั่น

ควรแยกไฟล์ Flow (ร้อยเรียงท่อ) ออกจาก Task (งานย่อย):
```text
project/
├── flows/
│   ├── data_flow.py
│   ├── feature_flow.py
│   ├── training_flow.py
│   ├── deploy_flow.py
├── tasks/
│   ├── data_tasks.py
│   ├── feature_tasks.py
│   ├── training_tasks.py
├── config/
├── models/
├── data/
├── mlruns/
└── requirements.txt
```

---

## 3. ตัวอย่างการดึงข้อมูลแบบ Parallel

ใช้ความสามารถของ Prefect ในการดึงหลาย API พร้อมกัน (เร็วขึ้นมาก):

```python
from prefect import task, flow
import yfinance as yf

# Task สามารถตั้งค่า Retry, Delay และ Monitoring ได้ทันที
@task(retries=3, retry_delay_seconds=10)
def fetch_market_data():
    return yf.download("EURUSD=X", interval="1h", period="30d")

@task
def fetch_fred_data(): ...

@task
def fetch_news(): ...

@flow
def collect_all_data():
    # สั่งรัน Parallel ด้วย .submit()
    market = fetch_market_data.submit()
    fred = fetch_fred_data.submit()
    news = fetch_news.submit()

    return {
        "market": market.result(),
        "fred": fred.result(),
        "news": news.result()
    }
```

---

## 4. Prefect + PostgreSQL (แหล่งเก็บข้อมูลกลาง)

ฐานข้อมูลคือหัวใจของการสเกล แนะนำให้ใช้ PostgreSQL ทำหน้าที่: `Feature Store`, `Model Metadata`, `Prediction Logs`

**ตารางที่ควรมี:**
*(ดูโค้ดและดีไซน์ของตารางทั้ง 9 Layers แบบละเอียดได้ที่ `quant-database-architecture`)*
1. `market_data` (timestamp, open, high, low, close, volume)
2. `features` (feature_name, value, timestamp)
3. `predictions` (model_version, prediction, probability, timestamp)
4. `trades` (symbol, entry, exit, profit)
5. `model_metrics` (Sharpe, PF, Win Rate, Drawdown)

**ตัวอย่างโค้ด (การเซฟลง DB):**
```bash
pip install sqlalchemy psycopg2-binary
```
```python
from sqlalchemy import create_engine
engine = create_engine("postgresql+psycopg2://user:password@localhost:5432/trading")

@task
def save_market_data(df):
    df.to_sql("market_data", engine, if_exists="append", index=False)

@flow
def data_flow():
    data = fetch_market_data()
    save_market_data(data)
```

---

## 5. Prefect + MLflow (คู่หูสำคัญที่สุด)

Prefect ทำหน้าที่ "จัดการ Workflow" ส่วน MLflow ทำหน้าที่ "เก็บ Experiment & Registry"

**เริ่ม MLflow:**
```bash
pip install mlflow
mlflow ui
# เปิดที่ http://localhost:5000
```

**ตัวอย่าง Training Task ผสม MLflow:**
```python
import mlflow
from lightgbm import LGBMClassifier

@task
def train_model(X_train, y_train):
    with mlflow.start_run():
        model = LGBMClassifier()
        model.fit(X_train, y_train)

        # เก็บพารามิเตอร์และตัวชี้วัดลง MLflow
        mlflow.log_param("model", "lightgbm")
        mlflow.log_param("n_estimators", 100)
        mlflow.log_metric("accuracy", 0.65)
        mlflow.lightgbm.log_model(model, "model")
    return model

@flow
def training_flow():
    X_train, y_train = load_data()
    model = train_model(X_train, y_train)
```

---

## 6. Prefect + Optuna + MLflow (Production Tuning)

```python
@task
def objective(trial):
    params = {
        "num_leaves": trial.suggest_int("num_leaves", 16, 128)
    }
    score = train_and_validate(params)
    
    mlflow.log_params(params)
    mlflow.log_metric("score", score)
    return score
```

---

## 7. Auto Retrain Flow

ทริกเกอร์การเทรนใหม่เมื่อ `PSI > 0.25` หรือ `Sharpe < 1` (ประเมินโดย Evidently):

```python
@flow
def retrain_flow():
    drift = check_drift()
    if drift:
        training_flow()
        deploy_flow()
```

---

## 8. Full Production Master Flow

ร้อยเรียงทุกระบบเข้าด้วยกันเป็น Flow เดียว:

```python
@flow
def production_flow():
    raw_data = collect_data()
    features = generate_features(raw_data)
    model = train_model(features)
    metrics = validate_model(model)
    register_model(model)
    export_onnx(model)
    deploy_mt5()
```

---

## ⏰ Scheduling Strategy ที่ใช้งานจริง

- **ทุก 1 ชั่วโมง:** `Prefect` → `Yahoo/MT5/FRED` → `PostgreSQL`
- **ทุกวัน:** `Database` → `Feature Engineering` → `Feature Store`
- **ทุกสัปดาห์:** `Feature Store` → `LightGBM` → `Optuna` → `MLflow`
- **ทุกเดือน:** `Walk Forward` → `Promotion` → `ONNX` → `MT5`
- **ทุกวันหลัง Deploy:** `Predictions` → `PostgreSQL` → `Evidently` (เช็ค Drift) → `Retrain Flow`

> **โครงสร้างนี้ขยายไปสู่ Production และ Auto-Retraining ได้ง่ายที่สุด เพราะทุกอย่างตรวจสอบย้อนหลัง สั่ง Schedule และจัดการ Error ผ่านหน้าต่างของ Prefect ได้เบ็ดเสร็จ**