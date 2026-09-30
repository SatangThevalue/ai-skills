#!/usr/bin/env python3
"""
Meta Graph API Publisher & Job Execution Engine
"""
import os
import sys
import json
import time
import requests
import subprocess
from datetime import datetime

DB_CMD = ['docker', 'exec', '-i', 'satang-vault-db', 'psql', '-U', 'admin', '-d', 'media_studio']

def run_db_query(sql):
    cmd = DB_CMD + ['-c', sql]
    res = subprocess.run(cmd, capture_output=True, text=True)
    return res.returncode == 0, res.stdout.strip(), res.stderr.strip()

def get_page_credentials(page_id):
    sql = f"SELECT app_id, page_access_token_encrypted, is_valid, expires_at FROM page_credentials WHERE page_id = {page_id} AND is_valid = TRUE LIMIT 1;"
    ok, out, _ = run_db_query(sql)
    lines = [l.strip() for l in out.split('\n') if l.strip() and not l.startswith('-') and not l.startswith('app_id') and not l.startswith('(')]
    if lines:
        parts = [p.strip() for p in lines[0].split('|')]
        return {
            "app_id": parts[0],
            "access_token": parts[1] if len(parts) > 1 else None,
            "is_valid": parts[2] == 't' if len(parts) > 2 else False,
            "expires_at": parts[3] if len(parts) > 3 else None
        }
    return None

def publish_facebook_post(evaluation_id, dry_run=False):
    sql_eval = f"""
    SELECT e.id, e.page_id, m.fb_page_id, m.page_name, e.headline, e.caption, e.pinned_comment, e.image_path, e.is_approved, e.total_tokens, e.estimated_cost_usd
    FROM facebook_content_evaluations e
    JOIN managed_pages m ON e.page_id = m.id
    WHERE e.id = {evaluation_id};
    """
    ok, out, err = run_db_query(sql_eval)
    if not ok or "1 row" not in out:
        print(f"[ERROR] Evaluation ID {evaluation_id} not found: {err}")
        return False

    lines = [l.strip() for l in out.split('\n') if l.strip() and not l.startswith('-') and not l.startswith('id') and not l.startswith('(')]
    if not lines:
        return False
        
    parts = [p.strip() for p in lines[0].split('|')]
    eval_id = int(parts[0])
    page_id = int(parts[1])
    fb_page_id = parts[2]
    page_name = parts[3]
    headline = parts[4]
    caption = parts[5]
    pinned_comment = parts[6]
    image_path = parts[7]
    is_approved = parts[8] == 't'
    total_tokens = int(parts[9])
    estimated_cost_usd = float(parts[10])

    if not is_approved:
        print(f"[GATE REJECTION] Post ID {eval_id} is NOT approved. Publishing blocked.")
        return False

    sql_job_start = f"""
    INSERT INTO publishing_jobs (evaluation_id, page_id, status, graph_api_endpoint)
    VALUES ({eval_id}, {page_id}, 'RUNNING', 'https://graph.facebook.com/v19.0/{fb_page_id}/photos')
    RETURNING id;
    """
    ok, job_out, _ = run_db_query(sql_job_start)
    job_id = 1
    for l in job_out.split('\n'):
        if l.strip().isdigit():
            job_id = int(l.strip())
            break

    creds = get_page_credentials(page_id)
    token = creds.get("access_token") if creds else None

    if not token or dry_run or token == "MOCK_TOKEN":
        time.sleep(1.0)
        simulated_post_id = f"{fb_page_id}_mock_{int(time.time())}"
        payload_record = {
            "status": "SUCCESS_SIMULATED",
            "fb_post_id": simulated_post_id,
            "timestamp": datetime.utcnow().isoformat()
        }
        sql_job_finish = f"""
        UPDATE publishing_jobs SET
            status = 'COMPLETED_SIMULATED',
            executed_at = NOW(),
            response_payload = '{json.dumps(payload_record)}'::jsonb
        WHERE id = {job_id};
        UPDATE facebook_content_evaluations SET
            published_status = 'PUBLISHED_SIMULATED',
            fb_post_id = '{simulated_post_id}',
            published_at = NOW()
        WHERE id = {eval_id};
        INSERT INTO token_ledger (
            page_id, evaluation_id, model_name, prompt_tokens, completion_tokens,
            total_tokens, cost_usd, cost_thb, billing_cycle
        ) VALUES (
            {page_id}, {eval_id}, 'gemini-2.5-flash', 1490, 920,
            {total_tokens}, {estimated_cost_usd}, {round(estimated_cost_usd * 35.0, 4)},
            to_char(NOW(), 'YYYY-MM')
        );
        """
        run_db_query(sql_job_finish)
        print(f"[SUCCESS] Post processed! Simulated Post ID: {simulated_post_id}")
        return True

    # Live Meta Graph API
    url_photos = f"https://graph.facebook.com/v19.0/{fb_page_id}/photos"
    headers = {"Authorization": f"Bearer {token}"}
    try:
        with open(image_path, "rb") as img_file:
            files = {"source": img_file}
            data = {"caption": caption, "published": "true"}
            resp = requests.post(url_photos, headers=headers, data=data, files=files, timeout=30)
            res_json = resp.json()

        if "id" not in res_json:
            raise Exception(f"Upload Failed: {res_json}")

        live_post_id = res_json.get("post_id", res_json.get("id"))
        if pinned_comment:
            requests.post(f"https://graph.facebook.com/v19.0/{live_post_id}/comments",
                          headers=headers, data={"message": pinned_comment}, timeout=15)

        sql_live_success = f"""
        UPDATE publishing_jobs SET status = 'COMPLETED', executed_at = NOW(), response_payload = '{json.dumps(res_json)}'::jsonb WHERE id = {job_id};
        UPDATE facebook_content_evaluations SET published_status = 'PUBLISHED', fb_post_id = '{live_post_id}', published_at = NOW() WHERE id = {eval_id};
        INSERT INTO token_ledger (page_id, evaluation_id, model_name, prompt_tokens, completion_tokens, total_tokens, cost_usd, cost_thb, billing_cycle)
        VALUES ({page_id}, {eval_id}, 'gemini-2.5-flash', 1490, 920, {total_tokens}, {estimated_cost_usd}, {round(estimated_cost_usd * 35.0, 4)}, to_char(NOW(), 'YYYY-MM'));
        """
        run_db_query(sql_live_success)
        return True
    except Exception as e:
        err_msg = str(e).replace("'", "''")
        run_db_query(f"UPDATE publishing_jobs SET status = 'FAILED', error_message = '{err_msg}' WHERE id = {job_id};")
        return False

if __name__ == "__main__":
    eval_id = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    publish_facebook_post(eval_id, dry_run=True)
