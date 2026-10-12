#!/usr/bin/env python3
"""Contact sheet: footage frame + overlay PNG for each rendered test frame. usage: sheet.py SPEC FRAMES_DIR OUT.jpg [cols]"""
import json, os, subprocess, sys, glob
import numpy as np, cv2
spec = json.load(open(sys.argv[1])); fd = sys.argv[2]; out = sys.argv[3]; cols = int(sys.argv[4]) if len(sys.argv) > 4 else 5
tiles = []
for p in sorted(glob.glob(os.path.join(fd, "f_*.png"))):
    f = int(os.path.basename(p)[2:7]); t = f / spec.get("fps", 30)
    vf = ("hflip," if spec.get("mirror") else "") + "scale=1080:1920"
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(t), "-i", spec["src"], "-frames:v", "1", "-vf", vf, "-f", "rawvideo", "-pix_fmt", "bgr24", "-"], capture_output=True).stdout
    fr = np.frombuffer(raw, np.uint8).reshape(1920, 1080, 3).astype(np.float32)
    ov = cv2.imread(p, cv2.IMREAD_UNCHANGED).astype(np.float32)
    al = ov[:, :, 3:4] / 255 if ov.shape[2] == 4 else np.ones_like(ov[:, :, :1])
    im = (ov[:, :, :3] * al + fr * (1 - al)).astype(np.uint8)
    im = cv2.resize(im, (360, 640), interpolation=cv2.INTER_AREA)
    cv2.putText(im, f"{t:.1f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, .9, (0, 0, 255), 2)
    tiles.append(im)
while len(tiles) % cols: tiles.append(np.zeros_like(tiles[0]))
rows = [np.hstack(tiles[i:i + cols]) for i in range(0, len(tiles), cols)]
cv2.imwrite(out, np.vstack(rows), [cv2.IMWRITE_JPEG_QUALITY, 85]); print(out)
