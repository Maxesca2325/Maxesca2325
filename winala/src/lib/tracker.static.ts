// Static test build: no database connection, so the public track record is
// empty (honest: there are no real settled picks yet).
import type { TrackerRow } from "./tracker-types";
export type { TrackerRow };
export { summarize } from "./tracker-summary";

export async function getTracker(): Promise<{ rows: TrackerRow[]; connected: boolean }> {
  return { rows: [], connected: false };
}
