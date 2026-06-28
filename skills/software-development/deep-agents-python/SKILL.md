---
name: deep-agents-python
description: Guide and best practices for using LangChain's Deep Agents framework (langchain-ai/deepagents), an opinionated agent harness built on LangGraph for long-horizon tasks.
---

# Deep Agents (Python)

**Deep Agents** (`deepagents`) is an open-source, batteries-included agent harness created by LangChain. It provides an opinionated but highly extensible framework for building AI agents that can handle long-horizon, multi-step tasks out of the box.

It sits on top of LangGraph and acts as a fully-featured alternative to the minimal `create_agent` from LangChain.

## Core Concepts

- **Opinionated Harness**: Comes pre-configured with middleware for planning, context management, memory, and delegation.
- **Model Agnostic**: Works with any LLM that supports tool calling (OpenAI, Anthropic, local models via Ollama/vLLM, etc.).
- **Sub-agents**: Agents can spawn child agents with isolated contexts to delegate sub-tasks.
- **Tools & Ecosystem**: Natively supports filesystem/shell operations, human-in-the-loop approvals, pluggable state stores, and **MCP (Model Context Protocol)** servers.
- **Composability**: Because it's built on LangGraph, any `CompiledStateGraph` can be passed as a sub-agent.

## Installation

```bash
uv add deepagents
```

*(Note: LangChain also provides a pre-built terminal coding agent based on this called Deep Agents Code: `curl -LsSf https://langch.in/dcode | bash`)*

## Quickstart

```python
from deepagents import create_deep_agent

# my_custom_tool must be a valid tool (e.g. @tool decorated function)
agent = create_deep_agent(
    model="openai:gpt-4o", # Replace with desired model string
    tools=[my_custom_tool],
    system_prompt="You are a specialized research assistant."
)

result = agent.invoke({"messages": "Research LangGraph and write a summary"})
```

## Security Philosophy

Deep Agents operates on a "trust the LLM" model. The framework assumes the agent will use the tools provided to it. 
**Best Practice:** Enforce security boundaries and permissions at the tool or sandbox level (e.g., using Vercel Sandbox, Daytona, or Modal), not via prompt instructions.

## Advanced Features

1. **MCP Integration**: Deep Agents natively supports loading and connecting to any Model Context Protocol server.
2. **Persistence & Memory**: Built-in mechanisms to offload tool outputs to disk and maintain cross-session recall.
3. **`deepagents-talon`**: A related local runtime host designed for long-running agents, including channel adapters (like WhatsApp) and cron capabilities.
4. **Prompt Caching**: Middleware available for prompt caching (e.g., AWS Bedrock) to optimize costs and latency.
