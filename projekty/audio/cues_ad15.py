#!/usr/bin/env python3
"""Sound design + music for ad 15 (style 10, "skill h2 v5", one version).  usage: cues_ad15.py SFXDIR MUSIC.mp3 OUT.json\nBuilt from cues_ad13.py (same palette, rules and music). Original ad13 notes:
Same palette and relative levels as ad12 (approved). The voice here is -20.3 LUFS vs -27.5 in ad12, so every SFX gets +7.2 dB
(VO_SHIFT) to keep the same SFX/voice balance. Music: Mixkit 173 "Better Times are Coming" (Konrad's pick for ad12), ~13 LU under
the voice. The track is 1:40 and the film 2:03, so the hooks play it from 0 and the body restarts it from 0 on the body cut:
exactly what each cut variant (hook + body) sounds like. Hook cuts: sounds start ON the cut, nothing rings across one."""
import json, os, subprocess, sys
import numpy as np
SD, MUSIC, OUT = sys.argv[1:4]   # + optional MUSIC_START MUSIC_DB
S = lambda n: os.path.join(SD, n + ".wav")
VO_SHIFT = 8.2                                         # voice -19.3 LUFS vs -27.5 in ad12
HOOK_CUTS = ()
CUTS = [1.8, 3.567, 4.467, 7.6, 8.4, 9.3, 12.5, 15.633, 16.867, 18.6, 21.267, 24.7, 26.5, 29.2, 30.567, 34.867, 36.533, 40.3, 42.8,
        43.333, 48.1, 53.067, 56.967, 60.467, 67.3, 70.8, 74.2, 79.3, 81.967, 84.4, 88.067, 91.133]
BIG = {3.567, 7.6, 12.5, 21.267, 40.3, 56.967, 79.3, 88.067}   # scene changes with the blur-in

ACC = [  # (t, sound, dB as in ad12 scale, peak-aligned)
    (7.80, "pop", -16, False),                        # megaphone bursts in "Halo, halo!"
    (21.64, "ding", -16, False),                      # "Ale dzisiaj AI"
    (22.18, "swoosh_big", -20, True),                 # laptop lights up
    (27.08, "pop", -18, False),                       # "AI pomoże" (ebook)
    (31.32, "pop", -18, False),                       # "z pomocą AI" (strona)
    (36.66, "pop", -18, False),                       # "AI może pomóc" (marketing)
    (59.02, "boom", -16, False),                      # "Cyfrowy Autopilot"
    (67.58, "pop", -18, False),                       # "znalezienia pomysłu"
    (70.42, "pop", -18, False),                       # "ebooka"
    (71.50, "pop", -18, False),                       # "stronę"
    (77.68, "ding", -17, False),                      # "48 godzin"
    (88.20, "click", -11, True),                      # CTA "Kliknij poniżej"
    (88.35, "pop", -16, False),                       # yellow arrow
    (91.25, "kaching", -13, True),                    # box "17 zł"
]
sfx = [dict(t=t, f=S(n), db=db, peak=p) for t, n, db, p in ACC]
busy = [t for t, *_ in ACC]
wh, last = ["whoosh_a", "whoosh_b", "whoosh_c", "whoosh_d"], -9
for i, c in enumerate(CUTS):                          # whoosh on cuts, never two within 1 s, never on top of a story beat
    if c - last < 1.0 or (c not in BIG and any(abs(c - b) < 0.35 for b in busy)): continue
    if c in HOOK_CUTS:
        sfx.append(dict(t=c, f=S("whip"), db=-21, peak=False)); last = c; continue
    big = c in BIG
    sfx.append(dict(t=c, f=S("swoosh_big" if big else wh[i % 4]), db=-19 if big else -23, peak=True)); last = c
for s in sfx: s["db"] = round(s["db"] + VO_SHIFT, 1)
dur = lambda f: float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f], capture_output=True, text=True).stdout)
pk = {}
for s in sfx:                                         # trim anything that would ring across a hook cut
    if s["f"] not in pk:
        a = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", s["f"], "-ac", "1", "-ar", "8000", "-f", "s16le", "-"], capture_output=True).stdout, np.int16)
        pk[s["f"]] = float(np.argmax(np.abs(a.astype(np.int32)))) / 8000
    st = s["t"] - (pk[s["f"]] if s["peak"] else 0)
    for hc in HOOK_CUTS:
        if st < hc < st + dur(s["f"]): s["dur"] = round(hc - st - 0.01, 3)
cues = dict(music=MUSIC, musicStart=float(sys.argv[4]) if len(sys.argv) > 4 else 0, musicDb=float(sys.argv[5]) if len(sys.argv) > 5 else -18,
            fadeOut=2.0, duckThreshold=0.02, sfx=sorted(sfx, key=lambda s: s["t"]))   # music: Konrad picked A = Mixkit 678 "Epical Drums 03" (start 2.5, -15.0 dB)
json.dump(cues, open(OUT, "w"), indent=1)
print(len(sfx), "sfx cues, music", cues["musicDb"], "dB")
for s in cues["sfx"]: print(f'{s["t"]:7.2f} {os.path.basename(s["f"]):16s} {s["db"]:5.1f} dB' + (f' trim {s["dur"]}' if "dur" in s else ""))
