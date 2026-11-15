"""Generates the 15 s 'protocole' prototype (hf/index.html + hf/compositions/*.html).
Run from hf/:  python3 tools/gen_proto.py
Hand-edit the generated scene files freely afterwards; this script is only the first draft.
"""
from pathlib import Path

W, H, DUR = 1080, 1920, 15
OUT = Path(__file__).resolve().parent.parent
GSAP = '<script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>'

# ---------- palette (styles/protocole.md, "Ours") ----------
NIGHT0, NIGHT1, SHADOW, MOON, WARM, RED, SKIN, SKIN_SH, INK = (
    "#0E0C1C", "#1E1B38", "#2A2850", "#9FB2FF", "#F2C27A", "#E0303A", "#F2EEE8", "#C9C3DC", "#1A1426")

# ---------- captions: (start, end, word, red?) ----------
CAPS = [
    (0.15, 0.95, "2H41.", False),
    (1.05, 1.5, "QUELQU'UN", False), (1.5, 1.95, "FRAPPE", True), (1.95, 2.55, "À LA PORTE", False),
    (2.55, 3.4, "DE TA CHAMBRE.", False),
    (5.75, 6.15, "TROIS", False), (6.15, 6.55, "PETITS", False), (6.55, 7.3, "COUPS.", False),
    (7.6, 7.9, "TU", False), (7.9, 8.2, "VIS", False), (8.2, 9.2, "SEUL.", True),
    (10.3, 10.6, "SOUS", False), (10.6, 11.0, "LA PORTE,", False), (11.0, 11.3, "UNE", False),
    (11.3, 12.0, "FEUILLE.", False),
]


def scene(cid, dur, style, body, script):
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


def head(cx, cy, r, pre):
    """Round two-tone head lying on a pillow, eyes + lids + brows + sweat (ids prefixed)."""
    return f"""
      <g id="{pre}-head">
        <circle cx="{cx}" cy="{cy}" r="{r}" fill="{SKIN}"/>
        <path d="M{cx} {cy-r} A{r} {r} 0 0 1 {cx} {cy+r} Z" fill="{SKIN_SH}"/>
        <path d="M{cx-r+6} {cy-30} Q{cx-60} {cy-r-40} {cx+40} {cy-r+4} Q{cx+r} {cy-r+20} {cx+r-10} {cy-40} Q{cx+40} {cy-r+40} {cx-r+6} {cy-30} Z" fill="#3B2A2A"/>
        <g id="{pre}-eyes">
          <circle cx="{cx-48}" cy="{cy+8}" r="22" fill="#fff"/><circle cx="{cx+48}" cy="{cy+8}" r="22" fill="#fff"/>
          <g id="{pre}-pupils"><circle cx="{cx-48}" cy="{cy+10}" r="10" fill="{INK}"/><circle cx="{cx+48}" cy="{cy+10}" r="10" fill="{INK}"/></g>
          <rect id="{pre}-lidL" x="{cx-72}" y="{cy-16}" width="48" height="0" fill="{SKIN}"/>
          <rect id="{pre}-lidR" x="{cx+24}" y="{cy-16}" width="48" height="0" fill="{SKIN_SH}"/>
        </g>
        <path id="{pre}-browL" d="M{cx-74} {cy-30} L{cx-26} {cy-26}" stroke="{INK}" stroke-width="7" stroke-linecap="round"/>
        <path id="{pre}-browR" d="M{cx+26} {cy-26} L{cx+74} {cy-30}" stroke="{INK}" stroke-width="7" stroke-linecap="round"/>
        <path id="{pre}-mouth" d="M{cx-18} {cy+70} Q{cx} {cy+66} {cx+18} {cy+70}" stroke="{INK}" stroke-width="7" fill="none" stroke-linecap="round"/>
        <path id="{pre}-sweat" d="M{cx+r-30} {cy-60} q14 26 0 36 q-14 -10 0 -36 Z" fill="#BFE3FF" opacity="0"/>
      </g>"""


# ---------- scene 1: bedroom (0 – 5.3 s) ----------
s1_style = f"""    #s1-cam {{ position:absolute; inset:0; }}
    svg {{ position:absolute; inset:0; width:100%; height:100%; }}"""
s1_body = f"""    <div id="s1-cam"><div id="s1-shake" style="position:absolute;inset:0">
    <svg viewBox="0 0 {W} {H}" data-layout-ignore>
      <defs>
        <linearGradient id="s1-wall" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{NIGHT0}"/><stop offset="1" stop-color="{NIGHT1}"/></linearGradient>
        <linearGradient id="s1-beam" x1="0" y1="0" x2="0.4" y2="1"><stop offset="0" stop-color="{MOON}" stop-opacity="0.45"/><stop offset="1" stop-color="{MOON}" stop-opacity="0"/></linearGradient>
        <linearGradient id="s1-warm" x1="1" y1="0" x2="0" y2="0"><stop offset="0" stop-color="{WARM}" stop-opacity="0.85"/><stop offset="1" stop-color="{WARM}" stop-opacity="0"/></linearGradient>
        <radialGradient id="s1-clockglow"><stop offset="0" stop-color="{RED}" stop-opacity="0.55"/><stop offset="1" stop-color="{RED}" stop-opacity="0"/></radialGradient>
      </defs>
      <rect x="-200" y="-200" width="{W+400}" height="{H+400}" fill="url(#s1-wall)"/>
      <g id="s1-world" transform="translate(-120,-430) scale(1.15)">
      <rect x="-200" y="1520" width="{W+400}" height="900" fill="#15132A"/>
      <!-- window + moon -->
      <rect x="120" y="300" width="380" height="520" rx="8" fill="#26305E" stroke="#3A3566" stroke-width="18"/>
      <circle cx="390" cy="420" r="58" fill="#E9EEFF"/>
      <path d="M310 300 V820 M120 560 H500" stroke="#3A3566" stroke-width="14"/>
      <path id="s1-curtain" d="M100 280 Q150 560 120 860 L60 860 L60 280 Z" fill="#3D2F5C"/>
      <polygon id="s1-beamp" points="140,820 500,820 820,1600 260,1600" fill="url(#s1-beam)"/>
      <!-- bed -->
      <rect x="40" y="1160" width="900" height="80" rx="30" fill="#4B3B6E"/>
      <rect x="60" y="1220" width="860" height="300" rx="40" fill="#2E2752"/>
      <ellipse cx="300" cy="1180" rx="210" ry="70" fill="#D8D4EC"/>
      {head(330, 1060, 130, "s1")}
      <path id="s1-blanket" d="M40 1200 Q300 1130 560 1190 Q760 1240 940 1180 L940 1500 L40 1500 Z" fill="#5A4A8C"/>
      <path d="M40 1200 Q300 1130 560 1190 Q760 1240 940 1180" stroke="#7666AE" stroke-width="10" fill="none"/>
      <!-- nightstand + clock -->
      <rect x="800" y="1040" width="220" height="250" rx="12" fill="#3A2F58"/>
      <circle cx="905" cy="1000" r="150" fill="url(#s1-clockglow)"/>
      <rect x="830" y="960" width="160" height="80" rx="14" fill="#141024"/>
      <text x="910" y="1015" text-anchor="middle" font-family="JetBrains Mono" font-weight="700" font-size="48" fill="{RED}">2:41</text>
      <!-- warm light from under the door, off-screen right -->
      <polygon id="s1-under" points="1080,1560 1080,1600 640,1700 760,1560" fill="url(#s1-warm)" opacity="0"/>
      </g>
    </svg>
    </div></div>"""
s1_script = f"""    // camera: slow push + drift, never still
    tl.fromTo("#s1-cam", {{ scale: 1.02, x: 0, y: 0 }}, {{ scale: 1.14, x: -40, y: -30, duration: 4.9, ease: "power1.inOut", transformOrigin: "40% 60%" }}, 0);
    tl.fromTo("#s1-curtain", {{ skewX: 0 }}, {{ skewX: 3, duration: 2.4, ease: "sine.inOut", yoyo: true, repeat: 1, transformOrigin: "100% 0%" }}, 0);
    // knocks: tiny camera jolts
    tl.set("#s1-shake", {{ y: 0 }}, 0);
    [1.5, 1.72, 1.94].forEach((t) => tl.to("#s1-shake", {{ y: 8, duration: 0.09, ease: "power2.out", yoyo: true, repeat: 1 }}, t));
    // light appears under the door (off-screen right)
    tl.fromTo("#s1-under", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.6, ease: "power2.out" }}, 2.2);
    // acting: blink, eyes widen, sweat, look at the door
    tl.fromTo(["#s1-lidL", "#s1-lidR"], {{ attr: {{ height: 0 }} }}, {{ attr: {{ height: 46 }}, duration: 0.07, ease: "power2.in", yoyo: true, repeat: 1 }}, 0.8);
    tl.fromTo("#s1-eyes", {{ scale: 1 }}, {{ scale: 1.18, duration: 0.25, ease: "back.out(2)", transformOrigin: "50% 50%" }}, 3.3);
    tl.fromTo(["#s1-browL"], {{ rotation: 0 }}, {{ rotation: -12, duration: 0.25, ease: "power2.out", transformOrigin: "100% 50%" }}, 3.3);
    tl.fromTo(["#s1-browR"], {{ rotation: 0 }}, {{ rotation: 12, duration: 0.25, ease: "power2.out", transformOrigin: "0% 50%" }}, 3.32);
    tl.fromTo("#s1-mouth", {{ attr: {{ d: "M312 1130 Q330 1126 348 1130" }} }}, {{ attr: {{ d: "M316 1134 Q330 1116 344 1134" }}, duration: 0.16, ease: "power2.out" }}, 3.4);
    tl.fromTo("#s1-sweat", {{ opacity: 0, y: 0 }}, {{ opacity: 1, y: 30, duration: 0.9, ease: "power1.in" }}, 3.8);
    tl.fromTo("#s1-pupils", {{ x: 0 }}, {{ x: -3, duration: 0.12, ease: "power2.out" }}, 4.15);
    tl.to("#s1-pupils", {{ x: 11, duration: 0.3, ease: "power3.out" }}, 4.27);
    // whip to the door (cut at the fastest frame, motion blur on the root)
    tl.to("#s1-cam", {{ x: -620, duration: 0.32, ease: "power3.in" }}, 4.98);
"""

# ---------- scene 2: the door (5.3 – 10.0 s, local time 0 – 4.7) ----------
s2_style = """    #s2-cam { position:absolute; inset:0; }
    svg { position:absolute; inset:0; width:100%; height:100%; }"""
s2_body = f"""    <div id="s2-cam"><div id="s2-shake" style="position:absolute;inset:0">
    <svg viewBox="0 0 {W} {H}" data-layout-ignore>
      <defs>
        <linearGradient id="s2-wall" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{NIGHT0}"/><stop offset="1" stop-color="{NIGHT1}"/></linearGradient>
        <linearGradient id="s2-gap" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFE0A8"/><stop offset="1" stop-color="{WARM}"/></linearGradient>
        <linearGradient id="s2-spill" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{WARM}" stop-opacity="0.7"/><stop offset="1" stop-color="{WARM}" stop-opacity="0"/></linearGradient>
        <linearGradient id="s2-moon" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{MOON}" stop-opacity="0.22"/><stop offset="1" stop-color="{MOON}" stop-opacity="0"/></linearGradient>
      </defs>
      <rect x="-300" y="-300" width="{W+600}" height="{H+600}" fill="url(#s2-wall)"/>
      <rect x="-300" y="1560" width="{W+600}" height="700" fill="#15132A"/>
      <path d="M-300 1640 H{W+300} M-300 1760 H{W+300} M-300 1900 H{W+300}" stroke="#1F1C3A" stroke-width="6"/>
      <!-- frame + door -->
      <rect x="230" y="420" width="620" height="1150" fill="#2B2448"/>
      <g id="s2-door">
        <rect x="262" y="450" width="556" height="1105" fill="#4A3A6A"/>
        <rect x="320" y="520" width="440" height="420" rx="10" fill="none" stroke="#3A2D58" stroke-width="16"/>
        <rect x="320" y="1010" width="440" height="470" rx="10" fill="none" stroke="#3A2D58" stroke-width="16"/>
        <circle cx="735" cy="1000" r="24" fill="#C9B27A"/><rect x="700" y="992" width="40" height="16" rx="8" fill="#C9B27A"/>
      </g>
      <polygon points="230,420 520,420 380,1560 230,1560" fill="url(#s2-moon)"/>
      <!-- light under the door + feet shadows -->
      <rect x="262" y="1555" width="556" height="14" fill="url(#s2-gap)"/>
      <polygon points="262,1569 818,1569 980,1760 100,1760" fill="url(#s2-spill)" opacity="0.55"/>
      <g id="s2-feet"><rect x="420" y="1555" width="70" height="14" fill="#1A1426"/><rect x="560" y="1555" width="70" height="14" fill="#1A1426"/></g>
      <!-- dust from the knocks -->
      <g id="s2-dust" opacity="0"><circle cx="300" cy="460" r="5" fill="#8C84B8"/><circle cx="520" cy="452" r="4" fill="#8C84B8"/><circle cx="760" cy="466" r="6" fill="#8C84B8"/><circle cx="640" cy="458" r="3" fill="#8C84B8"/></g>
    </svg>
    </div></div>"""
s2_script = """    // arrive from the whip: lands blurred, settles
    tl.fromTo("#s2-cam", { x: 520, scale: 1.0 }, { x: 0, duration: 0.38, ease: "power3.out" }, 0);
    tl.fromTo("#s2-cam", { scale: 1.0, y: 0 }, { scale: 1.08, y: 20, duration: 3.3, ease: "sine.inOut", transformOrigin: "50% 60%", immediateRender: false }, 0.38);
    // three knocks: door jumps, camera punches in, dust falls
    tl.set("#s2-door", { scale: 1, x: 0, svgOrigin: "540 1000" }, 0);
    tl.set("#s2-shake", { scale: 1 }, 0);
    [0.55, 0.9, 1.25].forEach((t, i) => {
      tl.to("#s2-door", { scale: 1.018, x: i % 2 ? -6 : 6, duration: 0.06, ease: "power2.out", yoyo: true, repeat: 1, svgOrigin: "540 1000" }, t);
      tl.to("#s2-shake", { scale: 1.03, duration: 0.07, ease: "power3.out", yoyo: true, repeat: 1, transformOrigin: "50% 50%" }, t);
    });
    tl.fromTo("#s2-dust", { opacity: 0, y: 0 }, { opacity: 1, y: 180, duration: 1.4, ease: "power1.in" }, 0.6);
    tl.to("#s2-dust", { opacity: 0, duration: 0.3 }, 2.0);
    // the feet shift: someone is still there
    tl.fromTo("#s2-feet", { x: 0 }, { x: 40, duration: 0.5, ease: "power2.inOut" }, 3.2);
    // push down to the gap, accelerating (cut at the fastest frame)
    tl.to("#s2-cam", { scale: 2.6, y: -1250, duration: 1.0, ease: "power3.in", transformOrigin: "50% 82%" }, 3.7);
"""

# ---------- scene 3: the paper (10.0 – 15.0 s, local 0 – 5) ----------
s3_style = f"""    #s3-cam {{ position:absolute; inset:0; }}
    svg {{ position:absolute; inset:0; width:100%; height:100%; }}
    #s3-note {{ position:absolute; left:150px; top:430px; width:740px; height:820px; background:#EFE6D2; border-radius:6px;
      box-shadow: 0 40px 90px rgba(0,0,0,.55); display:flex; flex-direction:column; align-items:center; justify-content:center; gap:60px; }}
    #s3-rule {{ font-family:'Oswald'; font-weight:700; font-size:104px; color:{INK}; letter-spacing:.04em; }}
    #s3-line {{ font-family:'EB Garamond'; font-style:italic; font-size:100px; color:#8E1B22; text-align:center; line-height:1.05; }}"""
s3_body = f"""    <div id="s3-cam" data-layout-allow-overflow>
    <svg viewBox="0 0 {W} {H}" data-layout-ignore>
      <defs>
        <linearGradient id="s3-floor" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1E1A36"/><stop offset="1" stop-color="#0E0C1C"/></linearGradient>
        <linearGradient id="s3-spill" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{WARM}" stop-opacity="0.9"/><stop offset="1" stop-color="{WARM}" stop-opacity="0"/></linearGradient>
      </defs>
      <rect x="-200" y="-200" width="{W+400}" height="{H+400}" fill="#0E0C1C"/>
      <rect x="-200" y="0" width="{W+400}" height="760" fill="#3A2D58"/>
      <rect x="-200" y="740" width="{W+400}" height="40" fill="#FFE0A8"/>
      <rect id="s3-footL" x="200" y="740" width="230" height="40" fill="#1A1426"/>
      <rect id="s3-footR" x="600" y="740" width="230" height="40" fill="#1A1426"/>
      <polygon id="s3-glow" points="-200,780 {W+200},780 {W+600},1900 -600,1900" fill="url(#s3-spill)" opacity="0.6"/>
      <rect x="-200" y="780" width="{W+400}" height="1300" fill="url(#s3-floor)" opacity="0.55"/>
      <path d="M-200 1000 H{W+200} M-200 1300 H{W+200} M-200 1700 H{W+200}" stroke="#1F1C3A" stroke-width="8"/>
      <polygon id="s3-paper" points="380,770 700,770 760,900 320,900" fill="#EFE6D2"/>
    </svg>
    <div id="s3-note" data-layout-allow-overflow>
      <div id="s3-rule">RÈGLE N°1</div>
      <div id="s3-line">Ne réponds<br>pas.</div>
    </div>
    </div>"""
s3_script = """    // camera keeps falling from the cut, then settles on the gap
    tl.fromTo("#s3-cam", { scale: 1.25, y: -120 }, { scale: 1.0, y: 0, duration: 0.5, ease: "power3.out", transformOrigin: "50% 45%" }, 0);
    tl.fromTo("#s3-cam", { x: 0 }, { x: -12, duration: 2, ease: "sine.inOut", immediateRender: false }, 0.5);
    // the paper slides in from under the door
    tl.fromTo("#s3-paper", { y: -140, scaleY: 0.1 }, { y: 0, scaleY: 1, duration: 0.7, ease: "power2.out", svgOrigin: "540 770" }, 0.4);
    tl.fromTo("#s3-paper", { y: 0 }, { y: 40, duration: 0.5, ease: "power1.inOut", immediateRender: false }, 1.1);
    // object becomes the world: the note rises to fill the frame
    tl.fromTo("#s3-note", { scale: 0.32, y: 300, rotationX: 70, opacity: 0 }, { scale: 1, y: 0, rotationX: 0, opacity: 1, duration: 0.75, ease: "power2.inOut", transformPerspective: 1400 }, 1.95);
    tl.to("#s3-paper", { opacity: 0, duration: 0.2 }, 2.0);
    tl.fromTo("#s3-rule", { opacity: 0, filter: "blur(8px)" }, { opacity: 1, filter: "blur(0px)", duration: 0.18, ease: "power4.out" }, 2.6);
    tl.fromTo("#s3-line", { opacity: 0, filter: "blur(8px)" }, { opacity: 1, filter: "blur(0px)", duration: 0.2, ease: "power4.out" }, 2.85);
    // the note drifts (camera never still), then the light under the door goes out
    tl.fromTo("#s3-note", { rotation: 0 }, { rotation: -2, duration: 2.1, ease: "sine.inOut", immediateRender: false }, 2.7);
    tl.to(["#s3-glow"], { opacity: 0, duration: 0.15 }, 4.4);
    tl.to("#s3-note", { filter: "brightness(0.45)", duration: 0.15 }, 4.4);
"""

# ---------- overlay: clock bar + grain + vignette (whole film) ----------
secs = range(7, 7 + DUR + 1)
digits = "\n".join(f'      <span id="ov-s{s}" class="ov-sec">{s:02d}</span>' for s in secs)
ov_style = """    #ov-bar { position:absolute; left:0; right:0; top:310px; display:flex; flex-direction:column; align-items:center; gap:6px; }
    #ov-room { font-family:'Oswald'; font-weight:700; font-size:30px; letter-spacing:.35em; color:rgba(255,255,255,.7); }
    #ov-time { font-family:'JetBrains Mono'; font-weight:700; font-size:64px; color:#fff; text-shadow:0 0 18px rgba(224,48,58,.55); display:flex; }
    .ov-sec { position:absolute; opacity:0; }
    #ov-secs { position:relative; width:78px; }
    #ov-vig { position:absolute; inset:0; background:radial-gradient(ellipse at 50% 45%, rgba(0,0,0,0) 45%, rgba(6,4,16,.78) 100%); }
    #ov-grain { position:absolute; inset:-40px; opacity:.13; mix-blend-mode:overlay; }"""
ov_body = f"""    <svg id="ov-grain" viewBox="0 0 {W+80} {H+80}" data-layout-ignore><filter id="ov-noise"><feTurbulence id="ov-turb" type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed="1"/></filter><rect width="100%" height="100%" filter="url(#ov-noise)"/></svg>
    <div id="ov-vig" data-layout-ignore></div>
    <div id="ov-bar">
      <div id="ov-room">CHAMBRE</div>
      <div id="ov-time">02:41:<span id="ov-secs">
{digits}
      </span></div>
    </div>"""
ticks = "\n".join(f'    tl.set("#ov-s{s}", {{ opacity: 1 }}, {i}); tl.set("#ov-s{s}", {{ opacity: 0 }}, {i + 1});' for i, s in enumerate(secs))
grain = "\n".join(f'    tl.set("#ov-turb", {{ attr: {{ seed: {k % 97 + 1} }} }}, {k / 12:.4f}); tl.set("#ov-grain", {{ x: {((k * 37) % 40) - 20}, y: {((k * 53) % 40) - 20} }}, {k / 12:.4f});' for k in range(DUR * 12))
ov_script = f"""{ticks}
{grain}
    tl.fromTo("#ov-bar", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.25 }}, 0.0);
    tl.to("#ov-bar", {{ opacity: 0, duration: 0.15 }}, 14.4);
"""

# ---------- captions ----------
cap_style = f"""    .cap {{ position:absolute; left:150px; right:150px; top:1020px; text-align:center; opacity:0; visibility:hidden;
      font-family:'Oswald'; font-weight:700; font-size:104px; letter-spacing:.01em; color:#fff;
      -webkit-text-stroke: 10px {INK}; paint-order: stroke fill; text-shadow: 0 8px 22px rgba(0,0,0,.6); }}
    .cap.red {{ color:{RED}; }}"""
cap_body = "\n".join(f'    <div id="cap-{i}" class="cap{" red" if red else ""}">{w}</div>' for i, (a, b, w, red) in enumerate(CAPS))
cap_script = "\n".join(
    f'    tl.set("#cap-{i}", {{ visibility: "visible" }}, {a}); tl.fromTo("#cap-{i}", {{ opacity: 0, scale: 1.18 }}, {{ opacity: 1, scale: 1, duration: 0.09, ease: "power3.out" }}, {a});'
    f' tl.to("#cap-{i}", {{ opacity: 0, duration: 0.06, ease: "power2.in" }}, {b - 0.06:.3f}); tl.set("#cap-{i}", {{ opacity: 0, visibility: "hidden" }}, {b});'
    for i, (a, b, w, red) in enumerate(CAPS))

files = {
    "compositions/s1-chambre.html": scene("s1-chambre", 5.3, s1_style, s1_body, s1_script),
    "compositions/s2-porte.html": scene("s2-porte", 4.7, s2_style, s2_body, s2_script),
    "compositions/s3-feuille.html": scene("s3-feuille", 5.0, s3_style, s3_body, s3_script),
    "compositions/overlay.html": scene("overlay", DUR, ov_style, ov_body, ov_script),
    "compositions/captions.html": scene("captions", DUR, cap_style, cap_body, cap_script),
}
for p, s in files.items():
    (OUT / p).write_text(s)

host = lambda cid, a, d, track, kind="graphics", z=1: (
    f'      <div id="{cid}" data-composition-id="{cid}" data-composition-src="compositions/{cid}.html" data-start="{a}" data-duration="{d}" '
    f'data-track-index="{track}" data-track-kind="{kind}" data-width="{W}" data-height="{H}" style="z-index:{z}"></div>')
index = f"""<!doctype html>
<html lang="fr" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={W}, height={H}" />
    {GSAP}
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: {W}px; height: {H}px; overflow: hidden; background: {NIGHT0}; }}
      #bg {{ position: absolute; inset: 0; background: {NIGHT0}; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-width="{W}" data-height="{H}" data-fps="60" data-motion-blur="on">
      <div id="bg" data-layout-ignore></div>
{host("s1-chambre", 0, 5.3, 1, z=1)}
{host("s2-porte", 5.3, 4.7, 1, z=1)}
{host("s3-feuille", 10.0, 5.0, 1, z=1)}
{host("overlay", 0, DUR, 2, z=5)}
{host("captions", 0, DUR, 3, "captions", z=6)}
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
"""
(OUT / "index.html").write_text(index)
print("wrote", ", ".join(["index.html", *files]))
