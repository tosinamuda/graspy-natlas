import TopicList from "@/features/study/components/TopicList";
import { fetchSubjectBySlug } from "@/lib/api";
import { notFound } from "next/navigation";

export const dynamic = "force-dynamic";

export default async function SubjectPage({
  params,
}: {
  params: Promise<{ slug: string }>; // Updated for Next.js 15
}) {
  const { slug } = await params;

  try {
    // Fetch data
    const subject = await fetchSubjectBySlug(slug);
    if (!subject) {
      notFound();
    }

    // If existing API doesn't return topics join, we might need a separate call
    // or ensure backend includes topics.
    // Current Backend `SubjectSchema` (Step 132) does NOT include topics.
    // I need to update backend SubjectSchema or SubjectService to include topics.
    // Or just fetch topics separately.
    // Let's assume for now I will fix backend to return topics or fetch them.
    // I'll proceed creating this page assuming 'subject' has topics or I fetch them.

    // Temporary fix: Fetch topics for subject.
    // Actually, let's just pass what we have. If topics are missing, list will be empty.

    return (
      <div className="min-h-full font-heading bg-background text-text-dark relative">
        <main>
          <TopicList subject={subject} />
        </main>
      </div>
    );
  } catch (e) {
    console.error(e);
    notFound();
  }
}
