import glob, subprocess, difflib, re, numpy as np
from faster_whisper import WhisperModel
REF = "Sispann peye pou flyer ou. Avèk entèlijans atifisyèl, ou ka fè youn ki sanble pwofesyonèl, nan twa minit, sou telefòn ou."
norm = lambda s: re.sub(r"[^\w ]", "", s.lower()).split()
m = WhisperModel("small", device="cpu", compute_type="int8")
for f in sorted(glob.glob("fishaudio_*.mp3")):
    cut = subprocess.run(["ffmpeg","-loglevel","error","-i",f,"-af","silenceremove=start_periods=1:start_threshold=-40dB:start_silence=0.03:stop_periods=-1:stop_duration=0.05:stop_threshold=-40dB:stop_silence=0.13","-ac","1","-ar","16000","-f","f32le","-"],capture_output=True).stdout
    a = np.frombuffer(cut, dtype=np.float32); dur = len(a)/16000
    segs, _ = m.transcribe(a, language="ht")
    txt = " ".join(s.text.strip() for s in segs)
    r = difflib.SequenceMatcher(None, norm(REF), norm(txt)).ratio()
    print(f"{f[10:18]}  cut={dur:.2f}s  {21/dur:.2f} w/s  match={r:.0%}  heard: {txt}")
