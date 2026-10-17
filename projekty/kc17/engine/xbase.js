/* kc17 "X swipefile" engine base: helpers + init/seek. Each page adds a caption renderer (window.CAPS) and builders (B.*).
   Spec: {dur, capY, caps:[{t0,t1,words:[{d,t,h}]}], items:[{type,t0,t1,hideCaps?,...}], hide:[[a,b]]}. */
const W = 1080, H = 1920; const ICONS = window.ICONS || {};
const cl = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x)), lerp = (a, b, p) => a + (b - a) * p, P = (t, t0, d) => cl((t - t0) / d);
const E = { out: t => 1 - Math.pow(1 - t, 3), out5: t => 1 - Math.pow(1 - t, 5), inout: t => t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2,
  back: t => { const c1 = 1.5, c3 = c1 + 1; return 1 + c3 * Math.pow(t - 1, 3) + c1 * Math.pow(t - 1, 2) } };
const svg = n => ICONS[n] || '';
function el(tag, cls, parent, html) { const e = document.createElement(tag); if (cls) e.className = cls; if (html != null) e.innerHTML = html; (parent || document.getElementById('stage')).appendChild(e); return e }
function abs(parent, css, html) { const d = el('div', '', parent, html || ''); d.style.cssText = 'position:absolute;' + css; return d }
function ico(name, px, col, sw) { return `<span style="display:inline-flex;width:${px}px;height:${px}px;color:${col || 'currentColor'}">${svg(name).replace('<svg', `<svg style="width:100%;height:100%;stroke-width:${sw || 2.4}"`)}</span>` }
function icoC(name, px, col, sw) { return `<span style="position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);display:block;width:${px}px;height:${px}px;color:${col || 'currentColor'}">${svg(name).replace('<svg', `<svg style="display:block;width:100%;height:100%;stroke-width:${sw || 2.4}"`)}</span>` }
/* pop-in: scale s0 -> overshoot -> 1 with blur (the swipefile's universal entrance) */
function pop(e, t, t0, o = {}) { const d = o.d || .3, p = P(t, t0, d), pe = (o.ease || E.back)(p);
  e.style.opacity = E.out(P(t, t0, d * .5)); e.style.filter = p < 1 ? `blur(${(1 - E.out(p)) * (o.b0 ?? 10)}px)` : 'none';
  e.style.transform = `translate(${(1 - pe) * (o.x0 || 0)}px,${(1 - pe) * (o.y0 ?? 0)}px) scale(${lerp(o.s0 ?? .6, 1, pe)}) ${o.rot ? `rotate(${o.rot}deg)` : ''}`; return p }
function out(e, t, t1, d = .16) { const k = P(t, t1 - d, d); if (k > 0) { e.style.opacity = Math.min(+e.style.opacity || 1, 1 - k); } }
function typed(t, t0, s, cps = 24) { return s.slice(0, Math.max(0, Math.min(s.length, Math.floor((t - t0) * cps)))) }
const B = {};
let SPEC = null;
window.init = spec => { SPEC = spec; spec.items.forEach(o => B[o.type](o)); const c = el('div', ''); c.id = 'caps'; return true };
window.seek = t => {
  SPEC.items.forEach(o => { const on = t >= o.t0 - 1e-3 && t < o.t1; if (o.e) o.e.style.display = on ? '' : 'none'; if (on) B[o.type].u(o, t) });
  const hide = SPEC.items.some(o => o.hideCaps && t >= o.t0 && t < o.t1) || (SPEC.hide || []).some(([a, b]) => t >= a && t < b);
  window.CAPS(SPEC, t, hide); return true };
