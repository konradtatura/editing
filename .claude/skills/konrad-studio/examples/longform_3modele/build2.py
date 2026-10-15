#!/usr/bin/env python3
"""„3 modele biznesu” batch 2 (plan #26–50 + wall callout). Same conventions as build1.py (B = full MP4, K = MOV with alpha)."""
import json, math, os, sys
from page import page, HERE
from words import W
from build1 import R, CHECK, PAUSE, WALL_CSS, MODELS_CSS, models_card, GL

S = {}


def sc(key, a, b, mode, body, js, css=""):
    S[key] = dict(a=round(a, 2), b=round(b, 2), ov=mode == "K", body=body, js=js, css=css)


X = '<svg viewBox="0 0 26 26"><path d="M6 6 L20 20 M20 6 L6 20" stroke="#fff" stroke-width="4.5" stroke-linecap="round"/></svg>'

# ================================================================ 26 · B callback: 4 years, 10 projects that failed
a = W("i zatrzymaj", 258.8) - 0.1; b = W("bo widzisz", 266.6) - 0.06; r = R(a)
apps = "".join(f'<div class="ap2" id="a{i}"><svg viewBox="0 0 64 64">{g}</svg><div class="xb" id="x{i}">{X}</div></div>' for i, g in enumerate(GL))
sc("S26", a, b, "B", f"""
      <div class="cam" id="cam">
        <div class="abs hd"><div class="h-xl" id="l1" style="font-size:124px">4 lata.</div><div class="h-xl red" id="l2" style="font-size:124px"><span id="n10">0</span> projektów</div><div class="h-m w300" id="l3">nie wyszło.</div></div>
        <div class="abs home" id="home">{apps}</div>
      </div>""", f"""
      K.push(DUR, 1.035);
      tl.set(".ap2", {{ opacity: 1 }}, 0);
      K.lift("#home", 0.0, {{ y: 30, dur: 0.5, ease: "expo.out" }});
      tl.to("#a10", {{ backgroundColor: "#0071e3", duration: 0.01 }}, 0);
      K.rise("#l1", 0.25); tl.fromTo("#l1", {{ scale: 1 }}, {{ scale: 1.07, transformOrigin: "left center", duration: 0.18, yoyo: true, repeat: 1, immediateRender: false }}, {r("4")} - 0.1);
      const t10 = {r("10")};
      K.lift("#l2", t10 - 0.15, {{ y: 40, dur: 0.45, ease: "expo.out" }});
      K.count("#n10", 0, 10, t10 - 0.1, 0.9, (v) => String(Math.round(v)), "power2.out");
      for (let i = 0; i < 10; i++) tl.fromTo("#x" + i, {{ scale: 0, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.22, ease: "back.out(3)", immediateRender: true }}, t10 - 0.05 + i * 0.09);
      tl.to("#a0, #a1, #a2, #a3, #a4, #a5, #a6, #a7, #a8, #a9", {{ opacity: 0.35, duration: 0.3, stagger: 0.04 }}, {r("wyszły")});
      K.rise("#l3", {r("wyszły")} - 0.15, {{ stagger: 0.05 }});
      tl.to("#a10", {{ scale: 1.2, duration: 0.4, ease: "expo.out" }}, {r("zna")} - 0.1);
      tl.to("#l1, #l2, #l3", {{ opacity: 0.25, duration: 0.3 }}, {r("zna")} - 0.1);""", """
      .hd { left: 150px; top: 250px; }
      .home { left: 960px; top: 170px; width: 800px; display: flex; flex-wrap: wrap; gap: 46px; }
      .ap2 { position: relative; width: 160px; height: 160px; border-radius: 38px; background: var(--ink); display: flex; align-items: center; justify-content: center; }
      .ap2 svg { width: 80px; height: 80px; }
      .xb { position: absolute; right: -14px; top: -14px; width: 56px; height: 56px; border-radius: 50%; background: var(--red); display: flex; align-items: center; justify-content: center; }
      #x10 { display: none; }
      .xb svg { width: 26px; height: 26px; }""")

# ================================================================ 27 · B headlines → 3 blue dots in a sea of grey (survivorship) ⭐
a = W("tak to", 274) - 0.08; b = W("a software", 283.4) - 0.06; r = R(a)
heads = [("Tech · 2 godz. temu", "Startup zebrał 15 mln zł w pierwszej rundzie"), ("Biznes · wczoraj", "Aplikacja AI wyceniona na 100 mln"),
         ("Twitter · 4 godz. temu", "24 lata i pierwszy milion z aplikacji")]
hh = "".join(f'<div class="nw" id="h{i}"><div class="src">{s_}</div><div class="ht">{t}</div></div>' for i, (s_, t) in enumerate(heads))
COLS, ROWS, GAP = 56, 24, 30
blue = {(20, 9), (35, 15), (47, 6)}
dots = "".join(f'<i class="{"b" if (c, rr) in blue else ""}" style="left:{c * GAP}px;top:{rr * GAP}px"></i>' for rr in range(ROWS) for c in range(COLS))
sc("S27", a, b, "B", f"""
      <div class="cam" id="cam">
        <div class="abs sea" id="sea">{dots}</div>
        <div class="abs news" id="news">{hh}</div>
        <div class="abs lg" id="lg"><span class="bd"></span> wyszło <span class="gd"></span> nikt nie chciał</div>
      </div>""", f"""
      K.push(DUR, 1.03);
      K.lift(".nw", 0.0, {{ y: 40, s: 0.96, dur: 0.5, stagger: 0.12, ease: "expo.out" }});
      tl.set("#sea i", {{ opacity: 0 }}, 0);
      const tz = {r("tylko")};
      tl.to("#news", {{ scale: 0.25, opacity: 0, duration: 0.6, ease: "power3.in" }}, tz);
      tl.to("#sea i.b", {{ opacity: 1, duration: 0.25 }}, tz + 0.45);
      tl.fromTo("#sea i.b", {{ scale: 2.6 }}, {{ scale: 1, duration: 0.5, ease: "expo.out", immediateRender: false }}, tz + 0.45);
      const tt = {r("tysięcy")};
      tl.to("#sea i:not(.b)", {{ opacity: 1, duration: 0.3, stagger: {{ each: 0.0011, from: "random" }} }}, tz + 0.7);
      tl.to("#sea i:not(.b)", {{ backgroundColor: "#c7c7cc", duration: 0.4 }}, tt - 0.1);
      K.lift("#lg", tt + 0.6, {{ y: 14, dur: 0.4 }});""", """
      .news { left: 0; top: 0; width: 1920px; height: 1080px; display: flex; align-items: center; justify-content: center; gap: 36px; transform-origin: 50% 50%; }
      .nw { width: 560px; padding: 44px 46px; border-radius: 32px; background: #fff; box-shadow: 0 24px 64px rgba(0,0,0,0.14); }
      .nw .src { font-size: 28px; font-weight: 600; color: var(--grey); margin-bottom: 16px; }
      .nw .ht { font-size: 56px; font-weight: 800; letter-spacing: -0.035em; line-height: 1.08; }
      .sea { left: 135px; top: 165px; width: 1680px; height: 720px; }
      .sea i { position: absolute; width: 16px; height: 16px; border-radius: 50%; background: #d8d8de; }
      .sea i.b { background: var(--blue); width: 22px; height: 22px; margin: -3px 0 0 -3px; }
      .lg { left: 135px; top: 930px; font-size: 38px; font-weight: 600; display: flex; align-items: center; gap: 16px; }
      .lg .bd, .lg .gd { width: 26px; height: 26px; border-radius: 50%; background: var(--blue); display: inline-block; }
      .lg .gd { background: #d8d8de; margin-left: 36px; }""")

# ================================================================ 28 · B the route to the first złoty keeps getting longer
a = W("zanim zarobisz", 286.4) - 0.1; b = W("ten model", 296.7) - 0.06; r = R(a)
stops = [("Produkt", "produkt"), ("Serwery", "serwery"), ("Marketing", "marketing"), ("Błędy", "błędy"), ("Zgłoszenia", "zgłoszenia"), ("Konkurencja", "konkurować")]
st = "".join(f'<div class="stp" id="s{i}"><i></i><span>{n}</span></div>' for i, (n, _) in enumerate(stops))
sc("S28", a, b, "B", f"""
      <div class="cam" id="cam">
        <div class="abs hd"><div class="lab" style="font-size:36px">Trasa do</div><div class="h-l" id="h1">pierwszej złotówki</div></div>
        <div class="abs road"><div class="ln" id="ln"></div><div class="start"><i></i><span>Start</span></div><div class="stops" id="stops">{st}</div>
          <div class="goal" id="goal"><b>1 zł</b></div></div>
        <div class="abs eta" id="eta"><span class="lab">Przystanki</span><b id="cnt">0</b></div>
      </div>""", f"""
      K.push(DUR, 1.03);
      K.rise("#h1", 0.05);
      K.lift(".start, #goal", 0.0, {{ y: 20, dur: 0.45 }}); K.lift("#eta", 0.2, {{ y: 14, dur: 0.4 }});
      tl.set(".stp", {{ width: 0, opacity: 0 }}, 0);
      {"".join(f'tl.to("#s{i}", {{ width: 236, opacity: 1, duration: 0.35, ease: "power3.out" }}, {r(w)} - 0.15); K.count("#cnt", {i}, {i + 1}, {r(w)} - 0.1, 0.2, (v) => String(Math.round(v))); ' for i, (_, w) in enumerate(stops))}
      tl.to("#goal", {{ x: 260, duration: 0.6, ease: "power2.inOut" }}, {r("konkurować")} + 0.2);
      tl.to("#goal", {{ opacity: 0.4, duration: 0.3 }}, {r("inwestorów")} - 0.2);""", """
      .hd { left: 150px; top: 150px; }
      .hd .h-l { font-size: 120px; }
      .road { left: 120px; top: 520px; width: 1700px; height: 240px; display: flex; align-items: center; }
      .ln { position: absolute; left: 30px; right: -400px; top: 98px; height: 8px; border-radius: 4px; background: #d2d2d7; }
      .start, .stp, .goal { position: relative; flex: none; display: flex; flex-direction: column; align-items: center; gap: 22px; }
      .start { width: 150px; } .start i { width: 40px; height: 40px; border-radius: 50%; background: var(--ink); display: block; margin-top: 78px; }
      .start span, .stp span { font-size: 33px; font-weight: 700; white-space: nowrap; }
      .stops { display: flex; }
      .stp { overflow: hidden; } .stp i { width: 30px; height: 30px; border-radius: 50%; background: #fff; border: 7px solid var(--blue); display: block; margin-top: 85px; }
      .goal { width: 200px; } .goal b { margin-top: 64px; padding: 16px 30px; border-radius: 999px; background: var(--green); color: #fff; font-size: 44px; font-weight: 900; }
      .eta { right: 150px; top: 130px; text-align: right; } .eta b { display: block; font-size: 150px; font-weight: 900; letter-spacing: -0.06em; line-height: 1; }""")

# ================================================================ 29 · K Model 3: Produkty cyfrowe ⭐
a = W("i teraz model", 309) - 0.1; b = W("jeżeli nie znasz", 312.2) - 0.06; r = R(a)
sc("S29", a, b, "K", models_card(done=(1, 2)), f"""
      K.card(DUR);
      tl.set("#mn1, #mn2", {{ backgroundColor: "#c7c7cc" }}, 0);
      const tu = {r("produkty")};
      tl.to("#mt3", {{ filter: "blur(0px)", opacity: 1, color: "#0071e3", duration: 0.35, ease: "power2.out" }}, tu - 0.2);
      tl.to("#mn3", {{ backgroundColor: "#0071e3", scale: 1.15, duration: 0.25, yoyo: true, repeat: 1 }}, tu - 0.2);
      tl.to("#mt3", {{ scale: 1.06, transformOrigin: "left center", duration: 0.2, yoyo: true, repeat: 1 }}, {r("cyfrowe")});""", MODELS_CSS)

# ================================================================ 30 · B Mail: pays → access lands right away
a = W("jeżeli nie znasz", 312.2) - 0.06; b = W("czyli poradnik", 317.9) - 0.06; r = R(a)
old = [("Newsletter", "Nowości w tym tygodniu", "wt."), ("Bank", "Wyciąg za wrzesień", "pon."), ("Kalendarz", "Przypomnienie: spotkanie", "pon.")]
om = "".join(f'<div class="ml"><b>{f}</b><span>{s_}</span><em>{d}</em></div>' for f, s_, d in old)
sc("S30", a, b, "B", f"""
      <div class="cam" id="cam">
        <div class="abs hd"><div class="lab" id="h0" style="font-size:40px;margin-bottom:10px">Produkt cyfrowy</div><div class="h-l w300" id="h1">Kupuje.</div><div class="h-l" id="h2">Dostęp od razu.</div></div>
        <div class="abs pay" id="pay"><div class="pc">✓</div><div><b>Płatność przyjęta</b><span>Produkt cyfrowy</span></div></div>
        <div class="card mbox" id="mb"><div class="mh">Skrzynka odbiorcza</div>
          <div class="ml new" id="nm"><i class="dot"></i><b>Twój sklep</b><span>Twój dostęp do produktu — kliknij i zacznij</span><em>teraz</em></div>{om}</div>
      </div>""", f"""
      K.push(DUR, 1.03);
      K.lift("#mb", 0.0, {{ y: 40, dur: 0.55, ease: "expo.out" }}); K.rise("#h0", 0.05, {{ stagger: 0.04 }});
      K.rise("#h1", {r("kupuje")} - 0.15);
      K.lift("#pay", {r("kupuje")} - 0.05, {{ y: -30, s: 0.9, dur: 0.45, ease: "expo.out" }});
      tl.set("#nm", {{ height: 0, opacity: 0, padding: 0 }}, 0);
      const td = {r("dostęp")};
      tl.to("#nm", {{ height: 118, opacity: 1, padding: "0 34px", duration: 0.45, ease: "expo.out" }}, td - 0.2);
      tl.fromTo("#nm", {{ backgroundColor: "#e8f1fd" }}, {{ backgroundColor: "#ffffff", duration: 1.4, immediateRender: false }}, td + 0.3);
      K.rise("#h2", td - 0.1, {{ stagger: 0.05 }});""", """
      .hd { left: 150px; top: 380px; }
      .pay { left: 150px; top: 150px; display: flex; align-items: center; gap: 22px; padding: 22px 34px 22px 22px; border-radius: 26px; background: var(--fill); }
      .pay .pc { width: 66px; height: 66px; border-radius: 50%; background: var(--green); color: #fff; font-size: 0; position: relative; }
      .pay .pc::after { content: ""; position: absolute; left: 21px; top: 13px; width: 16px; height: 30px; border: solid #fff; border-width: 0 7px 7px 0; transform: rotate(45deg); }
      .pay b { display: block; font-size: 34px; font-weight: 800; } .pay span { font-size: 26px; color: var(--grey); font-weight: 500; }
      .mbox { left: 960px; top: 140px; width: 820px; padding: 34px 0 20px; overflow: hidden; }
      .mh { font-size: 46px; font-weight: 800; letter-spacing: -0.03em; padding: 0 34px 18px; }
      .ml { position: relative; height: 118px; padding: 0 34px; border-top: 1px solid var(--line); display: flex; flex-direction: column; justify-content: center; overflow: hidden; }
      .ml b { font-size: 32px; font-weight: 700; } .ml span { font-size: 26px; color: var(--grey); white-space: nowrap; }
      .ml em { position: absolute; right: 34px; top: 24px; font-style: normal; font-size: 24px; color: var(--grey); }
      .ml.new b { font-weight: 900; } .ml.new span { color: #3a3a3c; } .ml.new em { color: var(--blue); font-weight: 700; }
      .ml .dot { position: absolute; left: 12px; top: 50px; width: 14px; height: 14px; border-radius: 50%; background: var(--blue); }""")

# ================================================================ 31 · K what a digital product is: file tiles
a = W("czyli poradnik", 317.9) - 0.06; b = W("coś co", 320.9) + 0.2; r = R(a)
FI = {"doc": '<path d="M18 10 H38 L48 20 V54 H18 Z" fill="none" stroke="#fff" stroke-width="4" stroke-linejoin="round"/><path d="M25 30 H41 M25 38 H41 M25 46 H35" stroke="#fff" stroke-width="4" stroke-linecap="round"/>',
      "tpl": '<rect x="12" y="14" width="40" height="36" rx="5" fill="none" stroke="#fff" stroke-width="4"/><path d="M12 26 H52 M26 26 V50" stroke="#fff" stroke-width="4"/>',
      "vid": '<rect x="10" y="16" width="44" height="32" rx="7" fill="none" stroke="#fff" stroke-width="4"/><path d="M28 24 L40 32 L28 40 Z" fill="#fff"/>',
      "sht": '<rect x="12" y="12" width="40" height="40" rx="5" fill="none" stroke="#fff" stroke-width="4"/><path d="M12 25 H52 M12 38 H52 M26 12 V52 M39 12 V52" stroke="#fff" stroke-width="3"/>',
      "pln": '<path d="M16 20 L20 24 L28 16 M16 36 L20 40 L28 32" fill="none" stroke="#fff" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/><path d="M34 20 H48 M34 36 H48" stroke="#fff" stroke-width="4" stroke-linecap="round"/>',
      "pdf": '<path d="M18 10 H38 L48 20 V54 H18 Z" fill="none" stroke="#fff" stroke-width="4" stroke-linejoin="round"/><text x="33" y="44" font-family="Inter" font-weight="800" font-size="13" fill="#fff" text-anchor="middle">PDF</text>'}
files = [("Poradnik", "doc", "#1d1d1f", "poradnik"), ("Szablon", "tpl", "#5e5ce6", "szablon"), ("Kurs wideo", "vid", "#ff3b30", "kurs"),
         ("Arkusz", "sht", "#34c759", "arkusz"), ("Plan", "pln", "#ff9500", "plan"), ("PDF", "pdf", "#0071e3", "pdf")]
fh = "".join(f'<div class="fl" id="f{i}"><div class="fi" style="background:{c}"><svg viewBox="0 0 64 64">{FI[k]}</svg></div><span>{n}</span></div>' for i, (n, k, c, _) in enumerate(files))
sc("S31", a, b, "K", f"""
      <div class="card ovc" style="width:700px"><div class="lab" style="margin-bottom:18px">Produkt cyfrowy to np.</div><div class="fg">{fh}</div></div>""", f"""
      K.card(DUR);
      {"".join(f'tl.fromTo("#f{i}", {{ opacity: 0.18, scale: 0.9 }}, {{ opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2.2)", immediateRender: true }}, {r(w)} - 0.12); ' for i, (*_, w) in enumerate(files))}""", """
      .fg { display: grid; grid-template-columns: repeat(3, 1fr); gap: 26px 18px; }
      .fl { display: flex; flex-direction: column; align-items: center; gap: 12px; }
      .fi { width: 130px; height: 130px; border-radius: 30px; display: flex; align-items: center; justify-content: center; }
      .fi svg { width: 80px; height: 80px; }
      .fl span { font-size: 32px; font-weight: 700; letter-spacing: -0.02em; }""")

# ================================================================ 32 · B no shipping, no warehouse, no „parcel didn't arrive” call
a = W("i nic tutaj", 324) - 0.08; b = W("i teraz dajmy", 328) - 0.06; r = R(a)
BOX = '<svg viewBox="0 0 64 64" width="90" height="90"><path d="M10 20 L32 10 L54 20 V46 L32 56 L10 46 Z M10 20 L32 30 L54 20 M32 30 V56" fill="none" stroke="#1d1d1f" stroke-width="4" stroke-linejoin="round"/></svg>'
WH = '<svg viewBox="0 0 64 64" width="90" height="90"><path d="M8 26 L32 12 L56 26 V54 H8 Z" fill="none" stroke="#1d1d1f" stroke-width="4" stroke-linejoin="round"/><path d="M20 54 V36 H44 V54 M20 44 H44" stroke="#1d1d1f" stroke-width="4"/></svg>'
sc("S32", a, b, "B", f"""
      <div class="cam" id="cam">
        <div class="abs tl2"><div class="panel tt" id="t1">{BOX}<div><div class="lab">Wysyłka</div><b id="v1">—</b></div></div>
          <div class="panel tt" id="t2">{WH}<div><div class="lab">Magazyn</div><b id="v2">—</b></div></div></div>
        <div class="abs call" id="call"><div class="cav">K</div><div class="cn">Klient</div><div class="cs">„Paczka nie doszła!”</div>
          <div class="cb"><div class="btn r" id="dec"><svg viewBox="0 0 64 64"><path d="M14 36 C 22 26 42 26 50 36 L46 42 L38 38 V32 C 34 30 30 30 26 32 V38 L18 42 Z" fill="#fff" transform="rotate(0 32 32)"/></svg></div><div class="btn g"><svg viewBox="0 0 64 64"><path d="M14 36 C 22 26 42 26 50 36 L46 42 L38 38 V32 C 34 30 30 30 26 32 V38 L18 42 Z" fill="#fff" transform="rotate(-135 32 34)"/></svg></div></div></div>
      </div>""", f"""
      K.push(DUR, 1.03);
      K.lift("#t1", 0.0, {{ y: 30, dur: 0.45, ease: "expo.out" }}); K.lift("#t2", 0.1, {{ y: 30, dur: 0.45, ease: "expo.out" }});
      const tw = {r("wysyłasz")}, tm = {r("magazynu")};
      K.frame((T) => {{ document.getElementById("v1").textContent = T >= tw - 0.1 ? "0" : "—"; document.getElementById("v2").textContent = T >= tm - 0.1 ? "0" : "—"; }});
      tl.fromTo("#v1", {{ scale: 1.5, color: "#ff3b30" }}, {{ scale: 1, color: "#1d1d1f", duration: 0.35, immediateRender: false }}, tw - 0.1);
      tl.fromTo("#v2", {{ scale: 1.5, color: "#ff3b30" }}, {{ scale: 1, color: "#1d1d1f", duration: 0.35, immediateRender: false }}, tm - 0.1);
      const tc = {r("dzwoni")};
      K.lift("#call", tc - 0.4, {{ y: 60, dur: 0.45, ease: "expo.out" }});
      tl.to(".cav", {{ scale: 1.08, duration: 0.25, yoyo: true, repeat: 3, ease: "sine.inOut" }}, tc);
      tl.to("#dec", {{ scale: 0.86, duration: 0.08, yoyo: true, repeat: 1 }}, {r("doszła")} - 0.05);
      tl.to("#call", {{ y: 80, opacity: 0, duration: 0.3, ease: "power2.in" }}, {r("doszła")} + 0.12);""", """
      .tl2 { left: 150px; top: 200px; display: flex; flex-direction: column; gap: 36px; }
      .tt { position: relative; width: 720px; height: 290px; padding: 0 48px; display: flex; align-items: center; gap: 40px; }
      .tt b { display: block; font-size: 140px; font-weight: 900; letter-spacing: -0.05em; line-height: 1; transform-origin: left center; }
      .call { left: 1010px; top: 110px; width: 760px; height: 860px; border-radius: 60px; background: #1d1d1f; color: #fff; display: flex; flex-direction: column; align-items: center; padding-top: 110px; }
      .cav { width: 180px; height: 180px; border-radius: 50%; background: #8e8e93; font-size: 84px; font-weight: 700; display: flex; align-items: center; justify-content: center; }
      .cn { font-size: 64px; font-weight: 700; margin-top: 30px; } .cs { font-size: 40px; color: #c7c7cc; margin-top: 10px; }
      .cb { display: flex; gap: 220px; margin-top: auto; margin-bottom: 110px; }
      .btn { width: 150px; height: 150px; border-radius: 50%; display: flex; align-items: center; justify-content: center; } .btn svg { width: 90px; height: 90px; }
      .btn.r { background: var(--red); } .btn.g { background: var(--green); }""")

# ================================================================ 33 · B question #3: pause pressed → sales keep coming ⭐
a = W("co się dzieje", 330.5) - 0.1; b = W("robisz go", 335) - 0.08; r = R(a)
pts = []
for i in range(0, 61):
    x = 160 + i * 26.7; y = 960 - (i * 5.6 + 18 * math.sin(i * 0.9) + 30)
    pts.append(f"{x:.0f},{y:.0f}")
line = "M" + " L".join(pts)
sales = "".join(f'<div class="sl" id="sl{i}">+ sprzedaż</div>' for i in range(5))
sc("S33", a, b, "B", f"""
      <div class="cam" id="cam">
        <div class="abs pb" id="pb"><div class="tap" id="tp" style="left:50%;top:50%"></div>{PAUSE}</div>
        <div class="abs qq" id="qq"><div class="h-l w300" id="q1">Co się dzieje,</div><div class="h-l" id="q2">kiedy przestajesz pracować?</div></div>
        <svg class="abs" style="left:0;top:0" width="1920" height="1080"><path id="rv" d="{line}" fill="none" stroke="#34c759" stroke-width="9" stroke-linejoin="round" stroke-linecap="round"/></svg>
        <div class="abs sls">{sales}</div>
      </div>""", f"""
      K.push(DUR, 1.03);
      K.lift("#pb", 0.0, {{ y: 0, s: 0.7, dur: 0.4, ease: "expo.out" }});
      K.rise("#q1", 0.02, {{ stagger: 0.05 }}); K.rise("#q2", {r("kiedy")} - 0.12, {{ stagger: 0.05 }});
      const tp = {r("przestajesz")};
      tl.to("#pb", {{ scale: 0.88, duration: 0.09, yoyo: true, repeat: 1, ease: "power2.in" }}, tp); K.tap("#tp", tp);
      tl.to("#pb", {{ backgroundColor: "#0071e3", duration: 0.2 }}, tp + 0.05);
      K.draw("#rv", tp + 0.3, DUR - tp - 0.4, "none");
      [0, 1, 2, 3, 4].forEach((i) => tl.fromTo("#sl" + i, {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.3, ease: "expo.out", immediateRender: true }}, {r("sprzedaje")} - 0.1 + i * 0.45));""", """
      .pb { left: 860px; top: 110px; width: 200px; height: 200px; border-radius: 50%; background: var(--ink); display: flex; align-items: center; justify-content: center; }
      .pb svg { width: 120px; height: 120px; }
      .qq { left: 0; top: 380px; width: 1920px; text-align: center; }
      .sls { right: 150px; top: 620px; display: flex; flex-direction: column; align-items: flex-end; gap: 12px; }
      .sl { padding: 12px 30px; border-radius: 999px; background: var(--green); color: #fff; font-size: 38px; font-weight: 800; }""")

# ================================================================ 33b · B make once, sell 100 / 1 000 / 10 000 times (AirDrop)
a = W("robisz go", 335) - 0.08; b = W("nie ma klienta", 338) - 0.06; r = R(a)
rays = "".join(f'<div class="cp" id="c{i}" style="--a:{i * 30}deg"><svg viewBox="0 0 64 64"><path d="M18 10 H38 L48 20 V54 H18 Z" fill="#fff" stroke="#0071e3" stroke-width="4" stroke-linejoin="round"/></svg></div>' for i in range(12))
sc("S33b", a, b, "B", f"""
      <div class="cam" id="cam">
        <div class="abs ad">{rays}<div class="mf" id="mf"><svg viewBox="0 0 64 64"><path d="M18 10 H38 L48 20 V54 H18 Z" fill="#0071e3"/><path d="M38 10 V20 H48" fill="#5aa4ff"/></svg></div></div>
        <div class="abs ct"><div class="lab" style="font-size:36px">Zrobiony raz. Sprzedany</div><div class="big"><span id="n">1</span>×</div></div>
      </div>""", f"""
      K.push(DUR, 1.04);
      K.lift("#mf", 0.0, {{ y: 0, s: 0.6, dur: 0.4, ease: "back.out(2)" }}); K.lift(".ct", 0.05, {{ y: 20, dur: 0.4 }});
      const T = [{r("100")}, {r("1000")}, {r("10 tysięcy")}];
      K.count("#n", 1, 100, T[0] - 0.25, 0.3, (v) => K.pl(v)); K.count("#n", 100, 1000, T[1] - 0.2, 0.3, (v) => K.pl(v)); K.count("#n", 1000, 10000, T[2] - 0.2, 0.35, (v) => K.pl(v));
      document.querySelectorAll(".cp").forEach((c, i) => {{
        const ang = (i * 30) * Math.PI / 180, d = 520;
        tl.fromTo(c, {{ x: 0, y: 0, opacity: 0, scale: 0.4 }}, {{ x: Math.cos(ang) * d, y: Math.sin(ang) * d * 0.62, opacity: 1, scale: 1, duration: 0.6, ease: "expo.out", immediateRender: true }}, T[0] - 0.2 + (i % 4) * 0.05 + Math.floor(i / 4) * (T[i < 4 ? 0 : i < 8 ? 1 : 2] - T[0]) * 0 + (i < 4 ? 0 : i < 8 ? T[1] - T[0] : T[2] - T[0]));
      }});""", """
      .ad { left: 960px; top: 430px; width: 0; height: 0; }
      .mf { position: absolute; left: -160px; top: -160px; width: 320px; height: 320px; }
      .mf svg { width: 320px; height: 320px; }
      .cp { position: absolute; left: -65px; top: -65px; width: 130px; height: 130px; } .cp svg { width: 130px; height: 130px; }
      .ct { left: 0; top: 820px; width: 1920px; text-align: center; }
      .big { font-size: 150px; font-weight: 900; letter-spacing: -0.06em; line-height: 1; }""")

# ================================================================ 34 · B lock screen at 6:00 full of overnight sales ⭐
a = W("ja na przykład", 346.7) - 0.1; b = W("wstaję", 352.6) - 0.06; r = R(a)
times = ["5:41", "4:58", "4:12", "3:27", "2:50", "1:16"]
nn = "".join(f'<div class="noti n2" id="n{i}"><div class="si2">{CHECK}</div><div><b>Nowa sprzedaż</b><span>Produkt cyfrowy · {t}</span></div></div>' for i, t in enumerate(times))
sc("S34", a, b, "B", f"""
      <div class="cam" id="cam">
        <div class="abs hd34"><div class="h-l w300" id="h1">Budzę się rano…</div><div class="h-l" id="h2">a sprzedaż już była.</div></div>
        <div class="phone" style="left:1260px;top:90px"><div class="scr" style="background:#e9ecf2">
          <div class="di"></div>
          <div class="ls"><div class="dt">wtorek, 13 października</div><div class="tm" id="tm">5:59</div></div>
          <div class="stack">{nn}</div><div class="more" id="more">+ 9 kolejnych</div>
        </div></div>
      </div>""", f"""
      K.push(DUR, 1.04);
      K.lift(".phone", 0.0, {{ y: 60, dur: 0.6, ease: "expo.out" }});
      K.rise("#h1", {r("obudziłem")} - 0.2); K.rise("#h2", {r("nocy")} - 0.25, {{ stagger: 0.05 }});
      K.count("#tm", 0, 0, {r("rano")} - 0.2, 0.01, () => "6:00");
      tl.fromTo("#tm", {{ scale: 1 }}, {{ scale: 1.08, duration: 0.15, yoyo: true, repeat: 1, immediateRender: false }}, {r("rano")} - 0.2);
      const t0 = {r("zobaczyłem")} - 0.3;
      [0, 1, 2, 3, 4, 5].forEach((i) => tl.fromTo("#n" + i, {{ opacity: 0, y: -40, scale: 0.95 }}, {{ opacity: 1, y: 0, scale: 1, duration: 0.35, ease: "expo.out", immediateRender: true }}, t0 + i * 0.16));
      K.lift("#more", t0 + 1.1, {{ y: 10, dur: 0.3 }});""", """
      .hd34 { left: 150px; top: 380px; }
      .ls { position: absolute; left: 0; right: 0; top: 80px; text-align: center; }
      .ls .dt { font-size: 24px; font-weight: 600; color: #3a3a3c; }
      .ls .tm { font-size: 112px; font-weight: 700; letter-spacing: -0.04em; line-height: 1; }
      .stack { position: absolute; left: 0; right: 0; top: 270px; }
      .n2 { position: relative !important; left: auto !important; right: auto !important; margin: 0 22px 10px; height: 82px; }
      .si2 { width: 50px; height: 50px; border-radius: 12px; background: var(--green); display: flex; align-items: center; justify-content: center; flex: none; }
      .si2 svg { width: 26px; height: 24px; }
      .more { position: absolute; left: 0; right: 0; top: 836px; text-align: center; font-size: 22px; color: #3a3a3c; font-weight: 600; }""")

# ================================================================ 35 · K world clock: Floryda 6:00 · Polska 12:00
a = W("wstaję", 352.6) - 0.06; b = W("i to mam", 356.7) - 0.06; r = R(a)
sc("S35", a, b, "K", """
      <div class="card ovc" style="width:640px"><div class="lab">Zegar</div>
        <div class="wc" id="w1"><div><span>Floryda</span><em>dziś, −6 godz.</em></div><b>6:00</b></div>
        <div class="wc" id="w2"><div><span>Polska</span><em>dziś</em></div><b class="blue">12:00</b></div></div>""", f"""
      K.card(DUR);
      K.lift("#w1", 0.12, {{ y: 14, dur: 0.35 }}); K.lift("#w2", 0.22, {{ y: 14, dur: 0.35 }});
      tl.fromTo("#w1 b", {{ scale: 1 }}, {{ scale: 1.12, transformOrigin: "right center", duration: 0.18, yoyo: true, repeat: 1, immediateRender: false }}, {r("6")} - 0.1);
      tl.fromTo("#w2 b", {{ scale: 1 }}, {{ scale: 1.12, transformOrigin: "right center", duration: 0.18, yoyo: true, repeat: 1, immediateRender: false }}, {r("12")} - 0.1);""", """
      .wc { display: flex; justify-content: space-between; align-items: center; padding: 22px 0; border-top: 1px solid var(--line); }
      .wc span { display: block; font-size: 44px; font-weight: 700; letter-spacing: -0.02em; } .wc em { font-style: normal; font-size: 26px; color: var(--grey); }
      .wc b { font-size: 96px; font-weight: 300; letter-spacing: -0.04em; }""")

# ================================================================ 36 · A+ sold itself, delivered itself, money in the account
a = W("produkt się sprzedał", 358.5) - 0.12; b = W("i to nie jest", 361.8) - 0.06; r = R(a)
sc("S36", a, b, "K", """
      <div class="wall" style="top:200px">
        <div class="wr" id="r1"><i class="ck"></i><span>sprzedał się sam</span></div>
        <div class="wr" id="r2"><i class="ck"></i><span>sam się dostarczył</span></div>
        <div class="wr" id="r3"><i class="ck"></i><span>pieniądze na koncie</span></div></div>""", f"""
      [["#r1", {r("sprzedał")}], ["#r2", {r("dostarczył")}], ["#r3", {r("pieniądze")}]].forEach(([s, t]) => {{ K.lift(s, t - 0.15, {{ y: 24, dur: 0.35, ease: "expo.out" }});
        tl.fromTo(s + " .ck", {{ scale: 0 }}, {{ scale: 1, duration: 0.3, ease: "back.out(3)", immediateRender: true }}, t); }});
      K.fadeOut(".wall", DUR - 0.28, {{ y: -16, dur: 0.26 }});""", WALL_CSS + """
      .wr { display: flex; align-items: center; gap: 20px; font-size: 48px; font-weight: 800; letter-spacing: -0.035em; line-height: 1.5; white-space: nowrap; }
      .ck { width: 52px; height: 52px; border-radius: 50%; background: var(--green); display: block; position: relative; flex: none; }
      .ck::after { content: ""; position: absolute; left: 17px; top: 9px; width: 12px; height: 24px; border: solid #fff; border-width: 0 6px 6px 0; transform: rotate(45deg); }""")

# ================================================================ 37 · B scale bars: kilka tysięcy → kilkanaście milionów
a = W("są ludzie", 364.8) - 0.1; b = W("ale od razu", 370.9) - 0.06; r = R(a)
bars = [("kilka tys.", 26, "kilka"), ("kilkanaście tys.", 60, "kilkanaście"), ("kilkadziesiąt tys.", 150, "kilkadziesiąt"), ("kilkaset tys.", 420, "kilkaset"), ("kilkanaście mln", 2600, "milionów")]
bh = "".join(f'<div class="bc" id="b{i}"><i style="height:{h}px"></i><span>{l}</span></div>' for i, (l, h, _) in enumerate(bars))
sc("S37", a, b, "B", f"""
      <div class="cam" id="cam"><div class="abs hd"><div class="lab" style="font-size:36px">Ludzie robią na tym miesięcznie</div></div><div class="abs bars" id="bars">{bh}</div></div>""", f"""
      K.push(DUR, 1.0);
      K.lift(".hd", 0.0, {{ y: 14, dur: 0.4 }});
      tl.fromTo(".bc span", {{ opacity: 0 }}, {{ opacity: 0.25, duration: 0.3, stagger: 0.05, immediateRender: true }}, 0.05);
      {"".join(f'tl.fromTo("#b{i} i", {{ scaleY: 0 }}, {{ scaleY: 1, duration: {0.5 if i < 4 else 0.9}, ease: "power3.out", immediateRender: true }}, {r(w)} - 0.15); tl.to("#b{i} span", {{ opacity: 1, duration: 0.2 }}, {r(w)} - 0.1); ' for i, (_, _, w) in enumerate(bars))}
      tl.to("#b4 i", {{ backgroundColor: "#0071e3", duration: 0.3 }}, {r("milionów")});
      tl.to("#cam", {{ y: 260, duration: 1.1, ease: "power2.inOut" }}, {r("milionów")} - 0.1);""", """
      .hd { left: 150px; top: 120px; }
      .bars { left: 150px; top: 0; height: 900px; display: flex; align-items: flex-end; gap: 60px; }
      .bc { position: relative; width: 260px; display: flex; flex-direction: column; align-items: flex-start; }
      .bc i { display: block; width: 100%; background: var(--ink); border-radius: 16px 16px 4px 4px; transform-origin: bottom center; }
      .bc span { font-size: 36px; font-weight: 800; letter-spacing: -0.02em; margin-top: 16px; white-space: nowrap; }""")

# ================================================================ 38 · K honest footnote: first month usually little or nothing
a = W("to nie jest typowy", 373.8) - 0.1; b = W("to jest generalnie", 379.8) + 0.6; r = R(a)
mb = "".join(f'<div class="mb2" id="m{i}"><i style="height:{h}px"></i><span>{i + 1}.</span></div>' for i, h in enumerate([4, 18, 30, 52, 80, 120]))
sc("S38", a, b, "K", f"""
      <div class="card ovc" style="width:640px"><div class="lab">Uczciwie</div><div class="h-m" style="margin:4px 0 6px">Pierwszy miesiąc</div>
        <div class="t-s" id="t1" style="font-size:38px">zwykle: <b>mało albo 0 zł</b></div>
        <div class="mbs">{mb}</div><div class="lab" style="font-size:24px;margin-top:8px">miesiąc · przykład, nie obietnica</div></div>""", f"""
      K.card(DUR);
      tl.fromTo(".mb2 i", {{ scaleY: 0 }}, {{ scaleY: 1, duration: 0.4, stagger: 0.07, ease: "power3.out", immediateRender: true }}, 0.25);
      K.rise("#t1", {r("mało")} - 0.15, {{ stagger: 0.05 }});
      tl.to("#m0 i", {{ backgroundColor: "#ff3b30", height: 8, duration: 0.3 }}, {r("mało")});
      tl.to("#m0 span", {{ color: "#ff3b30", duration: 0.3 }}, {r("mało")});""", """
      .mbs { display: flex; align-items: flex-end; gap: 20px; height: 150px; margin-top: 22px; }
      .mb2 { display: flex; flex-direction: column; align-items: center; gap: 8px; width: 70px; }
      .mb2 i { display: block; width: 70px; border-radius: 10px 10px 3px 3px; background: #c7c7cc; transform-origin: bottom center; }
      .mb2 span { font-size: 24px; font-weight: 700; color: var(--grey); }""")

# ================================================================ 39 · B two lanes: products stack up, services reset to zero ⭐
a = W("równice", 380.9) - 0.1; b = W("i zanim", 389.9) - 0.06; r = R(a)
MON = 6
lane1 = "".join(f'<div class="col" id="p{m}">' + "".join(f'<i class="bk" style="bottom:{k * 34}px"></i>' for k in range(m + 1)) + "</div>" for m in range(MON))
lane2 = "".join(f'<div class="col" id="u{m}"><i class="ub"></i></div>' for m in range(MON))
sc("S39", a, b, "B", f"""
      <div class="cam" id="cam">
        <div class="abs ln1"><div class="lt"><b>Produkty</b><span>każdy zostaje i pracuje</span></div><div class="cols">{lane1}</div></div>
        <div class="abs ln2"><div class="lt"><b>Usługi</b><span>co miesiąc od zera</span></div><div class="cols">{lane2}</div></div>
        <div class="abs mo3">{"".join(f'<span>{m + 1}. mies.</span>' for m in range(MON))}</div>
      </div>""", f"""
      K.push(DUR, 1.03);
      K.lift(".ln1 .lt", 0.0, {{ y: 14, dur: 0.4 }});
      const tz = {r("zostaje")};
      for (let m = 0; m < {MON}; m++) tl.fromTo("#p" + m + " .bk", {{ scaleY: 0 }}, {{ scaleY: 1, duration: 0.2, stagger: 0.02, ease: "power2.out", immediateRender: true }}, 0.3 + m * (tz + 1.2) / {MON});
      K.lift(".ln2 .lt", {r("usługach")} - 0.4, {{ y: 14, dur: 0.4 }});
      const tu = {r("każdy miesiąc")};
      const nT = [{r("nową")}, {r("nową", W("nową", a) + 0.2)}, {r("nową", W("nową", a) + 0.5)}];
      for (let m = 0; m < {MON}; m++) {{ const t = tu - 0.2 + m * 0.62;
        tl.fromTo("#u" + m + " .ub", {{ height: 0 }}, {{ height: 120, duration: 0.3, ease: "power2.out", immediateRender: true }}, t);
        tl.to("#u" + m + " .ub", {{ backgroundColor: "#c7c7cc", duration: 0.2 }}, t + 0.45); }}
      tl.to(".ln2 .lt span", {{ color: "#ff3b30", duration: 0.25 }}, {r("zera")} - 0.1);""", """
      .ln1 { left: 150px; top: 120px; display: flex; align-items: flex-end; gap: 60px; height: 360px; }
      .ln2 { left: 150px; top: 600px; display: flex; align-items: flex-end; gap: 60px; height: 200px; }
      .lt { width: 420px; padding-bottom: 6px; } .lt b { display: block; font-size: 72px; font-weight: 900; letter-spacing: -0.045em; } .lt span { font-size: 34px; color: var(--grey); font-weight: 600; }
      .cols { display: flex; gap: 26px; align-items: flex-end; height: 100%; }
      .col { position: relative; width: 170px; height: 100%; }
      .bk { position: absolute; left: 0; width: 100%; height: 30px; border-radius: 8px; background: var(--blue); transform-origin: bottom center; display: block; }
      .ub { position: absolute; left: 0; bottom: 0; width: 100%; height: 0; border-radius: 12px 12px 4px 4px; background: var(--ink); display: block; }
      .mo3 { left: 630px; top: 830px; display: flex; gap: 26px; } .mo3 span { width: 170px; font-size: 28px; color: var(--grey); font-weight: 600; }""")

# ================================================================ 40 · K homework: search IG/TikTok in English
a = W("otwórz", 394.4) - 0.1; b = W("i szukaj", 402.4) - 0.06; r = R(a)
sc("S40", a, b, "K", """
      <div class="card ovc" style="width:660px"><div class="lab">Zadanie na dziś</div>
        <div class="aps"><img id="ig" src="assets/ig.png"><img id="tt" src="assets/tiktok.png"></div>
        <div class="sf"><svg viewBox="0 0 40 40" width="36" height="36"><circle cx="17" cy="17" r="11" fill="none" stroke="#86868b" stroke-width="4"/><path d="M26 26 L35 35" stroke="#86868b" stroke-width="4" stroke-linecap="round"/></svg><span id="q"></span><b class="caret"></b></div>
        <div class="lab" style="font-size:24px;margin-top:12px">po angielsku</div></div>""", f"""
      K.card(DUR);
      K.lift("#ig", {r("instagrama")} - 0.15, {{ y: 0, s: 0.6, dur: 0.35, ease: "back.out(2)" }}); K.lift("#tt", {r("tiktoka")} - 0.15, {{ y: 0, s: 0.6, dur: 0.35, ease: "back.out(2)" }});
      K.type("#q", {r("siłownia")} - 0.1, "", "gym", 0.2);
      K.type("#q", {r("gotowanie")} - 0.2, "gym", "", 0.1); K.type("#q", {r("gotowanie")} - 0.08, "", "cooking", 0.3);
      K.type("#q", {r("inwestowanie")} - 0.2, "cooking", "", 0.1); K.type("#q", {r("inwestowanie")} - 0.08, "", "investing", 0.35);
      K.type("#q", {r("nauka")} - 0.2, "investing", "", 0.1); K.type("#q", {r("nauka")} - 0.08, "", "learn english", 0.45);
      tl.fromTo(".caret", {{ opacity: 1 }}, {{ opacity: 0, duration: 0.35, repeat: 18, yoyo: true, ease: "steps(1)" }}, 0);""", """
      .aps { display: flex; gap: 20px; margin: 14px 0 20px; } .aps img { width: 110px; height: 110px; border-radius: 26px; }
      .sf { display: flex; align-items: center; gap: 16px; height: 96px; padding: 0 26px; border-radius: 22px; background: var(--fill); font-size: 46px; font-weight: 700; letter-spacing: -0.02em; }
      .caret { display: inline-block; width: 4px; height: 50px; background: var(--blue); margin-left: -12px; }""")

# ================================================================ 41 · B small account, one post way above its followers ⭐
a = W("małego konta", 403.6) - 0.1; b = W("nie szukaj", 410.9) - 0.06; r = R(a)
views = ["4,1 tys.", "6,8 tys.", "3,2 tys.", "5,5 tys.", "1,2 mln", "4,9 tys.", "7,3 tys.", "2,6 tys.", "5,1 tys."]
tiles = "".join(f'<div class="rl{" hit" if v.endswith("mln") else ""}" id="r{i}"><svg viewBox="0 0 24 24" width="26" height="26"><path d="M7 5 L19 12 L7 19 Z" fill="#fff"/></svg><b>{v}</b></div>' for i, v in enumerate(views))
sc("S41", a, b, "B", f"""
      <div class="cam" id="cam">
        <div class="abs prof"><div class="av"></div><div><div class="pn">mały profil</div><div class="fol"><b id="fc">10</b> tys. obserwujących</div></div></div>
        <div class="abs grid3" id="g">{tiles}</div>
        <div class="abs ex">przykład</div>
      </div>""", f"""
      K.push(DUR, 1.035);
      K.lift(".prof", 0.0, {{ y: 20, dur: 0.45, ease: "expo.out" }});
      const T = [{r("10")}, {r("15")}, {r("20")}, {r("50")}];
      K.count("#fc", 10, 15, T[1] - 0.15, 0.2, (v) => String(Math.round(v))); K.count("#fc", 15, 20, T[2] - 0.15, 0.2, (v) => String(Math.round(v)));
      K.count("#fc", 20, 50, T[3] - 0.15, 0.25, (v) => String(Math.round(v)));
      K.lift(".rl", 0.15, {{ y: 20, s: 0.95, dur: 0.35, stagger: 0.04, ease: "expo.out" }});
      const th = {r("dużo")};
      tl.to(".rl:not(.hit)", {{ opacity: 0.35, duration: 0.3 }}, th);
      tl.to(".rl.hit", {{ scale: 1.14, backgroundColor: "#0071e3", duration: 0.4, ease: "expo.out", zIndex: 5 }}, th - 0.05);""", """
      .prof { left: 150px; top: 380px; display: flex; align-items: center; gap: 30px; }
      .av { width: 150px; height: 150px; border-radius: 50%; background: #c7c7cc; }
      .pn { font-size: 40px; font-weight: 700; color: var(--grey); } .fol { font-size: 52px; font-weight: 500; letter-spacing: -0.02em; } .fol b { font-weight: 900; font-size: 72px; }
      .grid3 { left: 1000px; top: 90px; width: 760px; display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; }
      .rl { position: relative; height: 290px; border-radius: 14px; background: #3a3a3c; display: flex; align-items: flex-end; gap: 8px; padding: 18px; color: #fff; }
      .rl b { font-size: 30px; font-weight: 800; }
      .rl.hit b { font-size: 40px; }
      .ex { left: 150px; bottom: 60px; font-size: 22px; color: var(--grey); }""")

# ================================================================ 42 · B nobody served it yet → your first product (search: 0 results)
a = W("i bardzo często", 424.4) - 0.08; b = W("tylko że tutaj", 431.8) - 0.06; r = R(a)
sc("S42", a, b, "B", f"""
      <div class="cam" id="cam">
        <div class="abs sb3"><svg viewBox="0 0 40 40" width="44" height="44"><circle cx="17" cy="17" r="11" fill="none" stroke="#86868b" stroke-width="4"/><path d="M26 26 L35 35" stroke="#86868b" stroke-width="4" stroke-linecap="round"/></svg><span>kurs: ten temat po polsku</span></div>
        <div class="abs res" id="res"><div class="zero" id="z">0 wyników</div>
          <div class="pcard" id="pc"><div class="pi"><svg viewBox="0 0 64 64" width="90" height="90"><path d="M18 10 H38 L48 20 V54 H18 Z" fill="#fff"/></svg></div><div><div class="lab" style="color:var(--blue);font-weight:700">Nowość</div><div class="pt">Twój pierwszy produkt</div></div></div></div>
        <div class="abs tmr" id="tmr"><svg viewBox="0 0 40 40" width="40" height="40"><circle cx="20" cy="22" r="14" fill="none" stroke="#1d1d1f" stroke-width="4"/><path d="M20 22 V14 M15 4 H25" stroke="#1d1d1f" stroke-width="4" stroke-linecap="round"/></svg><b id="tv">0:00</b></div>
      </div>""", f"""
      K.push(DUR, 1.03);
      K.lift(".sb3", 0.0, {{ y: 20, dur: 0.45, ease: "expo.out" }});
      K.lift("#z", {r("nikt")} - 0.2, {{ y: 20, dur: 0.4, ease: "expo.out" }});
      const tp = {r("twój")};
      tl.to("#z", {{ opacity: 0, y: -20, duration: 0.25 }}, tp - 0.4);
      K.lift("#pc", tp - 0.2, {{ y: 60, s: 0.92, dur: 0.55, ease: "expo.out" }});
      K.lift("#tmr", {r("kilka minut")} - 0.3, {{ y: 14, dur: 0.35 }});
      K.count("#tv", 0, 240, {r("kilka minut")} - 0.3, 1.0, (v) => Math.floor(v / 60) + ":" + String(Math.floor(v % 60)).padStart(2, "0"), "power2.out");""", """
      .sb3 { left: 360px; top: 140px; width: 1200px; height: 120px; border-radius: 999px; background: var(--fill); display: flex; align-items: center; gap: 24px; padding: 0 44px; font-size: 48px; font-weight: 600; }
      .res { left: 360px; top: 330px; width: 1200px; height: 520px; display: flex; align-items: center; justify-content: center; }
      .zero { position: absolute; font-size: 120px; font-weight: 900; letter-spacing: -0.05em; color: #c7c7cc; }
      .pcard { display: flex; align-items: center; gap: 40px; padding: 44px 56px; border-radius: 36px; background: #fff; box-shadow: 0 24px 64px rgba(0,0,0,0.14); }
      .pi { width: 160px; height: 160px; border-radius: 36px; background: var(--blue); display: flex; align-items: center; justify-content: center; }
      .pt { font-size: 76px; font-weight: 900; letter-spacing: -0.045em; }
      .tmr { right: 150px; bottom: 120px; display: flex; align-items: center; gap: 14px; padding: 16px 30px; border-radius: 999px; background: var(--fill); }
      .tmr b { font-size: 48px; font-weight: 800; }""")

# ================================================================ 42b · A+ umiejętność → wypłata (wall)
a = W("ty masz", 443) - 0.12; b = W("a produkt", 448) - 0.06; r = R(a)
sc("S42b", a, b, "K", """
      <div class="wall" style="top:240px"><div class="wb2" id="l1">umiejętność</div><div class="wl" id="l2" style="font-size:64px">→ <span class="ws" id="ws"><span class="lo">wypłata</span><span class="hi" style="font-weight:900">wypłata</span></span></div>
        <div class="wl" id="l3" style="margin-top:20px">„tak pracowali rodzice”</div></div>""", f"""
      K.rise("#l1", {r("umiejętność")} - 0.15);
      K.lift("#l2", {r("płaci")} - 0.3, {{ y: 20, dur: 0.35 }}); K.weight("#ws", {r("płaci")});
      K.rise("#l3", {r("rodzice")} - 0.2, {{ stagger: 0.04 }});
      K.fadeOut(".wall", DUR - 0.28, {{ y: -16, dur: 0.26 }});""", WALL_CSS + """
      .wb2 { font-size: 92px; font-weight: 900; letter-spacing: -0.05em; }""")

# ================================================================ 43 · B Notes: the inner voice types itself ⭐
a = W("kim", 452) - 0.75; b = W("i powiem ci", 459.7) - 0.06; r = R(a)
lines = [("zwykły człowiek", "zwykłym"), ("zwykła praca", "zwykłą"), ("tylko student", "studentem"), ("tylko mama", "mamą"), ("zero certyfikatów", "certyfikatów"), ("kto mi za to zapłaci?", "kto")]
nl = "".join(f'<div class="nl" id="l{i}"><i></i><span id="y{i}"></span></div>' for i in range(len(lines)))
sc("S43", a, b, "B", f"""
      <div class="cam" id="cam">
        <div class="card notes"><div class="nb"><span>‹ Notatki</span><em>Gotowe</em></div>
          <div class="nt"><span id="tt"></span><b class="caret"></b></div><div class="nls">{nl}</div></div>
      </div>""", f"""
      K.push(DUR, 1.04);
      K.lift(".notes", 0.0, {{ y: 50, dur: 0.6, ease: "expo.out" }});
      K.type("#tt", {r("kim")} - 0.1, "", "Kim ja jestem, żeby kogoś uczyć?", 0.9);
      tl.set(".nl", {{ opacity: 0 }}, 0);
      {"".join(f'tl.to("#l{i}", {{ opacity: 1, duration: 0.05 }}, {r(w)} - 0.12); K.type("#y{i}", {r(w)} - 0.1, "", "{t}", {min(0.45, len(t) * 0.03):.2f}); ' for i, (t, w) in enumerate(lines))}
      tl.to("#l5", {{ color: "#ff3b30", duration: 0.2 }}, {r("zapłaci")});
      tl.fromTo(".caret", {{ opacity: 1 }}, {{ opacity: 0, duration: 0.35, repeat: 28, yoyo: true, ease: "steps(1)" }}, 0);""", """
      .notes { left: 410px; top: 70px; width: 1100px; height: 940px; padding: 40px 70px; }
      .nb { display: flex; justify-content: space-between; font-size: 34px; font-weight: 600; color: #e0a800; margin-bottom: 40px; } .nb em { font-style: normal; font-weight: 700; }
      .nt { font-size: 72px; font-weight: 800; letter-spacing: -0.035em; line-height: 1.1; min-height: 170px; }
      .caret { display: inline-block; width: 5px; height: 70px; background: #e0a800; margin-left: 4px; vertical-align: -8px; }
      .nl { display: flex; align-items: center; gap: 24px; font-size: 50px; font-weight: 500; letter-spacing: -0.02em; padding: 12px 0; }
      .nl i { width: 14px; height: 14px; border-radius: 50%; background: var(--ink); display: block; }""")

# ================================================================ 44 · B seller requirements form: all empty, he still sold at 14 ⭐
a = W("ja zacząłem", 465.3) - 0.1; b = W("podstawówki", 471) + 0.75; r = R(a)
sc("S44", a, b, "B", f"""
      <div class="cam" id="cam">
        <div class="card form"><div class="h-m">Kto może sprzedawać?</div>
          <div class="fr2" id="f0"><span>Wiek</span><b id="age">—</b></div>
          <div class="fr2" id="f1"><span>Certyfikaty</span><b class="no">brak</b></div>
          <div class="fr2" id="f2"><span>Dyplom</span><b class="no">brak</b></div>
          <div class="fr2" id="f3"><span>Podstawówka</span><b class="no">nieskończona</b></div>
          <div class="sell" id="sell">Sprzedaj</div></div>
      </div>""", f"""
      K.push(DUR, 1.03);
      K.lift(".form", 0.0, {{ y: 50, dur: 0.55, ease: "expo.out" }});
      const t14 = {r("14")};
      K.frame((T) => {{ const e = document.getElementById("age"); e.textContent = T < t14 - 0.3 ? "—" : String(Math.round(Math.min(1, (T - t14 + 0.3) / 0.4) * 14)) + " lat"; }});
      tl.fromTo("#age", {{ scale: 1.3, color: "#0071e3" }}, {{ scale: 1, color: "#1d1d1f", duration: 0.5, immediateRender: false }}, {r("14")} + 0.1);
      tl.set(".no", {{ opacity: 0 }}, 0);
      [["#f1 .no", {r("certyfikaty")}], ["#f2 .no", {r("dyplom")}], ["#f3 .no", {r("podstawówki")}]].forEach(([s, t]) => {{
        tl.fromTo(s, {{ opacity: 0, x: 20 }}, {{ opacity: 1, x: 0, duration: 0.3, ease: "expo.out", immediateRender: true }}, t - 0.15); }});
      tl.to("#sell", {{ backgroundColor: "#34c759", duration: 0.25 }}, {r("podstawówki")} + 0.3);
      tl.to("#sell", {{ scale: 0.95, duration: 0.08, yoyo: true, repeat: 1 }}, {r("podstawówki")} + 0.3);""", """
      .form { left: 460px; top: 90px; width: 1000px; padding: 56px 64px; }
      .fr2 { display: flex; justify-content: space-between; align-items: center; padding: 28px 0; border-top: 1px solid var(--line); font-size: 48px; }
      .fr2 span { font-weight: 600; color: #3a3a3c; } .fr2 b { font-weight: 800; transform-origin: right center; } .fr2 .no { color: var(--red); }
      .sell { margin-top: 30px; height: 120px; border-radius: 30px; background: var(--ink); color: #fff; font-size: 54px; font-weight: 800; display: flex; align-items: center; justify-content: center; }""")

# ================================================================ 45 · K kid with a laptop who knew how to go viral on Snapchat
a = 472.7; b = 476.75; r = lambda w, after=None: {"dzieciakiem": 472.82, "snapcie": 475.23, "vara": 474.82, "zadziałało": 476.02}[w] - a
sc("S45", a, b, "K", """
      <div class="card ovc" style="width:600px"><div class="sn"><div class="sni"><svg viewBox="0 0 64 64" width="88" height="88"><path d="M32 8 C 22 8 17 15 17 24 V30 L12 32 C 14 36 18 36 18 38 C 15 44 10 46 8 47 C 12 50 16 49 18 52 C 22 52 26 56 32 56 C 38 56 42 52 46 52 C 48 49 52 50 56 47 C 54 46 49 44 46 38 C 46 36 50 36 52 32 L47 30 V24 C 47 15 42 8 32 8 Z" fill="#fff" stroke="#1d1d1f" stroke-width="3" stroke-linejoin="round"/></svg></div>
        <div><div class="lab">Ja, 14 lat · Snapchat</div><div class="vw"><b id="v">0</b> wyświetleń</div></div></div>
        <div class="ok2" id="ok"><i class="ck"></i>zadziałało</div></div>""", f"""
      K.card(DUR);
      K.count("#v", 0, 1200000, {r("vara")} - 0.3, 0.9, (v) => K.pl(v), "power3.out");
      tl.fromTo("#ok", {{ opacity: 0, y: 14 }}, {{ opacity: 1, y: 0, duration: 0.35, ease: "expo.out", immediateRender: true }}, {r("zadziałało")} - 0.15);""", """
      .sn { display: flex; align-items: center; gap: 28px; }
      .sni { width: 130px; height: 130px; border-radius: 30px; background: #fffc00; display: flex; align-items: center; justify-content: center; flex: none; }
      .vw { font-size: 40px; font-weight: 500; } .vw b { font-size: 64px; font-weight: 900; letter-spacing: -0.04em; }
      .ok2 { display: flex; align-items: center; gap: 16px; margin-top: 22px; font-size: 44px; font-weight: 800; color: var(--green); }
      .ck { width: 48px; height: 48px; border-radius: 50%; background: var(--green); display: block; position: relative; flex: none; }
      .ck::after { content: ""; position: absolute; left: 16px; top: 8px; width: 11px; height: 22px; border: solid #fff; border-width: 0 6px 6px 0; transform: rotate(45deg); }""")

# ================================================================ 46 · B who did you learn from? professor vs one step ahead (cursor picks)
a = W("od profesora", 484.8) - 0.4; b = W("bo ludzie", 491.5) - 0.06; r = R(a)
sc("S46", a, b, "B", f"""
      <div class="cam" id="cam">
        <div class="abs hd"><div class="h-m w300" id="h1" style="font-size:72px">Od kogo ostatnio uczyłeś się w internecie?</div></div>
        <div class="abs two">
          <div class="pcd" id="c1"><div class="pav">P</div><div class="pnm">Profesor</div><div class="psb">40 lat stażu</div></div>
          <div class="pcd" id="c2"><div class="pav" style="background:#0071e3">K</div><div class="pnm">Ktoś</div><div class="psb">rok przed Tobą</div><div class="fb" id="fb">Obserwujesz ✓</div></div>
        </div>
        <svg class="cur" id="cur" viewBox="0 0 46 60">{'<path d="M4 3 L4 48 L15 37 L23 56 L31 52 L23 34 L39 34 Z" fill="#f4f6fa" stroke="#0a0d16" stroke-width="3" stroke-linejoin="round"/>'}</svg>
      </div>""", f"""
      K.push(DUR, 1.03);
      K.rise("#h1", 0.02, {{ stagger: 0.03 }});
      K.lift("#c1", {r("profesora")} - 0.2, {{ y: 40, dur: 0.5, ease: "expo.out" }});
      K.lift("#c2", {r("kogoś")} - 0.2, {{ y: 40, dur: 0.5, ease: "expo.out" }});
      const tk = {r("stoisz")};
      K.click("#cur", 1500, 1000, 1240, 760, tk - 1.0, tk - 0.1, "#c2");
      tl.set("#fb", {{ opacity: 0 }}, 0); tl.to("#fb", {{ opacity: 1, duration: 0.2 }}, tk - 0.05);
      tl.to("#c2", {{ boxShadow: "0 0 0 6px #0071e3, 0 24px 64px rgba(0,0,0,0.14)", duration: 0.25 }}, tk - 0.05);
      tl.to("#c1", {{ opacity: 0.4, duration: 0.3 }}, tk);""", """
      .hd { left: 150px; top: 110px; width: 1620px; }
      .two { left: 0; top: 290px; width: 1920px; display: flex; justify-content: center; gap: 80px; }
      .pcd { position: relative; width: 560px; height: 600px; border-radius: 40px; background: #fff; box-shadow: 0 24px 64px rgba(0,0,0,0.14); display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 14px; }
      .pav { width: 200px; height: 200px; border-radius: 50%; background: #8e8e93; color: #fff; font-size: 90px; font-weight: 800; display: flex; align-items: center; justify-content: center; margin-bottom: 12px; }
      .pnm { font-size: 72px; font-weight: 900; letter-spacing: -0.04em; } .psb { font-size: 40px; color: var(--grey); font-weight: 600; }
      .fb { margin-top: 16px; padding: 12px 30px; border-radius: 999px; background: var(--blue); color: #fff; font-size: 32px; font-weight: 700; }""")

# ================================================================ 47 · B one step ahead: two pairs with arcs
a = W("na przykład student", 497) - 0.1; b = W("ktoś kto na przykład", 504.9) - 0.06; r = R(a)
sc("S47", a, b, "B", """
      <div class="cam" id="cam">
        <svg class="abs" style="left:0;top:0" width="1920" height="1080">
          <path id="a1" d="M760,330 C 960,250 1060,250 1180,330" fill="none" stroke="#0071e3" stroke-width="6" stroke-linecap="round"/>
          <path id="a2" d="M760,720 C 960,640 1060,640 1180,720" fill="none" stroke="#0071e3" stroke-width="6" stroke-linecap="round"/>
        </svg>
        <div class="abs pr" style="top:250px"><div class="pa" id="p1">Student<br><span>2. rok</span></div><div class="pb2" id="q1">Maturzysta<br><span>materiały do matury</span></div></div>
        <div class="abs pr" style="top:640px"><div class="pa" id="p2">−10 kg<br><span>w zeszłym roku</span></div><div class="pb2" id="q2">Chce schudnąć<br><span>w tym roku</span></div></div>
        <div class="abs st1" id="s1">1 krok przed</div><div class="abs st1" id="s2" style="top:600px">1 krok przed</div>
      </div>""", f"""
      K.push(DUR, 1.03);
      tl.fromTo(".pa, .pb2", {{ opacity: 0 }}, {{ opacity: 0.12, duration: 0.3, immediateRender: true }}, 0.0);
      K.lift("#p1", 0.0, {{ y: 30, dur: 0.45, ease: "expo.out" }});
      K.draw("#a1", {r("matury")} - 0.6, 0.5); K.lift("#q1", {r("matury")} - 0.15, {{ y: 30, dur: 0.45, ease: "expo.out" }}); K.lift("#s1", {r("matury")}, {{ y: 10, dur: 0.3 }});
      K.lift("#p2", {r("ktoś")} - 0.15, {{ y: 30, dur: 0.45, ease: "expo.out" }});
      K.draw("#a2", {r("pomóc")} - 0.3, 0.5); K.lift("#q2", {r("pomóc")} + 0.1, {{ y: 30, dur: 0.45, ease: "expo.out" }}); K.lift("#s2", {r("pomóc")} + 0.25, {{ y: 10, dur: 0.3 }});""", """
      .pr { left: 150px; width: 1620px; display: flex; justify-content: space-between; }
      .pa, .pb2 { width: 600px; height: 190px; border-radius: 32px; padding: 0 44px; display: flex; flex-direction: column; justify-content: center; font-size: 64px; font-weight: 900; letter-spacing: -0.04em; line-height: 1.05; }
      .pa { background: var(--ink); color: #fff; } .pb2 { background: var(--fill); }
      .pa span, .pb2 span { font-size: 32px; font-weight: 600; letter-spacing: -0.01em; opacity: .7; }
      .st1 { left: 860px; top: 210px; width: 200px; text-align: center; font-size: 30px; font-weight: 800; color: var(--blue); }""")

# ================================================================ 48 · K you compete with your client's past self
a = W("więc nie konkurujesz", 508.9) - 0.1; b = W("a ai", 513.5) - 0.06; r = R(a)
sc("S48", a, b, "K", """
      <div class="card ovc" style="width:640px"><div class="lab">Konkurujesz z…</div>
        <div class="h-l" id="e1" style="font-size:96px">Ekspertem</div>
        <div class="h-l blue" id="e2" style="font-size:64px;margin-top:10px">klientem, który nie wie, od czego zacząć</div></div>""", f"""
      K.card(DUR);
      K.rise("#e1", 0.1); K.strike("#e1", {r("ekspertem")} + 0.1);
      K.rise("#e2", {r("wersją")} - 0.1, {{ stagger: 0.05 }});""")

# ================================================================ 49 · B calendar: months/years then → one Saturday ⭐
a = W("kiedyś największą", 514.8) - 0.1; b = W("wiedza jest", 525.3) - 0.06; r = R(a)
mths = ["sty", "lut", "mar", "kwi", "maj", "cze", "lip", "sie", "wrz", "paź", "lis", "gru"]
mg = "".join(f'<div class="mc" id="mo{i}"><span>{m}</span><i></i></div>' for i, m in enumerate(mths))
sc("S49", a, b, "B", f"""
      <div class="cam" id="cam">
        <div class="abs yv" id="yv"><div class="yh"><span class="w300">Kiedyś:</span> <b id="yr">rok</b></div><div class="mg">{mg}</div>
          <div class="legend"><span id="g1"><i style="background:#86868b"></i>Napisanie</span><span id="g2"><i style="background:#5e5ce6"></i>Projekt</span><span id="g3"><i style="background:#1d1d1f"></i>Złożenie</span></div></div>
        <div class="abs dv" id="dv"><div class="yh"><span class="w300">Dziś:</span> <b>sobota</b></div>
          <div class="day"><div class="hr">{"".join(f'<span style="top:{(h - 8) * 52}px">{h}:00</span>' for h in range(8, 23, 2))}</div>
          <div class="ev" id="ev"><b>Pierwsza wersja</b><span>9:00 – 21:00</span></div></div></div>
      </div>""", f"""
      K.push(DUR, 1.03);
      K.lift("#yv", 0.0, {{ y: 30, dur: 0.5, ease: "expo.out" }});
      const seg = [[0, 3, "#86868b", {r("napisanie")}], [3, 6, "#5e5ce6", {r("zaprojektowanie")}], [6, 12, "#1d1d1f", {r("złożenie")}]];
      seg.forEach(([s, e, c, t], k) => {{ K.lift("#g" + (k + 1), t - 0.15, {{ y: 10, dur: 0.3 }}); for (let i = s; i < e; i++) tl.fromTo("#mo" + i + " i", {{ scaleX: 0 }}, {{ scaleX: 1, backgroundColor: c, duration: 0.18, ease: "power2.out", immediateRender: true }}, t - 0.1 + (i - s) * 0.06); }});
      tl.set(".legend span", {{ opacity: 0 }}, 0);
      K.count("#yr", 0, 0, {r("miesiące")} - 0.1, 0.01, () => "miesiące");
      K.count("#yr", 0, 0, {r("lata")} - 0.1, 0.01, () => "lata");
      tl.fromTo("#yr", {{ color: "#1d1d1f" }}, {{ color: "#ff3b30", duration: 0.2, immediateRender: false }}, {r("lata")} - 0.1);
      const td = {r("dziś")};
      tl.to("#yv", {{ x: -1920, duration: 0.5, ease: "power3.inOut" }}, td - 0.3);
      tl.fromTo("#dv", {{ x: 1920 }}, {{ x: 0, duration: 0.5, ease: "power3.inOut", immediateRender: true }}, td - 0.3);
      tl.fromTo("#ev", {{ height: 0 }}, {{ height: 624, duration: 1.2, ease: "power2.inOut", immediateRender: true }}, {r("rano")} - 0.1);
      tl.fromTo("#ev", {{ backgroundColor: "#cfe3fb" }}, {{ backgroundColor: "#0071e3", duration: 0.3, immediateRender: false }}, {r("wersję")} - 0.2);
      tl.to("#ev b, #ev span", {{ color: "#fff", duration: 0.3 }}, {r("wersję")} - 0.2);""", """
      .yv, .dv { left: 150px; top: 100px; width: 1620px; }
      .yh { font-size: 96px; font-weight: 900; letter-spacing: -0.045em; margin-bottom: 36px; }
      .mg { display: grid; grid-template-columns: repeat(6, 1fr); gap: 20px; }
      .mc { height: 200px; border-radius: 24px; background: var(--fill); padding: 22px; display: flex; flex-direction: column; justify-content: space-between; }
      .mc span { font-size: 34px; font-weight: 700; } .mc i { display: block; height: 40px; border-radius: 10px; background: #c7c7cc; transform-origin: left center; transform: scaleX(0); }
      .legend { display: flex; gap: 40px; margin-top: 30px; font-size: 34px; font-weight: 700; }
      .legend i { display: inline-block; width: 26px; height: 26px; border-radius: 7px; margin-right: 12px; vertical-align: -3px; }
      .day { position: relative; height: 760px; border-top: 1px solid var(--line); }
      .hr span { position: absolute; left: 0; font-size: 28px; color: var(--grey); font-weight: 600; transform: translateY(-50%); }
      .ev { position: absolute; left: 160px; right: 0; top: 52px; border-radius: 22px; background: #cfe3fb; padding: 26px 34px; overflow: hidden; }
      .ev b { display: block; font-size: 60px; font-weight: 900; letter-spacing: -0.035em; color: #0058b0; } .ev span { font-size: 34px; font-weight: 600; color: #0058b0; }""")

# ================================================================ 50 · B four empty widgets: the model A to Z, #1 Produkt ⭐
a = W("teraz pokażę", 530) - 0.1; b = W("i największy", 534.6) - 0.06; r = R(a)
wd = "".join(f'<div class="wg2" id="w{i}"><div class="wn">{i + 1}</div><div class="wt" id="wt{i}">{n}</div></div>' for i, n in enumerate(["Produkt", "Sklep", "Content", "Drabinka"]))
sc("S50", a, b, "B", f"""
      <div class="cam" id="cam">
        <div class="abs hd"><div class="h-l w300" id="h1">Cały model.</div><div class="h-l" id="h2">Od A do Z.</div></div>
        <div class="abs wgs">{wd}</div>
      </div>""", f"""
      K.push(DUR, 1.035);
      K.rise("#h1", 0.02); K.rise("#h2", {r("od a")} - 0.15, {{ stagger: 0.06 }});
      tl.fromTo(".wg2", {{ opacity: 0, scale: 0.9 }}, {{ opacity: 1, scale: 1, duration: 0.4, stagger: 0.08, ease: "back.out(2)", immediateRender: true }}, 0.1);
      tl.to(".wn", {{ backgroundColor: "#1d1d1f", color: "#fff", duration: 0.15, stagger: 0.1, yoyo: true, repeat: 1 }}, {r("cztery")} - 0.1);
      tl.set(".wt", {{ opacity: 0 }}, 0);
      const tp = {r("produkt")};
      tl.to("#w0", {{ backgroundColor: "#0071e3", duration: 0.3 }}, tp - 0.15); tl.to("#w0 .wn", {{ color: "#fff", backgroundColor: "rgba(255,255,255,0.25)", duration: 0.3 }}, tp - 0.15);
      tl.fromTo("#wt0", {{ opacity: 0, y: 20 }}, {{ opacity: 1, y: 0, color: "#fff", duration: 0.35, ease: "expo.out", immediateRender: false }}, tp - 0.15);""", """
      .hd { left: 150px; top: 360px; }
      .wgs { left: 920px; top: 120px; display: grid; grid-template-columns: 400px 400px; gap: 40px; }
      .wg2 { height: 400px; border-radius: 56px; background: var(--fill); padding: 40px; display: flex; flex-direction: column; justify-content: space-between; }
      .wn { width: 76px; height: 76px; border-radius: 50%; background: #fff; font-size: 38px; font-weight: 800; display: flex; align-items: center; justify-content: center; color: var(--ink); }
      .wt { font-size: 64px; font-weight: 900; letter-spacing: -0.045em; }""")

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
