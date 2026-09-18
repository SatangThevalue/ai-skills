# Execution Troubleshooting & Pitfalls

When deploying the Python Quant MLOps stack, you may encounter several environment and library-specific issues. Here are the proven resolutions derived from live VPS deployment:

## 1. MetaTrader5 Package on Linux VPS
**Error:** `No solution found when resolving dependencies... metatrader5 has no wheels with a matching platform tag`
**Cause:** The `MetaTrader5` Python package is built exclusively for Windows (`win_amd64`). It cannot be installed natively via `pip` on a Linux server.
**Resolution:** Maintain Separation of Concerns. Do not attempt to install or run MT5 on the Linux MLOps server. Train the model on Linux, export the `.onnx` file, and run the MQL5 EA on a separate Windows VPS.

## 2. Polars Compilation on Older CPUs
**Error:** `Illegal instruction (core dumped)` when importing or running `polars`.
**Cause:** Modern `polars` binaries require CPUs with `avx2` and `fma` instruction sets. Older VPS CPUs (e.g., Intel Xeon E5 v2 series) lack these.
**Resolution:** Install the legacy CPU compatible version: `uv pip install polars-lts-cpu`.

## 3. MLflow Local File Store Deprecation
**Error:** `MlflowException: The filesystem tracking backend (e.g., './mlruns') is in maintenance mode...`
**Cause:** MLflow restricts using the local file system for tracking by default in newer versions to force database migration.
**Resolution:** Set the environment variable before setting the tracking URI:
```python
import os
os.environ["MLFLOW_ALLOW_FILE_STORE"] = "true"
mlflow.set_tracking_uri("file://./mlruns")
```

## 4. LightGBM Pandas Object Type Error
**Error:** `ValueError: pandas dtypes must be int, float or bool. Fields with bad pandas dtypes: created_at: object`
**Cause:** Passing a pandas DataFrame to LightGBM `.fit()` that contains datetime or string columns.
**Resolution:** Explicitly drop all non-numeric columns (like `timestamp`, `created_at`, `source`, `timeframe`) before isolating `X_train`.

## 5. LightGBM ONNX Export Type Mismatch
**Error:** `Operator LgbmClassifier got an input with a wrong type <class 'skl2onnx.common.data_types.FloatTensorType'>.`
**Cause:** Importing `FloatTensorType` from `skl2onnx` instead of `onnxmltools` when converting a LightGBM model.
**Resolution:** 
```python
# WRONG
from skl2onnx.common.data_types import FloatTensorType

# RIGHT
from onnxmltools.convert.common.data_types import FloatTensorType
```

## 6. Prefect Ephemeral Server Timeout
**Error:** `RuntimeError: Timed out while attempting to connect to ephemeral Prefect API server.`
**Cause:** On low-resource VPS instances, the background Prefect daemon may fail to start within the 60s timeout window.
**Resolution:** For local testing or bypassing the daemon on low-spec machines, call the underlying function directly using the `.fn()` attribute: `my_prefect_task.fn(args)`.