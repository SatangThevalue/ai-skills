---
name: business-dss-development
description: Use when designing, building, or evaluating Business Decision Support Systems (DSS). Guides the architecture of data management, model management (optimization/ML), user interface, and integration of AI agents for data-driven business decisions.
version: 1.0.0
author: Tonthong
license: MIT
metadata:
  hermes:
    tags: [dss, software-development, optimization, python, fastapi, business-intelligence]
    related_skills: [fastapi, postgresql, excel-author, business-analyst]
---

# Business Decision Support Systems (DSS) Development

## Overview
A **Decision Support System (DSS)** is an interactive, computer-based system designed to help decision-makers compile useful information from raw data, documents, personal knowledge, and mathematical models to identify, analyze, and solve business problems.

This skill provides a structured methodology, architectural patterns, and practical code recipes for developing robust, scalable, and user-centric DSS applications.

---

## When to Use
- **Resource Allocation & Scheduling:** Planning workforce shifts, factory production lines, inventory replenishment, or logistics routing.
- **Financial Planning & Scenario Analysis:** Portfolio optimization, budget planning, dynamic pricing, and "what-if" simulations.
- **Strategic Decision Pipelines:** Combining predictive ML models with deterministic optimization solvers.
- **AI-Augmented DSS:** Embedding LLM agents to translate natural language questions into database queries or optimization constraints.

### Do NOT Use For:
- Simple CRUD dashboard applications without mathematical modeling, predictive ML, or complex rule-based logic.
- Real-time transactional processing (OLTP) systems that do not involve decision logic or analysis.

---

## DSS System Architecture
A modern DSS consists of three core components:

```
┌─────────────────────────────────────────────────────────┐
│              User Interface (Presentation)              │
│       Next.js + Tailwind (Charts) / Streamlit UI        │
└────────────┬───────────────────────────────▲────────────┘
             │ Run Solver / Scenario ASSumptions
             ▼                               │ Results & Sensitivity
┌────────────────────────────────────────────┴────────────┐
│               Model Management (Backend)                │
│    FastAPI + Solvers (PuLP, SciPy, Pyomo, SimPy)        │
└────────────┬───────────────────────────────▲────────────┘
             │ Fetch Data                    │ Write Scenarios
             ▼                               │
┌────────────────────────────────────────────┴────────────┐
│                Data Management (Storage)                │
│       PostgreSQL + TimescaleDB / ClickHouse / RAG       │
└─────────────────────────────────────────────────────────┘
```

### 1. Data Management (Data Tier)
- **Transactional Data:** PostgreSQL for storing master data, scenario configurations, and run results.
- **Analytical Data:** ClickHouse or PostgreSQL with analytical indexes for processing heavy aggregates.
- **Unstructured Data:** pgvector or vector databases for retrieving business policies, historical manuals, or market reports via RAG.

### 2. Model Management (Analytics Tier)
- **Optimization Engines:** Mathematical programming (Linear, Mixed-Integer, Non-Linear) using Python libraries:
  - `PuLP` / `Pyomo`: Modeling languages that interface with solvers (CBC, GLPK, Gurobi).
  - `SciPy.optimize`: For continuous optimization, curve fitting, and statistics.
- **Predictive Engines:** `scikit-learn`, `XGBoost`, or `LightGBM` for forecasting demand, prices, or churn.
- **Simulation Engines:** `SimPy` for discrete-event simulations (queue modeling, logistics delays) or Monte Carlo simulation libraries.

### 3. Presentation & Interaction (UI Tier)
- **What-If Control Panel:** Interactive inputs allowing users to adjust parameters (e.g., slider for labor rate, text box for supply constraints).
- **Comparative Visualizations:** Visualizing "Scenario A" vs "Scenario B" side-by-side using charts (bar, line, waterfall).

---

## Code Recipe: Optimization API with FastAPI & PuLP

Below is a production-grade FastAPI template implementing a Product Mix Optimization model. It solves for the optimal quantities of two products to produce, given resource constraints (labor, materials) and profit margins.

### 1. FastAPI Model & Controller (`app/main.py`)
```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import pulp

app = FastAPI(title="Business Decision Support Optimizer")

class OptimizerInput(BaseModel):
    prod_a_margin: float = Field(..., description="Profit margin for Product A (THB/unit)")
    prod_b_margin: float = Field(..., description="Profit margin for Product B (THB/unit)")
    labor_limit: float = Field(..., description="Max labor hours available")
    material_limit: float = Field(..., description="Max raw material available (kg)")
    labor_per_a: float = Field(..., description="Labor hours needed per unit of A")
    labor_per_b: float = Field(..., description="Labor hours needed per unit of B")
    material_per_a: float = Field(..., description="Material needed per unit of A (kg)")
    material_per_b: float = Field(..., description="Material needed per unit of B (kg)")

class OptimizerOutput(BaseModel):
    status: str
    optimal_profit: float
    units_a: float
    units_b: float
    labor_used: float
    material_used: float
    shadow_price_labor: float
    shadow_price_material: float

@app.post("/api/optimize", response_model=OptimizerOutput)
def optimize_production(data: OptimizerInput):
    # 1. Define Optimization Problem (Maximization)
    prob = pulp.LpProblem("Product_Mix_Optimization", pulp.LpMaximize)

    # 2. Decision Variables (Continuous, non-negative)
    x_a = pulp.LpVariable("Units_A", lowBound=0, cat='Continuous')
    x_b = pulp.LpVariable("Units_B", lowBound=0, cat='Continuous')

    # 3. Objective Function (Maximize Profit)
    prob += data.prod_a_margin * x_a + data.prod_b_margin * x_b, "Total_Profit"

    # 4. Constraints
    labor_constraint = (data.labor_per_a * x_a + data.labor_per_b * x_b <= data.labor_limit)
    material_constraint = (data.material_per_a * x_a + data.material_per_b * x_b <= data.material_limit)
    
    prob += labor_constraint, "Labor_Constraint"
    prob += material_constraint, "Material_Constraint"

    # 5. Solve Problem
    # Using default CBC solver packaged with PuLP
    solver = pulp.PULP_CBC_CMD(msg=False)
    status = prob.solve(solver)

    if pulp.LpStatus[status] != "Optimal":
        raise HTTPException(
            status_code=400, 
            detail=f"Solver failed to find an optimal solution. Status: {pulp.LpStatus[status]}"
        )

    # 6. Extract Sensitivity Metrics (Shadow Prices)
    # Shadow price indicates how much the objective function increases per unit increase in the constraint limit.
    shadow_labor = labor_constraint.pi if labor_constraint.pi is not None else 0.0
    shadow_material = material_constraint.pi if material_constraint.pi is not None else 0.0

    return OptimizerOutput(
        status=pulp.LpStatus[status],
        optimal_profit=float(pulp.value(prob.objective)),
        units_a=float(x_a.varValue),
        units_b=float(x_b.varValue),
        labor_used=float(data.labor_per_a * x_a.varValue + data.labor_per_b * x_b.varValue),
        material_used=float(data.material_per_a * x_a.varValue + data.material_per_b * x_b.varValue),
        shadow_price_labor=float(shadow_labor),
        shadow_price_material=float(shadow_material)
    )
```

---

## Best Practices for DSS Development

### 1. Robust Constraint Design (Soft Constraints)
In mathematical models, hard constraints (e.g. `Usage <= Limit`) can easily cause solver failures (`Infeasible`) if parameters shift.
- **Action:** Convert critical hard constraints into **Soft Constraints** by introducing penalty/violation variables:
  $$Usage - Overlimit\_Variable \le Limit$$
- Add $Overlimit\_Variable \times Penalty\_Weight$ to the cost minimization objective. This allows the solver to find a solution even if limits are exceeded, pointing out the exact bottleneck.

### 2. Scenario Versioning (What-If Analysis)
Users need to experiment without corrupting master data.
- **Database Schema Pattern:**
  - `scenario` table: `id`, `name`, `parent_scenario_id`, `created_at`, `status` (draft, active, archived).
  - `scenario_parameters` table: Key-value configurations specific to each scenario.
  - `scenario_results` table: Storing solver output corresponding to the scenario version.
- **Action:** Implement a "Clone & Modify" workflow.

### 3. Sensitivity Analysis Output
Always present business users with shadow prices (dual values) or sensitivity intervals:
- **Shadow Price:** "Adding 1 more hour of labor will increase our profit by 150 THB."
- **Slack Variables:** "We have 15 kg of unused raw material."
- Translate these technical solver variables into human-readable business copy.

---

## Common Pitfalls

1. **Treating Solvers as Black Boxes:** Failing to handle `Infeasible` or `Unbounded` solver states in API responses. Always validate input ranges before running solvers.
2. **Hardcoding Constants inside Model Code:** Labor availability, material costs, and exchange rates should be fed from database parameters, never hardcoded.
3. **Ignoring Optimization Run Time:** Complex models (e.g., large Mixed-Integer Programming with thousands of variables) can block the event loop in Node.js or Python.
   - **Fix:** Execute solvers asynchronously via task queues like **Celery** or **Prefect**, storing results in a DB upon completion and notifying the client via WebSockets or polling.

---

## Verification Checklist

- [ ] Optimization inputs and parameters are fully validated using Pydantic models.
- [ ] Solver status is explicitly checked, and non-optimal outcomes (Infeasible, Unbounded, Undefined) return detailed errors instead of failing silently.
- [ ] Scenarios are versioned in the database schema to enable What-If comparison.
- [ ] Sensitivity metrics (slack, shadow prices) are exposed to explain recommendations.
- [ ] Large optimization processes are decoupled from main thread requests (Celery/background task).
