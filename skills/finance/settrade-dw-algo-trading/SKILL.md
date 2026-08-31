---
name: settrade-dw-algo-trading
description: "คู่มือและขั้นตอนการสร้างระบบ Algorithmic Trading สำหรับเทรด DW (Derivative Warrants) ในตลาดหุ้นไทยผ่าน Settrade Open API (settrade-v2) ด้วย Python พร้อมวิเคราะห์พารามิเตอร์แบบเจาะลึก"
prerequisites:
  - Python 3.8+ (ใช้งาน `pip install settrade-v2==2.2.1`)
  - บัญชี Algorithmic Trading จากโบรกเกอร์ (App ID, App Secret, Broker ID)
  - ความรู้พื้นฐานเกี่ยวกับ DW (Gearing, Time Decay)
---

# ระบบเทรดอัตโนมัติ (Algorithmic Trading) สำหรับ DW ผ่าน Settrade Open API

การประยุกต์ใช้ Settrade Open API ในการเทรด DW ต้องทำความเข้าใจพารามิเตอร์ของ SDK ทั้งหมด เพื่อดึงข้อมูลราคาได้อย่างถูกต้อง (ผ่าน Market Data และ Realtime MQTT) และยิงคำสั่งได้รวดเร็ว (ผ่าน Equity)

## 1. ติดตั้งไลบรารี

ใช้ pip (หรือ uv) ในการติดตั้ง settrade-v2 (เวอร์ชันปัจจุบันคือ 2.2.1)
```bash
pip install settrade-v2==2.2.1
```

## 2. การ Authentication และ Initialize

```python
from settrade_v2 import Investor

investor = Investor(
    app_id="YOUR_APP_ID",                                 
    app_secret="YOUR_APP_SECRET",
    broker_id="YOUR_BROKER_ID",
    app_code="YOUR_APP_CODE",
    is_auto_queue=False 
)
```

## 3. วิเคราะห์ Parameters แบบเจาะลึกในแต่ละ Module

จาก Source Code ของ `settrade-v2` เราแบ่งการทำงานได้ 3 ส่วนหลัก ดังนี้:

### 3.1 Market Data (ข้อมูลราคารายวัน / อดีต)
ใช้สำหรับดึงข้อมูล Snapshot หรือข้อมูลประวัติย้อนหลัง สำหรับทำ Backtest หรือคำนวณ Indicator

```python
market = investor.MarketData()
```

* **`get_quote_symbol(symbol: str)`**
  ใช้ดึงราคาล่าสุด, ราคาเปิด/ปิด, ปริมาณการซื้อขาย, Bid/Offer ล่าสุด
  * **symbol:** (String) ชื่อย่อหุ้นหรือ DW เช่น `"PTT"`, `"PTT01C2405A"`
  
* **`get_candlestick(symbol: str, interval: str, limit: int, start: str, end: str, normalized: bool)`**
  ใช้ดึงข้อมูลแท่งเทียนย้อนหลัง (OHLCV) เพื่อเข้าสูตรวิเคราะห์ทางเทคนิค
  * **symbol:** ชื่อย่อหุ้น หรือ DW
  * **interval:** Timeframe เช่น `"1m"`, `"5m"`, `"15m"`, `"1d"`, `"1w"`
  * **limit:** จำนวนแท่งเทียนสูงสุดที่ต้องการ (เช่น 100)
  * **start / end:** เวลาเริ่มต้นและสิ้นสุดในรูปแบบ ISO 8601 (ไม่บังคับ)
  * **normalized:** การปรับฐานราคาย้อนหลังจากการแตกพาร์/ปันผล (Boolean)

### 3.2 Realtime Data Connection (MQTT Websocket)
ใช้สำหรับดึงราคาแบบ Streaming **(สำคัญมากสำหรับการเทรด DW)** เพื่อหลีกเลี่ยง Rate Limit ของการยิง REST API แบบลูป

```python
realtime = investor.RealtimeDataConnection()
```

* **`subscribe_price_info(symbol: str, on_message: Callable)`**
  ติดตามข้อมูล Tick และราคาล่าสุดแบบ Real-time (รับค่า high, low, last, total_volume)
  * **symbol:** ชื่อหุ้น / DW
  * **on_message:** ฟังก์ชัน Callback ที่จะถูกเรียกเมื่อมีข้อมูลใหม่เข้ามา เช่น
    ```python
    def on_price_changed(result, subscriber):
        print("Last Price:", result['data']['last'])
    
    sub = realtime.subscribe_price_info("PTT01C2405A", on_message=on_price_changed)
    sub.start()
    ```

* **`subscribe_bid_offer(symbol: str, on_message: Callable)`**
  ติดตามความเคลื่อนไหวของช่อง Bid/Offer ทั้ง 5 ช่อง (สำหรับเช็คว่า DW ตั้ง Bid หนาพอที่จะไม่ถ่าง Spread หรือไม่)

### 3.3 Equity Module (ส่งคำสั่งซื้อขาย)
ส่วนของการ Execution คำสั่งไปยังตลาด

```python
equity = investor.Equity(account_no="YOUR_ACCOUNT_NO")
```

* **`place_order(pin, side, symbol, volume, price, qty_open=0, trustee_id_type='Local', price_type='Limit', validity_type='Day', bypass_warning=None, valid_till_date=None)`**
  ส่งคำสั่งซื้อหรือขายหุ้น/DW
  * **pin:** (String) รหัส PIN สำหรับเทรด 6 หลัก
  * **side:** (String) `"Buy"` หรือ `"Sell"`
  * **symbol:** (String) ชื่อหุ้น หรือ DW (เช่น `"PTT01C2405A"`)
  * **volume:** (Integer) จำนวนหุ้นที่ต้องการเทรด (ต้องเป็นทวีคูณของ 100)
  * **price:** (Float) ราคาที่ต้องการ (ถ้า `price_type` เป็น MKT หรือ MTL ให้ใส่ `0`)
  * **price_type:** (String) รูปแบบราคา เช่น `"Limit"` (กำหนดราคาเอง), `"MP-MKT"` (ราคาตลาด), `"MP-MTL"`
  * **validity_type:** (String) `"Day"` (หมดอายุในวัน), `"FOK"` (Fill or Kill), `"IOC"` (Immediate or Cancel)

* **`cancel_order(order_no: str, pin: str)`**
  * **order_no:** เลขที่ออเดอร์ (ได้รับจาก return ของ place_order)
  * **pin:** รหัส PIN ของพอร์ต

* **ข้อมูลพอร์ตอื่นๆ ที่มีใน Equity:** 
  * `get_account_info()`: ตรวจสอบวงเงิน (Line Available, Cash Balance)
  * `get_portfolios()`: ตรวจสอบหุ้น/DW ที่ถืออยู่
  * `get_orders()`: ดูออเดอร์ที่ค้างอยู่ (Pending)

## 4. ข้อแนะนำเชิงเทคนิคสำหรับเทรด DW ด้วย API

1. **Architecture ที่เหมาะสม (Data Sourcing):**
   `yfinance` ไม่รองรับข้อมูล DW ของไทย ต้องแยกดึงกราฟหุ้นอ้างอิง (Underlying) เช่น `PTT.BK` ผ่าน `yfinance` เพื่อให้ AI/Indicator วิเคราะห์เทรนด์ แต่ต้องดึงราคา DW แบบ Real-time ผ่าน `MarketData().get_quote_symbol("PTT01C2405A")` ของ Settrade เพื่อนำไปคำนวณ Position Sizing และยิงคำสั่ง
2. **Rate Limit Handling:**
   อย่าใช้ `market.get_quote_symbol` ถี่เกินไป (ไม่เกินข้อจำกัด TPS ของโบรกเกอร์) ควรใช้ `realtime.subscribe_price_info` ในการ Monitor จังหวะเข้า
3. **Price Step Calculation:**
   ราคา DW มักจะแกว่งอยู่ในช่องราคาเล็กๆ (เช่น 0.01 บาท ต่อ 1 Tick) การเขียน Logic เพื่อเช็คว่า Gearing ของ DW เทียบกับหุ้นแม่ขยับกี่ช่อง เป็นกุญแจสำคัญในการตั้ง Take Profit
4. **Sandbox Market Hours ("User is inactive" Error):**
   หากพบ Error `User is inactive` เมื่อเรียกใช้โมดูล `MarketData` ใน Sandbox สาเหตุหลักคือ **อยู่นอกเวลาทำการตลาด** (ระบบ Sandbox มักระงับบริการให้ข้อมูลราคานอกเวลา แม้ว่าโมดูล `Equity` จะยังคงล็อกอินและเช็คพอร์ตได้ก็ตาม) ให้ทดสอบรันระบบในช่วงเวลา 10:00 - 16:30 น.

## 5. Reference Implementations

**⚠️ Common Pitfall for Settrade API:**
Do NOT use `validity_type="Day"` with `price_type="MP-MKT"`. The SET exchange rejects Market Price orders paired with a Day validity. 
**Fix**: Pair `MP-MKT` with `validity_type="FOK"` (Fill or Kill) or `validity_type="IOC"` (Immediate or Cancel). If you need a `Day` order, use a specific `Limit` price.

Available in this skill's `templates/` and `references/` directories:
- `references/settrade_vulnerabilities.md`: Critical architectural considerations when moving a Settrade bot from Sandbox to Production (market hours, real-time data sync, slippage tracking, and FOK spam prevention).
- `templates/adaptive_survival_system.py`: Production-ready Python trading engine featuring ADX sideways filters, ATR-based dynamic position sizing, Board Lot rounding for SET, and JSON state management.
- `templates/settrade_full_loop_bot.py`: A complete execution loop connecting the survival engine to the Settrade Open API (Sandbox) for automated portfolio sync and order placement.
- `templates/settrade_scanner_bot.py`: Multi-symbol scanner template showing how to handle state isolation, cash simulation (`lineAvailable` deduction/addition), and rate limiting (`time.sleep`) across multiple iterations without re-authenticating.
- `templates/settrade_dw_scanner_bot.py`: DW scanner template demonstrating dual data sourcing (yfinance for underlying trends, Settrade MarketData for real-time DW pricing) and Call Warrant (C) evaluation logic.
- `templates/mtf_analysis.py`: Multi-Timeframe (MTF) confluence analyzer combining Weekly, Daily, and Hourly data via `yfinance`.