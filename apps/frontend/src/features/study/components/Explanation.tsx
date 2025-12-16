"use client";

import { useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import {
  BookOpen,
  ChevronLeft,
  MessageCircle,
  ThumbsUp,
  ThumbsDown,
  Languages,
} from "lucide-react";
import { useTranslation } from "@/i18n/client";
import { LANGUAGES } from "@/constants/languages";

type ExplanationProps = {
  onBack: () => void;
  handleLanguageSwitch: (langId: string) => void;
  isGenerating: boolean;
  currentExplanation: string | null;
  selectedTopic: string | null;
  language: string;
  onOpenSidebar: () => void;
};

export default function Explanation({
  onBack,
  handleLanguageSwitch,
  isGenerating,
  currentExplanation,
  selectedTopic,
  language,
  onOpenSidebar,
}: ExplanationProps) {
  const { t } = useTranslation();
  const [showLanguages, setShowLanguages] = useState(false);

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <button
        onClick={onBack}
        className="inline-flex items-center gap-2 text-text-medium hover:text-primary mb-6 transition-colors font-medium"
      >
        <ChevronLeft size={20} /> {t("study.back")}
      </button>

      {/* Page Title - Moved Outside */}
      {selectedTopic && (
        <h1 className="text-4xl md:text-5xl font-bold text-text-dark mb-6 capitalize font-heading tracking-tight">
          {selectedTopic}
        </h1>
      )}

      <div className="bg-surface border border-border rounded-xl shadow-sm min-h-[400px] overflow-hidden">
        {/* Language Header */}
        <div className="border-b border-border p-4 bg-surface/50 flex flex-wrap items-center justify-between gap-4">
          <div className="flex items-center gap-2 text-text-medium font-medium">
            <Languages size={18} className="text-primary" />
            <span>{t("study.readIn")}:</span>
          </div>
          <div className="flex flex-wrap gap-2">
            {LANGUAGES.filter((lang) => lang.hasModelSupport).map((lang) => (
              <button
                key={lang.id}
                onClick={() => handleLanguageSwitch(lang.id)}
                disabled={isGenerating}
                className={`px-3 py-1.5 rounded-md text-sm transition-all font-heading ${
                  language === lang.id
                    ? "bg-primary text-white font-bold shadow-sm"
                    : "text-text-medium hover:text-primary hover:bg-hover font-medium"
                } ${isGenerating ? "opacity-50 cursor-not-allowed" : ""}`}
              >
                {lang.label}
              </button>
            ))}
          </div>
        </div>

        <div className="p-8 sm:p-12">
          {isGenerating && !currentExplanation ? (
            <div className="flex flex-col items-center justify-center py-20">
              <div className="w-12 h-12 border-4 border-border border-t-primary rounded-full animate-spin mb-6"></div>
              <p className="text-text-medium font-medium">
                {t("study.generating", {
                  language: LANGUAGES.find((l) => l.id === language)?.label,
                })}
              </p>
            </div>
          ) : (
            <div className="prose prose-lg max-w-none **:font-body **:text-lg prose-headings:font-heading prose-headings:font-bold prose-headings:text-text-dark **:text-text-dark prose-li:marker:text-primary prose-a:text-primary">
              {currentExplanation ? (
                <>
                  <ReactMarkdown remarkPlugins={[remarkGfm]}>
                    {currentExplanation}
                  </ReactMarkdown>

                  <div className="mt-8 pt-6 border-t border-border flex items-center justify-end">
                    <p className="text-text-medium text-sm font-medium">
                      {t("study.helpful")}
                    </p>
                    <div className="flex gap-2">
                      <button className="p-2 rounded-full hover:bg-hover text-text-medium hover:text-primary transition-colors">
                        <ThumbsUp size={18} />
                      </button>
                      <button className="p-2 rounded-full hover:bg-hover text-text-medium hover:text-red-500 transition-colors">
                        <ThumbsDown size={18} />
                      </button>
                    </div>
                  </div>
                </>
              ) : (
                <div className="flex flex-col items-center justify-center py-20 opacity-50">
                  <BookOpen size={48} className="mb-4 text-border" />
                  <p>{t("study.contentPlaceholder")}</p>
                </div>
              )}
            </div>
          )}
        </div>
      </div>

      {/* FAB Chat Button */}
      {!isGenerating && currentExplanation && (
        <button
          onClick={onOpenSidebar}
          disabled={isGenerating || !currentExplanation}
          className="fixed bottom-6 right-6 flex items-center gap-2 px-6 py-3 bg-primary text-white rounded-full font-bold shadow-lg hover:bg-emerald-800 hover:scale-105 transition-all z-50 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <MessageCircle size={24} />
          <span>{t("study.chat")}</span>
        </button>
      )}
    </div>
  );
}
