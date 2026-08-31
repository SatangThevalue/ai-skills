# Dynamic Subtitles with Faster-Whisper and FFmpeg (ASS Format)

When building automated video pipelines (especially for TikTok/Reels where dynamic captions are required), generating a `.ass` (Advanced SubStation Alpha) file from Whisper timestamps and burning it in one pass with FFmpeg is the fastest and most resource-efficient method.

## 1. Extracting Timestamps (Faster-Whisper)
Use `faster-whisper` (CTranslate2 backend) instead of OpenAI's base Whisper. It requires less RAM and allows `word_timestamps=True`.
- For English: Use `base.en` or `tiny.en`.
- For Thai or mixed languages: Use `small` or `medium` (Base/Tiny often lack accuracy for non-Latin script parsing).

```python
from faster_whisper import WhisperModel

def generate_ass(audio_path, output_ass_path):
    model = WhisperModel("base", device="cpu", compute_type="int8")
    segments, info = model.transcribe(audio_path, beam_size=5, word_timestamps=True)
    
    # Write ASS Header
    ass_events = []
    for segment in segments:
        for word_info in segment.words:
            start_time = format_timestamp(word_info.start) # H:MM:SS.cs
            end_time = format_timestamp(word_info.end)
            text = word_info.word.strip()
            
            # Example: Karaoke Highlight (Yellow text) using ASS tag {\c&H00FFFF&}
            # (Note: ASS uses BGR hex format for colors)
            styled_text = f"{{\\c&H00FFFF&}}{text}"
            
            # Dialogue: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
            ass_line = f"Dialogue: 0,{start_time},{end_time},Default,,0,0,0,,{styled_text}\n"
            ass_events.append(ass_line)
    
    # ... write header and events to output_ass_path ...
```

## 2. Burning the ASS File via FFmpeg Filter
Once the `.ass` file is generated, burn it directly into the video stream using the `ass` video filter. No MoviePy TextClips required.

```bash
ffmpeg -i video.mp4 -i audio.mp3 -filter_complex "[0:v]ass='subtitles.ass'[vsub]" -map "[vsub]" -map 1:a -c:v libx264 output.mp4
```

### Pitfall: ASS Filter Path Escaping
The `ass=` filter in FFmpeg is extremely strict about file paths, especially on Windows or when the path contains colons/slashes.
**Fix:** Always escape Windows backslashes and drive letter colons before passing to FFmpeg:
```python
safe_ass_path = subtitle_ass_path.replace("\\\\", "/").replace(":", "\\\\:")
filter_string = f"[0:v]ass='{safe_ass_path}'[vsub]"
```

### Pitfall: Slow Whisper on CPU (Thai Language)
Transcribing Thai audio with Faster-Whisper on a CPU-only VPS takes significantly longer than English because the models cannot rely on spaces to tokenize words as easily.
**Fix:** Increase your API/HTTP timeout limits drastically (e.g., from 60s to 300s) when exposing a Whisper-based subtitle endpoint to an orchestrator like n8n, otherwise the connection will drop before FFmpeg even begins rendering.