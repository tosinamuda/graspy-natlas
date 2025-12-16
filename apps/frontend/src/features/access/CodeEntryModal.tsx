"use client";

import React, { useState } from "react";
// import { useAccess } from "@/context/AccessContext"; // Deprecated
import { useAuth } from "@/context/AuthContext";
import { verifyAccessCode } from "@/lib/api";
import { Lock, ArrowRight, AlertCircle, Loader2 } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import { useTranslation } from "react-i18next";

export const CodeEntryModal: React.FC = () => {
  const { isVerified, user, checkVerification } = useAuth();
  const [code, setCode] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");
  const { t } = useTranslation();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!code.trim()) return;

    setIsLoading(true);
    setError("");

    try {
      await verifyAccessCode(code.trim());
      await checkVerification(); // Update global auth state
    } catch (err) {
      setError(t("access.error") || "Invalid code");
    } finally {
      setIsLoading(false);
    }
  };

  // Only show if user is logged in BUT not verified
  if (!user || isVerified) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm p-4">
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        className="w-full max-w-md bg-[#0F0F12] border border-[#27272A] rounded-2xl shadow-2xl overflow-hidden"
      >
        <div className="p-8 space-y-6">
          <div className="text-center space-y-2">
            <div className="mx-auto w-12 h-12 bg-[#27272A] rounded-xl flex items-center justify-center mb-4">
              <Lock className="w-6 h-6 text-white" />
            </div>
            <h2 className="text-2xl font-bold text-white tracking-tight">
              {t("access.title")}
            </h2>
            <p className="text-[#A1A1AA] text-sm">{t("access.description")}</p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="space-y-2">
              <input
                type="text"
                placeholder={t("access.placeholder")}
                value={code}
                onChange={(e) => setCode(e.target.value)}
                className="w-full bg-[#18181B] border border-[#27272A] text-white px-4 py-3 rounded-xl focus:outline-none focus:ring-2 focus:ring-[#3B82F6] focus:border-transparent transition-all placeholder:text-[#52525B]"
                autoFocus
              />
              {error && (
                <div className="flex items-center gap-2 text-red-500 text-xs">
                  <AlertCircle className="w-3 h-3" />
                  <span>{error}</span>
                </div>
              )}
            </div>

            <button
              type="submit"
              disabled={isLoading || !code.trim()}
              className="w-full bg-white text-black font-medium py-3 rounded-xl hover:bg-gray-100 transition-colors flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isLoading ? (
                <Loader2 className="w-4 h-4 animate-spin" />
              ) : (
                <>
                  {t("access.button")}
                  <ArrowRight className="w-4 h-4" />
                </>
              )}
            </button>
          </form>

          <div className="text-center">
            <p className="text-[10px] text-[#52525B] uppercase tracking-wider font-medium">
              {t("access.footer")}
            </p>
          </div>
        </div>
      </motion.div>
    </div>
  );
};
