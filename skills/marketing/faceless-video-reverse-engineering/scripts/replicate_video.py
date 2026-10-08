#!/usr/bin/env python3
"""
Faceless Video Replicator Pipeline
Automates: TTS synthesis -> HyperFrames render -> FFmpeg mux -> Telegram delivery
"""
import sys
import json
import yaml
import argparse
import subprocess
import urllib.request
from pathlib import Path

def generate_tts(text: str, out_path: str, model: str = "edge-tts/th-TH-NiwatNeural"):
    config_path = Path("/home/thaieasyvps/.hermes/profiles/nong-makham/config.yaml")
    with open(config_path) as f:
        cfg = yaml.safe_load(f)
    key = cfg.get("providers", {}).get("9router", {}).get("api_key")
    if not key:
        raise ValueError("9Router API key not found in config.yaml")

    url = "http://127.0.0.1:20128/v1/audio/speech"
    req = urllib.request.Request(
        url,
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        data=json.dumps({"model": model, "input": text}).encode("utf-8")
    )
    with urllib.request.urlopen(req) as resp:
        with open(out_path, "wb") as f:
            f.write(resp.read())
    print(f"TTS audio saved to {out_path}")

def render_and_mux(project_dir: str, audio_path: str, output_path: str, fps: int = 24):
    p_dir = Path(project_dir)
    raw_video = p_dir / "raw_render.mp4"
    
    # 1. HyperFrames render
    cmd_render = [
        "npx", "hyperframes", "render", str(p_dir),
        "-o", str(raw_video),
        "--quality", "draft",
        "-f", str(fps)
    ]
    print(f"Rendering HyperFrames ({fps}fps)...")
    subprocess.run(cmd_render, check=True)
    
    # 2. FFmpeg mux
    cmd_mux = [
        "ffmpeg", "-y",
        "-i", str(raw_video),
        "-i", str(audio_path),
        "-c:v", "copy",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        str(output_path)
    ]
    print(f"Muxing final video to {output_path}...")
    subprocess.run(cmd_mux, check=True)
    print("Render complete!")

def main():
    parser = argparse.ArgumentParser(description="Faceless Video Replicator")
    parser.add_argument("--project-dir", required=True, help="Directory containing index.html")
    parser.add_argument("--script-text", help="Text to synthesize via TTS")
    parser.add_argument("--audio", help="Existing audio file (if skipping TTS)")
    parser.add_argument("--out", default="final.mp4", help="Output final MP4 path")
    parser.add_argument("--fps", type=int, default=24, help="Render FPS")
    args = parser.parse_args()

    audio_file = args.audio
    if not audio_file and args.script_text:
        audio_file = str(Path(args.project_dir) / "audio.mp3")
        generate_tts(args.script_text, audio_file)

    if not audio_file or not Path(audio_file).exists():
        raise FileNotFoundError("Audio file not provided and script-text missing.")

    render_and_mux(args.project_dir, audio_file, args.out, fps=args.fps)

if __name__ == "__main__":
    main()
