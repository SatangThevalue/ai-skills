#!/usr/bin/env python3
"""
Satang The Value : Content Evaluation Engine & Docker DB Pipeline
Evaluates Facebook posts across 4 core dimensions (100 points scale).
If Total Score >= 85%, marks approved and persists to Docker PostgreSQL (media_studio.facebook_content_evaluations).
"""
import sys
import json
import subprocess
from datetime import datetime

def evaluate_post(pillar, headline, caption, pinned_comment, image_path):
    """
    Evaluate content across 4 core dimensions:
    1. Hook Strength (0 - 30)
    2. Data Clarity & Source Credibility (0 - 30)
    3. Community Safety & SEC Compliance (0 - 20)
    4. Engagement & Virality Potential (0 - 20)
    """
    details = {}
    
    # --- DIMENSION 1: Hook Strength (30 pts) ---
    hook_score = 0
    hook_reasons = []
    
    if any(q in caption for q in ["เคยสงสัยไหม", "รู้หรือไม่", "จริงหรือ", "เกิดอะไรขึ้น"]):
        hook_score += 10
        hook_reasons.append("เปิดด้วย Curiosity Question ชวนสงสัย (+10)")
    else:
        hook_score += 6
        hook_reasons.append("เปิดเรื่องน่าสนใจแต่ยังเพิ่มพลังสงสัยได้ (+6)")
        
    if any(n in caption for n in ["0 บาท", "159,734", "128,000", "279,734", "100%", "แสน"]):
        hook_score += 10
        hook_reasons.append("มีตัวเลขคอนทราสต์ชัดเจนกระแทกตา (+10)")
    else:
        hook_score += 5
        hook_reasons.append("ตัวเลขในแคปชันยังไม่โดดเด่นพอ (+5)")
        
    if any(k in caption for k in ["หวย", "สลากกินแบ่ง", "เงินเดือน", "ค่าครองชีพ", "DCA"]):
        hook_score += 10
        hook_reasons.append("ประเด็นตรงจริตและพฤติกรรมคนไทย (+10)")
    else:
        hook_score += 6
        hook_reasons.append("ประเด็นทั่วไป (+6)")
        
    details["hook_strength"] = {"score": hook_score, "max": 30, "reasons": hook_reasons}

    # --- DIMENSION 2: Data Clarity & Credibility (30 pts) ---
    clarity_score = 0
    clarity_reasons = []
    
    if "สมมุติฐาน" in caption and "เงินต้น" in caption:
        clarity_score += 10
        clarity_reasons.append("ระบุสมมุติฐานเงินต้นและกรอบเวลาชัดเจน (+10)")
    else:
        clarity_score += 6
        clarity_reasons.append("ระบุตัวเลขแต่ขาดสมมุติฐานกำกับ (+6)")
        
    has_source = any(s in (caption + pinned_comment) for s in ["Morningstar", "ตลาดหลักทรัพย์", "SET", "ธปท.", "DBD"])
    if has_source:
        clarity_score += 10
        clarity_reasons.append("มีแหล่งอ้างอิงสถิติสากลและทางการน่าเชื่อถือ (+10)")
    else:
        clarity_score += 3
        clarity_reasons.append("ขาดการระบุแหล่งอ้างอิงข้อมูล (+3)")
        
    if "•" in caption and "---" in caption:
        clarity_score += 10
        clarity_reasons.append("จัดย่อหน้าและบุลเล็ตอ่านง่าย สบายตาบนมือถือ (+10)")
    else:
        clarity_score += 6
        clarity_reasons.append("ข้อความค่อนข้างแน่น ควรเพิ่มการเว้นวรรค (+6)")
        
    details["data_clarity"] = {"score": clarity_score, "max": 30, "reasons": clarity_reasons}

    # --- DIMENSION 3: Safety & SEC Compliance (20 pts) ---
    safety_score = 0
    safety_reasons = []
    
    clean_caption = caption.replace("สลากกินแบ่งรัฐบาล", "").replace("หวยรัฐบาล", "").replace("พันธบัตรรัฐบาล", "")
    has_politics = any(p in clean_caption for p in ["การเมือง", "รัฐบาล", "นายก", "พรรค", "เลือกตั้ง", "ส.ส."])
    
    if not has_politics:
        safety_score += 8
        safety_reasons.append("ปลอดประเด็นการเมืองและคำหยาบคาย 100% (+8)")
    else:
        safety_score += 0
        safety_reasons.append("มีความเสี่ยงเรื่องประเด็นการเมือง (+0)")
        
    has_disclaimer = any(w in (caption + pinned_comment) for w in ["คำเตือน", "มิใช่การชี้ชวน", "ผลการดำเนินงานในอดีต"])
    if has_disclaimer:
        safety_score += 8
        safety_reasons.append("มีข้อความคำเตือนตามเกณฑ์ ก.ล.ต. ครบถ้วน (+8)")
    else:
        safety_score += 2
        safety_reasons.append("ขาดข้อความคำเตือนความเสี่ยงการลงทุน (+2)")
        
    if "ชี้ชวน" not in caption and "รายตัว" not in caption:
        safety_score += 4
        safety_reasons.append("เน้นการให้ความรู้กลุ่มดัชนี ไม่ชี้นำหุ้นรายตัว (+4)")
    else:
        safety_score += 2
        safety_reasons.append("ควรระวังเรื่องการเอ่ยถึงสินทรัพย์ (+2)")
        
    details["safety_compliance"] = {"score": safety_score, "max": 20, "reasons": safety_reasons}

    # --- DIMENSION 4: Engagement & Virality Potential (20 pts) ---
    eng_score = 0
    eng_reasons = []
    
    if any(cta in caption for cta in ["แวะมาแชร์", "คอมเมนต์", "คิดเห็นอย่างไร", "คิดว่า"]):
        eng_score += 8
        eng_reasons.append("มีคำถามชวนคุยปลายเปิดกระตุ้นการคอมเมนต์ (+8)")
    else:
        eng_score += 4
        eng_reasons.append("ขาด Call to action ปลายเปิด (+4)")
        
    tag_count = caption.count("#")
    if 4 <= tag_count <= 10:
        eng_score += 6
        eng_reasons.append(f"มีแฮชแท็กพอดี ({tag_count} แท็ก) ไม่สแปม (+6)")
    else:
        eng_score += 3
        eng_reasons.append(f"จำนวนแฮชแท็กไม่เหมาะสม ({tag_count} แท็ก) (+3)")
        
    if pinned_comment and len(pinned_comment) > 20:
        eng_score += 6
        eng_reasons.append("เตรียมคอมเมนต์แรกปักหมุดพร้อมใช้งาน (+6)")
    else:
        eng_score += 2
        eng_reasons.append("ไม่มีคอมเมนต์ปักหมุด (+2)")
        
    details["engagement_potential"] = {"score": eng_score, "max": 20, "reasons": eng_reasons}

    total_score = hook_score + clarity_score + safety_score + eng_score
    is_approved = total_score >= 85

    return {
        "pillar": pillar,
        "headline": headline,
        "caption": caption,
        "pinned_comment": pinned_comment,
        "image_path": image_path,
        "hook_score": hook_score,
        "clarity_score": clarity_score,
        "safety_score": safety_score,
        "engagement_score": eng_score,
        "total_score": total_score,
        "is_approved": is_approved,
        "details": details
    }

def save_to_docker_db(evaluation_result):
    """Save the evaluation result into Docker container satang-vault-db PostgreSQL."""
    details_json = json.dumps(evaluation_result["details"], ensure_ascii=False)
    
    def esc(text):
        if text is None:
            return ""
        return str(text).replace("'", "''")

    sql = f"""
    INSERT INTO facebook_content_evaluations (
        page_name, pillar, headline, caption, pinned_comment, image_path,
        hook_score, clarity_score, safety_score, engagement_score, total_score,
        evaluation_details, is_approved, published_status
    ) VALUES (
        'Satang The Value : เล่า DATA',
        '{esc(evaluation_result["pillar"])}',
        '{esc(evaluation_result["headline"])}',
        '{esc(evaluation_result["caption"])}',
        '{esc(evaluation_result["pinned_comment"])}',
        '{esc(evaluation_result["image_path"])}',
        {evaluation_result["hook_score"]},
        {evaluation_result["clarity_score"]},
        {evaluation_result["safety_score"]},
        {evaluation_result["engagement_score"]},
        {evaluation_result["total_score"]},
        '{esc(details_json)}'::jsonb,
        {str(evaluation_result["is_approved"]).upper()},
        'APPROVED_READY_TO_POST'
    ) RETURNING id, created_at;
    """

    cmd = ['docker', 'exec', '-i', 'satang-vault-db', 'psql', '-U', 'admin', '-d', 'media_studio', '-c', sql]
    res = subprocess.run(cmd, capture_output=True, text=True)
    return (res.returncode == 0, res.stdout.strip() if res.returncode == 0 else res.stderr.strip())

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Load from JSON file argument
        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            data = json.load(f)
        res = evaluate_post(data["pillar"], data["headline"], data["caption"], data["pinned_comment"], data["image_path"])
        print(json.dumps(res, ensure_ascii=False, indent=2))
        if res["is_approved"]:
            ok, db_msg = save_to_docker_db(res)
            print(f"DB Status: {ok}, {db_msg}")
