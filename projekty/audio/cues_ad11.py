#!/usr/bin/env python3
"""Sound design cues for ad11.  usage: cues_ad11.py WORKDIR(ad11) AUDIODIR OUT.json"""
import json, os, sys
WD, AD, OUT = sys.argv[1:4]
S = lambda n: os.path.join(AD, "sfx", n + ".mp3")
cuts = json.load(open(os.path.join(WD, "cuts.json")))
spec = json.load(open(os.path.join(WD, "spec4_ad11.json")))

sfx, last = [], -9
whooshes = ["whoosh_fast", "sweep", "whoosh_trans"]
for i, c in enumerate(cuts):                      # soft whoosh on scene changes, never two within 1 s
    if c - last < 1.0: continue
    sfx.append(dict(t=c, f=S(whooshes[i % 3]), db=-17, peak=True)); last = c
for cp in spec["caps"]:                           # yellow emphasis words get a light pop
    if cp["em"] and "17" not in cp["html"]: sfx.append(dict(t=cp["t0"], f=S("pop_whoosh"), db=-12))
hit = lambda txt: next(cp["t0"] for cp in spec["caps"] if txt in cp["html"])
sfx += [dict(t=hit("941"), f=S("coins"), db=-11),                # 941 e-booków
        dict(t=hit("Automatycznie"), f=S("pop_msg"), db=-13),    # someone buys -> gets the product
        dict(t=hit("17 zł"), f=S("coin_prize"), db=-13),         # price reveal
        dict(t=hit("Kliknij przycisk"), f=S("click_select"), db=-9)]
json.dump(dict(music=os.path.join(AD, "music", "mk_140.mp3"), musicStart=0, musicDb=-21, fadeOut=2.0, sfx=sorted(sfx, key=lambda s: s["t"])),
          open(OUT, "w"), indent=1)
print(len(sfx), "sfx cues")
