---
name: loop-engineering-onboarding
description: Scaffolds Loop Engineering, tailwind v4, and binds subagents.
version: 0.1.0
metadata.hermes.tags:
  - Loop
  - Architecture
  - Nextjs
  - Subagents
---

# Loop Engineering Onboarding

Upgrades a legacy Next.js application to meet 2026/2027 Loop Engineering standards. It scaffolds loop control files, upgrades Tailwind CSS to v4, ensures Docker/PostgreSQL environments do not port-collide, and hard-binds subagent delegations to the loop constraints to prevent bounded context violations.

## Core Directives (User Preferences)
- **Mandatory Initialization:** You MUST automatically run `npx @cobusgreyling/loop init` for every new or migrated project *before* writing any code. Do not wait for permission.
- **Task Tracking:** You MUST initialize and use the `hermes kanban` toolset (`hermes kanban init`, `hermes kanban create`, `hermes kanban assign`) for every project to track tasks. Always assign the current profile to the tasks.

## When to Use
- "Apply loop engineering to this project."
- "Modernize this legacy project to 2026 standards."
- "Set up subagents and loop constraints for this repo."

## Prerequisites
- A Next.js application repository.
- Node.js and npm installed.
- Docker for database dependencies.

## How to Run
Execute the procedure steps in order through the `terminal` and `patch` tools. 

## Quick Reference
- `npx @cobusgreyling/loop init`
- `npm install -D @tailwindcss/postcss`
- `drizzle-kit push --force`

## Procedure

1. **Initialize Kanban Tracking (Mandatory)**
   Always use the Kanban board to track the onboarding and refactoring workflow:
   ```bash
   hermes kanban init
   hermes kanban create "Project Onboarding"
   hermes kanban assign <id> amooksan-dev
   ```

2. **Clean Legacy Context & Scaffold Loop**
   Remove old agent artifacts to reset context, then scaffold the loop baseline. Use the `terminal` tool:
   ```bash
   rm -rf .agents conductor
   npx --yes @cobusgreyling/loop init
   ```

2. **Upgrade UI to Tailwind v4**
   Install the correct PostCSS plugin to prevent Turbopack build errors:
   ```bash
   npm install -D @tailwindcss/postcss --legacy-peer-deps
   ```
   Create or patch `postcss.config.js`:
   ```javascript
   module.exports = {
     plugins: {
       '@tailwindcss/postcss': {},
     },
   }
   ```
   Patch `globals.css` to use v4 `@theme` block:
   ```css
   @import "tailwindcss";

   @theme {
     --color-background: #000000;
     --color-primary: #7b63ff;
     --color-text: #ffffff;
   }
   ```

3. **Ensure Database Readiness**
   Verify `docker-compose.yml` does not cause port collisions (e.g., change `5432:5432` to `5433:5432` if the local port is occupied).
   Start the database and forcefully push schema using the `terminal` tool:
   ```bash
   docker compose up -d postgres
   npx dotenv-cli -e .env.local -- npm run db:push --force
   ```

4. **Bind Sub-Agents to Loop Constraints**
   Use the `patch` tool to inject a Global Constraint into the project's `AGENTS.md` (or equivalent):
   ```markdown
   **⚠️ GLOBAL SUBAGENT CONSTRAINTS (LOOP ENGINEERING):**
   Every subagent MUST read and strictly adhere to `loop-constraints.md` located at the root of the project before making any codebase changes. Subagents must never violate the bounded context, and must report their actions back to the main orchestrator without auto-merging unless explicitly allowed.
   ```
   Use the `patch` tool to update `loop-constraints.md` with:
   ```markdown
   ## Orchestration & Sub-agents
   - When delegating tasks via `delegate_task`, the orchestrator MUST inject: "Read loop-constraints.md and AGENTS.md before starting" in the subagent's `context`.
   - Sub-agents are bound by these constraints just like the main agent.
   - Sub-agents must not invoke nested sub-agents (max_spawn_depth=1) unless configured otherwise.
   ```

5. **Save to Agent Memory**
   Invoke the `memory` tool (action="add") to record the delegation rule permanently for the current profile:
   "When deploying subagents via `delegate_task`, ALWAYS include the following in the `context` parameter: 'Read loop-constraints.md and AGENTS.md before starting your task'."

## Pitfalls
## Pitfalls
- **Subagent API Rate Limits:** Concurrent fan-out of subagents via `delegate_task` can exhaust the active model's API quota (e.g., HTTP 503 Resource Exhausted). If subagents fail repeatedly, the main orchestrator must fall back to manual execution using standard tools.
- **Tailwind v4 Errors:** Next.js Turbopack might throw "Cannot apply unknown utility class `bg-background`" if `@tailwindcss/postcss` is not used. Avoid using `tailwindcss` directly in `postcss.config.js`.
- **Drizzle Interactive Prompts:** `drizzle-kit push` fails in non-TTY environments. Always use the `--force` flag.
- **Postgres Port Collisions:** Local port `5432` is often taken. Remapping to `5433:5432` prevents `EADDRINUSE` errors.

## Verification
Run the dev server in the background and curl the endpoint to prove the application builds and serves successfully.
```bash
npm run dev -- -p 9999
sleep 5 && curl -s http://localhost:9999 | head -n 10
```