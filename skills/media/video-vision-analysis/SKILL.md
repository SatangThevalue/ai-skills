---
name: video-vision-analysis
description: "Framework for scoring and reviewing AI-generated videos before publishing."
version: 0.1.0
metadata:
  hermes:
    tags: [Video, QA, Quality-Assurance, Scoring, Evaluation]
    related_skills: [thai-faceless-video-automation, prefect-orchestration-monetization]
---

# Video QA & Vision Analysis Scoring

This skill defines the Quality Assurance (QA) workflow and scoring matrix used to evaluate auto-generated videos before they are published to social media. It serves as the final "Human/AI-in-the-loop" checkpoint in the Zero-Touch Monetization pipeline.

## When to Use
- Before pushing a generated `.mp4` to Facebook/TikTok/YouTube.
- When grading the quality of an AI-generated script, text overlay, or audio mix.
- When diagnosing why a video looks "cheap" or "robotic".

## Prerequisites
- Completed video file (e.g., `final_showcase_video.mp4`).
- Access to Vision AI (e.g., `vision_analyze` tool or external Gemini Vision API) to extract and inspect frames.

## How to Run
Trigger this scoring matrix via a Prefect task right before the `publish` task. If the total score is `< 80/100`, the pipeline should halt and send an alert via Telegram with the extracted frames for manual review.

## Quick Reference
- Minimum Passing Score: **80 / 100**
- Fatal Errors (Auto-Fail): Missing tone marks, overlapping text, silent audio.

## Procedure (The Scoring Matrix)

Evaluate the video across 4 dimensions (25 points each).

### 1. Typography & Readability (25 pts)
*Extract a frame at 00:00:05 and analyze text.*
- **[10 pts] Thai Grammar:** No missing tone marks (ไม้เอก, ไม้โท) or vowels (สระลอย).
- **[10 pts] Safe Zone:** Text is centered and does not bleed off the left/right edges of a 9:16 frame. Word wrap is functioning.
- **[5 pts] Contrast:** Text has a visible drop shadow or the background is dimmed (vignette/dimming) ensuring it is readable against bright backgrounds.
*Fatal Error:* If Thai tone marks are missing/overlapping (e.g., ยิง แทน ยิ่ง), SCORE = 0.

### 2. Audio & Pacing (25 pts)
*Analyze the audio stream.*
- **[10 pts] BGM Presence:** A background track (Lo-fi/Ambient) is present but does not overpower the main track.
- **[10 pts] Ducking/SFX:** SFX (like typewriter clicks) align with visual changes.
- **[5 pts] Voice Pace (If applicable):** TTS speaks at a natural pace with intentional pauses (no robotic run-on sentences).
*Fatal Error:* If the audio track is entirely silent or clipping violently, SCORE = 0.

### 3. Visual Engagement (25 pts)
*Analyze the overall composition.*
- **[10 pts] Movement:** The background is a video (B-roll), not a static image, to prevent "Sleep Streaming" penalties from algorithms.
- **[10 pts] Text Dynamics:** Text does not appear all at once. It uses staggered pop-ins or typewriter effects (Forced Attention).
- **[5 pts] Subject Clarity:** The text overlay does not completely cover the face of the main human subject (if present in the B-roll).

### 4. Content & Compliance (25 pts)
*Analyze the script text.*
- **[15 pts] The Hook:** The first 3 seconds contain a powerful hook (Outcome showcase, Specific Number, or Contrarian view).
- **[10 pts] Safe Language:** Zero forbidden words (e.g., รักษา, แอดไลน์, ขาวทันที). Must pass `thai-content-compliance`.
*Fatal Error:* If a forbidden word is detected, SCORE = 0.

## Pitfalls
- **False Positives in Vision AI:** Sometimes AI vision models misinterpret Thai tone marks due to low resolution. Always extract frames with high quality (`-q:v 2`) for analysis.
- **Subject Blocking:** If the B-roll subject is on the far left, centered text might cover them. The matrix must account for negative space.

## Verification
Extract a frame using `ffmpeg -ss 00:00:05 -i video.mp4 -vframes 1 -q:v 2 frame.jpg`, pass it to a Vision LLM along with this matrix, and request a structured JSON score out of 100.