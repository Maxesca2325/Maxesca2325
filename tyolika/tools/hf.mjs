// Runs the pinned HyperFrames CLI with telemetry off, on Windows, macOS and Linux alike.
// Usage (from hf/):  node tools/hf.mjs <command> [args]   e.g. node tools/hf.mjs render --fps 60
import { spawnSync } from "node:child_process";

const env = { ...process.env, HYPERFRAMES_NO_TELEMETRY: "1", DO_NOT_TRACK: "1" };
const r = spawnSync("npx", ["--yes", "hyperframes@0.9.50", ...process.argv.slice(2)], { stdio: "inherit", env, shell: process.platform === "win32" });
process.exit(r.status ?? 1);
