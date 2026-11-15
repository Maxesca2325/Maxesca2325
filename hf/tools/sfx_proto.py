"""Sound for the 15 s prototype, made in code (deterministic): low drone, 3 door knocks,
paper slide, light-off click, mixed under the voice. Writes hf/assets/proto_mix.wav.
Run from hf/:  python3 tools/sfx_proto.py
"""
import wave
import numpy as np

SR, DUR = 48000, 15.0
rng = np.random.default_rng(7)
t = np.arange(int(SR * DUR)) / SR
out = np.zeros_like(t)

# drone: two low sines with a slow beat, fades in, swells before the rule, dies with the light
drone = 0.10 * np.sin(2 * np.pi * 55 * t) + 0.06 * np.sin(2 * np.pi * 82.4 * t + 0.6) + 0.035 * np.sin(2 * np.pi * 110.7 * t)
drone *= 0.75 + 0.25 * np.sin(2 * np.pi * 0.23 * t)
env = np.clip(t / 2.0, 0, 1) * (1 + 0.6 * np.clip((t - 9.5) / 2.5, 0, 1)) * np.where(t < 14.0, 1, np.exp(-(t - 14.0) * 6))
out += drone * env


def place(sig, at, gain=1.0):
    i = int(at * SR)
    n = min(len(sig), len(out) - i)
    out[i:i + n] += gain * sig[:n]


# knock: a low wooden thump + a short click
k = np.arange(int(0.35 * SR)) / SR
knock = (np.sin(2 * np.pi * 72 * k) * np.exp(-k * 22) * 0.9
         + np.sin(2 * np.pi * 180 * k) * np.exp(-k * 45) * 0.35
         + rng.standard_normal(len(k)) * np.exp(-k * 120) * 0.25)
for i, at in enumerate([2.62, 2.84, 3.06, 4.9, 5.25, 5.6]):  # far knocks on "frappe", then the three on "Trois petits coups"
    place(knock, at, 0.38 if i < 3 else 0.85)

# paper slide: band-limited noise swell
p = np.arange(int(0.8 * SR)) / SR
noise = rng.standard_normal(len(p))
noise = np.convolve(noise, np.ones(18) / 18, mode="same") - np.convolve(noise, np.ones(160) / 160, mode="same")
place(noise * np.sin(np.pi * p / p[-1]) ** 1.5 * 0.55, 9.15)

# light off: click
c = np.arange(int(0.06 * SR)) / SR
place(rng.standard_normal(len(c)) * np.exp(-c * 140) * 0.5 + np.sin(2 * np.pi * 900 * c) * np.exp(-c * 90) * 0.2, 14.0)

# voice (24 kHz mono) on top
with wave.open("assets/proto_voice.wav") as w:
    vsr = w.getframerate()
    v = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float64) / 32768
v = np.interp(np.arange(int(len(v) * SR / vsr)) / SR, np.arange(len(v)) / vsr, v)
place(v, 0.0, 0.95)

out *= 0.89 / max(1e-9, np.abs(out).max())
with wave.open("assets/proto_mix.wav", "wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((out * 32767).astype(np.int16).tobytes())
print("wrote assets/proto_mix.wav", round(len(out) / SR, 2), "s")
