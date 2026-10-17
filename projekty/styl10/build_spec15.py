#!/usr/bin/env python3
"""Style 10 spec for ad 15 ("skill h2 v5": ebook / strona / megafon, one version, no hook variants).  usage: build_spec15.py WORKDIR NAME
Captions like Konrad's reference (the farting-man ad): ONE word at a time, CAPS, Montserrat 800, hard shadow, ~70 % height,
punch pop-in (128 % -> 90 % -> 103 % -> 100 % in 0.1 s), key words bigger. Words shorter than 0.12 s are glued to the next one.
Needs WORKDIR/NAME.mp4, tr_NAME.json, kf_17.json (styl9/track.py)."""
import difflib, json, os, re, subprocess, sys
WD, NAME = sys.argv[1], sys.argv[2]
HERE = os.path.dirname(os.path.abspath(__file__))
norm = lambda t: re.sub(r"[^\w]", "", t.lower())
WEAK = set()
s6 = open(os.path.join(HERE, "..", "styl6", "build_spec6.py")).read()
exec(s6[s6.index("def align"):s6.index("src = os.path.join")])      # align() from style 6

SCRIPT = ("Nie umiesz pisać ebooków? To jak zamierzasz mnie stworzyć? A co ze mną? Przecież nawet nie umiesz robić stron internetowych! "
          "Halo, halo! A marketing? Kto w ogóle dowie się, że ten ebook istnieje? Jeszcze kilka lat temu to był naprawdę spory problem. "
          "Musiałbyś nauczyć się zrobić to wszystko samodzielnie. Albo zapłacić komuś, kto zrobi to za Ciebie! "
          "Ale dzisiaj AI kompletnie zmieniło tę sytuację! Nie umiesz pisać ebooków? AI pomoże Ci przygotować moją treść! "
          "Nie umiesz robić stron? Z pomocą AI możesz zbudować mnie bez pisania kodu od zera! Nie znasz się na marketingu? "
          "AI może pomóc Ci przygotować pierwszą ofertę sprzedażową! I właśnie na tym polega największa zmiana. "
          "Nie musisz już spędzać miesięcy na nauce każdej z tych umiejętności, żeby zacząć! "
          "Bo AI może pomóc Ci zrobić rzeczy, których jeszcze nie potrafisz zrobić samodzielnie! "
          "Tylko musisz wiedzieć, jak połączyć to wszystko w jeden proces! I właśnie dlatego powstał Cyfrowy Autopilot. "
          "System, który pokazuje Ci krok po kroku, jak wykorzystać AI do stworzenia własnego produktu cyfrowego. "
          "Od znalezienia pomysłu, przez przygotowanie ebooka, aż po stronę, na której możesz go wystawić na sprzedaż. "
          "A wszystko według konkretnego procesu rozpisanego na 48 godzin! Bo dzisiaj najważniejsze pytanie nie brzmi, "
          "czy potrafię zrobić to wszystko samodzielnie? Tylko jak wykorzystać AI, żeby pomogło mi to zrobić? "
          "Kliknij poniżej i zobacz, jak działa cały proces. Zacznij z Cyfrowym Autopilotem już dzisiaj!")
BIG = {"ebooków", "ebooka", "ebook", "stron", "stronę", "internetowych", "marketing", "marketingu", "halo", "problem", "samodzielnie", "ai",
       "kompletnie", "zmieniło", "kodu", "zera", "ofertę", "zmiana", "miesięcy", "proces", "cyfrowy", "autopilot", "cyfrowym", "autopilotem",
       "48 godzin", "kliknij", "poniżej", "dzisiaj", "pytanie", "treść", "sprzedaż", "pomysłu"}
src = os.path.join(WD, NAME + ".mp4")
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", src], capture_output=True, text=True).stdout)
words = [dict(s=w["t"], e=w["e"], w=w["w"]) for s in json.load(open(os.path.join(WD, "tr_" + NAME + ".json"))) for w in s["words"]]
toks = align(words, SCRIPT)
for i in range(len(toks) - 2, -1, -1):              # "48 godzin" = one token
    if toks[i]["d"].isdigit() and toks[i + 1]["d"].startswith(("zł", "godzin")):
        toks[i]["d"] += " " + toks[i + 1]["d"]; toks[i]["e"] = toks[i + 1]["e"]; del toks[i + 1]
clean = lambda d: re.sub(r"[.,!?…:;]", "", d)
groups = []                                          # one word per caption; <0.12 s words glue onto the next
for k, u in enumerate(toks):
    nxt = toks[k + 1]["t"] if k + 1 < len(toks) else dur
    if groups and groups[-1]["glue"]:
        g = groups[-1]; g["w"].append(u); g["glue"] = False
    else:
        groups.append(dict(w=[u], glue=False))
    g = groups[-1]
    if nxt - g["w"][0]["t"] < 0.12 and not u["d"][-1] in ".?!" and len(clean(" ".join(x["d"] for x in g["w"]))) < 9: g["glue"] = True
caps = []
for i, g in enumerate(groups):
    t0 = g["w"][0]["t"] - 0.03; nxt = groups[i + 1]["w"][0]["t"] - 0.03 if i + 1 < len(groups) else dur
    end = g["w"][-1]["e"]; t1 = nxt if nxt - end < 0.6 else min(nxt, end + 0.3)
    text = clean(" ".join(x["d"] for x in g["w"]))
    caps.append(dict(t0=round(max(0, t0), 3), t1=round(t1, 3), text=text, big=any(norm(x["d"]) in {norm(b) for b in BIG} for x in g["w"])))
KF = lambda n: json.load(open(os.path.join(WD, f"kf_{n}.json")))
TB = lambda n, t0, t1, w, h, pad=16, **k: dict(type="box", t0=t0, t1=t1, x=KF(n)[0][1] - pad, y=KF(n)[0][2] - pad, w=w + 2 * pad, h=h + 2 * pad,
                                              kf=KF(n), dx=-pad, dy=-pad, **k)
FX = [dict(type="arrow", t0=88.2, t1=91.133, x=540, y=1800, size=130),     # "Kliknij poniżej" (below the card's button)
      TB("17", 91.25, dur, 520, 230, r=30)]                                # price on the final card
BLUR_CUTS = [3.567, 7.6, 12.5, 21.267, 40.3, 56.967, 79.3, 88.067]        # scene changes
ZONES = [[88.067, 91.133, 0.885]]                                           # first CTA card shot: 70 % would sit on "17 zł"
spec = dict(dur=round(dur, 3), fps=30, capY=0.70, capSize=84, bigSize=112, capPunch=True, capZones=ZONES,
            caps=caps, fx=FX, blurCuts=BLUR_CUTS, hideCaps=[])
json.dump(spec, open(os.path.join(WD, f"spec10_{NAME}.json"), "w"), ensure_ascii=False, indent=1)
for c in caps: print(f'{c["t0"]:6.2f}-{c["t1"]:6.2f} {"*" if c["big"] else " "} {c["text"]}')
