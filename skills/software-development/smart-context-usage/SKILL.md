---
name: smart-context-usage
description: Guidelines for maintaining token efficiency and executing context compression in Hermes
version: 1.0.0
---

# Smart Context Usage & Token Efficiency

This skill details how to manage token usage and optimize the context window in Tonthong (Hermes Agent).

## Core Principles

1. **Be Concise**: Keep replies focused and brief. Avoid intros/outros like "I'd be happy to help!" or restating the query.
2. **Batch Tool Calls**: Avoid doing one tool call per turn when multiple independent checks can be run together.
3. **Optimized Configuration**:
   - `compression.threshold`: Triggers summarization earlier (e.g., at `0.4` instead of `0.5`).
   - `compression.protect_last_n`: Keeps a tighter window of recent history (e.g., `15` instead of `20`).

## Key Actions for the Agent

- Use `/compress` to force context compression when the session becomes slow or token-heavy.
- Call `/usage` to inspect current token consumption.
- Use targeted read/search tools (`read_file` with offset/limit, `search_files`) instead of loading entire large datasets.
- Ensure `smart-context` is loaded during development sessions where token cost is a priority.
