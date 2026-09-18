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
*แผนแตกงานสำหรับการบริหารจัดการโครงการแบบเจาะลึก 16 Phases ดูรายละเอียดได้ที่สกิล `quant-platform-master-plan`*

### Phase A: Core Platform (สัปดาห์ 1-4)
| งาน (Tasks) | รายละเอียด |
|-------|---------|
| **Data Platform** | เขียนสคริปต์ดึง Data และทำระบบฐานข้อมูล |
| **Feature Store** | สร้าง Pipeline สกัด Feature ให้เป็นมาตรฐาน |
| **ML Models & MLflow** | เทรน LightGBM, จูน Optuna และเก็บ Metadata เข้า MLflow (หาก CPU เก่าขาด avx2 หรือพื้นที่ดิสก์น้อย ควรย้ายขั้นตอนนี้ไปรันบน Local PC/Mac) |
| **ONNX Export** | แปลงโมเดลและไฟล์ Config ออกมารอไว้ |

### Phase B: Execution & Risk (สัปดาห์ 5-8)
| งาน (Tasks) | รายละเอียด |
|-------|---------|
| **Execution Engine** | เขียน MQL5 สำหรับจัดการออเดอร์เข้า/ออก |
| **ATR Sizing** | สร้างระบบ Sizing อิงความผันผวนของตลาด |
| **Risk Engine** | ทำหน้าด่านกรอง Daily Loss, Max Drawdown |

### Phase C: Intelligence & Monitoring (เดือน 3-4)
| งาน (Tasks) | รายละเอียด |
|-------|---------|
| **Regime Detection**| สร้างโมเดลวิเคราะห์เทรนด์/ความผันผวน |
| **Drift Detection** | ทำระบบตรวจ Data/Concept Drift ผ่าน Evidently |
| **Monitoring** | สร้าง Dashboard ติดตาม Sharpe/PF |

### Phase D: Portfolio Management (เดือน 5)
| งาน (Tasks) | รายละเอียด |
|-------|---------|
| **Portfolio Engine**| ควบคุมการจัดสรรน้ำหนัก (Allocation) |
| **Correlation Engine**| ป้องกัน Exposure ซ้ำซ้อนจากการถือหลายคู่เงิน |
| **Strategy Router** | สลับใช้โมเดลตามสภาพตลาดแบบ Real-time |

### Phase E: Advanced Quant (เดือน 6 เป็นต้นไป)
| งาน (Tasks) | รายละเอียด |
|-------|---------|
| **Statistical Arbitrage**| ทำ Pair Trading, Cointegration |
| **Ensemble Models** | ทำระบบโหวตด้วย Meta Model หลายตัว |

---

## 🚫 15 ข้อควรระวังสำหรับ PM (The Pitfalls)
การทำโปรเจกต์นี้ให้สำเร็จ PM ต้องระวังข้อผิดพลาดคลาสสิกที่ทำให้ระบบเจ๊งตอนรัน Production *(อ่านรายละเอียด 15 ข้อผิดพลาดแบบเต็มๆ ได้ที่สกิล `quant-platform-pm-pitfalls`)* เช่น:
- **Dependency Issues (VPS/OS Limits):** ระวังการใช้ Package ที่มีข้อจำกัดด้าน OS บน Production (เช่น `MetaTrader5` รันบน Linux ไม่ได้, `empyrical` ไม่รองรับ Python 3.12+) ต้องวางสถาปัตยกรรมชดเชย หรือใช้ไลบรารีทางเลือก (เช่น `quantstats` แทน `empyrical`)
- ใช้เวลากับการทำโมเดลมากเกินไป แต่ลืมทำ Execution และ Risk Engine
- กลัวโมเดล ONNX พัง มากกว่ากลัว "สูตรคำนวณ Feature ไม่ตรงกัน" ระหว่าง Python กับ MT5
- วัดผลด้วย Accuracy แทนที่จะวัดที่ Sharpe Ratio หรือ Profit Factor
- ลืมทำ Feature Versioning และ Label Versioning
- รีบทำระบบ Self-Learning / Auto Retrain เร็วเกินไป

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