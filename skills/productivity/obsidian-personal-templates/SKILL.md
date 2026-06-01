---
name: obsidian-personal-templates
title: Obsidian personal vault templates & backup workflow
summary: ชุดเทมเพลตและ workflow สำหรับบันทึกชีวิต การเงิน การลงทุน ประกัน หนี้สิน ทรัพย์สิน ภาษี ใน Obsidian พร้อมวิธี backup เป็น Git และ validator
description: |
  สกิลนี้ติดตั้งชุดเทมเพลตมาตรฐานสำหรับการจัดการชีวิตและการเงินใน Obsidian (Transaction, Investment, Asset, Debt, Insurance, Tax, Budget, Net Worth, Goal, Daily note, ฯลฯ), สร้างไฟล์ ledger canonical (transactions.csv), accounts.yml, สคริปต์สำหรับตรวจสอบความถูกต้องของข้อมูล (validator) และสคริปต์/cron สำหรับสำรอง Vault ขึ้น Git ทุก 15 นาที พร้อมคำแนะนำเรื่องความปลอดภัยและตัวอย่าง Dataview snippets.
author: Hermes (assistant)
maintainer: user
created: 2026-06-01
tags: [obsidian, templates, personal-finance, vault, dataview, templater]
---

## เมื่อใช้สกิลนี้
สกิลนี้ติดตั้งชุดเทมเพลตที่เป็นมาตรฐาน (Transaction, Investment, Asset, Debt, Insurance, Tax, Budget, Net Worth, Goal, Daily note, ฯลฯ) ไว้ใน Vault, ตัวอย่าง Dataview queries, และคำสั่ง/สคริปต์เพื่อสำรอง Vault ขึ้น Git ทุก 15 นาที (cron). เหมาะสำหรับเก็บข้อมูลการเงินเป็น machine-readable (amount_cents, ISO dates, unique id).

## Trigger / When to run
- เรียกใช้ครั้งแรกเมื่อสร้าง Obsidian Vault ใหม่สำหรับการเงินส่วนตัว
- รันอีกครั้งเมื่อต้องการรีเซ็ต/อัปเดตชุดเทมเพลต

## ตำแหน่งไฟล์ (assumes vault path)
- Vault root: ~/Documents/Obsidian Vault/
- Templates: Templates/ (หลายไฟล์ .md)
- Ledger (canonical): transactions.csv (CSV machine-readable)
- Accounts summary: accounts.yml
- Scripts: scripts/ (validate_transactions.py, git_push_cron.sh, setup_github_pat.sh)
- .obsidian/community-plugins.json (enabled plugins list)

## สิ่งที่สกิลนี้ทำ (สรุป)
1. สร้างชุดเทมเพลต .md ใน Templates/ (Transaction, Investment Transaction, Asset, Debt, Insurance, Tax, Monthly Budget, Net Worth, Goal, Daily, Meeting, Project, Contact, Health Log)
2. สร้างตัวอย่าง transactions.csv (header) และ accounts.yml
3. สร้าง validator script (Python) สำหรับตรวจ schema, date, amount และ checksum
4. สร้างสคริปต์ช่วย push อัตโนมัติ และติดตั้ง crontab: */15 * * * * scripts/git_push_cron.sh
5. ติดตั้ง/enable community plugins ที่แนะนำ (Dataview, Templater, Advanced Tables) ด้วย .obsidian/community-plugins.json
6. เต็มคำอธิบายการใช้งาน และ verification steps

## วิธีเรียกใช้ (manual steps)
1. เปิด Vault ใน Obsidian (AppImage หรือ App) และตรวจว่า Plugins ที่ต้องการถูกติดตั้งและ Enable
2. เปิด terminal ในเครื่องและเข้า Vault:

   cd "$HOME/Documents/Obsidian Vault"

3. ถ้ายังไม่มี git remote แล้วต้องตั้ง origin ก่อน (สองทาง):
   - ทางที่แนะนำ: สร้าง repo บน GitHub ผ่านเว็บ (owner: SatangThevalue, name: my-vault-repo) แล้วให้ assistant push ให้
   - ทางเลือก: ใช้ SSH deploy key (ปลอดภัย) — สร้าง keypair แล้วเพิ่ม public key เป็น Deploy key ของ repo (allow write)

4. ใช้สคริปต์ `scripts/setup_github_pat.sh` ถ้าต้องการเก็บ PAT ชั่วคราวและตั้ง origin (ห้ามใส่ token ในที่สาธารณะ)

## Verification (ตรวจสอบหลังติดตั้ง)
- ตรวจว่าไฟล์ Templates/ มีไฟล์ .md ดังนี้: Transaction.md, Investment Transaction.md, Asset Item.md, Debt Item.md, Insurance Policy.md, Tax Record.md, Monthly Budget.md, Net Worth.md, Goal.md, Daily Template.md, Meeting.md, Project.md, Contact.md, Health Log.md
- ตรวจว่า transactions.csv มี header:
  id,date,account,counterparty,category,amount_cents,currency,type,tags,notes,source_file,created_at
- รัน validator:

  python3 scripts/validate_transactions.py transactions.csv

  ควรได้ exit 0 และข้อความยืนยันว่า valid (หรือ list ข้อผิดพลาด)

- ตรวจว่า git remote ถูกตั้งและ push สำเร็จ:

  git remote -v
  git ls-remote origin HEAD

- ตรวจว่า cron มี entry ทุก 15 นาที:

  crontab -l | grep git_push_cron.sh

## Pitfalls & Security
- ห้ามเก็บ PAT / token ในที่สาธารณะ ควรเก็บในไฟล์ credentials เฉพาะเครื่อง (permission 600) หรือใช้ SSH deploy key
- เก็บจำนวนเงินเป็น minor units (amount_cents) เสมอ เพื่อหลีกเลี่ยงการเพี้ยนของ float
- วันที่ต้องเป็น ISO-8601 (YYYY-MM-DD) เพื่อให้ Dataview และ scripts ทำงานถูกต้อง
- หากต้องการแชร์ Vault กับทีม ใช้ remote Git private repo และไม่ commit ไฟล์ที่มี secret

## Examples / Dataview snippets
- รวมยอดตามหมวดหมู่ (transactions.csv ต้องเป็นแหล่งข้อมูลที่ Dataview อ่านได้ หรือ import เป็น page per transaction):

```dataview
TABLE sum(rows.amount_cents) as total_cents, rows.category
FROM "transactions.csv"
GROUP BY rows.category
```

(หมายเหตุ: Dataview ต้องการให้ข้อมูลอยู่ในหน้า Markdown หรือ Dataview v2 CSV import — adjust ตาม plugin capability)

## Tests and validation
- Validator script checks:
  - CSV columns exist
  - date format ISO
  - amount_cents integer
  - unique id
  - checksum (optional) — script returns non-zero exit code on failure

## Maintenance
- อัปเดตเทมเพลตใน Templates/ เมื่อต้องการฟิลด์ใหม่
- หากเปลี่ยน schema ของ transactions.csv ให้ปรับ validator และ importer scripts พร้อมกัน
- ปรับความถี่ cron ใน crontab หากต้องการ

## Files created by this skill (list)
- Templates/Transaction.md
- Templates/Investment Transaction.md
- Templates/Asset Item.md
- Templates/Debt Item.md
- Templates/Insurance Policy.md
- Templates/Tax Record.md
- Templates/Monthly Budget.md
- Templates/Net Worth.md
- Templates/Goal.md
- Templates/Daily Template.md
- Templates/Meeting.md
- Templates/Project.md
- Templates/Contact.md
- Templates/Health Log.md
- Templates/.templates_index.md
- transactions.csv
- accounts.yml
- scripts/validate_transactions.py
- scripts/git_push_cron.sh
- scripts/setup_github_pat.sh
- .obsidian/community-plugins.json

## Offer
หากต้องการ ผมสามารถ:
- แปลงขั้นตอนนี้เป็น automation ที่เรียกจาก CLI (script) เพื่อ recreate templates ใน Vault ใด ๆ
- เพิ่ม importer สำหรับ CSV จากธนาคารไทย (Bangkok Bank, KBank, SCB) ให้แปลงเป็น transactions.csv
- สร้าง Dataview example dashboards (Net Worth, Monthly Budget, Investment positions)

---
# End of skill
