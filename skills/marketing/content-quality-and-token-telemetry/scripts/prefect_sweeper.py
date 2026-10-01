#!/usr/bin/env python3
"""
Zero-Token Prefect Sweeper Daemon
Polls Docker PostgreSQL for posts explicitly marked APPROVED_BY_USER and scheduled for publishing.
Consumes 0 LLM tokens.
"""
import os
import sys
import subprocess
from datetime import datetime
from prefect import flow, task

DB_CMD = ['docker', 'exec', '-i', 'satang-vault-db', 'psql', '-U', 'admin', '-d', 'media_studio']

def run_db_query(sql):
    cmd = DB_CMD + ['-c', sql]
    res = subprocess.run(cmd, capture_output=True, text=True)
    return res.returncode == 0, res.stdout.strip(), res.stderr.strip()

@task(name="Sweep Approved Queue")
def sweep_approved_queue():
    sql = """
    SELECT e.id, e.page_id, m.page_name, e.headline, e.gdrive_file_name, e.scheduled_at
    FROM facebook_content_evaluations e
    JOIN managed_pages m ON e.page_id = m.id
    WHERE e.human_approval_status = 'APPROVED_BY_USER'
      AND e.published_status = 'APPROVED_READY_TO_POST'
      AND (e.scheduled_at IS NULL OR e.scheduled_at <= NOW())
    ORDER BY e.scheduled_at ASC NULLS FIRST
    LIMIT 1;
    """
    ok, out, _ = run_db_query(sql)
    if not ok or "1 row" not in out:
        return None
    lines = [l.strip() for l in out.split('\n') if l.strip() and not l.startswith('-') and not l.startswith('id') and not l.startswith('(')]
    if not lines:
        return None
    parts = [p.strip() for p in lines[0].split('|')]
    return {
        "evaluation_id": int(parts[0]),
        "page_id": int(parts[1]),
        "page_name": parts[2],
        "headline": parts[3],
        "file_name": parts[4],
        "scheduled_at": parts[5]
    }

@task(name="Execute Publishing Job")
def execute_publish(eval_id):
    cmd = ["python3", "/home/thaieasyvps/satang_publisher_engine.py", str(eval_id)]
    res = subprocess.run(cmd, capture_output=True, text=True)
    return res.returncode == 0, res.stdout.strip(), res.stderr.strip()

@flow(name="Satang Facebook Auto-Publisher Sweeper")
def auto_publisher_sweeper_flow():
    target = sweep_approved_queue()
    if not target:
        print("[PREFECT SWEEPER] Queue checked: No approved posts due at this tick. Sleeping quietly (0 tokens used).")
        return "IDLE_NO_POST_DUE"

    eval_id = target["evaluation_id"]
    print(f"[PREFECT SWEEPER] Found approved post ready to publish! ID: {eval_id} | Headline: {target['headline']}")
    
    success, stdout, stderr = execute_publish(eval_id)
    if success:
        print(f"[PREFECT SWEEPER] Post {eval_id} successfully published and logged!")
        try:
            import requests
            bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
            chat_id = os.getenv("TELEGRAM_CHAT_ID", "7789252439")
            if bot_token:
                msg = f"<b>🎉 โพสต์สำเร็จเรียบร้อยแล้ว!</b>\n\n<b>หัวข้อ:</b> {target['headline']}\n<b>สถานะ:</b> เผยแพร่ขึ้น Facebook Feed เรียบร้อย พร้อมปักหมุดลิงก์สร้างรายได้ (Affiliate)\n\n<i>ระบบ Prefect ดำเนินการยิงโพสต์ตรงเวลาเสร็จสิ้น (0 Tokens)</i>"
                requests.post(f"https://api.telegram.org/bot{bot_token}/sendMessage", json={
                    "chat_id": chat_id, "text": msg, "parse_mode": "HTML"
                }, timeout=10)
        except Exception:
            pass
        return f"SUCCESS_PUBLISHED_{eval_id}"
    else:
        print(f"[PREFECT SWEEPER] Failed to publish post {eval_id}: {stderr}")
        return f"FAILED_PUBLISHED_{eval_id}"

if __name__ == "__main__":
    res = auto_publisher_sweeper_flow()
    print("Flow Result:", res)
