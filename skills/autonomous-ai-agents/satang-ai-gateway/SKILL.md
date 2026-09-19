---
name: satang-ai-gateway
description: "Satang AI: Integration patterns for FastAPI Gateway, Better Auth, and LINE OA."
version: 0.2.0
metadata:
  hermes:
    tags: [A2A, LINE, FastAPI, Auth, SaaS, Monetization]
    related_skills: [infisical-secrets-management, prefect-orchestration-monetization]
---

# Satang AI Gateway (A2A Inbound Architecture)

This skill defines the architecture for transforming the local Hermes agent ("Tonthong") into a headless API Gateway that can receive A2A (Agent-to-Agent) commands from external web services, specifically a Next.js frontend (using Better Auth) and a LINE OA Webhook.

This is the core infrastructure for the B2B Micro-SaaS/DaaS monetization path, allowing external customers to pay for and interact with the AI without accessing the terminal.

## Architecture Overview

1. **The Caller (External):** 
   - A Next.js Web App (Customer Dashboard / Better Auth).
   - A FastAPI Webhook Server (LINE OA connection).
2. **The Transport (Tailscale):** 
   - External servers communicate with the VPS via Tailscale VPN IP (100.115.66.121), ensuring no public ports are exposed on the AI server.
3. **The Receiver (Hermes Gateway):** 
   - Hermes runs in `--gateway` mode, listening on port 9900 via the A2A protocol.
4. **The Security (Infisical):** 
   - A2A Bearer tokens are stored in Infisical and injected at runtime.

## Procedure: Setting up the A2A Inbound Gateway

### 1. Enable A2A Platform in Hermes
Configure Hermes to listen for incoming A2A HTTP requests.
```bash
hermes config set gateway.platforms.a2a.enabled true
hermes config set gateway.platforms.a2a.extra '{"port": 9900}'
```

### 2. Configure A2A Security
Edit `~/.hermes/.env` (or preferably, inject these via Infisical when starting the gateway) to secure the endpoint. By default, A2A binds to `127.0.0.1`. To allow the Next.js server (on the Tailscale network) to call it, we bind to the Tailscale IP.

```env
# A2A Security Configuration
A2A_HOST="100.115.66.121"
A2A_PORT="9900"
A2A_PEER_TOKENS="web_...
```

To configure via the CLI instead of `.env`:
```bash
hermes config set gateway.a2a.host "100.115.66.121"
hermes config set gateway.a2a.port 9900
```

### 3. Start the Hermes Gateway via Infisical
To ensure the gateway has access to the A2A tokens and any other secrets (e.g., Database passwords, API keys for tools), start it using the Infisical CLI wrapper.

```bash
cd /home/thaieasyvps/zero-touch-infrastructure/workspace
infisical run --env=prod --domain http://100.115.66.121:8080 -- hermes gateway run
```
*Note: For production, this command should be daemonized (e.g., using `pm2` or `systemd`).*

### 4. Integration Pattern: Next.js (Better Auth) -> A2A
When a user interacts with the Satang AI web dashboard, the Next.js server handles authentication (via Better Auth), verifies quotas, and then forwards the prompt to Hermes via A2A.

**Next.js Server-Side Code (Conceptual):**
```javascript
// Inside a Next.js Server Action or API Route
import { auth } from "@/lib/auth";

export async function askSatangAI(prompt) {
  const session = await auth();
  if (!session) throw new Error("Unauthorized");
  
  // 1. Check user quota in PostgreSQL...
  
  // 2. Call Hermes via A2A Protocol (Over Tailscale)
  const a2aToken = process.env.A2A_WEB_APP_TOKEN; 
  const response = await fetch("http://100.115.66.121:9900/api/v1/message", {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${a2aToken}`,
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      message: prompt,
      contextId: `user-${session.user.id}` // Maintains conversation memory per user
    })
  });
  
  const data = await response.json();
  return data.reply;
}
```

### 5. Integration Pattern: LINE OA Webhook -> A2A
When a user sends a message to the LINE Official Account, the LINE Webhook Server (e.g., FastAPI) receives it and forwards it to Hermes.

**FastAPI Webhook Code (Conceptual):**
```python
import os
import requests
from fastapi import FastAPI, Request

app = FastAPI()

@app.post("/line/webhook")
async def line_webhook(request: Request):
    body = await request.json()
    user_msg = body['events'][0]['message']['text']
    user_id = body['events'][0]['source']['userId']
    
    # Call Hermes via A2A
    a2a_token = os.getenv("A2A_LINE_WEBHOOK_TOKEN")
    res = requests.post(
        "http://100.115.66.121:9900/api/v1/message",
        headers={"Authorization": f"Bearer {a2a_token}"},
        json={
            "message": user_msg,
            "contextId": f"line-{user_id}" # Maps LINE user to a Hermes session
        }
    )
    
    hermes_reply = res.json().get("reply")
    
    # Send hermes_reply back to user via LINE Messaging API...
    return "OK"
```

## Pitfalls
- **Context Bleeding:** The `contextId` in the A2A request is critical. If you use the same `contextId` for all requests, User A will see the memory and conversation history of User B. Always map `contextId` to the unique User ID from Better Auth or LINE.
- **Tailscale Offline:** If the Next.js server or the Webhook server loses its Tailscale connection, it will not be able to reach `100.115.66.121:9900` and will throw timeout errors. Ensure Tailscale runs as a background service on all nodes.
- **Port Conflicts:** Ensure no other service on the VPS is using port `9900`.

## Verification
With the Hermes gateway running, test the endpoint using `curl`:
```bash
curl -X POST http://100.115.66.121:9900/api/v1/message \
  -H "Authorization: Bearer <your_secret_token_1>" \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello Tonthong, what can you do?", "contextId": "test-cli-01"}'
```