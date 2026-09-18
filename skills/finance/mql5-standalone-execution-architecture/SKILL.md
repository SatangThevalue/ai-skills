---
name: mql5-standalone-execution-architecture
description: "สถาปัตยกรรม MQL5 EA แบบ Standalone สำหรับรันโมเดล ONNX โดยไม่ง้อ Backend Python เซิร์ฟเวอร์"
---

# MQL5 Standalone Execution Architecture (Zero-Backend Pattern)

ระบบ AI Quant Trading ที่ดีที่สุด คือระบบที่ตัวโมเดล (Prediction Engine) และตัวออกออเดอร์ (Execution Engine) สามารถทำงานแยกขาดจากกัน (Decoupled) ได้ 100% เอกสารนี้ระบุมาตรฐานการเขียน Expert Advisor (EA) ใน MT5 ให้เป็นแบบ Standalone เพื่อให้ผู้ใช้นำไฟล์ไปรันบน VPS เปล่าๆ ได้โดยไม่เกิด Connection Error.

---

## 1. Dynamic Configuration Loading (ป้องกัน Human Error)
ห้ามให้ผู้ใช้ต้องมากรอกค่าพารามิเตอร์เชิงลึก (เช่น `Buy Threshold`, `Sell Threshold`, `ATR Multipliers`) เองหน้างาน เพราะถ้าอัปเดตโมเดลเวอร์ชันใหม่แล้วลืมแก้ค่า พอร์ตจะพังทันที
- **วิธีแก้:** ฝั่ง Python (ตอน Export ONNX) จะต้องคลอดไฟล์ `model_config.json` ออกมาด้วย
- **ใน MQL5:** ใช้ไลบรารี `JAson.mqh` สั่งอ่านไฟล์ JSON ในฟังก์ชัน `OnInit()` แล้วจองหน่วยความจำ (ArrayResize) เท่ากับจำนวน Features ที่โมเดลนั้นต้องการเป๊ะๆ

## 2. Standalone News Filter (ดักข่าวจาก ForexFactory)
EA สาย Quant มักจะล้างพอร์ตตอนช่วงเวลาประกาศข่าวเศรษฐกิจสำคัญ (NFP, CPI) การจะให้ Python ส่งข้อมูลข่าวมาให้ตลอดเวลาเสี่ยงต่อการหลุดเน็ต
- **วิธีแก้:** เขียนให้ MQL5 ยิงคำสั่ง `WebRequest()` ไปดึงไฟล์ XML จากปฏิทินข่าว (เช่น ForexFactory) ด้วยตัวเอง **แต่อนุญาตให้ยิงแค่วันละ 1 ครั้งเท่านั้น** (เช่น ตอน 00:01 น.) แล้วเก็บแผนการหลบข่าวทั้งสัปดาห์ไว้ใน RAM ของ MT5 เพื่อไม่ให้โดนแบน IP.

## 3. Dynamic Timezone Synchronization (แก้ปัญหา MT5 เวลาไม่ตรง)
Broker โฟเร็กซ์ส่วนใหญ่มีเซิร์ฟเวอร์อยู่คนละ Timezone กับเวลาที่โมเดล AI ของเราเทรนมา (ซึ่งมักจะเป็น UTC) หรือเวลาข่าวของ ForexFactory ที่ส่งมาเป็น GMT.
- **วิธีแก้:** ห้าม Hardcode โซนเวลาใน MQL5 เด็ดขาด! ให้เขียนโค้ดเพื่อหาค่าส่วนต่างเวลาแบบ Dynamic ดังนี้:
  ```cpp
  int server_offset_seconds = TimeCurrent() - TimeGMT();
  // นำ offset ไปบวก/ลบ กับเวลาของข่าว เพื่อให้ EA รู้ว่าจะต้องสั่งระงับออเดอร์ (Blackout) ในเวลาเซิร์ฟเวอร์ที่เท่าไหร่เป๊ะๆ
  ```

## 4. Double Logging (กันข้อมูลสืบสวนสูญหาย)
การเปิดรันบอทบน VPS 24/5 มักจะเจอปัญหาเซิร์ฟเวอร์ Restart หรือเน็ตหลุดโดยไม่คาดคิด ทำให้ Logs บนหน้าจอ Experts หายไป.
- **วิธีแก้:** เขียนฟังก์ชัน `LogMsg()` ทุกครั้งที่ระบบตัดสินใจเรื่องสำคัญ (เช่น Spread ถ่าง, โดน News Filter บล็อก, คำนวณ Lot Sizing) ให้พิมพ์ออกจอ **พร้อมกับเขียนลงไฟล์ `EA_Name_Date.log` และสั่ง `FileFlush()` ทันที** เพื่อการันตีว่าข้อมูลลงดิสก์แน่นอน.

## 5. Graceful Degradation (ถ้าเน็ตหลุด EA ห้ามพัง)
ถ้าระบบดึงข้อมูล Macro Economics (เช่น ยีลด์พันธบัตร US10Y) หรือเว็บ ForexFactory ล่ม EA ต้องไม่ล่มตาม
- **วิธีแก้:** ใส่เงื่อนไขตรวจสอบ ถ้าเชื่อมต่อ API หรือดึง JSON ไม่ได้ ให้ EA แจ้งเตือนลง Log ว่า "Offline Mode" แล้วปรับลอจิกเทรดให้เปลี่ยนไปใช้ค่า Default ที่ปลอดภัยที่สุด หรือระงับการเปิดออเดอร์ใหม่จนกว่าอินเทอร์เน็ตจะกลับมา.

---
**Verification:** สคริปต์ EA ต้องสามารถนำไป Compile ผ่านใน MetaEditor โดยที่ไม่มีการพึ่งพาตัวแปรจากเซิร์ฟเวอร์ภายนอก (Zero External Variable Dependency) ในจังหวะยิงออเดอร์.
EOF