---
name: ecosystem-knowledge-orchestration
description: "Convert continuous domain inputs into cross-linked modules."
version: 0.1.0
metadata.hermes.tags: [Skill Management, Knowledge Base, Orchestration]
---

# Ecosystem Knowledge Orchestration

This skill captures the agentic workflow for managing a sprawling, multi-file knowledge base within the Hermes skill system. It ensures that master index documents stay updated with references and child modules remain tightly focused, preventing context limit exhaustion. Uses stdlib only.

## When to Use
- User provides a continuous stream of complex, interrelated domain knowledge (e.g., system architectures).
- An existing skill grows too large and needs to be decomposed into an index and child skills.
- A central roadmap, framework, or checklist needs updating based on newly provided sub-domain details.

## Prerequisites
- None. Relies entirely on the native `skill_manage` and `skill_view` tools.

## How to Run
Invoke implicitly through conversational reasoning when parsing and saving large suites of interrelated documents.

## Quick Reference
- `skill_manage(action="create", name="<child-skill>")`
- `skill_manage(action="patch", name="<index-skill>")`

## Procedure
1. Parse the incoming domain text to identify if it defines a new sub-domain or updates an existing topic.
2. If it is a new sub-domain, use `skill_manage` (action="create") to author a highly focused `SKILL.md`.
3. Identify the master index skill (or skills) that govern this overarching topic in the existing knowledge base.
4. Call `skill_manage` (action="patch") on the master index skill.
5. Set `old_string` to the exact block of text in the master index that corresponds to the new sub-domain. Include surrounding context lines to ensure uniqueness.
6. Set `new_string` to the updated text, explicitly appending a cross-link to the new skill using backticks (e.g., `*(See details in \`child-skill-name\`)*`). Ensure that this patch is logically integrated and not just appended as a disjointed sentence.
7. If the user corrects a stylistic pattern, formatting habit, or workflow preference during the conversation, locate the skill that governs that class of task (e.g., `quant-platform-pm-pitfalls` or a similar operational guideline) and PATCH it to embed the correction. Do not just rely on episodic memory for task-specific rules.
8. Summarize the ecosystem updates to the user, confirming both the creation of the child skill and the successful linking from the parent.

## Pitfalls
- Patching fails if `old_string` is not unique or has mismatched trailing whitespace; always include ample surrounding context.
- Forgetting to cross-link makes the new skill an "orphan" that the agent or user might not discover organically.
- Creating deep circular dependencies that confuse the reading flow.

## Verification
Use `skill_view` on the master index skill to verify that the cross-link backticks are correctly formatted and present.