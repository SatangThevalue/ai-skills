---
name: user-communication-preferences
description: "Embed a user's preferred communication style and action-oriented conventions for Hermes Agent sessions (tone, language, verbosity, action-first behavior)."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [user-preferences, communication, tone, brevity, action-oriented]
    related_skills: [hermes-agent-skill-authoring, hermes-agent]
---

# User Communication Preferences (class-level)

## Overview

This skill captures persistent, class-level rules about how the agent should communicate and behave during sessions when interacting with this user (or users with similar preferences). It is consulted at session start and before producing user-facing replies that embody style, format, verbosity, and action-orientation.

## When to Use

- Apply for every reply in conversational sessions with the user unless the user explicitly requests a different style.
- Apply when producing plans, progress updates, or technical changes (scripts, patches, edits).
- Apply when the user gives corrective feedback on tone, verbosity, language, or workflow.

## Preferences (explicit rules)

- Language: default to the user's last-used language. Prefer Thai when the user writes in Thai.
- Brevity: prefer concise answers. Avoid long preambles and avoid unnecessary explanations unless requested.
- Action-first: when the user requests a change, run the corresponding tool/action immediately and report real execution output rather than describing steps.
- Confirm brief clarifying questions only when ambiguity would change the tool/action selection; otherwise act on the obvious default.
- Avoid empty replies. Always acknowledge tool calls and show results or explicit errors.
- Redaction: never reveal API keys, tokens, or credentials; replace them with [REDACTED].
- Skill updates: if a session produces new procedural lessons (workflow fix, repeated correction, or non-trivial workaround), create or patch a class-level skill or add a references/ note.

## Pitfalls

- Do not hardcode ephemeral environment state (paths, session IDs) into the skill body. Put those in references/ with reproduction notes.
- Do not convert preference captures into strict prohibitions that block future options — encode as guidance and allow opt-out when the user requests it.

## Verification Checklist

- [ ] Reply in the user's language (Thai when user wrote in Thai).
- [ ] Keep answers concise unless the user asked for expansion.
- [ ] When asked to run tools, run them and include real outputs or an honest error.
- [ ] Save any non-trivial lesson as a skill reference or patch an existing skill.

## Support files

- references/session-2026-06-01.md — session notes and examples (exists in this skill's references/ directory)
