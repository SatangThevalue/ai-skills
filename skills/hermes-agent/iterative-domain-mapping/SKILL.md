---
name: iterative-domain-mapping
description: "Structure continuous domain expertise into linked skills."
version: 0.1.0
metadata.hermes.tags: [Skill Authoring, Knowledge Management, System Design]
---

# Iterative Domain Mapping
Converts sequential, unstructured domain expertise provided over multiple conversation turns into a modular network of Markdown files. It prevents context window bloat by splitting massive architectures into focused modules and explicitly cross-linking them. Uses standard built-in tools only.

## When to Use
- User provides a multi-part masterclass, architecture document, or complex tutorial across several messages.
- User asks to organize a large domain (e.g., MLOps, Quant Trading) into reusable knowledge.
- Existing skills require continuous updates with new granular details without losing structure.

## Prerequisites
- No external environment variables or credentials required.

## How to Run
Invoke through standard conversation turns, leveraging the `skill_manage` tool to progressively build and patch the knowledge base as the user provides more information.

## Quick Reference
- `skill_manage(action="create", name="<skill-name>", category="<category>", content="<markdown>")`
- `skill_manage(action="patch", name="<skill-name>", old_string="<exact-match>", new_string="<replacement>")`
- `skill_view(name="<skill-name>")`

## Procedure
1. Parse the incoming text chunk and identify its core domain boundary.
2. If the domain is new, formulate a focused `SKILL.md` and use `skill_manage` (action="create") to save it.
3. If the domain expands on an existing skill, locate the insertion point and use `skill_manage` (action="patch") to append or replace sections using exact `old_string` matching.
4. Inject cross-links into the text using Markdown italics and backticks (e.g., `*(See details in \`related-skill-name\`)*`) to connect the new knowledge to the broader ecosystem.
5. Summarize the changes to the user, confirming which skills were created or patched and how they connect.

## Pitfalls
- Patch failures occur due to non-unique `old_string` or trailing whitespace mismatches. Ensure `old_string` includes enough surrounding context lines.
- Creating "mega-skills" that exceed practical readability; always split into sub-domains (e.g., separating Feature Engineering from Data Architecture).
- Neglecting to patch parent or index skills with cross-links to newly created child skills.

## Verification
Use `skill_view(name="<parent-skill>")` to verify that the injected cross-links point correctly to the newly updated or created child skills.