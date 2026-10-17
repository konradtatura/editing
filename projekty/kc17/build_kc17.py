#!/usr/bin/env python3
"""2026-10-17 talking-head ads (Konrad cut them himself; nothing is cut here, cuts only drive the zooms).
creatorh1V2 -> style 2, skillh2v2 -> style 3. Konrad: NO colour grading (grade = "" for footage and b-roll).
usage: build_kc17.py WORKDIR STOCKDIR   (WORKDIR: skillh2v2.mp4, creatorh1V2.mp4, tr_<name>.json)"""
import os, sys
P = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
def load(path, stop):  # helper functions of a style builder (everything before its ad-specific part)
    s = open(path).read(); g = {"__file__": path}; exec(compile(s[:s.index(stop)], path, "exec"), g); return g

# ---------------------------------------------------------------- CREATOR H1 v2 (style 2, 58.3 s)
s2 = load(os.path.join(P, "styl2", "build_spec2.py"), "END = dict"); s2["GRADE"] = ""
pw = s2["pw"]
FIXC = ("Większość ludzi używa ChatGPT, żeby szybciej wykonywać codzienne zadania. Ale jest coś znacznie ciekawszego, co możesz zrobić. "
        "Możesz wykorzystać AI do zbudowania czegoś własnego, co może zamienić się w *dodatkowy_dochód.* Bo pomyśl, możesz używać "
        "ChatGPT do pisania maili. Możesz generować obrazki, memy, zadawać pytania i mieć zapisane tysiące promptów. I to wszystko jest "
        "przydatne. Ale jest *ogromna_różnica* między używaniem AI do codziennych zadań, a wykorzystaniem AI do stworzenia czegoś, co "
        "*należy_do_Ciebie.* Na przykład własnego ebooka, szablonu albo prostego produktu cyfrowego, który możesz wystawić na sprzedaż. "
        "Bo tak, odpowiedź z ChatGPT może pomóc rozwiązać jeden problem, ale produkt, który zbudujesz z pomocą AI, możesz rozwijać, "
        "ulepszać i *sprzedawać_więcej_niż_raz.* I właśnie dlatego stworzyłem *Cyfrowy_Autopilot.* Nie po to, żeby nauczyć Cię "
        "kolejnych sztuczek z ChatGPT, tylko żeby pokazać Ci, jak wykorzystać AI do stworzenia własnego produktu cyfrowego. Od pomysłu "
        "na produkt, przez przygotowanie jego treści, aż po stronę, na której możesz go wystawić na sprzedaż. I to wszystko według "
        "konkretnego procesu rozpisanego od A do Z. Bo AI nie musi być tylko narzędziem, które oszczędza czas. Może być narzędziem, "
        "z pomocą którego zaczniesz budować *coś_własnego.* Więc kliknij poniżej i zacznij dzisiaj.")
# NEW components (engine/creator_fx.js) — Konrad: keep the style-2 look, never reuse its old animations 1:1
ITC = [
    dict(type="chat", t0=0.0, t1=3.55, y=1300, text="Napisz maila do klienta…"),
    dict(type="wipe", t0=3.62, t1=5.533, y=760, small="Ale jest coś", big=["znacznie", "ciekawszego"], size=130, bigT=4.05, hideCaps=True),
    dict(type="income", t0=5.68, t1=9.833, y=1330, label="dodatkowy dochód", lt=9.0),
    dict(type="bubbles", t0=10.38, t1=17.367, y=1640, okT=16.9, okText="przydatne… ale", items=[
        dict(emo="✉️", text="maile", t=11.70), dict(emo="🖼️", text="obrazki", t=13.0), dict(emo="😂", text="memy", t=13.60),
        dict(emo="❓", text="pytania", t=14.20), dict(emo="📁", text="tysiące promptów", t=15.28)]),
    dict(type="versus", t0=17.367, t1=23.033, hideCaps=True, lt=18.80, rt=20.55, winT=22.30),
    dict(type="ebook", t0=23.033, t1=27.567, y=1060, stampT=26.70, hideCaps=True, items=[dict(text="szablon", t=24.20), dict(text="produkt cyfrowy", t=25.36)]),
    dict(type="sales", t0=28.0, t1=34.867, y=1290, xT=33.70, notes=[dict(t=30.80), dict(t=31.90), dict(t=33.10)]),
    dict(type="brand", t0=34.96, t1=36.95, small="Dlatego stworzyłem", big="Cyfrowy<br>Autopilot", bigT=35.98, hideCaps=True),
    dict(type="strike", t0=37.0, t1=43.233, y=1330, bad="kolejne sztuczki z ChatGPT", strikeT=38.40, good="własny produkt cyfrowy", goodT=41.80),
    dict(type="path", t0=43.233, t1=47.533, y=1340, items=[dict(icon="lightbulb", text="pomysł", t=43.46),
        dict(icon="pen-line", text="treść", t=44.90), dict(icon="globe", text="strona", t=45.88)]),
    dict(type="atoz", t0=47.533, t1=50.733, y=1290, aT=50.10, zT=50.48, label="konkretny proces"),
    dict(type="morph", t0=50.733, t1=56.533, y=1360, a0="narzędzie, które oszczędza czas", b0="narzędzie do budowania", swapT=53.90),
    dict(type="tap", t0=56.6, t1=58.4, y=1330, text="Kliknij poniżej", hideCaps=False),
]
BRC = [dict(t0=10.38, t1=12.40, file="typing_1", ss=1.0), dict(t0=12.42, t1=14.0, file="phone_1", ss=1.0),
       dict(t0=27.60, t1=30.62, file="think_1", ss=2.0)]
s2["make"]("creatorh1V2", "creatorh1V2.mp4", "tr_creatorh1V2.json", FIXC, ITC, BRC, 0.6, [], {})
import json as _j                                   # no end card: the film ends on Konrad's CTA
_p = os.path.join(sys.argv[1], "spec2_creatorh1V2.json"); _s = _j.load(open(_p))
_s["items"] = [i for i in _s["items"] if i["type"] != "end"]; _s["dur"] = _s["srcDur"]; _j.dump(_s, open(_p, "w"), ensure_ascii=False, indent=1)

# ---------------------------------------------------------------- SKILL H2 v2 (style 3, 67.0 s)
s3 = load(os.path.join(P, "styl3", "build_spec3.py"), "PL = dict"); s3["GRADE"] = ""
pw, PL = s3["pw"], dict(type="plansza", hideCaps=True)
FIXS = ("Nie umiesz pisać ebooków? To nie znaczy, że nie możesz stworzyć własnego. Nie umiesz robić stron? Nie znasz się na marketingu? "
        "Jeszcze kilka miesięcy temu te *trzy_rzeczy* mogły skutecznie powstrzymać Cię przed rozpoczęciem sprzedaży produktów cyfrowych. "
        "Ale dzisiaj sztuczna inteligencja ~kompletnie~ zmieniła tę sytuację. Bo pomyśl, kiedyś, żeby stworzyć i sprzedawać własnego "
        "ebooka, musiałeś nauczyć się kilku różnych rzeczy. Najpierw pisania, potem budowania stron internetowych, a na końcu jeszcze "
        "marketingu, żeby ktokolwiek w ogóle dowiedział się o Twoim produkcie. Jeśli czegoś nie potrafiłeś, to miałeś dwie opcje. Albo "
        "spędzić miesiące na nauce, albo zapłacić komuś, kto zrobi to za Ciebie. Ale dzisiaj masz *trzecią_opcję.* Możesz wykorzystać "
        "~sztuczną_inteligencję.~ Nie umiesz pisać ebooków? AI pomoże Ci przygotować strukturę, rozdziały i pierwszą wersję treści, którą "
        "następnie możesz dopracować. Nie umiesz robić stron? AI może pomóc Ci stworzyć stronę pod Twój produkt. Nie znasz się na "
        "marketingu? AI może pomóc Ci przygotować pierwszą wersję oferty sprzedażowej. I właśnie dlatego stworzyliśmy Cyfrowy Autopilot, "
        "żeby pokazać Ci, jak połączyć te wszystkie elementy w *jeden_konkretny_proces.* Od pomysłu, przez stworzenie produktu, aż po "
        "stronę, na której możesz go wystawić na sprzedaż. A wszystko według planu ~od_A_do_Z.~ Bo dzisiaj, żeby zacząć tworzyć produkty "
        "cyfrowe, nie musisz najpierw zostać *ekspertem* od wszystkiego. Musisz po prostu wiedzieć, jak wykorzystać sztuczną inteligencję "
        "do rzeczy, których jeszcze nie potrafisz zrobić ~samodzielnie.~ Więc kliknij poniżej i zacznij działać już dzisiaj.")
# NEW components (engine/skill_fx.js), style-3 look only
ITS = [
    dict(type="locks", t0=0.0, t1=13.367, y=1330, shakeT=7.96, unlockT=11.92, items=[
        dict(icon="file-text", text="ebooki", t=0.52), dict(icon="layout-template", text="strony", t=3.66), dict(icon="megaphone", text="marketing", t=4.74)]),
    dict(type="bars", t0=13.46, t1=23.467, y=1320, head="kiedyś musiałeś nauczyć się:", items=[
        dict(text="Pisania", t=17.60), dict(text="Budowania stron", t=18.60), dict(text="Marketingu", t=20.70)]),
    dict(type="options", t0=23.467, t1=32.2, hideCaps=True, h0="Nie potrafisz?", hT=25.02, c1T=25.52, c2T=27.40, c3T=29.20, aiT=30.92),
    dict(type="builds", t0=32.2, t1=44.533, y=1300, steps=[dict(t=32.2, title="Twój ebook"), dict(t=37.70, title="Twoja strona"), dict(t=40.68, title="Twoja oferta")]),
    dict(type="merge", t0=44.533, t1=50.1, hideCaps=True, head="Dlatego stworzyliśmy", mergeT=47.64),
    dict(type="chev", t0=50.1, t1=55.467, y=1330, azT=54.48, label="według planu od A do Z", items=[
        dict(text="pomysł", t=50.38), dict(text="produkt", t=51.32), dict(text="strona", t=52.10)]),
    dict(type="expert", t0=57.62, t1=59.7, y=1330, stampT=58.82),
    dict(type="cta2", t0=64.80, t1=67.0, y=1420, text="Kliknij poniżej"),
]
s3["make"]("skillh2v2", "skillh2v2.mp4", "tr_skillh2v2.json", FIXS, ITS, capY=0.6)
