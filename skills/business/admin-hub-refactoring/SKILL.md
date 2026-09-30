---
name: admin-hub-refactoring
description: Audits and plans a complete e-commerce admin refactoring.
version: 0.1.0
metadata.hermes.tags:
  - Architecture
  - Admin
  - E-Commerce
  - Finance
---

# Admin Hub Refactoring & System Audit

Creates a comprehensive master plan for refactoring an e-commerce or marketplace Admin Hub. It addresses critical missing logic such as real-world financial reporting, tax extraction, DMCA takedowns, KYC user management, and system health monitoring (like email quotas). This skill does NOT write code directly; it performs an audit and generates a specification document.

## When to Use
- "The Admin section lacks proper logic, plan a refactor."
- "Design financial reporting, tax, and moderation for the admin dashboard."
- "Audit the admin platform from a PM and system analyst perspective."

## Prerequisites
- A Next.js e-commerce / marketplace application.
- Existing but incomplete admin routes (e.g., `src/app/[locale]/admin/dashboard`).

## How to Run
Invoke the analysis process through the `terminal` tool to draft a Markdown specification.

## Quick Reference
- Creates `docs/ADMIN_HUB_REFACTOR_SPEC.md`
- Detailed metric formulas & Pareto SQL patterns: see `references/proactive-bi-analytics.md`

## Human Approval Gate (Strict Rule)
When the user requests an audit, refactor plan, or admin overhaul, **output the plan/summary ONLY and wait for explicit human approval before modifying code** ("ห้ามเริ่มทำงานก่อน ให้ฉันตรวจสอบก่อน"). Never start editing files or dispatching execution subagents until the user has reviewed and signed off on the roadmap.

## Procedure

1. **Perform System Audit**
   Analyze current admin dashboard logic using the `terminal` tool:
   ```bash
   ls src/app/\[locale\]/admin/dashboard/
   grep -r "Mock" src/app/\[locale\]/admin/ || true
   ```

2. **Draft the Master Plan Document**
   Write a comprehensive PM-level analysis and roadmap into the `docs` folder using the `terminal` tool:
   ```bash
   cat << "EOF" > docs/ADMIN_HUB_REFACTOR_SPEC.md
   # Admin Hub Refactoring Master Plan

   ## 1. Financial & Tax Reporting (Missing)
   - **Monthly / Annual Tax Reports**: Generate exportable CSV/PDF reports separating Withholding Tax, VAT, Platform Fee, and Net Payable.
   - **Forecasting**: Predict next month's revenue based on rolling averages.
   - **Ledger Adjustments**: Interface to manually credit/debit seller balances for disputes.

   ## 2. Content & DMCA Moderation (Missing)
   - **Copyright Takedown System**: Ability to suspend products post-approval and issue DMCA notices.
   - **Metadata Override**: Admin editor for correcting UPC/ISRC mismatches without seller intervention.
   - **Audit Logs**: Track which admin performed which moderation action.

   ## 3. User & Seller Governance (Missing)
   - **KYC Verification**: Workflow for approving identity documents before granting seller status.
   - **Suspension / Ban Workflow**: Revoke privileges with automated email triggers.

   ## 4. System Health & Infrastructure (Missing)
   - **Email Quota Tracker**: Real-time progress bar for daily SMTP limits (e.g., 500/day).
   - **Webhook & Error Logs**: Surface failed Stripe webhooks directly to the UI.

   ## 5. Platform Configurations (Missing)
   - **Global Settings**: Dynamic commission rate adjustments, maintenance mode toggles.
   EOF
   ```

3. **Establish Execution Timelines and Delegation**
   Do not modify files until the user reviews the generated plan. When approved:
   - Use the `kanban` toolset (`hermes kanban create`, `hermes kanban assign`) to track execution. Break the plan down into distinct smaller tickets rather than one monolithic task.
   - Schedule execution tasks using `hermes cron create` ensuring absolute timestamps are used (e.g. `date -d '+23 hours 10 minutes' +'%Y-%m-%dT%H:%M:%S'`).
   - Use `delegate_task` to assign subsets of the plan to specific subagents (like `db_engineer`, `i18n_frontend_specialist`).

## Pitfalls
- **Over-engineering:** Avoid detailing every single API endpoint in the PM plan; keep it focused on features and architecture.
- **Mock Data Oversight:** Ensure the plan explicitly outlaws hardcoded logic or mock API returns.
- **Unrequested Business Models:** When designing marketplace analytics, strictly respect the business model constraint (e.g. pure digital file sales for single tracks and albums). Do not introduce subscriptions or complex recurring billing models unless explicitly requested.
- **Subagent Rate Limits (HTTP 429):** Fanning out 3+ background subagents concurrently frequently triggers API provider rate limits (429 Resource Exhausted). Cap parallel subagents to a maximum of 2, or serialize execution through the primary agent for multi-file refactoring.
- **Agent Context Limits / Protocol Violations:** Do not assign a single subagent to execute a massive admin overhaul in one phase. The resulting diffs will exceed context bounds and the agent will crash with a `protocol violation` (rc=0 without completion). Break the execution into smaller, targeted phases (e.g., "Phase 3.1 Finance", "Phase 3.2 Moderation") and assign them separately.

## Verification
Verify the document was created successfully:
```bash
cat docs/ADMIN_HUB_REFACTOR_SPEC.md | head -n 10
```