---
name: quant-lightgbm-onnx-mql5
description: Enterprise standards for exporting LightGBM models to ONNX and deploying to MQL5, covering scalers, feature metadata, and production bundles.
category: finance
---

# Quant Trading: LightGBM to ONNX & MQL5 Deployment Standards

มาตรฐานและข้อกำหนดระดับองค์กรสำหรับ Pipeline `Feature -> Scaler -> ONNX -> MQL5` เพื่อแก้ปัญหา "Training Accuracy ดี แต่ Live Trading แย่ (จากปัญหา Data Shift หรือ Scale Mismatch)" 

ให้ยึดปฏิบัติตามมาตรฐานนี้เมื่อต้อง Export โมเดล Machine Learning สำหรับนำไปเทรดจริงบน MetaTrader 5 (MT5)

## 1. Scaler Selection Standards

การเลือกใช้ Data Scaler ต้องสอดคล้องกับธรรมชาติของโมเดลและตลาดการเงิน (มักมี Outlier / Black Swan)

*   **LightGBM / Tree-based Models (XGBoost, Random Forest, CatBoost):**
    *   ✅ **ไม่ใช้ Scaler (ดีที่สุด):** ปล่อยให้ Tree จัดการค่าดิบ (เช่น RSI=65, ATR=0.0023) ได้เลย ช่วยลดความซับซ้อนและโอกาสเพี้ยน
    *   *ข้อยกเว้น:* อาจทำ Z-Score หรือ Ratio เฉพาะบาง Feature (เช่น Volume Ratio, ATR Ratio) หากจำเป็น
*   **Neural Network / Transformer / LSTM Models:**
    *   ✅ **RobustScaler เท่านั้น:** ใช้ Median และ IQR (แทน Mean/Std) ทนทานต่อ Outlier และ Unexpected Volatility ได้ดีที่สุด
*   **ข้อห้ามเด็ดขาด (Anti-patterns):**
    *   ❌ **MinMaxScaler:** พังทันทีเมื่อเจอค่าใน Live ทะลุขอบเขต Train (เช่น Train 0.5-2.0 แต่ Live เจอ 4.5 สัดส่วนจะเพี้ยนหนัก)
    *   ❌ **StandardScaler:** ไม่แนะนำเพราะได้รับผลกระทบจาก Outlier โดยตรง

---

## 2. Feature Metadata Export (บังคับทำ)

ป้องกันปัญหา Feature ลำดับเพี้ยนตอนนำไปใส่ใน MQL5 ต้อง Export เป็น JSON เสมอ

**2.1 Export Feature Order**
```python
import json

selected_features = ["ret_5", "ret_20", "rsi14", "adx14", "atr_ratio", "bb_width", "volume_ratio", "trend_score"]

feature_order = {
    "feature_version": "FS_V1",
    "feature_count": len(selected_features),
    "features": selected_features
}

with open("feature_order.json", "w", encoding="utf8") as f:
    json.dump(feature_order, f, indent=4)
```

**2.2 Export Feature Metadata (Level UP)**
```python
feature_registry = {
    name: {"dtype": "float32", "order": idx} 
    for idx, name in enumerate(selected_features)
}

with open("feature_metadata.json", "w", encoding="utf8") as f:
    json.dump(feature_registry, f, indent=4)
```

---

## 3. Scaler Export (กรณีใช้ RobustScaler)

อย่าเซฟเป็น Pickle (`.pkl`) ให้ดึง Parameter ออกมาเป็น JSON เพื่อให้นำไปเขียน Hardcode หรือโหลดใน MQL5 / ภาษาอื่นๆ ได้ตรงกัน

```python
from sklearn.preprocessing import RobustScaler
import json

# สมมติว่า scaler ถูก fit มาแล้ว
scaler_info = {
    "center": scaler.center_.tolist(),
    "scale": scaler.scale_.tolist(),
    "features": selected_features
}

with open("scaler.json", "w", encoding="utf8") as f:
    json.dump(scaler_info, f, indent=4)
```

---

## 4. ONNX Model Export

แปลง LightGBM เป็น ONNX สำหรับรันบน MT5

```python
import onnxmltools

# model คือ LightGBM Booster object
onnx_model = onnxmltools.convert_lightgbm(model)

with open("model.onnx", "wb") as f:
    f.write(onnx_model.SerializeToString())
```

---

## 5. Production Artifacts Bundle

ชุดไฟล์มาตรฐานที่ต้อง Deploy ขึ้นระบบ Production (VPS / MT5) ประกอบด้วย:
1. `model.onnx` (ไฟล์โมเดลหลัก)
2. `feature_order.json` (ลำดับ Feature)
3. `feature_metadata.json` (โครงสร้างและ Data Type)
4. `model_config.json` (ตั้งค่า Threshold, Versioning - ถ้ามี)
5. `scaler.json` (เฉพาะกรณีใช้ Neural Net / RobustScaler)

---

## 6. MQL5 Implementation Pattern

โครงสร้างโค้ด MQL5 มาตรฐานสำหรับการโหลดและรันโมเดล ONNX

```cpp
long onnx_handle;

int OnInit() {
    // 1. Load Model
    onnx_handle = OnnxCreate("model.onnx");
    if(onnx_handle == INVALID_HANDLE) {
        Print("Load ONNX Failed: Error ", GetLastError());
        return(INIT_FAILED);
    }
    return(INIT_SUCCEEDED);
}

void OnTick() {
    // 2. Input Features (ต้องเรียงตาม feature_order.json เป๊ะๆ)
    float features[8];
    features[0] = ret_5;
    features[1] = ret_20;
    features[2] = rsi14;
    features[3] = adx14;
    features[4] = atr_ratio;
    features[5] = bb_width;
    features[6] = volume_ratio;
    features[7] = trend_score;

    // 3. Create Output Vector (สมมติโมเดลให้ค่า Probability ออกมา 1 ค่า)
    float output[1];

    // 4. Run Model
    if(OnnxRun(onnx_handle, ONNX_NO_CONVERSION, features, output)) {
        Print("Model Prediction: ", output[0]);
        // นำค่า output ไปเข้า Logic การเปิด Order ต่อไป
    } else {
        Print("ONNX Run Failed: Error ", GetLastError());
    }
}

void OnDeinit(const int reason) {
    if(onnx_handle != INVALID_HANDLE) {
        OnnxRelease(onnx_handle);
    }
}
```