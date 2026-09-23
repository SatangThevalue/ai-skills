#!/usr/bin/env python3
import os
import re
from datetime import datetime

skills_dir = os.path.expanduser('~/.hermes/skills')
categories = {}

def parse_skill_md(path):
    name = ''
    desc = ''
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        match = re.search(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
        if match:
            fm = match.group(1)
            name_m = re.search(r'^name:\s*(.+)$', fm, re.MULTILINE)
            desc_m = re.search(r'^description:\s*(.+)$', fm, re.MULTILINE)
            if name_m:
                name = name_m.group(1).strip('\"\' ')
            if desc_m:
                desc = desc_m.group(1).strip('\"\' ')
    except Exception:
        pass
    return name, desc

for root, dirs, files in os.walk(skills_dir):
    if 'SKILL.md' in files:
        rel = os.path.relpath(root, skills_dir)
        parts = rel.split(os.sep)
        cat = parts[0]
        skill_folder = parts[-1]
        fm_name, fm_desc = parse_skill_md(os.path.join(root, 'SKILL.md'))
        display_name = fm_name or skill_folder
        desc = fm_desc or '-'
        desc_clean = desc.replace('|', '/').replace('\n', ' ').strip()
        categories.setdefault(cat, []).append((display_name, desc_clean, rel))

total_skills = sum(len(v) for v in categories.values())
sorted_cats = sorted(categories.keys())
today = datetime.now().strftime('%Y-%m-%d')

# 1. Generate INDEX.md
lines_idx = [
    '# 📚 Hermes Skills Directory Index',
    '',
    f'> คลังทักษะทั้งหมดของ Hermes Agent: **{total_skills} skills** จัดระเบียบใน **{len(sorted_cats)} หมวดหมู่**',
    '',
    '---',
    '',
    '## 📊 สรุปภาพรวมหมวดหมู่ (Category Overview)',
    '',
    '| หมวดหมู่ (Category) | จำนวน | ตัวอย่างสกิลเด่น |',
    '|---|:---:|---|',
]

for cat in sorted_cats:
    skills = sorted(categories[cat], key=lambda x: x[0].lower())
    count = len(skills)
    sample = ', '.join([f'`{s[0]}`' for s in skills[:3]])
    if count > 3:
        sample += f' *(+อีก {count-3})*'
    lines_idx.append(f'| [{cat}](#{cat}) | **{count}** | {sample} |')

lines_idx.extend(['', '---', ''])

for cat in sorted_cats:
    skills = sorted(categories[cat], key=lambda x: x[0].lower())
    lines_idx.append(f'## <a id="{cat}"></a>📂 {cat} ({len(skills)} skills)')
    lines_idx.append('')
    lines_idx.append('| Skill Name | Description | Path |')
    lines_idx.append('|---|---|---|')
    for name, desc, path in skills:
        short_desc = desc[:137] + '...' if len(desc) > 140 else desc
        lines_idx.append(f'| `{name}` | {short_desc} | `{path}` |')
    lines_idx.append('')

with open(os.path.join(skills_dir, 'INDEX.md'), 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines_idx) + '\n')

# 2. Generate README.md
lines_readme = [
    '# 🧠 AI Skills — Tonthong (ต้นทอง) Skill Library',
    '',
    '> **Repository:** [SatangTheValue/ai-skills](https://github.com/SatangTheValue/ai-skills)  ',
    '> **ผู้ดูแล:** Thanapol N (Satang) · ผู้ช่วย: ต้นทอง (Hermes Agent)  ',
    f'> **อัปเดตล่าสุด:** {today}',
    '',
    '---',
    '',
    '## 📖 คืออะไร?',
    '',
    'คลังสกิลของต้นทอง (Hermes Agent) ที่ใช้ในการทำงานร่วมกับ Satang — ครอบคลุมตั้งแต่ DevOps, Finance, Trading, Marketing, AI/ML ไปจนถึงการพัฒนาซอฟต์แวร์ทั้งหมด',
    '',
    'สกิลแต่ละตัวคือ **ชุดคำสั่งและขั้นตอนที่พิสูจน์แล้ว** ที่ต้นทองโหลดขึ้นมาใช้โดยอัตโนมัติเมื่อได้รับงานที่เกี่ยวข้อง ทำให้ไม่ต้องอธิบายขั้นตอนซ้ำในทุก Session',
    '',
    '---',
    '',
    '## 🚀 วิธีใช้งาน',
    '',
    '```bash',
    '# ดูรายชื่อ Skill ทั้งหมด',
    'hermes skills list',
    '',
    '# โหลด Skill เพื่อดูเนื้อหา',
    'hermes skills view <ชื่อ-skill>',
    '```',
    '',
    '---',
    '',
    f'## 📚 รายชื่อ Skills แบ่งตามหมวดหมู่ ({total_skills} skills ใน {len(sorted_cats)} หมวดหมู่)',
    ''
]

for cat in sorted_cats:
    skills = sorted(categories[cat], key=lambda x: x[0].lower())
    lines_readme.append(f'### 📁 {cat.upper()} ({len(skills)})')
    lines_readme.append('')
    for name, desc, _ in skills:
        lines_readme.append(f'- **`{name}`**: {desc}')
    lines_readme.append('')

readme_content = '\n'.join(lines_readme) + '\n'

with open(os.path.join(skills_dir, 'README.md'), 'w', encoding='utf-8') as f:
    f.write(readme_content)

ai_skills_root = os.path.expanduser('~/ai-skills')
if os.path.exists(ai_skills_root):
    with open(os.path.join(ai_skills_root, 'README.md'), 'w', encoding='utf-8') as f:
        f.write(readme_content)

print(f'Done: {total_skills} skills in {len(sorted_cats)} categories.')
