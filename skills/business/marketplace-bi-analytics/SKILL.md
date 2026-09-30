---
name: marketplace-bi-analytics
description: Calculates marketplace GMV, take rate, and sales forecasts.
version: 0.1.0
metadata.hermes.tags:
  - Analytics
  - Business
  - Nextjs
  - Drizzle
---

# Marketplace BI & Revenue Analytics

Calculates real-time executive metrics including GMV, effective take rate, 30-day moving average forecasting, and Pareto distributions for digital asset marketplaces. It replaces hardcoded or client-side mock data with direct relational SQL aggregations. It does NOT manage user subscriptions or external accounting ledger syncs.

## When to Use
- "Build executive BI dashboard for marketplace."
- "Calculate real GMV, take rate, and revenue forecast."
- "Analyze top sellers and product sales distribution."
- "Replace mock sales data with real database analytics."

## Prerequisites
- Next.js App Router project with Drizzle ORM and PostgreSQL.
- Database tables: `order` (with `amount`, `platformFee`, `status`, `createdAt`, `trackId`, `productId`), `product`, `user`, and `platformTransaction`.
- Environment variable `DATABASE_URL` configured.

## How to Run
Invoke database migrations and TypeScript checks through the `terminal` tool. Inspect files using `read_file` and update components using `patch` or `write_file`.

## Quick Reference
- API Route: `GET /api/admin/analytics`
- UI Route: `/admin/dashboard/sales`
- Run typecheck: `npx tsc --noEmit`
- Test analytics query: `npx dotenv-cli -e .env.local -- node -e '...'`

## Procedure

1. **Verify Database Schema**
   Confirm that the `order` table tracks `amount` (cents), `platformFee` (cents), `status`, `createdAt`, `currency`, and file licensing granularity (`trackId`, `productId`) using `read_file`.

2. **Implement Backend Analytics Endpoint**
   Use `write_file` to create `src/app/api/admin/analytics/route.ts`:
   - Enforce admin authentication via session headers.
   - Compute GMV (`sum(amount)`), Platform Fee (`sum(platformFee)`), and Take Rate (`(fee / gmv) * 100`).
   - Group transactions by digital file type: Single Track (`trackId != null`) vs Full Album (`trackId == null`).
   - Generate 30-day chronological rolling timeline map (`dailyTrendMap`) to compute 30-day daily average (`dailyAvg30`) and 30-day run-rate forecast (`dailyAvg30 * 30`).
   - Aggregate sales by product ID and seller ID, sort descending by revenue, and slice top 10 items for Pareto distribution.

3. **Construct Frontend Executive Dashboard**
   Use `write_file` or `patch` on `src/app/[locale]/admin/dashboard/sales/page.tsx`:
   - Replace in-memory mock calculations with `fetch("/api/admin/analytics")`.
   - Render executive metric cards: GMV (Gross Sales), Platform Fee & Take Rate, 30D Run-Rate & Forecast, Refund Rate & Risk.
   - Render digital file breakdown cards comparing single tracks versus full master bundles.
   - Implement tabbed navigation for `30-Day Trend` (visual bar charts), `Top 10 Pareto Analysis`, and paginated `Transaction Log`.

4. **Surface Real-time Deltas to Admin Overview**
   Use `patch` on `src/app/[locale]/admin/dashboard/page.tsx`:
   - Query daily deltas using `gte(order.createdAt, startOfDay)` and `gte(user.createdAt, startOfDay)`.
   - Display Today's Activity and Month-to-Date revenue alongside live email quota indicators.

## Pitfalls
- **SQL Quote Escaping:** In raw node scripts or SQL strings, string literals like `'completed'` require single quotes. Double quotes `"completed"` are treated as column identifiers in PostgreSQL and throw `errorMissingColumn`.
- **Currency Cents Conversion:** Monetary values are stored in cents/satang integers. Divide by 100 before UI display to prevent 100x overcounting.
- **Client-Side Array Filtering:** Avoid fetching all records and filtering in JavaScript memory. Execute aggregate sums and joins in the database to prevent memory crashes at scale.

## Verification
Execute the verification script through the `terminal` tool to validate non-mock database aggregates:
```bash
npx dotenv-cli -e .env.local -- node -e 'const postgres = require("postgres"); const sql = postgres(process.env.DATABASE_URL); async function main() { const res = await sql`SELECT count(*), coalesce(sum(amount),0) as gmv FROM "order" WHERE status = '\''completed'\''`; console.log("Verified GMV:", res[0]); process.exit(0); } main();'
```
