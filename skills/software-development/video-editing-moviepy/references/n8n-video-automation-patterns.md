# n8n Video Automation Architecture Best Practices

When building video automation pipelines using n8n and Python APIs (like MoviePy/FastAPI), avoid naive payload passing to prevent crippling timeouts and out-of-memory (OOM) failures. 

## 1. Avoid Uploading Binary Media Across Nodes
The primary cause of failure in n8n media workflows is the `HTTP Request` node transferring 100MB+ video binaries via `multipart/form-data`.
- **Why it fails:** n8n serializes binary payloads into its own memory pool and execution database, maxing out RAM. Further, sending large files over HTTP triggers n8n's strict 60-second timeouts.
- **The Solution:** Use **Local Paths (Shared Volumes)**.
  - If n8n and the API share the same VPS or Docker host, mount a shared directory (e.g. `/shared_media`).
  - Use n8n's **Write Binary File** node to save media to `/shared_media/input.mp4`.
  - Pass a JSON/String parameter like `video_local_path=/shared_media/input.mp4` instead of uploading.
  - Have the API return a string like `{"output_path": "/shared_media/out.mp4"}`.
  - Use n8n's **Read Binary File** node to pick it up.

## 2. Managing n8n HTTP Timeouts
Even with local paths, video rendering takes time (e.g. 5 minutes for a 3-minute video on a slow VPS).
- The default n8n HTTP Request timeout is `60,000 ms` (1 minute).
- **The Solution:** Edit the HTTP Node Settings > Set `Timeout` to `600,000` (10 minutes) for any endpoint that invokes FFmpeg or video rendering.

## 3. Dealing with FFmpeg / ImageMagick Deadlocks
When scaling an automated video node, FFmpeg via MoviePy can lock up the host machine.
- **ImageMagick Overloads:** Rendering `TextClip` for subtitles via ImageMagick scales poorly. If the machine freezes, disable TextClips and defer subtitling to native platform apps (TikTok/CapCut) or bypass `with_position` logic in v2.
- **Thread Exhaustion:** Setting `threads=4` or higher in `write_videofile` on a 2-core VPS causes race conditions and infinite hangs. Force `threads=1` and `preset="ultrafast"` to ensure completion.
- **FastAPI Freezing:** Never block the `asyncio` event loop. Offload video writes into background processes, e.g.:
```python
await asyncio.to_thread(_render_sync_func, args)
```