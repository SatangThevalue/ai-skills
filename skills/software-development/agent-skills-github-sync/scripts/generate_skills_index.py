#!/usr/bin/env python3
"""
generate_skills_index.py — Generate INDEX.md and update README.md for Hermes skills.
Scans ~/.hermes/skills/ (or specified path), extracts metadata, formats:
1. INDEX.md with a categorized table and anchors.
2. README.md with the full category TOC.
Also syncs to ~/ai-skills/ if it exists.
"""

import os
import re
import sys
from datetime import datetime

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

def build_catalog(skills_dir):
    categories = {}
    for root, dirs, files in os.walk(skills_dir):
        if 'SKILL.md' in files:
            rel = os.path.relpath(root, skills_dir)
            parts = rel.split(os.sep)
            cat = parts[0]
            skill_folder = parts[-1]
            fm_name, fm_desc = parse_skill_md(os.path.join(root, 'SKILL.md'))
            display_name = fm_name or skill_folder
            desc = fm_desc or '-'
            desc = desc.replace('\n', ' ').strip()
            categories.setdefault(cat, []).append((display_name, desc, rel))
    return categories

def write_index(skills_dir, categories):
    total_skills = sum(len(v) for v in categories.values())
    sorted_cats = sorted(categories.keys())

    lines = [
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
        lines.append(f'| [{cat}](#{cat}) | **{count}** | {sample} |')

    lines.extend(['', '---', ''])

    for cat in sorted_cats:
        skills = sorted(categories[cat], key=lambda x: x[0].lower())
        lines.append(f'## <a id="{cat}"></a>📂 {cat} ({len(skills)} skills)')
        lines.append('')
        lines.append('| Skill Name | Description | Path |')
        lines.append('|---|---|---|')
        for name, desc, path in skills:
            clean_desc = desc.replace('|', '/')
            if len(clean_desc) > 140:
                clean_desc = clean_desc[:137] + '...'
            lines.append(f'| `{name}` | {clean_desc} | `{path}` |')
        lines.append('')

    index_path = os.path.join(skills_dir, 'INDEX.md')
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines) + '\n')
    print(f'✓ INDEX.md written: {total_skills} skills in {len(sorted_cats)} categories.')

def write_readme(skills_dir, categories):
    total_skills = sum(len(v) for v in categories.values())
    sorted_cats = sorted(categories.keys())
    today = datetime.now().strftime('%Y-%m-%d')

    lines = [
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
        '',
    ]

    for cat in sorted_cats:
        skills = sorted(categories[cat], key=lambda x: x[0].lower())
        lines.append(f'### 📁 {cat.upper()} ({len(skills)})')
        lines.append('')
        for name, desc in skills:
            lines.append(f'- **`{name}`**: {desc}')
        lines.append('')

    content = '\n'.join(lines) + '\n'

    # Local skills README
    with open(os.path.join(skills_dir, 'README.md'), 'w', encoding='utf-8') as f:
        f.write(content)
    print('✓ ~/.hermes/skills/README.md updated.')

    # ai-skills repo README if exists
    repo_root = os.path.expanduser('~/ai-skills')
    if os.path.isdir(repo_root):
        with open(os.path.join(repo_root, 'README.md'), 'w', encoding='utf-8') as f:
            f.write(content)
        print('✓ ~/ai-skills/README.md updated.')

if __name__ == '__main__':
    target = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser('~/.hermes/skills')
    cats = build_catalog(target)
    write_index(target, cats)
    write_readme(target, cats)
