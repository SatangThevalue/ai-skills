---
name: tts-audio-post-processing
description: "Techniques for processing, chunking, and mastering AI-generated Thai audio (Edge-TTS / gTTS)."
version: 0.1.0
metadata:
  hermes:
    tags: [Audio, TTS, FFmpeg, Voiceover, Post-Processing]
    related_skills: [thai-faceless-video-automation]
---

# TTS & Audio Post-Processing Pipeline

This skill covers the generation of text-to-speech (TTS) audio and the subsequent audio engineering required to make it sound professional and engaging for short-form videos. It focuses on free tools like `Edge-TTS` combined with `FFmpeg` audio filters.

## When to Use
- Converting LLM-generated Thai scripts into voiceovers.
- Applying "Audio Ducking" (lowering BGM when voice is active).
- Normalizing volume levels to meet platform standards (LUFS).

## Prerequisites
- Python environment.
- `edge-tts` installed (`uv pip install edge-tts`).
- `ffmpeg` installed.

## How to Run
Invoke generation via CLI commands or Python subprocess through the `terminal` tool.

## Quick Reference
- Edge-TTS Thai Voices: `th-TH-PremwadeeNeural` (Female), `th-TH-NiwatNeural` (Male)
- Adjust speed: `--rate=+10%`
- Adjust pitch: `--pitch=-5Hz`

## Procedure

1. **Generate Raw TTS Audio**
   Use `edge-tts` to convert a text file or string into an MP3.
   ```bash
   edge-tts --voice th-TH-PremwadeeNeural --rate=+15% --text "สวัสดีค่ะ วันนี้มีของดีมาบอกต่อ" --write-media voiceover.mp3
   ```
   *Note: Increasing the rate by 10-15% is crucial for TikTok/Reels, as viewers prefer fast-paced speaking.*

2. **Mastering the Audio (FFmpeg)**
   Raw TTS often lacks "punch" or sounds thin. Use FFmpeg to apply compression, EQ, and normalization.
   ```bash
   # Add bass, compress dynamic range, and normalize to -14 LUFS (YouTube/TikTok standard)
   ffmpeg -i voiceover.mp3 -af "compand=attacks=0:points=-80/-80|-15/-15|0/-10.8|20/-5.2, loudnorm=I=-14:TP=-1.5:LRA=11" mastered_voice.mp3
   ```

3. **Audio Ducking (Mixing with BGM)**
   Combine the voiceover with background music, automatically lowering the BGM volume when the voice speaks.
   ```bash
   # [0:a] is BGM, [1:a] is Voiceover. Sidechain compress the BGM based on Voiceover.
   ffmpeg -i bgm.mp3 -i mastered_voice.mp3 -filter_complex \
   "[0:a]volume=0.5[bgm_low]; \
    [bgm_low][1:a]sidechaincompress=threshold=0.0625:ratio=10:attack=5:release=50[bgm_ducked]; \
    [bgm_ducked][1:a]amix=inputs=2:duration=first[out]" \
   -map "[out]" final_audio_mix.mp3
   ```

## Pitfalls
- **Unnatural Pauses:** `edge-tts` will pause at punctuation. If the LLM generates a script without commas or periods, the voice will run out of breath and sound robotic. Instruct the LLM to use `...` or `,` for pacing.
- **Volume Clipping:** Simply adding two audio tracks (`amix`) without lowering the volume of one will cause distortion/clipping. Always lower BGM volume *before* mixing.
- **Thai Word Tokenization:** TTS engines occasionally mispronounce Thai words that have ambiguous tokenization (e.g., "ตากลม" vs "ตา-กลม"). Use phonetic spelling in the script if a specific brand name is continually mispronounced.

## Verification
Play the `final_audio_mix.mp3` to ensure the voice is clearly audible over the background music, and the overall volume does not clip.