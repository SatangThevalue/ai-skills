---
name: python-mean-reversion-backtesting
description: "แนวทางและแหล่งอ้างอิงสำหรับการทำ Backtest กลยุทธ์ Mean Reversion บน Python"
version: 0.1.0
metadata:
  hermes:
    tags: [Python, Backtest, Mean Reversion, Algorithmic Trading, QuantifiedStrategies]
---

# Backtesting Mean Reversion in Python

สกิลนี้สรุปแนวคิด ข้อจำกัด และแหล่งข้อมูลอ้างอิงที่จำเป็นสำหรับการเขียนโค้ด Backtest (ทดสอบย้อนหลัง) กลยุทธ์ Mean Reversion ด้วยภาษา Python โดยอิงจากงานวิจัยเชิงปริมาณ (Quantitative Research)

## When to Use

- "ช่วยหาข้อมูลมาทดสอบ backtest ได้ไหม โดยใช้ข้อมูลจาก python"
- "จะเขียนโค้ด Python แบคเทสกลยุทธ์ Mean Reversion"
- เมื่อผู้ใช้ต้องการรู้ข้อดี/ข้อเสียของการรัน Backtest กลยุทธ์สวนเทรนด์

## Quick Reference

- **Library แนะนำ:** `Backtrader` (ยืดหยุ่นสูง) หรือการจำลองด้วย `Pandas` (Vectorized Backtesting)
- **ตัวแปรชี้วัด (Metrics):** วิเคราะห์ค่า Win Rate (ควรสูง) เทียบกับ Max Drawdown (อาจลงลึก)
- **ปัญหาคลาสสิก:** The Stop-Loss Paradox (การตั้ง Stop loss มักทำให้ผล Backtest แย่ลง)

## สาระสำคัญจากวิจัยสาย Quant (QuantifiedStrategies)

นักพัฒนาระบบ Algorithmic ต้องเข้าใจธรรมชาติของ Mean Reversion ก่อนนำไปเขียนโค้ด Backtest:

1. **The Stop-Loss Paradox (จุดอ่อนของ Stop Loss):**
   - งานวิจัยสาย Quant ชี้ว่า **ในกลยุทธ์ Mean Reversion ยิ่งตั้ง Stop loss แคบ ผล Backtest ยิ่งแย่** 
   - เหตุผล: เพราะถ้าราคายิ่งลง (หลุดกรอบมากขึ้น) สัญญาณทางสถิติจะยิ่งบอกว่า "มันถูกเกินไปแล้ว" (Better Signal) การตัดขายทิ้งจึงเป็นการตัดโอกาสเด้งกลับ 
   - *คำแนะนำในการเขียนโค้ด:* ให้ทดสอบ (Optimize) ระหว่างการไม่มี Stop Loss เลย (ทนลาก) กับการตั้ง Stop Loss ที่กว้างมากๆ (Wide Stop) และต้องใช้ Time-based Exit (เช่น ปิดออเดอร์เมื่อผ่านไป N แท่ง)

2. **Negative Skew (กำไรบ่อย แต่เสียหนัก):**
   - ผล Backtest จะโชว์ Win Rate ที่สูงมาก (เช่น 70-80%) แต่กำไรต่อไม้จะน้อย 
   - ตอนขาดทุน 1 ไม้ อาจจะล้างกำไรของ 10 ไม้ที่ผ่านมาได้ ดังนั้น บอทจะต้องมี Position Sizing ที่เล็กมาก (เช่น เทรดแค่ 1-2% ของพอร์ต)

3. **ตลาดที่ควรนำไป Backtest:**
   - ได้ผลดีเยี่ยม: **ตลาดหุ้น (Equities / Indices)** ในระยะสั้น (Short-term)
   - ไม่ค่อยได้ผล: **Forex และ Commodities** (มักจะวิ่งเป็นเทรนด์ยาวๆ)
   - *Note:* หากต้องการใช้กับ Forex ต้องทดสอบบน Timeframe สั้นมากๆ หรือมีตัวกรองสภาพตลาดที่แข็งแกร่ง (เช่น กรองด้วย ADX)

## โครงสร้างการเขียน Backtest บน Python (ด้วย Pandas)

ตัวอย่างสถาปัตยกรรมโค้ด (Vectorized Backtest) อย่างง่าย เพื่อหาจุดเข้าและออก:

```python
import pandas as pd
import yfinance as yf
import numpy as np

# 1. โหลดข้อมูล
df = yf.download('EURUSD=X', start='2020-01-01', end='2024-01-01', progress=False)
if isinstance(df.columns, pd.MultiIndex):
    df.columns = df.columns.droplevel(1)

# 2. คำนวณ Indicators (Bollinger Bands)
window = 20
df['SMA'] = df['Close'].rolling(window).mean()
df['STD'] = df['Close'].rolling(window).std()
df['Upper'] = df['SMA'] + (2 * df['STD'])
df['Lower'] = df['SMA'] - (2 * df['STD'])

# 3. สร้าง Signals (1=Buy, -1=Sell)
df['Signal'] = 0
df.loc[df['Close'] < df['Lower'], 'Signal'] = 1   # Oversold -> Buy
df.loc[df['Close'] > df['Upper'], 'Signal'] = -1  # Overbought -> Sell
# Exit signal (Mean reversion)
df.loc[((df['Close'] > df['SMA']) & (df['Signal'].shift(1) == 1)) | 
       ((df['Close'] < df['SMA']) & (df['Signal'].shift(1) == -1)), 'Signal'] = 0

# 4. Forward Fill Position (ถือออเดอร์จนกว่าจะเปลี่ยน)
df['Position'] = df['Signal'].replace(0, np.nan).ffill()

# 5. คำนวณกำไร (Returns)
df['Daily_Return'] = df['Close'].pct_change()
df['Strategy_Return'] = df['Position'].shift(1) * df['Daily_Return']

# 6. ประเมินผล (Cumulative)
cumulative_return = (1 + df['Strategy_Return'].fillna(0)).cumprod() - 1
print(f"Total Return: {cumulative_return.iloc[-1]:.2%}")
```

## Pitfalls (สิ่งที่ต้องระวังตอนทำ Backtest)

- **Survivorship Bias:** การดึงข้อมูลหุ้นเฉพาะที่ยังมีชีวิตอยู่ในปัจจุบันมาเทรนโมเดล ทำให้บอทดูเก่งกว่าความเป็นจริง เพราะมองไม่เห็นหุ้นที่ล้มละลายหรือถูกเพิกถอนไปแล้ว
- **Curve-Fitting (Overfitting):** การปรับค่า Parameter ของ Indicator (เช่น หาเส้นค่าเฉลี่ยที่ดีที่สุดเป๊ะๆ บนข้อมูลในอดีต) ทำให้เวลาไปรันบน Live Market จริงๆ แล้วบอทพังทันที (ต้องทำ Out-of-Sample Testing เสมอ)
- **Slippage & Commission:** กลยุทธ์ Mean Reversion / Scalping ซื้อขายถี่มาก หากโค้ด Backtest ไม่หักค่า Commission และ Spread ต่อออเดอร์ ผลลัพธ์ที่ได้จะเป็นการหลอกตัวเอง (Illusion of Profitability)

## Verification
- กราฟ Equity Curve ของ Backtest กลยุทธ์นี้ มักจะมีลักษณะค่อยๆ ไต่ขึ้นเป็นขั้นบันไดเล็กๆ และมีการร่วงลงลึกเป็นบางครั้ง (Negative Skew) หากกราฟพุ่งขึ้นเป็นเส้นตรงสมบูรณ์ ให้ตรวจสอบว่ามี Look-ahead bias (แอบดูราคาอนาคต) ในโค้ดหรือไม่