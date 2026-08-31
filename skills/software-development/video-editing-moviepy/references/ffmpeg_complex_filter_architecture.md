# Ultimate Performance FFmpeg Architecture

When rendering video on constrained VPS environments, relying on MoviePy causes high memory usage, intermediate temporary file disk I/O, and frequent CPU deadlocks (ImageMagick `convert` hangs on `TextClip`).

The "Ultimate Performance" pattern for n8n/FastAPI video backends is to abandon MoviePy and construct a single-pass `ffmpeg -filter_complex` command dynamically in Python.

## The Single-Pass Python FFmpeg Processor

This pattern processes everything in memory concurrently:
1. Video track: Crops to 9:16 vertical, adds text overlay via `drawtext`.
2. Audio track: Optionally maps original audio, maps BGM, and mixes them (`amix`).

```python
import os
import subprocess
import json

def process_video_single_pass(
    input_video: str,
    output_video: str,
    mute_original_audio: bool = False,
    bgm_file: str = None,
    bgm_volume: float = 0.3,
    crop_916: bool = False,
    drawtext_text: str = None,
    font_file: str = None,
    font_size: int = 48,
    font_color: str = "white"
):
    """
    Dynamically constructs an FFmpeg command using complex filters.
    Optimized for single-pass processing without MoviePy.
    """
    cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "info", "-i", input_video]
    
    input_count = 1
    bgm_idx = -1
    if bgm_file and os.path.exists(bgm_file):
        cmd.extend(["-i", bgm_file])
        bgm_idx = input_count
        input_count += 1

    filter_complex = []
    
    # 1. Video Filters
    video_filters = []
    last_v = "[0:v]"
    
    if crop_916:
        video_filters.append(f"{last_v}crop='ih*9/16':'ih'[vcrop]")
        last_v = "[vcrop]"
        
    if drawtext_text:
        font_opt = f":fontfile={font_file}" if font_file and os.path.exists(font_file) else ""
        text_safe = drawtext_text.replace("'", r"\'").replace(":", r"\:")
        video_filters.append(
            f"{last_v}drawtext=text='{text_safe}':fontcolor={font_color}:fontsize={font_size}{font_opt}:x=(w-text_w)/2:y=(h-text_h)/2[vtext]"
        )
        last_v = "[vtext]"
        
    if video_filters:
        filter_complex.append(";".join(video_filters))
        final_v = last_v
    else:
        final_v = "0:v"

    # 2. Audio Filters
    audio_filters = []
    final_a = None
    
    if mute_original_audio and bgm_idx == -1:
        pass # -an behavior 
    elif mute_original_audio and bgm_idx != -1:
        audio_filters.append(f"[{bgm_idx}:a]volume={bgm_volume}[a_bgm]")
        final_a = "[a_bgm]"
    elif not mute_original_audio and bgm_idx != -1:
        audio_filters.append(f"[{bgm_idx}:a]volume={bgm_volume}[a_bgm]")
        audio_filters.append(f"[0:a][a_bgm]amix=inputs=2:duration=first:dropout_transition=2[a_mix]")
        final_a = "[a_mix]"
    else:
        final_a = "0:a"
        
    if audio_filters:
        filter_complex.append(";".join(audio_filters))

    # Assemble Command
    if filter_complex:
        cmd.extend(["-filter_complex", ";".join(filter_complex)])
        
    # Maps
    cmd.extend(["-map", final_v])
    if final_a and final_a != "0:a":
        cmd.extend(["-map", final_a])
    elif not mute_original_audio:
        cmd.extend(["-map", "0:a?"])

    # Encoding profile
    cmd.extend([
        "-c:v", "libx264", 
        "-preset", "fast", 
        "-crf", "23",
        "-c:a", "aac",
        "-b:a", "128k",
        output_video
    ])
    
    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        return {"status": "success", "output": output_video, "cmd": " ".join(cmd)}
    except subprocess.CalledProcessError as e:
        return {"status": "error", "error": e.stderr}
```

## Integration with FastAPI for n8n

When exposing this to n8n, simply wrap it in an `asyncio.to_thread` call to ensure the `subprocess.run` execution doesn't block the ASGI event loop:

```python
import asyncio
from fastapi import FastAPI, Form, HTTPException

app = FastAPI()

@app.post("/api/video/edit")
async def api_video_edit(
    video_path: str = Form(...),
    bgm_path: str = Form(None),
    mute_original_audio: bool = Form(False),
    short_video_format: bool = Form(False)
):
    output = f"{video_path}_edited.mp4"
    result = await asyncio.to_thread(
        process_video_single_pass,
        input_video=video_path,
        output_video=output,
        mute_original_audio=mute_original_audio,
        bgm_file=bgm_path,
        crop_916=short_video_format
    )
    if result["status"] == "error":
        raise HTTPException(status_code=500, detail=result["error"])
    return result
```