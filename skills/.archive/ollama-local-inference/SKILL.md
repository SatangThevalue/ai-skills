---
name: ollama-local-inference
description: Run and manage local LLMs and embedding models using Ollama.
version: 0.1.0
metadata:
  hermes:
    tags:
      - Ollama
      - Local-Inference
      - LLM
      - Embedding
      - Memory-Management
---

# Ollama Local Inference

Ollama allows running open-source large language models and embedding models locally. This skill covers model management, optimization, and memory configuration.

## When to Use
- When deploying local models (e.g., Llama 3, Qwen 2, Nomic Embed) on a resource-constrained VPS or workstation.
- When configuring Ollama's memory model-retention policies to prevent RAM exhaustion.
- When troubleshooting slow generation speeds or connection failures.

## Prerequisites
- Ollama binary installed and running as a service.
- Sufficient RAM (minimum 4GB for embeddings/small models, 8GB+ for 7B+ parameters).

## How to Run
- Manage Ollama services and download models using the `terminal` tool.
- Edit service environments or system config files using the `patch` or `write_file` tools.

## Quick Reference
- Start service: `ollama serve`
- Run model: `ollama run <model>`
- List loaded models: `ollama ps`
- Unload all models: Send a request with `keep_alive: 0` or set `OLLAMA_KEEP_ALIVE=0`.

## Procedure

### 1. Model Management
1. Download and run a model (e.g., Nomic text embedding):
   ```bash
   ollama run nomic-embed-text
   ```
2. Verify the model is loaded:
   ```bash
   ollama list
   ```

### 2. Optimizing RAM Usage (Memory Management)
Ollama keeps models in memory for 5 minutes by default (`OLLAMA_KEEP_ALIVE=5m`). To reclaim RAM immediately:
1. **Per-Request Unloading:**
   In your API requests (to `/api/generate`, `/api/chat`, or `/api/embeddings`), include the `keep_alive` parameter set to `0`:
   ```json
   {
     "model": "nomic-embed-text",
     "prompt": "Hello world",
     "keep_alive": 0
   }
   ```
2. **Global Service Unloading Configuration:**
   Configure the systemd service to never keep models in memory after execution.
   Edit the systemd service environment:
   ```bash
   # Create override file
   systemctl edit ollama.service
   ```
   Add the environment variable under the service section:
   ```ini
   [Service]
   Environment="OLLAMA_KEEP_ALIVE=0"
   ```
   Reload systemd and restart the service:
   ```bash
   systemctl daemon-reload
   systemctl restart ollama
   ```

## Pitfalls
- **High Concurrency RAM Spikes**: Running multiple models simultaneously can cause out-of-memory (OOM) kills. Ensure `OLLAMA_NUM_PARALLEL` is configured if concurrency is needed, or keep it to `1` on lower-RAM VPS instances.
- **CPU Bottlenecks**: Without a GPU, inference uses CPU threads. Restrict threads using `OLLAMA_NUM_PARALLEL=1` and ensure the model size matches available CPU cores.

## Verification
Query the running models and ensure memory is released after use:
```bash
ollama ps
```
The output should show no active models running in memory if the keep-alive timeout has passed or `OLLAMA_KEEP_ALIVE=0` is active.
