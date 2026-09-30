---
name: data-storytelling-page-launch
description: Plan, design, and automate data storytelling social media pages.
version: 0.2.0
metadata:
  hermes:
    tags:
      - Marketing
      - Facebook
      - DataStorytelling
      - Automation
      - Infographics
---

# Data Storytelling Page Launch & Graphic Automation

Comprehensive workflow for analyzing, designing, and automating data-driven social media pages from initial Facebook OpenGraph reconnaissance to programmatic image/video generation. Strictly focuses on non-political business, lifestyle, technology, and economic metrics.

## When to Use

- "วิเคราะห์เพจและสร้างกลยุทธ์คอนเทนต์ตัวเลข" (Analyze page and devise data storytelling strategy)
- "ออกแบบเทมเพลตอินโฟกราฟิกตัวเลขและสถิติ" (Design statistical infographic templates)
- "สร้างภาพอินโฟกราฟิกแบบมีตัวเลขเติบโต +/- อัตโนมัติ" (Generate programmatic metric cards with +/- growth badges)
- "เพิ่มลายกราฟิกดาว 4 แฉก หรือลายวงจร PCB ให้เทมเพลตดูแกรนด์" (Add 4-point radiant stars, constellations, or circuit traces)
- "จัดวางเลย์เอาต์แนวตั้ง 9:16 สำหรับ Facebook Reels ให้ปลอดภัยจาก Safe Zone" (Layout 9:16 Reels frames compliant with Meta safe zones)

## Prerequisites

- Linux environment with Python 3.10+ and Pillow installed (`pip install Pillow`).
- Free modern loopless Thai sans-serif font installed: **Google Fonts Prompt** (`Prompt-Bold.ttf`, `Prompt-SemiBold.ttf`, `Prompt-Regular.ttf` in `~/.fonts/Prompt/`).
- `curl` available for OpenGraph crawler emulation.
- Reference templates stored in `scripts/`.

## 7-Day Content & Template Architecture

| Day | Pillar | Format & Dimensions | Visual Signature | Focus & Upstream Source |
| :--- | :--- | :--- | :--- | :--- |
| **Mon** | Macro / Pocket Debt | **Template D: The Giant Metric** (4:5, 1080x1350) | 120pt bold hero metric + 4-year progression cards | BOT / NSO debt per capita |
| **Tue** | Real Cost Audit | **Template C: Receipt Breakdown** (4:5, 1080x1350) | Ivory receipt card + red expense deductions | Pantip / Food delivery GP breakdown |
| **Wed** | Pocket Brand Battle | **Template A: The Versus Card** (4:5, 1080x1350) | Split 2-column card + green/red YoY badges | DBD / Retail margin comparisons |
| **Thu** | Career & Income | **Template B: Top 5 Ranking Bar** (4:5, 1080x1350) | Horizontal progress bars + salary range labels | Adecco / GitHub salary & skills |
| **Fri** | Consumer Spending | **Template E: The 4-Card Grid** (4:5, 1080x1350) | 2x2 symmetrical cards + summary total banner | Kasikorn Research / Friday expenses |
| **Sat** | Resource Curation | **Template F: Single Spotlight** (4:5, 1080x1350) | Grand radiant stars + 3-step usage guide | Single GitHub repo / Awesome datasets |
| **Sun** | What-If Simulation | **Template G: SET-Style 2-Column Split** (4:5, 1080x1350) | Side-by-Side Red vs Green + Central VS Badge + Fund Tickers + SEC Box | SET / Morningstar DCA Comparisons |

## AI Content Scoring Gate & Docker DB Pipeline

Before publishing any post to Facebook, content must pass through the automated evaluation pipeline (`scripts/satang_content_evaluator.py`):
- **Dimension 1: Hook Strength (30 pts):** Curiosity opening, high-contrast numbers, Thai culture relevance.
- **Dimension 2: Data Clarity & Sources (30 pts):** Explicit principal/timeframe assumptions, institutional citations (SET, Morningstar, BOT, DBD), scannable bullet formatting.
- **Dimension 3: Community Safety & SEC Compliance (20 pts):** 100% non-political, clean language, mandatory SEC past-performance disclaimer, broad index fund hinting without single-stock solicitation.
- **Dimension 4: Engagement Potential (20 pts):** Open-ended community CTA, 4-8 targeted hashtags, prepared first pinned comment.
- **Publishing Gate:** Total score must be **$\ge 85 / 100$ points** (`is_approved = True`). Posts below 85 are held for refinement.
- **Docker Database Logging:** Approved post metadata, detailed score JSON, and timestamps are persisted to Docker PostgreSQL (`satang-vault-db` container -> `media_studio.facebook_content_evaluations`) for continuous AI feedback loop analysis.

## Thai SEC (IC P1) Compliance Rules

When creating financial comparison or investment content:
1. **No Individual Asset Solicitation:** Never give direct buy/sell recommendations for individual stocks. Focus on broad asset classes or market-cap weighted passive index funds (e.g. SET50, S&P 500 with low fees < 0.5%/year).
2. **Mandatory Standard Disclaimer Box:** Always embed the SEC-compliant disclaimer on the graphic and in the first pinned comment:
   - "คอนเทนต์นี้จัดทำขึ้นเพื่อการศึกษาเปรียบเทียบเชิงสถิติเท่านั้น มิใช่การชักชวน ชี้ชวน หรือให้คำปรึกษาการลงทุน"
   - "ผู้ลงทุนควรทำความเข้าใจลักษณะสินค้า เงื่อนไขผลตอบแทน และความเสี่ยงก่อนตัดสินใจลงทุน | ผลการดำเนินงานในอดีตมิได้เป็นสิ่งยืนยันถึงผลการดำเนินงานในอนาคต"
3. **Data Transparency:** Always cite primary data providers (Morningstar Thailand, SET, Bank of Thailand, Gold Traders Association) with exact sample periods.

## Graphic Design & Visual DNA Standards

1. **Brand Palette:**
   - Deep Navy canvas (`#070D1F` to `#0A1128`).
   - Satang Gold brand accent (`#F5A623`).
   - Electric Cyan secondary accent (`#38BDF8`).
   - Positive Growth / Yield Green (`#00E676`).
   - Expense Surge / Loss Warning Red (`#FF3B30` / `#EF4444`).
2. **Side-by-Side 2-Column Split (SET Reference Architecture):**
   - For 1-on-1 What-If comparisons, avoid stacked vertical boxes that feel long, text-dense, and cluttered.
   - Use a **Side-by-Side 2-Column Split** (Left: Loss/Reality A, Right: Gain/Reality B) with a central floating `VS` badge.
   - Consolidate bottom summary into **ONE single takeaway card** (never stack multiple summary banners + insight callouts together).
3. **Grand Starbursts & Constellation Network:**
   - Mathematical 4-point radiant stars (`✦`) with outer radius `R` and inner radius `R * 0.22`.
   - Subtle 1px constellation lines connecting outer stars, representing Big Data network topologies.
   - Dual-color radiant nebula glows behind top-right focal stars.
4. **Short File Naming Standard:**
   - **Strict Rule:** Never use long descriptive slugs on Google Drive (e.g. `satang-the-value_20261001_whatif_TPL-G_001.png`).
   - **Required Format:** `\mathbf{\{YYYYMMDD\}-\{XXXX\}.png}` (e.g. `20261001-0001.png`, `20261002-0002.png`). Short, clean, auto-sorted by date in Drive. All metadata belongs in PostgreSQL.
5. **Human-Jitter Timing (Anti-Bot Pattern):**
   - Never publish at round hour/minute timestamps (e.g. `16:30:00` or `19:30:00`). Meta's algorithm penalizes robotic cadence.
   - Always apply **Human-Jitter**: randomize the minutes (`random.randint(30, 58)`) and seconds (`random.randint(10, 50)`) so posts publish naturally (e.g. `16:37:35` or `19:54:12`).
6. **Facebook 2026 Algorithm & Social SEO Caption Rules:**
   - **The 125-Character Cliffhanger:** Front-load the hook question in the first 125 characters before the "See More / ...ดูเพิ่มเติม" cut.
   - **Zero External Links in Body:** Never put URLs or affiliate links in the main caption; Meta's algorithm drastically deprioritizes posts with outbound links in the caption. Place all links exclusively in the **First Pinned Comment**.
   - **Social SEO Density:** Naturally embed high-volume search terms (หวย, กองทุนรวม, ดอกเบี้ยทบต้น, DCA, ออมเงิน, แผนการเงิน).
   - **Meaningful Social Interaction (MSI) CTA:** Conclude with an open-ended conversational debate prompt to stimulate comments in the first 15 minutes.
7. **Anti-Duplication Guard (SHA-256 & 45-Day Cooldown):**
   - Normalize Thai topic text (remove punctuation, stop words, whitespace) and generate SHA-256 hash.
   - Check `facebook_content_evaluations`: if matching hash was published within 45 days, reject generation and rotate topic.

## 0-Token Prefect Autonomous Operations

All mechanical, repetitive operations run via Python Prefect without calling LLMs (0 Tokens / $0 cost):
- **Flow 1: Open Upstream APIs Harvester (Daily 05:00 AM):** Pulls free exchange rates, World Bank GDP, GitHub AI repos, Open-Meteo climate data into `upstream_api_feeds`.
- **Flow 2: Pantip Forum Harvester (Every 6h: 00, 06, 12, 18):** Scrapes hot topics from Pantip (Silom, Sinthorn, Food) with numeric keywords into `pantip_trending_topics`.
- **Flow 3: Morning Executive Briefing (Daily 07:30 AM):** Aggregates today's plan, pending reviews, and 24h token costs, delivering HTML card to Telegram bot (`@satang_notifications_bot`).
- **Flow 4: Auto-Publisher Sweeper (Every 15m):** Queries PostgreSQL for `human_approval_status = 'APPROVED_BY_USER'` and `scheduled_at <= NOW()`. Pushes to Meta Graph API and pins first comment with 0 LLM tokens. On lazy days when user doesn't approve, the sweeper sleeps silently.

## Procedure

1. **Reconnaissance & Brand Ingestion:**
   Inspect target Facebook page metadata using curl with crawler user-agent:
   ```bash
   curl -sL -A "facebookexternalhit/1.1" "<PAGE_URL>" | grep -o -E '<title>[^<]+</title>|<meta property="og:[^"]+" content="[^"]+"'
   ```
2. **Execute Python Graphic Script:**
   Render the required day's template using the corresponding script in `scripts/`:
   ```bash
   python3 scripts/satang_template_f_grand_stars.py
   python3 scripts/satang_template_g_whatif.py
   ```
3. **Vision QA Gate:**
   Invoke `vision_analyze` on the rendered `.png` to check:
   - Text bounding boxes (zero word clipping or border collisions).
   - Thai diacritics and tone mark alignment.
   - Color contrast ratio against dark navy canvas.
   - Reels safe-zone compliance (for 9:16 assets).

## Pitfalls

- **PIL Long Text Overflow & Footer Collision:** Unlike browser DOMs, PIL `draw.text()` does not wrap lines automatically. Always calculate line width (`font.getbbox()`) so text fits within container padding (<890px on 1080px canvas). Keep sentences short and punchy; long compound sentences cause border collisions and reading fatigue. Never place long footer sources and social handles on the same baseline without verifying their combined width, which causes ugly double-layer text ghosting.
- **SEC / IC P1 Regulatory Violations:** Mentioning specific stocks without an investment consultant license risks severe regulatory action from the SEC (ก.ล.ต.). Always frame comparisons around broad passive index funds (SET50 / S&P 500) and strictly embed the mandatory disclaimer.
- **Unverified Post Auto-Publishing:** Never push posts directly to Meta Graph API without executing the pre-publish scoring script. Any score below 85% must be revised first.
- **Information Overload in Curations:** Listing 5+ resources on a single mobile image causes cognitive friction. Always feature ONE single high-value spotlight repository with an actionable 3-step guide.
- **Badge Color Inconsistency:** When presenting expenses or financial drains, avoid green badges for positive percentage growth (`▲ +18%`); use warning red (`#FF3B30`) to represent money leaving the pocket.

## Verification

Run verification probe against the template render suite:
```bash
python3 -c "from PIL import Image; img=Image.open('/home/thaieasyvps/satang_template_g_whatif.png'); assert img.size == (1080, 1920); print('VERIFIED_REELS_916')"
```
Output `VERIFIED_REELS_916` proves the 9:16 vertical high-resolution asset renders correctly.