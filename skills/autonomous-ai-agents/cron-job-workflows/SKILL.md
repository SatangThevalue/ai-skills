---
name: cron-job-workflows
description: Guidelines and pitfalls for executing headless, non-interactive tasks as a scheduled cron job in Hermes.
category: autonomous-ai-agents
---

# Cron Job Workflows

Executing tasks as a scheduled cron job in Hermes differs fundamentally from interactive sessions. You have no human partner to clarify intent, and your lifecycle is strictly bounded by your turn execution.

## Core Principles

1. **Zero Interaction**: Do not ask questions or pause for approval. You must make reasonable rulings and execute autonomously to completion. If you get stuck, your final output must be an actionable report of the exact blocker.
2. **Direct Delivery**: Your final response is the payload delivered to the cron job's configured destination. Put the primary content (reports, summaries) directly in your response text instead of using `send_message`.
3. **Silent Suppression**: If the job runs but there is genuinely nothing new to report (e.g., a periodic check where state hasn't changed), output exactly `[SILENT]` and nothing else to suppress the delivery. Never mix `[SILENT]` with other text.

## Pitfall: Background Delegations (`delegate_task`)

**Do not use background `delegate_task` in a cron job if you intend to exit immediately.** 

Background delegations are not durable across session boundaries. If your cron session finishes its turn and returns a final response before the subagents complete, the Hermes process exits and **all running background subagents are instantly killed**. Their work is discarded entirely.

**Workarounds for Execution in Cron Jobs:**
- **Inline Execution (Preferred):** Use direct tool calls (`terminal`, `patch`, `write_file`) to execute the work yourself in the foreground. This guarantees the work completes before your session turn ends.
- **`execute_code` Scripts:** If you need heavy processing or multi-tool logic, write an `execute_code` Python script. It runs in the foreground and blocks until completion.
- **Strict Wait-Loops (If you must delegate):** If you absolutely must use background tasks, you *must* implement a wait mechanism (e.g. `process(action='wait')` or terminal polling) so your cron turn does not end until the work is done. However, this is risky due to LLM context timeouts. Inline execution is vastly preferred for cron jobs.

## Pitfall: Fragile Regex on Large Files

Because you cannot rely on subagents easily, you may need to edit large files directly (e.g., 100KB+ JSX files). 
- Avoid fragile regex replacements using `sed` or Python AST parsers that can silently break enclosing tags (e.g., stripping `</div>` accidentally). 
- Prefer finding unique anchor strings and replacing exactly the intended block, or use `patch` with enough context lines to guarantee safety. 
- Always run `npm run build` or the project's equivalent compilation step immediately after patching a large file to verify structural integrity before committing.

## Error Handling

When a tool, script, or compilation fails, you cannot ask the user for a fix. You must read the error, attempt a fix, and if it completely blocks the goal, your final response must be a structured error report containing:
1. The exact failure.
2. What you attempted to fix it.
3. What manual intervention is needed by the user.