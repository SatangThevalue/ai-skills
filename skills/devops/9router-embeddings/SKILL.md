---
name: 9router-embeddings
description: Generate vector embeddings via 9Router for RAG, semantic search, similarity.
version: 0.1.0
metadata.hermes.tags:
  - 9Router
  - Embeddings
  - RAG
  - VectorSearch
---

# 9Router — Embeddings

Requires `NINEROUTER_URL` (and `NINEROUTER_KEY` if auth enabled). See `9router` skill for setup.

## When to Use

- User wants embeddings, vectors, RAG, semantic search, or to embed text chunks.

## Discover

```bash
curl $NINEROUTER_URL/v1/models/embedding | jq '.data[].id'
curl "$NINEROUTER_URL/v1/models/info?id=openai/text-embedding-3-small"
```

## Quick Reference

- **Endpoint:** `POST $NINEROUTER_URL/v1/embeddings`
- **Fields:** `model` (required), `input` string or array (required), `encoding_format` float/base64, `dimensions` (OpenAI v3 only)

## Procedure

**bash:**
```bash
curl -X POST $NINEROUTER_URL/v1/embeddings \
  -H "Authorization: Bearer *** \
  -H "Content-Type: application/json" \
  -d '{"model":"openai/text-embedding-3-small","input":["hello","world"]}'
```

**JS:**
```js
const r = await fetch(`${process.env.NINEROUTER_URL}/v1/embeddings`, {
  method: "POST",
  headers: { "Authorization": `Bearer ${process.env.NINEROUTER_KEY}`, "Content-Type": "application/json" },
  body: JSON.stringify({ model: "gemini/text-embedding-004", input: "RAG chunk text" }),
});
const { data } = await r.json();
console.log(data[0].embedding.length);  // dimension
```

## Response Shape

```json
{ "object": "list", "model": "openai/text-embedding-3-small",
  "data": [
    { "object": "embedding", "index": 0, "embedding": [0.0123, -0.045, ...] }
  ],
  "usage": { "prompt_tokens": 5, "total_tokens": 5 } }
```

## Provider Quirks

| Provider | Notes |
|---|---|
| `openai`, `openrouter`, `mistral`, `voyage-ai`, `fireworks`, `together`, `nebius`, `github`, `nvidia`, `jina-ai` | Native OpenAI shape. `dimensions` only on OpenAI v3 |
| `gemini`, `google_ai_studio` | Auto-converts to `embedContent`/`batchEmbedContents` |
| `openai-compatible-*`, `custom-embedding-*` | Custom `baseUrl` from credentials |

Batch (`input` as array) is faster; some providers cap batch size.

## Verification

```bash
curl -X POST $NINEROUTER_URL/v1/embeddings \
  -H "Authorization: Bearer *** \
  -H "Content-Type: application/json" \
  -d '{"model":"gemini/text-embedding-004","input":"test"}' | jq '.data[0].embedding | length'
```
