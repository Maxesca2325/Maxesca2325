"""Builds video 1 ("Sispann peye pou flyer ou") from episodes/v01/timing.json.
Writes index.html, compositions/captions.html and episodes/v01/sfx.json (then run tools/mix.py v01).
Every animation is anchored to a WORD of the voice, so a new recording only needs:
  python3 ../scripts/import_voice.py v01 <audio> --lang ht ; python3 tools/build_v01.py ; python3 tools/mix.py v01
Run from tyolika/.  Style rules: ../styles/tyolika.md
"""
import json, re
from pathlib import Path

EP = "v01"
ROOT = Path(__file__).resolve().parent.parent
tim = json.loads((ROOT / "episodes" / EP / "timing.json").read_text())
SH = {s["id"]: s for s in tim["shots"]}
DUR = round(tim["total"] + 1.0, 2)
W, H = 1080, 1920
BG, ACC, RED, TXT, MUT = "#121212", "#39FF14", "#FF3B3B", "#F5F5F5", "#9A9A9A"


def w(shot, i):  # start time of word i of shot
    return SH[shot]["words"][i]["start"]


def we(shot, i):
    return SH[shot]["words"][i]["end"]


def st(shot):
    return SH[shot]["words"][0]["start"]


def en(shot):
    return SH[shot]["words"][-1]["end"]


J, SFX = [], []


def js(s):
    J.append(s)


def sfx(t, name, gain=0.5):
    SFX.append({"t": round(max(0, t), 3), "name": name, "gain": gain})


f = lambda x: f"{x:.3f}"
_rot = {"whoosh": 0}


def whoosh(t, gain=0.45):
    names = ["whoosh", "whoosh-short", "whoosh-cinematic"]
    sfx(t - 0.08, names[_rot["whoosh"] % 3], gain)
    _rot["whoosh"] += 1


# ---------------------------------------------------------------- reusable pieces
ICON_OK = f'<svg viewBox="0 0 24 24" class="ico"><circle cx="12" cy="12" r="11" fill="{ACC}"/><path d="M6.5 12.5l3.6 3.6 7.4-8" stroke="#0b0b0b" stroke-width="2.8" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>'
ICON_NO = f'<svg viewBox="0 0 24 24" class="ico"><circle cx="12" cy="12" r="11" fill="{RED}"/><path d="M7.5 7.5l9 9M16.5 7.5l-9 9" stroke="#fff" stroke-width="2.8" stroke-linecap="round"/></svg>'


def art(pre):
    """Party background drawn in code: night sky to sunset, sun, palms, neon line, bokeh."""
    dots = "".join(
        f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}" opacity="{o}"/>'
        for x, y, r, c, o in [(70, 120, 26, ACC, .25), (430, 90, 18, "#ff6ad5", .35), (360, 210, 34, "#ffd36a", .18),
                              (120, 300, 14, "#ff6ad5", .4), (480, 330, 22, ACC, .22), (250, 60, 12, "#ffffff", .5)])
    palm = lambda x, s, flip: (f'<g transform="translate({x},560) scale({s * (-1 if flip else 1)},{s})" fill="#08060f">'
                               '<path d="M-6 0 Q4 -120 -2 -230 L8 -230 Q14 -120 6 0 Z"/>'
                               '<path d="M2 -230 Q-70 -270 -130 -220 Q-70 -250 2 -222 Z"/><path d="M2 -230 Q70 -280 140 -230 Q70 -255 2 -222 Z"/>'
                               '<path d="M2 -232 Q-40 -300 -100 -300 Q-40 -285 2 -226 Z"/><path d="M2 -232 Q50 -310 110 -300 Q50 -288 2 -226 Z"/></g>')
    return f'''<svg class="art" viewBox="0 0 540 760" preserveAspectRatio="xMidYMid slice" data-layout-ignore>
      <defs><linearGradient id="{pre}-sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#090b24"/><stop offset=".45" stop-color="#3b1460"/><stop offset=".72" stop-color="#c2366a"/><stop offset="1" stop-color="#ff9a4a"/></linearGradient>
      <radialGradient id="{pre}-sun"><stop offset="0" stop-color="#ffd86b"/><stop offset=".6" stop-color="#ff7a45"/><stop offset="1" stop-color="#ff7a45" stop-opacity="0"/></radialGradient></defs>
      <rect width="540" height="760" fill="url(#{pre}-sky)"/>{dots}
      <circle cx="270" cy="560" r="170" fill="url(#{pre}-sun)"/>
      <rect y="600" width="540" height="160" fill="#0b0716"/>
      <path d="M0 600 Q270 585 540 600" stroke="{ACC}" stroke-width="4" fill="none" opacity=".9"/>
      {palm(70, 1.1, False)}{palm(470, 1.25, True)}{palm(400, .8, False)}
    </svg>'''


def flyer(fid, garbled=False, low=False):
    t1, t2, t3, t4 = ("BÈL FÈT LAKAY", "SAMDI 20 DESANM · 8È DISWA", "PÉTION-VILLE", "VIN DANSE AK NOU!")
    if garbled:
        t1, t2, t3, t4 = ("BÈL FÈTT LAKYA", "SAMDDI 2O DSANM · 8È DSWA", "PÉTOIN-VLIE", "VIN DASNE AK NUO!")
    cls = "fly low" if low else "fly"
    return f'''<div id="{fid}" class="{cls}" data-layout-allow-overlap>{art(fid)}
      <div class="fly-txt" data-layout-ignore><div class="f1">{t1.replace(" ", "<br>", 2) if not garbled else t1}</div><div class="f2">{t2}</div><div class="f3">{t3}</div><div class="f4">{t4}</div></div></div>'''


FINGER = '<div class="finger" id="{id}"><div class="ring"></div></div>'

# ---------------------------------------------------------------- times
T = {k: st(k) for k in SH}
END = DUR

# ---------------------------------------------------------------- HTML
prompt_txt = "Flyer pou: BÈL FÈT LAKAY, samdi 20 desanm, Pétion-Ville. Ban m 3 liy kout."
prompt_spans = "".join(f'<span class="ch" id="pc{i}">{c if c != " " else "&nbsp;"}</span>' for i, c in enumerate(prompt_txt))

html = f'''<!doctype html>
<html lang="ht" data-resolution="portrait">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width={W}, height={H}" />
<script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
<style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
html, body {{ width:{W}px; height:{H}px; overflow:hidden; background:{BG}; }}
#bg {{ position:absolute; inset:0; background:
   radial-gradient(ellipse 70% 55% at 50% 38%, rgba(57,255,20,.07), rgba(0,0,0,0) 70%),
   linear-gradient(rgba(255,255,255,.04) 1px, transparent 1px) 0 0/60px 60px,
   linear-gradient(90deg, rgba(255,255,255,.04) 1px, transparent 1px) 0 0/60px 60px, {BG}; }}
#vig {{ position:absolute; inset:0; background:radial-gradient(ellipse 85% 70% at 50% 45%, rgba(0,0,0,0) 55%, rgba(7,7,7,.92) 100%); pointer-events:none; }}
#grain {{ position:absolute; inset:-40px; opacity:.07; mix-blend-mode:overlay; }}
#cam {{ position:absolute; inset:0; transform-origin:50% 36%; }}
.sc {{ position:absolute; inset:0; opacity:0; }}
.ico {{ width:44px; height:44px; flex:none; }}
/* flyer */
#fly {{ left:270px; top:250px; }}
.fly {{ position:absolute; width:540px; height:760px; border-radius:28px; overflow:hidden; box-shadow:0 40px 110px rgba(0,0,0,.65), 0 0 0 2px rgba(255,255,255,.06); }}
.fly .art {{ position:absolute; inset:0; width:100%; height:100%; }}
.fly-txt {{ position:absolute; inset:0; padding:70px 40px; display:flex; flex-direction:column; align-items:center; text-align:center; }}
.f1 {{ font-family:'Montserrat'; font-weight:900; font-size:92px; line-height:.92; color:#fff; letter-spacing:-.02em; text-shadow:0 6px 30px rgba(0,0,0,.55); }}
.f2 {{ margin-top:26px; font-family:'Inter'; font-weight:700; font-size:26px; color:{ACC}; letter-spacing:.06em; }}
.f3 {{ margin-top:10px; font-family:'Inter'; font-weight:700; font-size:24px; color:#fff; letter-spacing:.2em; }}
.f4 {{ position:absolute; left:0; right:0; bottom:56px; font-family:'Playfair Display'; font-style:italic; font-weight:700; font-size:44px; color:#fff; }}
.fly.low .f1, .fly.low .f3, .fly.low .f4 {{ color:#8d7a9a; text-shadow:none; }} .fly.low .f2 {{ color:#a0789a; }}
.fly.low .art {{ filter:saturate(.35) brightness(1.25); }}
/* phone */
#pwrap {{ position:absolute; left:0; top:0; width:1080px; height:1920px; transform:scale(.86); transform-origin:540px 305px; }}
#phone {{ position:absolute; left:280px; top:305px; width:520px; height:880px; border-radius:66px; background:#050505; box-shadow:0 0 0 3px #2c2c2c, 0 0 0 12px #141414, 0 50px 140px rgba(0,0,0,.75); opacity:0; }}
#screen {{ position:absolute; inset:14px; border-radius:54px; overflow:hidden; background:#171717; }}
.notch {{ position:absolute; top:16px; left:50%; width:120px; margin-left:-60px; height:30px; border-radius:16px; background:#050505; z-index:9; }}
.pane {{ position:absolute; inset:0; opacity:0; }}
/* chat */
.bar {{ position:absolute; left:0; right:0; top:0; height:118px; padding:62px 30px 0; font-family:'Inter'; font-weight:700; font-size:26px; color:#fff; border-bottom:1px solid #2a2a2a; display:flex; gap:12px; align-items:center; }}
.dot {{ width:14px; height:14px; border-radius:7px; background:{ACC}; }}
#inp {{ position:absolute; left:20px; right:20px; bottom:26px; min-height:120px; border-radius:30px; background:#262626; padding:22px 96px 22px 24px; font-family:'Inter'; font-weight:400; font-size:23px; line-height:1.35; color:#eee; }}
.ch {{ opacity:0; }}
#send {{ position:absolute; right:34px; bottom:44px; width:64px; height:64px; border-radius:32px; background:{ACC}; }}
#send:after {{ content:''; position:absolute; left:22px; top:18px; border:12px solid transparent; border-left:20px solid #0b0b0b; transform:rotate(-90deg); transform-origin:10px 14px; }}
#umsg {{ position:absolute; right:22px; top:150px; width:380px; border-radius:26px 26px 6px 26px; background:#2f2f2f; padding:18px 22px; font-family:'Inter'; font-size:21px; line-height:1.35; color:#ddd; opacity:0; }}
#bot {{ position:absolute; left:22px; top:330px; width:430px; display:flex; flex-direction:column; gap:16px; }}
.bl {{ display:flex; align-items:center; gap:14px; font-family:'Inter'; font-weight:700; font-size:25px; color:#fff; opacity:0; }}
.bl .ico {{ width:34px; height:34px; }}
/* step number */
.step {{ position:absolute; left:0; right:0; top:560px; text-align:center; font-family:'Montserrat'; font-weight:900; font-size:330px; line-height:1; color:{ACC}; text-shadow:0 0 60px rgba(57,255,20,.45); opacity:0; }}
.steplab {{ position:absolute; left:0; right:0; top:500px; text-align:center; font-family:'Inter'; font-weight:700; font-size:40px; letter-spacing:.5em; color:#fff; opacity:0; }}
.pill {{ position:absolute; left:0; right:0; margin:0 auto; width:380px; text-align:center; top:236px; padding:10px 0; border-radius:40px; border:2px solid {ACC}; font-family:'Inter'; font-weight:700; font-size:26px; letter-spacing:.18em; color:{ACC}; background:rgba(18,18,18,.85); opacity:0; }}
/* chips */
.chip {{ position:absolute; padding:16px 26px; border-radius:22px; background:rgba(28,28,28,.92); border:2px solid #333; font-family:'Montserrat'; font-weight:900; font-size:34px; color:#fff; opacity:0; display:flex; gap:12px; align-items:center; }}
.chip b {{ color:{ACC}; }}
/* image generation */
#gen {{ position:absolute; left:150px; top:300px; width:720px; height:720px; border-radius:36px; background:#1b1b1b; border:2px solid #2d2d2d; overflow:hidden; }}
#gen .head {{ position:absolute; left:28px; right:28px; top:24px; font-family:'Inter'; font-weight:700; font-size:24px; color:{MUT}; display:flex; justify-content:space-between; }}
#genq {{ position:absolute; left:28px; right:28px; top:70px; padding:14px 20px; border-radius:18px; background:#262626; font-family:'Inter'; font-size:23px; color:#eee; }}
#genart {{ position:absolute; left:28px; right:28px; top:150px; height:480px; border-radius:22px; overflow:hidden; background:#222; }}
#genart .art {{ position:absolute; inset:0; width:100%; height:100%; }}
#genbar {{ position:absolute; left:28px; right:28px; bottom:34px; height:12px; border-radius:6px; background:#2b2b2b; overflow:hidden; }}
#genfill {{ position:absolute; left:0; top:0; bottom:0; width:100%; background:{ACC}; transform-origin:0 50%; }}
.badge {{ position:absolute; left:-20px; right:-20px; padding:12px 0; white-space:nowrap; display:flex; gap:10px; justify-content:center; align-items:center; font-family:'Inter'; font-weight:700; font-size:22px; letter-spacing:.06em; color:#fff; }}
.badge .ico {{ width:34px; height:34px; }}
.squig {{ position:absolute; height:10px; background:repeating-linear-gradient(135deg, {RED} 0 6px, transparent 6px 12px); opacity:0; }}
#stamp {{ position:absolute; left:0; right:0; top:880px; text-align:center; font-family:'Montserrat'; font-weight:900; font-size:120px; color:{RED}; -webkit-text-stroke:8px #121212; paint-order:stroke fill; letter-spacing:.04em; opacity:0; }}
/* editor */
#edbar {{ position:absolute; left:0; right:0; top:0; height:118px; padding:62px 30px 0; font-family:'Inter'; font-weight:700; font-size:26px; color:#fff; display:flex; justify-content:space-between; background:linear-gradient(90deg,#1d1640,#13263a); }}
#edbar i {{ font-style:normal; color:{ACC}; }}
#canvas {{ position:absolute; left:56px; top:160px; width:380px; height:535px; border:3px dashed #444; border-radius:8px; overflow:hidden; background:#202020; }}
#cart {{ position:absolute; inset:0; opacity:0; }} #cart .art {{ width:100%; height:100%; }}
.ct {{ position:absolute; left:0; right:0; text-align:center; color:#fff; opacity:0; }}
#ct1 {{ top:46px; font-family:'Montserrat'; font-weight:900; font-size:62px; line-height:.92; letter-spacing:-.02em; text-shadow:0 4px 18px rgba(0,0,0,.6); }}
#ct2 {{ top:200px; font-family:'Inter'; font-weight:700; font-size:18px; color:{ACC}; letter-spacing:.06em; }}
#ct3 {{ top:232px; font-family:'Inter'; font-weight:700; font-size:17px; letter-spacing:.2em; }}
#tray {{ position:absolute; left:20px; right:20px; bottom:24px; height:130px; border-radius:24px; background:#232323; }}
#thumb {{ position:absolute; left:36px; bottom:40px; width:70px; height:98px; border-radius:10px; overflow:hidden; }}
#thumb .art {{ width:100%; height:100%; }}
#tbtn {{ position:absolute; left:130px; bottom:46px; width:86px; height:86px; border-radius:20px; background:#333; font-family:'Playfair Display'; font-weight:700; font-size:50px; color:#fff; text-align:center; line-height:86px; }}
#dl {{ position:absolute; right:40px; bottom:52px; padding:18px 28px; border-radius:20px; background:{ACC}; font-family:'Inter'; font-weight:700; font-size:24px; color:#0b0b0b; opacity:0; }}
#drag {{ position:absolute; left:36px; top:714px; width:70px; height:98px; border-radius:10px; overflow:hidden; opacity:0; transform-origin:0 0; }}
#drag .art {{ width:100%; height:100%; }}
/* fonts */
.fc {{ position:absolute; left:555px; width:330px; padding:22px 26px; border-radius:24px; background:#1c1c1c; border:2px solid #333; display:flex; justify-content:space-between; align-items:center; opacity:0; }}
.fc .nm {{ color:#fff; }} .fc small {{ display:block; margin-top:6px; font-family:'Inter'; font-weight:700; font-size:20px; letter-spacing:.14em; color:{MUT}; }}
/* contrast */
#cmpL, #cmpR {{ position:absolute; top:380px; width:360px; height:507px; }}
#cmpL {{ left:130px; }} #cmpR {{ left:530px; }}
#cmpL .fly, #cmpR .fly {{ transform:scale(.6667); transform-origin:0 0; }}
.cmpb {{ position:absolute; left:0; right:0; top:-74px; }}
/* end */
#counter {{ position:absolute; left:0; right:0; top:500px; text-align:center; font-family:'Montserrat'; font-weight:900; color:#fff; }}
#cA, #cB {{ font-size:140px; line-height:1.02; opacity:0; }} #cB {{ color:{ACC}; text-shadow:0 0 50px rgba(57,255,20,.4); }}
#file {{ position:absolute; left:330px; top:960px; padding:16px 24px; border-radius:18px; background:#232323; border:2px solid {ACC}; font-family:'JetBrains Mono'; font-weight:700; font-size:24px; color:#fff; opacity:0; }}
#save {{ position:absolute; left:760px; top:560px; width:130px; height:130px; border-radius:65px; background:#1d1d1d; border:2px solid #333; opacity:0; }}
#save svg {{ position:absolute; left:33px; top:30px; width:64px; height:72px; }}
#handle {{ position:absolute; left:0; right:0; top:930px; text-align:center; font-family:'Montserrat'; font-weight:900; font-size:56px; color:#fff; opacity:0; }}
#handle span {{ color:{ACC}; }}
#p2 {{ position:absolute; left:50%; top:1000px; margin-left:-150px; width:300px; text-align:center; padding:14px 0; border-radius:40px; background:{ACC}; font-family:'Montserrat'; font-weight:900; font-size:34px; color:#0b0b0b; opacity:0; }}
/* finger */
.finger {{ position:absolute; left:0; top:0; width:84px; height:84px; margin:-42px 0 0 -42px; border-radius:42px; background:rgba(255,255,255,.88); box-shadow:0 10px 30px rgba(0,0,0,.5); opacity:0; z-index:50; }}
.finger .ring {{ position:absolute; inset:-14px; border-radius:60px; border:4px solid {ACC}; opacity:0; }}
#flash {{ position:absolute; inset:0; background:#fff; opacity:0; pointer-events:none; }}
#cap {{ position:absolute; inset:0; }}
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-width="{W}" data-height="{H}" data-fps="60">
 <div id="bg"></div>
 <div id="cam" data-layout-allow-overlap>

  <!-- 1-2 hook: the result first -->
  <div id="sc1" class="sc" style="z-index:5">
   {flyer("fly")}
   <div id="tag" style="position:absolute;left:600px;top:640px;width:250px;padding:18px 0;border-radius:20px;background:{RED};text-align:center;font-family:'Montserrat';font-weight:900;font-size:54px;color:#fff;box-shadow:0 18px 50px rgba(0,0,0,.5)">PRI: $$$</div>
  </div>

  <!-- phone (shots 2-4, 8-11) -->
  <div id="pwrap" data-layout-allow-overlap><div id="phone"><div id="screen"><div class="notch"></div>
    <div id="pChat" class="pane">
      <div class="bar"><div class="dot"></div>ChatGPT</div>
      <div id="umsg">{prompt_txt}</div>
      <div id="bot">
        <div class="bl" id="bl1">{ICON_OK}BÈL FÈT LAKAY</div>
        <div class="bl" id="bl2">{ICON_OK}Samdi 20 desanm · 8è diswa</div>
        <div class="bl" id="bl3">{ICON_OK}Vin danse ak nou!</div>
      </div>
      <div id="inp">{prompt_spans}</div><div id="send"></div>
    </div>
    <div id="pEd" class="pane">
      <div id="edbar"><span>Canva</span><i>Flyer</i></div>
      <div id="canvas"><div id="cart">{art("cart")}</div>
        <div class="ct" id="ct1">BÈL FÈT<br>LAKAY</div><div class="ct" id="ct2">SAMDI 20 DESANM · 8È DISWA</div><div class="ct" id="ct3">PÉTION-VILLE</div></div>
      <div id="tray"></div><div id="thumb">{art("thumb")}</div><div id="tbtn">T</div><div id="dl">Telechaje · PNG</div>
      <div id="drag">{art("drag")}</div>
    </div>
  </div></div></div>

  <div class="chip" id="chIA" style="left:140px;top:400px"><b>IA</b></div>
  <div class="chip" id="chMin" style="left:670px;top:520px">3 <b>MIN</b></div>
  <div class="chip" id="chTel" style="left:130px;top:760px;font-size:28px">TELEFÒN</div>

  <div class="steplab" id="lab1">ETAP</div><div class="step" id="n1">01</div>
  <div class="steplab" id="lab2">ETAP</div><div class="step" id="n2">02</div>
  <div class="steplab" id="lab3">ETAP</div><div class="step" id="n3">03</div>
  <div class="pill" id="pill1">ETAP 1 · TÈKS</div>
  <div class="pill" id="pill2">ETAP 2 · IMAJ</div>
  <div class="pill" id="pill3">ETAP 3 · CANVA</div>

  <!-- 5 image generation -->
  <div id="sc5" class="sc">
   <div id="gen"><div class="head"><span>IA · Imaj</span><span id="pct">100%</span></div>
     <div id="genq">Background fèt, nwit, palmis, neon vèt</div>
     <div id="genart">{art("gen")}</div><div id="genbar"><div id="genfill"></div></div></div>
  </div>

  <!-- 6-7 background only vs full flyer -->
  <div id="sc6" class="sc">
   <div id="cardA" style="position:absolute;left:130px;top:380px;width:360px;height:507px">
     <div class="badge" style="top:-74px;color:{ACC}">{ICON_OK}BACKGROUND SÈLMAN</div>
     <div style="position:absolute;inset:0;border-radius:24px;overflow:hidden;box-shadow:0 30px 80px rgba(0,0,0,.6)">{art("ca")}</div>
     <div id="ringA" style="position:absolute;inset:-10px;border-radius:32px;border:5px solid {ACC};opacity:0"></div></div>
   <div id="cardB" style="position:absolute;left:530px;top:380px;width:360px;height:507px;transform-origin:50% 40%">
     <div class="badge" style="top:-74px;color:{RED}">{ICON_NO}FLYER KONPLÈ</div>
     <div style="position:absolute;left:0;top:0;width:540px;height:760px;transform:scale(.6667);transform-origin:0 0">{flyer("flyB", garbled=True)}</div>
     <div class="squig" id="sq1" style="left:30px;top:96px;width:300px"></div>
     <div class="squig" id="sq2" style="left:30px;top:206px;width:300px"></div>
     <div class="squig" id="sq3" style="left:70px;top:482px;width:220px"></div></div>
   <div id="stamp">FOT!</div>
  </div>

  <!-- 9 fonts -->
  <div class="fc" id="fc1" style="top:300px"><div class="nm" style="font-family:'Montserrat';font-weight:900;font-size:44px">Aa Gwo<small>TIT</small></div>{ICON_OK}</div>
  <div class="fc" id="fc2" style="top:460px"><div class="nm" style="font-family:'Inter';font-weight:400;font-size:40px">Aa Senp<small>RÈS LA</small></div>{ICON_OK}</div>
  <div class="fc" id="fc3" style="top:620px"><div class="nm" style="font-family:'Playfair Display';font-style:italic;font-size:40px">Aa Fancy<small>3YÈM FONT</small></div>{ICON_NO}</div>

  <!-- 10 contrast -->
  <div id="sc10" class="sc">
   <div id="cmpL"><div class="badge cmpb" style="color:{RED}">{ICON_NO}KONTRAS FÈB</div>{flyer("flyL", low=True)}</div>
   <div id="cmpR"><div class="badge cmpb" style="color:{ACC}">{ICON_OK}KONTRAS FÒ</div>{flyer("flyR")}</div>
  </div>

  <!-- 11-12 end -->
  <div id="file">bel-fet-lakay.png</div>
  <div id="counter"><div id="cA">3 MINIT</div><div id="cB">0 GOUD</div></div>
  <div id="sc12" class="sc">
   <div style="position:absolute;left:315px;top:290px;width:450px;height:633px"><div style="position:absolute;left:0;top:0;width:540px;height:760px;transform:scale(.8333);transform-origin:0 0">{flyer("flyE")}</div></div>
   <div id="save"><svg viewBox="0 0 64 72"><path id="savep" d="M8 4h48v64L32 50 8 68Z" fill="none" stroke="#fff" stroke-width="6" stroke-linejoin="round"/></svg></div>
   <div id="handle">SWIV <span>@tyolika</span></div>
   <div id="p2">PATI 2 →</div>
  </div>

  {FINGER.format(id="fg")}
 </div>
 <svg id="grain" viewBox="0 0 1160 2000" data-layout-ignore><filter id="gnoise"><feTurbulence id="gturb" type="fractalNoise" baseFrequency="0.85" numOctaves="2" seed="1"/></filter><rect width="100%" height="100%" filter="url(#gnoise)"/></svg>
 <div id="vig" data-layout-ignore></div>
 <div id="flash" data-layout-ignore></div>
 <div id="cap" data-composition-id="captions" data-composition-src="compositions/captions.html" data-start="0" data-duration="{DUR}" data-track-index="3" data-track-kind="captions" data-width="{W}" data-height="{H}" style="z-index:20"></div>
 <audio id="mix" class="clip" src="assets/{EP}_mix.wav" data-start="0" data-duration="{DUR}" data-track-index="4" data-volume="1"></audio>
</div>
<script>
window.__timelines = window.__timelines || {{}};
const tl = gsap.timeline({{ paused: true }});
__JS__
window.__timelines["main"] = tl;
</script>
</body>
</html>
'''

# ---------------------------------------------------------------- animation
P = lambda s: js(s)

# camera: continuous drift (never still) — alternate slow push / pull per shot
cuts = [0.0] + [T[k] - 0.12 for k in range(2, 13)] + [END]
for i in range(len(cuts) - 1):
    a, b = cuts[i], cuts[i + 1]
    s0, s1 = (1.0, 1.035) if i % 2 == 0 else (1.035, 1.0)
    x0, x1 = (-6, 6) if i % 3 else (6, -6)
    P(f'tl.fromTo("#cam", {{scale:{s0}, x:{x0}, y:0}}, {{scale:{s1}, x:{x1}, y:-8, duration:{f(b - a)}, ease:"sine.inOut", immediateRender:{"true" if i == 0 else "false"}}}, {f(a)});')


def kick(sel, t, amt=1.08):
    P(f'tl.to("{sel}", {{scale:{amt}, duration:0.12, ease:"expo.out"}}, {f(t)}); tl.to("{sel}", {{scale:1, duration:0.55, ease:"power2.inOut"}}, {f(t + 0.12)});')


def ph(x, y):
    """frame coords drawn for the unscaled phone (top 232) -> real frame coords (phone top 305, scale .86)"""
    return round(540 + (x - 540) * .86), round(305 + (y - 232) * .86)


def finger_to(x, y, t, d=0.35):
    P(f'tl.to("#fg", {{x:{x}, y:{y}, duration:{d}, ease:"power2.inOut"}}, {f(t)});')


def tap(t, soft=False):
    P(f'tl.to("#fg", {{scale:0.8, duration:0.07, ease:"power2.in"}}, {f(t)}); tl.to("#fg", {{scale:1, duration:0.18, ease:"expo.out"}}, {f(t + 0.07)});')
    P(f'tl.fromTo("#fg .ring", {{opacity:0.9, scale:0.6}}, {{opacity:0, scale:1.5, duration:0.35, ease:"power2.out", immediateRender:false}}, {f(t + 0.05)});')
    sfx(t + 0.04, "click-soft" if soft else "click", 0.55)


def fin_show(t, x, y):
    P(f'tl.set("#fg", {{x:{x + 160}, y:{y + 260}, scale:1}}, {f(t - 0.01)}); tl.to("#fg", {{opacity:1, x:{x}, y:{y}, duration:0.3, ease:"expo.out"}}, {f(t)});')


def fin_hide(t):
    P(f'tl.to("#fg", {{opacity:0, y:"+=160", duration:0.2, ease:"power3.in"}}, {f(t)});')


def blur_in(sel, t, d=0.35, frm="scale:1.08", y=0):
    P(f'tl.fromTo("{sel}", {{opacity:0, filter:"blur(12px)", {frm}, y:{y}}}, {{opacity:1, filter:"blur(0px)", scale:1, y:0, duration:{d}, ease:"expo.out"}}, {f(t)});')


def blur_out(sel, t, d=0.16):
    P(f'tl.to("{sel}", {{opacity:0, filter:"blur(10px)", duration:{d}, ease:"power3.in"}}, {f(t)});')


def whip_out(sel, t, dx=-1100):
    P(f'tl.to("{sel}", {{x:{dx}, filter:"blur(16px)", duration:0.22, ease:"power3.in"}}, {f(t)}); tl.set("{sel}", {{opacity:0}}, {f(t + 0.22)});')


def whip_in(sel, t, dx=1100):
    P(f'tl.fromTo("{sel}", {{opacity:1, x:{dx}, filter:"blur(16px)"}}, {{x:0, filter:"blur(0px)", duration:0.3, ease:"expo.out"}}, {f(t)});')


def pop(sel, t, gain=0.4, name="pop"):
    P(f'tl.fromTo("{sel}", {{opacity:0, scale:0.6, filter:"blur(6px)"}}, {{opacity:1, scale:1, filter:"blur(0px)", duration:0.28, ease:"back.out(1.6)"}}, {f(t)});')
    sfx(t, name, gain)


def step_slam(n, t, pill_at):
    """giant step number slams in, then flies to its pill in the top-left (carry across)."""
    P(f'tl.fromTo("#lab{n}", {{opacity:0, y:20}}, {{opacity:1, y:0, duration:0.25, ease:"expo.out"}}, {f(t)});')
    P(f'tl.fromTo("#n{n}", {{opacity:0, scale:2.4, filter:"blur(20px)"}}, {{opacity:1, scale:1, filter:"blur(0px)", duration:0.32, ease:"expo.out"}}, {f(t)});')
    sfx(t, "impact-bass-2" if n == 2 else "impact-bass-1", 0.32)
    P(f'tl.to("#n{n}", {{x:0, y:-470, scale:0.15, opacity:0, duration:0.32, ease:"power3.in"}}, {f(pill_at)});')
    P(f'tl.to("#lab{n}", {{opacity:0, filter:"blur(8px)", duration:0.15, ease:"power3.in"}}, {f(pill_at)});')
    P(f'tl.fromTo("#pill{n}", {{opacity:0, scale:0.7}}, {{opacity:1, scale:1, duration:0.3, ease:"back.out(1.7)"}}, {f(pill_at + 0.26)});')
    whoosh(pill_at + 0.05, 0.3)


# ===== shot 1: frame 0 = the finished flyer + price tag, already moving
P('tl.set("#sc1", {opacity:1}, 0);')
P('tl.fromTo("#fly", {rotation:-4, scale:1.06}, {rotation:2, scale:1, duration:0.9, ease:"power2.out"}, 0);')
P('tl.fromTo("#tag", {rotation:12, scale:1.15}, {rotation:6, scale:1, duration:0.5, ease:"expo.out"}, 0);')
sfx(0.0, "impact-bass-1", 0.5)
# a finger swipes the price tag away on "peye"
fin_show(w(1, 0) + 0.05, 725, 685)
P(f'tl.to("#fg", {{x:1100, y:200, duration:0.28, ease:"power3.in"}}, {f(w(1, 1))});')
P(f'tl.to("#tag", {{x:520, y:-180, rotation:48, opacity:0, filter:"blur(10px)", duration:0.32, ease:"power3.in"}}, {f(w(1, 1) + 0.1)});')
whoosh(w(1, 1) + 0.12, 0.5)
P(f'tl.set("#fg", {{opacity:0}}, {f(w(1, 1) + 0.3)});')
kick("#fly", w(1, 3), 1.05)

# ===== shot 2: flyer lands inside a phone; chips IA / 3 MIN / phone
t2 = T[2]
P(f'tl.fromTo("#phone", {{opacity:0, scale:1.35, filter:"blur(14px)"}}, {{opacity:1, scale:1, filter:"blur(0px)", duration:0.5, ease:"expo.out"}}, {f(t2 - 0.1)});')
P(f'tl.to("#fly", {{x:0, y:53, scale:0.77, rotation:0, duration:0.5, ease:"expo.out"}}, {f(t2 - 0.1)});')
whoosh(t2, 0.45)
pop("#chIA", w(2, 1), 0.35)
kick("#fly", w(2, 9), 1.04)
pop("#chMin", w(2, 11), 0.4, "ping")
pop("#chTel", w(2, 14), 0.35)
# ===== shot 3: step 1 slam, chat app opens
t3 = T[3]
for c in ["#chIA", "#chMin", "#chTel"]:
    blur_out(c, t3 - 0.15, 0.15)
P(f'tl.to("#phone", {{opacity:0.0, scale:0.92, filter:"blur(10px)", duration:0.18, ease:"power3.in"}}, {f(t3 - 0.15)});')
P(f'tl.to("#fly", {{opacity:0, filter:"blur(12px)", duration:0.18, ease:"power3.in"}}, {f(t3 - 0.15)});')
step_slam(1, t3 - 0.02, w(3, 2) - 0.05)
P(f'tl.set("#pChat", {{opacity:1}}, {f(w(3, 2))});')
P(f'tl.to("#phone", {{opacity:1, scale:1, filter:"blur(0px)", duration:0.4, ease:"expo.out"}}, {f(w(3, 2))});')
whoosh(w(3, 2), 0.35)
# ===== shot 4: finger types the prompt, taps send, 3 lines come back
t4 = T[4]
fin_show(w(3, 4), *ph(520, 1010))
tap(w(3, 5), True)
n = len(prompt_txt)
ta, tb = w(3, 6), w(4, 10)
for i in range(n):
    P(f'tl.set("#pc{i}", {{opacity:1}}, {f(ta + (tb - ta) * i / n)});')
k = 0
tt = ta
while tt < tb - 0.05:  # typing sound in short bursts
    sfx(tt, "typing", 0.22); tt += 1.3
P(f'tl.to("#fg", {{x:{ph(470, 1000)[0]}, y:{ph(470, 1000)[1]}, duration:0.4, ease:"sine.inOut", yoyo:true, repeat:{max(1, int((tb - ta) / 0.4) - 1)}}}, {f(ta)});')
finger_to(*ph(720, 1022), tb, 0.3)
tap(tb + 0.32)
P(f'tl.set("#inp .ch", {{opacity:0}}, {f(tb + 0.38)});')
P(f'tl.fromTo("#umsg", {{opacity:0, y:40, scale:0.9}}, {{opacity:1, y:0, scale:1, duration:0.35, ease:"expo.out"}}, {f(tb + 0.38)});')
sfx(tb + 0.38, "whoosh-short", 0.25)
fin_hide(tb + 0.55)
for j, wi in enumerate([14, 16, 19]):
    tj = max(w(4, wi) - 0.1, tb + 0.55 + 0.25 * j)
    P(f'tl.fromTo("#bl{j + 1}", {{opacity:0, x:-30, filter:"blur(6px)"}}, {{opacity:1, x:0, filter:"blur(0px)", duration:0.3, ease:"expo.out"}}, {f(tj)});')
    sfx(tj, "pop", 0.35)
# ===== shot 5: step 2, image generates
t5 = T[5]
whip_out("#phone", t5 - 0.2, -1100)
P(f'tl.to("#pill1", {{opacity:0, x:-60, duration:0.18, ease:"power3.in"}}, {f(t5 - 0.2)});')
step_slam(2, t5, w(5, 2) - 0.05)
whip_in("#sc5", w(5, 2))
P(f'tl.set("#sc5", {{opacity:1}}, {f(w(5, 2))});')
P(f'tl.fromTo("#genart .art", {{opacity:0, filter:"blur(30px)", scale:1.2}}, {{opacity:1, filter:"blur(0px)", scale:1, duration:{f(en(5) - w(5, 3) + 0.2)}, ease:"power2.out"}}, {f(w(5, 3))});')
P(f'tl.fromTo("#genfill", {{scaleX:0}}, {{scaleX:1, duration:{f(en(5) - w(5, 3) + 0.2)}, ease:"power1.inOut"}}, {f(w(5, 3))});')
sfx(w(5, 3), "sparkle", 0.3)
sfx(en(5) + 0.1, "ping", 0.35)
# ===== shot 6: background only (good) vs full flyer (bad)
t6 = T[6]
P(f'tl.to("#sc5", {{scale:0.7, opacity:0, filter:"blur(12px)", duration:0.25, ease:"power3.in"}}, {f(t6 - 0.15)});')
P(f'tl.set("#sc6", {{opacity:1}}, {f(t6 - 0.05)});')
blur_in("#cardA", t6 - 0.05, 0.4, "scale:0.8", 40)
blur_in("#cardB", t6 + 0.1, 0.4, "scale:0.8", 40)
whoosh(t6 - 0.05, 0.35)
fin_show(w(6, 4), 310, 640)
tap(w(6, 5))
P(f'tl.fromTo("#ringA", {{opacity:0, scale:1.08}}, {{opacity:1, scale:1, duration:0.25, ease:"expo.out"}}, {f(w(6, 5) + 0.05)});')
kick("#cardA", w(6, 5) + 0.05, 1.05)
finger_to(710, 640, w(6, 8), 0.3)
tap(w(6, 10))
sfx(w(6, 10) + 0.05, "error", 0.3)
fin_hide(w(6, 10) + 0.3)
# ===== shot 7: zoom on the garbled AI text
t7 = T[7]
P(f'tl.to("#cardA", {{opacity:0, x:-300, filter:"blur(10px)", duration:0.25, ease:"power3.in"}}, {f(t7 - 0.1)});')
P(f'tl.to("#cardB", {{x:-200, y:30, scale:1.25, duration:0.5, ease:"power3.inOut"}}, {f(t7 - 0.1)});')
whoosh(t7 - 0.05, 0.35)
P(f'tl.to(["#cardB .badge", "#pill2"], {{opacity:0, filter:"blur(8px)", duration:0.16, ease:"power3.in"}}, {f(t7 - 0.1)});')
for j, wi in enumerate([4, 5, 9]):
    P(f'tl.fromTo("#sq{j + 1}", {{opacity:0, scaleX:0, transformOrigin:"0 50%"}}, {{opacity:1, scaleX:1, duration:0.25, ease:"power2.out"}}, {f(w(7, wi))});')
P(f'tl.fromTo("#stamp", {{opacity:0, scale:2, rotation:-8}}, {{opacity:1, scale:1, rotation:-8, duration:0.25, ease:"expo.out"}}, {f(w(7, 5))});')
sfx(w(7, 5), "glitch-1", 0.3)
P(f'tl.fromTo("#cardB", {{rotation:0}}, {{rotation:1.5, duration:0.05, yoyo:true, repeat:5, ease:"none"}}, {f(w(7, 5))});')
# ===== shot 8: step 3, Canva: finger drags the image in, taps T, text drops
t8 = T[8]
P(f'tl.to("#sc6", {{opacity:0, scale:1.3, filter:"blur(16px)", duration:0.22, ease:"power3.in"}}, {f(t8 - 0.2)});')
step_slam(3, t8, w(8, 2) - 0.05)
P(f'tl.set("#pChat", {{opacity:0}}, {f(w(8, 2))}); tl.set("#pEd", {{opacity:1}}, {f(w(8, 2))});')
P(f'tl.fromTo("#phone", {{opacity:1, x:1100, scale:1, filter:"blur(16px)"}}, {{opacity:1, x:0, filter:"blur(0px)", duration:0.3, ease:"expo.out", immediateRender:false}}, {f(w(8, 2))});')
whoosh(w(8, 2), 0.35)
# finger on the thumbnail (phone screen origin = 294,246 in frame)
fin_show(w(8, 4) - 0.2, *ph(365, 1009))
tap(w(8, 4) - 0.02, True)
P(f'tl.set("#drag", {{opacity:1}}, {f(w(8, 4))});')
P(f'tl.to("#drag", {{x:20, y:-554, scaleX:5.43, scaleY:5.46, duration:0.5, ease:"power3.inOut"}}, {f(w(8, 4) + 0.05)});')
finger_to(*ph(540, 676), w(8, 4) + 0.05, 0.5)
P(f'tl.set("#cart", {{opacity:1}}, {f(w(8, 4) + 0.55)}); tl.set("#drag", {{opacity:0}}, {f(w(8, 4) + 0.56)});')
sfx(w(8, 4) + 0.55, "pop", 0.35)
finger_to(*ph(467, 1009), w(8, 7), 0.3)
tap(w(8, 8), True)
for j, (cid, wi) in enumerate([("#ct1", 9), ("#ct2", 10), ("#ct3", 11)]):
    tj = w(8, wi) + 0.02
    P(f'tl.fromTo("{cid}", {{opacity:0, y:-30, filter:"blur(6px)"}}, {{opacity:1, y:0, filter:"blur(0px)", duration:0.3, ease:"expo.out"}}, {f(tj)});')
    sfx(tj, "key-press", 0.4)
fin_hide(en(8))
# ===== shot 9: 2 fonts only
t9 = T[9]
P(f'tl.to("#phone", {{x:-245, duration:0.45, ease:"power3.inOut"}}, {f(t9 - 0.1)});')
whoosh(t9 - 0.05, 0.25)
pop("#fc1", w(9, 1), 0.35)
pop("#fc2", w(9, 2) + 0.1, 0.35)
kick("#ct1", w(9, 5), 1.12)
sfx(w(9, 5), "click-soft", 0.3)
pop("#fc3", w(9, 9) - 0.25, 0.3)
P(f'tl.to("#fc3", {{opacity:0.35, duration:0.2}}, {f(w(9, 10))});')
kick("#ct2", w(9, 10), 1.12)
sfx(w(9, 10), "click-soft", 0.3)
# ===== shot 10: contrast + from far away
t10 = T[10]
for c in ["#fc1", "#fc2", "#fc3", "#pill3"]:
    blur_out(c, t10 - 0.2, 0.15)
whip_out("#phone", t10 - 0.2, -1100)
P(f'tl.set("#sc10", {{opacity:1}}, {f(t10 - 0.02)});')
whip_in("#cmpL", t10 - 0.02, 1100)
whip_in("#cmpR", t10 + 0.06, 1100)
whoosh(t10, 0.4)
kick("#cmpR", w(10, 3), 1.05)
sfx(w(10, 3), "ping", 0.3)
# "depi lwen": both shrink, the dark one stays readable
P(f'tl.to(["#cmpL", "#cmpR"], {{scale:0.55, y:120, duration:0.6, ease:"power2.inOut"}}, {f(w(10, 9))});')
P(f'tl.to("#cmpL .fly", {{filter:"blur(2.5px)", duration:0.6}}, {f(w(10, 9))});')
sfx(w(10, 9), "whoosh-short", 0.25)
# ===== shot 11: download PNG, counters
t11 = T[11]
P(f'tl.to("#sc10", {{opacity:0, filter:"blur(12px)", scale:1.2, duration:0.2, ease:"power3.in"}}, {f(t11 - 0.15)});')
P(f'tl.set("#phone", {{x:0}}, {f(t11 - 0.15)});')
P(f'tl.fromTo("#phone", {{opacity:0, scale:1.25, filter:"blur(14px)"}}, {{opacity:1, scale:1, filter:"blur(0px)", duration:0.4, ease:"expo.out", immediateRender:false}}, {f(t11 - 0.05)});')
P(f'tl.set("#canvas", {{borderColor:"rgba(0,0,0,0)"}}, {f(t11 - 0.05)});')
whoosh(t11 - 0.05, 0.35)
pop("#dl", w(11, 0) + 0.1, 0.3)
fin_show(w(11, 1), *ph(611, 1011))
tap(w(11, 3))
P(f'tl.fromTo("#file", {{opacity:0, y:40, scale:0.8}}, {{opacity:1, y:0, scale:1, duration:0.3, ease:"back.out(1.7)"}}, {f(w(11, 3) + 0.1)});')
sfx(w(11, 3) + 0.12, "notification", 0.3)
fin_hide(w(11, 4))
P(f'tl.to("#file", {{y:-120, opacity:0, filter:"blur(8px)", duration:0.3, ease:"power3.in"}}, {f(w(11, 6))});')
sfx(w(11, 5) - 0.6, "riser", 0.28)
P(f'tl.to("#phone", {{opacity:0.0, scale:0.85, filter:"blur(14px)", duration:0.3, ease:"power3.in"}}, {f(w(11, 7) - 0.15)});')
P(f'tl.fromTo("#cA", {{opacity:0, scale:1.6, filter:"blur(14px)"}}, {{opacity:1, scale:1, filter:"blur(0px)", duration:0.3, ease:"expo.out"}}, {f(w(11, 7))});')
sfx(w(11, 7), "impact-bass-2", 0.3)
P(f'tl.fromTo("#cB", {{opacity:0, scale:1.6, filter:"blur(14px)"}}, {{opacity:1, scale:1, filter:"blur(0px)", duration:0.3, ease:"expo.out"}}, {f(w(11, 9))});')
sfx(w(11, 9), "impact-bass-1", 0.45)
P(f'tl.fromTo("#flash", {{opacity:0.25}}, {{opacity:0, duration:0.25, immediateRender:false}}, {f(w(11, 9))});')
# ===== shot 12: the finished flyer again (loop), finger taps save, handle
t12 = T[12]
P(f'tl.to("#counter", {{opacity:0, scale:0.8, filter:"blur(10px)", duration:0.18, ease:"power3.in"}}, {f(t12 - 0.12)});')
P(f'tl.set("#sc12", {{opacity:1}}, {f(t12 - 0.05)});')
blur_in("#sc12 .fly", t12 - 0.05, 0.4, "scale:0.85")
whoosh(t12 - 0.05, 0.3)
pop("#save", w(12, 0) + 0.15, 0.3)
fin_show(w(12, 0) + 0.2, 825, 625)
tap(w(12, 0) + 0.5)
P(f'tl.set("#savep", {{attr:{{fill:"{ACC}", stroke:"{ACC}"}}}}, {f(w(12, 0) + 0.55)});')
kick("#save", w(12, 0) + 0.55, 1.2)
sfx(w(12, 0) + 0.55, "pop", 0.4)
fin_hide(w(12, 3))
P(f'tl.fromTo("#handle", {{opacity:0, y:30, filter:"blur(8px)"}}, {{opacity:1, y:0, filter:"blur(0px)", duration:0.35, ease:"expo.out"}}, {f(w(12, 11))});')
sfx(w(12, 11), "whoosh-short", 0.25)
pop("#p2", w(12, 12), 0.4, "ping")

# film grain: new noise every 5 frames
g = 0.0
i = 0
while g < DUR:
    P(f'tl.set("#gturb", {{attr:{{seed:{i % 40 + 1}}}}}, {f(g)}); tl.set("#grain", {{x:{(i * 37) % 40 - 20}, y:{(i * 23) % 40 - 20}}}, {f(g)});')
    g += 5 / 60; i += 1
P(f'tl.set("#bg", {{opacity:1}}, {f(DUR - 0.01)});')  # pin the timeline length

out = html.replace("__JS__", "\n".join(J))
(ROOT / "index.html").write_text(out)

# ---------------------------------------------------------------- captions (1-3 words, one green/red word)
GREEN = {"peye", "entèlijans", "atifisyèl", "pwofesyonèl", "3", "minit", "telefòn", "chatgpt", "tèks", "liy", "ia", "imaj",
         "background", "sèlman", "canva", "2", "font", "gwo", "senp", "kontras", "fonse", "lwen", "png", "fini", "0", "goud",
         "anrejistre", "swiv", "pati", "1"}
REDW = {"konplè", "fot", "sispann"}
norm = lambda s: re.sub(r"[^\wèòàé]", "", s.lower())
groups = []
for s in tim["shots"]:
    cur = []
    for wd in s["words"]:
        cur.append(wd)
        if len(cur) == 3 or re.search(r"[.,:!?]$", wd["w"]) or (len(cur) == 2 and len(cur[0]["w"]) + len(wd["w"]) > 14):
            groups.append(cur); cur = []
    if cur:
        groups.append(cur)
cap_html, cap_js = [], []
for gi, gr in enumerate(groups):
    a = gr[0]["start"] - 0.03
    b = groups[gi + 1][0]["start"] - 0.03 if gi + 1 < len(groups) else min(DUR - 0.05, gr[-1]["end"] + 0.6)
    spans, used = [], False
    for wd in gr:
        txt = wd["w"].rstrip(",:").upper()
        k = norm(wd["w"])
        cls = ""
        if not used and k in REDW:
            cls, used = "r", True
        elif not used and k in GREEN:
            cls, used = "g", True
        spans.append(f'<span class="{cls}">{txt}</span>' if cls else txt)
    nch = len(" ".join(wd["w"] for wd in gr))
    fs = int(min(96, 700 / (nch * 0.74)))
    cap_html.append(f'<div id="c{gi}" class="cap" style="font-size:{fs}px">{" ".join(spans)}</div>')
    cap_js.append(f'tl.set("#c{gi}", {{visibility:"visible"}}, {f(a)}); tl.fromTo("#c{gi}", {{opacity:0, scale:1.12, filter:"blur(8px)"}}, {{opacity:1, scale:1, filter:"blur(0px)", duration:0.1, ease:"power3.out"}}, {f(a)}); tl.set("#c{gi}", {{opacity:0, visibility:"hidden"}}, {f(b)});')
caps = f'''<template>
  <style>
    #root {{ position:absolute; inset:0; overflow:hidden; }}
    .cap {{ position:absolute; left:190px; right:190px; top:1090px; white-space:nowrap; text-align:center; opacity:0; visibility:hidden;
      font-family:'Montserrat'; font-weight:900; font-size:96px; line-height:1.02; letter-spacing:-.01em; color:{TXT};
      text-shadow:0 6px 24px rgba(0,0,0,.75), 0 0 2px rgba(0,0,0,.9); }}
    .cap .g {{ color:{ACC}; text-shadow:0 0 28px rgba(57,255,20,.45), 0 6px 24px rgba(0,0,0,.75); }}
    .cap .r {{ color:{RED}; }}
  </style>
  <div id="root" data-composition-id="captions" data-width="{W}" data-height="{H}">
    {chr(10).join("    " + c for c in cap_html)}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
{chr(10).join("    " + c for c in cap_js)}
    window.__timelines["captions"] = tl;
  </script>
</template>
'''
(ROOT / "compositions").mkdir(exist_ok=True)
(ROOT / "compositions" / "captions.html").write_text(caps)
(ROOT / "episodes" / EP / "sfx.json").write_text(json.dumps({"total": DUR, "events": sorted(SFX, key=lambda e: e["t"])}, indent=1))
print(f"index.html ({DUR}s), {len(groups)} caption groups, {len(SFX)} sound effects")
