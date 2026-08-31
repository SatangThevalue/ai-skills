---
name: python-technical-indicators
description: Comprehensive guide to implementing technical indicators in Python using pandas-ta and TA-Lib for algorithmic trading.
---
# Python Technical Indicators for Algorithmic Trading

This skill provides a comprehensive guide to implementing technical analysis (TA) indicators in Python. It focuses primarily on **`pandas-ta`** (the most pythonic and easiest to use) and **`TA-Lib`** (the industry standard for speed).

## 1. Library Selection & Installation
- **`pandas-ta` (Highly Recommended)**: Built directly on top of Pandas. Extremely easy to install and use.
  - Install: `pip install pandas_ta`
- **`TA-Lib`**: Written in C, extremely fast, but notoriously difficult to install on Windows/Mac without binaries.
  - Install (Linux): `apt-get install ta-lib && pip install TA-Lib`
- **`ta`**: A good pure-Python alternative if `pandas-ta` is unavailable.

## 2. Core Implementation (using pandas-ta)
To use `pandas-ta`, simply import it. It extends Pandas DataFrames with a `.ta` extension.
Assume `df` is a DataFrame with columns: `Open`, `High`, `Low`, `Close`, `Volume`.

```python
import pandas as pd
import pandas_ta as ta

# Load data
# df = pd.read_csv("data.csv") 
# Ensure index is datetime for best results
```

## 3. Indicator Categories & Python Code

### A. Trend Indicators (ระบุแนวโน้ม)
Used to determine the direction and strength of a trend.
- **Moving Averages (SMA, EMA, WMA)**
  ```python
  df['SMA_20'] = df.ta.sma(length=20)
  df['EMA_50'] = df.ta.ema(length=50)
  ```
- **MACD (Moving Average Convergence Divergence)**
  ```python
  # Returns MACD, Histogram, and Signal columns
  macd = df.ta.macd(fast=12, slow=26, signal=9)
  df = pd.concat([df, macd], axis=1)
  ```
- **ADX (Average Directional Index) - วัดความแข็งแกร่งของเทรนด์**
  ```python
  adx = df.ta.adx(length=14)
  df = pd.concat([df, adx], axis=1)
  ```

### B. Momentum Indicators (วัดความแกว่งและจุดกลับตัว)
Used to identify overbought or oversold conditions.
- **RSI (Relative Strength Index)**
  ```python
  df['RSI_14'] = df.ta.rsi(length=14)
  ```
- **Stochastic Oscillator**
  ```python
  stoch = df.ta.stoch(k=14, d=3, smooth_k=3)
  df = pd.concat([df, stoch], axis=1)
  ```

### C. Volatility Indicators (วัดความผันผวน)
Crucial for dynamic Stop Loss and Take Profit calculations.
- **Bollinger Bands (BBANDS)**
  ```python
  bbands = df.ta.bbands(length=20, std=2)
  df = pd.concat([df, bbands], axis=1) # Columns: BBL, BBM, BBU, BBB, BBP
  ```
- **ATR (Average True Range)** - *Best for Trailing Stops*
  ```python
  df['ATR_14'] = df.ta.atr(length=14)
  ```

### D. Volume Indicators (ปริมาณการซื้อขาย)
- **VWAP (Volume Weighted Average Price)** - *Intraday standard*
  ```python
  # Requires DateTime index
  df['VWAP'] = df.ta.vwap()
  ```
- **OBV (On-Balance Volume)**
  ```python
  df['OBV'] = df.ta.obv()
  ```

## 4. Bulk Processing (The Strategy Method)
If you want to calculate multiple indicators at once without writing them line-by-line, use `pandas-ta`'s Strategy feature.

```python
# Create a Custom Strategy
CustomStrategy = ta.Strategy(
    name="My Algo Strategy",
    description="SMA 50,200, BBANDS, RSI, MACD and Volume SMA 20",
    ta=[
        {"kind": "sma", "length": 50},
        {"kind": "sma", "length": 200},
        {"kind": "bbands", "length": 20},
        {"kind": "rsi"},
        {"kind": "macd", "fast": 8, "slow": 21},
        {"kind": "sma", "close": "volume", "length": 20, "prefix": "VOL"}
    ]
)
# Run it
df.ta.strategy(CustomStrategy)
```

## 5. Agent & AI Engineer Guidelines
1. **Handling NaNs:** Calculating indicators ALWAYS produces `NaN` (Not a Number) values at the beginning of the DataFrame (e.g., a 200-SMA will have 199 NaNs). Always use `df.dropna(inplace=True)` BEFORE passing data to Machine Learning models.
2. **Data Types:** Ensure `Open`, `High`, `Low`, `Close`, `Volume` columns are of type `float64`.
3. **Data Leakage in ML:** If calculating indicators to train ML models, compute the indicators on the *entire* dataset BEFORE splitting into Train/Test to avoid window-calculation errors at the boundary.
4. **Naming Conventions:** Use uppercase for OHLCV columns (`Open`, `High`, `Low`, `Close`, `Volume`) as `pandas-ta` defaults to recognizing these natively.