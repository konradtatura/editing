#!/usr/bin/env python3
"""„3 modele biznesu” batch 3 (plan #51–72, 9:01 → end). Same conventions as build1.py (B = full MP4, K = MOV with alpha)."""
import json, os, sys
from page import page, HERE
from words import W
from build1 import R, CHECK, PAUSE, WALL_CSS, GL

S = {}


def sc(key, a, b, mode, body, js, css=""):
    S[key] = dict(a=round(a, 2), b=round(b, 2), ov=mode == "K", body=body, js=js, css=css)


X = '<svg viewBox="0 0 26 26"><path d="M6 6 L20 20 M20 6 L6 20" stroke="#fff" stroke-width="4.5" stroke-linecap="round"/></svg>'
CUR = '<path d="M4 3 L4 48 L15 37 L23 56 L31 52 L23 34 L39 34 Z" fill="#f4f6fa" stroke="#0a0d16" stroke-width="3" stroke-linejoin="round"/>'
WIDGETS = ["Produkt", "Sklep", "Content", "Drabinka"]


def widget_card(filled, new=None, title="Model"):
    cells = ""
    for i, n in enumerate(WIDGETS):
        on = i in filled
        cells += (f'<div class="wc2{" on" if on else ""}" id="wg{i}"><span class="wn2">{i + 1}</span>'
                  f'<b id="wl{i}" style="{"" if on or i == new else "opacity:0"}">{n}</b></div>')
    return f'<div class="card ovc" style="width:600px"><div class="lab" style="margin-bottom:16px">{title}</div><div class="wgr">{cells}</div></div>'


WCSS = """
      .wgr { display: grid; grid-template-columns: 1fr 1fr; gap: 18px; }
      .wc2 { height: 220px; border-radius: 36px; background: var(--fill); padding: 24px; display: flex; flex-direction: column; justify-content: space-between; }
      .wc2.on { background: var(--blue); color: #fff; }
      .wn2 { width: 50px; height: 50px; border-radius: 50%; background: #fff; color: var(--ink); font-size: 26px; font-weight: 800; display: flex; align-items: center; justify-content: center; }
      .wc2.on .wn2 { background: rgba(255,255,255,0.25); color: #fff; }
      .wc2 b { font-size: 44px; font-weight: 900; letter-spacing: -0.04em; }"""


def fill_js(i, t):
    return (f'tl.to("#wg{i}", {{ backgroundColor: "#0071e3", color: "#ffffff", duration: 0.3 }}, {t} - 0.15); '
            f'tl.to("#wg{i} .wn2", {{ backgroundColor: "rgba(255,255,255,0.25)", color: "#ffffff", duration: 0.3 }}, {t} - 0.15); '
            f'tl.fromTo("#wl{i}", {{ opacity: 0, y: 16 }}, {{ opacity: 1, y: 0, duration: 0.35, ease: "expo.out", immediateRender: true }}, {t} - 0.15); '
            f'tl.fromTo("#wg{i}", {{ scale: 1 }}, {{ scale: 1.06, duration: 0.18, yoyo: true, repeat: 1, immediateRender: false }}, {t} - 0.1);')


# ================================================================ 51 · B original idea (0 transactions) vs proven topic (money flows)
a = W("nie szukaj oryginalnego", 541) - 0.1; b = W("najlepszą", 547.4) - 0.06; r = R(a)
pays = "".join(f'<div class="py" id="y{i}"><i>{CHECK}</i><span>Płatność</span><b>+{v} zł</b></div>' for i, v in enumerate([97, 49, 97, 147, 97, 49, 97]))
BULB = '<svg viewBox="0 0 64 64" width="96" height="96"><path d="M32 8 A18 18 0 0 1 42 41 V48 H22 V41 A18 18 0 0 1 32 8 Z M24 54 H40" fill="none" stroke="#86868b" stroke-width="4.5" stroke-linejoin="round" stroke-linecap="round"/></svg>'
sc("S51", a, b, "B", f"""
      <div class="cam" id="cam">
        <div class="panel cd" id="c1"><div class="lab">Oryginalny pomysł</div>{BULB}<div class="z">0 płatności</div></div>
        <div class="card cd" id="c2"><div class="lab">Sprawdzony temat</div><div class="pys" id="pys">{pays}</div><div class="win" id="win">wygrywa</div></div>
      </div>""", f"""
      K.push(DUR, 1.03);
      K.lift("#c1", 0.0, {{ y: 40, dur: 0.5, ease: "expo.out" }});
      K.lift("#c2", 0.12, {{ y: 40, dur: 0.5, ease: "expo.out" }});
      const tp = {r("płyną")};
      [0, 1, 2, 3, 4, 5, 6].forEach((i) => tl.fromTo("#y" + i, {{ opacity: 0, y: -30 }}, {{ opacity: 1, y: 0, duration: 0.3, ease: "expo.out", immediateRender: true }}, tp - 0.6 + i * 0.32));
      const tw = {r("wygrywa")};
      tl.to("#c1", {{ opacity: 0.35, scale: 0.94, duration: 0.4 }}, tw - 0.15);
      tl.to("#c2", {{ scale: 1.05, duration: 0.4, ease: "expo.out" }}, tw - 0.15);
      K.stamp("#win", tw - 0.1, {{ from: 1.4 }});""", """
      .cd { position: absolute; top: 150px; width: 700px; height: 780px; padding: 46px; overflow: hidden; }
      #c1 { left: 170px; display: flex; flex-direction: column; justify-content: space-between; }
      #c2 { left: 1050px; }
      .cd .lab { font-size: 40px; color: var(--ink); font-weight: 800; letter-spacing: -0.02em; }
      .z { font-size: 84px; font-weight: 900; color: #c7c7cc; letter-spacing: -0.04em; }
      .pys { margin-top: 26px; display: flex; flex-direction: column; gap: 12px; }
      .py { display: flex; align-items: center; gap: 18px; height: 72px; padding: 0 22px; border-radius: 18px; background: var(--fill); font-size: 32px; font-weight: 600; }
      .py i { width: 40px; height: 40px; border-radius: 50%; background: var(--green); display: flex; align-items: center; justify-content: center; } .py i svg { width: 20px; height: 18px; }
      .py b { margin-left: auto; font-weight: 800; color: #1f9d48; }
      .win { position: absolute; right: 40px; top: 36px; padding: 10px 26px; border-radius: 999px; background: var(--green); color: #fff; font-size: 34px; font-weight: 800; }""")

# ================================================================ 53 · B AI slop text on a sales page — people see it, 0 sales
a = W("ai nie jest", 552.6) - 0.1; b = W("sztuszna", 557.6) - 0.06; r = R(a)
SLOP = "Odkryj moc transformacji z naszym przełomowym kursem, który zrewolucjonizuje Twoje życie i odblokuje Twój pełny potencjał."
sc("S53", a, b, "B", f"""
      <div class="cam" id="cam">
        <div class="card pg"><div class="pgh"><i></i><span>Strona sprzedażowa</span></div>
          <div class="txt" id="tx"></div>
          <div class="buy" id="buy">Kup teraz</div><div class="sold" id="sold">Sprzedaże: 0</div></div>
        <div class="abs mk1" id="m1"></div><div class="abs mk2" id="m2"></div>
      </div>""", f"""
      K.push(DUR, 1.03);
      K.lift(".pg", 0.0, {{ y: 40, dur: 0.5, ease: "expo.out" }});
      K.type("#tx", 0.25, "", "{SLOP}", 1.6);
      K.lift("#buy", {r("stronę")} - 0.2, {{ y: 14, dur: 0.3 }});
      const tw = {r("widzą")};
      tl.to("#tx", {{ color: "#86868b", duration: 0.3 }}, tw - 0.1);
      K.lift("#sold", {r("kupią")} - 0.3, {{ y: 10, dur: 0.3 }}); K.shake("#sold", {r("kupią")}, 14);
      tl.to("#buy", {{ backgroundColor: "#c7c7cc", duration: 0.3 }}, {r("kupią")});""", """
      .pg { left: 360px; top: 100px; width: 1200px; height: 880px; padding: 0 80px; }
      .pgh { height: 90px; display: flex; align-items: center; gap: 16px; border-bottom: 1px solid var(--line); margin: 0 -80px 60px; padding: 0 40px; font-size: 28px; font-weight: 600; color: var(--grey); }
      .pgh i { width: 22px; height: 22px; border-radius: 50%; background: #c7c7cc; display: block; }
      .txt { font-size: 60px; font-weight: 700; letter-spacing: -0.03em; line-height: 1.2; min-height: 430px; }
      .buy { display: inline-flex; padding: 28px 60px; border-radius: 999px; background: var(--blue); color: #fff; font-size: 42px; font-weight: 800; }
      .sold { display: inline-block; margin-left: 40px; font-size: 44px; font-weight: 900; color: var(--red); }""")

# ================================================================ 54 · K what AI doesn't have: your toggles switch ON (callback of S08)
a = W("czyli swój", 561.2) - 0.12; b = W("i to jest różnica", 565) - 0.06; r = R(a)
rows = [("Twój głos", "głos"), ("Twoje przykłady", "przykłady"), ("Twoje doświadczenie", "doświadczenie")]
rh = "".join(f'<div class="tr3"><span>{n}</span><div class="tog" id="t{i}"><div class="on"></div><div class="k"></div></div></div>' for i, (n, _) in enumerate(rows))
sc("S54", a, b, "K", f"""
      <div class="card ovc" style="width:640px"><div class="lab">Tego AI nie ma</div>{rh}</div>""", f"""
      K.card(DUR);
      {"".join(f'K.toggle("#t{i}", {r(w)} - 0.1, true); ' for i, (_, w) in enumerate(rows))}""", """
      .tr3 { display: flex; justify-content: space-between; align-items: center; padding: 22px 0; border-top: 1px solid var(--line); font-size: 42px; font-weight: 700; letter-spacing: -0.02em; }
      .tr3 .tog { transform: scale(1.25); transform-origin: right center; }""")

# ================================================================ 55 · K widget 2: Sklep
a = W("punkt drugi", 569) - 0.12; b = W("pomyśleli", 572.2) - 0.06; r = R(a)
sc("S55", a, b, "K", widget_card({0}), f"""
      K.card(DUR);
      {fill_js(1, f'{r("sklep")}')}""", WCSS)

# ================================================================ 56 · B Shortcuts: one click → page, payment, delivery; a sale runs through itself ⭐
a = W("i budujesz", 578.8) - 0.1; b = W("teraz punkt", 586.2) - 0.06; r = R(a)
SH = {"str": '<rect x="10" y="12" width="44" height="40" rx="6" fill="none" stroke="#fff" stroke-width="4.5"/><path d="M10 24 H54" stroke="#fff" stroke-width="4.5"/>',
      "pay": '<rect x="8" y="16" width="48" height="32" rx="6" fill="none" stroke="#fff" stroke-width="4.5"/><path d="M8 27 H56" stroke="#fff" stroke-width="5"/>',
      "snd": '<path d="M8 32 L56 10 L44 54 L30 38 Z M30 38 L56 10" fill="none" stroke="#fff" stroke-width="4.5" stroke-linejoin="round"/>'}
blk = [("Strona", "str", "#0071e3", "strona"), ("Płatność", "pay", "#34c759", "płatność"), ("Wysyłka", "snd", "#ff9500", "wysyłka")]
bh = "".join(f'<div class="sh" id="b{i}"><div class="si3" style="background:{c}"><svg viewBox="0 0 64 64">{SH[k]}</svg></div><span>{n}</span></div>' for i, (n, k, c, _) in enumerate(blk))
sc("S56", a, b, "B", f"""
      <div class="cam" id="cam">
        <div class="abs hd"><div class="lab" style="font-size:36px">Skrót · Mój sklep</div></div>
        <div class="abs run" id="run"><svg viewBox="0 0 24 24" width="40" height="40"><path d="M7 4 L20 12 L7 20 Z" fill="#fff"/></svg>Uruchom</div>
        <div class="abs chain">{bh}</div>
        <div class="abs dot" id="dot"></div>
        <div class="abs outs"><div class="out" id="o1"><i>{CHECK}</i>Mail z dostępem</div><div class="out" id="o2"><i>{CHECK}</i><b>+97 zł</b> na koncie</div></div>
        <svg class="cur" id="cur" viewBox="0 0 46 60">{CUR}</svg>
      </div>""", f"""
      K.push(DUR, 1.03);
      K.lift(".sh", 0.0, {{ y: 30, dur: 0.45, stagger: 0.06, ease: "expo.out" }}); K.lift("#run", 0.1, {{ y: 20, dur: 0.4 }});
      tl.set(".sh", {{ opacity: 0.45 }}, 0.5);
      const tc = {r("kliknięciem")};
      K.click("#cur", 1400, 900, 1490, 165, tc - 0.9, tc - 0.05, "#run");
      {"".join(f'tl.to("#b{i}", {{ opacity: 1, scale: 1.04, duration: 0.2, ease: "power2.out" }}, {r(w)} - 0.12); tl.to("#b{i}", {{ scale: 1, duration: 0.2 }}, {r(w)} + 0.1); ' for i, (*_, w) in enumerate(blk))}
      const tk = {r("kupuje")};
      tl.fromTo("#dot", {{ x: 0, opacity: 0 }}, {{ x: 1240, opacity: 1, duration: 1.3, ease: "power1.inOut", immediateRender: true }}, tk - 0.2);
      tl.to("#dot", {{ opacity: 0, duration: 0.2 }}, tk + 1.1);
      K.lift("#o1", {r("mailu")} - 0.15, {{ y: 20, dur: 0.4, ease: "expo.out" }});
      K.lift("#o2", {r("pieniądze")} - 0.1, {{ y: 20, dur: 0.4, ease: "expo.out" }});
      tl.to("#cur", {{ opacity: 0, duration: 0.3 }}, {r("niczego")});""", """
      .hd { left: 160px; top: 140px; }
      .run { left: 1390px; top: 120px; display: flex; align-items: center; gap: 14px; padding: 22px 40px; border-radius: 999px; background: var(--ink); color: #fff; font-size: 40px; font-weight: 800; }
      .chain { left: 160px; top: 380px; display: flex; gap: 70px; }
      .sh { width: 486px; height: 220px; border-radius: 34px; background: var(--fill); display: flex; align-items: center; gap: 30px; padding: 0 40px; transform-origin: 50% 50%; }
      .si3 { width: 120px; height: 120px; border-radius: 28px; display: flex; align-items: center; justify-content: center; } .si3 svg { width: 72px; height: 72px; }
      .sh span { font-size: 56px; font-weight: 900; letter-spacing: -0.04em; }
      .dot { left: 300px; top: 480px; width: 28px; height: 28px; border-radius: 50%; background: var(--blue); box-shadow: 0 0 0 10px rgba(0,113,227,0.18); }
      .outs { left: 160px; top: 720px; display: flex; gap: 40px; }
      .out { display: flex; align-items: center; gap: 20px; padding: 30px 40px; border-radius: 30px; background: #fff; box-shadow: 0 20px 50px rgba(0,0,0,0.12); font-size: 46px; font-weight: 600; }
      .out i { width: 56px; height: 56px; border-radius: 50%; background: var(--green); display: flex; align-items: center; justify-content: center; } .out i svg { width: 28px; height: 26px; }
      .out b { font-weight: 900; color: #1f9d48; }""")

# ================================================================ 57 · K widget 3: Content
a = W("teraz punkt", 586.2) - 0.06; b = W("i tu też", 590.3) - 0.06; r = R(a)
sc("S57", a, b, "K", widget_card({0, 1}), f"""
      K.card(DUR);
      {fill_js(2, f'{r("content")}')}""", WCSS)

# ================================================================ 58 · B the outlier reel becomes your version (callback S41)
a = W("patrzysz", 592) - 0.1; b = W("i nie nie", 600.7) - 0.06; r = R(a)
views = ["4,1 tys.", "6,8 tys.", "3,2 tys.", "5,5 tys.", "1,2 mln", "4,9 tys.", "7,3 tys.", "2,6 tys.", "5,1 tys."]
tiles = "".join(f'<div class="rl{" hit" if v.endswith("mln") else ""}" id="r{i}"><svg viewBox="0 0 24 24" width="22" height="22"><path d="M7 5 L19 12 L7 19 Z" fill="#fff"/></svg><b>{v}</b></div>' for i, v in enumerate(views))
sc("S58", a, b, "B", f"""
      <div class="cam" id="cam">
        <div class="abs lab2">Twoja nisza</div>
        <div class="abs grid3" id="g">{tiles}</div>
        <svg class="abs" style="left:0;top:0" width="1920" height="1080"><path id="arc" d="M820,520 C 1000,380 1140,380 1260,470" fill="none" stroke="#0071e3" stroke-width="6" stroke-linecap="round"/></svg>
        <div class="abs mine" id="mine"><div class="mt">format, który wygrał</div><div class="mb">po swojemu</div><div class="tag" id="tag">Twoja rolka</div></div>
      </div>""", f"""
      K.push(DUR, 1.03);
      K.lift(".rl", 0.0, {{ y: 20, s: 0.95, dur: 0.35, stagger: 0.03, ease: "expo.out" }});
      const tw = {r("większą")};
      tl.to(".rl:not(.hit)", {{ opacity: 0.35, duration: 0.3 }}, tw - 0.2);
      tl.to(".rl.hit", {{ scale: 1.12, backgroundColor: "#0071e3", duration: 0.4, ease: "expo.out" }}, tw - 0.2);
      const tf = {r("format")};
      K.draw("#arc", tf - 0.3, 0.5);
      K.lift("#mine", tf, {{ y: 40, s: 0.9, dur: 0.5, ease: "expo.out" }});
      const ts = {r("swojemu")};
      tl.to("#mine", {{ backgroundColor: "#0071e3", color: "#ffffff", duration: 0.35 }}, ts - 0.25);
      K.stamp("#tag", ts - 0.1, {{ from: 1.4 }});""", """
      .lab2 { left: 160px; top: 110px; font-size: 40px; font-weight: 800; }
      .grid3 { left: 160px; top: 190px; width: 640px; display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; }
      .rl { position: relative; height: 250px; border-radius: 14px; background: #3a3a3c; display: flex; align-items: flex-end; gap: 6px; padding: 14px; color: #fff; }
      .rl b { font-size: 26px; font-weight: 800; } .rl.hit b { font-size: 34px; }
      .mine { left: 1260px; top: 190px; width: 500px; height: 770px; border-radius: 30px; background: var(--fill); padding: 40px; display: flex; flex-direction: column; justify-content: flex-end; }
      .mt { font-size: 40px; font-weight: 600; opacity: .8; } .mb { font-size: 84px; font-weight: 900; letter-spacing: -0.045em; line-height: 1; }
      .tag { position: absolute; left: 40px; top: 40px; padding: 12px 26px; border-radius: 999px; background: #fff; color: var(--blue); font-size: 32px; font-weight: 800; }""")

# ================================================================ 60 · B widget 4: Drabinka (full screen, ladder grows) ⭐
a = W("i teraz punkt czwarty", 607.7) - 0.1; b = W("bo większo", 615.7) - 0.06; r = R(a)
wd = "".join(f'<div class="wg2{" on" if i < 3 else ""}" id="w{i}"><div class="wn">{i + 1}</div><div class="wt" id="wt{i}">{n}</div></div>' for i, n in enumerate(WIDGETS))
rungs = "".join(f'<i class="rg" id="g{k}" style="bottom:{24 + k * 52}px"></i>' for k in range(4))
sc("S60", a, b, "B", f"""
      <div class="cam" id="cam">
        <div class="abs hd"><div class="h-l w300" id="h1" style="font-size:84px">Punkt czwarty</div><div class="h-l" id="h2" style="font-size:84px">najciekawszy.</div>
          <div class="t-s grey" id="h3" style="font-size:44px;margin-top:30px">kilka stówek → <b style="color:#1d1d1f">prawdziwy biznes</b></div></div>
        <div class="abs wgs">{wd}</div>
        <div class="abs lad" id="lad"><i class="rl1"></i><i class="rl2"></i>{rungs}</div>
      </div>""", f"""
      K.push(DUR, 1.035);
      tl.set(".wt", {{ opacity: 1 }}, 0); tl.set("#wt3", {{ opacity: 0 }}, 0);
      K.lift(".wg2", 0.0, {{ y: 20, dur: 0.4, stagger: 0.06 }});
      K.rise("#h1", 0.1); K.rise("#h2", {r("najciekawszy")} - 0.15);
      const td = {r("drabinka")};
      tl.to("#w3", {{ backgroundColor: "#0071e3", duration: 0.3 }}, td - 0.15); tl.to("#w3 .wn", {{ backgroundColor: "rgba(255,255,255,0.25)", color: "#fff", duration: 0.3 }}, td - 0.15);
      tl.fromTo("#wt3", {{ opacity: 0, y: 16 }}, {{ opacity: 1, y: 0, color: "#fff", duration: 0.35, ease: "expo.out", immediateRender: false }}, td - 0.15);
      tl.fromTo(".rg", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.25, stagger: 0.12, ease: "power3.out", immediateRender: true }}, td + 0.1);
      tl.fromTo(".rl1, .rl2", {{ scaleY: 0 }}, {{ scaleY: 1, duration: 0.4, ease: "power3.out", immediateRender: true }}, td);
      K.lift("#h3", {r("stówkami")} - 0.3, {{ y: 14, dur: 0.4 }});""", """
      .hd { left: 150px; top: 330px; }
      .wgs { left: 920px; top: 120px; display: grid; grid-template-columns: 400px 400px; gap: 40px; }
      .wg2 { height: 400px; border-radius: 56px; background: var(--fill); padding: 40px; display: flex; flex-direction: column; justify-content: space-between; }
      .wg2.on { background: var(--blue); color: #fff; }
      .wn { width: 76px; height: 76px; border-radius: 50%; background: #fff; font-size: 38px; font-weight: 800; display: flex; align-items: center; justify-content: center; color: var(--ink); }
      .wg2.on .wn { background: rgba(255,255,255,0.25); color: #fff; }
      .wt { font-size: 64px; font-weight: 900; letter-spacing: -0.045em; }
      .lad { left: 1620px; top: 600px; width: 110px; height: 240px; }
      .rl1, .rl2 { position: absolute; bottom: 0; width: 10px; height: 230px; border-radius: 6px; background: #fff; transform-origin: bottom center; display: block; }
      .rl1 { left: 0; } .rl2 { right: 0; }
      .rg { position: absolute; left: 0; right: 0; height: 12px; border-radius: 6px; background: #fff; display: block; transform-origin: left center; }""")

# ================================================================ 60b · A+ trust of a stranger = hardest thing online (wall)
a = W("tylko że przekonanie", 623) - 0.1; b = W("dlatego ten", 627.9) - 0.06; r = R(a)
sc("S60b", a, b, "K", """
      <div class="wall" style="top:210px"><div class="wl" id="l1">zaufanie obcej osoby</div><div class="wb" id="l2" style="font-size:66px;line-height:1.05">= najtrudniejsza rzecz w internecie</div></div>""", f"""
      K.rise("#l1", {r("przekonanie")} - 0.1, {{ stagger: 0.04 }});
      K.rise("#l2", {r("najtrudniejsza")} - 0.2, {{ stagger: 0.05 }});
      K.fadeOut(".wall", DUR - 0.28, {{ y: -16, dur: 0.26 }});""", WALL_CSS)

# ================================================================ 62 · B the gap: stranger → client, the cheap product is the bridge ⭐
a = W("dlatego ten", 627.9) - 0.06; b = W("i dlatego ja", 638.8) - 0.06; r = R(a)
P = '<svg viewBox="0 0 80 80" width="180" height="180"><circle cx="40" cy="40" r="40" fill="{c}"/><circle cx="40" cy="31" r="13" fill="#fff"/><path d="M16 66 C20 50 60 50 64 66" fill="#fff"/></svg>'
sc("S62", a, b, "B", f"""
      <div class="cam" id="cam">
        <div class="abs prd" id="prd"><div class="lab">Pierwszy, tani produkt</div><div class="pj"><span class="ws" id="zb"><span>miał cię zbogacić</span></span></div><div class="pj2" id="pj2">ma zamienić obcego w klienta</div></div>
        <div class="abs cl1" id="cl1"></div><div class="abs cl2" id="cl2"></div>
        <div class="abs pp" id="p1">{P.format(c="#c7c7cc")}<b>Obcy</b><span>nigdy nie zapłacił</span></div>
        <div class="abs pp" id="p2">{P.format(c="#0071e3")}<b>Klient</b><span>zapłacił raz</span></div>
        <div class="abs bridge" id="br">tani produkt</div>
        <div class="abs gapl" id="gl">największa przepaść</div>
      </div>""", f"""
      K.push(DUR, 1.03);
      K.lift("#prd", 0.0, {{ y: 30, dur: 0.5, ease: "expo.out" }});
      K.strike("#zb", {r("zbogacić")} - 0.1);
      K.lift("#pj2", {r("zamienić")} - 0.15, {{ y: 14, dur: 0.4 }});
      const tg = {r("przepłaść")};
      tl.to("#prd", {{ y: -40, opacity: 0, duration: 0.35 }}, tg - 0.45);
      K.lift("#cl1, #cl2", tg - 0.2, {{ y: 120, dur: 0.6, ease: "expo.out" }});
      K.lift("#p1", tg - 0.1, {{ y: 30, dur: 0.45, ease: "expo.out" }});
      K.lift("#p2", {r("kimś", W("raz", a) - 0.8)} - 0.1, {{ y: 30, dur: 0.45, ease: "expo.out" }});
      tl.fromTo("#br", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.6, ease: "expo.out", immediateRender: true }}, {r("raz")} - 0.1);
      K.lift("#gl", {r("największa")} - 0.15, {{ y: 14, dur: 0.4 }});""", """
      .prd { left: 160px; top: 140px; } .prd .lab { font-size: 40px; }
      .pj { font-size: 96px; font-weight: 300; letter-spacing: -0.04em; } .pj2 { font-size: 96px; font-weight: 900; letter-spacing: -0.045em; color: var(--blue); }
      .cl1, .cl2 { top: 640px; height: 440px; background: var(--ink); }
      .cl1 { left: 0; width: 760px; border-radius: 0 40px 0 0; } .cl2 { right: 0; width: 760px; border-radius: 40px 0 0 0; }
      .pp { top: 380px; width: 400px; display: flex; flex-direction: column; align-items: center; gap: 6px; }
      #p1 { left: 260px; } #p2 { right: 260px; }
      .pp b { font-size: 52px; font-weight: 900; letter-spacing: -0.03em; } .pp span { font-size: 30px; color: var(--grey); font-weight: 600; }
      .bridge { left: 700px; top: 610px; width: 520px; height: 64px; border-radius: 16px; background: var(--blue); color: #fff; font-size: 34px; font-weight: 800; display: flex; align-items: center; justify-content: center; transform-origin: left center; }
      .gapl { left: 0; width: 1920px; top: 540px; text-align: center; font-size: 46px; font-weight: 900; color: var(--ink); }""")

# ================================================================ 63 · K price slider: 5 zł looks weak → 30–100 zł
a = W("i dlatego ja", 638.8) - 0.06; b = W("a nad nim", 648.2) - 0.06; r = R(a)
sc("S63", a, b, "K", """
      <div class="card ovc" style="width:680px"><div class="lab">Cena pierwszego produktu</div><div class="pv" id="pv">5 zł</div><div class="pn2" id="pn2">wygląda słabo</div>
        <div class="trk"><div class="zone" id="zn"></div><div class="knob" id="kn"></div></div><div class="sc"><span>0</span><span>50</span><span>100</span><span>150 zł</span></div></div>""", f"""
      K.card(DUR);
      const t5 = {r("5")}, tz = {r("okolice")};
      tl.set("#pn2", {{ opacity: 0 }}, 0); tl.set("#zn", {{ opacity: 0 }}, 0);
      tl.to("#pv, #kn", {{ color: "#ff3b30", backgroundColor: "#ff3b30", duration: 0.01 }}, 0);
      tl.set("#pv", {{ backgroundColor: "transparent" }}, 0.02);
      K.lift("#pn2", {r("taniej")} - 0.15, {{ y: 10, dur: 0.3 }}); K.shake("#kn", {r("słabejego")}, 8);
      tl.to("#zn", {{ opacity: 1, duration: 0.3 }}, tz - 0.1);
      tl.to("#kn", {{ left: 280, backgroundColor: "#34c759", duration: 0.7, ease: "power3.inOut" }}, tz);
      tl.to("#pn2", {{ opacity: 0, duration: 0.2 }}, tz);
      K.count("#pv", 5, 97, tz, 0.7, (v) => Math.round(v) + " zł", "power3.inOut");
      tl.to("#pv", {{ color: "#1f9d48", duration: 0.3 }}, tz + 0.4);""", """
      .pv { font-size: 120px; font-weight: 900; letter-spacing: -0.05em; line-height: 1.05; }
      .pn2 { font-size: 36px; font-weight: 700; color: var(--red); height: 46px; }
      .trk { position: relative; height: 16px; border-radius: 8px; background: var(--fill); margin: 40px 0 14px; }
      .zone { position: absolute; left: 115px; width: 255px; top: -8px; height: 32px; border-radius: 10px; background: rgba(52,199,89,0.25); }
      .knob { position: absolute; left: 10px; top: -18px; width: 52px; height: 52px; margin-left: -26px; border-radius: 50%; background: var(--red); box-shadow: 0 4px 14px rgba(0,0,0,0.2); }
      .sc { display: flex; justify-content: space-between; font-size: 24px; color: var(--grey); font-weight: 600; }""")

# ================================================================ 64 · K ladder: step 2 = program for a few hundred – few thousand
a = W("a nad nim", 648.2) - 0.06; b = W("i zobacz", 653.8) - 0.06; r = R(a)
sc("S64", a, b, "K", """
      <div class="card ovc" style="width:680px"><div class="lab">Drabinka</div>
        <div class="stp2" id="s2"><b>2</b><div><span>Program, praca bliżej z Tobą</span><em>kilkaset – kilka tys. zł</em></div></div>
        <div class="stp2 one" id="s1"><b>1</b><div><span>Pierwszy produkt</span><em>30–100 zł</em></div></div></div>""", f"""
      K.card(DUR);
      K.lift("#s1", 0.1, {{ y: 10, dur: 0.35 }});
      K.lift("#s2", {r("większego")} - 0.2, {{ y: 40, dur: 0.5, ease: "expo.out" }});
      tl.fromTo("#s2 em", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3, immediateRender: true }}, {r("kilkaset")} - 0.15);""", """
      .stp2 { display: flex; align-items: center; gap: 26px; padding: 26px 28px; margin-top: 18px; border-radius: 28px; background: var(--blue); color: #fff; margin-left: 60px; }
      .stp2.one { background: var(--fill); color: var(--ink); margin-left: 0; margin-right: 60px; }
      .stp2 b { width: 68px; height: 68px; border-radius: 50%; background: rgba(255,255,255,0.25); font-size: 34px; display: flex; align-items: center; justify-content: center; flex: none; }
      .stp2.one b { background: #fff; }
      .stp2 span { display: block; font-size: 36px; font-weight: 800; letter-spacing: -0.02em; } .stp2 em { font-style: normal; font-size: 30px; font-weight: 600; opacity: .85; }""")

# ================================================================ 65 · B iOS calculator: 100 × 97 = 9 700 ⭐
a = W("jak powiedzmy", 655) - 0.1; b = W("i teraz tych", 660.7) - 0.06; r = R(a)
keys = [["AC", "+/−", "%", "÷"], ["7", "8", "9", "×"], ["4", "5", "6", "−"], ["1", "2", "3", "+"], ["0", "", ",", "="]]
kh = "".join(f'<div class="k{" op" if c in "÷×−+=" and c else ""}{" fn" if c in ("AC", "+/−", "%") else ""}{" zero" if c == "0" else ""}" id="k_{ "eq" if c == "=" else ("x" if c == "×" else "") }">{c}</div>' for row in keys for c in row if not (c == "" ))
sc("S65", a, b, "B", f"""
      <div class="cam" id="cam">
        <div class="abs hd"><div class="lab" style="font-size:36px">Przykład, nie obietnica</div><div class="h-l w300" id="h1">100 osób</div><div class="h-l" id="h2">× 97 zł</div></div>
        <div class="calc"><div class="disp" id="d">0</div><div class="keys">{kh}</div></div>
      </div>""", f"""
      K.push(DUR, 1.03);
      K.lift(".calc", 0.0, {{ y: 50, dur: 0.55, ease: "expo.out" }}); K.lift(".hd .lab", 0.05, {{ y: 10, dur: 0.4 }});
      const t1 = {r("100")}, t2 = {r("97")}, t3 = {r("ile")};
      K.rise("#h1", t1 - 0.15); K.rise("#h2", t2 - 0.15);
      K.frame((T) => {{ document.getElementById("d").textContent = T >= t3 ? "9 700" : T >= t2 - 0.1 ? "97" : T >= t1 + 0.6 ? "100" : T >= t1 - 0.1 ? "100" : "0"; }});
      tl.to("#k_x", {{ backgroundColor: "#ffffff", color: "#ff9500", duration: 0.1 }}, t1 + 0.5); tl.to("#k_x", {{ backgroundColor: "#ff9500", color: "#ffffff", duration: 0.1 }}, t2 - 0.1);
      tl.to("#k_eq", {{ scale: 0.9, duration: 0.08, yoyo: true, repeat: 1 }}, t3 - 0.05);
      tl.fromTo("#d", {{ scale: 1 }}, {{ scale: 1.06, transformOrigin: "right center", duration: 0.15, yoyo: true, repeat: 1, immediateRender: false }}, t3);""", """
      .hd { left: 160px; top: 320px; }
      .calc { position: absolute; left: 1080px; top: 60px; width: 640px; height: 960px; border-radius: 60px; background: #000; padding: 40px 40px; display: flex; flex-direction: column; justify-content: flex-end; }
      .disp { color: #fff; font-size: 150px; font-weight: 300; text-align: right; letter-spacing: -0.04em; margin-bottom: 20px; transform-origin: right center; }
      .keys { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; }
      .k { height: 124px; border-radius: 62px; background: #333336; color: #fff; font-size: 54px; font-weight: 500; display: flex; align-items: center; justify-content: center; }
      .k.fn { background: #a5a5a5; color: #000; } .k.op { background: #ff9500; } .k.zero { grid-column: span 2; justify-content: flex-start; padding-left: 50px; }""")

# ================================================================ 66 · K 10% of 100 → 10 people × 350 zł = 3 500 zł / month
a = W("i teraz tych", 660.7) - 0.06; b = W("i ci sami", 668.8) - 0.06; r = R(a)
dots = "".join(f'<i id="d{i}"></i>' for i in range(100))
sc("S66", a, b, "K", f"""
      <div class="card ovc" style="width:640px"><div class="lab">Te same 100 osób</div><div class="dg">{dots}</div>
        <div class="eq"><span id="e1">10 osób × 350 zł</span><b id="e2">= 3 500 zł / mies.</b></div></div>""", f"""
      K.card(DUR);
      const t10 = {round(662.20 - a, 2)};
      tl.to("#d0, #d11, #d23, #d37, #d44, #d58, #d62, #d79, #d85, #d96", {{ backgroundColor: "#0071e3", scale: 1.2, duration: 0.25, stagger: 0.05 }}, t10 - 0.1);
      K.rise("#e1", {r("350")} - 0.2, {{ stagger: 0.04 }});
      K.rise("#e2", {round(666.66 - a, 2)} - 0.15, {{ stagger: 0.05 }});""", """
      .dg { display: grid; grid-template-columns: repeat(10, 1fr); gap: 14px; margin: 12px 0 26px; }
      .dg i { display: block; width: 36px; height: 36px; border-radius: 50%; background: #d8d8de; }
      #e1 { display: block; font-size: 40px; font-weight: 600; } #e2 { display: block; font-size: 58px; font-weight: 900; letter-spacing: -0.04em; color: var(--blue); }""")

# ================================================================ 67 · B same people → 9 700 becomes 13 200 + 3 500 every month ⭐
a = W("i ci sami", 668.8) - 0.06; b = W("pieniądze cały", 677.7) - 0.06; r = R(a)
sc("S67", a, b, "B", f"""
      <div class="cam" id="cam">
        <div class="abs chips"><div class="chp" id="c1">nowi klienci: <b>0</b></div><div class="chp" id="c2">nowe filmy: <b>0</b></div></div>
        <div class="abs big2"><div class="old" id="old"><span class="ws" id="ow"><span>9 700 zł</span></span></div><div class="new"><span id="nv">9 700</span> zł</div>
          <div class="rec" id="rec"><svg viewBox="0 0 40 40" width="44" height="44"><path d="M8 20 A12 12 0 0 1 30 12 M32 20 A12 12 0 0 1 10 28" fill="none" stroke="#fff" stroke-width="4" stroke-linecap="round"/><path d="M30 4 V13 H21 M10 36 V27 H19" fill="none" stroke="#fff" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/></svg>+ 3 500 zł co miesiąc</div></div>
      </div>""", f"""
      K.push(DUR, 1.035);
      K.lift("#c1", {r("klienta")} - 0.4, {{ y: 20, dur: 0.4, ease: "expo.out" }}); K.lift("#c2", {r("filmu")} - 0.3, {{ y: 20, dur: 0.4, ease: "expo.out" }});
      tl.set(".old", {{ opacity: 0 }}, 0);
      K.lift(".new", 0.1, {{ y: 30, dur: 0.5, ease: "expo.out" }});
      const tz = {r("zamiast")}, tn = {r("13200")};
      K.count("#nv", 9700, 13200, tn - 0.35, 0.8, (v) => K.pl(Math.round(v / 100) * 100), "power3.inOut");
      tl.to(".old", {{ opacity: 1, duration: 0.3 }}, tn - 0.4);
      K.strike("#ow", tn - 0.2);
      tl.to(".new", {{ color: "#0071e3", duration: 0.3 }}, tn + 0.3);
      K.lift("#rec", {round(675.60 - a, 2)} - 0.15, {{ y: 30, s: 0.9, dur: 0.45, ease: "expo.out" }});""", """
      .chips { left: 160px; top: 130px; display: flex; gap: 20px; }
      .chp { padding: 18px 32px; border-radius: 999px; background: var(--fill); font-size: 38px; font-weight: 600; } .chp b { font-weight: 900; }
      .big2 { left: 160px; top: 300px; }
      .old { font-size: 80px; font-weight: 300; color: var(--grey); letter-spacing: -0.04em; height: 100px; }
      .new { font-size: 280px; font-weight: 900; letter-spacing: -0.065em; line-height: 0.95; }
      .rec { display: inline-flex; align-items: center; gap: 20px; margin-top: 40px; padding: 24px 40px; border-radius: 999px; background: var(--green); color: #fff; font-size: 54px; font-weight: 800; }""")

# ================================================================ 68 · K the whole model: 4 widgets filled
a = W("produkt sklep", 680.8) - 0.15; b = W("i teraz rzecz", 683.7) - 0.06; r = R(a)
sc("S68", a, b, "K", widget_card(set(), new=None, title="Cały model"), f"""
      K.card(DUR);
      {fill_js(0, f'{r("produkt")}')} {fill_js(1, f'{r("sklep")}')} {fill_js(2, f'{r("konta")}')} {fill_js(3, f'{r("drabinka")}')}""", WCSS)

# ================================================================ 69 · A+ easy start ≠ easy result (wall)
a = W("ale łatwy", 692.5) - 0.12; b = W("bo ja widzę", 694.7) + 0.3; r = R(a)
sc("S69", a, b, "K", """
      <div class="wall" style="top:230px"><div class="wl" id="l1" style="font-size:62px">łatwy start</div><div class="wb" id="l2" style="font-size:80px"><span class="ws" id="ww"><span>≠ łatwy wynik</span></span></div></div>""", f"""
      K.rise("#l1", {r("łatwy")} - 0.12, {{ stagger: 0.04 }});
      K.lift("#l2", {r("nie znaczy")} - 0.15, {{ y: 24, dur: 0.4, ease: "expo.out" }});
      K.fadeOut(".wall", DUR - 0.28, {{ y: -16, dur: 0.26 }});""", WALL_CSS)

# ================================================================ 70 · B app switcher: agency → app → trading → dropshipping, every time from zero ⭐
a = W("skacze", 703.4) - 0.1; b = W("i właśnie ten", 711.2) - 0.06; r = R(a)
apps = [("Agencja", "agencja"), ("Aplikacja", "aplikacja"), ("Trading", "trading"), ("Dropshipping", "dropshipping"), ("Coś jeszcze", "coś")]
ah = "".join(f'<div class="sw" id="a{i}"><div class="swh">{n}</div><div class="swb"><div class="pg2"><i id="p{i}"></i></div><span id="v{i}">0%</span></div></div>' for i, (n, _) in enumerate(apps))
sc("S70", a, b, "B", f"""
      <div class="cam" id="cam">
        <div class="abs hd"><div class="h-m w300" id="h1" style="font-size:72px">Skacze do następnej rzeczy…</div></div>
        <div class="abs strip" id="strip">{ah}</div>
        <div class="abs zero" id="z">i znowu od zera</div>
      </div>""", f"""
      K.push(DUR, 1.02);
      K.rise("#h1", 0.02, {{ stagger: 0.04 }});
      const T = [{", ".join(str(r(w)) for _, w in apps)}];
      T.forEach((t, i) => {{
        tl.fromTo("#a" + i, {{ opacity: 0, y: 40 }}, {{ opacity: 1, y: 0, duration: 0.35, ease: "expo.out", immediateRender: true }}, t - 0.2);
        tl.fromTo("#p" + i, {{ scaleX: 0 }}, {{ scaleX: 0.35, duration: 0.4, ease: "power2.out", immediateRender: true }}, t);
        K.count("#v" + i, 0, 35, t, 0.4, (v) => Math.round(v) + "%");
        if (i > 0) {{ tl.to("#p" + (i - 1), {{ scaleX: 0, duration: 0.3, ease: "power2.in" }}, t - 0.2); K.count("#v" + (i - 1), 35, 0, t - 0.2, 0.3, (v) => Math.round(v) + "%"); tl.to("#a" + (i - 1), {{ opacity: 0.35, duration: 0.3 }}, t - 0.2); }}
      }});
      const tz = {r("zera")};
      tl.to("#p4", {{ scaleX: 0, duration: 0.3 }}, tz - 0.2); K.count("#v4", 35, 0, tz - 0.2, 0.3, (v) => Math.round(v) + "%");
      tl.to("#v0, #v1, #v2, #v3, #v4", {{ color: "#ff3b30", duration: 0.2 }}, tz - 0.1);
      K.lift("#z", tz - 0.15, {{ y: 14, dur: 0.35 }});""", """
      .hd { left: 160px; top: 120px; }
      .strip { left: 130px; top: 330px; display: flex; gap: 30px; }
      .sw { width: 306px; height: 460px; border-radius: 40px; background: #fff; box-shadow: 0 24px 64px rgba(0,0,0,0.14); padding: 32px; display: flex; flex-direction: column; justify-content: space-between; flex: none; }
      .swh { font-size: 46px; font-weight: 900; letter-spacing: -0.04em; }
      .swb { display: flex; align-items: center; gap: 12px; } .swb span { font-size: 34px; font-weight: 800; width: 84px; text-align: right; }
      .pg2 { flex: 1; height: 20px; border-radius: 10px; background: var(--fill); overflow: hidden; } .pg2 i { display: block; height: 100%; background: var(--blue); transform-origin: left center; }
      .zero { left: 0; width: 1920px; top: 900px; text-align: center; font-size: 56px; font-weight: 900; color: var(--red); letter-spacing: -0.03em; }""")

# ================================================================ 72 · B callback: not the 1st, not the 5th — he hit it because he didn't quit
a = W("mój znajomy", 719.2) - 0.1; b = W("i różnica", 723.4) - 0.06; r = R(a)
apps2 = "".join(f'<div class="ap2" id="q{i}"><svg viewBox="0 0 64 64">{g}</svg><div class="xb" id="x{i}">{X}</div></div>' for i, g in enumerate(GL))
sc("S72", a, b, "B", f"""
      <div class="cam" id="cam"><div class="abs hd"><div class="h-m w300" id="h0">Nie za pierwszym.</div><div class="h-m w300" id="h2">Nie za piątym.</div><div class="h-l" id="h1" style="margin-top:20px">Nie odpuścił.</div></div><div class="abs home">{apps2}</div></div>""", f"""
      K.push(DUR, 1.04);
      K.lift(".ap2", 0.0, {{ y: 20, s: 0.9, dur: 0.35, stagger: 0.03, ease: "expo.out" }});
      const t1 = {r("pierwszym")}, t5 = {r("piątym")}, tt = {round(722.52 - a, 2)};
      tl.fromTo("#x0", {{ scale: 0, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.25, ease: "back.out(3)", immediateRender: true }}, t1 - 0.1);
      tl.fromTo("#x1, #x2, #x3", {{ scale: 0, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.2, stagger: 0.08, ease: "back.out(3)", immediateRender: true }}, t1 + 0.25);
      tl.fromTo("#x4", {{ scale: 0, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.25, ease: "back.out(3)", immediateRender: true }}, t5 - 0.1);
      tl.fromTo("#x5, #x6, #x7, #x8, #x9", {{ scale: 0, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.18, stagger: 0.05, ease: "back.out(3)", immediateRender: true }}, t5 + 0.15);
      tl.to("#q0, #q1, #q2, #q3, #q4, #q5, #q6, #q7, #q8, #q9", {{ opacity: 0.3, duration: 0.3 }}, tt - 0.1);
      tl.to("#q10", {{ scale: 1.22, backgroundColor: "#0071e3", duration: 0.4, ease: "expo.out" }}, tt - 0.1);
      K.rise("#h0", t1 - 0.2, {{ stagger: 0.04 }}); K.rise("#h2", t5 - 0.2, {{ stagger: 0.04 }});
      K.rise("#h1", {r("odpuścił")} - 0.2, {{ stagger: 0.05 }});""", """
      .hd { left: 160px; top: 360px; }
      .home { left: 960px; top: 170px; width: 800px; display: flex; flex-wrap: wrap; gap: 46px; }
      .ap2 { position: relative; width: 160px; height: 160px; border-radius: 38px; background: var(--ink); display: flex; align-items: center; justify-content: center; }
      .ap2 svg { width: 80px; height: 80px; }
      .xb { position: absolute; right: -14px; top: -14px; width: 56px; height: 56px; border-radius: 50%; background: var(--red); display: flex; align-items: center; justify-content: center; }
      #x10 { display: none; } .xb svg { width: 26px; height: 26px; }""")

# ================================================================ 73 · K one try: software (a year, a million) vs digital product (a few weekends)
a = W("i różnica", 723.4) - 0.06; b = W("więc za pół", 729.7) - 0.06; r = R(a)
sc("S73", a, b, "K", """
      <div class="card ovc" style="width:680px"><div class="lab">Jedna próba kosztuje</div>
        <div class="rc" id="r1"><span>Software</span><b class="red">rok · 1 mln zł</b></div>
        <div class="rc" id="r2"><span>Produkt cyfrowy</span><b class="green">kilka weekendów</b></div></div>""", f"""
      K.card(DUR);
      K.lift(".rc", 0.15, {{ y: 14, dur: 0.35, stagger: 0.08 }});
      tl.fromTo("#r1 b", {{ opacity: 0, x: -14 }}, {{ opacity: 1, x: 0, duration: 0.3, immediateRender: true }}, {r("rok")} - 0.15);
      tl.fromTo("#r2 b", {{ opacity: 0, x: -14 }}, {{ opacity: 1, x: 0, duration: 0.3, immediateRender: true }}, {r("kilka", W("tylko", a))} - 0.15);""", """
      .rc { display: flex; flex-direction: column; gap: 4px; padding: 24px 0; border-top: 1px solid var(--line); }
      .rc span { font-size: 34px; font-weight: 600; color: #3a3a3c; } .rc b { font-size: 60px; font-weight: 900; letter-spacing: -0.04em; }""")

# ================================================================ 74 · B two futures in six months ⭐
a = W("więc za pół", 729.7) - 0.06; b = W("i tak może", 740.4) - 0.06; r = R(a)
vids = "".join(f'<div class="vi" id="v{i}"><i></i><div><b>{t}</b><span>Do obejrzenia później</span></div></div>' for i, t in enumerate(["Jak zarabiać z AI", "Biznes online 2026", "3 modele biznesu", "Pasywny dochód?", "Jak zacząć…"]))
sc("S74", a, b, "B", f"""
      <div class="cam" id="cam">
        <div class="abs hd"><div class="h-m" id="h1">Za pół roku</div></div>
        <div class="panel half" id="L"><div class="hh">Albo…</div><div class="vl">{vids}</div></div>
        <div class="panel half" id="Rr" style="left:990px"><div class="hh">…albo</div>
          <div class="prc" id="pc"><div class="pi2"></div><div><b>Twój produkt</b><span>online · sklep działa</span></div></div>
          <div class="sale" id="sl"><i>{CHECK}</i><div><b>Nowa sprzedaż</b><span>3:12 · kiedy spałeś</span></div></div></div>
      </div>""", f"""
      K.push(DUR, 1.03);
      K.rise("#h1", 0.05);
      K.lift("#L", {r("albo")} - 0.2, {{ y: 40, dur: 0.5, ease: "expo.out" }});
      [0, 1, 2, 3, 4].forEach((i) => tl.fromTo("#v" + i, {{ opacity: 0, y: -20 }}, {{ opacity: 1, y: 0, duration: 0.3, ease: "expo.out", immediateRender: true }}, {r("oglądać")} - 0.2 + i * 0.35));
      const tb = {r("albo", W("zacznę", a))};
      tl.to("#L", {{ opacity: 0.4, duration: 0.3 }}, tb);
      K.lift("#Rr", tb - 0.15, {{ y: 40, dur: 0.5, ease: "expo.out" }});
      K.lift("#pc", {round(736.14 - a, 2)} - 0.1, {{ y: 20, dur: 0.4, ease: "expo.out" }});
      K.lift("#sl", {round(738.74 - a, 2)} - 0.2, {{ y: -30, s: 0.95, dur: 0.45, ease: "expo.out" }});""", """
      .hd { left: 160px; top: 90px; }
      .half { position: absolute; left: 160px; top: 230px; width: 770px; height: 760px; padding: 44px; overflow: hidden; }
      .hh { font-size: 56px; font-weight: 900; letter-spacing: -0.04em; margin-bottom: 30px; }
      .vi { display: flex; align-items: center; gap: 22px; padding: 16px 0; } .vi i { width: 170px; height: 96px; border-radius: 14px; background: #c7c7cc; display: block; flex: none; }
      .vi b { display: block; font-size: 34px; font-weight: 800; } .vi span { font-size: 24px; color: var(--grey); font-weight: 600; }
      .prc { display: flex; align-items: center; gap: 26px; padding: 30px; border-radius: 30px; background: #fff; margin-bottom: 24px; }
      .pi2 { width: 120px; height: 120px; border-radius: 28px; background: var(--blue); flex: none; }
      .prc b, .sale b { display: block; font-size: 44px; font-weight: 900; letter-spacing: -0.03em; } .prc span, .sale span { font-size: 30px; color: var(--grey); font-weight: 600; }
      .sale { display: flex; align-items: center; gap: 22px; padding: 26px 30px; border-radius: 30px; background: #fff; box-shadow: 0 16px 40px rgba(0,0,0,0.1); }
      .sale i { width: 70px; height: 70px; border-radius: 18px; background: var(--green); display: flex; align-items: center; justify-content: center; flex: none; } .sale i svg { width: 34px; height: 32px; }""")

# ================================================================ 75 · K CTA: free course (was 10 000 zł), link first in description ⭐
a = W("cały ten model", 743) - 0.1; b = W("a jeśli z tego", 752.6) - 0.06; r = R(a)
sc("S75", a, b, "K", """
      <div class="card ovc" style="width:680px"><div class="lab">Darmowy kurs · krok po kroku</div>
        <div class="flow"><span id="f1">pomysł</span><i>→</i><span id="f2">produkt</span><i>→</i><span id="f3">drabinka</span></div>
        <div class="pr"><span class="ws" id="old"><span>10 000 zł</span></span><b id="free">0 zł</b></div>
        <div class="lk" id="lk">Link pierwszy w opisie ↓</div></div>""", f"""
      K.card(DUR);
      [["#f1", {r("pomysłu")}], ["#f2", {r("produkt")}], ["#f3", {r("drabinkę")}]].forEach(([s, t]) => K.lift(s, t - 0.15, {{ y: 10, s: 0.9, dur: 0.3, ease: "back.out(2)" }}));
      tl.set("#old, #free", {{ opacity: 0 }}, 0);
      const t0 = {r("darmowym")};
      tl.to("#free", {{ opacity: 1, duration: 0.2 }}, t0 - 0.15);
      tl.to("#old", {{ opacity: 1, duration: 0.2 }}, {round(750.78 - a, 2)} - 0.2); K.strike("#old", {round(751.22 - a, 2)} - 0.1);
      K.lift("#lk", {r("link")} - 0.15, {{ y: 14, dur: 0.35, ease: "expo.out" }});
      tl.to("#lk", {{ scale: 1.05, duration: 0.25, yoyo: true, repeat: 3 }}, {r("opisie")});""", """
      .flow { display: flex; align-items: center; gap: 12px; margin: 16px 0 26px; font-size: 34px; font-weight: 700; } .flow span { padding: 10px 20px; border-radius: 999px; background: var(--fill); } .flow i { font-style: normal; color: var(--grey); }
      .pr { display: flex; align-items: baseline; gap: 26px; } .pr .ws { font-size: 54px; font-weight: 300; color: var(--grey); } .pr b { font-size: 120px; font-weight: 900; letter-spacing: -0.05em; color: var(--green); }
      .lk { margin-top: 20px; padding: 24px 30px; border-radius: 24px; background: var(--blue); color: #fff; font-size: 40px; font-weight: 800; text-align: center; }""")

# ================================================================ 76 · B the question one last time (pause), then the one black card
a = W("co się dzieje z", 755.3) - 0.1; b = W("i jeżeli odpowiedź", 757.8) - 0.06; r = R(a)
sc("S76", a, b, "B", f"""
      <div class="cam" id="cam">
        <div class="abs pb" id="pb"><div class="tap" id="tp" style="left:50%;top:50%"></div>{PAUSE}</div>
        <div class="abs qq"><div class="h-l w300" id="q1">Co się dzieje z Twoimi pieniędzmi,</div><div class="h-l" id="q2">kiedy przestajesz pracować?</div></div>
      </div>""", f"""
      K.push(DUR, 1.04);
      K.lift("#pb", 0.0, {{ y: 0, s: 0.7, dur: 0.4, ease: "expo.out" }});
      K.rise("#q1", 0.05, {{ stagger: 0.04 }}); K.rise("#q2", {r("kiedy")} - 0.15, {{ stagger: 0.05 }});
      const tp = {r("przestajesz")};
      tl.to("#pb", {{ scale: 0.88, duration: 0.09, yoyo: true, repeat: 1, ease: "power2.in" }}, tp); K.tap("#tp", tp);""", """
      .pb { left: 860px; top: 160px; width: 200px; height: 200px; border-radius: 50%; background: var(--ink); display: flex; align-items: center; justify-content: center; }
      .pb svg { width: 120px; height: 120px; }
      .qq { left: 0; top: 440px; width: 1920px; text-align: center; } .qq .h-l { font-size: 96px; }""")

a = W("i jeżeli odpowiedź", 757.8) - 0.06; b = 763.13; r = R(a)
sc("S76b", a, b, "B", """
      <div class="cam" id="cam" style="background:#000">
        <div class="abs bl"><div class="t-s" id="l0" style="color:#86868b;font-size:44px;margin-bottom:10px">A jeśli odpowiedź brzmi</div><div class="h-l w300" id="l1" style="color:#86868b">„Wszystko staje”</div><div class="h-xl" id="l2" style="color:#fff;margin-top:30px">To nie biznes.</div><div class="h-hero" id="l3" style="color:#fff">To etat.</div></div>
      </div>""", f"""
      K.push(DUR, 1.05);
      K.rise("#l0", 0.03, {{ stagger: 0.04 }}); K.rise("#l1", {r("wszystko")} - 0.15, {{ stagger: 0.05 }});
      K.rise("#l2", {r("nie masz")} - 0.15, {{ stagger: 0.06 }});
      K.rise("#l3", {r("etat")} - 0.15, {{ stagger: 0.08 }});
      tl.to("#l0, #l1, #l2", {{ opacity: 0.35, duration: 0.4 }}, {r("etat")} + 0.3);""", """
      html, body, #root { background: #000 !important; }
      .bl { left: 0; top: 0; width: 1920px; height: 1080px; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; }""")

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
