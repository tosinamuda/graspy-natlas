"use client";

import { useState, useEffect, useCallback } from "react";
import { Mic, MicOff, Volume2, Square } from "lucide-react";

interface AudioControlsProps {
  onTranscript: (text: string) => void;
  textToRead?: string;
  language: string;
  isDark?: boolean;
}

export default function AudioControls({
  onTranscript,
  textToRead,
  language,
  isDark = false,
}: AudioControlsProps) {
  // ... state ...
  // (Assuming state and effects remain same, just updating render)
  // Wait, replace_file_content needs context. I should just update the return statement styles.

  // Let me re-write the component definition start and return block to include `isDark`.
  // Wait, I need to wrap the whole function to inject `isDark`.
  // I will proceed with multi-edit if needed or just replace the component.
  // Actually, I can just replace the definition and the JSX.

  // NOTE: I cannot use `...` to skip code in `replace_file_content` unless I am precise.
  // I will replace lines 6-16 and lines 126-158.

  // Strategy: Update interface and de-structuring first.

  // Then update JSX.

  // I'll do this in two chunks using `multi_replace_file_content`? No, I only have `replace_file_content` available in my thought process?
  // No, I have `multi_replace_file_content`. I will use it.
  const [isListening, setIsListening] = useState(false);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [recognition, setRecognition] = useState<any>(null); // eslint-disable-line @typescript-eslint/no-explicit-any

  // Initialize Speech Recognition
  useEffect(() => {
    if (typeof window !== "undefined") {
      /* eslint-disable @typescript-eslint/no-explicit-any */
      const SpeechRecognition =
        (window as any).SpeechRecognition ||
        (window as any).webkitSpeechRecognition;
      /* eslint-enable @typescript-eslint/no-explicit-any */
      if (SpeechRecognition) {
        const recognitionInstance = new SpeechRecognition();
        recognitionInstance.continuous = false;
        recognitionInstance.interimResults = false;
        // Map language selection to BCP 47 tags roughly
        // Yoraba: yo-NG, Hausa: ha-NG, Pidgin: en-NG (fallback), English: en-US or en-NG
        let langTag = "en-US";
        if (language.toLowerCase() === "yoruba")
          langTag = "yo-NG"; // Chrome supports yo-NG? Maybe not.
        else if (language.toLowerCase() === "hausa") langTag = "ha-NG";
        else if (language.toLowerCase() === "pidgin") langTag = "en-NG";

        // Note: Browser support for African languages is spotty.
        recognitionInstance.lang = langTag;

        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        recognitionInstance.onresult = (event: any) => {
          const transcript = event.results[0][0].transcript;
          onTranscript(transcript);
          setIsListening(false);
        };

        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        recognitionInstance.onerror = (event: any) => {
          console.error("Speech recognition error", event.error);
          setIsListening(false);
        };

        recognitionInstance.onend = () => {
          setIsListening(false);
        };

        setRecognition(recognitionInstance);
      }
    }
  }, [language, onTranscript]);

  const toggleListening = useCallback(() => {
    if (!recognition) {
      alert("Speech recognition not supported in this browser.");
      return;
    }

    if (isListening) {
      recognition.stop();
    } else {
      // Update language before starting
      let langTag = "en-US";
      if (language.toLowerCase() === "yoruba") langTag = "yo-NG";
      else if (language.toLowerCase() === "hausa") langTag = "ha-NG";
      else if (language.toLowerCase() === "pidgin") langTag = "en-NG";
      recognition.lang = langTag;

      try {
        recognition.start();
        setIsListening(true);
      } catch (e) {
        console.error("Error starting recognition:", e);
      }
    }
  }, [isListening, recognition, language]);

  const toggleSpeaking = useCallback(() => {
    if (!textToRead) return;

    if (isSpeaking) {
      window.speechSynthesis.cancel();
      setIsSpeaking(false);
    } else {
      const utterance = new SpeechSynthesisUtterance(textToRead);
      // Attempt to set voice/lang
      // Voices are loaded async, ideally we wait or pick best match.
      // For now just set lang.
      let langTag = "en-US";
      if (language.toLowerCase() === "yoruba") langTag = "yo-NG";
      else if (language.toLowerCase() === "hausa") langTag = "ha-NG";
      // Pidgin isn't usually a standard TTS voice, fallback to EN-NG or EN-US
      else if (language.toLowerCase() === "pidgin") langTag = "en-NG";

      utterance.lang = langTag;

      utterance.onend = () => setIsSpeaking(false);
      utterance.onerror = () => setIsSpeaking(false);

      window.speechSynthesis.speak(utterance);
      setIsSpeaking(true);
    }
  }, [textToRead, isSpeaking, language]);

  // Cancel speech on unmount
  useEffect(() => {
    return () => {
      window.speechSynthesis.cancel();
    };
  }, []);

  return (
    <div className="flex gap-2">
      <button
        type="button"
        onClick={toggleListening}
        className={`p-2 rounded-full transition-colors ${
          isListening
            ? "bg-red-500/10 text-red-500 animate-pulse border border-red-500/20"
            : isDark
            ? "bg-zinc-800 text-zinc-400 hover:text-white hover:bg-zinc-700 border border-white/5"
            : "bg-slate-100 text-slate-600 hover:bg-slate-200"
        }`}
        title="Voice Input"
      >
        {isListening ? <MicOff size={20} /> : <Mic size={20} />}
      </button>

      {textToRead && (
        <button
          type="button"
          onClick={toggleSpeaking}
          className={`p-2 rounded-full transition-colors ${
            isSpeaking
              ? "bg-sky-500/10 text-sky-500 border border-sky-500/20"
              : isDark
              ? "bg-zinc-800 text-zinc-400 hover:text-white hover:bg-zinc-700 border border-white/5"
              : "bg-slate-100 text-slate-600 hover:bg-slate-200"
          }`}
          title="Read Aloud"
        >
          {isSpeaking ? (
            <Square size={20} fill="currentColor" />
          ) : (
            <Volume2 size={20} />
          )}
        </button>
      )}
    </div>
  );
}
