import { useQuery } from "@tanstack/react-query";

import { loadModels } from "./api";

export function useModels({ enabled = true }: { enabled?: boolean } = {}) {
  const { data, isLoading, error } = useQuery({
    queryKey: ["models"],
    queryFn: () => loadModels(),
    enabled,
    refetchOnWindowFocus: false,
  });

  // Debug logging
  console.log("[useModels] Query state:", {
    isLoading,
    error: error?.message,
    dataLength: data?.length,
    enabled,
  });

  return { models: data ?? [], isLoading, error };
}
