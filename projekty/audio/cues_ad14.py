#!/usr/bin/env python3
"""Sound design + music for ad 14 (style 9, 3D "dropshipping vs AI ebooks", 3 hooks + body).  usage: cues_ad14.py SFXDIR MUSIC.mp3 OUT.json\nBuilt from cues_ad13.py (same palette, rules and music). Original ad13 notes:
Same palette and relative levels as ad12 (approved). The voice here is -20.3 LUFS vs -27.5 in ad12, so every SFX gets +7.2 dB
(VO_SHIFT) to keep the same SFX/voice balance. Music: Mixkit 173 "Better Times are Coming" (Konrad's pick for ad12), ~13 LU under
the voice. The track is 1:40 and the film 2:03, so the hooks play it from 0 and the body restarts it from 0 on the body cut:
exactly what each cut variant (hook + body) sounds like. Hook cuts: sounds start ON the cut, nothing rings across one."""
import json, os, subprocess, sys
import numpy as np
SD, MUSIC, OUT = sys.argv[1:4]
S = lambda n: os.path.join(SD, n + ".wav")
VO_SHIFT = 7.7                                         # voice -19.8 LUFS vs -27.5 in ad12
HOOK_CUTS = (14.967, 27.3, 41.1)
CUTS = [3.9, 5.033, 7.5, 9.133, 10.567, 12.4, 14.967, 17.633, 19.133, 21.367, 23.767, 24.433, 27.3, 28.867, 30.733, 32.967, 36.633,
        41.1, 45.7, 47.033, 50.067, 54.167, 58.0, 59.7, 60.733, 62.467, 65.7, 66.9, 71.2, 74.5, 75.7, 77.5, 80.433, 84.133, 87.167,
        91.9, 95.233, 97.133, 99.967, 102.033, 104.4, 107.967]
BIG = {65.7, 77.5, 97.133, 104.4}                     # section changes with the blur-in

ACC = [  # (t, sound, dB as in ad12 scale, peak-aligned)
    (2.36, "kaching", -14, True),                     # box "199 zł"
    (3.95, "coins", -19, False),                      # "i już świętuje"
    (6.50, "whoosh_b", -19, True),                    # "swoje zabiera dostawca" (snatch)
    (8.08, "whoosh_b", -19, True),                    # "swoje zabierają reklamy"
    (9.68, "whoosh_b", -19, True),                    # "dochodzi dostawa"
    (11.90, "buzz", -24, False),                      # "odeśle paczkę?" (ZWROT)
    (17.70, "notif", -18, False),                     # "Klient zamawia produkt"
    (23.84, "boom", -18, False),                      # "Ty!"
    (28.90, "pop", -16, False),                       # BRAK MAGAZYNU
    (36.63, "boom", -17, False),                      # parcels crush him ("fizyczne problemy")
    (38.62, "ding", -17, False),                      # the ebook appears ("coś, czego nie trzeba wysyłać")
    (58.60, "click", -15, True),                      # "wystawiasz go na swojej stronie"
    (60.48, "notif", -18, False),                     # "kiedy ktoś go kupi"
    (61.40, "pop", -17, False),                       # "otrzymuje plik automatycznie"
    (64.60, "coins", -15, False),                     # money rain "sprzedawać wielokrotnie"
    (74.06, "pop", -18, False),                       # "pomysł"
    (74.60, "pop", -18, False),                       # "przygotować ebooka"
    (76.42, "pop", -18, False),                       # "stronę sprzedażową"
    (79.20, "boom", -17, False),                      # "Cyfrowy Autopilot"
    (85.20, "boom", -12, False),                      # "941" + money burst
    (85.24, "money", -16, False),
    (94.10, "ding", -17, False),                      # "48 godzin"
    (98.90, "rev_cymbal", -21, True),                 # build-up into the price
    (98.90, "kaching", -13, True),                    # box "17 zł"
    (102.12, "click", -11, True),                     # CTA "Kliknij poniżej"
    (102.30, "pop", -16, False),                      # yellow arrow
    (111.55, "coins", -15, False),                    # final money rain "sprzedawać wielokrotnie"
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
# v3 music (Konrad picked B from 3 samples): Mixkit 322 "Life's a Movie" (film score, -19.3 LUFS), from 4.5 s (skips the quiet intro)
cues = dict(music=MUSIC, musicStart=4.5, musicDb=round(-19.8 - 13 + 19.3, 1), fadeOut=2.0, duckThreshold=0.02, sfx=sorted(sfx, key=lambda s: s["t"]))
json.dump(cues, open(OUT, "w"), indent=1)
print(len(sfx), "sfx cues, music", cues["musicDb"], "dB")
for s in cues["sfx"]: print(f'{s["t"]:7.2f} {os.path.basename(s["f"]):16s} {s["db"]:5.1f} dB' + (f' trim {s["dur"]}' if "dur" in s else ""))
