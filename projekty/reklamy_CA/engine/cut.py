#!/usr/bin/env python3
"""Cut raw takes into a tight edit.
usage: cut.py TAKES.json OUT.mp4 [--preview]
TAKES.json = {"src": "raw.mp4", "takes": [[s, e], ...]}   (s = start of first word, e = end of last word, seconds)
Edges are snapped to the audio envelope (30–60 ms before the first sound, 60 ms after the last),
silences > 0.28 s inside a take are shortened to 0.13 s. Writes OUT.mp4 and OUT.edl.json (src ranges in output order).
"""
import json, subprocess, sys
import numpy as np

a = sys.argv[1:]; cfg = json.load(open(a[0])); out = a[1]
src = cfg["src"]; SR = 16000; HOP = 0.01
pcm = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", src, "-ac", "1", "-ar", str(SR), "-f", "s16le", "-"],
                                   capture_output=True).stdout, np.int16).astype(np.float32) / 32768
h = int(HOP * SR)
db = 20 * np.log10(np.sqrt(np.convolve(pcm ** 2, np.ones(h) / h, "same")[::h] + 1e-12))
thr = max(np.percentile(db, 10) + 12, -45)
on = db > thr
idx = lambda t: int(round(t / HOP))


def snap(s, e):
    i0, i1 = idx(s - 0.25), idx(s + 0.12)
    st = next((i for i in range(max(0, i0), min(len(on), i1)) if on[i]), idx(s)) * HOP - 0.05
    j0, j1 = idx(e - 0.12), idx(e + 0.3)
    en = (max([i for i in range(max(0, j0), min(len(on), j1)) if on[i]] or [idx(e)]) + 1) * HOP + 0.06
    return max(0.0, st), en


ranges = []
for tk in cfg["takes"]:
    s, e = tk[0], tk[1]
    st, en = snap(s, e)
    if len(tk) > 2 and "x" in tk[2]: st = s - 0.02          # exact start, no snapping (word glued to a previous one)
    if len(tk) > 2 and "y" in tk[2]:                          # end no later than e (next take glued right after)
        en = (max([i for i in range(max(0, idx(e) - 40), min(len(on), idx(e) + 1)) if on[i]] or [idx(e)]) + 1) * HOP + 0.05
    # split on long internal silences
    cur = st; i = idx(st); end_i = idx(en); run0 = None
    while i < end_i:
        if not on[i]:
            if run0 is None: run0 = i
        else:
            if run0 is not None and (i - run0) * HOP > 0.28:
                ranges.append([cur, run0 * HOP + 0.065]); cur = i * HOP - 0.065
            run0 = None
        i += 1
    ranges.append([cur, en])
ranges = [[round(x, 3), round(y, 3)] for x, y in ranges if y - x > 0.08]

import os, tempfile
n = len(ranges); crf = "26" if "--preview" in a else "15"
tmp = tempfile.mkdtemp(prefix="cut_", dir=os.path.dirname(os.path.abspath(out)))
lst = []
for k, (s, e) in enumerate(ranges):
    d = e - s; seg = os.path.join(tmp, f"s{k:03d}.mkv")
    o0 = min(2, s)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{max(0, s - 2):.3f}", "-i", src,
                    "-vf", f"trim=start={o0:.3f}:duration={d:.3f},setpts=PTS-STARTPTS,scale=1080:1920,fps=30,setsar=1",
                    "-af", f"atrim=start={o0:.3f}:duration={d:.3f},asetpts=PTS-STARTPTS,afade=t=in:d=0.02,afade=t=out:st={max(0, d - 0.025):.3f}:d=0.025",
                    "-c:v", "libx264", "-preset", "medium", "-crf", crf, "-pix_fmt", "yuv420p", "-c:a", "pcm_s16le", "-ar", "48000", seg], check=True)
    lst.append(f"file '{seg}'")
open(os.path.join(tmp, "list.txt"), "w").write("\n".join(lst))
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", os.path.join(tmp, "list.txt"), "-c:v", "copy",
                "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", out], check=True)
t, edl = 0.0, []
for s, e in ranges:
    edl.append({"src": [s, e], "t": round(t, 3)}); t += e - s
json.dump({"src": src, "ranges": edl, "dur": round(t, 3)}, open(out + ".edl.json", "w"), indent=0)
print(f"{n} ranges, {t:.2f} s -> {out}")
