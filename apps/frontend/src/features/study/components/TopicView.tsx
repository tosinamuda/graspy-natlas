"use client";

import { useState, useEffect } from "react";
import { useTranslation } from "@/i18n/client";
import { useStudyExplainer } from "../hooks/useStudyExplainer";
import ChatSidebar from "./ChatSidebar";
import { LANGUAGES } from "@/constants/languages";
import Explanation from "./Explanation";
import Link from "next/link";
import { ChevronLeft } from "lucide-react";
// Add imports for useRouter and useAuth
import { useRouter } from "next/navigation";
import { useAuth } from "@/context/AuthContext";
type Topic = {
  id: string;
  title: string;
  slug: string;
  content: string;
  subject_id: string;
  is_featured?: boolean;
  language?: string; // Added from backend
};

type TopicViewProps = {
  topic: Topic;
};

export default function TopicView({ topic }: TopicViewProps) {
  const { t, i18n } = useTranslation();
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const router = useRouter(); // Need router for redirect
  const { user } = useAuth(); // Need user status

  const searchParams =
    typeof window !== "undefined"
      ? new URLSearchParams(window.location.search)
      : null;
  const urlLang = searchParams?.get("language");

  // Helper to map i18n code (e.g. 'yo') to our internal ID (e.g. 'yoruba')
  const getLanguageIdFromCode = (code: string) => {
    const lang = LANGUAGES.find((l) => l.code === code);
    return lang ? lang.id : "english";
  };

  const initialLang =
    urlLang ||
    (topic.language && topic.language !== "english"
      ? topic.language
      : getLanguageIdFromCode(i18n.language));

  const [studyLanguage, setStudyLanguage] = useState(initialLang);

  // Sync study language with global language when it changes IF NOT OVERRIDDEN by URL
  useEffect(() => {
    if (!urlLang) {
      setStudyLanguage(getLanguageIdFromCode(i18n.language));
    }
  }, [i18n.language, urlLang]);

  const handleStudyLanguageSwitch = (langId: string) => {
    setStudyLanguage(langId);
  };

  const EXPLANATION_CONTEXT =
    "Do not include the topic title as a heading. Start directly with the definition or explanation. Structure the response clearly with headings for 'What is it?', 'Key Concepts', 'Common Misconceptions', and 'Exam Notes (JAMB/WAEC)'.";

  const { explanation, isGenerating, error } = useStudyExplainer(
    topic.title,
    studyLanguage,
    EXPLANATION_CONTEXT,
    topic.subject_id,
    // Pass initial content only if it matches language
    // We must compare IDs. studyLanguage might be 'yo' (code) or 'yoruba' (ID) depending on state initialization.
    // Actually `studyLanguage` state is initialized via `getLanguageIdFromCode` (which returns ID "yoruba").
    // Wait, the log said "studyLanguage: yo".
    // Check `useState` init logic:
    // `const initialLang = urlLang || ... getLanguageIdFromCode(i18n.language)`
    // If `urlLang` was "yo" (from query param), then `initialLang` is "yo".
    // We should normalize `urlLang` to ID in `TopicView` too!

    // Let's normalize comparison here:
    topic.language === studyLanguage ||
      topic.language === getLanguageIdFromCode(studyLanguage) ||
      (!topic.language &&
        (studyLanguage === "english" || studyLanguage === "en"))
      ? topic.content
      : null
  );

  // Auth Redirect Effect
  useEffect(() => {
    if (error && error.includes("Authentication") && !user) {
      // Save current URL as redirect
      const currentPath = window.location.pathname + window.location.search;
      // Append the language param if missing from current search (since state updated)
      const targetUrl = currentPath.includes("language=")
        ? currentPath
        : `${currentPath}?language=${studyLanguage}`;

      router.push(`/login?redirect=${encodeURIComponent(targetUrl)}`);
    }
  }, [error, user, router, studyLanguage]);

  // Logic: Use `explanation` (fresh fetch) if available.
  // Fallback to `topic.content` ONLY IF `topic.language` matches target `studyLanguage`.
  // If `topic.language` is missing (legacy), assume 'english'.
  const topicLang = topic.language || "english";
  const contentIsRelevant =
    topicLang.toLowerCase() === studyLanguage.toLowerCase();

  const displayedContent =
    explanation || (contentIsRelevant ? topic.content : null);

  return (
    <div className="min-h-full font-heading bg-background text-text-dark relative pb-20">
      <Explanation
        onBack={() => {
          const source = searchParams?.get("source");
          if (source === "home") {
            router.push("/");
          } else {
            window.history.back();
          }
        }}
        handleLanguageSwitch={handleStudyLanguageSwitch}
        isGenerating={isGenerating && !displayedContent}
        currentExplanation={displayedContent}
        selectedTopic={topic.title}
        language={studyLanguage}
        onOpenSidebar={() => setIsSidebarOpen(true)}
      />

      <ChatSidebar
        isOpen={isSidebarOpen}
        onClose={() => setIsSidebarOpen(false)}
        topicName={topic.title}
        topicId={topic.id}
        language={studyLanguage}
        context={displayedContent}
      />
    </div>
  );
}
