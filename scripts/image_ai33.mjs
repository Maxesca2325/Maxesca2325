// Images with ai33.pro (gpt-image, seedream, recraft, flux, gemini...).
// Usage:
//   node scripts/image_ai33.mjs --models
//   node scripts/image_ai33.mjs <prompts.json> <out_dir>
// prompts.json: [{ "name": "post1", "prompt": "...", "model": "gpt-image-2", "aspect_ratio": "4:5", "resolution": "1K", "quality": "high", "n": 1 }]
// Images already downloaded (same name) are skipped, so a re-run only pays for new ones.
// API key: injected by the cloud network proxy. On your own PC: export AI33_API_KEY=... (never in a file of this project).
import { execFileSync } from "node:child_process";
import fs from "node:fs";
import path from "node:path";

const API = "https://api.ai33.pro";
const KEY = process.env.AI33_API_KEY || "proxy-injected";
const curl = (args) => {
  const out = execFileSync("curl", ["-sS", "--fail-with-body", "-m", "120", "-H", `xi-api-key: ${KEY}`, ...args]).toString();
  const j = JSON.parse(out);
  if (j.success === false) throw new Error(`ai33: ${j.message || out}`);
  return j;
};
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const [a1, a2] = process.argv.slice(2);

if (a1 === "--models") {
  for (const m of curl([`${API}/v1i/models`]).models)
    console.log(m.model_id.padEnd(34), String(m.presented_credits ?? "").padEnd(6), (m.aspect_ratios || []).join(","));
  process.exit(0);
}
if (!a1 || !a2) { console.log("Usage: node scripts/image_ai33.mjs <prompts.json> <out_dir>  |  --models"); process.exit(1); }

const items = JSON.parse(fs.readFileSync(a1, "utf8"));
fs.mkdirSync(a2, { recursive: true });
const todo = items.filter((it) => !fs.existsSync(path.join(a2, `${it.name}_1.jpg`)));
let credits = 0;
// task ids are saved, so a re-run after a crash waits for the same tasks instead of paying again
const tasksFile = path.join(a2, "tasks.json");
const saved = fs.existsSync(tasksFile) ? JSON.parse(fs.readFileSync(tasksFile, "utf8")) : {};
const sig = (it) => JSON.stringify([it.prompt, it.model, it.aspect_ratio, it.resolution, it.quality, it.n]);

for (const it of todo) {
  if (saved[it.name]?.sig === sig(it)) { it.task = saved[it.name].task; console.log(`${it.name}: resuming task ${it.task}`); continue; }
  const model_parameters = {};
  for (const k of ["aspect_ratio", "resolution", "quality"]) if (it[k]) model_parameters[k] = it[k];
  const body = { prompt: it.prompt, model_id: it.model || "gpt-image-2", generations_count: it.n || 1, model_parameters };
  const r = curl(["-X", "POST", "-H", "Content-Type: application/json", "-d", JSON.stringify(body), `${API}/v1i/task/generate-image`]);
  it.task = r.task_id;
  saved[it.name] = { task: it.task, sig: sig(it) };
  fs.writeFileSync(tasksFile, JSON.stringify(saved, null, 1));
  console.log(`${it.name}: submitted (${r.estimated_credits} credits est.)`);
}

const t0 = Date.now();
while (todo.some((it) => !it.done)) {
  if (Date.now() - t0 > 15 * 60e3) throw new Error("tasks still not done after 15 minutes");
  await sleep(6000);
  for (const it of todo.filter((x) => !x.done)) {
    let d;
    try { d = curl([`${API}/v1/task/${it.task}`]); } catch (e) { continue; } // 503 "server_busy": try again next round
    if (d.status === "failed" || d.status === "error") { it.done = true; console.log(`${it.name}: FAILED ${d.error_message || ""}`); continue; }
    if (d.status !== "done") continue;
    it.done = true;
    credits += d.credit_cost || 0;
    (d.metadata?.result_images || []).forEach((img, i) => {
      const f = path.join(a2, `${it.name}_${i + 1}.jpg`);
      execFileSync("curl", ["-sS", "--fail", "-m", "120", "-o", f, img.imageUrl]);
      console.log(`${it.name}: ${f} (${img.width}x${img.height})`);
    });
  }
}
console.log(`Done. ${credits} credits. Left: ${curl([`${API}/v1/credits`]).credits}`);
