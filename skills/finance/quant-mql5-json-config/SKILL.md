---
name: quant-mql5-json-config
description: JSON library selection (JAson.mqh), scaler.json structure with metadata, and Data Scaling decision matrix for LightGBM -> ONNX -> MQL5 pipelines.
category: finance
---

# Quant MQL5 JSON Config & Scaling Strategy

คู่มือการตัดสินใจและโครงสร้างการจัดการ Configuration (JSON) และกลยุทธ์การทำ Data Scaling สำหรับ AI Trading Pipeline (LightGBM -> ONNX -> MQL5) ระดับ Production

## 1. การเลือก JSON Library สำหรับ MQL5

### อันดับ 1: `JAson.mqh` ⭐⭐⭐⭐⭐ (แนะนำที่สุด)
*   **ข้อดี**: ใช้งานง่าย, รองรับ Array และ Nested JSON, Community ใหญ่มีตัวอย่างเยอะ
*   **Use Cases**: เหมาะสำหรับการอ่าน `scaler.json`, `feature_order.json`, `model_config.json`
*   **ตัวอย่าง**:
    ```cpp
    #include <JAson.mqh>
    
    CJAVal root;
    root.Deserialize(json_text);
    
    double buy_threshold = root["buy_threshold"].ToDbl();
    string version = root["model_version"].ToStr();
    ```

### ทางเลือกอื่นๆ
*   **อันดับ 2: `CJsonNode`**: ทำงานเร็วและเบา (Native style) แต่เขียนยากกว่าและตัวอย่างน้อยกว่า
*   **อันดับ 3: เขียน Parser เอง** (`StringFind`, `StringSplit`): ❌ **ไม่แนะนำ** (เกิด Bug ง่าย ดูแลรักษายาก และเสียเวลา)

> **Recommendation**: สำหรับทีมพัฒนา V1-V3 ให้เริ่มด้วย `JAson.mqh` ก่อนเลย

---

## 2. โครงสร้างไฟล์ `scaler.json`

### กรณีไม่มี Scaler (Version 1)
ควรมี Metadata กำกับเพื่อความชัดเจน:
```json
{
  "scaler_type": "none",
  "feature_version": "FS_V1",
  "feature_count": 5
}
```

### กรณีใช้ RobustScaler พร้อม Metadata
การเพิ่ม Metadata (เช่น `created_at`, `model_version`) จะช่วยให้การทำ Audit ในอนาคตง่ายขึ้นมาก:

```json
{
  "scaler_type": "robust",
  "created_at": "2026-08-31",
  "model_version": "V1.2",
  "feature_version": "FS_V2",
  "features": [
      "ret_5",
      "rsi14",
      "atr_ratio",
      "adx14",
      "volume_ratio"
  ],
  "center": [
      0.0002,
      51.3,
      1.10,
      22.4,
      1.05
  ],
  "scale": [
      0.004,
      14.8,
      0.32,
      9.4,
      0.51
  ]
}
```

### การนำไปใช้ใน MQL5 (RobustScaler)
```cpp
scaled_value = (value - center[i]) / scale[i];
```

---

## 3. Decision Matrix: ควรใช้ Scaler เมื่อไร?

คำถามนี้สำคัญกว่าการเขียนโค้ด!

### 3.1 กรณีที่ไม่ต้องใช้ Scaler
*   **โมเดลเป็น Tree-based (LightGBM, XGBoost, CatBoost, Random Forest)**: โดยธรรมชาติโมเดลกลุ่มนี้ไม่ค่อยสนใจ Scale ของข้อมูล (เช่น RSI = 60 หรือ 0.60 ให้ผลลัพธ์แทบไม่ต่างกัน) แนะนำให้ **ไม่ใช้ Scaler** ในเวอร์ชันแรก
*   **Feature ถูก Normalize อยู่แล้ว**: เช่น RSI (0-100), Stochastic (0-100) การทำ Scale ซ้ำอาจทำให้เสียข้อมูล
*   **Feature เป็น Binary**: เช่น `bull_regime`, `news_flag`, `buy_signal` (ไม่ต้อง Scale)

### 3.2 กรณีที่ควรพิจารณาใช้ RobustScaler
*   **Feature มี Outlier สูง**: เช่น Volume Ratio, ATR Ratio, Spread, Return ที่อาจพุ่งสูงผิดปกติช่วงข่าว (NFP, CPI) หรือ Flash Crash
*   **Feature มี Distribution เบ้มาก (Right Skew)**: แนะนำให้ใช้คู่กับ `log1p()` + `RobustScaler`
*   **ใช้โมเดลกลุ่ม Neural Network**: (LSTM, Transformer, MLP, TabTransformer) เพราะโมเดลกลุ่มนี้แพ้ Outlier ได้ง่าย

---

## 4. Quant Lead Strategy & Roadmap

### V1: The Standard Pipeline (จุดเริ่มต้นที่แนะนำ)
เน้นความเรียบง่าย, Debug ง่าย, เขียน MQL5 ง่าย:
*   ✅ ใช้ **`JAson.mqh`** ใน MQL5
*   ✅ มีไฟล์ **`feature_order.json`** และ **`model_config.json`**
*   ✅ โมเดล: **LightGBM + ONNX**
*   ✅ Data: RSI, ATR, ADX, EMA Gap
*   ✅ **No Scaler**

### V2: Scaling Experimentation
เปรียบเทียบผลลัพธ์ผ่าน **MLflow**: `FS_V1 (No Scale)` vs `FS_V2 (RobustScale)`
*   ทดลองใช้ `RobustScaler` เฉพาะ Feature กลุ่ม *Return, Volume Ratio, ATR Ratio, Spread*
*   วัดผลเทียบที่: Profit Factor, Sharpe Ratio, Drawdown, และ Walk Forward Stability