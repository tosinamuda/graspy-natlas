"use client";

import React, { createContext, useContext, useEffect, useState } from "react";
import { env } from "@/env.client";

interface AccessContextType {
  accessCode: string | null;
  sessionId: string | null;
  isAuthenticated: boolean;
  verifyCode: (code: string) => Promise<boolean>;
  setSessionId: (id: string) => void;
  logout: () => void;
}

const AccessContext = createContext<AccessContextType | undefined>(undefined);

export function AccessProvider({ children }: { children: React.ReactNode }) {
  const [accessCode, setAccessCode] = useState<string | null>(null);
  const [sessionId, setSessionIdState] = useState<string | null>(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isInitializing, setIsInitializing] = useState(true);

  useEffect(() => {
    // Load from storage on mount
    const storedCode = localStorage.getItem("graspy_access_code");
    const storedSession = sessionStorage.getItem("graspy_session_id");

    if (storedCode) {
      setAccessCode(storedCode);
      // Optimistically assume authenticated if code exists,
      // specific requests will fail if invalid/expired, triggering re-login logic if implementing interceptors (skip for now)
      setIsAuthenticated(true);
    }

    if (storedSession) {
      setSessionIdState(storedSession);
    }

    setIsInitializing(false);
  }, []);

  const verifyCode = async (code: string): Promise<boolean> => {
    try {
      const apiUrl = env.NEXT_PUBLIC_API_URL || "http://localhost:8082";
      const res = await fetch(`${apiUrl}/api/access/verify`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ code }),
      });

      if (res.ok) {
        setAccessCode(code);
        setIsAuthenticated(true);
        localStorage.setItem("graspy_access_code", code);
        return true;
      }
      return false;
    } catch (error) {
      console.error("Verification failed", error);
      return false;
    }
  };

  const setSessionId = (id: string) => {
    setSessionIdState(id);
    sessionStorage.setItem("graspy_session_id", id);
  };

  const logout = () => {
    setAccessCode(null);
    setIsAuthenticated(false);
    localStorage.removeItem("graspy_access_code");
  };

  return (
    <AccessContext.Provider
      value={{
        accessCode,
        sessionId,
        isAuthenticated,
        verifyCode,
        setSessionId,
        logout,
      }}
    >
      {!isInitializing && children}
    </AccessContext.Provider>
  );
}

export function useAccess() {
  const context = useContext(AccessContext);
  if (context === undefined) {
    throw new Error("useAccess must be used within an AccessProvider");
  }
  return context;
}
