---
name: farmed-hedge-yield-strategy
description: กลยุทธ์การเทรดแบบ Systematic Hedging และ Yield Farming จาก Farmed Hedge Yield Copy I พร้อมการปรับใช้ด้วย Python/MT5
category: algorithmic-trading
author: Tonthong
---

# Farmed Hedge Yield Strategy (Systematic Hedging)

กลยุทธ์นี้ถอดรหัสจาก MQL5 Signal "Farmed Hedge Yield Copy I" โดยเน้นการสร้างกระแสเงินสด (Yield) ผ่านโครงสร้างการ Hedge อย่างเป็นระบบ (Systematic Hedging) ในตลาด Forex โดยเฉพาะคู่เงิน Cross Pairs ที่มีพฤติกรรมแกว่งตัวในกรอบ (Mean-Reverting)

## 📊 การวิเคราะห์กลยุทธ์ต้นฉบับ (Strategy Analysis)
*   **Core Concept:** Market-Neutral Framework (ลดความเสี่ยงจากทิศทางตลาด), 99% Algorithmic, เน้นเปิด Position ตลอดเวลา (95.39% Market Exposure)
*   **Asset Class:** Cross Pairs (AUDCAD, GBPAUD, EURAUD, EURJPY, AUDJPY)
*   **Directional Split:** สมดุล 50% Long / 50% Short 
*   **Trade Frequency:** สูงมาก (เฉลี่ย 90 trades/week, ถือครองเฉลี่ย 24 ชม.)
*   **Risk Profile:** **High Risk / High Return** 
    *   Max Drawdown ต้นฉบับสูงถึง 42.20%
    *   Max Deposit Load 96.99% (มีการใช้ Margin หนักมาก มักเกิดจากการถัวเฉลี่ยแบบ Grid/Recovery)
    *   Win Rate ~59%, Risk:Reward (Avg Win/Loss) = 1:1 

## 🛠 กลไกการทำงาน (Mechanics)
1.  **Pair Selection:** เลือกเทรดเฉพาะกลุ่มคู่เงิน Cross ที่มีค่า Correlation เชิงลบต่อกัน หรือมีพฤติกรรม Mean Reversion ชัดเจน เพื่อทำ Statistical Arbitrage หรือ Grid Hedging
2.  **Continuous Hedging:** เปิดสถานะ Buy และ Sell พร้อมกันหรือสลับฝั่งในกรอบราคา เพื่อเก็บสะสมกำไรจากความผันผวน (Yield Farming)
3.  **Position Sizing:** เติบโตแบบเชิงเส้น (Linear Scaling)
    *   ทุน $400 - $500 : เทรด 0.01 Lot (Base)
    *   ทุน $1,000 : เทรด 0.02 - 0.03 Lot

## 🛡 Survival-First Adjustments (การปรับปรุงเพื่อการอยู่รอดตามสไตล์ Satang)
เนื่องจากต้นฉบับมี Drawdown ถึง 42% และเตือนเรื่อง "Absence of risk limitation" รวมถึง Deposit Load พุ่งไปถึง 96.99% เราต้องปรับปรุงดังนี้:
1.  **Portfolio-Level Equity Stop:** กำหนด Hard Stop Loss ที่ระดับ Portfolio (เช่น Max DD 15-20%) หาก Equity ลดลงถึงจุดนี้ ให้ Close All และหยุดบอททันที
2.  **Dynamic Grid Spacing (ATR-Based):** แทนที่จะเปิดไม้ถี่ๆ แบบระยะคงที่ (Fixed Pips) ให้ใช้ระยะห่างตาม ATR (Average True Range) เพื่อลด Deposit Load ในช่วงตลาดผันผวนรุนแรง
3.  **Exposure Cap (Max Open Lots):** จำกัด Max Deposit Load ไม่ให้เกิน 20-30% เพื่อป้องกันล้างพอร์ตจากการเกิด Black Swan Event

## 📊 ข้อมูลเชิงลึกจากบัญชีจริง (Axi-US50-Live)
- **Top Traded Symbols:** เน้นหนักไปที่คู่เงิน Cross ที่มีความสัมพันธ์กัน (Correlation) เช่น AUDCAD, GBPAUD, EURAUD, EURJPY, AUDJPY คู่เงินพวกนี้มักจะแกว่งตัวในกรอบ (Mean-reverting) มากกว่าคู่หลักอย่าง EURUSD
- **Win Rate vs Payoff:** Win Rate อยู่ที่ 59.02% โดยมี Average Win เท่ากับ Average Loss ($3.52 / -$3.52) ทำให้ Profit Factor ออกมาเป็นบวก (1.44) ซึ่งหมายความว่าระบบไม่ได้ใช้การตั้ง Take Profit ที่แคบมากๆ แบบ Scalping ทั่วไป แต่เน้นการปิดรวบยอด (Basket Close)
- **Holding Time:** เฉลี่ยถือออเดอร์ 24 ชั่วโมง ดังนั้นการเลือกบัญชีที่ Swap Free (Islamic Account) หรือค่า Swap ต่ำๆ เป็นสิ่งที่จำเป็นมาก
- **Drawdown Behavior:** ระบบจะมีการลาก (Drawdown) เพื่อสู้กับราคาค่อนข้างลึก (30-35% บ่อยครั้ง) นี่คือพฤติกรรมปกติของระบบประเภท Systematic Hedging ที่ไม่มี Hard Stop Loss ในแต่ละไม้

## 💻 แนวทางการเขียนบอท (Python + MT5)

### 1. การกำหนด Position Sizing
```python
def calculate_base_lot(account_balance):
    # Rule: 0.01 lot per $500
    base_lot = (account_balance / 500) * 0.01
    return round(base_lot, 2)
```

### 2. ลอจิกการเข้าเทรดแบบ Hedging & Grid (Pseudo-code)
```python
def execute_hedge_logic(symbol, base_lot, atr_value):
    current_price = mt5.symbol_info_tick(symbol).ask
    positions = get_open_positions(symbol)
    
    # หากไม่มี Position ให้เปิดพร้อมกันทั้ง Buy และ Sell (Market Neutral)
    if len(positions) == 0:
        open_buy(symbol, base_lot)
        open_sell(symbol, base_lot)
        return
        
    # ลอจิก Grid & Take Profit
    for pos in positions:
        # หากกำไรถึงเป้าหมาย (Yield Farming) -> ปิดทำกำไร
        if pos.profit >= TARGET_PROFIT:
            close_position(pos.ticket)
            
        # หากผิดทางเกินระยะ ATR -> เปิดไม้แก้ (Recovery) 
        # *คำเตือน: ต้องมี Exposure Cap
        if is_drawdown_exceed_atr(pos, current_price, atr_value):
            if get_total_exposure() < MAX_EXPOSURE:
                open_recovery_trade(pos.type, symbol, base_lot)
```

### 3. การควบคุมความเสี่ยงระดับพอร์ต (รันทุกๆ Tick หรือ นาที)
```python
def check_portfolio_survival(initial_balance, current_equity):
    max_allowed_drawdown = 0.20 # 20%
    current_drawdown = (initial_balance - current_equity) / initial_balance
    
    if current_drawdown >= max_allowed_drawdown:
        print("🚨 SURVIVAL ALERT: Max Drawdown Reached! Closing all positions.")
        close_all_positions()
        disable_auto_trading()
```

## ⚠️ Pitfalls (ข้อควรระวัง)
*   **Swap Costs:** การเปิดออเดอร์ทิ้งไว้ 2 ฝั่งหรือถือครองข้ามคืน (24 ชม.+) จะโดนค่า Swap กินกำไร ต้องเลือกคู่เงินที่ Swap สุทธิ (Net Swap) ไม่ติดลบหนักเกินไป หรือบัญชี Swap-free
*   **Margin Call:** สัญญาณต้นฉบับใช้ Margin โหดมาก (96.99% Load) หากเจอตลาดวิ่งเป็นเทรนด์ยาว (Trending Market) แบบไม่พัก พอร์ตจะระเบิดได้ง่าย ต้องมีระบบ Cut-loss รวม
*   **Broker Execution:** ต้องรันบน Broker ที่มีค่า Spread/Commission ต่ำที่สุดเท่านั้น เพราะเน้นเก็บกำไรทีละนิด (Win:Loss 1:1, Profit Factor 1.44)

## 📚 การเรียกใช้งาน
เมื่อต้องการพัฒนาระบบนี้ ให้ใช้ร่วมกับ Skill: `eamt5-python-architecture` และ `mt5-python-trading` เพื่อวางโครงสร้างบอทให้แข็งแกร่ง