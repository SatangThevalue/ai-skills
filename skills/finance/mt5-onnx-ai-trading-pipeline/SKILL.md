---
name: mt5-onnx-ai-trading-pipeline
description: Data Science pipeline and architecture for building AI Trading Systems for MT5 via ONNX.
category: finance
---

# 📈 MT5 ONNX AI Trading Pipeline (Data Science Perspective)

## 🎯 Trigger Conditions
- When designing an AI/ML trading system for MetaTrader 5 (MT5) using ONNX.
- When discussing Data Pipeline, Feature Engineering, Labeling, or Validation for quantitative trading models.
- When evaluating which machine learning model to use for trading (e.g., Deep Learning vs. Gradient Boosting).

## 🧠 Core Philosophy
**"กว่า 80% ของความสำเร็จมาจาก Data และ Validation ไม่ใช่ตัวโมเดลเอง"**

ห้ามเริ่มต้นด้วยคำถามว่า *"ใช้ Deep Learning อะไรดี?"* แต่ให้เริ่มตาม Framework นี้:
`Problem Definition` → `Data Pipeline` → `Feature Engineering` → `Model Selection` → `Validation` → `Deployment` → `Monitoring`

---

## 🏗️ ภาพรวม Architecture

```text
Market Data
    │
    ▼
Data Collection
    │
    ▼
Feature Engineering
    │
    ▼
Dataset Construction
    │
    ▼
Train ML/DL Model
    │
    ▼
Backtest + Walk Forward
    │
    ▼
Export ONNX
    │
    ▼
MQL5 EA (Live Trading)
    │
    ▼
Monitoring & Retraining
```

---

## 🛠️ Phase 1: Business Understanding (เป้าหมายต้องชัดเจน)

| Case | สิ่งที่ต้องการทำนาย | Problem Type |
|---|---|---|
| **Case 1** | ทิศทาง 1 ชั่วโมงข้างหน้า (UP / DOWN) | **Binary Classification** |
| **Case 2** | ราคาปิดในอนาคต (Future Close Price) | **Regression** |
| **Case 3** | แอคชั่นการเทรด (BUY / SELL / HOLD) | **Multi-Class Classification** |

---

## 📦 Phase 2: Data Collection (การเก็บรวบรวมข้อมูล)

### ข้อมูลที่ควรเก็บ
| กลุ่มข้อมูล | ตัวอย่าง Features |
|---|---|
| **OHLCV** | Open, High, Low, Close, Volume |
| **Indicators** | RSI, MACD, ATR, ADX |
| **Time** | Hour, Day, Month, Session |
| **Spread** | Bid-Ask Spread |
| **Volatility** | ATR, Historical Volatility (HV), Realized Volatility (RV) |
| **Market Structure** | Swing High, Swing Low |
| **Economic Data** | CPI, NFP, Interest Rate |

### Timeframe ที่นิยมตามสไตล์การเทรด
| ประเภท | Timeframe |
|---|---|
| **Scalping** | M1, M5 |
| **Intraday** | M15, H1 |
| **Swing** | H4, D1 |
| **Position** | D1, W1 |

---

## 🧬 Phase 3: Feature Engineering (ขั้นตอนที่ใช้เวลามากที่สุด)

* **Price Features:** Close Change %, High-Low Range, Body Size, Upper Shadow, Lower Shadow
* **Technical Features:** RSI, MACD, ATR, EMA20, EMA50, EMA200, Bollinger Band
* **Statistical Features:** Rolling Mean, Rolling Std, Skewness, Kurtosis, Z-score
* **Time Features:** Hour, Day of Week, Month, London Session, New York Session

---

## 🤖 Phase 4: Model Selection (การเลือกโมเดล)

### สิ่งที่ Hedge Fund ส่วนใหญ่ใช้จริง
หลายคนคิดว่า Hedge Fund ใช้ GPT, Transformer หรือ Deep Learning ขั้นสูง แต่ในทางปฏิบัติ **นิยมใช้ Gradient Boosting** (เช่น XGBoost, LightGBM, CatBoost) เนื่องจาก:
1. Train เร็ว
2. Overfit น้อยกว่า
3. ใช้ข้อมูลไม่เยอะเท่า Deep Learning
4. อธิบายผลลัพธ์ได้ (Explainable)

### Classical ML Comparison
| Algorithm | Accuracy | Speed | Explainable | ONNX Support |
|---|---|---|---|---|
| Logistic Regression | ปานกลาง | สูงมาก | ดีมาก | ดี |
| Random Forest | ดี | สูง | ดี | ดี |
| XGBoost | ดีมาก | สูง | ปานกลาง | ดี |
| **LightGBM 🏆** | **ดีมาก** | **สูงมาก** | **ปานกลาง** | **ดี** |
| CatBoost | ดีมาก | สูง | ดี | ดี |

*(🏆 แนะนำอันดับ 1 สำหรับ Trading Data: **LightGBM**)*

### Deep Learning Comparison
| Model | เหมาะกับ | ความซับซ้อน |
|---|---|---|
| MLP | Tabular Data | ต่ำ |
| CNN | Pattern Recognition | ปานกลาง |
| LSTM | Time Series | สูง |
| GRU | Time Series | ปานกลาง |
| Transformer | Long Sequence | สูงมาก |
| TFT | Financial Forecasting | สูงมาก |

### เปรียบเทียบประสิทธิภาพรวมสำหรับตลาดการเงิน
| Model | ความแม่นยำ | ความเร็ว |
|---|---|---|
| **LightGBM** | 9/10 | 10/10 |
| **XGBoost** | 9/10 | 8/10 |
| **Transformer** | 9/10 | 3/10 |
| **MLP** | 8/10 | 9/10 |
| **LSTM** | 8.5/10 | 5/10 |
| **GRU** | 8.5/10 | 6/10 |

---

## 🏷️ Phase 5: Label Engineering (ส่วนที่สำคัญที่สุดของการทำโมเดลเทรด)

* **วิธีที่ 1: Direction Label**
  * `Price(t+5) > Price(t)` = **BUY**
  * Else = **SELL**
* **วิธีที่ 2: Threshold Label**
  * `Up > 10 pips` = **BUY**
  * `Down > 10 pips` = **SELL**
  * `อื่นๆ` = **HOLD**
* **วิธีที่ 3: Triple Barrier (นิยมมากที่สุดใน Quant Finance) 🌟**
  * กำหนด 3 กรอบ: **Take Profit (TP)**, **Stop Loss (SL)**, **Time Limit (หมดเวลา)**
  * แตะฝั่งไหนก่อน ให้ Label ตามฝั่งนั้น (ใช้เพื่อจำลองพฤติกรรมการเทรดจริง)

---

## 🧪 Phase 6: Validation (ข้อควรระวังสำหรับมือใหม่)

🚨 **ข้อห้ามเด็ดขาด:** ห้ามทำ **Random Split** (เช่น Train 80% / Test 20% แบบสุ่ม) เพราะจะทำให้เกิด **Data Leakage** (โมเดลเห็นข้อมูลอนาคต)

✅ **วิธีที่ถูกต้อง (Best Practices):**
1. **Time Series Split:**
   * Train: `2020 - 2023`
   * Test: `2024`
2. **Walk Forward Validation:** เลื่อนหน้าต่างเวลาไปเรื่อยๆ เพื่อจำลองสถานการณ์จริง
   * *รอบที่ 1:* Train `2020-2022` ➡️ Test `2023`
   * *รอบที่ 2:* Train `2021-2023` ➡️ Test `2024`
