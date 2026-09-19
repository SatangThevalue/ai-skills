---
name: broll-free-video-automation
description: "Generate high-retention faceless videos without manual B-roll sourcing."
version: 0.1.0
metadata:
  hermes:
    tags: [Video, Automation, FFmpeg, Retention, Faceless]
    related_skills: [ffmpeg-thai-drawtext-pipeline, thai-faceless-video-automation]
---

# B-Roll Free Video Automation (The Gameplay Loop)

This skill outlines strategies and executable workflows for generating high-retention, short-form videos without manually searching for context-specific B-roll footage (e.g., from Pexels). It leverages the "Satisfying Loop" psychological trigger (using gameplay like Minecraft Parkour or GTA V) to hold visual attention while a voiceover delivers unrelated content (stories, facts, reddit threads).

## When to Use
- Mass-producing faceless channels (e.g., Horror stories, Psychology facts, Reddit summaries).
- When context-specific B-roll is too expensive, time-consuming, or inaccurate to source via AI.
- Maximizing viewer retention (Watch Time) with zero visual-sourcing effort.

## Prerequisites
- A large, local source video of satisfying gameplay (e.g., a 1-hour royalty-free Minecraft Parkour video) saved on the VPS.
- `ffmpeg` installed.
- Python 3.

## How to Run
Invoke the provided Python script `scripts/gameplay_broll_automation.py` through the `terminal` tool to randomly slice the master video and assemble the final output.

## Quick Reference
- Get video duration: `ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 <file>`
- Slice video: `ffmpeg -ss <start_time> -i <input> -t <duration> -c copy <output>`
- Burn ASS subtitles: `ffmpeg -i <vid> -i <aud> -vf ass='<file.ass>' -shortest <out.mp4>`

## Procedure

1. **Source the Master Gameplay File**
   Download a 1-hour+ royalty-free or creative-commons gameplay video (Minecraft Parkour, GTA V racing, ASMR kinetic sand). Save it to the VPS (e.g., `parkour_1hr.mp4`).

2. **The Random Slicer (Python)**
   To ensure every generated short looks unique, use Python to randomly select a start time from the master file and slice out a segment equal to the voiceover length.
   *(See `scripts/gameplay_broll_automation.py` for the exact implementation).*

   ```python
   # Pseudocode logic:
   total_duration = probe_duration("parkour_1hr.mp4")
   start_time = random.randint(0, total_duration - 60)
   
   # FFmpeg slice command
   cmd = f"ffmpeg -ss {start_time} -i parkour_1hr.mp4 -t 60 -c:v libx264 -an sliced_bg.mp4"
   ```
   *Note: `-an` removes the original gameplay audio to prevent interference with the voiceover.*

3. **Subtitles & Voiceover Assembly**
   Generate TTS audio and an `.ass` (Advanced SubStation Alpha) subtitle file using `faster-whisper`.
   Combine the sliced background, the TTS audio, and burn the subtitles directly onto the video in one pass.
   
   ```bash
   ffmpeg -y -i sliced_bg.mp4 -i tts_audio.mp3 -vf "ass='karaoke_subs.ass'" -c:v libx264 -preset fast -crf 23 -c:a aac -b:a 192k -shortest final_short.mp4
   ```
   *Note: `-shortest` ensures the video ends exactly when the TTS audio finishes, cleanly trimming any excess gameplay footage.*

## Pitfalls
- **Copyright Claims:** Ensure the gameplay footage is truly royalty-free or falls under fair use. Avoid videos with prominent UI elements, copyrighted music, or streamer facecams.
- **Audio Clashes:** Failing to use the `-an` flag during slicing will leave the original game audio (explosions, music) in the background, making the TTS hard to hear.
- **Stale Visuals:** If the master video is too short (e.g., 5 minutes) and you generate 50 clips a day, the audience will quickly recognize repeating loops. Use master files that are at least 1 hour long.

## Verification
Run the python script `scripts/gameplay_broll_automation.py` (with valid paths) via the `terminal` tool. Inspect the resulting `.mp4` using `ffprobe` to confirm it matches the length of the provided audio and contains no original gameplay audio.