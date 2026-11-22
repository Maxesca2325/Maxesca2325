/** "" in production on a domain; "/Maxesca2325" for the GitHub Pages test build. */
export const BASE_PATH = process.env.NEXT_PUBLIC_BASE_PATH ?? "";
/** True for the static GitHub Pages test build (no server: waitlist inactive). */
export const STATIC_DEMO = process.env.NEXT_PUBLIC_STATIC_DEMO === "1";
