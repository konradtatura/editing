#!/usr/bin/env python3
"""„3 modele biznesu” batch 1 (plan #1–25 + 3 wall callouts). B = full-screen MP4, K = card / wall text (MOV with alpha).
Every timing is a word of CUT.mp4 (words.py), relative to the scene in-point. Style: white Apple v2 (base.css), Inter only."""
import json, os, sys
from page import page, HERE
from words import W
from geo import Shape

S = {}


def sc(key, a, b, mode, body, js, css=""):
    S[key] = dict(a=round(a, 2), b=round(b, 2), ov=mode == "K", body=body, js=js, css=css)


def R(a):            # word time relative to scene start
    return lambda w, after=None: round(W(w, a if after is None else after) - a, 2)


CHECK = '<svg viewBox="0 0 28 26"><path d="M3 13 L11 21 L25 4" fill="none" stroke="#fff" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round"/></svg>'
PAUSE = '<svg viewBox="0 0 100 100"><rect x="30" y="24" width="13" height="52" rx="4" fill="#fff"/><rect x="57" y="24" width="13" height="52" rx="4" fill="#fff"/></svg>'
# wall text (A+): white type on the wooden wall right of the head (x 1290–1800, y 170–640)
WALL_CSS = """
      .wall { position: absolute; left: 1330px; top: 190px; width: 560px; color: #fff; text-shadow: 0 3px 10px rgba(0,0,0,0.55), 0 1px 3px rgba(0,0,0,0.45); }
      .wall .wl { font-size: 50px; font-weight: 300; letter-spacing: -0.02em; line-height: 1.15; }
      .wall .wb { font-size: 104px; font-weight: 900; letter-spacing: -0.055em; line-height: 1; }"""

# 3-models card (callback through the film): rows with blurred names, revealed chapter by chapter
MODELS = ["Usługi", "Software", "Produkty cyfrowe"]
MODELS_CSS = """
      .mr { display: flex; align-items: center; gap: 22px; padding: 20px 0; border-top: 1px solid var(--line); }
      .mr .n { width: 52px; height: 52px; border-radius: 50%; background: var(--ink); color: #fff; font-size: 26px; font-weight: 700; display: flex; align-items: center; justify-content: center; flex: none; }
      .mr .nm { font-size: 46px; font-weight: 700; letter-spacing: -0.025em; flex: 1; white-space: nowrap; }
      .mr .bl { filter: blur(11px); opacity: .5; }
      .mr .q { font-size: 34px; font-weight: 700; color: var(--grey); padding: 8px 18px; border-radius: 999px; background: var(--fill); filter: blur(5px); }"""


def models_card(shown=(), done=(), q=False, extra=""):
    rows = ""
    for i, n in enumerate(MODELS, 1):
        cls = "nm" + ("" if i in shown or i in done else " bl")
        sty = ' style="color:var(--grey)"' if i in done else ""
        rows += (f'<div class="mr" id="m{i}"><span class="n" id="mn{i}">{i}</span><span class="{cls}" id="mt{i}"{sty}>{n}</span>'
                 + (f'<span class="q" id="mq{i}">0000 zł</span>' if q else "") + "</div>")
    return f'<div class="card ovc" style="width:680px"><div class="h-m w800" id="mh" style="margin-bottom:18px">3 modele</div>{rows}{extra}</div>'


# ================================================================ 1 · B Ty + laptop + AI
a = W("sam", 5.5) - 0.15; b = W("i właśnie", 7.5) - 0.05; r = R(a)
MAC = ('<svg viewBox="0 0 440 300" width="640" height="436"><rect x="50" y="6" width="340" height="226" rx="16" fill="#1d1d1f"/>'
       '<rect x="62" y="18" width="316" height="202" rx="6" fill="#fff"/><rect x="92" y="54" width="150" height="14" rx="7" fill="#e5e5ea"/>'
       '<rect x="92" y="84" width="240" height="14" rx="7" fill="#e5e5ea"/><rect x="92" y="114" width="200" height="14" rx="7" fill="#e5e5ea"/>'
       '<path d="M8 236 H432 L420 262 Q418 268 410 268 H30 Q22 268 20 262 Z" fill="#d2d2d7"/><rect x="186" y="236" width="68" height="8" rx="4" fill="#b8b8be"/></svg>')
sc("S01", a, b, "B", f"""
      <div class="cam" id="cam">
        <div class="abs eqr">
          <div class="it" id="i1"><div class="ic"><svg viewBox="0 0 860 900" width="330" height="345"><circle cx="430" cy="290" r="230" fill="none" stroke="#1d1d1f" stroke-width="44"/><path d="M60 840 C 100 620 260 520 430 520 C 600 520 760 620 800 840" fill="none" stroke="#1d1d1f" stroke-width="44" stroke-linecap="round"/></svg></div><div class="lb">Ty</div></div>
          <div class="pl" id="p1">+</div>
          <div class="it" id="i2"><div class="ic">{MAC}</div><div class="lb">Laptop</div></div>
          <div class="pl" id="p2">+</div>
          <div class="it" id="i3"><div class="ic"><img src="assets/chatgpt.png" style="width:320px;border-radius:72px"></div><div class="lb">AI</div></div>
        </div>
      </div>""", f"""
      K.push(DUR, 1.05);
      K.lift("#i1", 0.0, {{ y: 40, s: 0.92, dur: 0.55, ease: "expo.out" }});
      K.lift("#p1", {r("laptop")} - 0.12, {{ y: 0, s: 0.6, dur: 0.3 }}); K.lift("#i2", {r("laptop")} - 0.1, {{ y: 40, s: 0.92, dur: 0.55, ease: "expo.out" }});
      K.lift("#p2", {r("sztuczna")} - 0.12, {{ y: 0, s: 0.6, dur: 0.3 }}); K.lift("#i3", {r("sztuczna")} - 0.1, {{ y: 40, s: 0.92, dur: 0.55, ease: "expo.out" }});
      tl.to("#i3 img", {{ scale: 1.06, duration: 0.18, yoyo: true, repeat: 1, ease: "power2.out" }}, {r("inteligencja")});""", """
      .eqr { left: 0; top: 0; width: 1920px; height: 1080px; display: flex; align-items: center; justify-content: center; gap: 40px; }
      .it { display: flex; flex-direction: column; align-items: center; gap: 30px; }
      .it .ic { height: 470px; display: flex; align-items: center; justify-content: center; }
      .it .lb { font-size: 72px; font-weight: 800; letter-spacing: -0.035em; }
      .pl { font-size: 130px; font-weight: 300; color: var(--grey); margin-bottom: 110px; }""")

# ================================================================ 2 · B everyone starts (dot crowd)
a = W("bo jak", 11.2) - 0.1; b = W("a prawie", 13.5) - 0.05; r = R(a)
COLS, ROWS = 30, 11
dots = "".join(f'<i style="left:{c * 52}px;top:{rr * 52}px" data-d="{((c - COLS / 2) ** 2 + (rr - ROWS / 2) ** 2) ** 0.5:.2f}"></i>'
               for rr in range(ROWS) for c in range(COLS))
sc("S02", a, b, "B", f"""
      <div class="cam" id="cam">
        <div class="abs hd"><div class="h-l w300" id="h1">Łatwe do zaczęcia</div><div class="h-l" id="h2">= zaczynają wszyscy.</div></div>
        <div class="abs crowd" id="cr">{dots}</div>
      </div>""", f"""
      K.push(DUR, 1.04);
      K.rise("#h1", 0.02);
      K.lift("#cr", 0.0, {{ y: 20, dur: 0.5 }});
      const tz = {r("zaczynają", a + 1.4)};
      document.querySelectorAll("#cr i").forEach((d) => tl.to(d, {{ backgroundColor: "#0071e3", scale: 1.15, duration: 0.25, ease: "power2.out" }}, tz - 0.15 + parseFloat(d.dataset.d) * 0.035));
      K.rise("#h2", tz - 0.15);""", """
      .hd { left: 160px; top: 110px; }
      .crowd { left: 192px; top: 470px; width: 1560px; height: 560px; }
      .crowd i { position: absolute; width: 30px; height: 30px; border-radius: 50%; background: #d8d8de; }""")

# ================================================================ 3 · B three „Biznes” stickers, two hide „Etat”
a = W("że są", 15.5) - 0.1; b = W("nazywam", 21) - 0.06; r = R(a)
card3 = lambda i, under, sub: (f'<div class="panel bc" id="c{i}"><div class="no">{i}</div>'
                               f'<div class="und"><div class="uw">{under}</div><div class="us">{sub}</div></div>'
                               f'<div class="stk" id="s{i}">Biznes</div><div class="stk2" id="t{i}">biznes</div></div>')
sc("S03", a, b, "B", f"""
      <div class="cam" id="cam">
        <div class="abs row3">{card3(1, "Etat", "szef · godziny · wypłata")}{card3(2, "Etat", "szef · godziny · wypłata")}{card3(3, '<span class="blue">?</span>', "&nbsp;")}</div>
      </div>""", f"""
      K.push(DUR, 1.035);
      ["#c1", "#c2", "#c3"].forEach((s, i) => K.lift(s, {r("trzy")} - 0.25 + i * 0.09, {{ y: 60, s: 0.94, dur: 0.6, ease: "expo.out" }}));
      tl.set(".stk2", {{ opacity: 0 }}, 0);
      const td = {r("dwie")};
      tl.to("#c3", {{ opacity: 0.35, duration: 0.3 }}, td);
      const te = {r("etaty")};
      ["#s1", "#s2"].forEach((s, i) => tl.to(s, {{ rotation: 16, y: 520, x: 60, opacity: 0, duration: 0.6, ease: "power2.in", transformOrigin: "0% 0%" }}, te - 0.2 + i * 0.1));
      const tn = {r("nakryił")};
      K.stamp("#t1", tn - 0.05, {{ from: 1.5, r0: -14, r1: -7 }}); K.stamp("#t2", tn + 0.1, {{ from: 1.5, r0: 10, r1: 5 }});""", """
      .row3 { left: 0; top: 0; width: 1920px; height: 1080px; display: flex; align-items: center; justify-content: center; gap: 48px; }
      .bc { position: relative; width: 480px; height: 600px; overflow: hidden; }
      .bc .no { position: absolute; left: 34px; top: 28px; font-size: 34px; font-weight: 700; color: var(--grey); }
      .und { position: absolute; inset: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 14px; }
      .und .uw { font-size: 150px; font-weight: 900; letter-spacing: -0.06em; }
      .und .us { font-size: 30px; font-weight: 500; color: var(--grey); }
      .stk { position: absolute; left: 30px; right: 30px; top: 170px; height: 260px; border-radius: 26px; background: #fff; box-shadow: 0 16px 40px rgba(0,0,0,0.12);
             display: flex; align-items: center; justify-content: center; font-size: 104px; font-weight: 900; letter-spacing: -0.05em; }
      .stk2 { position: absolute; left: 110px; top: 72px; padding: 14px 30px; border-radius: 14px; background: #fff; box-shadow: 0 10px 26px rgba(0,0,0,0.16);
              font-size: 54px; font-weight: 800; letter-spacing: -0.03em; }""")

# ================================================================ 4 · A+ 130 000+ produktów (wall)
a = W("sprzedałem", 22.5) - 0.3; b = W("i jako", 26.9) - 0.1; r = R(a)
sc("S04", a, b, "K", """
      <div class="wall">
        <div class="wl" id="l0">sprzedałem ponad</div>
        <div class="wb"><span id="n">0</span>+</div>
        <div class="wl" id="l1">produktów cyfrowych</div>
        <div class="wl" id="l2" style="margin-top:34px"><b style="font-weight:800">start:</b> 14 lat</div>
      </div>""", f"""
      K.rise("#l0", 0.02, {{ stagger: 0.04 }});
      K.lift(".wb", 0.05, {{ y: 30, dur: 0.5, ease: "expo.out" }});
      K.count("#n", 0, 130000, {r("130")} - 0.15, 1.0, K.pl, "power3.out");
      K.rise("#l1", {r("produktów")} - 0.15, {{ stagger: 0.05 }});
      K.rise("#l2", {r("14")} - 0.15, {{ stagger: 0.05 }});
      K.fadeOut(".wall", DUR - 0.3, {{ y: -16, dur: 0.28 }});""", WALL_CSS)

# ================================================================ 5 · B 15 lat → real photo at Times Square (Konrad's photo, review n46)
a = W("i jako", 26.9) - 0.1; b = W("i zanim", 32.8) - 0.06; r = R(a)
PIN = '<svg viewBox="0 0 48 64" width="30" height="40"><path d="M24 62 C24 62 4 36 4 22 A20 20 0 0 1 44 22 C44 36 24 62 24 62 Z" fill="#ff3b30"/><circle cx="24" cy="22" r="8" fill="#fff"/></svg>'
sc("S05", a, b, "B", f"""
      <div class="cam" id="cam">
        <div class="abs hd"><div class="h-xl" id="h1">15 lat.</div><div class="h-m w300" id="h2">jedyna osoba w Polsce</div>
          <div class="h-m" id="h3" style="margin-top:6px">na billboardzie</div><div class="tag" id="tag">{PIN}Times Square, Nowy Jork</div></div>
        <div class="abs ph" id="ph"><img id="phi" src="assets/times_square.jpg"></div>
      </div>""", f"""
      K.lift("#ph", 0.0, {{ y: 40, s: 0.96, dur: 0.6, ease: "expo.out" }});
      tl.fromTo("#phi", {{ scale: 1.14 }}, {{ scale: 1.0, duration: DUR, ease: "sine.out", immediateRender: true }}, 0);
      K.rise("#h1", {r("15")} - 0.25);
      K.rise("#h2", {r("jedyna")} - 0.1, {{ stagger: 0.05 }});
      const tb = {r("billboard")};
      K.rise("#h3", tb - 0.3, {{ stagger: 0.05 }});
      K.lift("#tag", tb + 0.15, {{ y: 14, s: 0.9, dur: 0.4, ease: "expo.out" }});
      tl.fromTo("#ph", {{ boxShadow: "0 30px 80px rgba(0,0,0,0.18)" }}, {{ boxShadow: "0 30px 80px rgba(0,0,0,0.18), 0 0 0 8px #0071e3", duration: 0.3, immediateRender: false }}, tb - 0.1);""", """
      .hd { left: 160px; top: 260px; }
      .ph { left: 1080px; top: 60px; width: 640px; height: 960px; border-radius: 36px; overflow: hidden; box-shadow: 0 30px 80px rgba(0,0,0,0.18); }
      .ph img { width: 100%; height: 100%; object-fit: cover; object-position: 50% 30%; transform-origin: 50% 25%; display: block; }
      .tag { display: inline-flex; align-items: center; gap: 14px; margin-top: 30px; padding: 16px 28px; border-radius: 999px; background: var(--ink); color: #fff; font-size: 40px; font-weight: 800; letter-spacing: -0.02em; white-space: nowrap; }""")

# ================================================================ 6 · K 3 models, hidden names + hidden cost
a = W("więc w tym", 37) - 0.1; b = W("potem powiem", 41.8) - 0.06; r = R(a)
sc("S06", a, b, "K", models_card(q=True), f"""
      K.card(DUR);
      K.rise("#mh", 0.1);
      K.lift(".mr", 0.12, {{ y: 14, dur: 0.45, stagger: 0.07 }});
      tl.to(".mr .n", {{ backgroundColor: "#0071e3", scale: 1.15, duration: 0.18, yoyo: true, repeat: 1, stagger: 0.1 }}, {r("trzy")} - 0.1);
      tl.set(".mr .q", {{ opacity: 0 }}, 0);
      K.lift(".mr .q", {r("kosztuje")} - 0.15, {{ y: 0, s: 0.8, dur: 0.3, stagger: 0.08 }});
      K.frame((T) => {{ [1, 2, 3].forEach((i) => {{ const f = Math.floor(T * 9) * 7 + i * 131; document.getElementById("mq" + i).textContent = String(1000 + (f * 7919) % 9000) + " zł"; }}); }});""",
   MODELS_CSS)

# ================================================================ 7 · B YouTube search → two kinds of videos
a = W("pisz sobie", 48.3) - 0.1; b = W("czyli jakiś", 54.5) - 0.06; r = R(a)
th1 = ["50 000 zł/mies. z AI", "Pasywny dochód w 7 dni", "AI zarabia za mnie"]
th2 = ["Naucz się kodować", "Załóż agencję AI", "100 maili dziennie"]
thumbs = lambda L, row: "".join(f'<div class="th" id="t{row}{i}"><span>{t}</span><i>{["18:42", "24:10", "31:05"][i]}</i></div>' for i, t in enumerate(L))
sc("S07", a, b, "B", f"""
      <div class="cam" id="cam">
        <div class="abs sb2" id="sb"><img src="assets/youtube.png"><span id="q"></span><b class="caret"></b></div>
        <div class="abs grid" id="g"><div class="rw2" id="r1"><div class="nb">1</div>{thumbs(th1, 1)}</div><div class="rw2" id="r2"><div class="nb">2</div>{thumbs(th2, 2)}</div></div>
      </div>""", f"""
      K.push(DUR, 1.03);
      K.lift("#sb", 0.0, {{ y: 30, s: 0.96, dur: 0.5, ease: "expo.out" }});
      tl.fromTo("#sb", {{ top: 400, scale: 1.25 }}, {{ top: 90, scale: 1, duration: 0.6, ease: "expo.inOut", immediateRender: true }}, {r("zobaczysz")} - 0.35);
      K.type("#q", {r("youtube")}, "", "biznes AI", 0.55);
      K.type("#q", {r("albo")} - 0.05, "biznes AI", "", 0.25);
      K.type("#q", {r("jak")} - 0.02, "", "jak zarabiać z AI", 0.7);
      tl.fromTo(".caret", {{ opacity: 1 }}, {{ opacity: 0, duration: 0.35, repeat: 12, yoyo: true, ease: "steps(1)" }}, 0);
      K.lift(".th", {r("zobaczysz")} - 0.1, {{ y: 30, s: 0.95, dur: 0.45, stagger: 0.05, ease: "expo.out" }});
      K.lift(".nb", {r("dwa rodzaje")}, {{ y: 0, s: 0.6, dur: 0.3, stagger: 0.12 }});
      tl.to("#r2", {{ y: 34, duration: 0.4, ease: "power3.out" }}, {r("dwa rodzaje")});
      tl.to("#r2", {{ opacity: 0.25, duration: 0.35 }}, {r("pierwszy rodzaj")});
      tl.to("#r1 .th", {{ scale: 1.04, duration: 0.3, stagger: 0.06, ease: "power2.out" }}, {r("obietnice")} - 0.1);
      tl.to("#r1 .th span", {{ color: "#0071e3", duration: 0.25, stagger: 0.06 }}, {r("obietnice")} - 0.1);""", """
      .sb2 { left: 360px; top: 90px; width: 1200px; height: 110px; border-radius: 999px; background: var(--fill); display: flex; align-items: center; gap: 26px; padding: 0 40px; font-size: 50px; font-weight: 600; letter-spacing: -0.02em; }
      .sb2 img { width: 62px; height: 62px; border-radius: 14px; }
      .caret { display: inline-block; width: 4px; height: 56px; background: var(--blue); margin-left: -20px; }
      .grid { left: 160px; top: 290px; display: flex; flex-direction: column; gap: 36px; }
      .rw2 { display: flex; align-items: center; gap: 36px; }
      .nb { width: 64px; height: 64px; border-radius: 50%; background: var(--ink); color: #fff; font-size: 32px; font-weight: 700; display: flex; align-items: center; justify-content: center; }
      .th { position: relative; width: 480px; height: 270px; border-radius: 24px; background: var(--fill); display: flex; align-items: center; padding: 0 36px; }
      .th span { font-size: 52px; font-weight: 900; letter-spacing: -0.045em; line-height: 1.02; }
      .th i { position: absolute; right: 16px; bottom: 14px; padding: 4px 10px; border-radius: 8px; background: rgba(0,0,0,0.78); color: #fff; font-size: 22px; font-weight: 600; font-style: normal; }""")

# ================================================================ 8 · B Settings: things you don't have (toggles refuse to switch on)
a = W("każdy ci", 61.5) - 0.1; b = W("weź", 68.9) - 0.05; r = R(a)
ICONS = {
    "code": '<path d="M24 18 L12 30 L24 42 M40 18 L52 30 L40 42" fill="none" stroke="#fff" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>',
    "term": '<path d="M14 20 L26 30 L14 40 M30 42 H48" fill="none" stroke="#fff" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>',
    "bolt": '<path d="M34 10 L18 34 H30 L26 52 L44 26 H32 Z" fill="#fff"/>',
    "mail": '<rect x="12" y="18" width="40" height="28" rx="5" fill="none" stroke="#fff" stroke-width="4.5"/><path d="M14 21 L32 34 L50 21" fill="none" stroke="#fff" stroke-width="4.5" stroke-linejoin="round"/>'}
rows8 = [("Kodowanie", "code", "#1d1d1f", "kodować"), ("Programowanie", "term", "#5e5ce6", "programować"),
         ("Agencja automatyzacji", "bolt", "#ff9500", "agencję"), ("100 maili dziennie", "mail", "#0071e3", "100")]
r8 = "".join(f'<div class="srow" id="w{i}"><div class="si" style="background:{c}"><svg viewBox="0 0 64 64">{ICONS[ic]}</svg></div>'
             f'<span>{n}</span><div class="tog" id="tg{i}"><div class="on"></div><div class="k"></div></div></div>' for i, (n, ic, c, _) in enumerate(rows8))
sc("S08", a, b, "B", f"""
      <div class="cam" id="cam">
        <div class="abs hd"><div class="h-l w300" id="h1" style="font-size:86px">Zanim zaczniesz,</div><div class="h-l" id="h2" style="font-size:86px">potrzebujesz…</div></div>
        <div class="abs set" id="set">{r8}</div>
      </div>""", f"""
      K.push(DUR, 1.03);
      K.rise("#h1", 0.05); K.rise("#h2", {r("rzeczy")} - 0.2);
      K.lift("#set", {r("kodować")} - 0.3, {{ y: 30, dur: 0.45, ease: "expo.out" }});
      {"".join(f'tl.fromTo("#w{i}", {{ height: 0, opacity: 0 }}, {{ height: 190, opacity: 1, duration: 0.35, ease: "power3.out", immediateRender: true }}, {r(w)} - 0.2); ' for i, (_, _, _, w) in enumerate(rows8))}
      // try to switch on → snaps back off + wrong-PIN shake (you don't have it)
      [[0, {r("kodować")} + 0.35], [2, {r("automatyzacji")} + 0.2], [3, {r("dziennie")} + 0.1]].forEach(([i, t]) => {{
        K.toggle("#tg" + i, t, true); K.toggle("#tg" + i, t + 0.3, false); K.shake("#w" + i, t + 0.3, 14);
        tl.to("#w" + i + " span", {{ color: "#ff3b30", duration: 0.15, yoyo: true, repeat: 1 }}, t + 0.3); }});""", """
      .hd { left: 110px; top: 150px; }
      .set { left: 840px; top: 150px; width: 1000px; border-radius: 32px; background: var(--fill); padding: 10px 0; }
      .srow { display: flex; align-items: center; gap: 30px; height: 190px; padding: 0 44px; border-bottom: 1px solid var(--line); overflow: hidden; }
      .srow:last-child { border-bottom: 0; }
      .srow .si { width: 96px; height: 96px; border-radius: 22px; display: flex; align-items: center; justify-content: center; flex: none; }
      .srow .si svg { width: 64px; height: 64px; }
      .srow span { flex: 1; font-size: 54px; font-weight: 700; letter-spacing: -0.03em; }
      .srow .tog { transform: scale(1.5); transform-origin: right center; }""")

# ================================================================ 8b · A+ każda rada wymaga (wall list)
a = W("umiejętności technicznej", 74.5) - 0.2; b = W("i powiem", 79.9) - 0.06; r = R(a)
sc("S08b", a, b, "K", """
      <div class="wall" style="top:170px">
        <div class="wl" id="l0" style="margin-bottom:22px">każda rada wymaga:</div>
        <div class="wi2" id="q1">umiejętności</div><div class="wi2" id="q2">klienta</div><div class="wi2" id="q3">pieniędzy na start</div><div class="wi2" id="q4">sprzedaży</div>
      </div>""", f"""
      K.rise("#l0", 0.0, {{ stagger: 0.03 }});
      [["#q1", {r("umiejętności")}], ["#q2", {r("klienta")}], ["#q3", {r("pieniędzy")}], ["#q4", {r("sprzedaży")}]].forEach(([s, t]) => K.rise(s, t - 0.12, {{ stagger: 0.04 }}));
      K.fadeOut(".wall", DUR - 0.3, {{ y: -16, dur: 0.28 }});""", WALL_CSS + """
      .wi2 { font-size: 66px; font-weight: 800; letter-spacing: -0.04em; line-height: 1.12; }""")

# ================================================================ 9 · B the „AI agency” wave in the US
a = W("tam fala", 81.3) - 0.1; b = W("zgadnij", 87) - 0.06; r = R(a)
X0, X1, Y0 = 220, 1700, 900
rise_d = f"M{X0},880 C 520,875 700,860 860,780 S 1080,430 1180,330"
fall_d = "M1180,330 C 1280,250 1330,520 1420,700 S 1600,860 1700,872"
sc("S09", a, b, "B", f"""
      <div class="cam" id="cam">
        <div class="abs hd"><div class="h-l" id="h1">„Załóż agencję AI”</div><div class="t-s grey" id="h2" style="font-size:38px;margin-top:10px">zainteresowanie · USA</div></div>
        <svg class="abs" style="left:0;top:0" width="1920" height="1080">
          <line x1="{X0}" y1="{Y0}" x2="{X1}" y2="{Y0}" stroke="#e5e5ea" stroke-width="3"/>
          <path id="ar" d="{rise_d} L1180,{Y0} L{X0},{Y0} Z" fill="rgba(0,113,227,0.10)"/>
          <path id="ln1" d="{rise_d}" fill="none" stroke="#0071e3" stroke-width="9" stroke-linecap="round"/>
          <path id="ln2" d="{fall_d}" fill="none" stroke="#ff3b30" stroke-width="9" stroke-linecap="round"/>
          <line id="mk" x1="1180" y1="330" x2="1180" y2="{Y0}" stroke="#1d1d1f" stroke-width="3" stroke-dasharray="8 10"/>
          <circle id="pk" cx="1180" cy="330" r="14" fill="#1d1d1f"/>
        </svg>
        <div class="abs pk2" id="pk2">2 lata temu</div>
        <div class="abs yrs"><span>2022</span><span>2023</span><span>2024</span><span>2025</span><span>2026</span></div>
        <div class="abs src">kształt poglądowy</div>
      </div>""", f"""
      K.push(DUR, 1.03);
      K.rise("#h1", 0.02); K.rise("#h2", 0.25, {{ stagger: 0.03 }});
      K.draw("#ln1", {r("fala")} - 0.1, 1.9, "power1.inOut");
      tl.fromTo("#ar", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.5, immediateRender: true }}, {r("wszyscy")} - 0.1);
      tl.fromTo("#pk", {{ scale: 0, transformOrigin: "50% 50%" }}, {{ scale: 1, duration: 0.3, ease: "back.out(3)", immediateRender: true }}, {r("2 lata")} - 0.1);
      K.draw("#mk", {r("2 lata")} - 0.05, 0.4);
      K.lift("#pk2", {r("2 lata")}, {{ y: 12, s: 0.9, dur: 0.35, ease: "expo.out" }});
      K.draw("#ln2", {r("skończyło")} - 0.2, 0.9, "power2.in");
      K.lift(".yrs span", 0.1, {{ y: 10, dur: 0.4, stagger: 0.05 }});""", """
      .hd { left: 160px; top: 100px; }
      .pk2 { left: 890px; top: 300px; padding: 12px 24px; border-radius: 999px; background: var(--ink); color: #fff; font-size: 36px; font-weight: 700; }
      .yrs { left: 220px; top: 922px; width: 1480px; display: flex; justify-content: space-between; font-size: 30px; font-weight: 500; color: var(--grey); }
      .src { right: 120px; bottom: 50px; font-size: 22px; color: var(--grey); }""")

# ================================================================ 10 · K same wave, Poland now
a = W("i polska", 89) - 0.1; b = W("i ja wolę", 94.3) - 0.06; r = R(a)
us_s = Shape("USA", 0, 0, 170, 110); pl_s = Shape("POL", 0, 0, 170, 130)
wave = "M0,92 C 60,90 90,84 120,66 S 170,10 200,8 C 222,6 236,50 256,76 S 290,92 310,92"
wave_up = "M0,92 C 60,90 90,84 120,66 S 170,10 200,8"
sc("S10", a, b, "K", f"""
      <div class="card ovc" style="width:700px">
        <div class="cr" id="u"><svg width="170" height="130" viewBox="0 0 170 130"><path d="{us_s.path()}" fill="#c7c7cc"/></svg>
          <div class="cw"><svg width="320" height="100" viewBox="0 0 320 100"><path d="{wave}" fill="none" stroke="#c7c7cc" stroke-width="7" stroke-linecap="round"/></svg><div class="cl">USA · 2 lata temu</div></div></div>
        <div class="sep"></div>
        <div class="cr" id="p"><svg width="170" height="130" viewBox="0 0 170 130"><path d="{pl_s.path()}" fill="#1d1d1f"/></svg>
          <div class="cw"><svg width="320" height="100" viewBox="0 0 320 100"><path id="wp" d="{wave_up}" fill="none" stroke="#0071e3" stroke-width="7" stroke-linecap="round"/></svg><div class="cl" style="color:var(--ink)">Polska · teraz</div></div></div>
        <div class="tr" id="tr">EN → PL</div>
      </div>""", f"""
      K.card(DUR);
      K.lift("#u", 0.15, {{ y: 14, dur: 0.45 }});
      K.lift("#p", {r("polska")} - 0.1, {{ y: 14, dur: 0.45 }});
      K.draw("#wp", {r("fala")} - 0.2, 1.3, "power1.inOut");
      K.lift("#tr", {r("przetłumaczone")} - 0.15, {{ y: 0, s: 0.8, dur: 0.35, ease: "back.out(2)" }});""", """
      .cr { display: flex; align-items: center; gap: 30px; padding: 22px 0; }
      .cw { display: flex; flex-direction: column; gap: 8px; }
      .cl { font-size: 40px; font-weight: 700; color: var(--grey); letter-spacing: -0.02em; }
      .tr { position: absolute; right: 44px; bottom: 40px; padding: 10px 22px; border-radius: 999px; background: var(--fill); font-size: 30px; font-weight: 700; }""")

# ================================================================ 11 · B THE QUESTION (pause button) ⭐
a = W("więc przejdziemy", 96.5) - 0.1; b = W("model pierwszy", 101.5) - 0.06; r = R(a)
sc("S11", a, b, "B", f"""
      <div class="cam" id="cam">
        <div class="abs nums"><div class="nn" id="n1">1</div><div class="nn" id="n2">2</div><div class="nn" id="n3">3</div></div>
        <div class="abs pb" id="pb"><div class="tap" id="tp" style="left:50%;top:50%"></div>{PAUSE}</div>
        <div class="abs qq"><div class="h-l w300" id="q1">Co się dzieje,</div><div class="h-l" id="q2">kiedy przestaniesz pracować?</div></div>
      </div>""", f"""
      K.push(DUR, 1.04);
      ["#n1", "#n2", "#n3"].forEach((s, i) => K.lift(s, 0.02 + i * 0.08, {{ y: 30, s: 0.8, dur: 0.45, ease: "expo.out" }}));
      tl.to(".nn", {{ backgroundColor: "#1d1d1f", color: "#fff", duration: 0.2, stagger: 0.1 }}, {r("3")} - 0.1);
      const tq = {r("samo")};
      tl.to("#n1", {{ x: 200, opacity: 0, scale: 0.6, duration: 0.45, ease: "power3.inOut" }}, tq);
      tl.to("#n3", {{ x: -200, opacity: 0, scale: 0.6, duration: 0.45, ease: "power3.inOut" }}, tq);
      tl.to("#n2", {{ opacity: 0, scale: 0.6, duration: 0.45, ease: "power3.inOut" }}, tq);
      K.lift("#pb", tq + 0.3, {{ y: 0, s: 0.6, dur: 0.5, ease: "expo.out" }});
      K.rise("#q1", {r("co się")} - 0.12, {{ stagger: 0.05 }});
      K.rise("#q2", {r("kiedy")} - 0.12, {{ stagger: 0.05 }});
      const tp = {r("przestaniesz")};
      tl.to("#pb", {{ scale: 0.88, duration: 0.09, yoyo: true, repeat: 1, ease: "power2.in" }}, tp); K.tap("#tp", tp);
      tl.to("#pb", {{ backgroundColor: "#0071e3", duration: 0.2 }}, tp + 0.05);""", """
      .nums { left: 0; top: 300px; width: 1920px; display: flex; justify-content: center; gap: 50px; }
      .nn { width: 220px; height: 220px; border-radius: 50%; background: var(--fill); font-size: 110px; font-weight: 800; display: flex; align-items: center; justify-content: center; }
      .pb { left: 840px; top: 170px; width: 240px; height: 240px; border-radius: 50%; background: var(--ink); display: flex; align-items: center; justify-content: center; }
      .pb svg { width: 140px; height: 140px; }
      .qq { left: 0; top: 520px; width: 1920px; text-align: center; }
      .qq .h-l { font-size: 124px; }""")

# ================================================================ 12 · K Model 1: Usługi (card callback)
a = W("model pierwszy", 101.5) - 0.02; b = W("i zasada", 107) - 0.06; r = R(a)
sc("S12", a, b, "K", models_card(extra='<div class="chips"><span id="c1">Agencja</span><span id="c2">Freelancing</span><span id="c3">AI Automation Agency</span></div>'), f"""
      K.card(DUR);
      tl.set("#mh", {{ opacity: 1 }}, 0);
      const tu = {r("usługi")};
      tl.to("#mt1", {{ filter: "blur(0px)", opacity: 1, color: "#0071e3", duration: 0.35, ease: "power2.out" }}, tu - 0.2);
      tl.to("#mn1", {{ backgroundColor: "#0071e3", scale: 1.12, duration: 0.25, yoyo: true, repeat: 1 }}, tu - 0.2);
      [["#c1", {r("agencją")}], ["#c2", {r("freelancingiem")}], ["#c3", {r("ai")}]].forEach(([s, t]) => K.lift(s, t - 0.1, {{ y: 10, s: 0.85, dur: 0.3, ease: "back.out(2)" }}));
      tl.to(".chips span", {{ backgroundColor: "#0071e3", color: "#fff", duration: 0.25, stagger: 0.05 }}, {r("jak zwał")});""",
   MODELS_CSS + """
      .chips { display: flex; flex-wrap: wrap; gap: 12px; margin-top: 22px; }
      .chips span { padding: 12px 22px; border-radius: 999px; background: var(--fill); font-size: 30px; font-weight: 700; }""")

# ================================================================ 13 · B pipeline: skill → client → monthly payment
a = W("uczysz", 107.8) - 0.12; b = W("i powiem uczciwie", 118) - 0.06; r = R(a)
skills = [("stron", "Strony"), ("czadłoty", "Chatboty"), ("automatyzację", "Automatyzacje"), ("montaż", "Montaż"), ("grafika", "Grafika"), ("cokolwiek", "Cokolwiek")]
sk = '<div class="sv grey" id="ki">…</div>' + "".join(f'<div class="sv" id="k{i}">{n}</div>' for i, (_, n) in enumerate(skills))
CAL = ('<svg viewBox="0 0 64 64" width="64" height="64"><rect x="8" y="12" width="48" height="44" rx="8" fill="none" stroke="#1d1d1f" stroke-width="4.5"/>'
       '<path d="M8 26 H56 M20 6 V16 M44 6 V16" stroke="#1d1d1f" stroke-width="4.5" stroke-linecap="round"/></svg>')
BLD = ('<svg viewBox="0 0 64 64" width="64" height="64"><rect x="14" y="8" width="36" height="50" rx="4" fill="none" stroke="#1d1d1f" stroke-width="4.5"/>'
       '<path d="M24 20 H28 M36 20 H40 M24 31 H28 M36 31 H40 M28 58 V46 H36 V58" stroke="#1d1d1f" stroke-width="4.5" stroke-linecap="round"/></svg>')
sc("S13", a, b, "B", f"""
      <div class="cam" id="cam">
        <svg class="abs" style="left:0;top:0" width="1920" height="1080">
          <path id="cv1" d="M630,540 C 665,540 665,540 700,540" fill="none" stroke="#1d1d1f" stroke-width="5" stroke-linecap="round"/>
          <path id="cv2" d="M1220,540 C 1255,540 1255,540 1290,540" fill="none" stroke="#1d1d1f" stroke-width="5" stroke-linecap="round"/>
        </svg>
        <div class="panel blk" id="b1" style="left:110px"><div class="lab">Umiejętność</div><div class="slot">{sk}</div></div>
        <div class="panel blk" id="b2" style="left:700px"><div class="lab">Klient</div><div class="row4">{BLD}<div class="bv">Firma</div></div></div>
        <div class="panel blk" id="b3" style="left:1290px;background:var(--ink);color:#fff"><div class="lab" style="color:#a1a1a6">Płaci</div><div class="bv">co miesiąc</div>
          <div class="mo"><i id="o1"></i><i id="o2"></i><i id="o3"></i><i id="o4"></i></div></div>
      </div>""", f"""
      K.push(DUR, 1.03);
      K.lift("#b1", 0.0, {{ y: 40, s: 0.95, dur: 0.55, ease: "expo.out" }});
      const T = [{", ".join(str(r(w)) for w, _ in skills)}];
      K.rise("#ki", 0.25, {{ dur: 0.35 }}); K.sink("#ki", T[0] - 0.14, {{ dur: 0.18 }});
      T.forEach((t, i) => {{ K.rise("#k" + i, t - 0.12, {{ dur: 0.35, stagger: 0 }}); if (i < T.length - 1) K.sink("#k" + i, T[i + 1] - 0.14, {{ dur: 0.18 }}); }});
      tl.to("#k5", {{ color: "#0071e3", duration: 0.2 }}, T[5]);
      K.draw("#cv1", {r("znajdujesz")} - 0.3, 0.4); K.lift("#b2", {r("znajdujesz")} - 0.05, {{ y: 40, s: 0.95, dur: 0.55, ease: "expo.out" }});
      K.draw("#cv2", {r("płaci")} - 0.45, 0.4); K.lift("#b3", {r("płaci")} - 0.2, {{ y: 40, s: 0.95, dur: 0.55, ease: "expo.out" }});
      const tm = {r("co miesiąc")};
      tl.fromTo("#b3 .mo i", {{ backgroundColor: "#3a3a3c" }}, {{ backgroundColor: "#34c759", duration: 0.12, stagger: 0.12, immediateRender: true }}, tm - 0.1);""", """
      .blk { position: absolute; top: 340px; width: 520px; height: 400px; padding: 40px 36px; display: flex; flex-direction: column; justify-content: space-between; }
      .slot { position: relative; height: 90px; }
      .blk .lab { font-size: 38px; }
      .sv { position: absolute; left: 0; top: 0; font-size: 60px; font-weight: 800; letter-spacing: -0.045em; white-space: nowrap; }
      .row4 { display: flex; align-items: center; gap: 22px; }
      .bv { font-size: 64px; font-weight: 800; letter-spacing: -0.045em; }
      .mo { display: flex; gap: 12px; } .mo i { width: 70px; height: 14px; border-radius: 7px; background: #3a3a3c; display: block; }""")

# ================================================================ 14 · B Contacts: you're replaceable ⭐
a = W("klienci", 137.2) - 0.12; b = W("i nie było", 144) - 0.06; r = R(a)
people = [("A", "Montażysta"), ("B", "Montażysta"), ("K", "Konrad (ja)"), ("C", "Montażysta"), ("D", "Montażysta")]
extra = [("E", "Montażysta"), ("F", "Montażysta"), ("G", "Montażysta")]
ct = "".join((f'<div class="swp" id="p{i}"><div class="delb">Usuń</div><div class="ctr me" id="p{i}c"><i>{l}</i><span>{n}</span></div><div class="ctr nw2" id="nw"><i>H</i><span>Montażysta</span><b>taniej</b></div></div>' if n.startswith("Konrad")
              else f'<div class="ctr" id="p{i}"><i>{l}</i><span>{n}</span></div>') for i, (l, n) in enumerate(people + extra))
sc("S14", a, b, "B", f"""
      <div class="cam" id="cam">
        <div class="abs hd"><div class="h-l w300" id="h1">Kolejny gość</div><div class="h-l" id="h2">od montażu.</div></div>
        <div class="abs cts"><div class="ch">Kontakty · montaż</div><div class="clip"><div class="lst" id="lst">{ct}</div></div></div>
      </div>""", f"""
      K.push(DUR, 1.03);
      K.lift(".cts", 0.0, {{ y: 40, dur: 0.55, ease: "expo.out" }});
      tl.set("#p5, #p6, #p7", {{ opacity: 0 }}, 0);
      const tr = {r("rzucali")};
      tl.to("#p2", {{ y: 2 * 118, duration: 0.5, ease: "power3.inOut" }}, tr - 0.2);
      tl.to("#p3, #p4", {{ y: -118, duration: 0.5, ease: "power3.inOut" }}, tr - 0.2);
      K.rise("#h1", {r("kolejnym")} - 0.15);
      K.rise("#h2", {r("montażu")} - 0.15);
      tl.to("#p2c", {{ backgroundColor: "#ffffff", duration: 0.3 }}, {r("kolejnym")}); tl.to("#p2c i", {{ backgroundColor: "#c7c7cc", duration: 0.3 }}, {r("kolejnym")});
      tl.to("#p5, #p6, #p7", {{ opacity: 1, duration: 0.3, stagger: 0.1 }}, {r("kolejnym")});
      tl.to("#lst", {{ y: -236, duration: 0.8, ease: "power2.inOut" }}, {r("kolejnym")});
      const tw = {r("wmienić")};
      tl.to("#p2c", {{ x: -230, duration: 0.35, ease: "power3.out" }}, tw - 0.2);
      const tt = {r("tańszego")};
      tl.to("#p2c", {{ x: -760, duration: 0.3, ease: "power3.in" }}, tt - 0.35);
      tl.fromTo("#nw", {{ x: 760 }}, {{ x: 0, duration: 0.45, ease: "expo.out", immediateRender: true }}, tt - 0.1);""", """
      .hd { left: 160px; top: 380px; }
      .cts { left: 1000px; top: 90px; width: 760px; height: 900px; border-radius: 32px; background: var(--fill); padding: 34px 30px; overflow: hidden; }
      .ch { font-size: 44px; font-weight: 800; letter-spacing: -0.03em; margin: 0 0 18px 10px; }
      .lst { position: relative; }
      .ctr { position: relative; height: 106px; margin-bottom: 12px; border-radius: 22px; background: #fff; display: flex; align-items: center; gap: 24px; padding: 0 26px; }
      .ctr i { width: 64px; height: 64px; border-radius: 50%; background: #c7c7cc; color: #fff; font-style: normal; font-size: 30px; font-weight: 700; display: flex; align-items: center; justify-content: center; }
      .ctr span { font-size: 40px; font-weight: 600; letter-spacing: -0.02em; }
      .ctr.me { background: #e8f1fd; } .ctr.me i { background: var(--blue); } .ctr.me span { font-weight: 800; }
      .clip { position: relative; height: 770px; overflow: hidden; }
      .nw2 { position: absolute !important; left: 0; right: 0; top: 0; margin: 0 !important; }
      .nw2 b { margin-left: auto; padding: 8px 18px; border-radius: 999px; background: var(--green); color: #fff; font-size: 28px; }
      .swp { position: relative; height: 106px; margin-bottom: 12px; border-radius: 22px; overflow: hidden; background: var(--red); }
      .swp .ctr { margin: 0; }
      .delb { position: absolute; right: 0; top: 0; width: 230px; height: 106px; color: #fff; font-size: 36px; font-weight: 700; display: flex; align-items: center; justify-content: center; }
      .del_unused { left: 1530px; top: 0; width: 230px; height: 106px; border-radius: 0 22px 22px 0; background: var(--red); color: #fff; font-size: 36px; font-weight: 700; display: flex; align-items: center; justify-content: center; }""")
# ================================================================ 15 · K koszt w tabelce
a = W("i nie było", 144) - 0.04; b = W("i mimo", 148.5) - 0.06; r = R(a)
tbl = [("Hosting", "89 zł"), ("Księgowość", "350 zł"), ("Montaż — Konrad", "1 200 zł"), ("Reklamy", "2 000 zł")]
tb = "".join(f'<div class="tr2" id="r{i}"><span>{n}</span><b>{v}</b></div>' for i, (n, v) in enumerate(tbl))
sc("S15", a, b, "K", f"""
      <div class="card ovc" style="width:680px"><div class="lab">październik</div><div class="h-m" style="margin:4px 0 16px">Koszty firmy</div>{tb}<div class="ex">przykład</div></div>""", f"""
      K.card(DUR);
      K.lift(".tr2", 0.2, {{ y: 12, dur: 0.35, stagger: 0.08 }});
      const tk = {r("kosztem")};
      tl.to("#r2", {{ backgroundColor: "rgba(255,59,48,0.12)", duration: 0.3 }}, tk - 0.1);
      tl.to("#r2 b, #r2 span", {{ color: "#ff3b30", duration: 0.3 }}, tk - 0.1);
      tl.fromTo("#r2", {{ boxShadow: "inset 0 0 0 0px #ff3b30" }}, {{ boxShadow: "inset 0 0 0 4px #ff3b30", duration: 0.25, immediateRender: false }}, {r("tabelce")} - 0.1);""", """
      .tr2 { display: flex; justify-content: space-between; align-items: center; padding: 18px 16px; border-top: 1px solid var(--line); border-radius: 12px; font-size: 38px; }
      .tr2 span { font-weight: 600; } .tr2 b { font-weight: 800; }
      .ex { margin-top: 12px; font-size: 22px; color: var(--grey); text-align: right; }""")

# ================================================================ 16 · A+ tańszy o 5 zł (wall)
a = W("bo wiadomo", 152.6) - 0.1; b = W("i to nie tak", 155) - 0.06; r = R(a)
sc("S16", a, b, "K", """
      <div class="wall" style="top:230px">
        <div class="wl" id="l0" style="font-size:62px">zawsze ktoś tańszy</div>
        <div class="pill5" id="p5">−5 zł</div>
      </div>""", f"""
      K.rise("#l0", {r("zawsze")} - 0.15, {{ stagger: 0.04 }});
      K.stamp("#p5", {r("5")} - 0.2, {{ from: 1.4 }});
      K.fadeOut(".wall", DUR - 0.28, {{ y: -16, dur: 0.26 }});""", WALL_CSS + """
      .pill5 { display: inline-block; margin-top: 18px; padding: 10px 36px 16px; border-radius: 999px; background: var(--red); color: #fff; font-size: 150px; font-weight: 900; letter-spacing: -0.05em; }""")

# ================================================================ 17 · B client = new boss, Saturday 21:47 ⭐
a = W("każdy klient", 159.5) - 0.12; b = W("i w polsce", 167.2) - 0.06; r = R(a)
notis = [("Klient A", "tylko mała poprawka", "pisze"), ("Klient B", "da się na jutro rano?", "wieczorem"),
         ("Klient A", "jeszcze jedna mała poprawka", "poprawka"), ("Klient C", "termin: poniedziałek 8:00", "terminów")]
nh = "".join(f'<div class="noti" id="n{i}" style="top:{560 - i * 0}px"><img src="assets/wa.png"><div><b>{c}</b><span>{m}</span></div><em>teraz</em></div>' for i, (c, m, _) in enumerate(notis))
sc("S17", a, b, "B", f"""
      <div class="cam" id="cam">
        <div class="abs hd"><div class="h-l w300" id="h1">Każdy klient</div><div class="h-xl" id="h2">= nowy szef.</div></div>
        <div class="phone" style="left:1250px;top:90px"><div class="scr" style="background:#eceef3">
          <div class="di"></div>
          <div class="ls"><div class="dt" id="dt">sobota, 10 października</div><div class="tm">21:47</div></div>
          <div class="stack" id="st">{nh}</div>
        </div></div>
      </div>""", f"""
      K.push(DUR, 1.035);
      K.rise("#h1", 0.05); K.rise("#h2", {r("nowy szef")} - 0.15);
      tl.to("#dt", {{ color: "#0071e3", duration: 0.2 }}, {r("sobotę")} - 0.1);
      const T = [{", ".join(str(r(w)) for *_, w in notis)}];
      T.forEach((t, i) => {{
        tl.fromTo("#n" + i, {{ y: -80, opacity: 0, scale: 0.94 }}, {{ y: 0, opacity: 1, scale: 1, duration: 0.45, ease: "expo.out", immediateRender: true }}, t - 0.12);
        for (let j = 0; j < i; j++) tl.to("#n" + j, {{ y: "+=118", duration: 0.45, ease: "expo.out" }}, t - 0.12);
      }});""", """
      .hd { left: 160px; top: 330px; }
      .ls { position: absolute; left: 0; right: 0; top: 96px; text-align: center; }
      .ls .dt { font-size: 24px; font-weight: 600; color: #3a3a3c; }
      .ls .tm { font-size: 112px; font-weight: 700; letter-spacing: -0.04em; line-height: 1; color: #1d1d1f; }
      .stack { position: absolute; left: 0; right: 0; top: 0; }
      .noti { top: 300px !important; height: 100px; }
      .noti b { font-size: 25px; } .noti span { font-size: 23px; }
      .noti em { position: absolute; right: 20px; top: 16px; font-style: normal; font-size: 18px; color: var(--grey); }""")

# ================================================================ 18 · B invoice: 30 → 60 → 90 days
a = W("faktura", 169.6) - 0.12; b = W("a potem", 175.8) - 0.06; r = R(a)
sc("S18", a, b, "B", """
      <div class="cam" id="cam">
        <div class="card inv" id="inv">
          <div class="ih"><div><div class="lab">Faktura VAT</div><div class="h-m">FV 10/2026</div></div><div class="stt" id="stt"><i class="sp"></i><span id="sx">Oczekuje</span></div></div>
          <div class="sep" style="margin:30px 0"></div>
          <div class="lab" id="tl">Termin płatności</div>
          <div class="days"><span id="d">30</span> <span class="w300">dni</span></div>
          <div class="tlx"><div class="fl" id="fl"></div><span style="left:33.3%">30</span><span style="left:66.6%">60</span><span style="left:100%">90</span></div>
        </div>
      </div>""", f"""
      K.push(DUR, 1.035);
      K.lift("#inv", 0.0, {{ y: 50, s: 0.96, dur: 0.6, ease: "expo.out" }});
      const t30 = {r("30")}, t60 = {r("60")}, t90 = {r("90")};
      K.count("#d", 30, 30, 0, 0.01, (v) => String(Math.round(v)));
      K.count("#d", 30, 60, t60 - 0.15, 0.35, (v) => String(Math.round(v)), "power2.out");
      K.count("#d", 60, 90, t90 - 0.15, 0.35, (v) => String(Math.round(v)), "power2.out");
      K.count("#d", 90, 117, {r("dalej")} - 0.2, 1.4, (v) => String(Math.round(v)), "power1.inOut");
      tl.fromTo("#fl", {{ scaleX: 0 }}, {{ scaleX: 0.333, duration: 0.4, ease: "power2.out", immediateRender: true }}, t30 - 0.1);
      tl.to("#fl", {{ scaleX: 0.666, backgroundColor: "#ff9500", duration: 0.4, ease: "power2.out" }}, t60 - 0.1);
      tl.to("#fl", {{ scaleX: 1, backgroundColor: "#ff3b30", duration: 0.4, ease: "power2.out" }}, t90 - 0.1);
      tl.to("#stt", {{ backgroundColor: "#fff4e5", color: "#c26a00", duration: 0.3 }}, t60 - 0.1);
      tl.to("#stt", {{ backgroundColor: "#ffecea", color: "#ff3b30", duration: 0.3 }}, t90 - 0.1);
      tl.to(".days", {{ color: "#ff3b30", duration: 0.3 }}, t90 - 0.1);
      const tc = {r("dalej")} - 0.25;
      K.frame((T) => {{ document.getElementById("sx").textContent = T >= t90 - 0.1 ? "Po terminie" : "Oczekuje";
        document.getElementById("tl").textContent = T >= tc ? "Czekasz już" : "Termin płatności"; }});
      tl.fromTo(".sp", {{ rotation: 0 }}, {{ rotation: 360 * 8, duration: DUR, ease: "none", immediateRender: true }}, 0);""", """
      .inv { left: 460px; top: 120px; width: 1000px; padding: 56px 64px; }
      .ih { display: flex; justify-content: space-between; align-items: flex-start; }
      .stt { display: flex; align-items: center; gap: 14px; padding: 14px 26px; border-radius: 999px; background: var(--fill); color: #3a3a3c; font-size: 32px; font-weight: 700; }
      .sp { width: 28px; height: 28px; border-radius: 50%; border: 4px solid currentColor; border-right-color: transparent; display: block; }
      .days { font-size: 200px; font-weight: 900; letter-spacing: -0.065em; line-height: 1; margin: 10px 0 36px; }
      .days .w300 { font-size: 90px; letter-spacing: -0.03em; }
      .tlx { position: relative; height: 16px; border-radius: 8px; background: var(--fill); }
      .tlx .fl { position: absolute; inset: 0; border-radius: 8px; background: var(--ink); transform-origin: left center; transform: scaleX(0); }
      .tlx span { position: absolute; top: 28px; transform: translateX(-50%); font-size: 26px; color: var(--grey); font-weight: 600; }""")

# ================================================================ 19 · K cięcie kosztów: podwykonawcy (Ty) first
a = W("a potem", 175.8) - 0.04; b = W("ludzie sprzedają", 181.8) + 0.45; r = R(a)
sc("S19", a, b, "K", """
      <div class="card ovc" style="width:680px"><div class="lab">Słaby miesiąc w firmie</div><div class="h-m" style="margin:4px 0 16px">Tniemy koszty</div>
        <div class="cc" id="c0"><span id="c0t">Podwykonawcy</span><b class="ty" id="ty">= Ty</b></div><div class="cc" id="c1"><span>Nowy sprzęt</span></div><div class="cc" id="c2"><span>Szkolenia</span></div></div>""", f"""
      K.card(DUR);
      K.lift(".cc", 0.25, {{ y: 12, dur: 0.35, stagger: 0.08 }});
      tl.fromTo(".cc", {{ backgroundColor: "rgba(0,0,0,0)" }}, {{ backgroundColor: "#f5f5f7", duration: 0.2, stagger: 0.1, yoyo: true, repeat: 1, immediateRender: false }}, {r("koszty")} - 0.1);
      K.strike("#c0t", {r("cnie", a + 3.5)} - 0.05);
      tl.to("#c0", {{ backgroundColor: "rgba(255,59,48,0.08)", duration: 0.3 }}, {r("pierwsze")});
      K.stamp("#ty", {r("ciebie")} - 0.2, {{ from: 1.5 }});""", """
      .cc { display: flex; align-items: center; justify-content: space-between; padding: 20px 16px; border-top: 1px solid var(--line); border-radius: 12px; font-size: 40px; font-weight: 600; letter-spacing: -0.02em; }
      .ty { padding: 6px 20px; border-radius: 999px; background: var(--red); color: #fff; font-size: 34px; font-weight: 800; }""")

# ================================================================ 20 · K przychód cykliczny = nadzieja
a = W("jako przychód", 182.8) - 0.1; b = W("i w dodatku", 191) - 0.06; r = R(a)
mons = ["paź", "lis", "gru", "sty"]
mh = "".join(f'<div class="mo2" id="o{i}"><div class="mn">{m}</div><div class="mv"><div class="ok">{CHECK}</div><div class="qm">?</div></div></div>' for i, m in enumerate(mons))
sc("S20", a, b, "K", f"""
      <div class="card ovc" style="width:680px">
        <div class="ttl"><div class="h-m" id="t1">Przychód cykliczny</div><div class="h-m blue" id="t2">Nadzieja.</div></div>
        <div class="mos">{mh}</div>
      </div>""", f"""
      K.card(DUR);
      K.rise("#t1", 0.1);
      tl.set("#t2", {{ opacity: 0 }}, 0);
      K.lift(".mo2", 0.25, {{ y: 14, dur: 0.4, stagger: 0.06 }});
      tl.set(".mo2 .qm", {{ opacity: 0 }}, 0); tl.set(".mo2 .ok", {{ opacity: 0 }}, 0);
      tl.to("#o0 .ok", {{ opacity: 1, duration: 0.2 }}, {r("płaci")} - 0.1); tl.to("#o0", {{ backgroundColor: "#34c759", duration: 0.2 }}, {r("płaci")} - 0.1);
      const tb = {r("piękna")};
      tl.to("#o1 .ok, #o2 .ok, #o3 .ok", {{ opacity: 1, duration: 0.15, stagger: 0.08 }}, tb - 0.1);
      tl.to("#o1, #o2, #o3", {{ backgroundColor: "#34c759", duration: 0.15, stagger: 0.08 }}, tb - 0.1);
      const tn = {r("nie jest")};
      tl.to("#o1 .ok, #o2 .ok, #o3 .ok", {{ opacity: 0, duration: 0.15, stagger: 0.08 }}, tn);
      tl.to("#o1, #o2, #o3", {{ backgroundColor: "#ffffff", boxShadow: "inset 0 0 0 3px #c7c7cc", duration: 0.2, stagger: 0.08 }}, tn);
      tl.to("#o1 .qm, #o2 .qm, #o3 .qm", {{ opacity: 1, duration: 0.2, stagger: 0.08 }}, tn + 0.05);
      const th = {r("nadzieja")};
      K.strike("#t1", th - 0.2);
      tl.to("#t1", {{ y: -12, scale: 0.8, transformOrigin: "left center", duration: 0.35 }}, th - 0.05);
      tl.fromTo("#t2", {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.4, ease: "expo.out", immediateRender: false }}, th - 0.05);
      tl.fromTo("#o1", {{ scale: 1 }}, {{ scale: 1.08, duration: 0.25, yoyo: true, repeat: 1 }}, {r("przyszłym")});""", """
      .ttl { position: relative; height: 150px; }
      #t2 { position: absolute; left: 0; top: 70px; font-size: 76px; font-weight: 900; }
      .mos { display: flex; gap: 16px; margin-top: 16px; }
      .mo2 { width: 136px; height: 160px; border-radius: 22px; background: var(--fill); display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 10px; }
      .mo2 .mn { font-size: 30px; font-weight: 700; color: #3a3a3c; }
      .mv { position: relative; width: 60px; height: 60px; }
      .mv .ok, .mv .qm { position: absolute; inset: 0; display: flex; align-items: center; justify-content: center; }
      .mv .ok svg { width: 44px; height: 40px; }
      .mv .qm { font-size: 56px; font-weight: 800; color: var(--grey); }""")

# ================================================================ 21 · B ceiling: 15 h / week, 2× money = 2× hours
a = W("i w dodatku", 191) - 0.06; b = W("a w dniu", 198) - 0.06; r = R(a)
BASE, CEIL = 940, 520
sc("S21", a, b, "B", f"""
      <div class="cam" id="cam">
        <div class="abs hd"><div class="h-l" id="h1">Sufit.</div><div class="h-m w300" id="h2" style="margin-top:8px">15 wolnych godzin w tygodniu</div></div>
        <div class="abs ceil" id="ce"><span>sufit</span></div>
        <div class="abs bar" id="bh" style="left:820px"><div class="bf" id="bhf"></div><div class="bl">Godziny</div><div class="bt" id="bht">15 h</div></div>
        <div class="abs bar" id="bm" style="left:1220px"><div class="bf blue" id="bmf"></div><div class="bl">Zarobki</div><div class="bt" id="bmt">×1</div></div>
        <div class="abs link" id="lk"></div>
      </div>""", f"""
      K.push(DUR, 1.03);
      K.rise("#h1", 0.05);
      tl.fromTo("#ce", {{ y: -500, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.45, ease: "power4.in", immediateRender: true }}, {r("sufit")} - 0.35);
      tl.to("#cam", {{ y: 6, duration: 0.06, yoyo: true, repeat: 1 }}, {r("sufit")} + 0.1);
      K.rise("#h2", {r("15")} - 0.15, {{ stagger: 0.04 }});
      tl.set(".bar", {{ opacity: 1 }}, 0);
      tl.fromTo("#bhf, #bmf", {{ height: 0 }}, {{ height: 250, duration: 0.7, ease: "power3.out", immediateRender: true }}, {r("15")} - 0.05);
      K.lift(".bt, .bl", {r("15")}, {{ y: 10, dur: 0.3 }});
      const t2 = {r("dwa razy")};
      tl.to("#bmf", {{ height: 500, duration: 0.6, ease: "power3.inOut" }}, t2 - 0.1);
      K.count("#bmt", 1, 2, t2 - 0.1, 0.5, (v) => "×" + Math.round(v));
      const t3 = {r("pracować", a + 5.5)};
      tl.to("#bhf", {{ height: 500, backgroundColor: "#ff3b30", duration: 0.6, ease: "power3.inOut" }}, t3 - 0.15);
      K.count("#bht", 15, 30, t3 - 0.15, 0.6, (v) => Math.round(v) + " h");
      tl.to("#bht", {{ color: "#ff3b30", duration: 0.2 }}, t3);
      K.shake("#bh", t3 + 0.45, 12); tl.to("#ce", {{ backgroundColor: "#ff3b30", duration: 0.2 }}, t3 + 0.45);""", f"""
      .hd {{ left: 160px; top: 110px; }}
      .ceil {{ left: 720px; top: {BASE - 290}px; width: 880px; height: 6px; border-radius: 3px; background: #1d1d1f; }}
      .ceil span {{ position: absolute; right: 0; top: -54px; font-size: 34px; font-weight: 700; }}
      .bar {{ top: 0; width: 280px; height: {BASE}px; opacity: 0; }}
      .bf {{ position: absolute; left: 0; right: 0; bottom: 0; height: 0; border-radius: 20px 20px 6px 6px; background: var(--ink); }}
      .bf.blue {{ background: var(--blue); }}
      .bl {{ position: absolute; left: 0; top: {BASE + 14}px; font-size: 36px; font-weight: 700; }}
      .bt {{ position: absolute; right: -10px; top: {BASE + 12}px; font-size: 40px; font-weight: 900; letter-spacing: -0.03em; }}""")

# ================================================================ 22 · B the question again → everything stops → Etat × szefowie ⭐
a = W("więc odpowiedz", 200.8) - 0.1; b = W("i okej", 209.5) - 0.06; r = R(a)
pts = []
import math
for i in range(0, 61):
    x = 160 + i * 26.7
    y = 960 - (i * 3.2 + 26 * math.sin(i * 0.9) + 40)
    pts.append(f"{x:.0f},{y:.0f}")
line = "M" + " L".join(pts)
BOSS = '<svg viewBox="0 0 80 80" width="96" height="96"><circle cx="40" cy="40" r="40" fill="#c7c7cc"/><circle cx="40" cy="32" r="13" fill="#fff"/><path d="M16 66 C20 50 60 50 64 66" fill="#fff"/></svg>'
sc("S22", a, b, "B", f"""
      <div class="cam" id="cam">
        <div class="abs pb" id="pb"><div class="tap" id="tp" style="left:50%;top:50%"></div>{PAUSE}</div>
        <div class="abs qq" id="qq"><div class="h-l w300" id="q1">Co się dzieje,</div><div class="h-l" id="q2">kiedy przestajesz pracować?</div></div>
        <svg class="abs" style="left:0;top:0" width="1920" height="1080"><path id="rv" d="{line}" fill="none" stroke="#34c759" stroke-width="8" stroke-linejoin="round" stroke-linecap="round"/>
          <line id="flat" x1="160" y1="958" x2="1760" y2="958" stroke="#ff3b30" stroke-width="8" stroke-linecap="round"/></svg>
        <div class="abs zero" id="z0">0 zł</div>
        <div class="abs et" id="et"><div class="h-l w300" id="e1">To nie biznes.</div><div class="h-xl" id="e2">To etat.</div>
          <div class="bs" id="bs"><div class="bb" id="b1">{BOSS}</div><div class="bb" id="b2">{BOSS}</div><div class="bb" id="b3">{BOSS}</div><span id="bx">× szefów</span></div></div>
      </div>""", f"""
      K.push(DUR, 1.03);
      K.lift("#pb", 0.02, {{ y: 0, s: 0.7, dur: 0.45, ease: "expo.out" }});
      K.draw("#rv", 0.0, 2.0, "none");
      K.rise("#q1", {r("pytanie")} - 0.2, {{ stagger: 0.05 }}); K.rise("#q2", {r("kiedy", a + 1.5)} - 0.12, {{ stagger: 0.05 }});
      const tp = {r("przestajesz")};
      tl.to("#pb", {{ scale: 0.88, duration: 0.09, yoyo: true, repeat: 1, ease: "power2.in" }}, tp); K.tap("#tp", tp);
      tl.to("#pb", {{ backgroundColor: "#ff3b30", duration: 0.2 }}, tp + 0.05);
      const ts = {r("wszystko staje")};
      tl.to("#rv", {{ opacity: 0, duration: 0.25 }}, ts - 0.1);
      tl.set("#flat", {{ opacity: 0 }}, 0); tl.to("#flat", {{ opacity: 1, duration: 0.15 }}, ts - 0.1);
      K.stamp("#z0", ts - 0.05, {{ from: 1.5 }});
      const tb = {r("nie jest biznes")};
      K.sink("#q1", tb - 0.4, {{ dur: 0.3 }}); K.sink("#q2", tb - 0.4, {{ dur: 0.3 }});
      tl.to("#pb, #z0, #flat", {{ opacity: 0, duration: 0.3 }}, tb - 0.35);
      K.rise("#e1", tb - 0.15, {{ stagger: 0.05 }});
      K.rise("#e2", {r("etat")} - 0.15, {{ stagger: 0.06 }});
      tl.set("#bs .bb, #bx", {{ opacity: 0 }}, 0);
      const tk = {r("kilkoma")};
      ["#b1", "#b2", "#b3"].forEach((s, i) => K.lift(s, tk - 0.1 + i * 0.12, {{ y: 20, s: 0.7, dur: 0.35, ease: "back.out(2)" }}));
      K.lift("#bx", {r("szefami")} - 0.1, {{ y: 10, dur: 0.3 }});""", """
      .pb { left: 860px; top: 120px; width: 200px; height: 200px; border-radius: 50%; background: var(--ink); display: flex; align-items: center; justify-content: center; }
      .pb svg { width: 120px; height: 120px; }
      .qq { left: 0; top: 400px; width: 1920px; text-align: center; }
      .zero { left: 1600px; top: 860px; font-size: 64px; font-weight: 900; color: var(--red); letter-spacing: -0.04em; }
      .et { left: 0; top: 250px; width: 1920px; text-align: center; }
      .bs { display: flex; justify-content: center; align-items: center; gap: 18px; margin-top: 40px; }
      .bs span { font-size: 48px; font-weight: 700; color: var(--grey); margin-left: 12px; }""")

# ================================================================ 23 · K Model 2: Software (card callback + monthly/yearly)
a = W("model drugi", 217.3) - 0.1; b = W("muszę", 222.4) + 0.4; r = R(a)
sc("S23", a, b, "K", models_card(done=(1,), extra='<div class="seg" id="seg"><i id="hl"></i><span id="sm">Miesięcznie</span><span id="sy">Rocznie</span></div>'), f"""
      K.card(DUR);
      const tu = {r("drugi")};
      tl.to("#mt2", {{ filter: "blur(0px)", opacity: 1, color: "#0071e3", duration: 0.35, ease: "power2.out" }}, tu - 0.2);
      tl.to("#mn2", {{ backgroundColor: "#0071e3", scale: 1.12, duration: 0.25, yoyo: true, repeat: 1 }}, tu - 0.2);
      tl.set("#mn1", {{ backgroundColor: "#c7c7cc" }}, 0);
      K.lift("#seg", {r("dostęp")} - 0.2, {{ y: 14, dur: 0.4 }});
      tl.fromTo("#hl", {{ scale: 0.6, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.3, ease: "back.out(2)", immediateRender: true }}, {r("co miesiąc")} - 0.1);
      tl.to("#hl", {{ x: 300, duration: 0.35, ease: "power3.inOut" }}, {r("rok")} - 0.2);""", MODELS_CSS + """
      .seg { position: relative; display: flex; margin-top: 26px; width: 600px; height: 76px; border-radius: 20px; background: var(--fill); padding: 6px; }
      .seg i { position: absolute; left: 6px; top: 6px; width: 294px; height: 64px; border-radius: 15px; background: #fff; box-shadow: 0 3px 10px rgba(0,0,0,0.12); }
      .seg span { position: relative; flex: 1; display: flex; align-items: center; justify-content: center; font-size: 30px; font-weight: 700; }""")

# ================================================================ 23b · K MRR (right wall, small chart)
a = W("masz ten", 228.4) - 0.1; b = W("i zbudowanie", 230.9) - 0.06; r = R(a)
sc("S23b", a, b, "K", """
      <div class="card" id="mrr" style="left:1290px;top:150px;width:500px;padding:36px 40px">
        <div class="h-l" style="font-size:96px">MRR</div><div class="t-xs" id="mt" style="font-size:26px">Monthly Recurring Revenue</div>
        <svg width="420" height="170" viewBox="0 0 420 170" style="margin-top:14px"><path id="mc" d="M6,160 C 90,150 140,130 200,100 S 320,30 414,14" fill="none" stroke="#34c759" stroke-width="8" stroke-linecap="round"/></svg>
      </div>""", f"""
      K.tl.fromTo("#mrr", {{ opacity: 0, y: 24, scale: 0.97 }}, {{ opacity: 1, y: 0, scale: 1, duration: 0.5, ease: "expo.out", immediateRender: true }}, 0.03);
      K.tl.to("#mrr", {{ opacity: 0, y: 10, duration: 0.26, ease: "power2.in" }}, DUR - 0.28);
      K.draw("#mc", 0.2, 1.4, "power2.out");
      K.rise("#mt", {r("monthly")} - 0.15, {{ stagger: 0.04 }});""")

# ================================================================ 24 · K „terminal” advice (dark card, typed)
a = W("czyli odpusz", 243.3) - 0.12; b = W("mam znajomego", 247.8) - 0.06; r = R(a)
lines = [("odpal terminal", "odpusz"), ("naucz się kodować z AI", "nałóż"), ("postaw aplikację", "postaw"), ("zgarnij miliony z fundingu", "zgarnij")]
lh = "".join(f'<div class="cl2"><b>›</b><span id="y{i}"></span></div>' for i in range(len(lines)))
sc("S24", a, b, "K", f"""
      <div class="card ovc dk" style="width:700px"><div class="lab" style="color:#8e8e93;margin-bottom:12px">rady z YouTube'a</div>{lh}</div>""", f"""
      K.card(DUR);
      {"".join(f'K.type("#y{i}", {r(w)} - 0.1, "", "{t}", {min(0.55, len(t) * 0.035):.2f}); ' for i, (t, w) in enumerate(lines))}
      tl.set(".cl2", {{ opacity: 0 }}, 0);
      {"".join(f'tl.to(".cl2:nth-of-type({i + 2})", {{ opacity: 1, duration: 0.05 }}, {r(w)} - 0.12); ' for i, (t, w) in enumerate(lines))}
      tl.to("#y3", {{ color: "#4da3ff", fontWeight: 900, duration: 0.15 }}, {r("miliony")} - 0.05);
      tl.fromTo("#y3", {{ scale: 1 }}, {{ scale: 1.06, transformOrigin: "left center", duration: 0.16, yoyo: true, repeat: 1, immediateRender: false }}, {r("miliony")} - 0.05);""", """
      .dk { background: #1d1d1f; color: #fff; }
      .cl2 { display: flex; gap: 18px; font-size: 44px; font-weight: 600; letter-spacing: -0.02em; padding: 10px 0; min-height: 76px; }
      .cl2 b { color: #8e8e93; font-weight: 400; }
      .cl2 span { display: inline-block; }""")

# ================================================================ 25 · B 11 apps in 4 years, only the last one works ⭐
a = W("mam znajomego", 247.8) - 0.06; b = W("robi teraz", 256) - 0.06; r = R(a)
GL = ['<circle cx="32" cy="32" r="16" fill="#fff"/>', '<rect x="16" y="16" width="32" height="32" rx="6" fill="#fff"/>',
      '<path d="M32 12 L52 50 H12 Z" fill="#fff"/>', '<path d="M14 46 V30 M26 46 V18 M38 46 V26 M50 46 V12" stroke="#fff" stroke-width="7" stroke-linecap="round"/>',
      '<path d="M32 10 L38 26 L54 26 L41 36 L46 52 L32 42 L18 52 L23 36 L10 26 L26 26 Z" fill="#fff"/>', '<path d="M12 32 H52 M32 12 V52" stroke="#fff" stroke-width="8" stroke-linecap="round"/>',
      '<circle cx="32" cy="32" r="18" fill="none" stroke="#fff" stroke-width="7"/>', '<path d="M14 40 L26 26 L36 36 L50 18" fill="none" stroke="#fff" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>',
      '<rect x="12" y="20" width="40" height="26" rx="6" fill="none" stroke="#fff" stroke-width="6"/>', '<path d="M20 14 H44 V50 L32 40 L20 50 Z" fill="#fff"/>',
      '<path d="M32 12 C 44 24 44 40 32 52 C 20 40 20 24 32 12 Z" fill="#fff"/>']
OKB = '<div class="okb" id="okb">' + CHECK + '</div>'
apps = "".join(f'<div class="ap2" id="a{i}"><svg viewBox="0 0 64 64">{g}</svg>{OKB if i == 10 else ""}</div>' for i, g in enumerate(GL))
yrs = "".join(f'<span id="y{i}">{y}</span>' for i, y in enumerate([2022, 2023, 2024, 2025]))
sc("S25", a, b, "B", f"""
      <div class="cam" id="cam">
        <div class="abs hd"><div class="lab" style="font-size:36px">Znajomy, software</div><div class="cnt"><span id="n">0</span><span class="w300 u" id="u">aplikacji</span></div>
          <div class="yrs2">{yrs}</div></div>
        <div class="abs home" id="home">{apps}</div>
      </div>""", f"""
      K.push(DUR, 1.035);
      K.lift(".hd .lab", 0.05, {{ y: 14, dur: 0.4 }}); K.lift(".cnt", 0.1, {{ y: 24, dur: 0.5, ease: "expo.out" }});
      const t4 = {round(249.64 - a, 2)};
      K.lift(".yrs2 span", t4 - 0.15, {{ y: 10, dur: 0.3, stagger: 0.12 }});
      const t0 = t4 + 0.2, t11 = {round(251.40 - a, 2)};
      for (let i = 0; i < 11; i++) {{ const t = t0 + (t11 - t0) * i / 10; tl.fromTo("#a" + i, {{ scale: 0, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.3, ease: "back.out(2.2)", immediateRender: true }}, t); }}
      K.count("#n", 0, 11, t0, t11 - t0 + 0.1, (v) => String(Math.round(v)), "none");
      tl.fromTo("#u", {{ opacity: 0, x: -20 }}, {{ opacity: 1, x: 0, duration: 0.35, ease: "expo.out", immediateRender: true }}, t11);
      tl.fromTo(".cnt", {{ scale: 1 }}, {{ scale: 1.08, transformOrigin: "left center", duration: 0.18, yoyo: true, repeat: 1, immediateRender: false }}, {round(252.98 - a, 2)} - 0.05);
      const td = {r("dopiero")};
      for (let i = 0; i < 10; i++) tl.to("#a" + i, {{ opacity: 0.18, scale: 0.92, duration: 0.3, ease: "power2.out" }}, td - 0.1 + i * 0.03);
      tl.to("#a10", {{ scale: 1.22, backgroundColor: "#0071e3", duration: 0.4, ease: "expo.out" }}, {r("ostatni")} - 0.1);
      tl.fromTo("#okb", {{ scale: 0, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.3, ease: "back.out(3)", immediateRender: true }}, {r("wychodzi")} - 0.1);""", """
      .hd { left: 160px; top: 300px; }
      .cnt { font-size: 260px; font-weight: 900; letter-spacing: -0.065em; line-height: 0.95; }
      .cnt .u { font-size: 76px; letter-spacing: -0.03em; margin-left: 20px; }
      .yrs2 { display: flex; gap: 14px; margin-top: 24px; }
      .yrs2 span { padding: 10px 22px; border-radius: 999px; background: var(--fill); font-size: 32px; font-weight: 700; }
      .home { left: 960px; top: 150px; width: 800px; display: flex; flex-wrap: wrap; gap: 46px; }
      .ap2 { position: relative; width: 160px; height: 160px; border-radius: 38px; background: var(--ink); display: flex; align-items: center; justify-content: center; }
      .ap2 svg { width: 80px; height: 80px; }
      .okb { position: absolute; right: -16px; top: -16px; width: 64px; height: 64px; border-radius: 50%; background: var(--green); display: flex; align-items: center; justify-content: center; }
      .okb svg { width: 32px; height: 30px; }""")

if __name__ == "__main__":
    only = set(sys.argv[1:])
    meta = {}
    for k, s in S.items():
        meta[k] = [s["a"], s["b"], "K" if s["ov"] else "B"]
        if only and k not in only:
            continue
        d = round(s["b"] - s["a"], 2)
        js = s["js"].replace("DUR", str(d))
        if not s["ov"]:
            js += f"\n      K.whip({d});"
            body = s["body"] if s["body"].lstrip().startswith('<div class="cam"') else f'      <div class="cam" id="cam">{s["body"]}\n      </div>'
        else:
            body = s["body"]
        page(k, d, body, js, s["css"], overlay=s["ov"])
    old = json.load(open(os.path.join(HERE, "scenes.json"))) if os.path.exists(os.path.join(HERE, "scenes.json")) else {}
    old.update(meta); json.dump(old, open(os.path.join(HERE, "scenes.json"), "w"), indent=1)
    for k, (a, b, m) in sorted(meta.items(), key=lambda x: x[1][0]):
        print(k, m, f"{a:.2f}-{b:.2f}", f"{b - a:.1f}s")
