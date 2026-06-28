---
name: cost-accounting-inventory
description: การคำนวณบัญชีต้นทุนและการบริหารจัดการสินค้าคงคลัง (FIFO, Weighted Average, EOQ, Reorder Point, Safety Stock) พร้อม Python Implementation
category: finance
---

# คู่มือและสูตรการคำนวณบัญชีต้นทุนและสินค้าคงคลัง (Cost Accounting & Inventory Management)

สกิลนี้รวบรวมแนวคิด วิธีการบันทึกบัญชี สูตรคำนวณ และโค้ดตัวอย่างภาษา Python สำหรับการวิเคราะห์และคำนวณต้นทุนสินค้าคงคลัง และการวางแผนการสั่งซื้อที่ประหยัดที่สุด

---

## 1. วิธีการบันทึกบัญชีสินค้าคงคลัง (Perpetual vs Periodic)

1. **Perpetual Inventory System (ระบบบันทึกบัญชีสินค้าคงคลังแบบต่อเนื่อง)**
   - บันทึกการเพิ่ม/ลดของสินค้าและต้นทุนขายทันทีที่มีรายการเกิดขึ้น
   - เหมาะกับธุรกิจที่ใช้ระบบ POS หรือมีระบบจัดการคลังสินค้าอัตโนมัติ
   - ช่วยให้ทราบยอดคงเหลือและต้นทุนขาย ณ ปัจจุบันได้ตลอดเวลา

2. **Periodic Inventory System (ระบบบันทึกบัญชีสินค้าคงคลังเมื่อสิ้นงวด)**
   - ไม่บันทึกต้นทุนขายในระหว่างงวด แต่จะใช้วิธีตรวจนับสินค้าคงเหลือ ณ วันสิ้นงวด
   - คำนวณต้นทุนสินค้าที่ขายด้วยสูตร:
     $$\text{ต้นทุนขาย} = \text{สินค้าคงเหลือต้นงวด} + \text{ซื้อสุทธิระหว่างงวด} - \text{สินค้าคงเหลือปลายงวด}$$

---

## 2. วิธีการตีราคาสินค้าคงคลัง (Inventory Valuation Methods)

### A. FIFO (First-In, First-Out: เข้าก่อน ออกก่อน)
สินค้าที่ซื้อเข้ามาก่อนจะถูกบันทึกเป็นต้นทุนขายก่อน สินค้าที่เหลืออยู่ปลายงวดจึงเป็นสินค้าที่ซื้อเข้ามาล็อตหลังสุด
* **ข้อดี:** สะท้อนมูลค่าสินค้าคงเหลือปลายงวดใกล้เคียงกับราคาตลาดปัจจุบันมากที่สุด
* **ข้อเสีย:** หากราคาสินค้ามีแนวโน้มสูงขึ้น (Inflation) ต้นทุนขายจะต่ำ ทำให้กำไรสุทธิสูงและต้องเสียภาษีมากขึ้น

### B. Weighted Average & Moving Average (ถัวเฉลี่ยถ่วงน้ำหนัก / เฉลี่ยเคลื่อนที่)
* **Weighted Average (Periodic):** คำนวณหาต้นทุนถัวเฉลี่ยต่อหน่วยเพียงครั้งเดียว ณ วันสิ้นงวด
* **Moving Average (Perpetual):** คำนวณต้นทุนถัวเฉลี่ยใหม่ทุกครั้งที่มีการซื้อสินค้าล็อตใหม่เข้ามา
* **สูตรการหาต้นทุนเฉลี่ยต่อหน่วยใหม่:**
  $$\text{ต้นทุนเฉลี่ยใหม่} = \frac{(\text{สินค้าคงเหลือเดิม} \times \text{ต้นทุนเฉลี่ยเดิม}) + \text{มูลค่าของสินค้าที่ซื้อเข้ามาใหม่}}{\text{จำนวนสินค้าเดิม} + \text{จำนวนสินค้าที่ซื้อเข้ามาใหม่}}$$

### C. LIFO (Last-In, First-Out: เข้าหลัง ออกก่อน)
สินค้าที่ซื้อเข้ามาทีหลังสุดจะถูกขายออกไปก่อน
* *หมายเหตุ:* ปัจจุบัน**มาตรฐานการรายงานทางการเงินระหว่างประเทศ (IFRS / TFRS) ไม่อนุญาตให้ใช้วิธี LIFO** เนื่องจากมูลค่าสินค้าปลายงวดไม่สะท้อนราคาปัจจุบัน แต่ยังสามารถนำมาใช้ศึกษาเชิงพฤติกรรมการจัดการภายในได้

---

## 3. การวางแผนและการบริหารจัดการสินค้าคงคลัง (Inventory Control)

### A. ปริมาณการสั่งซื้อที่ประหยัดที่สุด (Economic Order Quantity: EOQ)
สูตรคำนวณปริมาณการสั่งซื้อในแต่ละครั้งที่ทำให้ผลรวมของต้นทุนการสั่งซื้อ (Ordering Cost) และต้นทุนการเก็บรักษา (Holding Cost) ต่ำที่สุด
$$EOQ = \sqrt{\frac{2 \times D \times S}{H}}$$
* $D$: ปริมาณความต้องการสินค้าต่อปี (Annual Demand)
* $S$: ต้นทุนการสั่งซื้อสินค้าต่อครั้ง (Setup / Ordering Cost per order)
* $H$: ต้นทุนการเก็บรักษาสินค้าต่อหน่วยต่อปี (Annual Holding / Carrying Cost per unit)

### B. จุดสั่งซื้อใหม่ (Reorder Point: ROP)
ระดับสินค้าคงคลังที่เมื่อลดลงมาถึงจุดนี้แล้ว จะต้องส่งคำสั่งสั่งซื้อสินค้าล็อตใหม่เข้ามาทันที
$$ROP = (d \times L) + SS$$
* $d$: อัตราความต้องการสินค้าเฉลี่ยต่อวัน (Average Daily Demand)
* $L$: ระยะเวลารอคอยสินค้า (Lead Time in days)
* $SS$: สินค้าคงคลังเพื่อความปลอดภัย (Safety Stock)

### C. สินค้าคงคลังเพื่อความปลอดภัย (Safety Stock: SS)
ปริมาณสินค้าคงเหลือที่เก็บไว้สำรองเพื่อป้องกันสินค้าขาดมือ (Stockout) จากความไม่แน่นอนของความต้องการหรือระยะเวลารอคอย
$$\text{Safety Stock} = (\text{Max Daily Sales} \times \text{Max Lead Time}) - (\text{Avg Daily Sales} \times \text{Avg Lead Time})$$

---

## 4. ตัวอย่างการใช้ Python คำนวณ (Python Code Implementation)

คุณสามารถนำโค้ดด้านล่างนี้ไปปรับใช้ประมวลผลผ่าน `execute_code` เพื่อหาผลลัพธ์จากข้อมูลจริงได้

### 4.1 ฟังก์ชันคำนวณต้นทุนคงคลังแบบ FIFO และ Moving Average

```python
def calculate_inventory_valuation(transactions):
    """
    transactions: รายการบันทึกการเข้า/ออกสินค้าคงคลัง
    ตัวอย่าง:
    [
        {"type": "buy", "qty": 100, "price": 10},
        {"type": "buy", "qty": 50, "price": 12},
        {"type": "sell", "qty": 120},
    ]
    """
    # 1. การคำนวณแบบ FIFO
    fifo_queue = [] # เก็บ tuple (qty, price)
    fifo_cogs = 0
    
    for tx in transactions:
        if tx["type"] == "buy":
            fifo_queue.append([tx["qty"], tx["price"]])
        elif tx["type"] == "sell":
            qty_to_sell = tx["qty"]
            while qty_to_sell > 0 and fifo_queue:
                first_lot = fifo_queue[0]
                if first_lot[0] <= qty_to_sell:
                    fifo_cogs += first_lot[0] * first_lot[1]
                    qty_to_sell -= first_lot[0]
                    fifo_queue.pop(0)
                else:
                    fifo_cogs += qty_to_sell * first_lot[1]
                    first_lot[0] -= qty_to_sell
                    qty_to_sell = 0
                    
    fifo_ending_qty = sum([lot[0] for lot in fifo_queue])
    fifo_ending_value = sum([lot[0] * lot[1] for lot in fifo_queue])
    
    # 2. การคำนวณแบบ Moving Average
    ma_qty = 0
    ma_avg_price = 0.0
    ma_cogs = 0
    
    for tx in transactions:
        if tx["type"] == "buy":
            total_cost = (ma_qty * ma_avg_price) + (tx["qty"] * tx["price"])
            ma_qty += tx["qty"]
            ma_avg_price = total_cost / ma_qty if ma_qty > 0 else 0
        elif tx["type"] == "sell":
            ma_cogs += tx["qty"] * ma_avg_price
            ma_qty -= tx["qty"]
            
    ma_ending_value = ma_qty * ma_avg_price
    
    return {
        "fifo": {
            "ending_qty": fifo_ending_qty,
            "ending_value": fifo_ending_value,
            "cogs": fifo_cogs
        },
        "moving_average": {
            "ending_qty": ma_qty,
            "ending_value": ma_ending_value,
            "cogs": ma_cogs,
            "current_avg_price": ma_avg_price
        }
    }
```

### 4.2 ฟังก์ชันคำนวณ EOQ, Safety Stock และ Reorder Point

```python
import math

def calculate_inventory_planning(annual_demand, order_cost, holding_cost, 
                                 avg_daily_sales, max_daily_sales, 
                                 avg_lead_time, max_lead_time):
    # 1.คำนวณ EOQ
    eoq = math.sqrt((2 * annual_demand * order_cost) / holding_cost)
    
    # 2.คำนวณ Safety Stock (SS)
    safety_stock = (max_daily_sales * max_lead_time) - (avg_daily_sales * avg_lead_time)
    
    # 3.คำนวณ Reorder Point (ROP)
    reorder_point = (avg_daily_sales * avg_lead_time) + safety_stock
    
    return {
        "eoq": round(eoq, 2),
        "safety_stock": round(safety_stock, 2),
        "reorder_point": round(reorder_point, 2)
    }
```

---

## 5. การวิเคราะห์ปัญหาที่พบบ่อย (Common Pitfalls)
1. **การละเลยต้นทุนแอบแฝง (Holding Cost):** หลายกิจการคำนวณต้นทุนถือครองต่ำไป (เช่น ลืมคิดค่าเสื่อมราคาของโกดัง, ค่าไฟระบบแช่เย็น, หรือค่าเสียโอกาสของเงินทุน) ทำให้สั่งซื้อสินค้ามากเกินไป (EOQ มีค่าสูงเกินความเป็นจริง)
2. **ความไม่สอดคล้องของหน่วยเวลา (Time Horizon Inconsistency):** การหาค่า $D$ (Annual Demand) ต้องใช้หน่วยปี และ $H$ (Holding Cost) ต้องคิดเป็นปีเช่นกัน แต่ Lead Time หรือยอดขายรายวันมักคิดเป็นหน่วยวัน ต้องแปลงหน่วยให้ตรงกันก่อนเข้าสูตร ROP และ SS
3. **ใช้ FIFO กับสินค้าผันผวนสูงโดยไม่สำรองผลขาดทุน:** ในภาวะเงินเฟ้อสูง FIFO จะแสดงกำไรทางบัญชีที่สูงเกินจริง (Phantom Profit) เนื่องจากนำต้นทุนเก่าราคาถูกมาหักกลบ ส่งผลให้เกิดปัญหากระแสเงินสดขาดแคลนในการสั่งซื้อสินค้าล็อตใหม่ที่เป็นราคาตลาดปัจจุบัน
