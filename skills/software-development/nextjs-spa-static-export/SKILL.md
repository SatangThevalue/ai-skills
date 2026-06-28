---
name: nextjs-spa-static-export
description: Best practices for building Single-Page Applications (SPA) and static sites with Next.js using the Static Export feature.
tags:
  - nextjs
  - spa
  - static
  - frontend
version: 1.0.0
date: 2026-06-25
---

# Next.js SPA & Static Export Guide

While Next.js is famous for Server-Side Rendering (SSR), it is also an excellent tool for building Single-Page Applications (SPA) and Static Sites that can be hosted on purely static web servers (Nginx, S3, GitHub Pages, Firebase Hosting) without needing a Node.js server.

## 1. Enabling SPA / Static Export Mode

Starting from Next.js 13.3.0+, you do not use the `next export` command anymore. Instead, you configure it inside `next.config.js`.

```javascript
/**
 * @type {import('next').NextConfig}
 */
const nextConfig = {
  output: 'export', // <--- This tells Next.js to build as a static SPA

  // Optional configurations:
  // trailingSlash: true, // Changes `/about` to `/about/index.html`
}

module.exports = nextConfig
```

Running `next build` will now generate an `out/` directory containing only HTML, CSS, and JS assets.

## 2. Architecture: Server vs. Client Components in an SPA

Even in a purely static export, you still use both Server and Client components in the App Router (`app/` directory).

*   **Server Components (Default):** These are executed **once during build time**. Next.js renders them into static HTML. This is great for SEO and initial load speed.
*   **Client Components (`"use client"`):** These run in the browser just like a traditional React SPA. Route transitions after the initial load happen entirely on the client side.

## 3. Data Fetching in an SPA

Since there is no Node.js server running in production:

*   **Static Data (Build Time):** Fetch data inside Server Components. This data is baked into the HTML during `next build`.
*   **Dynamic Data (Client Side):** To fetch real-time user data, do it inside Client Components using `useEffect` or data-fetching hooks like `SWR` or `@tanstack/react-query`.

## 4. Unsupported Features

When you set `output: 'export'`, Next.js disables features that require a Node.js server to run. Attempting to use these will break the build:

❌ **Not Supported:**
*   `cookies()` and `headers()` from `next/headers`
*   Server Actions
*   Dynamic Routes without `generateStaticParams()`
*   Rewrites, Redirects, and Headers in `next.config.js` (you must handle these on your web server, e.g., Nginx)
*   Incremental Static Regeneration (ISR)
*   Default Next.js Image Optimization (see below)

## 5. Handling Images

The default `<Image src="..." />` component relies on a Node.js server to optimize images on the fly. To use images in a static export, you have two choices:

1.  **Unoptimized Images:** Use standard `<img>` tags or set `unoptimized: true` on the Next.js `<Image>`.
2.  **Custom Loader:** Use a third-party CDN (like Cloudinary or Imgix) to optimize images and configure a custom loader in `next.config.js`:

```javascript
const nextConfig = {
  output: 'export',
  images: {
    loader: 'custom',
    loaderFile: './my-custom-image-loader.js',
  },
}
```

## 6. Accessing Browser APIs (`window`)

Because even Client Components are pre-rendered into HTML at build time, accessing `window`, `document`, or `localStorage` directly in the component body will cause a build error ("window is not defined").

**Always access browser APIs inside `useEffect`:**

```javascript
"use client"
import { useEffect, useState } from 'react'

export default function MyComponent() {
  const [width, setWidth] = useState(0)

  useEffect(() => {
    // This only runs in the browser
    setWidth(window.innerWidth)
  }, [])

  return <div>Window width: {width}px</div>
}
```

## 7. Deployment (e.g., Nginx)

When deploying the `out/` folder to a static server like Nginx, ensure you route `.html` extensions properly so direct links work:

```nginx
server {
  listen 80;
  server_name my-spa.com;
  root /path/to/nextjs/out;

  location / {
      try_files $uri $uri.html $uri/ =404;
  }
}
```