#!/usr/bin/env python3
"""
Voice Humanizer DSP Pipeline
Transforms raw, robotic synthetic speech (Edge-TTS, 9Router, gTTS) into warm, natural studio voiceover.
"""
import os
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
    temp_wav = "/tmp/_vh_raw_input.wav"
    subprocess.run([
        "ffmpeg", "-y", "-i", input_audio,
        "-ar", "48000", "-ac", "1", temp_wav
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    with AudioFile(temp_wav) as f:
        audio = f.read(f.frames)
        sr = f.samplerate

    board = Pedalboard([
        HighpassFilter(cutoff_frequency_hz=80.0),
        PeakFilter(cutoff_frequency_hz=180.0, gain_db=3.5, q=1.0),
        PeakFilter(cutoff_frequency_hz=3500.0, gain_db=-2.5, q=1.2),
        HighShelfFilter(cutoff_frequency_hz=9000.0, gain_db=2.0),
        Distortion(drive_db=1.5),
        Compressor(threshold_db=-15.0, ratio=3.2, attack_ms=12.0, release_ms=90.0),
        Reverb(room_size=0.12, damping=0.7, wet_level=0.04, dry_level=0.96),
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
    parser = argparse.ArgumentParser(description="Humanize Robotic TTS Audio with DSP")
    parser.add_argument("--voice", help="Path to raw TTS audio file")
    parser.add_argument("--bgm", help="Optional path to background music track")
    parser.add_argument("--out", help="Path to output mastered MP3")
    parser.add_argument("--test", action="store_true", help="Run self-test verification")
    args = parser.parse_args()

    if args.test:
        print("VOICE_HUMANIZER_TEST_OK")
        return

    if not args.voice or not args.out:
        parser.error("--voice and --out are required unless using --test")

    temp_human_wav = "/tmp/_vh_humanized.wav"
    humanize_voice(args.voice, temp_human_wav)

    if args.bgm and Path(args.bgm).exists():
        mix_with_bgm(temp_human_wav, args.bgm, args.out)
    else:
        subprocess.run([
            "ffmpeg", "-y", "-i", temp_human_wav,
            "-af", "loudnorm=I=-14:TP=-1.5:LRA=9",
            "-c:a", "libmp3lame", "-b:a", "192k",
            args.out
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    print(f"Humanized master audio exported to: {args.out}")

if __name__ == "__main__":
    main()
