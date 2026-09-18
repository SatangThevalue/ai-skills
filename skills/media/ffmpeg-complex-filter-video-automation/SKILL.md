---
name: ffmpeg-complex-filter-video-automation
description: Best practices for building fully automated video pipelines (templates, shorts, overlays) entirely in FFmpeg without MoviePy.
---

# FFmpeg Complex Filter Video Automation

Use this skill when building automated video production systems (e.g. for n8n, API backends, shorts automation).

**Core Principle:** `MoviePy` consumes excessive RAM and disk I/O by splitting audio/video into intermediate files and frames. Always replace `MoviePy` with a single-pass `ffmpeg -filter_complex` command when running on a VPS or constrained server.

## 1. Smart Background Blur for Vertical/Horizontal Conversion
When turning a 9:16 vertical video into a 16:9 horizontal video (or vice versa), do not stretch the footage or use black bars. Use the standard "smart blur" technique in a single FFmpeg pass:

**Vertical (9:16) to Horizontal (16:9):**
```bash
# Splits the stream in two: scales the background to 1920x1080 and blurs it,
# scales the foreground to fit within 1920x1080, and overlays it.
[0:v]split=2[bg][fg];
[bg]scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,gblur=sigma=30[bg_blur];
[fg]scale=1920:1080:force_original_aspect_ratio=decrease[fg_scaled];
[bg_blur][fg_scaled]overlay=(W-w)/2:(H-h)/2[vcrop]
```

**Horizontal (16:9) to Vertical (9:16 for TikTok/Reels):**
```bash
[0:v]split=2[bg][fg];
[bg]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,gblur=sigma=30[bg_blur];
[fg]scale=1080:1920:force_original_aspect_ratio=decrease[fg_scaled];
[bg_blur][fg_scaled]overlay=(W-w)/2:(H-h)/2[vcrop]
```

## 2. Dynamic Karaoke Subtitles (TikTok Style)
Do not render static text for speech. Viewers on Shorts/Reels expect word-by-word karaoke subtitles.

**Pipeline:**
1. Generate TTS audio (e.g. Piper, Edge-TTS).
2. Transcribe the audio using `faster-whisper` (Base model is sufficient and runs on CPU fast) with `word_timestamps=True`.
3. Format the output into an `.ass` (Advanced SubStation Alpha) file.
4. Burn into the video using the FFmpeg `ass` filter: `[0:v]ass='subs.ass'[vsub]`

**Python to ASS Converter (Faster-Whisper):**
```python
def format_timestamp(seconds: float) -> str:
    # Converts float seconds to H:MM:SS.cs
    hours, remainder = divmod(seconds, 3600)
    minutes, secs = divmod(remainder, 60)
    centisecs = int(round((secs - int(secs)) * 100))
    if centisecs == 100: secs, centisecs = int(secs) + 1, 0
    return f"{int(hours)}:{int(minutes):02d}:{int(secs):02d}.{centisecs:02d}"

# ASS Styling: Yellow text, black outline, Bottom-Center alignment (Alignment: 2)
# The karaoke highlight uses the {\c&H00FFFF&} tag (BGR hex)
ass_header = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Sarabun,80,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,1,6,2,2,10,10,250,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
# Append events: Dialogue: 0,{start},{end},Default,,0,0,0,,{\c&H00FFFF&}Word
```

## 3. Font File Paths & Complex Scripts (Pitfall)
When using the `drawtext` filter in FFmpeg via Python `subprocess`, relative font paths or missing system fonts cause text rendering to fail (often resulting in squares for non-Latin scripts like Thai).
**Fix:** Always pass the absolute path to the `.ttf` file using the `fontfile` argument.

**CRITICAL THAI TEXT LIMITATION:** Even with the correct font, FFmpeg's native `drawtext` filter severely struggles with complex Thai typography (missing tone marks like *Mai Ek*, overlapping top/bottom vowels, ghosting, and inserting rogue consonants when attempting word wrap). 
**Architecture Fix for Thai Text:** Do NOT use `drawtext` for Thai text. Instead, use Python `Pillow` (PIL) to generate transparent PNG images containing the properly rendered Thai text (handling wrapping and line spacing natively), and then use FFmpeg's `overlay` filter to composite those PNG frames onto the video at the correct timestamps.
```bash
# For English/Basic text only:
[vcrop]drawtext=text='My Text':fontcolor=yellow:fontsize=100:fontfile='/absolute/path/to/Sarabun-Bold.ttf':x=(w-text_w)/2:y=(h-text_h)/2[vtext]
```

## 4. Quotes / Motivation Video Overlays (Drop Shadow & Dimming)
When overlaying text on a background video or image (e.g., for motivational quotes on TikTok/Reels), the background must be dimmed, and the text must have a drop shadow for readability.

**1. Background Dimming (`colorchannelmixer`):**
```bash
# Dim the background by 50%
[0:v]colorchannelmixer=r=0.5:g=0.5:b=0.5[dark_bg]
```

**2. Multi-line Text with Drop Shadow:**
Chain `drawtext` filters to add multiple lines of text. Use `shadowcolor`, `shadowx`, and `shadowy` to create a drop shadow. Use math expressions for `x` and `y` to center text dynamically.

```bash
# Headline (Yellow/Gold, centered, large drop shadow)
[dark_bg]drawtext=text='7 สัญญาณว่าคุณเริ่มคิดแบบ':fontfile='/path/to/Sarabun-Bold.ttf':fontcolor='#FFD700':fontsize=70:x=(w-text_w)/2:y=(h/2)-300:shadowcolor=black:shadowx=4:shadowy=4[v1];
[v1]drawtext=text='"เจ้าของธุรกิจ" แล้ว':fontfile='/path/to/Sarabun-Bold.ttf':fontcolor='#FFD700':fontsize=80:x=(w-text_w)/2:y=(h/2)-200:shadowcolor=black:shadowx=4:shadowy=4[v2];

# Body list item (White, offset x, smaller drop shadow)
[v2]drawtext=text='1. นั่งเล่นอยู่..แต่สมองคิดเรื่องหาเงินตลอด':fontfile='/path/to/Sarabun-Regular.ttf':fontcolor='white':fontsize=50:x=100:y=(h/2)-50:shadowcolor=black:shadowx=2:shadowy=2[v_out]
```

## 4. Multi-Track Audio Mixing (`amix`)
When combining a voiceover with background music (BGM):
1. Adjust the volume of the BGM first.
2. Mix the two tracks.
3. Set `duration=first` so the output ends when the voiceover ends.
```bash
# Assuming [0:a] is Voiceover, [1:a] is BGM
[1:a]volume=0.3[a_bgm];
[0:a][a_bgm]amix=inputs=2:duration=first:dropout_transition=2[a_mix]
```
Ensure you map the mixed audio correctly: `-map "[a_mix]"`

## 5. Listicle / Motivation Video Overlays (Staggered Text & Vignette)
When generating short-form quotes or listicles (e.g., "7 Tips for..."), static text lacks engagement and hard-coded boxes look amateurish.

**1. Vignette for Readability:** Instead of drawing a solid or semi-transparent rectangle (`drawbox`) behind the text, darken the background naturally using `colorchannelmixer` and `vignette`.
```bash
# Darken RGB channels to 40% and apply a vignette
colorchannelmixer=rr=0.4:gg=0.4:bb=0.4[dimmed];[dimmed]vignette=PI/3[vignetted]
```

**2. Staggered Text Appearance:** Use the `enable` parameter in `drawtext` to make list items appear one by one, mimicking a typewriter or presentation pacing to force viewer retention.
```bash
# Headline appears immediately
[vignetted]drawtext=text='Headline':x=(w-text_w)/2:y=200:fontcolor='#FFD700'[t1];
# Item 1 appears at 1 second
[t1]drawtext=text='1. First item':x=50:y=400:enable='between(t,1,20)'[t2];
# Item 2 appears at 3 seconds
[t2]drawtext=text='2. Second item':x=50:y=500:enable='between(t,3,20)'[out]
```

## 5. Typewriter & Ambient Audio Video Generation (No TTS)
For focus/knowledge-based videos that rely on text reading without voiceover:
- **Visuals:** Use the `enable` filter within `drawtext` to stagger text appearance simulating typing (e.g., `enable='between(t,3,20)'`). Dim the background (`colorchannelmixer=rr=0.4:gg=0.4:bb=0.4`) and use a semi-transparent box (`drawbox`).
- **Audio:** Mix a Lo-Fi/Ambient BGM track with typing/whoosh Sound Effects (SFX) synchronized to the text appearance timestamps. Use an audio `lowpass=f=400` filter on the BGM to create an immersive, "muffled" room effect.
*(See `templates/typewriter-lofi-video.md` for the full FFmpeg graph.)*