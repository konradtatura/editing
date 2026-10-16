#!/usr/bin/env python3
"""Style 9 spec for ad 13 (LEGO AI, "gadający ziemniak", 3 hooks + body).  usage: build_spec13.py WORKDIR NAME
Needs WORKDIR/NAME.mp4, WORKDIR/tr_NAME.json (faster-whisper words t/e/w) and the tracked boxes WORKDIR/kf_*.json (track.py).
Konrad: captions "in the middle" but never over important on-screen text (ebook cover, prices, Cyfrowy Autopilot).
The middle band is busy, so captions sit at 40 % by default and move per SHOT (only on cuts) to 76 % or 30 % where the
40 % band hits text (picked from tesseract OCR + red/green colour mask of covers, price tags and buttons)."""
import difflib, json, os, re, subprocess, sys
WD, NAME = sys.argv[1], sys.argv[2]
HERE = os.path.dirname(os.path.abspath(__file__))
norm = lambda t: re.sub(r"[^\w]", "", t.lower())
WEAK = {"i", "w", "z", "na", "do", "a", "o", "że", "się", "to", "nie", "co", "ale", "ten", "niż", "go", "za", "tam", "bo", "od", "ci", "jak", "te"}
s6 = open(os.path.join(HERE, "..", "styl6", "build_spec6.py")).read()
exec(s6[s6.index("def align"):s6.index("src = os.path.join")])      # align() + chunk() from style 6

SCRIPT = ("Zwykli ludzie po cichu budują biznesy w internecie. A co najdziwniejsze? Nikt nawet nie wie, jak wyglądają. "
          "Bo zamiast nich klientów przyciągają kreskówkowe postacie stworzone przez AI. "
          "Ten koleś właśnie śpi. A w tym czasie ludzie oglądają reklamy jego AI ebooka, w której występuje gadający ziemniak. "
          "Tak. Ziemniak. I co najdziwniejsze? Ten ziemniak został stworzony przez AI. "
          "Co wspólnego mają kawa za 17 zł, ebook za 79 zł i gadający ziemniak? Brzmi jak jakiś idiotyczny żart. "
          "Ale te trzy rzeczy mogą pokazać Ci jeden z ciekawszych sposobów, jak zwykli ludzie wykorzystują AI do zarabiania przez internet. "
          "I to jest coś, czego większość ludzi jeszcze nie rozumie. Jeszcze niedawno, żeby tworzyć takie reklamy, "
          "potrzebowałeś animatorów, montażystów albo sam musiałeś występować przed kamerą. "
          "Dzisiaj AI może stworzyć Ci nawet gadającego, kreskówkowego ziemniaka. Wyobraź sobie. Siedzisz w domu. Nie jesteś znany. "
          "Nie chcesz nagrywać swojej twarzy. Ale tworzysz własną postać AI, która występuje w filmikach i promuje Twojego ebooka. "
          "A najlepsze? Nie musisz nawet umieć pisać ebooków. Bo AI może pomóc Ci znaleźć pomysł, stworzyć ebooka "
          "i przygotować stronę, na której ludzie mogą go kupić. Twoja kreskówkowa postać przyciąga uwagę. "
          "Zainteresowani trafiają na stronę. A część z nich może kupić Twojego ebooka. I teraz robi się ciekawie. "
          "Bo takiego ebooka możesz wystawić na sprzedaż na przykład za 79 zł. A kiedy już go stworzysz, "
          "możesz sprzedawać ten sam plik wielokrotnie. Właśnie dlatego powstał Cyfrowy Autopilot. "
          "System, który pokazuje zwykłym ludziom, jak z pomocą AI stworzyć własnego ebooka i stronę gotową do sprzedaży w 48 godzin. "
          "Nawet jeśli zaczynają od kompletnego zera. A ile kosztuje dostęp do całego systemu? "
          "Mniej więcej tyle, co zwykła kawa na mieście. 17 zł. Więc kliknij przycisk poniżej i zobacz, jak zacząć. "
          "Bo nie musisz zostać influencerem, żeby sprzedawać ebooki w internecie. Możesz stworzyć własnego dzięki AI.")
HOOK_CUTS = (11.3, 23.933, 40.233)   # hook 1 | hook 2 | hook 3 | body: no caption may straddle these
LOW, UP = 0.76, 0.30
ZONES = [(6.167, 11.3, LOW), (11.3, 12.767, LOW), (16.367, 18.767, LOW), (18.767, 20.233, UP), (30.533, 32.5, LOW),
         (43.267, 48.167, LOW), (48.167, 50.533, LOW), (55.2, 57.9, LOW), (82.667, 89.067, UP), (90.3, 92.967, UP),
         (111.9, 113.133, UP), (113.133, 114.933, UP), (116.267, 120.033, LOW), (120.033, 999, UP)]
src = os.path.join(WD, NAME + ".mp4")
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", src], capture_output=True, text=True).stdout)
words = [dict(s=w["t"], e=w["e"], w=w["w"]) for s in json.load(open(os.path.join(WD, "tr_" + NAME + ".json"))) for w in s["words"]]
toks = align(words, SCRIPT)
for i in range(len(toks) - 2, -1, -1):              # "17 zł" / "79 zł" = one token, never split or glued to the next word
    if toks[i]["d"].isdigit() and toks[i + 1]["d"].startswith("zł"):
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
FX = [TB("pot", 18.88, 20.233, 480, 900, pad=10, r=70),                     # "Tak. Ziemniak."
      TB("17a", 25.45, 26.9, 260, 180, r=26, rot=-3),                       # "kawa za 17 zł"
      TB("79a", 27.58, 29.067, 275, 150, r=26),                             # "ebook za 79 zł"
      dict(type="rain", t0=38.9, t1=40.233, emo=MONEY, n=22, spawn=1.0, seed=11),   # "do zarabiania przez internet"
      TB("79b", 87.65, 89.067, 560, 280, r=34),                             # "na przykład za 79 zł"
      dict(type="rain", t0=90.8, t1=92.967, emo=MONEY, n=26, spawn=1.3, seed=5),    # "sprzedawać ten sam plik wielokrotnie"
      TB("17b", 112.0, 113.133, 315, 110, r=24, rot=-3),                    # "17 zł"
      dict(type="arrow", t0=113.46, t1=dur, x=540, y=1690, size=170)]      # "kliknij przycisk poniżej"
BLUR_CUTS = [11.3, 23.933, 40.233, 55.2, 82.667, 92.967, 107.133]          # hook starts + section changes
spec = dict(dur=round(dur, 3), fps=30, capY=0.40,  # Konrad: one fixed height, no per-shot zones (ZONES kept as a fallback idea)
            caps=caps, fx=FX, blurCuts=BLUR_CUTS, hideCaps=[])
json.dump(spec, open(os.path.join(WD, f"spec9_{NAME}.json"), "w"), ensure_ascii=False, indent=1)
for c in caps: print(f'{c["t0"]:6.2f}-{c["t1"]:6.2f} {c["text"]}')
