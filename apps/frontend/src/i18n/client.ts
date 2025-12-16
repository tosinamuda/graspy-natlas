"use client";

import { FlatNamespace, KeyPrefix } from "i18next";
import {
  useTranslation as useTranslationOrg,
  UseTranslationOptions,
  UseTranslationResponse,
  FallbackNs,
} from "react-i18next";

export function useTranslation<
  Ns extends FlatNamespace,
  KPrefix extends KeyPrefix<FallbackNs<Ns>> = undefined
>(
  ns?: Ns,
  options?: UseTranslationOptions<KPrefix>
): UseTranslationResponse<FallbackNs<Ns>, KPrefix> {
  return useTranslationOrg(ns, options);
}
