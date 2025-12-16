import { useEffect } from "react";
import { useQuery, useQueryClient } from "@tanstack/react-query";
import { explainTopic } from "@/lib/api";
// import { useAccess } from "@/context/AccessContext";

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
  // const { setSessionId } = useAccess(); // REMOVED: AccessProvider deprecated

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
        // TODO: subject_id is needed in explainTopic.
        // useStudyExplainer needs to accept subject_id or optional.
        // For now passing "general" or "unknown" and letting backend handle or passed via props?
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

  // Side Effect: Update Session ID when fresh data arrives
  // Side Effect: Update Session ID when fresh data arrives
  // useEffect(() => {
  //   if (data?.session_id) {
  //     setSessionId(data.session_id);
  //   }
  // }, [data?.session_id, setSessionId]);

  return {
    explanation: data?.explanation ?? null,
    isGenerating,
    error: queryError ? (queryError as Error).message : null,
    refetch,
  };
}
