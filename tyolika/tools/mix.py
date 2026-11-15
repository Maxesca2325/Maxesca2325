"""Mix: the voice (public/<ep>/voice.wav, if it exists) on top + every SFX from episodes/<ep>/sfx.json. No music.
Writes assets/<ep>_mix.wav (48 kHz mono). Run from tyolika/: python3 tools/mix.py v01
"""
import json, subprocess, sys, wave
from pathlib import Path
import numpy as np
SR = 48000
ep = sys.argv[1]
spec = json.loads(Path(f"episodes/{ep}/sfx.json").read_text())
out = np.zeros(int(SR * spec["total"]))
cache = {}

def load(path):
    if path not in cache:
        pcm = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", str(path), "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True, check=True).stdout
        a = np.frombuffer(pcm, dtype=np.float32).astype(np.float64)
        cache[path] = a / max(1e-9, np.abs(a).max())
    return cache[path]

def place(sig, at, gain):
    i = int(at * SR); n = min(len(sig), len(out) - i)
    if n > 0: out[i:i + n] += gain * sig[:n]

SFX_LEVEL = 0.5  # SFX peaks about -6 dB under the voice
for e in spec["events"]:
    place(load(Path("assets/sfx") / f"{e['name']}.mp3"), e["t"], e["gain"] * SFX_LEVEL)
voice = Path(f"public/{ep}/voice.wav")
if voice.exists():
    place(load(voice), 0.0, 0.89)
    print("voice:", voice)
else:
    print("no voice yet (SFX only preview)")
peak = np.abs(out).max()
if peak > 0.89: out *= 0.89 / peak
Path("assets").mkdir(exist_ok=True)
with wave.open(f"assets/{ep}_mix.wav", "wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((np.clip(out, -1, 1) * 32767).astype(np.int16).tobytes())
print(f"wrote assets/{ep}_mix.wav {len(out) / SR:.2f}s, {len(spec['events'])} sfx")
