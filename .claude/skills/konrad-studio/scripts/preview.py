#!/usr/bin/env python3
"""Render still frames of built scenes and tile them into one contact sheet you can READ.

usage: preview.py PROJECT_DIR NAME:sec [NAME:sec ...]          specific moments (sec = scene-local time)
       preview.py PROJECT_DIR --auto 0.3 0.7 0.95 [--only S0]   every project at fractions of its length
writes PROJECT_DIR/checks/<name>_<t>.png and PROJECT_DIR/checks/sheet.jpg (4 per row).
Always look at the sheet before delivering: empty frames, text on the face, clipped text, typos, overlaps.
"""
import glob, json, os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from apple import TSRCT, ENV


def main():
    a = sys.argv[1:]
    if len(a) < 2:
        sys.exit(__doc__)
    root, a = os.path.abspath(a[0]), a[1:]
    only = a[a.index("--only") + 1] if "--only" in a else ""
    if "--only" in a:
        i = a.index("--only"); del a[i:i + 2]
    jobs = []
    if a[0] == "--auto":
        fr = [float(x) for x in a[1:]]
        for p in sorted(glob.glob(os.path.join(root, "projects", "*.tsrct"))):
            name = os.path.basename(p)[:-6]
            if only and not name.startswith(only):
                continue
            ej = os.path.join(root, ".work", f"{name}_editable.json")
            dur = json.load(open(ej))["duration"] if os.path.exists(ej) else 4.0
            jobs += [(name, f"{dur * x:.2f}") for x in fr]
    else:
        jobs = [tuple(x.rsplit(":", 1)) for x in a]
    os.makedirs(os.path.join(root, "checks"), exist_ok=True)
    pngs = []
    for name, t in jobs:
        png = os.path.join(root, "checks", f"{name}_{t}.png")
        r = subprocess.run([TSRCT, "preview", "--project", os.path.join(root, "projects", f"{name}.tsrct"),
                            "--time", t, "--output", png], env=ENV, capture_output=True, text=True)
        if r.returncode == 0:
            pngs.append((png, f"{name} @{t}"))
        else:
            print(f"FAIL {name}:{t} {r.stderr[-300:]}")
    if not pngs:
        return
    from PIL import Image, ImageDraw
    ims = [Image.open(p).convert("RGB") for p, _ in pngs]
    w0, h0 = ims[0].size
    tw = 480 if w0 >= h0 else 270
    th = round(tw * h0 / w0)
    cols = min(4, len(ims))
    rows = (len(ims) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * tw, rows * (th + 22)), (40, 40, 40))
    d = ImageDraw.Draw(sheet)
    for k, (im, (_, lab)) in enumerate(zip(ims, pngs)):
        x, y = (k % cols) * tw, (k // cols) * (th + 22)
        sheet.paste(im.resize((tw, th)), (x, y + 22))
        d.text((x + 6, y + 5), lab, fill=(255, 255, 255))
    out = os.path.join(root, "checks", "sheet.jpg")
    sheet.save(out, quality=85)
    print(out)


if __name__ == "__main__":
    main()
