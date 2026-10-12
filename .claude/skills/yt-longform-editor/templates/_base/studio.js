/* Studio Clean — shared motion vocabulary. Every template calls S.init(DATA) first.
   All motion is built on one paused GSAP timeline (HyperFrames contract). */
(function () {
  const S = {};
  S.EASE_IN = "expo.out";        // fast start, soft landing (Apple / Iman)
  S.EASE_OUT = "power2.in";
  S.EASE_MOVE = "expo.inOut";    // layout moves (speaker shrink, frame travel)
  S.T_IN = 0.6;                  // entry
  S.T_OUT = 0.32;                // exit is always faster than entry
  S.WORD_STAGGER = 0.07;         // word-by-word reveal
  S.ITEM_STAGGER = 0.14;         // list items / cards

  S.init = function (data) {
    const f = (data && data.film) || {};
    const root = document.documentElement;
    if (f.surface === "light") root.classList.add("surface-light");
    if (f.overlayInk === "dark") root.classList.add("overlay-dark-ink");
    if (f.accent) {
      root.style.setProperty("--accent", f.accent);
      root.style.setProperty("--accent-soft", S.alpha(f.accent, 0.16));
    }
    return f;
  };

  S.alpha = function (hex, a) {
    const h = hex.replace("#", "");
    const n = parseInt(h.length === 3 ? h.split("").map((c) => c + c).join("") : h, 16);
    return `rgba(${(n >> 16) & 255}, ${(n >> 8) & 255}, ${n & 255}, ${a})`;
  };

  /* Split text into word spans. accent: array of words (case-insensitive, punctuation ignored)
     mode "color" → accent colour, "weight" → light text with the accent word in SemiBold (Iman light→bold). */
  S.words = function (el, text, accent, mode) {
    const acc = (accent || []).map((w) => S.norm(w));
    el.innerHTML = "";
    const parts = String(text).split(/\s+/).filter(Boolean);
    parts.forEach((p, i) => {
      const s = document.createElement("span");
      s.className = "w";
      s.textContent = p + (i < parts.length - 1 ? " " : "");
      if (acc.includes(S.norm(p))) s.classList.add(mode === "weight" ? "acc-weight" : "accent");
      el.appendChild(s);
    });
    return el.querySelectorAll(".w");
  };
  S.norm = (w) => String(w).toLowerCase().replace(/[^\p{L}\p{N}%$€+.-]/gu, "");

  /* Standard reveal of a word set: rise + fade + de-blur */
  S.inWords = function (tl, targets, t, opts) {
    const o = Object.assign({ y: 16, blur: 8, stagger: S.WORD_STAGGER, dur: 0.55 }, opts || {});
    tl.fromTo(targets, { y: o.y, opacity: 0, filter: `blur(${o.blur}px)` },
      { y: 0, opacity: 1, filter: "blur(0px)", duration: o.dur, ease: S.EASE_IN, stagger: o.stagger }, t);
  };

  /* Card / block entry: scale 0.94 → 1, rise, fade, de-blur */
  S.inBlock = function (tl, targets, t, opts) {
    const o = Object.assign({ y: 26, scale: 0.94, blur: 10, stagger: S.ITEM_STAGGER, dur: 0.7 }, opts || {});
    tl.fromTo(targets, { y: o.y, scale: o.scale, opacity: 0, filter: `blur(${o.blur}px)` },
      { y: 0, scale: 1, opacity: 1, filter: "blur(0px)", duration: o.dur, ease: S.EASE_IN, stagger: o.stagger }, t);
  };

  /* Exit: quick fade + small lift + slight blur */
  S.out = function (tl, targets, t, opts) {
    const o = Object.assign({ y: -10, dur: S.T_OUT, stagger: 0 }, opts || {});
    tl.to(targets, { y: o.y, opacity: 0, filter: "blur(6px)", duration: o.dur, ease: S.EASE_OUT, stagger: o.stagger }, t);
  };

  /* Rolling number. el gets text like prefix + formatted + suffix. */
  S.roll = function (tl, el, to, t, opts) {
    const o = Object.assign({ from: 0, dur: 1.2, decimals: 0, prefix: "", suffix: "", locale: "pl-PL" }, opts || {});
    const obj = { v: o.from };
    const fmt = (v) => o.prefix + Number(v).toLocaleString(o.locale, { minimumFractionDigits: o.decimals, maximumFractionDigits: o.decimals }) + o.suffix;
    el.textContent = fmt(o.from);
    tl.to(obj, { v: to, duration: o.dur, ease: "power3.out", onUpdate: () => { el.textContent = fmt(obj.v); } }, t);
    tl.call(() => { el.textContent = fmt(to); }, null, t + o.dur);
  };

  /* Draw an SVG stroke (underline, ring, arrow) */
  S.draw = function (tl, path, t, dur) {
    const len = path.getTotalLength ? path.getTotalLength() : 1000;
    path.style.strokeDasharray = len;
    tl.fromTo(path, { strokeDashoffset: len }, { strokeDashoffset: 0, duration: dur || 0.45, ease: "power1.inOut" }, t);
  };

  /* Seeded PRNG for any jitter (determinism rule) */
  S.rng = function (seed) { let s = seed >>> 0 || 1; return () => ((s = (s * 1664525 + 1013904223) >>> 0) / 4294967296); };

  /* Minimal line icons (SF Symbols feel, 24px grid, stroke inherits currentColor) */
  const ICONS = {
    check: '<path d="M5 12.5l4.2 4.2L19 7"/>',
    x: '<path d="M6 6l12 12M18 6L6 18"/>',
    up: '<path d="M12 19V5M5.5 11.5L12 5l6.5 6.5"/>',
    down: '<path d="M12 5v14M5.5 12.5L12 19l6.5-6.5"/>',
    arrow: '<path d="M5 12h14M13 6l6 6-6 6"/>',
    clock: '<circle cx="12" cy="12" r="8.5"/><path d="M12 7.5V12l3 2"/>',
    money: '<rect x="3" y="6.5" width="18" height="11" rx="2.5"/><circle cx="12" cy="12" r="2.6"/>',
    user: '<circle cx="12" cy="8.5" r="3.6"/><path d="M4.8 19.5c1.2-3.4 4-5 7.2-5s6 1.6 7.2 5"/>',
    bolt: '<path d="M13 3L5.5 13.5H12L11 21l7.5-10.5H12L13 3z"/>',
    chart: '<path d="M4 20h16"/><path d="M7 16v-4M12 16V8M17 16v-7"/>',
    cart: '<path d="M3.5 4.5h2.2l2.2 10.5h9.6l2-7.5H6.6"/><circle cx="9.5" cy="19" r="1.3"/><circle cx="17" cy="19" r="1.3"/>',
    mail: '<rect x="3.5" y="5.5" width="17" height="13" rx="2.5"/><path d="M4.5 7l7.5 6 7.5-6"/>',
    globe: '<circle cx="12" cy="12" r="8.5"/><path d="M3.5 12h17M12 3.5c2.6 2.6 2.6 14.4 0 17M12 3.5c-2.6 2.6-2.6 14.4 0 17"/>',
    lock: '<rect x="5" y="10.5" width="14" height="9.5" rx="2.5"/><path d="M8.5 10.5V8a3.5 3.5 0 017 0v2.5"/>',
    sparkle: '<path d="M12 3.5l1.9 5.6 5.6 1.9-5.6 1.9L12 18.5l-1.9-5.6L4.5 11l5.6-1.9L12 3.5z"/>',
    file: '<path d="M7 3.5h6.5L18 8v12.5H7z"/><path d="M13 3.5V8.5h5"/>',
    book: '<path d="M5 5.5A2 2 0 017 3.5h11v14H7a2 2 0 00-2 2zM5 19.5v-14"/>',
    play: '<circle cx="12" cy="12" r="8.5"/><path d="M10.2 8.8l5 3.2-5 3.2z"/>',
    star: '<path d="M12 4l2.5 5.2 5.7.8-4.1 4 1 5.6L12 17l-5.1 2.6 1-5.6-4.1-4 5.7-.8z"/>',
    target: '<circle cx="12" cy="12" r="8.5"/><circle cx="12" cy="12" r="4.5"/><circle cx="12" cy="12" r="1"/>',
    rocket: '<path d="M12 3.5c3 2 4.5 5.5 4 9.5l-2 2h-4l-2-2c-.5-4 1-7.5 4-9.5z"/><path d="M10 15l-2.5 4M14 15l2.5 4"/><circle cx="12" cy="9" r="1.4"/>',
    brain: '<path d="M9 4.5a3 3 0 00-3 3 3 3 0 00-1.5 5.3A3 3 0 008 18.5h1V4.5zM15 4.5a3 3 0 013 3 3 3 0 011.5 5.3 3 3 0 01-3.5 5.7h-1V4.5z"/>',
    chat: '<path d="M5 5.5h14v10H10l-4 3.5v-3.5H5z"/>',
    code: '<path d="M9 7l-5 5 5 5M15 7l5 5-5 5"/>',
    calendar: '<rect x="4" y="5.5" width="16" height="14" rx="2.5"/><path d="M4 10h16M8.5 3.5v4M15.5 3.5v4"/>',
    gift: '<rect x="4" y="9" width="16" height="11" rx="1.5"/><path d="M3 9h18M12 9v11M12 9c-1-3-5-4-5-1.5S12 9 12 9zm0 0c1-3 5-4 5-1.5S12 9 12 9z"/>',
  };
  S.icon = function (name, size) {
    const body = ICONS[name] || ICONS.sparkle;
    const s = size || 32;
    return `<svg width="${s}" height="${s}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">${body}</svg>`;
  };

  S.register = function (id, tl) { window.__timelines = window.__timelines || {}; window.__timelines[id] = tl; };

  window.S = S;
})();
