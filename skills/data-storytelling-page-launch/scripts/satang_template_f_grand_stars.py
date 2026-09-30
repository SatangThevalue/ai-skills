#!/usr/bin/env python3
"""
Render Template F: 'Resource Spotlight' - GRAND STAR EDITION!
4:5 Aspect Ratio (1080 x 1350).
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

def draw_starfield_and_constellations(draw, width, height):
    gold, gold_light = "#F5A623", "#FDE68A"
    cyan, cyan_light = "#38BDF8", "#BAE6FD"
    circuit_color = "#16254F"

    lines = [
        ((width - 320, 140), (width - 210, 100)),
        ((width - 210, 100), (width - 110, 160)),
        ((width - 110, 160), (width - 70, 250)),
        ((width - 80, 990), (width - 130, 1080)),
        ((width - 130, 1080), (width - 60, 1180)),
        ((35, 450), (70, 530)),
        ((70, 530), (40, 630)),
    ]
    for p1, p2 in lines:
        draw.line([p1, p2], fill=circuit_color, width=2)

    draw_4point_star(draw, width - 110, 160, r_outer=32, r_inner=7, fill_color=gold, glow=True)
    draw_4point_star(draw, width - 110, 160, r_outer=16, r_inner=4, fill_color=gold_light, glow=False)
    draw_4point_star(draw, width - 210, 100, r_outer=20, r_inner=5, fill_color=cyan, glow=True)
    draw_4point_star(draw, 42, 138, r_outer=14, r_inner=4, fill_color=gold, glow=False)
    draw_4point_star(draw, 520, 138, r_outer=12, r_inner=3, fill_color=gold, glow=False)
    draw_4point_star(draw, 70, 530, r_outer=18, r_inner=4, fill_color=cyan, glow=True)
    draw_4point_star(draw, 40, 630, r_outer=14, r_inner=3, fill_color=gold, glow=False)
    draw_4point_star(draw, width - 130, 1080, r_outer=28, r_inner=6, fill_color=cyan, glow=True)
    draw_4point_star(draw, width - 60, 1180, r_outer=18, r_inner=4, fill_color=gold, glow=False)

def create_grand_star_spotlight(output_path="/home/thaieasyvps/satang_template_f_grand_stars.png"):
    width, height = 1080, 1350
    img = Image.new("RGB", (width, height), color="#070D1F")
    draw = ImageDraw.Draw(img)

    glow_overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_overlay)
    for r in range(450, 80, -25):
        alpha = int(9 * (1.0 - (r / 450.0)))
        glow_draw.ellipse([width - 150 - r, 120 - r, width - 150 + r, 120 + r], fill=(56, 189, 248, alpha))
    for r in range(320, 60, -20):
        alpha = int(10 * (1.0 - (r / 320.0)))
        glow_draw.ellipse([width - 150 - r, 120 - r, width - 150 + r, 120 + r], fill=(245, 166, 35, alpha))
    for r in range(380, 70, -25):
        alpha = int(8 * (1.0 - (r / 380.0)))
        glow_draw.ellipse([40 - r, height - 120 - r, 40 + r, height - 120 + r], fill=(245, 166, 35, alpha))

    img = Image.alpha_composite(img.convert("RGBA"), glow_overlay).convert("RGB")
    draw = ImageDraw.Draw(img)
    draw_starfield_and_constellations(draw, width, height)

    font_dir = "/home/thaieasyvps/.fonts/Prompt"
    f_badge = ImageFont.truetype(os.path.join(font_dir, "Prompt-Bold.ttf"), 22)
    f_cat = ImageFont.truetype(os.path.join(font_dir, "Prompt-SemiBold.ttf"), 22)
    f_title = ImageFont.truetype(os.path.join(font_dir, "Prompt-Bold.ttf"), 48)
    f_subtitle = ImageFont.truetype(os.path.join(font_dir, "Prompt-Regular.ttf"), 25)
    f_tag = ImageFont.truetype(os.path.join(font_dir, "Prompt-Bold.ttf"), 18)
    f_repo_head = ImageFont.truetype(os.path.join(font_dir, "Prompt-Bold.ttf"), 35)
    f_stars = ImageFont.truetype(os.path.join(font_dir, "Prompt-Bold.ttf"), 22)
    f_section_head = ImageFont.truetype(os.path.join(font_dir, "Prompt-Bold.ttf"), 26)
    f_body = ImageFont.truetype(os.path.join(font_dir, "Prompt-Regular.ttf"), 23)
    f_step_num = ImageFont.truetype(os.path.join(font_dir, "Prompt-Bold.ttf"), 22)
    f_step_txt = ImageFont.truetype(os.path.join(font_dir, "Prompt-Medium.ttf"), 23)
    f_bm_title = ImageFont.truetype(os.path.join(font_dir, "Prompt-Bold.ttf"), 24)
    f_bm_sub = ImageFont.truetype(os.path.join(font_dir, "Prompt-Regular.ttf"), 20)
    f_insight_title = ImageFont.truetype(os.path.join(font_dir, "Prompt-Bold.ttf"), 26)
    f_insight_body = ImageFont.truetype(os.path.join(font_dir, "Prompt-Regular.ttf"), 24)
    f_footer = ImageFont.truetype(os.path.join(font_dir, "Prompt-Regular.ttf"), 20)

    draw.line([(0, 0), (width, 0)], fill="#F5A623", width=4)
    draw.line([(width - 350, 4), (width, 4)], fill="#38BDF8", width=2)

    icon_path = "/home/thaieasyvps/satang_the_value_icon_only.png"
    if os.path.exists(icon_path):
        icon = Image.open(icon_path).convert("RGBA").resize((54, 54), Image.Resampling.LANCZOS)
        mask = Image.new("L", (54, 54), 0)
        ImageDraw.Draw(mask).rounded_rectangle([0, 0, 53, 53], radius=14, fill=255)
        img.paste(icon, (60, 50), mask)
        draw.rounded_rectangle([59, 49, 115, 105], radius=14, outline="#38BDF8", width=1)

    draw.rounded_rectangle([128, 50, 410, 104], radius=14, fill="#121C3D", outline="#253563", width=2)
    draw.text((146, 62), "SATANG THE VALUE", fill="#FFFFFF", font=f_badge)
    draw.rounded_rectangle([424, 50, 550, 104], radius=14, fill="#F5A623")
    draw.text((444, 62), "เล่า DATA", fill="#0A1128", font=f_badge)

    draw.text((60, 130), "RESOURCE SPOTLIGHT • เจาะลึกคลังข้อมูลฟรี", fill="#F5A623", font=f_cat)
    draw.text((60, 168), "คลัง Dataset ฟรีที่ใหญ่ที่สุดบน GitHub", fill="#FFFFFF", font=f_title)
    draw.text((60, 240), "แนะนำ awesomedata รวมสถิติเปิดกว่า 30 หมวดหมู่ สำหรับคนฝึก Data Analytics", fill="#A0AEC0", font=f_subtitle)

    cx0, cy0, cx1, cy1 = 60, 300, 1020, 935
    draw.rounded_rectangle([cx0, cy0, cx1, cy1], radius=24, fill="#0E1733", outline="#1F2F5E", width=2)
    draw.rounded_rectangle([cx0, cy0, cx1, cy0 + 6], radius=3, fill="#F5A623")
    draw_4point_star(draw, cx0 + 25, cy0 + 20, r_outer=10, r_inner=3, fill_color="#F5A623", glow=False)
    draw_4point_star(draw, cx1 - 25, cy0 + 20, r_outer=10, r_inner=3, fill_color="#38BDF8", glow=False)

    draw.rounded_rectangle([100, 335, 260, 372], radius=8, fill="#F5A623")
    draw.text((116, 343), "RECOMMENDED", fill="#0A1128", font=f_tag)
    draw.rounded_rectangle([275, 335, 425, 372], radius=8, fill="#19274E", outline="#38BDF8", width=1)
    draw.text((292, 343), "OPEN SOURCE", fill="#38BDF8", font=f_tag)
    draw.rounded_rectangle([805, 335, 980, 372], radius=8, fill="#1B284E", outline="#F5A623", width=1)
    draw_4point_star(draw, 825, 353, r_outer=10, r_inner=3, fill_color="#F5A623", glow=False)
    draw.text((845, 343), "62.8k Stars", fill="#F5A623", font=f_stars)

    draw.text((100, 395), "awesomedata / awesome-public-datasets", fill="#FFFFFF", font=f_repo_head)
    draw.text((100, 448), "คลังรวมข้อมูลดิบระดับโลกที่ถูกอัปเดตสม่ำเสมอ ครอบคลุมตั้งแต่การเงินจนถึงไลฟ์สไตล์", fill="#94A3B8", font=f_body)
    draw.line([(100, 498), (980, 498)], fill="#1E2A4E", width=1)

    draw.text((100, 516), "จุดเด่นของคลังข้อมูลนี้ :", fill="#F5A623", font=f_section_head)
    bullets = [
        "• รวบรวมข้อมูลแยก 30+ หมวดหมู่: การเงิน, ธุรกิจ, อสังหาฯ, สภาพอากาศ, และกีฬา",
        "• ไฟล์ฟอร์แมตมาตรฐาน (.csv, .json, .parquet) โหลดไปเปิดใน Excel หรือ Python ได้ทันที",
        "• ใช้งานได้ฟรี 100% ภายใต้สัญญาอนุญาตแบบ Public Domain & Open Source"
    ]
    by = 560
    for b in bullets:
        draw.text((100, by), b, fill="#E2E8F0", font=f_body)
        by += 44

    draw.line([(100, 706), (980, 706)], fill="#1E2A4E", width=1)
    draw.text((100, 724), "วิธีเข้าถึงและนำไปใช้งาน (3 สเต็ปง่ายๆ) :", fill="#38BDF8", font=f_section_head)
    steps = [
        ("1", "ค้นหาใน GitHub :  awesomedata / awesome-public-datasets"),
        ("2", "เลือกหมวดหมู่ที่สนใจ :  ดาวน์โหลดไฟล์ .csv หรือ .json เข้าเครื่องได้ทันที"),
        ("3", "นำไปสร้างพอร์ต :  พล็อต Dashboard บน Power BI หรือฝึกรันโมเดลบน Python")
    ]
    sy = 768
    for s_num, s_txt in steps:
        draw.rounded_rectangle([100, sy, 135, sy + 32], radius=6, fill="#19274E", outline="#253A6E", width=1)
        draw.text((112, sy + 4), s_num, fill="#F5A623", font=f_step_num)
        draw.text((150, sy + 4), s_txt, fill="#CBD5E1", font=f_step_txt)
        sy += 45

    draw.rounded_rectangle([60, 955, 1020, 1025], radius=16, fill="#121F45", outline="#F5A623", width=2)
    draw_4point_star(draw, 80, 990, r_outer=10, r_inner=3, fill_color="#F5A623", glow=False)
    draw.text((105, 975), "กด Save โพสต์นี้เก็บไว้ :", fill="#F5A623", font=f_bm_title)
    draw.text((375, 978), "เปิดคอมพิวเตอร์เพื่อค้นหาชื่อ Repo และดาวน์โหลดไฟล์ไปฝึกทำพอร์ตได้เลย", fill="#FFFFFF", font=f_bm_sub)

    draw.rounded_rectangle([60, 1045, 1020, 1225], radius=20, fill="#121D3F", outline="#253563", width=2)
    draw.rectangle([60, 1045, 72, 1225], fill="#F5A623")
    draw.text((95, 1070), "บทวิเคราะห์เชิงข้อมูล (Data Insight) :", fill="#F5A623", font=f_insight_title)
    draw.text((95, 1115), "คนสาย Data ที่มีพอร์ตโฟลิโอจาก Open Data จริงบน GitHub มีโอกาสได้งานสูงกว่า 2.4 เท่า", fill="#E2E8F0", font=f_insight_body)
    draw.text((95, 1158), "เพราะองค์กรชั้นนำให้ความสำคัญกับทักษะการทำ Data Cleaning จากข้อมูลดิบที่จับต้องได้", fill="#94A3B8", font=f_insight_body)

    draw.line([(60, 1255), (1020, 1255)], fill="#1E293B", width=1)
    draw.text((60, 1280), "พิกัด: github.com/awesomedata (Open Source 2026)", fill="#64748B", font=f_footer)
    draw.text((790, 1280), "fb.com/SatangTheValue", fill="#94A3B8", font=f_footer)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path, quality=95)

if __name__ == "__main__":
    create_grand_star_spotlight()
