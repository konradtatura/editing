#!/usr/bin/env python3
"""Build render specs (captions + plansze + overlays + zooms) for ad8 / ad9.
usage: build_spec.py WORKDIR   (WORKDIR has ad8.mp4, ad9.mp4, tr8.json, tr9.json) -> writes spec_ad8.json, spec_ad9.json
"""
import difflib, json, os, re, subprocess, sys

WD = sys.argv[1]
WEAK = {"i", "w", "z", "na", "do", "od", "po", "a", "o", "że", "bo", "się", "to", "jak", "czy", "nie", "co", "za", "ci", "ten", "tego"}


def norm(t):
    return re.sub(r"[^\w]", "", t.lower())


def align(words, fixed):
    """fixed tokens (hero joined by _ and wrapped in *) get the time of the matching ASR word."""
    toks = []
    for raw in fixed.split():
        h = raw.startswith("*")
        clean = raw.strip("*")
        parts = clean.split("_")
        for k, p in enumerate(parts):
            toks.append({"d": p, "h": h, "join": k > 0})
    a = [norm(w["w"]) for w in words]
    b = [norm(t["d"]) for t in toks]
    times = [None] * len(toks)
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        if op == "equal":
            for k in range(i2 - i1): times[j1 + k] = words[i1 + k]["s"]
        elif op == "replace":
            s0, e0 = words[i1]["s"], words[i2 - 1]["e"]
            for j in range(j1, j2): times[j] = s0 + (e0 - s0) * (j - j1) / max(1, j2 - j1)
    for j in range(len(toks)):
        if times[j] is None:
            times[j] = next((times[k] for k in range(j - 1, -1, -1) if times[k] is not None), 0.0)
    for j, t in enumerate(toks): t["t"] = round(times[j], 3)
    # merge hero sub-tokens into one display unit
    units = []
    for t in toks:
        if t["join"] and units: units[-1]["d"] += " " + t["d"]
        else: units.append(dict(t))
    return units


def chunk(units, maxw=3, maxc=20):
    blocks, cur = [], []
    def flush():
        if cur: blocks.append(cur[:]); cur.clear()
    for i, u in enumerate(units):
        if u["h"]:
            # hero closes the block: keep at most 2 small words before it
            while len([x for x in cur if not x["h"]]) > 2:
                blocks.append([cur.pop(0)])
            cur.append(u); flush(); continue
        clen = sum(len(x["d"]) + 1 for x in cur) + len(u["d"])
        if cur and (len(cur) >= maxw or clen > maxc):
            # do not leave a weak word dangling at the end of a block
            last = cur[-1]["d"].lower().strip(",.?")
            if (last in WEAK or last.isdigit()) and len(cur) > 1:
                carry = cur.pop(); flush(); cur.append(carry)
            else: flush()
        cur.append(u)
        if u["d"].endswith((".", "?", "!")): flush()
    flush()
    out = []
    for b in blocks:
        out.append({"t0": b[0]["t"], "words": [{"d": w["d"], "t": w["t"], "h": w["h"]} for w in b]})
    return out


def dur(p):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p], capture_output=True, text=True).stdout)


def words_of(n):
    return [w for s in json.load(open(os.path.join(WD, f"tr{n}.json"))) for w in s["words"]]


def sentence_starts(n):
    return [round(s["start"], 2) for s in json.load(open(os.path.join(WD, f"tr{n}.json")))]


def cuts_of(n):
    out = subprocess.run([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), "engine", "cuts.py"),
                          os.path.join(WD, f"ad{n}.mp4")], capture_output=True, text=True).stdout
    return json.loads(out)


def snap_scenes(scenes, cuts):
    """plansza starts on the first frame of a shot and ends on a cut when one is near; back-to-back scenes hard-cut."""
    for s in scenes:
        c = [c for c in cuts if s["t0"] - 0.35 <= c <= s["t0"] + 0.6]
        if c: s["t0"] = c[0]
        c = [c for c in cuts if abs(c - s["t1"]) <= 0.6]
        if c: s["t1"] = min(c, key=lambda c: abs(c - s["t1"]))
    scenes.sort(key=lambda s: s["t0"])
    for a, b in zip(scenes, scenes[1:]):
        if b["t0"] - a["t1"] <= 0.4:
            b["t0"] = a["t1"]; b["noReveal"] = True
    return scenes


def shot_zooms(cuts, dur, scenes, cta_t0):
    """one zoom level per shot, switching only on real cuts; CTA shots stay at 100 %."""
    z, big = [], False
    for t in [0.0] + cuts:
        if any(s["t0"] - .05 <= t < s["t1"] - .05 for s in scenes): continue
        z.append([t, 1.0 if t >= cta_t0 - 0.5 else (1.10 if big else 1.0)]); big = not big
    # a shot that starts under a plansza gets its zoom from the plansza's end
    for s in scenes:
        inside = [c for c in cuts if s["t0"] - .05 <= c < s["t1"] - .05]
        if inside and not any(abs(zt - s["t1"]) < .05 for zt, _ in z):
            z.append([s["t1"], 1.0]); 
    return sorted(z)


def zooms_from(starts, scenes):
    z, big = [], False
    for t in starts:
        if any(s["t0"] - .05 <= t < s["t1"] for s in scenes): continue
        z.append([t, 1.12 if big else 1.0]); big = not big
    return z


WM_MONEY = [dict(icon="circle-dollar-sign", x=140, y=300, s=380, r=-12), dict(icon="circle-dollar-sign", x=930, y=1500, s=460, r=10),
            dict(icon="sparkles", x=900, y=260, s=300, r=8), dict(icon="file-text", x=180, y=1560, s=360, r=-6)]

# ------------------------------------------------------------------ AD 8
FIX8 = ("Za cenę takiej jednej kawy na mieście pokażę Ci, jak w *48_godzin* stworzyć z pomocą sztucznej inteligencji coś, "
        "co można *sprzedawać* przez internet. I nie, nie mówię tutaj o kolejnym pomyśle na biznes. Mówię o prawdziwym "
        "produkcie cyfrowym, własnej stronie sprzedażowej i wszystkim, czego potrzebujesz, żeby zacząć. I zanim pomyślisz, "
        "że to kolejny kurs, w którym przez *10_godzin* oglądasz, jak ktoś opowiada Ci o zarabianiu w internecie, to zobacz, "
        "co dokładnie zrobisz. Po pierwsze, wybierzesz pomysł na produkt cyfrowy, którego ludzie faktycznie potrzebują. "
        "Nie musisz go sam wymyślać. Sztuczna inteligencja pomoże Ci znaleźć odpowiedni *kierunek.* Po drugie, stworzysz ten "
        "produkt. Może to być poradnik, planner, zestaw szablonów, PDF albo coś zupełnie innego. Po trzecie, z pomocą AI "
        "przygotujesz własną stronę sprzedażową, na której ludzie będą mogli kupić, a po czwarte pokażę Ci, jak tworzyć treści "
        "i reklamy, które mogą przyciągać do niego klientów. Pomysł, produkt, strona, marketing i to wszystko z pomocą "
        "sztucznej inteligencji. Generalnie jest to cały proces krok po kroku i moim celem nie jest to, żebyś po 48 godzinach "
        "wiedział więcej o AI. Moim celem jest to, żebyś miał coś, czego *dzisiaj_nie_masz.* Własny produkt cyfrowy, który "
        "realnie ma szansę się *sprzedawać.* Ja sam sprzedaję produkty cyfrowe od ponad 3 lat, a w najlepszym dniu sprzedałem "
        "941 e-booków. I właśnie na tej podstawie stworzyłem Cyfrowy Autopilot. I dzisiaj dostęp do tego możesz dostać tylko "
        "za *17_zł.* I w dodatku daję Ci na to gwarancję. Jeżeli w 48 godzin nie zbudujesz wszystkiego, zwracam Ci 100% kwoty. "
        "Kliknij przycisk poniżej i zacznij działać już teraz, dosłownie za mniej niż kubek *kawy* na mieście. I zamiast "
        "kupować kolejną wiedzę o zarabianiu, zacznij w końcu tworzyć coś, co może się *sprzedać.*")

SC8 = [
    # 1: "nie kolejny pomysł na biznes" -> 3 real deliverables
    dict(type="discTile", t0=6.86, t1=13.86, cap=dict(mode="light", y=0.6, hideIn=[[9.36, 13.9]]), a=dict(
        tiles=[dict(icon="lightbulb", t=7.05, y=700, size=250, spark=True, t1=9.3, s1=.5)],
        strike=dict(t=8.9, y=690, t1=9.3),
        pills=[dict(text="Prawdziwy produkt cyfrowy", icon="book-open", t=9.7, y=640, cls="white"),
               dict(text="Własna strona sprzedażowa", icon="layout-template", t=11.16, y=790, cls="white"),
               dict(text="Wszystko, by zacząć", icon="rocket", t=12.22, y=940, cls="white")])),
    # 2: krok 1 – pomysł, AI pomaga znaleźć kierunek
    dict(type="orbit", t0=20.28, t1=27.08, cap=dict(mode="light", y=0.79), a=dict(
        wm=WM_MONEY, R=340, cy=760, center=dict(icon="lightbulb", t=20.6, size=200, spark=True),
        sats=[dict(icon="users", ang=-150, t=22.36, label="Ludzie tego potrzebują"),
              dict(icon="sparkles", ang=-30, t=24.76, label="AI pomaga"),
              dict(icon="compass", ang=90, t=26.32, label="Kierunek")])),
    # 3: krok 3+4 – strona sprzedażowa, zakup, treści i reklamy
    dict(type="phone", t0=32.2, t1=39.98, cap=dict(mode="dark", y=0.885), a=dict(
        cy=780, buildT=33.2, buyT=35.72, notifT1=36.9,
        ads=[dict(icon="clapperboard", x=175, y=560, t=37.5, rot=-8), dict(icon="megaphone", x=905, y=520, t=38.06, rot=7),
             dict(icon="video", x=905, y=1080, t=38.5, rot=-5)],
        people=[dict(x=170, y=1060, t=39.3), dict(x=250, y=1180, t=39.42)])),
    # 5: dowód – najlepszy dzień
    dict(type="discTile", t0=53.66, t1=58.42, cap=dict(mode="light", y=0.6, hideIn=[[56.3, 58.5]]), a=dict(
        slot=dict(x=540, y=1480, w=460, h=330, rot=-5, t=54.3),
        tiles=[dict(icon="trending-up", t=53.9, y=640, size=220, t1=56.2, s1=.6)],
        pills=[dict(text="Od ponad 3 lat", icon="clock", t=55.48, y=880, cls="white", t1=56.2)],
        counter=dict(t=56.84, d=1.0, to=941, y=640, fs=230, sub="e-booków w jeden dzień", subT=57.5))),
    # 6: gwarancja
    dict(type="hero", t0=63.72, t1=68.74, cap=dict(mode="light", y=0.84), a=dict(
        wm=WM_MONEY, icon="shield-check", iy=560, isize=270, it=63.95,
        items=[dict(kind="text", text="Gwarancja", fs=120, y=820, t=64.76),
               dict(kind="pill", text="48 godzin", icon="clock", y=990, t=65.78, cls="white"),
               dict(kind="text", text="100%", fs=150, y=1170, t=67.88, count=dict(t=67.88, d=.5, to=100, suf="%"))])),
]
OV8 = [
    dict(type="tile", t0=2.76, t1=6.6, a=dict(icon="clock", x=540, y=1410, size=150, badge="48 h", badgeT=2.9)),
    dict(type="pills", t0=28.8, t1=32.1, a=dict(items=[
        dict(text="Poradnik", icon="book-open", x=310, y=1480, t=28.88), dict(text="Planner", icon="calendar-check", x=770, y=1480, t=29.42),
        dict(text="Szablony", icon="files", x=310, y=1580, t=30.04), dict(text="PDF", icon="file-text", x=770, y=1580, t=30.66)])),
    dict(type="pills", t0=40.05, t1=43.5, cap=dict(mode="face", y=0.645, hideIn=[[40.0, 41.6]]), a=dict(items=[
        dict(text="Pomysł", icon="lightbulb", x=310, y=1480, t=40.12, cls="solid"), dict(text="Produkt", icon="package", x=770, y=1480, t=40.52, cls="solid"),
        dict(text="Strona", icon="layout-template", x=310, y=1580, t=40.96, cls="solid"), dict(text="Marketing", icon="megaphone", x=770, y=1580, t=41.34, cls="solid"),
        dict(text="+ AI", icon="sparkles", x=540, y=1680, t=42.58, cls="white")])),
    dict(type="brand", t0=59.6, t1=60.8, a=dict(y=1420)),
    dict(type="price", t0=62.8, t1=63.72, a=dict(text="17 zł", x=540, y=1610, w=480, h=230, fs=150)),
    dict(type="cta", t0=68.9, t1=99, a=dict(text="Kliknij poniżej", y=1420)),
]

# ------------------------------------------------------------------ AD 9
FIX9 = ("ChatGPT nie zapłaci Ci *ani_złotówki.* Możesz mieć najlepsze prompty na świecie, znać wszystkie narzędzia AI "
        "i codziennie spędzać po 5–10 godzin przed laptopem. Ale dopóki nie masz czegoś, za co ktoś jest gotowy zapłacić, "
        "to nadal *nie_masz_biznesu.* I właśnie tego nie rozumie większość ludzi próbujących zarabiać z AI. Bo finalnie to "
        "nie sztuczna inteligencja płaci pieniądze, płacą Ci *ludzie.* Za co? Za rozwiązywanie ich *problemu.* Pomyśl, ktoś "
        "potrzebuje planera budżetu, żeby uporządkować swoje wydatki. Ktoś inny szuka prostych przepisów, bo nie ma czasu na "
        "gotowanie. A jeszcze ktoś potrzebuje gotowego szablonu CV, żeby szybciej przygotować dokumenty do rekrutacji. "
        "To są rzeczy, za które ludzie mogą *zapłacić.* I teraz najlepsze, bo dzisiaj AI może pomóc takie rzeczy stworzyć. "
        "I to wszystko bez pisania wszystkiego od zera czy pokazywania swojej twarzy. Dokładnie dlatego zbudowałem Cyfrowy "
        "Autopilot. System, który pokazuje Ci, jak znaleźć pomysł na produkt cyfrowy, stworzyć go z pomocą sztucznej "
        "inteligencji i przygotować całą stronę sprzedażową. I oczywiście następnie pokazuje Ci, jak zacząć go sprzedawać "
        "przy pomocy sztucznej inteligencji. I to wszystko po to, żebyś w ciągu *48_godzin* mógł przejść od pustego czatu GPT "
        "do produktu gotowego na sprzedaż. I co jest najciekawsze, aktualnie możesz otrzymać dostęp za jedyne *17_zł.* Czyli "
        "dosłownie mniej niż jedna kawa na mieście. Kliknij przycisk poniżej pod tym filmem i przestań pisać do ChatGPT, jak "
        "zarabiać pieniądze, a zacznij używać go do stworzenia czegoś, za co ludzie mogą *zapłacić.*")

SC9 = [
    dict(type="checklist", t0=2.12, t1=7.62, cap=dict(mode="hide"), a=dict(cy=900, rowH=200, items=[
        dict(icon="wand-sparkles", text="Najlepsze prompty na świecie", t=2.6),
        dict(icon="wrench", text="Wszystkie narzędzia AI", t=4.28),
        dict(icon="laptop", text="5–10 godzin dziennie przed laptopem", t=5.44, fs=52)])),
    dict(type="discTile", t0=14.44, t1=19.22, cap=dict(mode="light", y=0.62), a=dict(
        tiles=[dict(icon="bot", t=14.65, y=640, size=230, t1=16.85, s1=.5),
               dict(icon="users", t=16.95, y=640, size=250, spark=True)],
        pills=[dict(text="0 zł", icon="x", t=16.12, y=880, cls="white", t1=16.85),
               dict(text="Płacą ludzie", icon="hand-coins", t=17.26, y=880, cls="white")])),
    dict(type="orbit", t0=19.22, t1=29.72, cap=dict(mode="light", y=0.8), a=dict(
        wm=WM_MONEY, R=340, cy=760, center=dict(icon="user", t=19.5, size=200),
        sats=[dict(icon="wallet", ang=-140, t=20.22, label="Planer budżetu"),
              dict(icon="chef-hat", ang=-40, t=23.18, label="Proste przepisy"),
              dict(icon="file-user", ang=90, t=26.36, label="Szablon CV")])),
    dict(type="checklist", t0=40.95, t1=49.46, cap=dict(mode="hide"), a=dict(cy=900, rowH=200, connector=True, items=[
        dict(icon="lightbulb", text="Pomysł na produkt cyfrowy", t=41.26),
        dict(icon="sparkles", text="Stworzenie go z AI", t=43.32),
        dict(icon="layout-template", text="Cała strona sprzedażowa", t=44.96),
        dict(icon="trending-up", text="Sprzedaż z pomocą AI", t=47.96)])),
]
OV9 = [
    dict(type="pills", t0=34.9, t1=37.95, a=dict(items=[
        dict(text="Bez pisania od zera", icon="pen-line", x=540, y=1420, t=35.18, cls="white"),
        dict(text="Bez pokazywania twarzy", icon="user", x=540, y=1530, t=36.76, cls="white")])),
    dict(type="brand", t0=39.0, t1=40.95, a=dict(y=1420)),
    dict(type="flow", t0=52.3, t1=54.85, a=dict(items=[
        dict(icon="message-square-dashed", x=290, y=1450, t=52.46, label="Pusty czat"),
        dict(x=540, y=1450, t=53.2), dict(icon="package", x=790, y=1450, t=53.52, label="Gotowy produkt", dark=True)])),
    dict(type="cta", t0=60.55, t1=99, a=dict(text="Kliknij poniżej", y=1420)),
]


def make(n, fixed, scenes, overlays, mirror, capY):
    src = os.path.join(WD, f"ad{n}.mp4")
    units = align(words_of(n), fixed)
    cuts = cuts_of(n); scenes = snap_scenes(scenes, cuts); d = round(dur(src), 3)
    cta = min([o["t0"] for o in overlays if o["type"] == "cta"] or [d])
    spec = dict(src=src, dur=d, fps=30, mirror=mirror, capY=capY, zoomCenter=[0.5, 0.34], cuts=cuts,
                caps=chunk(units), scenes=scenes, overlays=overlays,
                zooms=shot_zooms(cuts, d, scenes, cta))
    p = os.path.join(WD, f"spec_ad{n}.json")
    json.dump(spec, open(p, "w"), ensure_ascii=False, indent=1)
    print(p, len(spec["caps"]), "caption blocks")
    for b in spec["caps"]:
        print(f'  {b["t0"]:6.2f}  ' + " ".join(("*" + w["d"] + "*") if w["h"] else w["d"] for w in b["words"]))


make(8, FIX8, SC8, OV8, False, 0.645)
make(9, FIX9, SC9, OV9, True, 0.56)
