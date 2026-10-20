#!/usr/bin/env python3
"""Style 10 captions for AI song 2 (kurs/aisong2.mp4, 3:16). Konrad: captions a bit higher than song 1 (0.62).  usage: build_spec18.py WORKDIR NAME
Lyrics = faster-whisper (no VAD, condition_on_previous_text=False) corrected by hand; same caption treatment as the AI ads."""
import difflib, json, os, re, subprocess, sys
WD, NAME = sys.argv[1], sys.argv[2]
HERE = os.path.dirname(os.path.abspath(__file__))
norm = lambda t: re.sub(r"[^\w]", "", t.lower())
WEAK = set()
s6 = open(os.path.join(HERE, "..", "styl6", "build_spec6.py")).read()
exec(s6[s6.index("def align"):s6.index("src = os.path.join")])      # align() from style 6

SCRIPT = ("Wracam z roboty, osiemnasta trzydzieści. W lodówce światło, w głowie znowu ten szum. Na feedzie znowu typ w nowym Porsche "
          "bełkocze, że pensja to wstyd i że trzeba mieć luz. Więc siadam do biurka, odpalam to całe AI, dwanaście promptów, gotowy plik w PDF. "
          "Trzy noce w Canvie, układałem nagłówki. I na obiad znowu odgrzewam parówki. Wrzucam na stronę, czekam na pierwszy przelew. "
          "Odświeżam panel co dwadzieścia sekund. W statystykach od tygodnia dwa wejścia w niedzielę. Jedno z Bydgoszczy, to ciotka z ciekawości. "
          "Druga wizyta to jakiś bot z Indonezji. I tak się kończy ten wielki biznes w sieci, bo każdy Ci powie: weź, zrób produkt z AI, "
          "lecz nikt Ci nie powie, czemu nikt go nie kupuje. Siedzisz z tym plikiem jak z cegłą na dachu. Bez żadnej strony, bez ruchu, w strachu. "
          "Bo nikt nie kupi pliku od ducha. Sam PDF Ci życia nie zmieni, gdy nie masz systemu, co w tle to ogarnia. To Twoja praca idzie do piachu. "
          "Odpalam Autopilot. 48 godzin. Wszystko w jednym miejscu. Bez wstydu, bez twarzy. 17 złotych zamiast drogich subskrypcji. "
          "Wreszcie ktoś kupił. Wreszcie to działa. Kupiłem kiedyś kurs za dwa tysiące. Zostałem z długiem i stertą folderów. Tu nie ma lania "
          "wody o wolności finansowej. Dostajesz niszę, klikasz i gotowe. Nawet na reklamę dorzucają osiem stów, żebyś wreszcie ruszył, "
          "zamiast kląć po nocy znów. Bo nikt nie kupi pliku od ducha. Sam PDF Ci życia nie zmieni, gdy nie masz systemu, co w tle to ogarnia. "
          "To Twoja praca idzie do piachu. Odpalam Autopilot. 48 godzin. Wszystko w jednym miejscu. Bez wstydu, bez twarzy. 17 złotych zamiast "
          "drogich subskrypcji. Wreszcie ktoś kupił. Wreszcie to działa. Link masz na dole. Siedemnaście złotych. Gwarancja zwrotu, jak nic "
          "nie ogarniesz. Przestań wreszcie pisać do szuflady.")
BIG = {"szum", "porsche", "wstyd", "luz", "ai", "dwanaście", "promptów", "pdf", "canvie", "parówki", "przelew", "dwadzieścia", "sekund",
       "dwa", "wejścia", "bydgoszczy", "ciotka", "bot", "indonezji", "biznes", "kupuje", "cegłą", "strachu", "ducha", "systemu", "piachu",
       "autopilot", "48 godzin", "miejscu", "wstydu", "twarzy", "17 złotych", "subskrypcji", "kupił", "działa", "kurs", "tysiące", "długiem",
       "folderów", "wolności", "niszę", "gotowe", "osiem", "stów", "znów", "link", "dole", "siedemnaście", "złotych", "gwarancja", "zwrotu", "szuflady"}
src = os.path.join(WD, NAME + ".mp4")
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", src], capture_output=True, text=True).stdout)
words = [dict(s=w.get("t", w.get("s")), e=w["e"], w=w["w"]) for s in json.load(open(os.path.join(WD, "tr_" + NAME + ".json"))) for w in s["words"]]
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
FX = [dict(type="arrow", t0=161.8, t1=dur, x=540, y=1790, size=130)]                   # "Link masz na dole"
BLUR_CUTS = []
ZONES = []
spec = dict(dur=round(dur, 3), fps=30, capY=0.62, capSize=84, bigSize=112, capPunch=True, capZones=ZONES,
            caps=caps, fx=FX, blurCuts=BLUR_CUTS, hideCaps=[])
json.dump(spec, open(os.path.join(WD, f"spec10_{NAME}.json"), "w"), ensure_ascii=False, indent=1)
for c in caps: print(f'{c["t0"]:6.2f}-{c["t1"]:6.2f} {"*" if c["big"] else " "} {c["text"]}')
