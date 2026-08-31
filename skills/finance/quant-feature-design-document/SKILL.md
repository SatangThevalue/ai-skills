---
name: quant-feature-design-document
description: "คู่มือ Feature Design Document สำหรับวางโครงสร้าง Feature Engineering 11 Stages เพื่อสร้าง AI Trading ด้วย LightGBM/ONNX"
---

# Feature Design Document (Quant Trading)

ในการทำโปรเจกต์ AI Trading ด้วย MT5 + LightGBM กฎเหล็กของ Feature Engineer คือ: **"สร้าง Feature Design Document ก่อนเขียนโค้ดเสมอ"** 

`Raw Data` → `Feature Layer` → `Feature Validation` → `Feature Selection` → `Model`
(ไม่ใช่สร้าง Feature ไปเรื่อย ๆ แล้วโยนเข้าโมเดล)

---

## The 11-Stage Feature Engineering Architecture

สมมติมีข้อมูลดิบจาก MT5: `timestamp, open, high, low, close, tick_volume, spread`
เราจะไม่ส่งข้อมูลดิบเหล่านี้เข้าโมเดล แต่จะแปลงให้เป็นพฤติกรรมผ่าน 11 Stages ดังนี้:

### Stage 1: Price Action Features (ราคาเคลื่อนที่อย่างไร)
- `ret_1, ret_5, ret_20` (Return: `(close - close_1)/close_1`)
- `log_ret_1, log_ret_5` (Log Return)
- `mom_5, mom_20` (Momentum: แรงซื้อยังต่อเนื่องไหม)

### Stage 2: Candle Intelligence (พฤติกรรมแท่งเทียน)
- `body_size`: `abs(close-open)`
- `upper_shadow`: `high - max(open,close)`
- `lower_shadow`: `min(open,close) - low`
- `body_ratio`: `body_size / (high - low)` *(0.8+ = Strong Candle, 0.1 = Doji)*

### Stage 3: Trend Features (แนวโน้ม)
- ❌ ไม่ใช้: EMA20, EMA50 ตรง ๆ
- ✅ ใช้: **EMA Gap** `(EMA20-EMA50)/EMA50`
- ✅ ใช้: **EMA Alignment** (เช่น `EMA20 > EMA50 > EMA200 = 1`)
- ✅ ใช้: **EMA Slope** (เช่น `EMA20.diff(5)`) *ตอบว่าแนวโน้มกำลังเร่งหรือชะลอ*

### Stage 4: Momentum Features
- ❌ ไม่ใช้: RSI14 ตรง ๆ (ไม่สน 70/30)
- ✅ ใช้: **RSI Distance** (`RSI14 - 50`)
- ✅ ใช้: **RSI Slope** (`RSI14.diff(3)`)
- ✅ ใช้: **RSI Regime** (ถ้า `RSI > 60` เป็น bull_momentum)
- **MACD:** `macd_hist_slope`

### Stage 5: Volatility Features (สำคัญมากสำหรับ Forex)
- **ATR Ratio:** `ATR14 / ATR100` *(1.5+ = ตลาดผันผวนสูง, 0.7- = ตลาดนิ่ง)*
- **Bollinger Width:** `UpperBand - LowerBand`
- **Volatility Expansion:** `std20 / std100`

### Stage 6: Volume Features (ใช้ Tick Volume)
- **Volume Ratio:** `volume / volume_ma20` *(เช่น 2.5 หมายถึง Volume สูงกว่าปกติ 2.5 เท่า)*
- **Volume Z-score:** `(volume - mean) / std`

### Stage 7: Market Structure (ส่วนที่คนส่วนใหญ่มองข้าม)
- `high20`, `low20` (20-Bar High/Low)
- **Donchian Position:** `(close - low20) / (high20 - low20)`
  *(1.0 = ใกล้ Breakout ด้านบน, 0.0 = ใกล้ Breakout ด้านล่าง)*

### Stage 8: Statistical Features
- `mean20, std20`
- **Z-Score:** `(close - mean20) / std20` *(+2 = Overbought, -2 = Oversold)*

### Stage 9: Time Features (มีผลมาก แต่คนมักลืม)
- `hour, dow` (Day of Week)
- `session`: `asia_session, london_session, newyork_session` *(เช่น London Open มักจะมีความผันผวนมากกว่าปกติ)*

### Stage 10: Regime Features
- **Trend Score (0-100):** รวม ADX + EMA Gap + EMA Slope
- **Volatility Score:** รวม ATR Ratio + BB Width
- **Composite Regime Score:** Trend + Volatility + Momentum

### Stage 11: Feature Interaction (จุดเปลี่ยนของ LightGBM)
การเอา Feature มาคูณกันเพื่อสร้างมิติใหม่:
- **Momentum + Volatility:** `RSI14 * ATR_RATIO`
- **Trend + Volume:** `volume_ratio * ADX14`
- **Breakout Strength:** `donchian_position * volume_ratio * ADX14`

---

## 🚀 Feature Set Roadmap

### V1 (เริ่มต้น) - ประมาณ 60 Features
- Return (8) + Candle (5) + Trend (10) + Momentum (8) + Volatility (8) + Volume (4) + Structure (4) + Time (4) + Interaction (8)

### V2 (ระบบนิ่งแล้ว) - ประมาณ 100-150 Features
- เพิ่ม **Multi-Timeframe Features:** `RSI_H1, RSI_H4, RSI_D1`
- เพิ่ม Market Regime Features เต็มรูปแบบ

---

## 🔍 Feature Selection Pipeline ที่แนะนำ

ในขั้นตอน Production บน MT5 + ONNX เราไม่ควรยัด 150 Features เข้าโมเดล (มันช้าและ Overfit ง่าย) ให้ใช้ Pipeline บีบอัดจนเหลือแต่หัวกะทิดังนี้:

```text
Generate Features (120 Features)
      ↓
Drop NaN
      ↓
Variance Threshold (ลบ Feature ที่ค่าคงที่)
      ↓
Correlation Filter (ลบ Feature ที่หน้าตาเหมือนกัน)
      ↓
Mutual Information
      ↓
LightGBM Importance
      ↓
SHAP Ranking
      ↓
Final 30-50 Features 
```

> **เป้าหมายสูงสุด:** โมเดลสุดท้ายใช้เพียง 30-50 ฟีเจอร์ที่มีคุณภาพสูงที่สุด เพราะจะเทรนเร็วกว่า ตีความด้วย XAI ง่ายกว่า และแปลงเป็น ONNX ไปใช้งานบน MT5 ได้มีเสถียรภาพมากกว่าครับ