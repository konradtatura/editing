#!/usr/bin/env python3
"""Sound design cues for ailego12 (style 9, LEGO AI, voice-over).  usage: cues_ad12.py SFXDIR OUT.json [MUSIC.mp3]
Music (v4, chosen by Konrad from 3 samples): Mixkit 173 "Better Times are Coming" (synthpop, -12.3 LUFS) at -28.2 dB = ~13 LU under the
voice (-27.5 LUFS), ducked with threshold 0.01 (quiet voice track). Without MUSIC: SFX only (v3).
SFX are CC0 from Openverse (Freesound), peak-normalised to -1 dBFS; list + links in SFXDIR/SOURCES.json.
Hook cuts 12.767 / 23.133: sounds there start ON the cut (no pre-roll) and nothing before a hook cut rings past it,
so Konrad can cut the hook variants himself."""
import json, os, sys
SD, OUT = sys.argv[1], sys.argv[2]
S = lambda n: os.path.join(SD, n + ".wav")
HOOK_CUTS = (12.767, 23.133)
CUTS = [0.867, 4.767, 10.367, 12.767, 16.467, 17.8, 18.667, 23.133, 27.333, 28.4, 32.667, 37.367, 38.467, 40.067, 42.167, 44.733,
        46.933, 50.0, 51.933, 53.067, 54.233, 55.8, 57.167, 62.067, 66.7, 70.867, 74.3, 78.033, 79.5, 82.567, 84.033]
BIG = {28.4, 62.067, 78.033}                          # section changes with the blur-in: wider, airier swoosh

ACC = [  # (t, sound, dB, peak-aligned) on the story beats
    (0.05, "ui_click", -16, False),                   # "Otwórz TikToka": tap on the phone
    (8.76, "kaching", -17, True),                     # "tysięcy złotych" while the money rains
    (8.30, "coins", -22, False),
    (10.44, "buzz", -24, False),                      # "I nie" + red X
    (11.72, "click", -15, True),                      # pointer taps the product card
    (18.12, "lego_click", -14, False),                # red box "Link w jej bio"
    (35.88, "kaching", -13, True),                    # "79 zł" boxed
    (38.62, "click", -13, True),                      # "klika link"
    (39.36, "notif", -18, False),                     # "kupuje" -> sale
    (40.14, "pop_low", -17, False),                   # "Bez magazynu" X
    (41.18, "pop_low", -17, False),                   # "bez wysyłania" X
    (43.50, "coins", -15, False),                     # "sprzedawać wielokrotnie" coin rain
    (46.93, "rev_cymbal", -21, True),                 # build-up "robi się naprawdę ciekawie" -> "Bo AI"
    (46.95, "boom", -18, False),
    (57.20, "lego_click", -15, False),                # icon row snaps in ("Czyli wykonać")
    (66.95, "lego_fall", -18, False),                 # PDF brick tumbles in the 941 scene
    (68.86, "boom", -12, False),                      # "941" + money burst
    (68.90, "money", -16, False),
    (78.28, "lego_click", -15, False),                # step 1 "Od pomysłu"
    (79.02, "lego_click2", -15, False),               # step 2 "do produktu"
    (81.42, "ding", -17, False),                      # "48 godzin" badge
    (82.68, "click", -11, True),                      # CTA "Kliknij"
    (84.20, "pop", -16, False),                       # yellow arrow down
]
sfx = [dict(t=t, f=S(n), db=db, peak=p) for t, n, db, p in ACC]
busy = [t for t, *_ in ACC]
wh, last = ["whoosh_a", "whoosh_b", "whoosh_c", "whoosh_d"], -9
for i, c in enumerate(CUTS):                          # whoosh on cuts, never two within 1 s, never on top of a story beat
    if c - last < 1.0 or (c not in BIG and any(abs(c - b) < 0.35 for b in busy if b not in (46.93, 46.95))): continue
    if c in HOOK_CUTS:
        sfx.append(dict(t=c, f=S("whip"), db=-21, peak=False)); last = c; continue
    if c == 46.933: last = c; continue                # cymbal + boom already mark it
    big = c in BIG
    sfx.append(dict(t=c, f=S("swoosh_big" if big else wh[i % 4]), db=-19 if big else -23, peak=True)); last = c
dur = lambda f: float(os.popen(f'ffprobe -v error -show_entries format=duration -of csv=p=0 "{f}"').read())
pk = {}
import numpy as np, subprocess
for s in sfx:                                         # trim anything that would ring across a hook cut
    if s["f"] not in pk:
        a = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", s["f"], "-ac", "1", "-ar", "8000", "-f", "s16le", "-"], capture_output=True).stdout, np.int16)
        pk[s["f"]] = float(np.argmax(np.abs(a.astype(np.int32)))) / 8000
    st = s["t"] - (pk[s["f"]] if s["peak"] else 0)
    for hc in HOOK_CUTS:
        if st < hc < st + dur(s["f"]): s["dur"] = round(hc - st - 0.01, 3)
mus = dict(music=sys.argv[3], musicStart=0, musicDb=-28.2, fadeOut=2.0, duckThreshold=0.01) if len(sys.argv) > 3 else {}
json.dump(dict(mus, sfx=sorted(sfx, key=lambda s: s["t"])), open(OUT, "w"), indent=1)
print(len(sfx), "sfx cues")
for s in sorted(sfx, key=lambda s: s["t"]): print(f'{s["t"]:6.2f} {os.path.basename(s["f"]):16s} {s["db"]:4d} dB' + (f' trim {s["dur"]}' if "dur" in s else ""))
