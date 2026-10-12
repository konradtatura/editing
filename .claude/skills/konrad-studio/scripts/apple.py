"""Apple-style Tesseract scene library (konrad-studio skill).
Look: white + soft glows, Geist / Geist Mono, Apple system colours, eased motion, everything on the word.
Fonts: text layers use typographic family ("Geist") + style ("SemiBold"); the Regular face must be packaged.

Usage in a project's scenes file (always init BEFORE `from apple import *`, so W/H are right):
    sys.path.insert(0, os.path.expanduser("~/.claude/skills/konrad-studio/scripts"))
    import apple; apple.init(PROJECT_DIR, 1080, 1920)      # or 1920, 1080
    from apple import *
Outputs: PROJECT_DIR/projects/<name>.tsrct, cache in PROJECT_DIR/.work and PROJECT_DIR/Source."""
import json, math, os, random, subprocess
from fontTools.ttLib import TTFont

SKILL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT_DIR = os.path.join(SKILL, "assets", "fonts")
ROOT = os.getcwd()
WORK = os.path.join(ROOT, ".work")
TSRCT = os.path.expanduser("~/Library/Application Support/Tesseract/bin/tsrct")
FONTS = ["Geist-Regular", "Geist-Medium", "Geist-SemiBold", "GeistMono-Regular", "GeistMono-Medium", "StudioSerif-Regular"]
ENV = dict(os.environ, TESSERACT_CALLER="agent-skill", TESSERACT_SKILL="tesseract-motion",
           TESSERACT_HOST="claude", TESSERACT_DISTRIBUTION="standalone-skill")
W, H = 1920, 1080


def init(project_dir, w=1920, h=1080):
    """Point the library at a project folder and set the canvas (1920×1080 or 1080×1920)."""
    global ROOT, WORK, W, H
    ROOT, W, H = os.path.abspath(project_dir), w, h
    WORK = os.path.join(ROOT, ".work")
    for d in (WORK, os.path.join(ROOT, "Source"), os.path.join(ROOT, "projects"), os.path.join(ROOT, "checks")):
        os.makedirs(d, exist_ok=True)

A_BG = [1, 1, 1, 1]
A_INK = [0.114, 0.114, 0.122, 1]      # #1D1D1F
A_GREY = [0.525, 0.525, 0.545, 1]     # #86868B
A_LINE = [0.898, 0.898, 0.918, 1]     # #E5E5EA
A_FILL = [0.961, 0.961, 0.969, 1]     # #F5F5F7
A_BLUE = [0.0, 0.443, 0.890, 1]       # #0071E3
A_GREEN = [0.204, 0.780, 0.349, 1]    # #34C759
A_RED = [1.0, 0.231, 0.188, 1]        # #FF3B30
A_ORANGE = [1.0, 0.584, 0.0, 1]       # #FF9500
PURPLE = [0.69, 0.32, 0.87, 1]
TEAL = [0.35, 0.78, 0.86, 1]
DARK = [0.08, 0.08, 0.09, 1]
GOLD = [1.0, 0.78, 0.25, 1]
GOLD_D = [0.72, 0.50, 0.05, 1]
DKGREEN = [0.1, 0.5, 0.2, 1]


def a(c, alpha):
    return c[:3] + [alpha]


APPLE = {"type": "cubicBezier", "x1": 0.32, "y1": 0.72, "x2": 0.0, "y2": 1.0}
OUT = {"type": "cubicBezier", "x1": 0.16, "y1": 1.0, "x2": 0.3, "y2": 1.0}
SOFT = {"type": "cubicBezier", "x1": 0.25, "y1": 0.1, "x2": 0.25, "y2": 1.0}
INOUT = {"type": "cubicBezier", "x1": 0.65, "y1": 0.0, "x2": 0.35, "y2": 1.0}
EIN = {"type": "cubicBezier", "x1": 0.5, "y1": 0.0, "x2": 0.9, "y2": 0.4}
HOLD = {"type": "hold"}
LIN = {"type": "linear"}


def f(v): return {"type": "float", "value": v}
def v2(x, y): return {"type": "vector2", "value": [x, y]}
def s(t): return {"type": "string", "value": t}
def col(c): return {"type": "color", "value": c}


def tf(x=0, y=0, ax=0, ay=0, op=100, sc=100, rot=0):
    return {"anchorPoint": [ax, ay], "position": [x, y], "scale": [sc, sc], "rotation": rot, "opacity": op}


_fonts = {st: TTFont(os.path.join(FONT_DIR, f"Geist-{st}.ttf")) for st in ("Medium", "SemiBold")}
_mono = TTFont(os.path.join(FONT_DIR, "GeistMono-Medium.ttf"))


def adv(t, size, style="Medium"):
    ft = _fonts["SemiBold" if style == "SemiBold" else "Medium"]
    cm = ft.getBestCmap()
    return sum(ft["hmtx"][cm[ord(c)]][0] for c in t if ord(c) in cm) * size / ft["head"].unitsPerEm * 0.975


def madv(t, size):
    cm = _mono.getBestCmap()
    return sum(_mono["hmtx"][cm[ord(c)]][0] for c in t) * size / _mono["head"].unitsPerEm


def zl(v):
    return f"{int(round(v)):,}".replace(",", " ") + " zł"


class Scene:
    def __init__(self, name, in_s, out_s, words_json, src, word_offset=0.0):
        sp = os.path.join(ROOT, "snap.json")          # snap_gaps.py: back-to-back scenes butt with no camera frames
        if os.path.exists(sp):
            out_s = json.load(open(sp)).get(name, out_s)
        self.name, self.in_s, self.out_s, self.src = name, in_s, out_s, src
        self.dur = int(round((out_s - in_s) * 1000))
        self.layers, self.A, self._kid = [], [], 0
        w = json.load(open(words_json))
        self.words = [dict(x, start=x["start"] + word_offset) for seg in w["segments"] for x in seg["words"]]

    def image(self, lid, name, path, x, y, w=None, h=None, r=0, op=100, ax=None, ay=None):
        """Real image (icon, screenshot, photo) as a doc-level layer; (x, y) = top-left, w/h = display size in px, r = corner radius in px
        (the engine stores image cornerRadius RELATIVE to the short side — converted here).
        Doc-level layers sit UNDER every createFx layer unless you build the covering elements with
        `self.under_images = True` (see silnik-tesseract.md). Animate it with k()/kpos() like any layer."""
        from PIL import Image as _I
        iw, ih = _I.open(path).size
        if w and not h:
            h = w * ih / iw
        w, h = w or iw, h or ih
        aid = f"img{lid}"
        self.images = getattr(self, "images", []) + [(aid, os.path.abspath(path))]
        ax = w / 2 if ax is None else ax
        ay = h / 2 if ay is None else ay
        self.layers.insert(0, {"type": "Image", "id": lid, "name": name, "blendMode": "normal",
                               "activeRange": {"start": 0, "duration": self.dur},
                               "transform": {"anchorPoint": [ax * iw / w, ay * ih / h], "position": [x + ax, y + ay],
                                             "scale": [100 * w / iw, 100 * h / ih], "rotation": 0, "opacity": op},
                               "cornerRadius": (r / min(w, h)) if r else None, "source": {"assetId": aid}})
        return lid

    def lower(self, lid):
        """Send a ROOT-level element (usually a card group) to the back, just above the footage/background,
        so images added with image() draw on top of it. Call right after creating it."""
        for act in self.A:
            if act.get("layerId") == lid and act["type"].startswith("createFx"):
                act["_lower"] = True          # resolved in build(), when the number of images is final
                return lid
        raise SystemExit(f"lower(): layer {lid} not found")

    def motion_blur(self, lid, on=True):
        """Real motion blur on a moving layer (push-ins, whip pans, flying cards) — the premium 'camera' feel."""
        self.A.append({"type": "setFxLayerMotionBlur", "compositionId": "main", "layerId": lid, "enabled": on})

    def t(self, video_s):
        return int(round((video_s - self.in_s) * 1000))

    def word(self, video_s):
        wb = min(self.words, key=lambda x: abs(x["start"] - video_s))
        assert abs(wb["start"] - video_s) < 0.05, (video_s, wb)
        return self.t(wb["start"])

    def rng(self, a0=0, a1=None):
        return {"start": a0, "duration": (self.dur if a1 is None else a1) - a0}

    def group(self, lid, name, parent=None, x=0, y=0, ax=0, ay=0, op=100, sc=100):
        self.A.append({"type": "createFxGroupLayer", "compositionId": "main", "layerId": lid, "name": name,
                       "parentLayerId": parent, "insertIndex": 0, "activeRange": self.rng(),
                       "transform": tf(x, y, ax, ay, op, sc)})
        return lid

    def rect(self, lid, name, parent, x, y, w, h, fill, r=0, stroke=None, op=100, ax=0, ay=0):
        shape = {"size": [w, h], "fillColor": fill, "roundness": r}
        if stroke:
            shape.update({"strokeEnabled": True, "strokeColor": stroke[0], "strokeWidth": stroke[1]})
        self.A.append({"type": "createFxRectLayer", "compositionId": "main", "layerId": lid, "name": name,
                       "parentLayerId": parent, "insertIndex": 0, "activeRange": self.rng(),
                       "transform": tf(x + ax, y + ay, ax, ay, op), "rect": shape})
        return lid

    def text(self, lid, name, parent, x, y, txt, size, color=A_INK, style="SemiBold", family="Geist",
             tracking=0, just="left", op=100, animators=None):
        st = {"text": txt, "fontFamily": family, "fontStyle": style, "fontSize": size, "fillColor": color,
              "strokeWidth": 0, "justification": just, "tracking": tracking}
        act = {"type": "createFxTextLayer", "compositionId": "main", "layerId": lid, "name": name,
               "parentLayerId": parent, "insertIndex": 0, "activeRange": self.rng(),
               "transform": tf(x, y, op=op), "sourceText": st}
        if animators:
            act["animators"] = animators
        self.A.append(act)
        return lid

    def mono(self, lid, name, parent, x, y, txt, size, color=A_INK, just="left", op=100, style="Medium"):
        return self.text(lid, name, parent, x, y, txt, size, color, style=style, family="Geist Mono", just=just, op=op)

    def path(self, lid, name, parent, pts, x=0, y=0, fill=None, stroke=None, op=100, closed=True, trim=None, ax=0, ay=0):
        cmds = [{"type": "moveTo", "x": pts[0][0], "y": pts[0][1]}] + [{"type": "lineTo", "x": px, "y": py} for px, py in pts[1:]]
        if closed:
            cmds.append({"type": "close"})
        shape = {"path": {"commands": cmds}, "fills": [], "strokes": []}
        if trim is not None:
            shape["trim"] = {"start": 0, "end": trim, "offset": 0, "mode": "simultaneously"}
        if fill:
            shape["fills"].append({"paint": {"type": "solid", "color": fill}, "fillRule": "nonZeroWinding",
                                   "blendMode": "normal", "opacity": 1})
        if stroke:
            shape["strokes"].append({"paint": {"type": "solid", "color": stroke[0]}, "width": stroke[1], "cap": "round",
                                     "join": "round", "miterLimit": 4, "blendMode": "normal", "opacity": 1})
        self.A.append({"type": "createFxShapeLayer", "compositionId": "main", "layerId": lid, "name": name,
                       "parentLayerId": parent, "insertIndex": 0, "activeRange": self.rng(),
                       "transform": tf(x + ax, y + ay, ax, ay, op), "shape": shape})
        return lid

    def ring(self, lid, name, parent, cx, cy, d, color, width, trim_end=100, op=100):
        shape = {"path": {"commands": []}, "ellipse": {"size": [d, d], "position": [0, 0]}, "fills": [],
                 "strokes": [{"paint": {"type": "solid", "color": color}, "width": width, "cap": "round", "join": "round",
                              "miterLimit": 4, "blendMode": "normal", "opacity": 1}],
                 "trim": {"start": 0, "end": trim_end, "offset": 0, "mode": "simultaneously"}}
        self.A.append({"type": "createFxShapeLayer", "compositionId": "main", "layerId": lid, "name": name,
                       "parentLayerId": parent, "insertIndex": 0, "activeRange": self.rng(),
                       "transform": tf(cx, cy, op=op), "shape": shape})
        return lid

    def shadow(self, lid, alpha=0.10, blur_=48, oy=16):
        self.A.append({"type": "addFxLayerEffect", "compositionId": "main", "layerId": lid, "effectId": 5000 + lid,
                       "effect": {"type": "dropShadow", "enabled": True, "color": [0, 0, 0, alpha], "offset": [0, oy],
                                  "blurRadius": blur_, "spreadRadius": 0, "blendMode": "normal"}})

    def blur(self, lid, eid, amount):
        self.A.append({"type": "addFxLayerEffect", "compositionId": "main", "layerId": lid, "effectId": eid,
                       "effect": {"type": "gaussianBlur", "blurriness": amount}})

    def matte(self, lid, matte_lid):
        self.A.append({"type": "setFxLayerTrackMatte", "compositionId": "main", "layerId": lid, "matteLayerId": matte_lid, "mode": "alpha"})

    def k(self, lid, prop, keys):
        self._kid += 1
        self.A.append({"type": "setFxPropertyKeyframes", "compositionId": "main",
                       "property": {"layerId": lid, "propertyType": prop},
                       "keyframes": [{"id": f"k{self._kid}-{i}", "layerTime": int(t), "value": v, "easing": e}
                                     for i, (t, v, e) in enumerate(keys)]})

    def kpos(self, lid, keys):
        self._kid += 1
        mk = lambda ax_: {"keyframes": [{"id": f"p{self._kid}{ax_}-{i}", "layerTime": int(t), "value": f(x if ax_ == "x" else y),
                                         "easing": e} for i, (t, x, y, e) in enumerate(keys)]}
        self.A.append({"type": "setFxPositionKeyframes", "compositionId": "main", "layerId": lid,
                       "positionX": mk("x"), "positionY": mk("y")})

    def kstyle(self, lid, item, prop, keys):
        self._kid += 1
        self.A.append({"type": "setFxAnimator", "compositionId": "main", "dependencies": [],
                       "target": {"type": "styleProperty", "layerId": lid, "itemId": item, "propertyName": prop},
                       "animator": {"type": "keyframes", "enabled": True, "keyframes": [
                           {"id": f"s{self._kid}-{i}", "layerTime": int(t), "value": v, "easing": e}
                           for i, (t, v, e) in enumerate(keys)]}})

    @staticmethod
    def reveal_animator(aid, sel_id, dy=26, blur_=10):
        return {"id": aid, "name": "word reveal", "opacity": 0, "blur": [blur_, blur_], "position": [0, dy],
                "selectors": [{"id": sel_id, "units": "index", "basedOn": "words", "mode": "add", "amount": 1,
                               "shape": "square", "start": 0, "end": 999}]}

    @staticmethod
    def color_animator(aid, sel_id, color, w0, w1):
        return {"id": aid, "name": "accent words", "fillColor": color,
                "selectors": [{"id": sel_id, "units": "index", "basedOn": "words", "mode": "add", "amount": 1,
                               "shape": "square", "start": w0, "end": w1}]}

    def reveal_words(self, lid, sel_id, times, step=170):
        keys = [(0, f(0), LIN)]
        for i, tt in enumerate(times):
            keys.append((max(tt, keys[-1][0] + 1), f(i), HOLD))
            keys.append((tt + step, f(i + 1), OUT))
        self.kstyle(lid, sel_id, "start", keys)

    @staticmethod
    def roll_keys(t0, t1, fmt, v0, v1, fps=30, ease_pow=2.2):
        keys, n, last = [], max(2, int((t1 - t0) / 1000 * fps)), None
        for i in range(n + 1):
            p = i / n
            txt = fmt(v0 + (v1 - v0) * (1 - (1 - p) ** ease_pow))
            if txt != last:
                keys.append((t0 + (t1 - t0) * p, s(txt), HOLD)); last = txt
        return keys

    def apple_bg(self):
        self.bg = A_BG
        self.layers += [blob(6, -620, -760, 1400, [1.0, 0.90, 0.85, 0.30], dur=self.dur),
                        blob(7, 1250, 560, 1400, [0.90, 0.93, 1.0, 0.22], dur=self.dur)]

    def footage(self):
        clip = os.path.join(ROOT, "Source", f"{self.name}_src.mp4")
        stamp = clip + ".range"
        want = f"{self.src}|{self.in_s:.3f}|{self.dur}"
        if not (os.path.exists(clip) and os.path.exists(stamp) and open(stamp).read() == want):
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{self.in_s:.3f}", "-i", self.src, "-t", f"{self.dur/1000:.3f}",
                            "-c:v", "libx264", "-crf", "12", "-preset", "slow", "-pix_fmt", "yuv420p",
                            "-c:a", "aac", "-b:a", "256k", clip], check=True)
            open(stamp, "w").write(want)
        self.video_clip = clip
        return {"type": "Video", "id": 11, "name": "Footage", "blendMode": "normal",
                "activeRange": {"start": 0, "duration": self.dur}, "sourceRange": {"start": 0, "duration": self.dur},
                "sourceIntrinsicDuration": self.dur, "volume": 1.0, "transform": tf(),
                "source": {"assetId": "footage", "fit": "contain"}}

    def build(self, out_basename=None):
        src_audio = os.path.join(ROOT, "Source", f"{self.name}_audio.wav")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{self.in_s:.3f}", "-i", self.src, "-t", f"{self.dur/1000:.3f}",
                        "-vn", "-ac", "2", "-ar", "48000",
                        "-af", "afade=t=in:d=0.012,afade=t=out:st=%.3f:d=0.02" % (self.dur / 1000 - 0.02), src_audio], check=True)
        os.makedirs(WORK, exist_ok=True)
        proj = os.path.join(WORK, f"{self.name}_build.tsrct")
        if os.path.exists(proj):
            os.remove(proj)
        run = lambda *a_: subprocess.run([TSRCT, *a_], check=True, env=ENV, capture_output=True, text=True).stdout
        run("project", "create", "--project", proj)
        if getattr(self, "video_clip", None):
            run("project", "import-video", "--project", proj, "--file", self.video_clip, "--asset-id", "footage")
        else:
            run("project", "import-asset", "--project", proj, "--file", src_audio, "--asset-id", "vo", "--kind", "audio")
        for aid, pth in getattr(self, "images", []):
            run("project", "import-asset", "--project", proj, "--file", pth, "--asset-id", aid, "--kind", "image")
        for fn in FONTS:
            run("project", "import-font", "--project", proj, "--file", os.path.join(FONT_DIR, fn + ".ttf"))
        ej = os.path.join(WORK, f"{self.name}_editable.json")
        run("project", "checkout", "--project", proj, "--output", ej)
        doc = json.load(open(ej))
        doc["dimensions"] = {"width": W, "height": H}
        doc["duration"] = self.dur / 1000
        voice = [] if getattr(self, "video_clip", None) else [
            {"type": "Audio", "id": 9, "name": "Voice", "windowMs": 100, "source": {"assetId": "vo"},
             "activeRange": {"start": 0, "duration": self.dur}, "sourceRange": {"start": 0, "duration": self.dur},
             "sourceIntrinsicDuration": self.dur, "volume": 1.0, "captionsEnabled": False}]
        doc["composition"]["layers"] = self.layers + voice + [
            {"type": "Rect", "id": 8, "name": "Background", "blendMode": "normal",
             "activeRange": {"start": 0, "duration": self.dur}, "transform": tf(),
             "rect": {"size": [W, H], "fillColor": getattr(self, "bg", A_BG)}}]
        json.dump(doc, open(ej, "w"), indent=1, ensure_ascii=False)
        run("project", "commit", "--project", proj, "--file", ej)
        ids = {}
        for act in self.A:
            if act["type"].startswith("createFx") and "layerId" in act:
                if act["layerId"] in ids:
                    raise SystemExit(f"duplicate layer id {act['layerId']}: {ids[act['layerId']]} / {act.get('name')}")
                ids[act["layerId"]] = act.get("name")
        seen = {}
        for act in self.A:
            if act["type"] == "setFxPropertyKeyframes":
                tracks = [((act["property"]["layerId"], act["property"]["propertyType"]), act["keyframes"])]
            elif act["type"] == "setFxPositionKeyframes":
                tracks = [((act["layerId"], ax_), act[ax_]["keyframes"]) for ax_ in ("positionX", "positionY")]
            else:
                continue
            for key, kfs in tracks:
                last = -1
                for kf in kfs:
                    if (key, kf["layerTime"]) in seen:
                        raise SystemExit(f"duplicate key time {kf['layerTime']} on layer {key[0]} {key[1]}")
                    if kf["layerTime"] < last:
                        raise SystemExit(f"unsorted key time {kf['layerTime']} < {last} on layer {key[0]} {key[1]}")
                    last = kf["layerTime"]
                    seen[(key, kf["layerTime"])] = 1
        n_img, prev = len(getattr(self, "images", [])), 0
        for act in self.A:
            if act.pop("_lower", False):
                act["insertIndex"] = n_img + prev
            if act["type"].startswith("createFx") and act.get("parentLayerId") is None:
                prev += 1
        aj = os.path.join(WORK, f"{self.name}_actions.json")
        json.dump(self.A, open(aj, "w"), indent=1, ensure_ascii=False)
        r = subprocess.run([TSRCT, "project", "apply", "--project", proj, "--actions", aj], env=ENV, capture_output=True, text=True)
        if r.returncode:
            raise SystemExit(r.stderr)
        final = os.path.join(ROOT, "projects", f"{self.name}.tsrct")
        os.makedirs(os.path.dirname(final), exist_ok=True)
        os.replace(proj, final)
        print(f"built {self.name}: {len(self.A)} actions, {self.dur} ms", flush=True)
        return final


# ------------------------------------------------------------------ helpers
def blob(lid, x, y, d, c, blur_=320, dur=None):
    return {"type": "Rect", "id": lid, "name": "Glow", "blendMode": "normal", "activeRange": {"start": 0, "duration": dur},
            "transform": tf(x, y), "rect": {"size": [d, d], "fillColor": c, "roundness": d / 2},
            "effects": [{"id": 7000 + lid, "effect": {"type": "gaussianBlur", "blurriness": blur_}}]}


def fade(sc, lid, t_in, t_out=None, d_in=260, d_out=220):
    keys = [(0, f(0), LIN), (t_in, f(0), HOLD), (t_in + d_in, f(100), SOFT)]
    if t_out is not None:
        keys += [(t_out, f(100), HOLD), (t_out + d_out, f(0), SOFT)]
    sc.k(lid, "opacity", keys)


def scale_keys(sc, lid, keys):
    for p in ("scaleX", "scaleY"):
        sc.k(lid, p, keys)


def pop(sc, lid, t, dur=520, frm=70):
    scale_keys(sc, lid, [(0, f(frm), LIN), (t, f(frm), HOLD), (t + dur, f(100), APPLE)])


def check(sc, lid, parent, cx, cy, size, color, width=4, op=100):
    k_ = size / 24
    return sc.path(lid, "Check", parent, [(0, 12 * k_), (8 * k_, 20 * k_), (24 * k_, 2 * k_)], cx - 12 * k_, cy - 11 * k_,
                   stroke=(color, width), closed=False, op=op)


def arc(cx, cy, r, a0, a1, n=36):
    return [(cx + r * math.cos(math.radians(a0 + (a1 - a0) * i / n)), cy + r * math.sin(math.radians(a0 + (a1 - a0) * i / n)))
            for i in range(n + 1)]


def card_bg(sc, lid, parent, x, y, w_, h_, r=30, fill=A_BG, sh=(0.10, 50, 16), stroke=None, op=100):
    c = sc.rect(lid, "Card", parent, x, y, w_, h_, fill, r=r, stroke=stroke, op=op)
    if sh:
        sc.shadow(c, *sh)
    return c


def pill_text(sc, base, parent, cx, cy, text, size, fg, bg, pad=26, style="Medium", h=None):
    h = h or size + 26
    wd = adv(text, size, style) + pad * 2
    sc.rect(base, "Pill", parent, cx - wd / 2, cy - h / 2, wd, h, bg, r=h / 2)
    sc.text(base + 1, "Pill text", parent, cx, cy + size * 0.36, text, size, fg, style=style, just="center")
    return wd


def ok_badge(sc, base, parent, cx, cy, t, d=36, color=A_GREEN):
    g = sc.group(base, "Ok", parent, cx, cy, cx, cy, op=0)
    sc.rect(base + 1, "Ok bg", g, cx - d / 2, cy - d / 2, d, d, color, r=d / 2)
    check(sc, base + 2, g, cx, cy + 1, d * 0.36, A_BG, max(2.5, d / 12))
    fade(sc, g, t, d_in=160)
    pop(sc, g, t, 420, 50)
    return g


def card_in(sc, g, t_in, t_out, sc0=96):
    sc.k(g, "opacity", [(0, f(0), LIN), (t_in, f(0), HOLD), (t_in + 260, f(100), SOFT), (t_out, f(100), HOLD), (t_out + 260, f(0), SOFT)])
    scale_keys(sc, g, [(0, f(sc0), LIN), (t_in, f(sc0), HOLD), (t_in + 700, f(100), OUT)])


def cursor(sc, lid, parent, x, y, op=0):
    """macOS arrow cursor, tip at the group's anchor (x, y). Returns group id."""
    g = sc.group(lid, "Cursor", parent, x, y, x, y, op=op)
    sc.path(lid + 1, "Arrow", g, [(0, 0), (0, 34), (9, 26), (15, 40), (21, 37), (15, 24), (26, 24)], x, y, fill=A_INK, stroke=(A_BG, 2.5))
    return g


def toggle(sc, base, parent, x, y, t_on, on_color=A_GREEN):
    """iOS switch (104×60) with top-left (x, y); flips on at t_on (None = stays off)."""
    tr = sc.rect(base, "Track", parent, x, y, 104, 60, A_LINE, r=30)
    kn = sc.rect(base + 1, "Knob", parent, x + 3, y + 3, 54, 54, A_BG, r=27)
    sc.shadow(kn, 0.2, 8, 3)
    if t_on is not None:
        sc.k(kn, "positionX", [(0, f(x + 3), LIN), (t_on, f(x + 3), HOLD), (t_on + 300, f(x + 47), APPLE)])
        sc.k(tr, "fillColor", [(0, col(A_LINE), LIN), (t_on, col(A_LINE), HOLD), (t_on + 220, col(on_color), SOFT)])
    return tr, kn


def overlay(sc):
    sc.layers.append(sc.footage())
    return sc.group(100, "FX", None, 0, 0)


# ------------------------------------------------------------------ helpers added 2026-10-03 (reference study)
LEAD = 100      # ms: visual entrances land a hair BEFORE the word (shots/hits: 50 ms); use w(t) - LEAD


def curve(sc, lid, parent, p0, p1, t, dur=420, color=None, width=4, bend=0.5, op=100):
    """Hand-drawn style S-curve connector from p0 to p1 that DRAWS itself (trimEnd 0→100) starting at t.
    Straight connectors read cheap; both reference films use these curves to link icon → labels."""
    (x0, y0), (x3, y3) = p0, p1
    dx = (x3 - x0) * bend
    pts = []
    for i in range(41):
        u = i / 40
        a_, b_, c_, d_ = (1 - u) ** 3, 3 * (1 - u) ** 2 * u, 3 * (1 - u) * u ** 2, u ** 3
        pts.append((a_ * x0 + b_ * (x0 + dx) + c_ * (x3 - dx) + d_ * x3, a_ * y0 + b_ * y0 + c_ * y3 + d_ * y3))
    sc.path(lid, "Curve", parent, pts, stroke=(color or A_GREY, width), closed=False, trim=0, op=op)
    sc.k(lid, "trimEnd", [(0, f(0), LIN), (t, f(0), HOLD), (t + dur, f(100), OUT)])
    return lid


def highlight(sc, lid, parent, x, y, w_, h_, t, dur=480, color=None):
    """Yellow marker sweeping left→right over a row/phrase on the spoken keyword (the 'real page + highlighter' move).
    Create it BEFORE the text it marks so it sits under the words."""
    c = color or [1.0, 0.84, 0.04, 0.38]
    sc.rect(lid, "Highlight", parent, x, y, w_, h_, c, r=6, ax=0, ay=h_ / 2)
    sc.k(lid, "scaleX", [(0, f(0), LIN), (t, f(0), HOLD), (t + dur, f(100), OUT)])
    return lid


def push_in(sc, gid, t0, t1, s0=100, s1=106, cx=None, cy=None):
    """Slow camera push on a whole group (create the group with ax/ay = the point to push toward).
    Full-screen scenes feel filmed, not slid: 3–6 % over the scene, or a fast 0.6 s push to a detail (to 140–160 %)."""
    keys = [(0, f(s0), LIN)] + ([(t0, f(s0), HOLD)] if t0 > 0 else [])
    scale_keys(sc, gid, keys + [(t1, f(s1), SOFT if (s1 - s0) < 15 else INOUT)])
    return gid


def type_keys(t0, text, cps=22, caret=True, start=0):
    """textContent keys that TYPE `text` from t0 (cps = characters per second) with an optional caret '|'.
    start = characters already on screen at frame 0 (use the first word when typing opens a scene — no blank frame)."""
    keys = [(0, s(text[:start]), LIN)]
    for i in range(start + 1, len(text) + 1):
        keys.append((t0 + int((i - start) * 1000 / cps), s(text[:i] + ("|" if caret and i < len(text) else "")), HOLD))
    return keys


def flap_keys(t0, t1, final, seed=7):
    """Split-flap / slot effect for a BIG spoken amount: digits spin and lock left→right, last one exactly at t1."""
    rng = random.Random(seed)
    keys, n, tt, locked = [(0, s(final), LIN)], len(final), t0, 0
    step = 45
    while tt < t1:
        locked = int(n * (tt - t0) / max(1, t1 - t0))
        txt = "".join(ch if (i < locked or not ch.isdigit()) else str(rng.randint(0, 9)) for i, ch in enumerate(final))
        keys.append((tt, s(txt), HOLD)); tt += step
    keys.append((t1, s(final), HOLD))
    keys[0] = (0, s("".join("0" if ch.isdigit() else ch for ch in final)), LIN)
    return keys
