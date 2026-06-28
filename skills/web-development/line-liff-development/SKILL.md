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
*   `liff.getAccessToken()`: Returns access token string (valid 12h max).
*   `liff.getIDToken()`: Returns raw JWT ID token (Requires `openid` scope).
*   `liff.getDecodedIDToken()`: Returns payload object. **Do not send this data to your server.**

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