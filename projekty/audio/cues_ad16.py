#!/usr/bin/env python3
"""Sound design + music for ad 15 (style 10, "skill h2 v5", one version).  usage: cues_ad16.py SFXDIR MUSIC.mp3 OUT.json\nBuilt from cues_ad13.py (same palette, rules and music). Original ad13 notes:
Same palette and relative levels as ad12 (approved). The voice here is -20.3 LUFS vs -27.5 in ad12, so every SFX gets +7.2 dB
(VO_SHIFT) to keep the same SFX/voice balance. Music: Mixkit 173 "Better Times are Coming" (Konrad's pick for ad12), ~13 LU under
the voice. The track is 1:40 and the film 2:03, so the hooks play it from 0 and the body restarts it from 0 on the body cut:
exactly what each cut variant (hook + body) sounds like. Hook cuts: sounds start ON the cut, nothing rings across one."""
import json, os, subprocess, sys
import numpy as np
SD, MUSIC, OUT = sys.argv[1:4]   # + optional MUSIC_START MUSIC_DB
S = lambda n: os.path.join(SD, n + ".wav")
VO_SHIFT = 4.2                                         # voice -23.3 LUFS vs -27.5 in ad12
HOOK_CUTS = ()
CUTS = [2.8, 5.533, 7.967, 11.133, 12.3, 15.733, 17.133, 21.733, 22.967, 26.033, 28.6, 32.067, 35.467, 38.7, 41.167, 43.633, 46.5,
        48.867, 52.3, 54.3, 56.033, 57.767, 61.333, 64.3, 66.767, 70.567, 73.933, 77.1, 81.3, 83.433, 85.433, 86.167, 89.8]
BIG = {15.733, 32.067, 43.633, 61.333, 83.433}        # scene changes with the blur-in

ACC = [  # (t, sound, dB as in ad12 scale, peak-aligned)
    (2.33, "buzz", -23, False),                       # "kolejnego maila" (refuses)
    (6.57, "pop", -16, False), (8.29, "pop", -16, False), (10.27, "pop", -16, False),   # 14 maili / 6 obrazków / 30 pytań
    (11.71, "boom", -19, False),                      # "najgorsze"
    (21.17, "ding", -18, False),                      # "coś własnego"
    (25.47, "kaching", -15, True),                    # "na sprzedaż"
    (32.17, "pop", -15, False), (32.59, "pop", -15, False),   # "Halo, halo!"
    (40.26, "click", -14, True),                      # "własną stronę"
    (53.30, "ding", -17, False),                      # "należy do Ciebie"
    (56.22, "kaching", -15, True),                    # "sprzedawać więcej niż raz"
    (63.10, "boom", -15, False),                      # "Cyfrowy Autopilot"
    (79.98, "ding", -16, False),                      # "48 godzin"
    (85.56, "pop", -15, False),                       # "Będę!"
    (89.90, "click", -11, True),                      # CTA "Kliknij poniżej"
    (90.05, "pop", -16, False),                       # yellow arrow
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
