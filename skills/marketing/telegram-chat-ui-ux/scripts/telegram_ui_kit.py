#!/usr/bin/env python3
"""
Telegram Chat UI/UX Kit for Social Media Studio & Approval Gate
Builds mobile-optimized HTML layouts, expandable blockquotes, and 2D inline keyboard matrices.
"""
import sys
import json
import html

def escape_html(text: str) -> str:
    if not text:
        return ""
    return html.escape(str(text))

def build_review_card_payload(eval_data: dict) -> dict:
    """
    Constructs an interactive Telegram Review Card with:
    - Status & Headline
    - Monospace KPI Table
    - Expandable Caption Blockquote
    - Interactive 2D Button Grid
    """
    eval_id = eval_data.get("id", 1)
    headline = escape_html(eval_data.get("headline", "หัวข้อคอนเทนต์"))
    pillar = escape_html(eval_data.get("pillar", "Data Storytelling"))
    score = eval_data.get("score", 100)
    scheduled_at = eval_data.get("scheduled_at", "19:42 น.")
    gdrive_link = eval_data.get("gdrive_link", "https://drive.google.com")
    file_name = escape_html(eval_data.get("file_name", "20261001-0001.png"))
    cost_thb = eval_data.get("cost_thb", 0.0134)
    tokens = eval_data.get("tokens", 2410)
    caption = escape_html(eval_data.get("caption", "ตัวอย่างแคปชัน..."))
    
    # HTML Formatted Text
    msg = []
    msg.append("<b>📊 [คิวคอนเทนต์ใหม่รอการอนุมัติ]</b>")
    msg.append(f"<b>หัวข้อ:</b> {headline}")
    msg.append(f"<b>หมวด:</b> <code>{pillar}</code> | <b>คะแนน:</b> <code>{score}/100</code>")
    msg.append(f"<b>กำหนดเวลาโพสต์:</b> <code>{scheduled_at}</code> (สุ่มเป็นธรรมชาติ)")
    msg.append(f"<b>ไฟล์ภาพ:</b> <code>{file_name}</code>")
    msg.append("")
    
    # Monospace Financial / Telemetry Card
    msg.append("<b>── ข้อมูลการผลิต & ต้นทุน AI ──</b>")
    msg.append(f"<code>• โทเค็นทั้งหมด: {tokens:,} tokens</code>")
    msg.append(f"<code>• ต้นทุนค่ารัน: ~{cost_thb:.4f} บาท</code>")
    msg.append("")
    
    # Expandable Caption Blockquote
    msg.append("<b>📝 แคปชันตัวเต็ม (แตะเพื่อย่อ-ขยาย) :</b>")
    msg.append(f"<blockquote expandable>{caption}</blockquote>")
    
    # 2D Inline Keyboard Matrix
    keyboard = [
        # Row 1: Primary Action Buttons
        [
            {"text": "✅ อนุมัติยิงตามเวลา", "callback_data": f"APPROVE_{eval_id}"},
            {"text": "✏️ ขอให้แก้ไข", "callback_data": f"MENU_REVISE_{eval_id}"}
        ],
        # Row 2: Secondary / Resource Links
        [
            {"text": "🖼️ เปิดดูภาพบน Drive", "url": gdrive_link},
            {"text": "❌ ปัดตก / ไม่อนุมัติ", "callback_data": f"REJECT_{eval_id}"}
        ]
    ]
    
    return {
        "text": "\n".join(msg),
        "parse_mode": "HTML",
        "reply_markup": {"inline_keyboard": keyboard}
    }

def build_revision_menu_payload(eval_id: int) -> dict:
    """Sub-menu when user taps '✏️ ขอให้แก้ไข'."""
    text = (
        "<b>✏️ เมนูผ่าตัดแก้ไขด่วน (Surgical Revision) :</b>\n"
        "คุณสตางค์ต้องการให้ปรับปรุงส่วนไหนเป็นพิเศษครับ?\n\n"
        "<i>แตะตัวเลือกด้านล่าง AI จะปรับให้เฉพาะจุดทันทีใน 3 วินาที :</i>"
    )
    keyboard = [
        [
            {"text": "🎣 1. ปรับ Hook ให้กระตุกต่อมสงสัย", "callback_data": f"REV_HOOK_{eval_id}"}
        ],
        [
            {"text": "✂️ 2. ตัดแคปชันให้สั้นกระชับลงอีก", "callback_data": f"REV_SHORTEN_{eval_id}"}
        ],
        [
            {"text": "🎨 3. ปรับขนาดตัวเลข / สีในภาพ", "callback_data": f"REV_IMAGE_{eval_id}"}
        ],
        [
            {"text": "🎙️ 4. พิมพ์หรือส่งเสียงสั่งเอง", "callback_data": f"REV_CUSTOM_{eval_id}"}
        ],
        [
            {"text": "🔙 ยกเลิก (กลับไปหน้าเดิม)", "callback_data": f"CANCEL_REV_{eval_id}"}
        ]
    ]
    return {
        "text": text,
        "parse_mode": "HTML",
        "reply_markup": {"inline_keyboard": keyboard}
    }

def build_approved_card_payload(eval_id: int, headline: str, scheduled_at: str, user_name="คุณสตางค์") -> dict:
    """In-place updated card after user approves."""
    text = (
        f"<b>✅ อนุมัติการเผยแพร่เรียบร้อยแล้ว</b>\n\n"
        f"<b>หัวข้อ:</b> {escape_html(headline)}\n"
        f"<b>กำหนดการ:</b> <code>{scheduled_at}</code>\n"
        f"<b>ผู้อนุมัติ:</b> <code>{escape_html(user_name)}</code>\n\n"
        f"<i>ระบบ Python Prefect จะดำเนินการยิงโพสต์ขึ้น Facebook Feed ตามเวลาให้อัตโนมัติ (0 Tokens)</i>"
    )
    return {
        "text": text,
        "parse_mode": "HTML",
        "reply_markup": {"inline_keyboard": []}  # Buttons removed once approved
    }

if __name__ == "__main__":
    sample_data = {
        "id": 2,
        "headline": "เปลี่ยนเงินซื้อหวย มาลุย 'กองทุนรวม' สู่เงินแสน",
        "pillar": "What-If Simulation",
        "score": 100,
        "scheduled_at": "19:42:15 น.",
        "file_name": "20261001-0001.png",
        "tokens": 2410,
        "cost_thb": 0.0136,
        "gdrive_link": "https://drive.google.com/file/d/1imOqJTDg5MiWYzWMi2fZDZ_yFjtVSFtb/view",
        "caption": "เคยสงสัยไหมครับ... ถ้าเราเปลี่ยนเงินที่ 'ซื้อหวยงวดละ 500 บาท' ตลอด 10 ปี ไปสะสมในกองทุนรวม วันนี้พอร์ตเราจะโตไปอยู่ที่เท่าไหร่?\n\nเงินต้น 120,000 บาทเท่ากัน แต่ปลายทางต่างกันถึง 279,734 บาท!\n\n#SatangTheValue #เล่าDATA"
    }
    
    payload = build_review_card_payload(sample_data)
    print("=== TELEGRAM UI/UX REVIEW CARD VALIDATION ===")
    print("Length:", len(payload["text"]))
    print(payload["text"])
    print("\nInline Keyboard Rows:", len(payload["reply_markup"]["inline_keyboard"]))
    print("Valid JSON:", json.dumps(payload, ensure_ascii=False)[:120], "...")
