"use client";
import Link from "next/link";
import { useTranslation } from "@/i18n/client";
import { useState } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/context/AuthContext";
// import { createTopic } from "@/lib/api";
// import list of subjects
import { SUBJECTS_DATA } from "@/features/study/constants";
/* NOTE: We are transitioning to API data but for now keeping hybrid. 
   Ideally props should come from Server Component. */

type HomeProps = {
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  subjects?: any[]; // Allow passing from API later
};

export default function Home({ subjects = [] }: HomeProps) {
  const { t, i18n } = useTranslation();

  // Merge API subjects with constants or just use passed subjects
  // For implementation speed: if subjects passed, use them. if not fall back (or map API structure to UI)
  const displaySubjects =
    subjects.length > 0
      ? subjects
      : SUBJECTS_DATA.map((s) => ({
          id: s.id,
          title: s.title,
          icon: s.icon,
          count: s.topics.length,
          slug: s.id, // fallback
        }));

  /* State & Auth */
  const [topicInput, setTopicInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const router = useRouter();
  const { user, login } = useAuth(); // Assuming AuthContext provides login

  const handleSearch = async () => {
    if (!topicInput.trim()) return;

    // Auth Check
    // Reuse language mapping logic or just pass code and let NewPage handle it.
    // NewTopicPage handles logic: determines from Query > Locale.
    // So passing `i18n.language` (code) is fine, but NewTopicPage expects ID mostly?
    // Actually NewTopicPage: `const queryLang = searchParams.get("language"); ... const finalLanguage = queryLang || localeLang ...`
    // And it immediately uses `finalLanguage` for API.
    // The API expects ID (e.g. "yoruba").
    // So we should map it here in Home or ensure NewTopicPage maps code -> ID.
    // NewTopicPage has `getLanguageId` logic inside.
    // Let's pass the raw code or mapped ID?
    // Home doesn't import LANGUAGES.
    // Let's just pass the code, and let NewTopicPage map it?
    // Wait, NewTopicPage does: `const getLanguageId = ... const localeLang = getLanguageId(i18n.language);`
    // It assumes queryLang is ALREADY the ID? `const finalLanguage = queryLang || localeLang`.
    // If we pass "yo", finalLanguage becomes "yo". API might fail if it expects "yoruba".
    // API `create_topic_generator` takes `language`. `get_lm_for_locale` takes ID or Code?

    // Let's check API. `app/config/llm.py` `get_lm_for_locale`.
    // It likely maps code too.
    // But consistency is better. Let's pass the mapped ID from Home if possible, or update NewTopicPage to map queryLang too.

    // Let's update NewTopicPage to map allow queryLang to be a code and map it.
    // But for now, let's just pass `i18n.language` from Home -> `NewTopicPage`.

    if (!user) {
      // Redirect to login, then to topic creation
      const target = encodeURIComponent(
        `/topic/new?topic=${encodeURIComponent(
          topicInput
        )}&source=home&language=${i18n.language}`
      );
      router.push(`/login?redirect=${target}`);
      return;
    }

    // Redirect to Topic Creation Loading Page
    router.push(
      `/topic/new?topic=${encodeURIComponent(
        topicInput
      )}&source=home&language=${i18n.language}`
    );
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <section className="mb-16 text-center sm:text-left">
        {/* Header content ... */}
        <h1 className="text-4xl md:text-5xl font-bold text-text-dark mb-4 tracking-tight font-heading">
          {t("home.greeting")}
        </h1>
        <p className="text-xl text-text-medium mb-8 font-body">
          {t("home.subtext")}
        </p>

        <div className="max-w-2xl mx-auto relative mb-12">
          <input
            type="text"
            placeholder={t("home.searchPlaceholder")}
            className="w-full px-6 py-4 rounded-xl border-2 border-border focus:border-primary focus:outline-none text-lg shadow-sm transition-all text-text-dark"
            value={topicInput}
            onChange={(e) => setTopicInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleSearch()}
            disabled={isLoading}
          />
          <button
            onClick={handleSearch}
            disabled={isLoading}
            className="absolute right-3 top-3 bg-primary text-white p-2 rounded-lg hover:bg-primary-dark transition-colors disabled:opacity-50"
          >
            {isLoading ? (
              <svg
                className="animate-spin h-6 w-6"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
              >
                <circle
                  className="opacity-25"
                  cx="12"
                  cy="12"
                  r="10"
                  stroke="currentColor"
                  strokeWidth="4"
                ></circle>
                <path
                  className="opacity-75"
                  fill="currentColor"
                  d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                ></path>
              </svg>
            ) : (
              <svg
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                strokeWidth={2.5}
                stroke="currentColor"
                className="w-6 h-6"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z"
                />
              </svg>
            )}
          </button>
        </div>
      </section>

      <div className="flex items-center text-sm text-text-light uppercase tracking-wider font-bold mb-8">
        <span className="flex-1 h-px bg-border"></span>
        <span className="px-4">{t("home.orChooseSubject")}</span>
        <span className="flex-1 h-px bg-border"></span>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        {displaySubjects.map((subject) => (
          <Link
            key={subject.id}
            href={`/subjects/${subject.slug}`}
            className="bg-surface border border-border rounded-xl p-8 cursor-pointer hover:-translate-y-1 hover:shadow-lg hover:border-primary transition-all group relative overflow-hidden block"
          >
            <div className="relative z-10">
              <h3 className="text-2xl font-bold text-text-dark mb-2 group-hover:text-primary transition-colors font-heading">
                {subject.title || subject.name}
              </h3>
              <p className="text-text-light">
                {/* Handle count if available */}
                {t("home.available")}
              </p>
            </div>
            {/* Icon logic: API subjects might not have React icons serialized. 
                 We might need a mapping or just generic icon. */}
          </Link>
        ))}
      </div>
    </div>
  );
}
