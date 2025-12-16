import { useState, useEffect, useRef } from "react";
import { Send, X, Bot, ChevronDown, ChevronUp } from "lucide-react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { useTranslation, Trans } from "react-i18next";
import { useSidebarChat } from "@/features/study/hooks/useSidebarChat";
import { env } from "@/env.client";
import { LANGUAGES } from "@/constants/languages";

interface ChatSidebarProps {
  isOpen: boolean;
  onClose: () => void;
  topicName: string | null;
  topicId: string | null;
  language: string;
  context: string | null; // The explanation content to seed context if needed
}

// Internal Collapsible Message Component
const CollapsibleMessage = ({ content }: { content: string }) => {
  const [isExpanded, setIsExpanded] = useState(false);
  const maxLength = 300; // Character limit for collapsed state
  const shouldCollapse = content.length > maxLength;

  const displayContent =
    shouldCollapse && !isExpanded
      ? content.slice(0, maxLength) + "..."
      : content;

  return (
    <div>
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        className="prose prose-sm max-w-none prose-p:my-1 prose-headings:my-2 prose-ul:my-1 text-inherit dark:prose-invert prose-headings:text-text-dark prose-strong:text-text-dark prose-em:text-text-dark prose-li:text-text-dark"
      >
        {displayContent}
      </ReactMarkdown>
      {shouldCollapse && (
        <button
          onClick={() => setIsExpanded(!isExpanded)}
          className="text-xs font-bold text-primary mt-2 flex items-center gap-1 hover:underline"
        >
          {isExpanded ? (
            <>
              Show Less <ChevronUp size={12} />
            </>
          ) : (
            <>
              Read More <ChevronDown size={12} />
            </>
          )}
        </button>
      )}
    </div>
  );
};

export default function ChatSidebar({
  isOpen,
  onClose,
  topicName,
  topicId,
  language,
  context,
}: ChatSidebarProps) {
  const { t } = useTranslation();

  const initialUserMessage = topicName
    ? t("sidebar.initialPrompt", { topic: topicName })
    : null;

  // Pass context as initialContext and topic for seeding
  const { messages, isGenerating, sendMessage } = useSidebarChat(
    env.NEXT_PUBLIC_API_URL,
    context,
    topicName,
    topicId,
    initialUserMessage
  );
  const [input, setInput] = useState("");
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isOpen]);

  const handleSend = async (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    if (!input.trim() || isGenerating) return;

    const msg = input;
    setInput("");
    await sendMessage(msg, language);
  };

  const languageLabel =
    LANGUAGES.find((l) => l.id === language)?.label || language;

  if (!isOpen) return null;

  return (
    <div className="fixed inset-y-0 right-0 w-full sm:w-[400px] bg-white shadow-2xl z-50 flex flex-col transform transition-transform border-l border-border">
      {/* Header */}
      <div className="bg-primary p-4 flex items-center justify-between text-white">
        <div>
          <h3 className="font-bold font-heading text-lg">
            {t("sidebar.headerTitle")}
          </h3>
          <p className="text-xs opacity-90">
            {topicName
              ? t("sidebar.askAbout", { topic: topicName })
              : t("sidebar.askAboutAnything")}
          </p>
        </div>
        <button
          onClick={onClose}
          className="p-1 hover:bg-white/20 rounded-full transition-colors"
        >
          <X size={20} />
        </button>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-stone-50">
        {messages.length === 0 && (
          <div className="text-center text-text-medium py-10 px-4">
            <div className="bg-white p-4 rounded-xl border border-border shadow-sm inline-block mb-4">
              <Bot size={32} className="text-primary mx-auto" />
            </div>
            <p className="font-medium mb-2">{t("sidebar.greeting")}</p>
            <p className="text-sm">
              <Trans
                i18nKey="sidebar.helpText"
                values={{
                  topic: topicName || "anything",
                  language: languageLabel,
                }}
                components={{ strong: <strong /> }}
              />
            </p>
          </div>
        )}

        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={`flex ${
              msg.role === "user" ? "justify-end" : "justify-start"
            }`}
          >
            <div
              className={`max-w-[85%] p-3 rounded-2xl text-sm ${
                msg.role === "user"
                  ? "bg-primary text-white rounded-br-none"
                  : "bg-white text-text-dark border border-border rounded-bl-none shadow-sm"
              }`}
            >
              <CollapsibleMessage content={msg.content} />
            </div>
          </div>
        ))}
        {isGenerating && (
          <div className="flex justify-start">
            <div className="bg-white border border-border p-3 rounded-2xl rounded-bl-none shadow-sm flex items-center gap-2">
              <div className="w-2 h-2 bg-primary rounded-full animate-bounce" />
              <div className="w-2 h-2 bg-primary rounded-full animate-bounce delay-75" />
              <div className="w-2 h-2 bg-primary rounded-full animate-bounce delay-150" />
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <form
        onSubmit={handleSend}
        className="p-4 bg-white border-t border-border"
      >
        <div className="relative">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder={t("sidebar.inputPlaceholder")}
            className="w-full pl-4 pr-12 py-3 bg-stone-50 border border-border rounded-full focus:outline-none focus:border-primary focus:ring-1 focus:ring-primary font-body text-sm"
          />
          <button
            type="submit"
            disabled={!input.trim() || isGenerating}
            className="absolute right-2 top-2 p-1.5 bg-primary text-white rounded-full hover:bg-emerald-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <Send size={16} />
          </button>
        </div>
      </form>
    </div>
  );
}
