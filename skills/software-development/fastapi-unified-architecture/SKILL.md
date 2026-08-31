---
name: fastapi-unified-architecture
description: Patterns for deploying FastAPI, Gradio, and MCP servers in a single script, especially on Google Colab.
---
# FastAPI Unified Architecture (API + UI + MCP)

Use this skill when building AI tools that require an API (for automation like n8n), a Web UI (for end-users), and an MCP server (for AI agents) simultaneously, particularly when deploying to Google Colab or single-container environments.

## Event Loop Freezing and Blocking I/O
FastAPI is asynchronous. If you run heavy, CPU-bound, synchronous tasks (like audio processing with `pedalboard` or `numpy`, or video rendering with `moviepy`) directly in a route handler or an `async` function, the entire server event loop will freeze. This causes API timeouts, prevents new connections, and crashes the app.

**Fix:** Wrap CPU-heavy synchronous calls in `asyncio.to_thread()`.
```python
# Helper to run blocking processing in a thread
async def process_audio_safely(audio_data):
    return await asyncio.to_thread(synchronous_heavy_processing, audio_data)
```
*(Note: Very fast synchronous operations like small numpy array concatenations or basic file I/O `sf.write` usually do not need thread offloading, but multi-second operations absolutely do).*

## The All-in-One Architecture
Run everything through a single `uvicorn` instance on one port. This reduces overhead and simplifies deployment.

1. **FastAPI Base:** `app = FastAPI()`
2. **MCP Server:** 
   ```python
   from mcp.server.fastmcp import FastMCP
   mcp = FastMCP("My_Server")
   # Mount SSE endpoint for Agents to connect to
   app.mount("/sse", mcp.get_starlette_app())
   ```
3. **Gradio UI:** 
   ```python
   import gradio as gr
   with gr.Blocks() as demo:
       ...
   # Mount Gradio at the root
   app = gr.mount_gradio_app(app, demo, path="/")
   ```
4. **Launch:** `uvicorn.run(app, host="0.0.0.0", port=7860)`

## Google Colab 1-Click Deployment Hacks

### ⚠️ Pitfall: Event Loop Collision
Colab runs a Jupyter event loop by default. A standard `uvicorn.run()` will crash with `RuntimeError: This event loop is already running`.
**Fix:** Use `nest_asyncio`.
```python
import nest_asyncio
nest_asyncio.apply() # CRITICAL for Colab
```

### ⚠️ Pitfall: Gradio Public Share Link alongside FastAPI
If you want Gradio to generate a public `.gradio.live` link (via `share=True`) while still allowing the underlying FastAPI app (and API routes) to run in the same Colab cell, you must launch the Gradio demo in a non-blocking background thread *before* starting uvicorn:
```python
# Launch Gradio with share=True in the background thread
demo.launch(server_name="0.0.0.0", server_port=7860, share=True, prevent_thread_lock=True)

# Run the FastAPI server (which already has Gradio mounted to / in app.py)
uvicorn.run(app, host="0.0.0.0", port=7860)
```

## Production Considerations
- `references/fastmcp_sse_integration.md`: Important changes to FastMCP 1.x routing, `get_starlette_app()` deprecation, and safe SSE mounting patterns.
*   **File Cleanup:** If the application accepts file uploads or generates media, implement a `cleanup_old_files()` routine triggered on every request to delete files older than 1 hour from `tempfile.gettempdir()`. This prevents VPS disk-full crashes.
*   **Security:** Wrap API routes in `Depends(api_key_header)` to prevent unauthorized consumption of GPU resources when the app is publicly exposed via Gradio or Colab tunnels.