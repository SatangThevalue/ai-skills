---
name: google-adk
description: Use when building multi-agent systems with Google's Agent Development Kit (ADK), configuring agents, tools, workflows, state, and sessions.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [google-adk, agents, multi-agent, framework, gemini, google-cloud]
    related_skills: [agent-frameworks-integration, plan]
---

# Google ADK (Agent Development Kit) Workflow

## Overview
Google's Agent Development Kit (ADK) is an open-source, code-first framework designed for building, evaluating, and deploying multi-agent systems. It treats agents as structured software components rather than simple prompt chains. It features first-class orchestration (hierarchical/dynamic), native Agent2Agent (A2A) protocol support, structured context management, and deep observability via ADK Studio.

## When to Use
- Building multi-agent workflows requiring sequential, parallel, or loop structures.
- Integrating Gemini models (or other models via LiteLLM) in a code-first, structured environment.
- Requiring deep tracing of agent decisions, prompts, state updates, and latency (via ADK Studio).
- Implementing Agent-to-Agent (A2A) communication across different frameworks.

### Do Not Use For:
- Simple, single-prompt chat scripts with no routing or state requirements.
- Environments where installing the ADK Python/Java/Go/TypeScript SDK is restricted.

## Setup & Preparation

### 1. Installation
Install the Google ADK Python SDK (typically done within a virtual environment):
```bash
pip install google-adk
```
Ensure you have the required API key for Gemini set in your environment (e.g., `GEMINI_API_KEY`) or GCP Vertex AI authenticated.

### 2. Project Structure
ADK prefers a structured layout. Create a clean project module:
```
my_agent_project/
├── main.py
├── agents.py
├── tools.py
└── README.md
```

## Core Implementation Patterns

### 1. Defining Agents and Tools
Agents are instances of `LlmAgent`. Tools are normal Python functions that accept a `ToolContext` argument.

```python
from google.adk.agents import LlmAgent
from google.adk.tools import ToolContext

# Tools use docstrings for LLM selection
def exit_loop(tool_context: ToolContext) -> dict:
    """Call this when the draft is good enough to publish."""
    tool_context.actions.escalate = True
    tool_context.actions.skip_summarization = True
    return {}

writer_agent = LlmAgent(
    name="writer_agent",
    model="gemini-2.5-flash",
    instruction="You write short popular-science articles. Write about 200 words.",
    output_key="draft",
)

critic_agent = LlmAgent(
    name="critic_agent",
    model="gemini-2.5-flash",
    instruction="You are a sharp editor. Review the draft. If good, call exit_loop.",
    tools=[exit_loop],
    output_key="critique",
)
```

### 2. Deterministic Orchestration
Use structured wrapper agents to control flow:
- `SequentialAgent`: Runs sub-agents in a fixed sequence.
- `ParallelAgent`: Runs sub-agents concurrently.
- `LoopAgent`: Runs sub-agents iteratively up to `max_iterations` or until a tool escalates.

```python
from google.adk.agents import LoopAgent, SequentialAgent

refinement_loop = LoopAgent(
    name="refinement_loop",
    sub_agents=[writer_agent, critic_agent],
    max_iterations=3,
)

root_agent = SequentialAgent(
    name="writing_pipeline",
    sub_agents=[theme_agent, refinement_loop],
)
```

### 3. State Management & Instruction Templating
State is a key-value store shared across a session. Agents write to the key specified in `output_key`. Other agents read this data using curly braces `{key}`:
- `{topic}`: Required key. If not present in state, execution will error out.
- `{critique?}`: Optional key. Evaluates to empty string if not present in state.

```python
# In writer_agent instruction:
# "Write a short article about {topic}. Review previous feedback: {critique?}"
```

### 4. Runner & Session Service
To run the agent, initialize a `Runner` with a `SessionService` (like `InMemorySessionService` for local dev):

```python
import asyncio
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner

async def main():
    session_service = InMemorySessionService()
    runner = Runner(
        agent=root_agent,
        app_name="writing_assistant",
        session_service=session_service,
    )
    
    session_id = "session_1"
    user_id = "user_123"
    
    await session_service.create_session(
        app_name="writing_assistant",
        user_id=user_id,
        session_id=session_id,
    )
    
    async for event in runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message="Let's write about quantum computing.",
    ):
        print(f"Event: {event}")
        
    # Extract output state
    session = await session_service.get_session(
        app_name="writing_assistant",
        user_id=user_id,
        session_id=session_id,
    )
    print("Final Draft:", session.state.get("draft"))

if __name__ == "__main__":
    asyncio.run(main())
```

### 5. Memory Management (Cross-Session)
Archiving finished session state to long-term memory:
```python
async def archive_run(callback_context):
    await callback_context.add_session_to_memory()
    return None
```
Retrieving memory from a tool:
```python
from google.adk.tools import load_memory
# Pass load_memory in tools list and instruct the agent to use it
```

## Running ADK Studio
To observe execution paths, prompt history, state transitions, and latency, launch ADK Studio in your project root:
```bash
adk web
```
This starts a local dashboard where you can step through Events and inspect the Traces/Graph.

## Common Pitfalls
1. **Model tool-calling docs:** ADK agents select tools based on docstrings. If your docstrings are ambiguous or missing, the model will call tools incorrectly.
2. **Infinite loops:** If `LoopAgent` does not hit the stop condition, it runs up to `max_iterations`. Always set a safe limit for `max_iterations` and implement a clear exit tool using `tool_context.actions.escalate = True`.
3. **Template errors:** Using `{key}` in instruction templates raises errors if the key is not initialized in the state yet. Use `{key?}` for optional keys.
4. **Skip Summarization:** For exit or utility tools that output nothing, set `tool_context.actions.skip_summarization = True` to avoid redundant LLM calls.

## Verification Checklist
- [ ] ADK SDK installed (`google-adk`) and python import works.
- [ ] API keys (`GEMINI_API_KEY` etc.) exported.
- [ ] Exit tools explicitly set `tool_context.actions.escalate = True`.
- [ ] Optional state references in instructions formatted with `?` (e.g. `{critique?}`).
- [ ] Local dashboard verified via `adk web` during trial runs.
