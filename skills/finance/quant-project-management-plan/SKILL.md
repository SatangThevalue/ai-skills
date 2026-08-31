---
name: quant-project-management-plan
description: "แผนการบริหารโครงการ (Project Management Plan) และ WBS สำหรับการสร้าง AI Trading Platform ระดับ MLOps"
---

# Project Management Plan: AI Trading Platform
**(MT5 + LightGBM + Optuna + ONNX + MLflow + Prefect)**

ในมุมมองของ Project Manager (PM) โครงการนี้ไม่ใช่แค่การ "สร้างโมเดล AI หรือทำ EA" แต่เป็นการบริหารระบบแบบ 3 แกนหลักที่ต้องทำงานสอดประสานกัน:
`Research Platform` + `MLOps Platform` + `Trading Platform`

---

## 🎯 เป้าหมายโครงการ (Project Goals)

### 1. Goal ระยะสั้น: MVP (ภายใน 8-12 สัปดาห์)
โฟกัสที่การพิสูจน์ว่าไปป์ไลน์หลักทำงานได้และสามารถเทรดได้จริง
- ✅ ดึงข้อมูลตลาดอัตโนมัติ (Data Pipeline)
- ✅ สร้าง Feature 80+ รายการ
- ✅ เทรน LightGBM
- ✅ ทำ Walk Forward Testing
- ✅ Export โมเดลเป็น ONNX
- ✅ นำไปใช้งานเทรดจริงบน MT5 ได้

### 2. Goal ระยะกลาง: Production (ภายใน 3-6 เดือน)
โฟกัสที่ความเสถียร ระบบอัตโนมัติ และการดูแลรักษาระยะยาว (MLOps)
- ✅ วางระบบ MLflow (Experiment & Model Registry)
- ✅ วางระบบ Prefect (Workflow Orchestration)
- ✅ Monitoring ระบบ
- ✅ Drift Detection (ตรวจจับ Data/Concept Drift)
- ✅ Auto Retraining (เทรนโมเดลใหม่เมื่อประสิทธิภาพตก)

### 3. Goal ระยะยาว: Quant Platform (Advanced)
โฟกัสที่การทำกำไรแบบสถาบัน การสเกล และเทคนิคขั้นสูง
- ✅ Portfolio Optimization (เทรดหลายคู่เงินพร้อมบริหารความเสี่ยงรวม)
- ✅ Ensemble Models (โหวตติ้งโมเดลหลายตัว)
- ✅ Market Regime Detection (แยกสภาวะตลาดอัจฉริยะ)
- ✅ Automated Deployment เต็มรูปแบบ

---

## 📋 Work Breakdown Structure (WBS)
*แผนแตกงานสำหรับการบริหารจัดการโครงการแบ่งตามระยะเวลาที่แนะนำ*

### Phase 0: Project Setup (สัปดาห์ 1-2)
| งาน (Tasks) | รายละเอียด |
|-------|---------|
| **Define Architecture** | กำหนดโครงสร้าง Tech Stack, Database Schema และ Flow กลาง |
| **Environment Setup** | ตั้งค่า Python, สร้าง Git Repo, วางโครงสร้างโฟลเดอร์แบบ Modular |

### Phase 1: Data & MVP Model (สัปดาห์ 3-7)
| งาน (Tasks) | รายละเอียด |
|-------|---------|
| **Data Collection** | เขียนสคริปต์ดึง OHLCV จาก MT5 / Yahoo API เซฟลง DuckDB/PostgreSQL |
| **Feature Engineering** | เขียน Pipeline สกัด 80+ ฟีเจอร์ (Trend, Volatility, Momentum ฯลฯ) |
| **Model Training** | เทรน LightGBM, จูนด้วย Optuna, ประเมินด้วย Walk Forward |

### Phase 2: Deployment & MT5 (สัปดาห์ 8-12)
| งาน (Tasks) | รายละเอียด |
|-------|---------|
| **ONNX Export** | แปลงโมเดล, บันทึก Metadata/Scaler และเทสต์ด้วย ONNX Runtime |
| **MT5 EA Integration** | เขียน MQL5, โหลด ONNX, เขียน Risk Engine (Spread/Slippage Protection) |
| **Paper Trading** | รัน Forward Test บนบัญชี Demo อย่างน้อย 30 วัน |

### Phase 3: MLOps & Automation (เดือน 4-6)
| งาน (Tasks) | รายละเอียด |
|-------|---------|
| **MLflow Setup** | นำโค้ด Training มาผูกกับ MLflow เพื่อทำ Experiment Tracking |
| **Prefect Orchestration**| เปลี่ยน Script ธรรมดาเป็น Prefect Flows (Data, Train, Deploy) |
| **Evidently Integration** | ติดตั้ง Drift Detection เพื่อจับตาดูความแม่นยำและการเปลี่ยนของข้อมูล |

---

## 📊 Monitoring Checklist (หลังขึ้น Production)
เมื่อระบบขึ้นเทรดจริง ต้องมีการเช็คลิสต์สิ่งเหล่านี้เป็นประจำ:

- [ ] **Data Drift:** การกระจายตัวของข้อมูลเปลี่ยนไปจากตอน Train หรือไม่
- [ ] **Concept Drift:** ความสัมพันธ์ระหว่าง Feature กับทิศทางราคาเปลี่ยนไปหรือไม่
- [ ] **Sharpe Ratio:** ผลตอบแทนเทียบกับความเสี่ยงยัง > 1.5 หรือเปล่า
- [ ] **Max Drawdown:** อยู่ในเกณฑ์ที่ตั้งไว้ (เช่น < 15%) หรือไม่
- [ ] **Auto Retraining:** ระบบทริกเกอร์การเทรนใหม่และสลับโมเดลได้สำเร็จเมื่อพบค่าที่ผิดปกติ

> **บทสรุปสำหรับ PM:** 
> หากบริหารจัดการโครงการและทำตามแผนนี้ครบ ระบบที่ได้จะไม่ใช่แค่เพียง "EA" หรือ "AI Trading Bot ทั่วไป" แต่จะกลายเป็น **MLOps-based Quant Trading Platform** ที่สามารถ ดึงข้อมูล, สร้างฟีเจอร์, เทรน, วัดผล, Deploy, Monitor และปรับปรุงโมเดลอย่างต่อเนื่องได้ในระดับ Production จริง
> *(ดูรายละเอียดมาตรฐานการดำเนินการราย Phase ในระดับสถาบันได้ที่สกิล `quant-trading-standard-framework`)*