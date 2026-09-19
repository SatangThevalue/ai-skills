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

### 2. Complex Typography (Thai/Vowels) via PIL Overlay
When `drawtext` fails on complex fonts (vowels, tone marks), render transparent PNGs via Python Pillow and composite them sequentially. See `references/pil-overlay-text.md`.

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

1. **Thai/Complex Vowels and Tone Marks with `drawtext`:** FFmpeg's `drawtext` filter handles Thai tone marks (ไม้เอก, ไม้โท) and upper/lower vowels poorly, often stripping them or rendering text overlapping and jumbled when word wrapping. **Do NOT use `drawtext` for complex Thai typography.** Instead, generate transparent PNG overlays using Python's Pillow (`PIL.ImageDraw`), then use FFmpeg's `overlay` filter to composite the PNGs onto the video.
2. **Overlay Ghosting in `filter_complex`:** When chaining multiple `overlay` filters with `enable='between(t,A,B)'`, ensure you chain them sequentially (`[bg][ol1]overlay...[v1]; [v1][ol2]overlay...[v2]`) rather than overlapping them onto the same base. However, if the base video already has burned-in text you need to hide, you may need a blackout mask (e.g. `drawbox`) before overlaying new text.
3. **Font Rendering Squares (Non-Latin Characters):** When using `drawtext` with custom fonts (like Thai fonts), **always use an absolute path** for `fontfile`. If FFmpeg cannot resolve a relative path, it silently falls back to a system font, causing non-Latin characters to render as missing square boxes. Ensure forward slashes even on Windows.
2. **Escaping Characters in Drawtext:** Text strings in `drawtext` must have colons `:` and single quotes `'` escaped (e.g., `\:` and `\'`).
3. **Audio Mapping with Complex Filters:** When generating a new video stream via `filter_complex` (e.g., `[vcrop]`), remember to explicitly map it alongside the audio: `-map "[vcrop]" -map 0:a` (or the respective audio mix).