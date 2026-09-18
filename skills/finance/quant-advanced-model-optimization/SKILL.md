---
name: quant-advanced-model-optimization
description: "เทคนิคขั้นสูง (Meta-Labeling, VolTarget, FracDiff) เพื่อแก้ปัญหาโมเดลขาดทุนในทองคำ บิทคอยน์ และกราฟ 15m"
---

# Advanced Model Optimization (The Underperformer Solutions)

เอกสารฉบับนี้รวบรวมงานวิจัยทาง Quantitative Finance ขั้นสูง (อ้างอิงจากงานของ Marcos Lopez de Prado และ Institutional Quant Funds) เพื่อนำมาแก้ปัญหาเฉพาะจุดให้กับ Asset หรือ Timeframe ที่สอบตกจาก Baseline Model ปกติ

---

## 1. วิธีแก้ปัญหา GOLD (XAUUSD)
**ปัญหา:** Noise ระหว่างวันสูงมาก, False Breakout เยอะ, ชอบทำ Spike ล่า Stop Loss
**Solutions (เทคนิคที่ควรใช้):**
1. **Fractional Differencing (FracDiff):** การแปลงข้อมูลแบบปกติ (เช่น Percent Return) จะทำลาย Memory (ความจำ) ของเทรนด์ทิ้งไปหมด ทองคำเป็นสินทรัพย์ที่มีความจำยาว ให้ใช้ FracDiff (ค่า d=0.4) เพื่อคงสภาพเทรนด์ไว้แต่ทำให้ข้อมูล Stationary
2. **Hidden Markov Model (HMM) Regime Filter:** สร้างโมเดล HMM แยกสภาวะ "ระเบิด (Breakout)" กับ "สะสมพลัง (Consolidation)" หาก HMM บอกว่ากำลังสะสมพลัง ให้บล็อกคำสั่ง Buy/Sell ทั้งหมด
3. **Volume-Synchronized Probability (VPIN):** ราคาหลอกได้ แต่ Volume หลอกไม่ได้ ใน MT5 ให้ดึง Tick Volume มาจับความผิดปกติของแรงซื้อขายก่อนราคาจะพุ่งจริง

## 2. วิธีแก้ปัญหา BTC (Bitcoin / Crypto)
**ปัญหา:** ความผันผวนสุดขั้ว (Extreme Fat Tails), Max Drawdown -80% พอร์ตแหว่ง
**Solutions (เทคนิคที่ควรใช้):**
1. **Volatility Target Sizing (VolTarget):** ห้ามใช้สูตร Risk = 1% แบบตายตัวเด็ดขาด สำหรับคริปโตต้องคำนวณ "Target Volatility" (เช่น คุมความแกว่งไม่เกิน 20% ต่อปี) ถ้าช่วงไหน BTC วิ่งแรง ATR สูงปรี๊ด ระบบต้อง "หั่น Lot Size ลง 3-5 เท่า" อัตโนมัติ (Inverse Volatility Sizing)
2. **Asymmetric Triple Barrier:** คริปโตมักจะวิ่งเป็นเทรนด์ยาวมาก (Trend Following) ไม่ควรตั้ง Take Profit กับ Stop Loss เท่ากัน ควรตั้ง TP = 3.0 ATR และ SL = 1.0 ATR เพื่อกินกำไรคำใหญ่ชดเชยเวลาที่โดน Whipsaw
3. **Funding Rate & Open Interest Features:** Price Action อย่างเดียวจับคริปโตไม่อยู่ ต้องดึงข้อมูล Market Microstructure (เช่น Funding Rate ของ Binance) มาเป็น Feature ให้ LightGBM

## 3. วิธีแก้ปัญหา Timeframe 15 นาที (15m)
**ปัญหา:** โดนค่า Spread กินรวบเกลี้ยง (Transaction Cost Ruins Alpha), สัญญาณหลอกเยอะเกินไป
**Solutions (เทคนิคที่ควรใช้):**
1. **Meta-Labeling (ท่าไม้ตายของ Lopez de Prado):**
   - *Primary Model:* รันโมเดล V1/V2 ปกติ เพื่อสร้างสัญญาณ (Buy/Sell)
   - *Secondary Model (Meta-Model):* สร้างโมเดล LightGBM อีกตัว มาเรียนรู้ว่า "สัญญาณจากตัวแรก ควรกดเทรด (1) หรือ ควรปล่อยผ่าน (0)" 
   - *ผลลัพธ์:* ลดจำนวนการเทรดจาก 1,000 ไม้ เหลือแค่ 200 ไม้ที่ "ชัวร์ที่สุด" ประหยัดค่า Spread ไปได้มหาศาลและกำไรพลิกกลับมาเป็นบวก
2. **Spread-Adjusted Loss Function:** ปรับแต่ง Custom Objective ใน LightGBM ตอน Train โดยบังคับให้โมเดลลงโทษ (Penalize) สัญญาณที่ได้กำไรน้อยกว่าค่า Spread อย่างรุนแรง

## 4. วิธีแก้ปัญหา GBPUSD และ USDJPY
**ปัญหา:** Whipsaw รุนแรง, ขับเคลื่อนด้วยเศรษฐกิจมหภาค (Macro-driven) มากกว่าปัจจัยทางเทคนิค
**Solutions (เทคนิคที่ควรใช้):**
1. **Macro-Economic Features:** ต้องดึงข้อมูลอัตราผลตอบแทนพันธบัตร (เช่น US 10-Year Bond Yield vs JP 10-Year Bond Yield) และ Interest Rate Spreads มาประกอบเป็น Feature หลัก
2. **Statistical Arbitrage (Cointegration):** เลิกทายทิศทาง (Directional) แต่ไปจับคู่เทรด Pair Trading แทน เช่น หาคู่ที่มี Cointegration กับ GBPUSD แล้วเปิด Hedge Buy/Sell พร้อมกันเพื่อกินส่วนต่าง (Spread Convergence)

See `references/advanced_optimization.md` for a detailed breakdown of these techniques.

*See `references/intraday-noise-handling.md` for a technical breakdown of applying fractional differencing, asymmetric barriers, and meta-labeling to rescue intraday strategies.*

---
**บทสรุปสำหรับ Quant Builder:**
โมเดลกลุ่มที่สอบตก ไม่ใช่เพราะ LightGBM ไม่เก่ง แต่เป็นเพราะเราใช้ "เครื่องมือผิดประเภทกับนิสัยของสินทรัพย์" การอัปเกรดระบบเพื่อ Asset เหล่านี้ จะเป็นก้าวต่อไปในการพัฒนาเป็น **V3 Architecture**