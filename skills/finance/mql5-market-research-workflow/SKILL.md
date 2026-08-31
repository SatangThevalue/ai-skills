---
name: mql5-market-research-workflow
description: "Reverse-engineer commercial EAs from MQL5 Market to build custom trading bots."
version: 0.1.0
metadata:
  hermes:
    tags: [MQL5, Reverse Engineering, EA, Prop Firm, GitHub]
---

# MQL5 Market Research & Clone Workflow

This skill outlines the workflow to systematically scrape, analyze, and reverse-engineer top-selling commercial Expert Advisors (EAs) from the MQL5 Market. It distills complex marketing descriptions into quantitative logic, converts them into modular MQL5 code, and packages them into a documented GitHub repository for deployment.

## When to Use

- "ช่วยก๊อปปี้การทำงานของ ea 6 ตัว วิเคราะห์การทำงานการทำงานทั้งหมดในแต่ละตัว แล้วนำมาสร้างใหม่"
- When researching state-of-the-art features for Prop Firm EAs (e.g., FTMO compliance).
- When transitioning from a monolithic Python script to a modular native MQL5 architecture.

## Prerequisites

- Target MQL5 Market URLs (e.g., `https://www.mql5.com/en/market/mt5/expert/paid`).
- Local directory for staging MQL5 files (e.g., `~/mql5-expert-advisors`).
- Configured GitHub CLI (`gh`) and Git user profile.

## How to Run

1. Scrape target EA descriptions using `web_extract`.
2. Generate modular `.mq5` files and `.md` documentation using `terminal` (cat heredoc).
3. Initialize and push the repository using `terminal` (git/gh commands).

## Quick Reference

- **Prop Firm Mechanics:** Daily Drawdown Limit, Friday Auto-Close, Trade Randomization (to avoid behavioral copying bans).
- **Core Strategy Examples:** Asian Range Breakout, Selective Grid (RSI + Distance), Dual TP with Break-Even.
- **Git Init:** `git init && git add . && git commit -m "Init"`
- **GH Repo Create:** `gh repo create <name> --public --source=. --remote=origin --push`

## Procedure

1. **Extract Commercial Logic**
   Identify the top paid EAs on MQL5 and extract their product descriptions.
   ```bash
   # Use the web_extract tool on MQL5 URLs to pull text, then deduce the underlying indicators.
   ```

2. **Generate Modular MQL5 Components**
   Break down the discovered logic into reusable MQL5 modules rather than a monolithic file.
   - *Risk Protector:* Equity tracking and Friday closure.
   - *News Filter:* ATR-based volatility spike detection.
   - *Grid Recovery:* Distance + Indicator confirmation for averaging down.
   Create these using the `terminal` tool.

3. **Synthesize the Ultimate EA**
   Combine the modules into a single production-ready EA (e.g., `Ultimate_PropFirm_EA.mq5`) that features Prop Firm compliance (Daily DD limits, random slippage injection).

4. **Document the Architecture**
   Create individual Markdown files for each EA explaining the Core Strategy, Indicator Stack, Parameters, and Risk Management. Update the main `README.md` to index the collection.

5. **Deploy to GitHub**
   Use the `terminal` tool to initialize the repository and push it publicly.
   ```bash
   cd ~/mql5-expert-advisors
   git init
   git add .
   git commit -m "Initial commit: Add cloned MT5 EAs with Prop Firm features"
   gh repo create mql5-expert-advisors --public --source=. --remote=origin --push
   ```

## Pitfalls

- **Marketing Fluff:** MQL5 descriptions often use buzzwords ("Quantum AI", "Neural Algorithms"). You must strip this away to find the underlying math (e.g., Moving Average Crossover + Martingale).
- **Git Initialization Errors:** If `gh repo create` fails with "not a git repository", ensure `git init` was run successfully in the exact same directory before calling `gh`.
- **MQL5 Compilation:** The provided scripts are templates. They lack the complete `#include` structure for complex Trailing Stops unless explicitly coded. They must be compiled via MetaEditor (F7) before attaching to a chart.

## Verification

The workflow is successful when the local `~/mql5-expert-advisors` directory contains `.mq5` files, matching `.md` documentation, a comprehensive `README.md`, and the entire structure is live on the user's GitHub account.