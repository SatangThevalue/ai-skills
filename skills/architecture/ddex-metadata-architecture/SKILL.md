---
name: ddex-metadata-architecture
description: Refactors flat music metadata into relational DDEX standards.
version: 0.1.0
metadata.hermes.tags:
  - Architecture
  - Database
  - Music
  - Nextjs
---

# DDEX Metadata Relational Architecture

Converts flat schema models (where track-level data is incorrectly stored at the release level) into the standard music industry relational model used by Believe and DDEX. It splits releases and tracks, introduces Many-to-Many contributors, and separates localization definitions. This skill does not implement UI changes directly, but lays the database and localization foundation.

## When to Use
- "Fix the metadata placement for tracks and albums."
- "Refactor the database schema to comply with DDEX or Believe standards."
- "Move ISRC and lyrics to the track level."

## Prerequisites
- A Next.js application using Drizzle ORM and PostgreSQL.
- Legacy `product` and `productTrack` schemas present.
- Python 3 for localization script generation.

## How to Run
Execute the procedure steps using `terminal` and `patch` tools to draft the architecture before applying database migrations.

## Quick Reference
- `product`: Keep UPC/EAN, Release Title, Release Date.
- `productTrack`: Add ISRC, Track Type (original/cover), Lyrics.
- `contributor`: New table for artist profiles.
- `trackContributorRole`: New table linking track to contributor with a specific role.

## Financial & System Metrics (Admin Hub)
When designing the administrative view of a DDEX/Marketplace system, the overview dashboard MUST include actionable metrics, not just counts. Standard widgets:
- **Email Quota Tracker:** Avoid silent failures. Example: "Daily Gmail Quota: X/500". Tracked via an `emailLog` table.
- **Financial Overview:** Display "Monthly Revenue", "Net Income", "Pending Payouts", "Platform Commission", and "Sellers Share".
- **System Monitoring/Action Required:** Alerts for failed webhooks, refunds requested, or unapproved seller requests.

## Procedure

1. **Analyze and Draft the Spec**
   Read current database schema using `read_file`. Draft a Markdown spec explaining the metadata migration from flat to relational. Write the spec to the `docs/` folder using `terminal`:
   ```bash
   cat << "EOF" > docs/METADATA_REFACTOR_SPEC.md
   # METADATA REFACTORING SPECIFICATION
   ...
   EOF
   ```

2. **Patch Drizzle Schema**
   Back up the schema first using `terminal`:
   ```bash
   cp src/db/schema.ts src/db/schema.backup.ts
   ```
   Append the new relational tables (`contributor`, `trackContributorRole`) to `src/db/schema.ts` using `terminal`:
   ```bash
   cat << "EOF" >> src/db/schema.ts
   export const contributor = pgTable("contributor", {
   	id: text("id").primaryKey(),
   	sellerId: text("sellerId").notNull().references(() => user.id, { onDelete: 'cascade' }),
   	name: text("name").notNull(),
   });

   export const trackContributorRole = pgTable("trackContributorRole", {
   	id: text("id").primaryKey(),
   	trackId: text("trackId").notNull().references(() => productTrack.id, { onDelete: 'cascade' }),
   	contributorId: text("contributorId").notNull().references(() => contributor.id, { onDelete: 'cascade' }),
   	role: text("role").notNull(),
   	instrument: text("instrument"),
   });
   EOF
   ```
   Use `patch` to remove or deprecate (comment out) track-level fields (e.g., `isrc`, `vocalLanguage`, `explicitRating`) from the `product` (Release) level in `schema.ts`.

3. **Inject Localization Keys**
   Write a Python script via `terminal` to inject new translation keys for UI elements (e.g., Track Types, Lyrics Status, Add Contributor buttons) into `.json` dictionary files:
   ```bash
   cat << "EOF" > scripts/update_translations.py
   import json
   def update_json(filepath):
       with open(filepath, 'r', encoding='utf-8') as f:
           data = json.load(f)
       data["UploadWizard"].update({
           "track_type_original": "Original",
           "add_role_btn": "+ ADD ANOTHER ROLE"
       })
       with open(filepath, 'w', encoding='utf-8') as f:
           json.dump(data, f, ensure_ascii=False, indent=2)
   update_json('messages/en.json')
   EOF
   python3 scripts/update_translations.py
   ```

4. **Establish Admin Hub Financial & Quota Metrics**
   Integrate an `emailLog` table or quota counter to prevent reaching SMTP limits (e.g., 500/day for free Gmail). Surface financial summaries (Platform Fee, Net Revenue, Sellers Share) from the database (`order`, `platformTransaction` tables) into the primary Admin Overview.

5. **Verify Database Push**
   Validate the schema via Drizzle CLI through the `terminal` tool.
   ```bash
   npx dotenv-cli -e .env.local -- npm run db:push
   ```

## Pitfalls
- **Breaking Changes:** Removing fields like `isrc` from `product` can break existing production queries. Always comment out or deprecate fields first before doing a destructive migration.
- **Port Collisions:** Ensure PostgreSQL docker instances don't clash on port 5432 during testing.
- **Missing Locales:** If keys are injected into `en.json` but not others (like `th.json`), the UI might crash or show raw string keys.

## Verification
Inspect the schema file to ensure `contributor` tables exist and verify the translation files contain the new keys.
```bash
grep -n "trackContributorRole" src/db/schema.ts
```