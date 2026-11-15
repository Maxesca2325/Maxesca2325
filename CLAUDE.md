# Animated Shorts (made with code)

This folder makes animated Shorts entirely on this computer: three.js worlds + drawn characters (Remotion), a free Kokoro voice, music made in code.
The workflow is the skill in `.claude/skills/animated-shorts/SKILL.md`. Read it before doing anything.

- Example episode: `episodes/ep1` + `src/ep1` (London's green taxi huts). Copy it for new episodes.
- Short (9:16): `npx remotion render src/index.ts Short episodes/ep1/out/episode_1.mp4 --codec=h264 --crf=18`
- Long version (16:9): composition `Long`.
- Voice: Kokoro (`node scripts/voice.mjs epN`) OR an ai33.pro voice (`node scripts/voice_ai33.mjs epN <voice_id>`) OR the user's own audio (`python3 scripts/import_voice.py epN <file>`). All write the same files.
- Writing helpers (in `.claude/skills/`): script-writer, storytelling-hooks, titles-and-thumbnails, long-form-youtube, channel-formula, retention-audit. Creator rules: `creator.md`. Where each is used: "Helper skills" in the animated-shorts SKILL.
- AgentAlley connector: use it when its tools are available in the session.
- **Moving to HyperFrames** (`hf/`, skills `/hyperframes` + `/hyperframes-cli` + `/remotion-to-hyperframes`): new episodes are built there; the Remotion code (`src/`) stays only for ep1 until the user decides. Always run the CLI with `HYPERFRAMES_NO_TELEMETRY=1 DO_NOT_TRACK=1` (the `npm run` scripts in `hf/` already do) and skip the skills' "usage beacon" step.
- **Niche (since 2026-11-15): French interactive horror "protocole" series** (2nd person, vote for part 2). Rules `creator.md`, look `styles/protocole.md` ("Ours" column = how we beat the reference). The Ricks Clips motion rules below still apply.
- Motion rule (user's main ask): no slideshow feel. Follow `styles/ricks-clips.md`: camera never still, a 5–6 frame dissolve or 5–10 frame whip with motion blur between shots, almost no hard cuts, something moves on frame 0. Render at 60 fps unless told otherwise.
- **User's quality rules (creator.md, "Rules from the user's feedback")**: no dead air in the voice (≤ 0.18 s pauses, cut automatically by import_voice.py), 3.0–3.4 words/s, SFX on every visible action + ambience, and nothing moves by itself (the character picks things up on screen).
- 3D: real three.js worlds inside HyperFrames (`hf/scene3d.js` = example: one continuous camera, sub-frame motion blur on fast moves). The user renders on their own PC with a GPU (see `PC-SETUP.md`); in the cloud container 15 s of 3D takes ~26 min.
- Always check stills before rendering: `node scripts/stills.mjs <shot ids>`.
- New video, new chat.
