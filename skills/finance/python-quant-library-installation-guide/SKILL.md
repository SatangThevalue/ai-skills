---
name: python-quant-library-installation-guide
description: "คู่มือการติดตั้ง 15 Library Stack แบบแบ่ง 3 Phases (Research, Training, Production) และ Workflow สำหรับระบบ AI Trading"
---

# Python Quant Library Installation & Workflow Guide

การขึ้นระบบ AI Trading ระดับโปรดักชั่น ไม่ควรติดตั้งทุก Library พร้อมกันในวันแรก แต่ควรแบ่งออกเป็น 3 Phases เพื่อลดปัญหา Dependency และให้ง่ายต่อการ Debug:
`Phase 1: Research Environment` → `Phase 2: Training & MLOps` → `Phase 3: Production Deployment`

---

## 0. เตรียม Python Environment

แนะนำให้ใช้ **Python 3.12** และใช้เครื่องมือ **`uv`** (แทน pip/venv ธรรมดา) เพื่อความรวดเร็วในการจัดการ Dependency ขนาดใหญ่ของงาน Quant
*(การใช้เวอร์ชันใหม่เกินไปเช่น 3.14 อาจทำให้แพ็กเกจรุ่นเก่าเกิดข้อผิดพลาดในการติดตั้ง)*

```bash
# สร้าง Environment ด้วย uv
uv venv --python 3.12

# Activate (Windows)
.venv\Scripts\activate

# Activate (Linux / WSL)
source .venv/bin/activate

# หมายเหตุ: ในขั้นตอนถัดไปทั้งหมด ให้ใช้คำสั่ง `uv pip install` แทน `pip install`
```

---

## 1. Phase 1: Research Environment (ฐานราก)

กลุ่มนี้ใช้สำหรับการจัดการข้อมูล ทำ Data Analysis และเก็บ Data
```bash
uv pip install numpy pandas polars pyarrow scipy duckdb matplotlib seaborn plotly
```

**Workflow:** `MT5 Data` → `DuckDB` → `Polars` → `Data Analysis` → `Feature Engineering`
- **Polars:** ทำงานเร็วกว่า Pandas แนะนำให้ใช้เป็นหลักในการทำ Feature Engineering, Join, Aggregation
- **DuckDB:** เก็บ OHLCV, Features, Backtest Results แบบ Data Lake (`bronze/`, `silver/`, `gold/`) แทนไฟล์ Excel

---

## 2. Phase 2: Data Collection & Feature Engineering

เตรียมข้อมูลจาก MT5 และสกัดฟีเจอร์ด้วย `pandas-ta`
```bash
pip install pandas-ta
```
*(หมายเหตุ: แพ็กเกจ `MetaTrader5` สำหรับ Python รองรับเฉพาะ Windows เท่านั้น หากรันบน Linux VPS ให้ข้ามการติดตั้งแพ็กเกจนี้ และใช้ MQL5 EA บน MT5 Windows โยนข้อมูลมาแทน)*

**Workflow:** `MT5` → `Polars DataFrame` → `pandas-ta (Indicators)` → `Feature Store`
- ใช้สร้าง RSI, MACD, ATR, ADX, Bollinger, EMA
- **⚠️ เทคนิคสำคัญ:** ห้ามส่ง EMA20 หรือ EMA50 ตรง ๆ เข้าโมเดล แต่ต้องสร้างเป็น `EMA_GAP` หรือ `EMA_SLOPE` เสมอ (ดูรายละเอียดที่สกิล `quant-feature-design-document`)

---

## 3. Phase 3: Feature Selection & Model Training (แกนกลาง ML)

กรองฟีเจอร์ที่ไม่จำเป็นออก และเทรนโมเดลตัวหลัก
*(หมายเหตุ: หากใช้ Python 3.12 ขึ้นไป บางแพ็กเกจการเงินรุ่นเก่าเช่น `empyrical` อาจเกิดข้อผิดพลาดในการติดตั้ง แนะนำให้ข้ามไปใช้ `quantstats` แทน)*

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
pip install optuna quantstats
```

**Workflow:** `LightGBM` → `Optuna` → `Walk Forward (Time Series Split)` → `QuantStats`
- **Optuna:** เริ่มต้น `n_trials=100`, โปรดักชั่น `n_trials=300-500` (ให้ Optimize ด้วยโจทย์ Maximize Sharpe Ratio แทน Accuracy)
- **Walk Forward:** (เช่น Train 2020-2022 -> Test 2023, จากนั้นเลื่อน Train 2021-2023 -> Test 2024)

---

## 5. Phase 5: Explainability (XAI) & Experiment Tracking

ตอบคำถามว่าโมเดลกด BUY เพราะอะไร และเก็บประวัติการเทรน
```bash
uv pip install shap mlflow
```

**Workflow:** `Model` → `SHAP` → `Feature Ranking` → `MLflow Model Registry`
- **SHAP:** ดูสัดส่วนความสำคัญ (เช่น RSI 25%, ATR 20%, ADX 15%) แล้วนำมาตัดฟีเจอร์ที่ไม่มีประโยชน์ออก
- **MLflow:** บันทึก Parameters, Metrics, Artifacts, Models (เปรียบเทียบ Sharpe Ratio ระหว่าง Model_V1 กับ V2 ได้)

---

## 6. Phase 6: Orchestration, ONNX & Production

แปลงโมเดลส่งเข้า MT5 และสร้างระบบ MLOps อัตโนมัติ
```bash
uv pip install onnx onnxruntime onnxmltools skl2onnx prefect evidently prometheus-client loguru pydantic-settings
```

**Workflow:** `Prefect` → `LightGBM` → `ONNX` → `MT5 EA` → `Evidently` → `Retrain`
- **ONNX:** ต้องทดสอบผ่าน `onnxruntime` ก่อนส่งเข้า MT5 เสมอ
- **Prefect:** จัดตารางเวลา (เช่น 02:00 Fetch Data, 02:30 Train, 03:00 Validate)
- **Evidently:** ใช้ตรวจ Data Drift หากค่า `PSI > 0.25` ให้สั่ง Trigger Retraining อัตโนมัติ
- **Loguru / Pydantic-Settings:** ใช้จัดการ Config (`dev.yaml`, `prod.yaml`) และระบบ Logging ที่ดีกว่ามาตรฐาน

---

## ⚠️ ข้อควรระวังและการแก้ปัญหา (Implementation Troubleshooting)
การนำ Stack นี้ไปติดตั้งและเขียนโค้ดรันจริงบนสภาพแวดล้อม VPS มักจะพบปัญหาความเข้ากันได้ของไลบรารีและฮาร์ดแวร์ เช่น `MetaTrader5` รันบน Linux ไม่ได้, `Polars` แคชบน CPU เก่า, หรือ `MLflow` deprecation errors.
👉 **อ่านวิธีแก้ปัญหาโค้ดและไลบรารีทั้งหมดได้ที่ไฟล์อ้างอิง:** `references/execution-troubleshooting.md`

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

## ⚠️ Troubleshooting & VPS Hardware Limits

เมื่อนำ Stack นี้ไปติดตั้งบน VPS ขนาดเล็กหรือ CPU รุ่นเก่า มักพบปัญหา 2 ประการ:
1. **Disk Space Exhaustion (No space left on device):** การแตกไฟล์ (Extract) ของแพ็กเกจสาย Data (เช่น `scipy`, `polars`, `onnxruntime`) ผ่าน `uv pip` ใช้พื้นที่ดิสก์มหาศาล *วิธีแก้:* เคลียร์แคชด้วย `rm -rf ~/.cache/uv` และเคลียร์ Docker ขยะด้วย `docker system prune -a --volumes` ก่อนติดตั้ง
2. **Illegal instruction (core dumped):** เกิดจาก CPU ของ VPS เก่าเกินไปและขาดชุดคำสั่ง `avx2` หรือ `fma` ทำให้รัน `polars` หรือ `lightgbm` สมัยใหม่ไม่ได้ *วิธีแก้:* สำหรับ Polars ให้ลง `polars[rtcompat]` แทน หรือย้าย Pipeline ส่วน Training ไปรันบน Local PC/Mac ที่มี CPU ทันสมัยกว่า

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

---

## ⚠️ Known Pitfalls & Linux VPS Limitations (ข้อควรระวังหน้างาน)
เมื่อนำ Stack เหล่านี้ไป Deploy บน Linux VPS มักจะเจอข้อจำกัดทาง OS และ Hardware ดังนี้:

1. **MetaTrader5 is Windows-Only:** แพ็กเกจ `MetaTrader5` ใน Python มีเฉพาะ wheel สำหรับ Windows (`win_amd64`) **ห้ามติดตั้งบน Linux เด็ดขาด** หากใช้ Linux VPS ให้ดึงข้อมูลผ่าน `yfinance`/`ccxt` แทน แล้วให้ฝั่ง Windows รัน MT5 คอยรับไฟล์ `.onnx` ไป Execute
2. **CPU เก่าไม่มี AVX2 (Illegal instruction):** VPS รุ่นเก่ามักไม่มีชุดคำสั่ง `avx2` / `fma` ทำให้เมื่อรัน `polars` หรือ `LightGBM` จะเกิด Error `core dumped` **วิธีแก้:** ให้ติดตั้ง `polars-lts-cpu` แทน `polars` ปกติ
3. **Python Version Conflict:** `pandas-ta` บังคับใช้ **Python 3.12+** ในขณะที่ไลบรารีเก่าอย่าง `empyrical` พังบน Python 3.12 (เพราะโมดูล `SafeConfigParser` ถูกถอดออก) **วิธีแก้:** ใช้ Python 3.12 เป็นแกนหลัก และตัด `empyrical` ทิ้งโดยหันไปใช้ `quantstats` แทน 100%
4. **Prefect Ephemeral Timeout:** บน VPS ที่ทรัพยากรน้อย การรัน `@flow` อาจจะ Timeout ระหว่างรอเปิด Ephemeral Server **วิธีแก้:** ตอนเทสต์ Local ให้รันฟังก์ชันตรงๆ ผ่าน `task_name.fn()` เพื่อ Bypass ตัว Orchestrator ไปก่อน

> *ถ้าเข้าใจเครื่องมือเหล่านี้และหลีกเลี่ยงข้อจำกัดของ Environment ได้ คุณจะสามารถสร้างระบบ AI Trading แบบครบวงจร ตั้งแต่ Data → Train → Optimize → Deploy → Monitor → Retrain ได้ในระดับ Production ของจริง*

---

## 🛑 Troubleshooting & Known Infrastructure Pitfalls

1. **MetaTrader5 on Linux VPS:** The `MetaTrader5` Python package **only supports Windows (`win_amd64`)**. You cannot `pip install metatrader5` on an Ubuntu/Linux VPS. The architecture MUST split: Python/MLOps on Linux, MT5 Terminal + Execution on Windows.
2. **Polars on Older VPS CPUs:** Default `polars` requires modern CPU instructions (AVX2/FMA). If your VPS has an older CPU, importing polars or training will crash with `Illegal instruction (core dumped)`. **Fix:** Install `polars[rtcompat]` instead.
3. **Disk Space Exhaustion during `uv` Install:** Extracting heavy data science wheels (`scipy`, `polars`, `onnxruntime`) via `uv` takes gigabytes of temporary space. If you hit `No space left on device (os error 28)`, immediately clear the cache: `rm -rf ~/.cache/uv` or `docker system prune` to free up root partition space.

## Pitfalls (ข้อควรระวังหน้างานจริง)
- **MetaTrader5 บน Linux VPS:** ไลบรารี `MetaTrader5` ใน Python มีเฉพาะ wheel สำหรับ Windows (`win_amd64`) เท่านั้น **ติดตั้งบน Linux ไม่ได้** หากรัน Backend บน Ubuntu ให้ตัด `MetaTrader5` ออกจาก `requirements.txt` (พึ่งพาสถาปัตยกรรม Python บน Linux เทรนโมเดล -> Export `.onnx` -> MT5 EA บน Windows โหลด ONNX ไปรันและดึงข้อมูลแทน)
- **Dependency Conflicts (`empyrical` vs `pandas-ta`):** `pandas-ta` บังคับใช้ Python >= 3.12 แต่แพ็กเกจเก่าอย่าง `empyrical` จะพังบน Python 3.12 (เพราะ `configparser.SafeConfigParser` ถูกถอดออกจาก Python) **วิธีแก้:** ใช้ Python 3.12, เลิกใช้ `empyrical` แล้วหันมาใช้ `quantstats` คำนวณ Sharpe/Sortino แทน 100%
- **Disk Space เต็มตอนติดตั้ง:** การรัน `uv pip install` แพ็กเกจสาย Data (SciPy, Polars, ONNX) จะมีการแตกไฟล์ `.so` ที่กินพื้นที่มหาศาล (อาจเจอ `No space left on device`) **วิธีแก้:** ต้องเคลียร์ `~/.cache/uv` (`uv cache clean`) หรือจัดการพื้นที่ Docker / Node modules บน VPS ก่อนติดตั้งเซ็ตใหญ่