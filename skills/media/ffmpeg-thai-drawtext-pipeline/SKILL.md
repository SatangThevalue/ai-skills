---
name: ffmpeg-thai-drawtext-pipeline
description: "Assemble vertical videos with typewriter effects and Thai text using pure FFmpeg."
version: 0.1.0
metadata:
  hermes:
    tags: [FFmpeg, Video-Editing, Thai-Language, Automation]
---

# Pure FFmpeg Thai Video Assembly

This skill details how to assemble a vertical short-form video (9:16) entirely within a single FFmpeg `filter_complex` command. It applies background dimming, vignette, audio ducking, and a staggered "typewriter-like" text appearance using the `drawtext` filter. 

While it attempts to handle Thai text spacing via `line_spacing` and python `textwrap`, note that native FFmpeg `drawtext` often struggles with complex Thai vowel/tone overlaps. For pixel-perfect Thai rendering, use the PIL-overlay method described in `thai-faceless-video-automation` instead.

## When to Use
- You need the absolute fastest video rendering pipeline without generating intermediate image assets.
- Staggered text appearance (timed pop-ins) is required.
- Applying cinematic background effects (dimming + vignette) to raw B-roll.

## Prerequisites
- `ffmpeg` installed.
- Python 3.
- TrueType Thai fonts (e.g., Sarabun) located at an absolute path (e.g., `/home/thaieasyvps/.fonts/Sarabun/Sarabun-Bold.ttf`).

## How to Run
Execute the included Python script through the `terminal` tool. The script wraps the complex FFmpeg command generation.

## Quick Reference
- Dimming filter: `colorchannelmixer=rr=0.5:gg=0.5:bb=0.5`
- Vignette filter: `vignette=PI/4`
- Timed appearance: `enable='between(t,<start_time>,<end_time>)'`
- Thai spacing fix: `line_spacing=15`

## Procedure

1. **Format Text with Python (Word Wrap)**
   FFmpeg's `drawtext` does not natively word-wrap. Use Python's `textwrap` to insert `\n` characters before passing the string to FFmpeg.
   ```python
   import textwrap
   raw_text = "ยิ่งยาก : ยิ่งมีเสน่ห์ ลองทำในสิ่งที่คนอื่นไม่กล้าทำ"
   wrapped_text = "\n".join(textwrap.wrap(raw_text, width=35))
   ```

2. **Construct the Filter Complex (Background & Headline)**
   Build the FFmpeg filter string step-by-step.
   ```python
   filter_complex = (
       "[0:v]format=yuv420p,scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280,"
       "colorchannelmixer=rr=0.5:gg=0.5:bb=0.5," # Dim 50%
       "vignette=PI/4[vignetted];" # Vignette
       
       # Headline (Always visible)
       f"[vignetted]drawtext=text='My Headline':fontfile='{font_path}':fontcolor='#FFD700':fontsize=45:x=(w-text_w)/2:y=(h/2)-250:shadowcolor=black:shadowx=2:shadowy=2[t1];"
   )
   ```

3. **Construct the Filter Complex (Timed Body Text)**
   Use the `enable` flag to stagger the appearance of text items, creating a pacing effect. Use `line_spacing=15` to mitigate Thai tone mark collisions.
   ```python
   filter_complex += (
       # Item 1 appears at t=1s
       f"[t1]drawtext=text='{wrapped_item1}':fontfile='{font_path}':fontcolor='white':fontsize=35:line_spacing=15:x=(w-text_w)/2:y=(h/2)-50:shadowcolor=black:shadowx=2:shadowy=2:enable='between(t,1,20)'[t2];"
       
       # Item 2 appears at t=3s
       f"[t2]drawtext=text='{wrapped_item2}':fontfile='{font_path}':fontcolor='white':fontsize=35:line_spacing=15:x=(w-text_w)/2:y=(h/2)+50:shadowcolor=black:shadowx=2:shadowy=2:enable='between(t,3,20)'[outv];"
   )
   ```

4. **Construct the Filter Complex (Audio Ducking)**
   Lower the background music volume.
   ```python
   filter_complex += "[1:a]volume=0.3[outa]"
   ```

5. **Execute FFmpeg**
   Run the command via `subprocess`.
   ```python
   cmd = [
       "ffmpeg", "-y",
       "-i", "input_broll.mp4",
       "-i", "bgm.mp3",
       "-filter_complex", filter_complex,
       "-map", "[outv]",
       "-map", "[outa]",
       "-c:v", "libx264", "-preset", "fast", "-crf", "23",
       "-c:a", "aac", "-b:a", "192k",
       "-t", "10", # Truncate duration
       "output.mp4"
   ]
   subprocess.run(cmd, check=True)
   ```

## Pitfalls
- **Thai Tone Mark Collisions:** If `line_spacing` is omitted or too small, upper vowels (like ิ) and tone marks (like  ่) will overlap and become illegible in `drawtext`.
- **Rogue Characters:** When `textwrap` splits sentences, it might insert newlines at awkward phonetic boundaries in Thai, occasionally confusing the renderer.
- **Ghosting:** Incorrectly chaining `enable` filters without advancing the stream label (e.g., `[t1] -> [t1]`) will cause previous text layers to ghost or overwrite. Always chain strictly: `[t1] -> [t2]`, `[t2] -> [outv]`.

## Verification
Use the `terminal` tool to run the provided script `scripts/ffmpeg_drawtext_assembler.py` and inspect the output MP4 using `ffprobe`.