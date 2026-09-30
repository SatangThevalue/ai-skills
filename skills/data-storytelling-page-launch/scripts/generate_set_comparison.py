#!/usr/bin/env python3
"""
Generate a Side-by-Side 2-Column Comparison Infographic (SET-Style 1-on-1 What-If).
Aspect ratio: 4:5 (1080 x 1350) for Facebook Mobile Feed.
Features:
- Left Column: Loss / Reality A (Coral Red #EF4444)
- Right Column: Profit / Reality B (Electric Green #00E676)
- Center: Floating 'VS' Badge
- Bottom: Single Consolidated Key Takeaway Card (No English badges, zero collision)
- Visual DNA: Deep Navy canvas, Prompt font, radiant 4-point stars (✦), circuit badges
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
    draw.polygon([(x - size//2, y + size//6), (x + size//2, y + size//6), (x, y + size//2)], fill=fill)

def draw_up_arrow(draw, x, y, size, fill):
    w = size // 3
    draw.rectangle([x - w//2, y - size//6, x + w//2, y + size//2], fill=fill)
    draw.polygon([(x - size//2, y - size//6), (x + size//2, y - size//6), (x, y - size//2)], fill=fill)

def render_set_style_comparison(
    output_path="/tmp/set_comparison.png",
    headline="เปลี่ยนเงินซื้อหวย มาลุย 'กองทุนรวม' สู่เงินแสน",
    subtitle="สมมุติฐานคนไทย: ซื้อหวยงวดละ 500 บาท (เดือนละ 1,000.-) ทยอยสะสม 10 ปี (เงินต้น 120,000 ฿)",
    left_title="ซื้อหวยรัฐบาล",
    left_loss_num="- 120,000",
    right_title="ลงทุนกองทุนรวม",
    right_gain_num="159,734",
    net_diff_num="279,734"
):
    width, height = 1080, 1350
    img = Image.new("RGB", (width, height), color="#070D1F")
    draw = ImageDraw.Draw(img)

    # Ambient Lighting
    glow_overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_overlay)
    for r in range(420, 80, -30):
        alpha = int(7 * (1.0 - (r / 420.0)))
        glow_draw.ellipse([280 - r, 620 - r, 280 + r, 620 + r], fill=(239, 68, 68, alpha))
        glow_draw.ellipse([800 - r, 620 - r, 800 + r, 620 + r], fill=(0, 230, 118, alpha))
    for r in range(350, 70, -25):
        alpha = int(7 * (1.0 - (r / 350.0)))
        glow_draw.ellipse([width - 120 - r, 100 - r, width - 120 + r, 100 + r], fill=(245, 166, 35, alpha))

    img = Image.alpha_composite(img.convert("RGBA"), glow_overlay).convert("RGB")
    draw = ImageDraw.Draw(img)

    # Radiant Stars
    gold = "#F5A623"
    gold_light = "#FDE68A"
    cyan = "#38BDF8"
    draw_4point_star(draw, width - 90, 130, r_outer=28, r_inner=6, fill_color=gold, glow=True)
    draw_4point_star(draw, width - 90, 130, r_outer=13, r_inner=3, fill_color=gold_light, glow=False)
    draw_4point_star(draw, width - 210, 85, r_outer=16, r_inner=4, fill_color=cyan, glow=True)
    draw_4point_star(draw, 45, 125, r_outer=14, r_inner=3, fill_color=gold, glow=False)
    draw_4point_star(draw, width - 45, 960, r_outer=16, r_inner=4, fill_color=gold, glow=False)

    font_dir = "/home/thaieasyvps/.fonts/Prompt"
    fb = os.path.join(font_dir, "Prompt-Bold.ttf")
    fsb = os.path.join(font_dir, "Prompt-SemiBold.ttf")
    fm = os.path.join(font_dir, "Prompt-Medium.ttf")
    fr = os.path.join(font_dir, "Prompt-Regular.ttf")

    f_badge = ImageFont.truetype(fb, 22)
    f_cat = ImageFont.truetype(fsb, 22)
    f_title = ImageFont.truetype(fb, 46)
    f_subtitle = ImageFont.truetype(fr, 24)
    f_col_head = ImageFont.truetype(fb, 26)
    f_col_sub = ImageFont.truetype(fm, 22)
    f_bullet = ImageFont.truetype(fr, 21)
    f_badge_pill = ImageFont.truetype(fb, 22)
    f_giant_num = ImageFont.truetype(fb, 52)
    f_unit = ImageFont.truetype(fb, 28)
    f_note = ImageFont.truetype(fr, 19)
    f_vs = ImageFont.truetype(fb, 24)
    f_summary_title = ImageFont.truetype(fb, 28)
    f_summary_body = ImageFont.truetype(fr, 22)
    f_footer = ImageFont.truetype(fr, 19)

    for i in range(5):
        draw.line([(0, i), (width, i)], fill="#F5A623", width=1)

    icon_path = "/home/thaieasyvps/satang_the_value_icon_only.png"
    if os.path.exists(icon_path):
        icon = Image.open(icon_path).convert("RGBA").resize((54, 54), Image.Resampling.LANCZOS)
        mask = Image.new("L", (54, 54), 0)
        ImageDraw.Draw(mask).rounded_rectangle([0, 0, 53, 53], radius=14, fill=255)
        img.paste(icon, (60, 48), mask)
        draw.rounded_rectangle([59, 47, 115, 103], radius=14, outline="#38BDF8", width=1)

    draw.rounded_rectangle([128, 48, 410, 102], radius=14, fill="#121C3D", outline="#253563", width=2)
    draw.text((146, 60), "SATANG THE VALUE", fill="#FFFFFF", font=f_badge)
    
    draw.rounded_rectangle([424, 48, 550, 102], radius=14, fill="#F5A623")
    draw.text((444, 60), "เล่า DATA", fill="#0A1128", font=f_badge)

    draw.text((60, 122), "WHAT-IF SIMULATION • มิติคู่ขนานการเงินฉบับคนไทย", fill="#F5A623", font=f_cat)
    draw.text((60, 156), headline, fill="#FFFFFF", font=f_title)
    draw.text((60, 224), subtitle, fill="#A0AEC0", font=f_subtitle)

    col_w = 465
    col_h = 670
    col_y = 275
    left_x = 60
    right_x = 555

    # Left Column: Loss / Reality A
    draw.rounded_rectangle([left_x, col_y, left_x + col_w, col_y + col_h], radius=22, fill="#12162B", outline="#2D1D2C", width=2)
    draw.rounded_rectangle([left_x, col_y, left_x + col_w, col_y + 6], radius=3, fill="#EF4444")
    draw.rounded_rectangle([left_x + 30, col_y + 25, left_x + 220, col_y + 65], radius=10, fill="#2C161D")
    draw.text((left_x + 50, col_y + 30), left_title, fill="#FF6B6B", font=f_col_head)
    draw.text((left_x + 30, col_y + 80), "ลุ้นโชค 2 งวด/เดือน (งวดละ 500.-)", fill="#94A3B8", font=f_col_sub)
    draw.line([(left_x + 30, col_y + 120), (left_x + col_w - 30, col_y + 120)], fill="#202138", width=1)

    steps_left = [
        ("•", "งวดละ 500 บ. (เดือนละ 1,000.-)", "#CBD5E1"),
        ("•", "1 ปี เสียเงินซื้อหวย :", "#CBD5E1"),
        (" ", "  12,000 บาท", "#FF6B6B"),
        ("•", "สะสม 10 ปี (เงินต้นจริง) :", "#CBD5E1"),
        (" ", "  120,000 บาท", "#FFFFFF"),
        ("•", "โอกาสถูกรางวัลที่ 1 : 0.0001%", "#64748B"),
    ]
    sy = col_y + 140
    for bullet, text, col in steps_left:
        draw.text((left_x + 35, sy), f"{bullet} {text}", fill=col, font=f_bullet)
        sy += 36

    arrow_box_y = col_y + 385
    draw.rounded_rectangle([left_x + 30, arrow_box_y, left_x + col_w - 30, arrow_box_y + 54], radius=10, fill="#281419")
    draw_down_arrow(draw, left_x + 60, arrow_box_y + 27, size=22, fill="#FF4444")
    draw.text((left_x + 85, arrow_box_y + 12), "โอกาสไม่ถูกรางวัลสะสม 100%", fill="#FF6B6B", font=f_badge_pill)

    val_box_y = col_y + 455
    draw.rounded_rectangle([left_x + 30, val_box_y, left_x + col_w - 30, col_y + col_h - 25], radius=16, fill="#1B1320", outline="#EF4444", width=1)
    draw.text((left_x + 50, val_box_y + 20), "มูลค่าคงเหลือจริง :", fill="#94A3B8", font=f_col_sub)
    draw.text((left_x + 50, val_box_y + 60), left_loss_num, fill="#FF4444", font=f_giant_num)
    draw.text((left_x + 325, val_box_y + 80), "บาท", fill="#FF6B6B", font=f_unit)
    draw.text((left_x + 50, val_box_y + 130), "ขาดทุน -100% (เหลือกองสลาก 240 ใบ)", fill="#8392A5", font=f_note)

    # Right Column: Gain / Reality B
    draw.rounded_rectangle([right_x, col_y, right_x + col_w, col_y + col_h], radius=22, fill="#0F1F2B", outline="#163830", width=2)
    draw.rounded_rectangle([right_x, col_y, right_x + col_w, col_y + 6], radius=3, fill="#00E676")
    draw_4point_star(draw, right_x + col_w - 35, col_y + 35, r_outer=12, r_inner=3, fill_color="#00E676", glow=False)

    draw.rounded_rectangle([right_x + 30, col_y + 25, right_x + 220, col_y + 65], radius=10, fill="#123828")
    draw.text((right_x + 50, col_y + 30), right_title, fill="#00E676", font=f_col_head)
    draw.text((right_x + 30, col_y + 80), "ออมเดือนละ 1,000.- (DCA สม่ำเสมอ)", fill="#94A3B8", font=f_col_sub)
    draw.line([(right_x + 30, col_y + 120), (right_x + col_w - 30, col_y + 120)], fill="#173534", width=1)

    steps_right = [
        ("•", "ทยอยสะสมเดือนละ 1,000 บาท", "#CBD5E1"),
        ("•", "เงินต้นสะสม 10 ปีเท่ากัน :", "#CBD5E1"),
        (" ", "  120,000 บาท", "#FFFFFF"),
        ("•", "ผลตอบแทนเฉลี่ย ~5.14% ต่อปี", "#38BDF8"),
        (" ", "  (อ้างอิงกองทุนหุ้นไทย 10 ปีย้อนหลัง)", "#64748B"),
        ("•", "เงินทำงานสร้างดอกเบี้ยทบต้นชัวร์", "#00E676"),
    ]
    sy = col_y + 140
    for bullet, text, col in steps_right:
        draw.text((right_x + 35, sy), f"{bullet} {text}", fill=col, font=f_bullet)
        sy += 36

    draw.rounded_rectangle([right_x + 30, arrow_box_y, right_x + col_w - 30, arrow_box_y + 54], radius=10, fill="#103328")
    draw_up_arrow(draw, right_x + 60, arrow_box_y + 27, size=22, fill="#00E676")
    draw.text((right_x + 85, arrow_box_y + 12), "ผลตอบแทนเฉลี่ยคาดการณ์ 5.14%", fill="#00E676", font=f_badge_pill)

    draw.rounded_rectangle([right_x + 30, val_box_y, right_x + col_w - 30, col_y + col_h - 25], radius=16, fill="#0E2B25", outline="#00E676", width=2)
    draw.text((right_x + 50, val_box_y + 20), "มูลค่าพอร์ตปลายทาง :", fill="#38BDF8", font=f_col_sub)
    draw.text((right_x + 50, val_box_y + 60), right_gain_num, fill="#00E676", font=f_giant_num)
    draw.text((right_x + 325, val_box_y + 80), "บาท", fill="#A7F3D0", font=f_unit)
    draw.text((right_x + 50, val_box_y + 130), "เงินต้น 120,000 + กำไรทบต้น 39,734 ฿", fill="#A7F3D0", font=f_note)

    # Center 'VS'
    vs_cx = width // 2
    vs_cy = col_y + 420
    draw.ellipse([vs_cx - 36, vs_cy - 36, vs_cx + 36, vs_cy + 36], fill="#0A132C", outline="#F5A623", width=2)
    draw.text((vs_cx - 16, vs_cy - 18), "VS", fill="#F5A623", font=f_vs)

    # Consolidated Bottom Card
    bot_y0 = 975
    bot_y1 = 1255
    draw.rounded_rectangle([60, bot_y0, 1020, bot_y1], radius=20, fill="#111D3E", outline="#38BDF8", width=2)
    draw.rectangle([60, bot_y0, 72, bot_y1], fill="#F5A623")

    draw.text((95, bot_y0 + 24), "สรุปบทเรียนสำคัญของมิติคู่ขนาน 10 ปี :", fill="#F5A623", font=f_summary_title)
    draw.text((95, bot_y0 + 72), f"เงินต้น 120,000 บาทเท่ากัน แต่ปลายทางต่างกันถึง {net_diff_num} บาท!", fill="#FFFFFF", font=f_summary_title)
    draw.line([(95, bot_y0 + 120), (985, bot_y0 + 120)], fill="#1D2E5C", width=1)

    draw.text((95, bot_y0 + 138), "• ไม่ได้ห้ามลุ้นโชค แต่หากแบ่งเงินงวดละ 500.- มาสะสมในกองทุนรวม จะสร้างเงินแสนแรกได้จริง", fill="#CBD5E1", font=f_summary_body)
    draw.text((95, bot_y0 + 176), "• กองทุนรวมเริ่มต้นง่าย ใช้เงินน้อย (ซื้อผ่านแอป Mobile Banking ได้ทุกธนาคาร เริ่มแค่ 1 บาท)", fill="#A7F3D0", font=f_summary_body)
    draw.text((95, bot_y0 + 214), "• พลังดอกเบี้ยทบต้น (DCA) ช่วยทำงานแทนเรา เปลี่ยนเงินเศษเล็กๆ ให้กลายเป็นความมั่นคง", fill="#94A3B8", font=f_summary_body)

    # Footer
    draw.line([(60, 1280), (1020, 1280)], fill="#1E293B", width=1)
    draw.text((60, 1298), "ข้อมูล: Morningstar Thailand (กองทุนหุ้นไทย 10 ปีย้อนหลัง) & ตลาดหลักทรัพย์ฯ (SET)", fill="#64748B", font=f_footer)
    draw.text((795, 1298), "fb.com/SatangTheValue", fill="#94A3B8", font=f_footer)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path, quality=95)
    print(f"Comparison saved to {output_path}")

if __name__ == "__main__":
    render_set_style_comparison()
