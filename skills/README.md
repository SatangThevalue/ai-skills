# 🧠 AI Skills — Tonthong (ต้นทอง) Skill Library

> **Repository:** [SatangTheValue/ai-skills](https://github.com/SatangTheValue/ai-skills)  
> **ผู้ดูแล:** Thanapol Nanthakaset (Satang) · ผู้ช่วย: ต้นทอง (Hermes Agent)  
> **อัปเดตล่าสุด:** 2026-06-28

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
```

---

## 📁 โครงสร้างโฟลเดอร์

```
skills/                        ← โฟลเดอร์หลัก (sync กับ ~/.hermes/skills/)
├── devops/
│   ├── hermes-dashboard-traefik/SKILL.md
│   ├── docker-management/SKILL.md
│   └── ...
├── finance/
│   └── ...
├── software-development/
│   └── ...
└── README.md
```

> ⚠️ **สำคัญ:** โฟลเดอร์นี้ sync ตรงกับ `~/.hermes/skills/` บน VPS เท่านั้น  
> ต้นทองจะอัปเดตสารบัญและ Push ขึ้น GitHub ทุกครั้งที่มีการเพิ่ม/แก้ไข Skill

---

## 📚 สารบัญ Skills

> อัปเดตอัตโนมัติโดยต้นทอง — **229 skills** ใน **78 หมวด**


### 30x-growth-marketing-panel

| Skill | คำอธิบาย |
|-------|----------|
| `30x-growth-marketing-panel` | AI Growth Marketing Expert Panel with 11 world-class experts distilled from 4,00… |

### abstract-strategy

| Skill | คำอธิบาย |
|-------|----------|
| `abstract-strategy` | Design abstract strategy games with perfect information, no randomness, and stra… |

### account-maintenance

| Skill | คำอธิบาย |
|-------|----------|
| `account-maintenance` | Process account maintenance requests across the account lifecycle. Use when chan… |

### account-opening-compliance

| Skill | คำอธิบาย |
|-------|----------|
| `account-opening-compliance` | Embed compliance controls into account opening and verify regulatory readiness. … |

### agent-swarm

| Skill | คำอธิบาย |
|-------|----------|
| `flow-nexus-swarm` | AI swarm orchestration and management specialist. Deploys, coordinates, and scal… |

### ai-agent-wars

| Skill | คำอธิบาย |
|-------|----------|
| `AI Agent Wars 2026` | 2026年全球AI Agent平台竞争格局深度分析——OpenAI Codex vs Kimi vs 扣子 vs Dify vs LangChain vs 百炼… |

### ai-boss-assistant

| Skill | คำอธิบาย |
|-------|----------|
| `ai-boss-assistant` | Transform any AI into a professional executive assistant with battle-tested pers… |

### ai-product-strategy

| Skill | คำอธิบาย |
|-------|----------|
| `ai-product-strategy` | Help users define AI product strategy. Use when someone is building an AI produc… |

### ai-proposal-generator

| Skill | คำอธิบาย |
|-------|----------|
| `ai-proposal-generator` | Generate professional HTML proposals from meeting notes. Features 5 proposal sty… |

### aicoin-trading

| Skill | คำอธิบาย |
|-------|----------|
| `aicoin-trading` | **CEX 中心化交易所**(Binance / OKX / Bybit / Bitget 等)的下单交易工具。严格规则:(1) 所有订单必须通过 node s… |

### algorithmic-trading

| Skill | คำอธิบาย |
|-------|----------|
| `algorithmic-trading` | Use when building trading systems, backtesting strategies, implementing executio… |

### analyze

| Skill | คำอธิบาย |
|-------|----------|
| `analyze` | 个股深度分析。当用户说"分析XX"、"看看XX怎么样"、"XX值得买吗"、"研究一下XX"时使用此skill。 |

### api-integration

| Skill | คำอธิบาย |
|-------|----------|
| `innovestx-open-api` | Guide and implementation details for using InnovestX Digital Asset Open API. |

### apple

| Skill | คำอธิบาย |
|-------|----------|
| `apple-notes` | Manage Apple Notes via memo CLI: create, search, edit. |
| `apple-reminders` | Apple Reminders via remindctl: add, list, complete. |
| `findmy` | Track Apple devices/AirTags via FindMy.app on macOS. |
| `imessage` | Send and receive iMessages/SMS via the imsg CLI on macOS. |
| `macos-computer-use` | \| |

### aster-bot-trading

| Skill | คำอธิบาย |
|-------|----------|
| `aster-bot-trading` | Automated perpetual futures trading bot for AsterDEX with dual strategies, risk … |

### autonomous-ai-agents

| Skill | คำอธิบาย |
|-------|----------|
| `agent-frameworks-integration` | Use when designing, building, or orchestrating multi-agent systems using Google … |
| `codex` | Delegate coding to OpenAI Codex CLI (features, PRs). |
| `google-adk` | Use when building multi-agent systems with Google's Agent Development Kit (ADK),… |
| `hermes-agent` | Configure, extend, or contribute to Hermes Agent. |
| `hermes-gateway-resilience` | Restore and harden the Hermes Messaging Gateway on Linux when it goes inactive, … |
| `hermes-kanban-swarm` | Orchestrate, configure, and execute multi-agent workflows (Swarms) using Hermes … |
| `hermes-workspace-setup` | Set up and run Hermes Workspace on a VPS with gateway auth. |
| `kanban-codex-lane` | Use when a Hermes Kanban worker wants to run Codex CLI as an isolated implementa… |
| `opencode` | Delegate coding to OpenCode CLI (features, PR review). |
| `research-to-skill-pipeline` | Research and author Hermes skills on demand from the web. |
| `security-reviewer` | Security-focused code review |

### backtest-expert

| Skill | คำอธิบาย |
|-------|----------|
| `backtest-expert` | Expert guidance for systematic backtesting of trading strategies. Use when devel… |

### backtesting-trading-strategies

| Skill | คำอธิบาย |
|-------|----------|
| `backtesting-trading-strategies` | \| |

### backup-global-cognitive-brain-20260316-100703

| Skill | คำอธิบาย |
|-------|----------|
| `backup-global-cognitive-brain-20260316-100703` | — |

### badman-agent-rental

| Skill | คำอธิบาย |
|-------|----------|
| `badman-agent-rental` | — |

### blockchain

| Skill | คำอธิบาย |
|-------|----------|
| `evm` | Read-only EVM client: wallets, tokens, gas across 8 chains. |
| `hyperliquid` | Hyperliquid market data, account history, trade review. |
| `solana` | Query Solana blockchain data with USD pricing — wallet balances, token portfolio… |

### boss-ai-agent

| Skill | คำอธิบาย |
|-------|----------|
| `boss-ai-agent` | Boss AI Agent — AI management advisor and team operations middleware. Use this s… |

### business-analyst

| Skill | คำอธิบาย |
|-------|----------|
| `business-analyst` | Master modern business analysis with AI-powered analytics, real-time dashboards,… |

### business-growth-skills

| Skill | คำอธิบาย |
|-------|----------|
| `business-growth-skills` | Router/index for the 4 business & growth skills bundled in this plugin: customer… |

### business-health-diagnostic

| Skill | คำอธิบาย |
|-------|----------|
| `business-health-diagnostic` | Diagnose SaaS business health across growth, retention, efficiency, and capital.… |

### business-operations

| Skill | คำอธิบาย |
|-------|----------|
| `HR จัดการแรงงานไทย-ต่างชาติ (พม่า, ไทย, เขมร)` | คำแนะนำการจัดการ HR แรงงานชาวไทยและชาวต่างชาติ (พม่า, ไทย, เขมร) รวมถึงกฎหมาย, ร… |
| `wholesale-chicken-distribution` | คู่มือการดำเนินธุรกิจและขั้นตอนทางกฎหมายสำหรับการซื้อไก่สดจากโรงงานเพื่อขายส่งแล… |

### business-operations-skills

| Skill | คำอธิบาย |
|-------|----------|
| `business-operations-skills` | Use when running, diagnosing, or designing internal business operations — proces… |

### business-writing

| Skill | คำอธิบาย |
|-------|----------|
| `business-writing` | You are a professional business analyst, skilled in writing various industry res… |

### cfo

| Skill | คำอธิบาย |
|-------|----------|
| `CFO / Chief Financial Officer` | Be the CFO with financial planning, cash management, fundraising, capital alloca… |

### claim-investigation

| Skill | คำอธิบาย |
|-------|----------|
| `claim-investigation` | Systematically investigate social media claims and viral content. Use when fact-… |

### claw-smart-context

| Skill | คำอธิบาย |
|-------|----------|
| `smart-context` | Token-efficient agent behavior — response sizing, context pruning, tool efficien… |

### clerk-nextjs-patterns

| Skill | คำอธิบาย |
|-------|----------|
| `clerk-nextjs-patterns` | Advanced Next.js patterns - middleware, Server Actions, caching with |

### competitor-price-analysis

| Skill | คำอธิบาย |
|-------|----------|
| `competitor-price-analysis` | Competitor pricing strategy analysis and market positioning. Price mapping, pric… |

### computer-use

| Skill | คำอธิบาย |
|-------|----------|
| `computer-use` | \| |

### content-marketing-2026-2027

| Skill | คำอธิบาย |
|-------|----------|
| `content-marketing-2026-2027` | > |

### creative

| Skill | คำอธิบาย |
|-------|----------|
| `Heritage` | Architectural minimalism meets journalistic gravitas. |
| `architecture-diagram` | Dark-themed SVG architecture/cloud/infra diagrams as HTML. |
| `ascii-art` | ASCII art: pyfiglet, cowsay, boxes, image-to-ascii. |
| `ascii-video` | ASCII video: convert video/audio to colored ASCII MP4/GIF. |
| `baoyu-article-illustrator` | Article illustrations: type × style × palette consistency. |
| `baoyu-comic` | Knowledge comics (知识漫画): educational, biography, tutorial. |
| `baoyu-infographic` | Infographics: 21 layouts x 21 styles (信息图, 可视化). |
| `claude-design` | Design one-off HTML artifacts (landing, deck, prototype). |
| `comfyui` | Generate images, video, and audio with ComfyUI — install, launch, manage nodes/m… |
| `excalidraw` | Hand-drawn Excalidraw JSON diagrams (arch, flow, seq). |
| `humanizer` | Humanize text: strip AI-isms and add real voice. |
| `ideation` | Generate project ideas via creative constraints. |
| `manim-video` | Manim CE animations: 3Blue1Brown math/algo videos. |
| `p5js` | p5.js sketches: gen art, shaders, interactive, 3D. |
| `pixel-art` | Pixel art w/ era palettes (NES, Game Boy, PICO-8). |
| `popular-web-designs` | 54 real design systems (Stripe, Linear, Vercel) as HTML/CSS. |
| `pretext` | Use when building creative browser demos with @chenglou/pretext — DOM-free text … |
| `sketch` | Throwaway HTML mockups: 2-3 design variants to compare. |
| `songwriting-and-ai-music` | Songwriting craft and Suno AI music prompts. |
| `touchdesigner-mcp` | Control a running TouchDesigner instance via twozero MCP — create operators, set… |

### crypto-com-app

| Skill | คำอธิบาย |
|-------|----------|
| `crypto-com-app` | Execute crypto trades (buy, sell, swap, exchange), manage cash deposits and with… |

### crypto-market-rank

| Skill | คำอธิบาย |
|-------|----------|
| `crypto-market-rank` | \| |

### crypto-protocol-diagram

| Skill | คำอธิบาย |
|-------|----------|
| `crypto-protocol-diagram` | Extracts protocol message flow from source code, RFCs, academic papers, pseudoco… |

### crypto-report

| Skill | คำอธิบาย |
|-------|----------|
| `crypto-report` | Analyze cryptocurrency projects with tokenomics, on-chain metrics, and market an… |

### data-science

| Skill | คำอธิบาย |
|-------|----------|
| `jupyter-live-kernel` | Iterative Python via live Jupyter kernel (hamelnb). |
| `prefect-workflows` | Design, monitor, and run data orchestrations with Prefect. |

### deep-productivity

| Skill | คำอธิบาย |
|-------|----------|
| `deep-productivity` | Master deep work productivity through the three types of work framework (Buildin… |

### design-trends-2026

| Skill | คำอธิบาย |
|-------|----------|
| `design-trends-2026` | Apply 2026's top graphic design trends to any creative brief. Based on Kittl × S… |

### designing-growth-loops

| Skill | คำอธิบาย |
|-------|----------|
| `designing-growth-loops` | Help users design and optimize growth loops. Use when someone is building viral … |

### devops

| Skill | คำอธิบาย |
|-------|----------|
| `cli-proxy-api-troubleshooting` | Diagnose and fix cli-proxy-api provider and auth failures. |
| `docker-compose-git-update` | Pull Git updates and rebuild Docker Compose stacks safely. |
| `docker-management` | Manage Docker containers, images, volumes, networks, and Compose stacks — lifecy… |
| `hermes-dashboard-traefik` | Expose Hermes Dashboard via Traefik with SSL and systemd. |
| `kanban-orchestrator` | Decomposition playbook + anti-temptation rules for an orchestrator profile routi… |
| `kanban-worker` | Pitfalls, examples, and edge cases for Hermes Kanban workers. The lifecycle itse… |
| `n8n-traefik-postgres` | Deploy n8n with PostgreSQL via Traefik with required headers. |
| `nextjs-traefik-www-redirect` | Deploy Next.js standalone app with Traefik www redirection. |
| `postgres-pgvector-traefik` | Deploy PostgreSQL 18 with pgvector and Traefik TCP proxying. |
| `traefik-docker29-fix` | Fix Traefik Docker API errors on Docker Engine 29.4 plus. |
| `webhook-subscriptions` | Webhook subscriptions: event-driven agent runs. |

### dogfood

| Skill | คำอธิบาย |
|-------|----------|
| `dogfood` | Exploratory QA of web apps: find bugs, evidence, reports. |

### ecommerce-business-plan

| Skill | คำอธิบาย |
|-------|----------|
| `ecommerce-business-plan` | Create a comprehensive e-commerce business plan. Market analysis, financial proj… |

### email

| Skill | คำอธิบาย |
|-------|----------|
| `himalaya` | Himalaya CLI: IMAP/SMTP email from terminal. |

### executive-dashboard-generator

| Skill | คำอธิบาย |
|-------|----------|
| `executive-dashboard-generator` | Transform raw data from CSVs, Google Sheets, or databases into executive-ready r… |

### fastapi

| Skill | คำอธิบาย |
|-------|----------|
| `fastapi` | FastAPI best practices and conventions. Use when working with FastAPI APIs and P… |

### finance

| Skill | คำอธิบาย |
|-------|----------|
| `3-statement-model` | Build fully-integrated 3-statement models (IS, BS, CF) in Excel with working cap… |
| `business-ledger-and-inventory` | สกิลการวางผังบัญชี 5 หมวด การจดบันทึกทางการเงิน และการบริหารจัดการคลังสินค้าสำหร… |
| `comps-analysis` | Build comparable company analysis in Excel — operating metrics, valuation multip… |
| `cost-accounting-inventory` | การคำนวณบัญชีต้นทุนและการบริหารจัดการสินค้าคงคลัง (FIFO, Weighted Average, EOQ, … |
| `dcf-model` | Build institutional-quality DCF valuation models in Excel — revenue projections,… |
| `diy-accounting-setup` | คู่มือและขั้นตอนการวางระบบบัญชี เอกสารควบคุมภายใน และปฏิทินภาษีด้วยตนเองสำหรับธุ… |
| `excel-author` | Build auditable Excel workbooks headless with openpyxl — blue/black/green cell c… |
| `fresh-chicken-business-th` | คู่มือขั้นตอนปฏิบัติการตั้งธุรกิจและควบคุมคุณภาพการค้าไก่สดในประเทศไทย อัปเดตระเ… |
| `innovestx-api` | InnovestX Digital Asset Open API integration guide and Python client implementat… |
| `lbo-model` | Build leveraged buyout models in Excel — sources & uses, debt schedule, cash swe… |
| `merger-model` | Build accretion/dilution (merger) models in Excel — pro-forma P&L, synergies, fi… |
| `mt5-python-trading` | Guide and best practices for automated trading using Python and MetaTrader 5 (MT… |
| `personal-finance-and-investment` | Guide for personal finance management, asset allocation, and algorithmic trading… |
| `pptx-author` | Build PowerPoint decks headless with python-pptx. Pairs with excel-author for mo… |
| `research-backed-investing` | Use when designing asset allocation frameworks, developing algorithmic trading s… |
| `stocks` | Stock quotes, history, search, compare, crypto via Yahoo. |
| `thai-business-law-guide` | คู่มือและกฎหมายสำคัญในการประกอบธุรกิจในประเทศไทย ครอบคลุมการจัดตั้งธุรกิจ ภาษี แ… |
| `thai-business-license-guide` | คู่มือเงื่อนไขการขอรับใบอนุญาตและระเบียบการดำเนินงานของธุรกิจเฉพาะประเภทในประเทศ… |
| `thai-business-registration` | คู่มือขั้นตอนการจัดตั้งห้างหุ้นส่วนและบริษัทจำกัดในประเทศไทยผ่านระบบ DBD Biz Reg… |
| `thai-business-setup-guide` | คู่มือขั้นตอนปฏิบัติในการจัดตั้งบริษัทจำกัดและเริ่มต้นธุรกิจในประเทศไทย ผ่านระบบ… |
| `thai-corporate-and-partnership-law` | คู่มือกฎหมายห้างหุ้นส่วนจำกัด (หจก.) และบริษัทจำกัด (บจก.) ในประเทศไทย ตามประมวล… |
| `thai-corporate-structure-and-positions` | Use when designing corporate organizational structures, defining department role… |
| `thai-digital-accounting` | ทักษะและความรู้ด้านการบัญชีดิจิทัล ระบบภาษีอิเล็กทรอนิกส์ (e-Tax & e-Withholding… |
| `thai-finance-legal-guide` | Reference for Thai tax, stock, and crypto regulations. |
| `thai-personal-accounting-and-finance` | คู่มือและเครื่องมือการทำบัญชีส่วนบุคคล งบการเงิน และการวิเคราะห์อัตราส่วนสุขภาพท… |
| `thai-tax-planning-strategy` | Guide and strategies for legal tax planning and tax optimization (Tax Avoidance)… |
| `thai-trading-business` | คู่มือและขั้นตอนปฏิบัติการทำธุรกิจซื้อมาขายไป (Trading Business) ในประเทศไทย ครอ… |

### founder-sales

| Skill | คำอธิบาย |
|-------|----------|
| `founder-sales` | Help founders close their first customers and build repeatable sales processes. … |

### gaming

| Skill | คำอธิบาย |
|-------|----------|
| `minecraft-modpack-server` | Host modded Minecraft servers (CurseForge, Modrinth). |
| `pokemon-player` | Play Pokemon via headless emulator + RAM reads. |

### github

| Skill | คำอธิบาย |
|-------|----------|
| `codebase-inspection` | Inspect codebases w/ pygount: LOC, languages, ratios. |
| `github-auth` | GitHub auth setup: HTTPS tokens, SSH keys, gh CLI login. |
| `github-code-review` | Review PRs: diffs, inline comments via gh or REST. |
| `github-issues` | Create, triage, label, assign GitHub issues via gh or REST. |
| `github-pr-workflow` | GitHub PR lifecycle: branch, commit, open, CI, merge. |
| `github-repo-management` | Clone/create/fork repos; manage remotes, releases. |

### initial-traefik

| Skill | คำอธิบาย |
|-------|----------|
| `initial-traefik` | Initialize and configure Traefik reverse proxy with Docker. Install Traefik, con… |

### marketing

| Skill | คำอธิบาย |
|-------|----------|
| `ai-business-thai-platforms` | Use when designing, building, or implementing AI strategies for Thai businesses … |
| `ai-fluency-framework` | > |
| `ai-fluency-social-seo` | AI fluency และ Social SEO สำหรับการทำการตลาด 2026 - ใช้ AI เพื่อสร้างเนื้อหา เพิ… |
| `social-seo-checklist` | > |
| `thai-branding-strategy` | Use when creating, positioning, or executing personal and business branding stra… |
| `thai-content-compliance` | Use when creating content for Thai audiences, checking for forbidden words, comp… |
| `thailand-content-strategy-2026` | Use when planning, creating, or adapting content marketing strategies for the Th… |
| `thailand-market-demand-2026-2027` | Use to analyze macroeconomic trends, consumer demand, and sector-specific perfor… |

### mcp

| Skill | คำอธิบาย |
|-------|----------|
| `fastmcp` | Build, test, inspect, install, and deploy MCP servers with FastMCP in Python. Us… |
| `native-mcp` | MCP client: connect servers, register tools (stdio/HTTP). |

### media

| Skill | คำอธิบาย |
|-------|----------|
| `gif-search` | Search/download GIFs from Tenor via curl + jq. |
| `heartmula` | HeartMuLa: Suno-like song generation from lyrics + tags. |
| `songsee` | Audio spectrograms/features (mel, chroma, MFCC) via CLI. |
| `spotify` | Spotify: play, search, queue, manage playlists and devices. |
| `youtube-content` | YouTube transcripts to summaries, threads, blogs. |

### mlops

| Skill | คำอธิบาย |
|-------|----------|
| `audiocraft-audio-generation` | AudioCraft: MusicGen text-to-music, AudioGen text-to-sound. |
| `dspy` | DSPy: declarative LM programs, auto-optimize prompts, RAG. |
| `evaluating-llms-harness` | lm-eval-harness: benchmark LLMs (MMLU, GSM8K, etc.). |
| `huggingface-hub` | HuggingFace hf CLI: search/download/upload models, datasets. |
| `llama-cpp` | llama.cpp local GGUF inference + HF Hub model discovery. |
| `obliteratus` | OBLITERATUS: abliterate LLM refusals (diff-in-means). |
| `ollama-local-inference` | Run and manage local LLMs and embedding models using Ollama. |
| `segment-anything-model` | SAM: zero-shot image segmentation via points, boxes, masks. |
| `serving-llms-vllm` | vLLM: high-throughput LLM serving, OpenAI API, quantization. |
| `weights-and-biases` | W&B: log ML experiments, sweeps, model registry, dashboards. |

### modesty-adhd-assistant

| Skill | คำอธิบาย |
|-------|----------|
| `adhd-assistant` | ADHD-friendly life management assistant for SkillBoss API Hub. Helps with daily … |

### next-dev-loop

| Skill | คำอธิบาย |
|-------|----------|
| `next-dev-loop` | > |

### note-taking

| Skill | คำอธิบาย |
|-------|----------|
| `obsidian` | Read, search, create, and edit notes in the Obsidian vault. Provides vault-first… |

### personal-productivity

| Skill | คำอธิบาย |
|-------|----------|
| `personal-productivity` | Build a Personal Productivity System Pack (weekly timebox plan, capture+to-do sy… |

### postgresql

| Skill | คำอธิบาย |
|-------|----------|
| `postgresql` | Design a PostgreSQL-specific schema. Covers best-practices, data types, indexing… |

### productivity

| Skill | คำอธิบาย |
|-------|----------|
| `airtable` | Airtable REST API via curl. Records CRUD, filters, upserts. |
| `brain-hacking-and-productivity` | Neuroscience-based protocols for brain hacking, entering flow states, managing e… |
| `business-analysis-frameworks` | Use when analyzing business strategy, evaluating strengths/weaknesses (SWOT/TOWS… |
| `google-workspace` | Gmail, Calendar, Drive, Docs, Sheets via gws CLI or Python. |
| `here.now` | Publish static sites to {slug}.here.now and store private files in cloud Drives … |
| `linear` | Linear: manage issues, projects, teams via GraphQL + curl. |
| `maps` | Geocode, POIs, routes, timezones via OpenStreetMap/OSRM. |
| `nano-pdf` | Edit PDF text/typos/titles via nano-pdf CLI (NL prompts). |
| `notion` | Notion API + ntn CLI: pages, databases, markdown, Workers. |
| `obsidian-personal-templates` | \| |
| `obsidian-workflow` | \| |
| `ocr-and-documents` | Extract text from PDFs/scans (pymupdf, marker-pdf). |
| `online-income-and-monetization` | Strategies for online monetization, content creation, digital products, and buil… |
| `petdex` | Install and select animated petdex mascots for Hermes. |
| `powerpoint` | Create, read, edit .pptx decks, slides, notes, templates. |
| `teams-meeting-pipeline` | Operate the Teams meeting summary pipeline via Hermes CLI — summarize meetings, … |
| `thai-business-excellence` | Use when establishing, auditing, or improving business operations in Thailand us… |
| `time-management-and-productivity` | Guidelines for task prioritization, time blocking, and learning systems (Second … |
| `user-communication-preferences` | Embed a user's preferred communication style and action-oriented conventions for… |
| `vision-net-registrar` | Use when scraping or integrating academic data (schedules, grades, registration)… |

### raai-business-analyst-pro

| Skill | คำอธิบาย |
|-------|----------|
| `business-analyst-pro` | > |

### react-2026

| Skill | คำอธิบาย |
|-------|----------|
| `react-2026` | Provides a comprehensive guide to the modern React 2026 stack. Use when starting… |

### react-composition-2026

| Skill | คำอธิบาย |
|-------|----------|
| `react-composition-2026` | Teaches modern React composition patterns for 2025/2026. Use when designing comp… |

### red-teaming

| Skill | คำอธิบาย |
|-------|----------|
| `godmode` | Jailbreak LLMs: Parseltongue, GODMODE, ULTRAPLINIAN. |

### research

| Skill | คำอธิบาย |
|-------|----------|
| `arxiv` | Search arXiv papers by keyword, author, category, or ID. |
| `blogwatcher` | Monitor blogs and RSS/Atom feeds via blogwatcher-cli tool. |
| `llm-wiki` | Karpathy's LLM Wiki: build/query interlinked markdown KB. |
| `polymarket` | Query Polymarket: markets, prices, orderbooks, history. |
| `research-paper-writing` | Write ML papers for NeurIPS/ICML/ICLR: design→submit. |

### saas-productivity

| Skill | คำอธิบาย |
|-------|----------|
| `saas-productivity` | Use when designing animations for business tools, project management, collaborat… |

### smart-home

| Skill | คำอธิบาย |
|-------|----------|
| `openhue` | Control Philips Hue lights, scenes, rooms via OpenHue CLI. |

### social-media

| Skill | คำอธิบาย |
|-------|----------|
| `xurl` | X/Twitter via xurl CLI: post, search, DM, media, v2 API. |

### software-development

| Skill | คำอธิบาย |
|-------|----------|
| `agent-skills-github-sync` | Use when synchronizing Hermes Agent local skills with a remote GitHub repository… |
| `better-auth-nextjs` | Configure modern authentication in Next.js using better-auth. |
| `business-dss-development` | Use when designing, building, or evaluating Business Decision Support Systems (D… |
| `cli-proxy-api-management` | Configure and query the CLIProxyAPI management endpoints. |
| `cliproxy-quota-check` | Check CLIProxyAPI account quota and request success/failure counts. |
| `cliproxy-quota-inspector` | Query and inspect CLIProxyAPI account statuses and request quotas. |
| `debugging-hermes-tui-commands` | Debug Hermes TUI slash commands: Python, gateway, Ink UI. |
| `deep-agents-python` | Guide and best practices for using LangChain's Deep Agents framework (langchain-… |
| `hermes-s6-container-supervision` | Modify, debug, or extend the s6-overlay supervision tree inside the Hermes Agent… |
| `langgraph-development` | Best practices for building and tracing AI agents with LangGraph, Deep Agents, a… |
| `my-skill-name               # lowercase, hyphens, ≤64 chars (MAX_NAME_LENGTH)` | Use when <trigger>. <one-line behavior>. |
| `nextjs-16-migration` | Comprehensive guide and checklist for upgrading to Next.js 16, covering Turbopac… |
| `nextjs-spa-static-export` | Best practices for building Single-Page Applications (SPA) and static sites with… |
| `nextjs-ui-libraries` | Top UI libraries and UX frameworks for Next.js (shadcn/ui, Tailwind, NextUI, Cha… |
| `node-inspect-debugger` | Debug Node.js via --inspect + Chrome DevTools Protocol CLI. |
| `plan` | Plan mode: write markdown plan to .hermes/plans/, no exec. |
| `python-debugpy` | Debug Python: pdb REPL + debugpy remote (DAP). |
| `requesting-code-review` | Pre-commit review: security scan, quality gates, auto-fix. |
| `satang-project-suite` | Develop and deploy Thanapol's custom AI and trading projects. |
| `simplify-code` | Parallel 3-agent cleanup of recent code changes. |
| `smart-context-usage` | Guidelines for maintaining token efficiency and executing context compression in… |
| `spike` | Throwaway experiments to validate an idea before build. |
| `subagent-driven-development` | Execute plans via delegate_task subagents (2-stage review). |
| `systematic-debugging` | 4-phase root cause debugging: understand bugs before fixing. |
| `test-driven-development` | TDD: enforce RED-GREEN-REFACTOR, tests before code. |
| `uv-package-management` | Manage Python dependencies and virtual environments using uv. |
| `web-mobile-ux-guidelines` | Essential UI/UX design principles and best practices for developing responsive w… |
| `writing-plans` | Write implementation plans: bite-sized tasks, paths, code. |

### traefik

| Skill | คำอธิบาย |
|-------|----------|
| `Traefik` | Avoid common Traefik mistakes — router priority, TLS configuration, Docker label… |

### web

| Skill | คำอธิบาย |
|-------|----------|
| `Web Development` | Build, debug, and deploy websites with HTML, CSS, JavaScript, modern frameworks,… |

### web-development

| Skill | คำอธิบาย |
|-------|----------|
| `line-liff-development` | Development guide and pitfalls for LINE Front-end Framework (LIFF) apps based on… |
| `web-development` | Use when users need to implement, integrate, debug, build, deploy, or validate a… |

### yuanbao

| Skill | คำอธิบาย |
|-------|----------|
| `yuanbao` | Yuanbao (元宝) groups: @mention users, query info/members. |

---

*Generated and maintained by ต้นทอง (Tonthong) — Hermes Agent for Satang*
