import type { Metadata } from "next";

import Footer from "@/features/study/components/Footer";

export const metadata: Metadata = {
  title: "Graspy - Learn in Your Language",
  description: "Your AI study companion for Nigerian students.",
};

export default async function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <>
      {children}
      <Footer />
    </>
  );
}
