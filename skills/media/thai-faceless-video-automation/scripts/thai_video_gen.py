import os
import subprocess
from PIL import Image, ImageDraw, ImageFont
import textwrap

def create_text_overlay(output_path, text_data, font_path_bold, font_path_regular, width=720, height=1280):
    """
    Creates a transparent PNG with high-quality Thai text rendering.
    Bypasses FFmpeg's drawtext Thai tone mark overlapping issues.
    """
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    try:
        font_headline = ImageFont.truetype(font_path_bold, 55)
        font_subhead = ImageFont.truetype(font_path_bold, 75)
        font_body = ImageFont.truetype(font_path_regular, 40)
    except IOError:
        print("❌ Error loading font. Fallback to default.")
        font_headline = font_subhead = font_body = ImageFont.load_default()

    def draw_text_centered_with_shadow(text, font, y_pos, text_color, shadow_color="black"):
        lines = textwrap.wrap(text, width=32) # Wrap at ~32 chars for 720p width
        current_y = y_pos
        for line in lines:
            bbox = draw.textbbox((0, 0), line, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            x_pos = (width - text_width) / 2
            
            # Shadow
            draw.text((x_pos + 3, current_y + 3), line, font=font, fill=shadow_color)
            # Main Text
            draw.text((x_pos, current_y), line, font=font, fill=text_color)
            
            current_y += text_height + 20 # Line spacing
        return current_y

    y_offset = (height / 2) - 350
    if "headline" in text_data:
        y_offset = draw_text_centered_with_shadow(text_data["headline"], font_headline, y_offset, "#FFD700")
        y_offset += 10
    if "subhead" in text_data:
        y_offset = draw_text_centered_with_shadow(text_data["subhead"], font_subhead, y_offset, "#FFD700")
        y_offset += 60

    for item in text_data.get("items", []):
        y_offset = draw_text_centered_with_shadow(item, font_body, y_offset, "white")
        y_offset += 30

    img.save(output_path)
    print(f"✅ Text overlay saved: {output_path}")
    return output_path

def assemble_video(input_bg, overlay_img, bgm_audio, output_video, duration=10):
    filter_complex = (
        "[0:v]format=yuv420p,scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280,"
        "colorchannelmixer=rr=0.5:gg=0.5:bb=0.5," # Dim background by 50%
        "vignette=PI/4[bg_dimmed];"               # Add vignette
        "[bg_dimmed][1:v]overlay=0:0[outv];"      # Overlay the PIL text image
        "[2:a]volume=0.3[outa]"                   # Drop BGM volume
    )

    cmd = [
        "ffmpeg", "-y",
        "-i", input_bg,      # 0: video
        "-i", overlay_img,   # 1: text overlay image
        "-i", bgm_audio,     # 2: bgm
        "-filter_complex", filter_complex,
        "-map", "[outv]",       
        "-map", "[outa]",       
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "23",
        "-c:a", "aac",
        "-b:a", "192k",
        "-t", str(duration),             
        output_video
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"FFmpeg Error: {result.stderr}")
    print(f"✅ Video generated: {output_video}")

if __name__ == "__main__":
    # Example usage
    sample_text = {
        "headline": "3 กฎเหล็กของ",
        "subhead": "ความสำเร็จ",
        "items": [
            "1. ยิ่งยาก : ยิ่งมีเสน่ห์ ลองทำในสิ่งที่คนอื่นไม่กล้าทำ",
            "2. ยิ่งผิดพลาด : ยิ่งเก่งขึ้น ประสบการณ์คือครูที่ดีที่สุด",
            "3. ยิ่งล้มเหลว : ยิ่งใกล้สำเร็จ อย่ายอมแพ้ต่ออุปสรรค"
        ]
    }
    
    input_video = "/home/thaieasyvps/.hermes/cache/videos/video_c0648df9cdfd.mp4"
    bgm_audio = "/home/thaieasyvps/zero-touch-infrastructure/workspace/assets/bgm/lofi_test.mp3"
    overlay_path = "/tmp/overlay_final_test.png"
    output_video = "/home/thaieasyvps/zero-touch-infrastructure/workspace/final_showcase_video.mp4"

    create_text_overlay(
        output_path=overlay_path,
        text_data=sample_text,
        font_path_bold="/home/thaieasyvps/.fonts/Sarabun/Sarabun-Bold.ttf",
        font_path_regular="/home/thaieasyvps/.fonts/Sarabun/Sarabun-Regular.ttf"
    )

    assemble_video(
        input_bg=input_video,
        overlay_img=overlay_path,
        bgm_audio=bgm_audio,
        output_video=output_video,
        duration=10
    )