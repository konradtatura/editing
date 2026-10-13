#!/usr/bin/env python3
"""Style-4 caption spec (ad11).  usage: build_spec4.py WORKDIR
Script text is aligned onto whisper word times. Markup: ^word^ = yellow emphasis chunk (join words with _), | = force chunk break."""
import difflib, json, os, re, subprocess, sys
WD = sys.argv[1]
norm = lambda t: re.sub(r"[^\w]", "", t.lower())
WEAK = {"i", "w", "z", "na", "do", "od", "po", "a", "o", "że", "bo", "się", "to", "jak", "czy", "nie", "co", "za", "ci", "ten", "go", "im", "aż", "ani", "jest"}

SCRIPT = ("Jest biznes, w którym możesz sprzedać ten sam produkt setki razy… | I nie wysłać ^ani_jednej_paczki.^ "
          "A dzięki AI jego zbudowanie stało się znacznie prostsze niż kiedykolwiek wcześniej. "
          "Jest jeden sekretny model zarabiania przez internet, który istniał na długo przed ChatGPT. "
          "Ale AI właśnie sprawiło, że nawet zwykli ludzie mogą zacząć go budować bez bycia ekspertami. "
          "Mowa o ^produktach_cyfrowych.^ E-bookach, planerach i szablonach, za które ludzie płacą, bo pomagają im rozwiązywać "
          "konkretne problemy. Kiedyś stworzenie takiego biznesu wymagało wielu różnych umiejętności. Ale dzisiaj AI może wykonać "
          "znaczną część tej pracy. AI pomaga Ci znaleźć pomysł na produkt, sprawdzić, czego szukają potencjalni klienci, stworzyć "
          "produkt i przygotować stronę sprzedażową. Następnie pomaga tworzyć filmiki, które przyciągają zainteresowanych na Twoją "
          "stronę. Ktoś kupuje? Automatycznie otrzymuje produkt. Bez magazynu. Bez wysyłania paczek. A ten sam produkt możesz "
          "sprzedawać ^wielokrotnie.^ Konrad, twórca Cyfrowego Autopilota, sprzedaje produkty cyfrowe od ponad trzech lat. W swoim "
          "najlepszym dniu sprzedał aż | 941_e-booków i przez to wylądował na billboardach na Times Square jako jedyny Polak. Na "
          "podstawie swojego doświadczenia stworzył system, który pokazuje zwykłym ludziom, jak wykorzystać AI do zbudowania "
          "własnego biznesu cyfrowego. Od pomysłu do produktu i strony gotowej do sprzedaży w ^48_godzin.^ I nie, nie jest on "
          "kolejnym guru, który sprzedaje kurs za 5_000_zł. Aktualnie jest promocja i dostęp do całego systemu kosztuje jedyne "
          "^17_zł.^ Kliknij przycisk poniżej i zobacz, jak zacząć budować swój pierwszy biznes cyfrowy z AI.")


def align(words, text):
    toks = []
    for raw in text.split():
        if raw == "|": toks[-1]["brk"] = True; continue
        em = raw.startswith("^")
        parts = raw.strip("^").split("_")
        for k, p in enumerate(parts): toks.append({"d": p, "em": em, "join": k > 0, "brk": False})
    a = [norm(w["w"]) for w in words]; b = [norm(t["d"]) for t in toks]; T = [None] * len(toks); E = [None] * len(toks)
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        if op == "equal":
            for k in range(i2 - i1): T[j1 + k], E[j1 + k] = words[i1 + k]["s"], words[i1 + k]["e"]
        elif op == "replace":
            s0, e0 = words[i1]["s"], words[i2 - 1]["e"]; n = j2 - j1
            for j in range(j1, j2): T[j] = s0 + (e0 - s0) * (j - j1) / n; E[j] = s0 + (e0 - s0) * (j - j1 + 1) / n
    for j in range(len(toks)):
        if T[j] is None:
            T[j] = next((E[k] for k in range(j - 1, -1, -1) if E[k] is not None), 0.0); E[j] = T[j] + .2
        toks[j]["t"], toks[j]["e"] = round(T[j], 3), round(E[j], 3)
    return toks


def chunk(toks, maxw=3, maxc=17):
    out, cur = [], []
    def flush():
        if cur: out.append(cur[:]); cur.clear()
    for u in toks:
        if cur and not u["join"]:
            clen = sum(len(x["d"]) + 1 for x in cur) + len(u["d"])
            if u["em"] != cur[-1]["em"] or len(cur) >= maxw or clen > maxc:
                carry = []
                if not cur[-1]["em"]:  # a dangling weak word moves on to the next chunk (also into a yellow one)
                    while len(cur) > 1 and cur[-1]["d"][-1].isalnum() and cur[-1]["d"].lower() in WEAK: carry.insert(0, cur.pop())
                flush(); cur.extend(carry)
        cur.append(u)
        if u["brk"] or u["d"].endswith((".", "?", "!", "…")) or (u["d"].endswith(",") and len(cur) >= 2): flush()
    flush()
    return out


words = [w for s in json.load(open(os.path.join(WD, "tr_ad11.json"))) for w in s["words"]]
src = os.path.join(WD, "ad11.mp4")
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", src], capture_output=True, text=True).stdout)
ch = chunk(align(words, SCRIPT))
caps = []
for i, c in enumerate(ch):
    t0 = c[0]["t"] - 0.05; end = c[-1]["e"] + 0.35
    nxt = ch[i + 1][0]["t"] - 0.05 if i + 1 < len(ch) else dur
    t1 = nxt if nxt - c[-1]["e"] < 0.7 else min(nxt, end)
    txt = " ".join(w["d"] for w in c).rstrip(",.…")
    if any(w["em"] for w in c) and len(txt) > 12:  # two balanced lines
        sp = [m.start() for m in re.finditer(" ", txt)]; k = min(sp, key=lambda i: abs(i - len(txt) / 2)); txt = txt[:k] + "<br>" + txt[k + 1:]
    caps.append(dict(t0=round(max(0, t0), 3), t1=round(t1, 3), html=txt, em=any(w["em"] for w in c)))
# hook variants are cut at these scene cuts, so no caption may straddle them
for c in (10.733, 21.533):
    for cp in caps:
        if cp["t0"] < c < cp["t1"]:
            if c - cp["t0"] > cp["t1"] - c: cp["t1"] = c
            else: cp["t0"] = c
# where the animation has a big card in the frame centre, the caption drops lower
ZONES = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "zones_ad11.json")))
spec = dict(dur=round(dur, 3), fps=30, capY=0.5, zones=ZONES, caps=caps)
json.dump(spec, open(os.path.join(WD, "spec4_ad11.json"), "w"), ensure_ascii=False, indent=1)
for c in caps: print(f'{c["t0"]:6.2f}-{c["t1"]:6.2f} {"*" if c["em"] else " "} {c["html"]}')
