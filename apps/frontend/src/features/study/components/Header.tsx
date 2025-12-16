"use client";

import { useTranslation } from "@/i18n/client";
import LanguageSelector from "./LanguageSelector";
import { useAuth } from "@/context/AuthContext";
import { LogOut, User } from "lucide-react";
import { LANGUAGES } from "@/constants/languages";

export default function Header() {
  const { t, i18n } = useTranslation();
  const { user, login, logout } = useAuth();

  const currentLanguage =
    LANGUAGES.find((l) => l.code === i18n.language)?.id || "english";

  const handleLanguageSwitch = (langId: string) => {
    const lang = LANGUAGES.find((l) => l.id === langId);
    if (lang) {
      i18n.changeLanguage(lang.code);
    }
  };

  return (
    <div className="bg-surface border-b border-border sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-20 flex items-center justify-between">
        <div>
          <div className="text-2xl font-bold text-primary tracking-tight font-heading">
            {t("app.title")}
          </div>
          <div className="text-sm text-text-light font-body">
            {t("app.tagline")}
          </div>
        </div>
        <div className="flex items-center gap-6">
          <LanguageSelector
            currentLanguage={currentLanguage}
            onLanguageSwitch={handleLanguageSwitch}
          />
          {user ? (
            <div className="flex items-center gap-3">
              <div className="hidden sm:flex items-center gap-2 px-3 py-1.5 rounded-full bg-surface-hover border border-border">
                {user.photoURL ? (
                  // eslint-disable-next-line @next/next/no-img-element
                  <img
                    src={user.photoURL}
                    alt="pfp"
                    className="w-6 h-6 rounded-full"
                  />
                ) : (
                  <User className="w-4 h-4 text-text-medium" />
                )}
                <span className="text-sm font-medium text-text-dark">
                  {user.displayName?.split(" ")[0]}
                </span>
              </div>
              <button
                onClick={logout}
                className="p-2 text-text-light hover:text-red-600 transition-colors"
                title="Logout"
              >
                <LogOut className="w-5 h-5" />
              </button>
            </div>
          ) : (
            <button
              onClick={login}
              className="px-4 py-2 bg-primary text-white rounded-lg text-sm font-medium hover:bg-primary/90 transition-colors shadow-sm"
            >
              Login
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
