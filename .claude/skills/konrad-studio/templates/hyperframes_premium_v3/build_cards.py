#!/usr/bin/env python3
"""lfpdo Premium v3 — the 15 KARTA scenes (dark card on the left wall next to Konrad, transparent MOV).
Times are scene-relative seconds taken from premium/words_per_scene.txt."""
import json, os
from page import page, HERE

IDX = {x["key"]: x for x in json.load(open(os.path.join(HERE, "..", "..", "index.json")))}
for k, (a, b) in json.load(open(os.path.join(HERE, "timing.json"))).items():   # v3 holds some cards longer (still inside FSEG)
    IDX[k]["in"], IDX[k]["out"] = a, b
D = lambda k: round(IDX[k]["out"] - IDX[k]["in"], 3)
S = {}
CHK = ('<div class="chk"><div class="on"><svg viewBox="0 0 28 26"><path d="M3 13 L11 21 L25 4" fill="none" stroke="#fff" stroke-width="4.5" '
       'stroke-linecap="round" stroke-linejoin="round"/></svg></div><div class="off"><svg viewBox="0 0 24 24"><path d="M4 4 L20 20 M20 4 L4 20" '
       'fill="none" stroke="#fff" stroke-width="4.5" stroke-linecap="round"/></svg></div></div>')

# L01 — „jeżeli masz w głowie pomysł… mam złą wiadomość”
S["L01"] = dict(body="""
      <div class="card">
        <div class="lab" id="lab">Masz w głowie</div><div class="sp"></div>
        <div class="k1" id="a">pomysł.</div><div class="sp"></div>
        <div class="k2 w300 neg" id="b">Zła wiadomość.</div>
      </div>""", js="""
      K.card(DUR);
      K.rise("#lab", 0.15, { stagger: 0.04 });
      K.rise("#a", 1.35);
      K.strike("#a", 3.3);
      K.rise("#b", 3.42);""")

# L04 — „ponad 130 tysięcy produktów cyfrowych… zaczynając w wieku 14 lat”
S["L04"] = dict(body="""
      <div class="card">
        <div class="lab" id="lab">Sprzedane produkty cyfrowe</div><div class="sp"></div>
        <div class="k1" style="font-size:118px;font-weight:900" id="n">0</div><div class="sp"></div>
        <div class="k3" id="s"><span class="w300 mute">Start:</span> 14 lat</div>
      </div>""", js="""
      K.card(DUR);
      K.rise("#lab", 0.12, { stagger: 0.04 });
      K.lift("#n", 0.25, { y: 30, dur: 0.6, ease: "expo.out" });
      K.count("#n", 0, 130000, 0.3, 1.2, (v) => K.pl(v) + "+", "expo.out");
      K.lift("#s", 2.4, { y: 24, dur: 0.5, ease: "expo.out" });""")

# L07 — „nie robi produktu na czuja… w Polsce prawie nikt o tym nie mówi”
S["L07"] = dict(body="""
      <div class="card">
        <div class="lab" id="lab">Produkt robiony</div><div class="sp"></div>
        <div class="k1" id="a">na czuja</div><div class="hr"></div>
        <div class="k2 w300" id="b1">Dane:</div>
        <div class="k2" id="b2">kto już płaci?</div><div class="sp"></div>
        <div class="lab" id="c">W Polsce prawie nikt o tym nie mówi.</div>
      </div>""", js="""
      K.card(DUR);
      K.rise("#lab", 0.12, { stagger: 0.04 });
      K.rise("#a", 1.1);
      K.strike("#a", 1.85);
      K.rise("#b1", 2.15); K.rise("#b2", 2.35);
      K.rise("#c", 2.6, { stagger: 0.03 });""")

# L09 — „ten portfel już jest otwarty. Pieniądze już płyną w tej niszy”
S["L09"] = dict(css="""
      .tx { display: flex; justify-content: space-between; font-size: 36px; font-weight: 500; padding: 14px 0; border-top: 1px solid var(--line); }
      .tx b { font-weight: 700; }""", body="""
      <div class="card">
        <div class="lab" id="lab">Portfel w tej niszy jest</div><div class="sp"></div>
        <div class="k1"><span class="ws" id="ws"><span class="lo w300">otwarty.</span><span class="hi w900">otwarty.</span></span></div><div class="sp"></div>
        <div class="tx" id="t1"><span class="mute">Korepetycje</span><b>+80 zł</b></div>
        <div class="tx" id="t2"><span class="mute">Korepetycje</span><b>+70 zł</b></div>
        <div class="tx" id="t3"><span class="mute">Korepetycje</span><b>+80 zł</b></div>
      </div>""", js="""
      K.card(DUR);
      K.rise("#lab", 0.1, { stagger: 0.04 });
      K.lift(".k1", 0.25, { y: 30, dur: 0.6, ease: "expo.out" });
      K.weight("#ws", 1.2);
      K.lift("#t1", 1.7, { y: 20, dur: 0.45 }); K.lift("#t2", 1.98, { y: 20, dur: 0.45 }); K.lift("#t3", 2.26, { y: 20, dur: 0.45 });""")

# L11b — „jeden opis sprzedaje, a drugi nie sprzedaje”
S["L11b"] = dict(css="""
      .op { display: flex; align-items: baseline; justify-content: space-between; padding: 20px 0; border-top: 1px solid var(--line); }
      .op .a { font-size: 40px; font-weight: 300; color: var(--mute); }
      .op .b { font-size: 52px; font-weight: 800; letter-spacing: -0.03em; }""", body="""
      <div class="card">
        <div class="lab" id="lab">Ten sam produkt</div><div class="sp"></div>
        <div class="op" id="o1"><span class="a">Opis 1</span><span class="b acc" id="b1">sprzedaje</span></div>
        <div class="op" id="o2"><span class="a">Opis 2</span><span class="b mute" id="b2">nie sprzedaje</span></div>
      </div>""", js="""
      K.card(DUR);
      K.rise("#lab", 0.08);
      K.lift("#o1", 0.15, { y: 20, dur: 0.45 }); K.rise("#b1", 0.6);
      K.lift("#o2", 1.3, { y: 20, dur: 0.45 }); K.rise("#b2", 1.75);""")

# L14 — „rok wcześniej nie kupiłaby… rok później też nie kupi” → only NOW
S["L14"] = dict(css="""
      .tlw { position: relative; padding-left: 58px; }
      .rail { position: absolute; left: 14px; top: 20px; bottom: 20px; width: 2px; background: var(--line); transform-origin: top center; }
      .ev { position: relative; padding: 20px 0; }
      .ev .dot { position: absolute; left: -54px; top: 34px; width: 22px; height: 22px; border-radius: 50%; border: 2px solid var(--mute); background: #090d19; }
      .ev .y { font-size: 30px; font-weight: 500; color: var(--mute); }
      .ev .v { font-size: 56px; font-weight: 300; letter-spacing: -0.03em; color: var(--mute); }
      .ev.now .dot { background: var(--accent); border-color: var(--accent); }
      .ev.now .y { color: var(--fg); }
      .ev.now .v { font-weight: 900; color: var(--fg); font-size: 80px; letter-spacing: -0.045em; }""", body="""
      <div class="card">
        <div class="lab" id="lab">Ta sama osoba</div><div class="sp"></div>
        <div class="tlw">
          <div class="rail" id="rail"></div>
          <div class="ev" id="e1"><div class="dot"></div><div class="y">Rok wcześniej</div><div class="v">nie kupi</div></div>
          <div class="ev now" id="e2"><div class="dot"></div><div class="y">Teraz, 3 tygodnie przed egzaminem</div><div class="v">kupi</div></div>
          <div class="ev" id="e3"><div class="dot"></div><div class="y">Rok później</div><div class="v">nie kupi</div></div>
        </div>
      </div>""", js="""
      K.card(DUR);
      K.rise("#lab", 0.1);
      tl.fromTo("#rail", { scaleY: 0 }, { scaleY: 1, duration: 0.9, ease: "power3.inOut" }, 0.2);
      K.lift("#e1", 0.62, { y: 20, dur: 0.5 });
      K.lift("#e3", 4.1, { y: 20, dur: 0.5 });
      K.lift("#e2", 5.5, { y: 0, s: 0.9, dur: 0.6, ease: "back.out(1.6)" });""")

# L15 — „musi przejść przez wszystkie trzy… nie przez dwa… nie przez jeden… wszystkie trzy”
S["L15"] = dict(css="""
      .p { display: flex; align-items: center; gap: 24px; padding: 14px 0; font-size: 52px; font-weight: 700; letter-spacing: -0.03em; }
      .sc { display: flex; align-items: baseline; justify-content: space-between; margin-top: 18px; padding-top: 26px; border-top: 1px solid var(--line); }
      .sc .n { font-size: 120px; font-weight: 900; letter-spacing: -0.06em; line-height: 0.9; position: relative; }
      .sc .n > div { position: absolute; right: 0; bottom: 0; white-space: nowrap; }
      .sc .l { font-size: 34px; font-weight: 500; color: var(--mute); position: relative; width: 260px; height: 44px; }
      .sc .l > div { position: absolute; left: 0; top: 0; white-space: nowrap; }""", body="""
      <div class="card">
        <div class="lab" id="lab">Zasada 3P</div><div class="sp"></div>
        <div class="p" id="p1">%CHK%Portfel</div>
        <div class="p" id="p2">%CHK%Problem</div>
        <div class="p" id="p3">%CHK%Pora</div>
        <div class="sc">
          <div class="l"><div id="l1">sprzedaje</div><div id="l2" class="neg">nie sprzedaje</div><div id="l3" class="acc">sprzedaje</div></div>
          <div class="n" style="width:250px;height:108px"><div id="s3a">3/3</div><div id="s2" class="neg">2/3</div><div id="s1" class="neg">1/3</div><div id="s3b" class="acc">3/3</div></div>
        </div>
      </div>""", js="""
      K.card(DUR);
      K.rise("#lab", 0.1);
      ["#p1", "#p2", "#p3"].forEach((p, i) => { K.lift(p, 0.2 + i * 0.16, { y: 18, dur: 0.45 }); K.tick(p, 0.5 + i * 0.22); });
      K.lift("#s3a", 1.7, { y: 30, dur: 0.5, ease: "expo.out" }); K.rise("#l1", 1.75);
      // „nie może przejść przez dwa” → 2/3
      K.tick("#p3", 3.0, false); tl.to("#s3a", { opacity: 0, duration: 0.15 }, 3.0); K.lift("#s2", 3.0, { y: 24, dur: 0.4 });
      K.sink("#l1", 2.95); K.rise("#l2", 3.1);
      // „nie może przejść przez jeden” → 1/3
      K.tick("#p2", 4.0, false); tl.to("#s2", { opacity: 0, duration: 0.15 }, 4.0); K.lift("#s1", 4.0, { y: 24, dur: 0.4 });
      // „musi przejść przez wszystkie trzy” → 3/3
      K.tick("#p2", 5.45); K.tick("#p3", 5.6); tl.to("#s1", { opacity: 0, duration: 0.15 }, 5.6); K.lift("#s3b", 5.6, { y: 24, dur: 0.45, ease: "back.out(1.8)" });
      K.sink("#l2", 5.5); K.rise("#l3", 5.65);""")

# L19 — „płacą za skrót, za kolejność i za pewność”
S["L19"] = dict(css="""
      .it { font-size: 92px; letter-spacing: -0.045em; line-height: 1.08; }""", body="""
      <div class="card">
        <div class="lab" id="lab">Za co naprawdę płacą</div><div class="sp"></div>
        <div class="it"><span class="ws" id="a"><span class="lo w300 mute">skrót.</span><span class="hi w900">skrót.</span></span></div>
        <div class="it"><span class="ws" id="b"><span class="lo w300 mute">kolejność.</span><span class="hi w900">kolejność.</span></span></div>
        <div class="it"><span class="ws" id="c"><span class="lo w300 mute">pewność.</span><span class="hi w900">pewność.</span></span></div>
      </div>""", js="""
      K.card(DUR);
      K.rise("#lab", 0.06, { stagger: 0.03 });
      K.lift(".it", 0.12, { y: 26, dur: 0.5, stagger: 0.07, ease: "expo.out" });
      K.weight("#a", 0.4); K.weight("#b", 0.96); K.weight("#c", 1.68);""")

# L22 — „a co jeśli to scam? Niska cena zdejmuje strach… ryzyko tak małe… łatwiej kliknąć… 59 zł?”
S["L22"] = dict(css="""
      .q { font-size: 56px; font-weight: 300; letter-spacing: -0.03em; }
      .pr { font-size: 150px; font-weight: 900; letter-spacing: -0.06em; line-height: 0.95; }
      .rk { display: flex; align-items: center; gap: 22px; margin-top: 8px; }
      .rk .t { font-size: 32px; font-weight: 500; color: var(--mute); width: 130px; }
      .rk .tr { flex: 1; height: 14px; border-radius: 7px; background: rgba(255,255,255,0.08); position: relative; overflow: hidden; }
      .rk .f { position: absolute; inset: 0; background: var(--neg); transform-origin: left center; }
      .btn { margin-top: 34px; height: 104px; border-radius: 999px; background: var(--accent); display: flex; align-items: center; justify-content: center;
             font-size: 44px; font-weight: 700; letter-spacing: -0.02em; }""", body="""
      <div class="card">
        <div class="q" id="q">A co jeśli to scam?</div><div class="sp"></div>
        <div class="pr" id="pr">59 zł</div><div class="sp"></div>
        <div class="rk" id="rk"><div class="t">Ryzyko</div><div class="tr"><div class="f" id="f"></div></div></div>
        <div class="btn" id="btn">Kupuję</div>
      </div>
      <svg class="cur" id="cur" viewBox="0 0 46 60"><path d="M4 3 L4 48 L15 37 L23 56 L31 52 L23 34 L39 34 Z" fill="#f4f6fa" stroke="#0a0d16" stroke-width="3" stroke-linejoin="round"/></svg>""", js="""
      K.card(DUR);
      K.rise("#q", 0.12, { stagger: 0.05 });
      K.rise("#pr", 0.98, { dur: 0.8 });
      K.lift("#rk", 2.0, { y: 16, dur: 0.45 });
      tl.fromTo("#f", { scaleX: 0 }, { scaleX: 0.92, duration: 0.5, ease: "power2.out" }, 2.2);
      K.strike("#q", 2.9);
      tl.to("#f", { scaleX: 0.08, duration: 1.0, ease: "expo.inOut" }, 4.3);
      K.lift("#btn", 5.4, { y: 26, dur: 0.55, ease: "expo.out" });
      K.click("#cur", 760, 900, 420, 560, 5.55, 6.03, null); tl.to("#cur", { opacity: 0, duration: 0.3 }, DUR - 0.34);
      tl.to("#btn", { scale: 0.95, duration: 0.09, ease: "power2.in", yoyo: true, repeat: 1 }, 6.05);
      tl.fromTo("#btn", { backgroundColor: "#3d7bff" }, { backgroundColor: "#2a5fd6", duration: 0.12, ease: "none", yoyo: true, repeat: 1, immediateRender: false }, 6.05);""")

# L25 — „ani słowa o tym, jak ładny jest plik, jakie czcionki, jaki prompt… pieniądze robi psychologia”
S["L25"] = dict(css="""
      .x { font-size: 60px; font-weight: 300; letter-spacing: -0.03em; line-height: 1.25; }""", body="""
      <div class="card">
        <div class="lab" id="lab">Ani słowa o</div><div class="sp"></div>
        <div><span class="x" id="x1">ładnym pliku</span></div>
        <div><span class="x" id="x2">czcionkach</span></div>
        <div><span class="x" id="x3">prompcie</span></div>
        <div class="hr"></div>
        <div class="lab" id="m">Pieniądze robi</div>
        <div class="k1" style="font-size:82px;font-weight:900" id="p">psychologia.</div>
      </div>""", js="""
      K.card(DUR);
      K.rise("#lab", 0.3, { stagger: 0.04 });
      K.rise("#x1", 1.55); K.rise("#x2", 2.88); K.rise("#x3", 3.92);
      K.strike("#x1", 4.4, { dim: true }); K.strike("#x2", 4.55); K.strike("#x3", 4.7);
      K.rise("#m", 6.1, { stagger: 0.04 });
      K.rise("#p", 6.55, { dur: 0.7 });""")

# L26b — „na wszystkich rodziców ósmoklasistów… 6 osób. Na wszystkich przed egzaminem na prawko… 6 osób”
S["L26b"] = dict(css="""
      .g { padding: 22px 0; border-top: 1px solid var(--line); }
      .g .w1 { font-size: 34px; font-weight: 400; color: var(--mute); line-height: 1.25; }
      .g .w2 { display: flex; align-items: baseline; gap: 18px; margin-top: 10px; }
      .g .w2 b { font-size: 120px; font-weight: 900; letter-spacing: -0.06em; line-height: 0.9; }
      .g .w2 span { font-size: 44px; font-weight: 300; }""", body="""
      <div class="card">
        <div class="lab" id="lab">Musisz znaleźć tylko</div><div class="sp"></div>
        <div class="g" id="g1"><div class="w1">Wszyscy rodzice ósmoklasistów w Polsce</div><div class="w2" id="n1"><b>6</b><span>osób dziennie</span></div></div>
        <div class="g" id="g2"><div class="w1">Wszyscy 3 tygodnie przed egzaminem na prawo jazdy</div><div class="w2" id="n2"><b>6</b><span>osób dziennie</span></div></div>
      </div>""", js="""
      K.card(DUR);
      K.rise("#lab", 0.1, { stagger: 0.04 });
      K.lift("#g1 .w1", 0.3, { y: 18, dur: 0.5 });
      K.lift("#n1", 3.6, { y: 34, dur: 0.55, ease: "expo.out" });
      K.lift("#g2 .w1", 4.3, { y: 18, dur: 0.5 });
      K.lift("#n2", 6.55, { y: 34, dur: 0.5, ease: "expo.out" });""")

# L30 — „od zera do gotowego produktu maksymalnie 90 minut… realnie 15–20 minut”
S["L30"] = dict(css="""
      .tm { display: flex; align-items: baseline; gap: 18px; }
      .tm b { font-size: 190px; font-weight: 900; letter-spacing: -0.065em; line-height: 0.9; }
      .tm span { font-size: 56px; font-weight: 300; }
      .sub2 { position: relative; height: 56px; margin-top: 18px; }
      .sub2 > div { position: absolute; left: 0; top: 0; white-space: nowrap; font-size: 38px; }""", body="""
      <div class="card">
        <div class="lab" id="lab">Od zera do gotowego produktu</div><div class="sp"></div>
        <div class="tm" id="tm"><b id="n">0</b><span>min</span></div>
        <div class="sub2"><div class="w300" id="s1">maksymalnie, z systemem AI</div><div class="w700 acc" id="s2">realnie: 15–20 minut</div></div>
      </div>""", js="""
      K.card(DUR);
      K.rise("#lab", 0.1, { stagger: 0.04 });
      K.lift("#tm", 1.0, { y: 30, dur: 0.6, ease: "expo.out" });
      K.count("#n", 0, 90, 1.05, 0.9, K.pl, "expo.out");
      K.rise("#s1", 2.5, { stagger: 0.04 });
      K.sink("#s1", 5.4);
      K.count("#n", 90, 15, 5.6, 0.9, K.pl, "expo.inOut");
      K.rise("#s2", 5.8, { stagger: 0.05 });""")

# L32 — „darmowy kurs… cały system AI z moją wiedzą… zapytać o swoją sytuację… stworzyć gotowy produkt”
S["L32"] = dict(css="""
      .li { display: flex; align-items: center; gap: 22px; font-size: 34px; font-weight: 500; padding: 16px 0; border-top: 1px solid var(--line); }
      .li i { width: 12px; height: 12px; border-radius: 50%; background: var(--accent); flex: none; }
      .free { display: inline-block; margin-top: 30px; padding: 16px 30px; border-radius: 999px; background: var(--accent); font-size: 36px; font-weight: 700; }""", body="""
      <div class="card">
        <div class="k1" style="font-size:72px" id="a">Darmowy kurs</div>
        <div class="k1" style="font-size:72px"><span class="ws" id="b"><span class="lo w300 mute">+ system AI</span><span class="hi w900">+ system AI</span></span></div>
        <div class="sp"></div>
        <div class="li" id="i1"><i></i>cała moja wiedza w środku</div>
        <div class="li" id="i2"><i></i>pytasz o swoją sytuację</div>
        <div class="li" id="i3"><i></i>dostajesz gotowy produkt</div>
        <div class="free" id="fr">Za darmo, link w opisie</div>
      </div>""", js="""
      K.card(DUR);
      K.rise("#a", 0.1);
      K.lift("#b", 1.2, { y: 30, dur: 0.6, ease: "expo.out" });
      K.weight("#b", 2.8);
      K.lift("#i1", 3.7, { y: 16, dur: 0.45 });
      K.lift("#i2", 5.35, { y: 16, dur: 0.45 });
      K.lift("#i3", 6.6, { y: 16, dur: 0.45 });
      K.lift("#fr", 8.6, { y: 20, s: 0.94, dur: 0.5, ease: "back.out(1.8)" });""")

# L32b — „link jest w opisie, za darmo”
S["L32b"] = dict(css="""
      .ar { width: 70px; height: 90px; margin-top: 30px; }""", body="""
      <div class="card">
        <div class="k1" style="font-size:72px" id="a">Link w opisie</div>
        <div class="k2 w300 acc" style="margin-top:14px" id="b">za darmo.</div>
        <svg class="ar" id="ar" viewBox="0 0 70 90"><path d="M35 6 V78 M10 54 L35 80 L60 54" fill="none" stroke="#f4f6fa" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/></svg>
      </div>""", js="""
      K.card(DUR);
      K.rise("#a", 0.6);
      K.lift("#ar", 1.0, { y: -20, dur: 0.4 });
      tl.to("#ar", { y: 16, duration: 0.42, ease: "sine.inOut", yoyo: true, repeat: 3 }, 1.4);
      K.rise("#b", 1.85);""")

# L33 — „zasubskrybuj”
S["L33"] = dict(css="""
      .ch { display: flex; align-items: center; gap: 26px; }
      .av { width: 96px; height: 96px; border-radius: 50%; background: var(--surface2); display: flex; align-items: center; justify-content: center; font-size: 44px; font-weight: 800; }
      .nm { font-size: 46px; font-weight: 700; letter-spacing: -0.02em; }
      .nm small { display: block; font-size: 28px; font-weight: 400; color: var(--mute); letter-spacing: 0; }
      .sb { position: relative; margin-top: 40px; height: 100px; }
      .sb > div { position: absolute; inset: 0; border-radius: 999px; display: flex; align-items: center; justify-content: center; gap: 18px; font-size: 42px; font-weight: 700; }
      .sb .s1 { background: var(--fg); color: #0a0d16; }
      .sb .s2 { background: var(--surface2); color: var(--fg); opacity: 0; }
      .cur { position: absolute; left: 340px; top: 215px; width: 46px; height: 60px; }""", body="""
      <div class="card" style="top:300px">
        <div class="ch" id="ch"><div class="av">K</div><div class="nm">Konrad Tatura<small>YouTube</small></div></div>
        <div class="sb" id="sb"><div class="s1">Subskrybuj</div>
          <div class="s2" id="s2"><svg width="40" height="42" viewBox="0 0 40 42"><path d="M20 4 C12 4 8 10 8 17 V26 L4 32 H36 L32 26 V17 C32 10 28 4 20 4 Z M15 36 C16 39 18 40 20 40 C22 40 24 39 25 36" fill="none" stroke="#f4f6fa" stroke-width="3.4" stroke-linejoin="round"/></svg>Subskrybujesz</div></div>
        <svg class="cur" id="cur" viewBox="0 0 46 60"><path d="M4 3 L4 48 L15 37 L23 56 L31 52 L23 34 L39 34 Z" fill="#f4f6fa" stroke="#0a0d16" stroke-width="3" stroke-linejoin="round"/></svg>
      </div>""", js="""
      K.card(DUR);
      K.lift("#ch", 0.08, { y: 18, dur: 0.5 });
      K.lift("#sb", 0.18, { y: 18, dur: 0.5 });
      tl.fromTo("#cur", { x: 160, y: 120, opacity: 0 }, { x: 0, y: 0, opacity: 1, duration: 0.6, ease: "power3.out" }, 0.3);
      tl.to("#sb", { scale: 0.96, duration: 0.08, ease: "power2.in", yoyo: true, repeat: 1 }, 0.95);
      tl.to("#cur", { scale: 0.88, duration: 0.08, yoyo: true, repeat: 1 }, 0.95);
      tl.fromTo("#s2", { opacity: 0 }, { opacity: 1, duration: 0.15, ease: "none", immediateRender: false }, 1.02);
      tl.fromTo("#s2 svg", { rotation: 0 }, { rotation: 16, duration: 0.09, yoyo: true, repeat: 5, ease: "sine.inOut", transformOrigin: "50% 10%", immediateRender: false }, 1.15);
      tl.to("#cur", { x: 120, y: 80, opacity: 0, duration: 0.5, ease: "power2.in" }, 2.0);""")

for k, s in S.items():
    js = s["js"].replace("DUR", str(D(k)))
    page(k, D(k), s["body"].replace("%CHK%", CHK), js, s.get("css", ""), overlay=True)
print(len(S), "cards")
