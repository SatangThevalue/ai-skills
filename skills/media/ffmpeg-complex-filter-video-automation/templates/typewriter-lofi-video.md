# Media Studio Template: Typwriter/Lo-Fi Knowledge Video
# Target Audience: Studygram, productivity niches, evening scrolling.
# Vibe: Calm, focused, text-heavy (no TTS), ambient background.

This template outlines the FFmpeg architecture for generating a 9:16 video featuring a dimmed background, typewriter-effect text, and ambient audio (BGM + SFX).

## 1. Background Video Prep
Scale/crop to 9:16 (720x1280 or 1080x1920) and dim to ensure white text pops.

```bash
[0:v]format=yuv420p,colorchannelmixer=rr=0.4:gg=0.4:bb=0.4[dimmed]
```
*(Note: Use `rr, gg, bb` for colorchannelmixer on modern FFmpeg versions if `r, g, b` fail).*

## 2. Text Box Overlay (Optional Glassmorphism effect)
Draw a semi-transparent black box to hold the text.

```bash
[dimmed]drawbox=x=36:y=(h-800)/2:w=648:h=800:color=black@0.5:t=fill[boxed]
```

## 3. The Typography (Header)
Always use absolute paths to the `.ttf` font files.

```bash
[boxed]drawtext=text='Header Line 1':fontfile='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf':fontcolor='#FFD700':fontsize=40:x=(w-text_w)/2:y=(h/2)-300:shadowcolor=black:shadowx=2:shadowy=2[t1];
[t1]drawtext=text='HEADER LINE 2':fontfile='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf':fontcolor='#FFD700':fontsize=55:x=(w-text_w)/2:y=(h/2)-240:shadowcolor=black:shadowx=3:shadowy=3[t2]
```

## 4. The Typewriter Effect (Body List)
Use the `enable` flag to stagger the appearance of list items. Calculate the start time (`t, START, END`) for each bullet point to pace the reading speed.

```bash
[t2]drawtext=text='1. First point appears at 1s':fontcolor='white':fontsize=30:x=60:y=(h/2)-100:shadowcolor=black:shadowx=1:shadowy=1:enable='between(t,1,20)'[t3];
[t3]drawtext=text='2. Second point appears at 3s':fontcolor='white':fontsize=30:x=60:y=(h/2)-40:shadowcolor=black:shadowx=1:shadowy=1:enable='between(t,3,20)'[t4]
# Map [t4] to output
```

## 5. Audio Mixing (BGM + Typing SFX)
*Not shown in basic visual test, but conceptualized:*
Mix Lo-Fi BGM with typing sound effects that align with the `enable` timestamps in step 4. Add a lowpass filter to the BGM to create an immersive, "muffled" room aesthetic.

```bash
# Example audio graph:
[bgm]lowpass=f=400[muffled_bgm];
[muffled_bgm][sfx_typing]amix=inputs=2:duration=first[aout]
```