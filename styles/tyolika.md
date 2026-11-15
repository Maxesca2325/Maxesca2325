# @tyolika — look and editing rules (Creole digital-skills Shorts)

Editing style asked by the user: **"style Iman Gadzhi"** (premium business-education edit: dark, minimal, kinetic text, punch-ins, a lot of sound design). We take the *editing grammar*, not his footage, music or branding. Everything is drawn in code (faceless).

Every rule is a number or a yes/no a still can be checked against.

## Format
| Rule | Value |
|---|---|
| Frame | 1080×1920, 60 fps |
| Length | 35–55 s (≈ 110–170 words) |
| Voice | the user's own Creole voice-over, imported with `scripts/import_voice.py --lang ht` (dead air cut to ≤ 0.18 s) |
| Words per second | 3.0–3.4 after cutting |
| **Background music** | **none** (user's rule). Sound = voice + SFX only |

## Colour + type
| Rule | Value |
|---|---|
| Background | `#121212`, with a faint 60 px grid at 4 % white and a radial vignette to `#070707` |
| Accent | `#39FF14` (neon green), used on ONE word per caption group at most, on step numbers and on "good" states |
| "Bad" state | `#FF3B3B` (crosses, errors) — only for the wrong way |
| Text | white `#F5F5F5`; secondary `#9A9A9A` |
| Caption font | Montserrat 900, uppercase, 92–110 px, letter-spacing −0.01 em, black stroke 0, soft shadow `0 6px 24px rgba(0,0,0,.7)` |
| Elegant accent font | Playfair Display italic (one word per scene at most: "sekrè", "fini") |
| UI / numbers | Inter 700, JetBrains Mono 700 for timers and file names |
| Film grain | yes, 6–8 % opacity, changes every 5 frames (12 Hz) |

## Layout (TikTok safe zones)
| Rule | Value |
|---|---|
| Nothing readable above y = 170 px | yes |
| Main visual (phone, cards, UI) | centred, y 260–1120 |
| Captions | one line, centred, top at y ≈ 1190 (≈ 730 px from the bottom) |
| Nothing readable below y = 1330 or under the right rail (x > 940, y > 900) | yes |

## Motion (no slideshow)
| Rule | Value |
|---|---|
| Something moves on frame 0, and a full-size line is already on screen | yes |
| Camera (`#cam` wrapper) never still | drift 1.5–3 % scale per second + small x/y sway |
| Punch-in on key words | scale +6–10 % in 0.12 s (`expo.out`), hold, relax over 0.6 s |
| Visual change | every 1.5–3 s |
| Transitions between beats | whip (0.18–0.3 s, motion blur on), blur swap (out 0.15 s with 10 px blur, in 0.13 s), zoom-through (an element grows past the frame in 0.35–0.5 s, `power3.in`). Hard cuts: none between beats |
| Arrivals / exits | arrive `expo.out` 0.35–0.5 s; exits 40–50 % shorter, `power3.in` |
| Captions | 1–3 words, pop in with blur 8 → 0 px + scale 1.12 → 1 in 0.1 s; one accent-green word per group |
| Nothing moves by itself | UI actions are done by a cursor/finger on screen (drag, tap, type) |

## Sound (no music)
| Rule | Value |
|---|---|
| Whoosh on every transition | yes, rotate `whoosh`, `whoosh-short`, `whoosh-cinematic` |
| Pop on every chip/badge/number landing | yes (`pop`, `ping`) |
| Click on every tap | yes (`click`, `click-soft`) |
| Typing on typed text | `typing` / `key-press` |
| Impact | `impact-bass-1/2` on the hook and the payoff, max 3 per video |
| Riser | once, into the payoff |
| Error | `error` / `glitch` only on the "wrong way" |
| Levels | voice peak −1 dB on top; SFX −10 to −16 dB under it; mix ≈ −14 LUFS |
| Silence | never more than 0.25 s with neither voice nor SFX |

SFX source: `tyolika/assets/sfx/` (Pixabay Content License, free for commercial use, see CREDITS.md).
