#!/usr/bin/env python3
"""Style 2 compositor: graded footage (+per-shot zoom) with b-roll inserts, overlay PNGs on top, end card tail.
usage: compose2.py SPEC.json FRAMES_DIR OUT.mp4 [--preview]
spec: src, dur (total incl. end card), srcDur, cuts, zooms [[t,scale]], zoomCenter, brolls [{t0,t1,file,ss}], grade (ffmpeg filter)"""
import json, os, subprocess, sys
import numpy as np, cv2
a = sys.argv[1:]; spec = json.load(open(a[0])); fdir = a[1]; out = a[2]
W, H, fps = 1080, 1920, spec.get("fps", 30)
N = round(spec["dur"] * fps); NS = round(spec["srcDur"] * fps)
grade = spec.get("grade", "")
zooms = sorted(spec.get("zooms", [])); cx, cy = spec.get("zoomCenter", [0.5, 0.36])
def scale_at(t):
    s = 1.0
    for zt, zs in zooms:
        if zt <= t: s = zs
    return s
def dec(src, ss=0.0, vf=""):
    chain = f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={fps}" + ("," + vf if vf else "")
    return subprocess.Popen(["ffmpeg", "-v", "error", "-ss", f"{ss:.3f}", "-i", src, "-vf", chain, "-f", "rawvideo", "-pix_fmt", "bgr24", "-"], stdout=subprocess.PIPE)
main = dec(spec["src"], 0, grade)
brolls = sorted(spec.get("brolls", []), key=lambda b: b["t0"]); bdec = {}
crf = "23" if "--preview" in a else "17"
enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", str(fps), "-i", "-",
                        "-i", spec["src"], "-map", "0:v", "-map", "1:a", "-af", f"apad,atrim=0:{spec['dur']:.3f}",
                        "-c:v", "libx264", "-preset", "medium", "-crf", crf, "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
                        "-t", f"{spec['dur']:.3f}", "-movflags", "+faststart", out], stdin=subprocess.PIPE)
fsz = W * H * 3; last = np.zeros((H, W, 3), np.uint8)
for f in range(N):
    t = f / fps
    if f < NS:
        buf = main.stdout.read(fsz)
        fr = np.frombuffer(buf, np.uint8).reshape(H, W, 3) if len(buf) == fsz else last
        last = fr
        s = scale_at(t)
        if s > 1.001:
            w, h = W / s, H / s
            x0 = min(max(cx * W - w / 2, 0), W - w); y0 = min(max(cy * H - h / 2, 0), H - h)
            fr = cv2.warpAffine(fr, np.float32([[s, 0, -x0 * s], [0, s, -y0 * s]]), (W, H), flags=cv2.INTER_LINEAR)
    else:
        fr = np.zeros((H, W, 3), np.uint8)
    for k, b in enumerate(brolls):
        if b["t0"] <= t < b["t1"]:
            if k not in bdec: bdec[k] = dec(b["file"], b.get("ss", 0), grade)
            bb = bdec[k].stdout.read(fsz)
            if len(bb) == fsz:
                fr = np.frombuffer(bb, np.uint8).reshape(H, W, 3)
                ks = 1.04 + 0.05 * (t - b["t0"]) / max(.1, b["t1"] - b["t0"])          # slow push-in on b-roll
                fr = cv2.warpAffine(fr, np.float32([[ks, 0, -(ks - 1) * W / 2], [0, ks, -(ks - 1) * H / 2]]), (W, H))
        elif t >= b["t1"] and k in bdec:
            bdec[k].terminate(); bdec[k] = None
    p = os.path.join(fdir, f"f_{f:05d}.png")
    ov = cv2.imread(p, cv2.IMREAD_UNCHANGED) if os.path.exists(p) else None
    if ov is not None:
        al = ov[:, :, 3:4].astype(np.float32) / 255.0 if ov.shape[2] == 4 else np.ones(ov.shape[:2] + (1,), np.float32)
        if al.max() > 0:
            fr = (ov[:, :, :3].astype(np.float32) * al + fr.astype(np.float32) * (1 - al)).astype(np.uint8)
    enc.stdin.write(np.ascontiguousarray(fr).tobytes())
enc.stdin.close(); enc.wait(); main.terminate()
print("wrote", out)
