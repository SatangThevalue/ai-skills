---
name: quant-database-architecture
description: "สถาปัตยกรรมฐานข้อมูลสำหรับ Quant Trading (PostgreSQL Schema) รองรับ Multi-Asset, Feature Store, และ MLOps"
---

# สถาปัตยกรรมฐานข้อมูล Quant Platform (PostgreSQL)

ในมุมมองของ MLOps Architect และ Quant PM กฎเหล็กข้อแรกของการออกแบบฐานข้อมูลคือ: **"ห้ามออกแบบฐานข้อมูลตาม Source แต่ให้ออกแบบตาม Business Domain"**
วันนี้คุณอาจใช้ MT5, Yahoo Finance, Polygon แต่พรุ่งนี้คุณอาจเปลี่ยน API ดังนั้นทุกสินทรัพย์ต้องถูกแปลงให้อยู่ในรูปแบบมาตรฐาน (Canonical Symbol) ภายใต้ Schema เดียวกัน

---

## 🏗️ 9 Layers of Quant Database Schema

โครงสร้างนี้รองรับทั้ง Forex, Crypto, Stocks และ Alternative Data (ข่าว, ปฏิทินเศรษฐกิจ)

### Layer 1: Master Data (บัญชีสินทรัพย์กลาง)
- **`assets`**: เก็บข้อมูลสินทรัพย์แบบมาตรฐาน (เช่น `EURUSD`, `BTCUSDT`) ควรกำหนด `UNIQUE(symbol)`
- **`asset_sources`**: จับคู่สินทรัพย์เดียวที่มาจากหลาย Source
  - *เช่น EURUSD = `MT5: EURUSD`, `Yahoo: EURUSD=X`, `Polygon: C:EURUSD`*

### Layer 2: Raw Market Data
- **`market_ohlcv`**: ตารางกลางสำหรับกราฟแท่งเทียน (รองรับทั้ง MT5, Yahoo, CCXT)
  - *คอลัมน์:* `asset_id, timeframe, timestamp, open, high, low, close, volume, spread, source`
  - *Index:* `(asset_id, timeframe, timestamp)`
- **`market_ticks`**: สำหรับเก็บ Tick Data (แนะนำใช้ TimescaleDB หรือ ClickHouse แทนถ้าระดับ Tick จริงจัง)
- **`economic_events`**: ปฏิทินเศรษฐกิจ (CPI, NFP, GDP)
- **`news_events`**: ข่าวสาร (หัวข้อข่าว, Sentiment Score)

### Layer 3: Feature Store (หัวใจของระบบ)
- **`feature_definitions`**: เก็บ Metadata (เช่น `RSI14: FS_V1`, `ATR_RATIO: FS_V2`)
- **`feature_values`**:
  - *แบบ Long Table:* ยืดหยุ่น เพิ่ม Feature ใหม่ได้ทันทีโดยไม่ต้อง ALTER TABLE (`asset_id, timestamp, feature_id, value`)
  - *แบบ Wide Table (แนะนำสำหรับ Production):* โหลดเข้า LightGBM ได้เร็วกว่า (`timestamp, asset_id, RSI14, ATR_RATIO, MACD`)

### Layer 4: Label Store
- **`label_definitions`**: เก็บคำอธิบายเป้าหมาย (เช่น `DIRECTION_5BAR: LB_V1`)
- **`labels`**: ค่า Label เป้าหมาย (`asset_id, timestamp, label_version, target`)

### Layer 5: Training Dataset (เพื่อการ Audit)
- **`datasets`**: `dataset_id, version, start_date, end_date, symbol, rows`

### Layer 6: Model Registry Metadata
แม้จะใช้ MLflow แต่ควรเชื่อม ID กลับมาที่ PostgreSQL ด้วย
- **`models`**: `model_id, mlflow_run_id, model_name, model_version`
- **`model_metrics`**: `model_id, accuracy, f1, profit_factor, sharpe, drawdown`

### Layer 7: Prediction Store
- **`predictions`**: เก็บคำทำนายก่อนยิงออเดอร์ (`asset_id, timestamp, model_id, prediction, probability, regime`)

### Layer 8: Trading Store
- **`trades`**: ผลการเทรดจริงจาก MT5 (`ticket, asset_id, entry_time, exit_time, direction, entry_price, exit_price, profit`)

### Layer 9: Monitoring
- **`drift_reports`**: `feature_name, psi_score, drift_status`
- **`production_metrics`**: `date, sharpe, drawdown, profit_factor, win_rate`

---

## 🔄 Data Flow ภาพรวม

```text
[MT5, Yahoo, CCXT, Polygon, FRED]
        │
        ▼
Asset Mapping Layer (แปลงเป็น Canonical Symbol)
        │
        ▼
market_ohlcv (ตารางราคากลาง)
        │
        ▼
Feature Pipeline -> Feature Store -> Label Store
        │
        ▼
LightGBM -> MLflow -> Predictions
        │
        ▼
MT5 Trading (Execution)
        │
        ▼
Monitoring (Drift & Production Metrics)
```

---

## ✅ PM Checklist สำหรับ Database (ต้องมีก่อนขึ้น Production)

**Master Data & Market Data**
- [ ] Asset Mapping & Canonical Symbol
- [ ] Timeframe Standardization & UTC Timestamp

**Feature & Label Store**
- [ ] Feature/Label Registry
- [ ] Feature/Label Versioning
- [ ] Feature Audit

**MLOps & Production**
- [ ] Dataset Versioning
- [ ] Model Metadata & Metrics History
- [ ] Prediction & Trade Logging
- [ ] Drift Reports Monitoring

> **บทสรุป:** โครงสร้าง Schema นี้สามารถรองรับสเกลตั้งแต่ MT5 เพียงตัวเดียว ไปจนถึงระบบ Multi-Asset Quant Platform ที่มีสินทรัพย์หลายร้อยตัวและโมเดลหลายเวอร์ชัน โดยยังรักษามาตรฐานข้อมูลเดียวกันทั้งหมดได้ 100%