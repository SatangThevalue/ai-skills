---
name: agent-frameworks-integration
description: "Use when designing, building, or orchestrating multi-agent systems via A2A or LangGraph."
version: 0.2.0
metadata:
  hermes:
    tags: [A2A, Multi-Agent, LangGraph, Architecture, Gateway]
    related_skills: [langgraph-development, hermes-agent]
---

# Multi-Agent Frameworks Integration (A2A & LangGraph)

This skill covers integrating Hermes with other AI agents and frameworks, specifically detailing the **A2A (Agent-to-Agent) Protocol** and how Hermes can act as an orchestrator or a worker node in a broader ecosystem (like LangGraph or CrewAI).

## When to Use
- When the user asks about "a2a", "agent-to-agent", or communicating with other AI systems.
- When designing architectures where Hermes needs to delegate tasks to an external server or framework.
- When exposing Hermes to be callable by other tools (Inbound API).

## Quick Reference
- **A2A Inbound (Callable Service):** Enable via `hermes gateway setup` -> A2A.
- **A2A Outbound (Calling Others):** Enable via `hermes tools enable a2a`.
- **A2A Tools:** `a2a_discover(url)`, `a2a_call(agent, message)`, `a2a_orchestrate(capability, message)`.
- **Framework Compatibility (CrewAI/LangGraph/AutoGen/CAMEL):** See [`references/framework-install-and-compatibility.md`](references/framework-install-and-compatibility.md) for unified venv setup, import syntax, and disk recovery.

## 1. A2A Protocol Overview

[A2A](https://a2a-protocol.org) is the open Agent2Agent protocol (v1.0, stewarded by the Linux Foundation) for communication between independent AI agents. 

Hermes supports A2A in **both directions**:
1. **Outbound (Client):** Hermes can call other A2A-compliant agents (LangChain, CrewAI, Google ADK) as tools.
2. **Inbound (Server):** Other frameworks can send HTTP requests (tasks) to your Hermes agent.

*Note: For multi-agent workflows on the **same machine**, prefer Hermes' built-in `delegate_task` or the `kanban` board feature. A2A is specifically for crossing process/machine/framework boundaries.*

## 2. Inbound A2A (Making Hermes Callable)

To allow external agents (or external scripts like a Node.js webhook) to send tasks to Hermes:

1. Enable the A2A platform in the gateway:
   ```bash
   hermes config set gateway.platforms.a2a.enabled true
   ```
2. Configure Security (Crucial for VPS):
   The server binds to `127.0.0.1` by default. To expose it remotely, you MUST set a bearer token and host in `.env` (or via Infisical).
   ```bash
   A2A_PEER_TOKENS="rese..."
   A2A_HOST="0.0.0.0"
   A2A_PORT="9900"
   ```
3. Endpoints exposed:
   - `GET /.well-known/agent-card.json` (Advertises skills and auth)
   - `POST /` (JSON-RPC 2.0 endpoint for `SendMessage`, `GetTask`, etc.)

## 3. Outbound A2A (Calling other Agents)

If you have another agent running on a different server (e.g., a dedicated research bot), you can configure Hermes to call it.

1. Enable the toolset for the platform you use (e.g., CLI or Telegram):
   ```bash
   hermes tools enable a2a --platform cli
   ```
2. Configure known peers in `~/.hermes/config.yaml`:
   ```yaml
   a2a_agents:
     researcher:
       url: "http://research-box.local:9900"
       auth: { type: bearer, token: "..." }
       timeout: 120
       capabilities: [web_search, research]
   ```
3. Use the tools: Hermes can now use `a2a_call(agent="researcher", message="Summarize arXiv today")` directly in the conversation.

## 4. Integration with LangGraph / Python Ecosystem

While A2A is the official protocol, if you are building complex state machines (e.g., with LangGraph) on the same VPS, you can integrate them via API:

1. Build a FastAPI/LangGraph endpoint.
2. Configure it as a known A2A peer in Hermes `config.yaml`.
3. Hermes can now delegate complex reasoning paths to your LangGraph implementation via `a2a_call`.

Alternatively, use the `execute_code` tool to let Hermes write and run LangGraph scripts directly.