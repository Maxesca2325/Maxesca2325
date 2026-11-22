import type { NextConfig } from "next";

const securityHeaders = [
  { key: "X-Content-Type-Options", value: "nosniff" },
  { key: "Referrer-Policy", value: "strict-origin-when-cross-origin" },
  { key: "X-Frame-Options", value: "DENY" },
  { key: "Permissions-Policy", value: "camera=(), microphone=(), geolocation=()" },
  { key: "Strict-Transport-Security", value: "max-age=63072000; includeSubDomains" },
];

// `npm run build:pages` → static test build for GitHub Pages (no server).
const STATIC_DEMO = process.env.NEXT_PUBLIC_STATIC_DEMO === "1";
const BASE_PATH = process.env.NEXT_PUBLIC_BASE_PATH ?? "";

const nextConfig: NextConfig = {
  ...(STATIC_DEMO && {
    output: "export",
    basePath: BASE_PATH,
    trailingSlash: true,
    images: { unoptimized: true },
  }),
  // Static export cannot do partial prerendering, which Cache Components implies.
  cacheComponents: !STATIC_DEMO,
  partialPrefetching: !STATIC_DEMO,
  poweredByHeader: false,
  experimental: {
    // Unstable 3G/4G: failed navigations and server actions wait and retry
    // when the network comes back instead of throwing.
    useOffline: true,
  },
  turbopack: {
    root: process.cwd(),
    // Static export cannot run server actions: swap the waitlist action for a stub.
    resolveAlias: STATIC_DEMO
      ? {
          "@/lib/waitlist-action": "./src/lib/waitlist-action.static.ts",
          "@/lib/tracker": "./src/lib/tracker.static.ts",
        }
      : {},
    rules: {
      "*.css": {
        loaders: ["@tailwindcss/turbopack"],
        as: "*.css",
      },
    },
  },
  async headers() {
    if (STATIC_DEMO) return [];
    return [
      { source: "/:path*", headers: securityHeaders },
      {
        source: "/sw.js",
        headers: [
          { key: "Cache-Control", value: "no-cache, no-store, must-revalidate" },
          { key: "Content-Type", value: "application/javascript; charset=utf-8" },
        ],
      },
    ];
  },
};

export default nextConfig;
