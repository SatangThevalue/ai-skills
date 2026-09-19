---
name: iterative-domain-mapping
description: "Structure continuous domain expertise into linked skills."
version: 0.2.0
metadata:
  hermes:
    tags: [Skills, Workflow, Organization, Architecture, Continuous-Learning]
---

# Iterative Domain Mapping & Skill Creation

This skill provides a systematic framework for translating long, complex conversations involving continuous learning, system architecture, or niche domain expertise into a highly productive, organized network of Hermes Skills. It prevents the "mega-skill" anti-pattern and ensures knowledge remains modular, searchable, and instantly actionable for future agents.

## When to Use
- When the user asks to "find techniques to create the most productive skill files" or "Save all the skills we discussed."
- After a long session where multiple related concepts (e.g., A2A, Infisical, Prefect) were explored, built, and tested.
- When you need to refactor a massive, hard-to-read skill into smaller, interlinked modules.

## Prerequisites
- Understanding of the Hermes `skill_manage` tool.

## How to Run
Follow the 4-phase Domain Mapping Procedure below to evaluate the current session context and generate/patch the necessary `SKILL.md` files.

## Quick Reference
- **Anti-pattern:** One massive 2000-line SKILL.md.
- **Pro-pattern:** A "Hub" skill + multiple specialized "Node" skills linked via `related_skills`.
- **Command:** `skill_manage(action='create', name='...', category='...', content='...')`

## Procedure: The 4-Phase Knowledge Orchestration Framework

### Phase 1: Context Deconstruction (The Audit)
Before writing any files, analyze the conversation history. Identify distinct "Pillars" of knowledge.
1. **Infrastructure/Tools:** What software was installed or configured?
2. **Pipelines/Workflows:** How do the tools connect?
3. **Domain Knowledge/Rules:** What business logic or constraints were established?
4. **Code/Assets:** Are there specific scripts or templates that were finalized?

### Phase 2: Structural Design (The Hub and Spoke Model)
Do not create one giant skill. Design a network.
- **The Hub Skill (Playbook):** Create a high-level playbook that describes *how* the different pieces fit together. It should not contain raw code, but rather architectural diagrams and workflow steps. 
- **The Node Skills (Implementations):** Create specific skills for each technical pillar. These contain the actual code, CLI commands, and setup instructions.
- **The Links:** Ensure every Node skill references the Hub skill (and related Node skills) in its `metadata.hermes.related_skills` array.

### Phase 3: Skill Drafting (The Hermes Standard)
When drafting the `SKILL.md` for each node, strictly adhere to the Hermes authoring standards:
1. **Frontmatter:** Must be perfect YAML. `name` (lowercase-hyphenated), `description` (one sentence, <60 chars).
2. **Sectioning:** Use standard headers: `# Title`, `## When to Use`, `## Prerequisites`, `## How to Run`, `## Quick Reference`, `## Procedure`, `## Pitfalls`, `## Verification`.
3. **Actionable Procedures:** The `## Procedure` section must contain exact, copy-pasteable commands or code blocks. Never write vague summaries here.
4. **Script Extraction:** If a Python/Bash script is longer than 30 lines, do not inline it in the `SKILL.md`. Use `skill_manage(action='write_file', file_path='scripts/my_script.py')` and reference it in the skill documentation.

### Phase 4: Pitfall & Verification Hardening
A skill is only productive if it prevents future failures.
1. **Identify the "Scars":** Look back at the conversation. What failed? (e.g., "Downloading Infisical via curl failed due to GitHub blocking"). 
2. **Document the Workaround:** Add this failure and the successful workaround directly into the `## Pitfalls` section. This is the most valuable part of the skill.
3. **Define Verification:** Write a single, concrete CLI command in `## Verification` that a future agent can run to prove the skill was executed correctly.

## Pitfalls
- **The Router Anti-Pattern:** Creating a Hub skill that *only* lists other skills and provides no actual architectural context. A Hub skill must explain the "Why" and "When", not just link to the "How".
- **Missing Frontmatter:** Failing to format the YAML frontmatter correctly, causing the Hermes skill loader to reject the file.

## Verification
After creating the skills, run `skills_list(category='<your-chosen-category>')` to ensure the new skills appear in the agent's registry.