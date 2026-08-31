---
name: mlflow-dataset-tracking
description: Guide and implementation patterns for measuring, tracking, and versioning datasets using MLflow (mlflow.data API).
---
# MLflow Dataset Tracking & Measurement

This skill covers how to measure, track, and apply dataset versioning using MLflow's `mlflow.data` API (Available in MLflow 2.4.0+ / 3.x).

## 1. Core Concepts
In MLOps, tracking *what* data a model was trained or evaluated on is as important as tracking hyperparameters. MLflow extracts four main components from a dataset:
1. **Source:** Where the data lives (e.g., S3 URI, DB query, local file path, Hugging Face repo).
2. **Digest (Hash):** A cryptographic hash of the dataset's contents. If the data changes, the digest changes (crucial for reproducibility).
3. **Schema:** The columns, features, and data types (e.g., Integer, String, Tensor).
4. **Context:** How the data is used in the run (e.g., `train`, `validation`, `test`, `eval`).

## 2. How to Apply (Practical Implementations)

### A. Tracking a Pandas DataFrame
When dealing with tabular data, log the pandas dataframe directly.
```python
import pandas as pd
import mlflow

# 1. Load data
df = pd.read_csv("s3://my-bucket/train_data.csv")

# 2. Construct MLflow Dataset (calculates digest & schema)
dataset = mlflow.data.from_pandas(
    df, 
    source="s3://my-bucket/train_data.csv", 
    name="customer_churn_training",
    targets="churn" # specify the target column
)

# 3. Log it to the run
with mlflow.start_run():
    mlflow.log_input(dataset, context="training")
    # ... train model ...
```

### B. Tracking a Hugging Face Dataset (GenAI / NLP)
For LLMs or Deep Learning models, Hugging Face datasets are native to MLflow.
```python
from datasets import load_dataset
import mlflow

hf_dataset = load_dataset("rotten_tomatoes", split="train")
dataset = mlflow.data.from_huggingface(hf_dataset, name="rotten_tomatoes_train")

with mlflow.start_run():
    mlflow.log_input(dataset, context="training")
```

### C. Using Logged Datasets for Evaluation (`mlflow.evaluate`)
You can use the dataset object directly in MLflow's evaluation API.
```python
import mlflow

eval_df = pd.read_csv("eval_data.csv")
eval_dataset = mlflow.data.from_pandas(eval_df, targets="label", name="monthly_eval_data")

with mlflow.start_run():
    mlflow.log_input(eval_dataset, context="testing")
    
    # Auto-evaluate against the dataset
    results = mlflow.evaluate(
        model="runs:/<RUN_ID>/model",
        data=eval_dataset,
        model_type="classifier",
        evaluators=["default"]
    )
```

## 3. Real-World Applications (Why do this?)
1. **Reproducibility Audits:** If a model behaves poorly in production, an AI Engineer can check the run in MLflow, look at the Data Digest, and verify if the data was corrupted or changed upstream.
2. **Data Drift Detection:** By comparing the schema and profile of the `testing` dataset logged today vs the `training` dataset logged 6 months ago, you can detect missing columns or altered types.
3. **Model Lineage (Governance):** For compliance (e.g., GDPR, AI Act), you can prove exactly which version of a dataset (via its Source and Hash) was used to produce a specific model version in the Model Registry.

## 4. E2E Workflow & Implementation Constraints (AI Engineer)
When building AI systems, track datasets and handle constraints using these rules:

### A. Training & Optimization (Phase 1-2)
- **Problem:** Data drift, concept drift, or missing features breaking the pipeline upstream.
- **Constraint/Condition:** NEVER train a model without verifying the dataset schema and signature first.
- **Technique:** Use `mlflow.data` to log the dataset digest. Use `infer_signature(X, y)` before `mlflow.log_model()` to enforce strict input/output shapes.

### B. Evaluation & Statistical Metrics (Phase 3)
- **Problem:** Over-optimizing for the wrong metric (e.g., chasing 99% accuracy on highly imbalanced fraud data where predicting 'no fraud' always yields 99%).
- **Constraint/Condition:** Select metrics based on business impact.
  - *Imbalanced Data (Fraud/Churn):* Track F1-Score, PR-AUC, and Recall. Accuracy is statistically irrelevant.
  - *Generative AI (LLMs):* Track Perplexity, ROUGE/BLEU (legacy), or use LLM-as-a-judge metrics via `mlflow.evaluate`.
- **Technique:** Bind the evaluation dataset explicitly using `mlflow.evaluate(data=dataset, targets="target_col", model_type="...")`.

### C. Deployment & Serving (Phase 4)
- **Problem:** Serving environments crash due to mismatched dependencies or unexpected input data types (e.g., receiving string '10' instead of int 10).
- **Constraint/Condition:** Production code (FastAPI/Docker) must NEVER parse data manually if it breaks the registered model signature.
- **Technique:** 
  1. Build APIs pulling directly from Model Registry Aliases (e.g., `models:/MyModel@champion`).
  2. Use Pydantic models in FastAPI that exactly match the MLflow Model Signature to guarantee type safety before inference.

## 5. Agent Instructions
- Always use `mlflow.data.from_pandas()` or equivalent when tracking data. 
- NEVER just log dataset paths as text/parameters (e.g., `mlflow.log_param("data_path", "...")`). Always use `mlflow.log_input()` so MLflow can calculate the cryptographic digest and schema.
- Always provide a `context` (e.g., `"train"`, `"test"`) to distinguish multiple datasets in a single run.