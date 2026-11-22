import "server-only";
import { cacheLife } from "next/cache";
import { publicClient } from "./supabase/server";

export interface TrackerRow {
  id: string;
  match_id: string;
  market: string;
  /** null until kickoff: only the hash commitment is public before the match. */
  predicted_pick: string | null;
  probability: number | null;
  commitment: string;
  salt: string | null;
  result: "WIN" | "LOSS" | "VOID" | null;
  published_at: string;
  settled_at: string | null;
  home_team: string;
  away_team: string;
  league_name: string;
  kickoff_time: string;
}

/**
 * Reads the public track record (view `public_tracker`). Returns [] when the
 * backend is not connected yet: the page then shows an honest empty state.
 */
export async function getTracker(): Promise<{ rows: TrackerRow[]; connected: boolean }> {
  "use cache";
  cacheLife("minutes");
  const db = publicClient();
  if (!db) return { rows: [], connected: false };
  const { data, error } = await db
    .from("public_tracker")
    .select("*")
    .order("kickoff_time", { ascending: false })
    .limit(200);
  if (error || !data) return { rows: [], connected: true };
  return { rows: data as TrackerRow[], connected: true };
}

export function summarize(rows: TrackerRow[]) {
  const settled = rows.filter(
    (r): r is TrackerRow & { probability: number } =>
      (r.result === "WIN" || r.result === "LOSS") && r.probability !== null,
  );
  const wins = settled.filter((r) => r.result === "WIN").length;
  // Brier score on the published pick: mean (p - outcome)^2. Lower is better.
  const brier = settled.length
    ? settled.reduce((s, r) => s + (r.probability - (r.result === "WIN" ? 1 : 0)) ** 2, 0) / settled.length
    : null;
  // Expected wins if the model were perfectly calibrated.
  const expected = settled.reduce((s, r) => s + r.probability, 0);
  return { settled: settled.length, wins, rate: settled.length ? wins / settled.length : null, brier, expected };
}
