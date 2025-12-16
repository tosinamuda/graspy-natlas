"use client";

import { ReactNode, useEffect, useState } from "react";
import { I18nextProvider } from "react-i18next";
import { createInstance } from "i18next";
import resourcesToBackend from "i18next-resources-to-backend";
import LanguageDetector from "i18next-browser-languagedetector";
import { initReactI18next } from "react-i18next";
import { getOptions } from "@/i18n/settings";

export default function TranslationsProvider({
  children,
  locale,
}: {
  children: ReactNode;
  locale: string;
}) {
  const [i18nInstance] = useState(() => {
    const instance = createInstance();
    instance
      .use(initReactI18next)
      .use(LanguageDetector)
      .use(
        resourcesToBackend(
          (language: string, namespace: string) =>
            import(`../../public/locales/${language}/${namespace}.json`)
        )
      )
      .init({
        ...getOptions(locale),
        lng: locale,
        detection: {
          order: ["cookie", "localStorage", "navigator"],
          caches: ["cookie", "localStorage"],
        },
        react: {
          useSuspense: false,
        },
      });
    return instance;
  });

  const [isReady, setIsReady] = useState(false);

  useEffect(() => {
    if (i18nInstance.isInitialized) {
      setIsReady(true);
    } else {
      i18nInstance.on("initialized", () => {
        setIsReady(true);
      });
    }
  }, [i18nInstance]);

  if (!isReady) {
    return (
      <div className="flex h-screen items-center justify-center">
        <div className="text-center">
          <div className="w-12 h-12 border-4 border-gray-200 border-t-emerald-700 rounded-full animate-spin mx-auto mb-4"></div>
        </div>
      </div>
    );
  }

  return <I18nextProvider i18n={i18nInstance}>{children}</I18nextProvider>;
}
