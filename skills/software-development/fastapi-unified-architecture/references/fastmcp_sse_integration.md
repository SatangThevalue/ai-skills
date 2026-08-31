# FastMCP 1.x Upgrade & SSE Integration Patterns

When implementing Model Context Protocol (MCP) servers within a FastAPI/Starlette application using the `mcp` Python SDK (specifically the `FastMCP` wrapper), be aware of the following architectural shifts in `mcp>=1.0.0`:

## 1. Removal of `get_starlette_app()`
In early pre-1.0 versions of FastMCP, the SDK provided a `get_starlette_app()` method to easily mount the MCP SSE transport onto an existing FastAPI app. 
- **Change:** This method has been refactored or removed entirely in newer versions.
- **Result:** Attempting `app.mount("/sse", mcp.get_starlette_app())` will raise an `AttributeError`.

## 2. Recommended Integration Strategy
Do not attempt to force the FastMCP instance into a Starlette sub-mount by manually constructing the `SseServerTransport` unless you deeply understand the internal `_mcp_server` object graph.
Instead, treat the MCP server and the FastAPI server as separate concerns that can either be run concurrently via CLI tools or explicitly configured via `mcp.tool()` decorators.

### Correct Tool Registration
```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("My_MCP_Server")

@mcp.tool()
def my_tool(param: str) -> str:
    return f"Processed {param}"
```

### Safe Mounting (Graceful Fallback)
If you are writing a unified `app.py` that must serve both Web/API traffic and MCP traffic simultaneously, use `hasattr` to prevent application crashes when the underlying SDK version shifts:
```python
# Try to mount if the version supports it, otherwise ignore and let the web app run
try:
    if hasattr(mcp, 'get_starlette_app'):
        app.mount("/mcp", mcp.get_starlette_app())
except Exception as e:
    print(f"Warning: MCP SSE mounting skipped: {e}")
```
For production MCP deployments, run the FastMCP app directly using the provided CLI (`mcp run app.py`) rather than wrapping it in Uvicorn.