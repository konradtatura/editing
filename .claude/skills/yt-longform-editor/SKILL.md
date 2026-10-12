---
name: yt-longform-editor
description: Edit Konrad's raw talking-head recording (+ optional script/transcript) into a finished YouTube longform in the "Studio Clean" style — Iman Gadzhi's editorial structure with Apple-clean visuals. Cuts dead air, restarts and bad takes; plans animations from the transcript; after one approval renders every animation separately (alpha .mov / full-frame .mp4, each with the original audio) and assembles the final film with punch-ins, SFX, music and -14 LUFS. Use for "zmontuj film / longform / ten nagrany film", "wytnij powtórki i zrób animacje", "montaż w stylu Imana", raw video + script → finished video. Not for shorts-only edits or films built from scratch without footage.
---

# YT Longform Editor — Studio Clean

**Cel:** surówka + skrypt → film gotowy na YouTube. Montaż ma pomagać oglądać film (wizualizować to, co mówisz, trzymać retencję), a nie być filmem. Twarz Konrada niesie przekaz; grafika wchodzi tylko tam, gdzie zdanie tego potrzebuje.

Read these before planning (they are short and they are the style):
- `references/planning.md` — kiedy animować, budżet gęstości, urządzenie narracyjne, schemat `plan.json`
- `references/style.md` — wygląd i ruch (Iman × Apple), zakazy
- `references/catalog.md` — typy T1–T10 z parametrami
- `references/cutting.md` — zasady cięcia i przegląd podejść
- `references/sound.md`, `references/qa.md`
- `references/feedback.md` — uwagi Konrada z poprzednich filmów (zawsze stosuj)

Konrad is a marketer, not an editor: never ask him technical questions (codecs, engines, fps). Ask only about content/style when a choice really changes the film. Communicate in Polish.

## Pipeline (one film = one folder)

```
FILM_<nazwa>/
  00_input/   raw.mp4 (+ skrypt.md, transkrypt.json if he sends them)
  01_cut/     words_raw.json, takes_report.md, takes.json, edl.json, rough_cut.mp4, words_cut.json, transcript_cut.md
  02_plan/    plan.json, plan.md (the human-readable list he approves)
  03_assets/  screenshots, logos
  04_anim/    NN_tc_TYPE_NAKLADKA.mov | NN_tc_TYPE_MIX.mp4 | NN_tc_TYPE_BROLL.mp4   (+ _src/ projects)
  05_audio/   sfx.wav, mix.wav
  06_final/   FINAL.mp4
  qa/         sheets/*.jpg, report.md
```

`S=~/.claude/skills/yt-longform-editor/scripts` — all commands below.

### E1 · Transcribe
```bash
python3 $S/transcribe.py FILM/00_input/raw.mp4 FILM [--import FILM/00_input/transkrypt.json] [--prompt-from FILM/00_input/skrypt.md]
```
Default engine: **Parakeet** (verbatim, keeps every retake, ~20× realtime). If Konrad sends an ElevenLabs/Whisper JSON, `--import` it. Never cut from a Whisper transcript without checking `asr-gap` flags — Whisper silently skips repeated attempts.

### E2 · Cut (the film must sound great with eyes closed)
```bash
python3 $S/takes.py FILM [--script FILM/00_input/skrypt.md]     # → takes_report.md + takes_suggest.json
```
**You review the report word by word** (see `references/cutting.md`): keep the best complete take of every line (usually the last, not always), drop restarts / fillers / ASR junk, keep good improvisations even if off-script. Write `01_cut/takes.json`, then:
```bash
python3 $S/cutter.py build FILM && python3 $S/cutter.py render FILM
```
Read `01_cut/transcript_cut.md` end to end: no repeated phrase, no sentence cut in half, no orphan words. Fix takes.json and rebuild if needed.

### E3 · Look at the footage once
Extract 6 frames across the film (`ffmpeg -ss T -i rough_cut.mp4 -frames:v 1 -vf scale=960:-1 f_T.jpg`) and read them. Decide and write into `plan.json → film`:
- `speakerBox` — union of the head positions (hair to chin, with movement) in 1920×1080 px. Text never enters it.
- `surface` — `light` (bright room, Apple white) or `dark` (moody studio, Iman night). Full-screen scenes use it.
- `accent` — one colour taken from the footage (60/30/10 rule), fallback `#0A84FF`.

### E4 · Plan (the only approval gate)
Follow `references/planning.md`. Write `02_plan/plan.json` and a short Polish list `02_plan/plan.md`:
`| # | od–do | co mówisz | typ | co pokazujemy | po co |`. Run the self-check in planning.md, then show Konrad the list and **wait for his OK** (he often answers from his phone). Screenshots for browser scenes: `bash $S/shot.sh <url> FILM/03_assets/<name>.png`.

### E5 · Build every animation separately
```bash
python3 $S/anim.py all FILM/02_plan/plan.json FILM --jobs 3           # scaffold → render → deliver
```
Overlays (T1–T4) → `_NAKLADKA.mov` (ProRes 4444 alpha) + `_MIX.mp4` (over the footage, original audio).
Full frame (T5–T10) → `_BROLL.mp4` (with the original audio of that range). Re-render one item: `--only 07`.

### E6 · QA loop (do not hand over unchecked work)
```bash
python3 $S/qa.py check FILM FILM/02_plan/plan.json   # durations, alpha, audio, black frames
python3 $S/qa.py sheets FILM                          # contact sheets → read EVERY sheet
```
Read each sheet against `references/qa.md` (text on the face, clipped text, typos, wrong numbers, style drift, empty frames). Fix params in plan.json → re-render that id → re-check. Max 3 rounds per item, then report what is left.

### E7 · Assemble
```bash
python3 $S/assemble.py FILM/02_plan/plan.json FILM [--preview]       # → 06_final/FINAL.mp4
python3 $S/qa.py final FILM                                           # duration = rough cut, -14 LUFS, TP ≤ -1
```
Then sheet the FINAL at ~10 points (the moments with graphics + 3 punch-ins) and read it.

### E8 · Hand-over (Polish, short)
What was cut (min → min), how many animations by type, anything you flagged (numbers that differ between audio and brief, takes you were unsure about), paths to FINAL / 04_anim. Offer a `--preview` 720p file for the phone (SendUserFile).

## Models & effort
Plan + review + QA reading: Opus, high. Mechanical steps run as scripts. For very long films (> 20 min) split planning by chapters; parallel subagents may build different chapters' params, but one agent owns the final plan.json for consistency.

## After every film
Append Konrad's feedback to `references/feedback.md` (what he liked → keep, what he rejected → ban, one line why). That file is how the style gets better film after film.
