# Longform face-first re-edit, card builder (YT_Ciezka-praca, 2026-10-04). Copy into the project, adjust paths/boxes.
#!/usr/bin/env python3
"""v2 cards: full-screen b-rolls turned into floating cards on the left wall (beside Konrad's head).
For each key in reedit.json "crop": cut the window out of the b-roll, crop the content box, round the corners, add a soft
shadow, slide/fade in and fade out → Animacje_v2/KEY_KARTA.mov (ProRes 4444 alpha, window length, starts at window in).
Usage: cards_v2.py [KEY ...]"""
import json, os, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
R = json.load(open(os.path.join(HERE, "edit", "reedit.json")))
IDX = {i["key"]: i for i in json.load(open(os.path.join(HERE, "index.json")))}
OUT = os.path.join(HERE, "Animacje_v2"); os.makedirs(OUT, exist_ok=True)
TMP = os.path.join(HERE, "edit", "cards_tmp"); os.makedirs(TMP, exist_ok=True)
BOX_CX, BOX_CY, MAX_W, MAX_H = 405, 540, 700, 800     # left wall, clear of the head (head starts ≈ x 800)
RAD, SH_A, SH_BLUR, SH_DY = 40, 0.20, 34, 18


def main(keys):
    for k in keys:
        x0, y0, x1, y1 = R["crop"][k]
        a, b = R["card"][k]
        it = IDX[k]
        cw, ch = x1 - x0, y1 - y0
        s = min(MAX_W / cw, MAX_H / ch)
        w, h = int(round(cw * s / 2)) * 2, int(round(ch * s / 2)) * 2
        X, Y = int(BOX_CX - w / 2), int(BOX_CY - h / 2)
        # rounded mask + shadow as full-frame PNGs
        m = Image.new("L", (w * 4, h * 4), 0)
        rad = R.get("crop_r", {}).get(k, RAD / s) * s       # phone-shaped crops keep the phone's own corner radius
        ImageDraw.Draw(m).rounded_rectangle([0, 0, w * 4 - 1, h * 4 - 1], rad * 4, fill=255)
        m = m.resize((w, h), Image.LANCZOS)
        mp = os.path.join(TMP, f"{k}_mask.png"); m.save(mp)
        sh = Image.new("L", (1920, 1080), 0); sh.paste(m, (X, Y + SH_DY))
        sh = sh.filter(ImageFilter.GaussianBlur(SH_BLUR))
        sh = Image.merge("RGBA", [Image.new("L", (1920, 1080), 0)] * 3 + [sh.point(lambda v: int(v * SH_A))])
        shp = os.path.join(TMP, f"{k}_shadow.png"); sh.save(shp)
        d = b - a
        out = os.path.join(OUT, f"{k}_KARTA.mov")
        # slide 26 px up + fade in (0.24 s), fade out (0.26 s); paper outside the content box is the card itself
        fc = (f"[0:v]crop={cw}:{ch}:{x0}:{y0},scale={w}:{h}:flags=lanczos,format=rgba[c];"
              f"[1:v]format=gray[m];[c][m]alphamerge[cm];"
              f"color=c=black@0:s=1920x1080:r=30:d={d:.3f},format=rgba[bg];"
              f"[2:v]format=rgba,loop=-1:1:0,trim=duration={d:.3f}[sh];"
              f"[bg][sh]overlay=0:0:format=auto[b1];"
              f"[b1][cm]overlay=x={X}:y='{Y}+26*max(0,1-t/0.34)^2':eval=frame:format=auto,"
              f"fade=t=in:st=0:d=0.24:alpha=1,fade=t=out:st={d - 0.26:.3f}:d=0.26:alpha=1[o]")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{a - it['in']:.3f}", "-t", f"{d:.3f}", "-i", it["file"],
                        "-loop", "1", "-i", mp, "-loop", "1", "-i", shp, "-filter_complex", fc, "-map", "[o]",
                        "-t", f"{d:.3f}", "-c:v", "prores_ks", "-profile:v", "4444", "-pix_fmt", "yuva444p10le", out],
                       check=True)
        print(f"{k}: {w}×{h} at ({X},{Y}), scale {s:.2f}, {d:.1f} s → {os.path.basename(out)}", flush=True)


if __name__ == "__main__":
    main(sys.argv[1:] or list(R["crop"]))
