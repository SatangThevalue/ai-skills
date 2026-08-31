# 🧠 AI Skills — Tonthong (ต้นทอง) Skill Library

> **Repository:** [SatangTheValue/ai-skills](https://github.com/SatangTheValue/ai-skills)  
> **ผู้ดูแล:** Thanapol N (Satang) · ผู้ช่วย: ต้นทอง (Hermes Agent)  

---

## 📖 คืออะไร?

คลังสกิลของต้นทอง (Hermes Agent) ที่ใช้ในการทำงานร่วมกับ Satang — ครอบคลุมตั้งแต่ DevOps, Finance, Trading, Marketing, AI/ML ไปจนถึงการพัฒนาซอฟต์แวร์ทั้งหมด

สกิลแต่ละตัวคือ **ชุดคำสั่งและขั้นตอนที่พิสูจน์แล้ว** ที่ต้นทองโหลดขึ้นมาใช้โดยอัตโนมัติเมื่อได้รับงานที่เกี่ยวข้อง ทำให้ไม่ต้องอธิบายขั้นตอนซ้ำในทุก Session

---

## 🚀 วิธีใช้งาน

```bash
# ดูรายชื่อ Skill ทั้งหมด
hermes skills list

# โหลด Skill เพื่อดูเนื้อหา
hermes skills view <ชื่อ-skill>


## 📚 รายชื่อ Skills แบ่งตามหมวดหมู่


### 📁 ALGORITHMIC-TRADING

- **`farmed-hedge-yield-strategy`**: กลยุทธ์การเทรดแบบ Systematic Hedging และ Yield Farming จาก Farmed Hedge Yield Copy I พร้อมการปรับใช้ด้วย Python/MT5

### 📁 API-INTEGRATION

- **`innovestx-open-api`**: Guide and implementation details for using InnovestX Digital Asset Open API.

### 📁 APPLE

- **`apple-notes`**: Manage Apple Notes via memo CLI: create, search, edit.
- **`apple-reminders`**: Apple Reminders via remindctl: add, list, complete.
- **`findmy`**: Track Apple devices/AirTags via FindMy.app on macOS.
- **`imessage`**: Send and receive iMessages/SMS via the imsg CLI on macOS.
- **`macos-computer-use`**: |

### 📁 AUTOMATION

- **`python-media-automation`**: Best practices, pitfalls, and configuration fixes for running Python media libraries (MoviePy, Piper TTS, Pedalboard,...

### 📁 AUTONOMOUS-AI-AGENTS

- **`agent-frameworks-integration`**: Use when designing, building, or orchestrating multi-agent systems using Google ADK, Agent-to-Agent (A2A) protocol, M...
- **`claude-code`**: Delegate coding to Claude Code CLI (features, PRs).
- **`codex`**: Delegate coding to OpenAI Codex CLI (features, PRs).
- **`google-adk`**: Use when building multi-agent systems with Google's Agent Development Kit (ADK), configuring agents, tools, workflows...
- **`hermes-agent`**: Configure, extend, or contribute to Hermes Agent.
- **`hermes-discord-setup`**: Configure and enable the Discord bot integration for Hermes.
- **`hermes-gateway-resilience`**: Restore and harden the Hermes Messaging Gateway on Linux when it goes inactive, drops platform connections, or fails ...
- **`hermes-kanban-swarm`**: Orchestrate, configure, and execute multi-agent workflows (Swarms) using Hermes Kanban boards and profiles.
- **`hermes-profile-customization`**: Create and customize isolated profiles in Hermes.
- **`hermes-workspace-setup`**: Set up and run Hermes Workspace on a VPS with gateway auth.
- **`kanban-codex-lane`**: Use when a Hermes Kanban worker wants to run Codex CLI as an isolated implementation lane while Hermes keeps ownershi...
- **`opencode`**: Delegate coding to OpenCode CLI (features, PR review).
- **`research-to-skill-pipeline`**: Research and author Hermes skills on demand from the web.
- **`satang-ai-gateway`**: Satang AI: Integration patterns for FastAPI Gateway, Better-Auth, and Prefect.

### 📁 BLOCKCHAIN

- **`evm`**: Read-only EVM client: wallets, tokens, gas across 8 chains.
- **`hyperliquid`**: Hyperliquid market data, account history, trade review.
- **`solana`**: Query Solana blockchain data with USD pricing — wallet balances, token portfolios with values, transaction details, N...

### 📁 BUSINESS-GROWTH-SKILLS

- **`prefect-monetization-orchestration`**: Blueprint for replacing n8n and simple cronjobs with Prefect 2.x/3.x for enterprise-grade, code-based orchestration o...
- **`prefect-zero-touch-blueprint`**: Enterprise architecture, strict coding standards, fallback rules, and Dockerized setup for the Zero-Touch Monetizatio...
- **`thailand-monetization-2026`**: Predictive trends and architectural strategies for generating income in Thailand (2026-2027), focusing on AI automati...
- **`thailand-monetization-playbooks`**: Detailed execution methods and concrete examples for the 4 pillars of Thai monetization (Faceless Media, LINE Agents,...

### 📁 BUSINESS-OPERATIONS

- **`hr-thai-and-myanmar-worker-management`**: คำแนะนำการจัดการ HR แรงงานชาวไทยและชาวต่างชาติ (พม่า, ไทย, เขมร) รวมถึงกฎหมาย, ระบบเงินเดือน, ประกันสังคม และเอกสารที...
- **`wholesale-chicken-distribution`**: คู่มือการดำเนินธุรกิจและขั้นตอนทางกฎหมายสำหรับการซื้อไก่สดจากโรงงานเพื่อขายส่งและขนส่งไปต่างจังหวัดในประเทศไทย

### 📁 CREATIVE

- **`architecture-diagram`**: Dark-themed SVG architecture/cloud/infra diagrams as HTML.
- **`ascii-art`**: ASCII art: pyfiglet, cowsay, boxes, image-to-ascii.
- **`ascii-video`**: ASCII video: convert video/audio to colored ASCII MP4/GIF.
- **`baoyu-article-illustrator`**: Article illustrations: type × style × palette consistency.
- **`baoyu-comic`**: Knowledge comics (知识漫画): educational, biography, tutorial.
- **`baoyu-infographic`**: Infographics: 21 layouts x 21 styles (信息图, 可视化).
- **`claude-design`**: Design one-off HTML artifacts (landing, deck, prototype).
- **`comfyui`**: Generate images, video, and audio with ComfyUI — install, launch, manage nodes/models, run workflows with parameter i...
- **`creative-ideation`**: Generate project ideas via creative constraints.
- **`design-md`**: Author/validate/export Google's DESIGN.md token spec files.
- **`excalidraw`**: Hand-drawn Excalidraw JSON diagrams (arch, flow, seq).
- **`humanizer`**: Humanize text: strip AI-isms and add real voice.
- **`manim-video`**: Manim CE animations: 3Blue1Brown math/algo videos.
- **`p5js`**: p5.js sketches: gen art, shaders, interactive, 3D.
- **`pixel-art`**: Pixel art w/ era palettes (NES, Game Boy, PICO-8).
- **`popular-web-designs`**: 54 real design systems (Stripe, Linear, Vercel) as HTML/CSS.
- **`pretext`**: Use when building creative browser demos with @chenglou/pretext — DOM-free text layout for ASCII art, typographic flo...
- **`sketch`**: Throwaway HTML mockups: 2-3 design variants to compare.
- **`songwriting-and-ai-music`**: Songwriting craft and Suno AI music prompts.
- **`touchdesigner-mcp`**: Control a running TouchDesigner instance via twozero MCP — create operators, set parameters, wire connections, execut...

### 📁 DATA-SCIENCE

- **`data-science-and-engineering`**: Principles, methods, techniques, and workflows for Data Science (DS) and Data Engineering (DE).
- **`jupyter-live-kernel`**: Iterative Python via live Jupyter kernel (hamelnb).
- **`prefect-workflows`**: Design, monitor, and run data orchestrations with Prefect.

### 📁 DEVOPS

- **`ai-telemetry-and-billing`**: Implement database telemetry to track LLM token usage, latency, and estimated costs.
- **`cli-proxy-api-quota-and-update`**: Check CLIProxyAPI account quota and update binary to latest release.
- **`cli-proxy-api-troubleshooting`**: Diagnose and fix cli-proxy-api provider and auth failures.
- **`disk-space-management-docker-builds`**: Prevent disk space exhaustion during Docker container builds.
- **`docker-compose-git-update`**: Pull Git updates and rebuild Docker Compose stacks safely.
- **`docker-management`**: Manage Docker containers, images, volumes, networks, and Compose stacks — lifecycle ops, debugging, cleanup, and Dock...
- **`hermes-dashboard-traefik`**: Expose Hermes Dashboard via Traefik with SSL and systemd.
- **`hermes-production-deploy`**: Procedural best practices for deploying Node.js (Next.js) and Python (FastAPI) SaaS applications on Hermes-managed VP...
- **`hybrid-fastapi-line-deployment`**: Deploy and debug FastAPI LINE bots behind Traefik.
- **`kanban-orchestrator`**: Decomposition playbook + anti-temptation rules for an orchestrator profile routing work through Kanban. The "don't do...
- **`kanban-worker`**: Pitfalls, examples, and edge cases for Hermes Kanban workers. The lifecycle itself is auto-injected into every worker...
- **`line-bot-sdk-python`**: LINE Bot SDK (Python) สำหรับ Hermes
- **`n8n-traefik-postgres`**: Deploy n8n with PostgreSQL via Traefik with required headers.
- **`nextjs-traefik-www-redirect`**: Deploy Next.js standalone app with Traefik www redirection.
- **`postgres-pgvector-traefik`**: Deploy PostgreSQL 18 with pgvector and Traefik TCP proxying.
- **`prefect-orchestration`**: Set up and manage Prefect workflows, task queues, and auto-publishing pipelines.
- **`traefik-docker29-fix`**: Fix Traefik Docker API errors on Docker Engine 29.4 plus.
- **`webhook-subscriptions`**: Webhook subscriptions: event-driven agent runs.

### 📁 EMAIL

- **`himalaya`**: Himalaya CLI: IMAP/SMTP email from terminal.

### 📁 FINANCE

- **`3-statement-model`**: Build fully-integrated 3-statement models (IS, BS, CF) in Excel with working capital schedules, D&A roll-forwards, de...
- **`ai-trading-continuous-learning`**: Architecture and guidelines for building a Continuous Learning Pipeline for AI Trading models (Data Lake to MT5 ONNX)...
- **`backtesting-py-mean-reversion`**: วิธีเขียนโค้ดและทำ Optimization กลยุทธ์ Mean Reversion ด้วยไลบรารี Backtesting.py
- **`build-ea-python-strategy`**: Guidelines and architecture for building Expert Advisors using Python and MT5.
- **`business-ledger-and-inventory`**: สกิลการวางผังบัญชี 5 หมวด การจดบันทึกทางการเงิน และการบริหารจัดการคลังสินค้าสำหรับธุรกิจ SME ในประเทศไทย
- **`chicken-business-scale-up`**: Scale a fresh chicken shop from local market to regional or national level.
- **`comps-analysis`**: Build comparable company analysis in Excel — operating metrics, valuation multiples, statistical benchmarking vs peer...
- **`cost-accounting-inventory`**: การคำนวณบัญชีต้นทุนและการบริหารจัดการสินค้าคงคลัง (FIFO, Weighted Average, EOQ, Reorder Point, Safety Stock) พร้อม Py...
- **`dcf-model`**: Build institutional-quality DCF valuation models in Excel — revenue projections, FCF build, WACC, terminal value, Bea...
- **`diy-accounting-setup`**: คู่มือและขั้นตอนการวางระบบบัญชี เอกสารควบคุมภายใน และปฏิทินภาษีด้วยตนเองสำหรับธุรกิจ SME และสตาร์ทอัพในประเทศไทย
- **`dw-money-management-strategy`**: กลยุทธ์การบริหารเงิน (Money Management) และการบริหารความเสี่ยงสำหรับ DW
- **`dw-trading-thailand-strategy`**: คู่มือเทคนิคและการเลือกซื้อ DW (Derivative Warrants) ในประเทศไทย
- **`ea-analysis-to-python-workflow`**: Reverse-engineer commercial MT5 EAs into Python quantitative strategies.
- **`ea-capital-protection-features`**: ฟีเจอร์การปกป้องเงินทุน (Capital Protection) ขั้นสูงสำหรับ EA และบอทเทรด
- **`ea-dashboard-architecture`**: สถาปัตยกรรมและพารามิเตอร์สำหรับสร้าง Dashboard และระบบตั้งค่า EA (Python/MT5)
- **`ea-news-filter-architecture`**: แนวทางและสถาปัตยกรรมในการสร้างระบบ News Filter สำหรับ EA และ Python Bot
- **`eamt5-python-architecture`**: แนวทางและโครงสร้างการสร้าง EA บน MT5 เชื่อมต่อกับ Python สำหรับระบบเทรดอัตโนมัติ
- **`excel-author`**: Build auditable Excel workbooks headless with openpyxl — blue/black/green cell conventions, formulas over hardcodes, ...
- **`forex-exness-backtesting`**: การทดสอบสภาพแวดล้อมเสมือนจริงของ Exness (Free Swap) บน Python
- **`forex-fundamental-analysis`**: Framework for analyzing macroeconomic fundamentals to select Forex currency pairs.
- **`forex-mean-reversion-indicators`**: คู่มือการเลือกใช้อินดิเคเตอร์สำหรับระบบเทรด Mean Reversion และ Scalping
- **`forex-profitability-framework`**: กรอบความคิดและหลักการเชิงปริมาณ (Quant) เพื่อทำกำไรอย่างยั่งยืนในตลาด Forex
- **`forex-trading-concepts`**: คู่มือพื้นฐานตลาด Forex: คู่เงินหลัก (Majors), คู่เงินรอง (Minors), สเปรด (Spread), ค่าคอมมิชชั่น และค่าสวอป (Swap) พ...
- **`fresh-chicken-business-th`**: คู่มือขั้นตอนปฏิบัติการตั้งธุรกิจและควบคุมคุณภาพการค้าไก่สดในประเทศไทย อัปเดตระเบียบปศุสัตว์และกฎหมายท้องถิ่นปี 2569
- **`high-frequency-sweetspot-reversion`**: สูตรลับการปรับจูน Indicator เพื่อหา Sweet Spot (Win Rate ~70% + เทรดถี่) สำหรับ Daily Cashflow
- **`high-win-rate-mean-reversion`**: สูตรลับการปรับจูน Indicator (Optimization) ให้ได้ Win Rate 100% สำหรับ Mean Reversion
- **`innovestx-api`**: InnovestX Digital Asset Open API integration guide and Python client implementation.
- **`lbo-model`**: Build leveraged buyout models in Excel — sources & uses, debt schedule, cash sweep, exit multiple, IRR/MOIC sensitivi...
- **`lightgbm-mt5-onnx-pipeline`**: Architecture for LightGBM-based MT5 algorithmic trading bots using Walk-Forward testing and ONNX deployment.
- **`merger-model`**: Build accretion/dilution (merger) models in Excel — pro-forma P&L, synergies, financing mix, EPS impact. Pairs with e...
- **`metatrader5-docker-python`**: Run MT5 in Docker and trade via Python on Linux.
- **`modern-ea-features-2026`**: รวมฟีเจอร์และสถาปัตยกรรมของ EA ยุคใหม่ (2026-2027) สำหรับสอบกองทุน Prop Firm และใช้งานจริง
- **`mql5-acd-cs-architecture`**: โครงสร้างและอัลกอริทึมของ EA แบบ Adaptive Context-Driven (ACD-CS) บน MT5
- **`mql5-commercial-ea-collection`**: รวมเทคนิค สถาปัตยกรรม และอินดิเคเตอร์ของ 5 EA ยอดฮิตในตลาด MQL5 ปี 2026
- **`mql5-market-research-workflow`**: Reverse-engineer commercial EAs from MQL5 Market to build custom trading bots.
- **`mql5-modular-components`**: โมดูล MQL5 แบบแยกส่วน (Risk, News Filter, Grid) สำหรับประกอบร่าง EA ในอนาคต
- **`mql5-onnx-architecture-th`**: คู่มือและโครงสร้างสถาปัตยกรรม การนำโมเดล AI (ML/DL) มาใช้งานบน MetaTrader 5 ผ่าน ONNX สำหรับสาย AI/Big Data
- **`mql5-onnx-gui-integration`**: คู่มือและโครงสร้างโค้ดสำหรับสร้าง MQL5 EA ที่มีการเชื่อมต่อโมเดล ONNX (Machine Learning) และการสร้าง GUI Dashboard บน...
- **`mql5-onnx-integration`**: MQL5 ONNX Integration: Load, configure, and execute machine learning ONNX models natively in MetaTrader 5.
- **`mql5-scalping-ea-framework`**: Framework and MQL5 template for building a robust XAUUSD Scalping EA.
- **`mql5-scalping-grid-bot`**: โค้ด EA ต้นแบบ (MQL5) สำหรับการทำ Scalping และ Selective Grid เทียบเท่า EA เชิงพาณิชย์
- **`mt5-farmed-hedge-yield-strategy`**: Analysis and reverse-engineering of the MQL5 'Farmed Hedge Yield II' market-neutral hedging strategy, adapted for sur...
- **`mt5-onnx-ai-trading-pipeline`**: Data Science pipeline and architecture for building AI Trading Systems for MT5 via ONNX.
- **`mt5-python-trading`**: Guide and best practices for automated trading using Python and MetaTrader 5 (MT5), including Linux workarounds.
- **`personal-finance-and-investment`**: Guide for personal finance management, asset allocation, and algorithmic trading portfolio risk control.
- **`pptx-author`**: Build PowerPoint decks headless with python-pptx. Pairs with excel-author for model-backed decks where every number t...
- **`python-advanced-quant-trading`**: Advanced Python libraries for Candlestick pattern recognition, Price Action (Support/Resistance), Statistical indicat...
- **`python-mean-reversion-backtesting`**: แนวทางและแหล่งอ้างอิงสำหรับการทำ Backtest กลยุทธ์ Mean Reversion บน Python
- **`python-multi-asset-quant-trading`**: Frameworks, libraries, and mathematical constraints for quantitative trading across all major asset classes (Crypto, ...
- **`python-pair-trading-mt5`**: สถาปัตยกรรมและสมการสร้างบอท Pair Trading (Statistical Arbitrage) บน MT5 ด้วย Python
- **`python-quant-mlops-stack`**: Python Library Stack และ MLOps Architecture สำหรับระบบ AI Trading / Quant Platform ระดับ Enterprise
- **`python-technical-indicators`**: Comprehensive guide to implementing technical indicators in Python using pandas-ta and TA-Lib for algorithmic trading.
- **`quantum-omnigold-architecture`**: สถาปัตยกรรมและกลยุทธ์การเทรดทองคำ (XAUUSD) เลียนแบบ Quantum OmniGold EA
- **`research-backed-investing`**: Use when designing asset allocation frameworks, developing algorithmic trading strategies, or selecting investment ve...
- **`settrade-adaptive-survival-bot`**: Deploy an adaptive algorithmic trading bot for Thai stocks.
- **`settrade-dw-algo-trading`**: คู่มือและขั้นตอนการสร้างระบบ Algorithmic Trading สำหรับเทรด DW (Derivative Warrants) ในตลาดหุ้นไทยผ่าน Settrade Open ...
- **`settrade-dw-daily-income-bot`**: Deploy an automated DW trading bot using Settrade Open API.
- **`settrade-marketrep-derivatives-python`**: Guide and comprehensive API reference for Settrade Open API (MarketRep Derivatives SDK v2 for Python).
- **`settrade-multi-stock-scanner`**: Deploy a multi-stock Settrade scanner via Hermes cronjob.
- **`settrade-order-debugging`**: Debug Settrade API order rejections and OSS errors.
- **`settrade-sandbox-diagnostic`**: Diagnose and validate Settrade Open API Sandbox credentials.
- **`stock-selection-indicators`**: Framework and key indicators for systematic stock selection (Fundamental & Technical) for SET/Crypto and algorithmic ...
- **`stocks`**: Stock quotes, history, search, compare, crypto via Yahoo.
- **`thai-business-law-guide`**: คู่มือและกฎหมายสำคัญในการประกอบธุรกิจในประเทศไทย ครอบคลุมการจัดตั้งธุรกิจ ภาษี แรงงาน PDPA ทรัพย์สินทางปัญญา และกฎหมา...
- **`thai-business-license-guide`**: คู่มือเงื่อนไขการขอรับใบอนุญาตและระเบียบการดำเนินงานของธุรกิจเฉพาะประเภทในประเทศไทย เช่น อาหาร/เครื่องสำอาง (อย.), โร...
- **`thai-business-registration`**: คู่มือขั้นตอนการจัดตั้งห้างหุ้นส่วนและบริษัทจำกัดในประเทศไทยผ่านระบบ DBD Biz Regist (อัปเดตล่าสุด 2569)
- **`thai-business-setup-guide`**: คู่มือขั้นตอนปฏิบัติในการจัดตั้งบริษัทจำกัดและเริ่มต้นธุรกิจในประเทศไทย ผ่านระบบ DBD Biz Regist ดิจิทัล 100% อัปเดตปี...
- **`thai-corporate-and-partnership-law`**: คู่มือกฎหมายห้างหุ้นส่วนจำกัด (หจก.) และบริษัทจำกัด (บจก.) ในประเทศไทย ตามประมวลกฎหมายแพ่งและพาณิชย์ (ป.พ.พ.) และกฎหม...
- **`thai-corporate-structure-and-positions`**: Use when designing corporate organizational structures, defining department roles, job positions, and determining sal...
- **`thai-digital-accounting`**: ทักษะและความรู้ด้านการบัญชีดิจิทัล ระบบภาษีอิเล็กทรอนิกส์ (e-Tax & e-Withholding Tax) และการวิเคราะห์ข้อมูลสำหรับธุรก...
- **`thai-dw-price-table`**: คู่มือและวิธีการดึงข้อมูลตารางราคา DW (Derivative Warrants) ของแต่ละบริษัทผู้ออกหลักทรัพย์ในตลาดหุ้นไทย
- **`thai-dw-trading-strategy`**: คู่มือกลยุทธ์, การคำนวณ, และข้อควรระวังในการเทรด DW (Derivative Warrants) ในตลาดหุ้นไทย
- **`thai-finance-legal-guide`**: Reference for Thai tax, stock, and crypto regulations.
- **`thai-personal-accounting-and-finance`**: คู่มือและเครื่องมือการทำบัญชีส่วนบุคคล งบการเงิน และการวิเคราะห์อัตราส่วนสุขภาพทางการเงินตามมาตรฐานตลาดหลักทรัพย์แห่ง...
- **`thai-stock-seasonal-strategy`**: คู่มือและกลยุทธ์การเลือกหุ้นไทยด้วยปัจจัยพื้นฐาน ผสมผสานกับการเก็งกำไรตามฤดูกาล (Seasonal Effect) ในแต่ละไตรมาส
- **`thai-tax-planning-strategy`**: Guide and strategies for legal tax planning and tax optimization (Tax Avoidance) in Thailand for individuals and busi...
- **`thai-trading-business`**: คู่มือและขั้นตอนปฏิบัติการทำธุรกิจซื้อมาขายไป (Trading Business) ในประเทศไทย ครอบคลุมการตั้งค่าระบบบัญชี คลังสินค้า ภ...
- **`top5-dw-issuers-thailand`**: รายชื่อผู้ออก DW (Derivative Warrants) ในประเทศไทยที่มี Market Share ยอดนิยม 5 อันดับแรก
- **`topdown-stock-analysis`**: กรอบการวิเคราะห์หุ้นแบบ Top-Down Approach (Global -> Thai -> Stock)

### 📁 GAMING

- **`minecraft-modpack-server`**: Host modded Minecraft servers (CurseForge, Modrinth).
- **`pokemon-player`**: Play Pokemon via headless emulator + RAM reads.

### 📁 GITHUB

- **`codebase-inspection`**: Inspect codebases w/ pygount: LOC, languages, ratios.
- **`github-auth`**: GitHub auth setup: HTTPS tokens, SSH keys, gh CLI login.
- **`github-code-review`**: Review PRs: diffs, inline comments via gh or REST.
- **`github-issues`**: Create, triage, label, assign GitHub issues via gh or REST.
- **`github-pr-workflow`**: GitHub PR lifecycle: branch, commit, open, CI, merge.
- **`github-repo-management`**: Clone/create/fork repos; manage remotes, releases.

### 📁 MARKETING

- **`ai-business-thai-platforms`**: Use when designing, building, or implementing AI strategies for Thai businesses across LINE, Facebook, YouTube, and I...
- **`ai-fluency-framework`**: >
- **`ai-fluency-social-seo`**: AI fluency และ Social SEO สำหรับการทำการตลาด 2026 - ใช้ AI เพื่อสร้างเนื้อหา เพิ่มการมีส่วนไข้เข้าชมโดยรวม 10 ขั้นตอน
- **`social-seo-checklist`**: >
- **`thai-branding-strategy`**: Use when creating, positioning, or executing personal and business branding strategies for individuals and businesses...
- **`thai-business-marketing-guide`**: Marketing & business strategy guide for all Thai business types.
- **`thai-content-compliance`**: Use when creating content for Thai audiences, checking for forbidden words, compliance with FDA (อย.) / CPB (สคบ.), a...
- **`thai-psychology-engagement-2026`**: Mastering Thai human psychology for content, marketing, and communication in 2026-2027. Focuses on emotional triggers...
- **`thailand-content-strategy-2026`**: Use when planning, creating, or adapting content marketing strategies for the Thai market in 2026 across B2C, B2B, Re...
- **`thailand-market-demand-2026-2027`**: Use to analyze macroeconomic trends, consumer demand, and sector-specific performance in Thailand for 2026-2027 based...
- **`thailand-social-media-landscape`**: Insights, statistics, user behaviors, and platform-specific strategies for Social Media marketing in Thailand (Based ...

### 📁 MCP

- **`fastmcp`**: Build, test, inspect, install, and deploy MCP servers with FastMCP in Python. Use when creating a new MCP server, wra...
- **`native-mcp`**: MCP client: connect servers, register tools (stdio/HTTP).

### 📁 MEDIA

- **`ffmpeg-complex-filter-video-automation`**: Best practices for building fully automated video pipelines (templates, shorts, overlays) entirely in FFmpeg without ...
- **`ffmpeg-video-automation`**: FFmpeg complex filter recipes for automated social media video generation (TikTok, Shorts)
- **`gif-search`**: Search/download GIFs from Tenor via curl + jq.
- **`heartmula`**: HeartMuLa: Suno-like song generation from lyrics + tags.
- **`songsee`**: Audio spectrograms/features (mel, chroma, MFCC) via CLI.
- **`spotify`**: Spotify: play, search, queue, manage playlists and devices.
- **`youtube-content`**: YouTube transcripts to summaries, threads, blogs.

### 📁 MLOPS

- **`huggingface-hub`**: HuggingFace hf CLI: search/download/upload models, datasets.
- **`mlflow-dataset-tracking`**: Guide and implementation patterns for measuring, tracking, and versioning datasets using MLflow (mlflow.data API).
- **`ollama-local-inference`**: Run and manage local LLMs and embedding models using Ollama.
- **`pm-mlops-trading-framework`**: Project Management framework and strict governance rules for building an end-to-end MLOps AI Trading Platform (MT5 + ...

### 📁 NOTE-TAKING

- **`obsidian`**: Read, search, create, and edit notes in the Obsidian vault. Provides vault-first templates, canonical data schema, an...

### 📁 PRODUCTIVITY

- **`airtable`**: Airtable REST API via curl. Records CRUD, filters, upserts.
- **`brain-hacking-and-productivity`**: Neuroscience-based protocols for brain hacking, entering flow states, managing energy/dopamine, and optimizing cognit...
- **`business-analysis-frameworks`**: Use when analyzing business strategy, evaluating strengths/weaknesses (SWOT/TOWS), defining growth paths (Ansoff/BCG)...
- **`google-workspace`**: Gmail, Calendar, Drive, Docs, Sheets via gws CLI or Python.
- **`here-now`**: Publish static sites to {slug}.here.now and store private files in cloud Drives for agent-to-agent handoff.
- **`linear`**: Linear: manage issues, projects, teams via GraphQL + curl.
- **`maps`**: Geocode, POIs, routes, timezones via OpenStreetMap/OSRM.
- **`nano-pdf`**: Edit PDF text/typos/titles via nano-pdf CLI (NL prompts).
- **`notion`**: Notion API + ntn CLI: pages, databases, markdown, Workers.
- **`obsidian-personal-templates`**: |
- **`obsidian-workflow`**: |
- **`ocr-and-documents`**: Extract text from PDFs/scans (pymupdf, marker-pdf).
- **`online-income-and-monetization`**: Strategies for online monetization, content creation, digital products, and building a professional brand.
- **`petdex`**: Install and select animated petdex mascots for Hermes.
- **`powerpoint`**: Create, read, edit .pptx decks, slides, notes, templates.
- **`teams-meeting-pipeline`**: Operate the Teams meeting summary pipeline via Hermes CLI — summarize meetings, inspect pipeline status, replay jobs,...
- **`thai-business-excellence`**: Use when establishing, auditing, or improving business operations in Thailand using frameworks like TQA (Thailand Qua...
- **`time-management-and-productivity`**: Guidelines for task prioritization, time blocking, and learning systems (Second Brain/Obsidian).
- **`user-communication-preferences`**: Embed a user's preferred communication style and action-oriented conventions for Hermes Agent sessions (tone, languag...
- **`vision-net-registrar`**: Use when scraping or integrating academic data (schedules, grades, registration) from universities using Vision Net E...

### 📁 RED-TEAMING

- **`godmode`**: Jailbreak LLMs: Parseltongue, GODMODE, ULTRAPLINIAN.

### 📁 RESEARCH

- **`arxiv`**: Search arXiv papers by keyword, author, category, or ID.
- **`blogwatcher`**: Monitor blogs and RSS/Atom feeds via blogwatcher-cli tool.
- **`llm-wiki`**: Karpathy's LLM Wiki: build/query interlinked markdown KB.
- **`polymarket`**: Query Polymarket: markets, prices, orderbooks, history.
- **`research-paper-writing`**: Write ML papers for NeurIPS/ICML/ICLR: design→submit.
- **`scrape-grocery-thailand`**: Use when scraping, crawling, or extracting grocery product information from Thai retailers (specifically Lotus's and ...

### 📁 SMART-HOME

- **`openhue`**: Control Philips Hue lights, scenes, rooms via OpenHue CLI.

### 📁 SOCIAL-MEDIA

- **`xurl`**: X/Twitter via xurl CLI: post, search, DM, media, v2 API.

### 📁 SOFTWARE-DEVELOPMENT

- **`agent-skills-github-sync`**: Use when synchronizing Hermes Agent local skills with a remote GitHub repository. Guides the backup, management, and ...
- **`ai-content-studio-architecture`**: Architecture and workflows for the Satang AI Studio multi-agent content generation platform.
- **`audio-tts-post-processing`**: Techniques for processing, chunking, and mastering AI-generated TTS audio using Python (Pedalboard, Soundfile).
- **`better-auth-nextjs`**: Configure modern authentication in Next.js using better-auth.
- **`business-dss-development`**: Use when designing, building, or evaluating Business Decision Support Systems (DSS). Guides the architecture of data ...
- **`cli-proxy-api-management`**: Configure and query the CLIProxyAPI management endpoints.
- **`cliproxy-quota-check`**: Check CLIProxyAPI account quota and request success/failure counts.
- **`cliproxy-quota-inspector`**: Query and inspect CLIProxyAPI account statuses and request quotas.
- **`debugging-hermes-tui-commands`**: Debug Hermes TUI slash commands: Python, gateway, Ink UI.
- **`deep-agents-python`**: Guide and best practices for using LangChain's Deep Agents framework (langchain-ai/deepagents), an opinionated agent ...
- **`fastapi-unified-architecture`**: Patterns for deploying FastAPI, Gradio, and MCP servers in a single script, especially on Google Colab.
- **`hermes-agent-skill-authoring`**: Author in-repo SKILL.md: frontmatter, validator, structure.
- **`hermes-profile-isolation`**: Set up and configure isolated Hermes Agent profiles for different projects.
- **`hermes-s6-container-supervision`**: Modify, debug, or extend the s6-overlay supervision tree inside the Hermes Agent Docker image — adding new services, ...
- **`langgraph-development`**: Best practices for building and tracing AI agents with LangGraph, Deep Agents, and MLflow.
- **`langgraph-fastapi-hitl`**: Architecture and implementation guide for building Human-in-the-Loop (HITL) workflows with LangGraph and FastAPI, inc...
- **`nextjs-16-migration`**: Comprehensive guide and checklist for upgrading to Next.js 16, covering Turbopack, Async Request APIs, and breaking c...
- **`nextjs-spa-static-export`**: Best practices for building Single-Page Applications (SPA) and static sites with Next.js using the Static Export feat...
- **`nextjs-ui-libraries`**: Top UI libraries and UX frameworks for Next.js (shadcn/ui, Tailwind, NextUI, Chakra) to speed up frontend development.
- **`node-inspect-debugger`**: Debug Node.js via --inspect + Chrome DevTools Protocol CLI.
- **`plan`**: Plan mode: write markdown plan to .hermes/plans/, no exec.
- **`playwright-python`**: Playwright Python Best Practices and Techniques (Sync/Async, POM, Locators)
- **`python-debugpy`**: Debug Python: pdb REPL + debugpy remote (DAP).
- **`requesting-code-review`**: Pre-commit review: security scan, quality gates, auto-fix.
- **`satang-ai-gateway-dev`**: Development guide for the Satang AI Monorepo: FastAPI Gateway, Better-Auth integration, and Prefect orchestration.
- **`satang-project-suite`**: Develop and deploy Thanapol's custom AI and trading projects.
- **`server-side-video-processing`**: High-performance server-side video automation using pure FFmpeg complex filters (single-pass), avoiding MoviePy/Image...
- **`simplify-code`**: Parallel 3-agent cleanup of recent code changes.
- **`smart-context-usage`**: Guidelines for maintaining token efficiency and executing context compression in Hermes
- **`spike`**: Throwaway experiments to validate an idea before build.
- **`subagent-driven-development`**: Execute plans via delegate_task subagents (2-stage review).
- **`systematic-debugging`**: 4-phase root cause debugging: understand bugs before fixing.
- **`test-driven-development`**: TDD: enforce RED-GREEN-REFACTOR, tests before code.
- **`uv-package-management`**: Manage Python dependencies and virtual environments using uv.
- **`video-editing-moviepy`**: Video editing automation using MoviePy in Python, specifically for vertical 9:16 social media formats (Reels, TikTok,...
- **`web-mobile-ux-guidelines`**: Essential UI/UX design principles and best practices for developing responsive web apps across desktop and mobile.
- **`writing-plans`**: Write implementation plans: bite-sized tasks, paths, code.

### 📁 WEB-DEVELOPMENT

- **`chrome-extension-mv3-development`**: Official guidelines, architecture, and constraints for building Google Chrome Extensions using Manifest V3 (MV3).
- **`liff-external-payment-integration`**: Integrate external payments in LINE LIFF apps.
- **`line-liff-development`**: Development guide and pitfalls for LINE Front-end Framework (LIFF) apps based on official documentation.
- **`line-mini-app-liff-serverless`**: Create LINE MINI Apps using LIFF based on the SupremeTech serverless approach. Use when planning, designing, or build...
- **`nextjs-liff-fastapi-backend`**: Build a Next.js LIFF app using Python FastAPI with LangChain
- **`satangthebank-development`**: Guidelines and architecture specifics for developing and maintaining the SatangTheBank Omnichannel Ledger system (Nex...