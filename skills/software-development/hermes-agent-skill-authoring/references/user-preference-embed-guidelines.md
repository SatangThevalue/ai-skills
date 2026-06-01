Guidelines: Embedding user preferences into class-level skills

- When a session produces corrective feedback about style/tone/workflow, add a minimal rule to the relevant skill's `When to Use` or `Preferences`.
- Keep edits concise: one sentence rule + one example.
- Add a `references/<session-id>.md` that records the exact change and the command outputs (redact secrets). Link the reference from the SKILL.md.
- Avoid environment-specific facts in the SKILL.md body; put them in the reference file instead.

Example:
- In SKILL.md under "When to Use": "Prefer concise, action-first replies; when user asks for an operation, run it immediately and report the real output."
- In references/session-YYYY-MM-DD.md: record what ran and the outputs (redacted).
