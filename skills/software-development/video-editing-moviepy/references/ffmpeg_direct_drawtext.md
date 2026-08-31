# FFmpeg Direct DrawText Filter (ImageMagick Bypass)

When `moviepy` and ImageMagick deadlock your CPU during text overlay (especially on small VPS nodes), bypass `TextClip` completely. Use MoviePy strictly for audio composite and scaling, then run a secondary pass with `ffmpeg` using the `drawtext` filter.

## Multiline Centered Text Example

```python
import subprocess
import os

font_path = "/app/assets/fonts/Sarabun-Bold.ttf"
# FFmpeg drawtext requires forward slashes for fontfile paths
safe_font = font_path.replace("\\", "/") 

text_lines = ["Line 1: Studio Test", "Line 2: Ready for n8n"]
# Join lines with actual newline character for multiline support
multiline_text = "\n".join(text_lines)

# Escape colons and single quotes
safe_line = multiline_text.replace(":", "\\:").replace("'", "'\\''")

# Base Y position (25% from top), centered horizontally, 20px line spacing
draw_filter = (
    f"drawtext=fontfile='{safe_font}':text='{safe_line}':"
    f"fontcolor=white:fontsize=45:"
    f"box=1:boxcolor=black@0.6:boxborderw=10:"
    f"x=(w-text_w)/2:y=(h*0.25):"
    f"line_spacing=20:text_align=C"
)

ffmpeg_cmd = [
    "ffmpeg", "-y", 
    "-i", temp_no_text_path,
    "-vf", draw_filter,
    "-c:a", "copy", # Copy audio without re-encoding
    "-c:v", "libx264", "-preset", "ultrafast",
    output_path
]

result = subprocess.run(ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
if result.returncode != 0:
    print(f"FFmpeg DrawText Error: {result.stderr}")
```

This method is blazing fast, uses a fraction of the memory, and completely prevents Python event loop starvation and ImageMagick stalling on foreign language fonts.