---
name: facebook-monetized-content-engine
description: "Produce SEO-optimized monetized social media content."
version: 0.1.0
metadata:
  hermes:
    tags:
      - Facebook
      - Monetization
      - SEO
      - Automation
      - ContentProduction
---

# Facebook Monetized Content Engine

An end-to-end production pipeline for multi-slot daily social media content engineered for Facebook algorithms and affiliate monetization. It orchestrates 3 distinct daily time slots (morning, noon, evening), Social SEO copywriting, programmatic media rendering with clean `{YYYYMMDD}-{XXXX}.png` naming, Google Drive synchronization, and monetized pinned comments with regulatory disclaimers. It does not publish unapproved drafts or manage paid Facebook Ads.

## When to Use

- "ผลิตคอนเทนต์ประจำวันพร้อมปักหมุดลิงก์สร้างรายได้" (Produce daily content with monetized pinned comments)
- "สร้างแคปชัน Social SEO เอาใจอัลกอริทึม Facebook" (Generate Social SEO captions optimized for Facebook algorithm)
- "รันคิวคอนเทนต์แบบแบ่งสล็อตเวลา เช้า เที่ยง ค่ำ ไม่ให้แย่ง Reach" (Run multi-slot schedules morning noon evening to avoid reach cannibalization)
- "ตั้งค่าระบบผลิตคอนเทนต์หาเงินอัตโนมัติ" (Configure an automated monetized content creation pipeline)

## Prerequisites

- Linux host running Docker with PostgreSQL container `satang-vault-db` (`media_studio` database).
- Python 3.10+ with `Pillow`, `requests`, and Google Client libraries installed.
- Google Workspace OAuth credentials stored at `/home/thaieasyvps/.hermes/google_token.json`.
- Database tables initialized: `content_calendar_plans`, `facebook_content_evaluations`, `managed_pages`.

## How to Run

1. Query planned items in the multi-slot calendar using `terminal`.
2. Generate, render, and evaluate the draft using `terminal` invoking `scripts/produce_monetized_post.py`.
3. Verify asset upload to Google Drive and audit status in Docker PostgreSQL using `terminal`.

## Quick Reference

| Operation | Hermes Tool | Target Command / Script |
| :--- | :--- | :--- |
| View Calendar Slots | `terminal` | `docker exec -i satang-vault-db psql -U admin -d media_studio -c "SELECT plan_date, slot_name, pillar, topic_idea FROM content_calendar_plans ORDER BY id LIMIT 3;"` |
| Produce Next Slot | `terminal` | `python3 scripts/produce_monetized_post.py` |
| Check Review Queue | `terminal` | `docker exec -i satang-vault-db psql -U admin -d media_studio -c "SELECT id, headline, total_score, human_approval_status, gdrive_file_name FROM facebook_content_evaluations ORDER BY id DESC LIMIT 1;"` |

## Procedure

1. **Configure Multi-Slot Daily Cadence**
   Structure each day into 3 distinct operational slots spaced at least 4 hours apart to eliminate reach cannibalization:
   - **Slot 1 (Morning 08:30):** Macroeconomic or currency data (`The Giant Metric`). Catch early-commute feeds in 3 seconds.
   - **Slot 2 (Noon 12:30):** Food, lifestyle, or business cost breakdown (`Receipt Breakdown` / `4-Card Grid`). Engages midday leisure browsing.
   - **Slot 3 (Evening 19:30):** Brand battles or financial showdowns (`The Versus` / `What-If Simulation`). Prime-time conversational drivers.

2. **Draft Social SEO & Algorithm-Optimized Captions**
   Follow the proven viral formula:
   - **The Input-Output Formulaic Hook ("ใส่ X ได้ Y"):** Deliver immediate payoff within the first 125 characters (before the "...ดูเพิ่มเติม" button). Example: *"ใส่เงินต้นเท่ากัน ได้ผลลัพธ์ต่างกัน 2.7 แสน... เปิดตัวเลขจริงมิติคู่ขนาน 10 ปีที่หลายคนไม่เคยคำนวณ"*.
   - **Secret Vault / Insider Framing:** Frame frameworks, calculations, or datasets as high-value insider tools (e.g. *"เครื่องมือลับสาย Data / สูตรลับจัดการเงินที่คน 90% ไม่เคยรู้"*).
   - **Zero External Links in Body:** Never put outbound URLs in the caption body; external links throttle reach by 40-70%. Put all resource links in the first pinned comment.
   - **Keyword Semantic Density:** Weave natural high-volume search phrases (`DCA`, `กองทุนรวม`, `ดอกเบี้ยทบต้น`, `วางแผนการเงิน`, `สลากกินแบ่งรัฐบาล`) into the copy.
   - **Comment-to-DM Keyword Trigger (The Comment-for-Link Funnel):** Prompt users to comment a single trigger keyword: *"พิมพ์ 'DATA' หรือ 'พอร์ต' ในคอมเมนต์ เดี๋ยวส่งลิงก์ตารางคำนวณและสรุปให้ทันที"*. This sends massive Meaningful Social Interaction (MSI) signals to Meta's recommendation engine.
   - **Explicit Bookmark Cue:** Conclude with *"กดเซฟโพสต์นี้ไว้ แล้วแชร์ให้เพื่อนที่กำลังวางแผนการเงินด้วยนะครับ"* to directly elevate the algorithm's Bookmark score.
   - **Controlled Hashtags:** Use 4 to 8 relevant hashtags at the bottom; avoid hashtag stuffing.

3. **Assemble Monetized Pinned Comment with Regulatory Compliance**
   Attach high-intent conversion pathways to the first comment:
   - **Affiliate Finance:** Account opening link (Dime, InnovestX, banks) with promo code.
   - **Affiliate Books / Equipment:** E-commerce referral link.
   - **Digital Products:** Template downloads (Excel, Power BI).
   - **Mandatory SEC (IC P1) Warning:** Append the compulsory educational notice:
     `คำเตือน: จัดทำขึ้นเพื่อการศึกษาเชิงสถิติเท่านั้น มิใช่การชักชวน ชี้ชวน หรือให้คำแนะนำการลงทุน | ผลการดำเนินงานในอดีตมิได้เป็นสิ่งยืนยันถึงผลในอนาคต`

4. **Render Image with Brand DNA & Radical Simplification**
   Execute programmatic rendering enforcing the user's design standards:
   - **Radical 1-on-1 Focus:** Avoid multi-item clutter or stacked card layers. Keep visual focus on 1 comparison with 2 massive hero numbers (Loss Red vs Gain Green) understandable within 2 seconds.
   - **Visual Grandeur:** Adorn with mathematical 4-point radiant stars (✦) in Satang Gold (`#F5A623`) and Electric Cyan (`#38BDF8`) plus ambient nebula glow. Never use plain flat cards or unsupported emoji glyphs that render as tofu boxes.
   - **Strict Text Containment:** Calculate exact text widths using `.getbbox()`. Keep copy concise and ensure every line terminates at least 30-50px inside card borders without wrapping defects.
   - **Standardized Naming:** Save the asset using the short human-intuitive format:
     ```text
     {YYYYMMDD}-{XXXX}.png (e.g. 20261001-0001.png)
     ```
     Upload directly into `Satang_Social_Media_Hub / Satang_The_Value_Assets` on Google Drive.

5. **Pass 4-Dimension Quality Gate & Persist Telemetry**
   Evaluate the post across Hook (30), Clarity (30), Safety (20), and Engagement (20). If `total_score >= 85`, persist the record as `PENDING_REVIEW` into `facebook_content_evaluations` with full token consumption metrics.

## Pitfalls

- **Placing Links in the Caption Body:** Linking out in the main text drops organic post distribution by 40-70%. Always route traffic via the first pinned comment.
- **Posting Too Frequently (< 3 Hours Apart):** Firing multiple posts in quick succession causes Meta's distribution engine to cannibalize the impressions of earlier posts. Maintain at least 4 hours between slots.
- **Unverified Single-Stock Mentions:** Hype or definitive price targets on specific individual stocks without advisory licenses violate SEC regulations. Always focus on broad indices (SET50, S&P 500) and general educational statistics.

## Verification

Run the production pipeline in dry-run verification mode via `terminal`:
```bash
python3 /home/thaieasyvps/satang_content_studio/studio_pipeline.py && echo "CONTENT_ENGINE_OK"
```
The check outputs `CONTENT_ENGINE_OK` when an asset is rendered, synced to Google Drive with clean naming, and logged into Docker PostgreSQL with an approved quality score.