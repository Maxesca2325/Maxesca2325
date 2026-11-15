# Skill sources

| Skill(s) | From | Commit | License |
|---|---|---|---|
| animated-shorts | animated-shorts-skill.zip (user's Drive) | — | — |
| storytelling-hooks, long-form-youtube, titles-and-thumbnails, retention-audit, channel-formula, carousel-narratives, email-hooks, wireframe-writer, wireframe-reviewer | https://github.com/yaxeen/storytelling-skills | 24ef3c1e3d7fde66cc5f1c5953cd6c1d7afc0b4f | MIT (LICENSE in each folder) |
| script-writer | https://github.com/criscatalyst/creator-skills (`skills/script-writer`) | 47dcc85cc1d8132b498ef1e451d270d95c06d6c5 | MIT (LICENSE in folder) |
| hyperframes, hyperframes-cli, hyperframes-registry, media-use, remotion-to-hyperframes, reverse-any-video, style-sampling | https://github.com/heygen-com/hyperframes (`skills/`) | b5f5ab36a1f4b626da9de40adf7e40257967997c | Apache-2.0 (LICENSE in each folder) |

Copied unmodified into the project (not `~/.claude/skills`) so every cloud session has them.
Update: clone the repo again and copy the folder over, then read the diff before committing.

HyperFrames skills: scripts only call paid APIs (HeyGen, ElevenLabs, Gemini) when their API key is set — none is set here. Telemetry is turned off in this project: run the CLI with `HYPERFRAMES_NO_TELEMETRY=1 DO_NOT_TRACK=1` (see CLAUDE.md) and skip the skill's "usage beacon" step.
