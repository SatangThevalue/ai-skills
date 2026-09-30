#!/usr/bin/env python3
"""
Render Template G: 'The What-If Simulation' (Strict Reels 100% Safe-Zone)
9:16 Vertical Canvas (1080 x 1920) with 340px bottom clearance for Reels native UI.
"""
import os, math
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

def draw_grand_stars_916(draw, width, height):
    gold, gold_light = "#F5A623", "#FDE68A"
    cyan, line_col = "#38BDF8", "#15244D"
    lines = [
        ((width - 340, 160), (width - 220, 120)),
        ((width - 220, 120), (width - 110, 180)),
        ((width - 110, 180), (width - 70, 280)),
        ((40, 650), (85, 750)),
        ((85, 750), (45, 870)),
        ((width - 70, 1380), (width - 120, 1480)),
        ((width - 120, 1480), (width - 60, 1580)),
    ]
    for p1, p2 in lines:
        draw.line([p1, p2], fill=line_col, width=2)

    draw_4point_star(draw, width - 110, 180, r_outer=32, r_inner=7, fill_color=gold, glow=True)
    draw_4point_star(draw, width - 110, 180, r_outer=15, r_inner=3, fill_color=gold_light, glow=False)
    draw_4point_star(draw, width - 220, 120, r_outer=20, r_inner=5, fill_color=cyan, glow=True)
    draw_4point_star(draw, 50, 155, r_outer=15, r_inner=4, fill_color=gold, glow=False)
    draw_4point_star(draw, 85, 750, r_outer=18, r_inner=4, fill_color=cyan, glow=True)
    draw_4point_star(draw, width - 120, 1480, r_outer=26, r_inner=6, fill_color=gold, glow=True)
    draw_4point_star(draw, width - 120, 1480, r_outer=13, r_inner=3, fill_color=gold_light, glow=False)

def create_whatif_reels_template(output_path="/home/thaieasyvps/satang_template_g_whatif.png"):
    width, height = 1080, 1920
    img = Image.new("RGB", (width, height), color="#070D1F")
    draw = ImageDraw.Draw(img)

    glow_overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_overlay)
    for r in range(450, 100, -30):
        alpha = int(9 * (1.0 - (r / 450.0)))
        glow_draw.ellipse([width - 160 - r, 180 - r, width - 160 + r, 180 + r], fill=(56, 189, 248, alpha))
    for r in range(320, 60, -25):
        alpha = int(10 * (1.0 - (r / 320.0)))
        glow_draw.ellipse([width - 160 - r, 180 - r, width - 160 + r, 180 + r], fill=(245, 166, 35, alpha))
    for r in range(350, 70, -25):
        alpha = int(8 * (1.0 - (r / 350.0)))
        glow_draw.ellipse([width - 100 - r, 1000 - r, width - 100 + r, 1000 + r], fill=(245, 166, 35, alpha))
    for r in range(350, 70, -25):
        alpha = int(7 * (1.0 - (r / 350.0)))
        glow_draw.ellipse([80 - r, 1500 - r, 80 + r, 1500 + r], fill=(56, 189, 248, alpha))

    img = Image.alpha_composite(img.convert("RGBA"), glow_overlay).convert("RGB")
    draw = ImageDraw.Draw(img)
    draw_grand_stars_916(draw, width, height)

    font_dir = "/home/thaieasyvps/.fonts/Prompt"
    f_badge = ImageFont.truetype(os.path.join(font_dir, "Prompt-Bold.ttf"), 22)
    f_cat = ImageFont.truetype(os.path.join(font_dir, "Prompt-SemiBold.ttf"), 22)
    f_title = ImageFont.truetype(os.path.join(font_dir, "Prompt-Bold.ttf"), 48)
    f_subtitle = ImageFont.truetype(os.path.join(font_dir, "Prompt-Regular.ttf"), 24)
    f_side_title = ImageFont.truetype(os.path.join(font_dir, "Prompt-Bold.ttf"), 30)
    f_side_sub = ImageFont.truetype(os.path.join(font_dir, "Prompt-Regular.ttf"), 22)
    f_big_val = ImageFont.truetype(os.path.join(font_dir, "Prompt-Bold.ttf"), 68)
    f_val_lbl = ImageFont.truetype(os.path.join(font_dir, "Prompt-Medium.ttf"), 23)
    f_stat_item = ImageFont.truetype(os.path.join(font_dir, "Prompt-Regular.ttf"), 23)
    f_stat_bold = ImageFont.truetype(os.path.join(font_dir, "Prompt-Bold.ttf"), 23)
    f_badge_pct = ImageFont.truetype(os.path.join(font_dir, "Prompt-Bold.ttf"), 26)
    f_sum_lbl = ImageFont.truetype(os.path.join(font_dir, "Prompt-Bold.ttf"), 27)
    f_insight_title = ImageFont.truetype(os.path.join(font_dir, "Prompt-Bold.ttf"), 25)
    f_insight_body = ImageFont.truetype(os.path.join(font_dir, "Prompt-Regular.ttf"), 23)
    f_footer = ImageFont.truetype(os.path.join(font_dir, "Prompt-Regular.ttf"), 20)

    icon_path = "/home/thaieasyvps/satang_the_value_icon_only.png"
    if os.path.exists(icon_path):
        icon = Image.open(icon_path).convert("RGBA").resize((54, 54), Image.Resampling.LANCZOS)
        mask = Image.new("L", (54, 54), 0)
        ImageDraw.Draw(mask).rounded_rectangle([0, 0, 53, 53], radius=14, fill=255)
        img.paste(icon, (60, 90), mask)
        draw.rounded_rectangle([59, 89, 115, 145], radius=14, outline="#38BDF8", width=1)

    draw.rounded_rectangle([128, 90, 410, 144], radius=14, fill="#121C3D", outline="#253563", width=2)
    draw.text((146, 102), "SATANG THE VALUE", fill="#FFFFFF", font=f_badge)
    draw.rounded_rectangle([424, 90, 550, 144], radius=14, fill="#F5A623")
    draw.text((444, 102), "เล่า DATA", fill="#0A1128", font=f_badge)

    draw.text((60, 168), "WHAT-IF SIMULATION • มิติคู่ขนานการเงิน", fill="#F5A623", font=f_cat)
    draw.text((60, 204), "ถ้าเอาเงินค่าหวย 10 ปี ไปซื้อทองคำแท่ง?", fill="#FFFFFF", font=f_title)
    draw.text((60, 268), "จำลองตัวเลขจริง: ซื้อลอตเตอรี่งวดละ 2 ใบ (200 บาท) ทุกงวดตลอด 10 ปี (2016 - 2026)", fill="#A0AEC0", font=f_subtitle)

    # Reality A
    draw.rounded_rectangle([60, 325, 1020, 690], radius=22, fill="#0F1834", outline="#1F2F5E", width=2)
    draw.rounded_rectangle([60, 325, 1020, 331], radius=3, fill="#EF4444")
    draw.rounded_rectangle([95, 352, 260, 388], radius=8, fill="#2A1B28")
    draw.text((112, 358), "REALITY A : สายลุ้นโชค", fill="#F87171", font=f_badge)
    draw.text((95, 404), "ซื้อลอตเตอรี่ 2 ใบ ทุกงวด (240 งวด ตลอด 10 ปี)", fill="#FFFFFF", font=f_side_title)
    draw.text((95, 448), "เงินต้นสะสมที่จ่ายไปทั้งหมด :", fill="#94A3B8", font=f_val_lbl)
    draw.text((410, 442), "48,000 ฿", fill="#FFFFFF", font=f_side_title)
    draw.line([(95, 492), (985, 492)], fill="#1E2A4E", width=1)
    draw.text((95, 512), "• โอกาสถูกรางวัลที่ 1 :", fill="#CBD5E1", font=f_stat_item)
    draw.text((370, 512), "0.0001% (1 ใน 1,000,000)", fill="#F87171", font=f_stat_bold)
    draw.text((95, 552), "• สถิติคนไม่ถูกรางวัลสะสม :", fill="#CBD5E1", font=f_stat_item)
    draw.text((420, 552), "เสียเงินต้นทิ้ง 100% เต็มจำนวน", fill="#F87171", font=f_stat_bold)
    draw.rounded_rectangle([95, 595, 985, 680], radius=14, fill="#1B1728")
    draw.text((125, 622), "มูลค่าคงเหลือในมือวันนี้ :", fill="#94A3B8", font=f_val_lbl)
    draw.text((440, 600), "0 บาท", fill="#EF4444", font=f_big_val)
    draw.text((680, 624), "(เหลือกองกระดาษ 480 ใบ)", fill="#64748B", font=f_side_sub)

    # Reality B
    draw.rounded_rectangle([60, 715, 1020, 1145], radius=22, fill="#0F1B3A", outline="#F5A623", width=2)
    draw.rounded_rectangle([60, 715, 1020, 721], radius=3, fill="#F5A623")
    draw_4point_star(draw, 980, 745, r_outer=14, r_inner=4, fill_color="#F5A623", glow=False)
    draw.rounded_rectangle([95, 742, 300, 778], radius=8, fill="#3D2E17")
    draw.text((112, 748), "REALITY B : สายสะสมทองคำ", fill="#F5A623", font=f_badge)
    draw.text((95, 794), "ออมทองงวดละ 200.- (DCA ทองคำแท่ง 10 ปี)", fill="#FFFFFF", font=f_side_title)
    draw.text((95, 838), "เงินต้นสะสมที่ใช้ไปเท่ากัน :", fill="#94A3B8", font=f_val_lbl)
    draw.text((410, 832), "48,000 ฿", fill="#FFFFFF", font=f_side_title)
    draw.line([(95, 882), (985, 882)], fill="#233560", width=1)
    draw.text((95, 902), "• ปริมาณทองคำแท่งสะสมได้ :", fill="#CBD5E1", font=f_stat_item)
    draw.text((430, 902), "~2.20 บาททองคำ", fill="#F5A623", font=f_stat_bold)
    draw.text((95, 942), "• ราคาทองคำเติบโตเฉลี่ย :", fill="#CBD5E1", font=f_stat_item)
    draw.text((420, 942), "จาก 21,500 ฿ สู่ 45,000+ ฿", fill="#00E676", font=f_stat_bold)
    draw.rounded_rectangle([95, 995, 985, 1120], radius=14, fill="#122544", outline="#F5A623", width=2)
    draw.text((120, 1018), "มูลค่าทองคำในมือวันนี้ :", fill="#F5A623", font=f_val_lbl)
    draw.text((440, 1004), "99,000 ฿", fill="#FFFFFF", font=f_big_val)
    draw.rounded_rectangle([120, 1068, 370, 1108], radius=8, fill="#00E676")
    draw.text((135, 1074), "▲ กำไรสุทธิ +106%", fill="#0A1128", font=f_badge_pct)
    draw.text((390, 1076), "(กำไรฟรีๆ +51,000 บาท ไม่รวมเงินต้น)", fill="#CBD5E1", font=f_side_sub)

    # Summary
    draw.rounded_rectangle([60, 1170, 1020, 1285], radius=16, fill="#162754", outline="#38BDF8", width=2)
    draw_4point_star(draw, 95, 1205, r_outer=12, r_inner=3, fill_color="#38BDF8", glow=False)
    draw.text((120, 1195), "ส่วนต่างผลลัพธ์มิติคู่ขนาน 10 ปี :", fill="#38BDF8", font=f_sum_lbl)
    draw.text((120, 1235), "เงินต้นเท่ากัน 48,000 แต่พอร์ตต่างกันถึง 99,000 บาท!", fill="#FFFFFF", font=f_side_title)

    # Data Insight
    draw.rounded_rectangle([60, 1310, 1020, 1475], radius=18, fill="#111B3D", outline="#253563", width=2)
    draw.rectangle([60, 1310, 74, 1475], fill="#F5A623")
    draw.text((95, 1332), "บทวิเคราะห์เชิงข้อมูล (Data Insight) :", fill="#F5A623", font=f_insight_title)
    draw.text((95, 1374), "พลังของการสร้างวินัยการเงิน (DCA) ในสินทรัพย์ที่ชนะเงินเฟ้อ จะเปลี่ยนเงินเศษ", fill="#E2E8F0", font=f_insight_body)
    draw.text((95, 1416), "ให้กลายเป็นเงินแสนได้ โดยแทบไม่ต้องเปลี่ยนรูปแบบการใช้ชีวิตประจำวันเลยแม้แต่น้อย", fill="#94A3B8", font=f_insight_body)

    # Footer
    draw.line([(60, 1505), (1020, 1505)], fill="#1E293B", width=1)
    draw.text((60, 1522), "ข้อมูล: สถิติราคาทองคำแท่งย้อนหลัง สมาคมค้าทองคำ (2016 - 2026)", fill="#64748B", font=f_footer)
    draw.text((790, 1522), "fb.com/SatangTheValue", fill="#94A3B8", font=f_footer)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path, quality=95)

if __name__ == "__main__":
    create_whatif_reels_template()
