---
name: 9router-tts
description: Text-to-speech via 9Router /v1/audio/speech — OpenAI, ElevenLabs, Edge TTS, Google TTS, and more.
version: 0.1.0
metadata.hermes.tags:
  - 9Router
  - TTS
  - Audio
  - Voice
---

# 9Router — Text-to-Speech

Requires `NINEROUTER_URL` (and `NINEROUTER_KEY` if auth enabled). See `9router` skill for setup.

## When to Use

- Convert text to speech, generate voiceover, narrate, or read text aloud via 9Router.

## Discover

Use `terminal`:

```bash
# List available TTS models
curl $NINEROUTER_URL/v1/models/tts | jq '.data[].id'

# Per-model metadata
curl "$NINEROUTER_URL/v1/models/info?id=el/eleven_multilingual_v2"

# List voices (edge-tts, elevenlabs, deepgram, inworld). Optional ?lang=vi
curl "$NINEROUTER_URL/v1/audio/voices?provider=edge-tts&lang=vi" | jq '.data[].model'
```

`model` in `/v1/audio/speech` = voice ID directly (e.g. `edge-tts/vi-VN-HoaiMyNeural`, `el/<voice_id>`, `openai/tts-1`).

## Quick Reference

- **Endpoint:** `POST $NINEROUTER_URL/v1/audio/speech`
- **Fields:** `model` (required), `input` (required)
- **Format:** `?response_format=mp3` (default, raw bytes) or `?response_format=json` (`{audio: base64, format}`)

## Procedure

**Save MP3 (bash):**
```bash
curl -X POST "$NINEROUTER_URL/v1/audio/speech" \
  -H "Authorization: Bearer $NINEROUTER_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"openai/tts-1","input":"Hello world"}' \
  --output speech.mp3
```

**Save MP3 (JS):**
```js
import { writeFile } from "node:fs/promises";
const r = await fetch(`${process.env.NINEROUTER_URL}/v1/audio/speech`, {
  method: "POST",
  headers: { "Authorization": `Bearer ${process.env.NINEROUTER_KEY}`, "Content-Type": "application/json" },
  body: JSON.stringify({ model: "el/eleven_multilingual_v2", input: "Xin chào" }),
});
await writeFile("speech.mp3", Buffer.from(await r.arrayBuffer()));
```

## Provider Quirks

| Provider | `model` format | Notes |
|---|---|---|
| `openai` | `tts-1/alloy` or just voice | Default model `gpt-4o-mini-tts` |
| `elevenlabs` | `<model_id>/<voice_id>` or `<voice_id>` | Default `eleven_flash_v2_5` |
| `openrouter` | `openai/gpt-4o-mini-tts/alloy` | Via chat-completions audio modality |
| `edge-tts` | e.g. `vi-VN-HoaiMyNeural` | noAuth; default `vi-VN-HoaiMyNeural` |
| `google-tts` | language code e.g. `en`, `vi` | noAuth |
| `local-device` | OS voice name | noAuth; needs `ffmpeg` |
| `deepgram` | `aura-asteria-en` etc | Token auth |
| `hyperbolic` | model id | Body = `{text}` only |

## Verification

```bash
curl -X POST "$NINEROUTER_URL/v1/audio/speech" \
  -H "Authorization: Bearer $NINEROUTER_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"edge-tts/vi-VN-HoaiMyNeural","input":"ทดสอบ"}' \
  --output test.mp3 && echo "OK"
```
