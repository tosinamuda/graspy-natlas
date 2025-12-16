"use client";

import { useState, useRef, useEffect } from "react";
import { ChevronDown, Globe } from "lucide-react";

import { LANGUAGES } from "@/constants/languages";

export default function LanguageSelector({
  currentLanguage,
  onLanguageSwitch,
  direction = "down",
}: {
  currentLanguage: string;
  onLanguageSwitch: (langId: string) => void;
  direction?: "up" | "down";
}) {
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (
        dropdownRef.current &&
        !dropdownRef.current.contains(event.target as Node)
      ) {
        setIsOpen(false);
      }
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, []);

  const currentLangLabel = LANGUAGES.find(
    (l) => l.id === currentLanguage
  )?.label;

  return (
    <div className="relative" ref={dropdownRef}>
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center gap-2 text-text-dark hover:text-primary transition-colors font-heading text-sm font-medium"
      >
        <Globe size={18} className="text-text-medium" />
        {currentLangLabel}
        <ChevronDown
          size={14}
          className={`text-text-medium transition-transform ${
            isOpen ? "rotate-180" : ""
          }`}
        />
      </button>

      {isOpen && (
        <div
          className={`absolute right-0 ${
            direction === "up" ? "bottom-full mb-2" : "top-full mt-2"
          } w-48 bg-surface rounded-xl shadow-lg border border-border py-1 overflow-hidden z-50`}
        >
          {LANGUAGES.map((lang) => (
            <button
              key={lang.id}
              onClick={() => {
                onLanguageSwitch(lang.id);
                setIsOpen(false);
              }}
              className={`w-full text-left px-4 py-2.5 text-sm hover:bg-hover transition-colors font-heading flex items-center gap-2 ${
                currentLanguage === lang.id
                  ? "text-primary font-bold bg-primary/5"
                  : "text-text-dark"
              }`}
            >
              {lang.label}
            </button>
          ))}
        </div>
      )}
    </div>
  );
}
