---
name: faceless-video-reverse-engineering
description: Replicate viral faceless videos into animated compositions.
version: 0.3.0
metadata.hermes.tags:
  - ReverseEngineering
  - FacelessVideo
  - HyperFrames
  - SocialMedia
---

# Faceless Video Reverse-Engineering Pipeline

Reverse-engineer viral social media short videos (Facebook Reels, TikTok, YouTube Shorts) to extract visual design, narrative pacing, and data hierarchy, then reproduce them with HyperFrames and 9Router TTS. Excludes physical filming or human avatar generation. Uses Node.js HyperFrames CLI, Python stdlib, and FFmpeg.

## When to Use

- When tasked with replicating an existing viral Facebook Reel or TikTok.
- When transforming raw telemetry or geographic data into an animated vector video.
- When producing tech podcasts, developer CLI tips, or coding tool explainers.
- When producing emotional life-quote reels ("Read-Loop" atmospheric B-roll format).
- When analyzing post-publish telemetry to optimize retention, completion, and shares.

## Prerequisites

- HyperFrames CLI (`npx hyperframes render`).
- 9Router API listening on port 20128 (`http://127.0.0.1:20128/v1`).
- FFmpeg installed for video frame sampling, text rendering, and audio muxing.
- Hermes messaging gateway configured with Telegram.

## How to Run

1. Extract video and sample key frames using the `terminal` tool.
2. Inspect layout, typography, and hierarchy using the `vision_analyze` tool.
3. Generate TTS audio and HTML/GSAP composition through `scripts/replicate_video.py` via the `terminal` tool.
4. Render 24fps MP4 with HyperFrames and mux audio using the `terminal` tool.
5. Deliver uncompressed file to Telegram using `hermes send --to telegram "[[as_document]] ..."`.

## Quick Reference

- **Download Facebook Reel**: `curl -sL -A "Mozilla/5.0" "<URL>" | grep -o 'https://video[^"&]*mp4'`
- **Sample Key Frames**: `ffmpeg -y -ss <TIME> -i input.mp4 -vframes 1 frame.jpg`
- **Generate 9Router TTS**: `POST http://127.0.0.1:20128/v1/audio/speech` with model `edge-tts/th-TH-NiwatNeural`
- **Render HyperFrames**: `npx hyperframes render . -o raw.mp4 --quality draft -f 24`
- **Mux Audio & Video**: `ffmpeg -y -i raw.mp4 -i audio.mp3 -c:v copy -c:a aac -b:a 192k -shortest final.mp4`
- **Telegram Document Delivery**: `hermes send --to telegram "[[as_document]] <Caption> MEDIA:<path>"`

## Blueprints & Archetypes

1. **Animated GIS Map (`templates/animated-gis-map-reel.html`)**:
   - 3-Zone HUD: Brand header pill, central vector schematic map with pulsing telemetry pins, and bottom alert card.
2. **CLI Terminal Tech Explainer (`templates/cli-terminal-explainer.html`)**:
   - Dark HUD Podcast Style: Top mic branding (`AI Daily ~ เล่าให้ฟัง ~`), macOS terminal typing animation, staggered checklist cards (01–04), and standalone CLI callouts.
   - Reference: `references/cli-terminal-upstream-playbook.md`.
3. **Emotional Quote & Read-Loop Reel**:
   - Atmospheric B-roll (POV dusk driving, rain, transit) with static 3-tier gold/white typography.
   - Designed for 7–11s optimal duration driving 150–200% VTR via repeat loops.
   - Reference: `references/emotional-quote-loop-playbook.md`.

## Content Intelligence & Telemetry Matrix

Post-publish telemetry evaluates 5 key ratios (Hook Rate >65%, VTR >35%, Save Rate >3%, Share Velocity >1.5%, Total Engagement >8%). Use the triage matrix to adjust subsequent video hooks, pacing, and visual layouts.
- Detailed formulas & triage: `references/content-telemetry-triage-matrix.md`.

## Procedure

1. **Snoop & Download Target Video**
   Use `terminal` to resolve the direct media URL and download the MP4:
   ```bash
   curl -sL -A "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X)" "$REEL_URL" | \
     python3 -c "import sys, re, urllib.request, html; m = re.search(r'\"(https://video[^\"]+?)\"', sys.stdin.read()); urllib.request.urlretrieve(html.unescape(m.group(1)), '/tmp/target_reel.mp4') if m else None"
   ```

2. **Deconstruct Video Anatomy**
   Sample key timestamps across 0s, 15s, 30s, 60s, 90s:
   ```bash
   ffmpeg -y -ss 00:00:05 -i /tmp/target_reel.mp4 -vframes 1 /tmp/scene_05s.jpg
   ffmpeg -y -ss 00:00:30 -i /tmp/target_reel.mp4 -vframes 1 /tmp/scene_30s.jpg
   ```
   Inspect images using `vision_analyze` to extract:
   - Layout hierarchy: Header branding, center cards, bottom captions.
   - Color palette, typography, and card spacing.
   - Pacing, motion dynamics, and voice/audio transcript.

3. **Synthesize Voiceover with 9Router TTS (When Applicable)**
   Use Python via `terminal` to query local 9Router:
   ```bash
   python3 -c "
   import urllib.request, json, yaml
   with open('/home/thaieasyvps/.hermes/profiles/nong-makham/config.yaml') as f:
       key = yaml.safe_load(f)['providers']['9router']['api_key']
   req = urllib.request.Request('http://127.0.0.1:20128/v1/audio/speech',
       headers={'Authorization': f'Bearer {key}', 'Content-Type': 'application/json'},
       data=json.dumps({'model': 'edge-tts/th-TH-NiwatNeural', 'input': '$SCRIPT_TEXT'}).encode('utf-8'))
   with urllib.request.urlopen(req) as resp, open('audio.mp3', 'wb') as out:
       out.write(resp.read())
   "
   ```

4. **Author Composition (HTML/GSAP or FFmpeg Filter)**
   Create composition matching the audio duration:
   - Constrain content inside safe-zone `x: 60 to 1020` to prevent mobile edge clipping.
   - For explainer videos: Sequence cards using staggered GSAP tweens (`0.3s` - `0.4s` per entry).
   - For emotional quote reels: Apply static 3-tier text overlay over looping B-roll.

5. **Render, Mux, and Verify**
   Render and mux with AAC audio:
   ```bash
   npx hyperframes render . -o raw.mp4 --quality draft -f 24
   ffmpeg -y -i raw.mp4 -i audio.mp3 -c:v copy -c:a aac -b:a 192k -shortest final.mp4
   ```
   Extract a mid-point frame and run `vision_analyze` to confirm zero clipping.

6. **Deliver as Uncompressed Document**
   Send to Telegram as raw document to preserve quality:
   ```bash
   hermes send --to telegram "[[as_document]] <Caption> MEDIA:<path_to_final.mp4>"
   ```

## Pitfalls

- **Empty Text with `MEDIA:`**: Emitting `MEDIA:<path>` without text causes the gateway to strip the message. Always include descriptive caption text alongside the media tag.
- **Asymmetric List Badges**: When adding alert tags to list cards, ensure all cards in the set have balanced status tags. A single tagged card creates visual asymmetry and looks incomplete under vision inspection.
- **Mixed-Language Status Badges**: Avoid mixing English tech jargon (e.g., `syntax error`) inside Thai badge rows; keep pill badges in consistent Thai (e.g., `ฟอร์แมตพัง`).
- **Delayed Card Entrance in Short Reels**: Do not drag card entrance staggers past the halfway mark of a scene. All list cards must be fully displayed within the first 1.5 seconds of the beat to allow viewers time to absorb the text.
- **Over-Extending Emotional Quote Duration**: Setting quote reels to 25+ seconds without voice narration causes heavy drop-off. Limit to 7–11s to trigger multiple loop completions.
- **SVG Z-Index Occlusion**: SVG has no z-index property; element order defines paint order. Always place text labels after path lines in DOM order.
- **Software GL Timeout**: Rendering 30fps compositions on headless Linux without GPU acceleration takes ~3 minutes for 20s. Set `-f 24` to reduce capture time and prevent timeout.

## Verification

Run verification script to check audio, video stream parameters, and file delivery readiness:
```bash
ffprobe -v error -show_entries format=duration,size:stream=width,height,codec_name -of json final.mp4
```
A successful artifact reports 1080x1920 h264 video, an active audio stream, and non-zero duration matching the audio track.
