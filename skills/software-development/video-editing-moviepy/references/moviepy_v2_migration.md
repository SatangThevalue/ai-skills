# MoviePy v2.x Migration & Production Pitfalls

## Breaking Changes from v1.x to v2.x
MoviePy 2.x introduces a purely object-oriented API where methods return new instances rather than mutating in-place.
- `crop()` ➔ `cropped()`
- `resize()` ➔ `resized()`
- `set_duration()` ➔ `with_duration()`
- `set_position()` ➔ `with_position()`
- `set_audio()` ➔ `with_audio()`
- `volumex()` ➔ `with_volume_scaled()`

**TextClip Parameters:**
- `fontsize` ➔ `font_size`
- `align` ➔ `text_align`
- `txt` ➔ `text`

## ImageMagick Configuration on Linux
In v1.x, developers used `from moviepy.config import change_settings` to override the ImageMagick binary path. In v2.x, this configuration module is removed.
**Fix:** Set the environment variable directly via `os.environ` before initializing any `TextClip`:
```python
import os
if os.name == 'posix':
    os.environ["IMAGEMAGICK_BINARY"] = "/usr/bin/convert"
```
*(Ensure `/etc/ImageMagick-6/policy.xml` is patched to allow `@*` path reads in your Dockerfile).*

## Preventing CPU Deadlocks and FastAPI Event Loop Freezes
MoviePy's `write_videofile` is synchronous and completely blocks the async event loop.
**Fix:**
1. Wrap the render call in `asyncio.to_thread()`.
2. To prevent CPU deadlocks and timeouts on constrained VPS environments, aggressively lower the thread count and use the ultrafast preset:
```python
video.write_videofile(
    output_path,
    fps=24,              # Lower FPS speeds up render
    threads=1,           # Single thread avoids deadlock on 100% CPU usage
    preset="ultrafast",  # Prevents n8n HTTP Request timeouts
    logger=None
)
```