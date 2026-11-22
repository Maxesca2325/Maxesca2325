import "server-only";
import { cacheLife } from "next/cache";
import { publicClient } from "./supabase/server";

import type { TrackerRow } from "./tracker-types";
export type { TrackerRow };
export { summarize } from "./tracker-summary";

/**
 * Reads the public track record (RPC `get_public_tracker`). Returns [] when the
 * backend is not connected yet: the page then shows an honest empty state.
 */
export async function getTracker(): Promise<{ rows: TrackerRow[]; connected: boolean }> {
  "use cache";
  cacheLife("minutes");
  const db = publicClient();
  if (!db) return { rows: [], connected: false };
  const { data, error } = await db
    .rpc("get_public_tracker", { p_limit: 200 });
  if (error || !data) return { rows: [], connected: true };
  return { rows: data as TrackerRow[], connected: true };
}
