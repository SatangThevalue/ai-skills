#!/usr/bin/env python3
"""
generate_skills_index.py — Generate INDEX.md for Hermes skills directory.
Scans ~/.hermes/skills/ (or specified path), extracts metadata, and formats
a categorized markdown index table.
"""

import os
import re
import sys

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

def build_index(skills_dir):
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
            desc = desc.replace('|', '/').replace('\n', ' ').strip()
            if len(desc) > 140:
                desc = desc[:137] + '...'
            categories.setdefault(cat, []).append((display_name, desc, rel))

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
            lines.append(f'| `{name}` | {desc} | `{path}` |')
        lines.append('')

    index_path = os.path.join(skills_dir, 'INDEX.md')
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines) + '\n')
    print(f'Done: {total_skills} skills in {len(sorted_cats)} categories written to {index_path}')

if __name__ == '__main__':
    target = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser('~/.hermes/skills')
    build_index(target)
