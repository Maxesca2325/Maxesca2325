"""Check that each generated line says its text (catches TTS glitches where a voice says other words).
Usage: python3 scripts/check_lines.py lines.json [--lang en]
lines.json = [{"id": 1, "file": "public/ep2/ai33/shot1.mp3", "text": "..." or ["written text", "spoken text"]}]
Prints JSON: {"<id>": ratio 0..1, ...}  (share of the script words heard, in order)
"""
import difflib, json, re, subprocess, sys
import numpy as np
from faster_whisper import WhisperModel

lines = json.load(open(sys.argv[1]))
lang = sys.argv[sys.argv.index("--lang") + 1] if "--lang" in sys.argv else None
norm = lambda t: [re.sub(r"[^\w]", "", w.lower()) for w in t.split() if re.sub(r"[^\w]", "", w)]
model = WhisperModel("small", device="cpu", compute_type="int8")
out = {}
for l in lines:
    pcm = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", l["file"], "-ac", "1", "-ar", "16000", "-f", "f32le", "-"], capture_output=True, check=True).stdout
    segs, _ = model.transcribe(np.frombuffer(pcm, dtype=np.float32), language=lang)
    heard = norm(" ".join(s.text for s in segs))
    best = 0.0
    for t in (l["text"] if isinstance(l["text"], list) else [l["text"]]):  # e.g. ["... 1875", "... eighteen seventy-five"]
        want = norm(t)
        sm = difflib.SequenceMatcher(None, want, heard, autojunk=False)
        best = max(best, sum(b.size for b in sm.get_matching_blocks()) / max(1, len(want)))
    out[str(l["id"])] = round(best, 2)
print(json.dumps(out))
