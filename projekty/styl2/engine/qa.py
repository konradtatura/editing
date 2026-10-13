#!/usr/bin/env python3
"""QA sheet from a FINAL video: frames just before/after every cut, b-roll edge and overlay start/end.
usage: qa.py SPEC.json FINAL.mp4 OUT_prefix   -> OUT_prefix_1.jpg, _2.jpg ... (pairs: before | after)"""
import json, subprocess, sys
import numpy as np, cv2
spec = json.load(open(sys.argv[1])); vid = sys.argv[2]; pre = sys.argv[3]
ev = [("cut", c) for c in spec.get("cuts", [])]
ev += [("broll+", b["t0"]) for b in spec.get("brolls", [])] + [("broll-", b["t1"]) for b in spec.get("brolls", [])]
ev += [(o["type"] + "+", o["t0"]) for o in spec.get("items", spec.get("scenes", []))] + [(o["type"] + "-", o["t1"]) for o in spec.get("items", spec.get("scenes", [])) if o["t1"] < spec["dur"]]
ev = sorted(ev, key=lambda x: x[1])
def frame(t):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{max(0, t):.3f}", "-i", vid, "-frames:v", "1", "-vf", "scale=180:320", "-f", "rawvideo", "-pix_fmt", "bgr24", "-"], capture_output=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(320, 180, 3).copy() if len(raw) == 180 * 320 * 3 else np.zeros((320, 180, 3), np.uint8)
tiles = []
for name, t in ev:
    a, b = frame(t - 0.067), frame(t + 0.034)
    pair = np.hstack([a, np.full((320, 4, 3), 255, np.uint8), b])
    cv2.putText(pair, f"{name} {t:.2f}", (4, 16), cv2.FONT_HERSHEY_SIMPLEX, .45, (0, 0, 255), 1)
    tiles.append(pair)
cols, rows = 6, 4
for k in range(0, len(tiles), cols * rows):
    ch = tiles[k:k + cols * rows]
    while len(ch) % cols: ch.append(np.zeros_like(tiles[0]))
    cv2.imwrite(f"{pre}_{k // (cols * rows) + 1}.jpg", np.vstack([np.hstack(ch[i:i + cols]) for i in range(0, len(ch), cols)]))
print(len(tiles), "events")
