---
name: zero-touch-monetization-playbook
description: "คู่มือสถาปัตยกรรมและกระบวนการสร้างเครื่องจักรทำเงินอัตโนมัติ (Zero-Touch Monetization) บนเครื่อง VPS โดยใช้ Prefect, FFmpeg, CLIProxyAPI, และเทคนิค Faceless Video"
version: 1.0.0
author: Tonthong
license: MIT
metadata:
  hermes:
    tags: [monetization, automation, prefect, ffmpeg, tts, side-hustle]
    related_skills: [thailand-monetization-2026, prefect-zero-touch-blueprint, ffmpeg-complex-filter-video-automation, facebook-automation-suite]
---

# Zero-Touch Monetization Playbook

สกิลนี้ทำหน้าที่เป็น **"Master Plan"** และสถาปัตยกรรมอ้างอิงสำหรับการสร้างระบบหาเงินอัตโนมัติ 100% บนเครื่อง VPS โดยเชื่อมโยงเครื่องมือฟรีทั้งหมด (Prefect, Local LLM, FFmpeg, TTS) เข้าด้วยกันเพื่อสร้าง *Faceless Video Automation* และยิงโพสต์ขึ้น Social Media แบบคู่ขนาน

## 1. Core Architecture (สถาปัตยกรรมหลัก)
ระบบถูกออกแบบมาให้อยู่ในโครงสร้าง `~/zero-touch-infrastructure` เพื่อให้ AI (Hermes) และ Prefect สามารถเข้ามาทำงานต่อได้ทันทีโดยไม่หลงทาง

```text
/home/thaieasyvps/zero-touch-infrastructure/
  ├── prefect/           # [The Brain] Prefect Orchestrator (Docker)
  ├── postgres/          # [The Vault] ฐานข้อมูลเก็บ Log, สคริปต์, สถานะบอท (Docker)
  ├── traefik/           # [The Gateway] ระบบจัดการ Port และ Reverse Proxy (Docker)
  └── workspace/         # [The Factory] พื้นที่เขียน Python Scripts
       ├── .venv/                   # สภาพแวดล้อม Python (uv)
       ├── scrapers/                # สคริปต์ดูดข้อมูลสินค้า (Shopee/TikTok)
       ├── generators/
       │    ├── script_writer.py    # สคริปต์เรียก CLIProxyAPI (Local LLM) แต่งบทพูด
       │    ├── tts_engine.py       # สคริปต์ทำเสียงพากย์ (รองรับ Google TTS, Edge-TTS)
       │    └── subtitle_maker.py   # สคริปต์ Faster-Whisper ทำซับคาราโอเกะ
       ├── assemblers/
       │    └── ffmpeg_mixer.py     # สคริปต์ประกอบคลิป (Dim background, Text Overlay, Typewriter)
       └── publishers/
            ├── facebook_poster.py  # โพสต์ลง Facebook Reels (facebook-business)
            └── tiktok_poster.py    # โพสต์ลง TikTok
```

## 2. ขั้นตอนการสร้างวิดีโอ (The Factory Pipeline)
*ทุกฟังก์ชันในโฟลเดอร์ `workspace` จะต้องถูกเขียนให้รับคำสั่งผ่าน Command Line หรือถูกเรียกเป็น Python Module ได้ เพื่อให้ Prefect นำไปต่อจิ๊กซอว์*

1. **Information Gathering:** `scrapers/` หา Winning Product (ราคา 199-499, คอม >10%) หรือหา Quote คำคม 
2. **Compliance Check:** นำเนื้อหาผ่านระบบ `compliance_checker.py` (ดักคำว่า รักษา, หายขาด, แอดไลน์)
3. **AI Generation:** `script_writer.py` นำเนื้อหามาเขียนบทพูด 45 วินาที โดยใช้ 5 สูตร Hook ดึงสายตา
4. **Voice Creation:** `tts_engine.py` สุ่มเลือกค่ายเสียง (Edge/Google) เพื่อไม่ให้ซ้ำซาก
5. **Video Assembly (FFmpeg Magic):** `ffmpeg_mixer.py` ประกอบภาพ:
    *   ถ้าเป็นคลิป **"สายคำคม (Quotes)"**: ใช้ B-Roll นิ่งๆ + ทำขอบมืด (Vignette) + ใส่เอฟเฟกต์พิมพ์ดีดข้อความ + BGM Lo-fi คลอ
    *   ถ้าเป็นคลิป **"สาย Affiliate (ขายของ)"**: ตัดสลับภาพไวปานแสง (Fast Cuts) + ใส่ซับคาราโอเกะ (Faster-Whisper)
6. **Distribution:** `publishers/` โยนวิดีโอ .mp4 ขึ้นเพจเป้าหมาย พร้อมติดลิงก์ Affiliate

## 3. กิมมิคที่ห้ามลืม (Unique Hooks)
เพื่อให้วิดีโอไม่ถูกมองว่าเป็น AI ขยะ สคริปต์ `ffmpeg_mixer.py` ต้องมีสิ่งเหล่านี้เสมอ:
- **Audio Ducking:** เสียง BGM ต้องดรอป (เบาลง) ทุกครั้งที่มีเสียงพากย์ (TTS) หรือเสียง SFX (Typewriter) แทรกเข้ามา (ใช้ `amix=inputs=2:duration=first:dropout_transition=2`)
- **Typewriter Effect + SFX:** ใช้ `enable='between(t,start,end)'` ใน `drawtext` และมิกซ์เสียงพิมพ์ดีดเฉพาะวินาทีที่ข้อความเด้งขึ้นมา
- **Smart Blur / Dimming:** ฉากหลังต้องดรอปแสงลง หรือใส่ Vignette (`vignette=PI/4`) เพื่อให้ Text สีขาวลอยเด่นกระแทกตาเสมอ
- **Intentional Imperfection:** เสียงพากย์ TTS ต้องมีการบังคับใส่ `...` (เว้นวรรคหายใจ) ให้ฟังดูเป็นมนุษย์

## 4. ข้อควรระวัง (Pitfalls)
- **FFmpeg Default Audio Mapping (`-map 0:a?`):** เมื่อใช้คลิป B-Roll เป็นพื้นหลัง ต้องลบคำสั่ง `-map 0:a?` ออกเสมอเพื่อ Mute เสียงของคลิปวิดีโอต้นฉบับ ป้องกันไม่ให้เสียงเดิมตีกับ BGM หรือ TTS ที่เราใส่เข้าไปใหม่
- **Font Rendering Issue:** FFmpeg รันบน Linux เปล่าๆ จะไม่มีฟอนต์ไทย ทำให้สระลอยหรือกลายเป็นกรอบสี่เหลี่ยม *ต้องบังคับระบุ Path ไปที่ `/home/thaieasyvps/.fonts/Sarabun/Sarabun-Bold.ttf` เสมอ*
- **CRITICAL THAI TEXT LIMITATION (FFmpeg drawtext):** การใช้ `drawtext` ของ FFmpeg จะทำให้เกิดปัญหา สระ/วรรณยุกต์หาย (Tone marks missing), สระซ้อนทับกัน, ข้อความล้นจอ, และเกิดตัวอักษรขยะ (Rogue characters) เมื่อเจอภาษาไทยที่ซับซ้อน **ต้องเปลี่ยนไปใช้ Python PIL (Pillow)** วาดข้อความลงบนภาพ PNG โปร่งใสทีละเฟรม แล้วใช้ FFmpeg เอาภาพ PNG ไปซ้อนทับ (Overlay) แทนการใช้ `drawtext` โดยตรง
- **Local LLM Limitation:** แม้ CLIProxyAPI จะใช้ฟรี แต่ Model อาจจะหลอน (Hallucination) ได้ ต้องมี Task ตรวจสอบรูปแบบ (JSON Validator) เสมอก่อนส่งไปทำ TTS
- **Docker Compose Chaos:** Service `postgres`, `prefect`, `traefik` รันใน Network `satang_network` เดียวกัน เวลาเขียนโค้ดต่อ DB ให้ใช้ `127.0.0.1` ถ้ารัน Python บนโฮสต์, หรือใช้ชื่อ Container ถ้ารันโค้ดใน Docker ด้วยกัน

## 5. แผนการเพิ่มขยาย (Scale Up Plan)
เมื่อ Pipeline ชุดแรก (Template คำคม) สำเร็จ จะสามารถต่อยอดเป็น:
- **DaaS (Data as a Service):** นำข้อมูลที่ Scraper หามาได้ทุกวัน โยนเข้า The Vault แล้วเปิด FastAPI ให้คนเช่าดึงข้อมูล
- **Micro-SaaS:** นำคลิปวิดีโอไปรันแอดเข้า LINE OA และใช้ LangGraph ปั้น AI เป็นแอดมินตอบแชทปิดการขาย
