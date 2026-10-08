# Emotional & Life Quote Reel Playbook (The Read-Loop Formula)

Extracted from high-engagement Thai Facebook Pages (e.g. "การเดินทาง" @Ilovetraver, 2.4M followers). This archetype relies on emotional resonance, atmospheric B-roll, and looping readability to achieve viral reach and high completion rates without voice narration.

---

## 1. Core Psychological Triggers

1. **Subtle Venting (การระบายอารมณ์ทางอ้อม):**
   - Viewers use the video to express feelings they cannot speak directly to bosses, toxic coworkers, or partners.
   - Sharing on Facebook Feeds or Stories acts as an indirect signal ("รีบพัฒนาชีวิต จะได้รีบออกไปจากตรงนี้").
2. **The Read-Loop Watch Time Multiplier:**
   - Text is formatted across 3 tiers (Hook, Body, Action).
   - Reading takes 6–8 seconds. In a 7–11s video, viewers naturally loop 1.5–2 times, driving **Average Watch Time > 120-180%**, triggering aggressive algorithm distribution.
3. **Low Cognitive Load:**
   - Static high-contrast text overlay over slow, rhythmic motion (POV driving at twilight, train window, rain, city lights).
   - No complex transitions or frantic edits that distract from the emotional copy.

---

## 2. Visual Hierarchy & Safe Zones (9:16)

- **Canvas Size:** 1080 × 1920 px.
- **Top Safe Zone (0–350px):** Keep clear of brand text to avoid platform status bars.
- **Text Placement (Y: 450–900px):** Positioned in the upper-middle third against dark atmospheric sky or low-contrast background.
  - **Tier 1: Hook (Gold `#F5A623` or `#FFE082`):** 48–56px Bold. Key punchline in quotes.
  - **Tier 2: Body Context (White `#FFFFFF`):** 36–42px Regular/Medium. The relatable pain point.
  - **Tier 3: Action / Affirmation (White `#ECEFF1`):** 36–42px Regular/Medium. Encouragement or exit plan.
- **Bottom Vignette (Y: 1400–1920px):** Dark gradient overlay (`rgba(0,0,0,0.6)` to `transparent`) to protect readability from Facebook UI buttons (Like, Share, Comment, Audio tag).
- **Watermark (Y: 1350px):** Subtle, low-opacity (40%) page handle centered below text.

---

## 3. Four Content Pillars for Faceless Quote Pages

1. **Workplace & Toxic Escape:**
   - *Theme:* Career burnout, low pay, toxic environments, self-worth.
   - *Example:* "รีบพัฒนาชีวิต จะได้รีบออกไปจากตรงนี้ ที่ที่ทำให้คุณสุขภาพจิตแย่..."
2. **Quiet Self-Improvement & Discipline:**
   - *Theme:* Working in silence, financial independence, skill acquisition.
   - *Example:* "ไม่ต้องบอกใครว่าเรากำลังพยายามอะไร ให้ผลลัพธ์มันพูดเอง..."
3. **Boundaries & Letting Go:**
   - *Theme:* Cutting off one-sided relationships, social peace, adult solitude.
   - *Example:* "โตขึ้นจะเข้าใจว่า การไม่มีใครเลย ยังดีกว่ามีคนที่ทำให้รู้สึกโดดเดี่ยว..."
4. **Mindfulness & Slow Healing:**
   - *Theme:* Self-forgiveness, resting after long battles, enjoying ordinary days.
   - *Example:* "วันนี้เหนื่อยมามากพอแล้ว พักผ่อนเถอะ พรุ่งนี้ค่อยเริ่มใหม่..."

---

## 4. Production Recipe (FFmpeg / HyperFrames)

### Method A: Pure FFmpeg One-Liner (Over Looping Video Asset)
```bash
ffmpeg -y -i broll_twilight.mp4 -i audio_lofi.mp3 \
  -vf "drawtext=fontfile='/home/thaieasyvps/.fonts/Prompt/Prompt-Bold.ttf':text='“รีบพัฒนาชีวิต”':fontcolor=#F5A623:fontsize=54:x=(w-text_w)/2:y=500,\
       drawtext=fontfile='/home/thaieasyvps/.fonts/Prompt/Prompt-Bold.ttf':text='จะได้รีบออกไปจากตรงนี้':fontcolor=#F5A623:fontsize=50:x=(w-text_w)/2:y=570,\
       drawtext=fontfile='/home/thaieasyvps/.fonts/Prompt/Prompt-Regular.ttf':text='ที่ที่ทำให้คุณสุขภาพจิตแย่':fontcolor=#FFFFFF:fontsize=38:x=(w-text_w)/2:y=680,\
       drawtext=fontfile='/home/thaieasyvps/.fonts/Prompt/Prompt-Regular.ttf':text='ที่ที่คุณไม่คิดจะอยู่ไปตลอด':fontcolor=#FFFFFF:fontsize=38:x=(w-text_w)/2:y=740,\
       drawtext=fontfile='/home/thaieasyvps/.fonts/Prompt/Prompt-Regular.ttf':text='มีแค่คุณที่จะพาตัวเอง ออกไปได้นะ':fontcolor=#FFFFFF:fontsize=38:x=(w-text_w)/2:y=850" \
  -c:v libx264 -preset fast -crf 22 -c:a aac -b:a 192k -t 11 quote_reel_final.mp4
```

### Method B: HyperFrames Vector/HTML Composition
Create `index.html` with `<video autoplay loop muted>` behind an SVG or flex container holding structured typography. Set static duration to 8–10 seconds for optimal completion loops.
