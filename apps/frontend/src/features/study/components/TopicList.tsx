"use client";
import Link from "next/link";
import { ArrowRight, ChevronLeft } from "lucide-react";
import { useTranslation } from "@/i18n/client";

// eslint-disable-next-line @typescript-eslint/no-explicit-any
type Topic = {
  id: string; // This is UUID
  title: string;
  description?: string; // or content excerpt
  slug: string;
};

type Subject = {
  id: string;
  name?: string; // Backend returns name
  title?: string;
  slug: string;
  topics?: Topic[];
};

type TopicListProps = {
  subject: Subject;
};

export default function TopicList({ subject }: TopicListProps) {
  const { t } = useTranslation();
  const topics = subject.topics || [];

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 min-h-[60vh]">
      <Link
        href="/"
        className="inline-flex items-center gap-2 text-text-medium hover:text-primary mb-8 transition-colors font-medium"
      >
        <ChevronLeft size={20} /> {t("study.backToSubjects")}
      </Link>

      <div className="mb-10">
        <h1 className="text-3xl font-bold text-text-dark mb-2 font-heading">
          {t("study.topics", {
            subject: subject.name || subject.title,
          })}
        </h1>
        {topics.length > 0 && (
          <p className="text-text-medium font-body">{t("study.selectTopic")}</p>
        )}
      </div>

      <div className="space-y-4">
        {topics.length > 0 ? (
          topics.map((topic) => (
            <Link
              key={topic.id}
              href={`/topic/${topic.id}/${topic.slug}`}
              className="bg-surface border border-border rounded-lg p-6 cursor-pointer hover:bg-hover hover:border-primary transition-all flex justify-between items-center group"
            >
              <div>
                <h3 className="text-lg font-bold text-text-dark mb-1 group-hover:text-primary">
                  {topic.title}
                </h3>
                <p className="text-text-medium text-sm">
                  {topic.description || "Click to learn more"}
                </p>
              </div>
              <div className="text-text-light group-hover:text-primary group-hover:translate-x-1 transition-all">
                <ArrowRight size={20} />
              </div>
            </Link>
          ))
        ) : (
          <div className="py-20 text-center max-w-lg mx-auto">
            <p className="text-text-medium text-lg font-body mb-6">
              {t("study.noTopics")}
            </p>
            <div className="relative">
              <input
                type="text"
                placeholder={t("home.searchPlaceholder")}
                className="w-full px-6 py-4 rounded-xl border-2 border-border focus:border-primary focus:outline-none text-lg shadow-sm transition-all text-text-dark"
              />
              <button className="absolute right-3 top-3 bg-primary text-white p-2 rounded-lg hover:bg-primary-dark transition-colors">
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
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
