/* Skill H2 v2 — NEW components in the style-3 language (navy #05071A, electric blue #3B3BFF, moving light blobs, white UI,
   Instrument Serif italic accents). Builders: B.x = o => {...; o.e = root};  B.x.u = (o, t) => {...}. */
/* style-3 motion = quick focus pull (blur 14 px + scale from 112 %), like overlay3 blurIn; options y0/x0/s0/ease/d/b0 */
function appear(e, t, t0, o = {}) { const d = o.d || .24, p = P(t, t0, d), pe = (o.ease || E.out)(p);
  e.style.opacity = E.out(P(t, t0, d * .7)); e.style.filter = p < 1 ? `blur(${(1 - pe) * (o.b0 ?? 14)}px)` : 'none';
  e.style.transform = `translate(${(1 - pe) * (o.x0 || 0)}px,${(1 - pe) * (o.y0 ?? 0)}px) scale(${lerp(o.s0 ?? 1.12, 1, pe)})`; return p; }
const BL = '#3B3BFF', BL2 = '#5B5BFF', RED = '#FF4D5E';
function abs(parent, css, html) { const d = el('div', '', parent, html || ''); d.style.cssText = 'position:absolute;' + css; return d; }
function ico(name, px, col) { const h = svg(name); return `<span style="display:inline-flex;width:${px}px;height:${px}px;color:${col || 'currentColor'}">${h.replace('<svg', `<svg style="width:100%;height:100%;stroke-width:2.4"`)}</span>`; }
function icoC(name, px, col, sw) { return `<span style="position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);display:block;width:${px}px;height:${px}px;color:${col || 'currentColor'}">${svg(name).replace('<svg', `<svg style="display:block;width:100%;height:100%;stroke-width:${sw || 2.4}"`)}</span>` }
function blobs(p) { return [['#3B3BFF', 520, 120, 300], ['#1B1BB0', 620, 620, 1300], ['#5B5BFF', 380, 760, 620]].map(([c, s, x, y]) => abs(p, `width:${s}px;height:${s}px;left:${x - s / 2}px;top:${y - s / 2}px;border-radius:50%;background:${c};filter:blur(110px);opacity:.75`)); }
function moveBlobs(bs, t) { bs.forEach((b, i) => b.style.transform = `translate(${Math.sin(t * .5 + i * 2) * 60}px,${Math.cos(t * .4 + i) * 50}px)`); }
const tileCss = (x, y, s) => `left:${x - s / 2}px;top:${y - s / 2}px;width:${s}px;height:${s}px;border-radius:${s * .26}px;display:flex;align-items:center;justify-content:center;
  background:#fff;color:#0B0D24;box-shadow:0 20px 50px rgba(0,0,30,.5)`;

/* 1. three skills you "don't have" — locked; on "AI zmieniła" the locks fall off and tiles turn electric blue */
B.locks = o => {
  const r = abs(null, `left:0;top:${o.y}px;width:1080px;height:420px`); o.e = r;
  o.items.forEach((it, i) => { const x = 220 + i * 320;
    it.e = abs(r, tileCss(x, 130, 210), icoC(it.icon, 104));
    it.lk = abs(r, `left:${x + 40}px;top:150px;width:96px;height:96px;border-radius:50%;background:${RED};display:flex;align-items:center;justify-content:center;color:#fff;box-shadow:0 10px 26px rgba(120,0,20,.5)`, icoC('x', 54));
    it.lb = abs(r, `left:${x - 160}px;width:320px;top:265px;text-align:center;font:800 40px Inter;color:#fff;letter-spacing:-.02em;text-shadow:0 4px 14px rgba(0,0,0,.6)`, it.text); });
};
B.locks.u = (o, t) => {
  const u = E.out(P(t, o.unlockT, .35));
  o.items.forEach((it, i) => { const on = t >= it.t; [it.e, it.lk, it.lb].forEach(n => n.style.display = on ? '' : 'none'); if (!on) return;
    appear(it.e, t, it.t, { s0: .4, ease: E.back, y0: 40 }); appear(it.lb, t, it.t + .05, { y0: 16 });
    const shake = t > o.shakeT && t < o.shakeT + .45 ? Math.sin((t - o.shakeT) * 70) * 9 * (1 - (t - o.shakeT) / .45) : 0;
    it.e.style.transform += ` translateX(${shake}px)`;
    it.e.style.background = u > .5 ? `linear-gradient(160deg,${BL2},${BL})` : '#fff'; it.e.style.color = u > .5 ? '#fff' : '#0B0D24';
    it.e.style.boxShadow = u > .5 ? `0 0 ${60 * u}px ${BL},0 20px 50px rgba(0,0,30,.5)` : '0 20px 50px rgba(0,0,30,.5)';
    const lp = P(t, it.t + .15, .25); it.lk.style.opacity = Math.min(lp, 1 - u);
    it.lk.style.transform = `translate(0,${u * 260 + i * u * 40}px) rotate(${u * (i - 1) * 70}deg) scale(${lerp(1.8, 1, E.out(lp))})`; });
};

/* 2. "kiedyś": three skills to learn — progress bars that crawl and never finish */
B.bars = o => {
  const r = abs(null, `left:80px;top:${o.y}px;width:920px`); o.e = r;
  o.h = abs(r, `left:0;top:0;font:400 italic 64px 'Instrument Serif';color:#fff;text-shadow:0 4px 14px rgba(0,0,0,.6)`, o.head || ''); if (!o.head) o.h.style.display = 'none';
  o.items.forEach((it, i) => { const y = 100 + i * 120;
    it.e = abs(r, `left:0;right:0;top:${y}px;height:96px;border-radius:18px;background:rgba(5,7,26,.82);box-shadow:0 14px 40px rgba(0,0,30,.45);overflow:hidden`);
    it.f = abs(it.e, `left:0;top:0;bottom:0;background:linear-gradient(90deg,${BL},${BL2})`);
    abs(it.e, 'left:30px;top:0;bottom:0;display:flex;align-items:center;font:800 42px Inter;color:#fff', it.text);
    it.p = abs(it.e, 'right:30px;top:0;bottom:0;display:flex;align-items:center;font:700 34px Inter;color:#c9ccff'); });
};
B.bars.u = (o, t) => {
  if (o.head) appear(o.h, t, o.t0, { y0: 20 });
  o.items.forEach(it => { const on = t >= it.t; it.e.style.display = on ? '' : 'none'; if (!on) return; appear(it.e, t, it.t, { x0: -60, s0: .96 });
    const pr = Math.min(.42, (t - it.t) * .07); it.f.style.width = pr * 100 + '%'; it.p.textContent = Math.round(pr * 100) + '%'; });
};

/* 3. full screen: two options die, option 3 (AI) lands */
B.options = o => {
  const p = el('div', 'pl'); o.e = p; o.bs = blobs(p); el('div', 'grain', p);
  o.h = abs(p, 'left:0;right:0;top:330px;text-align:center;font:900 96px Inter;color:#fff;letter-spacing:-.05em', 'Dwie opcje');
  const card = (x, n, ic, a) => abs(p, `left:${x}px;top:620px;width:450px;height:700px;border-radius:38px;padding:56px 44px;background:#fff;color:#0B0D24;box-shadow:0 30px 80px rgba(0,0,30,.6)`,
    `<div style="font:900 170px Inter;color:${BL};letter-spacing:-.05em;line-height:1">${n}</div><div style="margin-top:40px">${ico(ic, 110)}</div><div style="font:800 62px Inter;margin-top:44px;line-height:1.02;letter-spacing:-.03em">${a}</div>`);
  o.c1 = card(60, 1, 'clock', 'Miesiące<br>nauki'); o.c2 = card(570, 2, 'wallet', 'Zapłacić<br>komuś');
  o.c3 = abs(p, `left:110px;top:560px;width:860px;height:760px;border-radius:44px;padding:60px 56px;background:linear-gradient(160deg,${BL2},${BL} 60%,#2222C8);color:#fff;
     box-shadow:0 0 120px rgba(80,80,255,.75),0 40px 90px rgba(0,0,30,.6)`,
    `<div style="font:900 200px Inter;letter-spacing:-.06em;line-height:.9">3</div><div style="font:400 italic 92px 'Instrument Serif';margin-top:30px">trzecia opcja</div>
     <div id="ai" style="margin-top:44px;display:inline-flex;align-items:center;gap:20px;padding:20px 36px;border-radius:999px;background:#fff;color:${BL};font:900 64px Inter">${ico('sparkles', 64)} AI</div>`);
  o.fl = abs(p, 'inset:0;background:radial-gradient(circle at 50% 50%,rgba(220,225,255,.95),rgba(120,130,255,.4) 60%,rgba(5,7,26,0))');
};
B.options.u = (o, t) => {
  moveBlobs(o.bs, t); const hs = t >= (o.hT || 0); o.h.textContent = hs ? 'Dwie opcje' : (o.h0 || 'Dwie opcje'); appear(o.h, t, hs ? o.hT : o.t0, { y0: 30 });
  [[o.c1, o.c1T], [o.c2, o.c2T]].forEach(([c, ct]) => { c.style.display = t >= ct ? '' : 'none'; if (t >= ct) appear(c, t, ct, { y0: 80, s0: .9 });
    const d = E.out(P(t, o.c3T, .4)); if (d > 0) { c.style.opacity = 1 - .8 * d; c.style.filter = `blur(${d * 6}px)`; c.style.transform += ` scale(${1 - .15 * d}) translateY(${-140 * d}px)` } });
  o.h.style.opacity = Math.min(+o.h.style.opacity, 1 - P(t, o.c3T, .25));
  o.c3.style.display = t >= o.c3T ? '' : 'none'; if (t >= o.c3T) appear(o.c3, t, o.c3T, { y0: 300, s0: .9, d: .45 });
  const ai = o.c3.querySelector('#ai'); const ap = P(t, o.aiT, .3); ai.style.opacity = ap; ai.style.transform = `scale(${lerp(.4, 1, E.back(ap))})`;
  const fp = P(t, o.c3T, .35); o.fl.style.opacity = t >= o.c3T ? (1 - fp) * .9 : 0;
};

/* 4. AI builds each piece: document -> web page -> sales offer (one card, content morphs) */
B.builds = o => {
  const r = abs(null, `left:150px;top:${o.y}px;width:780px;height:470px;border-radius:30px;background:#fff;box-shadow:0 30px 80px rgba(0,0,30,.55);overflow:hidden`); o.e = r;
  o.badge = abs(r, `right:26px;top:24px;padding:10px 22px;border-radius:999px;background:${BL};color:#fff;font:900 30px Inter;display:flex;gap:10px;align-items:center`, `${ico('sparkles', 30)} AI`);
  o.title = abs(r, 'left:36px;top:30px;font:900 44px Inter;color:#0B0D24;letter-spacing:-.03em');
  o.doc = abs(r, 'left:36px;right:36px;top:110px;bottom:30px');
  o.docRows = ['Struktura', 'Rozdziały', 'Pierwsza wersja treści'].map((x, i) => abs(o.doc, `left:0;right:0;top:${i * 106}px;height:86px;border-radius:16px;background:#F0F1FF;display:flex;align-items:center;gap:20px;padding:0 24px;font:700 36px Inter;color:#0B0D24`,
    `<span style="width:44px;height:44px;border-radius:50%;background:${BL};display:inline-flex;align-items:center;justify-content:center;color:#fff">${ico('check', 28)}</span>${x}`));
  o.web = abs(r, 'left:36px;right:36px;top:110px;bottom:30px');
  o.webParts = [abs(o.web, 'left:0;right:0;top:0;height:40px;border-radius:10px;background:#E6E7FF'),
    abs(o.web, 'left:0;width:420px;top:70px;height:150px;border-radius:14px;background:linear-gradient(160deg,#C9CCFF,#8E92FF)'),
    abs(o.web, 'left:450px;right:0;top:70px;height:30px;border-radius:8px;background:#E6E7FF'), abs(o.web, 'left:450px;right:40px;top:120px;height:30px;border-radius:8px;background:#E6E7FF'),
    abs(o.web, `left:0;width:300px;top:250px;height:76px;border-radius:999px;background:${BL};color:#fff;font:800 34px Inter;display:flex;align-items:center;justify-content:center`, 'Kup teraz')];
  o.off = abs(r, 'left:36px;right:36px;top:110px;bottom:30px');
  o.offParts = [abs(o.off, `left:0;right:0;top:0;font:400 italic 56px 'Instrument Serif';color:#0B0D24`, '„Rozwiąż X w 7 dni”'),
    abs(o.off, 'left:0;right:0;top:90px;font:600 32px Inter;color:#55597A;line-height:1.35', '✓ dla kogo jest produkt<br>✓ co dokładnie dostajesz<br>✓ dlaczego warto teraz'),
    abs(o.off, `left:0;top:270px;padding:14px 30px;border-radius:14px;background:${BL};color:#fff;font:900 40px Inter`, 'Oferta gotowa')];
};
B.builds.u = (o, t) => {
  appear(o.e, t, o.t0, { y0: 60, s0: .94 }); appear(o.badge, t, o.t0 + .2, { s0: .5, ease: E.back });
  const st = o.steps.filter(s => t >= s.t).length - 1, s = o.steps[Math.max(0, st)]; o.title.textContent = s.title;
  [o.doc, o.web, o.off].forEach((n, i) => n.style.display = i === Math.max(0, st) ? '' : 'none');
  if (st <= 0) o.docRows.forEach((n, i) => appear(n, t, o.steps[0].t + .3 + i * .55, { x0: -40 }));
  if (st === 1) o.webParts.forEach((n, i) => appear(n, t, s.t + .15 + i * .22, { y0: 20, s0: .8 }));
  if (st === 2) o.offParts.forEach((n, i) => appear(n, t, s.t + .15 + i * .35, { y0: 20 }));
  if (st > 0) { const k = P(t, s.t, .3); o.e.style.transform += ` rotateY(${(1 - E.out(k)) * 25}deg)` }
};

/* 5. full screen: three skill tiles orbit and merge into one block = Cyfrowy Autopilot */
B.merge = o => {
  const p = el('div', 'pl'); o.e = p; o.bs = blobs(p); el('div', 'grain', p);
  o.h = abs(p, 'left:0;right:0;top:330px;text-align:center;font:700 54px Inter;color:#fff', o.head);
  o.tiles = ['file-text', 'layout-template', 'megaphone'].map(n => abs(p, tileCss(540, 960, 190), icoC(n, 96)));
  o.blk = abs(p, `left:150px;top:720px;width:780px;height:470px;border-radius:44px;background:linear-gradient(160deg,${BL2},${BL} 60%,#2222C8);color:#fff;padding:58px 54px;box-shadow:0 0 140px rgba(80,80,255,.8)`,
    `<div style="font:900 104px Inter;letter-spacing:-.05em;line-height:.92">Cyfrowy<br>Autopilot</div><div style="font:400 italic 58px 'Instrument Serif';margin-top:34px">jeden konkretny proces</div>`);
  o.fl = abs(p, 'inset:0;background:radial-gradient(circle at 50% 50%,rgba(230,232,255,.95),rgba(120,130,255,.35) 55%,rgba(5,7,26,0))');
};
B.merge.u = (o, t) => {
  moveBlobs(o.bs, t); appear(o.h, t, o.t0, { y0: 20 });
  const m = E.out5(P(t, o.mergeT - .5, .5));
  o.tiles.forEach((n, i) => { const a = (t - o.t0) * 1.6 + i * 2.094, R = 300 * (1 - m);
    n.style.opacity = Math.min(P(t, o.t0 + i * .12, .3), 1 - P(t, o.mergeT, .1));
    n.style.transform = `translate(${Math.cos(a) * R}px,${Math.sin(a) * R * .55}px) scale(${1 - .5 * m})` });
  o.blk.style.display = t >= o.mergeT ? '' : 'none'; if (t >= o.mergeT) appear(o.blk, t, o.mergeT, { s0: .5, ease: E.back, d: .45, b0: 4 });
  const fp = P(t, o.mergeT, .35); o.fl.style.opacity = t >= o.mergeT ? (1 - fp) * .85 : 0;
};

/* 6. chevron steps filling blue: pomysł › produkt › strona */
B.chev = o => {
  const r = abs(null, `left:60px;top:${o.y}px;width:960px;height:140px`); o.e = r;
  o.items.forEach((it, i) => { const x = i * 315;
    it.e = abs(r, `left:${x}px;top:0;width:330px;height:120px;clip-path:polygon(0 0,86% 0,100% 50%,86% 100%,0 100%,14% 50%);background:#fff;color:#0B0D24;
      display:flex;align-items:center;justify-content:center;font:800 36px Inter;padding-left:44px;filter:drop-shadow(0 14px 30px rgba(0,0,30,.5))`, it.text); });
  o.az = abs(r, `left:0;right:0;top:150px;text-align:center;font:400 italic 60px 'Instrument Serif';color:#fff;text-shadow:0 4px 14px rgba(0,0,0,.6)`, o.label);
};
B.chev.u = (o, t) => {
  o.items.forEach(it => { const on = t >= it.t; it.e.style.display = on ? '' : 'none'; if (!on) return; appear(it.e, t, it.t, { x0: -70, s0: .9 });
    const f = P(t, it.t + .2, .3) > 0.5; it.e.style.background = f ? BL : '#fff'; it.e.style.color = f ? '#fff' : '#0B0D24' });
  o.az.style.display = o.label && t >= o.azT ? '' : 'none'; if (t >= o.azT) appear(o.az, t, o.azT, { y0: 16 });
};

/* 7. "ekspert od wszystkiego" badge gets a NIE MUSISZ stamp */
B.expert = o => {
  const r = abs(null, `left:0;top:${o.y}px;width:1080px;height:300px`); o.e = r;
  o.b = abs(r, 'left:170px;top:20px;width:740px;padding:30px;border-radius:26px;background:#fff;color:#0B0D24;text-align:center;font:800 46px Inter;box-shadow:0 24px 60px rgba(0,0,30,.5)', `${ico('user', 46)}&nbsp; ekspert od wszystkiego`);
  o.s = abs(r, `left:310px;top:120px;padding:12px 34px;border:7px solid ${RED};border-radius:16px;color:${RED};font:900 60px Inter;background:rgba(255,255,255,.92);transform:rotate(-7deg)`, 'NIE MUSISZ');
};
B.expert.u = (o, t) => {
  appear(o.b, t, o.t0, { y0: 40 }); const sp = P(t, o.stampT, .2); o.s.style.display = t >= o.stampT ? '' : 'none';
  o.s.style.opacity = sp; o.s.style.transform = `rotate(-7deg) scale(${lerp(2.4, 1, E.out(sp))})`;
};

/* 8. CTA: blue pill with expanding rings */
B.cta2 = o => {
  const r = abs(null, `left:0;top:${o.y}px;width:1080px;height:200px`); o.e = r;
  o.rings = [0, 1].map(() => abs(r, `left:540px;top:70px;width:620px;height:130px;margin-left:-310px;margin-top:-65px;border-radius:999px;border:4px solid ${BL2}`));
  o.b = abs(r, `left:230px;top:5px;width:620px;height:130px;border-radius:999px;background:${BL};color:#fff;font:900 50px Inter;display:flex;align-items:center;justify-content:center;gap:18px;box-shadow:0 0 60px rgba(80,80,255,.7)`, `${o.text} ${ico('arrow-down', 50)}`);
};
B.cta2.u = (o, t) => {
  appear(o.b, t, o.t0, { y0: 50, s0: .7, ease: E.back });
  o.rings.forEach((g, i) => { const k = ((t - o.t0 + i * .6) % 1.2) / 1.2; g.style.opacity = t > o.t0 + .3 ? (1 - k) * .8 : 0; g.style.transform = `scale(${1 + k * .35})` });
};
