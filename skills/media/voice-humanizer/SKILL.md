---
name: voice-humanizer
description: Process synthetic speech with audio DSP and music ducking.
version: 0.1.0
metadata:
  hermes:
    tags:
      - Audio
      - TTS
      - DSP
      - Voiceover
      - Mastering
---

# Voice Humanizer

Post-processes flat, robotic synthetic speech (Edge-TTS, 9Router, gTTS) into warm, natural studio-grade voiceovers using digital signal processing (DSP) and dynamic background ducking. It fixes digital harshness, restores missing chest resonance, injects subtle room reflections, and balances voice against background music. It does not train voice models or perform real-time speech synthesis. Operates on CPU via Spotify Pedalboard, SoundFile, and FFmpeg without GPU dependencies.

## When to Use

- "เสียง TTS ฟังดูปลอมมาก ช่วยปรับให้เป็นธรรมชาติ" (TTS sounds too robotic, make it natural)
- "ปรับแต่งเสียงพากย์ด้วย Python" (Master voiceover audio using Python)
- "ทำ Audio Ducking ให้เพลงเบาลงตอนคนพูด" (Apply audio ducking when speech is active)
- "ปรับเสียง TTS ให้ได้มาตรฐาน -14 LUFS" (Normalize voiceover loudness to -14 LUFS)

## Prerequisites

- Python 3.10+ environment with `pedalboard` and `soundfile` installed.
- System FFmpeg binary available in PATH with `libmp3lame` and `loudnorm` filters.
- Input raw voice file (WAV or MP3) from any TTS engine.

## How to Run

1. Place or generate your raw TTS narration file.
2. Invoke `scripts/humanize_voice.py` through the `terminal` tool with your raw audio and optional background music.
3. Inspect output audio parameters with `ffprobe` or playback directly.

## Quick Reference

- **Humanize Voice Only**: `python3 scripts/humanize_voice.py --voice raw_tts.mp3 --out mastered.mp3`
- **Humanize with BGM Ducking**: `python3 scripts/humanize_voice.py --voice raw_tts.mp3 --bgm music.mp3 --out final_mix.mp3`
- **Inspect Loudness Level**: `ffmpeg -i mastered.mp3 -af ebur128=framelog=verbose -f null -`
- **Run Verification Test**: `python3 scripts/humanize_voice.py --test`

## Procedure

1. **Synthesize Raw Audio from TTS**
   Generate raw narration using your configured TTS engine (e.g. Edge-TTS or 9Router speech endpoint):
   ```bash
   curl -s -X POST http://127.0.0.1:20128/v1/audio/speech \
     -H "Authorization: Bearer $ROUTER9_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{"model": "edge-tts/th-TH-NiwatNeural", "input": "ข้อความทดสอบ"}' \
     --output /tmp/raw_narration.mp3
   ```

2. **Execute DSP Audio Mastering**
   Invoke `scripts/humanize_voice.py` through the `terminal` tool. The script applies the 7-stage mastering chain:
   ```bash
   python3 scripts/humanize_voice.py \
     --voice /tmp/raw_narration.mp3 \
     --bgm /home/thaieasyvps/zero-touch-infrastructure/workspace/assets/bgm/lofi_test.mp3 \
     --out /tmp/final_master.mp3
   ```

   The processing stages executed are:
   - **Stage 1 (High-pass 80Hz):** Cleans sub-bass boom and microphone rumble.
   - **Stage 2 (Peak 180Hz +3.5dB):** Restores chest resonance and physical vocal thickness.
   - **Stage 3 (Peak 3500Hz -2.5dB):** Notches out harsh nasal digital sibilance.
   - **Stage 4 (High-shelf 9000Hz +2.0dB):** Adds condenser microphone presence and air.
   - **Stage 5 (Distortion 1.5dB):** Introduces warm even-harmonic tube saturation.
   - **Stage 6 (Compressor):** Levels dynamics (threshold -15dB, ratio 3.2:1, attack 12ms, release 90ms).
   - **Stage 7 (Micro-Reverb 4%):** Blends subtle room reflections to counter synthetic dryness.

3. **Apply Dynamic Sidechain Ducking**
   When `--bgm` is passed, the script ducks the background music automatically using FFmpeg sidechain compression:
   ```bash
   # Attenuates BGM by -18dB while voice is active, restores smoothly during pauses
   ffmpeg -y -i bgm.mp3 -i voice.wav \
     -filter_complex "[0:a]volume=0.20[b]; [b][1:a]sidechaincompress=threshold=0.04:ratio=8:attack=15:release=250[ducked]; [ducked][1:a]amix=inputs=2:duration=first[out]; [out]loudnorm=I=-14:TP=-1.5:LRA=9" \
     -c:a libmp3lame -b:a 192k output.mp3
   ```

4. **Verify Platform Loudness Standard**
   Ensure the output meets -14 LUFS for TikTok, Reels, and YouTube Shorts.

## Pitfalls

- **Anechoic Flatness:** Raw TTS is recorded in artificial mathematical silence. Without 4% micro-reverb, human ears immediately detect it as artificial.
- **Excessive Saturation:** Keeping drive above 3.0dB adds audible fuzz and clipping. Maintain tube drive between 1.0dB and 1.8dB for subtle warmth.
- **Sidechain Pumping:** Setting compressor release below 100ms causes background music volume to bounce unnaturally between words. Keep release at 250ms for smooth transitions.
- **Frequency Clashing:** Never boost both BGM mid-frequencies and vocal chest frequencies simultaneously. BGM volume must be scaled down before entering the sidechain mixer.

## Verification

Run the verification flag via the `terminal` tool:
```bash
python3 /home/thaieasyvps/.hermes/profiles/nong-makham/skills/media/voice-humanizer/scripts/humanize_voice.py --test
```
The command outputs `VOICE_HUMANIZER_TEST_OK` confirming that pedalboard, soundfile, and script dependencies are intact.
