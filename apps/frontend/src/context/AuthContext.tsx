"use client";

import React, { createContext, useContext, useEffect, useState } from "react";
import {
  User,
  signInWithPopup,
  signOut as firebaseSignOut,
  onAuthStateChanged,
} from "firebase/auth";
import { auth, googleProvider } from "../lib/firebase";
import { getAccessStatus } from "../lib/api";

interface AuthContextType {
  user: User | null;
  loading: boolean;
  isVerified: boolean;
  login: () => Promise<void>;
  logout: () => Promise<void>;
  checkVerification: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType>({} as AuthContextType);

export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [isVerified, setIsVerified] = useState(false);

  const checkVerification = async () => {
    if (!auth.currentUser) return;
    try {
      const status = await getAccessStatus();
      setIsVerified(status.is_verified);
    } catch (e) {
      console.error("Failed to check verification", e);
      setIsVerified(false);
    }
  };

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(
      auth,
      async (currentUser) => {
        setUser(currentUser);
        if (currentUser) {
          await checkVerification();
        } else {
          setIsVerified(false);
        }
        setLoading(false);
      },
      (error) => {
        console.error("Auth state change error:", error);
        setLoading(false);
      }
    );
    return () => unsubscribe();
  }, []);

  const login = async () => {
    try {
      await signInWithPopup(auth, googleProvider);
      // checkVerification will be triggered by onAuthStateChanged
    } catch (error) {
      console.error("Login failed", error);
      throw error;
    }
  };

  const logout = async () => {
    try {
      await firebaseSignOut(auth);
      setIsVerified(false);
    } catch (error) {
      console.error("Logout failed", error);
    }
  };

  return (
    <AuthContext.Provider
      value={{ user, loading, isVerified, login, logout, checkVerification }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
