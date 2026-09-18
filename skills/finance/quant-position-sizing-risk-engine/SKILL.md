---
name: quant-position-sizing-risk-engine
description: มาตรฐานการออกแบบ Position Sizing (5 ระดับ) และ Risk Engine (6 Layers) สำหรับ AI/Quant Trading รวมถึงหลักการ Walk Forward Validation
tags: [quant, risk-management, position-sizing, ai-trading, walk-forward, finance]
version: 1.0.0
---

# Quant Trading Core Philosophy

หัวใจสำคัญของการเทรดเชิงปริมาณ (Quant Trading) ไม่ใช่แค่ความแม่นยำของโมเดล แต่คือการบริหารความเสี่ยง โครงสร้างความสำคัญของระบบคือ:

- **Prediction Model**: 20%
- **Position Sizing**: 30%
- **Risk Engine**: 30%
- **Walk Forward Validation**: 20%

*ระบบที่ AI ทายแม่นยำแค่ไหน หากไร้ Position Sizing และ Risk Engine ที่ดี ท้ายที่สุดก็จะพ่ายแพ้ต่อความผันผวนของตลาด*

---

# 1. Position Sizing (ศาสตร์การกำหนดขนาดการลงทุน)

Position Sizing ไม่ได้ตอบคำถามว่า "BUY หรือ SELL" แต่ตอบว่า **"ต้องเปิดกี่ Lot/Size?"** 
เป้าหมายที่แท้จริงคือ **"รอดให้อยู่ในตลาดได้นานที่สุด"** ไม่ใช่ "กำไรเยอะที่สุด"

## ระดับของ Position Sizing

1. **ระดับที่ 1: Fixed Lot**
   - *วิธี:* ทุกไม้เปิดเท่ากันหมด เช่น 0.1 Lot
   - *ข้อดี:* ง่าย ทดสอบง่าย
   - *ข้อเสีย:* ไม่สนความเสี่ยง, Volatility และขนาดของพอร์ต
2. **ระดับที่ 2: Fixed Risk Percent (Recommended Standard)**
   - *วิธี:* ยอมเสียสูงสุดเป็น % ของพอร์ตต่อไม้ เช่น ทุน 100,000 Risk 1% = ยอมเสียไม้ละ 1,000
   - *ตัวอย่าง:* ถ้า Stop Loss (SL) = 30 pip (1 pip = 50 บาท) -> `Lot = 1,000 / (30 * 50) = 0.67 Lot`
   - *หลักการ:* SL กว้าง = Lot เล็ก / SL แคบ = Lot ใหญ่
3. **ระดับที่ 3: ATR Based Position Sizing (Quant Fund นิยม)**
   - *วิธี:* ปรับขนาดตามความผันผวน (Volatility) 
   - *ตัวอย่าง:* วันที่ตลาดนิ่ง (ATR 10 pip) เปิด 0.50 Lot | วันที่ตลาดผันผวนหนัก (ATR 80 pip) ลดเหลือ 0.06 Lot
   - *ข้อดี:* คงระดับความเสี่ยง (Risk) ให้เท่าเดิมเสมอแม้พฤติกรรมตลาดเปลี่ยน
4. **ระดับที่ 4: Confidence Sizing (AI Probability)**
   - *วิธี:* นำ Output (Probability) จาก AI มาเป็นตัวคูณ Lot ปกติ
   - *ตัวอย่าง:* Prob 50-60% = 0.50x | Prob 70-80% = 1.00x | Prob 90%+ = 1.50x
5. **ระดับที่ 5: Portfolio Aware Sizing (ระดับ Hedge Fund)**
   - *วิธี:* คำนวณความเสี่ยงภาพรวม (Correlation) 
   - *ตัวอย่าง:* หากเปิด EURUSD Buy และ GBPUSD Buy อยู่ ระบบจะลด Size ของ AUDUSD Buy อัตโนมัติเพื่อลดความเสี่ยงที่สัมพันธ์กัน

### สูตร Ultimate Position Sizing:
```python
Final_Position = (Base_Risk_Position 
                  * Confidence_Multiplier 
                  * Regime_Multiplier 
                  * Portfolio_Multiplier) / ATR_Ratio
```
*ตัวอย่าง:* Base Lot (0.50) * Conf (1.2) * Regime (1.0) * Port (0.8) / ATR (1.5) = 0.32 Lot

---

# 2. Risk Engine ("ตำรวจ" ประจำระบบ)

แม้ AI จะออก Signal "BUY EURUSD" แต่นั่นคือการ "เสนอแนะ" ส่วน "คนอนุมัติ" คือ Risk Engine 

**Architecture Flow:**
`Prediction -> Position Sizing -> Risk Engine -> Execution`

## 6 Layers of Risk Engine

1. **Layer 1: Trade Risk (ความเสี่ยงรายออเดอร์)**
   - Maximum Risk Per Trade: เช่น ห้ามเกิน 1% ของพอร์ต ถ้าเกิน = **Reject**
   - Mandatory Stop Loss: ทุกออเดอร์ **"ต้องมี"** SL และ TP ห้าม No SL เด็ดขาด
2. **Layer 2: Portfolio Risk (ความเสี่ยงรวมพอร์ต)**
   - คำนวณ Net Exposure ของกลุ่มคู่เงินที่เกี่ยวข้องกัน (เช่น เปิด Buy ตระกูล USD พร้อมกันหลายคู่ ถือเป็นการเปิด Long USD Exposure กระจุกตัว)
3. **Layer 3: Drawdown Control (การควบคุมความเสียหายสูงสุด)**
   - Maximum Drawdown: เช่น ตั้งไว้ 10% หากถึงจุดนี้ระบบจะทำ Hard Stop ตัดการเทรดทันที
4. **Layer 4: Daily Risk (ความเสี่ยงรายวัน)**
   - Daily Loss Limit: เช่น ขาดทุนสะสม 3% ใน 1 วัน -> **No Trade ทั้งวัน**
5. **Layer 5: Market Risk (สภาพแวดล้อมตลาด)**
   - Spread Filter: เช่น ถ้า Spread เกิน 30 points -> **Reject**
   - Volatility Filter: เช็คค่า ATR Ratio ว่าสูงผิดปกติเกินรับมือหรือไม่
   - News Filter: บล็อคการเข้าออเดอร์ล่วงหน้า 60 นาทีก่อนข่าวสำคัญ (NFP, CPI, FOMC)
6. **Layer 6: Strategy Risk (ความเสี่ยงเชิงกลยุทธ์)**
   - Market Regime Filter: หากกลยุทธ์เป็น Trend Following แต่ Regime ปัจจุบันคือ "Range (ไซด์เวย์)" -> **ไม่อนุญาต Entry**

### Risk Score Model
สร้าง Score ประเมินก่อนเข้าออเดอร์ (รวมปัจจัย Spread, Drawdown, Exposure, Volatility, Correlation)
- **0 - 30** : Safe (เปิดออเดอร์ปกติ)
- **30 - 60** : Normal (เปิดออเดอร์พร้อมลด Size หรือเฝ้าระวัง)
- **60 - 100** : No Trade (บล็อคการยิงออเดอร์)

---

# 3. Walk Forward Validation

นี่คือสิ่งที่ทำให้สาย Quant Research แตกต่างจากการทำ Backtest ทั่วไปโดยสิ้นเชิง

**สิ่งที่ห้ามทำเด็ดขาด (Anti-Pattern):**
- การใช้ฟังก์ชันสุ่มชุดข้อมูล เช่น `train_test_split()` (Random Split) มาใช้กับข้อมูล Time Series
- เช่น การสุ่มข้อมูลปี 2020-2024 รวมกันแล้วแบ่ง Train/Test 
- *เหตุผล:* จะทำให้เกิด **Look-ahead Bias** (การนำข้อมูลในอนาคตกลับมาสอนอดีต) 

**วิธีที่ถูกต้อง:** 
ต้องเรียงลำดับเวลา (Chronological) เสมอ โดยแบ่งเป็นช่วงๆ และขยับไปข้างหน้า (Rolling Window / Expanding Window) 
*ตัวอย่าง:* Train 2020-2021 -> Test 2022 | ขยับไป Train 2021-2022 -> Test 2023