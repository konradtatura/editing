#!/usr/bin/env python3
"""Style-3 render specs for ads5 and ads2.  usage: build_spec3.py WORKDIR STOCKDIR
Caption markup in FIX: *word* = blue box, ~word~ = serif italic typed; join multi-word with _."""
import difflib, json, os, re, subprocess, sys
WD, ST = sys.argv[1], sys.argv[2]
HERE = os.path.dirname(os.path.abspath(__file__))
WEAK = {"i", "w", "z", "na", "do", "od", "po", "a", "o", "że", "bo", "się", "to", "jak", "czy", "nie", "co", "za", "ci", "ten", "tego", "mi"}
GRADE = ("eq=contrast=1.06:saturation=0.9:brightness=-0.025,colorbalance=rs=-0.02:bs=0.03:bm=0.02,"
         "curves=all='0/0.02 0.5/0.47 1/0.95',vignette=angle=PI/4.5")
norm = lambda t: re.sub(r"[^\w]", "", t.lower())


def align(words, fixed):
    toks = []
    for raw in fixed.split():
        h = 1 if raw.startswith("*") else 2 if raw.startswith("~") else 0
        for k, p in enumerate(raw.strip("*~").split("_")): toks.append({"d": p, "h": h, "join": k > 0})
    a = [norm(w["w"]) for w in words]; b = [norm(t["d"]) for t in toks]; times = [None] * len(toks)
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        if op == "equal":
            for k in range(i2 - i1): times[j1 + k] = words[i1 + k]["s"]
        elif op == "replace":
            s0, e0 = words[i1]["s"], words[i2 - 1]["e"]
            for j in range(j1, j2): times[j] = s0 + (e0 - s0) * (j - j1) / max(1, j2 - j1)
    for j in range(len(toks)):
        if times[j] is None: times[j] = next((times[k] for k in range(j - 1, -1, -1) if times[k] is not None), 0.0)
    for j, t in enumerate(toks): t["t"] = round(times[j], 3)
    return toks


def chunk(units, maxw=4, maxc=20):
    blocks, cur = [], []
    def flush():
        if cur: blocks.append(cur[:]); cur.clear()
    for u in units:
        clen = sum(len(x["d"]) + 1 for x in cur) + len(u["d"])
        if cur and not u["join"] and (len(cur) >= maxw or clen > maxc):
            carry = []
            while len(cur) > 1 and (cur[-1]["d"].lower().strip(",.?") in WEAK or cur[-1]["d"].isdigit()): carry.insert(0, cur.pop())
            flush(); cur.extend(carry)
        cur.append(u)
        if u["d"].endswith((".", "?", "!")): flush()
    flush()
    return [{"t0": b[0]["t"], "words": [{"d": w["d"], "t": w["t"], "h": w["h"]} for w in b]} for b in blocks]


def dur(p): return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p], capture_output=True, text=True).stdout)
def cuts(p): return json.loads(subprocess.run([sys.executable, os.path.join(HERE, "..", "reklamy_CA", "engine", "cuts.py"), p], capture_output=True, text=True).stdout)
def pw(lst): return [{"d": w, "t": t, "h": h} for w, t, h in lst]
STILL = lambda n: os.path.join(ST, "stills", n + ".jpg")


def make(name, src, trname, fixed, items, extra_cuts=(), capY=0.6, brolls=()):
    srcp = os.path.join(WD, src); sd = round(dur(srcp), 3); cs = sorted(set(cuts(srcp)) | set(extra_cuts))
    words = [w for s in json.load(open(os.path.join(WD, trname))) for w in s["words"]]
    caps = chunk(align(words, fixed))
    z, big = [], False
    for t in [0.0] + cs: z.append([t, 1.14 if big else 1.0]); big = not big
    spec = dict(src=srcp, srcDur=sd, dur=sd, fps=30, capY=capY, caps=caps, items=items, brolls=list(brolls),
                cuts=cs, zooms=z, zoomCenter=[0.5, 0.3], grade=GRADE)
    p = os.path.join(WD, f"spec3_{name}.json"); json.dump(spec, open(p, "w"), ensure_ascii=False, indent=1)
    print(p, len(caps), "caption blocks,", len(cs), "cuts")
    for b in caps: print(f'  {b["t0"]:6.2f}  ' + " ".join(("*" + w["d"] + "*") if w["h"] == 1 else ("~" + w["d"] + "~") if w["h"] == 2 else w["d"] for w in b["words"]))


PL = dict(type="plansza", hideCaps=True)

# ------------------------------------------------------------------ ADS5 (53.2 s, 10 cuts) – angle: "gdzie jest haczyk?"
FIX5 = ("Gdybym zobaczył reklamę, w której jakiś gość mówi, że pokaże mi, jak zbudować *biznes_AI* w *48_godzin* za *17_zł,* "
        "to pierwsze, co bym pomyślał: dobra, ale gdzie jest ~haczyk?~ I szczerze, wcale Cię nie dziwię, bo w internecie jest "
        "pełno ludzi, którzy obiecują Ci *miliony_złotych* za ~kilka_kliknięć.~ Ale ja nie sprzedaję Ci magicznego sposobu na "
        "zarabianie, sprzedaję Ci coś znacznie prostszego. *Prosty_proces,* który pozwala Ci w końcu stworzyć coś ~własnego.~ "
        "Zobacz, najpierw wybierasz sobie pomysł na Twój produkt cyfrowy, potem AI pomaga Ci stworzyć jego zawartość, następnie "
        "przygotowujesz stronę sprzedażową z AI, podpinasz płatność i masz coś, co możesz realnie zaoferować innym ludziom. I to "
        "wszystko możesz przygotować w *48_godzin,* wykonując instrukcje krok po kroku. I czy to oznacza, że w 48 godzin będziesz "
        "milionerem? ~Nie.~ Ale zamiast kolejny miesiąc zastanawiać się, jak zacząć zarabiać w internecie, możesz w końcu mieć "
        "*produkt,* który faktycznie da się ~sprzedawać.~ I właśnie dlatego stworzyłem Cyfrowy Autopilot. Cały proces pokazuję Ci "
        "za jedyne *17_zł,* więc nie musisz mi wierzyć ~na_słowo.~ Kliknij poniżej, zobacz dokładnie, co dostajesz, i zdecyduj, "
        "czy chcesz spróbować.")
IT5 = [
    dict(PL, t0=6.333, t1=9.067, uh=dict(y=640, bar=560, words=pw([("Pierwsza", 6.34, 0), ("myśl:", 7.12, 0)])),
         bh=[dict(y=860, fs=120, words=pw([("Dobra,", 7.80, 0), ("ale", 8.26, 0), ("gdzie", 8.34, 0), ("jest", 8.50, 0), ("haczyk?", 8.66, 2)]))]),
    dict(PL, t0=14.333, t1=18.067, bh=[dict(y=560, fs=74, words=pw([("Nie", 14.62, 0), ("sprzedaję", 14.70, 0)]))], rows=[
        dict(y=820, t=15.22, icon="x", bad=True, html='magiczny<br>sposób'),
        dict(y=1080, t=16.72, icon="check", html='coś <span class="s">znacznie</span><br>prostszego')]),
    dict(type="tracker", t0=20.6, t1=34.033, capY=0.5, x=70, y=1250, gap=104, doneT=30.0, items=[
        dict(text="Pomysł na produkt", t=21.80), dict(text="Zawartość z AI", t=24.04),
        dict(text="Strona sprzedażowa", t=25.98), dict(text="Płatność", t=27.26)]),
    dict(PL, t0=30.133, t1=34.033, uh=dict(y=330, bar=640, words=pw([("Wszystko", 30.20, 0), ("to", 30.32, 0), ("przygotujesz", 30.96, 0), ("w", 31.28, 0)])),
         bh=[dict(y=440, fs=180, words=pw([("48", 31.50, 1), ("godzin", 31.96, 0)])),
             dict(y=900, fs=90, words=pw([("krok", 33.24, 2), ("po", 33.46, 2), ("kroku", 33.66, 2)]))]),
    dict(PL, t0=43.567, t1=48.2, bh=[dict(y=330, fs=80, words=pw([("Dlatego", 43.90, 0), ("stworzyłem", 44.22, 0)]))], cards=[
        dict(kind="brand", t=44.62, x=540, y=1060, w=860, h=760, title="Cyfrowy<br>Autopilot", sub="cały proces krok po kroku", subY=330,
             rows=["pomysł na produkt", "produkt z AI", "strona + płatność"], rowsY=420, price="17 zł")]),
    dict(type="cta", t0=49.92, t1=53.2, y=1480, text="Kliknij poniżej"),
]

# ------------------------------------------------------------------ ADS2 (71.1 s, 17 cuts) – angle: "AI slop zarabia"
FIX2 = ("~AI_slop.~ Na pewno widziałeś już te dziwne filmiki generowane przez sztuczną inteligencję, ale jest coś, czego większość "
        "z nich kompletnie nie rozumie. Niektórzy wykorzystują takie filmiki, żeby zarabiać *tysiące_złotych* miesięcznie. I nie, "
        "nie chodzi mi kompletnie o pieniądze z ~wyświetleń.~ Akurat tutaj chodzi o coś znacznie prostszego: AI *produkty_cyfrowe.* "
        "Na przykład taka postać AI codziennie pokazuje kobietom proste triki i sekrety w kuchni, a na profilu sprzedaje poradnik AI "
        "za 49 złotych. I teraz sobie policzmy: 10 sprzedaży dziennie to 490 złotych przychodu każdego dnia. A gdyby utrzymać takie "
        "tempo przez 30 dni, daje to 14 700 miesięcznie. I to wszystko z *jednego* prostego AI produktu ~cyfrowego.~ Oczywiście to "
        "tylko przykład, ale pokazuje, jak działa ten *model_biznesowy.* I najlepsze jest to, że dzisiaj nawet nie musisz "
        "samodzielnie tworzyć takiego produktu od zera, bo AI może pomóc Ci zrobić praktycznie ~wszystko.~ I właśnie dlatego "
        "stworzyłem Cyfrowy Autopilot. Gotowy system, który pomaga Ci znaleźć pomysł na produkt, którego ludzie już szukają. "
        "Następnie AI pomaga Ci stworzyć gotowy produkt cyfrowy i zbudować stronę, na której możesz go sprzedawać. A na koniec "
        "pokazuję Ci, jak stworzyć proste filmiki i reklamy z AI, które przyciągają potencjalnych klientów. Więc nie, spokojnie, "
        "nie musisz być ekspertem, nie musisz umieć programować ani nawet pokazywać swojej twarzy. Więc po prostu kliknij przycisk "
        "poniżej i pokażę Ci, jak możesz stworzyć swój pierwszy *produkt_cyfrowy* gotowy do sprzedaży. I zamiast dalej oglądać, "
        "jak inni wykorzystują AI do zarabiania, zacznij wykorzystywać je ~dla_siebie.~")
IT2 = [
    dict(PL, t0=0.8, t1=4.167, bh=[dict(y=300, fs=150, words=pw([("AI", 0.82, 0), ("slop", 0.9, 2)]))], reels=[
        dict(img=STILL("aiimage_0"), x=250, y=1080, w=330, h=560, rot=-6, t=1.0),
        dict(img=STILL("aiimage_1"), x=540, y=1020, w=330, h=560, rot=0, t=1.25),
        dict(img=STILL("aiimage_2"), x=830, y=1080, w=330, h=560, rot=6, t=1.5)]),
    dict(PL, t0=12.367, t1=15.567, uh=dict(y=600, bar=700, words=pw([("Chodzi", 13.04, 0), ("o", 13.26, 0), ("coś", 13.40, 0), ("prostszego:", 13.56, 0)])),
         bh=[dict(y=820, fs=130, words=pw([("AI", 14.50, 0), ("+", 14.70, 0), ("produkty", 14.88, 1), ("cyfrowe", 15.14, 2)]))]),
    dict(PL, t0=15.567, t1=22.5, bh=[dict(y=230, fs=90, words=pw([("Postać", 16.26, 0), ("AI", 16.58, 1)])),
                                   dict(y=340, fs=90, words=pw([("triki", 18.60, 0), ("w", 19.34, 2), ("kuchni", 19.44, 2)]))],
         reels=[dict(img=STILL("cooking_0"), x=330, y=1050, w=420, h=720, rot=-4, t=15.8)],
         cards=[dict(kind="product", t=20.44, x=770, y=1180, w=420, h=560, rot=5, img=STILL("cooking_1"), imgH=270,
                     title="Poradnik AI:<br>sekrety kuchni", sub="e-book PDF", price="49 zł")]),
    dict(PL, t0=22.5, t1=26.533, noFlash=True, eq=[
        dict(t=23.62, y=600, fs=120, html='10 <span style="font-size:.6em;opacity:.8">sprzedaży</span>'),
        dict(t=24.0, y=760, fs=120, html='× 49 zł'),
        dict(t=24.56, y=980, fs=190, color="#8F8FFF", pre="", suf=" zł", count=dict(t=24.56, d=.8, to=490)),
        dict(t=25.88, y=1210, fs=70, html='<span style="font-family:Instrument Serif;font-style:italic;font-weight:400">każdego dnia</span>')]),
    dict(PL, t0=26.533, t1=30.733, noFlash=True, eq=[
        dict(t=26.6, y=600, fs=110, html='490 zł'),
        dict(t=28.10, y=760, fs=120, html='× 30 dni'),
        dict(t=29.04, y=980, fs=180, color="#8F8FFF", suf=" zł", count=dict(t=29.04, d=1.0, to=14700)),
        dict(t=30.12, y=1210, fs=70, html='<span style="font-family:Instrument Serif;font-style:italic;font-weight:400">miesięcznie</span>')]),
    dict(PL, t0=42.833, t1=45.033, bh=[dict(y=300, fs=80, words=pw([("Dlatego", 43.32, 0), ("stworzyłem", 43.64, 0)]))], cards=[
        dict(kind="brand", t=44.04, x=540, y=1000, w=860, h=640, title="Cyfrowy<br>Autopilot", sub="gotowy system z AI", subY=330, price="17 zł")]),
    dict(type="tracker", t0=45.033, t1=57.5, capY=0.5, x=70, y=1250, gap=104, doneT=56.9, items=[
        dict(text="Pomysł, którego szukają", t=46.72), dict(text="Produkt z AI", t=49.62),
        dict(text="Strona sprzedażowa", t=50.98), dict(text="Filmiki i reklamy z AI", t=54.74)]),
    dict(type="irows", t0=58.6, t1=61.933, capY=0.5, rows=[
        dict(y=1200, t=58.66, icon="x", bad=True, html='bez bycia ekspertem'),
        dict(y=1340, t=59.58, icon="x", bad=True, html='bez programowania'),
        dict(y=1480, t=60.86, icon="x", bad=True, html='bez pokazywania twarzy')]),
    dict(type="cta", t0=62.48, t1=71.2, y=1500, text="Kliknij przycisk poniżej"),
]

make("ads5", "ads5.mp4", "tr_ads5.json", FIX5, IT5, capY=0.62)
make("ads2", "ads2.mp4", "tr_ads2.json", FIX2, IT2, extra_cuts=(4.167, 6.567), capY=0.62)
