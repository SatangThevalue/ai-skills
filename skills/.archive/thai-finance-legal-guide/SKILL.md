---
name: thai-finance-legal-guide
description: Reference for Thai tax, stock, and crypto regulations.
version: 0.1.0
metadata:
  hermes:
    tags:
      - Finance
      - Retirement-Funds
      - Thai-Stock
      - Crypto-Regulations
      - Civil-Law
---

# Thai Finance and Legal Reference Guide

This skill serves as a comprehensive procedural and database reference for evaluating Thai civil law capacities, personal income taxes, tax-saving mutual funds (SSF, RMF, Thai ESG), stock markets (SET/mai), derivative warrants (DW), and digital asset broker regulations. It does not provide dynamic external API retrieval but provides static logical constraints for math executions.

## When to Use
- When evaluating the legal age of majority or minor contracting capacity under Thai Civil Law.
- When calculating progressive income tax brackets or base deductions for Thai citizens.
- When validating retirement fund caps (SSF, RMF, PVD, GPF, Pension Life Insurance, NSF) or separate Thai ESG limits.
- When checking SET/mai trading hours or analyzing Call/Put DW variables.
- When checking SEC licensing structures or capital gains/loss offset rules for crypto.

## Prerequisites
- Standard Python environment (`python3`) to run inline calculation verification checks.

## How to Run
- Run numerical evaluations or display specific legal code sections using the `terminal` tool.

## Quick Reference
- Age of Majority: 20 years old (or 17 upon legal marriage).
- Personal Deduction: 60,000 THB.
- Retirement Cap: 500,000 THB max (RMF + SSF + PVD/GPF + Pension Life Insurance + NSF).
- Thai ESG Limit: 300,000 THB max (Separate from the 500,000 THB cap).
- SET Trading Session 1: 10:00 - 12:30.
- SET Trading Session 2: 14:30 - 16:30.

## Procedure

### 1. Civil Law & Minor Capacity Audit
Assess minor contract validity using civil capacity rules:
1. Verify age. If under 20, check for legal marriage status (min 17 years old + parental consent).
2. Evaluate exception capacity. Minors can execute contracts without guardian consent ONLY if the act:
   - Receives absolute rights or releases from duties.
   - Is strictly personal (e.g., child acknowledgment).
   - Is suitable for their station in life and daily living needs.
   - Is a Will (only if aged 15 or older).
3. Apply PDPA criteria:
   - Under 10 years old: Parental consent always required.
   - 10-20 years old: Joint consent required for acts outside standard minor civil capacity.

### 2. Personal Income Tax Calculations
Follow the progressive bracket formula to compute tax liability:
1. Calculate Net Income:
   $$\text{Net Income} = \text{Assessable Income} - \text{Expenses} - \text{Deductions}$$
2. Deduct base allowances:
   - Personal: 60,000 THB
   - Spouse (no income): 60,000 THB
   - Children: 30,000 THB each (60,000 THB for 2nd child onwards born in/after 2018)
   - Parents (60+ years old, income < 30,000 THB/yr): 30,000 THB each
3. Compute tax against progressive brackets:
   - 0 – 150,000 THB: Exempt (0%)
   - 150,001 – 300,000 THB: 5% (Max 7,500 THB)
   - 300,001 – 500,000 THB: 10% (Max 20,000 THB)
   - 500,001 – 750,000 THB: 15% (Max 37,500 THB)
   - 750,001 – 1,000,000 THB: 20% (Max 50,000 THB)
   - 1,000,001 – 2,000,000 THB: 25% (Max 250,000 THB)
   - 2,000,001 – 5,000,000 THB: 30% (Max 900,000 THB)
   - Over 5,000,000 THB: 35%

### 3. Tax-Saving Investment Auditing
Calculate mutual fund limits using the twin ceilings:
1. Retirement Savings Cap: Ensure the sum of SSF (max 30% income, cap 200k), RMF (max 30% income, cap 500k), PVD/GPF, Pension Life Insurance, and NSF does not exceed 500,000 THB.
2. Separate Cap: Verify Thai ESG (max 30% income, cap 300k, 5-year calendar holding) is calculated independently.
3. Total Allowable Mutual Fund Limit: Max 800,000 THB.

### 4. Derivative Warrants (DW) Technical Profiling
Analyze warrant properties:
1. Verify Call DW (bullish) or Put DW (bearish).
2. Calculate simulated moves using Gearing:
   $$\Delta \text{DW}\% = \Delta \text{Underlying}\% \times \text{Effective Gearing}$$
3. Estimate time cost using Time Decay metrics per day of holding.
4. Verify issuer broker (e.g., 01, 13, 19, 28, 41) to assess liquidity/market-making profiles.

### 5. Domestic Crypto Licensing & Tax Review
Confirm digital asset operations fall under authorized classes:
- Licensing: Exchange, Broker, Dealer (OTC), or Fund Manager.
- Tax rules: Ensure 7% VAT exemption is active (restricted to licensed domestic entities).
- Losses: Verify trading losses are only offset if generated on SEC-regulated domestic platforms.

## Pitfalls
- **RMF Inactivity Penalty**: RMF requires purchases at least every other year. Missing consecutive years triggers tax retro-charges.
- **SSF/RMF Calendar Counts**: SSF requires 10 calendar years, whereas RMF requires 5 years of active holding AND reaching age 55. Do not mix their redemption timelines.
- **Unlicensed Crypto Trading**: Capital gains from offshore exchanges (e.g. standard Binance, Bybit) are not eligible for VAT waivers or domestic loss offset rules.

## Verification
Confirm the tax calculations using a Python helper function executed via the `terminal` tool:
```bash
python3 -c "
rmf, ssf, esg = 150000, 200000, 300000
retirement_ok = (rmf + ssf) <= 500000
esg_ok = esg <= 300000
print(f'Retirement Cap Status: {retirement_ok}, ESG Status: {esg_ok}')
"
```
