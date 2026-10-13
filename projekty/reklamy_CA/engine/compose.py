#!/usr/bin/env python3
"""Footage (+zoom punch-ins, optional mirror) + overlay PNG frames -> final mp4 with the original audio.

usage: compose.py SPEC.json FRAMES_DIR OUT.mp4 [--from S --to S] [--preview]
Zoom: spec["zooms"] = [[t, scale], ...] hard punch at each t; after a plansza ends the face settles 1.07->1.0 in 0.35 s.
"""
import json, os, subprocess, sys
import numpy as np, cv2

a = sys.argv[1:]
spec = json.load(open(a[0])); fdir = a[1]; out = a[2]
opt = lambda k, d=None: a[a.index(k) + 1] if k in a else d
fps = spec.get("fps", 30); W, H = 1080, 1920
t_from = float(opt("--from", 0)); t_to = float(opt("--to", spec["dur"]))
f0, f1 = round(t_from * fps), round(t_to * fps)
zooms = sorted(spec.get("zooms", [])); settles = [s["t1"] for s in spec["scenes"]]
cx, cy = spec.get("zoomCenter", [0.5, 0.36])


def scale_at(t):
    s = 1.0
    for zt, zs in zooms:
        if zt <= t: s = zs
    return s


src = spec["src"]
vf = "hflip," if spec.get("mirror") else ""
dec = subprocess.Popen(["ffmpeg", "-v", "error", "-ss", str(t_from), "-i", src, "-t", str(t_to - t_from),
                        "-vf", f"{vf}scale={W}:{H},fps={fps}", "-f", "rawvideo", "-pix_fmt", "bgr24", "-"], stdout=subprocess.PIPE)
crf = "23" if "--preview" in a else "17"
enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", str(fps), "-i", "-",
                        "-ss", str(t_from), "-t", str(t_to - t_from), "-i", src, "-map", "0:v", "-map", "1:a",
                        "-c:v", "libx264", "-preset", "medium", "-crf", crf, "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
                        "-movflags", "+faststart", "-shortest", out], stdin=subprocess.PIPE)
fsz = W * H * 3
for f in range(f0, f1):
    buf = dec.stdout.read(fsz)
    if len(buf) < fsz: break
    fr = np.frombuffer(buf, np.uint8).reshape(H, W, 3)
    t = f / fps; s = scale_at(t)
    if s > 1.001:
        w, h = W / s, H / s
        x0 = min(max(cx * W - w / 2, 0), W - w); y0 = min(max(cy * H - h / 2, 0), H - h)
        M = np.float32([[s, 0, -x0 * s], [0, s, -y0 * s]])
        fr = cv2.warpAffine(fr, M, (W, H), flags=cv2.INTER_LINEAR)
    p = os.path.join(fdir, f"f_{f:05d}.png")
    ov = cv2.imread(p, cv2.IMREAD_UNCHANGED) if os.path.exists(p) else None
    if ov is not None:
        al = ov[:, :, 3:4].astype(np.float32) / 255.0 if ov.shape[2] == 4 else np.ones(ov.shape[:2] + (1,), np.float32)
        if al.max() > 0:
            fr = (ov[:, :, :3].astype(np.float32) * al + fr.astype(np.float32) * (1 - al)).astype(np.uint8)
    enc.stdin.write(np.ascontiguousarray(fr).tobytes())
enc.stdin.close(); enc.wait(); dec.terminate()
print("wrote", out)
