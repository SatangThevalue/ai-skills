---
name: video-editing-moviepy
description: Video editing automation using MoviePy in Python, specifically for vertical 9:16 social media formats (Reels, TikTok, Shorts).
tags:
  - python
  - video-editing
  - moviepy
  - automation
  - social-media
---

# MoviePy Video Automation for Social Media

Use this skill when building automated video editing pipelines in Python, specifically targeting vertical 9:16 formats for platforms like TikTok, Instagram Reels, and YouTube Shorts.

## CPU Constrained Environments & Timeout Prevention
When deploying MoviePy to a VPS running n8n via HTTP Requests, the render process can trigger HTTP timeouts if it takes longer than 60s, or cause `[Errno 98] address already in use` crashes if the asyncio event loop freezes.

To prevent this:
1. Always run `write_videofile` in a background thread: `await asyncio.to_thread(render_function)`
2. Reduce the video framerate (e.g., `fps=24` or `fps=25` instead of 30 or 60).
3. Set `preset="ultrafast"` in `write_videofile` to speed up CPU encoding dramatically.
4. Set `threads=1` or `threads=2` to prevent internal deadlocks when the CPU is at 100% load.

```python
video.write_videofile(
    output_path, 
    codec="libx264", 
    audio_codec="aac",
    fps=24,          
    logger=None,
    threads=1,       # Force single thread to prevent any deadlocks
    preset="ultrafast" 
)
```

## Available References
- `references/moviepy_v2_migration.md`: Critical breaking changes between v1.x and v2.x, ImageMagick config, and CPU deadlock prevention.
- `references/n8n-video-automation-patterns.md`: Best practices for integrating video APIs with n8n (bypassing multipart binary uploads via Local Paths, handling timeouts).
- `references/auto_provisioning_media_apis.md`: Scripts and patterns for automatically downloading HuggingFace TTS base models during FastAPI startup to ensure zero-config deployments.
- `references/dynamic_subtitles_whisper_ffmpeg.md`: Implementation patterns for extracting word-level timestamps with Faster-Whisper and burning karaoke-style ASS subtitles via FFmpeg.

## Auto-Provisioning Models (Zero-Config)

When building standalone FastAPI services for media APIs, ensure the application self-bootstraps missing dependencies on startup. For instance, rather than failing because TTS base models are missing on a fresh deploy, use a startup script to fetch them from official sources (like HuggingFace) before opening the HTTP ports.

```python
def ensure_base_models_exist():
    import os, subprocess
    piper_dir = os.path.join(BASE_DIR, "pretrained_models", "piper_voices")
    os.makedirs(piper_dir, exist_ok=True)
    
    if not any(f.endswith(".onnx") for f in os.listdir(piper_dir)):
        print("📥 [System] No TTS models found. Auto-Provisioning...")
        subprocess.run(["python3", "setup_models.py"], check=True)

ensure_base_models_exist()
```

MoviePy is a versatile Python library that wraps `ffmpeg` to provide programmatic video editing. It is ideal for building automated media pipelines (like FastAPI endpoints or n8n workflow nodes).

Key use cases:
1.  **Format Conversion:** Auto-cropping horizontal/square video into vertical 9:16.
2.  **Audio Replacement:** Muting original audio and replacing it with TTS or background music.
3.  **Text Overlay:** Adding multi-line text, subtitles, or captions.
4.  **Watermarking:** Adding logos or text watermarks.
5.  **Trimming:** Cutting specific segments of video.

## Implementation Patterns

### 1. The Rendering Lock (Crucial for APIs)

Video rendering is highly CPU and memory intensive. When exposing MoviePy via an API (like FastAPI), you **must** use an `asyncio.Lock()` and offload the synchronous rendering task to a background thread to ensure only one video renders at a time without freezing the main event loop. Otherwise, concurrent requests will immediately cause an Out-Of-Memory (OOM) crash or HTTP timeout on most VPS environments.

```python
import asyncio
from moviepy import VideoFileClip

cpu_render_lock = asyncio.Lock()

def _render_sync(video_path, output_path):
    video = VideoFileClip(video_path)
    # ... editing logic ...
    video.write_videofile(
        output_path, 
        codec="libx264", 
        audio_codec="aac",
        threads=2, # Limit threads to prevent CPU deadlocks
        preset="ultrafast" 
    )
    video.close()

async def process_video(video_path: str, output_path: str):
    async with cpu_render_lock:
        await asyncio.to_thread(_render_sync, video_path, output_path)
```

### 2. Auto-Cropping to 9:16 (Vertical)

To standardize varied input footage into a clean 1080x1920 vertical format without stretching, calculate the aspect ratio and perform a center crop before resizing.

```python
# MoviePy v2 Syntax
def crop_to_vertical(video):
    target_w, target_h = 1080, 1920
    video_aspect = video.w / video.h
    target_aspect = target_w / target_h
    
    if video_aspect > target_aspect:
        # Video is wider than target: Crop the sides (Center crop)
        new_w = int(video.h * target_aspect)
        video = video.cropped(x_center=video.w / 2, width=new_w, height=video.h)
    else:
        # Video is taller than target: Crop top/bottom
        new_h = int(video.w / target_aspect)
        video = video.cropped(y_center=video.h / 2, width=video.w, height=new_h)
    
    # Finally resize to exact target resolution
    return video.resized((target_w, target_h))
```

### 3. Subtitles and Multi-Scene Processing (The FFmpeg Advantage)
While MoviePy can handle basic editing, generating dynamic "TikTok-style" subtitles (karaoke highlighting, per-word popping) and multi-scene concatenation (stitching B-roll) is significantly faster and more memory-efficient when outsourced to native FFmpeg tools and specialized engines.

*   **Dynamic Subtitles (Faster-Whisper + FFmpeg):** Instead of generating hundreds of MoviePy `TextClip` objects (which will destroy your RAM and stall ImageMagick), use `faster-whisper` (e.g., the `base` or `tiny` models for speed) to extract word-level timestamps from the audio. Convert those timestamps into an Advanced SubStation Alpha (`.ass`) subtitle file. Then, use an FFmpeg filter (`-vf "ass=subtitles.ass"`) to burn the dynamic styling, outlines, and colors directly into the video stream in a single pass.
*   **Smart Background Blur (16:9 for Vertical Video):** When converting vertical 9:16 video to horizontal 16:9, avoid simple black pillars. Use an FFmpeg `filter_complex` to split the stream, scale and apply `gblur` to the background, and `overlay` the original un-stretched video on top.

```python
# Conceptual FFmpeg command for Smart Blur
cmd = [
    "ffmpeg", "-i", "input.mp4", "-filter_complex",
    "[0:v]split=2[bg][fg];"
    "[bg]scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,gblur=sigma=30[bg_blur];"
    "[fg]scale=1920:1080:force_original_aspect_ratio=decrease[fg_scaled];"
    "[bg_blur][fg_scaled]overlay=(W-w)/2:(H-h)/2[outv]",
    "-map", "[outv]", "output.mp4"
]
```

### 4. Audio Muting and Replacement

To replace the original audio with a new track (e.g., TTS output), you must handle durations carefully to prevent the audio from exceeding the video length.

```python
from moviepy import AudioFileClip, CompositeAudioClip

def replace_audio(video, new_audio_path, mute_original=True):
    new_audio = AudioFileClip(new_audio_path)
    # Ensure audio isn't longer than video (v2 syntax)
    new_audio = new_audio.with_duration(min(new_audio.duration, video.duration))
    
    if mute_original or video.audio is None:
        final_audio = new_audio
    else:
        # Merge original (lowered volume to 30%) + new audio (v2 syntax)
        final_audio = CompositeAudioClip([video.audio.with_volume_scaled(0.3), new_audio])
        
    return video.with_audio(final_audio)
```

### 4. Multi-line Text Overlays (Stacked Boxes)

When concatenating multi-speaker audio with NumPy and `soundfile` before inserting into MoviePy, **avoid wrapping simple NumPy array concatenation and `sf.write` operations in thread pools or `asyncio.to_thread`**. The disk I/O for `soundfile` and `np.concatenate` on moderately sized audio is generally fast enough that the thread/executor overhead introduces risk without meaningful benefit. Run it inline.

For social media, text is often presented as a stacked list of centered boxes. Use `TextClip` within a loop to calculate Y-positions dynamically.

**Important Font Consideration:** When rendering non-English characters (like Thai), you *must* provide a specific TrueType font file path, or ImageMagick will render boxes/errors. (e.g., `font='/usr/share/fonts/truetype/Sarabun/Sarabun-Bold.ttf'`)

```python
from moviepy import TextClip, CompositeVideoClip

def add_stacked_text(video, text_lines, font_path='Arial'):
    clips_to_composite = [video]
    lines = [l.strip() for l in text_lines.split("\\n") if l.strip()]
    
    box_width = int(video.w * 0.85) # 85% width of screen
    start_y = int(video.h * 0.25)   # Start 25% down the screen
    spacing = 30                    
    current_y = start_y
    
    for line in lines:
        txt_clip = TextClip(
            font=font_path,
            text=line, 
            font_size=45, 
            color='black', 
            bg_color='white',
            method='caption',
            text_align='center',
            size=(box_width, None) # Auto-height based on text wrapping
        )
        
        txt_clip = txt_clip.with_position(('center', current_y)).with_duration(video.duration)
        clips_to_composite.append(txt_clip)
        current_y += txt_clip.h + spacing
        
    return CompositeVideoClip(clips_to_composite)
```

## Pitfalls & Gotchas

*   **ImageMagick Dependency:** MoviePy's `TextClip` relies entirely on ImageMagick being installed on the host system. Without it, text generation will fail with obscure `convert` command errors. On POSIX systems, you may need to explicitly configure the path via Python: 
    ```python
    import os
    if os.name == 'posix':
        os.environ["IMAGEMAGICK_BINARY"] = "/usr/bin/convert"
    ```
*   **Font Paths for Non-English Text:** When rendering Thai or other non-Latin scripts using `TextClip` or FFmpeg's `drawtext`, you MUST provide an absolute path to a TrueType font file (e.g., `fontfile='/usr/share/fonts/truetype/Sarabun/Sarabun-Bold.ttf'`). Relying on system font names often results in tofu (square boxes) instead of characters.
*   **Bypassing TextClip / ImageMagick Freezes:** If you run into unrecoverable OS deadlocks where the script freezes without an error message (usually during `CompositeVideoClip` rendering involving text), it is often ImageMagick stalling on memory limits when generating `TextClip` objects. The ultimate solution for lightweight, blazing-fast processing is to abandon MoviePy and ImageMagick entirely, and instead construct a **single-pass FFmpeg Complex Filter** string via Python `subprocess.run()`. By writing a single `ffmpeg` command that maps video (`[0:v]`), crops (`crop='ih*9/16':'ih'`), mixes audio (`amix`), and renders text (`drawtext` or `ass=`) concurrently, you skip temporary files and bypass MoviePy's heavy RAM overhead and I/O bottlenecks.

See `references/ffmpeg_complex_filter_architecture.md` for a production-grade single-pass Python script.
*   **Temporary File Bloat:** MoviePy creates intermediate temporary audio files during rendering. You must explicitly tell it to clean up: `write_videofile(..., remove_temp=True)`. Additionally, ensure your API layer cleans up the final input/output files periodically.
*   **Memory Leaks:** Always explicitly call `.close()` on your VideoFileClip and AudioFileClip instances after `write_videofile` is finished. MoviePy does not reliably garbage-collect these large objects, leading to OOMs on long-running APIs.
*   **CPU Concurrency (FastAPI/Docker):** MoviePy rendering (especially composite clips) is heavily CPU-bound. When running inside a concurrent API, wrap the video processing block in an `asyncio.to_thread()` combined with a concurrency lock. However, be extremely careful: relying on heavy threads in a low-resource environment can freeze the GIL. **In MoviePy v2.x**, explicitly setting a lower `threads` count (e.g., `threads=1`) and `preset="ultrafast"` in `write_videofile` is required to prevent unrecoverable `subprocess` deadlocks during `ffmpeg` muxing.
*   **Consistent FPS:** Social media platforms prefer 30fps or 60fps. Explicitly set `fps=30` in `write_videofile()` to avoid issues where the input footage has an irregular framerate.