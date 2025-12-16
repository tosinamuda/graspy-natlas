import type { Metadata } from "next";
import { Crimson_Pro, Plus_Jakarta_Sans } from "next/font/google";
import { headers } from "next/headers";
import "./globals.css";
import TranslationsProvider from "@/context/TranslationsProvider";
import { fallbackLng, headerName } from "@/i18n/settings";
import { CodeEntryModal } from "@/features/access/CodeEntryModal";
import QueryProvider from "@/context/QueryProvider";
import GoogleAnalytics from "@/components/GoogleAnalytics";
import { AuthProvider } from "@/context/AuthContext";
import Header from "@/features/study/components/Header";
import Footer from "@/features/study/components/Footer";

const plusJakartaSans = Plus_Jakarta_Sans({
  subsets: ["latin"],
  variable: "--font-heading",
});

const crimsonPro = Crimson_Pro({
  subsets: ["latin"],
  variable: "--font-body",
});

export const metadata: Metadata = {
  title: "Graspy - Learn in Your Language",
  description: "Your AI study companion for Nigerian students.",
};

export default async function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  const headersList = await headers();
  const locale = headersList.get(headerName) || fallbackLng;

  return (
    <html lang={locale}>
      <body
        className={`${plusJakartaSans.variable} ${crimsonPro.variable} font-body antialiased bg-stone-50 text-stone-900`}
      >
        <GoogleAnalytics />
        <QueryProvider>
          <TranslationsProvider locale={locale}>
            <AuthProvider>
              <CodeEntryModal />
              <Header />
              {children}
            </AuthProvider>
          </TranslationsProvider>
        </QueryProvider>
      </body>
    </html>
  );
}
