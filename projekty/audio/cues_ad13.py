#!/usr/bin/env python3
"""Sound design + music for ad 13 (style 9, LEGO AI "gadający ziemniak", 3 hooks + body).  usage: cues_ad13.py SFXDIR MUSIC.mp3 OUT.json
Same palette and relative levels as ad12 (approved). The voice here is -20.3 LUFS vs -27.5 in ad12, so every SFX gets +7.2 dB
(VO_SHIFT) to keep the same SFX/voice balance. Music: Mixkit 173 "Better Times are Coming" (Konrad's pick for ad12), ~13 LU under
the voice. The track is 1:40 and the film 2:03, so the hooks play it from 0 and the body restarts it from 0 on the body cut:
exactly what each cut variant (hook + body) sounds like. Hook cuts: sounds start ON the cut, nothing rings across one."""
import json, os, subprocess, sys
import numpy as np
SD, MUSIC, OUT = sys.argv[1:4]
S = lambda n: os.path.join(SD, n + ".wav")
VO_SHIFT = 7.2
HOOK_CUTS = (11.3, 23.933, 40.233)
CUTS = [3.167, 4.233, 6.167, 11.3, 12.767, 16.367, 18.767, 20.233, 23.933, 29.067, 30.533, 32.5, 36.267, 40.233, 43.267, 48.167,
        50.533, 55.2, 57.9, 59.533, 62.0, 65.233, 68.533, 71.233, 72.433, 75.433, 77.967, 79.933, 82.667, 89.067, 90.3, 92.967,
        95.8, 101.2, 104.4, 107.133, 109.333, 111.9, 113.133, 114.933, 116.267, 120.033]
BIG = {55.2, 82.667, 92.967, 107.133}                 # section changes with the blur-in

ACC = [  # (t, sound, dB as in ad12 scale, peak-aligned)
    (8.58, "pop", -17, False),                        # "kreskówkowe postacie"
    (16.40, "ding", -21, False),                      # potato pops out of the tablet with sparkles
    (18.88, "lego_click", -14, False),                # red box "Tak."
    (19.68, "pop_low", -15, False),                   # "Ziemniak."
    (25.45, "lego_click", -15, False),                # box "kawa za 17 zł"
    (27.62, "kaching", -14, True),                    # box "ebook za 79 zł"
    (29.98, "pop", -18, False),                       # "gadający ziemniak?"
    (38.95, "coins", -16, False),                     # money rain "do zarabiania przez internet"
    (70.80, "lego_click", -16, False),                # "pomysł"
    (71.88, "lego_click2", -16, False),               # "ebooka"
    (73.30, "lego_click", -16, False),                # "stronę"
    (79.40, "click", -14, True),                      # "trafiają na stronę" (tap)
    (81.40, "notif", -18, False),                     # "może kupić" -> sale
    (87.72, "kaching", -13, True),                    # box "79 zł"
    (90.90, "coins", -15, False),                     # money rain "sprzedawać ... wielokrotnie"
    (92.00, "money", -19, False),
    (94.58, "boom", -16, False),                      # "Cyfrowy Autopilot" reveal
    (103.06, "ding", -17, False),                     # "48 godzin" badge
    (112.02, "rev_cymbal", -21, True),                # build-up into the price
    (112.02, "kaching", -13, True),                   # box "17 zł"
    (113.46, "click", -11, True),                     # CTA "kliknij przycisk"
    (113.62, "pop", -16, False),                      # yellow arrow
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
cues = dict(music=MUSIC, musicDb=round(-20.3 - 13 + 12.3, 1), fadeOut=2.0, duckThreshold=0.02,
            musicSegments=[[0, 40.233, 0], [40.233, 999, 0]], sfx=sorted(sfx, key=lambda s: s["t"]))
json.dump(cues, open(OUT, "w"), indent=1)
print(len(sfx), "sfx cues, music", cues["musicDb"], "dB")
for s in cues["sfx"]: print(f'{s["t"]:7.2f} {os.path.basename(s["f"]):16s} {s["db"]:5.1f} dB' + (f' trim {s["dur"]}' if "dur" in s else ""))
