---
name: quant-risk-sizing-drift-engine
description: "ระบบ Position Sizing, Risk Engine และ Data Drift Monitoring ซึ่งเป็นหัวใจสำคัญของการทำกำไรใน Quant Trading"
---

# Quant Position Sizing, Risk Engine & Data Drift

หลายคนพยายามจูน AI ให้ทำนายแม่นขึ้นจาก 55% เป็น 60% ซึ่งกำไรอาจเพิ่มเพียงเล็กน้อย แต่การมี **Position Sizing** และ **Risk Engine** ที่ดี สามารถเพิ่มผลตอบแทนและลด Drawdown ได้อย่างมหาศาล สกิลนี้อธิบาย 3 แกนหลักที่แยก "AI กากๆ" ออกจาก "Quant Trading Platform ระดับสถาบัน"

---

## 1. Position Sizing (การคำนวณขนาดไม้)
คำถามที่ต้องตอบคือ **"ควรเปิดกี่ Lot?"** (ไม่ใช่แค่ Buy หรือ Sell)

### แนวทางที่ 1: Fixed Risk (% Capital) - *มาตรฐานที่สุด*
เสี่ยงเป็นเปอร์เซ็นต์ของทุนเสมอ
- สมมุติทุน 100,000 บาท, Risk 1% = เสี่ยงได้ 1,000 บาทต่อไม้
- **สูตร:** `Lot Size = Risk Amount / (SL × Pip Value)`

### แนวทางที่ 2: Volatility Adjusted - *นิยมใน Quant*
ปรับ Lot ตามความผันผวนของตลาด (ATR)
- ตลาดนิ่ง (ATR ต่ำ) -> เปิด Lot ใหญ่ได้
- ตลาดผันผวน (ATR สูง) -> ลด Lot ลง
- **สูตร:** `Position Size ∝ 1 / ATR`

### แนวทางที่ 3: Confidence Based (ML Specific)
ให้ AI กำหนดขนาดตามความมั่นใจ (Probability)
- Model มั่นใจ 50-60% = 0.1 Lot
- Model มั่นใจ 90%+ = 0.5 Lot

### แนวทางที่ 4: Kelly Criterion
- **สูตร:** `K = W - (1-W)/R` (W=Win Rate, R=Reward Risk Ratio)
- ของจริงนิยมใช้ `Half Kelly` หรือ `Quarter Kelly` เพื่อลด Drawdown

### 🔥 สถาปัตยกรรมที่แนะนำ (The Hybrid Approach)
`1% Risk Rule` + `ATR Adjustment` + `Confidence Adjustment`
*ตัวอย่าง:* Base Size (0.5 Lot) -> เอาไปหาร Volatility Ratio -> เอาไปคูณ Confidence Score = **Final Lot**

---

## 2. Risk Engine (ด่านตรวจความเสี่ยง)
**AI ไม่มีสิทธิ์ส่งคำสั่งซื้อขายเข้า Broker โดยตรงเด็ดขาด** 
`Prediction` → `Risk Engine` → `Execution Engine` → `Broker`

### กฎการคัดกรองคำสั่ง (The 7 Rules)
- **Rule 1: Daily Loss Limit** (เช่น ติดลบ 3% ของทุน = STOP TRADING ทันที)
- **Rule 2: Max Drawdown Limit** (เช่น พอร์ตดรอปจากจุดสูงสุด 10% = หยุดระบบ)
- **Rule 3: Exposure Limit** (ป้องกันการถือคู่เงินที่มี Correlation เดียวกันมากไป เช่น ห้ามถือ USD เกิน 15% ของพอร์ต)
- **Rule 4: Spread Filter** (ถ้าระยะ Spread ถ่างเกิน Average Spread เช่นจาก 10 เป็น 35 = งดเทรด)
- **Rule 5: Slippage Filter** (ถ้าราคาคลาดเคลื่อนเกินที่รับได้ = ปฏิเสธ Order)
- **Rule 6: News Protection** (ก่อนข่าวแดง NFP, CPI 30-60 นาที = NO TRADE)
- **Rule 7: Consecutive Loss** (เช่น แพ้ติดกัน 7 ไม้ = หยุดเข้าสู่ Cooling Period)

---

## 3. Data Drift Monitoring (ตรวจจับความเสื่อมสภาพของโมเดล)
นี่คือสาเหตุที่ทำไมโมเดลที่เคยกำไรตอน Train ถึงขาดทุนยับตอน Deploy (เพราะตลาดเปลี่ยน)

### ประเภทของ Drift
1. **Data Drift:** ค่าเฉลี่ย/Distribution เปลี่ยน (เช่น Train RSI Mean=52, Deploy RSI Mean=68)
2. **Feature Drift:** ค่าตัวแปรเปลี่ยน (เช่น ATR พุ่งสูงปรี๊ดจากอดีต แสดงว่า High Volatility)
3. **Concept Drift (อันตรายสุด):** ความสัมพันธ์เปลี่ยน แม้ข้อมูลหน้าตาเหมือนเดิม (อดีต RSI>70 ราคาลง, ปัจจุบัน RSI>70 ราคากลับขึ้นต่อ) โมเดลพังทันที

### การวัดผลด้วย Population Stability Index (PSI)
- `PSI < 0.1` = Normal (ปกติ)
- `0.1 - 0.25` = Monitor (ต้องจับตาดู)
- **`> 0.25` = Drift (ต้อง Trigger การ Retrain โมเดลใหม่ทันที)**

---

## 🚀 The Real Production Workflow

โครงสร้างการทำงานใน Production ต้องผ่านทุกด่านนี้ตามลำดับ:

```text
Market Data
     ↓
Feature Engine
     ↓
Data Drift Check (เช็ค PSI ของ Features ก้อนล่าสุด)
     ↓
Model Prediction (LightGBM/ONNX)
     ↓
Position Sizing (คำนวณ Lot จาก Confidence + ATR + 1% Risk)
     ↓
Risk Engine (เช็ค Spread, ข่าว, Drawdown ก่อนอนุญาตให้ส่ง)
     ↓
Execution (ยิง Order เข้า Broker)
     ↓
Monitoring (PF, Sharpe)
     ↓
Retraining (หาก Drift เกิน 0.25 หรือ Sharpe ตก)
```

> **สรุปแบบ Quant Professional:** 
> - **Position Sizing** ตอบว่า "ควรเปิดกี่ Lot" *(ดูสูตร Sizing ที่เหมาะสมแยกตาม Asset Class ได้ที่สกิล `quant-concept-drift-position-sizing`)*
> - **Risk Engine** ตอบว่า "ออเดอร์นี้อนุญาตให้ส่งหรือไม่"
> - **Data Drift** ตอบว่า "ตลาดวันนี้ยังหน้าตาเหมือนตอนที่เราเทรนโมเดลมาหรือไม่" *(ดูวิธีแยก Concept Drift ออกจาก Data Drift ได้ที่สกิล `quant-concept-drift-position-sizing`)*

การทำทั้ง 3 สิ่งนี้ให้สมบูรณ์คือจุดชี้ขาดที่จะเปลี่ยนจาก AI Trading ธรรมดา ให้กลายเป็นกองทุน Quant ระดับสถาบัน