---
name: agent-frameworks-integration
description: Use when designing, building, or orchestrating multi-agent systems using Google ADK, Agent-to-Agent (A2A) protocol, Microsoft Agent Framework, Deep Agents (LangGraph/LangChain), and integrating them with n8n via Model Context Protocol (MCP).
version: 1.0.0
author: Tonthong
license: MIT
metadata:
  hermes:
    tags: [agents, a2a, adk, microsoft-agent, deep-agents, langgraph, n8n, mcp, fastmcp]
    related_skills: [langgraph-development, deep-agents-python, fastmcp]
---

# Multi-Agent Frameworks Integration (ADK, A2A, MS Agent, Deep Agent, n8n)

This skill provides patterns, architecture, and code templates for building and orchestrating AI agents across **Google ADK**, **A2A (Agent-to-Agent)**, **Microsoft Agent Framework**, **Deep Agents (LangGraph)**, and calling them from external workflow tools like **n8n** using **FastMCP**.

---

## When to Use
- Building enterprise-grade multi-agent architectures that span multiple frameworks.
- Deploying peer-to-peer agent networks using the **Agent2Agent (A2A)** protocol.
- Organizing multiple agent platforms inside a single monorepo safely without dependency hell.
- Exposing LangGraph, ADK, or Microsoft Agents to n8n using Model Context Protocol (MCP).

---

## 🏛️ Monorepo Project Structure

Since Google ADK, Microsoft Agent Framework, and LangGraph/LangChain have heavy and sometimes conflicting dependencies, managing them in a single Python environment is risky. Use **`uv` Workspaces** to enforce package isolation while keeping code in a single repository.

### Directory Layout
```text
my-agent-monorepo/
├── pyproject.toml                  # Roots workspace configuration
├── uv.lock                         # Single shared lockfile (uv manages constraints)
├── apps/
│   ├── google_adk_agent/           # Google ADK agent service
│   │   ├── pyproject.toml
│   │   └── main.py
│   ├── ms_agent_service/           # Microsoft Agent Framework service
│   │   ├── pyproject.toml
│   │   └── main.py
│   ├── langgraph_agent/            # LangGraph / Deep Agents service
│   │   ├── pyproject.toml
│   │   └── main.py
│   └── mcp_gateway/                # FastMCP gateway exposing A2A/ADK to n8n
│       ├── pyproject.toml
│       └── main.py
```

### Root `pyproject.toml`
```toml
[tool.uv]
workspace = { members = ["apps/*"] }
```

### App-specific `pyproject.toml` (e.g., LangGraph Agent)
```toml
[project]
name = "langgraph-agent"
version = "0.1.0"
dependencies = [
    "langgraph>=0.4.0",
    "deepagents>=0.1.0",
    "a2a-sdk>=1.0.1",
    "httpx>=0.27.0"
]
```

---

## 🛠️ Framework Implementations

### 1. Google ADK Agent (Agent Development Kit)
Google's code-first framework designed for Gemini.

```python
# apps/google_adk_agent/main.py
import asyncio
from google.adk import Agent
from google.adk.runners import Runner

# Initialize the core ADK agent
adk_agent = Agent(
    name="research_agent",
    model="gemini-2.5-flash",
    instruction="You are a research agent. Perform the requested task step-by-step."
)

async def main():
    # Execute the agent locally
    runner = Runner()
    session = runner.create_session(adk_agent)
    result = await session.run("Summarize the Agent2Agent protocol.")
    print(result.text)

if __name__ == "__main__":
    asyncio.run(main())
```

### 2. Microsoft Agent Framework (MAF)
The unified successor to AutoGen v0.4, supporting both .NET and Python.

```python
# apps/ms_agent_service/main.py
import asyncio
from agent_framework import Agent, tool
from agent_framework.openai import OpenAIChatCompletionClient
from typing import Annotated
from pydantic import Field

@tool(approval_mode="never_require")
def fetch_database_records(query: str) -> str:
    """Simulate database lookup."""
    return f"Records for: {query} -> Active status verified."

async def main():
    # Initialize the client (OpenAI or Azure Foundry compatible)
    client = OpenAIChatCompletionClient(model="gpt-4o")
    
    ms_agent = Agent(
        client=client,
        name="DBAgent",
        instructions="You are a database query assistant. Utilize your tools.",
        tools=[fetch_database_records]
    )
    
    result = await ms_agent.run("Verify status for customer 1042.")
    print(f"Agent Response: {result}")

if __name__ == "__main__":
    asyncio.run(main())
```

### 3. Deep Agents (LangGraph)
LangChain's opinionated agent harness running on LangGraph state machines.

```python
# apps/langgraph_agent/main.py
from deepagents import create_deep_agent
from langchain_core.tools import tool

@tool
def calculate_growth_rate(revenue: float, cost: float) -> float:
    """Calculate the operational profit margin percentage."""
    return ((revenue - cost) / revenue) * 100

# Create deep agent (comes with planning & execution loops out of the box)
deep_agent = create_deep_agent(
    model="openai:gpt-4o",
    tools=[calculate_growth_rate],
    system_prompt="You are a CFO assistant. Report values as percentages."
)

if __name__ == "__main__":
    response = deep_agent.invoke({"messages": "Our revenue was 150000 and cost was 90000. Calculate profit margin."})
    print(response["messages"][-1].content)
```

---

## 🔗 Framework Integration via A2A Protocol

The **Agent2Agent (A2A)** protocol enables agents from different frameworks to communicate via standard HTTP endpoints and JSON contracts.

### A2A Adapter for LangGraph
To expose a LangGraph or custom agent over the A2A network, subclass `AgentExecutor`:

```python
# apps/langgraph_agent/a2a_adapter.py
import logging
from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.server.tasks import TaskUpdater
from a2a.types import TaskState, Part, TextPart
from a2a.utils import new_agent_text_message, new_task
from a2a.utils.errors import ServerError

class LangGraphA2AExecutor(AgentExecutor):
    def __init__(self, langgraph_app):
        self.agent = langgraph_app

    async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
        query = context.get_user_input()
        task = context.current_task or new_task(context.message)
        
        # Enqueue the working task if it's new
        if not context.current_task:
            await event_queue.enqueue_event(task)
            
        updater = TaskUpdater(event_queue, task.id, task.context_id)
        
        try:
            # Stream the LangGraph execution (astream handles async generation)
            async for event in self.agent.astream(
                {"messages": [("user", query)]},
                config={"configurable": {"thread_id": task.context_id}}
            ):
                # Process events and send updates over A2A EventQueue
                if "messages" in event:
                    msg = event["messages"][-1]
                    await updater.update_status(
                        TaskState.working,
                        new_agent_text_message(msg.content, task.context_id, task.id)
                    )
            
            # Mark task complete
            await updater.complete()
            
        except Exception as e:
            await updater.update_status(TaskState.failed, new_agent_text_message(str(e), task.context_id, task.id))
            raise ServerError() from e
```

---

## 🌐 External Calling & n8n Integration

To allow external systems like **n8n** to interact with your agent mesh, use **FastMCP** as an API gateway. FastMCP standardizes agent access under the Model Context Protocol, which n8n consumes natively.

```
┌─────────┐      MCP over SSE      ┌────────────────┐      A2A / HTTP      ┌─────────────────────┐
│   n8n   │───────────────────────▶│ FastMCP Gateway│─────────────────────▶│  A2A Exposed Agent  │
│  Node   │      (HTTP / SSE)      │  (Port 8000)   │      (Port 8001)     │  (LangGraph or ADK) │
└─────────┘                        └────────────────┘                      └─────────────────────┘
```

### 1. FastMCP Gateway Code
Create a gateway server that lists and calls your A2A-exposed agents.

```python
# apps/mcp_gateway/main.py
from mcp.server.fastmcp import FastMCP
import httpx
import uvicorn

mcp = FastMCP("Agent Hub Bridge")

A2A_AGENT_URL = "http://localhost:8001/a2a/execute"

@mcp.tool()
async def trigger_a2a_agent(prompt: str, session_id: str = "default-session") -> str:
    """
    Sends a task execution prompt to the A2A-exposed agent.
    
    Args:
        prompt: The task instruction for the agent.
        session_id: Session identifier to maintain memory context.
    """
    payload = {
        "message": {
            "content": {"parts": [{"root": {"text": prompt}}]},
            "context_id": session_id
        }
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(A2A_AGENT_URL, json=payload, timeout=60.0)
        if response.status_code != 200:
            return f"A2A Server Error: {response.text}"
        
        # Parse standard A2A response contract
        data = response.json()
        return data.get("result", {}).get("text", "Execution completed.")

if __name__ == "__main__":
    # Expose MCP server over HTTP SSE for n8n compatibility
    # Always run SSE servers on 0.0.0.0 when hosting on VPS
    uvicorn.run("main:mcp.sse", host="0.0.0.0", port=8000)
```

### 2. Wiring to n8n
1. Open your n8n workflow.
2. Add an **MCP Client** node.
3. Configure the Transport as **SSE (Server-Sent Events)**.
4. Set the URL to: `http://<your-vps-ip>:8000/sse`.
5. The `trigger_a2a_agent` tool will auto-register. n8n agents can now dynamically call your A2A agent mesh.

---

## Common Pitfalls
1. **`graph.stream` inside Async Methods**: Calling LangGraph's synchronous `.stream()` inside async A2A functions blocks the event loop. Always use `.astream()` for async streaming.
2. **Missing `0.0.0.0` host binding**: Exposing FastMCP or A2A servers inside Docker/VPS without binding to `0.0.0.0` prevents external webhooks and n8n from reaching the ports.
3. **Dependency Clashes**: Trying to install both `google-adk` and `azure-identity` (for MAF) in a single virtual environment can trigger version conflicts. Enforce segregation using `uv` workspace directories.

---

## Verification Checklist
- [ ] Mono-repository packages declare isolation under `/apps/` via `uv` workspace.
- [ ] FastMCP gateway binds to `0.0.0.0` when running inside the VPS.
- [ ] The A2A executor maps incoming prompts safely to `astream()` loops.
- [ ] n8n's MCP Node connects successfully to `http://<vps-ip>:<port>/sse`.
