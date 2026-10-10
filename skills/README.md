# 🧠 AI Skills — Tonthong (ต้นทอง) Skill Library

> **Repository:** [SatangTheValue/ai-skills](https://github.com/SatangTheValue/ai-skills)  
> **ผู้ดูแล:** Thanapol N (Satang) · ผู้ช่วย: ต้นทอง (Hermes Agent)  
> **อัปเดตล่าสุด:** 2026-10-10

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

## 📚 รายชื่อ Skills แบ่งตามหมวดหมู่ (508 skills ใน 28 หมวดหมู่)

### 📁 .ARCHIVE (66)

- **`airtable`**: Airtable REST API via curl. Records CRUD, filters, upserts.
- **`apple-notes`**: Manage Apple Notes via memo CLI: create, search, edit.
- **`apple-reminders`**: Apple Reminders via remindctl: add, list, complete.
- **`architecture-diagram`**: Dark-themed SVG architecture/cloud/infra diagrams as HTML.
- **`arxiv`**: Search arXiv papers by keyword, author, category, or ID.
- **`ascii-art`**: ASCII art: pyfiglet, cowsay, boxes, image-to-ascii.
- **`ascii-video`**: ASCII video: convert video/audio to colored ASCII MP4/GIF.
- **`audiocraft-audio-generation`**: AudioCraft: MusicGen text-to-music, AudioGen text-to-sound.
- **`baoyu-infographic`**: Infographics: 21 layouts x 21 styles (信息图, 可视化).
- **`blogwatcher`**: Monitor blogs and RSS/Atom feeds via blogwatcher-cli tool.
- **`claude-code`**: Delegate coding to Claude Code CLI (features, PRs).
- **`codebase-inspection`**: Inspect codebases w/ pygount: LOC, languages, ratios.
- **`codex`**: Delegate coding to OpenAI Codex CLI (features, PRs).
- **`comfyui`**: Generate images, video, and audio with ComfyUI — install, launch, manage nodes/models, run workflows with parameter injection. Uses the official comfy-cli for lifecycle and direct REST/WebSocket API for execution.
- **`computer-use`**: |
- **`design-md`**: Author/validate/export Google's DESIGN.md token spec files.
- **`dogfood`**: Exploratory QA of web apps: find bugs, evidence, reports.
- **`evaluating-llms-harness`**: lm-eval-harness: benchmark LLMs (MMLU, GSM8K, etc.).
- **`excalidraw`**: Hand-drawn Excalidraw JSON diagrams (arch, flow, seq).
- **`findmy`**: Track Apple devices/AirTags via FindMy.app on macOS.
- **`gif-search`**: Search/download GIFs from Tenor via curl + jq.
- **`github-auth`**: GitHub auth setup: HTTPS tokens, SSH keys, gh CLI login.
- **`github-code-review`**: Review PRs: diffs, inline comments via gh or REST.
- **`github-issues`**: Create, triage, label, assign GitHub issues via gh or REST.
- **`github-pr-workflow`**: GitHub PR lifecycle: branch, commit, open, CI, merge.
- **`heartmula`**: HeartMuLa: Suno-like song generation from lyrics + tags.
- **`huggingface-hub`**: HuggingFace hf CLI: search/download/upload models, datasets.
- **`humanizer`**: Humanize text: strip AI-isms and add real voice.
- **`imessage`**: Send and receive iMessages/SMS via the imsg CLI on macOS.
- **`jupyter-live-kernel`**: Iterative Python via live Jupyter kernel (hamelnb).
- **`llama-cpp`**: llama.cpp local GGUF inference + HF Hub model discovery.
- **`llm-wiki`**: Karpathy's LLM Wiki: build/query interlinked markdown KB.
- **`manim-video`**: Manim CE animations: 3Blue1Brown math/algo videos.
- **`maps`**: Geocode, POIs, routes, timezones via OpenStreetMap/OSRM.
- **`nano-pdf`**: Edit PDF text/typos/titles via nano-pdf CLI (NL prompts).
- **`node-inspect-debugger`**: Debug Node.js via --inspect + Chrome DevTools Protocol CLI.
- **`notion`**: Notion API + ntn CLI: pages, databases, markdown, Workers.
- **`obsidian`**: Read, search, create, and edit notes in the Obsidian vault. Provides vault-first templates, canonical data schema, and repeatable scripts for financial-ledger workflows in Obsidian.
- **`ocr-and-documents`**: Extract text from PDFs/scans (pymupdf, marker-pdf).
- **`ollama-local-inference`**: Run and manage local LLMs and embedding models using Ollama.
- **`opencode`**: Delegate coding to OpenCode CLI (features, PR review).
- **`openhue`**: Control Philips Hue lights, scenes, rooms via OpenHue CLI.
- **`p5js`**: p5.js sketches: gen art, shaders, interactive, 3D.
- **`petdex`**: Install and select animated petdex mascots for Hermes.
- **`polymarket`**: Query Polymarket: markets, prices, orderbooks, history.
- **`popular-web-designs`**: 54 real design systems (Stripe, Linear, Vercel) as HTML/CSS.
- **`powerpoint`**: Create, read, edit .pptx decks, slides, notes, templates.
- **`pretext`**: Use when building creative browser demos with @chenglou/pretext — DOM-free text layout for ASCII art, typographic flow around obstacles, text-as-geometry games, kinetic typography, and text-powered generative art. Produces single-file HTML demos by default.
- **`python-debugpy`**: Debug Python: pdb REPL + debugpy remote (DAP).
- **`requesting-code-review`**: Pre-commit review: security scan, quality gates, auto-fix.
- **`research-paper-writing`**: Write ML papers for NeurIPS/ICML/ICLR: design→submit.
- **`segment-anything-model`**: SAM: zero-shot image segmentation via points, boxes, masks.
- **`serving-llms-vllm`**: vLLM: high-throughput LLM serving, OpenAI API, quantization.
- **`simplify-code`**: Parallel 3-agent cleanup of recent code changes.
- **`sketch`**: Throwaway HTML mockups: 2-3 design variants to compare.
- **`songsee`**: Audio spectrograms/features (mel, chroma, MFCC) via CLI.
- **`spike`**: Throwaway experiments to validate an idea before build.
- **`systematic-debugging`**: 4-phase root cause debugging: understand bugs before fixing.
- **`teams-meeting-pipeline`**: Operate the Teams meeting summary pipeline via Hermes CLI — summarize meetings, inspect pipeline status, replay jobs, manage Microsoft Graph subscriptions.
- **`test-driven-development`**: TDD: enforce RED-GREEN-REFACTOR, tests before code.
- **`thai-finance-legal-guide`**: Reference for Thai tax, stock, and crypto regulations.
- **`touchdesigner-mcp`**: Control a running TouchDesigner instance via twozero MCP — create operators, set parameters, wire connections, execute Python, build real-time visuals. 36 native tools.
- **`weights-and-biases`**: W&B: log ML experiments, sweeps, model registry, dashboards.
- **`xurl`**: X/Twitter via xurl CLI: post, search, DM, media, v2 API.
- **`youtube-content`**: YouTube transcripts to summaries, threads, blogs.
- **`yuanbao`**: Yuanbao (元宝) groups: @mention users, query info/members.

### 📁 API-INTEGRATION (1)

- **`innovestx-open-api`**: Guide and implementation details for using InnovestX Digital Asset Open API.

### 📁 APPLE (1)

- **`macos-computer-use`**: |

### 📁 ARCHITECTURE (2)

- **`ddex-metadata-architecture`**: Refactors flat music metadata into relational DDEX standards.
- **`loop-engineering-onboarding`**: Scaffolds Loop Engineering, tailwind v4, and binds subagents.

### 📁 AUTOMATION (1)

- **`python-media-automation`**: Best practices, pitfalls, and configuration fixes for running Python media libraries (MoviePy, Piper TTS, Pedalboard, PyDub) in automated pipelines or async servers.

### 📁 AUTONOMOUS-AI-AGENTS (25)

- **`agent-frameworks-integration`**: Use when designing, building, or orchestrating multi-agent systems via A2A or LangGraph.
- **`agent-reach-integration`**: Install, configure, and operate the Agent Reach (Panniantong) framework to give agents internet channel access (X, Reddit, Bilibili, YouTube, Exa).
- **`agent-swarm`**: Agent skill for swarm - invoke with $agent-swarm
- **`claude-handoff`**: Hand the current conversation off to a fresh background agent that picks up the work immediately.
- **`course-to-skill-pipeline`**: Convert course syllabi into actionable skills with rubrics.
- **`cron-job-workflows`**: Guidelines and pitfalls for executing headless, non-interactive tasks as a scheduled cron job in Hermes.
- **`dispatching-parallel-agents`**: Use when facing 2+ independent tasks that can be worked on without shared state or sequential dependencies
- **`find-skills`**: Helps users discover and install agent skills when they ask questions like "how do I do X", "find a skill for X", "is there a skill that can...", or express interest in extending capabilities. This skill should be used when the user is looking for functionality that might exist as an installable skill.
- **`google-adk`**: Use when building multi-agent systems with Google's Agent Development Kit (ADK), configuring agents, tools, workflows, state, and sessions.
- **`handoff`**: Compact the current conversation into a handoff document for another agent to pick up.
- **`hermes-agent`**: Configure, extend, or contribute to Hermes Agent.
- **`hermes-discord-setup`**: Configure and enable the Discord bot integration for Hermes.
- **`hermes-gateway-resilience`**: Restore and harden the Hermes Messaging Gateway on Linux when it goes inactive, drops platform connections, or fails under low-disk pressure.
- **`hermes-kanban-swarm`**: Orchestrate, configure, and execute multi-agent workflows (Swarms) using Hermes Kanban boards and profiles.
- **`hermes-profile-customization`**: Create and customize isolated profiles in Hermes.
- **`hermes-telegram-agent-provisioning`**: Provision an isolated profile as a Telegram daemon.
- **`hermes-workspace-setup`**: Set up and run Hermes Workspace on a VPS with gateway auth.
- **`kanban-codex-lane`**: Use when a Hermes Kanban worker wants to run Codex CLI as an isolated implementation lane while Hermes keeps ownership of task lifecycle, reconciliation, testing, and handoff.
- **`research-to-skill-pipeline`**: Research and author Hermes skills on demand from the web.
- **`satang-ai-gateway`**: Satang AI: Integration patterns for FastAPI Gateway, Better Auth, and LINE OA.
- **`skillopt-sleep`**: Validate and refine agent skills through nightly sleep cycles with held-out gates. Wraps Microsoft's SkillOpt-Sleep engine.
- **`smart-context`**: Token-efficient agent behavior — response sizing, context pruning, tool efficiency, and delegation
- **`subagent-driven-development`**: Use when executing implementation plans with independent tasks in the current session
- **`using-superpowers`**: Use when starting any conversation - establishes how to find and use skills, requiring skill invocation before ANY response including clarifying questions
- **`wayfinder`**: Plan a huge chunk of work (more than one agent session can hold) as a shared map of decision tickets on your issue tracker, and resolve them one at a time until the way to the destination is clear.

### 📁 BLOCKCHAIN (3)

- **`evm`**: Read-only EVM client: wallets, tokens, gas across 8 chains.
- **`hyperliquid`**: Hyperliquid market data, account history, trade review.
- **`solana`**: Query Solana blockchain data with USD pricing — wallet balances, token portfolios with values, transaction details, NFTs, whale detection, and live network stats. Uses Solana RPC + CoinGecko. No API key required.

### 📁 BUSINESS (24)

- **`account-maintenance`**: Process account maintenance requests across the account lifecycle. Use when changing a client address or contact info with identity verification, updating beneficiary designations after marriage, divorce, birth, or death, re-registering or re-titling an account to a trust or new entity, selecting tax lot methods or fixing cost basis records, applying legal or compliance holds or Reg T freezes, setting up systematic withdrawals or standing instructions, processing a death notification and estate account setup, handling a QDRO, power of attorney, or guardianship, closing accounts and managing escheatment, or designing data quality review programs.
- **`account-opening-compliance`**: Embed compliance controls into account opening and verify regulatory readiness. Use when designing CIP/KYC identity verification gates, implementing OFAC and sanctions screening at onboarding, collecting beneficial ownership certification for entity or trust accounts, building risk-based approval tiers that route applications by risk level, defining compliance screening requirements and exception tracking, adding senior investor protections (FINRA Rules 2165/4512) or trusted contact procedures, establishing CDD risk ratings and ongoing monitoring triggers, or preparing account opening procedures for SEC or FINRA examination. For the operational pipeline these controls plug into, see account-opening-workflow.
- **`admin-hub-refactoring`**: Audits and plans a complete e-commerce admin refactoring.
- **`ai-boss-assistant`**: Transform any AI into a professional executive assistant with battle-tested personas and workflows. Complete templates for Google Workspace integration (Gmail, Calendar, Drive), milestone delivery system, and security guidelines.
- **`ai-product-strategy`**: Help users define AI product strategy. Use when someone is building an AI product, deciding where to apply AI in their product, planning an AI roadmap, evaluating build vs buy for AI capabilities, or figuring out how to integrate AI into existing products.
- **`business-analyst`**: Master modern business analysis with AI-powered analytics, real-time dashboards, and data-driven insights. Build comprehensive KPI frameworks, predictive models, and strategic recommendations.
- **`business-analyst-pro`**: >
- **`business-growth-skills`**: Router/index for the 4 business & growth skills bundled in this plugin: customer-success-manager (health scoring, churn risk, expansion), sales-engineer (RFP analysis, competitive matrices, PoC planning), revenue-operations (pipeline, forecast accuracy, GTM efficiency), and contract-and-proposal-writer. Use when a growth/revenue request doesn't obviously match one skill and you need to pick the right one (e.g., 'which accounts are at risk', 'should we bid on this RFP').
- **`business-health-diagnostic`**: Diagnose SaaS business health across growth, retention, efficiency, and capital. Use when preparing a business review or prioritizing urgent fixes.
- **`business-operations-skills`**: Use when running, diagnosing, or designing internal business operations — process documentation, vendor SLAs, capacity planning, internal comms, SOP/runbook authoring, procurement spend. Triggers on "BizOps review", "where's the bottleneck", "vendor health", "internal SOP", "all-hands deck", "spend categorization", "capacity for Q3", "process mapping". Forks context to route to one of six BizOps sub-skills (process-mapper, vendor-management, capacity-planner, internal-comms, knowledge-ops, procurement-optimizer) and returns a digest. Distinct from business-growth (external sales motion) and c-level-advisor (strategic, not operational).
- **`business-writing`**: You are a professional business analyst, skilled in writing various industry research reports, business insights, consulting analyses, company research reports, competitive analysis, user research, market analysis, and more.## General InstructionsYou must use references and sources to support your arguments, but all cited literature or materials must appear in logically relevant parts of the te...
- **`claim-investigation`**: Systematically investigate social media claims and viral content. Use when fact-checking complex claims, when decomposing multi-part assertions, or when investigating narratives that mix facts with interpretation.
- **`competitor-price-analysis`**: Competitor pricing strategy analysis and market positioning. Price mapping, pricing gaps identification, elasticity signals evaluation, and strategic pricing optimization. Use when the user asks about competitor pricing, price analysis, pricing strategy, or competitive pricing research.
- **`creator-operations-architecture`**: Builds music creator dashboards, payouts, and analytics.
- **`designing-growth-loops`**: Help users design and optimize growth loops. Use when someone is building viral mechanics, designing referral programs, creating product-led acquisition, or figuring out how to make their product grow itself.
- **`ecommerce-business-plan`**: Create a comprehensive e-commerce business plan. Market analysis, financial projections, marketing strategy, operations planning, and milestone roadmap for new or growing e-commerce businesses.
- **`executive-dashboard-generator`**: Transform raw data from CSVs, Google Sheets, or databases into executive-ready reports with visualizations, key metrics, trend analysis, and actionable recommendations. Creates data-driven narratives for leadership. Use when users need to turn spreadsheets into executive summaries or board reports.
- **`founder-sales`**: Help founders close their first customers and build repeatable sales processes. Use when someone is doing founder-led sales, trying to get their first customers, writing cold outreach, running early sales calls, or asking when to hire their first salesperson.
- **`marketplace-bi-analytics`**: Calculates marketplace GMV, take rate, and sales forecasts.
- **`open-source-ai-monetization`**: Deploy open-source AI repos into profitable businesses.
- **`prefect-monetization-orchestration`**: Blueprint for replacing n8n and simple cronjobs with Prefect 2.x/3.x for enterprise-grade, code-based orchestration of Thai monetization pipelines.
- **`prefect-zero-touch-blueprint`**: Enterprise architecture, strict coding standards, fallback rules, and Dockerized setup for the Zero-Touch Monetization suite using Prefect.
- **`thailand-monetization-2026`**: Predictive trends and architectural strategies for generating income in Thailand (2026-2027), focusing on AI automation, algorithmic trading, and SaaS.
- **`thailand-monetization-playbooks`**: Detailed execution methods and concrete examples for the 4 pillars of Thai monetization (Faceless Media, LINE Agents, Quant Trading, DaaS).

### 📁 BUSINESS-OPERATIONS (2)

- **`HR จัดการแรงงานไทย-ต่างชาติ (พม่า, ไทย, เขมร)`**: คำแนะนำการจัดการ HR แรงงานชาวไทยและชาวต่างชาติ (พม่า, ไทย, เขมร) รวมถึงกฎหมาย, ระบบเงินเดือน, ประกันสังคม และเอกสารที่ต้องมี
- **`wholesale-chicken-distribution`**: คู่มือการดำเนินธุรกิจและขั้นตอนทางกฎหมายสำหรับการซื้อไก่สดจากโรงงานเพื่อขายส่งและขนส่งไปต่างจังหวัดในประเทศไทย

### 📁 CREATIVE (7)

- **`abstract-strategy`**: Design abstract strategy games with perfect information, no randomness, and strategic depth. Use when designing a board game, exploring abstract strategy games, brainstorming game mechanics, or evaluating game balance. Keywords: board game, game design, strategy, mechanics, balance.
- **`baoyu-article-illustrator`**: Article illustrations: type × style × palette consistency.
- **`baoyu-comic`**: Knowledge comics (知识漫画): educational, biography, tutorial.
- **`claude-design`**: Design one-off HTML artifacts (landing, deck, prototype).
- **`ideation`**: Generate project ideas via creative constraints.
- **`pixel-art`**: Pixel art w/ era palettes (NES, Game Boy, PICO-8).
- **`songwriting-and-ai-music`**: Songwriting craft and Suno AI music prompts.

### 📁 DATA-SCIENCE (2)

- **`data-science-and-engineering`**: Principles, methods, techniques, and workflows for Data Science (DS) and Data Engineering (DE).
- **`prefect-workflows`**: Design, monitor, and run data orchestrations with Prefect.

### 📁 DATA-STORYTELLING-PAGE-LAUNCH (1)

- **`data-storytelling-page-launch`**: Plan, design, and automate data storytelling social media pages.

### 📁 DEVOPS (43)

- **`9router`**: Entry point for 9Router — local/remote AI gateway with OpenAI-compatible REST for chat, image, TTS, embeddings, web search, web fetch. Use when the user mentions 9Router, NINEROUTER_URL, or wants AI without writing provider boilerplate. This skill covers setup + indexes capability skills; fetch the relevant capability SKILL.md from the URLs below when needed.
- **`9router-chat`**: Chat / code generation via 9Router using OpenAI /v1/chat/completions or Anthropic /v1/messages format with streaming + auto-fallback combos. Use when the user wants to ask an LLM, generate code, summarize text, or run prompts through 9Router.
- **`9router-docker-deployment`**: Deploy and troubleshoot 9Router via Docker and Tailscale with password/DB injection fixes.
- **`9router-embeddings`**: Generate vector embeddings via 9Router for RAG, semantic search, similarity.
- **`9router-image`**: Generate images via 9Router /v1/images/generations using OpenAI / Gemini Imagen / DALL-E / FLUX / MiniMax / SDWebUI / ComfyUI / Codex models. Use when the user wants to create, generate, draw, or render an image, picture, or text-to-image (txt2img).
- **`9router-stt`**: Speech-to-text via 9Router /v1/audio/transcriptions using OpenAI Whisper / Groq / Gemini / Deepgram / AssemblyAI / NVIDIA / HuggingFace models. Use when the user wants to transcribe audio, convert speech to text, or get subtitles from audio files.
- **`9router-tts`**: Text-to-speech via 9Router /v1/audio/speech — OpenAI, ElevenLabs, Edge TTS, Google TTS, and more.
- **`9router-web-fetch`**: Fetch URL → markdown / text / HTML via 9Router /v1/web/fetch using Ollama Cloud / Firecrawl / Jina Reader / Tavily Extract / Exa Contents. Use when the user wants to scrape a webpage, extract URL content, read article, or convert a URL to markdown.
- **`9router-web-search`**: Web and X search via 9Router /v1/search using Tavily / Exa / Brave / Serper / SearXNG / Google PSE / Linkup / SearchAPI / You.com / Perplexity / Xquik. Use when the user wants to search the web, find articles, or search public X posts.
- **`ai-telemetry-and-billing`**: Implement database telemetry to track LLM token usage, latency, and estimated costs.
- **`cli-proxy-api-quota-and-update`**: Check CLIProxyAPI account quota and update binary to latest release.
- **`cli-proxy-api-troubleshooting`**: Diagnose and fix cli-proxy-api provider and auth failures.
- **`disk-space-management-docker-builds`**: Prevent disk space exhaustion during Docker container builds.
- **`docker-compose-git-update`**: Pull Git updates and rebuild Docker Compose stacks safely.
- **`docker-compose-orchestration`**: Container orchestration with Docker Compose for multi-container applications, networking, volumes, and production deployment
- **`docker-management`**: Manage Docker containers, images, volumes, networks, and Compose stacks — lifecycle ops, debugging, cleanup, and Dockerfile optimization.
- **`hermes-dashboard-traefik`**: Expose Hermes Dashboard via Traefik with SSL and systemd.
- **`hermes-production-deploy`**: Procedural best practices for deploying Node.js (Next.js) and Python (FastAPI) SaaS applications on Hermes-managed VPS with Docker/Traefik.
- **`hermes-profile-telegram-gateway`**: Configure and verify Telegram gateway for a named Hermes profile.
- **`hermes-zero-trust-infrastructure`**: Deploy Hermes Gateway, WebUI, and 9Router via Tailscale.
- **`hybrid-fastapi-line-deployment`**: Deploy and debug FastAPI LINE bots behind Traefik.
- **`infisical-secrets-management`**: Self-host and implement Infisical for secure environment variable management.
- **`initial-traefik`**: Initialize and configure Traefik reverse proxy with Docker. Install Traefik, configure Docker Compose, set up service routing via path prefix or host-based routing, enable features like dashboard metrics logging tracing, configure Dashboard access via nip.io or path prefix
- **`kanban-orchestrator`**: Decomposition playbook + anti-temptation rules for an orchestrator profile routing work through Kanban. The "don't do the work yourself" rule and the basic lifecycle are auto-injected into every kanban worker's system prompt; this skill is the deeper playbook when you're specifically playing the orchestrator role.
- **`kanban-worker`**: Pitfalls, examples, and edge cases for Hermes Kanban workers. The lifecycle itself is auto-injected into every worker's system prompt as KANBAN_GUIDANCE (from agent/prompt_builder.py); this skill is what you load when you want deeper detail on specific scenarios.
- **`line-bot-sdk-python`**: LINE Bot SDK (Python) สำหรับ Hermes
- **`linux-security-hardening`**: Hardening Linux VPS environments, securing Docker ports, configuring UFW, and responding to rogue/malware processes.
- **`linux-server-administration`**: Linux server administration, malware remediation, firewall (UFW) setup, and non-interactive sudo execution techniques.
- **`llm-prompt-orchestration`**: Pipeline for querying local CLIProxyAPI to generate content scripts.
- **`n8n-traefik-postgres`**: Deploy n8n with PostgreSQL via Traefik with required headers.
- **`nextjs-traefik-www-redirect`**: Deploy Next.js standalone app with Traefik www redirection.
- **`postgres-pgvector-traefik`**: Deploy PostgreSQL 18 with pgvector and Traefik TCP proxying.
- **`postgresql`**: Design a PostgreSQL-specific schema. Covers best-practices, data types, indexing, constraints, performance patterns, and advanced features
- **`prefect-orchestration`**: Set up and manage Prefect workflows, task queues, and auto-publishing pipelines.
- **`prefect-orchestration-monetization`**: Schedule and monitor the Zero-Touch Monetization pipeline using Prefect, with Infisical and A2A integration.
- **`skill-credential-sanitization`**: Sanitize credentials and secrets in skill repositories.
- **`tailscale-docker-zero-trust`**: Secure Docker container deployments by binding critical services explicitly to Tailscale VPN IPs (Zero-Trust) instead of 0.0.0.0 or 127.0.0.1.
- **`telegram-polling-conflict-troubleshooting`**: Resolve Telegram bot getUpdates polling conflicts.
- **`Traefik`**: Avoid common Traefik mistakes — router priority, TLS configuration, Docker labels syntax, and middleware ordering.
- **`traefik-docker29-fix`**: Fix Traefik Docker API errors on Docker Engine 29.4 plus.
- **`tts-audio-post-processing`**: Techniques for processing, chunking, and mastering AI-generated Thai audio (Edge-TTS / gTTS).
- **`vps-disk-space-recovery`**: Recover emergency host disk space on constrained Linux VPS.
- **`webhook-subscriptions`**: Webhook subscriptions: event-driven agent runs.

### 📁 DOMAIN-KNOWLEDGE (1)

- **`music-metadata-standards`**: DDEX and Believe compliant metadata structures for music catalogs.

### 📁 EMAIL (1)

- **`himalaya`**: Himalaya CLI: IMAP/SMTP email from terminal.

### 📁 FINANCE (157)

- **`3-statement-model`**: Build fully-integrated 3-statement models (IS, BS, CF) in Excel with working capital schedules, D&A roll-forwards, debt schedule, and the plugs that make cash and retained earnings tie. Pairs with excel-author.
- **`ai-trading-continuous-learning`**: Architecture and guidelines for building a Continuous Learning Pipeline for AI Trading models (Data Lake to MT5 ONNX) targeting Risk-adjusted Returns.
- **`aicoin-trading`**: **CEX 中心化交易所**(Binance / OKX / Bybit / Bitget 等)的下单交易工具。严格规则:(1) 所有订单必须通过 node scripts/exchange.mjs create_order 执行,禁止写自定义代码下单 (2) create_order 分两步:第一次返回预览,展示给用户等确认,用户说确认后第二次加 confirmed=true 执行 (3) 禁止自动确认,禁止跳过预览 (4) 平仓必须用 close_position,禁止用 create_order 构建平仓单。Trigger 关键词: 'buy on okx', 'sell on binance', '在 OKX 买 BTC', '在 Binance 下单', '做多 BTC 永续', '杠杆做空 ETH', '平掉我的 SOL 仓位', 'CEX 下单', '现货买入', '合约开仓', '永续平仓', '止盈止损', 'long', 'short', 'leverage', '买', '卖', '下单', '做多', '做空', '开仓', '平仓', '平掉', '关仓'. **路由提示**: 用户说“链上 swap / Uniswap / DEX 买 PEPE / Solana 上买”是**链上 DEX 交易**,应走 `aicoin-onchain` 而不是本 skill. Hyperliquid 上的下单也走 aicoin-onchain(HL 是链上 perp DEX),不是这里. 本 skill **只**处理 CEX 现货 + 永续合约下单。
- **`algorithmic-trading`**: Use when building trading systems, backtesting strategies, implementing execution algorithms, or analyzing market microstructure - covers strategy development, risk management, and production deploymentUse when ", " mentioned.
- **`analyze`**: 个股深度分析。当用户说"分析XX"、"看看XX怎么样"、"XX值得买吗"、"研究一下XX"时使用此skill。
- **`asset-specific-quant-pipeline`**: Build and deploy asset-specific AI trading pipelines.
- **`aster-bot-trading`**: Automated perpetual futures trading bot for AsterDEX with dual strategies, risk management, and TypeScript/Node.js stack
- **`backtest-expert`**: Expert guidance for systematic backtesting of trading strategies. Use when developing, testing, stress-testing, or validating quantitative trading strategies. Covers "beating ideas to death" methodology, parameter robustness testing, slippage modeling, bias prevention, and interpreting backtest results. Applicable when user asks about backtesting, strategy validation, robustness testing, avoiding overfitting, or systematic trading development.
- **`backtesting-py-mean-reversion`**: วิธีเขียนโค้ดและทำ Optimization กลยุทธ์ Mean Reversion ด้วยไลบรารี Backtesting.py
- **`backtesting-trading-strategies`**: |
- **`build-ea-python-strategy`**: Guidelines and architecture for building Expert Advisors using Python and MT5.
- **`business-investment-advisor`**: >
- **`business-ledger-and-inventory`**: สกิลการวางผังบัญชี 5 หมวด การจดบันทึกทางการเงิน และการบริหารจัดการคลังสินค้าสำหรับธุรกิจ SME ในประเทศไทย
- **`catalyst-map`**: Build a ranked map of the catalysts that could move a watchlist, theme, or portfolio by showing what matters, when it matters, and how those events could transmit across related names or exposures.
- **`CFO / Chief Financial Officer`**: Be the CFO with financial planning, cash management, fundraising, capital allocation, and strategic financial leadership.
- **`chicken-business-scale-up`**: Scale a fresh chicken shop from local market to regional or national level.
- **`comps-analysis`**: Build comparable company analysis in Excel — operating metrics, valuation multiples, statistical benchmarking vs peer sets. Pairs with excel-author. Use for public-company valuation, IPO pricing, sector benchmarking, or outlier detection.
- **`cost-accounting-inventory`**: การคำนวณบัญชีต้นทุนและการบริหารจัดการสินค้าคงคลัง (FIFO, Weighted Average, EOQ, Reorder Point, Safety Stock) พร้อม Python Implementation
- **`crassula-investment-persona`**: น้องใบเงิน (Crassula) investment advisor persona — Risk-First framework, response structure, tone, and decision hierarchy for all investment analysis tasks. Load when acting as Crassula or when user asks for investment analysis, risk assessment, or portfolio advice.
- **`crypto-com-app`**: Execute crypto trades (buy, sell, swap, exchange), manage cash deposits and withdrawals, and query account balances, market prices, and transaction history via the Crypto.com APP API. View weekly trading limits, portfolio positions, bank accounts, and payment networks. Use when the user wants to trade cryptocurrency, deposit or withdraw cash, check bank account details, view deposit instructions, or manage fiat wallet operations. Supports BTC, ETH, CRO, and 200+ tokens across fiat and crypto wallets.
- **`crypto-market-rank`**: |
- **`crypto-protocol-diagram`**: Extracts protocol message flow from source code, RFCs, academic papers, pseudocode, informal prose, ProVerif (.pv), or Tamarin (.spthy) models and generates Mermaid sequenceDiagrams with cryptographic annotations. Use when diagramming a crypto protocol, visualizing a handshake or key exchange flow, extracting message flow from a spec or RFC, diagramming a ProVerif or Tamarin model, or drawing sequence diagrams for TLS, Noise, Signal, X3DH, Double Ratchet, FROST, DH, or ECDH protocols.
- **`crypto-report`**: Analyze cryptocurrency projects with tokenomics, on-chain metrics, and market analysis. Generate comprehensive crypto research reports.
- **`day-trading-investor-pro`**: Professional AI Trading Mentor. Master price action, technical analysis, and risk management logic. Companion logic model for the Day Trading Investor Course.
- **`dcf-model`**: Build institutional-quality DCF valuation models in Excel — revenue projections, FCF build, WACC, terminal value, Bear/Base/Bull scenarios, 5x5 sensitivity tables. Pairs with excel-author. Use for intrinsic-value equity analysis.
- **`diy-accounting-setup`**: คู่มือและขั้นตอนการวางระบบบัญชี เอกสารควบคุมภายใน และปฏิทินภาษีด้วยตนเองสำหรับธุรกิจ SME และสตาร์ทอัพในประเทศไทย
- **`dw-money-management-strategy`**: กลยุทธ์การบริหารเงิน (Money Management) และการบริหารความเสี่ยงสำหรับ DW
- **`dw-trading-thailand-strategy`**: คู่มือเทคนิคและการเลือกซื้อ DW (Derivative Warrants) ในประเทศไทย
- **`ea-analysis-to-python-workflow`**: Reverse-engineer commercial MT5 EAs into Python quantitative strategies.
- **`ea-capital-protection-features`**: ฟีเจอร์การปกป้องเงินทุน (Capital Protection) ขั้นสูงสำหรับ EA และบอทเทรด
- **`ea-dashboard-architecture`**: สถาปัตยกรรมและพารามิเตอร์สำหรับสร้าง Dashboard และระบบตั้งค่า EA (Python/MT5)
- **`ea-news-filter-architecture`**: แนวทางและสถาปัตยกรรมในการสร้างระบบ News Filter สำหรับ EA และ Python Bot
- **`eamt5-python-architecture`**: แนวทางและโครงสร้างการสร้าง EA บน MT5 เชื่อมต่อกับ Python สำหรับระบบเทรดอัตโนมัติ
- **`earnings-preview`**: Prepare for an upcoming earnings report or earnings week by identifying the reports that matter, framing the key debates, and surfacing the read-through risk that could affect the user's watchlist or positions.
- **`earnings-trade-prep`**: Orchestrate a disciplined earnings-event workflow by deciding which names deserve prep, mapping the key debates and read-through paths, pressure-testing the thesis and structure, and ending with a clear pre-earnings hold, avoid, or trade decision.
- **`etoro`**: Use when the user wants an agent to interact with the eToro API for market data, portfolio and social features, or trade execution.
- **`evidence-gap-check`**: Identify the most important missing facts, assumptions, and unresolved questions that should be answered before a trade or investment idea is trusted, sized, or acted on.
- **`excel-author`**: Build auditable Excel workbooks headless with openpyxl — blue/black/green cell conventions, formulas over hardcodes, named ranges, balance checks, sensitivity tables. Use for financial models, audit outputs, reconciliations.
- **`execution-plan-check`**: Review whether a trade plan is operationally executable by checking order type logic, liquidity and spread risk, event timing, stop realism, and whether the user can actually implement the plan cleanly.
- **`factor-investing`**: Apply factor models to portfolio construction and fund evaluation, from CAPM through the Fama-French 3- and 5-factor models plus momentum. Use when the user asks about 'Fama-French', 'value factor', 'smart beta', 'factor tilt', 'momentum exposure', or the 'factor zoo', wants to run or interpret a factor regression (loadings, alpha after controlling for factors, R-squared, t-stats), decompose a manager's returns into factor exposures versus skill, or asks 'is my fund closet indexing'. Also trigger on SMB, HML, RMW, CMA, UMD, size/value/quality/profitability/low-vol premia, factor ETF or smart-beta product evaluation (factor purity, turnover, capacity, fees), factor cyclicality and the danger of factor timing, factor crowding, long-short academic factors versus long-only implementable tilts, and post-publication factor decay.
- **`farmed-hedge-yield-strategy`**: กลยุทธ์การเทรดแบบ Systematic Hedging และ Yield Farming จาก Farmed Hedge Yield Copy I พร้อมการปรับใช้ด้วย Python/MT5
- **`finance-os-tracker`**: Process daily financial transactions and route them to FinanceOS double-entry system via MCP tools.
- **`financial-analyst`**: >
- **`forex-exness-backtesting`**: การทดสอบสภาพแวดล้อมเสมือนจริงของ Exness (Free Swap) บน Python
- **`forex-fundamental-analysis`**: Framework for analyzing macroeconomic fundamentals to select Forex currency pairs.
- **`forex-mean-reversion-indicators`**: คู่มือการเลือกใช้อินดิเคเตอร์สำหรับระบบเทรด Mean Reversion และ Scalping
- **`forex-profitability-framework`**: กรอบความคิดและหลักการเชิงปริมาณ (Quant) เพื่อทำกำไรอย่างยั่งยืนในตลาด Forex
- **`forex-trading-concepts`**: คู่มือพื้นฐานตลาด Forex: คู่เงินหลัก (Majors), คู่เงินรอง (Minors), สเปรด (Spread), ค่าคอมมิชชั่น และค่าสวอป (Swap) พร้อมแนวทางการประยุกต์ใช้กับ Algorithmic Trading
- **`fresh-chicken-business-th`**: คู่มือขั้นตอนปฏิบัติการตั้งธุรกิจและควบคุมคุณภาพการค้าไก่สดในประเทศไทย อัปเดตระเบียบปศุสัตว์และกฎหมายท้องถิ่นปี 2569
- **`high-frequency-sweetspot-reversion`**: สูตรลับการปรับจูน Indicator เพื่อหา Sweet Spot (Win Rate ~70% + เทรดถี่) สำหรับ Daily Cashflow
- **`high-win-rate-mean-reversion`**: สูตรลับการปรับจูน Indicator (Optimization) ให้ได้ Win Rate 100% สำหรับ Mean Reversion
- **`innovestx-api`**: InnovestX Digital Asset Open API integration guide and Python client implementation.
- **`intelligent-investor-graham`**: Use Graham value investing for Is this investment or speculation, defensive
- **`investment-memo`**: Write professional investment memorandums for VC, PE, or public market investments. Structure thesis, risks, and recommendations clearly.
- **`journal-pattern-analyzer`**: Use when the user has a trade journal or trade log and wants repeated strengths, mistakes, environment-dependent patterns, and process changes without turning the review into hindsight theater.
- **`lbo-model`**: Build leveraged buyout models in Excel — sources & uses, debt schedule, cash sweep, exit multiple, IRR/MOIC sensitivity. Pairs with excel-author. Use for PE screening, sponsor-case valuation, or illustrative LBO in a pitch.
- **`lightgbm-mt5-onnx-pipeline`**: Architecture for LightGBM-based MT5 algorithmic trading bots using Walk-Forward testing and ONNX deployment.
- **`macro-event-analysis`**: Prepare for upcoming macro catalysts by identifying the events that matter, mapping the likely transmission channels, and surfacing timing risk for the user's markets or positions.
- **`market-regime-analysis`**: Analyze current market context through trend, volatility, breadth, and event backdrop so the user can choose tactics that fit the environment without relying on black-box regime claims.
- **`market-regime-detection-quant`**: สถาปัตยกรรมและเทคนิคการสร้าง Market Regime Detection สำหรับระบบ AI Trading เพื่อแก้ปัญหาโมเดลขาดทุนเมื่อสภาวะตลาดเปลี่ยน
- **`merger-model`**: Build accretion/dilution (merger) models in Excel — pro-forma P&L, synergies, financing mix, EPS impact. Pairs with excel-author. Use for M&A pitches, board materials, or deal evaluation.
- **`metatrader5-docker-python`**: Run MT5 in Docker and trade via Python on Linux.
- **`mlflow-quant-tracking-guide`**: คู่มือการออกแบบ MLflow Tracking, Naming Convention และ Artifacts สำหรับ AI Quant Trading ระดับสถาบัน
- **`modern-ea-features-2026`**: รวมฟีเจอร์และสถาปัตยกรรมของ EA ยุคใหม่ (2026-2027) สำหรับสอบกองทุน Prop Firm และใช้งานจริง
- **`most-important-thing-in-investing-howard-marks`**: Apply Howard Marks investing judgment for second-level thinking, price
- **`mql5-acd-cs-architecture`**: โครงสร้างและอัลกอริทึมของ EA แบบ Adaptive Context-Driven (ACD-CS) บน MT5
- **`mql5-commercial-ea-collection`**: รวมเทคนิค สถาปัตยกรรม และอินดิเคเตอร์ของ 5 EA ยอดฮิตในตลาด MQL5 ปี 2026
- **`mql5-market-research-workflow`**: Reverse-engineer commercial EAs from MQL5 Market to build custom trading bots.
- **`mql5-modular-components`**: โมดูล MQL5 แบบแยกส่วน (Risk, News Filter, Grid) สำหรับประกอบร่าง EA ในอนาคต
- **`mql5-onnx-architecture-th`**: คู่มือและโครงสร้างสถาปัตยกรรม การนำโมเดล AI (ML/DL) มาใช้งานบน MetaTrader 5 ผ่าน ONNX สำหรับสาย AI/Big Data
- **`mql5-onnx-gui-integration`**: คู่มือและโครงสร้างโค้ดสำหรับสร้าง MQL5 EA ที่มีการเชื่อมต่อโมเดล ONNX (Machine Learning) และการสร้าง GUI Dashboard บนกราฟ (Chart)
- **`mql5-onnx-integration`**: MQL5 ONNX Integration: Load, configure, and execute machine learning ONNX models natively in MetaTrader 5.
- **`mql5-onnx-production-architecture`**: สถาปัตยกรรมการออกแบบ MQL5 (MT5 EA) ระดับ Production สำหรับรัน ONNX Model (แยก Inference ออกจาก Training)
- **`mql5-scalping-ea-framework`**: Framework and MQL5 template for building a robust XAUUSD Scalping EA.
- **`mql5-scalping-grid-bot`**: โค้ด EA ต้นแบบ (MQL5) สำหรับการทำ Scalping และ Selective Grid เทียบเท่า EA เชิงพาณิชย์
- **`mql5-standalone-execution-architecture`**: สถาปัตยกรรม MQL5 EA แบบ Standalone สำหรับรันโมเดล ONNX โดยไม่ง้อ Backend Python เซิร์ฟเวอร์
- **`mt5-farmed-hedge-yield-strategy`**: Analysis and reverse-engineering of the MQL5 'Farmed Hedge Yield II' market-neutral hedging strategy, adapted for survival-first principles.
- **`mt5-onnx-ai-trading-pipeline`**: Data Science pipeline and architecture for building AI Trading Systems for MT5 via ONNX.
- **`mt5-python-trading`**: Guide and best practices for automated trading using Python and MetaTrader 5 (MT5), including Linux workarounds.
- **`multidim-quant-dw-pipeline`**: Execute multi-dimensional quant screening and DW trading.
- **`personal-finance-and-investment`**: Guide for personal finance management, asset allocation, and algorithmic trading portfolio risk control.
- **`pm-quant-system-roadmap`**: แผนการพัฒนาสถาปัตยกรรมระบบ Quant Trading ในมุมมอง PM + Quant Architect โดยเน้น Real PnL Impact (Execution, Risk, Portfolio) มากกว่าความซับซ้อนของโมเดล
- **`portfolio-concentration`**: Evaluate whether a portfolio, account, or planned position is too dependent on a small number of issuers, sectors, themes, or correlated exposures before the user adds or holds more risk.
- **`portfolio-risk-review`**: Orchestrate a whole-book risk review by checking concentration, correlated exposure, catalyst clustering, market-context sensitivity, and live-position fragility before the user adds, holds, or reduces portfolio risk.
- **`position-management`**: Review an open position and decide whether to hold, trim, tighten risk, close, or wait by comparing current behavior against the original thesis, invalidation logic, catalyst calendar, and execution constraints.
- **`position-sizing`**: Use when the user needs a conservative position size from account equity, risk budget, entry, stop, and trading friction before entering a trade.
- **`post-trade-debrief`**: Orchestrate a disciplined post-trade workflow by reconstructing the original plan, reviewing execution and rule adherence, and deciding whether the lesson is trade-specific or part of a larger repeatable pattern.
- **`post-trade-review`**: Guide a disciplined post-trade review across thesis quality, setup quality, execution, adherence, mistakes, and lessons without turning the result into hindsight theater.
- **`pptx-author`**: Build PowerPoint decks headless with python-pptx. Pairs with excel-author for model-backed decks where every number traces to a workbook cell. Use for pitch decks, IC memos, earnings notes.
- **`pre-trade-check`**: Orchestrate a disciplined pre-trade workflow by routing a watchlist or trade idea through the minimum set of underlying skills needed to decide whether the trade is ready, not ready, or should be resized or reworked first.
- **`prefect-quant-orchestration`**: สถาปัตยกรรม MLOps สำหรับ Quant Trading โดยใช้ Prefect เป็น Orchestrator ผสาน Data Sources, MLflow, ONNX และ MT5 เข้าด้วยกัน
- **`prefect-quant-pipeline-implementation`**: คู่มือการเขียนโค้ดและขึ้นระบบ Prefect Orchestration สำหรับ Quant Trading (ต่อยอดกับ MLflow, PostgreSQL, Optuna, ONNX)
- **`python-advanced-quant-trading`**: Advanced Python libraries for Candlestick pattern recognition, Price Action (Support/Resistance), Statistical indicators, and Strategy Performance metrics.
- **`python-mean-reversion-backtesting`**: แนวทางและแหล่งอ้างอิงสำหรับการทำ Backtest กลยุทธ์ Mean Reversion บน Python
- **`python-multi-asset-quant-trading`**: Frameworks, libraries, and mathematical constraints for quantitative trading across all major asset classes (Crypto, Forex, Equities, Options/Futures).
- **`python-pair-trading-mt5`**: สถาปัตยกรรมและสมการสร้างบอท Pair Trading (Statistical Arbitrage) บน MT5 ด้วย Python
- **`python-quant-feature-pipeline`**: โค้ด Python สำหรับสร้าง Feature Pipeline (pandas-ta) และระบบ Feature Selection 4 ชั้น (Correlation, sklearn, LightGBM, SHAP) สำหรับ Quant Trading
- **`python-quant-library-installation-guide`**: คู่มือการติดตั้ง 15 Library Stack แบบแบ่ง 3 Phases (Research, Training, Production) และ Workflow สำหรับระบบ AI Trading
- **`python-quant-mlops-stack`**: สถาปัตยกรรม Python Library Stack สำหรับ AI Trading & Quant Platform เต็มรูปแบบ ตั้งแต่ Data Collection ถึง Auto Retraining
- **`python-technical-indicators`**: Comprehensive guide to implementing technical indicators in Python using pandas-ta and TA-Lib for algorithmic trading.
- **`quant-advanced-model-optimization`**: เทคนิคขั้นสูง (Meta-Labeling, VolTarget, FracDiff) เพื่อแก้ปัญหาโมเดลขาดทุนในทองคำ บิทคอยน์ และกราฟ 15m
- **`quant-concept-drift-position-sizing`**: เจาะลึกความสัมพันธ์ระดับสถาบัน: Market Regime, Concept Drift, Position Sizing, Risk Engine และ Walk Forward Validation (Top 5 Quant Platform)
- **`quant-data-cleaning-and-scaling`**: เทคนิคการจัดการ Missing Value แบบ Quant Professional และการใช้ RobustScaler + JSON Library ใน MQL5
- **`quant-database-architecture`**: สถาปัตยกรรมฐานข้อมูลสำหรับ Quant Trading (PostgreSQL Schema) รองรับ Multi-Asset, Feature Store, และ MLOps
- **`quant-exness-cost-framework`**: Framework for calculating and storing All-In Transaction Costs (Spread, Commission, Swap, Slippage) for Exness in Quant Trading Backtests and Risk Engines.
- **`quant-feature-design-document`**: คู่มือ Feature Design Document สำหรับวางโครงสร้าง Feature Engineering 11 Stages เพื่อสร้าง AI Trading ด้วย LightGBM/ONNX
- **`quant-feature-engineering`**: สถาปัตยกรรมการสร้าง Feature Engineering เชิงลึกสำหรับ AI Trading / Quant (แปลง Raw Data เป็น Feature Intelligence)
- **`quant-lightgbm-mql5-preprocessing`**: Data preprocessing, scaling (RobustScaler), and missing value handling for LightGBM -> ONNX -> MQL5 pipelines.
- **`quant-lightgbm-onnx-mql5`**: Enterprise standards for exporting LightGBM models to ONNX and deploying to MQL5, covering scalers, feature metadata, and production bundles.
- **`quant-live-dynamic-configuration`**: Architecture for dynamically loading Python-generated JSON configs (Thresholds, Features) directly into MQL5 EAs.
- **`quant-live-execution-optimization`**: กลยุทธ์เพิ่มกำไรใน Live Trading (Non-Model Alpha) ผ่าน Execution, Trade Management, Cost และ Infrastructure
- **`quant-mql5-json-config`**: JSON library selection (JAson.mqh), scaler.json structure with metadata, and Data Scaling decision matrix for LightGBM -> ONNX -> MQL5 pipelines.
- **`quant-platform-failure-prevention`**: Quant PM checklist for preventing AI trading system failures (Python to MQL5 via ONNX).
- **`quant-platform-master-plan`**: แผนแม่บท (Master Project Plan) 16 Phases ในการสร้าง AI Quant Trading Platform ระดับ MLOps
- **`quant-platform-pm-pitfalls`**: รวม 15 ข้อควรระวัง (Pitfalls) ที่ PM และ Quant Architect มักพลาดเมื่อสร้างระบบ AI Trading ระดับ Production
- **`quant-platform-prioritization-and-arbitrage`**: คู่มือจัดลำดับความสำคัญการพัฒนา Quant Platform และการวิเคราะห์ขีดความสามารถเรื่อง Arbitrage / Real-Time
- **`quant-platform-vs-commercial-ea`**: เปรียบเทียบความสามารถ Quant Platform กับ Commercial EA และ The Missing 25% สู่ระดับสถาบัน
- **`quant-position-sizing-risk-engine`**: มาตรฐานการออกแบบ Position Sizing (5 ระดับ) และ Risk Engine (6 Layers) สำหรับ AI/Quant Trading รวมถึงหลักการ Walk Forward Validation
- **`quant-project-management-plan`**: แผนการบริหารโครงการ (Project Management Plan) และ WBS สำหรับการสร้าง AI Trading Platform ระดับ MLOps
- **`quant-risk-sizing-drift-engine`**: ระบบ Position Sizing, Risk Engine และ Data Drift Monitoring ซึ่งเป็นหัวใจสำคัญของการทำกำไรใน Quant Trading
- **`quant-trading-standard-framework`**: มาตรฐานการดำเนินงานเชิง Quant สำหรับสินทรัพย์ทุกประเภท ครอบคลุม 17 Phases ตั้งแต่ Data ถึง MLOps Auto-Retraining
- **`quant-walk-forward-validation`**: คู่มือทำ Walk Forward Validation แบบ Rolling Window และการวิเคราะห์ความเสถียร (Stability) เชิง Quant
- **`quantum-omnigold-architecture`**: สถาปัตยกรรมและกลยุทธ์การเทรดทองคำ (XAUUSD) เลียนแบบ Quantum OmniGold EA
- **`research-backed-investing`**: Use when designing asset allocation frameworks, developing algorithmic trading strategies, or selecting investment vehicles across Stocks, Mutual Funds, Forex, and Crypto using academic research-backed methodologies.
- **`research-finance`**: >
- **`risk-management`**: Portfolio-level risk controls, drawdown management, exposure limits, and circuit breakers for crypto trading
- **`risk-management-specialist`**: Medical device risk management specialist implementing ISO 14971 throughout product lifecycle. Provides risk analysis, risk evaluation, risk control, and post-production information analysis. Use when user mentions risk management, ISO 14971, risk analysis, FMEA, fault tree analysis, hazard identification, risk control, risk matrix, benefit-risk analysis, residual risk, risk acceptability, or post-market risk.
- **`risk-reward-sanity-check`**: Use when the user wants to test whether a proposed entry, stop, and target structure is coherent, asymmetric enough, and vulnerable to obvious failure modes before the trade is placed.
- **`settrade-adaptive-survival-bot`**: Deploy an adaptive algorithmic trading bot for Thai stocks.
- **`settrade-api-sandbox-connection`**: Establish and verify connection to the Settrade Sandbox API.
- **`settrade-dw-algo-trading`**: คู่มือและขั้นตอนการสร้างระบบ Algorithmic Trading สำหรับเทรด DW (Derivative Warrants) ในตลาดหุ้นไทยผ่าน Settrade Open API (settrade-v2) ด้วย Python พร้อมวิเคราะห์พารามิเตอร์แบบเจาะลึก
- **`settrade-dw-daily-income-bot`**: Deploy an automated DW trading bot using Settrade Open API.
- **`settrade-dw-quant-execution`**: Execute DW trading strategies via Settrade Open API.
- **`settrade-marketrep-derivatives-python`**: Guide and comprehensive API reference for Settrade Open API (MarketRep Derivatives SDK v2 for Python).
- **`settrade-multi-stock-scanner`**: Deploy a multi-stock Settrade scanner via Hermes cronjob.
- **`settrade-order-debugging`**: Debug Settrade API order rejections and OSS errors.
- **`settrade-sandbox-diagnostic`**: Diagnose and validate Settrade Open API Sandbox credentials.
- **`stock-selection-indicators`**: Framework and key indicators for systematic stock selection (Fundamental & Technical) for SET/Crypto and algorithmic trading.
- **`stocks`**: Stock quotes, history, search, compare, crypto via Yahoo.
- **`thai-business-law-guide`**: คู่มือและกฎหมายสำคัญในการประกอบธุรกิจในประเทศไทย ครอบคลุมการจัดตั้งธุรกิจ ภาษี แรงงาน PDPA ทรัพย์สินทางปัญญา และกฎหมายคุ้มครองผู้บริโภค
- **`thai-business-license-guide`**: คู่มือเงื่อนไขการขอรับใบอนุญาตและระเบียบการดำเนินงานของธุรกิจเฉพาะประเภทในประเทศไทย เช่น อาหาร/เครื่องสำอาง (อย.), โรงแรม, ขายสินค้าออนไลน์ (ตลาดแบบตรง สคบ.), ทัวร์นำเที่ยว และร้านนวดสปา
- **`thai-business-registration`**: คู่มือขั้นตอนการจัดตั้งห้างหุ้นส่วนและบริษัทจำกัดในประเทศไทยผ่านระบบ DBD Biz Regist (อัปเดตล่าสุด 2569)
- **`thai-business-setup-guide`**: คู่มือขั้นตอนปฏิบัติในการจัดตั้งบริษัทจำกัดและเริ่มต้นธุรกิจในประเทศไทย ผ่านระบบ DBD Biz Regist ดิจิทัล 100% อัปเดตปี 2569
- **`thai-corporate-and-partnership-law`**: คู่มือกฎหมายห้างหุ้นส่วนจำกัด (หจก.) และบริษัทจำกัด (บจก.) ในประเทศไทย ตามประมวลกฎหมายแพ่งและพาณิชย์ (ป.พ.พ.) และกฎหมายภาษี บัญชี อัปเดตล่าสุด
- **`thai-corporate-structure-and-positions`**: Use when designing corporate organizational structures, defining department roles, job positions, and determining salary brackets for companies in Thailand based on local regulations and market benchmarks (Adecco 2026 / Jobsdb).
- **`thai-digital-accounting`**: ทักษะและความรู้ด้านการบัญชีดิจิทัล ระบบภาษีอิเล็กทรอนิกส์ (e-Tax & e-Withholding Tax) และการวิเคราะห์ข้อมูลสำหรับธุรกิจในประเทศไทย
- **`thai-dw-price-table`**: คู่มือและวิธีการดึงข้อมูลตารางราคา DW (Derivative Warrants) ของแต่ละบริษัทผู้ออกหลักทรัพย์ในตลาดหุ้นไทย
- **`thai-dw-trading-strategy`**: คู่มือกลยุทธ์, การคำนวณ, และข้อควรระวังในการเทรด DW (Derivative Warrants) ในตลาดหุ้นไทย
- **`thai-financial-operating-rules`**: กฎการเงินส่วนตัวสำหรับผู้อาศัยในไทย — ภาษี, ธนาคาร, การลงทุน, ป้องกันความเสี่ยง
- **`thai-personal-accounting-and-finance`**: คู่มือและเครื่องมือการทำบัญชีส่วนบุคคล งบการเงิน และการวิเคราะห์อัตราส่วนสุขภาพทางการเงินตามมาตรฐานตลาดหลักทรัพย์แห่งประเทศไทย (SET Happy Money) ร่วมกับการวางแผนภาษีและการลดหย่อนภาษี
- **`thai-stock-seasonal-strategy`**: คู่มือและกลยุทธ์การเลือกหุ้นไทยด้วยปัจจัยพื้นฐาน ผสมผสานกับการเก็งกำไรตามฤดูกาล (Seasonal Effect) ในแต่ละไตรมาส
- **`thai-tax-planning-strategy`**: Guide and strategies for legal tax planning and tax optimization (Tax Avoidance) in Thailand for individuals and businesses.
- **`thai-trading-business`**: คู่มือและขั้นตอนปฏิบัติการทำธุรกิจซื้อมาขายไป (Trading Business) ในประเทศไทย ครอบคลุมการตั้งค่าระบบบัญชี คลังสินค้า ภาษีบุคคล/นิติบุคคล และข้อกฎหมายที่เกี่ยวข้อง
- **`thesis-validation`**: Pressure-test a trade or investment thesis by clarifying the core claim, evidence, invalidation, timeframe, and dependency chain before the user turns it into an entry, stop, or size.
- **`top5-dw-issuers-thailand`**: รายชื่อผู้ออก DW (Derivative Warrants) ในประเทศไทยที่มี Market Share ยอดนิยม 5 อันดับแรก
- **`topdown-stock-analysis`**: กรอบการวิเคราะห์หุ้นแบบ Top-Down Approach (Global -> Thai -> Stock)
- **`watchlist-review`**: Review a watchlist and rank which names deserve active attention, background monitoring, or removal based on catalysts, tradability, redundancy, and evidence quality for the user's style and timeframe.

### 📁 GAMING (2)

- **`minecraft-modpack-server`**: Host modded Minecraft servers (CurseForge, Modrinth).
- **`pokemon-player`**: Play Pokemon via headless emulator + RAM reads.

### 📁 GITHUB (1)

- **`github-repo-management`**: Clone/create/fork repos; manage remotes, releases.

### 📁 HERMES-AGENT (5)

- **`cross-linked-skill-authoring`**: Build modular, cross-linked Hermes skills from raw domain input.
- **`ecosystem-knowledge-orchestration`**: Convert continuous domain inputs into cross-linked modules.
- **`hermes-gateway-multiplexer-fix`**: Fixes Hermes Gateway conflicts when multiplexing profiles.
- **`iterative-domain-mapping`**: Structure continuous domain expertise into linked skills.
- **`multi-profile-skills-sync`**: Sync and link agent skills across all profiles and GitHub.

### 📁 MARKETING (28)

- **`30x-growth-marketing-panel`**: AI Growth Marketing Expert Panel with 11 world-class experts distilled from 4,000+ YouTube videos for Claude Code
- **`ai-business-thai-platforms`**: Use when designing, building, or implementing AI strategies for Thai businesses across LINE, Facebook, YouTube, and Instagram.
- **`ai-fluency-framework`**: >
- **`ai-fluency-social-seo`**: AI fluency และ Social SEO สำหรับการทำการตลาด 2026 - ใช้ AI เพื่อสร้างเนื้อหา เพิ่มการมีส่วนไข้เข้าชมโดยรวม 10 ขั้นตอน
- **`ai-proposal-generator`**: Generate professional HTML proposals from meeting notes. Features 5 proposal styles (Corporate, Entrepreneur, Creative, Consultant, Minimal), 6+ color themes, and a Design Wizard for custom templates. Triggers on "create proposal", "proposal for [client]", "proposal wizard", "proposal from [notes]", "show proposal styles", "finalize proposal". Integrates with ai-meeting-notes for context. Outputs beautiful, responsive HTML ready to send or export as PDF.
- **`content-creation-github-stack`**: Curated open-source stack for multi-channel content creation.
- **`content-marketing-2026-2027`**: >
- **`content-quality-and-token-telemetry`**: Audit content quality and log token telemetry in DB.
- **`design-trends-2026`**: Apply 2026's top graphic design trends to any creative brief. Based on Kittl × Savee's 2026 Design Trends Report (10 trends + 2 honorable mentions), backed by Adobe, Figma, and Pinterest data. Use when: **Designing a brand identity** — pick the right aesthetic for your audience; **Creating social media assets** — use trending visual languages that perform; **Briefing a designer or AI image tool** — give precise style direction with vocabulary and references; **Refreshing a visual identity** — know what's rising vs saturating; **Building mood boards** — combine trends intentionally with data-backed rationale.
- **`digital-product-monetization`**: กรอบการทำงาน 5 ขั้นตอนในการสร้างและขาย Digital Product ให้ได้เงินหลักแสน (ถอดรหัสจากคลิปแนวคิด Alex Hormozi)
- **`facebook-automation-suite`**: คู่มือและการสร้างสคริปต์สำหรับจัดการ Facebook Fanpage (โพสต์ออโต้, ดูดข้อมูล, ดึงคอมเมนต์) ผ่าน Python
- **`facebook-monetized-content-engine`**: Produce SEO-optimized monetized social media content.
- **`faceless-video-reverse-engineering`**: Replicate viral faceless videos into animated compositions.
- **`fb-reels-monetization-playbook`**: ระบบสแครปและวิเคราะห์ Facebook Reels คู่แข่งด้วย Python เพื่อสกัดเป็นเทมเพลตสคริปต์ทำเงินสำหรับ Affiliate สินค้า
- **`prefect-social-media-factory`**: Orchestrate scheduled social media content workflows.
- **`shopee-affiliate-data-pipeline`**: Fetch and score Shopee affiliate products using pricing and seasonal matrices.
- **`social-seo-checklist`**: >
- **`stop-scroll-video-framework`**: สถาปัตยกรรมและเทคนิคการผลิตวิดีโอสั้นหยุดนิ้ว (Stop-Scroll High-Retention Reels) สไตล์แมนหยุดนิ้ว สำหรับ Facebook Reels / TikTok ด้วยเทคนิค Contrast Hook, Kinetic Subtitle และ Jump Cut
- **`telegram-chat-ui-ux`**: Design rich interactive UI/UX in Telegram chat interfaces.
- **`thai-branding-strategy`**: Use when creating, positioning, or executing personal and business branding strategies for individuals and businesses in Thailand, detailing steps, tools, and local ecosystem integration.
- **`thai-business-marketing-guide`**: Marketing & business strategy guide for all Thai business types.
- **`thai-content-compliance`**: Use when creating content for Thai audiences, checking for forbidden words, compliance with FDA (อย.) / CPB (สคบ.), and platform rules (TikTok, Shopee, Lazada, Facebook, YouTube).
- **`thai-psychology-engagement-2026`**: Mastering Thai human psychology for content, marketing, and communication in 2026-2027. Focuses on emotional triggers, empathy, and cultural consciousness.
- **`thailand-content-strategy-2026`**: Use when planning, creating, or adapting content marketing strategies for the Thai market in 2026 across B2C, B2B, Real Estate, and Finance sectors.
- **`thailand-market-demand-2026-2027`**: Use to analyze macroeconomic trends, consumer demand, and sector-specific performance in Thailand for 2026-2027 based on Kasikorn Research and SCB EIC data.
- **`thailand-social-media-landscape`**: Insights, statistics, user behaviors, and platform-specific strategies for Social Media marketing in Thailand (Based on 2024-2025 trends).
- **`tiktok-automation-suite`**: คู่มือและการสร้างสคริปต์สำหรับจัดการ TikTok (โพสต์ออโต้, ดึงข้อมูล) ผ่าน Python
- **`zero-touch-monetization-playbook`**: คู่มือสถาปัตยกรรมและกระบวนการสร้างเครื่องจักรทำเงินอัตโนมัติ (Zero-Touch Monetization) บนเครื่อง VPS โดยใช้ Prefect, FFmpeg, CLIProxyAPI, และเทคนิค Faceless Video

### 📁 MCP (2)

- **`fastmcp`**: Build, test, inspect, install, and deploy MCP servers with FastMCP in Python. Use when creating a new MCP server, wrapping an API or database as MCP tools, exposing resources or prompts, or preparing a FastMCP server for Claude Code, Cursor, or HTTP deployment.
- **`native-mcp`**: MCP client: connect servers, register tools (stdio/HTTP).

### 📁 MEDIA (13)

- **`ai-animation-production-pipeline`**: Four-stage AI animation and video production pipeline.
- **`ai-avatar-generation-stack`**: Tools and APIs for creating consistent AI avatars and talking-head videos.
- **`broll-free-video-automation`**: Generate high-retention faceless videos without manual B-roll sourcing.
- **`f5-tts-pipeline-integration`**: Train and serve voice cloning models on Colab and VPS.
- **`ffmpeg-complex-filter-video-automation`**: Best practices for building fully automated video pipelines (templates, shorts, overlays) entirely in FFmpeg without MoviePy.
- **`ffmpeg-thai-drawtext-pipeline`**: Assemble vertical videos with typewriter effects and Thai text using pure FFmpeg.
- **`ffmpeg-video-automation`**: FFmpeg complex filter recipes for automated social media video generation (TikTok, Shorts)
- **`python-ai-video-monetization`**: 10 Python AI video libraries categorized for monetization.
- **`spotify`**: Spotify: play, search, queue, manage playlists and devices.
- **`thai-faceless-video-automation`**: Pipeline for rendering Thai-language vertical videos with accurate text overlays.
- **`video-vision-analysis`**: Framework for scoring and reviewing AI-generated videos before publishing.
- **`voice-humanizer`**: Process synthetic speech with audio DSP and music ducking.
- **`youtube-data-extraction`**: Fetch YouTube channel videos, metadata, and transcripts using yt-dlp and APIs.

### 📁 MISC (10)

- **`adhd-assistant`**: ADHD-friendly life management assistant for SkillBoss API Hub. Helps with daily planning, task breakdown, time management, prioritization, body doubling, dopamine regulation, and maintaining routines. Use when the user asks for help organizing their life, staying on top of tasks, beating procrastination, planning their day/week, managing overwhelm, or mentions ADHD-related challenges like time blindness, forgetfulness, difficulty starting tasks, or emotional dysregulation.
- **`AI Agent Wars 2026`**: 2026年全球AI Agent平台竞争格局深度分析——OpenAI Codex vs Kimi vs 扣子 vs Dify vs LangChain vs 百炼等六大平台全面对比，涵盖框架评测、企业采用率、安全治理、融资动态、开发者工具链与2027预测
- **`ask-matt`**: Ask which skill or flow fits your situation. A router over the skills in this repo.
- **`backup-global-cognitive-brain-20260316-100703`**: -
- **`badman-agent-rental`**: -
- **`boss-ai-agent`**: Boss AI Agent — AI management advisor and team operations middleware. Use this skill whenever the user needs management advice, leadership guidance, or team operations help. Triggers for: 1:1 meeting prep, daily briefings ('what's important today'), team performance reviews (advice and analysis, not templates), risk assessments, KPI health checks, check-in question design, conflict resolution, cross-cultural feedback ('how do I give feedback to my Filipino/Chinese/Indonesian employee'), mentor philosophy application ('what would Musk/Inamori/Ma say'), C-Suite board simulation, promotion/hiring decisions, employee engagement issues, weekly reports, and incentive reviews. Supports 16 mentor philosophies (Musk, Inamori, Ma, Dalio, Grove, Bezos, etc.), 9 culture packs, and learns boss preferences over time. Works offline as advisor or connected to manageaibrain.com MCP for full 33-tool automation (check-ins, tracking, messaging, sync). Use this even if the user doesn't say 'management' explicitly — any people leadership question, team dynamics issue, or boss-level decision qualifies. Do NOT trigger for software development tasks (building apps, APIs, bots, schemas) even if they relate to HR/employees — this skill is for management advice, not code implementation.
- **`grill-me`**: A relentless interview to sharpen a plan or design.
- **`grill-with-docs`**: A relentless interview to sharpen a plan or design, which also creates docs (ADR's and glossary) as we go.
- **`grilling`**: Grill the user relentlessly about a plan, decision, or idea. Use when the user wants to stress-test their thinking, or uses any 'grill' trigger phrases.
- **`research`**: Investigate a question against high-trust primary sources and capture the findings as a Markdown file in the repo. Use when the user wants a topic researched, docs or API facts gathered, or reading legwork delegated to a background agent.

### 📁 MLOPS (4)

- **`dspy`**: DSPy: declarative LM programs, auto-optimize prompts, RAG.
- **`mlflow-dataset-tracking`**: Guide and implementation patterns for measuring, tracking, and versioning datasets using MLflow (mlflow.data API).
- **`obliteratus`**: OBLITERATUS: abliterate LLM refusals (diff-in-means).
- **`pm-mlops-trading-framework`**: Project Management framework and strict governance rules for building an end-to-end MLOps AI Trading Platform (MT5 + ONNX).

### 📁 PRODUCTIVITY (17)

- **`brain-hacking-and-productivity`**: Neuroscience-based protocols for brain hacking, entering flow states, managing energy/dopamine, and optimizing cognitive execution.
- **`business-analysis-frameworks`**: Use when analyzing business strategy, evaluating strengths/weaknesses (SWOT/TOWS), defining growth paths (Ansoff/BCG), assessing competitive forces (Porter's Five Forces/VRIO), and aligning organizational capabilities (McKinsey 7S), localized for the Thai business ecosystem.
- **`deep-productivity`**: Master deep work productivity through the three types of work framework (Building, Maintenance, Recovery). Use when user needs to: (1) Build a sustainable deep work routine with just 1 hour/day, (2) Create vision/anti-vision for life direction, (3) Structure goals using the 10-year → 1-year → 1-month → 1-week hierarchy, (4) Apply project-based learning to bridge skill gaps, (5) Identify lever-moving tasks that actually progress goals, (6) Balance focus work with necessary recovery for creativity.
- **`google-workspace`**: Gmail, Calendar, Drive, Docs, Sheets via gws CLI or Python.
- **`google-workspace-oauth-setup`**: Process for enabling Hermes access to personal Google accounts.
- **`here.now`**: Publish static sites to {slug}.here.now and store private files in cloud Drives for agent-to-agent handoff.
- **`linear`**: Linear: manage issues, projects, teams via GraphQL + curl.
- **`obsidian-personal-templates`**: |
- **`obsidian-workflow`**: |
- **`online-income-and-monetization`**: Strategies for online monetization, content creation, digital products, and building a professional brand.
- **`personal-productivity`**: Build a Personal Productivity System Pack (weekly timebox plan, capture+to-do system, daily/weekly review rituals, and a 7-day rollout). Use for timeboxing, calendar blocking, and staying on top of high-volume leadership work. Category: Career.
- **`saas-productivity`**: Use when designing animations for business tools, project management, collaboration software, or productivity apps
- **`teach`**: Teach the user a new skill or concept, within this workspace.
- **`thai-business-excellence`**: Use when establishing, auditing, or improving business operations in Thailand using frameworks like TQA (Thailand Quality Award), PMQA, EdPEx, and SEPA.
- **`time-management-and-productivity`**: Guidelines for task prioritization, time blocking, and learning systems (Second Brain/Obsidian).
- **`user-communication-preferences`**: Embed a user's preferred communication style and action-oriented conventions for Hermes Agent sessions (tone, language, verbosity, action-first behavior).
- **`vision-net-registrar`**: Use when scraping or integrating academic data (schedules, grades, registration) from universities using Vision Net E-Registrar (e.g., RMUTT, TU, WU).

### 📁 PROJECT-MANAGEMENT (1)

- **`orchestrating-kanban-subagents`**: Creates a master plan, sets up Kanban tasks, and schedules subagent dispatch.

### 📁 RED-TEAMING (1)

- **`godmode`**: Jailbreak LLMs: Parseltongue, GODMODE, ULTRAPLINIAN.

### 📁 SOFTWARE-DEVELOPMENT (87)

- **`agent-skills-github-sync`**: Use when synchronizing Hermes Agent local skills with a remote GitHub repository. Guides the backup, management, and deployment of agent skills.
- **`ai-content-studio-architecture`**: Architecture and workflows for the Satang AI Studio multi-agent content generation platform.
- **`audio-tts-post-processing`**: Techniques for processing, chunking, and mastering AI-generated TTS audio using Python (Pedalboard, Soundfile).
- **`awesome-python-apis-and-tools`**: 100+ Free Python libraries and APIs for scalable automation, AI, and monetization.
- **`better-auth-nextjs`**: Configure modern authentication in Next.js using better-auth.
- **`brainstorming`**: You MUST use this before any creative work - creating features, building components, adding functionality, or modifying behavior. Explores user intent, requirements and design before implementation.
- **`business-dss-development`**: Use when designing, building, or evaluating Business Decision Support Systems (DSS). Guides the architecture of data management, model management (optimization/ML), user interface, and integration of AI agents for data-driven business decisions.
- **`chrome-extension-mv3-development`**: Official guidelines, architecture, and constraints for building Google Chrome Extensions using Manifest V3 (MV3).
- **`clerk-nextjs-patterns`**: Advanced Next.js patterns - middleware, Server Actions, caching with
- **`cli-proxy-api-management`**: Configure and query the CLIProxyAPI management endpoints.
- **`cliproxy-quota-check`**: Check CLIProxyAPI account quota and request success/failure counts.
- **`cliproxy-quota-inspector`**: Query and inspect CLIProxyAPI account statuses and request quotas.
- **`code-review`**: Review the changes since a fixed point (commit, branch, tag, or merge-base) along two axes: Standards (does the code follow this repo's documented coding standards?) and Spec (does the code match what the originating issue/spec asked for?). Runs both reviews in parallel sub-agents and reports them side by side. Use when the user wants to review a branch, a PR, work-in-progress changes, or asks to \"review since X\".
- **`codebase-design`**: Shared vocabulary for designing deep modules. Use when the user wants to design or improve a module's interface, find deepening opportunities, decide where a seam goes, make code more testable or AI-navigable, or when another skill needs the deep-module vocabulary.
- **`debugging-hermes-tui-commands`**: Debug Hermes TUI slash commands: Python, gateway, Ink UI.
- **`deep-agents-python`**: Guide and best practices for using LangChain's Deep Agents framework (langchain-ai/deepagents), an opinionated agent harness built on LangGraph for long-horizon tasks.
- **`diagnosing-bugs`**: Diagnosis loop for hard bugs and performance regressions. Use when the user says "diagnose"/"debug this", or reports something broken/throwing/failing/slow.
- **`diagnosing-superpowers`**: Use when a superpowers session went wrong and your human partner wants to know why — repeated work, ignored plans, stumbles, poor results, a skill that didn't fire, "it took too long", "why is it so expensive", "what is it doing" — or wants to build a bug report for the superpowers maintainers, for the current session or a past one identified by id or path, on any harness.
- **`domain-modeling`**: Build and sharpen a project's domain model. Use when discussing codebase terminology, writing or editing a CONTEXT.md, or recording or editing an ADR.
- **`executing-plans`**: Use when executing an implementation plan in the current session as the implementer yourself — your human partner chose inline execution, or no subagent tool is available
- **`fastapi`**: FastAPI best practices and conventions. Use when working with FastAPI APIs and Pydantic models for them. Keeps FastAPI code clean and up to date with the latest features and patterns, updated with new versions. Write new code or refactor and update old code.
- **`fastapi-unified-architecture`**: Patterns for deploying FastAPI, Gradio, and MCP servers in a single script, especially on Google Colab.
- **`finishing-a-development-branch`**: Use when implementation is complete, all tests pass, and you need to decide how to integrate the work
- **`free-api-python-monetization-stack`**: 100 free Python libraries and APIs for TTS, AI, scraping, finance, and automation.
- **`git-guardrails-claude-code`**: Set up Claude Code hooks to block dangerous git commands (push, reset --hard, clean, branch -D, etc.) before they execute. Use when user wants to prevent destructive git operations, add git safety hooks, or block git push/reset in Claude Code.
- **`grill-with-docs`**: A relentless interview to sharpen a plan or design, which also creates docs (ADR's and glossary) as we go.
- **`hermes-9router-integration`**: Deploy 9Router and integrate it with Hermes Agent profiles.
- **`hermes-agent-skill-authoring`**: Author in-repo SKILL.md: frontmatter, validator, structure.
- **`hermes-profile-isolation`**: Set up and configure isolated Hermes Agent profiles for different projects.
- **`hermes-s6-container-supervision`**: Modify, debug, or extend the s6-overlay supervision tree inside the Hermes Agent Docker image — adding new services, debugging profile gateways, understanding the Architecture B main-program pattern.
- **`implement`**: Implement a piece of work based on a spec or set of tickets.
- **`implement-spec`**: Implement a specification in code.
- **`improve-codebase-architecture`**: Scan a codebase for deepening opportunities, present them as a visual HTML report, then grill through whichever one you pick.
- **`langgraph-development`**: Best practices for building and tracing AI agents with LangGraph, Deep Agents, and MLflow.
- **`langgraph-fastapi-hitl`**: Architecture and implementation guide for building Human-in-the-Loop (HITL) workflows with LangGraph and FastAPI, including business patterns (HITL vs HOTL).
- **`liff-external-payment-integration`**: Integrate external payments in LINE LIFF apps.
- **`line-liff-development`**: Development guide and pitfalls for LINE Front-end Framework (LIFF) apps based on official documentation.
- **`line-mini-app-liff-serverless`**: Create LINE MINI Apps using LIFF based on the SupremeTech serverless approach. Use when planning, designing, or building a LINE MINI App with LIFF, especially for membership management or m-commerce without a dedicated backend server.
- **`loop-engineering-integration`**: Sets up and integrates Loop Engineering boundaries (loop-init, loop-constraints) with Subagent-Driven Development.
- **`loop-me`**: Grill me about specs for the workflows I want to build, within this workspace.
- **`migrate-to-shoehorn`**: Migrate test files from `as` type assertions to @total-typescript/shoehorn. Use when user mentions shoehorn, wants to replace `as` in tests, or needs partial test data.
- **`multi-profile-messaging-gateway`**: Configure and route multiple Hermes profiles within a single Discord/Telegram gateway (Multiplexer).
- **`next-dev-loop`**: >
- **`nextjs-16-migration`**: Comprehensive guide and checklist for upgrading to Next.js 16, covering Turbopack, Async Request APIs, and breaking changes.
- **`nextjs-liff-fastapi-backend`**: Build a Next.js LIFF app using Python FastAPI with LangChain
- **`nextjs-spa-static-export`**: Best practices for building Single-Page Applications (SPA) and static sites with Next.js using the Static Export feature.
- **`nextjs-ui-libraries`**: Top UI libraries and UX frameworks for Next.js (shadcn/ui, Tailwind, NextUI, Chakra) to speed up frontend development.
- **`plan`**: Plan mode: write markdown plan to .hermes/plans/, no exec.
- **`playwright-python`**: Playwright Python Best Practices and Techniques (Sync/Async, POM, Locators)
- **`pr`**: Use when writing a PR body.
- **`prototype`**: Build a throwaway prototype to answer a design question. Use when the user wants to sanity-check whether a state model or logic feels right, or explore what a UI should look like.
- **`react-2026`**: Provides a comprehensive guide to the modern React 2026 stack. Use when starting a new React project or modernizing an existing one with current frameworks, build tools, routing, state management, or AI integration.
- **`react-composition-2026`**: Teaches modern React composition patterns for 2025/2026. Use when designing component APIs, building shared UI libraries, or refactoring prop-heavy components.
- **`receiving-code-review`**: Use when receiving code review feedback, before implementing suggestions, especially if feedback seems unclear or technically questionable - requires technical rigor and verification, not performative agreement or blind implementation
- **`resolving-merge-conflicts`**: Use when you need to resolve an in-progress git merge/rebase conflict.
- **`retro`**: Conduct a retrospective on a coding session.
- **`satang-ai-gateway-dev`**: Development guide for the Satang AI Monorepo: FastAPI Gateway, Better-Auth integration, and Prefect orchestration.
- **`satang-project-suite`**: Develop and deploy Thanapol's custom AI and trading projects.
- **`satangthebank-development`**: Guidelines and architecture specifics for developing and maintaining the SatangTheBank Omnichannel Ledger system (Next.js, FastAPI, PostgreSQL, Better-Auth, LINE).
- **`scaffold-exercises`**: Create exercise directory structures with sections, problems, solutions, and explainers that pass linting. Use when user wants to scaffold exercises, create exercise stubs, or set up a new course section.
- **`server-side-video-processing`**: High-performance server-side video automation using pure FFmpeg complex filters (single-pass), avoiding MoviePy/ImageMagick overhead.
- **`setup-matt-pocock-skills`**: Configure this repo for the engineering skills: set up its issue tracker, triage label vocabulary, and domain doc layout. Run once before first use of the other engineering skills.
- **`setup-pre-commit`**: Set up Husky pre-commit hooks with lint-staged (Prettier), type checking, and tests in the current repo. Use when user wants to add pre-commit hooks, set up Husky, configure lint-staged, or add commit-time formatting/typechecking/testing.
- **`setup-ts-deep-modules`**: Wire dependency-cruiser into a TypeScript repo so each package is a deep module, with implementation hidden in subfolders and reachable only through its entry-point files. User-invoked.
- **`shadcn-ui`**: Provides complete shadcn/ui component library patterns including installation, configuration, and implementation of accessible React components. Use when setting up shadcn/ui, installing components, building forms with React Hook Form and Zod, customizing themes with Tailwind CSS, or implementing UI patterns like buttons, dialogs, dropdowns, tables, and complex form layouts.
- **`smart-context-usage`**: Guidelines for maintaining token efficiency and executing context compression in Hermes
- **`subagent-driven-development`**: Execute plans via delegate_task subagents (2-stage review).
- **`tdd`**: Test-driven development. Use when the user wants to build features or fix bugs test-first, mentions "red-green-refactor", or wants integration tests.
- **`to-questionnaire`**: Turn a decision you can't fully answer into a questionnaire for someone else to fill in.
- **`to-spec`**: Turn the current conversation into a spec and publish it to the project issue tracker: no interview, just synthesis of what you've already discussed.
- **`to-tickets`**: Break a plan, spec, or the current conversation into a set of tracer-bullet tickets, each declaring its blocking edges, published to the configured tracker (edges as text in one file per ticket locally, or native blocking links on a real tracker).
- **`triage`**: Move issues and external PRs through a state machine of triage roles, categorise, verify, grill if needed, and write agent-ready briefs.
- **`using-git-worktrees`**: Use when starting feature work that needs isolation from current workspace or before executing implementation plans - ensures an isolated workspace exists via native tools or git worktree fallback
- **`uv-package-management`**: Manage Python dependencies and virtual environments using uv.
- **`verification-before-completion`**: Use when about to claim work is complete, fixed, or passing, before committing or creating PRs - requires running verification commands and confirming output before making any success claims; evidence before assertions always
- **`video-editing-moviepy`**: Video editing automation using MoviePy in Python, specifically for vertical 9:16 social media formats (Reels, TikTok, Shorts).
- **`wait-what`**: Stop. That last message did not land: re-pitch it.
- **`Web Development`**: Build, debug, and deploy websites with HTML, CSS, JavaScript, modern frameworks, and production best practices.
- **`web-development`**: Use when users need to implement, integrate, debug, build, deploy, or validate a Web frontend after the product direction is already clear, especially for React, Vue, Vite, browser flows, or CloudBase Web integration.
- **`web-mobile-ux-guidelines`**: Essential UI/UX design principles and best practices for developing responsive web apps across desktop and mobile.
- **`wizard`**: Generate an interactive bash wizard that walks a human through steps only they can perform. Use when provisioning infrastructure, setting up credentials or CI secrets, walking an unfamiliar third-party dashboard, or running a one-off migration or cutover. Don't invoke this for steps the agent can perform itself.
- **`writing-beats`**: Writing, exploit; assemble raw material into a journey of beats, grounding each term before a beat leans on it.
- **`writing-for-agents`**: Writing documents for agents. Use when creating or editing skills, or modifying AGENTS.md or CLAUDE.md.
- **`writing-fragments`**: Writing, explore: mine raw fragments, no structure yet.
- **`writing-plans`**: Write implementation plans: bite-sized tasks, paths, code.
- **`writing-shape`**: Writing, exploit: shape raw material into an article, paragraph by paragraph.
- **`writing-skills`**: Use when creating new skills, editing existing skills, or verifying skills work before deployment

