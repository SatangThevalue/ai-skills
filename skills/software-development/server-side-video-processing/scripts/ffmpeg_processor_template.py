import os
import subprocess
import argparse
import json
from typing import Optional

def process_video(
    input_video: str,
    output_video: str,
    mute_original_audio: bool = False,
    bgm_file: Optional[str] = None,
    bgm_volume: float = 0.3,
    crop_916: bool = False,
    drawtext_text: Optional[str] = None,
    font_file: Optional[str] = None,
    font_size: int = 48,
    font_color: str = "white"
):
    """
    Dynamically constructs and executes an FFmpeg command using complex filters.
    Highly optimized for single-pass processing without MoviePy.
    """
    if not os.path.exists(input_video):
        raise FileNotFoundError(f"Input video not found: {input_video}")

    cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "info"]
    cmd.extend(["-i", input_video])
    input_count = 1
    
    if bgm_file and os.path.exists(bgm_file):
        cmd.extend(["-i", bgm_file])
        bgm_input_index = input_count
        input_count += 1
    else:
        bgm_input_index = -1

    filter_complex = []
    
    # --- Video Filters ---
    video_filters = []
    last_v_pad = "[0:v]"
    
    if crop_916:
        video_filters.append(f"{last_v_pad}crop='ih*9/16':'ih'[vcrop]")
        last_v_pad = "[vcrop]"
        
    if drawtext_text:
        font_opt = f":fontfile={font_file}" if font_file and os.path.exists(font_file) else ""
        text_safe = drawtext_text.replace("'", r"\'").replace(":", r"\:")
        video_filters.append(
            f"{last_v_pad}drawtext=text='{text_safe}':fontcolor={font_color}:fontsize={font_size}{font_opt}:x=(w-text_w)/2:y=(h-text_h)/2[vtext]"
        )
        last_v_pad = "[vtext]"
        
    if video_filters:
        filter_complex.append(";".join(video_filters))
        final_v_pad = last_v_pad
    else:
        final_v_pad = "0:v"

    # --- Audio Filters ---
    audio_filters = []
    last_a_pad = "[0:a]"
    final_a_pad = None
    
    if mute_original_audio and bgm_input_index == -1:
        pass # Will map video only
    elif mute_original_audio and bgm_input_index != -1:
        audio_filters.append(f"[{bgm_input_index}:a]volume={bgm_volume}[a_bgm]")
        final_a_pad = "[a_bgm]"
    elif not mute_original_audio and bgm_input_index != -1:
        audio_filters.append(f"[{bgm_input_index}:a]volume={bgm_volume}[a_bgm]")
        audio_filters.append(f"[0:a][a_bgm]amix=inputs=2:duration=first:dropout_transition=2[a_mix]")
        final_a_pad = "[a_mix]"
    else:
        final_a_pad = "0:a"
        
    if audio_filters:
        filter_complex.append(";".join(audio_filters))

    # --- Command Assembly ---
    if filter_complex:
        cmd.extend(["-filter_complex", ";".join(filter_complex)])
        
    if final_v_pad != "0:v":
        cmd.extend(["-map", final_v_pad])
    else:
        cmd.extend(["-map", "0:v"])
        
    if mute_original_audio and bgm_input_index == -1:
        pass 
    else:
        if final_a_pad and final_a_pad != "0:a":
            cmd.extend(["-map", final_a_pad])
        else:
            cmd.extend(["-map", "0:a?"])

    cmd.extend([
        "-c:v", "libx264", 
        "-preset", "fast", 
        "-crf", "23",
        "-c:a", "aac",
        "-b:a", "128k"
    ])
    
    cmd.append(output_video)
    
    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        return {"status": "success", "output": output_video, "cmd": " ".join(cmd)}
    except subprocess.CalledProcessError as e:
        return {"status": "error", "error": e.stderr, "cmd": " ".join(cmd)}
