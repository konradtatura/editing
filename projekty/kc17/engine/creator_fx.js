/* Creator H1 v2 — NEW components in the style-2 language (turquoise glass, Inter + Instrument Serif italic, soft blur-in motion).
   Every builder: B.x = o => {...; o.e = root}  and  B.x.u = (o, t) => {...}.  Times are absolute seconds. */
const G = 'linear-gradient(180deg,#BDF3FF 0%,#5FD3E6 50%,#22B4CC 100%)';   // Konrad: same lighter gradient as the CTA button
const glass = 'background:rgba(245,250,252,.94);border-radius:34px;box-shadow:0 30px 70px rgba(0,0,0,.42),0 0 0 2px rgba(255,255,255,.5)';
const sh = 'text-shadow:0 1px 2px rgba(0,0,0,.85),0 3px 10px rgba(0,0,0,.75),0 0 30px rgba(0,0,0,.5)';
function abs(parent, css, html) { const d = el('div', '', parent, html || ''); d.style.cssText = 'position:absolute;' + css; return d; }
function typed(t, t0, text, cps = 26) { const n = Math.max(0, Math.min(text.length, Math.floor((t - t0) * cps))); return text.slice(0, n); }

/* 1. chat window typing an everyday prompt */
B.chat = o => {
  const r = abs(null, `left:110px;top:${o.y}px;width:860px;height:300px;${glass};overflow:hidden`); o.e = r;
  abs(r, 'left:34px;top:30px;font:700 26px Inter;color:#0B1A1E', `<span style="display:inline-block;width:14px;height:14px;border-radius:50%;background:#35C2DA;margin-right:10px"></span>ChatGPT`);
  o.q = abs(r, 'left:34px;top:90px;right:34px;min-height:70px;padding:20px 26px;border-radius:24px;background:#E4F4F8;font:500 32px Inter;color:#0B1A1E');
  o.dots = abs(r, 'left:34px;top:196px;font:900 44px Inter;color:#0E8FA8;letter-spacing:.12em', '•••');
};
B.chat.u = (o, t) => {
  appear(o.e, t, o.t0, { y0: 60, s0: .94 });
  o.q.textContent = typed(t, o.t0 + .25, o.text) + ((t * 2 | 0) % 2 ? '|' : '');
  const k = t - (o.t0 + .25 + o.text.length / 26); o.dots.style.opacity = k > 0 ? .35 + .65 * Math.abs(Math.sin(k * 6)) : 0;
  o.e.style.opacity = Math.min(+o.e.style.opacity, 1 - P(t, o.t1 - .18, .18));
};

/* 2. big gradient words revealed by a rising mask, line by line, with a turquoise underline swipe */
B.wipe = o => {
  const r = abs(null, `left:0;right:0;top:${o.y}px;text-align:center`); o.e = r;
  o.s = abs(r, `left:0;right:0;top:0;font:600 48px Inter;color:#fff;${sh}`, o.small);
  o.lines = o.big.map((l, i) => {
    const m = abs(r, `left:0;right:0;top:${70 + i * o.size * .95}px;height:${o.size}px;overflow:hidden`);
    const s = abs(m, `left:0;right:0;top:0;font:900 ${o.size}px Inter;letter-spacing:-.05em;line-height:1;filter:drop-shadow(0 6px 10px rgba(0,0,0,.6)) drop-shadow(0 14px 40px rgba(0,0,0,.6))`,
      `<span style="background:${G};-webkit-background-clip:text;background-clip:text;color:transparent">${l}</span>`); return s;
  });
  o.bar = abs(r, `left:50%;top:${70 + o.big.length * o.size * .95 + 18}px;height:10px;border-radius:5px;background:linear-gradient(90deg,#9EEBFF,#35C2DA);box-shadow:0 0 24px #35C2DA`);
};
B.wipe.u = (o, t) => {
  appear(o.s, t, o.t0, { y0: 16 });
  o.lines.forEach((s, i) => { const p = E.out5(P(t, o.bigT + i * .16, .42)); s.style.transform = `translateY(${(1 - p) * 110}%)` });
  const w = E.out(P(t, o.bigT + .35, .4)) * 520; o.bar.style.width = w + 'px'; o.bar.style.marginLeft = -w / 2 + 'px';
};

/* 3. "dodatkowy dochód": mini area chart drawing upward + pill */
B.income = o => {
  const r = abs(null, `left:140px;top:${o.y}px;width:800px;height:330px;${glass}`); o.e = r;
  r.innerHTML = `<svg width="800" height="330" style="position:absolute;left:0;top:0"><defs><linearGradient id="ig" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#35C2DA" stop-opacity=".45"/><stop offset="1" stop-color="#35C2DA" stop-opacity="0"/></linearGradient></defs>
   <path id="ia" d="M40 280 L180 250 L300 262 L430 200 L560 170 L700 80 L760 60 L760 300 L40 300Z" fill="url(#ig)"/>
   <path id="il" d="M40 280 L180 250 L300 262 L430 200 L560 170 L700 80 L760 60" fill="none" stroke="#0E8FA8" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>
   <circle id="id" r="15" fill="#fff" stroke="#0E8FA8" stroke-width="7"/></svg>`;
  o.pill = abs(r, 'left:36px;top:30px;padding:14px 26px;border-radius:999px;background:linear-gradient(180deg,#BDF3FF,#22B4CC);font:800 34px Inter;color:#04252D', o.label);
};
B.income.u = (o, t) => {
  appear(o.e, t, o.t0, { y0: 50 });
  const l = o.e.querySelector('#il'), L = l.getTotalLength(), p = E.out(P(t, o.t0 + .25, 1.6));
  l.style.strokeDasharray = L; l.style.strokeDashoffset = L * (1 - p);
  const pt = l.getPointAtLength(L * p), d = o.e.querySelector('#id'); d.setAttribute('cx', pt.x); d.setAttribute('cy', pt.y);
  o.e.querySelector('#ia').style.opacity = p * .9; appear(o.pill, t, o.lt, { s0: .7, ease: E.back });
};

/* 4. chat bubbles stacking up: what everybody uses ChatGPT for */
B.bubbles = o => {
  const r = abs(null, 'left:0;top:0;width:1080px;height:1920px'); o.e = r;
  o.items.forEach((it, i) => {
    const side = i % 2 ? 'right:90px' : 'left:90px';
    it.e = abs(r, `${side};top:${o.y - i * 112}px;padding:22px 34px;border-radius:40px;${i % 2 ? 'border-bottom-right-radius:10px' : 'border-bottom-left-radius:10px'};
      background:${i % 2 ? 'linear-gradient(180deg,#BDF3FF,#35C2DA)' : 'rgba(245,250,252,.95)'};box-shadow:0 18px 40px rgba(0,0,0,.35);font:700 38px Inter;color:#0B1A1E;white-space:nowrap`,
      `${it.emo}&nbsp; ${it.text}`);
  });
  o.ok = abs(r, `display:${o.okText ? 'block' : 'none'};left:0;right:0;top:${o.y - o.items.length * 112 - 40}px;text-align:center;font:400 italic 64px 'Instrument Serif';color:#9EEBFF;${sh}`, o.okText);
};
B.bubbles.u = (o, t) => {
  o.items.forEach(it => { const on = t >= it.t - .01; it.e.hidden = !(on); if (on) appear(it.e, t, it.t, { y0: 40, s0: .6, ease: E.back, d: .34 }); });
  o.ok.hidden = !(o.okText && t >= o.okT); if (o.okText && t >= o.okT) appear(o.ok, t, o.okT, { y0: 20 });
  if (t >= o.okT) o.items.forEach(it => it.e.style.opacity = lerp(1, .55, P(t, o.okT, .4)));
};

/* 5. full-screen "versus": everyday use vs building something yours */
B.versus = o => {
  const p = el('div', 'pl'); o.e = p; el('div', 'grain', p);
  o.c1 = abs(p, 'width:700px;height:700px;left:-320px;top:-260px;border-radius:50%;background:radial-gradient(circle at 30% 30%,#D8F8FF,#3FB9D0 62%,#14879F);opacity:.55');
  o.h = abs(p, 'left:0;right:0;top:330px;text-align:center;font:700 60px Inter;color:#fff', `Ogromna <span style="font:400 italic 72px 'Instrument Serif';color:#9EEBFF">różnica</span>`);
  const card = (x, dark, ic, a, b) => abs(p, `left:${x}px;top:620px;width:420px;height:560px;border-radius:36px;padding:44px 36px;
     background:${dark ? 'linear-gradient(160deg,#1B2A2E,#11191B)' : 'linear-gradient(160deg,#BDF3FF,#22B4CC)'};box-shadow:0 30px 70px rgba(0,0,0,.5)${dark ? '' : ',0 0 70px rgba(53,194,218,.55)'};
     color:${dark ? '#9fb3b8' : '#04252D'}`, `<div style="width:110px;height:110px;border-radius:28px;background:${dark ? '#26383C' : 'rgba(255,255,255,.55)'};display:flex;align-items:center;justify-content:center">${svg(ic)}</div>
     <div style="font:800 48px Inter;margin-top:56px;line-height:1.05">${a}</div><div style="font:500 32px Inter;margin-top:20px;opacity:.85">${b}</div>`);
  o.l = card(70, 1, 'clock', 'Używasz AI', 'do codziennych zadań'); o.r = card(590, 0, 'package', 'Tworzysz z AI', 'coś, co należy do Ciebie');
  [o.l, o.r].forEach(c => { const s = c.querySelector('svg'); if (s) { s.style.width = '60px'; s.style.height = '60px'; s.style.strokeWidth = 2.4 } });
  o.vs = abs(p, 'left:490px;top:840px;width:100px;height:100px;border-radius:50%;background:#fff;color:#0B1A1E;font:900 38px Inter;display:flex;align-items:center;justify-content:center;box-shadow:0 10px 30px rgba(0,0,0,.5)', 'VS');
};
B.versus.u = (o, t) => {
  o.c1.style.transform = `translate(${Math.sin(t * .6) * 30}px,${Math.cos(t * .5) * 24}px)`;
  appear(o.h, t, o.t0, { y0: 20 }); appear(o.l, t, o.lt, { x0: -80, s0: .92 }); appear(o.r, t, o.rt, { x0: 80, s0: .92 });
  appear(o.vs, t, o.lt + .25, { s0: .3, ease: E.back });
  const g = E.out(P(t, o.winT, .5)); o.r.style.transform += ` scale(${1 + .06 * g})`; o.l.style.opacity = Math.min(+o.l.style.opacity, 1 - .45 * g);
};

/* 6. 3D e-book mock-up swinging in, then "na sprzedaż" stamp */
B.ebook = o => {
  const r = abs(null, `left:0;top:0;width:1080px;height:1920px;perspective:1800px`); o.e = r;
  o.book = abs(r, `left:330px;top:${o.y}px;width:420px;height:560px;border-radius:10px 26px 26px 10px;transform-style:preserve-3d;
     background:linear-gradient(160deg,#0F2A31,#0B1A1E);box-shadow:-14px 0 0 #07282E inset,0 40px 80px rgba(0,0,0,.55);padding:56px 44px;color:#fff`,
    `<div style="font:500 26px Inter;color:#8fb4bc;letter-spacing:.2em">E-BOOK</div><div style="font:800 64px Inter;line-height:1;margin-top:26px;letter-spacing:-.03em">Twój<br>produkt</div>
     <div style="font:400 italic 46px 'Instrument Serif';color:#9EEBFF;margin-top:18px">z pomocą AI</div>
     <div style="position:absolute;left:44px;right:44px;bottom:50px;height:8px;border-radius:4px;background:linear-gradient(90deg,#9EEBFF,#35C2DA)"></div>`);
  o.tags = o.items.map((it, i) => (it.e = abs(r, `left:${i ? 700 : 110}px;top:${o.y + 80 + i * 170}px;padding:16px 26px;border-radius:999px;background:rgba(245,250,252,.95);font:700 32px Inter;color:#0B1A1E;box-shadow:0 14px 34px rgba(0,0,0,.35)`, it.text), it));
  o.stamp = abs(r, `left:300px;top:${o.y + 420}px;padding:16px 34px;border:6px solid #9EEBFF;border-radius:18px;font:900 50px Inter;color:#9EEBFF;letter-spacing:.04em;transform:rotate(-8deg);background:rgba(11,26,30,.75)`, 'NA SPRZEDAŻ');
};
B.ebook.u = (o, t) => {
  const p = E.out5(P(t, o.t0, .7)); o.book.style.opacity = P(t, o.t0, .25);
  o.book.style.transform = `rotateY(${lerp(-70, -16, p) + Math.sin(t * 1.2) * 2}deg) rotateX(4deg) translateY(${(1 - p) * 80}px)`;
  o.tags.forEach(it => { const on = t >= it.t; it.e.hidden = !(on); if (on) appear(it.e, t, it.t, { s0: .6, ease: E.back }) });
  const sp = P(t, o.stampT, .22); o.stamp.hidden = !(t >= o.stampT);
  o.stamp.style.transform = `rotate(-8deg) scale(${lerp(2.2, 1, E.out(sp))})`; o.stamp.style.opacity = sp;
};

/* 7. one answer = one problem  vs  one product sold again and again (notification stack + counter) */
B.sales = o => {
  const r = abs(null, 'left:0;top:0;width:1080px;height:1920px'); o.e = r;
  o.one = abs(r, `left:140px;top:${o.y}px;width:800px;padding:30px 36px;${glass};font:700 40px Inter;color:#0B1A1E;text-align:center`,
    `1 odpowiedź <span style="color:#0E8FA8">=</span> 1 problem`);
  o.ns = o.notes.map((n, i) => (n.e = abs(r, `left:150px;width:780px;top:${o.y + 150 + i * 168}px;display:flex;gap:22px;align-items:center;padding:20px 26px;${glass}`,
    `<div style="width:72px;height:72px;border-radius:20px;background:linear-gradient(160deg,#5FD3E6,#0E8FA8);display:flex;align-items:center;justify-content:center;color:#fff">${svg('banknote')}</div>
     <div style="flex:1"><div style="font:700 30px Inter;color:#0B1A1E">Nowa sprzedaż</div><div style="font:500 24px Inter;color:#46646c">Twój produkt cyfrowy</div></div>
     <div style="font:900 40px Inter;color:#0E8FA8">+79 zł</div>`), n));
  o.ns.forEach(n => { const s = n.e.querySelector('svg'); if (s) { s.style.width = '40px'; s.style.height = '40px' } });
  o.x = abs(r, `right:70px;top:${o.y - 40}px;font:900 150px Inter;letter-spacing:-.05em;filter:drop-shadow(0 8px 20px rgba(0,0,0,.6))`, `<span style="background:${G};-webkit-background-clip:text;color:transparent">×3</span>`);
};
B.sales.u = (o, t) => {
  o.one.hidden = !(t < o.notes[0].t); appear(o.one, t, o.t0, { y0: 30 });
  o.ns.forEach(n => { const on = t >= n.t; n.e.hidden = !(on); if (on) appear(n.e, t, n.t, { y0: -60, s0: .9, d: .32 }) });
  o.x.hidden = !(t >= o.xT); if (t >= o.xT) appear(o.x, t, o.xT, { s0: .4, ease: E.back });
};

/* 8. full-screen brand reveal with a light sweep */
B.brand = o => {
  const p = el('div', 'pl'); o.e = p; el('div', 'grain', p);
  o.k = abs(p, `left:0;right:0;top:640px;text-align:center;font:600 46px Inter;color:#9fb3b8`, o.small);
  o.w = abs(p, `left:0;right:0;top:730px;text-align:center;font:900 150px Inter;letter-spacing:-.05em;line-height:.95`,
    o.big.split('<br>').map(l => `<div><span style="background:${G};-webkit-background-clip:text;color:transparent">${l}</span></div>`).join(''));
  o.sw = abs(p, 'left:0;top:700px;width:260px;height:420px;background:linear-gradient(100deg,transparent,rgba(255,255,255,.55),transparent);mix-blend-mode:overlay;filter:blur(8px)');
};
B.brand.u = (o, t) => {
  appear(o.k, t, o.t0, { y0: 14 }); appear(o.w, t, o.bigT, { y0: 40, s0: .86, b0: 14, d: .5 });
  o.sw.style.transform = `translateX(${lerp(-300, 1200, P(t, o.bigT + .35, .8))}px) skewX(-15deg)`;
};

/* 9. strike-through: not more ChatGPT tricks  ->  your own product */
B.strike = o => {
  const r = abs(null, `left:110px;top:${o.y}px;width:860px`); o.e = r;
  o.a = abs(r, `left:0;right:0;top:0;padding:26px 34px;border-radius:30px;background:rgba(20,30,33,.85);font:700 40px Inter;color:#9fb3b8;text-align:center`, o.bad);
  o.ln = abs(o.a, 'left:30px;top:50%;height:7px;border-radius:4px;background:#FF5A5A');
  o.b = abs(r, `left:0;right:0;top:150px;padding:26px 34px;border-radius:30px;background:linear-gradient(180deg,#BDF3FF,#22B4CC);font:800 44px Inter;color:#04252D;text-align:center;box-shadow:0 0 50px rgba(53,194,218,.5)`, o.good);
};
B.strike.u = (o, t) => {
  appear(o.a, t, o.t0, { y0: 30 }); o.ln.style.width = E.out(P(t, o.strikeT, .3)) * 800 + 'px';
  o.b.hidden = !(t >= o.goodT); if (t >= o.goodT) appear(o.b, t, o.goodT, { y0: 30, s0: .85, ease: E.back });
};

/* 10. glowing path drawing through 3 nodes */
B.path = o => {
  const r = abs(null, `left:0;top:${o.y}px;width:1080px;height:300px`); o.e = r;
  o.line = abs(r, 'left:150px;top:96px;height:10px;border-radius:5px;background:linear-gradient(90deg,#9EEBFF,#35C2DA);box-shadow:0 0 30px #35C2DA');
  o.nodes = o.items.map((it, i) => { const x = 150 + i * 390;
    it.n = abs(r, `left:${x - 66}px;top:35px;width:132px;height:132px;border-radius:36px;display:flex;align-items:center;justify-content:center;color:#fff;
      background:linear-gradient(160deg,rgba(170,240,255,.9),rgba(53,194,218,.85) 45%,rgba(11,120,145,.9));box-shadow:inset 0 3px 0 rgba(255,255,255,.65),0 18px 40px rgba(0,40,55,.45)`, svg(it.icon));
    const s = it.n.querySelector('svg'); if (s) { s.style.width = '64px'; s.style.height = '64px'; s.style.strokeWidth = 2.5 }
    it.l = abs(r, `left:${x - 150}px;width:300px;top:190px;text-align:center;font:800 36px Inter;color:#fff;${sh}`, it.text); return it; });
};
B.path.u = (o, t) => {
  const last = o.items[o.items.length - 1].t; o.line.style.width = E.out(P(t, o.items[0].t, last - o.items[0].t + .2)) * 780 + 'px';
  o.items.forEach(it => { const on = t >= it.t; it.n.hidden = it.l.hidden = !(on); if (on) { appear(it.n, t, it.t, { s0: .4, ease: E.back }); appear(it.l, t, it.t + .06, { y0: 14 }) } });
};

/* 11. A -> Z */
B.atoz = o => {
  const r = abs(null, `left:0;top:${o.y}px;width:1080px;height:360px`); o.e = r;
  const L = (x, c) => abs(r, `left:${x}px;top:0;width:220px;text-align:center;font:900 220px Inter;line-height:1;letter-spacing:-.05em;filter:drop-shadow(0 8px 22px rgba(0,0,0,.6))`,
    `<span style="background:${G};-webkit-background-clip:text;color:transparent">${c}</span>`);
  o.A = L(120, 'A'); o.Z = L(740, 'Z');
  o.ar = abs(r, 'left:350px;top:104px;height:12px;border-radius:6px;background:#fff;box-shadow:0 0 20px rgba(158,235,255,.9)');
  o.cap = abs(r, `left:0;right:0;top:250px;text-align:center;font:400 italic 64px 'Instrument Serif';color:#9EEBFF;${sh}`, o.label);
};
B.atoz.u = (o, t) => {
  appear(o.A, t, o.aT, { s0: .5, ease: E.back }); o.ar.style.width = E.out(P(t, o.aT + .05, Math.max(.15, o.zT - o.aT - .05))) * 370 + 'px';
  o.Z.hidden = !(t >= o.zT); if (t >= o.zT) appear(o.Z, t, o.zT, { s0: .5, ease: E.back, d: .22 }); o.cap.hidden = !o.label; if (o.label) appear(o.cap, t, o.t0 + .1, { y0: 14 });
};

/* 12. label morph: tool that saves time -> tool you build with */
B.morph = o => {
  const r = abs(null, `left:110px;top:${o.y}px;width:860px;height:160px`); o.e = r;
  o.a = abs(r, `left:0;right:0;top:0;padding:28px;border-radius:30px;background:rgba(20,30,33,.85);font:700 40px Inter;color:#9fb3b8;text-align:center`, o.a0);
  o.b = abs(r, `left:0;right:0;top:0;padding:28px;border-radius:30px;background:linear-gradient(180deg,#BDF3FF,#22B4CC);font:800 44px Inter;color:#04252D;text-align:center;box-shadow:0 0 50px rgba(53,194,218,.5)`, o.b0);
};
B.morph.u = (o, t) => {
  appear(o.a, t, o.t0, { y0: 30 }); const p = E.out(P(t, o.swapT, .4));
  o.a.style.transform = `rotateX(${p * 90}deg)`; o.a.style.opacity = 1 - p;
  o.b.style.transform = `rotateX(${(1 - p) * -90}deg)`; o.b.style.opacity = p;
};

/* 13. CTA: button + cursor tap with ripple */
B.tap = o => {
  const r = abs(null, `left:0;top:${o.y}px;width:1080px;height:300px`); o.e = r;
  o.btn = abs(r, 'left:240px;top:40px;width:600px;height:124px;border-radius:999px;display:flex;align-items:center;justify-content:center;gap:16px;font:800 46px Inter;color:#04252D;background:linear-gradient(180deg,#BDF3FF,#5FD3E6 50%,#22B4CC);box-shadow:inset 0 2px 0 rgba(255,255,255,.7),0 16px 40px rgba(0,0,0,.4),0 0 50px rgba(53,194,218,.5)', `${o.text} ${svg('arrow-down')}`);
  const s = o.btn.querySelector('svg'); if (s) { s.style.width = '46px'; s.style.height = '46px'; s.style.strokeWidth = 3 }
  o.rip = abs(r, 'left:640px;top:102px;width:20px;height:20px;border-radius:50%;border:5px solid rgba(255,255,255,.9)');
  o.cur = abs(r, 'left:620px;top:90px;width:80px;height:80px;color:#fff;filter:drop-shadow(0 6px 10px rgba(0,0,0,.6))', svg('mouse-pointer-click'));
  const c = o.cur.querySelector('svg'); if (c) { c.style.width = '80px'; c.style.height = '80px'; c.style.fill = '#fff'; c.style.stroke = '#0B1A1E'; c.style.strokeWidth = 1.6 }
};
B.tap.u = (o, t) => {
  appear(o.btn, t, o.t0, { y0: 40, s0: .8, ease: E.back });
  const ct = o.t0 + .55, mv = E.out(P(t, o.t0 + .15, .4)); o.cur.style.transform = `translate(${(1 - mv) * 260}px,${(1 - mv) * 220}px) scale(${t > ct && t < ct + .12 ? .85 : 1})`;
  o.btn.style.transform += ` scale(${t > ct && t < ct + .12 ? .96 : 1})`;
  const rp = P(t, ct, .5); o.rip.style.opacity = t > ct ? 1 - rp : 0; o.rip.style.transform = `translate(-50%,-50%) scale(${1 + rp * 9})`;
  const b = Math.abs(Math.sin((t - o.t0) * 3)) * 10; o.btn.querySelector('svg') && (o.btn.querySelector('svg').style.transform = `translateY(${b}px)`);
};
