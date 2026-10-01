---
name: creator-operations-architecture
description: Builds music creator dashboards, payouts, and analytics.
version: 0.1.0
metadata.hermes.tags:
  - Marketplace
  - Creator
  - Payouts
  - Analytics
  - Drizzle
---

# Creator Operations & Marketplace Seller Hub

Architects and implements the complete creator/seller operations layer for digital music marketplaces. It covers creator payout setup (local bank transfers, PromptPay), seller-specific performance analytics, saved metadata presets, and per-track catalog management. It does NOT handle automated bank clearinghouse API executions or tax withholding filings.

## When to Use
- "Audit and overhaul the seller dashboard."
- "Implement creator payouts with local bank transfer or PromptPay."
- "Build creator performance analytics and top earning releases."
- "Add saved contributor presets to product upload wizard."

## Prerequisites
- Next.js App Router with Drizzle ORM and PostgreSQL.
- Database tables: `user`, `sellerProfile`, `order`, `product`, `productTrack`, `contributor`.
- Environment variable `DATABASE_URL` configured.

## How to Run
Apply database schema modifications using `patch` and `terminal` with `drizzle-kit push`. Review API routes with `read_file` and test endpoints using `terminal`.

## Quick Reference
- Payout API: `GET /api/seller/payout`, `POST /api/seller/payout`
- Analytics API: `GET /api/seller/analytics`
- Seller Payout Page: `/seller/dashboard/payout`
- Seller Analytics Dashboard: `/seller/dashboard`
- Catalog Management: `/seller/dashboard/products`

## Procedure

1. **Extend Schema for Creator Financials & Payout Ledger**
   Inspect `src/db/schema.ts` using `read_file`. Add bank transfer fields to `sellerProfile` (`bankName`, `bankAccountNumber`, `bankAccountName`, `promptPayId`, `payoutMethod`). Define the `sellerPayout` table:
   ```typescript
   export const sellerPayout = pgTable("sellerPayout", {
     id: text("id").primaryKey(),
     sellerId: text("sellerId").notNull().references(() => user.id, { onDelete: 'cascade' }),
     amount: integer("amount").notNull(), // satang / cents
     currency: text("currency").default("thb").notNull(),
     status: text("status").default("pending").notNull(), // pending, processing, completed, rejected
     payoutMethod: text("payoutMethod").notNull(),
     destinationDetails: text("destinationDetails"),
     transferSlipUrl: text("transferSlipUrl"),
     referenceNumber: text("referenceNumber"),
     requestedAt: timestamp("requestedAt").defaultNow().notNull(),
     processedAt: timestamp("processedAt"),
   });
   ```
   Synchronize changes to PostgreSQL using `terminal`:
   ```bash
   npx dotenv-cli -e .env.local -- npm run db:push -- --force
   ```

2. **Implement Seller Payout API Route**
   Create `src/app/api/seller/payout/route.ts` using `write_file`:
   - `GET`: Authenticate session, retrieve bank destination, calculate completed sales net earnings (`sum(amount - platformFee)`), deduct pending/completed payouts, and return `availableBalance`.
   - `POST` (`action: "update_bank"`): Update seller bank account or PromptPay ID.
   - `POST` (`action: "request_payout"`): Validate minimum threshold (e.g., 300 THB), verify available balance, and insert record into `sellerPayout`.

3. **Construct Creator Financial Dashboard**
   Use `patch` or `write_file` on `src/app/[locale]/seller/dashboard/payout/page.tsx`:
   - Display three summary metric cards: Available Balance, Pending Review, and Total Paid Out.
   - Add Bank / PromptPay destination configuration form with bank dropdowns.
   - Add Payout Request card with quick "Withdraw All" action.
   - Render Payout Statement table with date, amount, destination, status badge, and transfer slip link.

4. **Implement Creator Performance Analytics**
   Create `src/app/api/seller/analytics/route.ts` using `write_file`:
   - Compute seller net revenue, total sales, store conversion rate (`orders / views * 100`).
   - Group orders by date for 30-day moving sales volume trend.
   - Sort releases by revenue to return Top 5 Earning Releases.
   Update `src/app/[locale]/seller/dashboard/page.tsx` using `patch` to mount the Top Releases widget and 30-day bar trend.

5. **Wire Saved Contributor Presets in Upload Wizard**
   Use `patch` on `src/app/[locale]/seller/dashboard/upload/page.tsx`:
   - Fetch previously created contributors from `GET /api/seller/contributors`.
   - In Step 2 & Step 3 Track Modal, render quick-select pills or dropdowns so sellers can reuse composer/producer metadata without re-typing.

## Pitfalls
- **Duplicate Schema Declarations:** Avoid declaring `sellerPayoutRelations` multiple times in `schema.ts`. Duplicate exports cause Next.js Turbopack HMR compilation crashes.
- **Satang vs Baht Math:** Store amounts as integers in satang (cents) to avoid floating-point drift. Divide by 100 strictly on UI presentation.
- **Minimum Withdrawal Bounds:** Always validate payout requests on the server against `availableBalance` to prevent double-spending or negative balances.

## Verification
Verify the payout API endpoint returns valid balances for authenticated sellers:
```bash
curl -m 5 -s -o /dev/null -w "%{http_code}\n" http://localhost:9999/api/seller/payout
```
Expected output: `401` (when unauthenticated) or `200` (when authenticated).
