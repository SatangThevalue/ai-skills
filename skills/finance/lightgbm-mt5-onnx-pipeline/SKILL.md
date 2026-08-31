---
schema: hermes/skill@v1
name: lightgbm-mt5-onnx-pipeline
description: Architecture for LightGBM-based MT5 algorithmic trading bots using Walk-Forward testing and ONNX deployment.
category: finance
tags: [trading, mt5, mql5, onnx, lightgbm, machine-learning, quantitative-finance]
---

# LightGBM to MT5 ONNX Trading Pipeline

สถาปัตยกรรม "ที่คุ้มค่าที่สุด" สำหรับ Trader / Data Scientist ในปี 2026 ที่ให้ความสมดุลระหว่าง ความแม่นยำ, ความเร็ว, ความง่ายในการ Deploy, ความสามารถในการ Backtest, และความเสถียร โดยใช้ LightGBM ร่วมกับ ONNX ใน MT5

## Trigger
ใช้เมื่อผู้ใช้ต้องการสร้างโมเดล Machine Learning เพื่อการเทรดบน MT5, ทำ Feature Engineering สำหรับข้อมูล Time-Series การเงิน, หรือสร้างระบบ Walk-Forward Testing สำหรับ Algorithmic Trading

## Phase 1: Feature Engineering (70% ของงานทั้งหมด)
เนื่องจากตลาดการเงินมี Noise สูง การสร้างฟีเจอร์ที่ดีจึงสำคัญกว่าตัวโมเดล แนะนำให้เริ่มต้นที่ 50-100 Features ตาม Layers เหล่านี้:

1. **Layer 1: Raw Features** - ข้อมูลพื้นฐานจาก MT5 (Open, High, Low, Close, Tick Volume, Spread)
2. **Layer 2: Return Features** - เปลี่ยนจากราคาเป็นผลตอบแทนเพื่อให้ข้อมูลมีความ Stationary (เช่น `return_1 = Close(t)/Close(t-1)-1`, `return_5`, `return_20`)
3. **Layer 3: Momentum Features** - วัดแรงของตลาด (RSI, Stochastic, CCI, Momentum) ใช้หลาย Period พร้อมกัน เช่น RSI(14), RSI(28), RSI(50)
4. **Layer 4: Trend Features** - ใช้ระยะห่างจากเส้นค่าเฉลี่ยแทนการใช้ค่าตรงๆ (เช่น `close_above_ema50`, `ema20_ema50_gap`)
5. **Layer 5: Volatility Features** - สำคัญมากเพื่อจับการเปลี่ยน Regime ของตลาด (ATR, Rolling Std, Bollinger Width, `current_atr / atr_100_avg`)
6. **Layer 6: Market Structure** - โครงสร้างตลาดที่ Quant ใช้ (Distance to Support/Resistance, Swing High, Swing Low)
7. **Layer 7: Multi-Timeframe Features** - ใช้ M15, H1, H4, D1 พร้อมกันในแถวเดียว (เช่น RSI_H1, EMA50_H4)
8. **Layer 8: Session Features** - จับพฤติกรรมเวลาเปิดปิดของแต่ละ Session (is_london, is_newyork, is_asia, hour)

### เทคนิคเพิ่มประสิทธิภาพ Feature
*   **Lag Features:** สร้างข้อมูลอดีตหลายช่วง (close_lag1 ถึง close_lag20)
*   **Rolling Features:** ค่าสถิติเคลื่อนที่ (rolling_mean_10, rolling_std_20)
*   **Feature Interaction:** จับคู่ฟีเจอร์ เช่น `RSI * ATR` หรือ `EMA_GAP * ATR`

## Phase 2: LightGBM Model & Label Design
LightGBM เหมาะกับ Trading เพราะรวดเร็ว, จัดการ Nonlinear ได้ดี, ทน Noise, รองรับ Feature เยอะ, และสามารถ Export เป็น ONNX ได้ง่าย

### Label Design (สำคัญกว่าโมเดล)
*   **ห้ามใช้:** การเปรียบเทียบแค่ราคาปิดอนาคต > ราคาปิดปัจจุบัน (`future_close > current_close`) เพราะไม่สมจริงในการเทรด
*   **แนะนำ (Triple Barrier Method):** กำหนด Take Profit (TP = 30 Pips), Stop Loss (SL = 20 Pips), และ Time Limit (12 Hours) และ Label ผลลัพธ์เป็น `BUY`, `SELL`, `HOLD` จะตรงกับสภาพแวดล้อมการเทรดจริงมากกว่า

### Hyperparameter Tuning (ใช้ Optuna)
*   **แนะนำค่าเริ่มต้น:** `learning_rate=0.03`, `num_leaves=64`, `max_depth=6`
*   หลัง Train เสร็จ ให้ตรวจสอบ `model.feature_importances_` และตัดฟีเจอร์ที่ไม่สำคัญออกทุกเดือน

## Phase 3: Walk-Forward Testing
เป็นกระบวนการแบ่งแยกระหว่าง "Research" กับ "Gambling" ป้องกัน Data Leakage อย่างเด็ดขาด

*   **ห้ามทำ:** ใช้ `train_test_split()` แบบสุ่ม เพราะข้อมูลอนาคตจะรั่วไหลกลับไปสอนอดีต
*   **วิธีการที่ถูกต้อง (Walk Forward):**
    *   *Round 1:* Train `2020-2022` -> Test `2023`
    *   *Round 2:* Train `2020-2023` -> Test `2024`
    *   *Round 3:* Train `2020-2024` -> Test `2025`

## Phase 4: ONNX Export & MT5 Deployment
1. Export LightGBM เป็นรูปแบบ ONNX
2. โหลดไฟล์ `.onnx` เข้าไปยัง MQL5 ผ่านฟังก์ชัน `OnnxCreate()` และทำการ Inference สัญญาณซื้อขายโดยตรงในระบบ MT5

## Pitfalls & ข้อควรระวัง
*   **Data Leakage:** ระวังการใช้ Rolling Window หรือ Feature ที่แอบมองอนาคตโดยไม่รู้ตัว (เช่น การ Normalize ด้วยข้อมูลทั้งชุดแทนที่จะเป็น Rolling basis)
*   **Overfitting:** ตลาดการเงินมี Signal-to-Noise Ratio ต่ำมาก หากโมเดลแม่นยำเกินไปใน Test data มักจะพังตอนเทรดจริง ให้เน้นโมเดลที่เรียบง่ายและเสถียร (Robust) ผ่าน Walk-Forward Testing อย่างเข้มงวด
