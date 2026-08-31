---
name: backtesting-py-mean-reversion
description: "วิธีเขียนโค้ดและทำ Optimization กลยุทธ์ Mean Reversion ด้วยไลบรารี Backtesting.py"
version: 0.1.0
metadata:
  hermes:
    tags: [Python, Backtest, Mean Reversion, Algorithm, Optimization]
---

# Backtesting.py: Mean Reversion & Optimization

สกิลนี้สาธิตวิธีการใช้ไลบรารี `Backtesting.py` ซึ่งเป็นไลบรารีที่เร็วและใช้งานง่ายมากสำหรับเทรดเดอร์ Python เพื่อทดสอบย้อนหลัง (Backtest) กลยุทธ์ Mean Reversion (Bollinger Bands) รวมถึงการทำ **Parameter Optimization** เพื่อให้ระบบค้นหาค่าที่ดีที่สุดให้เราอัตโนมัติ

## When to Use

- "ช่วยโหลดข้อมูล มาทำการ https://kernc.github.io/backtesting.py/ ได้ไหม?"
- เมื่อผู้ใช้ต้องการทดสอบระบบเทรด หรือหาค่า Parameter ที่ดีที่สุด (เช่น ควรใช้ Period เท่าไหร่)
- เมื่อต้องการสร้างโมเดล Backtest พื้นฐานบน Python

## Prerequisites

- ติดตั้งไลบรารี: `pip install backtesting yfinance pandas numpy bokeh`
- โหลดข้อมูลจาก Yahoo Finance (`yf.download`)

## Quick Reference

- **Library:** `from backtesting import Backtest, Strategy`
- **Indicators:** การนำเข้า Indicator ต้องใช้ฟังก์ชัน `self.I()` 
- **Optimization:** ใช้ฟังก์ชัน `bt.optimize(n=range(10, 30, 5), maximize='Return [%]')`
- **Output:** ให้ค่าสถิติที่ครบถ้วน (Win Rate, Max Drawdown, Sharpe Ratio, Profit Factor)

## Procedure (The Code Structure)

โครงสร้างการทำ Backtest และ Optimize ประกอบด้วย 4 ขั้นตอน:

### 1. โหลดข้อมูล (Data Ingestion)
ดึงข้อมูลและทำความสะอาด DataFrame (ไลบรารีนี้ต้องการ Column ชื่อ Open, High, Low, Close ตัวพิมพ์ใหญ่)
```python
import pandas as pd
import yfinance as yf
data = yf.download('EURUSD=X', start='2020-01-01', end='2024-01-01')
if isinstance(data.columns, pd.MultiIndex):
    data.columns = data.columns.droplevel(1)
```

### 2. กำหนด Indicators แบบ Vectorized
สร้างฟังก์ชันสำหรับคำนวณ Indicator ข้างนอกคลาส Strategy 
```python
def SMA(array, n): 
    return pd.Series(array).rolling(n).mean()
def BB_LOWER(array, n, dev): 
    return pd.Series(array).rolling(n).mean() - (pd.Series(array).rolling(n).std() * dev)
def BB_UPPER(array, n, dev): 
    return pd.Series(array).rolling(n).mean() + (pd.Series(array).rolling(n).std() * dev)
```

### 3. เขียน Logic กลยุทธ์ (The Strategy Class)
สืบทอดคลาส `Strategy` และเขียนการตั้งค่าเริ่มต้นใน `init()` และเงื่อนไขการเทรดใน `next()`
```python
from backtesting import Backtest, Strategy

class MeanReversionBB(Strategy):
    n = 20        # Default Period
    dev = 2.0     # Default Deviation

    def init(self):
        # คำนวณ Indicator ล่วงหน้าผ่าน self.I()
        self.sma = self.I(SMA, self.data.Close, self.n)
        self.lower_bb = self.I(BB_LOWER, self.data.Close, self.n, self.dev)
        self.upper_bb = self.I(BB_UPPER, self.data.Close, self.n, self.dev)

    def next(self):
        # 1. เงื่อนไขการปิดออเดอร์ (Mean Reversion - แตะเส้นกลาง)
        if self.position.is_long and self.data.Close[-1] >= self.sma[-1]:
            self.position.close()
        elif self.position.is_short and self.data.Close[-1] <= self.sma[-1]:
            self.position.close()

        # 2. เงื่อนไขการเปิดออเดอร์
        if not self.position:
            if self.data.Close[-1] < self.lower_bb[-1]: 
                self.buy()  # ราคาถูกกว่าขอบล่าง
            elif self.data.Close[-1] > self.upper_bb[-1]: 
                self.sell() # ราคาแพงกว่าขอบบน
```

### 4. รันและ Optimize (Execution & Optimization)
สร้าง instance ของ `Backtest` พร้อมกำหนดเงินเริ่มต้นและค่าคอมมิชชั่น
```python
bt = Backtest(data, MeanReversionBB, cash=10000, commission=0.0001)

# การ Optimize หาค่า n และ dev ที่ดีที่สุด
stats = bt.optimize(
    n=range(10, 30, 5),          # ลอง Period 10, 15, 20, 25
    dev=[1.5, 2.0, 2.5, 3.0],    # ลอง Deviation 1.5 - 3.0
    maximize='Return [%]'        # เลือกตัวที่ให้ผลตอบแทนสูงสุด
)

print(stats)
print("Best Strategy:", stats._strategy)
```

## Pitfalls (ข้อควรระวัง)

- **Over-optimization:** ฟังก์ชัน `.optimize()` จะหาค่าที่ดีที่สุดจากอดีตให้คุณ ซึ่งอาจนำไปสู่อาการ Curve-fitting (เก่งแต่อดีต) ควรใช้เพื่อหา "กรอบราคา" ที่เหมาะสม มากกว่าการใช้ค่าเจาะจงที่ได้จากการ Optimize เพียงอย่างเดียว
- **Data Shape:** หากดึง yfinance เวอร์ชั่นใหม่ คอลัมน์จะเป็น MultiIndex (มีระดับบนเป็นชื่อหุ้น) ต้องลบระดับบนออก (`droplevel(1)`) ก่อนป้อนเข้า Backtesting.py
- **Trades vs Position:** Backtesting.py ป้องกันการยิงออเดอร์ซ้ำในตัว (ถ้าระบุ `self.buy()` มันจะเติม position) แต่ถ้ามี open trades เหลืออยู่ตอนกราฟหมด มันจะส่ง Warning `Some trades remain open` ซึ่งเป็นเรื่องปกติ

## Verification
- เมื่อรันโค้ด คุณควรจะเห็นสถิติต่างๆ เช่น `Return [%]`, `Max. Drawdown [%]`, และ `Win Rate [%]` 
- ในโหมด `.optimize()` จะมีแถบความคืบหน้า (Progress bar) โผล่ขึ้นมา และในตอนท้ายคุณจะเห็นค่าตัวแปรที่ดีที่สุด เช่น `MeanReversionBB(n=15,dev=2.5)`