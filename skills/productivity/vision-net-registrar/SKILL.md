---
name: vision-net-registrar
description: Use when scraping or integrating academic data (schedules, grades, registration) from universities using Vision Net E-Registrar (e.g., RMUTT, TU, WU).
version: 1.0.0
author: Tonthong
license: MIT
metadata:
  hermes:
    tags: [scraping, web, registrar, education, planning]
    related_skills: []
---

# Vision Net E-Registrar Data Integration Skill

## Overview
This skill provides guidelines and templates for authenticating, fetching, and parsing student academic data (such as study timetables, exam schedules, and grades) from Thai university registration portals built on Vision Net's **E-Registrar Educational Service System** (typically hosted under `/registrar/`).

## When to Use
- When extracting study timetables, exam schedules, or academic profiles for student planning systems.
- When automating course registration checks or grade fetching.
- Targeting universities using E-Registrar (e.g., `oreg3.rmutt.ac.th`, `web.reg.tu.ac.th`, `ces.wu.ac.th`, etc.).

## Technical Architecture & Endpoints
The E-Registrar system is an ASP Classic application with highly standardized endpoints:
- **Base Path:** `https://<domain>/registrar/`
- **Login Landing Page:** `/registrar/login.asp`
- **Auth Endpoint:** `/registrar/validate.asp` (Requires `POST` requests).
- **Study Timetable:** `/registrar/learn_time.asp`
- **Course Catalog Search:** `/registrar/class_info.asp`

### 1. Authentication (`validate.asp`)
To authenticate, issue a POST request to `/registrar/validate.asp` with form parameters:
- `f_uid`: Student ID (e.g., `116510001001-2` for RMUTT)
- `f_pwd`: Password
- `BUILDKEY` (Optional/if present): A hidden validation key often parsed from the HTML of `login.asp`.

A successful login returns session cookies (usually `ASPSESSIONIDXXXXXXXX`) and redirects to `/registrar/home.asp`.

### 2. Scraping Study Timetable (`learn_time.asp`)
Schedules can be queried via:
```
/registrar/learn_time.asp?f_cmd=2&studentid=<student_id>&acadyear=<year>&semester=<semester>
```
*Note: In many configurations, querying another student's ID is blocked unless authenticated as that student or as staff, but some portals allow query access without a session. The scraper should default to an authenticated session.*

## Script Template
This skill provides a helper script under `templates/registrar_scraper.py` containing a robust Python scraper using `requests` and `BeautifulSoup`.

## Common Pitfalls
1. **ASPSESSIONID Expiry:** Session tokens expire quickly. Always perform a health-check query (like requesting `home.asp`) to check if the session is still active.
2. **Encoding Issues:** E-Registrar portals frequently use legacy Thai encoding (`windows-874` / `tis-620`). Make sure to set `response.encoding = 'windows-874'` before reading text content to prevent garbled characters.
3. **HTTP 500 / Timeout Errors:** Legacy IIS servers running ASP Classic are unstable during heavy registration periods. Implement exponential backoff retries.

## Verification Checklist
- [ ] Verify target URL uses the Vision Net E-Registrar system.
- [ ] Test authentication against `/registrar/validate.asp` with mock/real credentials.
- [ ] Confirm parser handles `tis-620` / `windows-874` encoding properly.
- [ ] Ensure extracted data is saved in structured JSON format (courses, time blocks, instructors).
