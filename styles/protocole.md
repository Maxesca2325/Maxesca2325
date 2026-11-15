# « Protocole » horror (TikTok @suisleprotocole): measured style + how we do it better

Sources: the account's 10 most-viewed videos (59k–633k views, measured 2026-11-15) in `ref/suisleprotocole/` (study only, git-ignored, never reposted)
→ `scripts/measure.py` (numbers.json) + every contact sheet read + 3 transcripts (faster-whisper FR).
**Never reuse their stories, lines, characters or frames.** We take the format, then make our own stories, better-looking.

## Format
| Rule | Measured | Ours (amélioré) |
|---|---|---|
| Frame | 9:16, 1080×1920, **30 fps**, very low bitrate (~120 kbit/s → blurry, banding in the dark gradients) | 1080×1920, **60 fps**, high bitrate export (CRF ≤ 16), film grain on top so gradients never band after TikTok re-compression |
| Length | median 116 s (61–231) | 90–130 s per part |
| Series | the top videos are part 1s with "⚠️PARTIE 2 DISPONIBLE⚠️" in the caption; part 2/3 follow the most-voted comment | same; keep `episodes/<serie>/choices.md` (what was voted, what happens next) |

## Story + voice (3 transcripts)
| Rule | Measured |
|---|---|
| Person / tense | **2nd person, present** ("Tu t'endors… Quand tu te réveilles…"). The viewer is the hero. |
| First line | an ordinary night situation + one wrong detail, often with a time: "Imagine. Tu t'endors pendant un vol de nuit.", "Ta copine dort chez toi…", "Chaque soir à 22h, le voisin d'en face te fait coucou." Voice starts at 0.0 s. |
| Times on the clock | precise odd times: 2h41, 2h46, 2h58, 1h11, 3h14, 22h. |
| Escalation | short sentences, one new wrong detail per line; a written rule found in the world ("Lumières éteintes, tu dors.", "Règle numéro 1. Ne lui réponds jamais.") |
| Pace | **2.8–3.0 words/s** (227–487 words); calm, whispery male narration, long pauses on reveals |
| Ending | "Tu dois choisir." + two options (A / B) + "Vote en commentaire. La réponse la plus votée décide de la suite. Épisode 2 demain. Abonne-toi pour ne pas le rater." Variant: several choices inside one video with "On rembobine." and a "Règle numéro N" after each bad ending; last line "Il y avait une troisième option… Dis-le en commentaire." |
| Caption (post text) | "⚠️PARTIE 2 DISPONIBLE⚠️" + title + 1–2 line hook + question + #horreur #creepypasta #peur #nuit #pourtoi |

## Picture (measure.py medians over 10 videos)
| Rule | Measured | Ours (amélioré) |
|---|---|---|
| Look | flat vector cartoon: big round heads with two-tone face shading, stick limbs, ball hands; creepy characters = red ringed eyes, huge grin; simple 3D-ish rooms (cabin, building, room) | same family of look (it's what the audience expects) but drawn sharper (vector, no blur), with consistent recurring characters, blinking, breathing, walking |
| Shot length | median **3.1 s** (1.7–5.5), 19 cuts/min | 2.5–3.5 s |
| Camera | almost still: `camera_motion` 0.019 (Ricks Clips 0.082). Mostly held frames + slow zoom | **always moving**: slow push/drift (2–5 % scale per s), eased glides, a snap push on each scare |
| Transitions | mostly hard cuts, some fades to black | 5–6 frame dissolves, whip with motion blur on scares, a dip to black only for "time jumps"; never a plain cut except a deliberate jump-scare |
| Darkness | shadows near black RGB (5, 4, 9), **25 % of pixels pure black** (median), hue 248° (blue-violet) | deep blue-violet night instead of pure black (≈ `#0E0C1C`–`#1A1830`), max ~5 % pure black, so the picture stays readable on a phone |
| Highlights | warm cream (225, 220, 210) | same; practical lights warm `#F2C27A`, flashlight cold white with soft cone + flicker |
| Saturation | median 0.43 | 0.40–0.48; red reserved for danger (eyes, "PERDU", key word) |
| In-world text | yes: seat-back screen "ATTERRISSAGE 38 MIN", safety card "LUMIÈRES ÉTEINTES, TU DORS.", location + ticking clock at the top ("SALON 22:00:04", "HALL 07:32:00"), title card "LE VOISIN D'EN FACE", "RÈGLE 01", red "PERDU" | same devices, designed once as reusable HyperFrames components (clock bar, rule card, title card, choice menu, PERDU), animated in/out |
| Choice screen | split screen: villain top, hero bottom, two pills "A · OUVRIR" (red) / "B · GARDER FERMÉS" (blue), countdown 4-3-2-1 in a circle; or a menu card "CHOIX 1 « COUCOU » A … B …" with a progress bar | same structure, animated (pills slide in, countdown ring drains, heartbeat pulse) |
| "Eyes closed" shots | full red screen ("À travers tes paupières, tout devient rouge") | red with slow pulse + vignette + blur |

## Captions
| Rule | Measured |
|---|---|
| Words at a time | 1 (sometimes 2–3) |
| Font | heavy condensed or rounded sans, uppercase, white, thin dark outline + soft shadow |
| Key word | coloured: red for danger words (NOIR, MASQUE, COUCOU, GRAND, HUMAIN, MURÉ), yellow-green for the current word in multi-word chunks |
| Position | centre ≈ 77 % from the top (lower than Ricks Clips' 70 %), moved up when the choice pills are on screen |

## Sound (to measure later, by ear)
Low drone under everything, silence before reveals, small foley (clicks, footsteps, phone buzz), stinger on scares. Ours: same, made in code (`scripts/sound.mjs`) or free SFX.
