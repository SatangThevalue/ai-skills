---
name: ai-animation-production-pipeline
description: Four-stage AI animation and video production pipeline.
version: 0.1.0
metadata:
  hermes:
    tags:
      - AIAnimation
      - VideoProduction
      - Storyboard
      - ConsistencyLock
      - PromptEngineering
---

# AI Animation Production Pipeline

A standardized, multi-stage production framework for crafting consistent AI animation and cinematic short videos (Reels, TikTok, YouTube Shorts). Solves character drifting, style inconsistency, and disconnected camera framing by enforcing a strict sequential workflow: Storyboard -> Master Asset Lock -> Scene Keyframes -> Image-to-Video Animation.

## When to Use

- When producing multi-shot AI animated videos or storytelling reels.
- When maintaining 100% facial, clothing, and environmental consistency across scenes.
- When transforming a concept or script into actionable prompts for image and video engines.
- When coordinating multi-tool pipelines (FLUX/Midjourney for keyframes + Kling/Veo/Runway for motion).

## Prerequisites

- High-fidelity text-to-image engine (FLUX.1, Midjourney v6, or Gemini Image).
- Image-to-video generator supporting start-frame conditioning (Google Veo, Kling, Runway Gen-3, Haiper, or Minimax).
- Python environment for prompt compiling and FFmpeg for final assembly.

## Quick Reference

| Stage | Core Output | Primary Toolset | Mandatory Rule |
| :--- | :--- | :--- | :--- |
| **1. Storyboard** | Shot list + Focal Framing | Markdown / Scripting | Define every cut and camera angle before prompting. |
| **2. Asset Lock** | Master Character Sheet | T2I (FLUX / Midjourney) | Lock facial traits, skin tone, and signature props. |
| **3. Scene Keyframe** | Compositional Start Frames | I2I / Multi-Reference | Blend character into environment per storyboard shot. |
| **4. Motion Animate** | 3-5s Animated Clips | I2V (Veo / Kling) | **Motion verbs only** — never re-describe clothing. |

> **The Golden Rule:** Never generate Text-to-Video directly. Direct T2V causes continuous visual hallucinations and character morphing. Always condition motion on verified start-frame images.

---

## Procedure

### Stage 1: Script & Storyboard Architecture (The Blueprint)
Never generate visual assets before defining the shot list.

1. **Deconstruct Narrative into 3–5 Key Beats:**
   - Beat 1 (0–3s): Hook / Action trigger (Close-up / Dynamic angle).
   - Beat 2 (3–7s): Core interaction / Discovery (Medium shot).
   - Beat 3 (7–12s): Turning point / Climax (Wide or Low-angle heroic).
   - Beat 4 (12–15s): Resolution / Call to Action.
2. **Assign Shot Parameters per Scene:**
   - Camera lens (e.g. 50mm portrait vs 24mm wide establishing).
   - Shot framing (Macro, Extreme Close-Up, Medium, Establishing).
   - Aspect ratio (`9:16` vertical for mobile reels or `16:9` widescreen).

### Stage 2: Master Asset Lock (Visual DNA)
Create the unchangeable reference image for every recurring subject before placing them into scenes.

1. **Generate Master Character Reference:**
   - Single subject on neutral background (front & three-quarter view).
   - Define exact cultural/identifying anchors (e.g. skin undertone, wrist thread, distinct haircut, clothing texture).
   - Save this image as `master_character.png`.
2. **Generate Master Prop/Creature Reference:**
   - Clean profile and macro view of hero props or creatures.
   - Save as `master_prop.png`.

### Stage 3: Scene Keyframe Generation (Composition Assembly)
Combine master assets with scene-specific environments based on the Storyboard.

1. **Condition on Master Assets:**
   - Use Image-to-Image (I2I) or image reference weights (`--cref` in Midjourney, or multi-reference inputs in FLUX/ComfyUI).
   - Prompt focus: Specify camera framing, lighting direction, and pose matching the storyboard beat.
2. **Enforce Platform Safe Zones:**
   - Ensure critical facial features and hero objects remain within center bounds (`x: 80 to 1000` on 1080x1920) away from UI buttons.
3. **Save Scene Start Frames:**
   - Export approved stills as `scene_01_start.png`, `scene_02_start.png`, etc.

### Stage 4: Image-to-Video Animation (Motion Injection)
Bring keyframes to life through physics-based motion prompting.

1. **Load Keyframe as Start Frame:**
   - Upload `scene_0X_start.png` into the I2V engine.
2. **Structure Motion Prompts with Strict Grammar:**
   - **Allowed:** Directional movement, camera motions, fluid physics, atmospheric drift.
   - **Prohibited:** Re-describing clothing, colors, or facial features (this forces the model to redraw and morph).
   - *Example Good Prompt:* `Smooth upward lift at 24fps. Hands raise the object out of the water. Cascading water droplets splashing with realistic fluid physics. Subtle push-in camera zoom.`
   - *Example Bad Prompt:* `A boy wearing red clothes with black hair lifts a crab.` (Triggers clothing morphing).
3. **Clamp Clip Duration:**
   - Keep motion clips between 3 to 5 seconds to prevent generative breakdown and model drift.

---

## Pitfalls & Edge Cases

- **Motion Hallucination:** Typing character descriptions into the video motion box causes clothing to change color mid-shot. Use verbs exclusively.
- **Aspect Ratio Warping:** Requesting anamorphic lens keywords on vertical 9:16 canvases warps human proportions. Reserve anamorphic keywords for 16:9 widescreen.
- **Skipping the Master Lock:** Jumping straight from script to final scene causes characters to look like completely different people between shots. Always lock the master reference first.
- **Excessive Movement Speed:** Setting motion strength/speed too high results in melting limbs and broken anatomy. Keep motion intensity moderate (3–5 on a 1–10 scale).

---

## Verification Checklist

Before publishing or rendering final video clips, ensure:
- [ ] Storyboard shot list has defined focal lengths and durations.
- [ ] Master character reference is locked and used as visual anchor.
- [ ] Scene start frames pass mobile safe-zone checks (no edge cropping).
- [ ] Motion prompts contain zero redundant clothing or color descriptions.
- [ ] Motion clips rendered at consistent 24fps before audio muxing.
