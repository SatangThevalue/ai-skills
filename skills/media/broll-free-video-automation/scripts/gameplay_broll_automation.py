import os
import subprocess
import random

# --- Configuration & Paths ---
WORKSPACE_DIR = "/home/thaieasyvps/zero-touch-infrastructure/workspace"
ASSETS_DIR = f"{WORKSPACE_DIR}/assets"

def prepare_environment():
    """Ensure required directories and sample assets exist."""
    os.makedirs(f"{ASSETS_DIR}/gameplay", exist_ok=True)
    os.makedirs(f"{ASSETS_DIR}/audio", exist_ok=True)
    
def get_random_gameplay_clip(input_gameplay_path, output_clip_path, duration=60):
    """
    Randomly slice a segment from a long gameplay video to use as a background.
    """
    # Use ffprobe to get total duration
    probe_cmd = [
        "ffprobe", "-v", "error", "-show_entries",
        "format=duration", "-of",
        "default=noprint_wrappers=1:nokey=1", input_gameplay_path
    ]
    try:
        total_duration = float(subprocess.check_output(probe_cmd).strip())
    except Exception as e:
        raise RuntimeError(f"Failed to probe video duration: {e}")

    # Ensure video is long enough
    if total_duration <= duration:
        start_time = 0
    else:
        # Avoid the very end of the video
        max_start = int(total_duration - duration)
        start_time = random.randint(0, max_start)

    print(f"🔪 Slicing gameplay from {start_time}s to {start_time + duration}s...")
    
    cmd = [
        "ffmpeg", "-y",
        "-ss", str(start_time),
        "-i", input_gameplay_path,
        "-t", str(duration),
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "23",
        "-an", # Remove original audio (crucial for satisfying loops)
        output_clip_path
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"FFmpeg slice error: {result.stderr}")
    return output_clip_path

def assemble_gameplay_video(bg_clip_path, tts_audio_path, ass_subtitles_path, output_video):
    """
    Combine the sliced gameplay, TTS audio, and karaoke subtitles.
    """
    print(f"🎬 Assembling final video...")
    
    # Simple assembly: Video + Audio + ASS Subtitles
    cmd = [
        "ffmpeg", "-y",
        "-i", bg_clip_path,
        "-i", tts_audio_path,
        "-vf", f"ass='{ass_subtitles_path}'", # Burn subtitles
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "23",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest", # End when the shortest stream (usually audio) ends
        output_video
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"FFmpeg assembly error: {result.stderr}")
    print(f"✅ Video generated successfully at {output_video}")

if __name__ == "__main__":
    prepare_environment()
    # Mock usage:
    # 1. Provide a 1-hour Minecraft Parkour video
    # 2. Provide TTS audio and generated .ass subtitle file
    # get_random_gameplay_clip("parkour_1hr.mp4", "bg_clip.mp4", duration=30)
    # assemble_gameplay_video("bg_clip.mp4", "story_tts.mp3", "story_subs.ass", "final_short.mp4")
    print("Use this as an imported module: `from gameplay_broll_automation import get_random_gameplay_clip`")