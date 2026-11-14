# Creator rules (read by script-writer, storytelling-hooks, titles-and-thumbnails)

This file replaces `~/CLAUDE.md` for the script-writer skill (the cloud machine's home folder is wiped between sessions).
**These rules win over any generic skill rule.** Fill in the blanks as the channel grows.

## Channel
- Format: animated Shorts made in code (2D cartoon characters in a 3D world), narrated by one voice, true/strange stories with a twist.
- Style to follow: `styles/<channel>.md` (measured numbers). Example: `styles/ricks-clips.md`. Its numbers (words per second, length, opener, pivot, last-line twist) **override** the generic pacing of the skills (script-writer assumes ~2.5 words/s and 30–45 s; this channel measures ~3.7 words/s, ~60 s).
- Languages: English (voice `clone_2574492` "Maxime Voice USA") and French (French clone voices on ai33). Write the script in the video's language; talk to the user in French.

## Audience
- Who should follow: _to fill in (e.g. curious people who like "why is it like that?" history/science stories)._
- What they come for (core promise): _to fill in after the first winners (use channel-formula)._

## Script rules
- First line: a paradox or surprising fact. No intro, no "today", no question answered by yes/no.
- Escalate → pivot ("You see…") → payoff → twist on the last line that loops back to the first (bookend).
- Every claim fact-checked, sources table at the bottom of `story.md`. Never invent numbers or stories ("Ownable" = verifiable).
- CTA: _none by default (this format usually has none); fill in if the channel wants one._
- On screen = the animated scene. "Proof on screen" means the shot shows what the line says (signs/objects in the 3D world, not flat text).

## Fresh hooks / research
- Hook bank: `research/hooks.md` (create it; newest first).
- Channel profile (from channel-formula): `research/<channel>-formula.md`.
