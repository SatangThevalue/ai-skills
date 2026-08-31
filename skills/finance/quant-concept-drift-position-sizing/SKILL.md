---
name: quant-concept-drift-position-sizing
description: "เจาะลึกความสัมพันธ์ระดับสถาบัน: Market Regime, Concept Drift vs Data Drift (PSI), และ Position Sizing"
---

# Quant Research Core: Drift & Position Sizing

เมื่อก้าวพ้นจากการเป็น "คนสร้างโมเดล" ไปสู่ "ผู้สร้างระบบบริหารความเสี่ยง" การเข้าใจความสัมพันธ์ระหว่าง **Market Regime → Concept Drift → Position Sizing** ถือเป็นหัวใจของ Quant Trading

---

## 1. การใช้ PSI (Population Stability Index) อย่างถูกต้อง

**PSI ใช้ตรวจ Data Drift:** ว่า "Distribution" (การกระจายตัวของข้อมูล) เปลี่ยนไปจากตอน Train หรือไม่

**✅ PSI ใช้ได้ดีกับ:**
1. **Numerical Features:** `RSI, ATR, ADX, Spread, Volume Ratio` (เช่น ตอน Train RSI วิ่งแถว 52 ตอนเทรดจริงวิ่งแถว 70 -> เกิด Data Drift)
2. **Categorical Features:** `Market Regime` (เช่น สัดส่วนของ Trend/Range เปลี่ยนไป)
3. **Time Features:** `Session` (เช่น สัดส่วนการเทรดใน London Session ลดลง)

**❌ PSI ไม่เหมาะกับ:**
- **Target Label (Buy/Sell):** ใช้ได้แต่ไม่ใช่เป้าหมายหลัก
- **การหาความสัมพันธ์ระหว่าง X กับ Y:** PSI ดูแค่ข้อมูลหน้าตาเปลี่ยนไหม แต่ไม่ได้ดูว่า "ตรรกะของตลาด" เปลี่ยนไหม (นั่นคือหน้าที่ของ Concept Drift)

**Dashboard เกณฑ์การเฝ้าระวัง:**
- `< 0.1`: ปกติ (🟢 Green)
- `0.1 - 0.25`: จับตาดู (🟡 Yellow)
- `> 0.25`: ข้อมูลเปลี่ยนรุนแรง (🔴 Red -> Trigger Retrain)

---

## 2. Concept Drift (หายนะเงียบของโมเดล)

นี่คือประเภท Drift ที่อันตรายที่สุด เพราะ "ข้อมูลหน้าตาเหมือนเดิม (PSI ต่ำ) แต่ตรรกะตลาดเปลี่ยน"
- **อดีต:** `RSI > 70` ➔ `ราคาลง` (Overbought = Sell)
- **ปัจจุบัน (ตลาดกระทิงดุ):** `RSI > 70` ➔ `ราคาขึ้นต่อ`
โมเดลเดิมจะสั่ง Sell และพอร์ตจะพังทันที ทั้งที่ RSI Distribution ไม่ได้เปลี่ยนไปเลย

**ประเภทของ Concept Drift:**
1. **Sudden Drift:** เปลี่ยนชั่วข้ามคืน (COVID, Flash Crash, สงคราม)
2. **Gradual Drift:** ค่อยๆ เปลี่ยน (เช่น Volatility ของตลาด Forex ค่อยๆ ลดลง)
3. **Seasonal Drift:** ตามฤดูกาล (สิงหาคม/ธันวาคม ตลาดจะเงียบ)
4. **Recurring Drift:** เกิดซ้ำๆ แบบคาดเดาได้ (ช่วงก่อนข่าว NFP, FOMC)

**วิธีตรวจจับ Concept Drift:**
1. **Monitor Performance:** (ง่ายสุด) วัด Profit Factor หรือ Sharpe ถ้าตอนเทรน PF=1.8 เทรดจริง PF=0.9 = Drift แน่นอน
2. **Prediction Drift:** สัดส่วนการตอบของโมเดลเปลี่ยนกะทันหัน (อดีตทำนาย Buy 50% Sell 50%, ปัจจุบันทำนาย Buy 95%)
3. **Rolling Retraining Evaluation:** เทรนโมเดลใหม่ (Model B) มาเทียบกับตัวเก่า (Model A) บนข้อมูลปัจจุบัน ถ้าตัวใหม่ชนะขาด = เกิด Concept Drift แล้ว

---

## 3. Position Sizing เชิงลึก (เทคนิคแยกตามสินทรัพย์)

นี่คือด่านที่จะทำให้ AI ของคุณรอดหรือร่วงในตลาดจริง

1. **Fixed Lot (ทุกไม้ 0.1):** *เหมาะกับ Backtest / Demo เท่านั้น* ห้ามใช้ Production เพราะไม่สนความเสี่ยง
2. **Fixed Risk % (เช่น เสี่ยง 1% ของทุน):** มาตรฐานยอดนิยมที่สุด (เช่น ทุนแสน เสี่ยง 1% = เสียได้ไม้ละ 1,000)
3. **Volatility Sizing (อิงค่า ATR):** *สาย Quant ตัวจริง* ปรับ Lot ผกผันกับความผันผวน (ตลาดนิ่ง = Lot ใหญ่, ตลาดเหวี่ยง = Lot เล็ก)
4. **Confidence-Based (อิงความมั่นใจ AI):** ใช้น้ำหนักความน่าจะเป็นจาก LightGBM (ทำนาย Buy ด้วยความมั่นใจ 55% = 0.1 Lot, แต่ถ้ามั่นใจ 90% = 0.5 Lot)
5. **Kelly Criterion:** *เหมาะกับ Long-Term Portfolio* แต่อย่าใช้เต็ม ให้ใช้ `Half Kelly` หรือ `Quarter Kelly` เพื่อควบคุม Drawdown ให้ต่ำ

**สถาปัตยกรรม Position Sizing แบบสถาบัน (Asset-Specific):**
- **Forex / Gold:** Fixed Risk (0.5 - 1%) + ATR Sizing
- **Crypto:** Fixed Risk (0.25 - 0.5%) + ATR Sizing + Volatility Cap
- **Stocks:** Risk Parity + Volatility Sizing
- **Multi-Asset Portfolio:** Risk Parity + Volatility Targeting + Correlation Adjustment

---

## 🚀 The Ultimate Hybrid Sizing Formula (สำหรับ AI Trading)

สูตรที่สมดุลที่สุดในการเชื่อมโยงโมเดล LightGBM/ONNX สู่ MT5 Production:

```text
Base Risk (เช่น 1%)
       ↓
Volatility Adjustment (ปรับตาม ATR Ratio)
       ↓
AI Confidence Adjustment (ปรับตาม Probability Score จาก LightGBM)
       ↓
(ได้ Position Size เบื้องต้น)
       ↓
Risk Engine Approval (คัดกรอง Spread, News, Drawdown, Exposure)
       ↓
Execute Order
```

> **ตัวอย่าง:** ทุน 100,000 | Risk 1% | ATR Ratio 1.5 | ML Confidence 85% 
> *ผลลัพธ์อาจคำนวณได้เป็น 0.32 Lot ที่ยืดหยุ่น ปลอดภัย และรีดกำไรได้สูงสุดตามจังหวะที่ AI มั่นใจ*