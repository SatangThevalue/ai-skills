---
name: high-win-rate-mean-reversion
description: "สูตรลับการปรับจูน Indicator (Optimization) ให้ได้ Win Rate 100% สำหรับ Mean Reversion"
version: 0.1.0
metadata:
  hermes:
    tags: [Python, Backtest, Optimization, Mean Reversion, High Win Rate]
---

# High Win Rate Mean Reversion Optimization

สกิลนี้สาธิตวิธีการเขียนระบบ Backtest กลยุทธ์ Mean Reversion โดยใช้ตัวกรองหลายชั้น (Multi-layer Filtering) และการใช้ฟังก์ชัน Optimization ของ Python เพื่อค้นหาชุด Parameter ที่ให้ **Win Rate สูงที่สุด** ในช่วงหลายปีที่ผ่านมา

## When to Use

- "สามารถปรับ เพิ่ม เปลี่ยนแปลง ให้ win rate มากขึ้นได้ไหม?"
- เมื่อต้องการสร้างบอทที่มีความแม่นยำสูงมากๆ แลกกับความถี่ในการเทรดที่ลดลง
- เมื่อผู้ใช้อยากเห็นการปรับจูน Parameter (Tuning) ของ Algorithmic Trading

## Quick Reference

- **เป้าหมาย:** สั่ง AI ให้ `maximize='Win Rate [%]'`
- **Indicator Stack:** Bollinger Bands (ราคา) + RSI (โมเมนตัม) + ADX (เทรนด์)
- **The Secret Sauce:** บีบ Deviation ให้กว้างขึ้น (> 2.5) และห้าม ADX เกิน 20
- **ผลลัพธ์:** Win Rate 100% (แต่จำกัดโอกาสเทรดเหลือเพียงไม่กี่ครั้งต่อปี)

## Procedure (The Advanced Logic)

การจะทำ Win Rate ให้เข้าใกล้ 100% ได้ เราต้องเพิ่มตัวกรองให้บอท "เลือกกินเฉพาะคำที่ชัวร์ที่สุด"

### 1. การเพิ่มความยากในการเข้าเทรด
เปลี่ยนจากกราฟ 5 นาที ไปใช้กราฟ **1 ชั่วโมง (H1)** เพื่อลดสัญญาณหลอก (Noise) 
และปรับเงื่อนไข Entry ให้ยากขึ้นเป็น 3 ชั้น:

```python
# 1. กรองเทรนด์: ADX ต้องต่ำ (Side-ways เท่านั้น)
if ADX > 20: return

# 2. กรองกรอบราคา: ต้องทะลุ Bollinger Band ที่ตั้งค่า Deviation ไว้กว้างมากๆ (เช่น 3.0)
if Price < Lower_BB_3_0:

# 3. กรองความตึง: RSI ต้อง Oversold มากๆ
    if RSI(14) < 15:
        BUY()
```

### 2. การสั่ง Optimize เพื่อหา Win Rate
ในไลบรารี `Backtesting.py` สามารถปรับเป้าหมายของการ Optimize ได้ 
```python
stats = bt.optimize(
    n=[15, 20, 25],
    dev=[2.0, 2.5, 3.0],         # ลองถ่างขอบ BB ให้กว้างสุดๆ
    rsi_n=[2, 4, 14],            # ลอง RSI ทั้งระยะสั้นและยาว
    adx_limit=[20, 25, 30],      # ทดสอบการบล็อกเทรนด์
    maximize='Win Rate [%]'      # 🎯 เน้นความแม่นยำ ไม่เน้นจำนวนเงิน
)
```

## ผลลัพธ์จากการ Optimization เชิงลึก (EURUSD 1H, 2.5 ปีล่าสุด)

เมื่อปล่อยให้ AI คำนวณหาสมการที่เป็นไปได้ทั้งหมดกว่า 81 รูปแบบ พบว่าชุด Parameter ที่ได้ Win Rate **100% (ไม่แพ้เลยแม้แต่ไม้เดียวในรอบเกือบ 3 ปี)** คือ:

- `n=15` (Period ของ Bollinger Bands และค่าเฉลี่ย)
- `dev=3.0` (กางขอบ BB ให้กว้างแบบสุดๆ ต้องตกหนักจริงๆ ถึงจะเข้า)
- `rsi_n=14` (ใช้ RSI ระยะมาตรฐาน เพื่อความชัวร์)
- `adx_limit=20` (บังคับว่าเทรนด์ต้องนิ่งสนิทเท่านั้น)

## Pitfalls (Trade-off ของ Win Rate)

- **The Frequency Trap:** การที่ Win Rate 100% แลกมาด้วย **"โอกาสในการเทรดที่ลดลงอย่างมหาศาล"** จากผลทดสอบ บอทเจอสัญญาณซื้อขายเพียง **4 ครั้ง ในรอบ 2.5 ปี** 
- **Opportunity Cost:** กำไรสุทธิจากระบบนี้คือ `0.54%` ซึ่งแพ้การซื้อถือเฉยๆ (Buy & Hold `6.9%`) อย่างราบคาบ
- **บทเรียนทาง Quant:** ไม่มีอะไรเพอร์เฟกต์ในตลาดเทรด การเพิ่มความแม่นยำ (Win Rate) จะไปลดความถี่ (Frequency) ทำให้กระแสเงินสดรายวัน (Daily Cashflow) หายไป

## Verification
เมื่อรันโค้ด `optimize` โดยตั้งค่า `maximize='Win Rate [%]'` ผู้ใช้ควรวิเคราะห์ควบคู่กับค่า `# Trades` (จำนวนครั้งที่เทรด) เสมอ เพื่อหาสมดุล (Sweet Spot) ระหว่างความแม่นยำและโอกาสในการทำกำไร