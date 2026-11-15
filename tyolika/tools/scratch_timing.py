"""Scratch timing.json BEFORE the real voice exists (estimated at WPS words/s, 0.15 s between sentences),
so the video can be built and previewed. The real recording replaces it:
  python3 ../scripts/import_voice.py <ep> <audio> --lang ht      (run from tyolika/)
Usage (from tyolika/): python3 tools/scratch_timing.py v01 [words_per_second]
"""
import json, re, sys
from pathlib import Path
ep = sys.argv[1]; WPS = float(sys.argv[2]) if len(sys.argv) > 2 else 3.2
shots = json.loads((Path("episodes") / ep / "shots.json").read_text())
norm = lambda w: re.sub(r"[^\w]", "", w)
t, out = 0.12, []
for s in shots:
    spoken = (s.get("say") or s["text"]).split()
    written = s["text"].split()
    dur = len(spoken) / WPS
    lens = [max(2, len(norm(w))) + 2 for w in written]
    words, x = [], t
    for w, L in zip(written, lens):
        d = dur * L / sum(lens)
        words.append({"w": w, "start": round(x, 3), "end": round(x + d, 3)}); x += d
    out.append({"id": s["id"], "start": 0.0 if not out else round(t, 3), "end": round(t + dur, 3), "words": words})
    t += dur + 0.15
total = round(t + 0.6, 3)
(Path("episodes") / ep / "timing.json").write_text(json.dumps({"voice": "scratch", "speed": 1, "total": total, "shots": out}, indent=1, ensure_ascii=False))
print(f"scratch timing: {len(out)} shots, {total}s, {sum(len(s['words']) for s in out)} words")
