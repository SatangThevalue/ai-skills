---
name: quant-feature-engineering
description: "สถาปัตยกรรมการสร้าง Feature Engineering เชิงลึกสำหรับ AI Trading / Quant (แปลง Raw Data เป็น Feature Intelligence)"
---

# Feature Engineering Architecture สำหรับ Quant Trading

> **"Feature ต้องอธิบายพฤติกรรมตลาด ไม่ใช่แค่คำนวณ Indicator"** 
> *– หลักการจากทีม Quant Hedge Fund*

การส่งข้อมูลเข้าโมเดล (LightGBM/XGBoost) อย่างดิบ ๆ เช่น ราคาปิด หรือค่า RSI/MACD เพียว ๆ มักไม่เวิร์ค เพราะมันยังไม่ได้แปลงเป็น "บริบท" หรือ "พฤติกรรม" ของตลาด สกิลนี้อธิบายการแบ่ง Layer ของการสร้าง Feature อย่างเป็นระบบ ตั้งแต่ Raw Data ไปจนถึง Feature Interaction

---

## The Feature Pipeline

*(หากต้องการดูเอกสารแบบเจาะลึก 11 Stages พร้อมสูตรและตัวอย่างการตีความ กรุณาดูที่สกิล `quant-feature-design-document`)*

```text
Raw Market Data
       ↓
Layer 1: Return Features
Layer 2: Candle Features
Layer 3: Trend Features
Layer 4: Momentum Features
Layer 5: Volatility Features
Layer 6: Volume Features
Layer 7: Statistical Features
Layer 8: Market Structure Features
Layer 9: Multi Timeframe Features
Layer 10: Regime Features
Layer 11: Time Features
Layer 12: Feature Interaction
       ↓
Feature Selection (SHAP, Importance)
       ↓
LightGBM → ONNX → MT5
```

---

## Layer 0: Raw Data
เก็บ `timestamp, open, high, low, close, tick_volume, spread`
⚠️ **ข้อควรระวัง:** ห้ามใช้ ราคาโดยตรง (เช่น `close`) เป็น Input เข้าโมเดล เพราะเป็น Non-stationary data

## Layer 1: Return Features (สำคัญที่สุด)
- **Return:** `ret_1, ret_3, ret_5, ret_10, ret_20, ret_50` (สูตร: `close.pct_change(n)`)
- **Log Return:** `log_ret_1, log_ret_5, log_ret_20` (สูตร: `np.log(close / close.shift(1))`)
- **Cumulative Return:** `cumret_10, cumret_20` (บอก Momentum ระยะสั้น)

## Layer 2: Candle Features (ถอดรหัสพฤติกรรมแท่งเทียน)
เปลี่ยน Pin Bar, Doji ให้เป็นตัวเลข:
- **Body Size:** `abs(close - open)`
- **Upper / Lower Shadow:** ไส้เทียนบน / ล่าง
- **Body Ratio:** `body / (high - low)`
- **Shadow Ratio:** สัดส่วนไส้ต่อขนาดแท่ง

## Layer 3: Trend Features
- **EMA:** 20, 50, 100, 200
- **EMA Gap (สำคัญกว่าตัว EMA เอง):** `ema20_50_gap`, `ema50_200_gap` (สูตร: `(EMA20-EMA50)/EMA50`)
- **EMA Slope:** `EMA20.diff(5)`
- **Trend Score (0-100):** รวม ADX + EMA Alignment + EMA Slope

## Layer 4: Momentum Features
- **RSI หลายช่วง:** `RSI7, RSI14, RSI28, RSI50` (ไม่สน 70/30 มากนัก สนใจที่การกระจายตัว)
- **RSI Slope:** `RSI14.diff(3)`
- **RSI Distance:** `RSI14 - 50`
- **MACD & ROC (Rate of Change):** Histogram, MACD Slope, `ROC5, ROC10`

## Layer 5: Volatility Features (จุดชี้ขาดตลาด)
- **ATR & ATR Ratio (สำคัญมาก):** `ATR14 / ATR100` (>1.5 = High Vol, <0.7 = Low Vol)
- **Rolling Std:** 10, 20, 50
- **Bollinger Width:** `upper - lower` (วัดการบีบตัว/ระเบิดของราคา)
- **Volatility Expansion:** `std20 / std100`

## Layer 6: Volume Features
*Forex ใช้ Tick Volume แทน Real Volume*
- **Volume Ratio:** `volume / volume_ma20`
- **Relative Volume / Z-Score:** เปรียบเทียบความผิดปกติของ Volume ล่าสุดกับอดีต

## Layer 7: Statistical Features (Quant ใช้เยอะมาก)
- **Rolling Mean / Std:** 10, 20, 50
- **Z-Score:** `(close - ma20) / std20`
- **Skewness & Kurtosis:** วัดความเบ้และความโด่งของการแจกแจง

## Layer 8: Market Structure
- **Distance to Swing High / Low:** ระยะห่างจากจุดสูงสุด/ต่ำสุดรอบที่แล้ว
- **Breakout Distance:** `breakout_high20`, `breakout_low20`
- **Donchian Position:** `(close - low20) / (high20 - low20)`

## Layer 9: Multi Timeframe Features (สำคัญมาก)
- ดึง Feature หลักจาก TF ใหญ่มารวมกับ TF เล็ก (เช่น ถ้ารันบน M15 ต้องมีข้อมูล H1, H4, D1 ด้วย)
- ตัวอย่าง: `RSI_H1, RSI_H4`, `ADX_H1, ADX_H4`

## Layer 10: Regime Features
- **Composite Regime Score:** เอา ADX, ATR Ratio, BB Width, Volume Ratio มารวมเป็น Score เพื่อบอกสภาวะตลาดให้โมเดลรับรู้ (ดูรายละเอียดเพิ่มที่สกิล `market-regime-detection-quant`)

## Layer 11: Time Features (มักถูกมองข้าม)
- `hour`, `day_of_week`, `month`
- `session` (Asia, London, New York) เพื่อบอกสภาพคล่องของตลาด

## Layer 12: Feature Interaction (จุดที่ทำให้ LightGBM เก่งขึ้นมาก)
- **Momentum + Volatility:** `RSI14 * ATR_Ratio`
- **Trend + Volume:** `ADX14 * VolumeRatio`
- **Trend + Momentum:** `EMA_GAP * RSI14`
- **Breakout Strength:** `VolumeRatio * ATR_Ratio * ADX`

---

## 🚀 Roadmap การพัฒนา Feature Set

- **V1 (เริ่มต้น):** 60-80 Features (Returns, Candles, Trend, Momentum, Vol, Volume, Structure, Time, Interactions)
- **V2 (ทดสอบผ่าน):** 120-150 Features (เพิ่ม Multi Timeframe, Regime Features)
- **V3 (Production):** 50-80 Features (คัดตัวที่ไม่จำเป็นออกด้วย LightGBM Feature Importance, SHAP, Permutation Importance)

*(ดูตัวอย่างโค้ด Python สำหรับสร้าง Pipeline และการรัน Feature Selection ด้วย SHAP เชิงลึกได้ที่สกิล `python-quant-feature-pipeline`)*

---

## 🎯 15 Feature Priority ที่มี Impact สูงสุด (แนะนำสำหรับ V1)

หากต้องเลือกเพียง 15 Feature แรกสำหรับสร้างโมเดล LightGBM เพื่อส่งเข้า MT5 ชุดนี้ครอบคลุมทุกมิติมากที่สุด:

1. `ret_5`
2. `ret_20`
3. `RSI14`
4. `RSI28`
5. `ADX14`
6. `ATR14`
7. `ATR_RATIO`
8. `EMA20_50_GAP`
9. `EMA50_200_GAP`
10. `BB_WIDTH`
11. `VolumeRatio`
12. `ZScore20`
13. `Donchian_Position`
14. `Trend_Score`
15. `Regime_Score`

> **บทสรุป:** Core Feature Set ชุดนี้ครอบคลุมทั้ง Trend, Momentum, Volatility, Volume, Market Structure, และ Regime ถือเป็นจุดเริ่มต้นที่ดีที่สุดสำหรับการสร้างโมเดล LightGBM V1 ก่อนเข้ากระบวนการ Optuna Tuning, Walk Forward Testing และทำ ONNX Export
