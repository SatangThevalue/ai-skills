"use client";
import React, { createContext, useContext, useEffect, useState } from "react";
import liff from "@line/liff";

interface LiffContextType {
  liff: typeof liff | null;
  profile: any | null;
  isReady: boolean;
  login: () => void;
  logout: () => void;
}

const LiffContext = createContext<LiffContextType>({} as any);
export const useLiff = () => useContext(LiffContext);

export function LiffProvider({ children }: { children: React.ReactNode }) {
  const [liffObject, setLiffObject] = useState<typeof liff | null>(null);
  const [profile, setProfile] = useState<any | null>(null);
  const [isReady, setIsReady] = useState(false);

  useEffect(() => {
    const liffId = process.env.NEXT_PUBLIC_LIFF_ID;
    if (!liffId) {
      setIsReady(true);
      return;
    }
    liff.init({ liffId, withLoginOnExternalBrowser: true }).then(() => {
      setLiffObject(liff);
      if (liff.isLoggedIn()) {
        liff.getProfile().then(setProfile);
      }
      setIsReady(true);
    }).catch(console.error);
  }, []);

  const login = () => liffObject && !liffObject.isLoggedIn() && liffObject.login();
  const logout = () => {
    if (liffObject?.isLoggedIn()) {
      liffObject.logout();
      window.location.reload();
    }
  };

  return (
    <LiffContext.Provider value={{ liff: liffObject, profile, isReady, login, logout }}>
      {children}
    </LiffContext.Provider>
  );
}
