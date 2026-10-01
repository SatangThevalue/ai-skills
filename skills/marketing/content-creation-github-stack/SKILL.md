---
name: content-creation-github-stack
description: "Curated open-source stack for multi-channel content creation."
version: 0.1.0
metadata:
  hermes:
    tags:
      - ContentCreation
      - GitHub
      - AI
      - Automation
      - Design
---

# Content Creation GitHub Stack

A production-grade collection of 40 open-source tools and repositories from GitHub, categorized into four core operational domains: AI copywriting, Python programmatic media generation, generative video/image APIs, and graphic design/typography auditing. This skill serves as an engineering manual and reference index for constructing scalable content engines; it does not host model weights locally. Implementation relies on standard Python packages, headless CLI tools, and REST API endpoints.

## When to Use

- "หาสกิลหรือเครื่องมือสร้างคอนเทนต์บน GitHub" (Find content creation tools or skills on GitHub)
- "วิเคราะห์องค์ประกอบภาพ สี ฟอนต์ และการจัดวางด้วยโค้ด" (Audit visual composition, color contrast, and font metrics via code)
- "เชื่อมต่อ API Text-to-Video หรือ Text-to-Image" (Integrate Text-to-Video or Text-to-Image generation APIs)
- "สร้างกราฟิกและวิดีโออัตโนมัติด้วย Python" (Generate automated graphics and videos with Python)

## Prerequisites

- Python 3.10+ with `matplotlib`, `fonttools`, `Pillow`, `requests`, and `moviepy` installed.
- Access to generative API keys when running remote endpoints (Fal.ai, OpenAI, ComfyUI).
- Linux environment with Google Fonts (e.g. Prompt, Kanit, Sarabun) installed.

## How to Run

1. Browse and select appropriate tools across the 4 curated categories below.
2. Execute design audits (WCAG contrast, font bounding boxes) using `terminal` invoking `scripts/design_audit_toolkit.py`.
3. Chain tools together via Prefect flows or standalone Python pipeline scripts.

## Quick Reference

| Category | Primary Library | Canonical GitHub Repo |
| :--- | :--- | :--- |
| 1. AI Agents & Copy | `crewai`, `dspy`, `langgraph` | `crewAIInc/crewAI`, `stanfordnlp/dspy` |
| 2. Python Code-to-Media | `Pillow`, `manim`, `moviepy` | `python-pillow/Pillow`, `3b1b/manim` |
| 3. Generative Image/Video | `diffusers`, `comfyui`, `fal-client` | `huggingface/diffusers`, `comfyanonymous/ComfyUI` |
| 4. Design & Typography | `fonttools`, `colour`, `wcag` | `fonttools/fonttools`, `colour-science/colour` |

## Procedure

1. **Category 1: AI Writing & Agent Orchestration (10 Repos)**
   - `crewAIInc/crewAI`: Multi-agent role-playing teams (Researcher, Copywriter, Editor).
   - `geekan/MetaGPT`: SOP-driven multi-agent framework for structured content generation.
   - `assafelovic/gpt-researcher`: Autonomous web research agent producing cited data reports.
   - `dair-ai/Prompt-Engineering-Guide`: Comprehensive prompting strategies (Few-shot, CoT).
   - `Significant-Gravitas/AutoGPT`: Autonomous vision and web-browsing agent.
   - `langchain-ai/langgraph`: Cyclical graph state-machine for multi-pass copy review.
   - `stanfordnlp/dspy`: Algorithmic prompt compiler for consistent headlines and hooks.
   - `microsoft/autogen`: Multi-agent conversational brainstorming framework.
   - `brexhq/prompt-engineering`: Production-grade commercial prompt templates.
   - `FlowiseAI/Flowise`: Visual canvas for LLM chains and content routing.

2. **Category 2: Python Code-to-Media Automation (10 Repos)**
   - `python-pillow/Pillow`: 2D image drawing, Thai typography, and card composition.
   - `3b1b/manim`: Mathematical animation engine for explanatory data storytelling.
   - `Zulko/moviepy`: Scripted video cuts, audio dubbing, and text overlays.
   - `matplotlib/matplotlib`: Publication-quality statistical charts and plots.
   - `mwaskom/seaborn`: Statistical data visualization with refined color palettes.
   - `plotly/plotly.py`: Interactive financial charting with headless image export.
   - `kkroening/ffmpeg-python`: FFmpeg filter graph bindings for video assembly.
   - `pyecharts/pyecharts`: Modern interactive charts for infographic data layers.
   - `PrefectHQ/prefect`: Workflow orchestration for batch content schedules.
   - `zulko/gizeh`: Vector graphics drawing library based on Cairo for crisp shapes.

3. **Category 3: Generative AI Media APIs & Models (10 Repos)**
   - `comfyanonymous/ComfyUI`: Node-based modular FLUX and Stable Diffusion engine.
   - `huggingface/diffusers`: Pretrained diffusion models for text-to-image and text-to-video.
   - `THUDM/CogVideo`: CogVideoX state-of-the-art open text-to-video transformer.
   - `Wan-Video/Wan2.1`: Open high-resolution text-to-video foundation model.
   - `black-forest-labs/flux`: FLUX.1 12B parameter text-to-image foundation model.
   - `guoyww/AnimateDiff`: Motion modules for animating personalized diffusion models.
   - `TencentARC/PhotoMaker`: Personalized character consistency across images.
   - `fal-ai/fal-js`: Serverless API client for FLUX, Kling, and Luma endpoints.
   - `openai/openai-python`: DALL-E 3 API client for readable in-image text.
   - `Stability-AI/generative-models`: Stable Video Diffusion (SVD) image animation.

4. **Category 4: Design, Typography, & Color Auditing (10 Repos)**
   - `material-foundation/material-color-utilities`: Dynamic palette extraction and contrast.
   - `fonttools/fonttools`: Font metrics, glyph bounding boxes, and OpenType kerning.
   - `colour-science/colour`: Color science, delta-E difference, and chromaticity.
   - `chenglou/pretext`: High-speed multiline text measurement and layout box calculation.
   - `opencv/opencv-python`: Saliency detection and rule-of-thirds composition analysis.
   - `baoyu-io/baoyu-skills`: 21 layout × 21 style infographic design frameworks.
   - `shadcn-ui/ui`: Dark-mode card hierarchy and typographic tokens.
   - `googlefonts/tools`: Vertical font metrics, vowel clipping, and glyph coverage.
   - `AccessibilityX/wcag-contrast`: Automated WCAG 2.1 AA/AAA contrast verification.
   - `google/design-tokens`: Machine-readable DESIGN.md spatial scale specification.

5. **Execute Design Quality Verification**
   Verify visual compliance using the bundled audit script via `terminal`:
   ```bash
   python3 scripts/design_audit_toolkit.py --bg "#070D1F" --fg "#F5A623" --font "/home/thaieasyvps/.fonts/Prompt/Prompt-Bold.ttf"
   ```

## Pitfalls

- **WCAG Contrast Ratios on Mobile Displays:** Text smaller than 24px requires a minimum contrast ratio of 4.5:1 against the background; large text (>=24px) requires 3:1. Low contrast causes high drop-off rates on mobile feeds.
- **Thai Unicode Font Clipping:** When using PIL, calculating text height with `.getsize()` causes vertical vowel and tone-mark clipping. Always use `.getbbox()` or `fonttools` to retrieve the true optical bounding box.
- **Local GPU Memory for Diffusion Models:** Running CogVideoX or FLUX locally requires 24GB+ VRAM. Use serverless API endpoints (Fal.ai or HuggingFace Inference Endpoints) for constrained environments.

## Verification

Run the design audit verification check:
```bash
python3 /home/thaieasyvps/.hermes/profiles/nong-makham/skills/marketing/content-creation-github-stack/scripts/design_audit_toolkit.py --check | grep -q "DESIGN_AUDIT_OK" && echo "SKILL_VERIFIED"
```
The check outputs `SKILL_VERIFIED` when the design audit toolkit successfully evaluates contrast and font metrics.