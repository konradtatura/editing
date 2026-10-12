#!/usr/bin/env python3
"""lfpdo Premium v3 — the full-screen (PEŁNY) scenes. L18, L21, L26 (pilot) are hand-written HTML files.
Times are scene-relative seconds taken from premium/words_per_scene.txt."""
import json, os
from page import page, HERE

IDX = {x["key"]: x for x in json.load(open(os.path.join(HERE, "..", "..", "index.json")))}
for k, (a, b) in json.load(open(os.path.join(HERE, "timing.json"))).items():
    IDX[k]["in"], IDX[k]["out"] = a, b
D = lambda k: round(IDX[k]["out"] - IDX[k]["in"], 3)
GEO = json.load(open(os.path.join(HERE, "geo_paths.json")))
CHK = ('<div class="chk"><div class="on"><svg viewBox="0 0 28 26"><path d="M3 13 L11 21 L25 4" fill="none" stroke="#fff" stroke-width="4.5" '
       'stroke-linecap="round" stroke-linejoin="round"/></svg></div><div class="off"><svg viewBox="0 0 24 24"><path d="M4 4 L20 20 M20 4 L4 20" '
       'fill="none" stroke="#fff" stroke-width="4.5" stroke-linecap="round"/></svg></div></div>')
DOC = ('<svg viewBox="0 0 64 80" class="doc"><path d="M6 4 H42 L58 20 V76 H6 Z" fill="none" stroke="currentColor" stroke-width="4" stroke-linejoin="round"/>'
       '<path d="M42 4 V20 H58" fill="none" stroke="currentColor" stroke-width="4" stroke-linejoin="round"/>'
       '<path d="M16 38 H48 M16 50 H48 M16 62 H36" stroke="currentColor" stroke-width="4" stroke-linecap="round"/></svg>')
S = {}

# L02 — „każdy zrobi produkt w 10–15 minut… ebooka, planera, checklistę, cokolwiek”
S["L02"] = dict(css="""
      .lab1 { left: 160px; top: 120px; }
      .clock { left: 152px; top: 190px; font-size: 300px; font-weight: 900; letter-spacing: -0.06em; line-height: 1; }
      .clock span { font-weight: 300; color: var(--mute); }
      .tiles { left: 160px; top: 560px; display: flex; gap: 40px; }
      .tile { width: 370px; height: 380px; padding: 44px; display: flex; flex-direction: column; justify-content: space-between; }
      .tile .doc { width: 72px; height: 90px; color: var(--mute); }
      .tile b { font-size: 58px; font-weight: 700; letter-spacing: -0.03em; display: block; }
      .tile small { font-size: 28px; color: var(--mute); font-weight: 500; }""", body=f"""
      <div class="cam" id="cam">
        <div class="abs t-s mute lab1" id="lab">Z AI każdy zrobi produkt w</div>
        <div class="abs clock" id="clk"><b id="mm">00:00</b> <span>min</span></div>
        <div class="abs tiles">
          <div class="tile surf" id="f1">{DOC}<div><b>Ebook</b><small>PDF · gotowy</small></div></div>
          <div class="tile surf" id="f2">{DOC}<div><b>Planer</b><small>PDF · gotowy</small></div></div>
          <div class="tile surf" id="f3">{DOC}<div><b>Checklista</b><small>PDF · gotowa</small></div></div>
          <div class="tile surf" id="f4">{DOC}<div><b>Cokolwiek</b><small>PDF · gotowe</small></div></div>
        </div>
      </div>""", js="""
      K.push(DUR, 1.04);
      K.rise("#lab", 0.1, { stagger: 0.04 });
      K.lift("#clk", 0.3, { y: 40, dur: 0.6, ease: "expo.out" });
      K.count("#mm", 0, 900, 0.45, 2.7, (v) => { v = Math.round(v); return String(Math.floor(v / 60)).padStart(2, "0") + ":" + String(v % 60).padStart(2, "0"); }, "power2.inOut");
      [["#f1", 4.38], ["#f2", 4.78], ["#f3", 5.18], ["#f4", 5.58]].forEach(([s, t]) => K.lift(s, t, { y: 70, dur: 0.55, ease: "expo.out" }));""")

# L03 — „internet jest zalany plikami, których nikt nigdy nie kupił”
NAMES = ["ebook_final.pdf", "planer_2026.pdf", "checklista.pdf", "poradnik_v3.pdf", "kurs_mini.pdf", "przepisy.pdf", "workbook.pdf",
         "30_dni.pdf", "biznes_plan.pdf", "dieta_keto.pdf", "budzet.pdf", "fitness.pdf", "nawyki.pdf", "notion_szablon.pdf"]
tiles = "".join(f'<div class="ft">{DOC}<b>{NAMES[i % len(NAMES)]}</b><i>0 sprzedaży</i></div>' for i in range(12 * 9))
S["L03"] = dict(css="""
      .wall { left: -40px; top: -40px; width: 2000px; display: grid; grid-template-columns: repeat(12, 150px); gap: 16px; transform-origin: 1002px 560px; }
      .ft { height: 190px; border-radius: 16px; background: var(--surface); border: 1px solid var(--line); padding: 20px 16px; display: flex; flex-direction: column; gap: 10px; }
      .ft .doc { width: 34px; height: 42px; color: var(--mute); }
      .ft b { font-size: 17px; font-weight: 600; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
      .ft i { font-style: normal; font-size: 16px; color: var(--neg); font-weight: 500; }
      .say { left: 160px; top: 0; height: 1080px; display: flex; flex-direction: column; justify-content: center; }""", body=f"""
      <div class="cam" id="cam"><div class="abs wall" id="wall">{tiles}</div></div>
      <div class="abs say"><div class="t-xl w300" id="a">Nikt nigdy</div><div class="t-xl w900" id="b">nie kupił.</div></div>""", js="""
      tl.fromTo("#wall", { scale: 3.2 }, { scale: 1, duration: 2.3, ease: "power3.inOut" }, 0);
      tl.to("#wall", { opacity: 0.16, duration: 0.5, ease: "power2.out" }, 2.1);
      K.rise("#a", 2.2); K.rise("#b", 3.25);""")

# L06 — „przeprowadziłem się do USA… rynek polski i amerykański”
g6 = GEO["L06"]
S["L06"] = dict(css="""
      svg.map { position: absolute; left: 0; top: 0; }
      .lb { font-size: 40px; font-weight: 600; letter-spacing: -0.015em; }
      .say { left: 160px; top: 760px; }""", body=f"""
      <div class="cam" id="cam">
        <svg class="map" width="1920" height="1080" viewBox="0 0 1920 1080">
          <path id="usa" d="{g6['usa']}" fill="#1b2438" stroke="rgba(255,255,255,0.18)" stroke-width="1.5"/>
          <path id="pol" d="{g6['pol']}" fill="#f4f6fa"/>
          <path id="arc" d="M{g6['polC'][0]},{g6['polC'][1]} Q{(g6['polC'][0] + g6['usaC'][0]) / 2},{min(g6['polC'][1], g6['usaC'][1]) - 330} {g6['usaC'][0]},{g6['usaC'][1]}"
                fill="none" stroke="#3d7bff" stroke-width="4" stroke-linecap="round"/>
          <circle id="pd" r="9" fill="#3d7bff"/>
        </svg>
        <div class="abs lb" id="lpl" style="left:{g6['polC'][0] - 160}px; top:{g6['polC'][1] + 44}px">Polska</div>
        <div class="abs lb" id="lus" style="left:{g6['usaC'][0] - 40}px; top:{g6['usaC'][1] - 30}px">USA</div>
      </div>
      <div class="abs say"><div class="t-l w800" id="a">Rynek polski</div><div class="t-l w300" id="b">i amerykański.</div></div>""", js="""
      K.push(DUR, 1.05, 30, 0);
      const arc = K.$("#arc"), L = arc.getTotalLength(), pd = K.$("#pd");
      arc.style.strokeDasharray = L; arc.style.strokeDashoffset = L;
      const p0 = arc.getPointAtLength(0); pd.setAttribute("cx", p0.x); pd.setAttribute("cy", p0.y);
      K.lift("#usa", 0.0, { y: 0, dur: 0.5 }); K.lift("#lpl", 0.1, { y: 14, dur: 0.4 });
      const st = { p: 0 };
      tl.to(st, { p: 1, duration: 0.9, ease: "power2.inOut", onUpdate: () => { arc.style.strokeDashoffset = L * (1 - st.p);
        const q = arc.getPointAtLength(L * st.p); pd.setAttribute("cx", q.x); pd.setAttribute("cy", q.y); } }, 0.3);
      tl.fromTo("#usa", { fill: "#1b2438" }, { fill: "#3d7bff", duration: 0.35, ease: "power2.out", immediateRender: false }, 1.12);
      K.lift("#lus", 1.1, { y: 14, dur: 0.4 });
      K.rise("#a", 1.85); K.rise("#b", 2.4);""")

# L08 — „płacą za korki z matematyki, angielskiego, polskiego… kilkadziesiąt zł za godzinę… co tydzień, przez miesiące”
rows8 = [("matematyka", "80"), ("angielski", "70"), ("polski", "70"), ("fizyka", "80")]
def rows_html(weeks):
    h = ""
    for w in range(weeks):
        h += f'<div class="wk">Tydzień {w + 1}</div>' if w else ""
        h += "".join(f'<div class="tx" id="{"r%d" % i if w == 0 else ""}"><div><b>Korepetycje · {n}</b><small>60 min</small></div><em>−{v} zł</em></div>'
                     for i, (n, v) in enumerate(rows8))
    return h
S["L08"] = dict(css="""
      .pan { left: 1000px; top: 90px; width: 760px; height: 900px; padding: 44px 48px 0; overflow: hidden; }
      .pan .hd small { font-size: 30px; color: var(--mute); font-weight: 500; }
      .pan .hd b { display: block; font-size: 60px; font-weight: 800; letter-spacing: -0.035em; margin-top: 6px; }
      .vp { position: absolute; left: 48px; right: 48px; top: 190px; bottom: 150px; overflow: hidden; }
      .tx { display: flex; justify-content: space-between; align-items: center; padding: 22px 0; border-top: 1px solid var(--line); }
      .tx b { font-size: 34px; font-weight: 600; display: block; letter-spacing: -0.015em; }
      .tx small { font-size: 26px; color: var(--mute); }
      .tx em { font-style: normal; font-size: 38px; font-weight: 700; }
      .wk { font-size: 26px; color: var(--mute); padding: 26px 0 8px; font-weight: 500; }
      .tot { position: absolute; left: 48px; right: 48px; bottom: 0; height: 150px; border-top: 1px solid var(--line); display: flex; justify-content: space-between; align-items: center; }
      .tot span { font-size: 34px; color: var(--mute); font-weight: 500; }
      .tot b { font-size: 68px; font-weight: 900; letter-spacing: -0.045em; }
      .lcol { left: 160px; top: 0; width: 780px; height: 1080px; }
      .lcol > div { position: absolute; left: 0; }
      .ph { font-size: 220px; font-weight: 900; letter-spacing: -0.06em; line-height: 1; }
      .ph span { font-size: 72px; font-weight: 300; color: var(--mute); letter-spacing: -0.03em; }""", body=f"""
      <div class="cam" id="cam">
        <div class="abs lcol">
          <div class="t-s mute" style="top:150px" id="lab">Rodzice przed egzaminem płacą</div>
          <div class="ph" style="top:330px" id="ph">80 zł <span>/ godz.</span></div>
          <div class="t-l w800" style="top:330px" id="c1">co tydzień,</div>
          <div class="t-l w300" style="top:452px" id="c2">przez miesiące.</div>
        </div>
        <div class="abs pan surf">
          <div class="hd"><small>Historia płatności</small><b>Wrzesień</b></div>
          <div class="vp"><div id="list">{rows_html(8)}</div></div>
          <div class="tot"><span>Razem</span><b id="sum">0 zł</b></div>
        </div>
      </div>""", js="""
      K.push(DUR, 1.035);
      K.lift(".pan", 0.1, { y: 40, dur: 0.7, ease: "expo.out" });
      K.rise("#lab", 0.3, { stagger: 0.04 });
      [0.96, 2.06, 2.62, 3.08].forEach((t, i) => K.lift("#r" + i, t, { y: 24, dur: 0.45, ease: "expo.out" }));
      const tot = (v) => (v < 0.5 ? "" : "−") + K.pl(v) + " zł";
      K.count("#sum", 0, 80, 1.0, 0.5, tot);
      K.count("#sum", 80, 300, 2.1, 1.3, tot);
      K.lift("#ph", 3.65, { y: 40, dur: 0.6, ease: "expo.out" });
      K.fadeOut("#ph", 6.95, { y: -30 });
      K.rise("#c1", 7.4); K.rise("#c2", 8.25);
      tl.fromTo("#list", { y: 0 }, { y: -2600, duration: 2.3, ease: "power2.in", immediateRender: false }, 7.5);
      K.count("#sum", 300, 4800, 7.5, 2.3, tot, "power2.in");""")

# L10 — „awersja do straty… bardziej boją się stracić, niż chcą zyskać”
S["L10"] = dict(css="""
      .ttl { left: 160px; top: 140px; }
      .rows { left: 160px; top: 480px; width: 1600px; }
      .row { position: relative; height: 210px; }
      .row .lab { font-size: 44px; font-weight: 500; color: var(--mute); }
      .row .track { position: relative; height: 96px; margin-top: 14px; }
      .row .b { position: absolute; left: 0; top: 0; width: 1400px; height: 96px; transform-origin: left center; }
      .row .v { position: absolute; top: 14px; font-size: 60px; font-weight: 800; letter-spacing: -0.03em; white-space: nowrap; }""", body="""
      <div class="cam" id="cam">
        <div class="abs t-xl ttl"><span class="w300" id="t1">Awersja</span> <span class="w800" id="t2">do straty</span></div>
        <div class="abs rows">
          <div class="row"><div class="lab" id="la">Stracić 100 zł</div><div class="track"><div class="b" id="ba" style="background:var(--neg)"></div><div class="v" id="va" style="left:1430px">×2</div></div></div>
          <div class="row"><div class="lab" id="lb">Zyskać 100 zł</div><div class="track"><div class="b" id="bb" style="background:var(--fg)"></div><div class="v" id="vb" style="left:730px">×1</div></div></div>
        </div>
      </div>""", js="""
      K.push(DUR, 1.04);
      K.rise("#t1", 0.35); K.rise("#t2", 1.0);
      K.lift("#la", 2.9, { y: 18, dur: 0.4 });
      tl.fromTo("#ba", { scaleX: 0 }, { scaleX: 1, duration: 0.9, ease: "expo.out" }, 3.1);
      K.lift("#va", 3.6, { y: 0, s: 0.7, dur: 0.4, ease: "back.out(2)" });
      K.lift("#lb", 3.85, { y: 18, dur: 0.4 });
      tl.fromTo("#bb", { scaleX: 0 }, { scaleX: 0.5, duration: 0.8, ease: "expo.out" }, 4.05);
      K.lift("#vb", 4.4, { y: 0, s: 0.7, dur: 0.35, ease: "back.out(2)" });""")

# L11 — witamina vs tabletka przeciwbólowa
S["L11"] = dict(css="""
      .ad { top: 150px; width: 760px; height: 780px; padding: 52px 56px; display: flex; flex-direction: column; }
      .ad .lab { font-size: 30px; font-weight: 500; color: var(--mute); }
      .ad .h { font-size: 60px; font-weight: 700; letter-spacing: -0.035em; line-height: 1.1; margin-top: 22px; }
      .ad .kind { margin-top: auto; font-size: 104px; letter-spacing: -0.05em; line-height: 0.98; }
      .ad .sl { margin-top: 30px; padding-top: 26px; border-top: 1px solid var(--line); display: flex; justify-content: space-between; align-items: baseline; }
      .ad .sl span { font-size: 32px; color: var(--mute); font-weight: 500; }
      .ad .sl b { font-size: 60px; font-weight: 900; letter-spacing: -0.04em; }""", body="""
      <div class="cam" id="cam">
        <div class="abs ad surf" id="A" style="left:160px">
          <div class="lab">Reklama 1</div>
          <div class="h" id="ha">Twoje dziecko może mieć lepszy wynik na egzaminie.</div>
          <div class="kind w300" id="ka">Witamina</div>
          <div class="sl" id="sa"><span>Sprzedaż</span><b class="mute">0</b></div>
        </div>
        <div class="abs ad surf" id="B" style="left:1000px">
          <div class="lab">Reklama 2</div>
          <div class="h" id="hb">Twoje dziecko może nie dostać się do dobrego liceum.</div>
          <div class="kind w900" id="kb">Tabletka przeciw&shy;bólowa</div>
          <div class="sl" id="sb"><span>Sprzedaż</span><b class="acc" id="nb">0</b></div>
        </div>
      </div>""", js="""
      K.push(DUR, 1.03);
      K.lift("#A", 0.05, { y: 40, dur: 0.7, ease: "expo.out" });
      K.rise("#ha", 0.3, { stagger: 0.05 });
      K.rise("#ka", 3.0);
      K.lift("#sa", 3.5, { y: 16, dur: 0.4 });
      K.lift("#B", 4.75, { y: 40, dur: 0.7, ease: "expo.out" });
      K.rise("#hb", 4.95, { stagger: 0.05 });
      tl.to("#A", { opacity: 0.45, duration: 0.5, ease: "sine.inOut" }, 7.4);
      K.lift("#kb", 7.7, { y: 40, dur: 0.5, ease: "expo.out" });
      K.lift("#sb", 7.95, { y: 16, dur: 0.35 });
      K.count("#nb", 0, 124, 8.0, 0.7, K.pl, "power2.out");""")

# L12 — parasol: nikt nie kupuje w słońcu, tylko kiedy pada
rain = "".join(f'<i style="left:{(i * 53) % 560 + 20}px; top:{(i * 97) % 300}px"></i>' for i in range(34))
S["L12"] = dict(css="""
      .wx { left: 160px; top: 200px; width: 760px; }
      .ico { position: relative; width: 300px; height: 260px; }
      .ico svg { position: absolute; left: 0; top: 0; }
      .rain { position: absolute; left: -20px; top: 170px; width: 600px; height: 360px; overflow: hidden; }
      .rain i { position: absolute; width: 4px; height: 46px; border-radius: 2px; background: rgba(143,178,255,0.75); transform: rotate(14deg); }
      .tmp { font-size: 240px; font-weight: 900; letter-spacing: -0.06em; line-height: 1; margin-top: 30px; position: relative; height: 240px; }
      .tmp > div, .ds > div { position: absolute; left: 0; top: 0; }
      .ds { font-size: 64px; font-weight: 300; position: relative; height: 80px; margin-top: 10px; }
      .shop { left: 1060px; top: 250px; width: 700px; padding: 52px 56px; }
      .shop .n { font-size: 72px; font-weight: 800; letter-spacing: -0.04em; }
      .shop .p { font-size: 40px; color: var(--mute); font-weight: 400; margin-top: 6px; }
      .shop .k { display: flex; justify-content: space-between; align-items: baseline; margin-top: 46px; padding-top: 28px; border-top: 1px solid var(--line); }
      .shop .k span { font-size: 32px; color: var(--mute); font-weight: 500; }
      .shop .k b { font-size: 72px; font-weight: 900; letter-spacing: -0.04em; }
      .btn { position: relative; margin-top: 40px; height: 110px; }
      .btn > div { position: absolute; inset: 0; border-radius: 999px; display: flex; align-items: center; justify-content: center; font-size: 42px; font-weight: 700; }
      .btn .off { background: var(--surface2); color: var(--dim); }
      .btn .on { background: var(--accent); color: var(--fg); opacity: 0; }""", body=f"""
      <div class="cam" id="cam">
        <div class="abs wx">
          <div class="ico">
            <svg id="sun" width="300" height="260" viewBox="0 0 300 260"><circle cx="120" cy="120" r="62" fill="#f4f6fa"/>
              <g stroke="#f4f6fa" stroke-width="10" stroke-linecap="round"><path d="M120 18 V36 M120 204 V222 M18 120 H36 M204 120 H222 M48 48 L61 61 M179 179 L192 192 M48 192 L61 179 M179 61 L192 48"/></g></svg>
            <svg id="cloud" width="300" height="260" viewBox="0 0 300 260"><path d="M70 170 C30 170 30 110 74 108 C80 60 150 50 168 96 C210 80 250 110 236 150 C262 156 256 172 236 172 Z" fill="#7d879b"/></svg>
            <div class="rain" id="rain">{rain}</div>
          </div>
          <div class="tmp"><div id="t1">24°</div><div id="t2">14°</div></div>
          <div class="ds"><div id="d1">Słonecznie</div><div id="d2">Deszcz</div></div>
        </div>
        <div class="abs shop surf" id="shop">
          <div class="n">Parasol</div><div class="p">49 zł</div>
          <div class="k"><span>Kupiło dzisiaj</span><b id="cnt">0</b></div>
          <div class="btn"><div class="off">Kup parasol</div><div class="on" id="bon">Kup parasol</div></div>
        </div>
        <svg class="cur" id="cur" viewBox="0 0 46 60"><path d="M4 3 L4 48 L15 37 L23 56 L31 52 L23 34 L39 34 Z" fill="#f4f6fa" stroke="#0a0d16" stroke-width="3" stroke-linejoin="round"/></svg>
      </div>""", js="""
      K.push(DUR, 1.03);
      K.lift("#sun", 0.05, { y: 0, s: 0.8, dur: 0.7, ease: "back.out(1.6)" });
      tl.fromTo("#sun", { rotation: 0, transformOrigin: "120px 120px" }, { rotation: 40, duration: 7.6, ease: "none", immediateRender: false }, 0.1);
      K.rise("#t1", 0.2); K.rise("#d1", 1.4);
      K.lift("#shop", 0.45, { y: 40, dur: 0.7, ease: "expo.out" });
      // rain arrives on „pada”
      tl.set(["#cloud", "#rain", "#t2", "#d2"], { opacity: 0 }, 0);
      tl.to("#sun", { opacity: 0, scale: 0.8, duration: 0.4, ease: "power2.in" }, 7.7);
      tl.fromTo("#cloud", { opacity: 0, y: -30 }, { opacity: 1, y: 0, duration: 0.5, ease: "expo.out", immediateRender: false }, 7.8);
      tl.to("#rain", { opacity: 1, duration: 0.3 }, 7.95);
      tl.fromTo("#rain i", { y: -120 }, { y: 360, duration: 0.55, ease: "none", stagger: { each: 0.03, repeat: 3 }, immediateRender: false }, 7.95);
      K.sink("#t1", 7.75); K.rise("#t2", 7.95); K.sink("#d1", 7.8); K.rise("#d2", 8.0);
      K.click("#cur", 1700, 1000, 1400, 680, 7.45, 8.02, null); tl.to("#cur", { opacity: 0, duration: 0.3 }, 8.9);
      tl.to("#bon", { opacity: 1, duration: 0.25, ease: "power2.out" }, 8.05);
      tl.fromTo(".btn", { scale: 1 }, { scale: 1.04, duration: 0.18, yoyo: true, repeat: 1, ease: "power2.out", immediateRender: false }, 8.05);
      K.count("#cnt", 0, 318, 8.15, 1.5, K.pl, "power2.out");""")

# L13 — prawko za 3 tygodnie, oblany, kolejne opłaty
S["L13"] = dict(css="""
      .lcol { left: 160px; top: 180px; width: 800px; }
      .hero { display: flex; align-items: baseline; gap: 26px; margin-top: 20px; }
      .hero b { font-size: 300px; font-weight: 900; letter-spacing: -0.065em; line-height: 0.9; }
      .hero span { font-size: 88px; font-weight: 300; }
      .att { margin-top: 60px; font-size: 52px; font-weight: 300; }
      .att b { font-weight: 800; color: var(--neg); }
      .pan { left: 1040px; top: 180px; width: 720px; padding: 48px 52px; }
      .pan .hd { font-size: 30px; color: var(--mute); font-weight: 500; }
      .fee { display: flex; justify-content: space-between; align-items: baseline; padding: 26px 0; border-top: 1px solid var(--line); }
      .fee span { font-size: 36px; font-weight: 500; }
      .fee b { font-size: 44px; font-weight: 700; }
      .sum { display: flex; justify-content: space-between; align-items: baseline; padding-top: 30px; border-top: 1px solid rgba(255,255,255,0.3); margin-top: 6px; }
      .sum span { font-size: 36px; color: var(--mute); font-weight: 500; }
      .sum b { font-size: 92px; font-weight: 900; letter-spacing: -0.05em; }""", body="""
      <div class="cam" id="cam">
        <div class="abs lcol">
          <div class="t-s mute" id="lab">Egzamin na prawo jazdy za</div>
          <div class="hero" id="hero"><b id="d">0</b><span>dni</span></div>
          <div class="att" id="att">Podejście 1: <b>oblany</b></div>
        </div>
        <div class="abs pan surf" id="pan">
          <div class="hd">Kolejne opłaty</div><div style="height:16px"></div>
          <div class="fee" id="f1"><span>Poprawka egzaminu</span><b>200 zł</b></div>
          <div class="fee" id="f2"><span>Kolejna poprawka</span><b>200 zł</b></div>
          <div class="fee" id="f3"><span>Jazdy doszkalające</span><b>320 zł</b></div>
          <div class="sum"><span>Razem</span><b id="sum">0 zł</b></div>
        </div>
      </div>""", js="""
      K.push(DUR, 1.03);
      K.rise("#lab", 0.1, { stagger: 0.04 });
      K.lift("#hero", 1.15, { y: 40, dur: 0.6, ease: "expo.out" });
      K.count("#d", 0, 21, 1.2, 0.8, K.pl, "expo.out");
      K.lift("#att", 3.3, { y: 24, dur: 0.5, ease: "expo.out" });
      K.lift("#pan", 4.6, { y: 40, dur: 0.7, ease: "expo.out" });
      const zl = (v) => K.pl(v) + " zł";
      K.lift("#f1", 5.4, { y: 20, dur: 0.45 }); K.count("#sum", 0, 200, 5.45, 0.6, zl);
      K.lift("#f2", 7.3, { y: 20, dur: 0.45 }); K.count("#sum", 200, 400, 7.35, 0.6, zl);
      K.lift("#f3", 8.4, { y: 20, dur: 0.45 }); K.count("#sum", 400, 720, 8.45, 0.8, zl);""")

# L16 — „po co płacić za PDF, skoro wszystko jest w Google, YouTube, ChatGPT, Gemini za darmo”
apps = [("app_google", "Google", 1.68), ("app_youtube", "YouTube", 2.16), ("app_chatgpt", "ChatGPT", 2.78), ("app_google_gemini", "Gemini", 3.26)]
S["L16"] = dict(css="""
      .q { left: 160px; top: 130px; }
      .apps { left: 160px; top: 470px; display: flex; gap: 40px; }
      .app { width: 370px; height: 400px; padding: 44px; display: flex; flex-direction: column; }
      .app img { width: 120px; height: 120px; object-fit: contain; }
      .app b { font-size: 46px; font-weight: 700; letter-spacing: -0.025em; margin-top: auto; }
      .app em { font-style: normal; font-size: 64px; font-weight: 300; color: var(--mute); margin-top: 4px; letter-spacing: -0.03em; }""", body="""
      <div class="cam" id="cam">
        <div class="abs q t-xl"><span class="w300" id="q1">Po co płacić</span> <span class="w900" id="q2">za PDF?</span></div>
        <div class="abs apps">""" + "".join(
        f'<div class="app surf" id="a{i}"><img src="assets/{f}.png" alt="" /><b>{n}</b><em class="ws" id="z{i}"><span class="lo">0 zł</span><span class="hi w900" style="color:var(--fg)">0 zł</span></em></div>'
        for i, (f, n, _) in enumerate(apps)) + """</div>
      </div>""", js="""
      K.push(DUR, 1.035);
      K.rise("#q1", 0.05); K.rise("#q2", 0.3);
      """ + "\n      ".join(f'K.lift("#a{i}", {t}, {{ y: 60, dur: 0.55, ease: "expo.out" }});' for i, (_, _, t) in enumerate(apps)) + """
      [0, 1, 2, 3].forEach((i) => K.weight("#z" + i, 3.82 + i * 0.07, { kick: 1.08 }));""")

# L17 — produkt, który leży vs produkt, który się sprzedaje i zarabia kilkadziesiąt tysięcy miesięcznie
S["L17"] = dict(css="""
      .stc { top: 150px; width: 760px; height: 780px; padding: 52px 56px; }
      .stc .lab { font-size: 30px; color: var(--mute); font-weight: 500; }
      .stc .h { font-size: 72px; letter-spacing: -0.04em; line-height: 1.05; margin-top: 14px; }
      .stc svg { position: absolute; left: 56px; bottom: 210px; }
      .stc .v { position: absolute; left: 56px; bottom: 52px; font-size: 96px; font-weight: 900; letter-spacing: -0.05em; }
      .stc .v span { font-size: 40px; font-weight: 300; color: var(--mute); letter-spacing: -0.02em; }
      .nt { position: absolute; right: 56px; padding: 14px 24px; border-radius: 999px; background: var(--surface2); font-size: 30px; font-weight: 700; }""", body="""
      <div class="cam" id="cam">
        <div class="abs stc surf" id="A" style="left:160px">
          <div class="lab">Produkt 1</div><div class="h w300" id="ha">leży.</div>
          <svg width="648" height="260" viewBox="0 0 648 260"><path d="M0 256 H648" stroke="rgba(255,255,255,0.08)" stroke-width="2"/>
            <path id="la" d="M0 250 L108 250 L216 249 L324 250 L432 250 L540 249 L648 250" fill="none" stroke="#7d879b" stroke-width="5" stroke-linecap="round"/></svg>
          <div class="v" id="va">0 zł <span>/ mies.</span></div>
        </div>
        <div class="abs stc surf" id="B" style="left:1000px">
          <div class="lab">Produkt 2</div><div class="h w900" id="hb">sprzedaje się.</div>
          <svg width="648" height="260" viewBox="0 0 648 260"><path d="M0 256 H648" stroke="rgba(255,255,255,0.08)" stroke-width="2"/>
            <path id="lb" d="M0 248 C90 240 150 226 220 200 C300 170 340 150 410 110 C480 70 560 40 648 10" fill="none" stroke="#3d7bff" stroke-width="6" stroke-linecap="round"/></svg>
          <div class="v"><b id="nb">0 zł</b> <span>/ mies.</span></div>
          <div class="nt" id="n1" style="top:150px">+59 zł</div><div class="nt" id="n2" style="top:220px">+59 zł</div><div class="nt" id="n3" style="top:290px">+59 zł</div>
        </div>
      </div>""", js="""
      K.push(DUR, 1.03);
      const draw = (sel, t, d) => { const p = K.$(sel), L = p.getTotalLength(); p.style.strokeDasharray = L;
        tl.fromTo(p, { strokeDashoffset: L }, { strokeDashoffset: 0, duration: d, ease: "power2.inOut" }, t); };
      K.lift("#A", 0.6, { y: 40, dur: 0.7, ease: "expo.out" }); K.rise("#ha", 1.6);
      draw("#la", 1.2, 1.2); K.lift("#va", 1.9, { y: 20, dur: 0.4 });
      K.lift("#B", 2.25, { y: 40, dur: 0.7, ease: "expo.out" }); K.rise("#hb", 2.95);
      tl.to("#A", { opacity: 0.45, duration: 0.5 }, 3.2);
      draw("#lb", 3.4, 2.6);
      K.count("#nb", 0, 47200, 4.2, 2.1, (v) => K.pl(v) + " zł", "power2.in");
      [4.3, 4.85, 5.45].forEach((t, i) => K.lift("#n" + (i + 1), t, { y: 20, s: 0.9, dur: 0.4, ease: "back.out(2)" }));""")

# L20 — „59 zł to dużo czy mało? Nie wiesz, nikt nie wie”
S["L20"] = dict(css="""
      .wrap { left: 160px; top: 0; height: 1080px; display: flex; align-items: center; gap: 70px; }
      .p { font-size: 380px; font-weight: 900; letter-spacing: -0.065em; line-height: 0.9; }
      .qs { font-size: 130px; letter-spacing: -0.05em; line-height: 1.02; }
      .nk { left: 168px; top: 860px; }""", body="""
      <div class="cam" id="cam">
        <div class="abs wrap"><div class="p" id="p">59 zł</div>
          <div class="qs"><div class="w800" id="q1">dużo?</div><div class="w300" id="q2">mało?</div></div></div>
        <div class="abs t-m mute nk" id="nk">Nikt nie wie.</div>
      </div>""", js="""
      K.push(DUR, 1.05);
      K.rise("#p", 0.08, { dur: 0.8 });
      K.rise("#q1", 1.05); K.rise("#q2", 1.62);
      tl.to("#q1", { opacity: 0.4, duration: 0.25 }, 1.62);
      K.rise("#nk", 2.45, { stagger: 0.05 });""")

# L23 — film urywa się sekundę przed pluskiem
S["L23"] = dict(css="""
      .pl { left: 360px; top: 80px; width: 1200px; height: 760px; overflow: hidden; }
      .vid { position: absolute; left: 0; top: 0; width: 1200px; height: 675px; background: #0b1222; overflow: hidden; }
      .water { position: absolute; left: 0; right: 0; top: 530px; bottom: 0; background: #142650; }
      .water::before { content: ""; position: absolute; left: 0; right: 0; top: 0; height: 3px; background: rgba(143,178,255,0.6); }
      .cliff { position: absolute; left: 0; top: 0; width: 330px; height: 530px; background: #161e30; }
      .rock { position: absolute; left: 460px; top: 0; width: 140px; height: 115px; }
      .spin { position: absolute; left: 820px; top: 220px; width: 88px; height: 88px; border-radius: 50%; border: 8px solid rgba(255,255,255,0.18); border-top-color: #f4f6fa; opacity: 0; }
      .ctl { position: absolute; left: 0; right: 0; top: 675px; height: 85px; display: flex; align-items: center; gap: 28px; padding: 0 34px; }
      .ctl .tm { font-size: 30px; font-weight: 600; width: 170px; }
      .ctl .tr { flex: 1; height: 8px; border-radius: 4px; background: rgba(255,255,255,0.14); position: relative; }
      .ctl .f { position: absolute; inset: 0; background: var(--neg); transform-origin: left center; border-radius: 4px; }
      .cap { left: 360px; top: 890px; }""", body="""
      <div class="cam" id="cam">
        <div class="abs pl surf">
          <div class="vid"><div class="cliff"></div><div class="water"></div>
            <svg class="rock" id="rock" viewBox="0 0 110 90"><path d="M14 40 L34 10 L78 6 L104 34 L96 74 L52 88 L12 70 Z" fill="#7d879b"/></svg>
            <div class="spin" id="spin"></div></div>
          <div class="ctl"><svg width="26" height="30" viewBox="0 0 26 30"><path d="M3 2 L24 15 L3 28 Z" fill="#f4f6fa"/></svg>
            <div class="tm" id="tm">0:00 / 1:00</div><div class="tr"><div class="f" id="f"></div></div></div>
        </div>
        <div class="abs t-m cap"><span class="w300" id="c1">Urywa się sekundę</span> <span class="w800" id="c2">przed pluskiem.</span></div>
      </div>""", js="""
      K.push(DUR, 1.03);
      K.lift(".pl", 0.05, { y: 40, dur: 0.7, ease: "expo.out" });
      tl.fromTo("#rock", { y: 20, rotation: 0 }, { y: 380, rotation: 70, duration: 4.1, ease: "power2.in" }, 0.85);
      K.count("#tm", 0, 59, 0.3, 4.65, (v) => "0:" + String(Math.floor(v)).padStart(2, "0") + " / 1:00", "none");
      tl.fromTo("#f", { scaleX: 0 }, { scaleX: 59 / 60, duration: 4.65, ease: "none" }, 0.3);
      tl.to("#spin", { opacity: 1, duration: 0.2 }, 5.0);
      tl.fromTo("#spin", { rotation: 0 }, { rotation: 720, duration: 1.6, ease: "none", immediateRender: false }, 5.0);
      K.rise("#c1", 4.55); K.rise("#c2", 5.0);""")

# L24 — efekt w 10 minut, brak zwrotów, polecają na grupach na Facebooku
S["L24"] = dict(css="""
      .lcol { left: 160px; top: 170px; width: 820px; }
      .ch { display: flex; align-items: center; gap: 24px; font-size: 52px; font-weight: 700; letter-spacing: -0.025em; margin-top: 26px; }
      .post { left: 1040px; top: 190px; width: 720px; padding: 44px 48px; }
      .post .gh { display: flex; align-items: center; gap: 22px; }
      .post .gh img { width: 72px; height: 72px; }
      .post .gh b { font-size: 34px; font-weight: 700; display: block; letter-spacing: -0.015em; }
      .post .gh small { font-size: 26px; color: var(--mute); }
      .post .au { font-size: 30px; font-weight: 600; margin-top: 34px; }
      .post .au span { color: var(--mute); font-weight: 400; }
      .post .tx { font-size: 42px; font-weight: 400; line-height: 1.3; margin-top: 14px; letter-spacing: -0.015em; }
      .post .ft { display: flex; gap: 40px; margin-top: 34px; padding-top: 26px; border-top: 1px solid var(--line); font-size: 30px; color: var(--mute); font-weight: 500; }
      .post .ft b { color: var(--fg); font-weight: 800; }""", body=f"""
      <div class="cam" id="cam">
        <div class="abs lcol">
          <div class="t-l w300" id="h1">Pierwszy efekt</div>
          <div class="t-l w900" id="h2">w 10 minut.</div>
          <div style="height:50px"></div>
          <div class="ch" id="c1">{CHK}Brak zwrotów</div>
          <div class="ch" id="c2">{CHK}Polecają dalej</div>
        </div>
        <div class="abs post surf" id="post">
          <div class="gh"><img src="assets/app_facebook.png" alt="" /><div><b>Rodzice ósmoklasistów 2026</b><small>Grupa · 48 tys. członków</small></div></div>
          <div class="au">Monika <span>· 2 godz.</span></div>
          <div class="tx" id="ptx">Polecam z czystym sumieniem. Pierwszy efekt już po jednym wieczorze, zadziałało od razu!</div>
          <div class="ft"><span><b id="lk">0</b> polubień</span><span><b id="cm">0</b> komentarzy</span></div>
        </div>
      </div>""", js="""
      K.push(DUR, 1.03);
      K.rise("#h1", 1.35); K.rise("#h2", 2.3);
      K.lift("#c1", 4.3, { y: 20, dur: 0.45 }); K.tick("#c1", 4.5);
      K.lift("#c2", 5.55, { y: 20, dur: 0.45 }); K.tick("#c2", 5.75);
      K.lift("#post", 6.55, { y: 50, dur: 0.7, ease: "expo.out" });
      K.count("#lk", 0, 128, 7.4, 2.6, K.pl, "power1.out");
      K.count("#cm", 0, 46, 7.7, 2.4, K.pl, "power1.out");""")

# L27 — TK Maxx przy Pałacu Kultury, dziesiątki tysięcy ludzi dziennie, potrzebujesz 6
S["L27"] = dict(css="""
      canvas { position: absolute; left: 0; top: 0; }
      .lcol { left: 160px; top: 160px; width: 700px; }
      .pin { display: flex; align-items: center; gap: 18px; }
      .pin b { font-size: 64px; font-weight: 800; letter-spacing: -0.035em; }
      .six { display: flex; align-items: flex-end; gap: 22px; margin-top: 80px; }
      .six b { font-size: 300px; font-weight: 900; letter-spacing: -0.065em; line-height: 0.78; }
      .six span { font-size: 76px; font-weight: 300; letter-spacing: -0.03em; }""", body="""
      <div class="cam" id="cam"><canvas id="cv" width="1920" height="1080"></canvas></div>
      <div class="abs lcol">
        <div class="pin" id="pn"><svg width="44" height="58" viewBox="0 0 44 58"><path d="M22 56 C22 56 4 34 4 21 A18 18 0 0 1 40 21 C40 34 22 56 22 56 Z" fill="#3d7bff"/><circle cx="22" cy="21" r="7" fill="#070b15"/></svg><b>Warszawa</b></div>
        <div class="t-s mute" style="margin-top:14px" id="pk">TK Maxx przy Pałacu Kultury</div>
        <div class="t-s" style="margin-top:30px" id="ppl"><b id="n" style="font-weight:800">0</b> <span class="w300">osób dziennie</span></div>
        <div class="six" id="six"><b>6</b><span>wystarczy.</span></div>
      </div>""", js="""
      const cv = K.$("#cv"), cx = cv.getContext("2d"), rnd = K.rng(27), P = [];
      for (let r = 0; r < 26; r++) for (let c = 0; c < 46; c++)
        P.push({ x: 900 + c * 21 + (r % 2) * 10 + (rnd() - 0.5) * 6, y: 150 + r * 31 + (rnd() - 0.5) * 6, k: rnd(), s: 0.85 + rnd() * 0.3 });
      const SIX = [140, 377, 615, 702, 941, 1095];
      const st = { a: 0, on: 0, dim: 1 };
      function person(x, y, s, col) { cx.fillStyle = col; cx.beginPath(); cx.arc(x, y, 4.2 * s, 0, 6.2832); cx.fill();
        cx.beginPath(); cx.roundRect(x - 5 * s, y + 6 * s, 10 * s, 12 * s, 4 * s); cx.fill(); }
      function draw() { cx.clearRect(0, 0, 1920, 1080);
        P.forEach((p, i) => { const k = Math.min(1, Math.max(0, (st.a * 1.3 - p.k) * 5)); if (k <= 0) return;
          person(p.x, p.y, p.s, `rgba(125,135,155,${0.75 * k * st.dim})`); });
        SIX.forEach((i, j) => { const g = Math.min(1, Math.max(0, st.on * 6 - j)); if (g <= 0) return; const p = P[i];
          person(p.x, p.y, p.s * (1 + 0.6 * g), "#3d7bff"); cx.strokeStyle = `rgba(61,123,255,${0.55 * g})`; cx.lineWidth = 2;
          cx.beginPath(); cx.arc(p.x, p.y + 6, 26 + 8 * (1 - g), 0, 6.2832); cx.stroke(); }); }
      tl.fromTo("#cam", { scale: 1.06, transformOrigin: "1380px 540px" }, { scale: 1, duration: DUR, ease: "sine.out" }, 0);
      K.frame(draw);
      tl.to(st, { a: 1, duration: 5.0, ease: "power1.inOut" }, 0.2);
      K.lift("#pn", 0.1, { y: 20, dur: 0.5, ease: "expo.out" });
      K.rise("#pk", 1.75, { stagger: 0.05 });
      K.lift("#ppl", 4.4, { y: 20, dur: 0.5 });
      K.count("#n", 0, 40000, 4.45, 1.3, (v) => "~" + K.pl(v), "expo.out");
      tl.to(st, { dim: 0.45, duration: 0.6 }, 6.9);
      tl.to(st, { on: 1, duration: 0.8, ease: "none" }, 7.1);
      K.lift("#six", 7.1, { y: 50, dur: 0.6, ease: "expo.out" });""")

# L28 — 6 osób z kilkudziesięciu milionów internautów w Polsce
g28 = GEO["L28"]
S["L28"] = dict(css="""
      canvas, svg.pl { position: absolute; left: 0; top: 0; }
      .lcol { left: 160px; top: 170px; width: 760px; }
      .six { display: flex; align-items: flex-end; gap: 22px; }
      .six b { font-size: 300px; font-weight: 900; letter-spacing: -0.065em; line-height: 0.78; }
      .six span { font-size: 76px; font-weight: 300; letter-spacing: -0.03em; }
      .of { font-size: 76px; font-weight: 300; letter-spacing: -0.035em; margin-top: 40px; }
      .of b { font-weight: 800; }
      .bp { position: absolute; left: 160px; top: 860px; font-size: 76px; letter-spacing: -0.04em; }""", body=f"""
      <div class="cam" id="cam">
        <svg class="pl" width="1920" height="1080" viewBox="0 0 1920 1080"><path id="po" d="{g28['pol']}" fill="none" stroke="rgba(255,255,255,0.22)" stroke-width="2"/></svg>
        <canvas id="cv" width="1920" height="1080"></canvas>
      </div>
      <div class="abs lcol">
        <div class="six" id="six"><b>6</b><span>osób</span></div>
        <div class="of" id="of"><span class="w300">z</span> <b id="n">0</b></div>
        <div class="t-s mute" style="margin-top:14px" id="lb">internautów w Polsce, każdego dnia</div>
      </div>
      <div class="bp"><span class="ws" id="bp"><span class="lo w300">Banalnie proste.</span><span class="hi w900">Banalnie proste.</span></span></div>""", js="""
      const D = """ + json.dumps(g28["dots"]) + """;
      const cv = K.$("#cv"), cx = cv.getContext("2d"), rnd = K.rng(28), O = D.map(() => rnd());
      const SIX = [300, 820, 1290, 1777, 2240, 2650];
      const st = { a: 0, on: 0, dim: 1 };
      function draw() { cx.clearRect(0, 0, 1920, 1080);
        D.forEach(([x, y], i) => { const k = Math.min(1, Math.max(0, (st.a * 1.3 - O[i]) * 5)); if (k <= 0) return;
          cx.fillStyle = `rgba(125,135,155,${0.7 * k * st.dim})`; cx.fillRect(x, y, 3, 3); });
        SIX.forEach((i, j) => { const g = Math.min(1, Math.max(0, st.on * 6 - j)); if (g <= 0) return; const [x, y] = D[i];
          cx.fillStyle = "#3d7bff"; cx.beginPath(); cx.arc(x + 1.5, y + 1.5, 3 + 7 * g, 0, 6.2832); cx.fill();
          cx.strokeStyle = `rgba(61,123,255,${0.5 * g})`; cx.lineWidth = 2; cx.beginPath(); cx.arc(x + 1.5, y + 1.5, 20 + 8 * (1 - g), 0, 6.2832); cx.stroke(); }); }
      const po = K.$("#po"), L = po.getTotalLength(); po.style.strokeDasharray = L;
      tl.fromTo(po, { strokeDashoffset: L }, { strokeDashoffset: 0, duration: 1.2, ease: "power2.inOut" }, 0.0);
      tl.fromTo("#cam", { scale: 1.05, transformOrigin: "1370px 540px" }, { scale: 1, duration: DUR, ease: "sine.out" }, 0);
      K.frame(draw);
      tl.to(st, { a: 1, duration: 1.6, ease: "power2.inOut" }, 0.2);
      K.lift("#six", 0.95, { y: 50, dur: 0.6, ease: "expo.out" });
      tl.to(st, { dim: 0.5, duration: 0.5 }, 1.0);
      tl.to(st, { on: 1, duration: 0.7, ease: "none" }, 1.05);
      K.lift("#of", 1.9, { y: 24, dur: 0.5 });
      K.count("#n", 0, 30000000, 2.0, 1.6, K.pl, "expo.out");
      K.lift("#lb", 3.9, { y: 18, dur: 0.45 });
      K.lift(".bp", 6.65, { y: 30, dur: 0.5, ease: "expo.out" });
      K.weight("#bp", 7.0, { kick: 1.04 });""")

# L29 — jesteś za wolny: miesiącami nad jednym PDF-em, kolory, czcionki… dla rynku, którego nie sprawdzili
S["L29"] = dict(css="""
      .h { left: 160px; top: 110px; font-size: 230px; font-weight: 900; letter-spacing: -0.065em; line-height: 1; }
      .file { left: 160px; top: 420px; width: 1600px; height: 160px; padding: 0 48px; display: flex; align-items: center; gap: 34px; }
      .file .doc { width: 58px; height: 72px; color: var(--mute); }
      .file b { font-size: 56px; font-weight: 600; letter-spacing: -0.025em; flex: 1; white-space: nowrap; }
      .file .mo { font-size: 36px; color: var(--mute); font-weight: 500; }
      .file .mo em { font-style: normal; color: var(--fg); font-weight: 800; }
      .chips { left: 160px; top: 630px; display: flex; gap: 20px; }
      .chip { padding: 18px 30px; border-radius: 999px; background: var(--surface2); font-size: 36px; font-weight: 500; }
      .chip span { color: var(--mute); }
      .q { left: 160px; top: 820px; font-size: 96px; letter-spacing: -0.045em; }""", body=f"""
      <div class="cam" id="cam">
        <div class="abs h"><span class="w300" id="h1">Za</span> <span id="h2">wolno.</span></div>
        <div class="abs file surf" id="file">{DOC}<b id="fn">produkt_v1.pdf</b><div class="mo">Miesiąc <em id="mo">1</em></div></div>
        <div class="abs chips"><div class="chip" id="k1"><span>zmiana:</span> kolory</div><div class="chip" id="k2"><span>zmiana:</span> czcionka</div>
          <div class="chip" id="k3"><span>zmiana:</span> marginesy</div><div class="chip" id="k4"><span>zmiana:</span> okładka</div></div>
        <div class="abs q"><span class="w300" id="q1">Rynek sprawdzony?</span> <span class="w900 neg" id="q2">Nie.</span></div>
      </div>""", js="""
      K.push(DUR, 1.03);
      K.rise("#h1", 0.5); K.rise("#h2", 0.85);
      K.lift("#file", 1.5, { y: 40, dur: 0.6, ease: "expo.out" });
      const fn = K.$("#fn"), mo = K.$("#mo"), s = { v: 1 };
      tl.to(s, { v: 47, duration: 4.2, ease: "power1.in", onUpdate: () => { const v = Math.round(s.v);
        fn.textContent = "produkt_v" + v + (v > 40 ? "_FINAL_final2" : v > 25 ? "_FINAL" : "") + ".pdf"; mo.textContent = Math.min(6, 1 + Math.floor((v - 1) / 8)); } }, 1.9);
      [["#k1", 6.05], ["#k2", 6.95], ["#k3", 7.45], ["#k4", 7.9]].forEach(([k, t]) => K.lift(k, t, { y: 20, s: 0.9, dur: 0.4, ease: "back.out(2)" }));
      K.rise("#q1", 9.55); K.rise("#q2", 10.5, { dur: 0.5 });""")

# L31 — „to tylko wierzchołek góry lodowej… rynek, produkt, ściąganie ludzi”
S["L31"] = dict(css="""
      svg.ice { position: absolute; left: 0; top: 0; }
      .tag { position: absolute; font-size: 40px; font-weight: 600; letter-spacing: -0.015em; }
      .lay { position: absolute; left: 0; width: 1920px; text-align: center; font-size: 84px; font-weight: 800; letter-spacing: -0.04em; }
      .hd { left: 160px; top: 120px; }""", body="""
      <div class="cam" id="cam">
        <svg class="ice" width="1920" height="2100" viewBox="0 0 1920 2100">
          <rect x="0" y="560" width="1920" height="1540" fill="#0a1530"/>
          <path d="M840 560 L905 430 L950 470 L1000 380 L1080 560 Z" fill="#e9eef7"/>
          <path d="M840 560 L1080 560 L1340 760 L1500 1120 L1420 1560 L1120 1900 L760 1880 L470 1500 L420 1080 L600 760 Z" fill="#1b3366"/>
          <rect x="0" y="558" width="1920" height="4" fill="rgba(143,178,255,0.7)"/>
        </svg>
        <div class="tag" id="tg" style="left:1110px; top:430px">Ten film</div>
        <div class="abs t-m hd"><span class="w300" id="h1">Tylko</span> <span class="w800" id="h2">wierzchołek.</span></div>
        <div class="lay" id="y1" style="top:920px">Rynek</div>
        <div class="lay" id="y2" style="top:1060px">Produkt</div>
        <div class="lay" id="y3" style="top:1200px">Ruch i sprzedaż</div>
        <div class="lay" id="y4" style="top:1340px">System AI</div>
      </div>""", js="""
      K.rise("#h1", 1.2); K.rise("#h2", 1.5);
      K.lift("#tg", 1.9, { y: 14, dur: 0.4 });
      tl.fromTo("#cam", { y: 0 }, { y: -560, duration: 1.3, ease: "power3.inOut" }, 2.7);
      K.lift("#y1", 3.85, { y: 30, dur: 0.45, ease: "expo.out" });
      K.lift("#y2", 4.6, { y: 30, dur: 0.45, ease: "expo.out" });
      K.lift("#y3", 5.5, { y: 30, dur: 0.45, ease: "expo.out" });
      K.lift("#y4", 6.05, { y: 30, dur: 0.45, ease: "expo.out" });""")

if __name__ == "__main__":
    import sys
    only = set(sys.argv[1:])
    for k, s in S.items():
        if only and k not in only:
            continue
        page(k, D(k), s["body"], s["js"].replace("DUR", str(D(k))) + "\n      K.whip(DUR);".replace("DUR", str(D(k))), s.get("css", ""))
    print(len(S), "full scenes")
