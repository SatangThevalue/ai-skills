---
name: nextjs-liff-fastapi-backend
description: Build a Next.js LIFF app using Python FastAPI with LangChain
version: 0.2.0
metadata:
  hermes:
    tags:
      - nextjs
      - python
      - liff
      - fastapi
      - line-mini-app
---

# Next.js LIFF with FastAPI Backend

A modern, containerized architecture for building LINE Mini Apps (LIFF) with a Next.js App Router frontend and a Python FastAPI backend serving AI integrations (LangChain, Gemini).

## When to Use
- Building a LINE Mini App (LIFF) using Next.js 14+ (App Router).
- Integrating a FastAPI backend for LINE webhooks and LLM/AI processing.
- You need a mobile-first UI embedded within LINE Official Accounts.

## Prerequisites
- Node.js 18+ and `pnpm`
- Python 3.11+
- `@line/liff` npm package installed
- A LINE Channel with LIFF added, sized "Full", with endpoint pointing to your deployed Next.js app.

## How to Run
Invoke through the `terminal` tool.
- Frontend: `pnpm build && pnpm start`
- Backend: `uvicorn src.main:app --host 0.0.0.0 --port 8000`

## Procedure

1. **Install LIFF SDK in Next.js:**
   ```bash
   pnpm install @line/liff
   ```

2. **Create a Client-Side LiffProvider:**
   Since Next.js App Router uses Server Components by default, and `liff.init()` requires the browser `window`, wrap it in a client context provider (`src/components/liff/LiffProvider.tsx`):
   ```tsx
   "use client";
   import React, { createContext, useContext, useEffect, useState } from "react";
   import liff from "@line/liff";

   interface LiffContextType {
     liff: typeof liff | null;
     profile: any | null;
     isReady: boolean;
     login: () => void;
   }
   const LiffContext = createContext<LiffContextType>({} as LiffContextType);
   export const useLiff = () => useContext(LiffContext);

   export function LiffProvider({ children }: { children: React.ReactNode }) {
     const [liffObject, setLiffObject] = useState<typeof liff | null>(null);
     const [profile, setProfile] = useState<any | null>(null);
     const [isReady, setIsReady] = useState(false);

     useEffect(() => {
       const liffId = process.env.NEXT_PUBLIC_LIFF_ID;
       if (!liffId) { setIsReady(true); return; }

       liff.init({ liffId, withLoginOnExternalBrowser: true })
         .then(() => {
           setLiffObject(liff);
           if (liff.isLoggedIn()) liff.getProfile().then(p => setProfile(p));
           setIsReady(true);
         }).catch(err => setIsReady(true));
     }, []);

     const login = () => { if (liffObject && !liffObject.isLoggedIn()) liffObject.login(); };

     return (
       <LiffContext.Provider value={{ liff: liffObject, profile, isReady, login }}>
         {children}
       </LiffContext.Provider>
     );
   }
   ```

3. **Wrap the Application:**
   In `src/app/layout.tsx`:
   ```tsx
   import { LiffProvider } from "@/components/liff/LiffProvider";
   export default function RootLayout({ children }: { children: React.ReactNode }) {
     return (
       <html lang="th">
         <body><LiffProvider>{children}</LiffProvider></body>
       </html>
     );
   }
   ```

4. **Protect Routes requiring LINE Login:**
   In `src/app/dashboard/page.tsx`:
   ```tsx
   "use client";
   import { useEffect } from "react";
   import { useLiff } from "@/components/liff/LiffProvider";

   export default function Dashboard() {
     const { liff, profile, isReady, login } = useLiff();

     useEffect(() => {
       if (!isReady) return;
       // Force login if inside LINE app but not logged in (rare, but handles external browser opens)
       if (liff && !liff.isLoggedIn() && liff.isInClient()) {
         login();
       }
     }, [isReady, liff, login]);

     if (!isReady) return <div>Loading...</div>;
     return <div>Welcome {profile?.displayName}</div>;
   }
   ```

5. **Provide LIFF ID via Environment:**
   In `.env.local`:
   ```env
   NEXT_PUBLIC_LIFF_ID="1234567890-abcdefgh"
   ```

## Pitfalls
- **Window is not defined:** `liff` cannot be imported or initialized in Server Components. Always use `"use client"` and ensure `liff.init()` runs inside a `useEffect`.
- **404 Not Found on Production Build:** If a page fails to build due to a type error (e.g., exporting a non-component function from `page.tsx` or `layout.tsx`), Next.js will silently exclude it from the static export, leading to a 404 in production. Always run `pnpm build` and verify all routes were generated. Move utility functions (e.g., API fetchers) to `src/lib/`.
- **Next.js Caching:** If your dashboard fetches API data, ensure you handle caching correctly. Use `cache: 'no-store'` or handle client-side fetching with `useEffect` to ensure fresh data.

## Verification
Open the deployed frontend URL in a desktop browser; it should redirect to the LINE login screen (if `withLoginOnExternalBrowser: true` is set). Open the LIFF URL (`https://liff.line.me/<LIFF_ID>`) in the LINE app; it should load seamlessly and display the user's LINE profile.