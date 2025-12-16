import { env } from "@/env.client";

declare global {
  interface Window {
    gtag: (...args: any[]) => void;
  }
}

export const GA_TRACKING_ID = env.NEXT_PUBLIC_GA_MEASUREMENT_ID;

// https://developers.google.com/analytics/devguides/collection/gtagjs/pages
export const pageview = (url: string) => {
  if (
    typeof window !== "undefined" &&
    window.gtag &&
    GA_TRACKING_ID &&
    env.NEXT_PUBLIC_ENABLE_GA
  ) {
    window.gtag("config", GA_TRACKING_ID, {
      page_path: url,
    });
  }
};

// https://developers.google.com/analytics/devguides/collection/gtagjs/events
export const event = ({
  action,
  category,
  label,
  value,
  params,
}: {
  action: string;
  category: string;
  label: string;
  value?: number;
  params?: Record<string, any>;
}) => {
  if (
    typeof window !== "undefined" &&
    window.gtag &&
    env.NEXT_PUBLIC_ENABLE_GA
  ) {
    window.gtag("event", action, {
      event_category: category,
      event_label: label,
      value: value,
      ...params,
    });
  }
};
