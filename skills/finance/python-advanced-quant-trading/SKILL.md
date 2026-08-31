---
name: python-advanced-quant-trading
description: Advanced Python libraries for Candlestick pattern recognition, Price Action (Support/Resistance), Statistical indicators, and Strategy Performance metrics.
---
# Advanced Quantitative Trading Libraries in Python

While `pandas-ta` covers standard technical indicators (SMA, RSI, MACD), advanced algorithmic trading requires detecting visual price patterns, mathematical price action, statistical properties, and measuring portfolio performance. This skill covers the specialized libraries for these tasks.

## 1. Candlestick Pattern Recognition (`TA-Lib` & `pandas-ta`)
To detect classic Japanese candlestick patterns (Doji, Engulfing, Hammer).

### Using `TA-Lib` (The Industry Standard for Patterns)
TA-Lib has over 60 built-in pattern recognition functions. It returns `100` (Bullish pattern), `-100` (Bearish pattern), or `0` (No pattern).
```python
import talib
import pandas as pd

# Detect specific patterns
df['Engulfing'] = talib.CDLENGULFING(df['Open'], df['High'], df['Low'], df['Close'])
df['Doji'] = talib.CDLDOJI(df['Open'], df['High'], df['Low'], df['Close'])
df['Hammer'] = talib.CDLHAMMER(df['Open'], df['High'], df['Low'], df['Close'])
```

### Using `pandas-ta` (If TA-Lib is hard to install)
```python
import pandas_ta as ta
# Detect all available candlestick patterns at once
patterns = df.ta.cdl_pattern(name="all")
df = pd.concat([df, patterns], axis=1)
```

## 2. Price Action: Support, Resistance & Pivot Points (`scipy`)
True price action trading relies on finding local highs and lows (peaks and troughs) rather than lagging indicators. We use mathematical signal processing for this.

**Library: `scipy.signal`**
```python
import numpy as np
from scipy.signal import argrelextrema

# Find Local Maxima (Resistance) and Minima (Support) over a 20-candle window
order = 20 

# Minima (Support)
df['Support'] = df.iloc[argrelextrema(df['Low'].values, np.less_equal, order=order)[0]]['Low']

# Maxima (Resistance)
df['Resistance'] = df.iloc[argrelextrema(df['High'].values, np.greater_equal, order=order)[0]]['High']
```

## 3. Statistical Trading & Cointegration (`statsmodels`)
Used for Mean Reversion strategies, Pair Trading (Statistical Arbitrage), and testing if a market is trending or ranging.

**Library: `statsmodels`**
```python
from statsmodels.tsa.stattools import adfuller, coint

# 1. ADF Test (Stationarity Check)
# If p-value < 0.05, the asset is ranging (mean-reverting). If > 0.05, it is trending.
result = adfuller(df['Close'])
print(f"p-value: {result[1]}")

# 2. Cointegration Test (For Pair Trading e.g., PTT vs PTTEP)
# If p-value < 0.05, the two assets move together and can be pair-traded.
score, pvalue, _ = coint(df_asset1['Close'], df_asset2['Close'])
```

## 4. Strategy Performance & Analytics (`quantstats`)
Once you backtest a strategy, you must measure its quality. `quantstats` generates institutional-grade tear sheets (Sharpe ratio, max drawdown, win rate) from a simple Pandas series of daily returns.

**Library: `quantstats`**
- Install: `pip install quantstats`
```python
import quantstats as qs

# Assume 'strategy_returns' is a Pandas Series of daily percentage returns (e.g., 0.01 for 1%)
# Calculate specific metrics
sharpe = qs.stats.sharpe(strategy_returns)
max_dd = qs.stats.max_drawdown(strategy_returns)
win_rate = qs.stats.win_rate(strategy_returns)

# Generate a full HTML report (Tear Sheet)
qs.reports.html(strategy_returns, output='strategy_report.html', title='My Trading Strategy')
```

## 5. Agent Instructions
- **For Pattern Recognition:** Prefer `TA-Lib` if it is installed, as it is highly optimized in C. Fall back to `pandas-ta` if `TA-Lib` is unavailable.
- **For AI/ML Features:** Candlestick patterns return -100, 0, or 100. Normalize these values to -1, 0, 1 before feeding them into Neural Networks or classification models.
- **For Support/Resistance:** Always use `scipy.signal.argrelextrema`. Remember that pivot points look into the past (they are confirmed *after* they form). Ensure you don't introduce look-ahead bias if feeding pivots to an ML model.