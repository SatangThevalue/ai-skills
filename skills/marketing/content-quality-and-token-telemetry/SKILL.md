---
name: content-quality-and-token-telemetry
description: Audit content quality and log token telemetry in DB.
version: 0.1.0
metadata:
  hermes:
    tags:
      - Marketing
      - Telemetry
      - PostgreSQL
      - Docker
      - QualityGate
---

# Content Quality & Token Telemetry

Automated quality scoring gate and full-lifecycle telemetry pipeline for social media content. It audits post copy across 4 dimensions (100-point scale), enforces a quality threshold before publishing, tracks granular token consumption per production component, and persists structured audit records into a Dockerized PostgreSQL database for continuous performance feedback. It does not handle direct financial advisory or uninspected single-stock recommendations.

## When to Use

- "ประเมินคอนเทนต์และเก็บข้อมูลลงฐานข้อมูล Docker" (Evaluate content and save to Docker DB)
- "ตรวจคะแนนคอนเทนต์ก่อนโพสต์ลง Facebook" (Audit content quality before posting to Facebook)
- "บันทึกการใช้ token แยกแต่ละส่วนของคอนเทนต์" (Log granular token usage per content component)
- "สร้าง Quality Gate สำหรับคัดกรองแคปชันและภาพ" (Build a quality gate for caption and image screening)
- "ประเมินและปรับปรุงคอนเทนต์ตามคอมเมนต์และรีแอคของผู้ติดตาม" (Evaluate and adapt content using post-publish comments and reactions)

## Prerequisites

- Linux host running Docker with a PostgreSQL container (e.g. `satang-vault-db` running database `media_studio`).
- Python 3.10+ with `Pillow` installed (`pip install Pillow`).
- PostgreSQL client access via `docker exec -i satang-vault-db psql -U admin -d media_studio`.
- Read and execute permissions on `scripts/content_evaluator.py`.

## How to Run

1. Ensure the 6 enterprise tables exist in Docker PostgreSQL using `terminal`. Detailed schema in `references/enterprise-architecture.md`.
2. Execute quality evaluation and telemetry logging via `terminal` invoking `scripts/content_evaluator.py`.
3. Sync approved graphic assets to Google Drive using patterns in `references/google-drive-and-community-rules.md`.
4. Dispatch approved posts to the publishing queue via `terminal` invoking `scripts/publisher_engine.py`.
5. Query the audit record in Docker PostgreSQL using `terminal` to verify approval and token accounting.

## Quick Reference

| Action | Hermes Tool | Command / Endpoint |
| :--- | :--- | :--- |
| Ensure DB Tables | `terminal` | `docker exec -i satang-vault-db psql -U admin -d media_studio -c "\dt"` |
| Run Evaluator | `terminal` | `python3 scripts/content_evaluator.py` |
| Execute Publisher | `terminal` | `python3 scripts/publisher_engine.py <EVALUATION_ID>` |
| Run 0-Token Sweeper | `terminal` | `python3 scripts/prefect_sweeper.py` |
| Inspect Audit Row | `terminal` | `docker exec -i satang-vault-db psql -U admin -d media_studio -c "SELECT id, total_score, total_tokens, estimated_cost_usd, human_approval_status, is_approved FROM facebook_content_evaluations ORDER BY id DESC LIMIT 1;"` |
| View 30-Day Plan | `terminal` | `docker exec -i satang-vault-db psql -U admin -d media_studio -c "SELECT id, plan_date, day_of_week, pillar, topic_idea, status FROM content_calendar_plans ORDER BY id ASC LIMIT 7;"` |
| Inspect Token Ledger | `terminal` | `docker exec -i satang-vault-db psql -U admin -d media_studio -c "SELECT * FROM token_ledger ORDER BY id DESC LIMIT 1;"` |

## Procedure

1. **Verify Database Table Schema**
   Ensure the audit table exists in Docker PostgreSQL with all asset, token, and scoring columns:
   ```bash
   docker exec -i satang-vault-db psql -U admin -d media_studio -c "
   CREATE TABLE IF NOT EXISTS facebook_content_evaluations (
       id SERIAL PRIMARY KEY,
       page_id INT REFERENCES managed_pages(id),
       page_name VARCHAR(100) DEFAULT 'Satang The Value : เล่า DATA',
       pillar VARCHAR(100) NOT NULL,
       headline VARCHAR(255) NOT NULL,
       caption TEXT NOT NULL,
       pinned_comment TEXT,
       image_path VARCHAR(255),
       gdrive_file_id VARCHAR(100),
       gdrive_file_name VARCHAR(255),
       gdrive_web_view_link TEXT,
       template_type VARCHAR(50),
       aspect_ratio VARCHAR(20) DEFAULT '4:5',
       image_dimensions VARCHAR(30) DEFAULT '1080x1350',
       image_file_size_kb NUMERIC(10,2),
       source_data_origin VARCHAR(255),
       raw_dataset JSONB,
       tokens_research_prompt INT DEFAULT 0,
       tokens_research_completion INT DEFAULT 0,
       tokens_caption_prompt INT DEFAULT 0,
       tokens_caption_completion INT DEFAULT 0,
       tokens_evaluation_prompt INT DEFAULT 0,
       tokens_evaluation_completion INT DEFAULT 0,
       total_prompt_tokens INT DEFAULT 0,
       total_completion_tokens INT DEFAULT 0,
       total_tokens INT DEFAULT 0,
       llm_model VARCHAR(100) DEFAULT 'gemini-2.5-flash',
       estimated_cost_usd NUMERIC(10,6) DEFAULT 0,
       generation_latency_seconds NUMERIC(6,2) DEFAULT 0,
       hook_score INT CHECK (hook_score BETWEEN 0 AND 30),
       clarity_score INT CHECK (clarity_score BETWEEN 0 AND 30),
       safety_score INT CHECK (safety_score BETWEEN 0 AND 20),
       engagement_score INT CHECK (engagement_score BETWEEN 0 AND 20),
       total_score INT CHECK (total_score BETWEEN 0 AND 100),
       evaluation_details JSONB,
       is_approved BOOLEAN DEFAULT FALSE,
       human_approval_status VARCHAR(50) DEFAULT 'PENDING_REVIEW',
       published_status VARCHAR(50) DEFAULT 'PENDING',
       fb_post_id VARCHAR(100),
       created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
   );
   "
   ```

2. **Asset Naming Standard**
   Strictly enforce the short naming convention: `{YYYYMMDD}-{XXXX}.png` (e.g. `20261001-0001.png`). Do not include verbose topic slugs or page codes in the filename; all semantic attributes are stored in PostgreSQL.

2. **Assemble Post Payload & Granular Token Metrics**
   Gather the draft components: headline, 4-part caption, pinned comment with SEC disclaimer, rendered image path, and component token measurements:
   - Research & Data Ingestion (Prompt + Completion)
   - Caption & Copywriting (Prompt + Completion)
   - Scoring & Quality Audit (Prompt + Completion)

3. **Execute Evaluation Engine & Store in Docker DB**
   Run the evaluation script via `terminal`:
   ```bash
   python3 scripts/content_evaluator.py
   ```
   The engine scores the draft against the 4-dimension rubric (Hook 30, Clarity 30, Safety 20, Engagement 20). If `total_score >= 85`, it sets `is_approved = True`, calculates estimated LLM cost, and inserts the full row into `media_studio.facebook_content_evaluations`.

4. **Verify Database Persistence & Audit Approval**
   Query PostgreSQL in the Docker container to confirm the record was inserted:
   ```bash
   docker exec -i satang-vault-db psql -U admin -d media_studio -c "
   SELECT id, headline, total_score, total_tokens, estimated_cost_usd, is_approved, published_status 
   FROM facebook_content_evaluations ORDER BY id DESC LIMIT 1;
   "
   ```

## Pitfalls

- **Confusing Pre-Publish Quality Gate with Post-Publish Closed-Loop Feedback:** Pre-publish scoring (`content_evaluator.py` evaluating Hook, Clarity, Safety, Engagement heuristics) predicts quality before publication; it is NOT the closed-loop feedback system. Real optimization requires post-publish sync via Flow 5 (`analytics_snapshots` tracking real Reactions, Shares, and Comments from Meta Graph API) and feeding high-performing pillars/hooks back into the prompt generation engine.
- **Verbose File Naming & Lack of Clean Standards:** Naming assets with redundant page codes or long Thai titles creates clutter on Google Drive. Always use the ultra-short standard: `{YYYYMMDD}-{XXXX}.png` (e.g. `20261001-0001.png`), storing descriptive metadata inside PostgreSQL instead.
- **Burning Agent Tokens on Mechanical Polling:** Using LLM agent loops to poll database timestamps ("Is it 19:30 yet?") wastes tokens. Always decouple mechanical execution to a Python Prefect flow (`scripts/prefect_sweeper.py`) which runs natively on schedule and consumes **0 LLM tokens**.
- **Violating the Lazy vs Active Approval Model:** Never auto-publish a post simply because its score is $\ge 85$. Posts must remain in `PENDING_REVIEW` until the human explicitly marks them `APPROVED_BY_USER`. If the human is inactive or does not approve, the automated publisher must remain 100% idle.
- **Loose JSON Config Drift:** Storing multi-page brand configurations or tokens in local JSON files leads to fragmented state, credential leaks, and sync bugs. Always persist page configs into `managed_pages` and credentials into `page_credentials` inside PostgreSQL.
- **Visual Clutter & Information Overload:** Stacking 5+ dense cards, 15+ stars, and long text walls causes mobile drop-off. Enforce the 2-second rule: 1-on-1 side-by-side contrast (e.g. Red Loss vs Green Gain), 3-4 accent stars max, and massive whitespace.
- **Emoji Tofu & Line Overflows in PIL:** Default PIL bitmap fonts drop Thai characters and emojis, creating square "tofu" boxes `[]`. Always load explicit Google Fonts TTF (Prompt/Kanit). Never place raw emojis in text. Pre-calculate line widths using `font.getbbox(text)` to prevent border collisions.
- **Blanket Auto-Replying to Comments:** Triggering an LLM call for every user comment (emojis, stickers, compliments like "👍" or "ขอบคุณครับ") burns tokens pointlessly and makes the page appear spammy. Enforce Smart High-Intent Filtering: ignore superficial comments and cap AI responses to 3-5 high-value questions per post (<0.05 THB/post), as detailed in `references/google-drive-and-community-rules.md`.
- **Direct Port 5432 Auth Failures:** Connecting directly to `100.115.66.121:5432` or `localhost:5432` from host Python can encounter MD5/SCRAM password mismatches if credentials drift. Always route database queries through `docker exec -i satang-vault-db psql -U admin -d media_studio` over the local socket for zero-credential breakage.
- **SQL Quote Escaping in Captions:** Thai social captions frequently contain quotes (`"` and `'`). Never interpolate raw strings directly into SQL strings without doubling single quotes (`.replace("'", "''")`) or encoding JSON payloads properly.
- **SEC / IC P1 Compliance Violation:** Mentioning specific stocks or mutual funds without a mandatory risk warning ("ผลการดำเนินงานในอดีตมิได้เป็นสิ่งยืนยันถึงผลการดำเนินงานในอนาคต") triggers an instant deduction in Dimension 3 (Safety) and blocks automated posting.

## Verification

Run this one-line command through `terminal` to verify the evaluation pipeline and DB connection:
```bash
docker exec -i satang-vault-db psql -U admin -d media_studio -c "SELECT COUNT(*) FROM facebook_content_evaluations WHERE is_approved = TRUE;" | grep -q "[1-9]" && echo "TELEMETRY_PIPELINE_OK"
```
The check outputs `TELEMETRY_PIPELINE_OK` when at least one approved post evaluation is stored in the Docker database.