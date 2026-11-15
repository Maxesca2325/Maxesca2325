# @tyolika — Shorts éducatifs en créole (HyperFrames)

Second project in this repo, separate from the French horror series in `hf/`. TikTok **@tyolika** (~7 900 abonnés), pivot to digital skills for a Haitian / diaspora audience: IA + flyers, faceless channels and monetisation, vibe coding, automated trading + crypto (educational only).

## Rules (user's own)
- Faceless. **The user's own Creole voice-over.** No background music: voice + SFX only.
- Look: dark `#121212` + neon green `#39FF14`, 9:16, 60 fps, word-by-word captions, a visual change every 2–3 s, smooth transitions (whip / blur swap / zoom-through), "Iman Gadzhi"-style edit. Numbers in `../styles/tyolika.md`.
- No dead air (pauses ≤ 0.18 s), SFX on every visible action, nothing moves by itself (a finger/cursor does the UI actions).
- Phase 1 (videos 1–6): 100 % free value. **No price, no offer, no Discord.**
- Trading/crypto: education only, never promise gains, say "se pa konsèy finansye".
- Creole text: always through the `kreyol-writer` skill (spelling + checklist). The user is the final judge of the Creole.
- Topics + calendar: `research/sijè.md`.

## Workflow for one video (vNN)
1. Script with `script-writer` + `kreyol-writer` → `episodes/vNN/story.md` + `shots.json` (`text` = captions, `say` = spoken numbers).
2. Before the voice exists: `python3 tools/scratch_timing.py vNN` (estimated timing) so the video can be built and previewed.
3. Build: `python3 tools/build_vNN.py` (copy `build_v01.py`; every animation is anchored to a word) → `index.html`, `compositions/captions.html`, `episodes/vNN/sfx.json`.
4. Sound: `python3 tools/mix.py vNN` → `assets/vNN_mix.wav` (voice on top if `public/vNN/voice.wav` exists).
5. `npm run check` (0 errors), then snapshots of every shot (`node tools/hf.mjs snapshot --at …`) and look at them.
6. Render: `node tools/hf.mjs render --fps 60 --quality delivery --output renders/vNN.mp4`.

## When the user sends the voice recording
From `tyolika/` (first time only: `pip install faster-whisper`):
```
python3 ../scripts/import_voice.py vNN <audio file> --lang ht
python3 tools/build_vNN.py && python3 tools/mix.py vNN
npm run check && node tools/hf.mjs render --fps 60 --quality delivery --output renders/vNN.mp4
```
Check the "Matched X/Y" line (≥ 60 %) and the words/s (3.0–3.4; else `--tempo 1.08`).
