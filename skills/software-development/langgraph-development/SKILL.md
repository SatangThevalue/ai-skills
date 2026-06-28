---
name: langgraph-development
description: Best practices for building and tracing AI agents with LangGraph, Deep Agents, and MLflow.
---

# LangGraph & Deep Agents Development

This skill provides patterns for building stateful multi-actor AI applications using the LangChain ecosystem (LangGraph, Deep Agents) and tracing them with MLflow.

## 🏗️ Environment Setup
Prefer using `uv` for fast virtual environment creation and dependency management:
```bash
uv venv
source .venv/bin/activate
uv pip install langchain langchain-core langgraph langflow mlflow deepagents langchain-openai
```

## 🔍 Tracing with MLflow
MLflow natively supports LangChain/LangGraph tracing. This is critical for debugging complex agent reasoning steps, token usage, and tool invocations.
- **Enable Tracing:** Call `mlflow.langchain.autolog()` in the script before compiling or invoking the graph.
- **Start UI:** Run `mlflow ui --host 0.0.0.0 --port 5000`.

## 🚀 Deep Agents Framework
`deepagents` is LangChain's opinionated, batteries-included agent harness built on top of LangGraph.
- **Quickstart:** Use `from deepagents import create_deep_agent` to instantiate an agent that has built-in planning, context management, and delegation.
- **Composition:** Any custom LangGraph `CompiledStateGraph` can be passed as a sub-agent into a Deep Agent.

## ⚠️ Pitfalls & Constraints
- **Long-running Services:** When starting UI servers like `langflow run`, `mlflow ui`, or FastAPI `uvicorn`, ALWAYS use the terminal tool with `background=true` and `notify_on_complete=true`. Running them in the foreground will hang the terminal tool and result in a timeout error.
- **Host Binding on VPS:** When exposing UIs (MLflow, Langflow) on a remote VPS, explicitly bind to `0.0.0.0` (e.g., `--host 0.0.0.0`) so they are accessible externally, rather than defaulting to localhost.