# Enterprise Social Media Architecture & 6-Table PostgreSQL Schema

Complete production schema and orchestration specifications for multi-page automated content operations.

## Database Schema (Database: `media_studio` in `satang-vault-db`)

### 1. `managed_pages` (Single Source of Truth for Page Configs)
Replaces brittle local JSON configuration files. Stores brand identity, color tokens, font configurations, and compliance rules:
- `page_code` VARCHAR(50) UNIQUE (e.g. `satang-the-value`)
- `page_name` VARCHAR(150)
- `category` VARCHAR(100)
- `positioning` TEXT
- `tone_of_voice` TEXT
- `content_pillars` JSONB (Array of active content pillars)
- `posting_schedule` JSONB (Day-of-week target posting hours)
- `visual_ci` JSONB (Hex color codes, font families, signature motifs, logo path)
- `quality_gate_weights` JSONB (`{"hook": 30, "clarity": 30, "safety": 20, "engagement": 20, "min_score": 85}`)
- `negative_words` JSONB (Array of forbidden words to avoid shadowbans)
- `compliance_rules` JSONB (SEC/IC disclosure mandates)
- `gdrive_folder_id` VARCHAR(100)
- `gdrive_folder_link` VARCHAR(255)

### 2. `facebook_content_evaluations` (Content & Quality Audit Log)
Captures every draft, score breakdown, granular token measurement, and approval lifecycle:
- `page_id` INT REFERENCES `managed_pages(id)`
- `headline` VARCHAR(255)
- `caption` TEXT
- `pinned_comment` TEXT
- `image_path` VARCHAR(255)
- `gdrive_file_id` VARCHAR(100)
- `gdrive_file_name` VARCHAR(255) (Enforces `{YYYYMMDD}-{XXXX}.png`)
- `gdrive_web_view_link` TEXT
- `tokens_research_prompt` / `tokens_research_completion` INT
- `tokens_caption_prompt` / `tokens_caption_completion` INT
- `tokens_evaluation_prompt` / `tokens_evaluation_completion` INT
- `total_prompt_tokens` / `total_completion_tokens` / `total_tokens` INT
- `estimated_cost_usd` NUMERIC(10,6)
- `hook_score` (0-30), `clarity_score` (0-30), `safety_score` (0-20), `engagement_score` (0-20)
- `total_score` INT (0-100)
- `human_approval_status` VARCHAR(50) (`PENDING_REVIEW`, `APPROVED_BY_USER`, `REJECTED_BY_USER`, `REVISION_REQUESTED`)
- `approved_by` VARCHAR(100)
- `approved_at` TIMESTAMP WITH TIME ZONE
- `revision_count` INT
- `revision_history` JSONB
- `scheduled_at` TIMESTAMP WITH TIME ZONE (With randomized human-jitter minutes)
- `published_status` VARCHAR(50) (`PENDING`, `APPROVED_READY_TO_POST`, `PUBLISHED`, `CANCELLED`)
- `fb_post_id` VARCHAR(100)

### 3. `content_calendar_plans` (30-90 Day Rolling Planning Pipeline)
- `page_id` INT REFERENCES `managed_pages(id)`
- `plan_date` DATE
- `plan_time` TIME
- `day_of_week` VARCHAR(20)
- `pillar` VARCHAR(100)
- `template_type` VARCHAR(50)
- `topic_idea` VARCHAR(255)
- `data_source` VARCHAR(255)
- `status` VARCHAR(50) (`PLANNED`, `GENERATED`, `PENDING_REVIEW`, `APPROVED`, `PUBLISHED`)
- `evaluation_id` INT REFERENCES `facebook_content_evaluations(id)`

### 4. `publishing_jobs` (Execution Queue & Rate Limiter)
- `evaluation_id` INT
- `page_id` INT
- `status` (`QUEUED`, `RUNNING`, `COMPLETED`, `FAILED`, `RETRYING`)
- `attempt_count` / `max_attempts` INT
- `graph_api_endpoint` VARCHAR(255)
- `response_payload` JSONB
- `error_message` TEXT

### 5. `token_ledger` (Financial Accounting by Page & Month)
- `page_id` INT
- `evaluation_id` INT
- `model_name` VARCHAR(100)
- `total_tokens` INT
- `cost_usd` NUMERIC(10,6)
- `cost_thb` NUMERIC(10,4)
- `billing_cycle` VARCHAR(7) (e.g. `2026-09`)

### 6. `analytics_snapshots` (Closed-Loop Performance Feedback)
- `evaluation_id` INT
- `fb_post_id` VARCHAR(100)
- `snapshot_interval` (`1H`, `6H`, `24H`, `48H`, `7D`, `30D`)
- `reach`, `impressions`, `reactions`, `comments`, `shares`, `saves`, `clicks` INT

## Closed-Loop Feedback Engine Architecture (Post-Publish Adaptive Optimization)

The closed-loop system consists of two distinct stages:

```
[ Pre-Publish Quality Gate ] -> [ Human Approval ] -> [ Publisher ]
                                                          |
                                                          v
                                                   [ Facebook Post ]
                                                          |
  +-------------------------------------------------------+
  | (Every 6h / 24h via Flow 5)
  v
[ Meta Graph Insights API ] -> Sync to `analytics_snapshots`
                                       |
                                       v
[ Engagement & Comment Analyzer ] -> Sentiment & Topic Cluster (FAQ / Critique / Praise)
                                       |
                                       v
[ Performance Score Update ] ------> `facebook_content_evaluations.perf_score`
                                       |
                                       v
[ Prompt & Pillar Weight Adaptor ] -> Adjusts future research/hook prompt weighting:
                                      - Boost winning pillars (high share/save ratio)
                                      - Refine hooks matching high engagement styles
                                      - Flag confusion/questions for follow-up content
```

### Feedback Dimensions & Adjustment Rules
1. **Virality & Value Ratio (`Shares + Saves` / `Reach`)**:
   - $\ge 2.5\%$: Mark pillar and headline structure as HIGH_PERFORMER, boost frequency in `content_calendar_plans`.
   - $< 0.8\%$: Flag for angle revision or hook restructuring.
2. **Comment Sentiment & Intent Analysis**:
   - Questions/Debate: Extract recurring inquiries into topics for future What-If / Versus posts.
   - Confusion/Objections: Automatically tighten the Clarity & Assumption guidelines for that topic.
3. **Reaction Distribution**:
   - High Haha/Angry without virality indicates controversial framing or misinterpretation; triggers automatic tone dampening in prompt.
