---
name: ai-trading-continuous-learning
description: "Architecture and guidelines for building a Continuous Learning Pipeline for AI Trading models (Data Lake to MT5 ONNX) targeting Risk-adjusted Returns."
prerequisites: ["MLOps fundamentals", "Algorithmic trading concepts", "mt5-onnx-ai-trading-pipeline"]
---

# AI Trading: Continuous Learning Pipeline (ยิ่งเทรดยิ่งฉลาดขึ้น)

เป้าหมายหลักของการสร้างระบบ AI Trading ในระดับ Production ไม่ใช่การ Train โมเดลเพียงครั้งเดียวแล้วจบ แต่เป็นการสร้างระบบ **Continuous Learning Pipeline** ที่สามารถปรับตัวตามสภาวะตลาดที่เปลี่ยนแปลงไปได้ตลอดเวลา แนวคิดนี้จะคล้ายกับระบบ MLOps ในบริษัทยักษ์ใหญ่

---

## 🎯 เป้าหมายที่แท้จริง (The True Objective)

สิ่งสำคัญที่สุดที่ต้องตระหนัก: **เป้าหมายไม่ใช่ความแม่นยำ (Accuracy) สูงสุด แต่เป็น Risk-adjusted Return สูงสุด**

**ตัวอย่างความเข้าใจผิดที่พบบ่อย:**
| Model | Accuracy |
|---------|------------|
| Model A | 52% |
| Model B | 67% |

หลายครั้ง **Model A ทำกำไรได้ดีกว่า Model B** เพราะในการเทรดจริง เราสนใจตัวชี้วัดทางการเงินมากกว่าความแม่นยำทางสถิติเพียงอย่างเดียว

---

## 🏗️ Architecture ที่ควรสร้าง (The Pipeline)

```text
Market Data
     │
     ▼
Data Lake
     │
     ▼
Feature Store
     │
     ▼
Training Pipeline
     │
     ▼
Model Registry
     │
     ▼
ONNX Export
     │
     ▼
MT5 Production
     │
     ▼
Monitoring
     │
     ▼
Drift Detection
     │
     ▼
Retraining
```

---

## 📊 4 กลุ่มตัวชี้วัดที่ต้องวัด (The Core Metrics)

การจะรู้ว่าระบบทำงานได้ดีหรือไม่ ต้องวัดผลครอบคลุม 4 มิติ:

### 1. Data Metrics (คุณภาพข้อมูล)
*   **Data Quality:** ตรวจสอบความสมบูรณ์ของข้อมูล
    *   Missing Data % (เช่น ถ้า Missing > 1% ต้อง Alert)
    *   Duplicate %
    *   Outlier %
*   **Feature Drift:** ตรวจจับการเปลี่ยนแปลงพฤติกรรมของตลาด (Market Behavior Changed)
    *   เช่น RSI Distribution, ATR Distribution, Volume Distribution
    *   *ตัวอย่าง:* วันนี้ Mean RSI = 55 แต่ 3 เดือนต่อมา Mean RSI = 72 แสดงว่าตลาดเปลี่ยนไปแล้ว

### 2. Model Metrics (คุณภาพโมเดลเชิงสถิติ)
*   **Classification:** Accuracy, Recall, Precision, F1-Score, ROC-AUC
*   **Probability Quality:** วัดความน่าเชื่อถือของความน่าจะเป็นที่โมเดลทำนาย (Calibration Score)
    *   *ตัวอย่าง:* ถ้าโมเดลบอก BUY = 80% ความน่าจะเป็นที่ทิศทางจะถูกควรใกล้เคียง 80% จริงๆ

### 3. Trading Metrics (ตัวชี้วัดการเทรด - สำคัญที่สุด)
*   **Profit Factor:** (Gross Profit / Gross Loss) เป้าหมาย > 1.5
*   **Sharpe Ratio:** เป้าหมาย > 1.5
*   **Sortino Ratio:** มักดีกว่า Sharpe เพราะพิจารณาเฉพาะ Downside Risk (ความเสี่ยงขาลง)
*   **Maximum Drawdown:** เป้าหมาย < 15%
*   **Expected Value (EV):** `(WinRate × AvgWin) - (LossRate × AvgLoss)` เป้าหมายต้องเป็นบวก

### 4. Business Metrics (ผลกระทบต่อเงินจริง)
*   **Monthly Return:** 3-10% ต่อเดือนถือว่าอยู่ในเกณฑ์ดีมาก
*   **Recovery Factor:** (Net Profit / Max Drawdown)
*   **Capital Growth:** การเติบโตของพอร์ต (เช่น 100,000 → 120,000 → 150,000)

---

## 🔄 Model Improvement Loop (หัวใจของการพัฒนา)

การพัฒนาโมเดลควรทำเป็น Iteration (รอบ) อย่างต่อเนื่อง:

*   **Version 1:** เริ่มด้วย Features พื้นฐาน (เช่น 80 Features) ใช้ Gradient Boosting (เช่น LightGBM)
*   **Version 2:** เพิ่ม Feature Interaction (เช่น `RSI × ATR`, `EMA Gap × Volume`)
*   **Version 3:** เพิ่ม Multi-Timeframe Analysis (วิเคราะห์หลายกรอบเวลาพร้อมกัน)
*   **Version 4:** เพิ่ม Market Regime Detection (โมเดลวิเคราะห์สภาวะตลาด)
*   **Version 5:** ใช้ Ensemble Model (รวมพลังหลายโมเดล เช่น LightGBM + CatBoost + XGBoost)

### เทคนิคปรับปรุงโมเดลเพิ่มเติม
*   **Feature Selection:** ตัด Feature ที่ไม่มีประโยชน์ออกเป็นประจำทุกเดือน (เช่น ลดจาก 120 เหลือ 70 Features) เพื่อลด Noise
*   **Optuna Tuning:** ใช้ Optuna ค้นหา Hyperparameters อัตโนมัติ (learning_rate, num_leaves, max_depth)
*   **Ensemble:** เปลี่ยนจากการใช้โมเดลเดียว เป็น 3 โมเดลโหวตกัน (Voting)
*   **Threshold Optimization:** ปรับจุดตัดการตัดสินใจ เช่น ปกติ `BUY > 0.5` อาจปรับเป็น `BUY > 0.7` เพื่อลด False Signal ให้น้อยลงอย่างมีนัยสำคัญ

---

## 🕵️ Market Regime Detection (เทคนิคที่ Quant นิยมใช้)

ตลาดไม่ได้มีสภาวะเดียว แต่มีหลายสภาวะ:
*   **Trending** (มีเทรนด์ชัดเจน)
*   **Ranging** (ไซด์เวย์)
*   **Volatile** (ผันผวนสูง)
*   **Low Volatility** (ผันผวนต่ำ)

**กลยุทธ์:**
1.  สร้าง Model A สำหรับตลาด Trend
2.  สร้าง Model B สำหรับตลาด Range
3.  ใช้โมเดลตรวจ Regime ก่อน แล้วค่อยเลือกใช้โมเดลที่เหมาะสมกับสภาวะนั้นๆ
*(วิธีนี้มักให้ผลลัพธ์ดีกว่าการพยายามใช้โมเดลเดียวครอบจักรวาล)*

---

## 📉 Drift Detection (สิ่งที่คนมักลืม)

สภาวะตลาดเปลี่ยนไปตลอดเวลา โมเดลเดิมที่เคยเก่งอาจจะแย่ลง
*   *ตัวอย่าง:* ปี 2024 EURUSD เป็น Trend ชัดเจน แต่ปี 2026 เปลี่ยนเป็น Sideway
*   **วิธีแก้:** ต้องวัดค่า **PSI (Population Stability Index)**
*   **Action:** หากพบว่า **PSI > 0.25** แสดงว่าพฤติกรรมข้อมูลเปลี่ยนไปมาก ให้ **Trigger Retrain** ทันที

---

## 🔁 Retraining Strategy (กลยุทธ์การเทรนใหม่)

มี 3 รูปแบบหลัก:
1.  **Fixed Schedule:** เทรนใหม่ตามกำหนดเวลา (เช่น ทุกเดือน) - *ข้อดี: จัดการง่าย*
2.  **Rolling Window:** ใช้ข้อมูลล่าสุดตามช่วงเวลาที่กำหนดเสมอ (เช่น ใช้ข้อมูลล่าสุด 2 ปีตลอดเวลา โดยตัดข้อมูลที่เก่ากว่านั้นทิ้งไปเรื่อยๆ)
3.  **Trigger Based:** เทรนใหม่เมื่อเกิดเหตุการณ์ผิดปกติ (เช่น Accuracy ลดลง, Profit Factor ลดลง, ค่า PSI Drift สูง)

---

## 🚀 Model Promotion Process (การนำโมเดลขึ้นใช้งานจริง)

**ห้าม** นำโมเดลจากขั้นตอน Research ไปใช้งานบน Production (บัญชีเงินจริง) โดยตรงเด็ดขาด!

**ขั้นตอนที่ถูกต้อง (Must Follow):**
1.  **Research:** ค้นคว้าและสร้างโมเดลเริ่มต้น
2.  **Backtest:** ทดสอบกับข้อมูลในอดีต (ต้องระวัง Data Leakage อย่างเคร่งครัด)
3.  **Walk Forward:** ทดสอบความเสถียรของโมเดลด้วยเทคนิคการเลื่อนหน้าต่างเวลา (Rolling Window)
4.  **Paper Trade (Forward Test):** ทดสอบเทรดด้วยเงินจำลอง (Demo Account) ในสภาวะตลาดจริง (Live Market)
5.  **Production:** นำไปใช้งานจริง (ต้องมีระบบ Monitor กำกับเสมอ)
