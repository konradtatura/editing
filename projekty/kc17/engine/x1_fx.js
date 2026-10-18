/* x1 = creatorh1v4 — vibe of the swipefile's "Joshua" (digital products) + "Ruwan": two-tier captions (small sentence + BIG word,
   money-green accent), real-UI mock-ups (notification, chat, Figma selection, reminder, IG link), glossy app tiles with "+",
   white full-screen inserts, light leaks. Natural footage (no grading). */
const GR = '#46F28C', GR2 = '#13C15C', INK = '#0E1116';
const SH = 'text-shadow:0 2px 3px rgba(0,0,0,.85),0 4px 16px rgba(0,0,0,.7),0 0 34px rgba(0,0,0,.45)';
const CARD = 'background:rgba(250,250,252,.96);border-radius:30px;box-shadow:0 26px 60px rgba(0,0,0,.45),0 0 0 1.5px rgba(255,255,255,.6)';
const tile = (c1, c2) => `border-radius:30%;display:flex;align-items:center;justify-content:center;color:#fff;background:linear-gradient(160deg,${c1},${c2});
  box-shadow:inset 0 4px 0 rgba(255,255,255,.45),inset 0 -8px 16px rgba(0,0,0,.25),0 20px 40px rgba(0,0,0,.45)`;

/* ---- captions: small context line + one big word; accent (h=1) green glow, h=2 hot orange ---- */
let capKey = -1;
window.CAPS = (spec, t, hide) => {
  const box = document.getElementById('caps'); let bi = -1;
  for (let i = 0; i < spec.caps.length; i++) { if (t >= spec.caps[i].t0 - .02) bi = i; else break }
  const b = spec.caps[bi]; if (hide || !b || t >= b.t1) { box.style.visibility = 'hidden'; return } box.style.visibility = 'visible';
  if (capKey !== bi) { capKey = bi; box.innerHTML = '';
    const ac = b.words.filter(w => w.h), sm = ac.length ? b.words.filter(w => !w.h) : [];
    const big = ac.length ? ac : b.words;
    if (sm.length) { const s = el('div', 'sm', box); s.textContent = sm.map(w => w.d).join(' '); s.dataset.t = sm[0].t }
    const g = el('div', 'bg' + (ac.length ? ' h' + ac[0].h : ''), box); g.textContent = big.map(w => w.d).join(' ').replace(/[,.]$/, ''); g.dataset.t = big[0].t;
    if (!ac.length) g.classList.add('mid') }
  box.style.top = (spec.capY * H) + 'px';
  box.querySelectorAll('.sm,.bg').forEach(n => pop(n, t, +n.dataset.t - .03, { s0: n.classList.contains('sm') ? .9 : .55, d: .26, b0: 8 }));
};

/* 1. macOS/iOS notification card */
B.notif = o => { o.e = abs(null, `left:110px;top:${o.y}px;width:860px;display:flex;gap:24px;align-items:center;padding:24px 30px;${CARD}`,
  `<div style="width:84px;height:84px;${tile(o.c1 || '#10A37F', o.c2 || '#0B7A5F')}">${ico(o.icon || 'sparkles', 46)}</div>
   <div style="flex:1"><div style="font:700 30px Inter;color:${INK}">${o.title}</div><div style="font:500 27px Inter;color:#5A606B;margin-top:4px">${o.sub}</div></div>
   ${o.amount ? `<div style="font:900 44px Inter;color:${GR2}">${o.amount}</div>` : `<div style="font:500 24px Inter;color:#9AA0A8">teraz</div>`}`) };
B.notif.u = (o, t) => { pop(o.e, t, o.t0, { y0: -90, s0: .9, ease: E.out5, d: .35 }); out(o.e, t, o.t1) };

/* 2. chat answers fly away, a product box lands (with Figma-style selection + typed label) */
B.swap = o => {
  const r = abs(null, `left:0;top:0;width:1080px;height:1920px`); o.e = r;
  o.bub = [0, 1, 2].map(i => abs(r, `left:${130 + i * 40}px;top:${o.y + i * 120}px;width:${700 - i * 80}px;height:96px;border-radius:36px;border-bottom-left-radius:10px;background:rgba(235,238,242,.95);box-shadow:0 14px 30px rgba(0,0,0,.35);
     display:flex;align-items:center;padding:0 30px;font:600 30px Inter;color:#5A606B`, i ? '••• kolejna odpowiedź' : 'Oto odpowiedź na Twoje pytanie…'));
  o.box = abs(r, `left:390px;top:${o.y - 10}px;width:300px;height:300px;font-size:250px;line-height:300px;text-align:center;filter:drop-shadow(0 26px 34px rgba(0,0,0,.55))`, '📦');
  o.sel = abs(r, `left:370px;top:${o.y + 10}px;width:340px;height:300px;border:3px solid #2F7BFF;display:flex;align-items:center;justify-content:center;font:700 36px Inter;color:#fff;${SH}`);
  ['left:-9px;top:-9px', 'right:-9px;top:-9px', 'left:-9px;bottom:-9px', 'right:-9px;bottom:-9px'].forEach(p => abs(o.sel, `${p};width:15px;height:15px;background:#fff;border:3px solid #2F7BFF`));
  o.selT = el('span', '', o.sel, '');
};
B.swap.u = (o, t) => {
  o.bub.forEach((b, i) => { pop(b, t, o.t0 + i * .18, { y0: 40, s0: .85 }); const k = E.inout(P(t, o.boxT - .25, .4)); if (k > 0) { b.style.transform += ` translate(${-900 * k}px,${-120 * k}px) rotate(${-14 * k}deg)`; b.style.opacity = 1 - k } });
  o.box.hidden = o.sel.hidden = !(t >= o.boxT);
  if (t >= o.boxT) { pop(o.box, t, o.boxT, { s0: .3, y0: 120, d: .4 }); pop(o.sel, t, o.boxT + .3, { s0: 1.15, d: .22 }) }   // selection just frames the box (no typed label)
};

/* 3. glossy app tiles combined with "+" (ebook + produkt + strona) */
B.equation = o => {
  const r = abs(null, `left:0;top:${o.y}px;width:1080px;height:330px`); o.e = r; const n = o.items.length, s = 200, gap = 110, x0 = 540 - (n * s + (n - 1) * gap) / 2;
  o.items.forEach((it, i) => { const x = x0 + i * (s + gap);
    it.e = abs(r, `left:${x}px;top:0;width:${s}px;height:${s}px;${tile(it.c1, it.c2)}`, ico(it.icon, 104, '#fff', 2.2));
    it.l = abs(r, `left:${x - 40}px;width:${s + 80}px;top:${s + 18}px;text-align:center;font:800 34px Inter;color:#fff;${SH}`, it.text);
    if (i) it.p = abs(r, `left:${x - gap / 2 - 30}px;top:${s / 2 - 40}px;width:60px;text-align:center;font:900 70px Inter;color:#fff;${SH}`, '+') });
};
B.equation.u = (o, t) => o.items.forEach(it => { const on = t >= it.t; [it.e, it.l, it.p].forEach(n => n && (n.hidden = !(on))); if (!on) return;
  pop(it.e, t, it.t, { s0: .3, y0: 60, rot: 0 }); pop(it.l, t, it.t + .08, { s0: .8 }); it.p && pop(it.p, t, it.t - .05, { s0: .2 });
  it.e.style.transform += ` translateY(${Math.sin((t - it.t) * 3) * 6}px)` });

/* 4. stacked sale notifications + big MOJE stamp */
B.sales = o => {
  const r = abs(null, 'left:0;top:0;width:1080px;height:1920px'); o.e = r;
  o.ns = o.notes.map(n => (n.e = abs(r, `left:110px;width:860px;top:${o.y}px;display:flex;gap:24px;align-items:center;padding:22px 30px;${CARD}`,
    `<div style="width:80px;height:80px;${tile(GR, GR2)}">${ico('banknote', 44)}</div><div style="flex:1"><div style="font:700 30px Inter;color:${INK}">Nowa sprzedaż</div>
     <div style="font:500 26px Inter;color:#5A606B">Twój produkt cyfrowy</div></div><div style="font:900 46px Inter;color:${GR2}">+79 zł</div>`), n));
};
B.sales.u = (o, t) => { const seen = o.notes.filter(n => t >= n.t).length;
  o.notes.forEach((n, i) => { const on = t >= n.t; n.e.hidden = !(on); if (!on) return; pop(n.e, t, n.t, { y0: -120, s0: .92, ease: E.out5, d: .32 });
    const depth = seen - 1 - i; n.e.style.transform += ` translateY(${depth * 26}px) scale(${1 - depth * .05})`; n.e.style.zIndex = 10 + i; n.e.style.filter = depth ? `brightness(${1 - depth * .08})` : 'none' }) };

/* 5. half-empty gauge: "pełne możliwości AI" */
B.gauge = o => { o.e = abs(null, `left:130px;top:${o.y}px;width:820px;padding:30px 34px;${CARD}`,
  `<div style="display:flex;justify-content:space-between;font:700 32px Inter;color:${INK}"><span>${o.label}</span><span id="pc" style="color:#9AA0A8"></span></div>
   <div style="margin-top:22px;height:34px;border-radius:17px;background:#E7EAEE;overflow:hidden"><div id="gf" style="height:100%;border-radius:17px;background:linear-gradient(90deg,#FFB347,#FF6A3D)"></div></div>
   <div style="margin-top:16px;font:500 26px Inter;color:#7A808A">${o.sub}</div>`) };
B.gauge.u = (o, t) => { pop(o.e, t, o.t0, { y0: 50, s0: .9 }); const f = E.out(P(t, o.t0 + .3, 1.2)) * o.fill; o.e.querySelector('#gf').style.width = f * 100 + '%'; out(o.e, t, o.t1) };

/* 6. emoji pills stacking (what people use AI for) + ok tag */
B.pills = o => { const r = abs(null, `left:0;top:${o.y}px;width:1080px;height:400px`); o.e = r;
  o.items.forEach((it, i) => it.e = abs(r, `left:${[110, 420, 250][i % 3]}px;top:${i * 112}px;padding:20px 32px;border-radius:999px;${CARD};font:700 38px Inter;color:${INK};white-space:nowrap`, `${it.emo}&nbsp; ${it.text}`));
  o.ok = abs(r, `left:700px;top:${o.items.length * 112 - 40}px;padding:14px 26px;border-radius:16px;background:${GR};color:#04230F;font:900 32px Inter;transform:rotate(6deg)`, o.okText) };
B.pills.u = (o, t) => { o.items.forEach(it => { const on = t >= it.t; it.e.hidden = !(on); if (on) pop(it.e, t, it.t, { s0: .4, x0: it.t % 2 ? 80 : -80 }) });
  o.ok.hidden = !(t >= o.okT); if (t >= o.okT) pop(o.ok, t, o.okT, { s0: 1.8, ease: E.out, d: .2, rot: 6 }) };

/* 7. light leak (transition flash) */
B.leak = o => { o.e = abs(null, `inset:0;mix-blend-mode:screen;background:radial-gradient(ellipse at 20% 30%,rgba(255,170,60,.95),rgba(255,90,20,.6) 35%,rgba(255,60,0,0) 70%),radial-gradient(ellipse at 90% 80%,rgba(255,220,140,.8),rgba(255,120,40,0) 60%)`) };
B.leak.u = (o, t) => { const k = (t - o.t0) / (o.t1 - o.t0); o.e.style.opacity = Math.sin(Math.PI * cl(k)); o.e.style.transform = `translateX(${lerp(-200, 200, k)}px) scale(1.3)` };

/* 8. single chat window collapsing into a product (box) with growth arrow */
B.chat2prod = o => { const r = abs(null, `left:0;top:${o.y}px;width:1080px;height:520px`); o.e = r;
  o.win = abs(r, `left:140px;top:0;width:800px;height:300px;${CARD};padding:28px 34px`, `<div style="display:flex;gap:14px;align-items:center;font:700 28px Inter;color:${INK}"><span style="width:16px;height:16px;border-radius:50%;background:#10A37F"></span>Rozmowa z AI</div>
    <div style="margin-top:22px;height:70px;border-radius:22px;background:#EEF1F4;width:80%"></div><div style="margin-top:16px;height:70px;border-radius:22px;background:#DFF7EA;width:65%;margin-left:auto"></div>`);
  o.box = abs(r, `left:400px;top:40px;width:280px;height:280px;font-size:230px;line-height:280px;text-align:center;filter:drop-shadow(0 24px 30px rgba(0,0,0,.5))`, '📦');
  o.tag = abs(r, `left:300px;top:330px;width:480px;text-align:center;padding:18px;border-radius:20px;background:${GR};color:#04230F;font:900 40px Inter`, 'Twój produkt');
  o.arr = abs(r, `left:700px;top:20px;color:${GR};filter:drop-shadow(0 6px 14px rgba(0,0,0,.5))`, ico('trending-up', 120, GR, 3)) };
B.chat2prod.u = (o, t) => { pop(o.win, t, o.t0, { y0: 60, s0: .9 }); const k = E.inout(P(t, o.prodT - .3, .35));
  if (k > 0) { o.win.style.transform += ` scale(${1 - .8 * k})`; o.win.style.opacity = 1 - k }
  [o.box, o.tag].forEach(n => n.hidden = !(t >= o.prodT)); if (t >= o.prodT) { pop(o.box, t, o.prodT, { s0: .2, d: .4 }); pop(o.tag, t, o.prodT + .2, { y0: 30, s0: .8 }) }
  o.arr.hidden = !(t >= o.growT); if (t >= o.growT) pop(o.arr, t, o.growT, { s0: .3, x0: -40, y0: 40 }) };

/* 9. white full-screen insert: brand title inside a Figma selection with cursor */
B.figma = o => { const p = abs(null, `inset:0;background:radial-gradient(circle at 50% 40%,#FFFFFF,#ECEEF2 70%,#DDE1E7)`); o.e = p;
  o.s = abs(p, `left:0;right:0;top:640px;text-align:center;font:600 46px Inter;color:#7A808A`, o.small);
  o.box = abs(p, `left:120px;top:740px;width:840px;height:330px;border:3px solid #2F7BFF;display:flex;flex-direction:column;align-items:center;justify-content:center`,
    `<div style="font:900 128px Inter;letter-spacing:-.05em;line-height:.9;color:${INK};text-align:center">${o.big}</div>`);
  ['left:-10px;top:-10px', 'right:-10px;top:-10px', 'left:-10px;bottom:-10px', 'right:-10px;bottom:-10px'].forEach(q => abs(o.box, `${q};width:17px;height:17px;background:#fff;border:3px solid #2F7BFF`));
  o.lb = abs(o.box, 'left:-3px;top:-46px;padding:4px 12px;background:#2F7BFF;color:#fff;font:600 24px Inter', 'Twój produkt · 840 × 330');
  o.cur = abs(p, 'left:0;top:0;width:70px;height:70px', `<svg viewBox="0 0 24 24" width="70" height="70"><path d="M4 2l15 9-7 1.5L9 20z" fill="#111" stroke="#fff" stroke-width="1.5"/></svg>`) };
B.figma.u = (o, t) => { pop(o.s, t, o.t0, { y0: 20, s0: .9 }); pop(o.box, t, o.bigT, { s0: .85, d: .35 }); const m = E.inout(P(t, o.bigT, .7));
  o.cur.style.transform = `translate(${lerp(980, 900, m)}px,${lerp(1500, 1050, m)}px)`; o.box.style.borderColor = t > o.bigT + .6 ? '#2F7BFF' : 'transparent' };

/* 10. iOS toggle: AI do zadań -> AI do budowania */
B.toggle = o => { o.e = abs(null, `left:150px;top:${o.y}px;width:780px;padding:30px 36px;${CARD};display:flex;align-items:center;gap:28px`,
  `<div style="flex:1"><div id="ta" style="font:800 40px Inter;color:${INK}">${o.a}</div><div id="tb" style="font:500 27px Inter;color:#7A808A;margin-top:6px">${o.sub}</div></div>
   <div id="tr" style="position:relative;width:150px;height:86px;border-radius:43px;background:#D7DBE0"><div id="kn" style="position:absolute;top:7px;left:7px;width:72px;height:72px;border-radius:50%;background:#fff;box-shadow:0 4px 12px rgba(0,0,0,.3)"></div></div>`) };
B.toggle.u = (o, t) => { pop(o.e, t, o.t0, { y0: 50, s0: .9 }); const k = E.out(P(t, o.flipT, .25));
  o.e.querySelector('#kn').style.left = (7 + 64 * k) + 'px'; o.e.querySelector('#tr').style.background = k > .5 ? GR2 : '#D7DBE0';
  o.e.querySelector('#ta').textContent = k > .5 ? o.b : o.a; out(o.e, t, o.t1) };

/* 11. path of tiles with arrows (pomysł → ebook → strona → marketing) */
B.flow = o => { const r = abs(null, `left:0;top:${o.y}px;width:1080px;height:300px`); o.e = r; const n = o.items.length, s = 150, gap = 92, x0 = 540 - (n * s + (n - 1) * gap) / 2;
  o.items.forEach((it, i) => { const x = x0 + i * (s + gap); it.e = abs(r, `left:${x}px;top:0;width:${s}px;height:${s}px;${tile(it.c1, it.c2)}`, ico(it.icon, 78, '#fff', 2.3));
    it.l = abs(r, `left:${x - 50}px;width:${s + 100}px;top:${s + 14}px;text-align:center;font:800 30px Inter;color:#fff;${SH}`, it.text);
    if (i) it.a = abs(r, `left:${x - gap + 14}px;top:${s / 2 - 26}px;color:#fff`, ico('arrow-right', 64, '#fff', 3)) }) };
B.flow.u = (o, t) => o.items.forEach(it => { const on = t >= it.t; [it.e, it.l, it.a].forEach(n => n && (n.hidden = !(on))); if (!on) return;
  pop(it.e, t, it.t, { s0: .3 }); pop(it.l, t, it.t + .06, { s0: .8 }); it.a && pop(it.a, t, it.t - .08, { s0: .4, x0: -30 }) });

/* 12. macOS reminder card with red dots, one line gets struck */
B.reminder = o => { const r = abs(null, `left:150px;top:${o.y}px;width:780px;padding:26px 34px;${CARD}`); o.e = r;
  abs(r, 'position:relative;font:800 34px Inter;color:#FF453A;margin-bottom:12px', o.title);
  o.rows = o.items.map(it => (it.e = el('div', '', r, `<span style="display:inline-block;width:26px;height:26px;border-radius:50%;border:3px solid #FF453A;margin-right:18px;vertical-align:-4px"></span><span class="tx">${it.text}</span>`),
    it.e.style.cssText = `position:relative;font:600 34px Inter;color:${INK};padding:14px 0;border-top:1px solid #E5E7EB`, it)) };
B.reminder.u = (o, t) => { pop(o.e, t, o.t0, { y0: 50, s0: .9 }); o.rows.forEach(it => { it.e.hidden = !(t >= it.t);
  const sk = it.strike && t >= it.strike; it.e.querySelector('.tx').style.textDecoration = sk ? 'line-through' : 'none'; it.e.querySelector('.tx').style.color = sk ? '#A0A4AB' : INK }); out(o.e, t, o.t1) };

/* 13. two pills: pracować szybciej (grey) vs budować coś swojego (green glow) */
B.duo = o => { const r = abs(null, `left:0;top:${o.y}px;width:1080px;height:300px`); o.e = r;
  o.a = abs(r, `left:110px;top:0;width:860px;text-align:center;padding:26px;border-radius:26px;background:rgba(30,32,36,.82);color:#C7CBD1;font:700 40px Inter`, `⚡ ${o.a0}`);
  o.b = abs(r, `left:110px;top:130px;width:860px;text-align:center;padding:26px;border-radius:26px;background:linear-gradient(180deg,${GR},${GR2});color:#04230F;font:900 44px Inter;box-shadow:0 0 60px rgba(70,242,140,.55)`, `🏗️ ${o.b0}`) };
B.duo.u = (o, t) => { pop(o.a, t, o.aT, { s0: .8, y0: 30 }); o.b.hidden = !(t >= o.bT); if (t >= o.bT) pop(o.b, t, o.bT, { s0: .5, y0: 40 }) };

/* 14. CTA: IG-style link sticker + finger tap */
B.link = o => { const r = abs(null, `left:0;top:${o.y}px;width:1080px;height:300px`); o.e = r;
  o.st = abs(r, `left:240px;top:30px;width:600px;height:120px;border-radius:30px;background:#fff;display:flex;align-items:center;justify-content:center;gap:18px;font:800 44px Inter;color:#2F7BFF;box-shadow:0 20px 50px rgba(0,0,0,.45)`,
    `${ico('arrow-down', 48, '#2F7BFF', 3)} ${o.text}`);
  o.f = abs(r, `left:640px;top:120px;font-size:120px;filter:drop-shadow(0 10px 16px rgba(0,0,0,.5))`, '👆') };
B.link.u = (o, t) => { pop(o.st, t, o.t0, { s0: .4 }); const ct = o.t0 + .7, m = E.out(P(t, o.t0 + .2, .45));
  o.f.style.transform = `translate(${(1 - m) * 200}px,${(1 - m) * 260}px) scale(${t > ct && t < ct + .14 ? .86 : 1})`;
  o.st.style.transform += ` scale(${t > ct && t < ct + .14 ? .95 : 1})`; const b = Math.abs(Math.sin((t - o.t0) * 3.2)) * 10; o.st.querySelector('span').style.transform = `translateY(${b}px)` };
