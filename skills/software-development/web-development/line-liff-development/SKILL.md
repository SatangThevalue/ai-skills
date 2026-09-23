---
name: line-liff-development
description: Development guide and pitfalls for LINE Front-end Framework (LIFF) apps based on official documentation.
tags:
  - liff
  - line
  - frontend
  - web
version: 1.0.0
date: 2026-06-25
---

# LINE Front-end Framework (LIFF) Development

This skill provides guidelines, operating environments, and common pitfalls when developing LIFF (LINE Front-end Framework) applications. 

## Operating Environments

LIFF apps can operate in two main environments with different feature access:

1. **LIFF Browser (In-App)**
   - A dedicated webview running inside the LINE app (WKWebView for iOS, Android WebView for Android).
   - Allows access to user data without login prompts.
   - Provides LINE-specific features like sharing and sending messages.
   - **Caching:** Managed strictly via HTTP headers (e.g., `Cache-Control`). There is no way to explicitly clear the LIFF browser cache programmatically or via UI.

2. **External Browser**
   - Runs on standard browsers (Chrome, Safari, Edge, Firefox).
   - Some LINE-specific APIs are restricted (e.g., `liff.scanCode()` will not work in an external browser).

## Key UI Components & Navigation

- **Action Button / Dropdown Menu:** Present in the header for apps set to `Full` size (unless Module Mode is enabled). It allows sharing, refreshing, and managing permissions.
- **Multi-tab View (LINE v15.12.0+):** Displays up to 50 recently used LIFF apps.
  - **Resume:** Opens exactly where the user left off (retains token, history, scroll) if opened within 12 hours and in the top 10 recent items.
  - **Reload:** Initializes at the last URL but discards token, history, and scroll position if resume conditions are not met.

## Environment & Context Methods

Use these to determine where and how the app is running. Some are available even before `liff.init()` finishes.

*   `liff.getOS()`: Returns `"ios"`, `"android"`, or `"web"`.
*   `liff.getAppLanguage()`: Returns LINE app language (RFC 5646). *Requires LIFF browser & LINE v14.11.0+.*
*   `liff.getVersion()`: Returns LIFF SDK version string.
*   `liff.getLineVersion()`: Returns LINE version string (LIFF browser only, `null` otherwise).
*   `liff.isInClient()`: Returns `true` if in LIFF browser, `false` if external.
*   `liff.isLoggedIn()`: Returns `true` or `false`.
*   `liff.isApiAvailable(apiName)`: Checks if an API/feature is supported (e.g., `shareTargetPicker`).
*   `liff.getContext()`: Gets context data.
    *   Returns object with `type` (`utou`, `group`, `room`, `external`, `none`), `userId`, `liffId`, `viewType`, etc.
    *   *Note: Chat room IDs (`utouId`, `groupId`, `roomId`) have been discontinued.*

## Initialization & Lifecycle

### `liff.init(config, successCallback, errorCallback)`
Must be called before using most LIFF APIs.
*   **Arguments:** `config` object `{ liffId: String (Required), withLoginOnExternalBrowser: Boolean (Optional, default false) }`
*   **Returns:** `Promise`
*   **Critical Rules:**
    1.  Execute at the exact Endpoint URL or a lower-level path.
    2.  Process URL changes (e.g., `window.location.replace`) only *after* the `Promise` resolves.
    3.  **Do not log the primary redirect URL to external analytics tools** (it contains the raw access token).
    4.  Do not modify SDK-injected query params (e.g., `liff.state`, `liff.referrer`).

### `liff.ready`
A `Promise` resolving after the first `liff.init()`. Can be used *before* initialization finishes.
```javascript
liff.ready.then(() => { // Safe to use APIs here });
```

## Authentication & Tokens

*   `liff.login({ redirectUri })`: Prompts login in external browsers. **Do not use in LIFF browser.** `redirectUri` must start with Endpoint URL.
*   `liff.logout()`: Logs the user out.
*   `liff.openWindow({ url, external })`: Opens a URL in the LIFF browser or the system's external browser (e.g., Safari/Chrome).
    *   *Mobile-First Payment Gateway UX Pattern:* When linking to external payment links (such as BeamCheckout) from inside the LINE App context, **always** use `liff.openWindow({ url, external: true })` to force the phone to open it in Chrome/Safari. This ensures mobile browser features (like App-to-App deep linking to banking apps for QR PromptPay payments) work natively, avoiding screen-freeze or screenshot-to-scan friction within the LINE in-app webview.
*   `liff.getAccessToken()`: Returns access token string (valid 12h max).
*   `liff.getIDToken()`: Returns raw JWT ID token (Requires `openid` scope). **This is the ONLY token you should send to your backend for authentication.**
*   `liff.getDecodedIDToken()`: Returns payload object. **Do not send this data to your server.**

### Secure Proxy Pattern (Next.js + LIFF)
When building full-stack LIFF apps with an external backend (e.g., n8n, external API):
1. **Frontend acts as a proxy:** The frontend must NEVER send `lineUserId` or `profile` objects as the source of truth for authentication (they can be spoofed by malicious clients).
2. **Pass ID Token:** The frontend should send ONLY the LINE ID Token (e.g., via an `X-Line-Id-Token` header) to the Next.js API Routes.
3. **Backend Validation:** The Next.js API Route acts as a secure proxy, forwarding the ID token (and a server-to-server shared secret) to the actual backend, which is responsible for verifying the LINE ID Token and resolving the user.

## Permissions

*   `liff.permission.getGrantedAll()`: Returns an array of scopes the user actually granted (e.g., `["profile", "openid"]`).
*   `liff.permission.query(permission)`: Checks specific scope status. Returns Promise `{ state: 'granted' | 'prompt' | 'unavailable' }`.

## API Errors

Errors are returned as `LiffError` objects: `{ code: String, message: String, cause: Unknown }`.
*   **Always identify errors using both `code` and `message`**.
*   Key codes: `400`, `401`, `403`, `INIT_FAILED`, `INVALID_ARGUMENT`, `UNAUTHORIZED`.

## Critical Pitfalls & Limitations

1. **OpenChat Restrictions:** LIFF apps are not officially supported inside OpenChat. Attempting to retrieve user profiles (`liff.getProfile()`) will generally fail.
2. **`liff.scanCode()`:** This function cannot be used when the app is opened in an external browser.
3. **Caching Issues:** Because the LIFF browser cache cannot be explicitly deleted, always ensure your web server returns appropriate `Cache-Control` headers, or use cache-busting techniques (like hashing filenames) during deployment.
4. **Share Function Failure:** The native "Share" feature from the LIFF dropdown menu will fail if the current URL does not start exactly with the **Endpoint URL** registered in the LINE Developers Console.
5. **`liff.sendMessages()` after Reload:** If a user re-opens the LIFF app from the "recently used services" (Multi-tab view) and a **Reload** occurs (discarding the token), using `liff.sendMessages()` will throw an error. To use it, the user must reopen the LIFF app by tapping the actual LIFF URL in a chat room.
6. **Secure Proxy Architecture:** Never expose backend URLs (e.g., `n8n` webhooks) or API shared secrets in the LIFF client environment. Always implement a secure proxy layer (e.g., Next.js API Routes). The client sends `liff.getIDToken()` to the proxy; the proxy validates it and attaches internal API secrets before forwarding the payload to the actual backend.

## Next.js App Router Integration

### Architecture Pattern (Security-First)
- **Frontend sends ID Token only** — never `lineUserId` as source of truth
- **Next.js acts as secure proxy** — API Routes forward idToken + shared secret to n8n
- **n8n verifies the ID Token** and resolves user identity server-side
- This prevents user ID spoofing from the client

```
LIFF Frontend → liff.getIDToken() → Next.js /api/* → n8n webhook (with X-API-Secret)
                                                      ↓ verify token + query DB
```

### liff.ts wrapper — always isolate SDK to a single client-only module
```typescript
// src/lib/liff.ts — "use client" at top (NOT in layout or RSC)
import liff from "@line/liff";
let initialized = false;

export async function initLiff(): Promise<void> {
  if (initialized) return;                        // guard against double-init
  await liff.init({ liffId: process.env.NEXT_PUBLIC_LIFF_ID!, withLoginOnExternalBrowser: true });
  initialized = true;
}
export function getLiffIdToken(): string | null {
  try { return liff.getIDToken(); } catch { return null; }
}
```

### LiffContext — call initLiff() inside useEffect, not at module level
```typescript
useEffect(() => {
  let cancelled = false;
  async function init() {
    await initLiff();
    if (cancelled) return;
    setIsReady(true);
    // fetch profile + idToken here
  }
  init();
  return () => { cancelled = true; };
}, []);
```

### `useSearchParams()` — MUST be wrapped in `<Suspense>`
Next.js 16 throws a build error if a page uses `useSearchParams()` outside a Suspense boundary. Pattern:
```tsx
// Split into inner component + wrapper export
function PageInner() {
  const searchParams = useSearchParams();   // safe inside Suspense
  // ...
}
export default function Page() {
  return (
    <Suspense fallback={<LoadingUI />}>
      <PageInner />
    </Suspense>
  );
}
```

### n8n Proxy — server-side only, never client-side
```typescript
// src/lib/n8n-proxy.ts (server-side only — no "use client")
export async function callN8n<T>(opts: N8nRequestOptions): Promise<T> {
  const res = await fetch(getN8nUrl(opts.endpoint), {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-API-Secret": process.env.N8N_API_SHARED_SECRET!,
    },
    body: JSON.stringify({ action: opts.action, idToken: opts.idToken, ...opts.payload }),
    cache: "no-store",
  });
  // ...
}
```

### Zod v4 API Changes (breaking from v3)
- `z.enum(["a","b"], { errorMap: ... })` → use `z.enum(["a","b"])` only (errorMap removed)
- `z.number({ invalid_type_error: "..." })` → use `.positive("msg")` directly
- These cause TS2769 errors at build time — remove the options object or use `.positive("msg")`

### Next.js 16 + Tailwind v4 — no separate tailwind.config.js needed
- Tailwind v4 uses `@import "tailwindcss"` in globals.css (no config file)
- CSS custom properties via `@layer base { :root { --color-primary: ... } }`
- `@layer utilities { .my-class { ... } }` works as before

### Build Checklist for LIFF + Next.js
- [ ] `NEXT_PUBLIC_LIFF_ID` set in `.env.local`
- [ ] `liff.ts` has `"use client"` at top — never imported in RSC
- [ ] All `useSearchParams()` calls wrapped in `<Suspense>`
- [ ] API Routes use `cache: "no-store"` when proxying to n8n
- [ ] `withLoginOnExternalBrowser: true` in `liff.init()` for non-LINE browsers
- [ ] `NEXT_PUBLIC_APP_URL` matches the LIFF Endpoint URL in LINE console exactly

## Development Tools

LY Corporation provides several official tools for LIFF development:
- **LIFF Playground:** For testing basic features online.
- **Create LIFF App:** A CLI tool (like Create React App) to quickly scaffold a development environment.
- **LIFF CLI:** Tool to create, update, list, and delete apps, debug via LIFF Inspector, and run local HTTPS servers.

## Workflow

1. Create a channel in the LINE Developers Console.
2. Register your endpoint URL and configure settings (App size, Module mode, etc.).
3. Scaffold your project using the **Create LIFF App** CLI.
4. Integrate the `liff` SDK and initialize it using `liff.init({ liffId: 'YOUR_LIFF_ID' })`.

## Reference Files

- `references/nextjs-liff-architecture.md` — Full production architecture for Next.js 16 + LIFF: env vars, file structure, n8n action convention, Zod v4/recharts TS build fixes, Tailwind v4 globals.css template. Verified build 2026-06-30.