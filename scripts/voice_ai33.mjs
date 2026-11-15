// Narration with ai33.pro voices (ElevenLabs, MiniMax, Fish Audio, your cloned voices, Edge, Kokoro...).
// Writes the same files as voice.mjs, so the rest of the workflow is unchanged:
//   public/<ep>/voice.wav  +  episodes/<ep>/timing.json   (word times by scripts/import_voice.py, free, local)
//
// Usage:
//   [TEMPO=1.1] [MAXPAUSE=0.18] node scripts/voice_ai33.mjs <ep> <voice_id> [speed]   (dead air is always cut to MAXPAUSE s)  e.g. node scripts/voice_ai33.mjs ep2 elevenlabs_nPczCjzI2devNBz1zQrb 1.05
//   node scripts/voice_ai33.mjs --voices <provider> [search]   provider: elevenlabs | minimax | fishaudio | clone | edge | kokoro | vbee
//   node scripts/voice_ai33.mjs --clone <sample.mp3> "<name>"  creates a cloned voice, prints its voice_id (clone_...)
//   node scripts/voice_ai33.mjs --delete-clone <id>
//
// API key: on the cloud environment it is added by the network proxy (nothing to do).
// On your own computer: export AI33_API_KEY=... before running. Never write the key in a file of this project.
// HTTP goes through curl so it uses the machine's proxy settings.
import { execFileSync } from "node:child_process";
import fs from "node:fs";
import path from "node:path";

const API = "https://api.ai33.pro";
const KEY = process.env.AI33_API_KEY || "proxy-injected";
const GAP = Number(process.env.GAP || 0.06); // seconds between lines (voice.mjs uses 0.06; horror: GAP=0.45)
const SR = 24000;
const PY = process.platform === "win32" ? "python" : "python3";

const curl = (args) => {
  const out = execFileSync("curl", ["-sS", "--fail-with-body", "-m", "300", "-H", `xi-api-key: ${KEY}`, ...args], { maxBuffer: 1 << 28 }).toString();
  const j = JSON.parse(out);
  if (j.success === false) throw new Error(`ai33: ${j.message || out}`);
  return j;
};
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const [a1, a2, a3] = process.argv.slice(2);

if (!a1) {
  console.log("Usage: node scripts/voice_ai33.mjs <ep> <voice_id> [speed]   |   --voices <provider> [search]   |   --clone <file> <name>");
  process.exit(1);
}

if (a1 === "--voices") {
  const q = new URLSearchParams({ provider: a2 || "elevenlabs", page_size: "100" });
  if (a3) q.set("search", a3);
  const j = curl([`${API}/v3/voices?${q}`]);
  for (const v of j.data) console.log(v.voice_id.padEnd(48), (v.name || "").slice(0, 50).padEnd(50), v.gender || "", v.language || "");
  console.log(`${j.data.length} shown of ${j.pagination?.total ?? "?"}`);
  process.exit(0);
}
if (a1 === "--clone") {
  if (!a2 || !a3) throw new Error('Usage: --clone <sample.mp3> "<name>"');
  const j = curl(["-X", "POST", `${API}/v3/text-to-speech/voice-clone`, "--form-string", `voice_name=${a3}`, "-F", `audio_file=@${a2}`]);
  console.log(`Cloned. voice_id: clone_${j.data.voice_id}`);
  process.exit(0);
}
if (a1 === "--delete-clone") {
  curl(["-X", "DELETE", `${API}/v3/text-to-speech/voice-clone/${String(a2).replace(/^clone_/, "")}`]);
  console.log("Deleted.");
  process.exit(0);
}

// ---- narration ----
const ep = a1, voice = a2, speed = Number(a3 || 1);
if (!voice || !/^[a-z]+_/.test(voice)) throw new Error("voice_id must have a provider prefix, e.g. elevenlabs_..., minimax_..., fishaudio_..., clone_...  (list them with --voices <provider>)");
if (!(speed >= 0.5 && speed <= 1.5)) throw new Error("speed must be between 0.5 and 1.5");
const shots = JSON.parse(fs.readFileSync(path.join("episodes", ep, "shots.json"), "utf8"));
const work = path.join("public", ep, "ai33");
fs.mkdirSync(work, { recursive: true });

// 1. submit every line (skip lines already downloaded with the same text + voice + speed, so re-runs only pay for changes)
const key = (s) => `${voice}|${speed}|${s.say ?? s.text}`;
const cacheFile = path.join(work, "cache.json");
const cache = fs.existsSync(cacheFile) ? JSON.parse(fs.readFileSync(cacheFile, "utf8")) : {};
const lineText = (s) => (s.say ?? s.text).replace(/_/g, " ");
const jobs = shots.map((s) => ({ s, file: path.join(work, `shot${s.id}.mp3`) }));
let credits = 0;

// submit lines, wait for the tasks, download the audio
async function generate(todo) {
  for (const j of todo) {
    j.done = false;
    j.task = curl(["-X", "POST", `${API}/v3/text-to-speech`, "--form-string", `text=${lineText(j.s)}`, "--form-string", `voice_id=${voice}`,
      "--form-string", `speed=${speed}`, "--form-string", "with_transcript=false"]).task_id;
    console.log(`shot ${j.s.id}: submitted`);
  }
  const t0 = Date.now();
  while (todo.some((j) => !j.done)) {
    if (Date.now() - t0 > 15 * 60e3) throw new Error("ai33 tasks still not done after 15 minutes");
    await sleep(3000);
    for (const j of todo.filter((j) => !j.done)) {
      const d = curl([`${API}/v3/task/${j.task}`]).data;
      if (d.status === "done") {
        execFileSync("curl", ["-sS", "--fail", "-L", "-m", "300", "-o", j.file, d.metadata.audio_url]);
        cache[j.s.id] = key(j.s);
        fs.writeFileSync(cacheFile, JSON.stringify(cache, null, 1));
        credits += d.credit_cost || 0;
        j.done = true;
        console.log(`shot ${j.s.id}: done (${d.credit_cost} credits)`);
      } else if (/fail|error|cancel/i.test(d.status)) {
        throw new Error(`shot ${j.s.id} failed on ai33: ${JSON.stringify(d.error_message || d.status)}`);
      }
    }
  }
}
// check new lines really say their text (voices sometimes say other words); redo a bad line once
function check(todo) {
  const f = path.join(work, "check.json");
  fs.writeFileSync(f, JSON.stringify(todo.map((j) => ({ id: j.s.id, file: j.file, text: [j.s.text, lineText(j.s)] }))));
  const r = JSON.parse(execFileSync(PY, ["scripts/check_lines.py", f], { stdio: ["ignore", "pipe", "ignore"] }).toString().trim().split("\n").pop());
  return todo.filter((j) => r[j.s.id] < 0.75).map((j) => ({ j, ratio: r[j.s.id] }));
}
const fresh = jobs.filter((j) => !(cache[j.s.id] === key(j.s) && fs.existsSync(j.file)));
if (fresh.length) {
  await generate(fresh);
  let bad = check(fresh);
  if (bad.length) {
    console.log(`Lines that don't say their text: ${bad.map((b) => `shot ${b.j.s.id} (${Math.round(b.ratio * 100)}%)`).join(", ")}. Generating them again once...`);
    await generate(bad.map((b) => b.j));
    bad = check(bad.map((b) => b.j));
    for (const b of bad) {
      delete cache[b.j.s.id]; // so the next run tries it again
      console.log(`WARNING: shot ${b.j.s.id} still doesn't match its text (${Math.round(b.ratio * 100)}%). Listen to ${b.j.file}; rephrase the line or pick another voice.`);
    }
    fs.writeFileSync(cacheFile, JSON.stringify(cache, null, 1));
  }
}

// 3. trim the silence around each line and join them with the same gap as voice.mjs
const trimmed = [];
for (const { s, file } of jobs) {
  const wav = path.join(work, `shot${s.id}.wav`);
  execFileSync("ffmpeg", ["-y", "-loglevel", "error", "-i", file, "-ac", "1", "-ar", String(SR),
    "-af", "silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.02,areverse,silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.04,areverse",
    "-c:a", "pcm_s16le", wav]);
  trimmed.push(wav);
}
const gap = path.join(work, "gap.wav");
execFileSync("ffmpeg", ["-y", "-loglevel", "error", "-f", "lavfi", "-t", String(GAP), "-i", `anullsrc=r=${SR}:cl=mono`, "-c:a", "pcm_s16le", gap]);
const list = path.join(work, "list.txt");
fs.writeFileSync(list, trimmed.flatMap((f, i) => [`file '${path.resolve(f)}'`, ...(i < trimmed.length - 1 ? [`file '${path.resolve(gap)}'`] : [])]).join("\n"));
const joined = path.join(work, "narration.wav");
execFileSync("ffmpeg", ["-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", list, "-c:a", "pcm_s16le", joined]);
if (credits) console.log(`ai33 credits used this run: ${credits}`);

// 4. word times + voice.wav + timing.json, exactly like an imported recording
execFileSync(PY, ["scripts/import_voice.py", ep, joined, "--max-pause", process.env.MAXPAUSE || "0.18", "--tempo", process.env.TEMPO || "1"], { stdio: "inherit" });
const tf = path.join("episodes", ep, "timing.json");
const t = JSON.parse(fs.readFileSync(tf, "utf8"));
t.voice = voice; t.speed = speed;
fs.writeFileSync(tf, JSON.stringify(t, null, 1));
