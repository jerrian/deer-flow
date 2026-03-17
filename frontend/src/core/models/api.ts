import { getBackendBaseURL } from "../config";

import type { Model } from "./types";

export async function loadModels() {
  const url = `${getBackendBaseURL()}/api/models`;
  console.log("[loadModels] Fetching models from:", url);
  try {
    const res = await fetch(url);
    console.log("[loadModels] Response status:", res.status);
    if (!res.ok) {
      console.error("[loadModels] Failed to load models:", res.status);
      return [];
    }
    const { models } = (await res.json()) as { models: Model[] };
    console.log("[loadModels] Models loaded:", models);
    return models;
  } catch (error) {
    console.error("[loadModels] Error:", error);
    return [];
  }
}
