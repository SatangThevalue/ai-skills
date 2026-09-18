---
name: quant-lightgbm-mql5-preprocessing
description: Data preprocessing, scaling (RobustScaler), and missing value handling for LightGBM -> ONNX -> MQL5 pipelines.
category: finance
---

# Quant Data Preprocessing: LightGBM to MQL5 via ONNX

แนวทางปฏิบัติและโครงสร้างสำหรับการทำ Data Preprocessing, Scaling และจัดการ Missing Values ในไปป์ไลน์ AI Trading (LightGBM -> ONNX -> MQL5)

## 1. Data Scaling Strategy

Financial data (ข้อมูลตลาดการเงิน) มักเป็นแบบ **Non-Normal Distribution** และมี **Outliers** สูง (Black Swan, Volatility Shock, Flash Crash, News Spike)

*   **StandardScaler** `(x - mean) / std`: ❌ อ่อนไหวต่อ Outlier (ค่าเพียงค่าเดียวสามารถทำให้ mean/std เพี้ยนได้ทั้งหมด)
*   **RobustScaler** `(x - median) / IQR`: ✅ ทนทานต่อ Outlier เพราะใช้ Median และ Q1, Q3 (IQR) แทน Mean/Std

### คำแนะนำการนำไปใช้ (Recommendation)
*   **LightGBM (Tree-based)**: ✅ **No Scaler** (เริ่มต้นโดยไม่ใช้ Scaler เพราะไม่มีผลกับ Tree)
*   **Neural Networks / Ensembles**: ✅ **RobustScaler**
*   **Experimentation (Version 2)**: หากจะจูน LightGBM เพิ่ม ให้ลองใส่ RobustScaler แล้ววัดผล (PF, Sharpe, Walk Forward) ว่าดีขึ้นจริงหรือไม่

---

## 2. การจัดการ Scaler ในฝั่ง MQL5 (Production)

หากใช้ RobustScaler ต้อง Export ค่า Center (Median) และ Scale (IQR) ออกมาเป็น JSON เพื่อนำไปใช้ฝั่ง MQL5

### Python Export (`scaler.json`)
```json
{
  "features": ["ret_5", "rsi14", "atr_ratio"],
  "center": [0.001, 52.3, 1.12],
  "scale": [0.005, 15.1, 0.42]
}
```

### MQL5: โหลดและใช้งาน (ใช้ร่วมกับ `JAson.mqh`)
```cpp
#include <JAson.mqh>

// 1. อ่านไฟล์และ Deserialize
string json_text;
int file_handle = FileOpen("scaler.json", FILE_READ|FILE_TXT);
if(file_handle != INVALID_HANDLE) {
   json_text = FileReadString(file_handle);
   FileClose(file_handle);
}

CJAVal root;
root.Deserialize(json_text);

double center[];
double scale[];
ArrayResize(center, 3);
ArrayResize(scale, 3);

for(int i=0; i<3; i++) {
   center[i] = root["center"][i].ToDbl();
   scale[i] = root["scale"][i].ToDbl();
}

// 2. ฟังก์ชันสเกลค่าแบบ Robust
double ScaleValue(double value, double _center, double _scale) {
   return (value - _center) / _scale;
}

// 3. ใช้งานจริงก่อนส่งเข้า ONNX
features[0] = ScaleValue(ret_5, center[0], scale[0]);
```

---

## 3. Missing Values Management (Critical Rule)

การจัดการ Missing Values สำคัญกว่าการเลือก Scaler ต้องป้องกันทั้งช่วง Train และ Live Trading โดยแบ่งเป็น 4 ประเภท:

### Type 1: Indicator Warmup
*   **ปัญหา**: แท่งแรกๆ ของ Indicator (เช่น RSI14 ช่วง 14 แท่งแรก) จะเป็น `NaN`
*   **วิธีแก้**: `df = df.dropna()` ในช่วง Training

### Type 2: Data Gap
*   **ปัญหา**: Broker Disconnect, API Fail (เช่น ข้อมูลกระโดดจาก 13:00 ไป 13:05)
*   **วิธีแก้**: ต้องตรวจจับ (Detect) `timestamp_gap` ก่อนทำ Feature Engineering

### Type 3: Feature Error
*   **ปัญหา**: การคำนวณผิดพลาด เช่น ส่วนเป็นศูนย์ (ATR14 / ATR100 ที่เป็น 0) ทำให้เกิด `Infinity`
*   **วิธีแก้ (Python)**:
    ```python
    import numpy as np
    df = df.replace([np.inf, -np.inf], np.nan)
    ```

### Type 4: Live Trading Data Issue
*   **ปัญหา**: Indicator Handle Fail หรือ Volume ยังไม่มีการอัปเดตในแท่งปัจจุบัน
*   **วิธีแก้**: ต้องมี Validation Gate ใน MQL5 ก่อนรัน Predict

---

## 4. Production Workflow Standard

ปฏิบัติตาม Pipeline นี้เสมอเพื่อป้องกัน Data Leakage และ Execution Error

### Python (Training & Validation)
```python
# 1. Training Preprocessing
df = df.replace([np.inf, -np.inf], np.nan)
df = df.dropna()

# 2. Validation Gate (ต้องผ่านก่อนเทรนหรือเทสต์)
assert not df.isna().any().any(), "Data contains NaN values!"
```

### MQL5 (Live Execution Gate)
ใน EA (MQL5) ก่อนส่ง Array ของ Features เข้าโมเดล ONNX จะต้องตรวจสอบความสมบูรณ์ของตัวเลขทุกครั้ง:
```cpp
bool ValidateFeatures(float &features[]) {
   for(int i=0; i<ArraySize(features); i++) {
      if(!MathIsValidNumber(features[i])) { // เช็ค NaN และ Infinity
         Print("Invalid feature detected at index: ", i);
         return false;
      }
   }
   return true;
}
```