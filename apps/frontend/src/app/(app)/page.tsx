import Home from "@/features/study/components/Home";
import { fetchSubjects } from "@/lib/api";

export const dynamic = "force-dynamic";

export default async function Page() {
  let subjects = [];
  try {
    // First try fetching real data from API
    subjects = await fetchSubjects(true); // Get featured subjects
  } catch (e) {
    console.warn(
      "Failed to fetch subjects from API, falling back to static data",
      e
    );
    // Fallback is handled inside Home component if array is empty or undefined
  }

  return (
    <div className="min-h-full font-heading bg-background text-text-dark relative">
      <main>
        <Home subjects={subjects} />
      </main>
    </div>
  );
}
