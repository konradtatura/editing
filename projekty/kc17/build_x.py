#!/usr/bin/env python3
"""v4 ads built from the X swipefile (projekty/swipefile/X_EDITS_2026-10-17.md). Konrad cut them; nothing is cut here.
creator4 -> engine/x1.html (Joshua + Ruwan vibe), skill4 -> engine/x2.html (Amber + Arham + Yoo vibe). No colour grading.
usage: build_x.py WORKDIR NAME   (WORKDIR/NAME.mp4 + tr_NAME.json) -> WORKDIR/specx_NAME.json"""
import json, os, sys
P = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
WD, NAME = sys.argv[1], sys.argv[2]
s = open(os.path.join(P, "styl2", "build_spec2.py")).read(); g = {"__file__": os.path.join(P, "styl2", "build_spec2.py")}
sys.argv = [sys.argv[0], WD, WD]; exec(compile(s[:s.index("END = dict")], "s2", "exec"), g)   # align(), chunk(), dur(), cuts()
dur, cuts = g["dur"], g["cuts"]
s3 = open(os.path.join(P, "styl3", "build_spec3.py")).read(); g3 = {"__file__": os.path.join(P, "styl3", "build_spec3.py")}
exec(compile(s3[:s3.index("PL = dict")], "s3", "exec"), g3); align, chunk = g3["align"], g3["chunk"]   # *x* -> h=1, ~x~ -> h=2

C1, C2 = dict(c1="#FF8A5C", c2="#E2452B"), dict(c1="#9B8CFF", c2="#5B47E0")
C3, C4, C5 = dict(c1="#4DB5FF", c2="#1572E8"), dict(c1="#FFC94D", c2="#F08C00"), dict(c1="#FF6FAE", c2="#D61F69")
ADS = {}
ADS["creator4"] = dict(page="x1.html", capY=0.615, maxw=4, maxc=22, text=(
    "AI może zaoszczędzić Ci mnóstwo *czasu.* Ale wyobraź sobie, że zamiast kolejnej odpowiedzi z ChatGPT, masz przed sobą coś, co "
    "*sam_stworzyłeś.* Własnego *ebooka,* własny *produkt_cyfrowy,* własną *stronę,* na której możesz go *sprzedawać.* Czyli coś, co się "
    "*sprzedaje,* na co możesz spojrzeć i powiedzieć: dobra, to jest *moje.* I właśnie dlatego uważam, że większość ludzi nie wykorzystuje "
    "jeszcze *pełnych_możliwości* sztucznej inteligencji, bo używają jej głównie do codziennych zadań. Czyli pisania *maili,* generowania "
    "*obrazków,* odpowiadania na *pytania.* I nie ma w tym nic złego. Ale wyobraź sobie, gdybyś wykorzystał te same narzędzia do stworzenia "
    "czegoś *własnego.* Czegoś, co nie kończy się na jednej rozmowie z ChatGPT czy Claude'em, tylko staje się *produktem,* który możesz "
    "rozwijać i *sprzedawać.* I właśnie dlatego powstał *Cyfrowy_Autopilot,* żeby pokazać Ci, jak wykorzystać AI nie tylko do wykonywania "
    "zadań, ale do *budowania* własnych produktów cyfrowych. Od znalezienia pomysłu, przez stworzenie ebooka, stronę i marketing z pomocą "
    "sztucznej inteligencji, według prostego procesu rozpisanego *od_A_do_Z.* I nie chodzi o to, żebyś został ekspertem od wszystkich "
    "możliwych narzędzi AI. Chodzi o to, żebyś wykorzystał je w *najmądrzejszy* sposób do stworzenia czegoś, czego dzisiaj jeszcze nie masz. "
    "Czegoś *własnego,* co możesz wystawić na sprzedaż. Bo AI może pomóc Ci pracować *szybciej,* ale może też pomóc Ci zacząć *budować* coś, "
    "co zostanie z Tobą na *dłużej.* Więc kliknij *poniżej* tego filmu i zobacz, jak to działa."),
  items=[
    dict(type="notif", t0=0.0, t1=1.967, y=1350, title="ChatGPT", sub="Gotowe ✓ odpowiedź w 3 sekundy", icon="sparkles"),
    dict(type="swap", t0=2.12, t1=6.433, y=1330, boxT=5.46, label="coś, co sam stworzyłeś"),
    dict(type="equation", t0=6.433, t1=10.067, y=1330, items=[dict(C1, icon="file-text", text="ebook", t=6.90),
        dict(C2, icon="package", text="produkt", t=7.66), dict(C3, icon="globe", text="strona", t=8.74)]),
    dict(type="sales", t0=10.067, t1=13.6, y=1370, notes=[dict(t=10.84), dict(t=11.50), dict(t=12.20)]),
    dict(type="gauge", t0=15.24, t1=19.767, y=1360, label="Możliwości AI, które wykorzystujesz", sub="większość ludzi zatrzymuje się tutaj", fill=.22),
    dict(type="pills", t0=19.767, t1=23.933, y=1330, okT=22.90, okText="✓ nic złego", items=[dict(emo="📧", text="maile", t=20.04),
        dict(emo="🖼️", text="obrazki", t=20.76), dict(emo="💬", text="pytania", t=21.78)]),
    dict(type="leak", t0=23.75, t1=24.2),
    dict(type="chat2prod", t0=27.867, t1=33.667, y=1330, prodT=31.60, growT=32.70),
    dict(type="figma", t0=33.667, t1=35.70, hideCaps=True, small="Dlatego powstał", big="Cyfrowy<br>Autopilot", bigT=34.70),
    dict(type="toggle", t0=35.72, t1=40.833, y=1370, a="AI do zadań", b="AI do budowania", sub="przełącz się z zadań na produkty", flipT=39.14),
    dict(type="flow", t0=40.833, t1=44.967, y=1340, items=[dict(C4, icon="lightbulb", text="pomysł", t=41.54), dict(C1, icon="file-text", text="ebook", t=42.48),
        dict(C3, icon="globe", text="strona", t=43.10), dict(C5, icon="megaphone", text="marketing", t=43.32)]),
    dict(type="reminder", t0=47.50, t1=50.50, y=1350, title="Nie musisz:", items=[dict(text="być ekspertem od każdego narzędzia AI", t=47.60, strike=48.66)]),
    dict(type="leak", t0=54.65, t1=55.05),
    dict(type="duo", t0=56.80, t1=61.80, y=1340, a0="pracować szybciej", aT=57.96, b0="budować coś swojego", bT=59.78),
    dict(type="link", t0=61.98, t1=64.10, y=1380, text="Kliknij poniżej"),
  ])

ADS["skill4"] = dict(page="x2.html", capY=0.60, maxw=4, maxc=20, text=(
    "Żeby sprzedać jednego ebooka, musisz najpierw nauczyć się *trzech* różnych zawodów: pisania, robienia stron i marketingu. Przecież to "
    "~bez_sensu.~ A właśnie tak jeszcze kilka miesięcy temu wyglądało rozpoczęcie sprzedaży produktów cyfrowych. Chciałeś stworzyć ebooka, "
    "to najpierw musiałeś nauczyć się go *pisać.* Potem dowiadywałeś się, że potrzebujesz *strony* internetowej, więc kupowałeś "
    "~kolejny_kurs~ i siedziałeś po ~nocach,~ żeby coś tam zbudować. Kiedy w końcu miałeś produkt i stronę, to okazywało się, że jeszcze "
    "trzeba jakoś przyciągać ~klientów.~ Czyli znowu nauka, znowu kursy, znowu kolejne rzeczy, które musisz opanować, zanim w ogóle zaczniesz. "
    "Ale dzisiaj żyjemy w pięknych czasach i jest jedna *ogromna_różnica.* Masz sztuczną inteligencję, i *AI* może pomóc Ci wykonać dużą "
    "część pracy, która wcześniej wymagała kilku różnych umiejętności. Nie umiesz napisać ebooka? *AI* pomoże Ci przygotować jego pierwszą "
    "wersję. Nie potrafisz zrobić strony? Możesz wykorzystać narzędzia *AI,* które pomogą Ci ją zbudować. Nie znasz się na przyciąganiu "
    "klientów? *AI* może pomóc Ci przygotować marketing. Więc nie musisz już zaczynać od ~miesięcy~ nauki wszystkiego od zera. I dokładnie "
    "dlatego stworzyłem *Cyfrowy_Autopilot.* To proces pokazujący krok po kroku, jak wykorzystać AI do zbudowania własnego produktu "
    "cyfrowego. Z jednym prostym celem: przeprowadzić Cię przez wszystko od A do Z w mniej niż *48_godzin.* Bo największa zmiana, jaką "
    "przyniosło AI, nie polega na tym, że wszyscy nagle stali się ~ekspertami.~ Polega właśnie na tym, że nie musisz być ekspertem, żeby "
    "*zacząć* coś stworzyć. Więc kliknij *poniżej* i zobacz, jak możesz z tym zacząć właśnie teraz."),
  items=[
    dict(type="badges", t0=3.30, t1=6.10, y=1310, badT=5.34, items=[dict(text="pisanie", t=3.44), dict(text="strony", t=3.96), dict(text="marketing", t=4.54)]),
    dict(type="kinetic", t0=6.60, t1=8.30, hideCaps=True, y=760, size=130, text="Kilka<br>miesięcy temu", sub="tak wyglądał start"),
    dict(type="courses", t0=12.20, t1=18.167, y=1290, items=[dict(emo="📝", text="Kurs pisania", t=12.26), dict(emo="🌐", text="Kurs stron", t=14.14),
        dict(emo="📚", text="Kolejny kurs", t=15.52), dict(emo="🌙", text="Noce przy laptopie", t=16.64)]),
    dict(type="clicker", t0=18.167, t1=22.733, hideCaps=True, items=[dict(icon="file-text", text="produkt", t=18.30), dict(icon="layout-template", text="strona", t=19.86),
        dict(icon=None, text="klienci?", t=21.70)]),
    dict(type="znowu", t0=22.733, t1=27.533, hideCaps=True, y=1230, items=[dict(text="nauka", t=23.00), dict(text="kursy", t=23.86), dict(text="kolejne rzeczy", t=24.56)]),
    dict(type="flash", t0=27.533, t1=27.90),
    dict(type="brackets", t0=29.42, t1=30.46, x=250, y=320, w=520, h=680),
    dict(type="orb", t0=30.46, t1=36.033, y=1290, lT=32.98, label="robi dużą część pracy"),
    dict(type="flips", t0=36.033, t1=46.20, y=1290, items=[dict(t=36.08, ft=37.30, bad="nie umiesz napisać ebooka", good="AI: pierwsza wersja ebooka"),
        dict(t=39.36, ft=40.58, bad="nie potrafisz zrobić strony", good="AI: buduje Twoją stronę"),
        dict(t=43.10, ft=44.52, bad="nie znasz się na klientach", good="AI: przygotuje marketing")]),
    dict(type="kinetic", t0=49.467, t1=51.68, hideCaps=True, y=760, size=140, text="Cyfrowy<br>Autopilot", sub="proces krok po kroku"),
    dict(type="loader", t0=51.68, t1=58.50, y=1320, title="Twój produkt cyfrowy", stages=[dict(text="pomysł", t=52.76), dict(text="produkt", t=54.58), dict(text="strona", t=55.80)]),
    dict(type="count", t0=58.50, t1=62.60, y=1330),
    dict(type="strike2", t0=62.60, t1=66.867, y=1340, text="Ekspert", sT=66.10),
    dict(type="search", t0=70.27, t1=73.20, y=1300, q="Cyfrowy Autopilot"),
  ])

cfg = ADS[NAME]; src = os.path.join(WD, NAME + ".mp4"); sd = round(dur(src), 3); cs = cuts(src)
words = [w for s in json.load(open(os.path.join(WD, "tr_" + NAME + ".json"))) for w in s["words"]]
caps = chunk(align(words, cfg["text"]), maxw=cfg["maxw"], maxc=cfg["maxc"])
ends = {round(w["s"], 2): w["e"] for w in words}
for i, b in enumerate(caps):
    nxt = caps[i + 1]["t0"] if i + 1 < len(caps) else sd
    b["t1"] = round(min(nxt, b["words"][-1]["t"] + 1.3), 3)
z, big = [], False
for t in [0.0] + cs: z.append([t, 1.10 if big else 1.0]); big = not big
spec = dict(src=src, srcDur=sd, dur=sd, fps=30, capY=cfg["capY"], caps=caps, items=cfg["items"], brolls=[], cuts=cs, zooms=z,
            zoomCenter=[0.5, 0.3], grade="", page=cfg["page"])
json.dump(spec, open(os.path.join(WD, f"specx_{NAME}.json"), "w"), ensure_ascii=False, indent=1)
print(len(caps), "caption blocks,", len(cs), "cuts")
for b in caps: print(f'  {b["t0"]:6.2f}-{b["t1"]:6.2f}  ' + " ".join(("*" + w["d"] + "*") if w["h"] else w["d"] for w in b["words"]))
