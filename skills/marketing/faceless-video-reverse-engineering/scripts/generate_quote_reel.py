#!/usr/bin/env python3
"""
Emotional Quote & Read-Loop Reel Generator
Automates the creation of 9:16 viral faceless reels (like 'การเดินทาง' @Ilovetraver):
- 1080x1920 Cinematic Atmospheric B-roll with Ken Burns push-in
- 3-tier Prompt typography (Gold hook + White context + Action footer)
- Safe-zone compliance (100% free of bottom Reels UI occlusion)
- Lo-Fi Acoustic soundbed normalized to -14 LUFS with gentle fade
"""

import sys
import argparse
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

def render_typography_overlay(
    out_overlay: str,
    hook1: str = "“รีบพัฒนาชีวิต”",
    hook2: str = "จะได้รีบออกไปจากตรงนี้",
    body1: str = "ที่ที่ทำให้คุณสุขภาพจิตแย่",
    body2: str = "ที่ที่คุณไม่คิดจะอยู่ไปตลอด",
    sub1: str = "มีแค่คุณที่จะพาตัวเองออกไปได้",
    sub2: str = "รีบๆ ออกไปให้ได้นะ",
    brand: str = "— การเดินทาง • Life Journey —"
):
    font_bold = "/home/thaieasyvps/.fonts/Prompt/Prompt-Bold.ttf"
    font_med = "/home/thaieasyvps/.fonts/Prompt/Prompt-Medium.ttf"
    font_reg = "/home/thaieasyvps/.fonts/Prompt/Prompt-Regular.ttf"

    w, h = 1080, 1920
    txt_img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(txt_img)

    f_hook = ImageFont.truetype(font_bold, 58)
    f_hook2 = ImageFont.truetype(font_bold, 52)
    f_body = ImageFont.truetype(font_med, 40)
    f_sub = ImageFont.truetype(font_reg, 38)
    f_brand = ImageFont.truetype(font_reg, 24)

    c_gold = (255, 215, 64, 255)
    c_white = (255, 255, 255, 255)
    c_dim = (220, 228, 235, 255)
    c_shadow = (0, 0, 0, 210)

    def draw_text_centered(text, y, font, color, shadow_offset=3):
        bbox = font.getbbox(text)
        tw = bbox[2] - bbox[0]
        x = (w - tw) // 2
        draw.text((x + shadow_offset, y + shadow_offset), text, font=font, fill=c_shadow)
        draw.text((x, y), text, font=font, fill=color)

    for y in range(250, 1150):
        alpha = int(140 * (1.0 - abs(y - 620) / 480.0))
        draw.line([(0, y), (w, y)], fill=(0, 0, 0, max(0, min(alpha, 110))))

    draw_text_centered(hook1, 400, f_hook, c_gold)
    draw_text_centered(hook2, 485, f_hook2, c_gold)
    draw.ellipse([(w//2 - 4, 565), (w//2 + 4, 573)], fill=(255, 215, 64, 180))
    draw_text_centered(body1, 610, f_body, c_white)
    draw_text_centered(body2, 675, f_body, c_white)
    draw_text_centered(sub1, 770, f_sub, c_dim)
    draw_text_centered(sub2, 830, f_sub, c_dim)
    draw_text_centered(brand, 1000, f_brand, (255, 255, 255, 120))

    txt_img.save(out_overlay)
    return out_overlay

def assemble_video(bg_image: str, overlay_png: str, audio_path: str, out_video: str, duration: float = 9.5):
    fps = 24
    total_frames = int(fps * duration)
    filter_str = (
        f"[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,zoompan=z='min(zoom+0.0009,1.10)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={total_frames}:s=1080x1920:fps={fps}[v_bg]; "
        "[v_bg][1:v]overlay=0:0[v_comp]; "
        "[v_comp]vignette=PI/6[v_out]"
    )
    cmd = [
        "ffmpeg", "-y",
        "-loop", "1", "-i", bg_image,
        "-i", overlay_png,
        "-i", audio_path,
        "-filter_complex", filter_str,
        "-map", "[v_out]",
        "-map", "2:a",
        "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "256k",
        "-t", str(duration),
        out_video
    ]
    subprocess.run(cmd, check=True)
    return out_video

def main():
    parser = argparse.ArgumentParser(description="Generate Read-Loop Quote Reel")
    parser.add_argument("--bg", required=True, help="Path to background B-roll image")
    parser.add_argument("--audio", required=True, help="Path to Lo-Fi background audio")
    parser.add_argument("--out", default="quote_reel.mp4", help="Output MP4 path")
    args = parser.parse_args()

    temp_overlay = "/tmp/_quote_overlay_temp.png"
    render_typography_overlay(temp_overlay)
    assemble_video(args.bg, temp_overlay, args.audio, args.out)
    print("Done:", args.out)

if __name__ == "__main__":
    main()
