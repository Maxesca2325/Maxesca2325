---
name: kreyol-writer
description: Write natural, correctly spelled Haitian Creole (Kreyòl ayisyen) for voice-over scripts, captions, TikTok post text, Discord texts and landing pages. Use for any text in Creole for the @tyolika channel or its community, and to proofread Creole written by anyone (including Claude). Official orthography (IPN 1979), spoken Port-au-Prince register, tech vocabulary, numbers, and a final checklist.
---

# Kreyòl writer

The audience speaks Creole every day and reads it rarely. The text must **sound like a young Haitian explaining something to a friend**, not like a translation from French. Correct spelling matters on screen (captions), because a wrong spelling looks amateur.

Use with `script-writer` / `storytelling-hooks` for structure; this skill decides the words and the spelling. **Proofread every Creole line with the checklist at the end before delivering it.**

## 1. Spelling (òtograf ofisyèl)

One sound = one spelling. No silent letters, no French spelling.

| Sound | Write | Never | Examples |
|---|---|---|---|
| open e / open o | **è**, **ò** | ê, ai, au | fè, tèks, pwofesyonèl, telefòn, kòb, mòd |
| closed e / o | **e**, **o** | é, eau | kreye, videyo, foto |
| "ou" | **ou** | u | sou, toujou, ouvri |
| nasals | **an, en, on, oun** | am, em, in, un | lajan, mwen, konn, moun, enpòtan |
| "sh" / "zh" | **ch**, **j** | sh, g+e | chaje, Chèche, jodi a, imaj |
| always hard g, k | **g**, **k** | c, q, qu, gu | konnen, kantite, gen |
| "w" / "y" glides | **w**, **y** | oi, ill | mwen, pwofi, travay, bay |
| x | **ks** / **gz** | x | tèks, egzanp, ekspè |
| a + n NOT nasal | **àn** | | pàn, Jàn |

Hyphens only in fixed forms (no hyphen in "kounye a", "jodi a", "pou kont ou").

## 2. Grammar that makes it sound native

- **Short pronouns** after a vowel and in fast speech: mwen → **m**, ou → **w**, li → **l**, nou → **n**, yo → **y** (before a vowel). "M ap montre w", "Ba l non an", "Pou w pa bliye", "Kote l ap fèt". Keep the full form at the start of a sentence for emphasis ("Mwen menm, …").
- **Markers before the verb**: te (past) · ap (in progress / near future) · pral / prale (going to) · va / ava (will) · ta (would) · konn (usually) · fèk / sot (just did). "Li te fè", "N ap fè", "W ta dwe".
- **Negation**: **pa** before the verb, **p ap** (= pa + ap), **pa t** (past). "Li p ap mache", "M pa t konnen".
- **Determiner after the noun** (la / a / an / lan / nan, plural **yo**), chosen by the last sound:
  - after a consonant sound → **la**: tèks la, imaj la, bot la, prompt la
  - English words follow how they are SAID: "flyer" is said "flayè" → **flyer a**
  - after an oral vowel → **a**: videyo a, IA a, kafe a, bato a
  - after a nasal vowel → **an**: aplikasyon an, lajan an, mwayen an
  - after a nasal consonant (m, n, ng) → **nan** / **lan**: machin nan, fanm nan
  - plural: tèks yo, videyo yo, moun yo
- **Questions**: Èske…? · Kisa…? · Ki jan / Kijan…? · Konbyen…? · Poukisa…? · Kilè…? · Kote…? · Kiyès…?
- **Possession**: noun + pronoun: "telefòn ou", "kont mwen", "chèn ou an".
- **No French words when Creole has one**: maintenant → kounye a · beaucoup → anpil · argent → lajan / kòb · pour → pou · avec → avèk / ak · gratuit → gratis · facile → fasil · vraiment → vrèman · déjà → deja · seulement → sèlman · chaque → chak · aussi → tou · parce que → paske · mais → men.

## 3. Tech and money vocabulary (as Haitians say it)

| Concept | Write | Note |
|---|---|---|
| artificial intelligence | entèlijans atifisyèl, **IA** (said "i-a") | "AI" also heard; pick IA and keep it |
| app | aplikasyon, **app** | |
| website / landing page | sitwèb, paj | "landing page" fine as is |
| code / coding | kòd, kode | "vibe coding" stays English |
| download / install | telechaje, enstale | |
| save (a video) | anrejistre | the TikTok "save" |
| share / comment / follow | pataje, kòmantè, swiv | |
| subscribers / views | abòne, vi (or "views") | |
| account / channel | kont, chèn | "chèn faceless" |
| money / earn | lajan, kòb, goud, dola · fè kòb, touche | |
| Haitian dollar | dola ayisyen (= 5 goud) | 375 dola ayisyen = 1 875 goud |
| bot, prompt, background, PNG, trading, crypto, USDT, backtest | keep the English word | Creole grammar around it: "bot la", "prompt sa a" |
| risk / loss / profit | risk, pèt, pwofi | |
| phone / computer / internet | telefòn, òdinatè, entènèt | |

Brand names stay as written by the brand: ChatGPT, Canva, TikTok, YouTube, MonCash, Natcash, Discord, Binance.

## 4. Numbers

- On screen (captions): digits ("3 minit", "0 goud", "1 875 goud").
- In `shots.json`, the `say` field gives what is spoken: 1 youn/en · 2 de · 3 twa · 4 kat · 5 senk · 6 sis · 7 sèt · 8 uit · 9 nèf · 10 dis · 11 onz · 12 douz · 15 kenz · 20 ven · 30 trant · 50 senkant · 100 san · 1 000 mil · 1 500 mil senk san.
- Never make up statistics. If a number isn't sourced, use words ("anpil moun", "pifò").

## 5. Voice-over style (@tyolika)

- 2nd person "ou/w", present tense. Sentences of 4–12 words. One idea per sentence.
- Spoken connectors: Men… · Gade… · Koute… · Sa k pi enpòtan an… · Pa bliye… · Epi… · Konsa… · Rezilta a?
- Hook patterns that work in Creole: "Sispann [bad habit]." · "Pèsonn pa di w sa." · "Si w gen yon telefòn, ou ka…" · "Men 3 [things] ki…" · "Ou konnen poukisa…?" · "[Number] minit. [Number] goud."
- Write numbers and English tools the way the speaker will say them; the speaker must be able to read it once without stumbling.
- **Trading / crypto**: never promise gains ("garanti", "lajan fasil", "w ap vin rich"). Say "risk", "pèt posib", "teste anvan", "se pa konsèy finansye". Educational only.

## 6. Checklist (run on every line before delivering)

1. Read it aloud in your head as a Port-au-Prince 22-year-old: does any word sound French or bookish? Replace it.
2. Every è/ò where the vowel is open; no é, ê, c, q, u, x.
3. Contractions consistent (m/w/l/n after vowels) and determiners match the last sound.
4. Negation: pa / p ap / pa t, before the verb.
5. Numbers: digits in `text`, words in `say`.
6. No invented stats, no gain promises, brand names spelled by the brand.
7. Sentence ≤ 12 words; one idea; the key word at the end of the sentence (it lands on the beat).
8. Mark anything you are unsure of with `(?)` and tell the user: they are the native speaker and the final judge.
