import { fetchTopic } from "@/lib/api";
import { notFound } from "next/navigation";
import TopicView from "@/features/study/components/TopicView";

export const dynamic = "force-dynamic";

export default async function TopicPage({
  params,
  searchParams,
}: {
  params: Promise<{ uuid: string; slug: string }>;
  searchParams?: Promise<{ language?: string }>;
}) {
  const { uuid } = await params;
  const { language } = (await searchParams) || {};
  const currentLanguage = language || "english";

  try {
    const topic = await fetchTopic(uuid, currentLanguage);
    if (!topic) {
      notFound();
    }

    return (
      <main>
        <TopicView topic={topic} />
      </main>
    );
  } catch (e) {
    console.error(e);
    notFound();
  }
}
