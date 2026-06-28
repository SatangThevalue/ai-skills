---
name: mt5-python-trading
description: Guide and best practices for automated trading using Python and MetaTrader 5 (MT5), including Linux workarounds.
---
# Python MetaTrader 5 (MT5) Integration

## Core Constraints & Environment (CRITICAL)
The official `MetaTrader5` Python module is **Windows-only**. Since you often deploy on Ubuntu (VPS):
1. **Local Windows Development:** Use the official `MetaTrader5` package directly.
2. **Linux VPS Deployment Workarounds:**
   - **ZeroMQ Bridge (Recommended for Prod):** Write an MQL5 Expert Advisor using `ZeroMQ` to run on a Windows VPS/Desktop MT5, then connect your Linux Python agent (using `pyzmq`) via TCP.
   - **mt5linux:** A Python package (`pip install mt5linux`) that uses `rpyc` to bridge your Linux Python script to a Windows machine running MT5.
   - **Wine:** Run both MT5 and Python Windows binaries via Wine on Ubuntu.

## 1. Windows Implementation (Official Lib)

### Installation
```bash
pip install MetaTrader5 pandas datetime pytz
```

### Initialization & Login
```python
import MetaTrader5 as mt5
import pandas as pd

# Connect to MT5 Terminal
if not mt5.initialize():
    print("initialize() failed, error code =", mt5.last_error())
    quit()

# Login to account
account = 12345678
password = "YOUR_PASSWORD"
server = "Broker-Server"

authorized = mt5.login(account, password=password, server=server)
if not authorized:
    print("Login failed, error code:", mt5.last_error())
```

## 2. Fetching Market Data (Rates & Ticks)
```python
from datetime import datetime
import pytz

# Set time zone to UTC
timezone = pytz.timezone("Etc/UTC")
utc_from = datetime.now(timezone)

symbol = "XAUUSD"
# Ensure symbol is visible in Market Watch
mt5.symbol_select(symbol, True)

# Get 1000 M15 candles
rates = mt5.copy_rates_from(symbol, mt5.TIMEFRAME_M15, utc_from, 1000)
rates_frame = pd.DataFrame(rates)
rates_frame['time'] = pd.to_datetime(rates_frame['time'], unit='s')
print(rates_frame.tail())
```

## 3. Order Execution (Market Buy Example)
```python
symbol = "XAUUSD"
lot = 0.01

point = mt5.symbol_info(symbol).point
price = mt5.symbol_info_tick(symbol).ask
deviation = 20

request = {
    "action": mt5.TRADE_ACTION_DEAL,
    "symbol": symbol,
    "volume": lot,
    "type": mt5.ORDER_TYPE_BUY,
    "price": price,
    "sl": price - 100 * point,
    "tp": price + 100 * point,
    "deviation": deviation,
    "magic": 234000,
    "comment": "python script open",
    "type_time": mt5.ORDER_TIME_GTC,
    "type_filling": mt5.ORDER_FILLING_IOC, # Change if broker rejects
}

# Send order
result = mt5.order_send(request)
if result.retcode != mt5.TRADE_RETCODE_DONE:
    print("Order send failed, retcode:", result.retcode)
else:
    print("Order executed successfully:", result.order)
```

## 4. Closing Positions
To close a position, you must send an opposite order (e.g., SELL to close a BUY) and specify the original `position` ticket ID.

```python
close_request = {
    "action": mt5.TRADE_ACTION_DEAL,
    "symbol": symbol,
    "volume": lot,
    "type": mt5.ORDER_TYPE_SELL,
    "position": result.order, # The ticket of the position to close
    "price": mt5.symbol_info_tick(symbol).bid,
    "deviation": deviation,
    "magic": 234000,
    "comment": "python script close",
    "type_time": mt5.ORDER_TIME_GTC,
    "type_filling": mt5.ORDER_FILLING_IOC,
}
mt5.order_send(close_request)
```

## Pitfalls & Best Practices
- **`type_filling`:** Brokers support different filling policies (`ORDER_FILLING_FOK`, `ORDER_FILLING_IOC`, `ORDER_FILLING_RETURN`). If `order_send` fails with "Unsupported filling mode", try changing this parameter.
- **Auto-Trading Button:** The "Algo Trading" button must be enabled in the MT5 terminal.
- **Symbol Selection:** Always call `mt5.symbol_select(symbol, True)` before requesting data or trading. If it's hidden in Market Watch, API calls will return `None`.
- **Latency:** Direct Python->MT5 is fast locally. If using ZeroMQ between VPS instances, use PUB/SUB for tick data and REQ/REP for trade execution.