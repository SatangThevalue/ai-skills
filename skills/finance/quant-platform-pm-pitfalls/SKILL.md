---
name: quant-platform-pm-pitfalls
description: "รวม 15 ข้อควรระวัง (Pitfalls) ที่ PM และ Quant Architect มักพลาดเมื่อสร้างระบบ AI Trading ระดับ Production"
---

# 15 ข้อผิดพลาดที่ต้องระวังในการสร้าง Quant Platform

เอกสารนี้รวบรวม 15 ข้อเตือนใจ (Pitfalls) จากมุมมองของ MLOps Architect และ Quant PM เพื่อป้องกันไม่ให้โครงการ AI Trading ล้มเหลวเมื่อนำไปรันบนระบบจริง (Production)

---

## 🛑 หมวดที่ 1: แนวคิดที่ผิดพลาดเกี่ยวกับการทำโมเดล (Mindset & Metrics)

**1. ทุ่มเทเวลาให้โมเดลมากเกินไป**
- ความเชื่อ: โมเดลดี = กำไรดี (ใช้เวลา 80% กับ LightGBM, LSTM)
- ความจริง: การทำกำไรจริงเกิดจาก Risk Engine (30%) + Execution (20%) + Feature Eng (20%) + Model (20%) + Sizing (10%)

**2. วัดผลความสำเร็จด้วย Accuracy**
- หลายคนหลงดีใจกับ Accuracy 65% แต่กลับเทรดขาดทุน 
- KPI ที่ถูกต้องคือ: `Profit Factor`, `Sharpe Ratio`, `Max Drawdown`, `Expected Value`

**3. เข้าใจว่าตลาดการเงินคือ IID Data**
- Machine Learning ทั่วไปคิดว่า อดีต = อนาคต แต่ความจริงตลาดคือ Non-Stationary, Adaptive, Dynamic
- สิ่งที่ขาดไม่ได้คือ: `Walk Forward Testing`, `Drift Detection`, `Retraining`

**4. Data Leakage (Killer อันดับ 1)**
- การปล่อยให้ข้อมูลอนาคตหลุดเข้ามารวมตอนทำ Feature (เช่น เผลอใช้ `rolling_mean.shift(-1)`)
- ผลลัพธ์: Backtest สวยหรูระดับเทพ แต่เทรด Live พังทันที

---

## 🗂️ หมวดที่ 2: การจัดการ Data และ MLOps (Governance)

**5. ทำ Model Versioning แต่ละเลย Feature Versioning**
- โมเดลเปลี่ยนง่าย แต่โครงสร้าง Feature เปลี่ยนยาก ต้องควบคุมเวอร์ชัน Feature เสมอ (เช่น `FS_V1`, `FS_V2`)

**6. ละเลย Label Versioning**
- เป้าหมายการให้ AI เรียนรู้เปลี่ยนไปตลอดเวลา (เช่น เปลี่ยนจากทำนาย `Return > 0` เป็น `Triple Barrier`)
- ต้องเก็บ: `LB_V1`, `LB_V2` ควบคู่กับการเทรนเสมอ

**7. ขาด Feature Contract ที่เป็นเอกสารทางการ**
- ห้ามเขียนสูตรลอยๆ ต้องมี Metadata กำกับทุก Feature:
  ```json
  {"feature": "atr_ratio", "version": "1.0", "formula": "atr14/atr100", "dtype": "float32", "order": 5}
  ```

**8. ไม่สามารถทำ Backtest Reproducibility ได้**
- ผ่านไป 1 ปี ต้องตอบได้ว่า Model V3 เทรนมาได้อย่างไร
- ต้องเก็บ: `Dataset Version`, `Feature Version`, `Label Version`, `Optuna Study`, `MLflow Run`

---

## ⚙️ หมวดที่ 3: ระบบเทรดจริงและการเชื่อมต่อ MT5 (Execution & Architecture)

**9. มองข้าม Transaction Costs**
- Backtest มักโกหกเพราะลืมคำนวณ Spread, Commission, Swap, Slippage
- วิธีแก้: ต้องสร้าง **Execution Simulator** ทดสอบก่อนขึ้นระบบจริง

**10. ข้ามขั้นตอน Paper Trading**
- ระบบห้ามกระโดดจาก Research → Production เด็ดขาด
- Workflow บังคับ: `Research` ➔ `Staging` ➔ `Paper Trading` ➔ `Production`

**11. กลัวปัญหา ONNX มากกว่าปัญหา Feature Mismatch**
- ปัญหาใหญ่สุดในการต่อ Python เข้า MT5 ไม่ใช่ ONNX แต่คือ **"การคำนวณสูตรไม่ตรงกัน"** (เช่น Python รัน RSI14 แบบหนึ่ง MT5 รันอีกแบบ หรือ Python เทรนบน UTC แต่ Broker ใช้ UTC+3 ทำให้ Prediction เพี้ยน)
- **วิธีแก้:** สำหรับเรื่องเวลา ห้ามนำเวลาเข้าเป็น Feature ให้ AI หรือถ้าต้องหลบข่าว ให้ใช้ `TimeCurrent() - TimeGMT()` บน MT5 เพื่อซิงค์ Timezone อัตโนมัติ

**12. มองข้าม Market Regime**
- คนส่วนใหญ่มักอยากสร้าง "1 Model ที่เก่งทุกตลาด" ซึ่งไม่มีจริง
- Quant Fund ใช้: `Trend Model`, `Range Model`, `High Vol Model` สลับกัน ดังนั้น Regime Detection ต้องอยู่ต้นๆ ของ Roadmap

**13. สนใจ Symbol Risk แต่ลืม Portfolio Risk**
- ถ้าระบบเปิด BUY EURUSD, GBPUSD, AUDUSD พร้อมกัน ไม่ใช่กระจายความเสี่ยง 3 ไม้ แต่คือ **อมความเสี่ยงดอลลาร์ (USD Exposure) 15-20% รวดเดียว**
- ต้องมี: `Correlation Matrix` และ `Exposure Matrix` ในระดับพอร์ต

---

## 📊 หมวดที่ 4: การบำรุงรักษา (Maintenance & Logging)

**14. เก็บ Log น้อยเกินไป**
- **ทุก Prediction ต้อง Log:** Timestamp, Features, Probability, Signal, Regime, Spread, ATR, Position Size
- **ทุก Order ต้อง Log:** Entry, Exit, SL, TP, Profit, Model Version
- *(ข้อมูลเหล่านี้มีค่ามหาศาลตอนที่ต้องมานั่ง Debug หาว่าทำไมพอร์ตถึงแตก)*

**15. รีบทำ Auto Retrain เร็วเกินไป**
- หลายคนอยากได้ Self Learning AI ทันที
- Roadmap ที่ถูกต้อง: `Manual Retrain` ➔ `Scheduled Retrain` ➔ `Conditional Retrain` ➔ `Auto Retrain`

**16. Optimize ค่า Sharpe อย่างเดียว**
- Sharpe สูงไม่ได้แปลว่าดีเสมอไป ต้องดูควบคู่กับ `Profit Factor`, `Sortino`, `Drawdown`, และ `Stability` ของพอร์ต

**17. ไม่ตั้ง Risk Budget เป็น Hard Rule ตั้งแต่วันแรก**
- ห้ามใช้ความรู้สึก ควรกำหนดเพดานความเสี่ยงเป็นกฎตายตัวแต่แรก:
  - Max Trade Risk: `1%`
  - Max Daily Loss: `3%`
  - Max Drawdown: `10%`
  - Max Exposure: `20%`

**18. สร้าง Engine ไม่ครบ 4 ส่วน**
- ระบบที่สมบูรณ์ไม่ได้มีแค่โมเดลทำนาย แต่ต้องทำงานพร้อมกัน 4 แกน:
  1. `Prediction Engine` (LightGBM)
  2. `Risk Engine` (Exposure / DD)
  3. `Execution Engine` (Entry / Exit)
  4. `Portfolio Engine` (Allocation / Correlation)

**19. ลืมคำนวณ Execution Cost ทั้ง 4 ตัวเสมอ**
- PM ต้องไม่อนุมัติโมเดลหากประเมินแค่ "Profit Factor ก่อนหัก Cost" แล้วสูงปรี๊ด แต่พอรวม Cost แล้วเหลือ 1.1 
- Backtest/Walk Forward ทุกครั้งต้องคำนวณครบทั้ง 4 ส่วน: `Spread + Commission + Swap + Slippage` 
- *แนะนำ:* ให้ใช้ **Raw Spread Account** เป็นมาตรฐานอ้างอิงในการพัฒนาแพลตฟอร์ม เพราะ Spread ต่ำ, ต้นทุนคงที่, จำลอง Backtest ง่าย และเหมาะกับ AI ที่สุด

**20. ไม่คุม Exposure/Portfolio Correlation**
- `Correlation Trap:` ระบบเปิด BUY EURUSD, GBPUSD, AUDUSD พร้อมกัน ทำให้อมความเสี่ยง `Long USD Risk` สูงเกินไป ระบบต้องมี Correlation Matrix ช่วยป้องกัน
- `Over Allocation:` ทุ่มเงินลง Crypto 80% ระบบควรต้องมี Capital Allocation Rules ที่ดี

**21. Auto Retrain บ่อยและง่ายเกินไป**
- การตั้ง Auto Retrain บ่อยเกินจะเกิด `Model Oscillation` (โมเดลแกว่งไปมา)
- เงื่อนไขที่ควรกำหนด: ทริกเกอร์ Retrain ก็ต่อเมื่อ `PSI > 0.25` **และ** `Performance Drop (เช่น PF, Sharpe ร่วง)` เกิดขึ้นพร้อมกันเท่านั้น

**22. ใช้ Web Terminal Automation ในการส่งคำสั่ง (เช่น Selenium/Playwright)**
- **ห้ามทำเด็ดขาด:** การสั่งคลิกเมาส์ผ่านหน้าเว็บมีความหน่วงสูงมาก (500ms+) ทำให้เจอ Slippage รุนแรง, ขาดความเสถียร (Pop-up โฆษณาบัง), และไม่สามารถดึงค่า Spread แบบ Real-time มาเข้า Risk Engine ได้
- *ทางแก้:* ใช้ Broker API (REST/FIX) โดยตรง หรือส่งคำสั่งผ่าน MT5 EA

**23. ฝืนรัน MT5 บน Docker (Linux) เพื่อประหยัดเซิร์ฟเวอร์**
- **ห้ามทำเด็ดขาด:** MT5 ไม่ใช่ Native Linux การรันผ่าน WINE Emulator บน Docker จะกิน CPU/RAM สูงกว่าปกติ 2-3 เท่า เสี่ยงต่อการเกิด OOM (Out of Memory) และเพิ่ม Execution Latency อย่างรุนแรง
- *ทางแก้:* ยึดหลัก Separation of Concerns ให้ Linux เป็น MLOps Server และเช่า Windows VPS แยกต่างหากเพื่อเป็น Execution Node

---

## 🎯 บทสรุป 6 ความเสี่ยงใหญ่ที่สุดของโปรเจกต์ (The 6 Big Risks)

ความเสี่ยงที่ใหญ่ที่สุดของโปรเจกต์ Quant AI ไม่ใช่เรื่องเทคโนโลยี แต่คือเรื่องเหล่านี้:
1. **Data Leakage Prevention:** ข้อมูลอนาคตต้องไม่หลุดเข้ามาตอน Train
2. **Feature Contract:** โค้ดสูตรและลำดับใน Python ต้องตรงกับ MT5 100%
3. **Walk Forward Validation:** การวัดผลโมเดลที่แท้จริง ไม่ใช้ `train_test_split` แต่ต้องดูค่า `Mean` และ `Std` ของ Profit Factor ว่าโมเดลทำกำไรได้เสถียรในทุกช่วงเวลาจริงไหม *(อ่านวิธีรัน Walk Forward เชิงลึกได้ที่ `quant-walk-forward-validation`)*
4. **Risk Engine + Position Sizing:** ตัวชี้เป็นชี้ตายตอนยิงออเดอร์
5. **Drift Monitoring + Retraining Strategy:** แผนการรับมือเมื่อตลาดเปลี่ยนไป
6. **การฝืนเทรด Timeframe ปราบเซียน:** กราฟ 15m และ 30m ของสินทรัพย์ผันผวนจะเต็มไปด้วย Noise และโดน Spread กินรวบ การจะทำกำไรได้ต้องมีกระบวนการ Alternative Data เสมอ

> หากทีมงานควบคุมความเสี่ยง 5 ข้อนี้ได้ ต่อให้ LightGBM จะมี Accuracy เพียง 55-60% ระบบที่คุณออกแบบก็จะยังมีโอกาสอยู่รอดและทำกำไรเติบโตในระยะยาวได้มากกว่า EA ทั่วไปในตลาดแน่นอนครับ