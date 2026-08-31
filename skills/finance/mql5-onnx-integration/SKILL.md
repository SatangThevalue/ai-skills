---
name: mql5-onnx-integration
description: "MQL5 ONNX Integration: Load, configure, and execute machine learning ONNX models natively in MetaTrader 5."
---

# MQL5 ONNX Integration

MetaTrader 5 natively supports ONNX (Open Neural Network Exchange) models. This skill provides the workflow and code templates for running ML models (PyTorch, TensorFlow, Scikit-learn exported to `.onnx`) directly inside MQL5 Expert Advisors (EAs) or Indicators, without using DLLs or external Python sockets.

## 1. Required ONNX Workflow in MQL5

The lifecycle of an ONNX model in MQL5 consists of the following steps:
1. **Model Loading**: Initialize the model using `OnnxCreate` (from file) or `OnnxCreateFromBuffer` (from resource).
2. **Shape Configuration**: Define input and output tensor shapes using `OnnxSetInputShape` and `OnnxSetOutputShape`.
3. **Execution**: Run inference using `OnnxRun`.
4. **Cleanup**: Free memory using `OnnxRelease`.

## 2. Core MQL5 ONNX Functions

### `OnnxCreateFromBuffer` (Recommended for EAs)
Loads a model embedded directly into the EA's executable via `#resource`.
```cpp
long OnnxCreateFromBuffer(
   const uchar& buffer[], // Model as resource byte array
   uint flags             // ONNX_DEFAULT, ONNX_DEBUG_LOGS
);
```

### `OnnxSetInputShape` & `OnnxSetOutputShape`
Required to define the dimensions of the tensors if the ONNX model has dynamic axes (like variable batch size).
```cpp
bool OnnxSetInputShape(long onnx_handle, long input_index, const long& shape[]);
bool OnnxSetOutputShape(long onnx_handle, long output_index, const long& shape[]);
```

### `OnnxRun`
Executes the model. The input matrices/vectors MUST be of type `float` (`matrixf`, `vectorf`) if the ONNX model expects float32.
```cpp
bool OnnxRun(
   long onnx_handle, 
   ulong flags, // ONNX_NO_CONVERSION, ONNX_DEBUG_LOGS
   ...          // input1, input2, output1, output2 (must match model signature)
);
```

## 3. Standard Template: Running ONNX in an EA

Here is a robust template for embedding and executing an ONNX model inside an EA.

```cpp
//+------------------------------------------------------------------+
//|                                                   ONNX_Agent.mq5 |
//+------------------------------------------------------------------+
#property strict

// 1. Embed the ONNX model into the EA
#resource "Python/model.onnx" as uchar ExtModel[]

// 2. Define Model Shapes (Batch Size = 1)
const long ExtInputShape[]  = {1, 10, 4}; // Example: 1 batch, 10 time steps, 4 features (OHLC)
const long ExtOutputShape[] = {1, 1};     // Example: 1 batch, 1 output (Prediction)

long onnx_handle = INVALID_HANDLE;

//+------------------------------------------------------------------+
//| Expert initialization function                                   |
//+------------------------------------------------------------------+
int OnInit()
  {
   // 3. Create ONNX Session
   onnx_handle = OnnxCreateFromBuffer(ExtModel, ONNX_DEFAULT);
   if(onnx_handle == INVALID_HANDLE)
     {
      Print("OnnxCreateFromBuffer failed, error: ", GetLastError());
      return(INIT_FAILED);
     }

   // 4. Set Shapes
   if(!OnnxSetInputShape(onnx_handle, 0, ExtInputShape))
     {
      Print("OnnxSetInputShape failed, error: ", GetLastError());
      return(INIT_FAILED);
     }
     
   if(!OnnxSetOutputShape(onnx_handle, 0, ExtOutputShape))
     {
      Print("OnnxSetOutputShape failed, error: ", GetLastError());
      return(INIT_FAILED);
     }

   return(INIT_SUCCEEDED);
  }

//+------------------------------------------------------------------+
//| Expert deinitialization function                                 |
//+------------------------------------------------------------------+
void OnDeinit(const int reason)
  {
   // 5. Cleanup
   if(onnx_handle != INVALID_HANDLE)
     {
      OnnxRelease(onnx_handle);
      onnx_handle = INVALID_HANDLE;
     }
  }

//+------------------------------------------------------------------+
//| Expert tick function                                             |
//+------------------------------------------------------------------+
void OnTick()
  {
   // 6. Prepare Input Data (Must match ExtInputShape)
   matrixf input_data(10, 4); 
   // ... [Fill input_data with normalized OHLC float values] ...
   
   // 7. Prepare Output Vector
   vectorf output_data(1);
   
   // 8. Run Inference
   // Use ONNX_NO_CONVERSION to avoid automatic double-to-float overhead 
   // if you are already passing float matrices (matrixf/vectorf).
   if(!OnnxRun(onnx_handle, ONNX_NO_CONVERSION, input_data, output_data))
     {
      Print("OnnxRun failed, error: ", GetLastError());
      return;
     }
     
   // 9. Use Prediction
   float prediction = output_data[0];
   Print("Model Prediction: ", prediction);
  }
```

## 4. Best Practices & Pitfalls

1. **Data Types (Float vs Double)**:
   MQL5 uses `double` for prices natively. Most ML models (PyTorch/TensorFlow) export inputs as `float32`.
   - **Pitfall**: Passing a `matrix` (double) to `OnnxRun` when the model expects floats will incur an implicit conversion cost or fail. 
   - **Solution**: Always convert price data to `matrixf` or `vectorf` manually before passing to `OnnxRun`, and use the `ONNX_NO_CONVERSION` flag.
2. **Normalization**:
   Models are trained on normalized data (e.g., Z-score, MinMax). You MUST replicate the EXACT same normalization logic in MQL5 before passing data to `OnnxRun`, otherwise the model output will be garbage. Store mean/std values as constants or input parameters in the EA.
3. **Dynamic Batch Sizes**:
   If you exported your ONNX model with a dynamic batch axis (e.g., `batch_size=?`), you MUST call `OnnxSetInputShape` and `OnnxSetOutputShape` in `OnInit` to lock the batch size to `1` for live trading. If the model was exported with static shapes, setting shapes might not be strictly necessary, but it is best practice.
4. **Memory Leaks**:
   Always call `OnnxRelease(onnx_handle)` in `OnDeinit`. Failing to do so can cause the MT5 terminal to leak memory on recompilation or chart changes.
5. **Debugging**:
   If the model fails to load or run, create the model using the `ONNX_DEBUG_LOGS` flag. Check the "Experts" tab in MT5 for detailed ONNX Runtime backend errors (e.g., dimension mismatch).