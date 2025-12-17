import { useEffect } from "react";
import { useQuery, useQueryClient } from "@tanstack/react-query";
import { explainTopic } from "@/lib/api";

interface UseStudyExplainerReturn {
  explanation: string | null;
  isGenerating: boolean;
  error: string | null;
  refetch: () => void;
}

export function useStudyExplainer(
  topic: string | null,
  language: string,
  contextPrompt: string,
  subjectId: string = "general",
  initialData?: string | null // Added
): UseStudyExplainerReturn {
  const {
    data,
    isLoading: isGenerating,
    error: queryError,
    refetch,
  } = useQuery({
    queryKey: ["explanation", topic, language],
    queryFn: async () => {
      if (!topic) return null;
      try {
        return await explainTopic(subjectId, topic, language, contextPrompt);
      } catch (e) {
        throw e;
      }
    },
    enabled: !!topic, // && !!user handled in api call check
    staleTime: Infinity,
    gcTime: 1000 * 60 * 60,
    retry: 1,
    initialData: initialData
      ? { explanation: initialData, session_id: "", slug: "", topic_id: "" }
      : undefined, // Hydrate cache
  });

  return {
    explanation: data?.explanation ?? null,
    isGenerating,
    error: queryError ? (queryError as Error).message : null,
    refetch,
  };
}
