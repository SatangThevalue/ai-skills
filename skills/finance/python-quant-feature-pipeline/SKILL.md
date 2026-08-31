---
name: python-quant-feature-pipeline
description: "โค้ด Python สำหรับสร้าง Feature Pipeline (pandas-ta) และระบบ Feature Selection 4 ชั้น (Correlation, sklearn, LightGBM, SHAP) สำหรับ Quant Trading"
---

# Python Quant Feature Pipeline & Selection

สกิลนี้คือ **ภาคปฏิบัติ (Implementation)** ที่ต่อยอดจากสถาปัตยกรรมในสกิล `quant-feature-engineering` โดยใช้ Python, `pandas-ta`, `scikit-learn`, `lightgbm` และ `shap` 

แนวทางที่ดีที่สุดสำหรับการทำ Feature Engineering ระดับ Production ไม่ใช่แค่วิธีใดวิธีหนึ่ง แต่คือการใช้ Pipeline คัดกรอง 4 ชั้น:
`Generate Features` → `Correlation Analysis` → `sklearn Feature Selection` → `LightGBM Importance` → `SHAP Analysis` → `Final Feature Set`

---

## 1. Project Structure (โครงสร้างโปรเจกต์)

ควรแบ่งไฟล์ตามหมวดหมู่ของ Feature เพื่อไม่ให้โค้ดรก:
```text
src/
├── features/
│   ├── price.py
│   ├── trend.py
│   ├── momentum.py
│   ├── volatility.py
│   ├── volume.py
│   └── structure.py
├── pipelines/
│   └── feature_pipeline.py
├── selection/
│   ├── correlation.py
│   ├── sklearn_select.py
│   └── shap_select.py
└── train/
    └── train_lightgbm.py
```

---

## 2. Feature Generation Pipeline (ตัวอย่างโค้ด)

ต้องใช้ไลบรารี `pandas-ta` เป็นแกนหลัก:
```bash
pip install pandas-ta
```

### Price & Candle Features
```python
import numpy as np
import pandas as pd

def create_price_features(df):
    periods = [1, 3, 5, 10, 20, 50]
    for p in periods:
        df[f"ret_{p}"] = df["close"].pct_change(p)
    for p in [1, 5, 20]:
        df[f"log_ret_{p}"] = np.log(df["close"] / df["close"].shift(p))
    return df

def create_candle_features(df):
    df["body_size"] = abs(df["close"] - df["open"])
    df["upper_shadow"] = df["high"] - df[["open","close"]].max(axis=1)
    df["lower_shadow"] = df[["open","close"]].min(axis=1) - df["low"]
    
    candle_range = (df["high"] - df["low"]).replace(0, np.nan)
    df["body_ratio"] = df["body_size"] / candle_range
    return df
```

### Trend & Momentum Features (via pandas-ta)
```python
import pandas_ta as ta

def create_trend_features(df):
    df["EMA20"] = ta.ema(df["close"], length=20)
    df["EMA50"] = ta.ema(df["close"], length=50)
    df["EMA200"] = ta.ema(df["close"], length=200)

    df["ema20_50_gap"] = (df["EMA20"] - df["EMA50"]) / df["EMA50"]
    df["ema50_200_gap"] = (df["EMA50"] - df["EMA200"]) / df["EMA200"]

    adx = ta.adx(df["high"], df["low"], df["close"], length=14)
    df["ADX14"] = adx["ADX_14"]
    return df

def create_momentum_features(df):
    df["RSI14"] = ta.rsi(df["close"], length=14)
    df["RSI28"] = ta.rsi(df["close"], length=28)
    
    macd = ta.macd(df["close"])
    df["MACD"] = macd["MACD_12_26_9"]
    df["MACD_SIGNAL"] = macd["MACDs_12_26_9"]
    df["MACD_HIST"] = macd["MACDh_12_26_9"]
    return df
```

### Volatility, Volume & Structure Features
```python
def create_volatility_features(df):
    df["ATR14"] = ta.atr(df["high"], df["low"], df["close"], length=14)
    df["ATR100"] = ta.atr(df["high"], df["low"], df["close"], length=100)
    df["ATR_RATIO"] = df["ATR14"] / df["ATR100"]

    bb = ta.bbands(df["close"], length=20)
    df["BB_WIDTH"] = bb["BBU_20_2.0"] - bb["BBL_20_2.0"]
    return df

def create_volume_features(df):
    df["volume_ma20"] = df["tick_volume"].rolling(20).mean()
    df["volume_ratio"] = df["tick_volume"] / df["volume_ma20"]
    return df

def create_structure_features(df):
    rolling_high = df["high"].rolling(20).max()
    rolling_low = df["low"].rolling(20).min()
    df["donchian_position"] = (df["close"] - rolling_low) / (rolling_high - rolling_low)
    return df
```

### Master Pipeline & Labeling
```python
def build_feature_pipeline(df):
    df = create_price_features(df)
    df = create_candle_features(df)
    df = create_trend_features(df)
    df = create_momentum_features(df)
    df = create_volatility_features(df)
    df = create_volume_features(df)
    df = create_structure_features(df)
    return df

# ตัวอย่างการสร้าง Target Label (Predict อนาคต 5 แท่ง)
df["target"] = np.where(df["close"].shift(-5) > df["close"], 1, 0)
```

---

## 3. Production Feature Selection (ระบบคัดกรอง 4 ชั้น)

การมี 120 Features แล้วโยนเข้าโมเดลเลยมักจะเกิด Overfitting แนวทางสถาบันคือการคัดกรองตามลำดับนี้:

### Layer 1: Correlation Filter (ลบ Feature ซ้ำซ้อน)
```python
corr = X.corr().abs()
upper = corr.where(np.triu(np.ones(corr.shape), k=1).astype(bool))

# ลบ Feature ที่มีความสัมพันธ์กันเกิน 95%
drop_cols = [column for column in upper.columns if any(upper[column] > 0.95)]
X = X.drop(columns=drop_cols)
```

### Layer 2: sklearn Feature Selection (ความสัมพันธ์กับ Target)
เลือกใช้ **SelectFromModel** (แนะนำ) หรือ **Mutual Information**:
```python
from sklearn.feature_selection import SelectFromModel
from lightgbm import LGBMClassifier

model = LGBMClassifier(n_estimators=300)
model.fit(X, y)

selector = SelectFromModel(model, prefit=True)
X_selected = selector.transform(X)
```

### Layer 3 & 4: LightGBM Importance & SHAP Selection
หลังเทรนโมเดล ใช้ SHAP ดูว่า Feature ไหนมีอิทธิพลต่อทิศทางราคาจริงๆ:
```python
# pip install shap
import shap
import pandas as pd
import numpy as np

explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X)

importance = np.abs(shap_values).mean(axis=0)

feature_rank = pd.DataFrame({
    "feature": X.columns,
    "importance": importance
})
feature_rank = feature_rank.sort_values("importance", ascending=False)
```

---

## 4. สรุป Workflow คัดกรอง (The Funnel)

*(รายละเอียดการออกแบบฟีเจอร์แต่ละชั้นแบบละเอียด อ่านได้ที่ `quant-feature-design-document`)*

```text
Generate Features (120 Features)
         ↓
1. Correlation Filter (เหลือ 90 Features)
         ↓
2. Mutual Information / SelectFromModel (เหลือ 60 Features)
         ↓
3. LightGBM Importance (เหลือ 40 Features)
         ↓
4. SHAP Analysis (เหลือ 25-35 Features)
         ↓
Train Final Model -> Export ONNX
```

### Core Feature Set V1 (ชุดเริ่มต้นที่แนะนำ)
เมื่อคัดกรองแล้ว มักจะเหลือตัวท็อปๆ ประมาณ 15-30 Features เช่น:
`ret_5, ret_20, body_ratio, RSI14, RSI28, ADX14, ATR14, ATR_RATIO, MACD_HIST, ema20_50_gap, ema50_200_gap, BB_WIDTH, volume_ratio, donchian_position, trend_score, regime_score`

> 15-30 Features แรกก็เพียงพอที่จะสร้าง LightGBM V1 ที่มีคุณภาพได้ ก่อนจะขยายไป 80-150 Features และใช้ Optuna + Walk Forward Testing เพื่อหาชุด Feature ที่ดีที่สุดสำหรับ ONNX Deployment บน MT5 ต่อไปครับ