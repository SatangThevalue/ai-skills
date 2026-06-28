---
name: hermes-discord-setup
description: Configure and enable the Discord bot integration for Hermes.
version: 0.1.0
metadata:
  hermes:
    tags: [Discord, Integration, Gateway, Chatbot, Configuration]
---

# การตั้งค่าการเชื่อมต่อ Discord Bot สำหรับ Hermes Agent

Skill นี้รวบรวมขั้นตอน วิธีการกำหนดสิทธิ์ และการตั้งค่าตัวแปรสภาพแวดล้อมเพื่อเชื่อมโยงบอท Hermes Agent เข้ากับเซิร์ฟเวอร์ Discord รวมถึงกลเม็ดทางเทคนิคในการรีสตาร์ทบริการ Gateway จากภายในห้องแชต (Deferred Restart)

ไม่ครอบคลุมการเขียนโปรแกรม Discord API เพิ่มเติม

## When to Use

- เมื่อต้องการเชื่อมต่อบอท Hermes เข้ากับ Discord
- ต้องการล็อกสิทธิ์ให้บอทคุยเฉพาะกับผู้ใช้ที่ได้รับอนุญาต (Allowed Users)
- ต้องการเปิดโหมดไม่ต้องพิมพ์ `@mention` นำหน้าในห้องแชตที่กำหนด (Free Response Channel)
- ต้องการรีสตาร์ทบอทเพื่อรับค่าคอนฟิกใหม่โดยไม่มีการขัดข้องทางเซสชัน

## Prerequisites

- มีบัญชี Discord และสิทธิ์ในการจัดการเซิร์ฟเวอร์ (Manage Server)
- สร้างแอปพลิเคชันบอทใน Discord Developer Portal และได้รับ Token
- มีสิทธิ์เขียนทับไฟล์ `~/.hermes/.env` บน VPS

## How to Run

ใช้งานผ่านเครื่องมือ `terminal` ในการเขียนทับหรืออัปเดตไฟล์ `.env` และเรียกใช้เครื่องมือ `cronjob` สำหรับสั่งการรันคำสั่งควบคุมบริการของระบบ (Systemd)

## Quick Reference

ตัวแปรสภาพแวดล้อมสำคัญที่ต้องกำหนดใน `~/.hermes/.env`:
```text
DISCORD_BOT_TOKEN=your-token-here
DISCORD_ALLOWED_USERS=your-user-id
DISCORD_HOME_CHANNEL=channel-id
DISCORD_FREE_RESPONSE_CHANNELS=channel-id
```

---

## Procedure

### ขั้นตอนที่ 1: ตั้งค่าบอทบน Discord Developer Portal

1. ไปที่ [Discord Developer Portal](https://discord.com/developers/applications) และสร้าง **New Application**
2. ไปที่เมนู **Bot** จากนั้น:
   - สลับเปิด **Public Bot** เป็น **ON** (หากต้องการใช้ลิงก์เชิญมาตรฐาน)
   - เลื่อนไปยังหัวข้อ **Privileged Gateway Intents** และเปิด **ON** ที่ตัวเลือก:
     - `Server Members Intent`
     - `Message Content Intent` (⚠️ **ห้ามลืม:** หากไม่เปิด บอทจะออนไลน์แต่จะไม่ตอบสนองต่อแชตใดๆ)
3. กดปุ่ม **Reset Token** เพื่อสร้างและคัดลอก **Bot Token** นำมาใช้ในขั้นตอนถัดไป

---

### ขั้นตอนที่ 2: การเชิญบอทเข้าสู่เซิร์ฟเวอร์

1. ไปที่เมนู **OAuth2** > **URL Generator** หรือเมนู **Installation**
2. เลือก Scopes: `bot` และ `applications.commands`
3. เลือก Bot Permissions ขั้นต่ำ: `Send Messages`, `Read Message History`, `Attach Files`, `Embed Links`, `Add Reactions`
4. คัดลอกลิงก์ที่ระบบสร้างให้ นำไปเปิดในเบราวเซอร์ เลือกเซิร์ฟเวอร์ปลายทาง แล้วกดยืนยัน

---

### ขั้นตอนที่ 3: กำหนดค่าคอนฟิกบน VPS

เขียนข้อมูลการเชื่อมต่อไปยังไฟล์สภาพแวดล้อมของ Hermes ใน VPS โดยใช้การอัปเดตบรรทัดแทนที่จะเขียนใหม่ทั้งหมดเพื่อรักษารายการ API Key เดิม:

1. ใช้เครื่องมือ `terminal` รันคำสั่ง Python เพื่อจัดเตรียมคีย์และไอดีให้เรียบร้อย:
   ```bash
   python3 -c "
   import os
   path = os.path.expanduser('~/.hermes/.env')
   with open(path, 'r') as f:
       lines = f.readlines()

   new_lines = [l for l in lines if not l.startswith(('DISCORD_BOT_TOKEN=', 'DISCORD_ALLOWED_USERS=', 'DISCORD_HOME_CHANNEL=', 'DISCORD_FREE_RESPONSE_CHANNELS='))]
   
   new_lines.append('DISCORD_BOT_TOKEN=YOUR_BOT_TOKEN\n')
   new_lines.append('DISCORD_ALLOWED_USERS=YOUR_DISCORD_USER_ID\n') # บังคับสิทธิ์เข้าถึงเฉพาะคุณ
   new_lines.append('DISCORD_HOME_CHANNEL=YOUR_TARGET_CHANNEL_ID\n') # ห้องหลักที่ใช้ส่งข้อความแจ้งเตือน
   new_lines.append('DISCORD_FREE_RESPONSE_CHANNELS=YOUR_TARGET_CHANNEL_ID\n') # ห้องที่ไม่ต้อง tag บอทนำหน้า
   
   with open(path, 'w') as f:
       f.writelines(new_lines)
   print('Updated Discord configs in .env')
   "
   ```
2. ตั้งค่าให้เปิดใช้งานแพลตฟอร์ม Discord ในไฟล์คอนฟิกหลัก:
   ```bash
   hermes config set gateway.platforms '["telegram", "discord"]'
   ```

---

### ขั้นตอนที่ 4: สั่งรีสตาร์ทบริการแบบเลื่อนเวลา (Deferred Restart)

⚠️ **ข้อพึงระวัง:** คุณไม่สามารถสั่ง `hermes gateway restart` หรือ `systemctl --user restart hermes-gateway` ตรงๆ จากหน้าต่างแชต (Telegram หรือ Web Dashboard) ได้ เพราะระบบความปลอดภัยจะบล็อกไว้ (การรีสตาร์ทตรงๆ จะส่งสัญญาณ SIGTERM ไปตัดกระบวนการทำงานของคำสั่งตัวเองและทำให้ระบบหยุดค้าง)

**วิธีการแก้ไข (Deferred Restart):**
1. หาเวลาปัจจุบันของระบบเป็นรูปแบบ UTC:
   ```bash
   date -u +"%Y-%m-%dT%H:%M:%SZ"
   ```
2. สร้าง **one-shot cronjob** ให้เริ่มทำงานในอีก 30 วินาทีถัดไป เพื่อส่งคำสั่งรีสตาร์ทระดับระบบปฏิบัติการภายนอกแชต:
   ```json
   cronjob(action="create", prompt="systemctl --user restart hermes-gateway", schedule="2026-06-28T07:55:00")
   ```
3. เมื่อเวลาผ่านไป ตรวจสอบว่าบอทรีสตาร์ทสำเร็จและระบบทำความสะอาดเรียบร้อย:
   ```bash
   systemctl --user status hermes-gateway
   hermes cron list
   ```

---

## Pitfalls

- **Message Content Intent ปิดอยู่:** อาการคือบอทมีสถานะออนไลน์ (สีเขียว) ใน Discord แต่ไม่ว่าเราจะพิมพ์อะไร บอทก็ไม่ตอบสนองเลย ให้กลับไปเปิด Intent นี้ใน Developer Portal แล้วรีสตาร์ท Gateway
- **จำกัดสิทธิ์ผู้ใช้ (`DISCORD_ALLOWED_USERS`):** หากไม่ได้ระบุไอดีของคุณ บอทอาจไม่ยอมคุยด้วย หรือถ้าใส่ไอดีผิด บอทจะทำการ Ignore ข้อความทั้งหมดเพื่อความปลอดภัย ให้เช็คความถูกต้องของไอดี
- **บอทค้างจากการรีสตาร์ทตรงๆ:** หากเผลอรันคำสั่ง restart หรือ stop ภายในแชตจนบริการค้าง ให้ล็อกอิน SSH เข้ามาที่ VPS แล้วสั่งรัน `systemctl --user restart hermes-gateway`

## Verification

การตรวจสอบว่าเชื่อมต่อสำเร็จ:
- บริการ `hermes-gateway` ต้องมีสถานะเป็น `active (running)` ในระบบ systemd
- เมื่อพิมพ์ข้อความทักทายลงในห้องแชต Discord ที่กำหนด บอท "น้องต้นทอง" จะต้องสามารถตอบกลับแชตของคุณได้ทันทีโดยไม่ต้อง @mention
