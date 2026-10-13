#!/usr/bin/env python3
"""Style 6 ("10/10" list) spec.  usage: build_spec6.py WORKDIR NAME   (reads WORKDIR/NAME.mp4 + WORKDIR/tr_NAME.json)
Script text is aligned onto whisper word times; captions = 2-3 words, hard cuts. Each emoji swaps in on the first word
of its point (snapped back to a camera cut when one is within 0.3 s before)."""
import difflib, json, os, re, subprocess, sys
WD, NAME = sys.argv[1], sys.argv[2]
HERE = os.path.dirname(os.path.abspath(__file__))
norm = lambda t: re.sub(r"[^\w]", "", t.lower())
WEAK = {"i", "w", "z", "na", "do", "a", "o", "że", "się", "to", "nie", "co", "ale", "ten", "niż"}

TITLE = "10/10 nawyków, których<br>nikt Cię nie uczy"
SCRIPT = ("10 na 10 prostych nawyków, których nikt Cię nie uczy, a zmienią Twoje życie. "
          "Ustawiaj budzik na godzinę, o której masz iść spać, a nie wstawać. Przestań oglądać wiadomości. "
          "Naucz się mówić nie częściej niż tak. Przestań obserwować ludzi na Instagramie, z którymi nawet nie przywitałbyś się na ulicy. "
          "Pamiętaj, że możesz odpuścić jeden dzień, ale nigdy dwa dni z rzędu. Inwestuj w siebie. "
          "Otaczaj się ludźmi, którzy osiągnęli więcej niż Ty. Czytaj codziennie minimum 10 stron książki. "
          "Zawsze zakładaj dobre intencje. Rób codziennie coś, czego się boisz. Zaobserwuj ten profil.")
# point -> (emoji, first word of the point in SCRIPT order)  -- same emoji as the original where the habit matches
POINTS = [("⏰", "Ustawiaj"), ("📺", "Przestań"), ("🚫", "Naucz"), ("📱", "Przestań"), ("💪", "Pamiętaj"),
          ("📈", "Inwestuj"), ("🤝", "Otaczaj"), ("📖", "Czytaj"), ("💡", "Zawsze"), ("😨", "Rób")]
COLORS = ["#FFFFFF", "#FD0004", "#F9A901", "#ADFA01", "#03FC04", "#00FCAC", "#03A8F8", "#0500FA", "#A700FE", "#FC00A7"]


def align(words, text):
    toks = [{"d": w} for w in text.split()]
    a = [norm(w["w"]) for w in words]; b = [norm(t["d"]) for t in toks]; T = [None] * len(toks); E = [None] * len(toks)
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        if op == "equal":
            for k in range(i2 - i1): T[j1 + k], E[j1 + k] = words[i1 + k]["s"], words[i1 + k]["e"]
        elif op == "replace":
            s0, e0 = words[i1]["s"], words[i2 - 1]["e"]; n = j2 - j1
            for j in range(j1, j2): T[j] = s0 + (e0 - s0) * (j - j1) / n; E[j] = s0 + (e0 - s0) * (j - j1 + 1) / n
    for j in range(len(toks)):
        if T[j] is None: T[j] = next((E[k] for k in range(j - 1, -1, -1) if E[k] is not None), 0.0); E[j] = T[j] + .2
        toks[j]["t"], toks[j]["e"] = round(T[j], 3), round(E[j], 3)
    return toks


def chunk(toks, maxw=3, maxc=16):
    out, cur = [], []
    for u in toks:
        if cur and (len(cur) >= maxw or sum(len(x["d"]) + 1 for x in cur) + len(u["d"]) > maxc):
            carry = []
            while len(cur) > 1 and cur[-1]["d"][-1].isalnum() and cur[-1]["d"].lower() in WEAK: carry.insert(0, cur.pop())
            out.append(cur); cur = carry
        cur.append(u)
        if u["d"][-1] in ".?!" or (u["d"][-1] == "," and len(cur) >= 2): out.append(cur); cur = []
    if cur: out.append(cur)
    return out


src = os.path.join(WD, NAME + ".mp4")
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", src], capture_output=True, text=True).stdout)
cuts = json.loads(subprocess.run([sys.executable, os.path.join(HERE, "..", "reklamy_CA", "engine", "cuts.py"), src], capture_output=True, text=True).stdout)
words = [w for s in json.load(open(os.path.join(WD, "tr_" + NAME + ".json"))) for w in s["words"]]
toks = align(words, SCRIPT)
ch = chunk(toks)
caps = []
for i, c in enumerate(ch):
    nxt = ch[i + 1][0]["t"] - 0.03 if i + 1 < len(ch) else dur
    t1 = nxt if nxt - c[-1]["e"] < 0.7 else min(nxt, c[-1]["e"] + 0.35)
    caps.append(dict(t0=round(max(0, c[0]["t"] - 0.03), 3), t1=round(t1, 3), text=" ".join(w["d"] for w in c).rstrip(",.")))
# swap times: k-th occurrence of each point's first word, after the hook sentence
items, pos = [], next(i for i, t in enumerate(toks) if t["d"].rstrip(".,").lower() == "ustawiaj")
for k, (emo, first) in enumerate(POINTS):
    j = next(i for i in range(pos, len(toks)) if toks[i]["d"].rstrip(".,") == first); pos = j + 1
    t = toks[j]["t"] - 0.05; c = [x for x in cuts if 0 <= t - x <= 0.3]
    items.append(dict(emoji=emo, color=COLORS[k], t=round(c[-1] if c else t, 3)))
# 1080x1920. Original (720x1280): title pill y 215-325, grid 534x164 at y 756, caption centre y 706. Here 6-7% lower (mouth sits lower).
layout = dict(titleY=318, titleFs=50, gridY=1268, cellW=148, cellH=111, capY=1192)
json.dump(dict(dur=round(dur, 3), fps=30, title=TITLE, layout=layout, items=items, caps=caps),
          open(os.path.join(WD, f"spec6_{NAME}.json"), "w"), ensure_ascii=False, indent=1)
for it in items: print(f'{it["t"]:6.2f} {it["emoji"]}')
for c in caps: print(f'{c["t0"]:6.2f}-{c["t1"]:6.2f} {c["text"]}')
