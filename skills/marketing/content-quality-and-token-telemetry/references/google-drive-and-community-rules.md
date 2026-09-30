# Google Drive Standards, Human Jitter & Smart Community Filtering

Operational specifications for asset file storage, schedule randomization, and community engagement.

## 1. Google Drive Master-Child Directory Hierarchy

Do not store assets across ad-hoc directories or rely solely on local disk storage. Maintain a clean Master-Child hierarchy:

```
📁 [Master Root Folder] Satang_Social_Media_Hub
    │
    ├── 📁 [Page A] Satang_The_Value_Assets (ID: 1s1Zq0NE1dqC_7dasq5cMi3wlkhzpM8_x)
    │      ├── 🖼️ 20261001-0001.png
    │      ├── 🖼️ 20261002-0002.png
    │      └── 🖼️ 20261003-0003.png
    │
    ├── 📁 [Page B] Lifestyle_Page_Assets
    └── 📁 [Page C] Tech_AI_Assets
```

### File Naming Standard (User Directive)
- **Format:** `{YYYYMMDD}-{XXXX}.{ext}`
- **Examples:** `20261001-0001.png`, `20261002-0002.png`
- **Rule:** Never embed redundant page codes, long Thai slugs, or cryptic pillar codes into the filename. The folder structure establishes the page identity, and the PostgreSQL database tracks the headline, pillar, template, and evaluation scores.

---

## 2. Randomized Human-Jitter Timing (Anti-Bot Detection)

Meta algorithms aggressively penalize automated bots that drop posts at exact `:00:00` or `:30:00` clock marks across multiple pages.

### Algorithm
Take the target hour (e.g., 08:00, 12:00, 16:00, 19:00) and generate random minutes and seconds within a realistic human window:
```python
import random
from datetime import datetime, time

def get_human_jitter_time(base_hour: int, start_min: int = 30, end_min: int = 58) -> time:
    rand_min = random.randint(start_min, end_min)
    rand_sec = random.randint(10, 50)
    return time(hour=base_hour, minute=rand_min, second=rand_sec)
```
- Base 16:30 -> Scheduled as `16:37:35` or `16:54:12`
- Base 19:30 -> Scheduled as `19:42:08` or `19:57:45`

---

## 3. Smart Community Engagement Filtering (Resource Conservation)

Never invoke LLM completion for every incoming comment. Blanket auto-replying consumes tokens needlessly and degrades the page reputation into an annoying spam bot.

### The 3-Tier Filter Rules
1. **Tier 1 — Ignore / Skip (0 Tokens):**
   - Emojis only (`👍`, `❤️`, `🔥`)
   - Stickers, GIF responses
   - Short compliments (`ขอบคุณครับ`, `สุดยอด`, `555`, `แชร์แล้วครับ`)
   - Political, hostile, or trolling remarks
2. **Tier 2 — Actionable / High-Intent Questions (Selective LLM Response):**
   - Direct purchase or setup queries (`"ซื้อผ่านแอปไหนคะ?"`, `"มีขั้นต่ำเท่าไหร่?"`)
   - Comparison and risk inquiries (`"ต่างจากสลากออมสินยังไง?"`, `"ถ้าตลาดหุ้นตกจะเป็นอย่างไร?"`)
3. **Budget Cap:**
   - Maximum **3 to 5 high-value replies per post**.
   - Strict context prompt: polite, concise (2-3 sentences max), disclaiming individual investment advice.
   - Total community AI cost kept under **0.05 THB per post**.

---

## 4. Telegram HITL Surgical Revision Matrix

When the creator clicks `[ ✏️ ขอให้แก้ไข ]`, present 4 surgical 1-tap options rather than an open-ended generic input prompt:
1. `[ 🎣 1. ปรับ Hook ให้กระตุกต่อมสงสัย ]`: Rewrites only the opening 3-second hook & first sentence. Preserves image and figures.
2. `[ ✂️ 2. ตัดแคปชันให้สั้นลง 30% ]`: Compresses body prose to improve mobile scannability.
3. `[ 🎨 3. ปรับขนาดตัวเลข / สีในภาพ ]`: Re-renders image graphic with boosted contrast or altered typography.
4. `[ 🎙️ 4. พิมพ์หรือส่งเสียงสั่งเอง ]`: Accepts free-form audio/text notes.
