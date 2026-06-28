---
name: hermes-kanban-swarm
description: "Orchestrate, configure, and execute multi-agent workflows (Swarms) using Hermes Kanban boards and profiles."
version: 1.0.0
author: Tonthong
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [hermes, multi-agent, swarm, kanban, automation, orchestration]
---

# Hermes Kanban Swarm Workflows

This skill provides the standard operating procedure for configuring, deploying, and managing multi-agent swarms using Hermes Agent's native Kanban system and named profiles. 

Use this skill when:
- Setting up parallel or pipelined multi-agent systems (e.g., Researcher -> Writer -> Reviewer).
- Organizing long-running collaborative tasks that must survive restarts or require human-in-the-loop review.
- Troubleshooting stuck worker tasks, dispatcher routing, or profile configuration.

## 1. Setup & Profile Creation

To run a multi-agent swarm, you must first define the specialized roles as independent Hermes profiles.

### Step 1: Create Profiles
Create a profile for each role. Pass `--description` (used by the decomposer for routing) and `--clone` (to copy API keys, `.env`, configuration, and custom skills while keeping session history isolated).
```bash
hermes profile create researcher --description "Researches topics using web search and extraction tools" --clone
hermes profile create writer --description "Drafts and synthesizes research into structured markdown reports" --clone
hermes profile create reviewer --description "Reviews written text for technical accuracy and formatting compliance" --clone
```

### Step 2: Verify Profiles
Verify that the profiles are successfully created and mapped to command aliases:
```bash
hermes profile list
```
Each profile has a command alias at `~/.local/bin/<profile>` (e.g., `researcher chat`, `writer setup`).

---

## 2. Instantiating a Swarm

Hermes Kanban Swarms run on a shared SQLite database (`~/.hermes/kanban.db` for the default board).

### Creating a Swarm (CLI)
Initialize a Swarm v1 graph (Parallel Workers -> Verifier -> Synthesizer) with the `hermes kanban swarm` command:
```bash
hermes kanban swarm "Research and write a report on the current status of Swarm AI Agent in 2026" \
  --worker researcher:"Research Swarm AI Agents status" \
  --verifier reviewer \
  --synthesizer writer
```

This creates a task graph where:
- A root card (e.g. `t_19b6c277`) is marked `done` immediately to serve as the shared blackboard.
- Worker tasks (e.g. `t_6a25ac43`) are assigned to their respective profiles and set to `ready`.
- The verifier task is set to `todo` and blocked until the workers complete.
- The synthesizer task is set to `todo` and blocked until the verifier passes.

---

## 3. Worker Execution & Dispatching

By default, tasks in the `ready` state sit in the queue until claimed by a worker lane.

### Manual Dispatch (Forced Tick)
To run or test the dispatcher immediately instead of waiting for the gateway daemon:
```bash
hermes kanban dispatch
```
The dispatcher will automatically claim the task, create an isolated workspace under `~/.hermes/kanban/workspaces/<task_id>`, and spawn the corresponding profile process (e.g., `hermes -p researcher chat -q ...`).

### Monitoring & Auditing
Track execution progress and trace logs:
```bash
# View active tasks and their state
hermes kanban list

# Check attempt history, run count, and elapsed time for a task
hermes kanban runs <task_id>

# Display live logs or stdout of the active worker process
hermes kanban log <task_id>
```

---

## 4. Key Developer Invariants & Pitfalls

### Ephemeral Workspaces
By default, tasks use `scratch` workspaces located at `~/.hermes/kanban/workspaces/<task_id>`. 
- **Pitfall:** This directory is **wiped immediately** upon task completion. 
- **Fix:** If workers write files that must persist, they must copy them to a shared host path or write them directly to a directory workspace (e.g., `dir:/absolute/path/to/project`) instead of scratch space. Alternatively, log paths can be recorded in comments or metadata.

### Stalled Tasks
- **Symptom:** Tasks remain in the `ready` state indefinitely.
- **Cause:** The dispatcher is not running.
- **Fix:** Run `hermes gateway start` (if configured to run gateway-dispatch) or invoke manual ticks with `hermes kanban dispatch`.

### Shared Bot Token Conflicts
- **Pitfall:** If multiple profiles attempt to launch the gateway (`hermes gateway run/start`) using the same Telegram or Discord bot token, the processes will block each other.
- **Fix:** Run only one main gateway dispatcher. Let worker lanes execute as command-line agents (`hermes -p <profile> chat -q`) instead of standalone gateway bots.
