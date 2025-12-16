import { useState, useCallback, useEffect } from "react";
// import { useAccess } from "@/context/AccessContext";

export type Message = {
  role: "user" | "assistant";
  content: string;
};

interface UseSidebarChatReturn {
  messages: Message[];
  isGenerating: boolean;
  setMessages: React.Dispatch<React.SetStateAction<Message[]>>;
  sendMessage: (content: string, language: string) => Promise<void>;
  clearMessages: () => void;
}

import { startChatSession, sendChatMessage } from "@/lib/api";

export function useSidebarChat(
  apiUrl?: string,
  initialContext?: string | null,
  topicName?: string | null,
  topicId?: string | null,
  initialUserMessage?: string | null
): UseSidebarChatReturn {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isGenerating, setIsGenerating] = useState(false);
  const [sessionId, setSessionId] = useState<string | null>(null);

  // const { sessionId, setSessionId } = useAccess(); // REMOVED: AccessProvider deprecated

  // Seed messages if initialContext is provided and messages are empty
  useEffect(() => {
    if (messages.length === 0 && initialContext && topicName) {
      setMessages([
        { role: "user", content: initialUserMessage || `Explain ${topicName}` },
        { role: "assistant", content: initialContext },
      ]);
    }
  }, [initialContext, topicName, messages.length]);

  const sendMessage = useCallback(
    async (content: string, language: string = "english") => {
      // Optimistically add user message
      const userMsg: Message = { role: "user", content };
      setMessages((prev) => [...prev, userMsg]);
      setIsGenerating(true);

      try {
        let currentSessionId = sessionId;

        if (!currentSessionId && topicId) {
          // Start new session
          const session = await startChatSession(
            topicId,
            topicName || undefined,
            initialContext || undefined
          );
          currentSessionId = session.session_id;
          setSessionId(session.session_id);
        }

        if (!currentSessionId) {
          throw new Error("No session ID and no Topic ID to start one.");
        }

        const data = await sendChatMessage(currentSessionId, content, language);

        const aiMsg: Message = { role: "assistant", content: data.answer };
        setMessages((prev) => [...prev, aiMsg]);
      } catch (error) {
        console.error("Error sending message:", error);
        // Optionally add an error message to the chat
      } finally {
        setIsGenerating(false);
      }
    },
    [sessionId, topicId, setSessionId]
  );

  const clearMessages = useCallback(() => {
    setMessages([]);
  }, []);

  return {
    messages,
    isGenerating,
    setMessages,
    sendMessage,
    clearMessages,
  };
}
