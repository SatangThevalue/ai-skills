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

### โหลด Skill ขึ้นมาใช้
```bash
# ดูรายชื่อ Skill ทั้งหมด
hermes skills list

# โหลด Skill เพื่อดูเนื้อหา
hermes skills view <ชื่อ-skill>
```

### โครงสร้างไฟล์
```
skills/
├── devops/
│   ├── hermes-dashboard-traefik/SKILL.md
│   ├── docker-management/SKILL.md
│   └── ...
├── finance/
│   ├── dcf-model/SKILL.md
│   └── ...
├── software-development/
│   ├── cliproxy-quota-check/SKILL.md
│   └── ...
└── README.md  ← ไฟล์นี้
```

---

## 📚 สารบัญ Skills

> ⚠️ **หมายเหตุ:** อัปเดตอัตโนมัติทุกครั้งที่มีการเพิ่ม/แก้ไข Skill

---

### 🤖 Autonomous AI Agents

| Skill | คำอธิบาย |
|-------|----------|
| `agent-frameworks-integration` | ออกแบบ/สร้าง/จัดการ Multi-agent systems (Google ADK, A2A, MCP, n8n) |
| `codex` | Delegate งานเขียนโค้ดไปยัง OpenAI Codex CLI |
| `google-adk` | สร้าง Multi-agent ด้วย Google Agent Development Kit (ADK) |
| `hermes-agent` | ตั้งค่า ขยาย และพัฒนา Hermes Agent |
| `hermes-gateway-resilience` | กู้คืนและเสริมความแข็งแกร่ง Hermes Messaging Gateway บน Linux |
| `hermes-kanban-swarm` | จัดการ Multi-agent Swarm ผ่าน Hermes Kanban |
| `hermes-workspace-setup` | ติดตั้ง Hermes Workspace บน VPS พร้อม Gateway Auth |
| `kanban-codex-lane` | รัน Codex CLI ในฐานะ Implementation Lane ภายใต้ Hermes Kanban |
| `opencode` | Delegate งานโค้ดไปยัง OpenCode CLI |
| `research-to-skill-pipeline` | รีเสิร์ชและสร้าง Hermes Skills จากเว็บ |

---

### ⚙️ DevOps

| Skill | คำอธิบาย |
|-------|----------|
| `cli-proxy-api-troubleshooting` | วินิจฉัยและแก้ไขปัญหา CLI Proxy API |
| `docker-compose-git-update` | Pull Git และ Rebuild Docker Compose Stacks อย่างปลอดภัย |
| `docker-management` | จัดการ Docker containers, images, volumes, networks |
| `hermes-dashboard-traefik` | เปิด Hermes Dashboard ผ่าน Traefik พร้อม SSL และ systemd |
| `kanban-orchestrator` | Playbook สำหรับ Orchestrator ใน Hermes Kanban |
| `kanban-worker` | Pitfalls และตัวอย่างสำหรับ Kanban Worker |
| `n8n-traefik-postgres` | Deploy n8n + PostgreSQL ผ่าน Traefik |
| `nextjs-traefik-www-redirect` | Deploy Next.js Standalone พร้อม Traefik www redirect |
| `postgres-pgvector-traefik` | Deploy PostgreSQL 18 + pgvector ผ่าน Traefik TCP |
| `traefik-docker29-fix` | แก้ปัญหา Traefik กับ Docker Engine 29.4+ |
| `webhook-subscriptions` | จัดการ Webhook Subscriptions แบบ Event-driven |

---

### 💰 Finance & Trading

| Skill | คำอธิบาย |
|-------|----------|
| `3-statement-model` | สร้าง 3-Statement Financial Models ใน Excel |
| `algorithmic-trading` | สร้างระบบเทรดอัลกอริทึม Backtest และ Deployment |
| `backtest-expert` | คำแนะนำเชิงลึกสำหรับ Backtesting กลยุทธ์การเทรด |
| `backtesting-trading-strategies` | Backtest กลยุทธ์ Crypto และ Traditional Trading |
| `comps-analysis` | Comparable Company Analysis ใน Excel |
| `dcf-model` | DCF Valuation Models ระดับ Institutional |
| `excel-author` | สร้าง Excel Workbooks แบบ Headless ด้วย openpyxl |
| `innovestx-api` | InnovestX Digital Asset Open API Integration |
| `lbo-model` | Leveraged Buyout Models ใน Excel |
| `merger-model` | Accretion/Dilution Merger Models ใน Excel |
| `mt5-python-trading` | Automated Trading ด้วย Python + MetaTrader 5 |
| `personal-finance-and-investment` | การจัดการการเงินส่วนตัว Asset Allocation และ Portfolio Risk |
| `research-backed-investing` | ออกแบบ Asset Allocation ด้วยงานวิจัยวิชาการ |
| `stocks` | ดึงราคาหุ้น ประวัติ เปรียบเทียบ ผ่าน Yahoo Finance |
| `thai-business-law-guide` | คู่มือกฎหมายธุรกิจในประเทศไทย |
| `thai-business-registration` | ขั้นตอนจัดตั้งบริษัทในไทยผ่าน DBD Biz Regist |
| `thai-finance-legal-guide` | อ้างอิงกฎหมายภาษี หุ้น และ Crypto ในไทย |
| `thai-tax-planning-strategy` | วางแผนภาษีอย่างถูกกฎหมายสำหรับบุคคลและนิติบุคคล |

---

### 💻 Software Development

| Skill | คำอธิบาย |
|-------|----------|
| `agent-skills-github-sync` | Sync Hermes Skills ขึ้น GitHub Repository |
| `better-auth-nextjs` | ตั้งค่า Authentication ใน Next.js ด้วย better-auth |
| `cli-proxy-api-management` | ตั้งค่าและ Query CLIProxyAPI Management Endpoints |
| `cliproxy-quota-check` | เช็คโควต้าและสถิติ CLIProxyAPI |
| `cliproxy-quota-inspector` | ตรวจสอบสถานะ Account และ Quota ของ CLIProxyAPI |
| `fastapi` | Best Practices และ Conventions สำหรับ FastAPI |
| `hermes-agent-skill-authoring` | เขียน SKILL.md ตามมาตรฐาน Hermes |
| `langgraph-development` | สร้าง AI Agents ด้วย LangGraph และ MLflow |
| `nextjs-16-migration` | คู่มือ Upgrade ไปยัง Next.js 16 |
| `nextjs-spa-static-export` | สร้าง SPA/Static Sites ด้วย Next.js |
| `nextjs-ui-libraries` | UI Libraries สำหรับ Next.js (shadcn/ui, Tailwind ฯลฯ) |
| `plan` | เขียน Plan แบบ Markdown ก่อน Execute |
| `python-debugpy` | Debug Python ด้วย pdb + debugpy remote |
| `requesting-code-review` | Pre-commit Review: Security Scan และ Quality Gates |
| `satang-project-suite` | พัฒนาและ Deploy โปรเจกต์ AI และ Trading ของ Satang |
| `simplify-code` | Parallel 3-agent Cleanup ของโค้ดที่เพิ่งเปลี่ยนแปลง |
| `smart-context-usage` | แนวทาง Token Efficiency และ Context Compression |
| `spike` | ทดลองไอเดียก่อน Build จริง |
| `subagent-driven-development` | Execute Plans ผ่าน Subagent Delegation |
| `systematic-debugging` | 4-Phase Root Cause Debugging |
| `test-driven-development` | TDD: RED-GREEN-REFACTOR |
| `uv-package-management` | จัดการ Python Dependencies ด้วย uv |
| `web-mobile-ux-guidelines` | หลักการ UI/UX สำหรับ Web และ Mobile |
| `writing-plans` | เขียน Implementation Plans แบบ Bite-sized |

---

### 🎨 Creative

| Skill | คำอธิบาย |
|-------|----------|
| `architecture-diagram` | SVG Architecture Diagrams แบบ Dark Theme |
| `ascii-art` | ASCII Art ด้วย pyfiglet, cowsay, boxes |
| `baoyu-infographic` | Infographics 21 layouts × 21 styles |
| `claude-design` | HTML Artifacts (Landing, Deck, Prototype) |
| `excalidraw` | Hand-drawn Excalidraw JSON Diagrams |
| `humanizer` | แปลงข้อความ AI ให้ฟังดูเป็นธรรมชาติ |
| `manim-video` | Manim CE Animations สไตล์ 3Blue1Brown |
| `p5js` | p5.js Sketches: Generative Art, Shaders, 3D |
| `pixel-art` | Pixel Art แบบ NES, Game Boy, PICO-8 |
| `popular-web-designs` | Design Systems จาก 54 แบรนด์จริง (Stripe, Linear ฯลฯ) |
| `sketch` | HTML Mockups 2-3 Design Variants |
| `songwriting-and-ai-music` | Songwriting และ Suno AI Music Prompts |

---

### 📊 Marketing & Business

| Skill | คำอธิบาย |
|-------|----------|
| `ai-product-strategy` | กำหนด AI Product Strategy |
| `business-analyst` | วิเคราะห์ธุรกิจด้วย AI Analytics และ KPI Frameworks |
| `business-health-diagnostic` | วินิจฉัยสุขภาพ SaaS Business |
| `competitor-price-analysis` | วิเคราะห์ราคาคู่แข่งและ Market Positioning |
| `content-marketing-2026-2027` | กลยุทธ์ Content Marketing สำหรับยุค AI (ตลาดไทย) |
| `designing-growth-loops` | ออกแบบ Growth Loops และ Viral Mechanics |
| `ecommerce-business-plan` | สร้างแผนธุรกิจ E-commerce ครบวงจร |
| `founder-sales` | ช่วย Founders ปิดลูกค้าคนแรกและสร้าง Sales Process |
| `thai-branding-strategy` | กลยุทธ์ Personal และ Business Branding ในไทย |
| `thai-content-compliance` | ตรวจสอบความถูกต้องของ Content ในตลาดไทย |
| `thailand-content-strategy-2026` | วางแผน Content Marketing สำหรับตลาดไทยปี 2026 |
| `thailand-market-demand-2026-2027` | วิเคราะห์เทรนด์เศรษฐกิจและ Consumer Demand ในไทย |

---

### 🧬 ML / AI (MLOps)

| Skill | คำอธิบาย |
|-------|----------|
| `audiocraft-audio-generation` | AudioCraft: MusicGen Text-to-Music |
| `dspy` | DSPy: Declarative LM Programs และ Auto-optimize Prompts |
| `evaluating-llms-harness` | Benchmark LLMs (MMLU, GSM8K) ด้วย lm-eval-harness |
| `huggingface-hub` | HuggingFace CLI: Search/Download/Upload Models |
| `llama-cpp` | Local GGUF Inference + HF Hub Model Discovery |
| `ollama-local-inference` | รัน Local LLMs ด้วย Ollama |
| `segment-anything-model` | SAM: Zero-shot Image Segmentation |
| `serving-llms-vllm` | vLLM: High-throughput LLM Serving |
| `weights-and-biases` | W&B: Log ML Experiments, Sweeps, Model Registry |

---

### 🔗 Blockchain

| Skill | คำอธิบาย |
|-------|----------|
| `evm` | Read-only EVM Client ทั้ง 8 Chains |
| `hyperliquid` | Hyperliquid Market Data, Account History |
| `solana` | Query Solana Blockchain Data + USD Pricing |
| `aicoin-trading` | ส่งคำสั่งซื้อขาย CEX (Binance, OKX, Bybit, Bitget) |
| `aster-bot-trading` | Automated Perpetual Futures Bot สำหรับ AsterDEX |
| `crypto-report` | วิเคราะห์โปรเจกต์ Crypto พร้อม Tokenomics |

---

### 🛠️ Productivity & Tools

| Skill | คำอธิบาย |
|-------|----------|
| `airtable` | Airtable REST API: Records CRUD, Filters |
| `google-workspace` | Gmail, Calendar, Drive, Docs, Sheets ผ่าน CLI |
| `linear` | Linear: Issues, Projects, Teams ผ่าน GraphQL |
| `maps` | Geocode, POIs, Routes, Timezones |
| `notion` | Notion API + ntn CLI |
| `obsidian` | อ่าน สร้าง แก้ไข Notes ใน Obsidian Vault |
| `ocr-and-documents` | Extract ข้อความจาก PDFs/Scans |
| `powerpoint` | สร้าง แก้ไข .pptx ด้วย python-pptx |
| `time-management-and-productivity` | Task Prioritization, Time Blocking, Second Brain |
| `vision-net-registrar` | Scrape ข้อมูลการศึกษาจาก Vision Net E-Registrar (RMUTT ฯลฯ) |

---

### 📡 Research & Data

| Skill | คำอธิบาย |
|-------|----------|
| `arxiv` | ค้นหา Papers บน arXiv |
| `blogwatcher` | Monitor Blogs และ RSS/Atom Feeds |
| `claim-investigation` | ตรวจสอบ Social Media Claims อย่างเป็นระบบ |
| `jupyter-live-kernel` | Iterative Python ผ่าน Jupyter Live Kernel |
| `polymarket` | Query Polymarket: Markets, Prices, Orderbooks |
| `postgresql` | ออกแบบ PostgreSQL Schema ตาม Best Practices |
| `prefect-workflows` | ออกแบบและรัน Data Orchestrations ด้วย Prefect |

---

### 🌐 Web Development

| Skill | คำอธิบาย |
|-------|----------|
| `line-liff-development` | Development Guide สำหรับ LINE LIFF Apps |
| `mcp/fastmcp` | สร้าง MCP Servers ด้วย FastMCP Python |
| `mcp/native-mcp` | MCP Client: Connect Servers, Register Tools |
| `react-2026` | Modern React 2026 Stack Guide |
| `react-composition-2026` | React Composition Patterns ปี 2025/2026 |
| `web-development` | สร้าง Debug Deploy เว็บด้วย React, Vue, Vite |

---

### 📱 Social & Media

| Skill | คำอธิบาย |
|-------|----------|
| `gif-search` | ค้นหาและดาวน์โหลด GIFs จาก Tenor |
| `spotify` | Spotify: Play, Search, Queue, Manage Playlists |
| `xurl` | X/Twitter ผ่าน xurl CLI |
| `youtube-content` | YouTube Transcripts → Summaries, Threads, Blogs |

---

### 🏠 Smart Home

| Skill | คำอธิบาย |
|-------|----------|
| `openhue` | ควบคุม Philips Hue Lights ผ่าน OpenHue CLI |

---

## 📝 หมายเหตุสำคัญ

- **ทุกครั้งที่มีการเพิ่มหรือแก้ไข Skill** ต้นทองจะอัปเดตสารบัญส่วน `## 📚 สารบัญ Skills` ในไฟล์นี้โดยอัตโนมัติ
- Skill ที่สร้างโดย Satang + ต้นทองโดยตรง จะอยู่ในส่วน DevOps และ Software Development เป็นหลัก
- Skill ระดับระบบ (เช่น `hermes-agent`, `hermes-dashboard-traefik`) เป็น Skill ที่ทดสอบแล้วบน VPS จริง

---

*Generated and maintained by ต้นทอง (Tonthong) — Hermes Agent for Satang*
