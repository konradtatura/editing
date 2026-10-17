#!/usr/bin/env python3
"""Style 9 spec for ad 14 (3D "dropshipping vs AI ebooks", 3 hooks + body).  usage: build_spec14.py WORKDIR NAME
Same caption look as ad13 v3 (Konrad: 39 % from the bottom, 28 px). Needs WORKDIR/NAME.mp4, tr_NAME.json, kf_*.json (track.py)."""
import difflib, json, os, re, subprocess, sys
WD, NAME = sys.argv[1], sys.argv[2]
HERE = os.path.dirname(os.path.abspath(__file__))
norm = lambda t: re.sub(r"[^\w]", "", t.lower())
WEAK = {"i", "w", "z", "na", "do", "a", "o", "że", "się", "to", "nie", "co", "ale", "ten", "niż", "go", "za", "tam", "bo", "od", "ci", "jak", "te"}
s6 = open(os.path.join(HERE, "..", "styl6", "build_spec6.py")).read()
exec(s6[s6.index("def align"):s6.index("src = os.path.join")])      # align() + chunk() from style 6

SCRIPT = ("Ten gość właśnie sprzedał produkt za 199 zł. I już świętuje. Tylko że teraz swoje zabiera dostawca. "
          "Swoje zabierają reklamy. Do tego dochodzi dostawa. A jeśli klient odeśle paczkę? No cóż, witamy w dropshippingu. "
          "Wyobraź sobie, że prowadzisz sklep internetowy. Klient zamawia produkt. Ale paczka nigdy do niego nie dociera. "
          "I zgadnij, kto musi się z tego tłumaczyć? Ty. Mimo że nigdy nawet nie miałeś tego produktu w rękach. "
          "Najdziwniejsze w dropshippingu? Nawet jeśli nie masz magazynu, nadal sprzedajesz fizyczne produkty. "
          "A fizyczne produkty mają fizyczne problemy. Ale co, gdybyś mógł sprzedawać coś, czego w ogóle nie trzeba wysyłać? "
          "I właśnie dlatego warto przyjrzeć się zupełnie innemu modelowi biznesowemu. Sprzedaży ebooków. "
          "Zamiast szukać dostawców i martwić się przesyłkami, tworzysz jeden prosty poradnik, który rozwiązuje konkretny problem. "
          "Na przykład ebook o tym, jak lepiej zarządzać domowym budżetem. Wystawiasz go na swojej stronie. "
          "Kiedy ktoś go kupi, otrzymuje plik automatycznie. A tego samego ebooka możesz sprzedawać wielokrotnie. "
          "I teraz najciekawsze. Dzięki AI nie musisz być pisarzem ani ekspertem od technologii. "
          "Bo sztuczna inteligencja może pomóc Ci znaleźć pomysł, przygotować ebooka i stworzyć stronę sprzedażową. "
          "Właśnie na tym opiera się Cyfrowy Autopilot. System stworzony przez Konrada, który w swoim najlepszym dniu sprzedał aż 941 ebooków. "
          "Pokazuje krok po kroku, jak z pomocą AI przygotować własnego ebooka i stronę gotową do sprzedaży w 48 godzin. "
          "Nawet jeśli zaczynasz od zera. A dostęp kosztuje jedyne 17 zł. Mniej więcej tyle, co kawa na mieście. "
          "Kliknij poniżej i zobacz, jak zacząć. Bo może wcale nie potrzebujesz kolejnego sklepu internetowego. "
          "Może potrzebujesz tylko jednego ebooka, którego możesz sprzedawać wielokrotnie.")
HOOK_CUTS = (14.967, 27.3, 41.1)   # hook 1 | hook 2 | hook 3 | body: no caption may straddle these
src = os.path.join(WD, NAME + ".mp4")
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", src], capture_output=True, text=True).stdout)
words = [dict(s=w["t"], e=w["e"], w=w["w"]) for s in json.load(open(os.path.join(WD, "tr_" + NAME + ".json"))) for w in s["words"]]
toks = align(words, SCRIPT)
for i in range(len(toks) - 2, -1, -1):              # "17 zł" / "199 zł" = one token, never split or glued to the next word
    if toks[i]["d"].isdigit() and toks[i + 1]["d"].startswith(("zł", "godzin")):
        toks[i]["d"] += " " + toks[i + 1]["d"]; toks[i]["e"] = toks[i + 1]["e"]; del toks[i + 1]
ch = chunk(toks, maxw=2, maxc=14)
merged = []                                          # no flash chunks (<0.3 s)
for c in ch:
    if merged and c[0]["t"] - merged[-1][0]["t"] < 0.3 and len(" ".join(w["d"] for w in merged[-1] + c)) <= 20 \
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
KF = lambda n: json.load(open(os.path.join(WD, f"kf_{n}.json")))
TB = lambda n, t0, t1, w, h, pad=16, **k: dict(type="box", t0=t0, t1=t1, x=KF(n)[0][1] - pad, y=KF(n)[0][2] - pad, w=w + 2 * pad, h=h + 2 * pad,
                                              kf=KF(n), dx=-pad, dy=-pad, **k)
MONEY = ["💵", "💵", "💸", "💵", "💰"]
FX = [TB("199", 2.3, 3.9, 400, 190, r=30),                                  # "sprzedał produkt za 199 zł"
      dict(type="rain", t0=64.45, t1=65.7, emo=MONEY, n=22, spawn=0.9, seed=11),    # "sprzedawać wielokrotnie"
      dict(type="burst", t0=85.2, t1=87.167, x=540, y=1300, emo=MONEY, n=30, seed=9), # "941"
      TB("17", 98.85, 99.967, 395, 160, r=26),                              # "jedyne 17 zł"
      dict(type="arrow", t0=102.12, t1=dur, x=540, y=1690, size=170),       # "Kliknij poniżej"
      dict(type="rain", t0=111.45, t1=dur, emo=MONEY, n=24, spawn=1.0, seed=5)]     # final "sprzedawać wielokrotnie"
BLUR_CUTS = [14.967, 27.3, 41.1, 65.7, 77.5, 97.133, 104.4]               # hook starts + section changes
HIDE = [[84.133, 87.167]]                                                  # 941 scene already says "941 sprzedanych ebooków"
spec = dict(dur=round(dur, 3), fps=30, capY=0.61, capSize=28,  # same as ad13 v3
            caps=caps, fx=FX, blurCuts=BLUR_CUTS, hideCaps=HIDE)
json.dump(spec, open(os.path.join(WD, f"spec9_{NAME}.json"), "w"), ensure_ascii=False, indent=1)
for c in caps: print(f'{c["t0"]:6.2f}-{c["t1"]:6.2f} {c["text"]}')
