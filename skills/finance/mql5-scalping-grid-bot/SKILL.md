---
name: mql5-scalping-grid-bot
description: "โค้ด EA ต้นแบบ (MQL5) สำหรับการทำ Scalping และ Selective Grid เทียบเท่า EA เชิงพาณิชย์"
version: 0.1.0
metadata:
  hermes:
    tags: [MQL5, EA, MT5, Scalping, Grid, XAUUSD]
---

# MQL5 Scalping Robot Pro (Clone)

สกิลนี้คือรหัสต้นฉบับ (Source Code) สำหรับการนำไปสร้าง Expert Advisor บน MetaTrader 5 โดยเขียนด้วยภาษา MQL5 ล้วน (ไม่ใช้ Python) ถอดแบบโครงสร้างมาจากบอท Scalping ทองคำ (XAUUSD) บนกราฟ M1 ซึ่งรวมระบบหน้าตั้งค่า, ระบบแก้พอร์ตแบบ Selective Grid, และระบบป้องกันข่าว

## When to Use

- "ช่วยแปลงเป็น ea mt5 ไม่ใช้ python"
- เมื่อต้องการ Source code EA ที่เอาไปคอมไพล์ลง MT5 ได้ทันที
- เมื่อต้องการดูตรรกะการเขียน MQL5 แบบ Object-Oriented (CTrade)

## Quick Reference

- **File Extension:** `.mq5`
- **Trading Class:** `#include <Trade\Trade.mqh>`
- **Logic:** เข้าออเดอร์เมื่อราคาทะลุขอบ BB + RSI ตึง และแก้พอร์ตด้วย Grid หากผิดทาง
- **Filter:** ป้องกันข่าวด้วยค่า ATR ของแท่งปัจจุบันเทียบกับค่าเฉลี่ย

## Architecture Highlights

โค้ดชุดนี้ครอบคลุมองค์ประกอบของบอทราคาแพง:
1. **Inputs:** แบ่งหมวดหมู่ชัดเจน (Risk, Execution, Protection) ด้วย `input group`
2. **Dashboard:** ใช้ฟังก์ชัน `Comment()` เพื่อแสดงสถานะ P/L รายวันแบบ Real-time บนหน้าจอ
3. **Daily Limits:** บันทึก Balance ตอนเช้า เพื่อคำนวณ Daily Profit หากชนเป้าหมายจะหยุดทำงาน
4. **News Filter:** แทนที่จะต้องเชื่อม API ข่าวภายนอก โค้ดนี้ใช้ `ATR Spike` (ความยาวแท่งปัจจุบัน > 3 เท่าของค่าเฉลี่ย) เพื่อระงับการทำงาน (Pause) ชั่วคราว

## Procedure (การนำไปใช้งาน)

1. เปิดโปรแกรม MetaTrader 5
2. กด `F4` เพื่อเปิด MetaEditor
3. สร้างไฟล์ Expert Advisor ใหม่ (New -> Expert Advisor (template))
4. ลบโค้ดทั้งหมดทิ้ง แล้ว Copy โค้ดจากสกิลนี้ไปวาง
5. กด `F7` เพื่อทำการ Compile
6. ลากบอทใส่กราฟ `XAUUSD` ใน Timeframe `M1`

## Pitfalls

- **Grid Sizing:** ตัวแปร `InpLotMultiplier = 1.5` หมายถึงหลอดจะใหญ่ขึ้นเรื่อยๆ หากพอร์ตมีเงินทุนน้อย (เช่น < $1,000) อาจทำให้เกิด Margin Call ได้หากตลาดวิ่งทางเดียวยาวๆ
- **Backtesting M1:** การทำ Backtest บนกราฟ 1 นาที ต้องเลือกโหมด "Every tick based on real ticks" เท่านั้น มิฉะนั้นการจำลอง Spread จะผิดเพี้ยนไปจากความจริงมาก
- **Trailing Stop:** โค้ดในส่วน Trailing Stop ถูกย่อไว้ (Snippet) หากนำไปใช้จริงต้องเขียนลูป `OrderModify` เพิ่มเติม

## Verification
เมื่อรันบนกราฟ มุมซ้ายบนของหน้าจอจะต้องปรากฏ Dashboard แสดงคำว่า `🤖 Scalping Robot Pro (Clone)` พร้อมยอด Equity และ Daily P/L ที่อัปเดตแบบเรียลไทม์