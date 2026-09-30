#!/usr/bin/env python3
"""
Render Template G: 'What-If Simulation' - Concise & Zero Overflow Edition.
Strict formatting:
- Short, tight, punchy copy (easy to read in 2 seconds)
- Guaranteed zero text overflow across all boxes
- 2-Column Side-by-Side (SET layout) + Dark-Tech Satang The Value CI
- 100% SEC (IC P1) Compliance Disclaimer
Dimensions: 1080 x 1350 (4:5 Aspect Ratio for Facebook Mobile).
Font: Prompt (Google Fonts OFL).
"""
import os
import math
from PIL import Image, ImageDraw, ImageFont

def draw_4point_star(draw, cx, cy, r_outer, r_inner, fill_color, glow=True):
    if glow:
        glow_r = int(r_outer * 1.8)
        draw.line([(cx - glow_r, cy), (cx + glow_r, cy)], fill="#1E3868", width=1)
        draw.line([(cx, cy - glow_r), (cx, cy + glow_r)], fill="#1E3868", width=1)

    points = []
    for i in range(8):
        angle = i * (math.pi / 4.0) - (math.pi / 2.0)
        radius = r_outer if i % 2 == 0 else r_inner
        px = cx + radius * math.cos(angle)
        py = cy + radius * math.sin(angle)
        points.append((px, py))
    draw.polygon(points, fill=fill_color)

def draw_down_arrow(draw, x, y, size, fill):
    w = size // 3
    draw.rectangle([x - w//2, y - size//2, x + w//2, y + size//6], fill=fill)
    draw.polygon([
        (x - size//2, y + size//6),
        (x + size//2, y + size//6),
        (x, y + size//2)
    ], fill=fill)

def draw_up_arrow(draw, x, y, size, fill):
    w = size // 3
    draw.rectangle([x - w//2, y - size//6, x + w//2, y + size//2], fill=fill)
    draw.polygon([
        (x - size//2, y - size//6),
        (x + size//2, y - size//6),
        (x, y - size//2)
    ], fill=fill)

def create_concise_template(output_path="/home/thaieasyvps/satang_template_g_concise.png"):
    width, height = 1080, 1350
    img = Image.new("RGB", (width, height), color="#070D1F")
    draw = ImageDraw.Draw(img)

    glow_overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_overlay)
    
    for r in range(400, 80, -30):
        alpha = int(7 * (1.0 - (r / 400.0)))
        glow_draw.ellipse([280 - r, 580 - r, 280 + r, 580 + r], fill=(239, 68, 68, alpha))
        
    for r in range(400, 80, -30):
        alpha = int(8 * (1.0 - (r / 400.0)))
        glow_draw.ellipse([800 - r, 580 - r, 800 + r, 580 + r], fill=(0, 230, 118, alpha))

    for r in range(350, 70, -25):
        alpha = int(7 * (1.0 - (r / 350.0)))
        glow_draw.ellipse([width - 120 - r, 100 - r, width - 120 + r, 100 + r], fill=(245, 166, 35, alpha))

    img = Image.alpha_composite(img.convert("RGBA"), glow_overlay).convert("RGB")
    draw = ImageDraw.Draw(img)

    gold = "#F5A623"
    gold_light = "#FDE68A"
    cyan = "#38BDF8"
    
    draw_4point_star(draw, width - 90, 115, r_outer=26, r_inner=6, fill_color=gold, glow=True)
    draw_4point_star(draw, width - 90, 115, r_outer=12, r_inner=3, fill_color=gold_light, glow=False)
    draw_4point_star(draw, width - 210, 70, r_outer=15, r_inner=4, fill_color=cyan, glow=True)
    draw_4point_star(draw, 45, 110, r_outer=13, r_inner=3, fill_color=gold, glow=False)

    font_dir = "/home/thaieasyvps/.fonts/Prompt"
    fb = os.path.join(font_dir, "Prompt-Bold.ttf")
    fsb = os.path.join(font_dir, "Prompt-SemiBold.ttf")
    fm = os.path.join(font_dir, "Prompt-Medium.ttf")
    fr = os.path.join(font_dir, "Prompt-Regular.ttf")

    f_badge = ImageFont.truetype(fb, 22)
    f_cat = ImageFont.truetype(fsb, 22)
    f_title = ImageFont.truetype(fb, 45)
    f_subtitle = ImageFont.truetype(fr, 23)
    
    f_col_head = ImageFont.truetype(fb, 25)
    f_col_sub = ImageFont.truetype(fm, 21)
    f_bullet = ImageFont.truetype(fr, 20)
    
    f_badge_pill = ImageFont.truetype(fb, 21)
    f_giant_num = ImageFont.truetype(fb, 48)
    f_unit = ImageFont.truetype(fb, 26)
    f_note = ImageFont.truetype(fr, 18)
    f_box_tag = ImageFont.truetype(fb, 17)
    f_box_txt = ImageFont.truetype(fr, 17)
    
    f_vs = ImageFont.truetype(fb, 24)
    f_summary_title = ImageFont.truetype(fb, 25)
    f_summary_body = ImageFont.truetype(fr, 21)
    f_warn_head = ImageFont.truetype(fb, 17)
    f_warn_body = ImageFont.truetype(fr, 16)
    f_footer = ImageFont.truetype(fr, 18)

    for i in range(5):
        draw.line([(0, i), (width, i)], fill="#F5A623", width=1)

    icon_path = "/home/thaieasyvps/satang_the_value_icon_only.png"
    if os.path.exists(icon_path):
        icon = Image.open(icon_path).convert("RGBA").resize((52, 52), Image.Resampling.LANCZOS)
        mask = Image.new("L", (52, 52), 0)
        ImageDraw.Draw(mask).rounded_rectangle([0, 0, 51, 51], radius=13, fill=255)
        img.paste(icon, (60, 40), mask)
        draw.rounded_rectangle([59, 39, 113, 93], radius=13, outline="#38BDF8", width=1)

    draw.rounded_rectangle([125, 40, 405, 92], radius=14, fill="#121C3D", outline="#253563", width=2)
    draw.text((142, 51), "SATANG THE VALUE", fill="#FFFFFF", font=f_badge)
    
    draw.rounded_rectangle([418, 40, 542, 92], radius=14, fill="#F5A623")
    draw.text((438, 51), "เล่า DATA", fill="#0A1128", font=f_badge)

    draw.text((60, 108), "WHAT-IF SIMULATION • มิติคู่ขนานการเงินฉบับคนไทย", fill="#F5A623", font=f_cat)
    draw.text((60, 140), "เปลี่ยนเงินซื้อหวย มาลุย 'กองทุนรวม' สู่เงินแสน", fill="#FFFFFF", font=f_title)
    draw.text((60, 202), "สมมุติฐานคนไทย: งวดละ 500 บ. (เดือนละ 1,000.-) สะสม 10 ปี = เงินต้น 120,000 บาท", fill="#A0AEC0", font=f_subtitle)

    col_w = 465
    col_h = 675
    col_y = 250
    left_x = 60
    right_x = 555

    # Left: Lottery
    draw.rounded_rectangle([left_x, col_y, left_x + col_w, col_y + col_h], radius=22, fill="#12162B", outline="#2D1D2C", width=2)
    draw.rounded_rectangle([left_x, col_y, left_x + col_w, col_y + 6], radius=3, fill="#EF4444")
    draw.rounded_rectangle([left_x + 25, col_y + 20, left_x + 215, col_y + 58], radius=8, fill="#2C161D")
    draw.text((left_x + 42, col_y + 25), "ซื้อหวยรัฐบาล", fill="#FF6B6B", font=f_col_head)
    draw.text((left_x + 25, col_y + 72), "ลุ้นโชค 2 งวด/เดือน (งวดละ 500.-)", fill="#94A3B8", font=f_col_sub)
    draw.line([(left_x + 25, col_y + 108), (left_x + col_w - 25, col_y + 108)], fill="#202138", width=1)

    steps_left = [
        ("•", "ซื้องวดละ 500.- (เดือนละ 1,000.-)", "#CBD5E1"),
        ("•", "ซื้อสะสม 1 ปี  =  เสียเงิน 12,000 ฿", "#CBD5E1"),
        ("•", "สะสมครบ 10 ปี =  เงินต้น 120,000 ฿", "#FFFFFF"),
        ("•", "โอกาสถูกรางวัลที่ 1 : 0.0001%", "#64748B"),
    ]
    sy = col_y + 128
    for bullet, text, col in steps_left:
        draw.text((left_x + 30, sy), f"{bullet} {text}", fill=col, font=f_bullet)
        sy += 38

    arrow_box_y = col_y + 325
    draw.rounded_rectangle([left_x + 25, arrow_box_y, left_x + col_w - 25, arrow_box_y + 50], radius=10, fill="#281419")
    draw_down_arrow(draw, left_x + 55, arrow_box_y + 25, size=20, fill="#FF4444")
    draw.text((left_x + 78, arrow_box_y + 11), "โอกาสชวดรางวัลสะสม 99.99%", fill="#FF6B6B", font=f_badge_pill)

    val_box_y = col_y + 395
    draw.rounded_rectangle([left_x + 25, val_box_y, left_x + col_w - 25, val_box_y + 140], radius=14, fill="#1B1320", outline="#EF4444", width=1)
    draw.text((left_x + 45, val_box_y + 16), "มูลค่าคงเหลือในมือ :", fill="#94A3B8", font=f_col_sub)
    draw.text((left_x + 45, val_box_y + 54), "- 120,000", fill="#FF4444", font=f_giant_num)
    draw.text((left_x + 305, val_box_y + 72), "บาท", fill="#FF6B6B", font=f_unit)
    draw.text((left_x + 45, val_box_y + 106), "ขาดทุน 100% (เหลือกองสลาก 240 ใบ)", fill="#8392A5", font=f_note)

    draw.rounded_rectangle([left_x + 25, col_y + 555, left_x + col_w - 25, col_y + col_h - 20], radius=10, fill="#181525")
    draw.text((left_x + 40, col_y + 568), "ความเป็นจริงของการลุ้นโชค :", fill="#F5A623", font=f_box_tag)
    draw.text((left_x + 40, col_y + 600), "• ซื้อความตื่นเต้น แต่เงินต้นหาย 100%", fill="#CBD5E1", font=f_box_txt)
    draw.text((left_x + 40, col_y + 626), "• ไม่เกิดพลังดอกเบี้ยทบต้นใดๆ ทั้งสิ้น", fill="#94A3B8", font=f_box_txt)

    # Right: Mutual Fund
    draw.rounded_rectangle([right_x, col_y, right_x + col_w, col_y + col_h], radius=22, fill="#0F1F2B", outline="#163830", width=2)
    draw.rounded_rectangle([right_x, col_y, right_x + col_w, col_y + 6], radius=3, fill="#00E676")
    draw_4point_star(draw, right_x + col_w - 35, col_y + 35, r_outer=12, r_inner=3, fill_color="#00E676", glow=False)

    draw.rounded_rectangle([right_x + 25, col_y + 20, right_x + 225, col_y + 58], radius=8, fill="#123828")
    draw.text((right_x + 42, col_y + 25), "ลงทุนกองทุนรวม", fill="#00E676", font=f_col_head)
    draw.text((right_x + 25, col_y + 72), "ออมเดือนละ 1,000.- (DCA สม่ำเสมอ)", fill="#94A3B8", font=f_col_sub)
    draw.line([(right_x + 25, col_y + 108), (right_x + col_w - 25, col_y + 108)], fill="#173534", width=1)

    steps_right = [
        ("•", "ทยอยออมเดือนละ 1,000.- สม่ำเสมอ", "#CBD5E1"),
        ("•", "สะสมครบ 10 ปี =  เงินต้น 120,000 ฿", "#FFFFFF"),
        ("•", "ผลตอบแทนเฉลี่ยคาดการณ์ ~5.14%/ปี", "#38BDF8"),
        ("•", "พลังดอกเบี้ยทบต้นทำงานแทนเรา", "#00E676"),
    ]
    sy = col_y + 128
    for bullet, text, col in steps_right:
        draw.text((right_x + 30, sy), f"{bullet} {text}", fill=col, font=f_bullet)
        sy += 38

    draw.rounded_rectangle([right_x + 25, arrow_box_y, right_x + col_w - 25, arrow_box_y + 50], radius=10, fill="#103328")
    draw_up_arrow(draw, right_x + 55, arrow_box_y + 25, size=20, fill="#00E676")
    draw.text((right_x + 78, arrow_box_y + 11), "ผลตอบแทนเฉลี่ยคาดการณ์ 5.14%", fill="#00E676", font=f_badge_pill)

    draw.rounded_rectangle([right_x + 25, val_box_y, right_x + col_w - 25, val_box_y + 140], radius=14, fill="#0E2B25", outline="#00E676", width=2)
    draw.text((right_x + 45, val_box_y + 16), "มูลค่าพอร์ตปลายทาง :", fill="#38BDF8", font=f_col_sub)
    draw.text((right_x + 45, val_box_y + 54), "+ 159,734", fill="#00E676", font=f_giant_num)
    draw.text((right_x + 305, val_box_y + 72), "บาท", fill="#A7F3D0", font=f_unit)
    draw.text((right_x + 45, val_box_y + 106), "เงินต้น 120,000 + กำไร 39,734 ฿", fill="#A7F3D0", font=f_note)

    draw.rounded_rectangle([right_x + 25, col_y + 555, right_x + col_w - 25, col_y + col_h - 20], radius=10, fill="#122A26", outline="#205040", width=1)
    draw.text((right_x + 40, col_y + 568), "ตัวอย่างกองทุนยอดฮิตสำหรับ DCA :", fill="#F5A623", font=f_box_tag)
    draw.text((right_x + 40, col_y + 600), "• กองทุนดัชนี SET50 / หุ้นโลก S&P 500", fill="#CBD5E1", font=f_box_txt)
    draw.text((right_x + 40, col_y + 626), "• เน้นกลุ่ม Passive ค่าธรรมเนียมต่ำ < 0.5%/ปี", fill="#86EFAC", font=f_box_txt)

    # VS badge
    vs_cx = width // 2
    vs_cy = col_y + 380
    draw.ellipse([vs_cx - 34, vs_cy - 34, vs_cx + 34, vs_cy + 34], fill="#0A132C", outline="#F5A623", width=2)
    draw.text((vs_cx - 15, vs_cy - 17), "VS", fill="#F5A623", font=f_vs)

    # Bottom Summary
    bot_y0 = 945
    bot_y1 = 1150
    draw.rounded_rectangle([60, bot_y0, 1020, bot_y1], radius=18, fill="#111D3E", outline="#38BDF8", width=2)
    draw.rectangle([60, bot_y0, 72, bot_y1], fill="#F5A623")
    draw.text((95, bot_y0 + 16), "สรุปบทเรียนสำคัญของมิติคู่ขนาน 10 ปี :", fill="#F5A623", font=f_summary_title)
    draw.text((95, bot_y0 + 52), "เงินต้น 120,000 บาทเท่ากัน แต่ปลายทางต่างกันถึง 279,734 บาท!", fill="#FFFFFF", font=f_summary_title)
    draw.line([(95, bot_y0 + 92), (985, bot_y0 + 92)], fill="#1D2E5C", width=1)
    draw.text((95, bot_y0 + 106), "• ไม่ได้ห้ามซื้อหวย แต่ถ้าแบ่งงวดละ 500.- มาออมกองทุน จะสร้างเงินแสนแรกได้ชัวร์", fill="#CBD5E1", font=f_summary_body)
    draw.text((95, bot_y0 + 138), "• เริ่มต้นง่าย ใช้เงินน้อย ซื้อผ่านแอปธนาคารได้ทุกที่ เริ่มต้นเพียง 1 บาท", fill="#A7F3D0", font=f_summary_body)
    draw.text((95, bot_y0 + 170), "• พลังดอกเบี้ยทบต้น (DCA) จะเปลี่ยนเศษเงินเล็กๆ ให้กลายเป็นเงินก้อนใหญ่", fill="#94A3B8", font=f_summary_body)

    # SEC Disclaimer
    dis_y0 = 1165
    dis_y1 = 1275
    draw.rounded_rectangle([60, dis_y0, 1020, dis_y1], radius=12, fill="#0C1428", outline="#1F2E52", width=1)
    draw.rectangle([60, dis_y0, 68, dis_y1], fill="#EAB308")
    draw.text((85, dis_y0 + 12), "⚠️ คำเตือน ก.ล.ต. (Compliance) : เพื่อการศึกษาเชิงสถิติเท่านั้น มิใช่การชักชวนหรือชี้ชวนลงทุน", fill="#FDE047", font=f_warn_head)
    draw.text((85, dis_y0 + 40), "• ผู้ลงทุนควรทำความเข้าใจลักษณะสินค้า เงื่อนไขผลตอบแทน และความเสี่ยงก่อนตัดสินใจลงทุน", fill="#94A3B8", font=f_warn_body)
    draw.text((85, dis_y0 + 68), "• ผลการดำเนินงานในอดีตมิได้เป็นสิ่งยืนยันถึงผลการดำเนินงานในอนาคต", fill="#64748B", font=f_warn_body)

    # Footer
    draw.line([(60, 1290), (1020, 1290)], fill="#1E293B", width=1)
    draw.text((60, 1306), "ข้อมูล: Morningstar Thailand (กองทุนหุ้นไทย 10 ปีย้อนหลัง) & ตลาดหลักทรัพย์ฯ (SET)", fill="#64748B", font=f_footer)
    draw.text((795, 1306), "fb.com/SatangTheValue", fill="#94A3B8", font=f_footer)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path, quality=95)
    print(f"Concise template saved: {output_path}")

if __name__ == "__main__":
    create_concise_template()
