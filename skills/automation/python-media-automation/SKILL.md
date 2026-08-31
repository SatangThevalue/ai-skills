---
name: python-media-automation
description: Best practices, pitfalls, and configuration fixes for running Python media libraries (MoviePy, Piper TTS, Pedalboard, PyDub) in automated pipelines or async servers.
---

# Python Media Automation (Video & Audio)

When building automated media pipelines (like AI video generators or TTS studios) in Python using FastAPI or Docker, several critical environment and dependency issues typically arise. This skill outlines the fixes for the most common pitfalls involving MoviePy, Audio DSP, and Local TTS.

## 🎬 Video Processing (MoviePy)

### 1. MoviePy 2.x Migration (Breaking Changes)
- **Imports:** `from moviepy import ...` (no longer `from moviepy.editor import ...`)
- **Immutability:** Most methods return a new object. 
  - `crop()` -> `cropped()`
  - `resize()` -> `resized()`
  - `set_duration()` -> `with_duration()`
  - `set_position()` -> `with_position()`
  - `set_audio()` -> `with_audio()`
  - `volumex()` -> `with_volume_scaled()`
- **TextClip Arguments:** Use named kwargs. `fontsize` is now `font_size`, `align` is `text_align`.

### 2. ImageMagick Dependency (The 'unset' or Policy Error)
- **Symptom:** `MoviePy Error: creation of None failed... [Errno 2] No such file or directory: 'unset'`
- **Cause:** MoviePy relies on ImageMagick for `TextClip`. On Linux/Docker, ImageMagick either isn't installed or its default security policy prevents ghostscript/text rendering.
- **Fix 1 (Dockerfile):**
  ```dockerfile
  RUN apt-get install -y imagemagick && \
      sed -i 's/<policy domain="path" rights="none" pattern="@\*"/<!-- <policy domain="path" rights="none" pattern="@\*" -->/g' /etc/ImageMagick-6/policy.xml || true
  ```
- **Fix 2 (MoviePy v2 Configuration):** Set the path via OS environment variables. The old `moviepy.config.change_settings` was removed in v2.
  ```python
  if os.name == 'posix':
      os.environ["IMAGEMAGICK_BINARY"] = "/usr/bin/convert"
  ```

### 3. Pillow Dependency Bug (MoviePy < 2.0)
- **Symptom:** `module 'PIL.Image' has no attribute 'ANTIALIAS'` during `TextClip` rendering.
- **Cause:** MoviePy 1.x relies on a deprecated Pillow feature removed in Pillow 10+.
- **Fix:** Pin Pillow: `Pillow<10.0.0` OR upgrade to MoviePy `>=2.0.0` and Pillow `>=10.0.0`.

### 4. Thai Fonts & Non-Latin Characters
- If text renders as square boxes (Tofu), you must provide the absolute path to a `.ttf` file.
- **Fix:** Download `Sarabun-Bold.ttf` and pass `font="/path/to/Sarabun-Bold.ttf"` into `TextClip`.

### 5. MoviePy Deadlocks in FastAPI (CPU/RAM Exhaustion)
- **Symptom:** FastAPI server hangs entirely during video render, causing n8n or client timeouts.
- **Fix 1 (Unblock Event Loop):** Wrap the MoviePy code in `asyncio.to_thread()` or `concurrent.futures.ProcessPoolExecutor()`.
- **Fix 2 (Prevent Thread Starvation):** In `write_videofile`, use conservative CPU thread counts and fast presets.
  ```python
  video.write_videofile(out, fps=25, threads=2, preset="ultrafast", logger=None)
  ```

## 🎙️ Audio Processing & TTS

### 1. Piper TTS: Valid WAV Output
- **Symptom:** `Format not recognised` when trying to read the synthesized output from Piper.
- **Cause:** Piper's `synthesize()` writes raw audio data if the provided file object doesn't already have valid WAV headers.
- **Fix:** Use the standard `wave` module to construct the headers before passing the file object:
  ```python
  import wave
  from piper.voice import PiperVoice
  
  voice = PiperVoice.load("model.onnx")
  with wave.open("out.wav", "wb") as wav_file:
      wav_file.setnchannels(1)
      wav_file.setsampwidth(2)
      wav_file.setframerate(22050) # Standard Piper sample rate
      voice.synthesize("Hello world", wav_file)
  ```

### 2. Pydub / Soundfile Concurrency
- `soundfile.read()`, `soundfile.write()`, and Pydub's `AudioSegment` operations are blocking I/O.
- In high-throughput APIs, ensure these are wrapped in `asyncio.to_thread()` if processing large files, though for tiny TTS chunks (1-2s), running them synchronously is often acceptable and avoids thread-spawning overhead.