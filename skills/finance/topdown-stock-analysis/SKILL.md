---
name: topdown-stock-analysis
description: "กรอบการวิเคราะห์หุ้นแบบ Top-Down Approach (Global -> Thai -> Stock)"
version: 0.1.0
metadata:
  hermes:
    tags: [Strategy, Top-Down, Trading, Analysis, Framework]
---

# กรอบการวิเคราะห์หุ้นแบบ Top-Down Approach

สกิลนี้คือ "แผนที่ความคิด (Framework)" ในการวิเคราะห์การลงทุนที่ครบวงจร ตั้งแต่การดูปัจจัยเศรษฐกิจระดับโลก ย่อลงมาที่ตลาดหุ้นไทย แล้วเจาะจงหาสินทรัพย์ที่เหมาะสม (เช่น หุ้นรายตัว หรือ DW) รวมถึงจุดเข้า-ออก และการบริหารพอร์ต เพื่อให้บอทเทรดและนักลงทุนมีกระบวนการตัดสินใจที่เป็นระบบ

## When to Use

- "สร้างกระบวนการเทรด DW ในประเทศไทย"
- "เริ่มตั้งแต่ดึงข้อมูลตลาดโลก วิเคราะห์ตลาด..."
- เมื่อต้องการสร้าง Trading System Architecture ที่ต้องเชื่อมข้อมูลจากหลายแหล่ง

## Quick Reference

- **Global Macro:** ดู VIX, US Bond Yield, USD Index
- **Thai Market:** ดู SET50 Trend, Fund Flow
- **Stock Selection:** ดู Sector Rotation, ADX > 25, Breakout
- **Execution:** Position Sizing (Risk 1-2%), Hedging ด้วย Put DW

## Procedure (The Trading Blueprint)

การสร้างกระบวนการเทรดที่สมบูรณ์ ควรแบ่งเป็น 5 ขั้นตอน (Phases) ดังนี้:

### 🌍 Phase 1: การวิเคราะห์ภาพรวมตลาดโลก (Global Macro Analysis)
ตรวจสอบอารมณ์ของนักลงทุนสถาบันต่างชาติ เพื่อประเมินสภาวะ **Risk-On** (กล้าเสี่ยง) หรือ **Risk-Off** (หนีตาย)
- **เครื่องมือ / Indicators:**
  - **VIX Index:** ดัชนีความกลัว ถ้าระดับ VIX พุ่งแรง (เช่น >25-30) แสดงว่าตลาดแพนิก การเล่นหน้า Long/Call จะอันตรายมาก
  - **USD Index & 10-Year US Bond Yield:** ถ้าเงินดอลลาร์แข็งค่าและยีลด์พันธบัตรพุ่ง มักหมายถึง Fund flow กำลังไหลออกจากตลาดเกิดใหม่ (รวมถึงไทย)
  - **Global Futures:** S&P500, Dow Jones, S50 Index Futures

### 🇹🇭 Phase 2: วิเคราะห์ตลาดหุ้นไทย (Thai Market Condition)
- **เครื่องมือ / Indicators:**
  - **Fund Flow:** ตรวจสอบยอดซื้อขายสะสมของนักลงทุนต่างชาติ (Foreign) และสถาบัน (Institution)
  - **Market Trend (SET / SET50):** ตลาดไทยเป็นขาขึ้น, ขาลง, หรือ Sideways เพื่อกำหนดกลยุทธ์หลัก:
    - *ตลาดย่อตัวรุนแรง (VIX สูง):* พิจารณาทำ Hedging ด้วย **SET50 Put DW**
    - *ตลาดขาขึ้นชัดเจน:* เล็งหุ้นที่แข็งแกร่งกว่าตลาด (Outperform)

### 📈 Phase 3: การคัดเลือกหุ้นรายตัว (Underlying Selection)
- กรองหุ้นในกลุ่ม **SET50 / SET100** ที่มีสภาพคล่องสูง
- **Technical Setup (เกณฑ์ของสมองกล):**
  - **Trend Strength:** ห้ามเล่น DW บนหุ้นที่กราฟนิ่ง (Sideways) ต้องใช้ค่า **ADX > 25** เพื่อยืนยันว่าหุ้นมีเทรนด์ (หนี Time Decay)
  - **Momentum:** หาราคาที่ทำ Breakout, ตัดเส้น EMA 20/50 ขึ้น, หรือราคาย่อมาที่แนวรับสำคัญ (Buy the Dip)

### 🔍 Phase 4: การคัดกรองตราสาร (DW Filtering & Price Mapping)
หากต้องการเทรด DW เพื่อเร่งผลตอบแทน (ใช้ทุนน้อย) เมื่อได้หุ้นแม่จาก Phase 3 แล้ว ให้คัดสเปก DW ดังนี้:
- **เวลา:** ต้องมีอายุคงเหลือ (Time to Maturity) > 1 - 1.5 เดือน
- **อัตราทด (Effective Gearing):** อยู่ระหว่าง 3 - 6 เท่า
- **ความไว (Sensitivity / Tick):** ประมาณ 0.8 - 1.2
- **Price Mapping:** คำนวณจุดเข้า (Entry), ตัดขาดทุน (SL), ทำกำไร (TP) จาก "กราฟหุ้นแม่" แล้วแปลงเป็นราคา DW จาก "ตารางราคา" ของผู้ออก

### 💰 Phase 5: การบริหารเงินและความเสี่ยง (Money & Risk Management)
- **Position Sizing:** กองทุนใหญ่ไม่เคย All-in การเทรด DW 1 ตัว **ไม่ควรใช้เงินเกิน 5-10% ของพอร์ต**
- **Risk per Trade:** กำหนดเงินที่จะยอมเสียได้สูงสุด (Max Loss) ไว้ที่ 1-2% ของพอร์ต
- **Execution Rule:**
  - ผิดทาง **Cut-Loss ทันที** ห้ามถัวเฉลี่ยขาลงเด็ดขาด เพราะหุ้นและ DW โดน Double Damage จาก Time Decay
  - ตรวจสอบวัน **XD (ปันผล)** ของหุ้นแม่ให้ดี หากหุ้นร่วงเพราะปันผล บอทที่ไม่ได้กรองปฏิทิน XD อาจจะสั่งคัตลอสฟรี

## Verification
- บอทที่ทำงานตาม Blueprint นี้ จะต้องเรียกใช้ API จากหลายแห่ง (Yahoo Finance สำหรับ VIX/USD, Settrade สำหรับยอด Fund Flow และการยิงคำสั่ง) และจะต้องมี Logic การปฏิเสธคำสั่ง (Reject Trade) ถ้าระดับ VIX พุ่งสูงผิดปกติ