import json
import asyncpg
import re

async def verify_script_compliance(script_text: str) -> dict:
    """
    Automated compliance checker against the system_logs.global_configs dictionary.
    """
    conn = await asyncpg.connect(
        user="admin",
        password="YOUR_PASSWORD_HERE",
        database="system_logs",
        host="127.0.0.1",
        port=5432
    )

    config_row = await conn.fetchrow('SELECT config_value FROM global_configs WHERE config_key = $1', 'forbidden_words_th_v1')
    await conn.close()
    
    if not config_row:
        return {"is_safe": False, "error": "Compliance dictionary not found in database."}

    forbidden_dict = json.loads(config_row['config_value'])
    found_violations = []
    script_lower = script_text.lower()

    for category, words in forbidden_dict.items():
        for word in words:
            if re.search(f"{word}", script_lower):
                found_violations.append({
                    "category": category,
                    "word": word
                })

    if found_violations:
        return {
            "is_safe": False,
            "violations": found_violations,
            "message": f"❌ พบคำต้องห้าม {len(found_violations)} จุด กรุณาให้ AI เขียนใหม่"
        }
    
    return {"is_safe": True, "message": "✅ สคริปต์ปลอดภัย ผ่านเกณฑ์กฎหมายและแพลตฟอร์ม"}
