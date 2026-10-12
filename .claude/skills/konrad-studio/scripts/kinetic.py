#!/usr/bin/env python3
"""kinetic.py: Konrad's kinetic-edit engine (16:9). Built for „16–26” (nathanazareth style, 2026-10-05); reusable for any
fast-cut reel/ad/longform segment. Renders every frame in Python (PIL + numpy) and pipes to ffmpeg.

Blocks (see references/biblioteka-efektow.md for when to use what):
  setup(words, display, keep_case)  word list from Scribe [{w,s,e}], display overrides {idx: text}
  Phrase(...)                       kinetic caption: pre / HERO / post, words rise in with motion blur, drift, exit, strike,
                                    redact, flap counter, quotes, chrome; styles video | light | blue | black
  clip_vf / read_clip / still       any source → 1920×1080 frames: band (vertical → 16:9), crop punch-in, push-in, grade
  LIGHT / BLUE / BLACK              card backgrounds (radial white→blue, saturated blue, black)
  FeedWall(n, tiles)                3D tilted wall of B&W thumbnails scrolling (feed / "everyone does this")
  Collage(photos, t0, t1)           polaroids dropping in on the light card (years, proof, journey)
  GuruWall(titles)                  fake YouTube wall of invented thumbnails, no real faces (sceptic / "another guru")
  grid_frame(cells, t, t0, i)       2×2 split built cell by cell with negative flash (travel, PL vs US, many results)
  giant(bg, text, t, t0)            huge translucent word over footage (city, country, one-word statement)
  letterbox(img, t)                 cinematic bars opening at the start
  desk_text(bg, text, p, quad)      word lying on a surface in perspective
  run(shots, phrases, out, ...)     frame loop; --frames-style preview sheet via frames=[t, ...]
"""
import io, json, math, os, random, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

W, H, FPS = 1920, 1080, 30
HN = "/System/Library/Fonts/HelveticaNeue.ttc"
BOLD, MED = 1, 10
BLUE_TXT = (98, 132, 210)
WORDS, DISPLAY, KEEP_CASE = [], {}, set()


def setup(words, display=None, keep_case=None):
    """words: [{"w": text, "s": start, "e": end}] (Scribe, verbatim); display: {index: shown text or "" to hide}."""
    WORDS[:] = words
    DISPLAY.clear(); DISPLAY.update(display or {})
    KEEP_CASE.clear(); KEEP_CASE.update(keep_case or set())
rng = random.Random(7)


def font(size, face=BOLD):
    return ImageFont.truetype(HN, int(size), index=face)


# ------------------------------------------------------------------ backgrounds
def radial_light():
    y, x = np.mgrid[0:H, 0:W].astype(np.float32)
    r = np.sqrt(((x - W * 0.42) / (W * 0.62)) ** 2 + ((y - H * 0.40) / (H * 0.75)) ** 2)
    t = np.clip(r, 0, 1)[..., None] ** 1.6
    c0, c1 = np.array([255, 255, 255], np.float32), np.array([176, 196, 236], np.float32)
    return (c0 * (1 - t) + c1 * t).astype(np.uint8)


def blue_grad():
    y, x = np.mgrid[0:H, 0:W].astype(np.float32)
    t = np.clip((x / W) * 0.35 + (y / H) * 0.65, 0, 1)[..., None]
    c0, c1 = np.array([92, 140, 236], np.float32), np.array([22, 70, 188], np.float32)
    g = c0 * (1 - t) ** 1.4 + c1 * (1 - (1 - t) ** 1.4)
    return g.astype(np.uint8)


LIGHT, BLUE, BLACK = radial_light(), blue_grad(), np.zeros((H, W, 3), np.uint8)


# ------------------------------------------------------------------ clip reading
GRADE = {
    "bw": "hue=s=0,eq=contrast=1.22:brightness=-0.04",
    "cine": "eq=contrast=1.08:saturation=0.9:brightness=-0.02,colorbalance=rs=-0.04:bs=0.05:rh=0.04:bh=-0.04",
    "night": "eq=contrast=1.06:saturation=0.95",
    "none": "null",
}


def clip_vf(band=None, zoom=0.0, dur=1.0, grade="cine", crop=None, speed=1.0):
    f = []
    if speed != 1.0:
        f.append(f"setpts=PTS/{speed}")
    if band is not None:   # vertical source → horizontal 16:9 band, band = vertical position 0..1
        f.append(f"crop=iw:iw*9/16:0:(ih-iw*9/16)*{band}")
    if crop:               # (scale, cx, cy) punch-in on a horizontal source
        s, cx, cy = crop
        f.append(f"crop=iw/{s}:ih/{s}:iw*{cx}-iw/{s}/2:ih*{cy}-ih/{s}/2")
    f.append(f"scale={W}:{H}:flags=lanczos")
    if zoom:   # slow push-in (crop w/h can't change per frame, scale with eval=frame can)
        f.append(f"scale=w='trunc({W}*(1+{zoom}*t/{dur:.3f})/2)*2':h=-2:eval=frame:flags=bicubic")
        f.append(f"crop={W}:{H}:(iw-{W})/2:(ih-{H})/2")
    f.append(GRADE[grade])
    return ",".join(f)


def read_clip(src, ss, n, vf):
    p = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{ss:.3f}", "-i", src, "-vf", f"{vf},fps={FPS},format=rgb24",
                        "-frames:v", str(n), "-f", "rawvideo", "-"], capture_output=True)
    a = np.frombuffer(p.stdout, np.uint8)
    k = len(a) // (W * H * 3)
    fr = [a[i * W * H * 3:(i + 1) * W * H * 3].reshape(H, W, 3) for i in range(k)]
    if not fr:
        raise SystemExit(f"no frames from {src} @ {ss}")
    while len(fr) < n:
        fr.append(fr[-1])
    return fr


def still(src, t, w=None, h=None, band=None, grade="none"):
    vf = []
    if band is not None:
        vf.append(f"crop=iw:iw*16/9:0:(ih-iw*16/9)*{band}" if False else "null")
    vf.append(GRADE[grade])
    if w:
        vf.append(f"scale={w}:{h or -2}")
    r = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.2f}", "-i", src, "-frames:v", "1", "-vf", ",".join(vf),
                        "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True).stdout
    return Image.open(io.BytesIO(r)).convert("RGB")


# ------------------------------------------------------------------ captions
def W_(i):
    return WORDS[i]


def disp(i):
    if i in DISPLAY:
        return DISPLAY[i]
    t = W_(i)["w"]
    return t if t in KEEP_CASE else t.lower()


def ease(p):
    p = min(1.0, max(0.0, p))
    return 1 - (1 - p) ** 3


def smear(im, amount, steps=7):
    """Vertical motion blur: average of copies shifted along y (what Nathan's words have while they move)."""
    if amount < 0.8:
        return im
    a = np.asarray(im).astype(np.float32)
    acc = np.zeros_like(a)
    for k in range(steps):
        dy = int(round((k / (steps - 1) - 0.5) * amount))
        acc += np.roll(a, dy, axis=0)
    return Image.fromarray((acc / steps).astype(np.uint8))


class Phrase:
    """Kinetic caption block: pre (small, above) · hero (big segments) · post (small, below).
    Every word slides up ~20–40 px into place with vertical motion blur + fade over ~0.2 s at the moment it is spoken;
    the hero also scales 106→100 %. The whole block drifts up slowly; if the phrase ends inside a shot it leaves upward
    with blur. Strong two-layer shadow (wide glow + tight drop) so it reads on bright backgrounds."""

    DUR_S, DUR_H = 0.20, 0.24

    def __init__(self, t0, t1, pre=(), hero=(), post=(), style="video", at=(1430, 470), hs=150, ss=44, maxw=820,
                 align="left", strike=None, redact=None, flap=None, chrome=False, quote=False):
        self.t0, self.t1 = t0, t1
        self.pre, self.hero, self.post = list(pre), list(hero), list(post)
        self.style, self.at, self.hs, self.ss, self.maxw, self.align = style, at, hs, ss, maxw, align
        self.strike, self.redact, self.flap, self.chrome, self.quote = strike, redact, flap, chrome, quote
        self.exit = True
        self.toks = None

    # ---------- layout (computed once with ALL words so nothing jumps while words are added)
    def layout(self):
        fs = font(self.ss, MED)
        full = [(disp(h[0]) if len(h) < 3 else h[2], h[1], h[0]) for h in self.hero]
        hs = self.hs
        while True:
            fb, fsm = font(hs, BOLD), font(hs * 0.32, MED)
            wsum = sum((fb if k == "big" else fsm).getlength(txt) for txt, k, _ in full) + max(0, len(full) - 1) * hs * 0.16
            if not full or wsum <= self.maxw or hs < 40:
                break
            hs *= 0.93
        self.hs_eff = hs
        fb, fsm = font(hs, BOLD), font(hs * 0.32, MED)
        pre_ids = [i for i in self.pre if disp(i)]
        post_ids = [i for i in self.post if disp(i)]
        wpre = fs.getlength(" ".join(disp(i) for i in pre_ids))
        wpost = fs.getlength(" ".join(disp(i) for i in post_ids))
        ax, ay = self.at
        width = max(wsum if full else 0, wpre, wpost)
        if self.align == "center":
            x0 = ax - (wsum if full else wpre) / 2
        else:
            x0 = min(ax, W - 60 - (wsum if full else wpre))
        toks = []
        sp = fs.getlength(" ")
        hero_top = ay - hs * 0.5
        # pre (wrapped to the block width when too long)
        lim = max(wsum if full else 0, min(self.maxw, W - 70 - x0), 300)
        lines, cur = [], []
        for i in pre_ids:
            if cur and fs.getlength(" ".join(disp(j) for j in cur + [i])) > lim and not self.quote:
                lines.append(cur); cur = []
            cur.append(i)
        if cur:
            lines.append(cur)
        for li, line in enumerate(lines):
            if full:
                y = hero_top - self.ss * 1.12 * (len(lines) - li)
            else:
                y = ay - self.ss / 2 - self.ss * 1.12 * (len(lines) - 1 - li)
            lw = fs.getlength(" ".join(disp(j) for j in line))
            x = (ax - lw / 2) if (self.align == "center" and not full) else x0
            for j in line:
                txt = disp(j)
                if self.quote and j == pre_ids[0]:
                    txt = "„" + txt
                if self.quote and j == pre_ids[-1]:
                    txt = txt + "”"
                toks.append(dict(t=W_(j)["s"], x=x, y=y, txt=txt, f=fs, kind="s", idx=j))
                x += fs.getlength(txt) + sp
        # hero
        x = x0 if self.align != "center" else ax - wsum / 2
        for txt, kind, idx in full:
            f = fb if kind == "big" else fsm
            y = hero_top - fb.getbbox("H")[1] if kind == "big" else hero_top - fb.getbbox("H")[1] + hs * 0.02
            toks.append(dict(t=W_(idx)["s"], x=x, y=y, txt=txt, f=f, kind="h" if kind == "big" else "s", idx=idx))
            x += f.getlength(txt) + hs * 0.16
        self.hero_box = (x0 if self.align != "center" else ax - wsum / 2, hero_top, wsum, hs)
        # post (right-aligned under the hero when it fits, else left)
        if post_ids:
            y = hero_top + hs * 1.0 if full else ay + self.ss * 0.7
            if full and self.align == "left" and wpost <= wsum:
                x = x0 + wsum - wpost
            elif self.align == "center":
                x = ax - wpost / 2
            else:
                x = x0
            for j in post_ids:
                toks.append(dict(t=W_(j)["s"], x=x, y=y, txt=disp(j), f=fs, kind="s", idx=j))
                x += fs.getlength(disp(j)) + sp
        self.toks = toks

    # ---------- per-frame drawing
    def render(self, t):
        if self.toks is None:
            self.layout()
        life = max(0.3, self.t1 - self.t0)
        drift = -14 * ease((t - self.t0) / life * 0.9) - 4 * (t - self.t0) / life
        gone = 0.0
        if self.exit and t > self.t1 - 0.13:
            gone = ease((t - (self.t1 - 0.13)) / 0.13)
        mask = Image.new("L", (W, H), 0)
        red = bool(self.redact and self.redact[0] <= t < self.redact[1])
        boxes = []
        locked = not self.flap or t >= self.flap[1]
        for tk in self.toks:
            p = (t - tk["t"] + 0.05) / (self.DUR_H if tk["kind"] == "h" else self.DUR_S)
            if p < 0:
                continue
            e = ease(p)
            txt = tk["txt"]
            if self.flap and tk["kind"] == "h" and not locked:
                r = random.Random(int(t * 15))
                txt = "".join(str(r.randint(0, 9)) if c.isdigit() else c for c in txt)
            f = tk["f"]
            big = tk["kind"] == "h"
            rise = (40 if big else 22) * (1 - e) + 26 * gone
            x, y = tk["x"], tk["y"] + rise + drift
            if red and tk["kind"] == "s" and tk["idx"] in self.pre:
                wd = f.getlength(tk["txt"])
                boxes.append((x, y + f.size * 0.15, x + wd, y + f.size * 1.05))
                continue
            bb = f.getbbox(txt)
            pad = 40
            tw, th = int(bb[2] + pad * 2), int(bb[3] + pad * 2)
            im = Image.new("L", (tw, th), 0)
            ImageDraw.Draw(im).text((pad, pad), txt, font=f, fill=int(255 * min(1, p * 2.4) * (1 - gone)))
            blur = (16 if big else 10) * (1 - e) + 12 * gone
            im = smear(im, blur)
            if big and e < 1:
                sc = 1.06 - 0.06 * e
                im = im.resize((int(tw * sc), int(th * sc)), Image.BICUBIC)
                x -= (im.width - tw) / 2; y -= (im.height - th) / 2
            mask.paste(Image.fromarray(np.maximum(np.asarray(mask.crop((int(x - pad), int(y - pad), int(x - pad) + im.width,
                                                                          int(y - pad) + im.height))), np.asarray(im))),
                       (int(x - pad), int(y - pad)))
        a = np.asarray(mask).astype(np.float32)
        out = np.zeros((H, W, 4), np.float32)
        if self.chrome:
            g = np.linspace(255, 165, H, dtype=np.float32)[:, None]
            col = np.dstack([g * np.ones((1, W))] * 3)
        else:
            col = np.empty((H, W, 3), np.float32)
            col[:] = BLUE_TXT if self.style == "light" else (255, 255, 255)
        if self.style in ("video",):
            wide = np.asarray(mask.filter(ImageFilter.GaussianBlur(22))).astype(np.float32) * 0.85
            tight = np.asarray(mask.filter(ImageFilter.GaussianBlur(3)).transform(mask.size, Image.AFFINE, (1, 0, -2, 0, 1, -4)))
            sh = np.maximum(wide, tight.astype(np.float32) * 0.7)
        elif self.style == "black":
            sh = None
        else:
            sh = np.asarray(mask.filter(ImageFilter.GaussianBlur(18))).astype(np.float32) * (0.18 if self.style == "light" else 0.35)
        if sh is not None:
            out[..., 3] = np.minimum(sh, 255)
        alpha = np.maximum(a, out[..., 3])
        out[..., :3] = col * (a / np.maximum(alpha, 1))[..., None]
        out[..., 3] = alpha
        img = out.clip(0, 255).astype(np.uint8)
        if self.strike and t >= self.strike and self.toks:
            st = ease((t - self.strike) / 0.22)
            hx, hy, hw, hh = self.hero_box
            yy = int(hy + hh * 0.48 + drift)
            img[yy:yy + max(6, int(hh * 0.07)), int(hx - 10):int(hx - 10 + (hw + 20) * st)] = (235, 64, 52, 255)
        for b in boxes:
            x1, y1, x2, y2 = map(int, b)
            img[y1:y2, x1:x2] = (255, 255, 255, 255)
        return img


def comp(bg, rgba):
    a = rgba[..., 3:4].astype(np.float32) / 255
    return (bg.astype(np.float32) * (1 - a) + rgba[..., :3].astype(np.float32) * a).astype(np.uint8)


def ws(i):
    return W_(i)["s"]


# ------------------------------------------------------------------ special scenes
def rounded(im, r):
    m = Image.new("L", im.size, 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, im.size[0] - 1, im.size[1] - 1], r, fill=255)
    out = im.convert("RGBA"); out.putalpha(m)
    return out


def persp_coeffs(src, dst):
    m = []
    for (x, y), (u, v) in zip(dst, src):
        m.append([x, y, 1, 0, 0, 0, -u * x, -u * y]); m.append([0, 0, 0, x, y, 1, -v * x, -v * y])
    A = np.array(m, np.float64); bvec = np.array(src, np.float64).reshape(8)
    return np.linalg.solve(A, bvec).tolist()


class FeedWall:
    def __init__(self, n, tiles):
        """tiles: [(video_path, time_s), ...] — frames become B&W 9:16 tiles (repeated to fill 7×5)."""
        picks = tiles
        tw, th, gap, cols, rows = 300, 533, 26, 7, 5
        CW, CH = cols * (tw + gap), rows * (th + gap)
        canvas = Image.new("RGB", (CW, CH), (8, 8, 8))
        k = 0
        for r in range(rows):
            for c in range(cols):
                f, t = picks[k % len(picks)]; k += 1
                im = ImageOps.fit(still(f, t, grade="bw"), (tw, th))
                canvas.paste(rounded(im, 22), (c * (tw + gap) + (r % 2) * 0, r * (th + gap)), rounded(im, 22))
        self.canvas, self.n = canvas, n
        self.CW, self.CH = CW, CH

    def frame(self, i):
        p = i / max(1, self.n - 1)
        oy = 260 + 420 * p
        src = [(260, oy), (self.CW - 260, oy), (self.CW, oy + 1500), (0, oy + 1500)]
        dst = [(560, 300), (1360, 300), (2400, 1250), (-480, 1250)]
        im = self.canvas.transform((W, H), Image.PERSPECTIVE, persp_coeffs(src, dst), Image.BICUBIC, fillcolor=(0, 0, 0))
        a = np.asarray(im).astype(np.float32)
        top = np.asarray(im.filter(ImageFilter.GaussianBlur(9))).astype(np.float32)
        y = np.linspace(0, 1, H)[:, None, None]
        m = np.clip((0.55 - y) / 0.35, 0, 1)
        a = a * (1 - m) + top * m
        vign = (np.clip(1.25 - np.hypot(np.linspace(-1, 1, W)[None, :], np.linspace(-1, 1, H)[:, None] * 1.2), 0, 1) ** 0.8)[..., None]
        a = a * (0.25 + 0.75 * vign) * 0.82
        return a.clip(0, 255).astype(np.uint8)


class Collage:
    def __init__(self, photos, t0, t1):
        """photos: list of image paths (EXIF-rotated); they drop in one by one between t0 and t1 on the right half."""
        files = photos
        self.cards = []
        r = random.Random(3)
        n = len(files)
        for k, f in enumerate(files):
            im = ImageOps.exif_transpose(Image.open(f)).convert("RGB")
            im = ImageOps.fit(im, (300, 360))
            card = Image.new("RGB", (330, 430), (250, 250, 250)); card.paste(im, (15, 15))
            card = card.rotate(r.uniform(-8, 8), resample=Image.BICUBIC, expand=True, fillcolor=(0, 0, 0, 0)) if False else card
            card = card.convert("RGBA").rotate(r.uniform(-8, 8), resample=Image.BICUBIC, expand=True)
            cx = 1240 + (k % 3) * 210 + r.uniform(-40, 40) - (k // 3) * 60
            cy = 330 + (k // 3) * 300 + r.uniform(-50, 50)
            ta = t0 + 0.05 + k * (t1 - t0 - 0.5) / n
            self.cards.append((card, cx, cy, ta))

    def frame(self, t):
        img = Image.fromarray(LIGHT.copy()).convert("RGBA")
        for card, cx, cy, ta in self.cards:
            if t < ta:
                continue
            p = min(1, (t - ta) / 0.18)
            s = 1.18 - 0.18 * (1 - (1 - p) ** 3)
            c = card.resize((int(card.width * s), int(card.height * s)), Image.BICUBIC)
            shadow = Image.new("RGBA", c.size, (0, 0, 0, 0))
            shadow.putalpha(c.getchannel("A").point(lambda v: int(v * 0.28 * p)))
            shadow = shadow.filter(ImageFilter.GaussianBlur(14))
            x, y = int(cx - c.width / 2), int(cy - c.height / 2)
            img.alpha_composite(shadow, (x + 8, y + 16))
            if p < 1:
                c.putalpha(c.getchannel("A").point(lambda v: int(v * p)))
            img.alpha_composite(c, (x, y))
        return np.asarray(img.convert("RGB"))


TITLES = [("$500", "DZIENNIE"), ("PASYWNY", "DOCHÓD"), ("10K/MSC", "OD ZERA"), ("SEKRET", "GURU"), ("KURS", "997 ZŁ"),
          ("MILION", "W ROK?"), ("ZARABIAJ", "ŚPIĄC"), ("DROP", "SHIPPING")]


def thumb(seed, w=1280, h=720, titles=None):
    r = random.Random(seed)
    pal = [((36, 20, 70), (210, 60, 90)), ((10, 40, 30), (40, 200, 120)), ((60, 30, 10), (240, 160, 40)),
           ((10, 20, 60), (60, 120, 240)), ((40, 10, 10), (230, 50, 40)), ((20, 20, 20), (200, 200, 60))][seed % 6]
    y, x = np.mgrid[0:h, 0:w].astype(np.float32)
    t = np.clip(x / w * 0.7 + y / h * 0.3, 0, 1)[..., None]
    g = (np.array(pal[0]) * (1 - t) + np.array(pal[1]) * t).astype(np.uint8)
    im = Image.fromarray(g)
    d = ImageDraw.Draw(im)
    sx = r.choice([0.22, 0.75]) * w
    d.ellipse([sx - 130, h * 0.18, sx + 130, h * 0.18 + 290], fill=(20, 16, 18))           # anonymous blurred figure
    d.rounded_rectangle([sx - 260, h * 0.55, sx + 260, h * 1.3], 120, fill=(16, 14, 16))
    im = im.filter(ImageFilter.GaussianBlur(10))
    d = ImageDraw.Draw(im)
    titles = titles or TITLES
    a, b = titles[seed % len(titles)]
    tx = 70 if sx > w / 2 else w * 0.48
    fsz = 150
    while max(font(fsz, BOLD).getlength(a), font(fsz, BOLD).getlength(b)) > w * 0.46:
        fsz -= 6
    f = font(fsz, BOLD)
    for k, line in enumerate((a, b)):
        col = (255, 225, 40) if k == 0 else (255, 255, 255)
        d.text((tx, 150 + k * fsz * 1.1), line, font=f, fill=col, stroke_width=8, stroke_fill=(0, 0, 0))
    return im


class GuruWall:
    def __init__(self, titles=None):
        """titles: [(line1, line2), ...] for invented thumbnails (anonymous blurred figures, never real creators)."""
        self.th = [thumb(s, titles=titles) for s in range(8)]
        self.side = [ImageOps.fit(thumb(s + 3, titles=titles), (300, 169)) for s in range(9)]

    def frame(self, t, k):
        img = Image.new("RGB", (W, H), (14, 14, 14))
        main = self.th[k % len(self.th)].resize((1240, 698))
        img.paste(rounded(main, 18), (50, 70), rounded(main, 18))
        d = ImageDraw.Draw(img)
        d.rounded_rectangle([50, 790, 900, 828], 8, fill=(60, 60, 60))
        d.rounded_rectangle([50, 846, 620, 870], 8, fill=(42, 42, 42))
        off = int(t * 60) % 190
        for j, s in enumerate(self.side):
            y = 70 + j * 190 - off
            img.paste(rounded(s, 12), (1330, y), rounded(s, 12))
            d.rounded_rectangle([1650, y + 14, 1860, y + 40], 6, fill=(70, 70, 70))
            d.rounded_rectangle([1650, y + 54, 1800, y + 72], 6, fill=(45, 45, 45))
        a = np.asarray(img).astype(np.float32)
        y = np.linspace(0, 1, H)[:, None, None]
        a = a * (1 - np.clip((y - 0.62) / 0.38, 0, 1) * 0.75)
        return a.clip(0, 255).astype(np.uint8)


def giant(bg, text, t, t0, size=520, y=440):
    p = min(1, max(0, (t - t0) / 0.15))
    if p <= 0:
        return bg
    f = font(size, BOLD)
    wd = f.getlength(text)
    while wd > 1780:
        size *= 0.95; f = font(size, BOLD); wd = f.getlength(text)
    s = 1 + 0.035 * min(1, (t - t0) / 1.2)
    lay = Image.new("L", (W, H), 0)
    ImageDraw.Draw(lay).text((W / 2 - wd / 2, y - size * 0.62), text, font=f, fill=255)
    lay = lay.resize((int(W * s), int(H * s)), Image.BICUBIC).crop((int((W * s - W) / 2), int((H * s - H) / 2),
                                                                     int((W * s - W) / 2) + W, int((H * s - H) / 2) + H))
    m = np.asarray(lay).astype(np.float32)[..., None] / 255
    grad = np.linspace(0.85, 0.35, H)[:, None, None]
    a = m * grad * p
    b = bg.astype(np.float32)
    return (b + (255 - b) * a).clip(0, 255).astype(np.uint8)


def letterbox(img, t):
    if t >= 0.75:
        return img
    p = t / 0.75
    e = 1 - (1 - p) ** 3
    h = int(400 * (1 - e))
    if h > 0:
        img = img.copy(); img[:h] = 0; img[H - h:] = 0
    return img


def desk_text(bg, text, p, quad=((250, 858), (820, 842), (880, 990), (175, 1012)), size=170):
    """quad = the surface corners on screen (TL, TR, BR, BL); find them on a still of the shot."""
    lay = Image.new("L", (900, 220), 0)
    ImageDraw.Draw(lay).text((20, 10), text, font=font(size, BOLD), fill=255)
    src = [(0, 0), (900, 0), (900, 220), (0, 220)]
    dst = list(quad)
    w = lay.transform((W, H), Image.PERSPECTIVE, persp_coeffs(src, dst), Image.BICUBIC)
    a = np.asarray(w).astype(np.float32)[..., None] / 255 * 0.92 * p
    return (bg * (1 - a) + 255 * a).astype(np.uint8)


# ------------------------------------------------------------------ the edit


def grid_frame(cells, t, t0, i, step=0.13, flash=2):
    """cells: 4 lists of 956×536 frames. Cells appear every `step` s with a `flash`-frame negative (flicker build)."""
    fr = np.zeros((H, W, 3), np.uint8)
    for c in range(4):
        tc = t0 + 0.04 + c * step
        if t < tc:
            continue
        cell = cells[c][min(i, len(cells[c]) - 1)]
        if t < tc + flash / FPS:
            cell = 255 - cell
        x, y = (c % 2) * 964, (c // 2) * 544
        fr[y:y + 536, x:x + 956] = cell
    return fr


def grid_cells(specs, n):
    """specs: [(path, ss, band), ...] ×4 → frame lists sized for grid_frame."""
    return [[np.asarray(Image.fromarray(f).resize((956, 536), Image.BILINEAR)) for f in
             read_clip(p, ss, n, clip_vf(band=b, grade="cine"))] for p, ss, b in specs]


def run(shots, phrases, out, aroll=None, dur=None, frames=None, face_crop=(1.14, 0.47, 0.42)):
    """shots: [(t0, t1, kind, params)] — kind: face | clip | light | blue | black | lapse | custom
         face  params: zoom (bool punch-in), open (letterbox)            → frames from `aroll` at the same time
         clip  params: src, ss, band, grade, zoom, crop, giant=(text, t)  → read_clip
         lapse params: src, a, b (seconds range sampled into the shot)    → timelapse
         custom params: fn(t, i) -> frame                                  → FeedWall/Collage/GuruWall/grid lambdas
         any   params: post(frame, t) -> frame                             → extra effect (desk_text etc.)
       phrases: [Phrase]; frames=[t,...] renders a preview sheet to `out` instead of a video."""
    dur = dur or shots[-1][1]
    cuts = [x[0] for x in shots] + [dur]
    for p in phrases:
        p.exit = not any(abs(c - p.t1) < 0.035 for c in cuts)
    only = [int(round(t * FPS)) for t in frames] if frames else None
    enc = None if only else subprocess.Popen(
        ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
         "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
    cache, sheet = {}, []
    for n in (only or range(int(round(dur * FPS)))):
        t = n / FPS
        k = next((i for i, s in enumerate(shots) if s[0] <= t + 1e-6 < s[1]), len(shots) - 1)
        t0, t1, kind, prm = shots[k]
        i = n - int(round(t0 * FPS))
        nshot = int(round(t1 * FPS)) - int(round(t0 * FPS))
        if k not in cache:
            cache.clear()
            if kind == "face":
                cache[k] = read_clip(aroll, t0, nshot, clip_vf(crop=face_crop if prm.get("zoom") else None, zoom=0.025,
                                                              dur=t1 - t0, grade="none"))
            elif kind == "clip":
                cache[k] = read_clip(prm["src"], prm["ss"], nshot, clip_vf(band=prm.get("band"), zoom=prm.get("zoom", 0),
                                     dur=t1 - t0, grade=prm.get("grade", "cine"), crop=prm.get("crop")))
            elif kind == "lapse":
                cache[k] = [np.asarray(still(prm["src"], tt, grade=prm.get("grade", "cine")).resize((W, H)))
                            for tt in np.linspace(prm["a"], prm["b"], nshot)]
        if kind in ("face", "clip", "lapse"):
            fr = cache[k][min(i, len(cache[k]) - 1)]
        elif kind == "light":
            fr = LIGHT
        elif kind == "blue":
            fr = BLUE
        elif kind == "black":
            fr = BLACK
        else:
            fr = prm["fn"](t, i)
        if prm.get("giant"):
            fr = giant(fr, prm["giant"][0], t, prm["giant"][1])
        if prm.get("post"):
            fr = prm["post"](fr, t)
        if prm.get("open"):
            fr = letterbox(fr, t)
        for p in phrases:
            if p.t0 <= t < p.t1:
                fr = comp(fr, p.render(t))
        fr = np.ascontiguousarray(fr, np.uint8)
        if only:
            sheet.append(Image.fromarray(fr).resize((640, 360)))
        else:
            enc.stdin.write(fr.tobytes())
    if only:
        cols = 4
        im = Image.new("RGB", (cols * 640, ((len(sheet) + cols - 1) // cols) * 360))
        for j, s_ in enumerate(sheet):
            im.paste(s_, ((j % cols) * 640, (j // cols) * 360))
        im.save(out)
        return out
    enc.stdin.close(); enc.wait()
    return out
