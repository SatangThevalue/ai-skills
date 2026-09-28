# FastMCP v4+ Integration & RBAC Patterns

## 1. Correct Mounting Syntax (FastMCP >= v4.0.0)
Older versions of `fastmcp` used `app.mount("/mcp", mcp.asgi_app)` or `mcp.get_starlette_app()`. In FastMCP v4+, the instance provides its own `.mount()` method which handles SSE transport setup internally onto an existing FastAPI/Starlette app:

```python
from fastapi import FastAPI
from fastmcp import FastMCP

app = FastAPI()
mcp = FastMCP("FinanceOS")

# Tools
@mcp.tool()
def example_tool() -> str:
    return "OK"

# Correct mounting pattern for v4+
mcp.mount(app, path="/mcp") # Automatically creates SSE and POST message endpoints under /mcp
```

## 2. Role-Based Access Control (RBAC) via Multiple Instances
To restrict which AI agents can perform write operations (e.g., executing trades) versus read-only queries (e.g., getting balances), instantiate multiple `FastMCP` objects, register specific tools to each, and mount them on separate endpoints within the same FastAPI app.

```python
# 1. Full Access (Admin / Trusted Agents)
mcp_full = FastMCP("Server-Full")
@mcp_full.tool()
def execute_trade(asset: str, qty: int): 
    pass # write operation

# 2. Read-Only Access (External / Reporting Agents)
mcp_read = FastMCP("Server-ReadOnly")
@mcp_read.tool()
def get_balances() -> dict: 
    pass # read operation

# Mount to the same FastAPI app on different paths
mcp_full.mount(app, path="/mcp/full")
mcp_read.mount(app, path="/mcp/read")
```
This ensures that an agent connecting to `/mcp/read` simply does not have the tools available in its schema to perform destructive or sensitive actions, eliminating prompt-injection risks at the transport layer.