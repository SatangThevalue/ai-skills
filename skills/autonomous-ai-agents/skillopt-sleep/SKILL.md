---
name: skillopt-sleep
description: Validate and refine agent skills through nightly sleep cycles with held-out gates. Wraps Microsoft's SkillOpt-Sleep engine.
version: 0.1.0
metadata:
  hermes:
    tags: [Optimization, Agents, Microsoft, SkillOpt]
---

# SkillOpt-Sleep

A nightly self-improvement loop for AI agents. It reads your recent session transcripts, mines recurring workflow patterns, replays them with proposed skill edits, and gates the proposals against a held-out test set. Only improvements that beat the baseline are staged for your manual adoption.

This solves the problem of agents forgetting corrections between sessions by formalizing the update of your `SKILL.md` files through a rigorous, validation-gated process (treating the skill document as trainable weights).

## When To Use

- When a skill is used 10+ times/week and starts drifting or feeling inefficient.
- After complex, multi-turn error correction where you want the agent to "remember" the fix for next time.
- When an existing skill regresses in quality.
- To run an offline consolidation pass on your agent's skills while you sleep.

## Prerequisites

- The `microsoft/SkillOpt` package installed (`pip install skillopt`).
- A configured LLM backend (e.g., Azure OpenAI, Anthropic, or Qwen) with credentials set in `~/.skillopt-sleep/config.json` or `.env`.
- An active `SKILL.md` you want to optimize.

## How to Run

Use the `terminal` tool to trigger the sleep cycle:

```bash
# Run one cycle to optimize a specific skill
python -m skillopt_sleep --target-skill-path ~/.hermes/skills/<skill-name>/SKILL.md

# Dry run (report only, no staging)
python -m skillopt_sleep --dry-run
```

## Quick Reference

- **Harvests:** Transcripts from recent sessions.
- **Mines:** Recurring tasks and pain points.
- **Replays:** Tests the task with the current skill vs. the proposed new skill.
- **Gates:** Rejects changes if the validation score drops.
- **Stages:** Saves successful updates to `~/.skillopt-sleep/staging/<night>/` for you to review.

## Procedure

1. **Verify Installation**
   Check that SkillOpt is installed and the CLI is available:
   ```bash
   python -m skillopt_sleep --help
   ```

2. **Run the Sleep Cycle (Manual Trigger)**
   Point the engine at a specific skill that needs improvement:
   ```bash
   python -m skillopt_sleep --target-skill-path ~/.hermes/skills/finance/settrade-dw-daily-income-bot/SKILL.md
   ```

3. **Review the Staged Proposal**
   If the optimizer finds an improvement that passes the validation gate, it will stage it. Use `read_file` to review the proposed diff:
   ```bash
   cat ~/.skillopt-sleep/staging/latest/report.md
   ```

4. **Adopt the Changes**
   If you agree with the proposed improvements, manually copy the `best_skill.md` over your existing skill, or let the tool adopt it if you ran with `--auto-adopt`.

## Pitfalls

- **Cost:** Running the optimizer requires multiple LLM calls (generating variants, judging rollouts, reflecting). Limit the number of tasks per night (`--max-tasks 10`) to control API spend.
- **Over-optimization:** Short skills (< 300 tokens) may become too rigid if optimized too aggressively against a narrow set of tasks.
- **Missing Signal:** If you haven't used the skill much recently, the engine won't have enough session transcripts to mine meaningful improvements.

## Verification

After a successful run, the staging directory will contain a `report.md` detailing the exact score improvements and the bounded edits proposed for the skill.