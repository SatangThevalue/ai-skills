---
name: ffmpeg-video-automation
description: FFmpeg complex filter recipes for automated social media video generation (TikTok, Shorts)
prerequisites: ["ffmpeg"]
---
# FFmpeg Video Automation (TikTok / Reels / Shorts)

Using `ffmpeg -filter_complex` allows for single-pass video processing, which is vastly superior in performance (RAM/IO) compared to wrappers like MoviePy or ImageMagick, especially on VPS environments.

## Core Recipes

### 1. Smart Background Blur (9:16 Vertical format)
Converts any video (landscape or square) into a 9:16 vertical video by copying the stream, scaling the background to fill and blurring it, then overlaying the original video in the center.
```bash
-filter_complex "[0:v]split=2[bg][fg];[bg]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,gblur=sigma=30[bg_blur];[fg]scale=1080:1920:force_original_aspect_ratio=decrease[fg_scaled];[bg_blur][fg_scaled]overlay=(W-w)/2:(H-h)/2[vcrop]"
```

### 2. Burning ASS Subtitles (Dynamic/Karaoke)
Advanced SubStation Alpha (`.ass`) files allow for word-level highlights and styling.
```bash
-vf "ass='/absolute/path/to/subtitle.ass'"
```
*Note: Always use absolute paths for the `ass` filter.*
See `references/faster-whisper-karaoke-subtitles.md` for generating word-level timestamped ASS files via faster-whisper.

### 3. Text Overlays (Drawtext)
```bash
-vf "drawtext=fontfile='/absolute/path/to/font.ttf':text='Hello World':fontcolor=yellow:fontsize=100:x=(w-text_w)/2:y=(h-text_h)/2"
```

## ⚠️ Pitfalls & Gotchas

1. **Font Rendering Squares (Non-Latin Characters):** When using `drawtext` with custom fonts (like Thai fonts), **always use an absolute path** for `fontfile`. If FFmpeg cannot resolve a relative path, it silently falls back to a system font, causing non-Latin characters to render as missing square boxes. Ensure forward slashes even on Windows.
2. **Escaping Characters in Drawtext:** Text strings in `drawtext` must have colons `:` and single quotes `'` escaped (e.g., `\:` and `\'`).
3. **Audio Mapping with Complex Filters:** When generating a new video stream via `filter_complex` (e.g., `[vcrop]`), remember to explicitly map it alongside the audio: `-map "[vcrop]" -map 0:a` (or the respective audio mix).