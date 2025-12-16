import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";
import acceptLanguage from "accept-language";
import { fallbackLng, languages } from "./i18n/settings";

acceptLanguage.languages(languages);

const cookieName = "i18next";

export function middleware(req: NextRequest) {
  let lng: string | undefined | null;

  // Check cookie first
  if (req.cookies.has(cookieName)) {
    lng = req.cookies.get(cookieName)?.value;
  }

  // If no cookie, check Accept-Language header
  if (!lng) {
    lng = acceptLanguage.get(req.headers.get("Accept-Language"));
  }

  // Fallback to default language
  if (!lng) {
    lng = fallbackLng;
  }

  // Clone the response
  const response = NextResponse.next();

  // Set the language in a custom header so server components can access it
  response.headers.set("x-locale", lng);

  return response;
}

export const config = {
  matcher: [
    /*
     * Match all request paths except for the ones starting with:
     * - api (API routes)
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     * - public folder
     */
    "/((?!api|_next/static|_next/image|favicon.ico|locales).*)",
  ],
};
