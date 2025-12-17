"use client";

import { useEffect, useState, useRef } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { useAuth } from "@/context/AuthContext";
import { useTranslation } from "@/i18n/client";
import { AlertCircle } from "lucide-react";
import Explanation from "@/features/study/components/Explanation";

export default function NewTopicPage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const { user, isVerified, loading: authLoading } = useAuth();
  const { t, i18n } = useTranslation();

  const topicQuery = searchParams.get("topic");

  // Determine language: Query Param > Client Locale > Default
  const queryLang = searchParams.get("language") || searchParams.get("lang");

  // Helper to map code/ID
  const getLanguageId = (codeOrId: string | null) => {
    if (!codeOrId) return "english";
    const lower = codeOrId.toLowerCase();
    if (lower.startsWith("yo")) return "yoruba";
    if (lower.startsWith("ha")) return "hausa";
    if (lower.startsWith("ig")) return "igbo";
    if (lower.startsWith("pcm")) return "pidgin";
    // Fallback: check against known codes if needed, or default
    return "english";
  };

  const uiLanguage = getLanguageId(queryLang || i18n.language);
  const [error, setError] = useState<string | null>(null);
  const [isCreating, setIsCreating] = useState(false);

  const [streamedContent, setStreamedContent] = useState<string | null>(null);

  // Use a ref to prevent double-firing in React Strict Mode
  const hasAttemptedRef = useRef(false);

  useEffect(() => {
    // Wait for auth to load
    if (authLoading) return;

    // If not logged in, redirect to login with return url
    if (!user) {
      const returnUrl = encodeURIComponent(
        `/topic/new?topic=${topicQuery || ""}`
      );
      router.push(`/login?redirect=${returnUrl}`);
      return;
    }

    // If no topic query, go back home
    if (!topicQuery) {
      router.push("/");
      return;
    }

    // If already attempting or attempted, skip
    if (isCreating || hasAttemptedRef.current) return;

    // Start creation with SSE
    const initCreation = async () => {
      hasAttemptedRef.current = true;
      setIsCreating(true);
      setError(null);

      try {
        const token = await user.getIdToken();
        const finalLanguage = uiLanguage; // Usage of calculated UI language

        const url = `${
          process.env.NEXT_PUBLIC_API_URL || ""
        }/api/study/topics/stream?topic=${encodeURIComponent(
          topicQuery
        )}&language=${encodeURIComponent(finalLanguage)}`;

        // Import dynamically to avoid SSR issues if any, though standard import is fine
        const { createSSEStream } = await import("@/lib/sse");

        let finalId = "";
        let finalSlug = "";

        for await (const chunk of createSSEStream<any>({
          url,
          headers: { Authorization: `Bearer ${token}` },
        })) {
          if (chunk.error) {
            throw new Error(chunk.error);
          }

          if (chunk.is_existing) {
            // Topic exists, set data immediately then replace
            setStreamedContent(chunk.content);
            const source = searchParams.get("source");
            const sourceParam = source
              ? `&source=${encodeURIComponent(source)}`
              : "";

            router.replace(
              `/topic/${chunk.id}/${chunk.slug}?language=${encodeURIComponent(
                finalLanguage
              )}${sourceParam}`
            );
            return;
          }

          if (chunk.id) finalId = chunk.id;
          if (chunk.slug) finalSlug = chunk.slug;

          // Update content if available (Chunk 2)
          if (chunk.content) {
            setStreamedContent(chunk.content);
          }

          if (chunk.is_complete) {
            // Generation finished.
            if (finalId && finalSlug) {
              const source = searchParams.get("source");
              const sourceParam = source
                ? `&source=${encodeURIComponent(source)}`
                : "";

              router.replace(
                `/topic/${finalId}/${finalSlug}?language=${encodeURIComponent(
                  finalLanguage
                )}${sourceParam}`
              );
            }
            return;
          }
        }
      } catch (err: any) {
        console.error("Creation failed", err);
        setError(err.message || "Failed to create topic");
        setIsCreating(false);
        hasAttemptedRef.current = false; // Allow retry
      }
    };

    initCreation();
  }, [
    user,
    authLoading,
    topicQuery,
    router,
    isCreating,
    uiLanguage,
    i18n.language,
  ]);

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-stone-50 p-4">
        <div className="max-w-md w-full bg-white rounded-2xl p-8 text-center shadow-lg border border-red-100">
          <div className="mx-auto w-12 h-12 bg-red-50 rounded-full flex items-center justify-center mb-4">
            <AlertCircle className="w-6 h-6 text-red-500" />
          </div>
          <h2 className="text-xl font-bold text-stone-900 mb-2">
            Something went wrong
          </h2>
          <p className="text-stone-500 mb-6">{error}</p>
          <div className="flex gap-3 justify-center">
            <button
              onClick={() => router.push("/")}
              className="px-4 py-2 rounded-lg border border-stone-200 hover:bg-stone-50 transition-colors"
            >
              Go Home
            </button>
            <button
              onClick={() => window.location.reload()}
              className="px-4 py-2 rounded-lg bg-primary text-white hover:bg-primary-dark transition-colors"
            >
              Try Again
            </button>
          </div>
        </div>
      </div>
    );
  }

  // Use Explanation component in loading state
  return (
    <div className="min-h-full font-heading bg-background text-text-dark relative pb-20">
      <Explanation
        onBack={() => router.push("/")}
        handleLanguageSwitch={() => {}} // Disabled during generation
        isGenerating={true}
        currentExplanation={null} // Shows loading placeholder
        selectedTopic={topicQuery}
        language={uiLanguage} // Usage of calculated UI language
        onOpenSidebar={() => {}} // Disabled
      />
    </div>
  );
}
