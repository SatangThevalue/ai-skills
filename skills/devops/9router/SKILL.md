---
name: 9router
description: Entry point for 9Router — local/remote AI gateway with OpenAI-compatible REST for chat, image, TTS, embeddings, web search, web fetch. Use when the user mentions 9Router, NINEROUTER_URL, or wants AI without writing provider boilerplate. This skill covers setup + indexes capability skills; fetch the relevant capability SKILL.md from the URLs below when needed.
version: 0.1.0
metadata.hermes.tags:
  - 9Router
  - Gateway
  - AI
  - Proxy
---

# 9Router

Local/remote AI gateway exposing OpenAI-compatible REST. One key, many providers, auto-fallback.

## Setup

```bash
export NINEROUTER_URL="http://localhost:20128"      # or VPS / tunnel URL
export NINEROUTER_KEY="sk-..."                      # from Dashboard → Keys (only if requireApiKey=true)
```

All requests: `${NINEROUTER_URL}/v1/...` with header `Authorization: Bearer ${NINEROUTER_KEY}` (omit if auth disabled).

Verify via `terminal`: `curl $NINEROUTER_URL/api/health` → `{"ok":true}`

## When to Use

- User mentions "9Router", `NINEROUTER_URL`, or wants to call AI models without writing provider boilerplate.
- Need auto-fallback across multiple LLM/image/TTS/STT accounts.

## Discover Models

Use `terminal` to list available models:

```bash
curl $NINEROUTER_URL/v1/models                  # chat/LLM (default)
curl $NINEROUTER_URL/v1/models/image            # image-gen
curl $NINEROUTER_URL/v1/models/tts              # text-to-speech
curl $NINEROUTER_URL/v1/models/embedding        # embeddings
curl $NINEROUTER_URL/v1/models/web              # web search + fetch
curl $NINEROUTER_URL/v1/models/stt              # speech-to-text
curl $NINEROUTER_URL/v1/models/image-to-text    # vision
```

Use `data[].id` as the `model` field in requests. Combos appear with `owned_by:"combo"`.

## Capability Skills

When the user needs a specific capability, fetch that skill's `SKILL.md` from its raw URL:

| Capability | Raw URL |
|---|---|
| Chat / code-gen | https://raw.githubusercontent.com/decolua/9router/refs/heads/master/skills/9router-chat/SKILL.md |
| Image generation | https://raw.githubusercontent.com/decolua/9router/refs/heads/master/skills/9router-image/SKILL.md |
| Text-to-speech | https://raw.githubusercontent.com/decolua/9router/refs/heads/master/skills/9router-tts/SKILL.md |
| Speech-to-text | https://raw.githubusercontent.com/decolua/9router/refs/heads/master/skills/9router-stt/SKILL.md |
| Embeddings | https://raw.githubusercontent.com/decolua/9router/refs/heads/master/skills/9router-embeddings/SKILL.md |
| Web search | https://raw.githubusercontent.com/decolua/9router/refs/heads/master/skills/9router-web-search/SKILL.md |
| Web fetch (URL → markdown) | https://raw.githubusercontent.com/decolua/9router/refs/heads/master/skills/9router-web-fetch/SKILL.md |

## Pitfalls

- `401` → set/refresh `NINEROUTER_KEY` (Dashboard → Keys)
- `400 Invalid model format` → check `model` exists in `/v1/models/<kind>`
- `503 All accounts unavailable` → wait `retry-after` or add another provider account

## Verification

```bash
curl $NINEROUTER_URL/api/health
```
→ `{"ok":true}`
