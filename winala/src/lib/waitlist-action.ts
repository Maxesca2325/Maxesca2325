// Indirection so the static GitHub Pages build can swap the server action
// for a stub (static export has no server). See next.config.ts.
export { joinWaitlist, type WaitlistState } from "@/app/actions";
