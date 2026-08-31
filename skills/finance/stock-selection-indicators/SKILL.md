---
name: "stock-selection-indicators"
description: "Framework and key indicators for systematic stock selection (Fundamental & Technical) for SET/Crypto and algorithmic trading."
category: finance
---
# Stock Selection Indicators & Framework

กรอบการคัดกรองหุ้น (Stock Screening) ที่ผสานการวิเคราะห์ปัจจัยพื้นฐาน (Fundamental) และเทคนิค (Technical) เหมาะสำหรับการเทรดอย่างเป็นระบบ (Systematic Trading) และ Algorithmic Trading

## 1. Fundamental Indicators (หา "หุ้นดี")
คัดกรองมูลค่า, ประสิทธิภาพการทำกำไร, และความเสี่ยงทางการเงิน

*   **P/E Ratio (Price-to-Earnings):** วัดความถูกแพง 
    *   *Rule:* P/E < 15 หรือ ต่ำกว่าค่าเฉลี่ยอุตสาหกรรม
*   **P/BV (Price-to-Book Value):** มูลค่าหุ้นเทียบกับมูลค่าทางบัญชี 
    *   *Rule:* < 1.5 - 2.0 (เหมาะกับสแกนหุ้น Value)
*   **ROE (Return on Equity):** ประสิทธิภาพการบริหารทุน 
    *   *Rule:* ROE > 15% ต่อเนื่อง แสดงถึงบริษัทที่นำเงินผู้ถือหุ้นไปสร้างกำไรได้เก่ง
*   **D/E Ratio (Debt-to-Equity):** ภาระหนี้สินต่อทุน 
    *   *Rule:* D/E < 1.5 - 2.0 (คัดบริษัทที่หนี้สูง/ความเสี่ยงล้มละลายช่วงวิกฤต)
*   **Dividend Yield:** ผลตอบแทนเงินปันผล 
    *   *Rule:* > 4-5% (ช่วยลดความเสี่ยงด้าน Downside)
*   **EPS Growth (Earnings Per Share Growth):** การเติบโตของกำไรต่อหุ้น 
    *   *Rule:* เติบโตต่อเนื่อง > 10-20% YoY

## 2. Technical Indicators (หา "จังหวะซื้อขาย / Trend")
จับจังหวะ (Timing) ยืนยันแนวโน้ม และหาโมเมนตัม

*   **EMA (Exponential Moving Average):**
    *   *Golden Cross:* EMA 50 ตัด EMA 200 ขึ้น (สัญญาณเข้าซื้อขาขึ้นรอบใหญ่)
    *   *Uptrend Validation:* ราคา > EMA 50 > EMA 200
*   **RSI (Relative Strength Index):**
    *   *Oversold (หาจุดเด้ง/สะสม):* RSI < 30
    *   *Momentum (เก็งกำไรตามน้ำ):* RSI > 50-60
*   **MACD (Moving Average Convergence Divergence):**
    *   *Bullish:* MACD ตัด Signal Line ขึ้น และอยู่เหนือเส้น 0 (Zero Line)
*   **Volume & Price Action:**
    *   *Breakout:* ราคาทะลุแนวต้านพร้อมปริมาณการซื้อขาย (Volume) ที่มากกว่าค่าเฉลี่ย 5-10 วันอย่างมีนัยสำคัญ

## 3. Screening Strategies (สูตรสแกนหุ้นยอดฮิต)

1. **Value & Dividend (สายคุณค่าปันผล):** 
   `PE < 15` AND `PBV < 1.5` AND `ROE > 10%` AND `Div > 5%`
2. **Growth & Momentum (สายเติบโตตามรอบ):** 
   `EPS Growth > 20%` AND `ราคา > EMA 50` AND `RSI > 55` AND `MACD > 0`
3. **Mean Reversion (สายย่อซื้อเล่นรอบ):** 
   `RSI < 30` (Oversold) AND `ราคาแตะแนวรับ/ขอบล่าง Bollinger Bands` AND `MACD Histogram วกกลับ`

## 4. Algorithmic Implementation (Python / pandas-ta)
เหมาะสำหรับใช้ประกอบกับ `SETTRADE API`

```python
import pandas as pd
import pandas_ta as ta

# คำนวณ Indicators เชิงเทคนิค
df.ta.ema(length=50, append=True)
df.ta.ema(length=200, append=True)
df.ta.macd(fast=12, slow=26, signal=9, append=True)
df.ta.rsi(length=14, append=True)

# สร้างเงื่อนไข (Condition) กรองหุ้น Momentum ขาขึ้น
is_uptrend = (df['EMA_50'] > df['EMA_200']) & (df['RSI_14'] > 50) & (df['MACD_12_26_9'] > 0)
```

## Pitfalls & Warnings
1. **Sector Bias:** ห้ามเทียบ P/E หรือ D/E ข้ามกลุ่มอุตสาหกรรมเด็ดขาด (เช่น แบงก์ ไม่สามารถเทียบ P/E กับกลุ่มเทคโนโลยีได้)
2. **Lagging Indicators:** MACD และ EMA เป็นตัวชี้วัดตามหลังราคา (Lagging) อาจทำให้เข้าช้ากว่าจุดกลับตัวจริง
3. **Market Sentiment:** ถ้าระบบตลาด (SET Index) เป็นขาลงรุนแรง (Systematic Risk) หุ้นที่เบรคเอาท์มักเป็น False Breakout ควรลด Position Sizing ลง