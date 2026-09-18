---
name: python-multi-asset-quant-trading
description: Frameworks, libraries, and mathematical constraints for quantitative trading across all major asset classes (Crypto, Forex, Equities, Options/Futures).
---
# Multi-Asset Quantitative Trading in Python

**Asset-Specific Modeling and Alpha Strategies:**
1. **Fiat Stable (EURUSD / USDCHF)**: Best suited for Mean-Reversion and standard Trend (RSI, Bollinger, EMA Gaps). Perform best on D1 and 4H timeframes.
2. **Fiat Whipsaw (GBPUSD / USDJPY)**: Susceptible to central bank intervention. Use Night Scalping (Asian Session Mean-Reversion) or Macro Yield Spreads (e.g. trading JPY when it deviates strongly from US10Y yields).
3. **Gold (XAUUSD)**: Very high noise. Standard indicators fail. Use Volatility Breakout (Stop Orders), Time-Based Exits, or Hidden Markov Models (HMM) to trade only during specific volatility regimes. Hard requirement: News Filter (ForexFactory).
4. **Crypto (BTCUSD)**: Prone to Stop Hunting and Liquidation Cascades. Avoid fixed risk (1%). Use Asymmetric Triple Barrier (Wide TP like 4.0 ATR, Tight SL 1.5 ATR), Volatility Target Sizing, and Alternative Data (Binance Funding Rates / Level 2 Orderbook).

Trading a cryptocurrency is mathematically and structurally different from trading a stock, a forex pair, or an options contract. A robust Quant AI must understand market hours, tick sizes, leverage mechanics, and the specific Python libraries used for each asset class.

## 1. Asset Class Characteristics & Libraries

### A. Cryptocurrencies (Spot & Perpetuals)
- **Characteristics:** 24/7/365 markets, high volatility, fractional sizing (e.g., buying 0.0001 BTC). For Perpetuals (Futures), you must account for **Funding Rates** (fees paid between longs and shorts).
- **Primary Library:** **`ccxt`** (CryptoCurrency eXchange Trading Library).
  - *Why:* It connects to 100+ exchanges (Binance, OKX, Bybit) using a single unified API.
  ```python
  import ccxt
  exchange = ccxt.binance({'apiKey': 'YOUR_KEY', 'secret': 'YOUR_SECRET'})
  # Fetch OHLCV data
  bars = exchange.fetch_ohlcv('BTC/USDT', timeframe='1h', limit=100)
  # Place order
  order = exchange.create_market_buy_order('BTC/USDT', 0.01) # Amount in BTC
  ```

### B. Forex (Foreign Exchange)
- **Characteristics:** 24/5 markets. Traded in "Lots" (Standard = 100,000 units, Micro = 1,000 units). Profits are calculated in "Pips" (usually the 4th decimal place, e.g., 0.0001). High leverage is standard.
- **Primary Library:** **`MetaTrader5`** (MT5) or `OANDA-REST-V20`.
  - *Why:* MT5 is the global standard for retail Forex brokers (Exness, IC Markets). The Python MT5 library allows direct memory access to the terminal.
  ```python
  import MetaTrader5 as mt5
  mt5.initialize()
  # Requesting tick data or sending orders requires strict dictionary structures
  request = {
      "action": mt5.TRADE_ACTION_DEAL,
      "symbol": "EURUSD",
      "volume": 0.1, # 0.1 Lots = 10,000 units
      "type": mt5.ORDER_TYPE_BUY,
      "price": mt5.symbol_info_tick("EURUSD").ask,
      "sl": 1.0500,
      "tp": 1.0700,
  }
  mt5.order_send(request)
  ```

### C. Equities (Stocks & ETFs)
- **Characteristics:** Strict market hours (e.g., 9:30 AM - 4:00 PM EST). Subject to overnight gaps. Data must account for Corporate Actions (Stock Splits, Dividends). 
- **Primary Libraries:** 
  - *Data:* **`yfinance`** (Free Yahoo Finance data) or `alpaca-trade-api`.
  - *Execution:* **`ib_insync`** (Interactive Brokers - professional standard) or **Settrade Open API** (for Thai Stocks).
  ```python
  import yfinance as yf
  # Always use 'Adj Close' to account for stock splits and dividends in backtesting
  df = yf.download('AAPL', start='2020-01-01', end='2023-01-01')
  ```

### D. Derivatives (Options & Futures)
- **Characteristics:** They have an Expiration Date (Decay / Theta) and a Strike Price. Each contract has a Multiplier (e.g., 1 US Stock Option = 100 shares). 
- **Primary Libraries:**
  - *Pricing & Greeks:* **`py_vollib`** (calculates Implied Volatility, Delta, Gamma, Theta, Vega using Black-Scholes/Binomial models).
  - *Strategy visualization:* **`opstrat`**.
  ```python
  import py_vollib.black_scholes.greeks.analytical as greeks
  # Calculate Delta of a Call option
  delta = greeks.delta('c', S=150, K=155, t=30/365, r=0.05, sigma=0.2)
  ```

## 2. Unifying the Math (The Quant Challenge)
If you build a bot that trades *both* Crypto and Stocks, you cannot hardcode order sizes. You must standardize sizing using **Position Sizing based on Risk (ATR or % of Equity)**.

**Universal Position Sizing Formula:**
```python
# Risk 1% of a $10,000 portfolio = $100 Risk per trade
risk_amount = account_balance * 0.01 

# Distance from Entry to Stop Loss determines the size
stop_loss_distance = entry_price - stop_loss_price 

# Position size (Units to buy)
# For Stocks: Number of shares
# For Crypto: Fractions of a coin
# For Forex: Calculate against pip value
position_size = risk_amount / stop_loss_distance 
```

## 3. Agent Instructions
- **Timezones:** NEVER ignore timezones. Stock APIs often return local exchange time (e.g., EST for US, ICT for Thai), while Crypto APIs return UTC. Always standardize backtest data to UTC (`df.tz_convert('UTC')`).
- **Data Integrity:** When backtesting Equities, ALWAYS use the `Adjusted Close` price to calculate returns, otherwise historical stock splits (e.g., Tesla 5-for-1 split) will look like an 80% price crash to the algorithm.
- **Crypto Futures:** If coding for Crypto Perpetuals, explicitly state `exchange.options['defaultType'] = 'future'` in `ccxt`. Spot and Futures have completely different API endpoints and margin rules.
- **Forex MT5:** `MetaTrader5` library functions often fail silently and return `None`. Always check `mt5.last_error()` after sending an order.