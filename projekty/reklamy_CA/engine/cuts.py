#!/usr/bin/env python3
"""Detect hard cuts (jump cuts) in footage: per-frame diff of a small grey thumbnail, peaks vs local median.
usage: cuts.py VIDEO [--mirror]  -> prints JSON list of cut times (s) = time of first frame of the new shot"""
import json, subprocess, sys
import numpy as np
src = sys.argv[1]; W, H = 64, 112
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", src, "-vf", f"scale={W}:{H},format=gray", "-f", "rawvideo", "-"], capture_output=True).stdout
fps = eval(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v", "-show_entries", "stream=r_frame_rate", "-of", "csv=p=0", src], capture_output=True, text=True).stdout.strip())
a = np.frombuffer(raw, np.uint8).reshape(-1, H, W).astype(np.float32)
d = np.abs(np.diff(a, axis=0)).mean(axis=(1, 2))
cuts = []
for i in range(len(d)):
    lo, hi = max(0, i - 8), min(len(d), i + 9)
    nb = np.concatenate([d[lo:i], d[i + 1:hi]])
    med = np.median(nb) if len(nb) else 0
    if d[i] > 9 and d[i] > 3.2 * med + 3 and d[i] == d[max(0, i - 2):i + 3].max():
        cuts.append(round((i + 1) / fps, 3))
print(json.dumps(cuts))
