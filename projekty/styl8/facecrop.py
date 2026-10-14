#!/usr/bin/env python3
"""Face-tracked crop for the rounded video card.  usage: facecrop.py IN.mp4 OUT.mp4 W H [face_y=0.42]
Scales the source to width W, detects the face every frame (OpenCV YuNet), smooths the centre (centred moving average,
dead-zone so small head moves don't wobble the frame) and crops a W x H window so the face sits at face_y of the card."""
import subprocess, sys
import numpy as np, cv2
src, out, W, H = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]); fy = float(sys.argv[5]) if len(sys.argv) > 5 else 0.42
cap = cv2.VideoCapture(src); fps = cap.get(cv2.CAP_PROP_FPS)
import os
det = None  # YuNet face detector (opencv_zoo), created on the first frame
frames, cy, cx = [], [], []
while True:
    ok, f = cap.read()
    if not ok: break
    f = cv2.resize(f, (W, int(round(f.shape[0] * W / f.shape[1] / 2)) * 2)); frames.append(f)
    g = cv2.resize(f, None, fx=.4, fy=.4)
    if det is None: det = cv2.FaceDetectorYN.create(os.path.join(os.path.dirname(os.path.abspath(__file__)), "face_yunet.onnx"), "", (g.shape[1], g.shape[0]), 0.6)
    _, d = det.detect(g)
    if d is not None and len(d): x, y, w, h = max(d[:, :4], key=lambda r: r[2] * r[3]); cy.append((y + h / 2) / .4); cx.append((x + w / 2) / .4)
    else: cy.append(np.nan); cx.append(np.nan)
FH = frames[0].shape[0]; cy = np.array(cy)
idx = np.arange(len(cy)); ok = ~np.isnan(cy)
cy = np.interp(idx, idx[ok], cy[ok]) if ok.any() else np.full(len(cy), FH * .4)
k = int(fps * 0.6) | 1; pad = np.pad(cy, k // 2, mode="edge"); cy = np.convolve(pad, np.ones(k) / k, mode="valid")   # smooth ~0.6 s
# dead-zone: follow only when the face drifts > 3% of the card
ys, cur = [], cy[0]
for v in cy:
    if abs(v - cur) > H * .03: cur += (v - cur) - np.sign(v - cur) * H * .03
    ys.append(cur)
top = np.clip(np.array(ys) - fy * H, 0, FH - H).astype(int)
p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", str(fps), "-i", "-",
                      "-i", src, "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-crf", "14", "-preset", "fast", "-c:a", "copy", out], stdin=subprocess.PIPE)
for f, t in zip(frames, top): p.stdin.write(f[t:t + H].tobytes())
p.stdin.close(); p.wait()
print("face found in", int(ok.sum()), "/", len(ok), "frames; crop top range", top.min(), "-", top.max())
