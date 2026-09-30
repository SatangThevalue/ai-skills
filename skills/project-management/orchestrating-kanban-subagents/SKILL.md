---
name: orchestrating-kanban-subagents
description: Creates a master plan, sets up Kanban tasks, and schedules subagent dispatch.
version: 0.1.0
metadata.hermes.tags:
  - Kanban
  - Cronjob
  - Subagents
  - Orchestration
---

# Orchestrating Kanban & Subagents via Cron

This skill demonstrates how to translate a comprehensive Master Plan into tracked Hermes Kanban tickets, and then schedule a Cronjob to autonomously dispatch AI subagents (`delegate_task`) to work on those tickets at a future time. It relies strictly on Hermes built-in `kanban` and `cronjob` tools.

## When to Use
- "Create a Kanban board for this plan and schedule subagents to start tomorrow."
- "Log these refactoring phases into Kanban and execute them via cron."
- "Divide the master plan into tickets and assign them to the team."

## Prerequisites
- Hermes Agent with `kanban`, `cronjob`, and `delegation` toolsets enabled.
- A running Hermes Gateway (required for Kanban tasks to transition states natively, though cronjobs trigger regardless).

## How to Run
Invoke the task setup through the `terminal` tool, followed by the `cronjob` tool.

## Quick Reference
- `hermes kanban init`
- `hermes kanban create "<Title>"`
- `hermes kanban comment <id> "<Description>"`
- `hermes kanban assign <id> <profile_name>`

## Procedure

1. **Initialize the Kanban Board**
   Use the `terminal` tool to initialize the local Kanban database:
   ```bash
   hermes kanban init
   ```

2. **Create Tasks for Each Phase**
   Break the Master Plan into distinct phases. For each phase, create a task and capture the returned Task ID (e.g., `t_1a2b3c4d`).
   ```bash
   hermes kanban create "Phase 1: Backend & DB Core Refactor"
   ```
   *Note:* `hermes kanban create` accepts ONLY the title string. Passing a second argument for description causes a CLI error (`unrecognized arguments`). Always add descriptions in step 3 via `comment`.

3. **Populate Task Details & Assignment**
   Use the `comment` command to add subagent assignments and specifics, then `assign` it to the active profile:
   ```bash
   hermes kanban comment t_1a2b3c4d "1. Fix DB query. 2. Implement nodemailer. (Assign to: db_engineer, payment_specialist)"
   hermes kanban assign t_1a2b3c4d amooksan-dev
   ```
   *(Repeat Steps 2 and 3 for all phases)*

4. **Human Verification Gate (Strict Rule)**
   Before dispatching execution subagents or starting background tasks, present the Kanban breakdown table to the user and wait for explicit confirmation ("ห้ามเริ่มทำงานก่อน ให้ฉันตรวจสอบก่อน"). Never start editing code or fanning out subagents until the user signs off on the roadmap.

5. **Schedule or Dispatch the Orchestrator**
   Use the `cronjob` tool (action="create") or sequential `delegate_task` calls to start the approved tasks. Cap parallel subagents to a maximum of 2 to prevent rate limits. Provide a clear prompt instructing the orchestrator to read the Kanban board, load specifications, and dispatch tasks.
   - **schedule:** `2026-09-28T21:01:28` (or use exact ISO timestamp).
   - **enabled_toolsets:** `["coding", "terminal", "file", "delegation", "kanban"]`
   - **prompt example:**
     ```markdown
     # Master Plan Execution (Cronjob Trigger)
     1. Use `hermes kanban ls` to identify tasks.
     2. Dispatch `delegate_task` to `db_engineer` to fix the Drizzle query in `src/api/orders.ts`.
     3. Dispatch `delegate_task` to `payment_specialist` to implement `nodemailer`.
     4. Update Kanban ticket states to 'in-progress'.
     ```

## Pitfalls
- **Concurrent Subagent Quota (HTTP 429 & Protocol Violations):** Never dispatch 3 or more subagents in parallel with `delegate_task`. LLM providers enforce tight per-minute quotas that trigger `HTTP 503 / 429 Resource Exhausted`. Furthermore, monolithic tasks given to background agents can hit context limits, causing `Agent crash: worker exited cleanly without calling kanban_complete — protocol violation`. Keep concurrent subagents to a maximum of 2, and break large phases into micro-tasks (e.g., Phase 3.1, 3.2, 3.3).
- **Kanban CLI Syntax:** `hermes kanban create "<title>"` takes only one positional argument. Do not pass description as a second parameter. Use `hermes kanban comment <id> "<desc>"` for specifications, and `hermes kanban complete <id> --summary "<summary>"` to finish.
- **Cronjob Syntax:** Absolute ISO timestamps (e.g., `2026-09-28T21:01:28`) are the safest format. Relative human formats like "in 2 hours 42 minutes" are often rejected.
- **Subagent Recursion:** Cronjobs invoking `delegate_task` will spawn background subagents. Ensure the cronjob prompt does not tell the subagent to spawn *more* subagents (max_spawn_depth defaults to 1).
- **Tool Access:** Ensure the `cronjob` definition explicitly includes `"kanban"` and `"delegation"` in its `enabled_toolsets`, otherwise the cron agent will lack the tools to execute the plan.

## Verification
Use the `terminal` tool to verify the Kanban board and the `cronjob` tool to verify the schedule:
```bash
hermes kanban ls
```
Call `cronjob(action="list")` to ensure the job is active.