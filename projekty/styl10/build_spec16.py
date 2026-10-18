#!/usr/bin/env python3
"""Style 10 spec for ad 16 ("CREATOR H1 V5": AI slime / mail / ebook / strona, one version).  usage: build_spec16.py WORKDIR NAME
No script from Konrad: text = cleaned transcript. Same treatment as ad 15 (his "jak zwykle AI montujesz").
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

SCRIPT = ("Nie, nie napiszę Ci kolejnego maila. Ej, spokojnie, przecież od tego jesteś. Od rana napisałem 14 maili, zrobiłem 6 obrazków "
          "i odpowiedziałem na 30 pytań. Wiesz, co jest najgorsze? Że ludzie wykorzystują tylko małą część tego, co potrafię. "
          "To co jeszcze niby potrafisz? Zamiast tylko zadawać mi pytania, możesz wykorzystać mnie do stworzenia czegoś własnego. "
          "Na przykład mnie, własnego ebooka, którego możesz wystawić na sprzedaż. Dokładnie. Mogę pomóc Ci znaleźć temat, "
          "przygotować spis treści i stworzyć pierwszą wersję rozdziałów. Halo, halo! A gdzie zamierzasz sprzedawać tego ebooka? "
          "Spokojnie! Z pomocą odpowiednich narzędzi AI możesz też zbudować własną stronę sprzedażową. No dobra, ale co w tym "
          "takiego wyjątkowego? Pomyśl. Kiedy używasz mnie do napisania maila, po prostu szybciej wykonujesz jedno zadanie. Ale kiedy "
          "wykorzystujesz AI do stworzenia własnego produktu, masz coś, co należy do Ciebie. Coś, co możesz rozwijać i sprzedawać "
          "więcej niż raz. Okej, ale skąd mam wiedzieć, jak to wszystko połączyć? I właśnie dlatego powstał Cyfrowy Autopilot! "
          "System, który pokazuje Ci krok po kroku, jak wykorzystać AI do stworzenia własnego produktu cyfrowego. Od znalezienia "
          "pomysłu, przez przygotowanie produktu, aż po stronę, na której możesz wystawić go na sprzedaż! Wszystko według "
          "konkretnego procesu, rozpisanego na 48 godzin. Bez konieczności pokazywania twarzy! Czyli co? Już nie będziesz pisać "
          "maili? Będę! Ale może tym razem zbudujemy też coś, co możesz sprzedawać? Kliknij poniżej i zacznij działać już dzisiaj!")
BIG = {"maila", "maili", "14", "6", "30", "najgorsze", "małą", "własnego", "ebooka", "sprzedaż", "temat", "halo", "stronę", "sprzedażową",
       "wyjątkowego", "pomyśl", "jedno", "produktu", "ciebie", "raz", "cyfrowy", "autopilot", "48 godzin", "twarzy", "będę", "kliknij",
       "poniżej", "dzisiaj", "ai", "pytań", "obrazków"}
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
FX = [dict(type="arrow", t0=89.90, t1=dur, x=540, y=1790, size=130)]                    # "Kliknij poniżej"
BLUR_CUTS = [15.733, 32.067, 43.633, 61.333, 83.433]                       # scene changes
ZONES = [[61.333, 64.3, 0.885], [77.1, 81.3, 0.885], [89.8, 999, 0.24]]   # on-screen text at ~70 % in these shots
spec = dict(dur=round(dur, 3), fps=30, capY=0.70, capSize=84, bigSize=112, capPunch=True, capZones=ZONES,
            caps=caps, fx=FX, blurCuts=BLUR_CUTS, hideCaps=[])
json.dump(spec, open(os.path.join(WD, f"spec10_{NAME}.json"), "w"), ensure_ascii=False, indent=1)
for c in caps: print(f'{c["t0"]:6.2f}-{c["t1"]:6.2f} {"*" if c["big"] else " "} {c["text"]}')
