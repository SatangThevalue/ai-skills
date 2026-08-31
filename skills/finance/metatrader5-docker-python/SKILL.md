---
name: metatrader5-docker-python
description: "Run MT5 in Docker and trade via Python on Linux."
version: 0.1.0
metadata:
  hermes:
    tags: [MetaTrader5, Docker, Trading, Python, mt5linux]
---

# MetaTrader5 Docker + Python API

รันระบบ MetaTrader5 ใน Docker Container บน Linux และเชื่อมต่อผ่าน Python ด้วย library `mt5linux` ซึ่ง API เหมือน `MetaTrader5` อย่างสมบูรณ์ ครอบคลุมตั้งแต่การ Setup Container, การดึงข้อมูลตลาด (Tick, OHLCV), การส่งคำสั่งซื้อขาย, และการจัดการ Order/Position ไม่รองรับ ARM หรือ Apple Silicon.

## When to Use

- ต้องการรัน MT5 บน Linux VPS พร้อมควบคุมผ่าน Python
- ต้องการส่งคำสั่งเทรด Forex/CFD อัตโนมัติจาก Python script
- ต้องการดึงข้อมูลราคา OHLCV, Tick จาก MT5 เข้า pandas DataFrame
- ต้องการตรวจสอบ Position, Order, หรือประวัติ Deal
- บอทเทรดที่ทำงานบน Windows ต้องการ Port มายัง Linux

## Prerequisites

- Docker Engine (Intel x86/amd64 เท่านั้น — ไม่รองรับ ARM)
- Python package: `pip install mt5linux pandas pytz`
- Port `3000` (VNC UI) และ `8001` (RPyC server) ต้องเปิดไว้
- บัญชีเทรดและ Trade Server Name จากโบรกเกอร์

## How to Run

1. ใช้ `terminal` tool รัน Docker Compose ตามในส่วน Procedure
2. เปิดเบราว์เซอร์ไปที่ `http://<ip>:3000` เพื่อเข้าสู่หน้าจอ MT5 และล็อกอินด้วยบัญชีเทรด
3. ใช้ `terminal` tool รัน Python script ที่เชื่อมต่อผ่าน `mt5linux`

## Quick Reference

```
Image (Full):    gmag11/metatrader5_vnc          (~4 GB, Python+RPyC included)
Image (Lite):    gmag11/metatrader5_vnc:1.1       (~600 MB, MQL5 only, no Python)
Port VNC:        3000
Port RPyC:       8001
MQL5 Folder:     config/.wine/drive_c/Program Files/MetaTrader 5/MQL5
Success retcode: 10009  (TRADE_RETCODE_DONE)
```

### Connection

```python
from mt5linux import MetaTrader5
mt5 = MetaTrader5(host='<docker-host-ip>', port=8001)  # Remote Docker
mt5 = MetaTrader5()                                     # Local Wine
```

### Key Functions

| Function | Purpose |
|---|---|
| `mt5.initialize(login, password, server)` | เชื่อมต่อและล็อกอิน |
| `mt5.shutdown()` | ปิดการเชื่อมต่อ |
| `mt5.account_info()` | ดูข้อมูลบัญชีและ Equity/Balance |
| `mt5.symbol_info_tick(symbol)` | ดู Bid/Ask ปัจจุบัน |
| `mt5.copy_rates_from_pos(symbol, tf, 0, N)` | ดึง N แท่งเทียนล่าสุด |
| `mt5.copy_rates_range(symbol, tf, d_from, d_to)` | ดึงแท่งเทียนในช่วงวันที่ |
| `mt5.copy_ticks_from(symbol, date, count, flags)` | ดึง Tick data |
| `mt5.order_send(request)` | ส่งคำสั่งเทรด |
| `mt5.positions_get(symbol=...)` | ดู Open Position |
| `mt5.orders_get(symbol=...)` | ดู Pending Order |
| `mt5.history_deals_get(d_from, d_to)` | ดูประวัติ Deal |
| `mt5.last_error()` | ดู error ล่าสุด |

### TIMEFRAME Constants

| Constant | Period |
|---|---|
| `mt5.TIMEFRAME_M1` | 1 นาที |
| `mt5.TIMEFRAME_M5` | 5 นาที |
| `mt5.TIMEFRAME_M15` | 15 นาที |
| `mt5.TIMEFRAME_M30` | 30 นาที |
| `mt5.TIMEFRAME_H1` | 1 ชั่วโมง |
| `mt5.TIMEFRAME_H4` | 4 ชั่วโมง |
| `mt5.TIMEFRAME_D1` | รายวัน |
| `mt5.TIMEFRAME_W1` | รายสัปดาห์ |
| `mt5.TIMEFRAME_MN1` | รายเดือน |

### ORDER_TYPE Constants

| Constant | ความหมาย |
|---|---|
| `mt5.ORDER_TYPE_BUY` | ซื้อ Market |
| `mt5.ORDER_TYPE_SELL` | ขาย Market |
| `mt5.ORDER_TYPE_BUY_LIMIT` | Buy Limit (Pending) |
| `mt5.ORDER_TYPE_SELL_LIMIT` | Sell Limit (Pending) |
| `mt5.ORDER_TYPE_BUY_STOP` | Buy Stop (Pending) |
| `mt5.ORDER_TYPE_SELL_STOP` | Sell Stop (Pending) |

### TRADE_ACTION Constants

| Constant | ความหมาย |
|---|---|
| `mt5.TRADE_ACTION_DEAL` | เปิด/ปิด Position ทันที (Market) |
| `mt5.TRADE_ACTION_PENDING` | วาง Pending Order |
| `mt5.TRADE_ACTION_SLTP` | แก้ SL/TP ของ Position ที่เปิดอยู่ |
| `mt5.TRADE_ACTION_MODIFY` | แก้ Pending Order |
| `mt5.TRADE_ACTION_REMOVE` | ลบ Pending Order |

### ORDER_FILLING Constants

| Constant | ความหมาย |
|---|---|
| `mt5.ORDER_FILLING_FOK` | Fill or Kill ทั้งหมดหรือยกเลิก |
| `mt5.ORDER_FILLING_IOC` | Immediate or Cancel ได้บางส่วน |
| `mt5.ORDER_FILLING_RETURN` | ส่งส่วนที่เหลือเป็น Pending ต่อ |

### COPY_TICKS Constants

| Constant | ความหมาย |
|---|---|
| `mt5.COPY_TICKS_ALL` | Tick ทุกประเภท |
| `mt5.COPY_TICKS_INFO` | เฉพาะ Bid/Ask |
| `mt5.COPY_TICKS_TRADE` | เฉพาะ Last/Volume |

## Procedure

### 1. ตั้งค่า Docker Compose

สร้างไฟล์ `docker-compose.yaml` ด้วย `terminal` tool:

```yaml
version: '3'
services:
  mt5:
    image: gmag11/metatrader5_vnc
    container_name: mt5
    volumes:
      - ./config:/config      # Linux
      # - mt5_config:/config  # Windows — ใช้อันนี้แทนบน Windows
    ports:
      - 3000:3000
      - 8001:8001
    environment:
      - CUSTOM_USER=myuser
      - PASSWORD=mypassword
      - MT5_CMD_OPTIONS=/login:123456   # optional auto-login
# volumes:
#   mt5_config:              # ปลด comment ถ้าใช้ Windows
```

```bash
docker compose up -d
```

เปิดเบราว์เซอร์ไปที่ `http://localhost:3000` รอ MT5 ติดตั้งเสร็จ (~5 นาที) แล้วล็อกอินด้วยบัญชีเทรด

### 2. เชื่อมต่อและ Initialize

```python
from mt5linux import MetaTrader5
import MetaTrader5 as mt5_const  # สำหรับ constants บน local

mt5 = MetaTrader5(host='127.0.0.1', port=8001)

if not mt5.initialize(login=25115284, password="mypassword", server="MetaQuotes-Demo"):
    print("Failed:", mt5.last_error())
    quit()

print(mt5.version())       # (500, 4120, '22 Dec 2023')
print(mt5.account_info())  # Balance, Equity, Margin, etc.
```

### 3. ดึงข้อมูล OHLCV

```python
import pandas as pd
import pytz
from datetime import datetime

# วิธีที่ 1: ดึง N แท่งล่าสุด (start_pos=0 คือแท่งปัจจุบัน)
rates = mt5.copy_rates_from_pos("EURUSD", mt5.TIMEFRAME_H1, 0, 100)
df = pd.DataFrame(rates)
df['time'] = pd.to_datetime(df['time'], unit='s')

# วิธีที่ 2: ดึงจากวันที่กำหนด (ต้องเป็น UTC เสมอ)
utc = pytz.timezone("Etc/UTC")
utc_from = datetime(2024, 1, 1, tzinfo=utc)
rates = mt5.copy_rates_from("EURUSD", mt5.TIMEFRAME_D1, utc_from, 365)

# วิธีที่ 3: ดึงในช่วง Date Range
utc_to = datetime(2024, 6, 30, tzinfo=utc)
rates = mt5.copy_rates_range("USDJPY", mt5.TIMEFRAME_M5, utc_from, utc_to)
```

**Columns ที่ได้:** `time, open, high, low, close, tick_volume, spread, real_volume`

### 4. ดึง Tick Data

```python
from datetime import datetime
import pytz

utc = pytz.timezone("Etc/UTC")
date_from = datetime(2024, 1, 10, tzinfo=utc)

ticks = mt5.copy_ticks_from("EURUSD", date_from, 1000, mt5.COPY_TICKS_ALL)
df_ticks = pd.DataFrame(ticks)
df_ticks['time'] = pd.to_datetime(df_ticks['time'], unit='s')
```

**Columns:** `time, bid, ask, last, volume, time_msc, flags, volume_real`

### 5. ดู Bid/Ask ปัจจุบัน

```python
tick = mt5.symbol_info_tick("EURUSD")
print(f"Bid: {tick.bid}, Ask: {tick.ask}")
```

### 6. ส่งคำสั่งซื้อ (Market Order)

```python
symbol = "EURUSD"
lot = 0.1
point = mt5.symbol_info(symbol).point
price = mt5.symbol_info_tick(symbol).ask

request = {
    "action": mt5.TRADE_ACTION_DEAL,
    "symbol": symbol,
    "volume": lot,
    "type": mt5.ORDER_TYPE_BUY,
    "price": price,
    "sl": price - 100 * point,   # Stop Loss
    "tp": price + 100 * point,   # Take Profit
    "deviation": 20,             # Max slippage in points
    "magic": 123456,             # EA identifier
    "comment": "python buy",
    "type_time": mt5.ORDER_TIME_GTC,
    "type_filling": mt5.ORDER_FILLING_RETURN,
}

result = mt5.order_send(request)

if result.retcode != mt5.TRADE_RETCODE_DONE:  # 10009 = สำเร็จ
    print(f"Failed: retcode={result.retcode}")
else:
    print(f"Opened! Ticket: {result.order}, Price: {result.price}")
```

### 7. ปิด Position

```python
position_ticket = result.order   # จาก Step 6
price = mt5.symbol_info_tick(symbol).bid

close_request = {
    "action": mt5.TRADE_ACTION_DEAL,
    "symbol": symbol,
    "volume": lot,
    "type": mt5.ORDER_TYPE_SELL,
    "position": position_ticket,  # ระบุ ticket ที่ต้องการปิด
    "price": price,
    "deviation": 20,
    "magic": 123456,
    "comment": "python close",
    "type_time": mt5.ORDER_TIME_GTC,
    "type_filling": mt5.ORDER_FILLING_RETURN,
}

result = mt5.order_send(close_request)
```

### 8. ดู Open Positions & Orders

```python
# ดู Position ทั้งหมด
positions = mt5.positions_get()

# กรองตาม Symbol
positions = mt5.positions_get(symbol="EURUSD")

# กรองตาม Group pattern
positions = mt5.positions_get(group="*USD*")

# แปลงเป็น DataFrame
df = pd.DataFrame(list(positions), columns=positions[0]._asdict().keys())
df['time'] = pd.to_datetime(df['time'], unit='s')

# ดู Pending Orders
orders = mt5.orders_get(symbol="EURUSD")
```

**Position fields:** `ticket, time, type, volume, price_open, sl, tp, price_current, swap, profit, symbol, comment`

### 9. ดูประวัติ Deal

```python
import pytz
from datetime import datetime

utc = pytz.timezone("Etc/UTC")
d_from = datetime(2024, 1, 1, tzinfo=utc)
d_to = datetime(2024, 12, 31, tzinfo=utc)

deals = mt5.history_deals_get(d_from, d_to)
df_deals = pd.DataFrame(list(deals), columns=deals[0]._asdict().keys())
df_deals['time'] = pd.to_datetime(df_deals['time'], unit='s')
```

### 10. ปิดการเชื่อมต่อ

```python
mt5.shutdown()   # เรียกทุกครั้งก่อนจบ script
```

## Pitfalls

- **Intel x86/amd64 เท่านั้น**: Image ไม่รองรับ ARM (Mac M-series, Raspberry Pi) โดยสิ้นเชิง
- **Image ขนาดใหญ่**: `gmag11/metatrader5_vnc` (latest) มีขนาด ~4 GB. ถ้าต้องการแค่รัน EA/MQL5 ไม่ต้องใช้ Python ให้ใช้ tag `:1.1` (~600 MB) แทน
- **Timezone ต้องเป็น UTC เสมอ**: Python `datetime` ใช้ timezone ท้องถิ่น แต่ MT5 เก็บเวลาเป็น UTC เสมอ ต้องสร้าง `datetime` ด้วย `pytz.timezone("Etc/UTC")` ก่อนส่งให้ฟังก์ชัน copy_rates ทุกครั้ง มิฉะนั้นข้อมูลจะผิด offset
- **Windows Bind Mount ไม่ได้**: บน Windows ต้องใช้ Docker Managed Volume (`mt5_config:`) แทน Bind Mount `./config:` เพราะจะเกิดปัญหา Permission
- **ต้องล็อกอิน MT5 ผ่าน VNC ก่อน**: แม้จะส่ง `MT5_CMD_OPTIONS=/login:xxx` แต่การล็อกอินผ่านหน้าจอ VNC ครั้งแรกยังจำเป็นเพื่อบันทึก session ลงใน Wine profile
- **`order_send` ไม่ประกัน Fill Price**: ราคาที่ได้จริงอยู่ใน `result.price` ไม่ใช่ราคาที่ส่งไป (`request["price"]`) เพราะมี slippage
- **`type_filling` ต้องตรงกับโบรกเกอร์**: โบรกเกอร์แต่ละเจ้ารองรับ filling mode ต่างกัน ถ้าได้ retcode 10030 ให้ลองเปลี่ยนจาก `ORDER_FILLING_RETURN` เป็น `ORDER_FILLING_FOK` หรือ `ORDER_FILLING_IOC`
- **Group filter syntax**: `group="*, !EUR"` หมายถึงเลือกทั้งหมดแล้วตัด EUR ออก ลำดับ inclusion ก่อน exclusion เสมอ

## Verification

ใช้ `terminal` tool รันคำสั่งตรวจสอบ:

```python
from mt5linux import MetaTrader5
mt5 = MetaTrader5(host='127.0.0.1', port=8001)
if mt5.initialize():
    print("✅ Connected:", mt5.version())
    print("💰 Account:", mt5.account_info().balance, mt5.account_info().currency)
    mt5.shutdown()
else:
    print("❌ Failed:", mt5.last_error())
```

Output ที่ถูกต้อง: `✅ Connected: (500, 4120, '22 Dec 2023')`
