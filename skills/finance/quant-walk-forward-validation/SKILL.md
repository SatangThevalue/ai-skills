---
name: quant-walk-forward-validation
description: "คู่มือทำ Walk Forward Validation แบบ Rolling Window และการวิเคราะห์ความเสถียร (Stability) เชิง Quant"
---

# Quant Walk Forward Validation & Stability Analysis

ในโลกของการทำ Machine Learning ทั่วไป การใช้ `train_test_split()` อาจเป็นเรื่องปกติ แต่สำหรับโลกของ Quant Trading ถือเป็น **ข้อห้ามเด็ดขาด** เพราะตลาดการเงินมี "Time Dependency" (ความสัมพันธ์ของเวลา) การสุ่มแบ่งข้อมูลอดีตกับอนาคตปนกันจะนำไปสู่ Data Leakage และ Overfitting ที่รุนแรง

## Strategy Validation Metrics & Limits
- **Grade A Benchmarks**: Sharpe Ratio > 1.5 and Low Max Drawdown (<10%). High Net Return is meaningless if Max DD is severe (e.g. BTC returns +40% but hits -77% DD).
- **Timeframe Traps**: High Frequency (like 15m) often succumb to transaction costs (Spread/Slippage) and noise. Mitigate using Meta-Labeling filters to reject unprofitable signals.

## Advanced Optimization (Meta-Labeling & Regimes)
When standard Price Action fails (like GOLD, BTC, or Whipsaw pairs):
1. **Meta-Labeling**: Train a base model for direction, and a Meta Model to predict if the base signal will survive the spread. Reject if Meta confidence is low.
2. **Hidden Markov Models (HMM)**: Predict the Market Regime (Sideways, Bull, Bear) instead of direction. Buy and hold only during the "Quiet" regime to avoid chop.
3. **Macro/Crypto Microstructure**: Integrate `DXY` and `US10Y Yield Spread` for Fiat/Gold. For BTC, use `Inverse Volatility Sizing` (shrink lot size when ATR spikes) and `Funding Rate / Liquidation` API data.

---

## 1. วิธีทำ Walk Forward แบบ Expanding vs Rolling Window

ตลาดการเงินไม่เหมือนรูปภาพหมาแมว เพราะข้อมูลมี `Time Dependency` การสุ่ม `[2020, 2022, 2024]` มาเทรนเพื่อไปเทสต์ปี `[2021, 2023]` จึงเป็นเรื่อง **ผิดหลักอย่างรุนแรง** เพราะเอาอนาคตมาทายอดีต

วิธีจำลองสถานการณ์จริงมี 2 แบบ:

### แบบที่ 1: Expanding Window
เพิ่มข้อมูลให้โมเดลเรียนรู้สะสมไปเรื่อยๆ:
- **Window 1:** `Train 2020` ➔ `Test 2021`
- **Window 2:** `Train 2020-2021` ➔ `Test 2022`
- **Window 3:** `Train 2020-2022` ➔ `Test 2023`
*ข้อดี:* โมเดลมีข้อมูลเรียนรู้มากขึ้นเรื่อยๆ

### แบบที่ 2: Rolling Window (นิยมในตลาดการเงินมากกว่า)
กำหนดขนาดข้อมูลอดีตคงที่ แล้วเลื่อนหน้าต่างไปเรื่อยๆ:
- **Window 1:** `Train 2020-2022` (3 ปี) ➔ `Test 2023` (1 ปี)
- **Window 2:** `Train 2021-2023` (3 ปี) ➔ `Test 2024` (1 ปี)
- **Window 3:** `Train 2022-2024` (3 ปี) ➔ `Test 2025` (1 ปี)
*ข้อดี:* สะท้อนสภาวะตลาด (Market Regime) ปัจจุบันได้ดีกว่าแบบสะสม เพราะข้อมูลที่เก่าเกินไป (เช่น พฤติกรรมเมื่อ 5 ปีที่แล้ว) จะถูกลบออกไปจากการตัดสินใจ

---

## 2. สิ่งที่ต้องวัดผลในทุกๆ Window

อย่าดูแค่ Classification Accuracy เด็ดขาด สิ่งที่ต้องเก็บทุกครั้งที่จบ 1 Window (Core Trading Metrics) คือ:
- `Profit Factor`
- `Sharpe Ratio`
- `Sortino Ratio`
- `Calmar Ratio`
- `Max Drawdown`
- `Win Rate`
- `Trade Count` (จำนวนออเดอร์)
- `Expected Value`

---

## 3. Stability Analysis (การวิเคราะห์ความเสถียร)

นี่คือจุดที่แยกระหว่าง "มือสมัครเล่น" กับ "Quant มืออาชีพ"
หลังจากรันจบ 3-4 Windows สิ่งที่ Quant ดูจริง ๆ ไม่ใช่แค่ **Mean Profit Factor** (ค่าเฉลี่ย) แต่ต้องดู **Std Profit Factor** (ส่วนเบี่ยงเบนมาตรฐาน หรือความแกว่ง) ควบคู่ไปด้วยเสมอ

**ตัวอย่างที่ดี:** `WF1=1.8`, `WF2=1.7`, `WF3=1.9`, `WF4=1.8` (เสถียรมาก คาดเดาความเสี่ยงได้)
**ตัวอย่างที่แย่:** `WF1=3.5`, `WF2=0.7`, `WF3=2.8`, `WF4=0.8` (แม้ค่าเฉลี่ยอาจเท่าด้านบน แต่กำไรแกว่งรุนแรงมาก)

### Quant Grade Evaluation (เกณฑ์ประเมินที่ใช้งานจริง)
- **🌟 Grade A:** `PF > 1.7`, `Sharpe > 1.5`, `DD < 15%`, `PF Std < 0.2` (เสถียรมาก เอาขึ้นรันเงินจริงได้)
- **✅ Grade B:** `PF > 1.4`, `Sharpe > 1.2`, `DD < 20%` (พอใช้งานได้ แต่อาจมีช่วง Drawdown ให้กังวล)
- **❌ Reject:** `PF < 1.2`, `Sharpe < 1` (โยนทิ้งทันที)

> 🎯 **เป้าหมายสูงสุด:** ระบบที่ดีไม่ใช่ระบบที่ทำกำไรสูงสุด แต่เป็นระบบที่ "รอดทุก Regime, ควบคุม Drawdown ได้, และผ่าน Walk Forward ได้สม่ำเสมอ"

---

## 4. The Gold Standard Workflow สำหรับการขึ้นระบบ

```text
Market Data
     ↓
Feature Engineering
     ↓
Feature Selection
     ↓
Walk Forward Validation (ประเมินความเสถียร Mean/Std)
     ↓
Trading Metrics
     ↓
MLflow (บันทึก Artifacts)
     ↓
ONNX Export
     ↓
Paper Trading
     ↓
Production
     ↓
Concept Drift Monitoring (Evidently / NannyML)
     ↓
Retraining
```

---

## 🚀 6 Next Actionable Steps (ลำดับถัดไปที่ควรลงมือทำ)

หากต้องการผลักดันโปรเจกต์นี้ให้เป็น Quant Trading Platform แบบสมบูรณ์ ขอแนะนำให้ลงมือเขียนโค้ดและสร้างระบบตามลำดับนี้:

1. **Walk Forward Engine:** เขียนสคริปต์ทำ TimeSeriesSplit (Rolling) + ประเมินค่า Mean/Std ของ Metrics
2. **Risk Engine:** เขียนด่านสกัดออเดอร์ก่อนยิงเข้า MT5 (คุม Drawdown/Exposure/News)
3. **Position Sizing Engine:** เขียนระบบปรับขนาดออเดอร์ตาม ATR และ ความมั่นใจของโมเดล
4. **Execution Engine:** ควบคุมการเข้าออกออเดอร์ให้เฉียบคม
5. **Concept Drift Monitoring:** วางระบบตรวจจับ Data Drift (เช็คค่า PSI และ Performance Drop)
6. **Portfolio Engine:** วางโครงสร้างบริหารการเทรดหลายสินทรัพย์แบบภาพรวม

> หากคุณสร้าง Engine เหล่านี้ครบ ระบบของคุณจะพร้อมและแข็งแกร่งกว่า EA ทั่วไปตามท้องตลาดอย่างแน่นอน และคุ้มค่าที่จะทำ **ก่อน** จะไปขยายโมเดล AI ให้ซับซ้อนขึ้นอย่างพวก Transformer หรือ Deep Learning ครับ