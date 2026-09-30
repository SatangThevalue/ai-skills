# 0-Token Prefect Architecture & Multi-Tenant Database Schema

This reference outlines the production database schema and zero-token Prefect worker pipelines deployed for 'Satang The Value : เล่า DATA'.

## Docker PostgreSQL Schema (`satang-vault-db` / `media_studio`)

### 1. `managed_pages` (Multi-Tenant Page Registry)
- `id`: Primary Key
- `page_code`: Unique slug (e.g. `satang-the-value`)
- `page_name`: Display name
- `platform`: Target platform (default `FACEBOOK`)
- `positioning`, `tone_of_voice`, `target_audience`: Strategy pillars
- `content_pillars` (JSONB): Array of approved pillars
- `posting_schedule` (JSONB): Weekly posting times
- `visual_ci` (JSONB): Hex colors, font family, logo path, motifs
- `gdrive_folder_id`, `gdrive_folder_link`: Master Drive folder integration
- `negative_words` (JSONB): Shadowban protection list
- `compliance_rules` (JSONB): SEC IC P1 disclaimer guidelines

### 2. `content_calendar_plans` (30-90 Day Rolling Schedule)
- `id`: Primary Key
- `page_id`: Foreign Key referencing `managed_pages(id)`
- `plan_date`: Target date (YYYY-MM-DD)
- `plan_time`: Base time (e.g. 19:30:00)
- `day_of_week`: Day name (Monday - Sunday)
- `pillar`: Content pillar
- `template_type`: Graphic template code (e.g. `TPL-G_SET_SPLIT`)
- `topic_idea`: Headline concept
- `data_source`: Institutional data provider
- `status`: `PLANNED`, `PENDING_REVIEW`, `APPROVED`, `PUBLISHED`
- `evaluation_id`: Foreign Key referencing `facebook_content_evaluations(id)`
- `content_hash`: SHA-256 topic signature for deduplication

### 3. `facebook_content_evaluations` (Content & Telemetry Ledger)
- `id`: Primary Key
- `page_id`: Foreign Key referencing `managed_pages(id)`
- `headline`, `caption`, `pinned_comment`: Complete post text
- `gdrive_file_id`, `gdrive_file_name`, `gdrive_web_view_link`: Google Drive metadata
- `hook_score` (30), `clarity_score` (30), `safety_score` (20), `engagement_score` (20): Total score (100)
- `is_approved`: Boolean (`total_score >= 85`)
- `human_approval_status`: `PENDING_REVIEW`, `APPROVED_BY_USER`, `REJECTED_BY_USER`, `REVISION_REQUESTED`
- `scheduled_at`: Timestamp with human-jitter randomized minutes
- `content_hash`: SHA-256 normalized hash
- `cooldown_until`: Timestamp locking topic from repeat for 45 days
- `total_tokens`, `estimated_cost_usd`: Granular financial accounting

## Automated Prefect 0-Token Flows

1. **`satang_prefect_open_apis_harvester.py` (Daily 05:00 AM):**
   - Fetches Open Exchange Rates, World Bank Open API, GitHub REST, and Open-Meteo.
   - Upserts into `upstream_api_feeds`. Consumes 0 LLM tokens.
2. **`satang_prefect_pantip_harvester.py` (Every 6h: 00, 06, 12, 18):**
   - Scrapes hot threads with numeric keywords from Silom, Sinthorn, and Food rooms.
   - Upserts into `pantip_trending_topics`. Consumes 0 LLM tokens.
3. **`prefect_morning_briefing.py` (Daily 07:30 AM):**
   - Dispatches daily executive briefing card to Telegram bot (`@satang_notifications_bot`).
   - Includes today's plan, pending review count, and 24h token costs. Consumes 0 LLM tokens.
4. **`satang_prefect_sweeper.py` (Every 15m):**
   - Queries `facebook_content_evaluations` where `human_approval_status = 'APPROVED_BY_USER'` and `scheduled_at <= NOW()`.
   - Dispatches approved posts to Meta Graph API and pins first comment. Sleeps silently on idle ticks (0 tokens).
