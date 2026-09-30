---
name: prefect-social-media-factory
description: Orchestrate scheduled social media content workflows.
version: 0.1.0
metadata:
  hermes:
    tags:
      - Prefect
      - Automation
      - Telegram
      - ContentStudio
      - PostgreSQL
---

# Prefect Social Media Factory

Orchestrates multi-channel content production, upstream dataset harvesting, Telegram approval workflows, and automated social publishing using Python Prefect. This skill runs zero-token background watchdogs and schedules; it does not replace the human creative decision or publish unapproved drafts. All database operations target Docker PostgreSQL, and media assets sync directly to Google Drive.

## When to Use

- "ตั้งค่าระบบกวาดข้อมูลและโพสต์อัตโนมัติด้วย Prefect" (Configure automated data harvesting and publishing with Prefect)
- "สร้างตารางสรุปงานเช้าและคิวรออนุมัติใน Telegram" (Create daily morning briefing and Telegram approval queue)
- "ตั้งเวลาสุ่มนาทีธรรมชาติเพื่อเลี่ยงการตรวจจับบ็อต" (Set randomized human-jitter posting times to avoid bot detection)
- "ดึงข้อมูลจากพันทิปและ Open API มาเป็นวัตถุดิบทำคอนเทนต์" (Scrape Pantip and Open APIs into database on schedule)

## Prerequisites

- Linux host running Docker with a PostgreSQL container (e.g. `satang-vault-db` running database `media_studio`).
- Python 3.10+ with `prefect`, `requests`, and `Pillow` installed.
- Telegram Bot Token stored in `/home/thaieasyvps/.satang_bot_token` and an authorized Telegram `chat_id`.
- Google Workspace token stored at `/home/thaieasyvps/.hermes/google_token.json`.
- System cron access (`crontab -e`).

## How to Run

1. Initialize database tables (`upstream_api_feeds`, `pantip_trending_topics`, `content_calendar_plans`).
2. Schedule data collection and briefing flows using `terminal` via crontab.
3. Review and approve pending drafts through the interactive Telegram bot daemon.
4. Execute publishing sweeps via Prefect when posts reach their randomized posting window.

## Quick Reference

| Component | Hermes Tool | Command / File |
| :--- | :--- | :--- |
| Open APIs Harvester | `terminal` | `python3 /home/thaieasyvps/satang_content_studio/satang_prefect_open_apis_harvester.py` |
| Pantip Forum Harvester | `terminal` | `python3 /home/thaieasyvps/satang_content_studio/satang_prefect_pantip_harvester.py` |
| Morning Executive Briefing | `terminal` | `python3 /home/thaieasyvps/satang_content_studio/prefect_morning_briefing.py` |
| Auto-Publisher Sweeper | `terminal` | `python3 /home/thaieasyvps/satang_prefect_sweeper.py` |
| Telegram Bot Daemon | `terminal` | `python3 /home/thaieasyvps/satang_content_studio/telegram_bot_daemon.py` |

## Procedure

1. **Configure Host Crontab Schedule (Asia/Bangkok GMT+7)**
   Set up cron jobs to trigger zero-token Prefect flows timed for a 05:30 AM wake-up routine:
   ```bash
   # Upstream Open APIs (World Bank, Currencies, GitHub AI, Climate) at 04:30 AM
   30 4 * * * python3 /home/thaieasyvps/satang_content_studio/satang_prefect_open_apis_harvester.py >> /home/thaieasyvps/open_apis_harvester.log 2>&1
   
   # Pantip Forum Scraper (Silom, Sinthorn, Food) every 6 hours (05:00, 11:00, 17:00, 23:00)
   0 5,11,17,23 * * * python3 /home/thaieasyvps/satang_content_studio/satang_prefect_pantip_harvester.py >> /home/thaieasyvps/pantip_harvester.log 2>&1
   
   # Daily Morning Executive Briefing to Telegram at 05:30 AM sharp
   30 5 * * * python3 /home/thaieasyvps/satang_content_studio/prefect_morning_briefing.py >> /home/thaieasyvps/morning_briefing.log 2>&1
   
   # Auto-Publisher Sweeper running every 15 minutes (0-token watchdog)
   */15 * * * * python3 /home/thaieasyvps/satang_prefect_sweeper.py >> /home/thaieasyvps/prefect_sweeper.log 2>&1
   ```

2. **Produce Content Drafts with Anti-Duplication Guard**
   Before rendering images or drafting copy, check the 45-day topic cooldown in PostgreSQL:
   ```bash
   python3 -c "
   from satang_content_studio.deduplication_guard import check_topic_cooldown
   res = check_topic_cooldown('หัวข้อที่ต้องการตรวจสอบ')
   print(res)
   "
   ```
   If `is_duplicate` is `False`, run `/home/thaieasyvps/satang_content_studio/studio_pipeline.py`. It renders the graphic, uploads to Google Drive with the short format `{YYYYMMDD}-{XXXX}.png`, evaluates quality, and records the post as `PENDING_REVIEW`.

3. **Handle Telegram In-Place Approval & Surgical Revisions**
   Run `telegram_bot_daemon.py` in the background. When an interactive card arrives:
   - Tap `[✅ อนุมัติยิงตามเวลา]` to transition state to `APPROVED_BY_USER`.
   - Tap `[✏️ ขอให้แก้ไข]` to reveal the surgical sub-menu (Hook, Shorten, Image, Custom).
   - Tap `[❌ ปัดตก]` to cancel publication.
   The bot mutates the message in-place via `editMessageText`, eliminating chat noise.

4. **Execute Publishing with Randomized Human Jitter**
   When the sweeper runs, it checks for posts where `human_approval_status = 'APPROVED_BY_USER'` and `scheduled_at <= NOW()`. It executes the Graph API upload, posts and pins the monetized comment, and logs the execution to `publishing_jobs` and `token_ledger`.

## Pitfalls

- **Prefect Server Ephemeral Mode Timeout:** When running raw flows from CLI without setting `PREFECT_API_URL`, Prefect may spin up a temporary server that times out under load. Always ensure `PREFECT_API_URL` points to your dedicated server (e.g. `http://100.115.66.121:4200/api`) or keep tasks lightweight.
- **Fixed-Time Posting Bot Flags:** Publishing at exact zero-second marks (`16:30:00`) repeatedly causes Meta spam filters to throttle page Reach. Always calculate a human-jitter minute (`random.randint(30, 58)`) and second (`random.randint(10, 50)`).
- **Telegram Bot Multi-User Security:** Unrestricted callback handlers allow unauthorized chat members to approve or delete posts. Always enforce `if user_id != AUTHORIZED_USER_ID: return` before processing callbacks.

## Verification

Test the morning briefing flow and verify Telegram message delivery:
```bash
python3 /home/thaieasyvps/satang_content_studio/prefect_morning_briefing.py | grep -q "Success = True" && echo "FACTORY_PIPELINE_OK"
```
The check outputs `FACTORY_PIPELINE_OK` when the briefing flow aggregates database metrics and sends the interactive report to Telegram successfully.