# Pedalboard Audio FX Patterns

Useful chains for processing audio with `pedalboard`, often used in post-processing TTS outputs.

## Requirements
```bash
pip install pedalboard soundfile
```

## Setup & Normalization
Usually done reading from `soundfile`:
```python
import soundfile as sf
from pedalboard import Pedalboard, Compressor, HighpassFilter, LowShelfFilter, HighShelfFilter, NoiseGate, Limiter, Reverb, Chorus, Distortion, PitchShift, Delay

audio_data, sample_rate = sf.read(input_path)
if len(audio_data.shape) > 1:
    audio_data = audio_data.T  # (channels, samples) for Pedalboard
```

## Podcast / Studio Mastering
- **HighpassFilter (80Hz):** Cut rumble/mic bumps.
- **LowShelfFilter (120Hz):** Proximity effect (adds bass/weight).
- **HighShelfFilter (6000Hz):** Clarity/Air (crispness).
- **Compressor:** Level out volume spikes.
- **NoiseGate:** Cut silence/breath noise.
- **Limiter:** Prevent clipping.

```python
board = Pedalboard([
    NoiseGate(threshold_db=-40.0, ratio=1.5, release_ms=250),
    HighpassFilter(cutoff_frequency_hz=80),
    LowShelfFilter(cutoff_frequency_hz=120, gain_db=5.0),
    HighShelfFilter(cutoff_frequency_hz=6000, gain_db=3.5),
    Compressor(threshold_db=-15, ratio=3.5, attack_ms=2.0, release_ms=100),
    Limiter(threshold_db=-1.0)
])
```

## Humanizer
Use a very subtle Chorus to add micro-modulation. This helps break up the "robotic perfection" of AI generated voices by creating tiny, imperceptible pitch variances simulating human vocal cord variations.
```python
Chorus(rate_hz=0.5, depth=0.05, mix=0.1)
```

## Telephone / Vintage Radio
Use `Highpass` at high frequencies and `LowShelf` cutting heavily to create a "bandpass" effect. Add `Distortion` for crackle/saturation.
```python
HighpassFilter(cutoff_frequency_hz=300),
LowShelfFilter(cutoff_frequency_hz=120, gain_db=-15.0), # Extreme cut
Distortion(drive_db=15.0)
```