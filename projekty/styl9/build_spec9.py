#!/usr/bin/env python3
"""Style 9 (LEGO AI ad) spec.  usage: build_spec9.py WORKDIR NAME   (WORKDIR/NAME.mp4 + WORKDIR/tr_NAME.json)
Captions from the script aligned onto whisper times (1-2 words, hard cuts), never crossing a hook boundary cut;
plus the original's extra layer (red boxes, money rain/burst, CTA arrow) and blur-in on a few section cuts (done in compose)."""
import difflib, json, os, re, subprocess, sys
WD, NAME = sys.argv[1], sys.argv[2]
HERE = os.path.dirname(os.path.abspath(__file__)); EM = os.path.join(HERE, "engine", "emoji_apple")
norm = lambda t: re.sub(r"[^\w]", "", t.lower())
WEAK = {"i", "w", "z", "na", "do", "a", "o", "że", "się", "to", "nie", "co", "ale", "ten", "niż", "go", "za", "tam", "bo", "od", "ci"}
s6 = open(os.path.join(HERE, "..", "styl6", "build_spec6.py")).read()
exec(s6[s6.index("def align"):s6.index("src = os.path.join")])      # align() + chunk() from style 6

SCRIPT = ("Otwórz TikToka. Zobaczysz tam dziesiątki postaci wygenerowanych przez sztuczną inteligencję. Ale najciekawsze jest to, "
          "że takie postacie są wykorzystywane do zarabiania tysięcy złotych miesięcznie. I nie, nie chodzi o pieniądze z wyświetleń. "
          "Otwórz TikToka i znajdź dowolną postać stworzoną przez AI. Teraz sprawdź jedną rzecz. Link w jej bio, bo właśnie tam może "
          "kryć się cały biznes, o którym większość ludzi nie ma pojęcia. Za takimi profilami często może stać coś znacznie ciekawszego "
          "niż same filmiki. Wyobraź sobie postać AI, która codziennie pokazuje proste przepisy kulinarne. A w swoim bio sprzedaje "
          "poradnik z przepisami za 79 złotych. Ktoś ogląda filmik, klika link i kupuje produkt. Bez magazynu. Bez wysyłania paczek. A ten "
          "sam produkt można sprzedawać wielokrotnie. I tutaj robi się naprawdę ciekawie. Bo AI może pomóc Ci nie tylko stworzyć taką "
          "postać. Może również znaleźć pomysł na produkt, przeanalizować rynek, stworzyć sam produkt, zbudować stronę sprzedażową "
          "i przygotować marketing. Czyli wykonać dużą część pracy, do której kiedyś potrzebowałeś kilku różnych umiejętności. "
          "Konrad, twórca Cyfrowego Autopilota, sprzedaje produkty cyfrowe od ponad 3 lat. W swoim najlepszym dniu sprzedał aż 941 "
          "e-booków. I na podstawie swojego doświadczenia stworzył system, który pokazuje, jak wykorzystać AI do budowania własnego "
          "biznesu cyfrowego. Od pomysłu do produktu i strony gotowej do sprzedaży w 48 godzin. Kliknij poniżej i zobacz, jak zacząć "
          "budować własny biznes cyfrowy z AI.")
HOOK_CUTS = (12.767, 23.133)        # hook 1 | hook 2 | body: no caption may straddle these (Konrad cuts the variants himself)
src = os.path.join(WD, NAME + ".mp4")
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", src], capture_output=True, text=True).stdout)
words = [w for s in json.load(open(os.path.join(WD, "tr_" + NAME + ".json"))) for w in s["words"]]
toks = align(words, SCRIPT)
for a, b in zip(toks, toks[1:]):                     # show "79 zł" although "79 złotych" is said
    if a["d"] == "79" and b["d"].startswith("złotych"): b["d"] = "zł" + b["d"][7:]
ch = chunk(toks, maxw=2, maxc=14)
merged = []                                          # no flash chunks: anything under 0.3 s joins its neighbour
for c in ch:
    if merged and (c[0]["t"] - merged[-1][0]["t"] < 0.3 or merged[-1][-1]["d"] == "79") and len(" ".join(w["d"] for w in merged[-1] + c)) <= 20 \
            and not merged[-1][-1]["d"].endswith((".", "?", "!")):
        merged[-1] = merged[-1] + c
    else: merged.append(c)
ch = merged
caps = []
for i, c in enumerate(ch):
    nxt = ch[i + 1][0]["t"] - 0.03 if i + 1 < len(ch) else dur
    t1 = nxt if nxt - c[-1]["e"] < 0.6 else min(nxt, c[-1]["e"] + 0.3)
    caps.append(dict(t0=round(max(0, c[0]["t"] - 0.03), 3), t1=round(t1, 3), text=" ".join(w["d"] for w in c).rstrip(",")))
for cut in HOOK_CUTS:
    for cp in caps:
        if cp["t0"] < cut < cp["t1"]:
            if cut - cp["t0"] > cp["t1"] - cut: cp["t1"] = cut
            else: cp["t0"] = cut
I = lambda c: os.path.join(EM, c + ".png")
MONEY, COINS = ["💵", "💵", "💸", "💵", "💰"], ["💰", "💵"]
FX = [dict(type="rain", t0=8.15, t1=10.43, emo=MONEY, n=26, spawn=1.3, seed=11),                 # "zarabiania tysięcy złotych miesięcznie"
      dict(type="box", t0=18.1, t1=18.66, x=350, y=1000, w=565, h=140, rot=3, r=34),              # "Link w jej bio"
      dict(type="box", t0=35.85, t1=37.36, x=595, y=1345, w=275, h=150, r=22),                     # "79 zł"
      dict(type="rain", t0=43.4, t1=44.75, emo=COINS, n=14, spawn=.8, seed=5),                   # "sprzedawać wielokrotnie"
      dict(type="burst", t0=68.84, t1=70.9, x=540, y=760, emo=MONEY, n=30, seed=9),              # "941"
      dict(type="arrow", t0=84.05, t1=dur, x=540, y=1560, size=170)]                              # CTA
BLUR_CUTS = [12.767, 23.133, 28.4, 62.067, 78.033]  # section changes: 0.2 s blur-in like the original
HIDE = [[66.7, 70.86]]                               # 941 scene already shows "e-booków w najlepszym dniu"
spec = dict(dur=round(dur, 3), fps=30, capY=0.645, caps=caps, fx=FX, blurCuts=BLUR_CUTS, hideCaps=HIDE)
json.dump(spec, open(os.path.join(WD, f"spec9_{NAME}.json"), "w"), ensure_ascii=False, indent=1)
for c in caps: print(f'{c["t0"]:6.2f} {c["text"]}')
