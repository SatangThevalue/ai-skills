---
name: cross-linked-skill-authoring
description: "Build modular, cross-linked Hermes skills from raw domain text."
version: 0.1.0
metadata.hermes.tags: [Knowledge Base, Documentation, Skill Authoring, Architecture]
---

# Cross-Linked Skill Authoring

This skill defines the workflow for converting large, monolithic brain-dumps from the user into a structured, modular, and cross-linked ecosystem of Hermes skills. It prevents mega-skills, ensures maintainability, and creates a navigable knowledge graph by establishing explicit references between related skills.

## When to Use
- User pastes massive architectural documents, codebases, or domain guides.
- User asks to "save this knowledge" that spans multiple distinct domains (e.g., Database, MLOps, Orchestration).
- Building a complex project documentation suite (e.g., Quant Trading Platform).

## Prerequisites
- None. Relies entirely on the native `skill_manage` and `skill_view` tools.

## How to Run
Invoke through standard conversational reasoning. Parse the user's input, plan the skill decomposition, and execute `skill_manage` calls concurrently or sequentially to build the ecosystem.

## Quick Reference
- `skill_manage(action="create", name="<skill-name>")`
- `skill_manage(action="patch", name="<skill-name>", old_string="...", new_string="...")`
- `skill_view(name="<skill-name>")`

## Procedure

1. **Decompose the Input (Domain Analysis)**
   Analyze the raw text and identify distinct domains. Do not cram everything into one skill. 
   *(Example: Separate "Database Architecture" from "Feature Engineering" from "Workflow Orchestration" from "Platform Comparison").*

2. **Create Modular Skills**
   Use the `skill_manage` tool (`action="create"`) to author a dedicated SKILL.md for each new domain. Keep names lower-kebab-case, concise, and descriptive.
   *(Example: `quant-database-architecture`, `mlflow-quant-tracking-guide`)*

3. **Iterative Updates via Patching**
   When the user provides follow-up information or deep-dives belonging to an existing domain, DO NOT create a redundant skill. 
   - Call `skill_view` to read the existing skill.
   - Call `skill_manage` (`action="patch"`) to inject the new information or replace placeholder sections.

4. **Establish Cross-Links (The Knowledge Graph)**
   Whenever a new skill relates to an existing one, update the existing skill to point to the new one.
   - Use `skill_manage` (`action="patch"`) on the parent/index skill.
   - Add explicit references using backticks. 
   - *(Example string: `*(ดูสถาปัตยกรรมระดับสถาบันเพิ่มเติมได้ที่สกิล \`quant-database-architecture\`)*`)*

5. **Report Ecosystem Status**
   Send a concise message to the user explaining:
   - The new skill(s) created.
   - What existing skills were updated.
   - How the new knowledge links back to the broader ecosystem.

## Pitfalls
- **The Mega-Skill:** Creating a single 500-line skill instead of breaking it down. This exceeds context limits and degrades recall.
- **Orphaned Skills:** Creating a new skill but forgetting to `patch` the related index/parent skills to link to it.
- **Redundant Creation:** Overwriting or creating a new skill with a slightly different name instead of patching the existing one.
- **Cross-link Typos:** Misspelling the skill name in the cross-link backticks, preventing the user or agent from loading it later.

## Verification
Call `skills_list()` to ensure all created skills appear in the registry, and use `skill_view(name="<parent-skill>")` to verify that the cross-links to child skills are intact.