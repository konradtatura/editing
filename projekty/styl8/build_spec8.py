#!/usr/bin/env python3
"""Style 8 (tier list) spec.  usage: build_spec8.py WORKDIR NAME   (WORKDIR/NAME.mp4 + WORKDIR/tr_NAME.json)"""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "styl6"))
WD, NAME = sys.argv[1], sys.argv[2]
HERE = os.path.dirname(os.path.abspath(__file__)); EM = os.path.join(HERE, "engine", "emoji_apple")
import importlib.util, subprocess
spec6 = open(os.path.join(HERE, "..", "styl6", "build_spec6.py")).read()
import re, difflib
norm = lambda t: re.sub(r"[^\w]", "", t.lower())
WEAK = {"i", "w", "z", "na", "do", "a", "o", "że", "się", "to", "nie", "co", "ale", "ten", "niż", "go"}
exec(spec6[spec6.index("def align"):spec6.index("src = os.path.join")])          # reuse align() + chunk() from style 6
import re, difflib
norm = lambda t: re.sub(r"[^\w]", "", t.lower())
WEAK = {"i", "w", "z", "na", "do", "a", "o", "że", "się", "to", "nie", "co", "ale", "ten", "niż", "go", "na"}
SCRIPT = ("Dropshipping z AI: D. Większość ludzi, którzy go promują, zarabia więcej na sprzedawaniu Ci narzędzi niż na samym dropshippingu. "
          "Modelki AI: F. Chyba nie muszę komentować. AI YouTube Shorts: poziom C. Fajne pod wyświetlenia, ale YouTube przestał płacić za content AI. "
          "Budowanie stron: F. AI zastąpiło Cię 3 lata temu, a Twój lokalny dentysta nie potrzebuje kolejnej strony. "
          "Montowanie filmów: poziom B. Da się na tym zarobić, ale to po prostu drugi etat. Tworzenie AI agentów i automatyzacji: poziom A. "
          "Większość firm w Polsce tego nie ma, tylko musisz tłumaczyć 60-latkom, co to AI, i cały czas gonić klientów. "
          "Tworzenie prostych produktów cyfrowych z pomocą AI: poziom S. Możesz stworzyć produkt w 100% z AI, a później sprzedawać go wielokrotnie "
          "bez konieczności wykonywania całej pracy od nowa. Plus cały content AI wchodzi bardzo mocno w viral. Dlatego zamiast szukać kolejnego "
          "sposobu na szybkie pieniądze, zacznij budować coś, co realnie działa. A jeżeli chcesz dowiedzieć się, jak to zrobić, "
          "skomentuj „AI”, a wyślę Ci mój cały poradnik.")
# (label, emoji codepoint, tier, drop time = when the tier letter is said, tray order)
ITEMS = [("Dropshipping z AI", "1f4e6", "D", 0.80, 3), ("Modelki AI", "1f483", "F", 5.60, 0), ("AI YouTube Shorts", "1f3ac", "C", 8.30, 5),
         ("Strony WWW", "1f4bb", "F", 11.92, 1), ("Montaż filmów", "1f3a5", "B", 17.20, 6), ("AI agenci", "1f916", "A", 21.56, 2),
         ("Produkty cyfrowe", "1f4d8", "S", 28.98, 4)]
TIERS = [("S", "#FF8A7B"), ("A", "#FFC079"), ("B", "#FFDA76"), ("C", "#FEF575"), ("D", "#B9F078"), ("F", "#73EA7B")]
src = os.path.join(WD, NAME + ".mp4")
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", src], capture_output=True, text=True).stdout)
words = [w for s in json.load(open(os.path.join(WD, "tr_" + NAME + ".json"))) for w in s["words"]]
ch = chunk(align(words, SCRIPT), maxw=3, maxc=18)
caps = []
for i, c in enumerate(ch):
    nxt = ch[i + 1][0]["t"] - 0.03 if i + 1 < len(ch) else dur
    t1 = nxt if nxt - c[-1]["e"] < 0.7 else min(nxt, c[-1]["e"] + 0.35)
    caps.append(dict(t0=round(max(0, c[0]["t"] - 0.03), 3), t1=round(t1, 3), text=" ".join(w["d"] for w in c).rstrip(",.:")))
# original 720x1280 x1.5: panel to y 808, title pill y 115-172, rows 64 px every 72 px from y 198, labels x 47-113, bars x 122-672, tray ~y 640
layout = dict(panelH=0, titleY=150, titleFs=56, rowsY=282, rowH=96, pitch=108, labX=70, labW=99, barX=183, marginR=72,
              slot=84, nameFs=32, tray=72, trayGap=14, trayY=950, capY=1054, dragDur=0.6)
spec = dict(dur=round(dur, 3), fps=30, title="TIERLISTA <b>AI BIZNESÓW</b>", layout=layout, hand=os.path.join(EM, "1f446.png"),
            tiers=[dict(k=k, c=c) for k, c in TIERS], caps=caps,
            items=[dict(name=n, img=os.path.join(EM, e + ".png"), tier=tr, t=t, tray=o) for n, e, tr, t, o in ITEMS],
            ctaT=42.55, ctaType=42.72, ctaWord="AI", ctaPost=43.35)
json.dump(spec, open(os.path.join(WD, f"spec8_{NAME}.json"), "w"), ensure_ascii=False, indent=1)
for c in caps: print(f'{c["t0"]:6.2f} {c["text"]}')
