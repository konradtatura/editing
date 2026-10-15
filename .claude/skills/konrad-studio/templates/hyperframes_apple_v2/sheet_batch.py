"""Contact sheet of a batch: one frame per scene (K over the real CUT frame), labelled — what Konrad approves."""
import json, subprocess, sys, os
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, "out", "tmp"); os.makedirs(OUT, exist_ok=True)
keys = sys.argv[2:]; dst = sys.argv[1]
SC = json.load(open(os.path.join(HERE, "scenes.json")))
F = ImageFont.truetype(os.path.join(HERE, "fonts", "Inter-Bold.otf"), 26)
W, H, cols = 640, 360, 4
rows = (len(keys) + cols - 1) // cols
sheet = Image.new("RGB", (cols * W + (cols + 1) * 16, rows * (H + 50) + 16), "white")
for n, k in enumerate(keys):
    a, b, m = SC[k]; p = 0.9; t = (b - a) * p
    fr = os.path.join(OUT, f"sh_{k}.png"); ext = "mov" if m == "K" else "mp4"
    src = os.path.join(HERE, "out", f"{k}_draft.{ext}")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.2f}", "-i", src, "-frames:v", "1", os.path.join(OUT, "f.png")], check=True)
    if m == "K":
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{a + t:.2f}", "-i", os.path.join(HERE, "..", "CUT.mp4"), "-i", os.path.join(OUT, "f.png"),
                        "-filter_complex", "[0:v][1:v]overlay", "-frames:v", "1", fr], check=True)
    else:
        os.replace(os.path.join(OUT, "f.png"), fr)
    im = Image.open(fr).convert("RGB").resize((W, H))
    x = 16 + (n % cols) * (W + 16); y = 16 + (n // cols) * (H + 50)
    sheet.paste(im, (x, y)); ImageDraw.Draw(sheet).rectangle([x, y, x + W - 1, y + H - 1], outline="#d2d2d7")
    mm = int(a // 60); ss = int(a % 60)
    ImageDraw.Draw(sheet).text((x, y + H + 10), f"{k[1:]}  ·  {mm}:{ss:02d}  ·  {'karta/ściana' if m == 'K' else 'pełny ekran'}", font=F, fill="#1d1d1f")
sheet.save(dst, quality=88); print(dst, sheet.size)
