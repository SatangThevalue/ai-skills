---
name: loop-engineering-integration
description: Sets up and integrates Loop Engineering boundaries (loop-init, loop-constraints) with Subagent-Driven Development.
---

# Loop Engineering & Subagent Integration

Use this skill whenever you are initializing a new project, setting up a workspace, or orchestrating subagents across a codebase.

## Mandatory Project Initialization

Every new project MUST be initialized with Loop Engineering before any code is written:
1. Run `npx @cobusgreyling/loop init` (or `npx --yes @cobusgreyling/loop init` if not installed) in the project root.
2. This creates `LOOP.md`, `STATE.md`, and `loop-constraints.md`.
3. If the project uses subagents (e.g. via `AGENTS.md`), you must bind the subagents to the loop constraints.

## Subagent Integration Rules

When a project uses both **Loop Engineering** (boundaries, state tracking) and **Subagent-Driven Development** (delegation via `delegate_task`), the orchestrator MUST bridge them:

1. **Global Subagent Constraints:** Inject a rule into `AGENTS.md` (or the project's root instructions) stating: "Every subagent MUST read and strictly adhere to `loop-constraints.md` located at the root of the project before making any codebase changes. Subagents must never violate the bounded context, and must report their actions back to the main orchestrator without auto-merging unless explicitly allowed."
2. **Orchestrator Context Injection:** Whenever invoking `delegate_task` to dispatch a subagent, the orchestrator MUST include the following in the `context` parameter:
   `"Read loop-constraints.md and AGENTS.md before starting your task to ensure adherence to Loop standards."`
3. **No Nested Loops:** Ensure `loop-constraints.md` specifies that subagents are bound by the main project constraints and should not spawn their own nested subagents (`max_spawn_depth=1`) without explicit configuration.

## Workflow

- **Pre-flight:** Always run `npx @cobusgreyling/loop doctor` and `npx @cobusgreyling/loop status` to check the health of the loop before proceeding with complex tasks.
- **State Management:** Keep `STATE.md` updated with "High Priority", "Watch List", and "Run log" entries.
- **Refusals:** Do not proceed with unbound subagent tasks if `loop-constraints.md` is not present or if the subagent context omits the directive to read it.