# Next.js and LINE LIFF Integration

## 1. Context and Provider Setup
To turn a Next.js app into a LINE Mini App, wrap your application in a LIFF Provider. This ensures the LIFF SDK initializes correctly and makes the user profile globally available.

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

const LiffContext = createContext<LiffContextType>({
  liff: null, profile: null, isReady: false, login: () => {}
});

export const useLiff = () => useContext(LiffContext);

export function LiffProvider({ children }: { children: React.ReactNode }) {
  const [liffObject, setLiffObject] = useState<typeof liff | null>(null);
  const [profile, setProfile] = useState<any | null>(null);
  const [isReady, setIsReady] = useState(false);

  useEffect(() => {
    const liffId = process.env.NEXT_PUBLIC_LIFF_ID;
    if (!liffId) return;

    liff.init({ liffId, withLoginOnExternalBrowser: true })
      .then(() => {
        setLiffObject(liff);
        if (liff.isLoggedIn()) {
          liff.getProfile().then(setProfile);
        }
        setIsReady(true);
      });
  }, []);

  const login = () => liffObject && !liffObject.isLoggedIn() && liffObject.login();

  return (
    <LiffContext.Provider value={{ liff: liffObject, profile, isReady, login }}>
      {children}
    </LiffContext.Provider>
  );
}
```

## 2. Using LIFF in Pages
In your components, consume the context. If the user is inside the LINE client but not logged in, trigger the login flow.

```tsx
"use client";
import { useLiff } from "@/components/liff/LiffProvider";

export default function Dashboard() {
  const { liff, profile, isReady, login } = useLiff();

  useEffect(() => {
    if (!isReady) return;
    if (liff && !liff.isLoggedIn() && liff.isInClient()) {
      login();
      return;
    }
  }, [isReady, liff, login]);

  if (!isReady) return <div>Loading...</div>;

  return <div>Welcome {profile?.displayName}</div>;
}
```

## 3. Deployment Notes
- Ensure `NEXT_PUBLIC_LIFF_ID` is set in your `.env.local` or Docker environment.
- The Endpoint URL in the LINE Developers Console must match your exact domain and path (e.g., `https://your-domain.com/dashboard`).
- HTTPS is strictly required for LIFF to initialize.