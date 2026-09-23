# Next.js Server-Side Proxy Pattern

A blueprint for proxying frontend requests through Next.js API Routes to a secure backend, ensuring sensitive backend URLs and internal secrets remain hidden from the browser.

## 1. Environment Parsing (`src/lib/env.ts`)
Strictly separate public variables (safe for the browser) from server variables (used only in API routes).

```typescript
import { z } from "zod";

const serverEnvSchema = z.object({
  BACKEND_API_URL: z.string().url(),
  BACKEND_API_SECRET: z.string().min(8),
});

export function getServerEnv() {
  if (typeof window !== "undefined") {
    throw new Error("serverEnv must not be accessed on the client side");
  }
  return serverEnvSchema.parse({
    BACKEND_API_URL: process.env.BACKEND_API_URL,
    BACKEND_API_SECRET: process.env.BACKEND_API_SECRET,
  });
}
```

## 2. API Route (`src/app/api/proxy/route.ts`)
The server-side proxy intercepts requests, attaches internal secrets, and forwards them to the actual backend.

```typescript
import { NextRequest, NextResponse } from "next/server";
import { getServerEnv } from "@/lib/env";

export async function POST(req: NextRequest) {
  try {
    const { action, payload } = await req.json();
    const env = getServerEnv();

    const authHeader = req.headers.get("Authorization") ?? "";
    const idToken = authHeader.replace("Bearer ", "").trim();

    const response = await fetch(env.BACKEND_API_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        ...(idToken && { Authorization: `Bearer ${idToken}` }),
        "X-Internal-Secret": env.BACKEND_API_SECRET, // Injected securely
      },
      body: JSON.stringify({ action, payload }),
    });

    if (!response.ok) {
        // Handle explicit backend errors
        const errorJson = await response.json().catch(() => null);
        return NextResponse.json(errorJson ?? { ok: false }, { status: response.status });
    }

    return NextResponse.json(await response.json());
  } catch (error) {
    return NextResponse.json({ ok: false, error: "Internal Server Error" }, { status: 500 });
  }
}
```

## 3. Frontend Caller (`src/lib/api-client.ts`)
The frontend points only to the Next.js API route.

```typescript
export async function callBackendApi<T>(action: string, payload: any, idToken?: string): Promise<T> {
  const headers: Record<string, string> = { "Content-Type": "application/json" };
  if (idToken) headers["Authorization"] = `Bearer ${idToken}`;

  const res = await fetch("/api/proxy", {
    method: "POST",
    headers,
    body: JSON.stringify({ action, payload }),
  });

  const json = await res.json();
  if (!json.ok) throw new Error(json.error?.message || "API Error");
  return json.data;
}
```