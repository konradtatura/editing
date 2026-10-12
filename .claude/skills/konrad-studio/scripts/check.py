#!/usr/bin/env python3
"""QA + hand-over helpers.

check.py sheet VIDEO [--n 12 | --times 3.2,10,44.5] [--out sheet.jpg]   contact sheet with timecodes → READ it
check.py loud SRC OUT [OUT2 ...]                                         integrated loudness + true peak (Δ ≤ ±0.5 dB, TP < −1 dBTP)
check.py pauses VIDEO [--min-ms 200]                                     every pause measured from AUDIO (target 100–150 ms)
check.py motion CLIP.mp4 [...] [--still 0.6]                             frozen stretches > 0.6 s + blank (empty) first frames
check.py alpha FILE.mov [...]                                            alpha present? (pix_fmt yuva…)
check.py tel VIDEO [--max-mb 28]                                         phone copy VIDEO_tel.mp4 (< 30 MB for SendUserFile)
"""
import json, os, subprocess, sys


def probe(path, entries):
    return json.loads(subprocess.run(["ffprobe", "-v", "error", "-show_entries", entries, "-of", "json", path],
                                     capture_output=True, text=True).stdout)


def dur(path):
    return float(probe(path, "format=duration")["format"]["duration"])


def sheet(video, times, out):
    from PIL import Image, ImageDraw
    tmp = out + "_f"; os.makedirs(tmp, exist_ok=True)
    ims = []
    for t in times:
        p = os.path.join(tmp, f"{t:.2f}.jpg")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.3f}", "-i", video, "-frames:v", "1", "-q:v", "3", p], check=True)
        ims.append((Image.open(p).convert("RGB"), t))
    w0, h0 = ims[0][0].size
    tw = 480 if w0 >= h0 else 270
    th = round(tw * h0 / w0)
    cols = 4 if w0 >= h0 else 6
    rows = (len(ims) + cols - 1) // cols
    sh = Image.new("RGB", (cols * tw, rows * (th + 20)), (30, 30, 30)); d = ImageDraw.Draw(sh)
    for k, (im, t) in enumerate(ims):
        x, y = (k % cols) * tw, (k // cols) * (th + 20)
        sh.paste(im.resize((tw, th)), (x, y + 20)); d.text((x + 5, y + 4), f"{int(t // 60)}:{t % 60:05.2f}", fill=(255, 255, 255))
    sh.save(out, quality=85)
    print(out)


def loud(path, peak=False):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", path, "-map", "0:a", "-af", "ebur128=peak=true", "-f", "null", "-"],
                       capture_output=True, text=True).stderr
    i_ = tp = None
    for line in r.splitlines():
        t = line.strip()
        if t.startswith("I:"):
            i_ = float(t.split()[1])
        if t.startswith("Peak:"):
            tp = float(t.split()[1])
    return (i_, tp) if peak else i_


def envelope(path, sr=16000):
    import numpy as np
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-map", "0:a:0", "-ac", "1", "-ar", str(sr), "-f", "s16le", "-"],
                         capture_output=True, check=True).stdout
    x = np.frombuffer(raw, np.int16).astype(np.float32) / 32768
    hop = sr // 100; n = len(x) // hop
    return 20 * np.log10(np.sqrt((x[:n * hop].reshape(n, hop) ** 2).mean(1)) + 1e-9)


def pauses(video, min_ms):
    """Konrad's rule: silence between sentences/joins ~100–150 ms, inside a sentence ~80–120 ms. ASR word ends lie."""
    import numpy as np
    db = envelope(video)
    quiet = db < np.percentile(db, 15) + 10
    runs, i = [], 0
    while i < len(quiet):
        if quiet[i]:
            j = i
            while j < len(quiet) and quiet[j]:
                j += 1
            runs.append((i, j)); i = j
        else:
            i += 1
    inner = [(a_, b_) for a_, b_ in runs if a_ > 0 and b_ < len(quiet)]
    long = [(a_, b_) for a_, b_ in inner if (b_ - a_) * 10 >= min_ms]
    for a_, b_ in long:
        print(f"{int(a_ / 6000)}:{a_ / 100 % 60:05.2f}  pause {(b_ - a_) * 10:4d} ms")
    ms = [(b_ - a_) * 10 for a_, b_ in inner if (b_ - a_) * 10 >= 60]
    print(f"-- {len(long)} pauses ≥ {min_ms} ms; median {np.median(ms) if ms else 0:.0f} ms. Shorten each to ~140 ms or keep on purpose.")


def motion(clip, still):
    """Frame-difference at 270 px: report stretches where nothing moves for > `still` s, and a blank opening."""
    import numpy as np
    st = probe(clip, "stream=width,height,r_frame_rate")["streams"][0]
    w = 270 if st["width"] >= st["height"] else 152
    h = round(w * st["height"] / st["width"] / 2) * 2
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", clip, "-vf", f"fps=30,scale={w}:{h},format=gray", "-f", "rawvideo", "-"],
                         capture_output=True, check=True).stdout
    fr = np.frombuffer(raw, np.uint8).reshape(-1, h, w).astype(np.int16)
    diff = np.abs(np.diff(fr, axis=0)).mean(axis=(1, 2))
    moving = diff > 0.08
    runs, i = [], 0
    while i < len(moving):
        if not moving[i]:
            j = i
            while j < len(moving) and not moving[j]:
                j += 1
            if (j - i) / 30 > still:
                runs.append((i / 30, (j - i) / 30))
            i = j
        else:
            i += 1
    blank = fr[0].std() < 3
    name = os.path.basename(clip)
    tail = [r for r in runs if r[0] + r[1] >= len(fr) / 30 - 0.05]
    body = [r for r in runs if r not in tail]
    msg = ", ".join(f"{a_:.2f}s+{d:.2f}" for a_, d in body) or "ok"
    print(f"{name}: still {msg}{'  (end hold ' + f'{tail[0][1]:.2f}s)' if tail else ''}{'  BLANK FIRST FRAME' if blank else ''}")


def main():
    a = sys.argv[1:]
    if not a:
        sys.exit(__doc__)
    cmd = a[0]
    if cmd == "sheet":
        v = a[1]
        if "--times" in a:
            ts = [float(x) for x in a[a.index("--times") + 1].split(",")]
        else:
            n = int(a[a.index("--n") + 1]) if "--n" in a else 12
            D = dur(v); ts = [D * (k + 0.5) / n for k in range(n)]
        out = a[a.index("--out") + 1] if "--out" in a else os.path.splitext(v)[0] + "_sheet.jpg"
        sheet(v, ts, out)
    elif cmd == "loud":
        ref, rtp = loud(a[1], True); print(f"source {ref} LUFS, TP {rtp} dBTP")
        for p in a[2:]:
            l_, tp = loud(p, True)
            flag = "  ← TP > −1" if tp is not None and tp > -1.0 else ""
            print(f"{os.path.basename(p)}: {l_} LUFS (Δ {l_ - ref:+.1f} dB), TP {tp} dBTP{flag}")
    elif cmd == "pauses":
        pauses(a[1], int(a[a.index("--min-ms") + 1]) if "--min-ms" in a else 200)
    elif cmd == "motion":
        still = float(a[a.index("--still") + 1]) if "--still" in a else 0.6
        for p in [x for x in a[1:] if x.endswith((".mp4", ".mov"))]:
            motion(p, still)
    elif cmd == "alpha":
        for p in a[1:]:
            pf = probe(p, "stream=pix_fmt,codec_name")["streams"][0]
            print(f"{os.path.basename(p)}: {pf['codec_name']} {pf['pix_fmt']}  {'OK alpha' if 'a' in pf['pix_fmt'][:4] else 'NO ALPHA'}")
    elif cmd == "tel":
        v = a[1]; mx = float(a[a.index("--max-mb") + 1]) if "--max-mb" in a else 28
        st = probe(v, "stream=width,height")["streams"][0]
        vert = st["height"] > st["width"]
        D = dur(v)
        vb = max(120, int((mx * 8 * 1024 * 0.92) / D - 64))          # kbit/s budget
        out = os.path.splitext(v)[0] + "_tel.mp4"
        final_out, out = out, out[:-4] + ".part.mp4"   # write aside + rename: Video Review keeps old versions as hard links
        sc = ("scale=540:-2" if vert else "scale=960:-2") if D < 240 else ("scale=432:-2" if vert else "scale=720:-2")
        # Apple hardware encoder (2026-10-10): the phone copy was ~1 min per 4 min of film on x264; quality is irrelevant here
        r = subprocess.run(["ffmpeg", "-v", "error", "-y", "-hwaccel", "videotoolbox", "-i", v, "-vf", sc, "-c:v", "h264_videotoolbox",
                            "-b:v", f"{int(vb * 0.9)}k", "-maxrate", f"{vb}k", "-bufsize", f"{2 * vb}k", "-c:a", "aac", "-b:a", "64k",
                            "-movflags", "+faststart", out])
        if r.returncode:                            # no hardware encoder → old x264 path
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", v, "-vf", sc, "-c:v", "libx264", "-preset", "medium", "-crf", "28",
                            "-maxrate", f"{vb}k", "-bufsize", f"{2 * vb}k", "-c:a", "aac", "-b:a", "64k", "-movflags", "+faststart", out], check=True)
        os.replace(out, final_out); out = final_out
        print(out, f"{os.path.getsize(out) / 1e6:.1f} MB")
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
