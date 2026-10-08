#!/usr/bin/env python3
"""
Prefect Workflow: AI Animation Production Pipeline
Orchestrates the 4-stage production pipeline via 9Router API:
Stage 1: Storyboard & Shot List (The Blueprint)
Stage 2: Master Asset Lock (Visual DNA)
Stage 3: Scene Keyframe Generation (Start Frames)
Stage 4: Image-to-Video Motion Prompts (Physics & Verbs Only)
"""

import os
import sys
import re
import json
import time
import yaml
import argparse
import urllib.request
from pathlib import Path
from prefect import task, flow, get_run_logger

def get_9router_credentials():
    api_key = os.getenv("ROUTER9_API_KEY")
    if api_key and (api_key == "***" or not api_key.strip() or len(api_key) < 10):
        api_key = None
        
    base_url = os.getenv("ROUTER9_BASE_URL", "http://0.0.0.0:20128/v1")
    
    if not api_key:
        paths = [
            Path("/home/thaieasyvps/.hermes/profiles/nong-makham/config.yaml"),
            Path(os.path.expanduser("~/.hermes/profiles/nong-makham/config.yaml")),
            Path(os.path.expanduser("~/.hermes/config.yaml"))
        ]
        for cfg_path in paths:
            if cfg_path.exists():
                with open(cfg_path, "r", encoding="utf-8") as f:
                    cfg = yaml.safe_load(f)
                for cp in cfg.get("custom_providers", []):
                    if cp.get("name") == "9router-docker":
                        candidate = cp.get("api_key")
                        if candidate and candidate != "***" and len(candidate) > 10:
                            api_key = candidate
                            base_url = cp.get("base_url", base_url)
                            break
                if not api_key:
                    candidate = cfg.get("providers", {}).get("9router", {}).get("api_key")
                    if candidate and candidate != "***" and len(candidate) > 10:
                        api_key = candidate
                        base_url = cfg.get("providers", {}).get("9router", {}).get("url", base_url)
                if api_key:
                    break
                
    if not api_key:
        raise ValueError("9Router API key not found in environment or config.yaml")
        
    return base_url, api_key

def query_9router(prompt: str, system_prompt: str = "", model: str = "ag/gemini-3.8-flash-high") -> str:
    base_url, api_key = get_9router_credentials()
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    payload = {
        "model": model,
        "messages": messages,
        "stream": False,
        "temperature": 0.3,
        "max_tokens": 1800
    }
    
    req = urllib.request.Request(
        f"{base_url}/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        data=json.dumps(payload).encode("utf-8")
    )
    
    with urllib.request.urlopen(req, timeout=90) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        if "choices" in data and len(data["choices"]) > 0:
            return data["choices"][0]["message"]["content"]
        if "error" in data:
            raise RuntimeError(f"9Router error: {data['error']}")
        raise KeyError(f"Unexpected 9Router response: {data}")

def parse_json_from_text(text: str, is_array: bool = False):
    s = text.strip()
    if is_array:
        start = s.find("[")
        end = s.rfind("]")
        if start != -1 and end != -1:
            return json.loads(s[start:end+1])
    else:
        start = s.find("{")
        end = s.rfind("}")
        if start != -1 and end != -1:
            return json.loads(s[start:end+1])
            
    # Fallback to general markdown removal
    clean = re.sub(r"^```(?:json)?", "", s, flags=re.MULTILINE)
    clean = re.sub(r"```$", "", clean, flags=re.MULTILINE).strip()
    return json.loads(clean)

@task(name="Stage 1: Generate Storyboard & Shot List", retries=2, retry_delay_seconds=3)
def generate_storyboard(concept: str) -> dict:
    logger = get_run_logger()
    logger.info("Executing Stage 1: Storyboard & Shot List...")
    
    system_prompt = (
        "You are an expert AI Animation Director specializing in Studio Ghibli aesthetics "
        "and authentic Southeast Asian/Thai cultural storytelling. "
        "Return ONLY a valid JSON object with keys: title, target_duration, "
        "beats (list of 4 objects: beat_number, time_range, shot_type, camera_lens, "
        "action_description, thai_cultural_anchors)."
    )
    user_prompt = f"Deconstruct this animation concept into a 4-beat storyboard:\n{concept}"
    
    raw = query_9router(user_prompt, system_prompt)
    storyboard = parse_json_from_text(raw, is_array=False)
    logger.info(f"Storyboard compiled with {len(storyboard.get('beats', []))} narrative beats.")
    time.sleep(1)
    return storyboard

@task(name="Stage 2: Lock Master Assets (Visual DNA)", retries=2, retry_delay_seconds=3)
def lock_master_assets(storyboard: dict) -> dict:
    logger = get_run_logger()
    logger.info("Executing Stage 2: Master Asset Lock...")
    
    system_prompt = (
        "You are a character designer for Ghibli-style animation. "
        "Generate detailed text-to-image prompts for master asset reference sheets. "
        "Return ONLY a valid JSON object with keys: "
        "master_character_prompt, master_prop_prompt, consistency_anchors (list of strings)."
    )
    user_prompt = f"Create master asset reference prompts for this storyboard:\n{json.dumps(storyboard, ensure_ascii=False)}"
    
    raw = query_9router(user_prompt, system_prompt)
    assets = parse_json_from_text(raw, is_array=False)
    logger.info("Master assets locked with cultural anchors.")
    time.sleep(1)
    return assets

@task(name="Stage 3: Compile Scene Keyframe Prompts", retries=2, retry_delay_seconds=3)
def compile_scene_keyframes(storyboard: dict, master_assets: dict) -> list:
    logger = get_run_logger()
    logger.info("Executing Stage 3: Scene Keyframe Assembly...")
    
    system_prompt = (
        "You are a production prompt engineer for FLUX.1 and Midjourney v6. "
        "Combine the master character visual DNA with each storyboard beat into ready-to-run "
        "Image-to-Image / Start Frame prompts. Enforce 9:16 safe zone and lighting details. "
        "Return ONLY a valid JSON array of objects: (beat_number, keyframe_prompt, safe_zone_notes)."
    )
    user_prompt = f"Storyboard: {json.dumps(storyboard, ensure_ascii=False)}\nMaster Assets: {json.dumps(master_assets, ensure_ascii=False)}"
    
    raw = query_9router(user_prompt, system_prompt)
    keyframes = parse_json_from_text(raw, is_array=True)
    logger.info(f"Compiled {len(keyframes)} scene start-frame prompts.")
    time.sleep(1)
    return keyframes

@task(name="Stage 4: Generate Motion Prompts (Verbs & Physics Only)", retries=2, retry_delay_seconds=3)
def generate_motion_prompts(storyboard: dict, keyframes: list) -> list:
    logger = get_run_logger()
    logger.info("Executing Stage 4: Motion Prompting (I2V Verbs Only)...")
    
    system_prompt = (
        "You are an AI Video Director for Google Veo, Kling, and Runway Gen-3. "
        "Enforce THE GOLDEN RULE: Motion prompts MUST contain ONLY directional verbs, "
        "camera motions, and fluid/cloth physics. NEVER re-describe clothing, face, or colors. "
        "Return ONLY a valid JSON array of objects: (beat_number, motion_prompt, duration_seconds)."
    )
    user_prompt = f"Storyboard beats: {json.dumps(storyboard, ensure_ascii=False)}\nKeyframes: {json.dumps(keyframes, ensure_ascii=False)}"
    
    raw = query_9router(user_prompt, system_prompt)
    motion_prompts = parse_json_from_text(raw, is_array=True)
    logger.info(f"Generated {len(motion_prompts)} motion prompts.")
    return motion_prompts

@task(name="Export Production Package")
def export_package(output_dir: str, storyboard: dict, master_assets: dict, keyframes: list, motion_prompts: list) -> str:
    logger = get_run_logger()
    out_path = Path(output_dir)
    out_path.mkdir(parents=True, exist_ok=True)
    
    package = {
        "storyboard": storyboard,
        "master_assets": master_assets,
        "keyframes": keyframes,
        "motion_prompts": motion_prompts
    }
    
    json_file = out_path / "production_package.json"
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(package, f, ensure_ascii=False, indent=2)
        
    md_file = out_path / "PRODUCTION_SHEET.md"
    lines = [
        f"# Production Sheet: {storyboard.get('title', 'AI Animation')}",
        f"**Target Duration:** {storyboard.get('target_duration', '15-20s')}\n",
        "## Master Asset Locks",
        f"- **Character Prompt:** `{master_assets.get('master_character_prompt')}`",
        f"- **Prop Prompt:** `{master_assets.get('master_prop_prompt')}`\n",
        "## Storyboard & Motion Prompts\n"
    ]
    
    for beat in storyboard.get("beats", []):
        b_num = beat.get("beat_number")
        kf = next((k for k in keyframes if k.get("beat_number") == b_num), {})
        mp = next((m for m in motion_prompts if m.get("beat_number") == b_num), {})
        
        lines.append(f"### Beat {b_num}: {beat.get('time_range')} ({beat.get('shot_type')})")
        lines.append(f"**Action:** {beat.get('action_description')}")
        lines.append(f"**Cultural Anchors:** {beat.get('thai_cultural_anchors')}")
        lines.append(f"**Keyframe Prompt (Start Frame):**\n```text\n{kf.get('keyframe_prompt', '')}\n```")
        lines.append(f"**Motion Prompt (Veo/Kling):**\n```text\n{mp.get('motion_prompt', '')}\n```\n")
        
    with open(md_file, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
        
    logger.info(f"Production package exported to {out_path.resolve()}")
    return str(json_file)

@flow(name="ai-animation-production-flow")
def ai_animation_pipeline_flow(concept: str, output_dir: str = "./production_output"):
    logger = get_run_logger()
    logger.info("Starting AI Animation Production Pipeline Flow...")
    
    sb = generate_storyboard(concept)
    ma = lock_master_assets(sb)
    kf = compile_scene_keyframes(sb, ma)
    mp = generate_motion_prompts(sb, kf)
    result = export_package(output_dir, sb, ma, kf, mp)
    
    logger.info(f"Flow completed successfully! Artifacts at: {result}")
    return result

def main():
    parser = argparse.ArgumentParser(description="Prefect AI Animation Pipeline via 9Router")
    parser.add_argument("--concept", default=(
        "เด็กชายชาวเลไทยจับปูดำยักษ์ในป่าชายเลนอ่าวไทย สไตล์อนิเมะ Ghibli "
        "มีสายสิญจน์ผูกข้อมือ ผ้าขาวม้า ล่องเรือหางยาวผูกผ้าสามสี"
    ), help="Animation concept prompt")
    parser.add_argument("--out", default="./production_output", help="Output directory")
    args = parser.parse_args()

    ai_animation_pipeline_flow(concept=args.concept, output_dir=args.out)

if __name__ == "__main__":
    main()
