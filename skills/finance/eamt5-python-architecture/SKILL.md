---
name: eamt5-python-architecture
description: "แนวทางและโครงสร้างการสร้าง EA บน MT5 เชื่อมต่อกับ Python สำหรับระบบเทรดอัตโนมัติ"
version: 0.1.0
metadata:
  hermes:
    tags: [MT5, Python, EA, Architecture, Trading]
---

# การสร้างระบบเทรด MT5 ด้วย Python (System Architecture)

สกิลนี้อธิบายโครงสร้าง (Architecture) และแนวทางการพัฒนาระบบเทรดอัตโนมัติที่เชื่อมต่อระหว่าง MetaTrader 5 (MT5) และ Python โดยมุ่งเน้นการใช้จุดแข็งของ Python (Data Science, ML/AI, Analytics) ร่วมกับความเสถียรในการส่งคำสั่งของ MT5 (Expert Advisor)

## When to Use

- "ช่วยค้นหาบทความนำมาสร้างสกิล EA MT5"
- "การวางแนวทาง โครงสร้างระบบเทรด MT5 ด้วย Python"
- เมื่อผู้ใช้ต้องการออกแบบสถาปัตยกรรม (Architecture) สำหรับระบบเทรด Algorithmic Trading

## Prerequisites

- ความเข้าใจในภาษา MQL5 สำหรับสร้าง EA พื้นฐาน
- ความเข้าใจในภาษา Python และ Data Science Libraries (Pandas, Scikit-learn, PyTorch)
- ไลบรารี `MetaTrader5` สำหรับ Python

## สถาปัตยกรรมระบบ (System Architecture Approaches)

การพัฒนาระบบเทรดเชื่อมต่อ MT5 กับ Python มักแบ่งออกเป็น 2 แนวทางหลัก:

### Approach 1: Python API Polling (Direct Python Execution)
*Python เป็นตัวควบคุมหลักทั้งหมด ดึงข้อมูล วิเคราะห์ และส่งคำสั่งเทรดตรงเข้า MT5*

*   **โครงสร้าง:** Python Script (รันบน VPS) <--> `MetaTrader5` Python Library <--> MT5 Terminal
*   **ข้อดี:** 
    *   เขียนและดูแลรักษาง่าย โค้ดทั้งหมดรวมอยู่ใน Python
    *   เข้าถึง Ecosystem ของ Python (Pandas, ML/DL) ได้ทันที
*   **ข้อเสีย:**
    *   ต้องเปิด Python Script ทิ้งไว้ตลอดเวลา
    *   อาจมี Latency เล็กน้อยจากการคุยผ่าน API
*   **Workflow:**
    1.  Python ใช้ `mt5.copy_rates_from_pos()` ดึงราคา OHLCV
    2.  คำนวณ Indicator (เช่น EMA, MACD, ADX) หรือนำเข้า ML Model
    3.  Python ตัดสินใจสร้าง Trade Signal
    4.  Python ใช้ `mt5.order_send()` เพื่อเปิด/ปิดออเดอร์ใน MT5

### Approach 2: Asynchronous Microservices (REST API / ZeroMQ)
*แยกหน้าที่กันชัดเจน: MT5 รับผิดชอบราคาและการส่งคำสั่ง, Python รับผิดชอบการวิเคราะห์ข้อมูลและ AI/ML*

*   **โครงสร้าง:** MQL5 EA (บน MT5) <--> HTTP REST API (Flask/FastAPI) <--> Python ML Engine
*   **ข้อดี:**
    *   มีความทนทาน (Robust) มากกว่า ลดปัญหาคอขวด
    *   EA ทำงานได้อย่างอิสระ หาก Python ฝั่งวิเคราะห์หลุด EA ยังดูแล Risk Management (SL/TP) ต่อได้
*   **Workflow:**
    1.  EA บน MT5 ดึงราคาปัจจุบัน
    2.  EA ทำ WebRequest (POST) ส่ง JSON Payload (ราคา, Volume) ไปยัง REST API ของ Python (`/analyze`)
    3.  Python API รับข้อมูล, ทำ Feature Engineering, และรัน AI Model (เช่น Gradient Boosting หรือ LSTM)
    4.  Python ส่ง Signal (BUY/SELL) พร้อมค่า Stop Loss (SL) / Take Profit (TP) กลับไปเป็น JSON
    5.  EA รับ Signal แล้วส่งคำสั่ง `OrderSend()` เข้าตลาด

### Approach 3: ONNX Model Export (Live Native Inference)
*รัน AI Model ในตัว MT5 โดยไม่ใช้ Python ตอนเทรดจริง*

*   **โครงสร้าง:** Python Train -> Export `.onnx` -> MQL5 EA Load `.onnx`
*   **ข้อดี:**
    *   เร็วที่สุด (Zero Latency จาก Network)
    *   ไม่ต้องรัน Python ทิ้งไว้ขณะเทรดจริง
*   **Workflow:**
    1.  Python (รันบน VPS) ดึงข้อมูลอดีตมาเทรนโมเดล (เช่น PyTorch LSTM)
    2.  Python ทำการแปลง (Export) โมเดลเป็นฟอร์แมต ONNX (`.onnx`)
    3.  Python บันทึกไฟล์ `.onnx` ลงใน Shared Folder ของ MT5
    4.  MQL5 EA รันบนกราฟ โหลดไฟล์ `.onnx` เข้ามาคำนวณ Signal สดๆ ในระดับ C++

## การออกแบบโครงสร้างเพื่อความปลอดภัย (Best Practices)

1.  **Risk Management in EA (Not Python):** ไม่ว่าจะใช้สถาปัตยกรรมไหน การตัดขาดทุน (Stop Loss) และทำกำไร (Take Profit) ควรกำหนดเข้าไปใน `OrderSend()` ทันที เพื่อให้ Server โบรกเกอร์รับทราบ หากเน็ตหลุด ออเดอร์จะยังคงปลอดภัย
2.  **Avoid Look-ahead Bias:** หากใช้ ML/DL ในการสร้าง Signal ต้องแยก Training Data และ Testing Data อย่างเด็ดขาด และระวังการใช้ข้อมูลอนาคตมาเทรน (เช่น คำนวณข้ามแท่งเทียน)
3.  **Heartbeat Check:** ใน Approach ที่ 2 (REST API) EA ควรมีระบบตรวจสอบว่า Python API ยังมีชีวิตอยู่หรือไม่ หาก Timeout ควรหยุดเปิดออเดอร์ใหม่

## Verification
- ระบบควรทดสอบในโหมด Sandbox / Demo Account เป็นเวลาอย่างน้อย 1-2 สัปดาห์ (Forward Test) เพื่อตรวจสอบ Latency และการทำงานข้ามคืนของ Python Script / EA