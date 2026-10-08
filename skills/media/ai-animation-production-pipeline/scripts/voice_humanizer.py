#!/usr/bin/env python3
"""
Studio Voice Humanizer Pipeline
Transforms robotic raw TTS into warm, human-like voiceover using Spotify's Pedalboard and FFmpeg:
1. Low-end Chest Warmth (180Hz Peak Filter)
2. Digital De-harshing (3.5kHz notch)
3. Tube Preamp Saturation (Harmonic Drive)
4. Studio Vocal Compression (Leveling)
5. Acoustic Room Presence (Micro-Reverb 4%)
6. Auto Audio-Ducking with Background Music (Sidechain Compress)
7. EBU R128 Loudness Normalization (-14 LUFS)
"""

import sys
import argparse
import subprocess
from pathlib import Path
import soundfile as sf
from pedalboard import (
    Pedalboard, Compressor, HighShelfFilter,
    PeakFilter, HighpassFilter, Gain, Reverb, Distortion
)
from pedalboard.io import AudioFile

def humanize_voice(input_audio: str, output_wav: str) -> str:
    # 1. Convert to temporary WAV
    temp_wav = "/tmp/_raw_voice_input.wav"
    subprocess.run([
        "ffmpeg", "-y", "-i", input_audio,
        "-ar", "48000", "-ac", "1", temp_wav
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    with AudioFile(temp_wav) as f:
        audio = f.read(f.frames)
        sr = f.samplerate

    # 2. Studio Mastering DSP Board
    board = Pedalboard([
        HighpassFilter(cutoff_frequency_hz=80.0),
        PeakFilter(cutoff_frequency_hz=180.0, gain_db=3.5, q=1.0),     # Chest Warmth
        PeakFilter(cutoff_frequency_hz=3500.0, gain_db=-2.5, q=1.2),   # De-harsh Nasal Digital
        HighShelfFilter(cutoff_frequency_hz=9000.0, gain_db=2.0),      # Air & Brilliance
        Distortion(drive_db=1.5),                                      # Tube Saturation
        Compressor(threshold_db=-15.0, ratio=3.2, attack_ms=12.0, release_ms=90.0), # Dynamic Leveler
        Reverb(room_size=0.12, damping=0.7, wet_level=0.04, dry_level=0.96),        # Room Presence
        Gain(gain_db=2.0)
    ])

    effected = board(audio, sr)

    with AudioFile(output_wav, "w", sr, effected.shape[0]) as f:
        f.write(effected)

    return output_wav

def mix_with_bgm(voice_wav: str, bgm_path: str, output_mp3: str, bgm_vol: float = 0.20):
    filter_complex = (
        f"[0:a]volume={bgm_vol}[bgm_base]; "
        "[bgm_base][1:a]sidechaincompress=threshold=0.04:ratio=8:attack=15:release=250[bgm_ducked]; "
        "[bgm_ducked][1:a]amix=inputs=2:duration=first:dropout_transition=2[mixed]; "
        "[mixed]loudnorm=I=-14:TP=-1.5:LRA=9[out]"
    )

    cmd = [
        "ffmpeg", "-y",
        "-i", bgm_path,
        "-i", voice_wav,
        "-filter_complex", filter_complex,
        "-map", "[out]",
        "-c:a", "libmp3lame", "-b:a", "192k",
        output_mp3
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return output_mp3

def main():
    parser = argparse.ArgumentParser(description="Humanize Robotic TTS Audio")
    parser.add_argument("--voice", required=True, help="Path to input TTS audio file")
    parser.add_argument("--bgm", help="Optional path to background music for ducking")
    parser.add_argument("--out", required=True, help="Path to output audio MP3")
    args = parser.parse_args()

    temp_human_wav = "/tmp/_humanized_voice.wav"
    humanize_voice(args.voice, temp_human_wav)

    if args.bgm and Path(args.bgm).exists():
        mix_with_bgm(temp_human_wav, args.bgm, args.out)
    else:
        # Just normalize without BGM
        subprocess.run([
            "ffmpeg", "-y", "-i", temp_human_wav,
            "-af", "loudnorm=I=-14:TP=-1.5:LRA=9",
            "-c:a", "libmp3lame", "-b:a", "192k",
            args.out
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    print(f"Humanized master audio exported to: {args.out}")

if __name__ == "__main__":
    main()
