---
name: nextjs-16-migration
description: Comprehensive guide and checklist for upgrading to Next.js 16, covering Turbopack, Async Request APIs, and breaking changes.
tags:
  - nextjs
  - migration
  - upgrade
  - react
version: 1.0.0
date: 2026-06-25
---

# Migrating to Next.js 16

Next.js 16 introduces major architectural changes, strict requirements for async APIs, and makes Turbopack the default bundler. Follow this guide to upgrade safely.

## 1. Upgrade Commands

**Automated (Codemod):**
```bash
pnpm dlx @next/codemod@canary upgrade latest
```
*(Handles Turbopack config migration, `middleware` -> `proxy` rename, and removes deprecated flags.)*

**Manual:**
```bash
pnpm add next@latest react@latest react-dom@latest
```

## 2. System Requirements
- **Node.js:** `20.9.0` (LTS) minimum. (Node 18 is dropped).
- **TypeScript:** `5.1.0` minimum.

## 3. Major Breaking Changes

### A. Async Request APIs (Strict Enforcement)
Synchronous access to request-time APIs is fully removed. **You MUST `await` them.**
- **Affected:** `cookies`, `headers`, `draftMode`, `params` (in pages/layouts), `searchParams`.
- **Images/Sitemaps:** The `params` and `id` passed to dynamic image generation (`opengraph-image`, `icon`) and `sitemap` functions are now Promises.

```tsx
// ❌ Next.js 15 (Sync)
export default function Page({ params }) {
  return <h1>{params.slug}</h1>
}

// ✅ Next.js 16 (Async)
export default async function Page(props) {
  const { slug } = await props.params
  return <h1>{slug}</h1>
}
```

### B. `middleware` is now `proxy`
If you are using middleware, you must migrate it:
- Rename `middleware.ts` to `proxy.ts`.
- Rename the exported function from `middleware` to `proxy`.
- **CRITICAL:** The new `proxy` runtime is strictly `nodejs`. The `edge` runtime is NO LONGER SUPPORTED in `proxy`. (If you absolutely need the edge runtime, you must keep using `middleware.ts` temporarily, but it is considered legacy).

### C. Turbopack by Default
Turbopack is now the default for both `next dev` and `next build`.
- If you have a custom Webpack config (`webpack` in `next.config.js`), the build will **fail** to prevent accidental misconfiguration. You must use `--webpack` to opt-out, or `--turbopack` to force Turbopack and ignore the webpack config.
- Config moved from `experimental.turbopack` to top-level `turbopack`.
- **Sass:** The `~` prefix for node_modules imports is removed. Use `@import 'bootstrap/...'` instead of `@import '~bootstrap/...'`.

## 4. Caching & Data Fetching Updates

- **`updateTag` (NEW):** A Server Action API for immediate read-your-writes. Refreshes data in the same request to prevent stale UI.
- **`revalidateTag`:** Now requires a second argument for a cache profile: `revalidateTag('posts', 'max')`.
- **`cacheLife` & `cacheTag`:** Now stable (remove `unstable_` prefix).
- **PPR:** `experimental_ppr` is removed. Enable via `cacheComponents: true` in config.

## 5. `next/image` Breaking Changes
- **Minimum Cache TTL:** Increased from 60 seconds to **4 hours** (14400s) to reduce CPU load.
- **Qualities:** Default allowed qualities changed from any number to just `[75]`.
- **Local Query Strings:** You must explicitly allow query strings on local images to prevent enumeration attacks via `localPatterns` in `next.config.ts`.

## 6. React 19.2 & Compiler
- Next.js 16 uses React 19.2 Canary (View Transitions, `useEffectEvent`).
- **React Compiler** is now stable. Opt-in via `reactCompiler: true` in `next.config.ts` (requires `babel-plugin-react-compiler`).