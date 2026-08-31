---
name: forex-mean-reversion-indicators
description: "คู่มือการเลือกใช้อินดิเคเตอร์สำหรับระบบเทรด Mean Reversion และ Scalping"
version: 0.1.0
metadata:
  hermes:
    tags: [Forex, Mean Reversion, Indicators, Scalping, Technical Analysis]
---

# Forex Mean Reversion & Scalping Indicators

สกิลนี้รวบรวมหลักการและชุด Indicator (Indicator Stack) ที่ดีที่สุดสำหรับการสร้างระบบเทรดแบบ **Mean Reversion** (เทรดกลับเข้าหาค่าเฉลี่ย) และ **Scalping** (ปิ้งกำไรระยะสั้น) ซึ่งเป็นกลยุทธ์ที่เหมาะกับ "พอร์ตขนาดเล็กที่ต้องการรายได้รายวัน" เนื่องจากมี Win Rate สูงในตลาด Sideways

## When to Use

- "ช่วยหาข้อมูลจากอินเทอร์เน็ตเพื่อนำมาเลือกอินดิเคเตอร์ในการใช้งาน"
- "หา Indicator สำหรับ Scalping หรือ Mean Reversion"
- เมื่อต้องการสร้างบอทเทรดช่วงตลาด Sideways

## Quick Reference

- **The Golden Rule:** Mean Reversion จะทำงานได้ดีที่สุดเมื่อ **ADX < 20** (ตลาดไร้เทรนด์)
- **Primary Signal:** Bollinger Bands (ราคาหลุดขอบ) หรือ Z-Score (> +2, < -2)
- **Confirmation:** RSI (>70, <30) หรือ Stochastic Momentum Index (SMI)
- **Timeframe:** M5, M15 ถึง H1 (เหมาะที่สุดในช่วงตลาดเอเชีย)

## The Indicator Stack (ชุดเครื่องมือที่แนะนำ)

การทำ Mean Reversion ที่แม่นยำ ไม่ควรใช้อินดิเคเตอร์ตัวเดียว แต่ควรใช้ประกอบกันเป็น "Stack" เพื่อยืนยันความน่าจะเป็น:

### 1. The Environment Filter (ตัวกรองสภาพตลาด - สำคัญที่สุด)
- **ADX (Average Directional Index):** 
  - *หน้าที่:* วัดว่าตลาดมีเทรนด์หรือไม่ 
  - *การใช้งาน:* ระบบจะต้องบล็อกการเปิดออเดอร์ (Wait) หากค่า **ADX > 25** เพราะการสวนเทรนด์แรงๆ จะทำให้พอร์ตแตกได้ 
  - *จุดเข้าที่ปลอดภัย:* อนุญาตให้เข้าเทรดเฉพาะเมื่อ **ADX < 20** เท่านั้น

### 2. The Statistical Extremes (ตัวจับความผิดปกติของราคา)
เลือกใช้ตัวใดตัวหนึ่ง:
- **Bollinger Bands (20, 2):**
  - ราคาหุ้น 95% จะวิ่งอยู่ในกรอบนี้ หากแท่งเทียนทะลุขอบบน (Upper Band) หรือขอบล่าง (Lower Band) ถือว่าเป็นความผิดปกติทางสถิติ (Overextended)
- **Z-Score (ระยะห่างจากค่าเฉลี่ย):**
  - วัดว่าราคาปัจจุบันห่างจากค่าเฉลี่ยกี่ Standard Deviation
  - หาก `Z-Score > +2.0` หรือ `< -2.0` คือจุดเข้าเทรดที่ยอดเยี่ยม
- **Keltner Channels:**
  - คล้าย Bollinger Bands แต่ใช้ ATR ในการคำนวณความกว้าง ทำให้เสถียรกว่าในช่วงตลาดที่ผันผวน

### 3. The Momentum Confirmation (ตัวยืนยันโมเมนตัม)
- **RSI (Relative Strength Index):** 
  - ใช้ Period 14 หรือ Period 2 (กลยุทธ์ RSI 2 ของ Larry Connors ที่แม่นยำมาก)
  - รอให้ค่า RSI ยืนยันการ Overbought (>70) หรือ Oversold (<30)
- **SMI (Stochastic Momentum Index):** 
  - มีความสมูท (Smooth) กว่า RSI ปกติ จับจุดเปลี่ยนเทรนด์ระยะสั้นได้ดี

## Trading Setups (ตัวอย่างการเข้าเทรด)

### The Classic BB Bounce (Win rate 60-70%)
1. **Setup:** ADX < 20 (ตลาดออกข้าง)
2. **Trigger (Short):** ราคาพุ่งทะลุ Upper Bollinger Band ทะลุขึ้นไป แล้วมีแท่งเทียน Reversal (เช่น Pinbar) กลับเข้ามาปิด *ด้านใน* ของกรอบ
3. **Confirm:** RSI(14) > 70
4. **Target (TP):** เส้นกลางของ Bollinger Band (SMA 20)
5. **Stop Loss (SL):** เลยจุดสูงสุด (Swing High) ของแท่งที่ทะลุกรอบออกไป หรือใช้ `1.5 * ATR`

### The Larry Connors RSI(2) (Win rate 70-75%)
1. **Setup:** ราคาหุ้นอยู่ *เหนือ* เส้น EMA 200 วัน (ภาพใหญ่เป็นขาขึ้น)
2. **Trigger (Long):** ค่า RSI(2) ร่วงลงต่ำกว่า 10 (เกิดการเทขายระยะสั้นรุนแรง)
3. **Exit:** เมื่อ RSI(2) กลับขึ้นไปปิดเหนือ 70

## Pitfalls (ข้อควรระวังในการใช้ Mean Reversion)

- **The Asymmetry Trap (กำไรน้อยแต่ขาดทุนหนัก):** กลยุทธ์นี้มักมี Win rate สูง (70%) แต่ R:R มักจะต่ำ (1:1 หรือแย่กว่า) หากไม่มี Stop Loss ที่เด็ดขาด การแพ้ครั้งเดียวอาจลบล้างกำไรที่สะสมมาทั้งสัปดาห์
- **Whipsaw Risk (โดนลากช่วงข่าว):** การสวนเทรนด์ในช่วงประกาศข่าวเศรษฐกิจ (News Release) เป็นหายนะของ Mean Reversion ควรปิดบอทช่วงนั้น
- **Trending Markets:** หากเผลอไปใช้ Indicator ชุดนี้ตอนตลาดมีเทรนด์ (เช่น ทองคำกำลังวิ่งเป็นเทรนด์ขาขึ้นแรงๆ) ราคาจะเกาะเส้น Upper Bollinger Band ขึ้นไปเรื่อยๆ การดัก Short จะทำให้พอร์ตเสียหายหนัก (นี่คือเหตุผลที่ต้องใช้ ADX กรองเสมอ)

## Verification
เมื่อนำไปเขียนโปรแกรม บอทจะต้องมีฟังก์ชันคำนวณ `ADX` ก่อนเป็นลำดับแรก หาก `ADX > 25` บอทจะต้อง `return` และข้ามการเช็คเงื่อนไข `Bollinger Bands` ทันที