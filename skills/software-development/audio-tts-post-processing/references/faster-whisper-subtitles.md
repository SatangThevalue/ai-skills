# Automated Subtitle Generation with Faster-Whisper

When building fully automated video pipelines (e.g., TikTok/Reels generators), static text overlays aren't enough. Viewers expect dynamic, karaoke-style subtitles that highlight words as they are spoken.

## Faster-Whisper Integration
`faster-whisper` (backed by CTranslate2) is lightweight enough to run on CPU instances while being nearly as accurate as the original Whisper.

**Model Selection:**
- English content: `tiny.en` or `base.en` (extremely fast, very accurate for TTS audio).
- Thai/Multilingual content: `small` or `medium` (better accuracy for non-spaced languages).

**Performance Settings:**
```python
from faster_whisper import WhisperModel
# Runs comfortably on standard VPS CPUs with minimal RAM
model = WhisperModel("base", device="cpu", compute_type="int8")
```

## Word-Level Timestamps to ASS Format
To create TikTok-style highlighting, you need *word-level timestamps*, not just sentence segments. Advanced SubStation Alpha (`.ass`) is the best format for this as it supports deep styling (colors, outlines, positioning).

1. Enable word timestamps:
```python
segments, info = model.transcribe(audio_path, beam_size=5, word_timestamps=True)
```

2. Generate `.ass` markup with styling (e.g., Yellow highlight on spoken words):
```python
# ASS syntax for karaoke/color highlight: {\c&H00FFFF&}word 
# Note: Colors in ASS are BGR hex, so 00FFFF is Yellow
```

3. Burn into video via FFmpeg Complex Filter:
```bash
# Important: the path to the .ass file must be safely escaped in FFmpeg
ffmpeg -i input.mp4 -vf "ass='subtitle.ass'" output.mp4
```

## Integrating with FFmpeg
When using FFmpeg's `filter_complex` for dynamic templates:
*   Pass the `.ass` subtitle burn step *before* any final scaling or audio mixing, but *after* background blurring if you want the subtitles crisp over the blurred background.
*   Ensure the `.ass` file has `PlayResX` and `PlayResY` set correctly (e.g., 1080x1920 for vertical video) so font sizing is predictable.