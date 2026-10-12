#!/usr/bin/env python3
"""Screen + camera layout (longform): wherever there is a screen recording, the camera shrinks smoothly into a
rounded PiP bottom-right (24 % width, 40 px margin, radius 130 @full size, soft shadow) and the screen fills the frame.

usage: layout_pip.py FILM.mp4 SCREEN.mp4 OUT.mp4 [--until SEC] [--avoid index.json] [--plan]
  FILM   = the edited film (camera, may already contain animations) — gives picture + audio
  SCREEN = screen recording matched to FILM's timeline, BLACK where there is no screen (Konrad exports it like that)
  --avoid  index.json from export.py: never show the screen layout during full-screen animations (they cut over it)
  --plan   only print the detected screen segments
Rules: gaps < 3 s between screen parts are merged (no flicker), parts < 4 s are ignored, morph 0.6 s smoothstep.
"""
import json, os, subprocess, sys
import numpy as np

FPS, WD, HD = 5, 96, 54
K, D, M = 0.24, 0.6, 40


def luma(path, until=None):
    cmd = ["ffmpeg", "-v", "error", "-i", path] + (["-t", str(until)] if until else []) + \
          ["-vf", f"fps={FPS},scale={WD}:{HD},format=gray", "-f", "rawvideo", "-"]
    raw = subprocess.run(cmd, capture_output=True, check=True).stdout
    fr = np.frombuffer(raw, np.uint8).reshape(-1, HD, WD).astype(np.float32)
    return fr.mean(axis=(1, 2)), fr.std(axis=(1, 2))


def segments(screen, until, avoid):
    ll, ls = luma(screen, until)
    on = (ll > 4) | (ls > 3)
    for a_, b_ in avoid:
        on[int(a_ * FPS):int(np.ceil(b_ * FPS))] = False
    runs, i = [], 0
    while i < len(on):
        if on[i]:
            j = i
            while j < len(on) and on[j]:
                j += 1
            runs.append([i, j]); i = j
        else:
            i += 1
    merged = []
    for a_, b_ in runs:
        if merged and a_ - merged[-1][1] < 3 * FPS:
            merged[-1][1] = b_
        else:
            merged.append([a_, b_])
    return [(a_ / FPS, b_ / FPS) for a_, b_ in merged if b_ - a_ >= 4 * FPS]


def main():
    a = sys.argv[1:]
    if len(a) < 3:
        sys.exit(__doc__)
    film, screen, out = a[:3]
    until = float(a[a.index("--until") + 1]) if "--until" in a else None
    avoid = []
    if "--avoid" in a:
        avoid = [(x["in"], x["out"]) for x in json.load(open(a[a.index("--avoid") + 1])) if not x.get("overlay")]
    segs = segments(screen, until, avoid)
    fmt = lambda t: f"{int(t // 60)}:{t % 60:05.2f}"
    print(len(segs), "screen parts,", round(sum(b - a_ for a_, b in segs) / 60, 1), "min")
    for k, (a_, b) in enumerate(segs):
        print(f"{k + 1:3d} {fmt(a_)}–{fmt(b)}  {b - a_:5.1f}s")
    if "--plan" in a or not segs:
        return
    from PIL import Image, ImageDraw, ImageFilter
    W, H = map(int, subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height",
                                    "-of", "csv=p=0", film], capture_output=True, text=True).stdout.strip().split(","))
    R = round(130 * W / 1920)
    work = os.path.splitext(os.path.abspath(out))[0] + "_layout"
    os.makedirs(work, exist_ok=True)
    m = Image.new("L", (W, H), 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, W - 1, H - 1], radius=R, fill=255)
    m.save(os.path.join(work, "mask.png"))
    sh = Image.new("RGBA", (W + 200, H + 200), (0, 0, 0, 0))
    al = Image.new("L", (W + 200, H + 200), 0)
    ImageDraw.Draw(al).rounded_rectangle([100, 100, 100 + W, 100 + H], radius=R, fill=110)
    sh.putalpha(al.filter(ImageFilter.GaussianBlur(45))); sh.save(os.path.join(work, "shadow.png"))
    sm = lambda u: f"(({u})*({u})*(3-2*({u})))"
    terms = [f"{sm(f'clip((t-{a_:.2f})/{D},0,1)')}*{sm(f'clip(({b:.2f}-t)/{D},0,1)')}" for a_, b in segs]
    S = f"(1-{1 - K}*({'+'.join(terms)}))"
    P = f"((1-{S})/{1 - K})"
    TX, TY = W - M - W * K / 2, H - M - H * K / 2
    EN = "gt(" + "+".join(f"between(t,{a_:.2f},{b:.2f})" for a_, b in segs) + ",0)"
    cx, cy = f"({W / 2}+({TX}-{W / 2})*{P})", f"({H / 2}+({TY}-{H / 2})*{P})"
    fc = (f"[0:v]format=yuv420p,split[base][ps];"
          f"[ps][2:v]alphamerge,format=yuva420p,scale=w='2*trunc({W}*{S}/2)':h='2*trunc({H}*{S}/2)':eval=frame[pip];"
          f"[3:v]format=yuva420p,scale=w='2*trunc({W + 200}*{S}/2)':h='2*trunc({H + 200}*{S}/2)':eval=frame[shd];"
          f"[1:v]scale={W}:{H}[scr];[base][scr]overlay=enable='{EN}'[b1];"
          f"[b1][shd]overlay=x='{cx}-overlay_w/2':y='{cy}-overlay_h/2+18*{P}':eval=frame:enable='{EN}'[b2];"
          f"[b2][pip]overlay=x='{cx}-overlay_w/2':y='{cy}-overlay_h/2':eval=frame:enable='{EN}',format=yuv420p[v]")
    fp = os.path.join(work, "filter.txt"); open(fp, "w").write(fc)
    t = ["-t", str(until)] if until else []
    subprocess.run(["ffmpeg", "-v", "error", "-y", *t, "-i", film, *t, "-i", screen,
                    "-loop", "1", "-i", os.path.join(work, "mask.png"), "-loop", "1", "-i", os.path.join(work, "shadow.png"),
                    "-filter_complex_script", fp, "-map", "[v]", "-map", "0:a", "-shortest",
                    "-c:v", "h264_videotoolbox", "-b:v", "16M", "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart", out],
                   check=True)
    print("done", out)


if __name__ == "__main__":
    main()
