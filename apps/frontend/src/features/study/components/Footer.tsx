"use client";

import { useTranslation } from "@/i18n/client";
import LanguageSelector from "./LanguageSelector";
import { footerLinks } from "@/features/study/constants";
import { LANGUAGES } from "@/constants/languages";

export default function RenderFooter() {
  const { t, i18n } = useTranslation();
  const currentLanguage =
    LANGUAGES.find((l) => l.code === i18n.language)?.id || "english";

  const handleLanguageSwitch = (langId: string) => {
    const lang = LANGUAGES.find((l) => l.id === langId);
    if (lang) {
      i18n.changeLanguage(lang.code);
    }
  };

  return (
    <footer className="bg-surface border-t border-border mt-auto">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-6 gap-8 mb-12">
          <div className="lg:col-span-2">
            <div className="flex items-center gap-2 mb-4">
              <span className="text-2xl font-bold text-primary tracking-tight font-heading">
                {t("app.title")}
              </span>
            </div>
            <p className="text-text-medium text-sm leading-relaxed max-w-xs mb-6">
              {t("app.tagline")}
            </p>
          </div>

          {footerLinks.map((column) => (
            <div key={column.title} className="lg:col-span-1">
              <h4 className="font-bold text-text-dark mb-4 text-sm font-heading">
                {column.title}
              </h4>
              <ul className="space-y-3">
                {column.links.map((link) => (
                  <li key={link}>
                    <button
                      disabled
                      className="text-sm text-text-light hover:text-primary transition-colors cursor-not-allowed opacity-70"
                    >
                      {link}
                    </button>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>

        <div className="pt-8 border-t border-border flex flex-col md:flex-row items-center justify-between gap-4">
          <div className="text-sm text-text-light">
            &copy; {new Date().getFullYear()} Graspy AI. All rights reserved.
          </div>

          <div className="flex items-center gap-6">
            <LanguageSelector
              currentLanguage={currentLanguage}
              onLanguageSwitch={handleLanguageSwitch}
              direction="up"
            />

            <div className="bg-hover px-3 py-1.5 rounded-md text-sm text-text-medium font-medium border border-border">
              {t("app.poweredBy")}
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
}
