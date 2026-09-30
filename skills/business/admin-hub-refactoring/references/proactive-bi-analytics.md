# Proactive BI & Analytics Reference

## Core Metric Definitions for Digital Music File Marketplaces

When designing or auditing e-commerce admin systems for digital file sales (single tracks & master album bundles), avoid vanity metrics. Focus on proactive, actionable financial and operational intelligence:

### 1. Key Business Metrics
- **GMV (Gross Merchandise Value)**: Total currency volume of completed orders: `SUM(order.amount) WHERE status = 'completed'`.
- **Take Rate**: Realized platform fee percentage: `(SUM(platformFee) / GMV) * 100`.
- **Refund Rate**: Customer dispute and chargeback percentage: `(Count(Refunds) / (Count(Completed) + Count(Refunds))) * 100`. Alert if > 2%; critical if > 5%.
- **30-Day Moving Run-Rate & Forecast**: Sum revenue of last 30 daily buckets, compute daily average `dailyAvg30 = sum30 / 30`, and project next month `forecast = dailyAvg30 * 30`.
- **Digital Asset Split**: Segment sales strictly by unit type:
  - Single Track Licenses (`WHERE trackId IS NOT NULL`)
  - Full Album Master Bundles (`WHERE trackId IS NULL`)
  *Note:* Do not introduce subscription metrics unless explicitly instructed.

### 2. Pareto Analysis (80/20 Rule)
- **Top 10 Releases / Products**: Group orders by `productId`, order by `SUM(amount) DESC`. Surfacing top revenue drivers reveals catalog concentration.
- **Top 10 Creators / Sellers**: Group by `product.sellerId`, order by `SUM(order.amount) DESC`. Allows proactive relationship management for top earners.

### 3. Action Center (Triage First)
Always position urgent alerts above analytics cards:
- Pending DMCA takedowns and copyright claims.
- Pending creator identity / KYC submissions.
- Failed webhook transactions requiring manual settlement.
- Daily outgoing email quota status (e.g., SMTP free tier limits).
