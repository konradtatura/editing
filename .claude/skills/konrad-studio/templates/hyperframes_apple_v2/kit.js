// lfpdo · Premium v3 kit. Deterministic helpers shared by every scene (see base.css for the style rules).
(function () {
  const K = {};
  K.tl = gsap.timeline({ paused: true });
  K.done = function () { K.tl.eventCallback("onUpdate", K.update); K.update(); window.__timelines = window.__timelines || {}; window.__timelines["main"] = K.tl; };
  K.rng = function (a) { return function () { a |= 0; a = (a + 0x6d2b79f5) | 0; let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; };
  K.pl = function (v) { return Math.round(v).toLocaleString("pl-PL"); };
  K.$ = function (s) { return document.querySelector(s); };

  // wrap every word of the matched elements in a mask so it can rise into place
  K.split = function (sel) {
    document.querySelectorAll(sel).forEach(function (el) {
      if (el.dataset.split) return; el.dataset.split = "1";
      const words = el.textContent.trim().split(/\s+/);
      el.innerHTML = words.map(function (w) { return '<span class="w"><span class="wi">' + w + "</span></span>"; }).join(" ");
    });
  };
  // words rise out of their mask (one entrance language for all type)
  K.rise = function (sel, t, o) {
    o = o || {}; K.split(sel);
    K.tl.fromTo(sel + " .wi", { yPercent: o.from || 112, opacity: 0 }, { yPercent: 0, opacity: 1, duration: o.dur || 0.75, ease: o.ease || "expo.out",
      stagger: o.stagger === undefined ? 0.055 : o.stagger, immediateRender: true }, t);
  };
  // words drop out (exit) — only used where one line replaces another inside the same shot
  K.sink = function (sel, t, o) {
    o = o || {}; K.split(sel);
    K.tl.to(sel + " .wi", { yPercent: -135, opacity: 0, duration: o.dur || 0.45, ease: o.ease || "power3.in", stagger: o.stagger || 0.03 }, t);
  };
  // plain block entrance: lift + fade (cards, rows)
  K.lift = function (sel, t, o) {
    o = o || {};
    K.tl.fromTo(sel, { opacity: 0, y: o.y === undefined ? 36 : o.y, scale: o.s || 1 },
      { opacity: 1, y: 0, scale: 1, duration: o.dur || 0.7, ease: o.ease || "power3.out", stagger: o.stagger || 0, immediateRender: true }, t);
  };
  K.fadeOut = function (sel, t, o) { o = o || {}; K.tl.to(sel, { opacity: 0, y: o.y || 0, duration: o.dur || 0.35, ease: "power2.in" }, t); };
  // rolling numbers: every counter is recomputed from the playhead each frame (seek-safe, several segments per element)
  K.counters = []; K.hooks = [];
  K.count = function (sel, from, to, t, dur, fmt, ease) {
    const el = K.$(sel); fmt = fmt || K.pl;
    let c = K.counters.find(function (c) { return c.el === el; });
    if (!c) { c = { el: el, segs: [] }; K.counters.push(c); el.textContent = fmt(from); }
    c.segs.push({ from: from, to: to, t: t, dur: dur, fmt: fmt, e: gsap.parseEase(ease || "power3.out") });
  };
  // per-frame hook (canvas drawing etc.), called with the playhead time after all tweens rendered
  K.frame = function (fn) { K.hooks.push(fn); };
  K.update = function () {
    const T = K.tl.time();
    K.counters.forEach(function (c) {
      let v = c.segs[0].from, f = c.segs[0].fmt;
      c.segs.forEach(function (g) { if (T >= g.t) { v = g.from + (g.to - g.from) * g.e(Math.min(1, (T - g.t) / g.dur)); f = g.fmt; } });
      const s = f(v); if (c.el.textContent !== s) c.el.textContent = s;
    });
    K.hooks.forEach(function (h) { h(T); });
  };
  // weight play: a light word turns heavy (two stacked copies, cross-swap with a small kick)
  K.weight = function (sel, t, o) {
    o = o || {};
    const el = K.$(sel), lo = el.querySelector(".lo"), hi = el.querySelector(".hi");
    K.tl.fromTo(hi, { opacity: 0 }, { opacity: 1, duration: 0.1, ease: "none", immediateRender: true }, t);
    K.tl.to(lo, { opacity: 0, duration: 0.1, ease: "none" }, t);
    K.tl.fromTo(el, { scale: 1 }, { scale: o.kick || 1.06, duration: 0.16, ease: "power2.out", yoyo: true, repeat: 1, immediateRender: false }, t);
  };
  // slow continuous camera drift so no frame is ever frozen
  K.push = function (dur, s1, x1, y1) {
    K.tl.fromTo("#cam", { scale: 1, x: 0, y: 0 }, { scale: s1 || 1.045, x: x1 || 0, y: y1 || 0, duration: dur, ease: "sine.inOut" }, 0);
  };
  // overlay card: in from the left wall, out at the end
  K.card = function (dur, o) {
    o = o || {};
    K.tl.fromTo(".ovc", { opacity: 0, y: 24, scale: 0.97 }, { opacity: 1, y: 0, scale: 1, duration: 0.55, ease: "expo.out", immediateRender: true }, o.t || 0.04);
    K.tl.to(".ovc", { opacity: 0, y: 10, scale: 0.98, duration: 0.28, ease: "power2.in" }, dur - 0.3);
  };
  // strike through a word/line (call after K.rise on the same element — split rewrites innerHTML)
  K.strike = function (sel, t, o) {
    o = o || {}; const el = K.$(sel); el.style.position = "relative"; if (getComputedStyle(el).display === "inline") el.style.display = "inline-block";
    const s = document.createElement("span"); s.className = "st"; if (o.color) s.style.background = o.color; el.appendChild(s);
    K.tl.fromTo(s, { scaleX: 0 }, { scaleX: 1, duration: 0.4, ease: "power3.inOut", immediateRender: true }, t);
    if (o.dim !== false) K.tl.to(el, { color: "#7d879b", duration: 0.3, ease: "power1.out" }, t + 0.12);
  };
  // check box markup + ticks
  K.CHK = '<div class="chk"><div class="on"><svg viewBox="0 0 28 26"><path d="M3 13 L11 21 L25 4" fill="none" stroke="#fff" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round"/></svg></div>' +
          '<div class="off"><svg viewBox="0 0 24 24"><path d="M4 4 L20 20 M20 4 L4 20" fill="none" stroke="#fff" stroke-width="4.5" stroke-linecap="round"/></svg></div></div>';
  K.tick = function (sel, t, on) {
    const a = K.$(sel + " .on"), b = K.$(sel + " .off");
    if (!b) { K.tl.fromTo(a, { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.25, ease: "power3.out", immediateRender: false }, t); return; }
    if (on === false) { K.tl.to(a, { opacity: 0, duration: 0.15 }, t); K.tl.fromTo(b, { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2.5)", immediateRender: false }, t); }
    else { K.tl.to(b, { opacity: 0, duration: 0.15 }, t); K.tl.fromTo(a, { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2.5)", immediateRender: false }, t); }
  };
  // whip transition for full-screen scenes: zoom + blur in, quick zoom + blur out (paired with whooshes in the SFX layer)
  K.whip = function (dur) {   // Apple v2: soft settle in, no blur-out (hard cut back to the face)
    K.tl.fromTo("#root", { scale: 1.045, filter: "blur(6px)" }, { scale: 1, filter: "blur(0px)", duration: 0.3, ease: "expo.out", immediateRender: true }, 0);
  };
  // iOS toggle on/off: <div class="tog"><div class="on"></div><div class="k"></div></div>
  K.toggle = function (sel, t, on) {
    on = on !== false;
    K.tl.to(sel + " .on", { opacity: on ? 1 : 0, duration: 0.22, ease: "power2.out" }, t);
    K.tl.to(sel + " .k", { x: on ? 34 : 0, duration: 0.28, ease: "power3.out" }, t);
  };
  K.TOG = function (id, on) { return '<div class="tog" id="' + id + '"><div class="on"' + (on ? ' style="opacity:1"' : '') + '></div><div class="k"' + (on ? ' style="transform:translateX(34px)"' : '') + '></div></div>'; };
  // finger tap ripple on an element with class .tap placed at the tap point
  K.tap = function (sel, t) {
    K.tl.fromTo(sel, { opacity: 0.45, scale: 0.5 }, { opacity: 0, scale: 1.5, duration: 0.45, ease: "power2.out", immediateRender: false }, t);
  };
  // highlighter sweep behind a word (.mk)
  K.mark = function (sel, t) { K.tl.fromTo(sel, { "--m": 0 }, { "--m": 1, duration: 0.4, ease: "power3.out", immediateRender: true }, t); };
  // UI cursor glides from (x0,y0) to (x1,y1), presses at tc (cursor element must exist: <svg class="cur" id=...>)
  K.click = function (sel, x0, y0, x1, y1, t0, tc, target) {
    K.tl.fromTo(sel, { x: x0, y: y0, opacity: 0 }, { x: x1, y: y1, opacity: 1, duration: tc - t0, ease: "power3.inOut", immediateRender: true }, t0);
    K.tl.to(sel, { scale: 0.85, duration: 0.07, yoyo: true, repeat: 1, ease: "power2.in" }, tc);
    if (target) K.tl.to(target, { scale: 0.95, duration: 0.08, yoyo: true, repeat: 1, ease: "power2.in" }, tc);
  };
  K.CUR = '<path d="M4 3 L4 48 L15 37 L23 56 L31 52 L23 34 L39 34 Z" fill="#f4f6fa" stroke="#0a0d16" stroke-width="3" stroke-linejoin="round"/>';

  // typing / erasing: K.type("#q", t, "", "biznes AI", 0.6) — text goes from string a to string b in dur (seek-safe)
  K.typers = [];
  K.type = function (sel, t, a, b, dur) {
    const el = K.$(sel);
    let c = K.typers.find(function (c) { return c.el === el; });
    if (!c) { c = { el: el, segs: [], first: a }; K.typers.push(c); el.textContent = a; }
    c.segs.push({ t: t, a: a, b: b, dur: dur });
  };
  K.hooks.push(function (T) {
    K.typers.forEach(function (c) {
      let s = c.first;
      c.segs.forEach(function (g) {
        if (T < g.t) return;
        const p = Math.min(1, (T - g.t) / g.dur);
        if (g.b.startsWith(g.a)) s = g.b.slice(0, g.a.length + Math.round((g.b.length - g.a.length) * p));
        else s = g.a.slice(0, g.a.length - Math.round((g.a.length - g.b.length) * p));
      });
      if (c.el.textContent !== s) c.el.textContent = s;
    });
  });
  // draw an SVG stroke on (path/line/polyline/circle): dash from its full length to 0
  K.draw = function (sel, t, dur, ease) {
    document.querySelectorAll(sel).forEach(function (el) {
      const L = el.getTotalLength(); el.style.strokeDasharray = L + " " + L; el.style.strokeDashoffset = L;
      K.tl.fromTo(el, { strokeDashoffset: L }, { strokeDashoffset: 0, duration: dur || 0.8, ease: ease || "power2.inOut", immediateRender: true }, t);
    });
  };
  // iOS "wrong PIN" shake
  K.shake = function (sel, t, amp) {
    K.tl.fromTo(sel, { x: 0 }, { keyframes: [{ x: amp || 18 }, { x: -(amp || 18) }, { x: (amp || 18) * 0.6 }, { x: -(amp || 18) * 0.4 }, { x: 0 }],
      duration: 0.42, ease: "none", immediateRender: false }, t);
  };
  // stamp: element lands from big to normal (sticker / pin)
  K.stamp = function (sel, t, o) {
    o = o || {};
    K.tl.fromTo(sel, { opacity: 0, scale: o.from || 1.35, rotation: o.r0 || 0 }, { opacity: 1, scale: 1, rotation: o.r1 || 0, duration: o.dur || 0.32,
      ease: "power4.in", immediateRender: true }, t);
  };
  window.K = K;
})();
