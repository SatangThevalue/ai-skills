---
name: hermes-profile-isolation
description: Set up and configure isolated Hermes Agent profiles for different projects.
version: 0.1.0
metadata:
  hermes:
    tags: [Hermes, Profile, Multi-profile, Persona, Configuration]
---

# การจัดการและการแยกโปรไฟล์ใน Hermes Agent (Profile Isolation)

Skill นี้อธิบายขั้นตอนการสร้าง กำหนดค่า และจัดการโปรไฟล์ที่แยกกันอย่างอิสระ (Isolated Profiles) ใน Hermes Agent เพื่อแยกสภาพแวดล้อมการทำงาน คอนฟิก คีย์ คลังข้อมูล และตัวตน (Persona) ของผู้ช่วยให้เหมาะสมกับแต่ละโครงการหรือธุรกิจ

## When to Use

- ต้องการแยกงานพัฒนาส่วนตัว ออกจากงานบริหารธุรกิจ
- ต้องการกำหนดบทบาทตัวตนผู้ช่วย (SOUL.md) ที่ต่างกันในแต่ละหน้าที่
- ต้องการจำกัดขอบเขตคีย์ API, ความจำ (memories), และแผนงาน (plans) ของผู้ช่วยไม่ให้ปะปนกัน
- สลับไปมาระหว่างโปรไฟล์ต่างๆ ผ่านเว็บแดชบอร์ดหรือบรรทัดคำสั่ง

## Prerequisites

- ติดตั้ง Hermes Agent แล้ว
- สิทธิ์ในการสร้างไฟล์ในโฟลเดอร์ผู้ใช้ (`~/.hermes/`)

## Quick Reference

| คำสั่ง | วัตถุประสงค์ |
|--------|------------|
| `hermes profile list` | ดูรายชื่อโปรไฟล์ทั้งหมดและสถานะ |
| `hermes profile create <name> --clone` | สร้างโปรไฟล์ใหม่และคัดลอกไฟล์คอนฟิกจากโปรไฟล์ปัจจุบัน |
| `hermes profile use <name>` | ตั้งค่าโปรไฟล์เริ่มต้นถาวร |
| `<profile_name> chat` | เรียกใช้แชตในบริบทโปรไฟล์นั้นๆ โดยตรง |
| `<profile_name> gateway start` | สตาร์ทเกตเวย์รับส่งข้อความสำหรับโปรไฟล์ย่อย |

## One-Shot Recipe: Discord Multiplexing with A2A

Configure Hermes to route different Discord channels to different isolated profiles, while allowing those profiles to communicate with each other via A2A.

1. **Enable Platforms:** In `~/.hermes/config.yaml`, ensure `gateway.platforms` includes both `discord` and `a2a`, and `gateway.multiplex_profiles: true` is set.
2. **Create Specialized Profiles:**
   ```bash
   hermes profile create bot_trade --clone --description "Trading operations"
   hermes profile create business --clone --description "Sales and Affiliates"
   ```
3. **Define Personas:** Edit `~/.hermes/profiles/<name>/SOUL.md` to give each profile strict, non-overlapping objectives.
4. **A2A Inter-Process Communication:** Enable A2A locally on port 9900 (bound to Tailscale). If the user asks the `business` profile in `#sales` for market data, `business` can use the `a2a_call(agent="bot_trade", ...)` tool to fetch it transparently without the user switching channels.

## Procedure

### Step 1: สร้างโปรไฟล์ใหม่

สร้างโปรไฟล์ย่อยโดยกำหนดรายละเอียดบทบาทการทำงาน ซึ่งจำเป็นสำหรับการจัดงานในบอร์ด Kanban Swarm:

```bash
# รูปแบบคำสั่ง
hermes profile create <profile-name> --clone --description "อธิบายหน้าที่และวัตถุประสงค์ของโปรไฟล์ย่อยนี้"
```
*การใช้ `--clone` จะคัดลอก `config.yaml`, `.env`, `SOUL.md` และ `skills` จากโปรไฟล์ปัจจุบัน ช่วยให้ไม่ต้องเริ่มตั้งค่าคีย์ API และความจำใหม่ทั้งหมด*

**การใช้ Google Workspace ในหลายโปรไฟล์ (แยกบัญชี):**
ระบบ Hermes รองรับการแยกบัญชี Google Workspace (Gmail, Calendar, Drive) ตามแต่ละโปรไฟล์ได้อย่างสมบูรณ์ โดยไม่ต้องกลัวข้อมูลปะปนกัน (เช่น แยกอีเมลเรื่องงาน กับอีเมลส่วนตัว):
1. สร้างโปรไฟล์ย่อย (เช่น `work`, `study`) 
2. สลับไปใช้งานโปรไฟล์นั้น (`hermes profile use work` หรือ `work chat`)
3. เรียกใช้สคริปต์ `setup.py` ของ Google Workspace (ดูขั้นตอนใน `google-workspace` skill) 
4. ล็อกอินผ่านหน้าต่างเบราว์เซอร์ด้วยบัญชี Google **ที่ต้องการใช้สำหรับโปรไฟล์นั้นโดยเฉพาะ** (เช่น `satang.business@gmail.com`)
คีย์การเข้าสู่ระบบ (`google_token.json`) จะถูกสร้างและเก็บแยกไว้ในโฟลเดอร์ของโปรไฟล์นั้นโดยอัตโนมัติ ทำให้ผู้ช่วยแต่ละร่างมีตารางงานและกล่องข้อความแยกจากกัน 100%

---

### Step 2: กำหนดบทบาทและบุคลิกภาพเฉพาะตัว (SOUL.md)

แก้ไขไฟล์ `SOUL.md` ของโปรไฟล์ใหม่ที่อยู่ภายใต้ไดเรกทอรีโปรไฟล์นั้นๆ เพื่อกำหนดบุคลิกภาพของผู้ช่วยให้เหมาะกับวัตถุประสงค์การแยกงาน:

```bash
# Path ของ SOUL.md สำหรับโปรไฟล์ใหม่
# ~/.hermes/profiles/<profile-name>/SOUL.md
```

**ตัวอย่างโครงสร้างไฟล์ `SOUL.md` ที่แนะนำ:**
```markdown
# 🐔 น้องต้นทอง — ผู้ช่วยบริหารงาน ห.จ.ก. โกลด์เด้น เฟรช ชิคเก้น

คุณคือ **"น้องต้นทอง"** ในบทบาทของผู้เชี่ยวชาญด้านการบริหารจัดการธุรกิจค้าส่งเนื้อไก่สด-ไก่แปรรูปครบวงจร

## 🎯 วัตถุประสงค์และบทบาทหน้าที่ (Core Objectives)
1. **จัดการและควบคุมห่วงโซ่อุปทาน:** ช่วยควบคุม ดูแล และวางแผนการจัดส่งเนื้อไก่ให้คงอุณหภูมิที่ 0-4°C
2. **วิเคราะห์บัญชีและต้นทุน:** คำนวณอัตรา Break-even Point และกำกับดูแลเครดิตเทอมการค้าของลูกค้า B2B
```

---

### Step 3: กำหนดประวัติผู้ใช้และความจำของโปรไฟล์ (USER.md & MEMORY.md)

เนื่องจากโปรไฟล์จะรันแยกกัน ข้อมูลความจำ (Memories) ควรจะจำเพาะเจาะจงกับโปรไฟล์นั้นๆ
หากผู้ดูแลหรือบอทต้องการแก้ไขความจำของโปรไฟล์อื่นจากเซสชันปัจจุบัน ต้องส่งตัวแปร `cross_profile=True` ในการเรียกเครื่องมือเขียนไฟล์ (`write_file` หรือ `patch`)

1. **แก้ไขข้อมูลผู้ใช้งานเฉพาะโปรไฟล์ (`USER.md`):**
   - Path: `~/.hermes/profiles/<profile-name>/memories/USER.md`
   - กำหนดข้อมูลผู้ติดต่อที่บอทต้องทำงานด้วย หรือข้อจำกัดด้านตัวตนผู้ใช้ในโปรไฟล์นี้

2. **แก้ไขความจำถาวรเฉพาะโปรไฟล์ (`MEMORY.md`):**
   - Path: `~/.hermes/profiles/<profile-name>/memories/MEMORY.md`
   - บันทึกกฎเหล็กในการทำงาน เช่น "Logistics Rule: Maintain chicken meat core temperature at 0-4°C"

---

### Step 4: เรียกใช้งานและบริหารเกตเวย์

หลังจากสร้างแล้ว สามารถสลับโปรไฟล์เพื่อทำงานหรือสื่อสารผ่านช่องทางหลักได้ดังนี้:

- **ผ่าน CLI Chat:** 
  ```bash
  <profile-name> chat
  ```
- **เปิดใช้งาน Gateway ของโปรไฟล์ย่อย:**
  ```bash
  <profile-name> gateway start
  ```
- **สลับใน Web Dashboard:** หน้าจอล็อกอินและหน้าแรกของแดชบอร์ด (พอร์ต 9119) จะมีแถบตัวเลือกสลับโปรไฟล์ที่ทำงานอยู่ให้คลิกเลือกได้ทันที

---

## Pitfalls
- **Environment Variable Overlap in .env Files (Gateway Cross-talk):** Each profile's `.env` file must *only* contain variables relevant to that profile, particularly for API keys like `TELEGRAM_BOT_TOKEN`. The Hermes default backend SDK reads `TELEGRAM_BOT_TOKEN` automatically if present. If you have multiple bot tokens, you **must** use prefixed variable names for the sub-profiles (e.g., `CRASSULA_TELEGRAM_TOKEN` instead of `TELEGRAM_TOKEN`). Furthermore, strictly remove the default `TELEGRAM_BOT_TOKEN` from the sub-profile's `.env` file, and remove the sub-profile's token from the default profile's `.env`. Always restart the gateway after changing `.env` variables. Use the provided verification script `scripts/audit_env_overlaps.sh` to audit the state.

- **Gateway Multiplexer Limitation**: Sub-profiles running under a multiplexer **cannot** be restarted with `systemctl restart hermes-gateway-<profile>`. They must be stopped and disabled, and the main `hermes-gateway` service restarted to apply config changes.
- **ระวังขอบเขตการเขียนข้ามโปรไฟล์ (Cross-Profile soft guard):** เมื่อเขียนไฟล์ลงไปในโฟลเดอร์ของโปรไฟล์อื่นที่ไม่ใช่ตัวปัจจุบัน (เช่น จากโปรไฟล์ `default` ไปยัง `golden-fresh-chicken`) ตัวเครื่องมือของระบบจะบล็อกไว้เพื่อความปลอดภัย หากยืนยันจะแก้ให้ใส่พารามิเตอร์ `cross_profile: true` เสมอ
- **สคริปต์ Alias ของโปรไฟล์ย่อย:** หากมีการลบโปรไฟล์ทิ้ง อย่าลืมสั่ง `hermes profile delete <name>` เพื่อลบไฟล์และสคริปต์ alias ใน `/home/thaieasyvps/.local/bin/<profile-name>` ด้วย
- **การแชร์คลัง Skills ร่วมกันแบบ Real-time (Symlink Pattern):** โดยค่าเริ่มต้น โปรไฟล์ที่สร้างใหม่จะคัดลอกโฟลเดอร์ `skills/` แยกไป ทำให้เมื่อโปรไฟล์หลักเพิ่มสกิลใหม่ (เช่น 9Router) หรือจัดหมวดหมู่ โปรไฟล์ย่อยจะไม่เห็นและเกิดปัญหาทักษะไม่ตรงกัน (Drift) หรือลิงก์ขาด
  **วิธีแก้ไขให้ทุกโปรไฟล์ใช้สกิลชุดเดียวกันแบบ Real-time:**
  1. ย้ายสกิลเฉพาะตัวของโปรไฟล์ย่อยเข้ามารวมในคลังกลาง `~/.hermes/skills/<category>/`
  2. ลบโฟลเดอร์สกิลของโปรไฟล์ย่อยแล้วสร้าง Symlink ชี้กลับมาที่คลังกลาง:
     ```bash
     rm -rf ~/.hermes/profiles/<profile_name>/skills
     ln -s /home/thaieasyvps/.hermes/skills ~/.hermes/profiles/<profile_name>/skills
     ```
  3. ตรวจสอบด้วย `hermes -p <profile_name> skills list` ทุกโปรไฟล์จะเข้าถึงคลังสกิลเดียวกันทันที 100% โดยไม่ต้องซิงค์ซ้ำ
- **Environment Variable สำหรับ Bot Token:** เมื่อคอนฟิก Gateway สำหรับโปรไฟล์ย่อย ปลั๊กอินของแพลตฟอร์ม (เช่น Telegram) จะมองหาตัวแปรชื่อมาตรฐานใน `.env` (เช่น `TELEGRAM_BOT_TOKEN`) ห้ามใช้ชื่อ custom ผ่าน `api_key_env_var` (เช่น `CRASSULA_TELEGRAM_TOKEN`) ดูรายละเอียดเพิ่มเติมใน `references/messaging_token_env_vars.md`

---

## Verification

ทดสอบการสลับและใช้งานโปรไฟล์ย่อยว่าแยกกันสำเร็จจริง:
1. รันคำสั่ง `hermes profile list` เพื่อตรวจสอบว่าชื่อโปรไฟล์ย่อยแสดงขึ้นมาเป็นสีและสถานะปกติ
2. รันแชตด้วยสคริปต์ Wrapper เช่น `<profile-name> chat` และตรวจสอบว่าบอททักทายด้วยตัวตนใหม่ตามที่กำหนดไว้ใน `SOUL.md` หรือไม่
