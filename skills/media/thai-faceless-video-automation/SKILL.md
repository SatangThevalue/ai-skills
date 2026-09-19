---
name: thai-faceless-video-automation
description: "Pipeline for rendering Thai-language vertical videos with accurate text overlays."
version: 0.1.0
metadata:
  hermes:
    tags: [Video, Automation, FFmpeg, Thai, Typography]
---

# Thai Faceless Video Automation

Generates vertical (9:16) short-form videos featuring dimmed backgrounds, centered Thai typography, and background music (BGM). This workflow relies on `Pillow` (PIL) for text rendering to bypass `FFmpeg`'s native `drawtext` limitations, which incorrectly overlaps Thai tone marks and vowels (e.g., สระ, วรรณยุกต์). It uses standard `ffmpeg` via the `terminal` tool for final assembly.

## When to Use
- Generating TikTok, YouTube Shorts, or Facebook Reels.
- Adding complex Thai text overlays (quotes, lists) to video backgrounds.
- Combining B-roll, BGM, and text overlays automatically.

## Prerequisites
- `ffmpeg` installed.
- Python `Pillow` (`uv pip install Pillow`).
- TrueType Thai fonts (e.g., Sarabun, Kanit) installed on the system (e.g., `/home/thaieasyvps/.fonts/Sarabun/Sarabun-Bold.ttf`).

## How to Run
Invoke the provided generation script through the `terminal` tool, or import its functions into a larger orchestration script.

## Quick Reference
- Text rendering: Python `Pillow` (`ImageDraw.Draw.text`)
- Word wrap: Python `textwrap`
- FFmpeg dimming: `colorchannelmixer=rr=0.5:gg=0.5:bb=0.5`
- FFmpeg vignette: `vignette=PI/4`
- FFmpeg audio ducking (static): `volume=0.3`

## Procedure

1. **Install Dependencies**
   Ensure `Pillow` is installed in the active environment.
   ```bash
   uv pip install Pillow
   ```

2. **Prepare Assets**
   Ensure you have the background video (`.mp4`), background music (`.mp3`), and Thai font files (`.ttf`).

3. **Execute Video Assembly**
   Use the included script `scripts/thai_video_gen.py` to generate the text overlay image and combine it with the video and audio using FFmpeg.
   
   ```python
   # Example invocation within Python
   from scripts.thai_video_gen import create_text_overlay, assemble_video

   text_data = {
       "headline": "3 กฎเหล็กของ",
       "subhead": "ความสำเร็จ",
       "items": [
           "1. ยิ่งยาก : ยิ่งมีเสน่ห์",
           "2. ยิ่งผิดพลาด : ยิ่งเก่งขึ้น"
       ]
   }
   
   overlay_path = "/tmp/overlay.png"
   create_text_overlay(
       output_path=overlay_path,
       text_data=text_data,
       font_path_bold="/home/thaieasyvps/.fonts/Sarabun/Sarabun-Bold.ttf",
       font_path_regular="/home/thaieasyvps/.fonts/Sarabun/Sarabun-Regular.ttf"
   )
   
   assemble_video(
       input_bg="background.mp4",
       overlay_img=overlay_path,
       bgm_audio="lofi.mp3",
       output_video="final_short.mp4",
       duration=10
   )
   ```

## Pitfalls
- **FFmpeg `drawtext` Thai Vowel Overlap:** Do NOT use FFmpeg's `drawtext` for Thai text containing upper/lower vowels or tone marks (like "ยิ่ง"). The marks will squish together. Always use the PIL overlay method.
- **Word Wrap Off-Screen:** Thai text lacks spaces between words. While `textwrap` helps, very long unspaced strings might still misbehave. Ensure input strings are reasonably segmented.
- **Audio Mapping Errors:** If the background video lacks an audio track and you attempt to map `0:a`, FFmpeg will fail. Ensure mappings match the actual streams, or omit original audio mapping if replacing entirely with BGM.

## Verification
Use `read_file` or `terminal` (with `ffprobe`) to verify the output video exists and has the expected duration and resolution (720x1280).