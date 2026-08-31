# FastMCP Fast Integration Patterns

## Bypassing get_starlette_app() Attribute Errors
When mounting a FastMCP `mcp` instance onto an existing `FastAPI` app in newer `mcp` versions (where `.get_starlette_app()` was removed), do NOT use manual routing logic. Try to access the private `.get_starlette_app` or `._app` directly with a broad fallback.

```python
from fastapi import FastAPI
from mcp.server.fastmcp import FastMCP

app = FastAPI()
mcp = FastMCP("My_MCP_Server")

@mcp.tool()
def generate_podcast_tts(text: str) -> str:
    return "ok"

# FastMCP SSE mounting
try:
    if hasattr(mcp, 'get_starlette_app'):
        app.mount("/sse", getattr(mcp, 'get_starlette_app')())
    elif hasattr(mcp, '_app'):
        app.mount("/sse", mcp._app)
except Exception as e:
    print(f"Warning: MCP SSE mounting failed: {e}")
```