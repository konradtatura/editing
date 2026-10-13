#!/usr/bin/env python3
"""Style-2 render specs for add7fixed and ads10.
usage: build_spec2.py WORKDIR STOCKDIR  (WORKDIR: add7fixed.mp4, ads10.mp4, tr_a7f.json, tr_ads10.json) -> spec2_<name>.json"""
import difflib, json, os, re, subprocess, sys
WD, ST = sys.argv[1], sys.argv[2]
HERE = os.path.dirname(os.path.abspath(__file__))
WEAK = {"i", "w", "z", "na", "do", "od", "po", "a", "o", "że", "bo", "się", "to", "jak", "czy", "nie", "co", "za", "ci", "ten", "tego"}
GRADE = ("eq=contrast=0.95:saturation=0.86,colorbalance=rs=0.05:gs=0.01:bs=-0.04:rm=0.03:bm=-0.02:rh=0.02:bh=-0.03,"
         "curves=all='0/0.035 0.25/0.235 0.75/0.775 1/0.975',vignette=angle=PI/5")
norm = lambda t: re.sub(r"[^\w]", "", t.lower())


def align(words, fixed):
    toks = []
    for raw in fixed.split():
        h = raw.startswith("*"); parts = raw.strip("*").split("_")
        for k, p in enumerate(parts): toks.append({"d": p, "h": h, "join": k > 0})
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


def chunk(units, maxw=4, maxc=22):
    blocks, cur = [], []
    def flush():
        if cur: blocks.append(cur[:]); cur.clear()
    for u in units:
        clen = sum(len(x["d"]) + 1 for x in cur) + len(u["d"])
        if cur and not u["join"] and (len(cur) >= maxw or clen > maxc):
            carry = []
            while len(cur) > 1 and (cur[-1]["d"].lower().strip(",.?") in WEAK or cur[-1]["d"].isdigit()):
                carry.insert(0, cur.pop())
            flush(); cur.extend(carry)
        cur.append(u)
        if u["d"].endswith((".", "?", "!")): flush()
    flush()
    return [{"t0": b[0]["t"], "words": [{"d": w["d"], "t": w["t"], "h": w["h"]} for w in b]} for b in blocks]


def dur(p):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p], capture_output=True, text=True).stdout)


def cuts(p):
    return json.loads(subprocess.run([sys.executable, os.path.join(HERE, "..", "reklamy_CA", "engine", "cuts.py"), p], capture_output=True, text=True).stdout)


def W(text, t0, step=0.0):
    """plansza words: 'a *b* c' -> list with times (given explicitly as list) """
    return text


def pw(spec_words):
    """[(word, t, accent)] -> plansza words"""
    return [{"d": w, "t": t, "h": h} for w, t, h in spec_words]


def make(name, src, trname, fixed, items, brolls, capY, hide, end):
    srcp = os.path.join(WD, src); sd = round(dur(srcp), 3); cs = cuts(srcp)
    words = [w for s in json.load(open(os.path.join(WD, trname))) for w in s["words"]]
    caps = chunk(align(words, fixed))
    z, big = [], False
    for t in [0.0] + cs:
        z.append([t, 1.12 if big else 1.0]); big = not big
    for b in brolls: b["file"] = os.path.join(ST, b["file"] + ".mp4")
    total = round(sd + 2.5, 3)
    items = items + [dict(type="end", t0=sd, t1=total, hideCaps=True, **end)]
    spec = dict(src=srcp, srcDur=sd, dur=total, fps=30, capY=capY, capHide=hide, caps=caps, items=items, brolls=brolls,
                cuts=cs, zooms=z, zoomCenter=[0.5, 0.3], grade=GRADE)
    p = os.path.join(WD, f"spec2_{name}.json"); json.dump(spec, open(p, "w"), ensure_ascii=False, indent=1)
    print(p, len(caps), "caption blocks,", len(cs), "cuts")
    for b in caps: print(f'  {b["t0"]:6.2f}  ' + " ".join(("*" + w["d"] + "*") if w["h"] else w["d"] for w in b["words"]))


END = dict(brand="Cyfrowy Autopilot", tag="Od pomysłu do produktu cyfrowego z AI", button="Zobacz, jak zacząć")

# ------------------------------------------------------------------ ADS7 (add7fixed, 62.2 s)
FIX7 = ("Zastanawiałeś się kiedyś, skąd ci wszyscy ludzie w internecie właściwie biorą pieniądze? Bo przecież nie dostają ich "
        "tylko za siedzenie przed komputerem. Przez kolejne 40 sekund pokażę Ci jeden z *najprostszych_modeli,* który możesz "
        "zacząć już dzisiaj. Wyobraź sobie, że ktoś tworzy poradnik z 30 szybkimi obiadami dla zapracowanych osób. Wystawia go "
        "na sprzedaż za *49_zł,* a następnie publikuje krótkie filmiki AI z przepisami, które przyciągają zainteresowanych ludzi. "
        "Czyli ktoś ogląda filmik, wchodzi na stronę i jeśli poradnik rozwiązuje jego problem, to może go kupić. I *39_zł* trafia "
        "na konto. A produkt nadal może zostać sprzedany kolejnej i kolejnej osobie. Więc nie musisz zamawiać nowego towaru, nie "
        "musisz pakować paczek i nie musisz tworzyć produktu od nowa dla każdego możliwego klienta. I na tym polega właśnie biznes "
        "na produktach cyfrowych. I teraz wyobraź sobie, że AI pomaga Ci stworzyć cały taki produkt, napisać stronę sprzedażową i "
        "przygotować filmiki do jego promocji. Brzmi to znacznie prościej niż otwieranie tradycyjnego sklepu, e-commerce czy "
        "dropshippingu, prawda? I właśnie dlatego stworzyłem *Cyfrowy_Autopilot.* System, który pokazuje Ci, jak przygotować taki "
        "biznes z pomocą sztucznej inteligencji. Od pomysłu przez gotowy produkt, aż po stronę sprzedażową i plan zdobywania "
        "klientów. Więc zamiast dalej zastanawiać się, jak ludzie zarabiają w internecie, po prostu kliknij poniżej i zobacz, jak "
        "możesz zacząć budować *własny_produkt_cyfrowy.*")
IT7 = [
    dict(type="hero", t0=2.6, t1=3.767, y=0.55, small="właściwie biorą", big="pieniądze?", size=170, bigT=3.30, hideCaps=True),
    dict(type="fan", t0=14.7, t1=16.47, x=300, y=1660, dx=230, w=270, h=370, hideCaps=False, cards=[
        dict(title="30 szybkich obiadów", sub="dla zapracowanych", icon="chef-hat", price="49 zł", t=14.68),
        dict(title="Przepisy na 15 minut", sub="e-book PDF", icon="book-open", bg="linear-gradient(160deg,#E8F7FB,#BFE9F2)", t=14.80),
        dict(title="Lista zakupów", sub="na cały tydzień", icon="shopping-bag", bg="linear-gradient(160deg,#F7FCFD,#D6EFF5)", t=14.92)]),
    dict(type="tiles", t0=21.0, t1=26.8, y=1430, size=150, gap=110, items=[
        dict(icon="play", label="ogląda filmik", t=21.02), dict(icon="globe", label="wchodzi na stronę", t=21.78),
        dict(icon="shopping-cart", label="kupuje", t=24.70)]),
    dict(type="notif", t0=25.1, t1=26.8, y=330, title="Nowa płatność", sub="Poradnik: 30 szybkich obiadów", amount="+39 zł"),
    dict(type="plansza", t0=35.267, t1=37.75, hideCaps=True, y0=820, fs=74, rows=[dict(words=pw([
        ("I", 35.36, 0), ("na", 35.48, 0), ("tym", 35.54, 0), ("polega", 35.64, 0), ("właśnie", 35.94, 0), ("biznes", 36.24, 0),
        ("na", 36.48, 1), ("produktach", 36.64, 1), ("cyfrowych.", 37.0, 1)]))]),
    dict(type="plansza", t0=37.75, t1=42.9, hideCaps=True, y0=820, gap=230, fs=64, rows=[
        dict(y=520, fs=54, words=pw([("Wyobraź", 37.82, 0), ("sobie,", 38.10, 0), ("że", 38.38, 0), ("AI", 38.46, 1), ("pomaga", 38.70, 0),
                                     ("Ci", 38.94, 0), ("stworzyć:", 39.06, 0)])),
        dict(num=1, t=39.86, y=820, words=pw([("Produkt", 39.86, 0), ("cyfrowy", 40.0, 1)])),
        dict(num=2, t=40.64, y=1050, words=pw([("Strona", 40.64, 0), ("sprzedażowa", 40.8, 1)])),
        dict(num=3, t=41.68, y=1280, words=pw([("Filmiki", 41.68, 0), ("promocyjne", 41.9, 1)]))]),
    dict(type="fan", t0=48.1, t1=52.43, x=300, y=1660, dx=230, w=270, h=370, cards=[
        dict(title="Moduł 1: Pomysł", sub="AI znajduje niszę", icon="lightbulb", bg="linear-gradient(160deg,#0F2A31,#0B1A1E)", ink="#fff", ink2="#8fb4bc", t=48.14),
        dict(title="Moduł 2: Produkt", sub="e-book z AI", icon="book-open", bg="linear-gradient(160deg,#0F2A31,#0B1A1E)", ink="#fff", ink2="#8fb4bc", t=48.30),
        dict(title="Moduł 3: Sprzedaż", sub="strona + reklamy", icon="trending-up", bg="linear-gradient(160deg,#0F2A31,#0B1A1E)", ink="#fff", ink2="#8fb4bc", t=48.46)]),
    dict(type="tiles", t0=52.433, t1=55.933, y=1430, size=140, gap=60, items=[
        dict(num="1", label="pomysł", t=52.62), dict(num="2", label="produkt", t=53.58), dict(num="3", label="strona", t=54.24), dict(num="4", label="klienci", t=54.96)]),
    dict(type="cta", t0=59.06, t1=62.3, y=1400, text="Kliknij poniżej"),
]
BR7 = [dict(t0=4.36, t1=6.467, file="typing_0", ss=2.0), dict(t0=12.6, t1=14.66, file="cooking_2", ss=1.0),
       dict(t0=17.0, t1=18.95, file="scroll_2", ss=3.0), dict(t0=30.24, t1=31.42, file="warehouse_0", ss=1.5),
       dict(t0=31.42, t1=32.46, file="packing_0", ss=2.0), dict(t0=44.1, t1=46.3, file="store_1", ss=4.0),
       dict(t0=56.48, t1=58.3, file="thinking_0", ss=3.0)]

# ------------------------------------------------------------------ ADS10 (95.6 s)
FIX10 = ("Każdy wie, że największą okazją na zarabianie przez internet w 2026 roku jest sztuczna inteligencja i w 2027 będzie to "
         "jeszcze bardziej aktualne, ale większość ludzi kompletnie nie rozumie, jak ją wykorzystać. I nie chodzi mi tutaj o "
         "zadawanie pytań ChatGPT czy generowanie śmiesznych obrazków. Mówię o wykorzystaniu AI, żeby pomogło Ci wykonać pracę "
         "potrzebną do stworzenia *własnego_biznesu_online.* I tutaj moim zdaniem pojawia się jedna z największych okazji: "
         "połączenie AI z produktami cyfrowymi. Wyobraź sobie, że zaczynasz od kompletnego zera. Nie masz pomysłu na biznes, nie "
         "jesteś ekspertem ani nie jesteś znany, więc wykorzystujesz AI, żeby znaleźć pomysł na produkt, na który istnieje "
         "zapotrzebowanie. Następnie AI pomaga Ci przeanalizować rynek, sprawdzić, kim są Twoi potencjalni klienci i jakie problemy "
         "próbują rozwiązać. I na tej podstawie pomaga Ci stworzyć produkt cyfrowy, który odpowiada na konkretną potrzebę. Potem "
         "pomaga Ci zbudować stronę, na której możesz go sprzedawać, a na koniec przygotować filmiki, posty i reklamy, które mogą "
         "przyciągać do niego potencjalnych klientów. I nagle teraz, zamiast kolejnych 100 magicznych promptów, masz coś, co "
         "faktycznie możesz *wystawić_na_sprzedaż.* I teraz najlepsze, bo produkty cyfrowe istnieją od kilkunastu lat, sam "
         "sprzedaję od ponad trzech lat, a w najlepszym dniu sprzedałem 941 e-booków. Ale AI kompletnie zmieniło to, jak łatwo "
         "można dzisiaj zacząć. Kiedyś musiałeś nauczyć się wielu różnych umiejętności albo płacić innym, żeby wykonali tę pracę za "
         "Ciebie, a dzisiaj sztuczna inteligencja może Ci w tym wszystkim pomóc. I właśnie dlatego stworzyłem *Cyfrowy_Autopilot,* "
         "gotowy system, w którym pokazuję Ci krok po kroku, jak przejść od kompletnego zera do własnego produktu cyfrowego i "
         "strony gotowej do sprzedaży. I to wszystko bez szczególnego doświadczenia i bez pokazywania twarzy. Aktualnie możesz "
         "otrzymać dostęp do całego systemu za jedyne 17 złotych. Więc teraz masz dwie opcje. Możesz dalej pytać AI, jak zarabiać "
         "pieniądze przez internet, albo możesz w końcu wykorzystać je do stworzenia czegoś, za co inni ludzie mogą zapłacić. "
         "Więc kliknij przycisk poniżej i zacznij budować swój pierwszy produkt cyfrowy z AI jeszcze dzisiaj.")


def step(n, t0, t1, wl):
    return dict(type="plansza", t0=t0, t1=t1, hideCaps=True, y0=820, fs=70, numSize=230, textX=360,
                rows=[dict(num=n, t=t0 + .05, words=pw(wl))])


IT10 = [
    dict(type="hero", t0=4.0, t1=5.133, y=0.52, small="jest", big="sztuczna<br>inteligencja", size=140, bigT=4.20, hideCaps=True),
    dict(type="plansza", t0=20.40, t1=23.533, hideCaps=True, y0=760, fs=96, rows=[
        dict(y=600, fs=56, words=pw([("Jedna", 20.48, 0), ("z", 20.72, 0), ("największych", 20.84, 0), ("okazji:", 21.20, 1)])),
        dict(y=760, words=pw([("AI", 22.10, 0), ("+", 22.44, 0), ("produkty", 22.62, 1), ("cyfrowe", 22.80, 1)]))]),
    step(1, 28.16, 32.167, [("Pomysł,", 29.88, 0), ("na", 30.68, 0), ("który", 30.80, 0), ("jest", 31.0, 0), ("zapotrzebowanie", 31.40, 1)]),
    step(2, 32.167, 34.6, [("Analiza", 33.38, 0), ("rynku", 33.94, 1), ("i", 34.1, 1), ("klientów", 34.2, 1)]),
    step(3, 37.633, 41.433, [("Produkt", 39.12, 0), ("cyfrowy", 39.40, 1)]),
    step(4, 41.433, 43.9, [("Strona", 42.48, 0), ("sprzedażowa", 43.40, 1)]),
    dict(type="notif", t0=50.6, t1=52.733, y=330, title="Nowa sprzedaż", sub="Twój produkt cyfrowy", amount="+17 zł", icon="banknote"),
    dict(type="hero", t0=57.4, t1=59.067, y=0.50, small="w najlepszym dniu", big="941", size=280, bigT=57.82, sub="e-booków", subT=58.3, hideCaps=True),
    dict(type="fan", t0=70.1, t1=73.4, x=300, y=1660, dx=230, w=270, h=370, cards=[
        dict(title="Moduł 1: Pomysł", sub="AI znajduje niszę", icon="lightbulb", bg="linear-gradient(160deg,#0F2A31,#0B1A1E)", ink="#fff", ink2="#8fb4bc", t=70.12),
        dict(title="Moduł 2: Produkt", sub="e-book z AI", icon="book-open", bg="linear-gradient(160deg,#0F2A31,#0B1A1E)", ink="#fff", ink2="#8fb4bc", t=70.30),
        dict(title="Moduł 3: Sprzedaż", sub="strona + reklamy", icon="trending-up", bg="linear-gradient(160deg,#0F2A31,#0B1A1E)", ink="#fff", ink2="#8fb4bc", t=70.48)]),
    dict(type="tiles", t0=77.9, t1=80.433, y=1430, size=150, gap=330, items=[
        dict(icon="check", label="bez doświadczenia", t=78.0), dict(icon="check", label="bez pokazywania twarzy", t=79.42)]),
    dict(type="hero", t0=82.6, t1=83.833, y=0.52, small="za jedyne", big="17 zł", size=260, bigT=83.04, hideCaps=True),
    step(1, 84.9, 87.933, [("Dalej", 85.24, 0), ("pytać", 85.56, 0), ("AI,", 85.86, 0), ("jak", 86.32, 1), ("zarabiać", 86.44, 1)]),
    step(2, 87.933, 91.833, [("Stworzyć", 89.50, 0), ("coś,", 89.84, 0), ("za", 90.30, 1), ("co", 90.30, 1), ("ludzie", 90.76, 1), ("zapłacą", 90.92, 1)]),
    dict(type="cta", t0=92.10, t1=95.7, y=1400, text="Kliknij poniżej"),
]
BR10 = [dict(t0=8.48, t1=10.7, file="confused_1", ss=5.0), dict(t0=11.72, t1=13.2, file="aichat_0", ss=4.0),
        dict(t0=13.2, t1=14.633, file="aiimage_1", ss=2.0), dict(t0=24.28, t1=25.42, file="blank_0", ss=3.0),
        dict(t0=44.36, t1=46.1, file="filming_2", ss=2.0), dict(t0=62.32, t1=64.7, file="office_1", ss=4.0)]

make("ads7", "add7fixed.mp4", "tr_a7f.json", FIX7, IT7, BR7, 0.6, [], END)
make("ads10", "ads10.mp4", "tr_ads10.json", FIX10, IT10, BR10, 0.6, [], END)
