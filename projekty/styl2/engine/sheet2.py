#!/usr/bin/env python3
"""Contact sheet for style-2 specs: graded footage/b-roll + zoom + overlay PNG at each rendered frame. usage: sheet2.py SPEC FRAMES OUT.jpg [cols]"""
import json, os, subprocess, sys, glob
import numpy as np, cv2
spec = json.load(open(sys.argv[1])); fd = sys.argv[2]; out = sys.argv[3]; cols = int(sys.argv[4]) if len(sys.argv) > 4 else 6
W, H = 1080, 1920
def grab(src, t, grade):
    vf = f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}" + ("," + grade if grade else "")
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", src, "-frames:v", "1", "-vf", vf, "-f", "rawvideo", "-pix_fmt", "bgr24", "-"], capture_output=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(H, W, 3).copy() if len(raw) == W * H * 3 else np.zeros((H, W, 3), np.uint8)
tiles = []
for p in sorted(glob.glob(os.path.join(fd, "f_*.png"))):
    f = int(os.path.basename(p)[2:7]); t = f / spec.get("fps", 30)
    b = next((b for b in spec.get("brolls", []) if b["t0"] <= t < b["t1"]), None)
    if b: fr = grab(b["file"], b.get("ss", 0) + t - b["t0"], spec["grade"])
    elif t < spec["srcDur"]:
        fr = grab(spec["src"], t, spec["grade"]); s = 1.0
        for zt, zs in spec["zooms"]:
            if zt <= t: s = zs
        if s > 1.001:
            cx, cy = spec["zoomCenter"]; w, h = W / s, H / s
            x0 = min(max(cx * W - w / 2, 0), W - w); y0 = min(max(cy * H - h / 2, 0), H - h)
            fr = cv2.warpAffine(fr, np.float32([[s, 0, -x0 * s], [0, s, -y0 * s]]), (W, H))
    else: fr = np.zeros((H, W, 3), np.uint8)
    ov = cv2.imread(p, cv2.IMREAD_UNCHANGED).astype(np.float32)
    al = ov[:, :, 3:4] / 255 if ov.shape[2] == 4 else np.ones_like(ov[:, :, :1])
    im = (ov[:, :, :3] * al + fr.astype(np.float32) * (1 - al)).astype(np.uint8)
    im = cv2.resize(im, (360, 640), interpolation=cv2.INTER_AREA)
    cv2.putText(im, f"{t:.1f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, .9, (0, 0, 255), 2); tiles.append(im)
while len(tiles) % cols: tiles.append(np.zeros_like(tiles[0]))
cv2.imwrite(out, np.vstack([np.hstack(tiles[i:i + cols]) for i in range(0, len(tiles), cols)]), [cv2.IMWRITE_JPEG_QUALITY, 85]); print(out)
