---
name: chrome-extension-mv3-development
description: Official guidelines, architecture, and constraints for building Google Chrome Extensions using Manifest V3 (MV3).
---
# Google Chrome Extension Development (Manifest V3)

This skill provides the official architectural patterns, code structures, and strict requirements for building Google Chrome Extensions based on the latest **Manifest V3 (MV3)** standard. MV2 is deprecated and must not be used.

## 1. Architecture & Planning
A modern Chrome Extension consists of four distinct environments that run in isolation and communicate via message passing:
1. **`manifest.json`**: The configuration file and heart of the extension.
2. **Service Worker (`background.js`)**: The event handler. Runs in the background, sleeps when idle. Has NO access to the DOM (`window` or `document`).
3. **Content Scripts**: JavaScript injected into web pages. Can read/modify the DOM of the web page but has limited access to Chrome APIs.
4. **UI Elements (Popup/Options)**: Standard HTML/JS pages displayed when clicking the extension icon or in the settings menu.

## 2. The `manifest.json` (V3 Structure)
Every extension requires this file in the root directory.
```json
{
  "manifest_version": 3,
  "name": "My Great Extension",
  "version": "1.0",
  "description": "An example Manifest V3 extension.",
  "permissions": [
    "storage",
    "activeTab",
    "scripting"
  ],
  "host_permissions": [
    "https://api.example.com/*"
  ],
  "background": {
    "service_worker": "background.js"
  },
  "action": {
    "default_popup": "popup.html",
    "default_icon": {
      "16": "images/icon16.png",
      "48": "images/icon48.png",
      "128": "images/icon128.png"
    }
  },
  "content_scripts": [
    {
      "matches": ["https://*.google.com/*"],
      "js": ["content.js"],
      "css": ["styles.css"]
    }
  ]
}
```

## 3. Core Functionalities & Code Examples

### A. Message Passing (Communication)
Since environments are isolated, they must communicate using the `chrome.runtime` API.

**Sending a message (from Popup or Content Script):**
```javascript
chrome.runtime.sendMessage({ action: "fetch_data", query: "cats" }, (response) => {
  console.log("Received response:", response);
});
```

**Receiving a message (in Service Worker):**
```javascript
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "fetch_data") {
    // Return true to indicate we will send a response asynchronously
    fetchDataAsync(request.query).then(sendResponse);
    return true; 
  }
});
```

### B. State Management (Chrome Storage)
Service workers are *ephemeral* (they terminate when not in use). Global variables will be lost. You MUST use `chrome.storage` to save state.
```javascript
// Saving data
chrome.storage.local.set({ key: "value" }).then(() => {
  console.log("Value is set");
});

// Reading data
chrome.storage.local.get(["key"]).then((result) => {
  console.log("Value currently is " + result.key);
});
```

## 4. Strict Official Constraints & Security (MV3 Rules)
- **No Remote Hosted Code:** You cannot load arbitrary executable code (JavaScript or Wasm) from an external server. All code must be bundled within the extension. No `<script src="https://...">`.
- **No `eval()`:** Content Security Policy (CSP) strictly forbids `eval()` and inline scripts (`<script>console.log('hi')</script>` inside HTML). All JS must be in separate `.js` files.
- **Service Workers ≠ Background Pages:** You cannot use `XMLHttpRequest` in a service worker; you MUST use the `fetch()` API. You cannot access the DOM or `window` object in a service worker.
- **Action API:** In MV3, `chrome.browserAction` and `chrome.pageAction` are unified into a single `chrome.action` API.

## 5. Agent Instructions (How to apply this skill)
- **NEVER use Manifest V2.** Always set `"manifest_version": 3`.
- **NEVER use `chrome.extension.getBackgroundPage()`.** This is MV2. Service workers do not have a page.
- **Check Permissions:** Only request permissions absolutely necessary for the feature. Separate API domains into `"host_permissions"` (do not put URLs in `"permissions"`).
- **Asynchronous Code:** Most modern `chrome.*` APIs support Promises. Prefer `async/await` and Promises over callbacks (except for event listeners like `onMessage`).
- **DOM Manipulation:** If a user asks to "click a button on a webpage", write a **Content Script**. If they ask to "listen for a browser tab closing", write a **Service Worker**.