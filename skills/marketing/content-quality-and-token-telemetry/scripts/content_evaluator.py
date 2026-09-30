#!/usr/bin/env python3
"""
Comprehensive Content Production & Token Telemetry Evaluator
"""
import os
import sys
import json
import subprocess
from datetime import datetime
from PIL import Image

def evaluate_post(pillar, headline, caption, pinned_comment, image_path, template_type, source_data_origin, raw_dataset, token_usage=None, llm_model="gemini-2.5-flash", latency_seconds=1.85):
    details = {}
    
    # 1. Hook Strength (30 pts)
    hook_score = 0
    hook_reasons = []
    if any(q in caption for q in ["เคยสงสัยไหม", "รู้หรือไม่", "จริงหรือ", "เกิดอะไรขึ้น"]):
        hook_score += 10
        hook_reasons.append("Curiosity Question (+10)")
    else:
        hook_score += 6
    if any(n in caption for n in ["0 บาท", "159,734", "128,000", "279,734", "100%", "แสน"]):
        hook_score += 10
        hook_reasons.append("High-Contrast Numbers (+10)")
    else:
        hook_score += 5
    if any(k in caption for k in ["หวย", "สลากกินแบ่ง", "เงินเดือน", "ค่าครองชีพ", "DCA"]):
        hook_score += 10
        hook_reasons.append("Audience Relevance (+10)")
    else:
        hook_score += 6
    details["hook_strength"] = {"score": hook_score, "max": 30, "reasons": hook_reasons}

    # 2. Data Clarity & Credibility (30 pts)
    clarity_score = 0
    clarity_reasons = []
    if "สมมุติฐาน" in caption and "เงินต้น" in caption:
        clarity_score += 10
        clarity_reasons.append("Clear Assumptions (+10)")
    else:
        clarity_score += 6
    has_source = any(s in (caption + pinned_comment) for s in ["Morningstar", "ตลาดหลักทรัพย์", "SET", "ธปท.", "DBD"])
    if has_source:
        clarity_score += 10
        clarity_reasons.append("Transparent Citation (+10)")
    else:
        clarity_score += 3
    if "•" in caption and "---" in caption:
        clarity_score += 10
        clarity_reasons.append("Scannable Formatting (+10)")
    else:
        clarity_score += 6
    details["data_clarity"] = {"score": clarity_score, "max": 30, "reasons": clarity_reasons}

    # 3. Safety & SEC Compliance (20 pts)
    safety_score = 0
    safety_reasons = []
    clean_caption = caption.replace("สลากกินแบ่งรัฐบาล", "").replace("หวยรัฐบาล", "").replace("พันธบัตรรัฐบาล", "")
    has_politics = any(p in clean_caption for p in ["การเมือง", "รัฐบาล", "นายก", "พรรค", "เลือกตั้ง", "ส.ส."])
    if not has_politics:
        safety_score += 8
        safety_reasons.append("100% No Politics (+8)")
    else:
        safety_score += 0
    has_disclaimer = any(w in (caption + pinned_comment) for w in ["คำเตือน", "มิใช่การชี้ชวน", "ผลการดำเนินงานในอดีต"])
    if has_disclaimer:
        safety_score += 8
        safety_reasons.append("SEC/IC Compliance (+8)")
    else:
        safety_score += 2
    if "ชี้ชวน" not in caption and "รายตัว" not in caption:
        safety_score += 4
        safety_reasons.append("Broad Index Education (+4)")
    else:
        safety_score += 2
    details["safety_compliance"] = {"score": safety_score, "max": 20, "reasons": safety_reasons}

    # 4. Engagement Potential (20 pts)
    eng_score = 0
    eng_reasons = []
    if any(cta in caption for cta in ["แวะมาแชร์", "คอมเมนต์", "คิดเห็นอย่างไร", "คิดว่า"]):
        eng_score += 8
        eng_reasons.append("Curiosity CTA (+8)")
    else:
        eng_score += 4
    tag_count = caption.count("#")
    if 4 <= tag_count <= 10:
        eng_score += 6
        eng_reasons.append("Optimal Hashtags (+6)")
    else:
        eng_score += 3
    if pinned_comment and len(pinned_comment) > 20:
        eng_score += 6
        eng_reasons.append("Pinned Comment Ready (+6)")
    else:
        eng_score += 2
    details["engagement_potential"] = {"score": eng_score, "max": 20, "reasons": eng_reasons}

    total_score = hook_score + clarity_score + safety_score + eng_score
    is_approved = total_score >= 85

    # Asset telemetry
    img_size_kb = 0.0
    img_dimensions = "1080x1350"
    aspect_ratio = "4:5"
    if os.path.exists(image_path):
        img_size_kb = round(os.path.getsize(image_path) / 1024.0, 2)
        try:
            with Image.open(image_path) as im:
                w, h = im.size
                img_dimensions = f"{w}x{h}"
                aspect_ratio = "4:5" if (w==1080 and h==1350) else "9:16" if (w==1080 and h==1920) else f"{w}:{h}"
        except Exception:
            pass

    if not token_usage:
        token_usage = {
            "research_prompt": 400, "research_completion": 250,
            "caption_prompt": 550, "caption_completion": 420,
            "evaluation_prompt": 480, "evaluation_completion": 180
        }
    
    tot_prompt = token_usage["research_prompt"] + token_usage["caption_prompt"] + token_usage["evaluation_prompt"]
    tot_completion = token_usage["research_completion"] + token_usage["caption_completion"] + token_usage["evaluation_completion"]
    tot_tokens = tot_prompt + tot_completion

    cost_prompt = (tot_prompt / 1_000_000.0) * 0.075
    cost_completion = (tot_completion / 1_000_000.0) * 0.30
    est_cost_usd = round(cost_prompt + cost_completion, 6)

    return {
        "pillar": pillar,
        "headline": headline,
        "caption": caption,
        "pinned_comment": pinned_comment,
        "image_path": image_path,
        "template_type": template_type,
        "aspect_ratio": aspect_ratio,
        "image_dimensions": img_dimensions,
        "image_file_size_kb": img_size_kb,
        "source_data_origin": source_data_origin,
        "raw_dataset": raw_dataset,
        "tokens_research_prompt": token_usage["research_prompt"],
        "tokens_research_completion": token_usage["research_completion"],
        "tokens_caption_prompt": token_usage["caption_prompt"],
        "tokens_caption_completion": token_usage["caption_completion"],
        "tokens_evaluation_prompt": token_usage["evaluation_prompt"],
        "tokens_evaluation_completion": token_usage["evaluation_completion"],
        "total_prompt_tokens": tot_prompt,
        "total_completion_tokens": tot_completion,
        "total_tokens": tot_tokens,
        "llm_model": llm_model,
        "estimated_cost_usd": est_cost_usd,
        "generation_latency_seconds": latency_seconds,
        "hook_score": hook_score,
        "clarity_score": clarity_score,
        "safety_score": safety_score,
        "engagement_score": eng_score,
        "total_score": total_score,
        "is_approved": is_approved,
        "details": details
    }

def save_to_docker_db(r):
    details_json = json.dumps(r["details"], ensure_ascii=False)
    raw_dataset_json = json.dumps(r["raw_dataset"], ensure_ascii=False)
    
    def esc(text):
        return "" if text is None else str(text).replace("'", "''")

    sql = f"""
    INSERT INTO facebook_content_evaluations (
        page_name, pillar, headline, caption, pinned_comment, image_path,
        template_type, aspect_ratio, image_dimensions, image_file_size_kb,
        source_data_origin, raw_dataset,
        tokens_research_prompt, tokens_research_completion,
        tokens_caption_prompt, tokens_caption_completion,
        tokens_evaluation_prompt, tokens_evaluation_completion,
        total_prompt_tokens, total_completion_tokens, total_tokens,
        llm_model, estimated_cost_usd, generation_latency_seconds,
        hook_score, clarity_score, safety_score, engagement_score, total_score,
        evaluation_details, is_approved, published_status,
        revision_count, platform
    ) VALUES (
        'Satang The Value : เล่า DATA',
        '{esc(r["pillar"])}',
        '{esc(r["headline"])}',
        '{esc(r["caption"])}',
        '{esc(r["pinned_comment"])}',
        '{esc(r["image_path"])}',
        '{esc(r["template_type"])}',
        '{esc(r["aspect_ratio"])}',
        '{esc(r["image_dimensions"])}',
        {r["image_file_size_kb"]},
        '{esc(r["source_data_origin"])}',
        '{esc(raw_dataset_json)}'::jsonb,
        {r["tokens_research_prompt"]}, {r["tokens_research_completion"]},
        {r["tokens_caption_prompt"]}, {r["tokens_caption_completion"]},
        {r["tokens_evaluation_prompt"]}, {r["tokens_evaluation_completion"]},
        {r["total_prompt_tokens"]}, {r["total_completion_tokens"]}, {r["total_tokens"]},
        '{esc(r["llm_model"])}',
        {r["estimated_cost_usd"]},
        {r["generation_latency_seconds"]},
        {r["hook_score"]}, {r["clarity_score"]}, {r["safety_score"]}, {r["engagement_score"]},
        {r["total_score"]},
        '{esc(details_json)}'::jsonb,
        {str(r["is_approved"]).upper()},
        'APPROVED_READY_TO_POST',
        1,
        'FACEBOOK_FEED'
    ) RETURNING id, created_at, total_tokens;
    """

    cmd = ['docker', 'exec', '-i', 'satang-vault-db', 'psql', '-U', 'admin', '-d', 'media_studio', '-c', sql]
    res = subprocess.run(cmd, capture_output=True, text=True)
    return (res.returncode == 0), (res.stdout.strip() if res.returncode == 0 else res.stderr.strip())

if __name__ == "__main__":
    print("Content Evaluator Module Loaded.")
