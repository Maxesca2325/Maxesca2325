"""Generates the 3D version of the 15 s prototype: hf/index.html (3D canvas + sound) and the
overlay (clock bar, grain, vignette) + captions compositions. The 3D world itself is hf/scene3d.js.
Captions come from episodes/proto/timing.json (the voice). Run from hf/:  python3 tools/gen_proto3d.py
"""
import json
from pathlib import Path

W, H, DUR = 1080, 1920, 15
HF = Path(__file__).resolve().parent.parent
INK, RED = "#1A1426", "#E0303A"
timing = json.loads((HF.parent / "episodes/proto/timing.json").read_text())
RED_WORDS = {"FRAPPE", "SEUL.", "FEUILLE"}
SKIP_SHOTS = {6}  # the rule is written on the paper itself: no duplicate captions


def scene(cid, style, body, script):
    return f"""<template>
  <style>
    #root {{ position: absolute; inset: 0; overflow: hidden; }}
{style}
  </style>
  <div id="root" data-composition-id="{cid}" data-width="{W}" data-height="{H}">
{body}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
{script}
    window.__timelines["{cid}"] = tl;
  </script>
</template>
"""


# ---------- captions (one word at a time, from the voice timing) ----------
caps = []
for s in timing["shots"]:
    if s["id"] in SKIP_SHOTS:
        continue
    for w in s["words"]:
        word = w["w"].upper()
        if not any(ch.isalnum() for ch in word):
            continue
        caps.append([max(0.12, w["start"]), w["end"], word])
for i in range(len(caps) - 1):  # back to back, never overlapping
    caps[i][1] = min(max(caps[i][1], caps[i][0] + 0.18), caps[i + 1][0])
cap_style = f"""    .cap {{ position:absolute; left:150px; right:150px; top:1020px; text-align:center; opacity:0; visibility:hidden;
      font-family:'Oswald'; font-weight:700; font-size:96px; letter-spacing:.01em; color:#fff;
      -webkit-text-stroke: 10px {INK}; paint-order: stroke fill; text-shadow: 0 8px 22px rgba(0,0,0,.6); }}
    .cap.red {{ color:{RED}; }}"""
cap_body = "\n".join(f'    <div id="cap-{i}" class="cap{" red" if w in RED_WORDS else ""}">{w}</div>' for i, (a, b, w) in enumerate(caps))
cap_script = "\n".join(
    f'    tl.set("#cap-{i}", {{ visibility: "visible" }}, {a:.3f}); tl.fromTo("#cap-{i}", {{ opacity: 0, scale: 1.16 }}, {{ opacity: 1, scale: 1, duration: {min(0.08, (b - a) / 3):.3f}, ease: "power3.out" }}, {a:.3f});'
    f' tl.to("#cap-{i}", {{ opacity: 0, duration: {min(0.05, (b - a) / 3):.3f}, ease: "power2.in" }}, {b - min(0.05, (b - a) / 3):.3f}); tl.set("#cap-{i}", {{ opacity: 0, visibility: "hidden" }}, {b:.3f});'
    for i, (a, b, w) in enumerate(caps))

# ---------- overlay: clock bar (higher than before), grain, vignette ----------
secs = range(7, 7 + DUR + 1)
digits = "\n".join(f'      <span id="ov-s{s}" class="ov-sec">{s:02d}</span>' for s in secs)
ov_style = """    #ov-bar { position:absolute; left:0; right:0; top:225px; display:flex; flex-direction:column; align-items:center; gap:4px; }
    #ov-room { font-family:'Oswald'; font-weight:700; font-size:28px; letter-spacing:.35em; color:rgba(255,255,255,.72); }
    #ov-time { font-family:'JetBrains Mono'; font-weight:700; font-size:60px; color:#fff; text-shadow:0 0 18px rgba(224,48,58,.55); display:flex; }
    .ov-sec { position:absolute; opacity:0; }
    #ov-secs { position:relative; width:74px; }
    #ov-vig { position:absolute; inset:0; background:radial-gradient(ellipse at 50% 45%, rgba(0,0,0,0) 50%, rgba(6,4,16,.7) 100%); }
    #ov-grain { position:absolute; inset:-40px; opacity:.10; mix-blend-mode:overlay; }"""
ov_body = f"""    <svg id="ov-grain" viewBox="0 0 {W+80} {H+80}" data-layout-ignore><filter id="ov-noise"><feTurbulence id="ov-turb" type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed="1"/></filter><rect width="100%" height="100%" filter="url(#ov-noise)"/></svg>
    <div id="ov-vig" data-layout-ignore></div>
    <div id="ov-bar">
      <div id="ov-room">CHAMBRE</div>
      <div id="ov-time">02:41:<span id="ov-secs" data-layout-allow-overlap>
{digits}
      </span></div>
    </div>"""
ticks = "\n".join(f'    tl.set("#ov-s{s}", {{ opacity: 1 }}, {i}); tl.set("#ov-s{s}", {{ opacity: 0 }}, {i + 1});' for i, s in enumerate(secs))
grain = "\n".join(f'    tl.set("#ov-turb", {{ attr: {{ seed: {k % 97 + 1} }} }}, {k / 12:.4f}); tl.set("#ov-grain", {{ x: {((k * 37) % 40) - 20}, y: {((k * 53) % 40) - 20} }}, {k / 12:.4f});' for k in range(DUR * 12))
ov_script = f"""{ticks}
{grain}
    tl.fromTo("#ov-bar", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.25 }}, 0.0);
    tl.to("#ov-bar", {{ opacity: 0, duration: 0.15 }}, 14.0);
"""

(HF / "compositions").mkdir(exist_ok=True)
for old in ["s1-chambre", "s2-porte", "s3-feuille"]:
    (HF / f"compositions/{old}.html").unlink(missing_ok=True)
(HF / "compositions/overlay.html").write_text(scene("overlay", ov_style, ov_body, ov_script))
(HF / "compositions/captions.html").write_text(scene("captions", cap_style, cap_body, cap_script))

host = lambda cid, track, kind, z: (
    f'      <div id="{cid}" data-composition-id="{cid}" data-composition-src="compositions/{cid}.html" data-start="0" data-duration="{DUR}" '
    f'data-track-index="{track}" data-track-kind="{kind}" data-width="{W}" data-height="{H}" style="z-index:{z}"></div>')
index = f"""<!doctype html>
<html lang="fr" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={W}, height={H}" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <script type="importmap">{{ "imports": {{ "three": "./lib/three/three.module.js", "three/addons/": "./lib/three/addons/" }} }}</script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: {W}px; height: {H}px; overflow: hidden; background: #0b0a18; }}
      #w3d-canvas {{ position: absolute; inset: 0; width: {W}px; height: {H}px; }}
      /* the 3D canvas textures use these faces: keep them in the font bundle */
      #fontkeep {{ position:absolute; left:-9999px; top:0; font-size:10px; }}
      #fontkeep .a {{ font-family:'Oswald'; font-weight:700; }} #fontkeep .b {{ font-family:'EB Garamond'; font-style:italic; }} #fontkeep .c {{ font-family:'JetBrains Mono'; font-weight:700; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-width="{W}" data-height="{H}" data-fps="60">
      <canvas id="w3d-canvas" class="clip" data-start="0" data-duration="{DUR}" data-track-index="0" width="{W}" height="{H}" data-layout-ignore></canvas>
      <div id="fontkeep" data-layout-ignore><span class="a">RÈGLE</span><span class="b">Ne réponds pas</span><span class="c">2:41</span></div>
{host("overlay", 2, "graphics", 5)}
{host("captions", 3, "captions", 6)}
      <audio id="mix" class="clip" src="assets/proto_mix.wav" data-start="0" data-duration="{DUR}" data-track-index="4" data-volume="1"></audio>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{ paused: true }});
      const state = {{ t: 0 }};
      const draw = () => {{ window.__w3dTime = state.t; if (window.__render3d) window.__render3d(state.t); }};
      tl.fromTo(state, {{ t: 0 }}, {{ t: {DUR}, duration: {DUR}, ease: "none", onUpdate: draw }}, 0);
      window.addEventListener("hf-seek", (e) => {{
        const d = e && e.detail;
        if (d && typeof d.time === "number") tl.totalTime(Math.min(d.time, tl.totalDuration()), true);
        draw();
      }});
      window.__timelines["main"] = tl;
    </script>
    <script type="module" src="scene3d.js"></script>
  </body>
</html>
"""
(HF / "index.html").write_text(index)
print("wrote index.html, compositions/overlay.html, compositions/captions.html;", len(caps), "captions")
