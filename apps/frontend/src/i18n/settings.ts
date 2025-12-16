export const fallbackLng = "en";
export const languages = ["en", "yo", "ig", "ha", "pcm"];
export const defaultNS = "translation";
export const headerName = "x-locale";

export function getOptions(lng = fallbackLng, ns = defaultNS) {
  return {
    // debug: true,
    supportedLngs: languages,
    fallbackLng,
    lng,
    fallbackNS: defaultNS,
    defaultNS,
    ns,
  };
}
