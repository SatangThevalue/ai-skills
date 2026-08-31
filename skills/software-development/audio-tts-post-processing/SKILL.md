---
name: audio-tts-post-processing
description: Techniques for processing, chunking, and mastering AI-generated TTS audio using Python (Pedalboard, Soundfile).
---
# Audio TTS Post-Processing & Mastering

Use this skill when asked to improve the quality of raw Text-to-Speech (TTS) output, add studio effects (podcast, audiobook, radio), or handle long-text TTS generation without crashing the GPU.

**See also:**
- [references/faster-whisper-subtitles.md](references/faster-whisper-subtitles.md) - Integrating Faster-Whisper for dynamic ASS subtitles.

## Long-Text Chunking & GPU Concurrency (OOM Prevention)
Raw TTS models (like CosyVoice, OmniVoice, XTTS) often crash with Out of Memory (OOM) errors or hallucinate on long text. 
1. **Regex Splitting:** Split long text by punctuation while keeping the punctuation intact so prosody isn't lost: 
   `chunks = re.split(r'(?<=[.!?\n])\s+', full_text.strip())`
2. **GPU Lock:** Wrap inference in `asyncio.Lock()` so concurrent API requests (e.g., from an n8n webhook) don't trigger simultaneous GPU loads. Use separate locks for CPU processes (e.g. Piper) and GPU processes.
3. **Concatenation:** Generate audio arrays chunk-by-chunk, append a short silence (e.g., `np.zeros((int(sample_rate * 0.2), channels))`) between sentences, and use `np.concatenate(arrays, axis=0)` before saving with `soundfile.write`. Note: If simply writing out a NumPy concatenation via `soundfile`, you usually *do not* need to wrap it in `asyncio.to_thread` since `sf.write` on small-medium numpy arrays is highly optimized and very fast. Wrapping simple fast operations in thread executors can actually cause lockups.

## Advanced Studio Presets

When processing TTS for different contexts, use specialized Pedalboard chains:

```python
from pedalboard import Pedalboard, Compressor, HighpassFilter, LowShelfFilter, HighShelfFilter, NoiseGate, Limiter, Reverb, Chorus, Distortion, PitchShift, Delay

# 1. Podcast Studio (Deep, rich, compressed)
# bass=5.0, treble=3.5, comp=3.5, gate=True

# 2. Audiobook Pro (Clean, slight room reflection)
# bass=2.0, treble=2.0, comp=2.5, reverb=0.15, gate=True

# 3. Vintage Radio (90s FM style)
# bass=7.0, treble=5.0, comp=6.0, drive=10.0, gate=True

# 4. Old Telephone (Muffled, cracked)
# bass=-15.0, treble=-8.0, comp=5.0, drive=25.0, gate=True
# NOTE: Requires aggressive Highpass (e.g., 300Hz) to remove all low-end.

# 5. Anonymous / Pitch Shift
# pitch=-4 (semitones)

### 3. Foley & Breath Insertion (Adding Human Realism)

TTS engines often produce audio with perfect, absolute silence between sentences. This "digital silence" is a dead giveaway of AI generation. To fix this, detect the silent gaps and insert human Foley (breaths) or synthesize them mathematically.

#### 4. Multi-Speaker Script Parsing

For podcasts or dialogue involving multiple speakers, parse a script format (e.g., `[Speaker: model_name] text`) to dynamically switch TTS models and pad pauses between turns. When concatenating these chunks using NumPy, ensure all arrays match in dimensions (e.g., shape `(N,)` vs `(N, 1)`) to avoid dimension mismatch errors:

```python
import numpy as np

all_audio_arrays = []

for chunk in chunks:
    audio_data, sr = generate_audio(chunk) # e.g. shape (N,) or (N, 1)
    
    # Pad with 0.6s silence between turns
    pause_samples = int(sr * 0.6)
    
    if len(audio_data.shape) > 1:
        # Stereo / 2D
        pause = np.zeros((pause_samples, audio_data.shape[1]))
    else:
        # Mono / 1D - Must reshape to 2D if you want consistency!
        pause = np.zeros((pause_samples,))
        audio_data = audio_data.reshape(-1, 1)
        pause = pause.reshape(-1, 1)

    all_audio_arrays.append(audio_data)
    all_audio_arrays.append(pause)

final_audio = np.concatenate(all_audio_arrays, axis=0)
```
```python
import soundfile as sf
import numpy as np
from pydub import AudioSegment
from pydub.silence import split_on_silence

# For PiperTTS or any raw model that outputs "digital silence" between phrases
# This inserts human-like pacing without real foley breath files

def humanize_pacing(input_wav, output_wav):
    sound = AudioSegment.from_wav(input_wav)
    
    # Split audio where silence is > 350ms (or slightly lower for faster speech)
    chunks = split_on_silence(
        sound,
        min_silence_len=350,
        silence_thresh=sound.dBFS - 16, # Adjust threshold based on noise floor
        keep_silence=150 # Leave a small tail on each word
    )

    # Insert a synthetic gap mimicking human pacing (e.g., taking a breath)
    # Using 350ms gap
    natural_gap = AudioSegment.silent(duration=350)
    
    final_audio = AudioSegment.empty()
    for i, chunk in enumerate(chunks):
        final_audio += chunk
        if i < len(chunks) - 1:
            final_audio += natural_gap # Insert pause between phrases

    final_audio.export(output_wav, format="wav")
```

### Advanced Studio Mastering Chain (Specific for Piper TTS)
Piper TTS models often output audio that is slightly muffled or "boxy" compared to modern online models like Edge-TTS. When applying `pedalboard` mastering to Piper, push the high-frequency shelf significantly more to restore brightness.

```python
from pedalboard import Pedalboard, Compressor, HighpassFilter, LowShelfFilter, HighShelfFilter, NoiseGate, Limiter, Reverb, Chorus, Distortion

# Piper-specific EQ: Cut mud, push brightness aggressively (+5.0dB)
piper_board = Pedalboard([
    HighpassFilter(cutoff_frequency_hz=100), 
    LowShelfFilter(cutoff_frequency_hz=250, gain_db=2.0),
    HighShelfFilter(cutoff_frequency_hz=4000, gain_db=5.0), # Critical: Brightness boost for Piper
    Distortion(drive_db=3.0),
    Compressor(threshold_db=-22, ratio=3.0, attack_ms=2.0, release_ms=100),
    Chorus(rate_hz=1.2, depth=0.03, mix=0.1), 
    Reverb(room_size=0.2, damping=0.7, wet_level=0.15, dry_level=0.9)
])
```s, keeping the punctuation
chunks = re.split(r'(?<=[.!?\n])\s+', full_text.strip())

all_audio_arrays = []
for chunk in chunks:
    # ... generate audio_data (numpy array) ...
    
    # 2. Reshape Mono arrays for consistency before concatenation!
    # A common dimension mismatch error occurs when combining 1D mono (N,) 
    # with 2D pauses (N, 1) or Stereo (N, 2).
    if len(audio_data.shape) == 1:
        audio_data = audio_data.reshape(-1, 1)
        
    all_audio_arrays.append(audio_data)
    
    # Add a natural 0.6s pause between sentences (or when speakers change)
    pause_samples = int(sample_rate * 0.6)
    
    # Always reshape mono data and pause arrays to 2D before concatenation
    if len(audio_data.shape) > 1:
        pause = np.zeros((pause_samples, audio_data.shape[1]))
    else:
        pause = np.zeros((pause_samples,))
        audio_data = audio_data.reshape(-1, 1)
        pause = pause.reshape(-1, 1)
        
    all_audio_arrays.append(audio_data)
    all_audio_arrays.append(pause)

# Concatenate all arrays
final_audio = np.concatenate(all_audio_arrays, axis=0)
```

## Studio Mastering (Pedalboard)
Use Spotify's `pedalboard` library instead of `pydub` for high-quality, VST-like processing. It is faster and supports professional DSP effects.
    
### ⚠️ Pitfalls & Gotchas

#### 1. TTS Pacing and Silence Injection (Humanize)
Text-to-speech models often output abrupt silence between phrases. Splitting the audio using `pydub.silence.split_on_silence` and inserting 250-350ms of generative natural gaps (e.g. `AudioSegment.silent(duration=350)`) before re-merging significantly increases perceived human-likeness. Additionally, lowering the TTS generation rate slightly (e.g. `edge-tts --rate="-15%"`) deepens the tone and produces a more relaxed pacing.

#### 2. EQ Compensation per Engine
- **Piper TTS**: Generally sounds flatter/duller. Requires EQ compensation: Highpass at 100Hz, strong HighShelf (+5dB at 4kHz) to add brightness.
- **Edge-TTS**: Brighter and sharper, but more digital. Use analog emulation (Distortion/Drive) and a de-esser (HighShelf cut around 6kHz).

#### 3. Font Rendering in FFmpeg (Thai/Non-Latin)
When using FFmpeg's `drawtext` filter for languages like Thai, relying on system font fallbacks often results in square boxes. 
*   **Fix:** Always pass an absolute path to a known-good TTF font (e.g. `Sarabun-Bold.ttf`) directly to the `fontfile` option in FFmpeg.
*   **Best Practice:** Resolve the path dynamically relative to your project's base directory so it survives deployment to new hosts: `font_file=os.path.join(BASE_DIR, 'assets', 'fonts', 'Sarabun-Bold.ttf')` -> `fontfile='{font_file}'`.

#### 4. Automated Video Formats (9:16 vs 16:9)
When building automated video pipelines for social media (TikTok, Reels, Shorts), the aspect ratio is strictly vertical **9:16 (1080x1920)**. 
*   **Pitfall:** Confusing 16:9 (horizontal) with 9:16 (vertical). For social media templates, always scale and crop to `1080:1920`.
*   **Smart Background Blur Filter (FFmpeg):** To convert any horizontal/square video into a polished 9:16 vertical video with a blurred background:
    ```bash
    [0:v]split=2[bg][fg];[bg]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,gblur=sigma=30[bg_blur];[fg]scale=1080:1920:force_original_aspect_ratio=decrease[fg_scaled];[bg_blur][fg_scaled]overlay=(W-w)/2:(H-h)/2[out]
    ```

#### 5. Array Shape Mismatch
*   `soundfile.read()` returns numpy arrays in the shape `(samples, channels)`
*   `pedalboard` requires arrays in the shape `(channels, samples)`.
*   **Fix:** Check dimensions and transpose before and after processing:
    ```python
    import soundfile as sf
    from pedalboard import Pedalboard
    
    audio_data, sample_rate = sf.read("input.wav")
    if len(audio_data.shape) > 1:
        audio_data = audio_data.T  # Transpose for Pedalboard
        
    board = Pedalboard([...])
    effected = board(audio_data, sample_rate)
    
    if len(effected.shape) > 1:
        effected = effected.T      # Transpose back for Soundfile
    sf.write("output.wav", effected, sample_rate)
    ```

### Wave writing requirement (Piper TTS compatibility)
Some TTS libraries like Piper write raw audio output without wave headers when given a standard Python file handle. To ensure `soundfile` or `pedalboard` can read the generated file, force the output file handle to be a properly configured `wave` object:

```python
import wave
from piper.voice import PiperVoice

voice = PiperVoice.load(model_path)
with wave.open("temp.wav", "wb") as wav_file:
    wav_file.setnchannels(1)
    wav_file.setsampwidth(2)
    wav_file.setframerate(22050) # Standard piper sample rate
    voice.synthesize(text, wav_file)
```

### Advanced Studio Mastering Chain
```python
from pedalboard import Pedalboard, Compressor, HighpassFilter, LowShelfFilter, HighShelfFilter, NoiseGate, Limiter, Reverb, Chorus, Distortion, PitchShift, Delay, Convolution

board = Pedalboard([
    NoiseGate(threshold_db=-40.0, ratio=1.5, release_ms=250),
    HighpassFilter(cutoff_frequency_hz=80), # Remove low rumble
    LowShelfFilter(cutoff_frequency_hz=120, gain_db=5.0), # Proximity effect (Bass)
    HighShelfFilter(cutoff_frequency_hz=6500, gain_db=-2.0), # De-essing (Dynamic EQ emulation)
    HighShelfFilter(cutoff_frequency_hz=10000, gain_db=3.5), # Clarity (Air)
    Distortion(drive_db=5.0), # Tape Saturation (Analog warmth)
    Compressor(threshold_db=-15, ratio=3.5, attack_ms=2.0, release_ms=100), # Dynamics
    Convolution("path/to/ir.wav", mix=0.1), # Real room acoustic fingerprint (Impulse Response)
    Chorus(rate_hz=0.5, depth=0.05, mix=0.1), # Humanize (Micro-modulation)
    Limiter(threshold_db=-1.0) # Safety clipping prevention
])
```

## FastMCP Mounting with FastAPI
In newer versions of the `mcp` library (1.0.0+), the `FastMCP` class exposes its Starlette app slightly differently depending on the version. To mount it securely in a FastAPI application:

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("My_MCP_Server")

# Register tools directly on the FastMCP instance
@mcp.tool()
def my_tool(param: str) -> str:
    return "ok"

# Safe mounting
try:
    if hasattr(mcp, 'get_starlette_app'):
        app.mount("/sse", getattr(mcp, 'get_starlette_app')())
    elif hasattr(mcp, '_mcp_server'):
        from starlette.applications import Starlette
        from starlette.routing import Mount, Route
        from mcp.server.sse import SseServerTransport
        
        sse = SseServerTransport("/messages")
        async def handle_sse(request):
            async with sse.connect_sse(request.scope, request.receive, request._send) as streams:
                await mcp._mcp_server.run(streams[0], streams[1], mcp._mcp_server.create_initialization_options())
        async def handle_messages(request):
            await sse.handle_post_message(request.scope, request.receive, request._send)
            
        mcp_app = Starlette(routes=[
            Route("/", endpoint=handle_sse),
            Route("/messages", endpoint=handle_messages, methods=["POST"])
        ])
        app.mount("/sse", mcp_app)
except Exception as e:
    print(f"Warning: MCP SSE mounting failed: {e}")
```

## LLM Auto-Tagging for Emotions
To insert emotion tags (e.g., `[laughter]`, `<|happy|>`), use a lightweight LLM prompt to dynamically analyze the text and insert supported model tags naturally, rather than forcing the user to memorize syntax. Provide the LLM with strict instructions to *only* insert tags and not alter the original text.