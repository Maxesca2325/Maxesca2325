"""Use your OWN voice recording instead of Kokoro.

Usage:
  python3 scripts/import_voice.py epN path/to/audio.(mp3|wav|m4a|...) [--lang en|fr|...] [--model small]

Writes exactly what scripts/voice.mjs writes, so everything after it (stills, sound, render) works the same:
  public/epN/voice.wav        the narration (24 kHz mono, peak -1 dB)
  episodes/epN/timing.json    per shot: start, end (s) + per word: start, end (for one-word captions)

Word times come from faster-whisper (free, runs locally).
- If episodes/epN/shots.json exists: the words of your script are matched to what was heard,
  so captions show YOUR text (spelling, numbers like "1875") at the moment it is said.
- If it doesn't exist: shots.json is created from the recording, one sentence per shot.
"""
import argparse, difflib, json, re, subprocess, sys, wave
from pathlib import Path

SR = 24000

ap = argparse.ArgumentParser()
ap.add_argument("ep")
ap.add_argument("audio")
ap.add_argument("--lang", default=None, help="language code (en, fr, ...). Default: detect")
ap.add_argument("--model", default="small", help="whisper model: tiny, base, small, medium, large-v3")
ap.add_argument("--max-pause", type=float, default=0.18,
                help="cut every silence longer than this (s) down to it: no dead air. 0 = keep the recording's pauses")
ap.add_argument("--tempo", type=float, default=1.0, help="speed up/down without changing pitch (e.g. 1.1); 0.5–2")
a = ap.parse_args()

ep_dir, pub_dir = Path("episodes") / a.ep, Path("public") / a.ep
ep_dir.mkdir(parents=True, exist_ok=True)
pub_dir.mkdir(parents=True, exist_ok=True)
out_wav = pub_dir / "voice.wav"
src = Path(a.audio)
if not src.exists():
    sys.exit(f"Audio file not found: {src}")

# 1. convert: 24 kHz mono 16-bit, dead air cut, optional tempo, peak normalised to -1 dB
tmp = pub_dir / "voice.tmp.wav"
filters = []
if a.max_pause > 0:  # trim the start, then shorten every inner pause to ~max_pause (kept = stop_duration + stop_silence)
    keep = max(0.0, a.max_pause - 0.05)
    filters.append("silenceremove=start_periods=1:start_threshold=-40dB:start_silence=0.03:"
                   f"stop_periods=-1:stop_duration=0.05:stop_threshold=-40dB:stop_silence={keep:.3f}")
if abs(a.tempo - 1.0) > 1e-3:
    filters.append(f"atempo={min(2.0, max(0.5, a.tempo))}")
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(src), "-ac", "1", "-ar", str(SR), *(["-af", ",".join(filters)] if filters else []),
                "-c:a", "pcm_s16le", str(tmp)], check=True)
peak = subprocess.run(["ffmpeg", "-i", str(tmp), "-af", "volumedetect", "-f", "null", "-"], capture_output=True, text=True).stderr
m = re.search(r"max_volume: (-?[\d.]+) dB", peak)
gain = -1.0 - float(m.group(1)) if m else 0.0
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(tmp), "-af", f"volume={gain}dB", "-c:a", "pcm_s16le", str(out_wav)], check=True)
tmp.unlink()
with wave.open(str(out_wav)) as w:
    total = w.getnframes() / w.getframerate()

# 2. transcribe with word timestamps
from faster_whisper import WhisperModel
print(f"Transcribing with whisper '{a.model}' (first run downloads the model)...")
model = WhisperModel(a.model, device="cpu", compute_type="int8")
# decode with ffmpeg (16 kHz float) instead of whisper's own decoder, which breaks with some PyAV versions
import numpy as np
pcm = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", str(out_wav), "-ac", "1", "-ar", "16000", "-f", "f32le", "-"], capture_output=True, check=True).stdout
segs, info = model.transcribe(np.frombuffer(pcm, dtype=np.float32), language=a.lang, word_timestamps=True, vad_filter=True)
heard = []
for s in segs:
    for w in s.words or []:
        if w.word.strip():
            heard.append({"w": w.word.strip(), "start": float(w.start), "end": float(w.end)})
print(f"Language: {info.language}, {len(heard)} words heard, {total:.1f}s")
if not heard:
    sys.exit("No speech found in the audio.")

norm = lambda t: re.sub(r"[^\w]", "", t.lower())

# 3. shots: from shots.json, or one sentence per shot from the recording
shots_path = ep_dir / "shots.json"
if shots_path.exists():
    shots = json.loads(shots_path.read_text())
else:
    shots, cur = [], []
    for h in heard:
        cur.append(h["w"])
        if re.search(r"[.!?]$", h["w"]):
            shots.append({"id": len(shots) + 1, "text": " ".join(cur)}); cur = []
    if cur:
        shots.append({"id": len(shots) + 1, "text": " ".join(cur)})
    shots_path.write_text(json.dumps(shots, indent=1, ensure_ascii=False))
    print(f"Created {shots_path} with {len(shots)} shots (one sentence each). Edit it to split/merge shots, then run this again.")

# align on what is SPOKEN ("say", e.g. "deux heures quarante et une"); captions show what is WRITTEN ("text", e.g. "2h41.")
spoken = lambda s: (s.get("say") or s["text"]).replace("_", " ")
script = [(si, w) for si, s in enumerate(shots) for w in spoken(s).split()]

# 4. match script words to heard words; words not matched get times in between their neighbours
sm = difflib.SequenceMatcher(None, [norm(w) for _, w in script], [norm(h["w"]) for h in heard], autojunk=False)
times = [None] * len(script)
for blk in sm.get_matching_blocks():
    for k in range(blk.size):
        h = heard[blk.b + k]
        times[blk.a + k] = (h["start"], h["end"])
# unmatched runs (numbers, misheard words): spread between the matched neighbours, by length
i = 0
while i < len(script):
    if times[i] is not None:
        i += 1; continue
    j = i
    while j < len(script) and times[j] is None:
        j += 1
    lo = times[i - 1][1] if i > 0 else heard[0]["start"]
    hi = times[j][0] if j < len(script) else heard[-1]["end"]
    if hi <= lo:
        hi = lo + 0.12 * (j - i)
    lens = [max(1, len(norm(script[k][1]))) for k in range(i, j)]
    t = lo
    for k, L in zip(range(i, j), lens):
        d = (hi - lo) * L / sum(lens)
        times[k] = (t, t + d); t += d
    i = j
matched = sum(blk.size for blk in sm.get_matching_blocks())
print(f"Matched {matched}/{len(script)} script words to the recording")
if matched < 0.6 * len(script):
    print("WARNING: under 60% of the script was heard. Is shots.json the text of THIS recording? Is --lang right?")

# monotonic, captions run back to back like voice.mjs
for k in range(1, len(times)):
    s = max(times[k][0], times[k - 1][0] + 0.06)
    times[k] = (s, max(times[k][1], s + 0.06))

timing = []
for si, s in enumerate(shots):
    idx = [k for k, (sj, _) in enumerate(script) if sj == si]
    words = []
    for n, k in enumerate(idx):
        start = times[k][0]
        end = times[idx[n + 1]][0] if n + 1 < len(idx) else min(total, times[k][1])
        words.append({"w": script[k][1], "start": round(start, 3), "end": round(max(end, start + 0.06), 3)})
    written = s["text"].split()
    if spoken(s).split() != written:  # spread the written words over the spoken span, by length
        a, b = words[0]["start"], words[-1]["end"]
        lens = [max(1, len(norm(w))) for w in written]
        t, words = a, []
        for w, L in zip(written, lens):
            d = (b - a) * L / sum(lens)
            words.append({"w": w, "start": round(t, 3), "end": round(t + d, 3)}); t += d
    timing.append({"id": s["id"], "start": 0.0 if si == 0 else words[0]["start"], "end": words[-1]["end"], "words": words})

(ep_dir / "timing.json").write_text(json.dumps({"voice": f"imported:{src.name}", "speed": 1, "total": round(total, 3), "shots": timing}, indent=1, ensure_ascii=False))
nw = len(script)
print(f"Wrote {out_wav} and {ep_dir / 'timing.json'}: {len(shots)} shots, {nw / total:.2f} words/s")
