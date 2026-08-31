---
name: data-science-and-engineering
description: Principles, methods, techniques, and workflows for Data Science (DS) and Data Engineering (DE).
---
# Data Science and Data Engineering Workflows

This skill provides comprehensive frameworks, principles, and techniques for executing Data Engineering (DE) and Data Science (DS) tasks effectively. 

## 1. Role Distinctions
- **Data Engineer (DE)**: The builders. They focus on infrastructure, building robust, scalable data pipelines (ETL/ELT), designing data warehouses/lakes, and ensuring data quality, reliability, and availability.
- **Data Scientist (DS)**: The analysts/modelers. They focus on extracting insights, applying statistical analysis, machine learning (ML), and predictive modeling to solve business problems using the data prepared by DEs.

## 2. Data Engineering (DE)
### Core Principles
- **ETL vs. ELT**: Extract-Transform-Load (traditional, transform happens in memory/scripts) vs. Extract-Load-Transform (modern, leveraging cloud data warehouse compute like BigQuery/Snowflake for transformations).
- **Idempotency**: Data pipelines must produce the exact same results regardless of how many times they are run for a given time window. (Crucial for backfilling and retries).
- **Data Modeling**: Designing schemas for analytical querying. Use Dimensional Modeling (Kimball - Star/Snowflake Schema) or Data Vault.
- **DataOps**: Applying DevOps principles to data (CI/CD, automated testing, monitoring, version control).

### Methods & Techniques
- **Pipeline Architecture**: Batch processing (large-scale, scheduled runs via cron/Airflow) vs. Streaming processing (real-time, Kafka/Flink).
- **Data Quality & Contracts**: Validating schema, nulls, uniqueness, and distribution before loading (e.g., using `Great Expectations` or `dbt tests`).
- **Orchestration**: Managing complex job dependencies using DAGs (Directed Acyclic Graphs).

### Essential Tools
- **Languages**: SQL (Advanced), Python, Scala.
- **Compute/Transform**: Spark, dbt (Data Build Tool), Pandas.
- **Orchestration**: Airflow, Prefect, Dagster.
- **Storage**: PostgreSQL, Snowflake, BigQuery, S3/GCS.

## 3. Data Science (DS)
### Core Principles
- **CRISP-DM Framework**: The gold standard lifecycle: Business Understanding -> Data Understanding -> Data Preparation -> Modeling -> Evaluation -> Deployment.
- **Bias-Variance Tradeoff**: Balancing model complexity. High bias = Underfitting. High variance = Overfitting (memorizing training data but failing on new data).
- **Reproducibility**: Ensuring experiments, code, hyperparameters, and data versions are tracked (e.g., MLflow, DVC).

### Methods & Techniques
- **Exploratory Data Analysis (EDA)**: Profiling data, handling missing values, identifying outliers, and understanding statistical distributions using visualizations.
- **Feature Engineering**: Creating new variables to improve model performance (Encoding categoricals, scaling/normalization, binning, creating interaction terms).
- **Model Selection & Tuning**: Cross-validation (K-Fold), Grid Search, Random Search, Bayesian Optimization.
- **Evaluation Metrics**:
  - *Classification*: Accuracy, Precision, Recall, F1-Score, ROC-AUC.
  - *Regression*: RMSE (Root Mean Square Error), MAE (Mean Absolute Error), R-squared.

### Essential Tools
- **Languages**: Python, R.
- **Libraries**: Pandas, NumPy, Scikit-Learn, PyTorch, TensorFlow, XGBoost, LightGBM.
- **Environments/Tracking**: Jupyter Notebooks, MLflow, Weights & Biases (W&B).

## 4. Synergy: MLOps (Machine Learning Operations)
Where DE and DS meet to put models into production.
- **Continuous Training (CT)**: Automating the retraining of models when data drift or concept drift is detected.
- **Model Registry**: Centralized tracking of model versions and stages (Staging, Production, Archived).
- **Feature Stores**: Centralized repositories for curated, pre-computed ML features (bridges the gap between DE pipelines and DS model training).

## 5. Data Types, Usage Conditions & Splitting Strategies
Understanding how to handle and split different data types is critical to prevent data leakage and ensure reliable models.

### A. Tabular Data (Structured: Numerical/Categorical)
- **Usage Conditions:** Business metrics, customer profiles, transactions. Best modeled with Tree-based algorithms (XGBoost, LightGBM) or regressions.
- **Splitting Strategy:**
  - *Standard:* Random Split (e.g., 70% Train, 15% Val, 15% Test).
  - *Imbalanced Data:* Stratified Split (ensures the ratio of target classes remains the exact same across all splits, critical for fraud/churn).

### B. Time Series Data (Temporal)
- **Usage Conditions:** Stock prices, weather, sales forecasting. Models: ARIMA, Prophet, LSTMs, Transformers.
- **Splitting Strategy:** *NEVER use Random Split* (this causes data leakage/look-ahead bias, as the model will 'see the future').
  - *Chronological Split:* Train on the past, test on the future (e.g., Train: Jan-Oct, Val: Nov, Test: Dec).
  - *Cross-Validation:* Use TimeSeriesSplit (Rolling or Expanding Window).

### C. Unstructured Data (Images, Text, Audio)
- **Usage Conditions:** Computer vision, NLP, GenAI. Models: CNNs, LLMs, Vision Transformers.
- **Splitting Strategy:**
  - *Standard:* Random/Stratified Split.
  - *Group-based (GroupKFold):* If multiple instances belong to the same entity (e.g., 5 medical scans from Patient A), all data for Patient A MUST go into *either* train or test, never split across both, to prevent the model from memorizing the patient instead of the disease.

## 6. Agent Instructions (How to apply this skill)
When requested to perform DE or DS tasks, strictly adhere to the following:
1. **For DE Tasks**: Always verify data schemas first. Write idempotent scripts. Prefer SQL/dbt for heavy transformations where possible, or Pandas/PySpark for complex row-level logic. Implement robust error handling, logging, and data quality checks (asserts/tests).
2. **For DS Tasks**: Never skip EDA. Always split data (Train/Validation/Test) properly to prevent data leakage. Document business assumptions. Evaluate models using metrics appropriate for the specific business context (e.g., optimizing Recall for fraud detection). If requested, generate and save clear visualizations (.png/.jpg) using matplotlib/seaborn.
3. **Communication**: Use clear, concise markdown tables and bullet points to report data summaries, schema structures, and model evaluation metrics.