# Marketplace Multi-Persona Audit & Architecture Framework

When evaluating or designing digital asset marketplaces (e.g. music, audio files, sheet music, creative assets), system audits must be conducted through four distinct operational personas.

---

## 1. The 4 Operational Personas

### 🧑‍💼 Persona 1: Platform Operator & Admin
**Core Mindset:** Risk control, proactive issue resolution, system health, and legal compliance.
- **Triage Action Center (Top of Screen):** Immediate visibility into high-friction items:
  - Pending copyright/DMCA takedowns with one-click suspension.
  - Pending creator/seller KYC applications.
  - Failed payment webhooks or stuck payout requests.
- **Risk & Fraud Radar:**
  - Seller anomaly tracking: high refund rates (>10-15%).
  - Unusual velocity spikes in orders from single IPs/cards.
- **Infrastructure & Cost Monitoring:**
  - Storage consumption (MinIO / S3 bucket size or database byte aggregates).
  - Outgoing email quota tracking (e.g. SMTP free tier 500/day limit with Green/Yellow/Red visual progress).
- **Governance Tools:**
  - Granular account bans (`isBanned: boolean`) with automatic session invalidation.
  - Emergency metadata overrides for UPC/ISRC mismatches without waiting for creator edits.

### 🎧 Persona 2: Music Buyer & Customer
**Core Mindset:** Low friction, trust, instant gratification, and legal safety for commercial use.
- **Global Persistent Audio Player:**
  - Music playback must survive client-side route transitions (wrap application layout with React Context `AudioPlayerProvider`).
  - Docked bottom scrubber with sample-accurate playback, scrub bar, and quick link to release detail.
- **Deliverables & Specification Transparency:**
  - Prominent card stating exact file formats (e.g. WAV 24-bit 44.1kHz Lossless, MP3 320kbps CBR, PDF 300DPI), file size, and delivery mode (instant download).
- **Clear Licensing Terms:**
  - Explicit checklist of rights: Worldwide Commercial & Sync Rights (YouTube, Games, Podcasts) ✓, 100% Royalty-Free Monetization ✓, Standalone Resale Prohibited ✗.
- **Mobile Sticky Purchase Bar:**
  - Fixed bottom bar on viewports `< 1024px` showing price and "Get Release / Buy" button so buyers don't have to scroll past long tracklists and credits.
- **Automated License Certificates:**
  - Dedicated printable HTML/PDF route (`/api/buyer/license/[orderId]`) detailing Licensee, Licensor, Asset Title, ISRC, Order ID, and terms for copyright dispute clearance.

### 🎤 Persona 3: Music Seller & Creator
**Core Mindset:** Financial trust, sales transparency, upload velocity, and rights management.
- **Financial Trust & Payout Setup (Most Critical):**
  - Never display a locked payout screen without an active destination setup. Provide PromptPay / Thai Bank account forms or Stripe Connect Express onboarding.
  - Transparent payout statement ledger: Pending vs Completed transfers with date, amount, and reference slips.
- **Granular Track Analytics:**
  - Top earning releases widget on the dashboard.
  - Per-track view/play/download breakdown for multi-track albums.
- **DDEX Standard Upload Wizard:**
  - 6-step wizard separating Release-level metadata (Album title, UPC, 1:1 artwork, Label) from Track-level metadata (ISRC, audio files, custom preview scrubber).
  - Multi-contributor role assignment (Composer, Producer, Sound Engineer, Instrumentalist).
  - Saved Contributor Presets: reuse previously entered artist identities across new releases.

### 📊 Persona 4: Data Scientist & BI Analyst
**Core Mindset:** Value realization, data-driven strategy, and non-distorted reporting.
- **Executive BI Metrics:**
  - **GMV (Gross Merchandise Value):** Real-time sum of completed orders.
  - **Effective Take Rate:** `(Platform Fee / GMV) * 100`.
  - **Refund Rate:** `Refunds / Total Orders (%)` with healthy target `< 2%`.
  - **Run-Rate & Forecast:** 30-day moving average daily sales multiplied by 30 days.
- **Pareto Insights (80/20 Rule):**
  - Top 10 Releases ranked by revenue.
  - Top 10 Creators ranked by GMV contribution.
- **Business Model Adherence:**
  - Never fabricate subscription metrics if the platform strictly licenses digital files (single tracks & albums). Segment sales by file granularity (Tracks vs Full Albums).

---

## 2. The Human Approval Gate (Strict Protocol)

Whenever evaluating a platform with these personas:
1. Conduct the audit and synthesize findings per persona.
2. Present the gap analysis and proposed roadmap (Tasks & Subtasks).
3. **DO NOT MODIFY CODE OR DISPATCH SUBAGENTS** until the user explicitly responds with approval ("ห้ามเริ่มทำงานก่อน").
4. Translate approved items into `hermes kanban` tickets, assign to active profile, and execute with capped subagent concurrency (max 2 parallel).
