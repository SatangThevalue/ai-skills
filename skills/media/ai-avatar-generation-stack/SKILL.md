---
name: ai-avatar-generation-stack
description: "Tools and APIs for creating consistent AI avatars and talking-head videos."
version: 0.1.0
metadata:
  hermes:
    tags: [AI, Avatar, Talking-Head, Replicate, Video, Monetization]
    related_skills: [python-ai-video-monetization, zero-touch-monetization-playbook]
---

# AI Avatar & Talking Head Generation

This skill documents the tool stack and architectural considerations for generating "talking head" videos from a single source image and an audio file. This prevents the "Temporal Inconsistency" (face morphing) commonly seen in text-to-video generation and is essential for building a consistent virtual persona for monetization (courses, personal branding, affiliate marketing).

## When to Use
- When the user wants to create a virtual clone of themselves for videos.
- When expanding a faceless channel into an avatar-led channel to increase viewer trust.
- When generating lipsynced video from TTS audio.

## Prerequisites
- High-quality, clear source image (front-facing, closed mouth, plain background).
- Generated TTS audio file (e.g., from `edge-tts`).
- `replicate` Python library (`uv pip install replicate`).
- Replicate API Token (`REPLICATE_API_TOKEN`).

## How to Run
Invoke the Python script through the `terminal` tool. The script sends the image and audio to the Replicate API, waits for processing, and downloads the resulting MP4.

## Quick Reference
- **Model (Best Open Source):** `LivePortrait` (KwaiVGI / Tencent)
- **Model (Alternative Open Source):** `SadTalker` (OpenTalker)
- **Commercial Alternatives:** Hedra, HeyGen (Enterprise level, separate APIs)
- **Replicate Client:** `replicate.run(...)`

## Procedure

1. **Prepare the Source Image**
   Ensure the image adheres to these strict rules to prevent distortion:
   - Well-lit, front-facing.
   - **Mouth completely closed** (no teeth showing).
   - No obstructions (hands, excessive hair) over the face or neck.
   - Solid or simple background (can be keyed out later via FFmpeg/AI).

2. **Setup the Replicate Client**
   Install the library and export your token.
   ```bash
   uv pip install replicate
   export REPLICATE_API_TOKEN="r8_..."
   ```

3. **Generate the Avatar Video via Replicate (LivePortrait)**
   Create a script `scripts/avatar_generator.py`:
   
   ```python
   import replicate
   import os
   import requests

   def generate_talking_head(image_path, audio_path, output_path):
       print("🚀 Uploading assets and starting LivePortrait generation on Replicate...")
       
       # Note: The exact model string might change; verify on replicate.com
       # We use an example model identifier for a LivePortrait implementation
       model_id = "fofr/liveportrait:30ce5eea1b3c95e1ebff5bdcc8e6ec2aa072e21074e0d9b68ff0cfd466f2284e"
       
       try:
           output_url = replicate.run(
               model_id,
               input={
                   "image": open(image_path, "rb"),
                   "audio": open(audio_path, "rb"),
                   # LivePortrait specific params (adjust based on model version)
                   "expression_scale": 1.0,
                   "lip_sync_multiplier": 1.0
               }
           )
           
           print(f"✅ Generation complete. Downloading from: {output_url}")
           
           # Download the resulting MP4
           response = requests.get(output_url)
           response.raise_for_status()
           
           with open(output_path, 'wb') as f:
               f.write(response.content)
               
           print(f"🎉 Avatar video saved to {output_path}")
           return output_path
           
       except Exception as e:
           print(f"❌ Failed to generate avatar: {e}")
           return None

   if __name__ == "__main__":
       # Example execution
       # generate_talking_head("my_face.jpg", "voiceover.mp3", "avatar_output.mp4")
       pass
   ```

4. **Integrate into the Pipeline**
   Once `avatar_output.mp4` is downloaded, feed it into the existing FFmpeg assembler (`ffmpeg-thai-drawtext-pipeline` or PIL overlay method) to add background music, subtitles, and branding.

## Pitfalls
- **Cost:** Running models on Replicate is not free. It bills by the second of GPU time. While cheap (~$0.001 - $0.003 / sec), high-volume generation requires a budget.
- **Rate Limits:** Free or low-tier Replicate accounts may experience queuing or rate limiting. Implement robust error handling and retries.
- **Teeth Distortion:** If the source image has an open mouth, the AI will try to open an already-open mouth when syncing audio, creating a double-mouth or horrific teeth artifact.

## Verification
Run the Python script and inspect the output MP4 file. The lips should move in sync with the provided audio, and the head should exhibit natural micro-movements without severe warping around the neck or background.