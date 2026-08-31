---
name: settrade-marketrep-derivatives-python
description: Guide and comprehensive API reference for Settrade Open API (MarketRep Derivatives SDK v2 for Python).
---

# Settrade Open API (MarketRep Derivatives SDK v2 for Python)

## บทนำ (Introduction)
สกิลนี้รวบรวมคำอธิบายการใช้งาน API ทุกฟังก์ชันสำหรับระบบ **Market Representative (Derivatives)** หรือตัวแทนตลาด (อนุพันธ์) ของ Settrade Open API V2 โดยใช้ภาษา Python

---

## 1. การเริ่มต้นใช้งาน (Getting Started)

### `MarketRep(app_id, app_secret, broker_id, app_code, is_auto_queue)`
ฟังก์ชันใช้สำหรับสร้าง Object หลักของระบบ เพื่อระบุตัวตนของผู้ใช้งานที่เป็น Market Representative (ผู้แนะนำการลงทุน หรือตัวแทนตลาด)

**พารามิเตอร์:**
- `app_id` (*string*): Application ID
- `app_secret` (*string*): Application Secret
- `broker_id` (*string*): รหัสโบรกเกอร์ (Broker ID)
- `app_code` (*string*): (Optional) ค่าเริ่มต้นคือ `"IC_ORDER"`
- `is_auto_queue` (*boolean*): (Optional) ค่าเริ่มต้นคือ `False`

**ตัวอย่าง:**
```python
from settrade_v2 import MarketRep

marketrep = MarketRep(
    app_id="Your App Id",
    app_secret="Your App Secret",
    broker_id="Your Broker Id",
    app_code="Your App Code",
    is_auto_queue=False
)
```

---

## 2. การสร้าง Derivatives Object (Build Object)

### `MarketRep.Derivatives(account_no)`
สร้าง object สำหรับเรียกใช้งาน API ต่างๆ ของระบบซื้อขายอนุพันธ์ (Derivatives) 

**พารามิเตอร์:**
- `account_no` (*string*): หมายเลขบัญชีซื้อขายอนุพันธ์ (Derivatives Account Number)

**ตัวอย่าง:**
```python
deri = marketrep.Derivatives(account_no="Your Account No")
```

---

## 3. ข้อมูลบัญชี (Get Account Info)

### `Derivatives.get_account_info()`
ดึงข้อมูลวงเงินและสถานะบัญชีอนุพันธ์ (Account Information)

**ตัวอย่าง:**
```python
account_info = deri.get_account_info()
print(account_info)
```

---

## 4. ข้อมูลคำสั่งซื้อขาย (Order Information)

### 4.1 ดูข้อมูลคำสั่งซื้อขาย 1 รายการ (Get Order)
`Derivatives.get_order(order_no)`
ดึงรายละเอียดของคำสั่งซื้อขายที่ระบุ 

**พารามิเตอร์:**
- `order_no` (*long*): หมายเลขคำสั่งซื้อขาย (Order Number)

**ตัวอย่าง:**
```python
order = deri.get_order(order_no=123456789)
print(order)
```

### 4.2 ดูข้อมูลคำสั่งซื้อขายทั้งหมด (Get Orders)
`Derivatives.get_orders()`
ดึงประวัติคำสั่งซื้อขายทั้งหมดของบัญชีที่ได้ทำการผูกไว้ใน Object `Derivatives`

**ตัวอย่าง:**
```python
orders = deri.get_orders()
print(orders)
```

### 4.3 ดูข้อมูลคำสั่งซื้อขายทั้งหมดแบบเจาะจงบัญชี (Get Orders By Account No)
`MarketRep.get_orders_by_account_no(account_no)`
(ดึงผ่าน object MarketRep ได้เลย)
ดึงข้อมูลคำสั่งซื้อขายทั้งหมด โดยระบุเลขที่บัญชี

**พารามิเตอร์:**
- `account_no` (*string*): หมายเลขบัญชีซื้อขาย

**ตัวอย่าง:**
```python
orders_acc = marketrep.get_orders_by_account_no(account_no="Your Account No")
print(orders_acc)
```

---

## 5. พอร์ตโฟลิโอ (Get Portfolios)

### `Derivatives.get_portfolios()`
ดึงข้อมูลสถานะสัญญา (Position) ที่ถือครองอยู่ทั้งหมดในพอร์ต

**ตัวอย่าง:**
```python
portfolios = deri.get_portfolios()
print(portfolios)
```

---

## 6. ข้อมูลรายการจับคู่ (Get Trades)

### `Derivatives.get_trades()`
ดึงข้อมูลรายการซื้อขายที่ได้รับการจับคู่แล้ว (Matched Trades) 

**ตัวอย่าง:**
```python
trades = deri.get_trades()
print(trades)
```

---

## 7. การส่งคำสั่งซื้อขาย (Place Order)

### `Derivatives.place_order(...)`
ส่งคำสั่งซื้อขายสัญญาอนุพันธ์เข้าสู่ระบบตลาด

**พารามิเตอร์:**
- `symbol` (*string*): ชื่อย่อสัญญา (เช่น `"S50M21"`)
- `price` (*float* หรือ *string*): ราคาที่ต้องการส่งคำสั่ง (สามารถใส่ค่าเป็นทศนิยม หรือ `"MP"`, `"MP-MTL"`, `"MP-MKT"` สำหรับราคาตลาดได้)
- `volume` (*long*): จำนวนสัญญาที่ต้องการซื้อ/ขาย
- `side` (*string*): ด้านในการส่งคำสั่ง (`"Long"` หรือ `"Short"`)
- `position` (*string*): สถานะ (`"Auto"`, `"Open"`, `"Close"`)
- `pin` (*string*): รหัส PIN Code ของบัญชี
- `price_type` (*string*, optional): ประเภทของราคา (default: `"Limit"`) - เช่น `"Limit"`, `"ATO"`, `"ATC"`
- `validity_type` (*string*, optional): เงื่อนไขเวลาการส่งคำสั่ง (default: `"Day"`) - เช่น `"Day"`, `"FOK"`, `"IOC"`, `"Date"`, `"Cancel"`
- `validity_date_ext` (*string*, optional): วันที่หมดอายุ กรณีที่ `validity_type` เป็น Date หรือ Cancel (Format: `YYYY-MM-DD`)
- `stop_condition` (*string*, optional): เงื่อนไข Stop Order
- `stop_symbol` (*string*, optional): ชื่อย่อสัญญาของ Stop Order
- `stop_price` (*float*, optional): ราคา Stop Price

**ตัวอย่าง:**
```python
order = deri.place_order(
    symbol="S50M21",
    price=900.5,
    volume=10,
    side="Long",
    position="Auto",
    pin="000000"
)
print(order)
```

---

## 8. การแก้ไขคำสั่งซื้อขาย (Change Order)

### `Derivatives.change_order(...)`
เปลี่ยนแปลงจำนวนหรือราคาของคำสั่งซื้อขายที่ยังจับคู่ไม่ครบ (Pending)

**พารามิเตอร์:**
- `order_no` (*long*): หมายเลขคำสั่งซื้อขาย
- `new_price` (*float*): ราคาใหม่ (ถ้าไม่เปลี่ยนให้ใส่ค่าเดิม)
- `new_volume` (*long*): จำนวนสัญญาใหม่ (ถ้าไม่เปลี่ยนให้ใส่ค่าเดิม - ห้ามใส่ 0)
- `pin` (*string*): รหัส PIN Code

**ตัวอย่าง:**
```python
changed_order = deri.change_order(
    order_no=123456789,
    new_price=905.0,
    new_volume=10,
    pin="000000"
)
print(changed_order)
```

---

## 9. การยกเลิกคำสั่งซื้อขาย (Cancel Order)

### 9.1 ยกเลิกคำสั่งซื้อขาย 1 รายการ
`Derivatives.cancel_order(order_no, pin)`

**พารามิเตอร์:**
- `order_no` (*long*): หมายเลขคำสั่งซื้อขายที่ต้องการยกเลิก
- `pin` (*string*): รหัส PIN Code

**ตัวอย่าง:**
```python
canceled = deri.cancel_order(
    order_no=123456789,
    pin="000000"
)
print(canceled)
```

### 9.2 ยกเลิกคำสั่งซื้อขายหลายรายการ (Cancel Orders)
`Derivatives.cancel_orders(order_no_list, pin)`

**พารามิเตอร์:**
- `order_no_list` (*list[long]*): ลิสต์ของหมายเลขคำสั่งซื้อขายที่ต้องการยกเลิก
- `pin` (*string*): รหัส PIN Code

**ตัวอย่าง:**
```python
canceled_orders = deri.cancel_orders(
    order_no_list=[123456789, 123456790, 123456791],
    pin="000000"
)
print(canceled_orders)
```

---

## 10. การบันทึกรายงานการซื้อขาย (Place Trade Report)

### `Derivatives.place_trade_report(...)`
บันทึกรายงานการซื้อขายเข้าสู่ระบบ (สำหรับธุรกรรม Block Trade หรืออื่นๆ ตามที่โบรกเกอร์รองรับ)

**พารามิเตอร์ (จำเป็นต้องอิงตาม Document หลัก):**
- `symbol` (*string*)
- `price` (*float*)
- `volume` (*long*)
- `buyer_account_no` (*string*)
- `seller_account_no` (*string*)
- `pin` (*string*)
- รวมถึงฟิลด์ออพชั่นเช่น `buyer_position`, `seller_position` เป็นต้น

**ตัวอย่าง:**
```python
trade_report = deri.place_trade_report(
    symbol="S50M21",
    price=900.5,
    volume=10,
    buyer_account_no="BUYER_ACC_NO",
    seller_account_no="SELLER_ACC_NO",
    pin="000000"
)
print(trade_report)
```
