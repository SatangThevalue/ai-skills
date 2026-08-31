---
name: server-side-video-processing
description: "High-performance server-side video automation using pure FFmpeg complex filters (single-pass), avoiding MoviePy/ImageMagick overhead."
---
# Server-Side Video Processing (Ultimate Performance Architecture)

When building video generation/editing pipelines for server environments (especially low-CPU VPS or n8n automated workflows), **DO NOT use multi-step wrappers like MoviePy**. MoviePy extracts audio, processes frames sequentially, and re-encodes, which leads to massive I/O bottlenecks and RAM bloat.

Instead, use **FFmpeg Complex Filters (`-filter_complex`)** to perform all operations (cropping, text overlays, audio mixing) in a **single pass**.

## Core Principles
1. **Single-Pass Execution**: Chain video and audio filters together inside `-filter_complex`. 
2. **Avoid Temporary Files**: Map the final output pads directly to the output file.
3. **Dynamic Assembly**: Build the FFmpeg command dynamically in Python based on requested features (e.g., if no BGM is requested, skip the `amix` filter).

## FFmpeg Complex Filter Patterns

### 1. Vertical Cropping (9:16 for Shorts/Reels)
```bash
[0:v]crop='ih*9/16':'ih'[vcrop]
```

### 2. Thai Text Overlay (Drawtext)
Requires a valid TTF font path. Note the escaped colon for fontfile and safe text formatting.
```bash
[vcrop]drawtext=text='ข้อความ':fontfile=/path/to/font.ttf:fontcolor=white:fontsize=48:x=(w-text_w)/2:y=(h-text_h)/2[vtext]
```

### 3. Audio Mixing (Amix)
To combine original audio and background music (BGM) while managing volume levels:
```bash
[1:a]volume=0.3[a_bgm];[0:a][a_bgm]amix=inputs=2:duration=first:dropout_transition=2[a_mix]
```

## Advanced Templates and Faster-Whisper

### Smart Background Blur (16:9 Transformation)
When converting vertical (9:16) footage to horizontal (16:9), split the stream, blur the background layer, and overlay the original on top:
```bash
[0:v]split=2[bg][fg];[bg]scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,gblur=sigma=30[bg_blur];[fg]scale=1920:1080:force_original_aspect_ratio=decrease[fg_scaled];[bg_blur][fg_scaled]overlay=(W-w)/2:(H-h)/2[vcrop]
```

### Dynamic Subtitles with Faster-Whisper
For TikTok/Reels karaoke-style subtitles, use `faster-whisper` (base or tiny models for low memory usage) in Python with `word_timestamps=True`. 
1. Convert the word-level output to an `.ass` (Advanced SubStation Alpha) file.
2. Use ASS override tags like `{\\c&H00FFFF&}` for color highlighting on specific words.
3. Burn the `.ass` file using FFmpeg's `ass` filter (`[0:v]ass='subtitle.ass'[vsub]`).

This is vastly more efficient than generating frames individually and can be run comfortably on CPU instances.

### Complete Assembly Example (Python)
See `scripts/ffmpeg_processor_template.py` for a complete, production-ready Python API script that dynamically builds these filters based on boolean flags (for n8n integration).

## Pitfalls & Edge Cases
- **Font Files**: Always provide an absolute path to a `.ttf` file when using `drawtext`, otherwise Thai/complex characters will render as boxes.
- **Audio Mapping Fallback**: If a video might not have an audio stream, map audio using the `?` flag (e.g., `-map 0:a?`) to prevent FFmpeg from crashing if audio is missing.
- **API Integration**: When exposing this via FastAPI (e.g. for n8n), run the FFmpeg subprocess using `asyncio.to_thread()` to prevent blocking the async event loop.
- **Quote Escaping**: When passing text to `drawtext`, always sanitize single quotes `replace("'", r"\'")` and colons `replace(":", r"\:")`.
