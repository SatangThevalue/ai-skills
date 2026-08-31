---
name: ea-capital-protection-features
description: "ฟีเจอร์การปกป้องเงินทุน (Capital Protection) ขั้นสูงสำหรับ EA และบอทเทรด"
version: 0.1.0
metadata:
  hermes:
    tags: [EA, Forex, Risk Management, Capital Protection, Prop Firm]
---

# EA Capital Protection Features (Advanced Risk Management)

สกิลนี้รวบรวมเทคนิคและฟีเจอร์ขั้นสูงในการปกป้องเงินทุน (Capital Protection) สำหรับการเขียน Expert Advisor (EA) หรือบอท Python โดยอ้างอิงจากมาตรฐานของระบบเทรดที่ใช้สอบกองทุน (Prop Firm) ซึ่งให้ความสำคัญกับการ "เอาตัวรอด" มากกว่าการ "ทำกำไรสูงสุด"

## When to Use

- "แล้วควรมี ฟีเจอร์อื่นๆอีกไหม เพื่อความอยู่รอดของพอร์ต"
- "ช่วยหาบทความเกี่ยวกับ risk management หรือ drawdown protection"
- เมื่อต้องการเพิ่มความทนทาน (Robustness) ให้กับระบบเทรดอัตโนมัติ

## Quick Reference

- **Daily Drawdown Limiter:** หยุดเทรดทันทีเมื่อพอร์ตติดลบรายวันถึง X% (เช่น -4.5%)
- **Dynamic Position Sizing:** ลด Risk% ลงเมื่อแพ้ติดกัน เพิ่มขึ้นเมื่อชนะ
- **Emergency Reversal / Hard Close:** ทิ้งออเดอร์ทันทีถ้าราคาเบรคเอาท์สวนทางรุนแรง
- **Triple-Layer Exits:** แบ่งปิดทำกำไร (Partial Close) + กันหน้าทุน (Breakeven) + Trailing Stop

## สถาปัตยกรรมการปกป้องเงินทุน (The Protection Blueprint)

จากบทความในชุมชนนักพัฒนา MQL5 บอทระดับมืออาชีพจะมีการป้องกันความเสี่ยง 4 ระดับ (4 Layers of Protection) ดังนี้:

### Layer 1: Account-Level Protection (ระบบปกป้องระดับพอร์ต)
นี่คือฟีเจอร์ "สับคัตเอาท์" เพื่อป้องกันพอร์ตล้าง หรือสอบตกกองทุน
*   **Daily Drawdown Limiter:** 
    *   บอทจะบันทึกค่า `Equity` ตอนเริ่มต้นวัน (Midnight Server Time)
    *   คำนวณตลอดเวลาว่า `((Current_Equity - Start_Equity) / Start_Equity) * 100` ติดลบกี่เปอร์เซ็นต์
    *   *กฏ:* ถ้าติดลบถึง -4.5% (เผื่อ Buffer ให้กองทุนที่ตั้งไว้ -5%) บอทจะ **"ปิดทุกออเดอร์ทันที (Close All)"** และระงับการเปิดออเดอร์ใหม่จนกว่าจะขึ้นวันถัดไป
*   **Overall Drawdown Limiter:**
    *   หยุดการทำงานถาวร หากพอร์ตติดลบรวมถึง -9% (ป้องกันกองทุนแบนที่ -10%)
*   **Profit Target Halter:**
    *   เมื่อทำกำไรถึงเป้าหมาย (เช่น +10% ของพอร์ต) ให้หยุดเทรดทันที ป้องกันการคืนกำไรให้ตลาด

### Layer 2: Dynamic Position Sizing (ระบบคุมความเสี่ยงต่อไม้)
*   **Risk per Trade:** ไม่ใช้ Lot คงที่ (เช่น 0.01 ตลอด) แต่คำนวณ Lot จากความเสี่ยง (เช่น เสี่ยงไม้ละ 1% หรือ 2%)
*   **Drawdown Recovery Logic (ลดสเปกเมื่อบาดเจ็บ):** 
    *   ถ้าแพ้ติดกัน 3 ไม้ บอทจะ **"ลด"** Risk per trade ลงครึ่งหนึ่ง (เช่น จาก 2% เหลือ 1%) เพื่อเซฟเงินทุน
    *   เมื่อกลับมาชนะติดกัน หรือพอร์ตกลับมาทำ New High ถึงจะปรับ Risk กลับไปเท่าเดิม

### Layer 3: Context & Filter Protection (ระบบหลีกเลี่ยงสภาวะอันตราย)
*   **News Filter (Pause Trading):** 
    *   บอทจะไม่ทำงานก่อนและหลังข่าวใหญ่ 15 นาที (เช่น NFP, CPI, FOMC)
    *   *วิธีทำ:* ใช้ API ปฏิทินข่าว หรือใช้วิธีคำนวณ Volatility (ATR Spike) ที่เราเคยทำ
*   **High Timeframe Confirmation (HTF Filter):**
    *   ต่อให้สัญญาณ M5 บอกให้ BUY แต่ถ้าเทรนด์ของ D1 หรือ H4 เป็นทิศทาง DOWN ระบบจะปฏิเสธการเข้าเทรดนั้นทันที (หลีกเลี่ยงการโดนรถบรรทุกชน)

### Layer 4: Triple-Layer Trade Management (ระบบทางหนีทีไล่)
การตั้ง TP/SL ธรรมดาไม่เพียงพอสำหรับตลาดที่ผันผวน (เช่น ทองคำ) บอทต้องจัดการออเดอร์ที่กำลังวิ่งอยู่ (In-flight management) ได้:
1.  **Partial Close & Breakeven (ปิดครึ่งนึง+กันทุน):** 
    *   สมมติ Risk:Reward คือ 1:2 ถ้าราคาบวกไปได้ 1 ส่วน (1R) บอทจะ **ปิดออเดอร์ครึ่งนึง (ปิด 50% ของ Lot)** เอาเงินเข้ากระเป๋า
    *   และขยับ Stop Loss ขึ้นมาบังที่ "จุดเข้าซื้อ (Entry Price)" การันตีว่าไม้นี้ไม่มีทางขาดทุน
2.  **ATR Trailing Stop:** 
    *   แทนที่จะขยับ TP ไปเรื่อยๆ บอทจะขยับ Stop Loss ตามราคาไปด้วยระยะห่าง `1.5 * ATR` เพื่อกินเทรนด์คำโตๆ โดยให้ตลาดเป็นคนตัดสินใจเตะเราออกเอง
3.  **Emergency Reversal Close:**
    *   หากถือฝั่ง BUY อยู่ แล้วเกิดแท่งเทียนสีแดงแทงทะลุแนวรับสำคัญรุนแรง (Breakout) ให้คัตทิ้งทันที โดยไม่ต้องรอให้ชน Stop Loss เดิม 

## Verification
- บอทที่มีสถาปัตยกรรมเหล่านี้ เมื่อนำไปทดสอบ Backtest จะเห็นว่ากราฟ Equity (เส้นสีเขียว) จะไม่มีจังหวะร่วงดิ่งเป็นเหว (Drawdown) ลึกเกินกว่า % ที่เรากำหนดไว้ใน Limiter อย่างเด็ดขาด