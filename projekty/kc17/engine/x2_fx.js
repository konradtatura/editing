/* x2 = skill h2v4 — vibe of the swipefile's "Amber" (CAPS word-by-word, blue accent, red negatives, glossy blue badges, outlined glass
   pills, black inserts with icon+cursor and kinetic motion-trail words) + "Arham" (cream cards stacking, focus brackets, search-bar CTA)
   + "Yoo" (white flash transition). Natural footage. */
const BLU = '#2F80FF', BLU2 = '#5CA8FF', RED = '#FF3B3B', DK = '#0A0C12';
const SH2 = 'text-shadow:0 3px 4px rgba(0,0,0,.65),0 6px 22px rgba(0,0,0,.6)';
const glossy = (s, c1 = BLU2, c2 = BLU) => `width:${s}px;height:${s}px;border-radius:50%;display:flex;align-items:center;justify-content:center;color:#fff;
  background:radial-gradient(circle at 35% 28%,#fff 0%,${c1} 22%,${c2} 62%,#0B3FB0 100%);box-shadow:inset 0 -10px 22px rgba(0,20,80,.45),0 18px 40px rgba(0,30,100,.5),0 0 40px rgba(47,128,255,.45)`;

/* ---- captions: CAPS Poppins 800, words pop in one by one, 2 lines max; h=1 blue, h=2 red ---- */
let ck = -1;
window.CAPS = (spec, t, hide) => {
  const box = document.getElementById('caps'); let bi = -1;
  for (let i = 0; i < spec.caps.length; i++) { if (t >= spec.caps[i].t0 - .02) bi = i; else break }
  const b = spec.caps[bi]; if (hide || !b || t >= b.t1) { box.style.display = 'none'; return } box.style.display = '';   // display, not visibility: word spans set their own visibility
  if (ck !== bi) { ck = bi; box.innerHTML = ''; b.words.forEach(w => { const s = el('span', 'w' + (w.h ? ' h' + w.h : ''), box, w.d.replace(/[,.]$/, '')); s.dataset.t = w.t }) }
  box.style.top = (spec.capY * H) + 'px';
  box.querySelectorAll('.w').forEach(s => { const on = t >= +s.dataset.t - .04; s.style.visibility = on ? 'visible' : 'hidden'; if (on) pop(s, t, +s.dataset.t - .04, { s0: .5, y0: 18, d: .2, b0: 6 }) });
};

/* 1. glossy numbered badges: three professions; on "bez sensu" they shake red */
B.badges = o => { const r = abs(null, `left:0;top:${o.y}px;width:1080px;height:360px`); o.e = r;
  o.items.forEach((it, i) => { const x = 230 + i * 310;
    it.e = abs(r, `left:${x - 85}px;top:0;${glossy(170)};font:800 86px Poppins`, `${i + 1}`);
    it.l = abs(r, `left:${x - 160}px;width:320px;top:190px;text-align:center;font:800 40px Poppins;color:#fff;text-transform:uppercase;${SH2}`, it.text) }) };
B.badges.u = (o, t) => o.items.forEach((it, i) => { const on = t >= it.t; it.e.style.display = it.l.style.display = on ? '' : 'none'; if (!on) return;
  pop(it.e, t, it.t, { s0: .2, y0: 80, d: .35 }); pop(it.l, t, it.t + .06, { s0: .7 });
  const bad = t >= o.badT, sh = bad && t < o.badT + .5 ? Math.sin((t - o.badT) * 60) * 10 * (1 - (t - o.badT) / .5) : 0;
  it.e.style.transform += ` translateX(${sh}px)`; if (bad) it.e.style.background = `radial-gradient(circle at 35% 28%,#fff 0%,#FF8A8A 22%,${RED} 62%,#A00010 100%)` });

/* 2. black full-screen insert: kinetic word with motion trail */
B.kinetic = o => { const p = abs(null, `inset:0;background:radial-gradient(circle at 50% 45%,#141824,#05060A 70%)`); o.e = p;
  o.ghost = [0.5, 0.3, 0.15].map(a => abs(p, `left:0;right:0;top:${o.y}px;text-align:center;font:800 ${o.size}px Poppins;color:#fff;opacity:${a};filter:blur(6px);text-transform:uppercase;line-height:1`, o.text));
  o.main = abs(p, `left:0;right:0;top:${o.y}px;text-align:center;font:800 ${o.size}px Poppins;color:#fff;text-transform:uppercase;line-height:1;letter-spacing:-.02em`, o.text);
  if (o.sub) o.s = abs(p, `left:0;right:0;top:${o.y + o.size * (o.text.split('<br>').length) + 40}px;text-align:center;font:500 40px Poppins;color:#8C93A6`, o.sub) };
B.kinetic.u = (o, t) => { const k = E.out5(P(t, o.t0, .45)); const x = (1 - k) * 900;
  o.main.style.transform = `translateX(${x}px)`; o.main.style.filter = k < 1 ? `blur(${(1 - k) * 10}px)` : 'none';
  o.ghost.forEach((g, i) => { g.style.transform = `translateX(${x + (i + 1) * 70 * (1 - k * .6)}px)`; g.style.opacity = (1 - k) * [.5, .3, .15][i] + .04 });
  if (o.s) pop(o.s, t, o.t0 + .35, { s0: .9, y0: 14 }); const dr = (t - o.t0) * 18; o.main.style.transform += ` translateX(${-dr}px)` };

/* 3. cream cards stacking: kurs, kurs, kolejny kurs, noce */
B.courses = o => { const r = abs(null, `left:0;top:${o.y}px;width:1080px;height:480px`); o.e = r;
  o.items.forEach((it, i) => it.e = abs(r, `left:${170 + i * 60}px;top:${i * 34}px;width:560px;height:150px;border-radius:26px;background:linear-gradient(160deg,#FFF8F0,#F6E7D7);
     box-shadow:0 22px 50px rgba(60,30,0,.35),0 0 0 1.5px rgba(255,255,255,.8);display:flex;align-items:center;gap:26px;padding:0 34px;font:700 40px Poppins;color:#3A2A1A`,
    `<span style="font-size:64px">${it.emo}</span><span>${it.text}</span>`));
  o.cnt = abs(r, `left:820px;top:-30px;${glossy(130, '#FF8A8A', RED)};font:800 50px Poppins`, '') };
B.courses.u = (o, t) => { let n = 0; o.items.forEach((it, i) => { const on = t >= it.t; it.e.style.display = on ? '' : 'none'; if (!on) return; n++;
    pop(it.e, t, it.t, { s0: .8, y0: -160, ease: E.out5, d: .3, rot: (i % 2 ? 3 : -3) }) });
  o.cnt.style.display = n > 1 ? '' : 'none'; o.cnt.textContent = '+' + n; const lt = o.items[n - 1] ? o.items[n - 1].t : 0; if (n > 1) pop(o.cnt, t, lt, { s0: .3, d: .25 }) };

/* 4. black insert: icons get clicked green by a cursor, the last slot stays an open question */
B.clicker = o => { const p = abs(null, `inset:0;background:radial-gradient(circle at 50% 45%,#141824,#05060A 75%)`); o.e = p;
  o.items.forEach((it, i) => { const y = 520 + i * 330;
    it.e = abs(p, `left:420px;top:${y}px;width:240px;height:240px;border-radius:56px;background:#fff;display:flex;align-items:center;justify-content:center;color:${DK};box-shadow:0 20px 50px rgba(0,0,0,.6)`, it.icon ? ico(it.icon, 120, null, 2.2) : `<span style="font:800 140px Poppins;color:${RED}">?</span>`);
    it.l = abs(p, `left:700px;top:${y + 90}px;font:800 44px Poppins;color:#fff;text-transform:uppercase`, it.text) });
  o.cur = abs(p, 'left:0;top:0;width:90px;height:90px', `<svg viewBox="0 0 24 24" width="90" height="90"><path d="M4 2l15 9-7 1.5L9 20z" fill="#fff" stroke="#000" stroke-width="1.2"/></svg>`) };
B.clicker.u = (o, t) => { let cx = 980, cy = 1700;
  o.items.forEach((it, i) => { const on = t >= it.t; it.e.style.display = it.l.style.display = on ? '' : 'none'; if (!on) return; pop(it.e, t, it.t, { s0: .4 }); pop(it.l, t, it.t + .1, { s0: .8, x0: 40 });
    if (it.icon) { const ct = it.t + .45; const g = t >= ct; it.e.style.background = g ? '#2BD96B' : '#fff'; it.e.style.color = g ? '#fff' : DK;
      if (t >= it.t) { const m = E.inout(P(t, it.t, .45)); cx = lerp(cx, 600, m); cy = lerp(cy, 520 + i * 330 + 170, m); } }
    else { const pu = 1 + .06 * Math.sin((t - it.t) * 9); it.e.style.transform += ` scale(${pu})`; it.e.style.boxShadow = `0 0 ${40 + 30 * Math.sin((t - it.t) * 9)}px rgba(255,59,59,.7)` } });
  o.cur.style.transform = `translate(${cx}px,${cy}px)` };

/* 5. stacked red ZNOWU slams with motion trails */
B.znowu = o => { const r = abs(null, `left:0;top:${o.y}px;width:1080px;height:420px`); o.e = r;
  o.items.forEach((it, i) => it.e = abs(r, `left:0;right:0;top:${i * 128}px;text-align:center;font:800 92px Poppins;text-transform:uppercase;letter-spacing:-.02em;color:#fff;${SH2}`,
    `<span style="color:${RED}">znowu</span> ${it.text}`)) };
B.znowu.u = (o, t) => o.items.forEach((it, i) => { const on = t >= it.t; it.e.style.display = on ? '' : 'none'; if (!on) return;
  const k = E.out5(P(t, it.t, .3)); it.e.style.transform = `translateX(${(i % 2 ? -1 : 1) * (1 - k) * 700}px) scale(${lerp(1.3, 1, k)})`; it.e.style.filter = k < 1 ? `blur(${(1 - k) * 12}px)` : 'none'; it.e.style.opacity = P(t, it.t, .1) });

/* 6. white flash (transition) */
B.flash = o => { o.e = abs(null, 'inset:0;background:#fff') };
B.flash.u = (o, t) => { o.e.style.opacity = 1 - E.out(P(t, o.t0, o.t1 - o.t0)) };

/* 7. focus brackets around the face */
B.brackets = o => { const r = abs(null, `left:${o.x}px;top:${o.y}px;width:${o.w}px;height:${o.h}px`); o.e = r;
  o.c = [['left:0;top:0', 'border-left', 'border-top'], ['right:0;top:0', 'border-right', 'border-top'], ['left:0;bottom:0', 'border-left', 'border-bottom'], ['right:0;bottom:0', 'border-right', 'border-bottom']]
    .map(([p, a, b]) => abs(r, `${p};width:110px;height:110px;${a}:8px solid #fff;${b}:8px solid #fff;filter:drop-shadow(0 0 10px rgba(0,0,0,.5))`)) };
B.brackets.u = (o, t) => { const k = E.out5(P(t, o.t0, .35)); o.c.forEach((c, i) => { const dx = (i % 2 ? 1 : -1) * (1 - k) * 120, dy = (i < 2 ? -1 : 1) * (1 - k) * 120; c.style.transform = `translate(${dx}px,${dy}px)`; c.style.opacity = k }) };

/* 8. big glossy AI orb with pulse rings + label */
B.orb = o => { const r = abs(null, `left:0;top:${o.y}px;width:1080px;height:460px`); o.e = r;
  o.rings = [0, 1, 2].map(() => abs(r, `left:540px;top:150px;width:300px;height:300px;margin:-150px 0 0 -150px;border-radius:50%;border:4px solid ${BLU2}`));
  o.orb = abs(r, `left:390px;top:0;${glossy(300)};font:800 130px Poppins`, 'AI');
  o.l = abs(r, `left:150px;width:780px;top:330px;text-align:center;padding:18px;border-radius:999px;border:3px solid rgba(92,168,255,.9);background:rgba(10,20,40,.55);font:700 38px Poppins;color:#fff`, o.label) };
B.orb.u = (o, t) => { pop(o.orb, t, o.t0, { s0: .2, d: .45 }); o.orb.style.transform += ` translateY(${Math.sin((t - o.t0) * 2.4) * 10}px)`;
  o.rings.forEach((g, i) => { const k = ((t - o.t0 + i * .5) % 1.5) / 1.5; g.style.opacity = t > o.t0 + .3 ? (1 - k) * .7 : 0; g.style.transform = `scale(${1 + k * 1.1})` });
  o.l.style.display = t >= o.lT ? '' : 'none'; if (t >= o.lT) pop(o.l, t, o.lT, { s0: .8, y0: 30 }) };

/* 9. outlined glass pills that flip from "nie umiesz X" (red) to "AI ✓" (blue) */
B.flips = o => { const r = abs(null, `left:0;top:${o.y}px;width:1080px;height:480px`); o.e = r;
  o.items.forEach((it, i) => it.e = abs(r, `left:110px;width:860px;top:${i * 124}px;height:104px;border-radius:24px;border:3px solid;display:flex;align-items:center;justify-content:center;gap:16px;font:700 38px Poppins;backdrop-filter:blur(8px)`)) };
B.flips.u = (o, t) => o.items.forEach(it => { const on = t >= it.t; it.e.style.display = on ? '' : 'none'; if (!on) return; pop(it.e, t, it.t, { s0: .85, x0: -80, d: .3 });
  const f = t >= it.ft; const k = E.out(P(t, it.ft, .25));
  it.e.innerHTML = f ? `${ico('check', 40, '#fff', 3)} ${it.good}` : `${ico('x', 40, RED, 3)} ${it.bad}`;
  it.e.style.borderColor = f ? BLU2 : 'rgba(255,90,90,.9)'; it.e.style.background = f ? `rgba(47,128,255,${.35 + .45 * k})` : 'rgba(40,10,10,.55)'; it.e.style.color = f ? '#fff' : '#FFC9C9';
  if (f) it.e.style.transform += ` rotateX(${(1 - k) * 90}deg)` });

/* 10. progress bar with stage ticks */
B.loader = o => { const r = abs(null, `left:110px;top:${o.y}px;width:860px;padding:30px 34px;border-radius:28px;border:3px solid rgba(92,168,255,.9);background:rgba(10,16,30,.7)`); o.e = r;
  o.t = abs(r, 'position:relative;font:800 38px Poppins;color:#fff;margin-bottom:22px', o.title);
  const bar = abs(r, 'position:relative;height:30px;border-radius:15px;background:rgba(255,255,255,.15);overflow:hidden'); o.f = abs(bar, `left:0;top:0;bottom:0;background:linear-gradient(90deg,${BLU},${BLU2});box-shadow:0 0 24px ${BLU2}`);
  o.lb = abs(r, 'position:relative;display:flex;justify-content:space-between;margin-top:18px;font:700 30px Poppins;color:#9FB4D8', o.stages.map(s => `<span>${s.text}</span>`).join('')) };
B.loader.u = (o, t) => { pop(o.e, t, o.t0, { s0: .9, y0: 40 }); const n = o.stages.filter(s => t >= s.t).length;
  o.f.style.width = lerp(0, 100, E.out(P(t, o.t0 + .2, o.stages[o.stages.length - 1].t - o.t0))) + '%';
  o.lb.querySelectorAll('span').forEach((s, i) => s.style.color = i < n ? '#fff' : '#6F7F9C') };

/* 11. countdown 48:00:00 in a glossy badge */
B.count = o => { const r = abs(null, `left:0;top:${o.y}px;width:1080px;height:300px`); o.e = r;
  o.b = abs(r, `left:170px;top:0;width:740px;height:220px;border-radius:120px;background:radial-gradient(circle at 30% 20%,#fff 0%,${BLU2} 18%,${BLU} 60%,#0B3FB0);
    box-shadow:inset 0 -12px 26px rgba(0,20,80,.45),0 22px 50px rgba(0,30,100,.5),0 0 50px rgba(47,128,255,.5);display:flex;align-items:center;justify-content:center;gap:20px;color:#fff;font:800 104px Poppins;letter-spacing:.02em`) };
B.count.u = (o, t) => { pop(o.b, t, o.t0, { s0: .4 }); const left = Math.max(0, 48 * 3600 - (t - o.t0) * 3600 * 2.2);
  const hh = Math.floor(left / 3600), mm = Math.floor(left % 3600 / 60), ss = Math.floor(left % 60);
  o.b.innerHTML = `${ico('clock', 84, '#fff', 2.6)}<span>${String(hh).padStart(2, '0')}:${String(mm).padStart(2, '0')}:${String(ss).padStart(2, '0')}</span>` };

/* 12. EKSPERT pill gets struck */
B.strike2 = o => { const r = abs(null, `left:0;top:${o.y}px;width:1080px;height:200px`); o.e = r;
  o.p = abs(r, `left:260px;width:560px;top:0;height:140px;border-radius:30px;background:#fff;color:${DK};font:800 76px Poppins;display:flex;align-items:center;justify-content:center;text-transform:uppercase;box-shadow:0 20px 50px rgba(0,0,0,.45)`, o.text);
  o.l = abs(r, `left:230px;top:62px;height:16px;border-radius:8px;background:${RED};transform-origin:0 50%;transform:rotate(-6deg)`) };
B.strike2.u = (o, t) => { pop(o.p, t, o.t0, { s0: .4 }); o.l.style.width = E.out(P(t, o.sT, .25)) * 620 + 'px' };

/* 13. CTA: search bar types, result drops down, cursor clicks */
B.search = o => { const r = abs(null, `left:110px;top:${o.y}px;width:860px`); o.e = r;
  o.bar = abs(r, `left:0;right:0;top:0;height:120px;border-radius:60px;background:#fff;display:flex;align-items:center;gap:22px;padding:0 36px;font:600 44px Poppins;color:${DK};box-shadow:0 20px 50px rgba(0,0,0,.45)`);
  o.res = abs(r, `left:0;right:0;top:140px;padding:26px 34px;border-radius:30px;background:#fff;display:flex;align-items:center;gap:24px;box-shadow:0 20px 50px rgba(0,0,0,.45)`,
    `<div style="${glossy(84)};font:800 34px Poppins">CA</div><div style="flex:1"><div style="font:800 38px Poppins;color:${DK}">Cyfrowy Autopilot</div><div style="font:500 28px Poppins;color:#6B7280">kliknij poniżej, żeby zacząć</div></div>${ico('arrow-down', 56, BLU, 3)}`);
  o.cur = abs(r, 'left:0;top:0;width:80px;height:80px', `<svg viewBox="0 0 24 24" width="80" height="80"><path d="M4 2l15 9-7 1.5L9 20z" fill="#111" stroke="#fff" stroke-width="1.4"/></svg>`) };
B.search.u = (o, t) => { pop(o.bar, t, o.t0, { s0: .7, y0: 40 }); o.bar.innerHTML = `${ico('search', 52, '#6B7280', 2.6)}<span>${typed(t, o.t0 + .25, o.q, 20)}<span style="color:${BLU}">${(t * 2 | 0) % 2 ? '|' : ''}</span></span>`;
  const rt = o.t0 + .25 + o.q.length / 20 + .1; o.res.style.display = t >= rt ? '' : 'none'; if (t >= rt) pop(o.res, t, rt, { s0: .9, y0: -30, ease: E.out5 });
  const m = E.inout(P(t, rt + .1, .5)); o.cur.style.transform = `translate(${lerp(900, 640, m)}px,${lerp(520, 210, m)}px) scale(${t > rt + .65 && t < rt + .8 ? .85 : 1})` };
