---
name: quant-data-cleaning-and-scaling
description: "เทคนิคการจัดการ Missing Value แบบ Quant Professional และการใช้ RobustScaler + JSON Library ใน MQL5"
---

# Quant Data Cleaning & Scaling (Python to MQL5)

กฎเหล็กของระบบเทรดคือ **Data Quality > Feature Engineering > Model**
หลายโปรเจกต์ไม่ได้พ่ายแพ้เพราะโมเดลไม่ดี แต่แพ้เพราะการจัดการ Missing Value ผิดพลาด และปัญหา Feature Mismatch ระหว่าง Python กับ MT5

---

## 1. วิธีจัดการ Missing Values (สิ่งที่ควร/ไม่ควรทำ)

### ❌ สิ่งที่ไม่ควรทำเด็ดขาด
- `df.fillna(0)`: ห้ามเติม 0 สุ่มสี่สุ่มห้า (เช่น `RSI14 = NaN` ไปแก้เป็น 0 โมเดลจะเข้าใจผิดว่า Oversold หนักมากแล้วสั่ง Buy)
- `df.ffill()` (Forward Fill): ดึงค่าเก่ามาใช้ (เช่น `ATR14` หายไป ก็ใช้ค่าเดิมตลอดเวลา ทำให้โมเดลคิดว่าตลาดนิ่ง ทั้งที่ความจริงอาจผันผวนแล้ว)

### ✅ แนวทางระดับ Quant Professional
**ฝั่ง Training (Python):**
- **กรณี Indicator Warmup (ช่วงแรกที่ข้อมูลยังไม่ครบ):** ปล่อยเป็น `NaN` ไปก่อนแล้วค่อยสั่ง `df.dropna()` ทิ้งทั้งหมดตอนจบ
- **กรณี Data Gap (เช่น ข้อมูลหายไป 4 นาที):** ให้สร้าง Flag เตือนดีกว่าเดาค่า (เช่น `df["missing_gap_flag"] = ~expected.isin(df.index)`)
- **กรณี Volume หาย:** ให้ใช้ `Median` แทน `Mean` (`df["volume"].fillna(df["volume"].median())`)
- **กฎเหล็กตอน Train:** `Replace INF -> NaN` ➔ `dropna()`

**ฝั่ง Live Trading (MQL5):**
- ถ้าเจอ `NaN`, `Infinity`, หรือ Feature หาย ➔ **NO TRADE** ทันที (Reject Prediction ทิ้ง ห้ามเติม 0)

---

## 2. โครงสร้าง Config Files ที่จำเป็นสำหรับการ Export

ในขั้นตอน Export จาก Python ควรแยก Config เป็นไฟล์ JSON หลายตัว เพื่อให้ MQL5 ดึงข้อมูลไปใช้ได้แบบอัตโนมัติ ไม่ต้อง Hardcode

**1. `feature_order.json` (จัดเรียง Feature ให้ตรงก่อนเข้าโมเดล)**
```json
{
  "feature_version": "FS_V1",
  "features": [
    "ret_5",
    "rsi14",
    "atr_ratio"
  ]
}
```

**2. `scaler.json` (ส่งค่าสถิติมาเพื่อทำ Normalize)**
```json
{
  "center": [0.001, 50, 1.15],
  "scale": [0.004, 12, 0.35]
}
```

**3. `model_config.json` (ตัวกำหนดพฤติกรรมการเทรด)**
```json
{
  "model_version": "1.0",
  "buy_threshold": 0.75,
  "sell_threshold": 0.25,
  "risk_percent": 1.0,
  "atr_sl": 1.5,
  "atr_tp": 3.0
}
```

---

## 3. การสร้าง RobustScaler ใน MQL5

ถ้าพิจารณาใช้ Scaler อย่าง RobustScaler (เช่น FS_V2) คุณสามารถนำค่า `center` และ `scale` จาก `scaler.json` มาใช้ตามตัวอย่างด้านล่าง:

### ฟังก์ชัน RobustScale (ใน MQL5)
```cpp
double RobustScale(double value, double center, double scale) {
   if(scale == 0.0) return 0.0;
   return (value - center) / scale;
}
```

### ตัวอย่างการประกอบร่างก่อนส่งเข้า ONNX
```cpp
double ret5_scaled = RobustScale(ret_5, center[0], scale[0]);
double rsi_scaled = RobustScale(rsi14, center[1], scale[1]);
double atr_scaled = RobustScale(atr_ratio, center[2], scale[2]);

float features[3];
features[0] = (float)ret5_scaled;
features[1] = (float)rsi_scaled;
features[2] = (float)atr_scaled;
```

---

## 4. Feature Validation (สำคัญมาก!)
ห้ามส่งข้อมูลเข้า Predict โดยไม่ตรวจสอบความสมบูรณ์ก่อน

```cpp
bool ValidateFeatures(float &features[]) {
   for(int i=0; i<ArraySize(features); i++) {
      if(!MathIsValidNumber(features[i])) { // ตรวจจับ NaN / INF
         return false;
      }
   }
   return true;
}

// วิธีใช้งาน
if(!ValidateFeatures(features)) {
   Print("Invalid Features - Reject Prediction");
   return;
}
```

---

## 5. แนะนำ JSON Library สำหรับ MQL5

เนื่องจากเราต้องโหลด JSON 3 ไฟล์จาก Python จึงต้องใช้ JSON Library ใน MQL5

**🥇 อันดับ 1: `JAson.mqh` (แนะนำที่สุด)**
- *ข้อดี:* ใช้ง่ายที่สุด, Community ใช้เยอะ, รองรับ Array และ Nested Object ได้ครบ
- *วิธีใช้:*
  ```cpp
  #include <JAson.mqh>
  CJAVal root;
  root.Deserialize(json_text);
  double value = root["center"][0].ToDbl();
  ```

**🥈 อันดับ 2: `CJsonNode`**
- *ข้อดี:* เร็วและเบา (แถมมากับตัวอย่างของ MQL5 Community) / *ข้อเสีย:* โค้ดเขียนยากกว่า JAson เล็กน้อย

**❌ ไม่แนะนำ: เขียน Parser เอง**
- การใช้ `StringFind()` กับ `StringSubstr()` มาตัดคำเองจะ Debug ยากมากและเกิดบั๊กได้ง่าย

---

## 🎯 บทสรุปในฐานะ Quant Lead

สำหรับ Version แรกของระบบ (V1) ควรเลือกใช้ส่วนผสมที่เบาที่สุดเพื่อลดโอกาสผิดพลาด:

- ✅ LightGBM
- ✅ **No Scaler**
- ✅ `feature_order.json`
- ✅ `model_config.json`
- ✅ `JAson.mqh`
- ✅ Missing Value Validation
- ✅ Reject Trade เมื่อ Feature ผิดปกติ

และจะพิจารณาใช้ RobustScaler ก็ต่อเมื่อผลใน Walk Forward และ MLflow แสดงชัดเจนว่า `FS_V2 (RobustScaler)` ดีกว่า `FS_V1 (No Scaler)` ในแง่ **Sharpe, Profit Factor, Drawdown, Stability** ไม่ใช่เลือกใช้เพราะเป็น Best Practice ทั่วไป 

*(เพราะสำหรับโมเดลอย่าง LightGBM แล้ว "Feature Quality" มีผลต่อผลลัพธ์มากกว่า "Scaler" อย่างชัดเจน)*