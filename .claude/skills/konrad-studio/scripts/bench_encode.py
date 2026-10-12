#!/usr/bin/env python3
"""Encoding benchmark on a SHORT sample (never a full render): speed, size and quality (VMAF + SSIM vs the source)
for the intermediate-cut encoders, plus the real cut pattern (many short segments, one ffmpeg each, like cut_takes.py).

usage: bench_encode.py SRC OUT_DIR [--at 300] [--dur 20] [--segs 10] [--seg-dur 3.4] [--only name,name] [--keep]
  continuous test: SRC[at : at+dur] → each variant → time, MB, VMAF, SSIM vs a lossless reference cut the same way (~26 MB/s on disk while running)
  segment test:    --segs × --seg-dur pieces spread over SRC, exact cut_takes.py command per variant → total time
Writes OUT_DIR/bench.json + bench.md. Encoded files are deleted after measuring unless --keep (disk is tight).
Run it when nothing else renders: concurrent jobs and heat (fanless MacBook Air) skew the numbers — the report logs
swap and `pmset -g therm` before/after.
"""
import json, os, re, subprocess, sys, time

COMMON = ["-pix_fmt", "yuv420p", "-r", "30", "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709"]
VARIANTS = {   # name: (encoder args, hardware decode)
    "x264_slow_crf12": (["-c:v", "libx264", "-preset", "slow", "-crf", "12"], False),        # today's cut_takes.py
    "x264_fast_crf14": (["-c:v", "libx264", "-preset", "fast", "-crf", "14"], False),
    "x264_veryfast_crf16": (["-c:v", "libx264", "-preset", "veryfast", "-crf", "16"], False),
    "vt_h264_25M": (["-c:v", "h264_videotoolbox", "-b:v", "25M", "-profile:v", "high"], False),
    "vt_h264_25M_hwdec": (["-c:v", "h264_videotoolbox", "-b:v", "25M", "-profile:v", "high"], True),
    "vt_hevc_20M_hwdec": (["-c:v", "hevc_videotoolbox", "-b:v", "20M", "-tag:v", "hvc1"], True),
}


def sysstate():
    sw = subprocess.run(["sysctl", "-n", "vm.swapusage"], capture_output=True, text=True).stdout.strip()
    th = subprocess.run(["pmset", "-g", "therm"], capture_output=True, text=True).stdout.strip().splitlines()
    return {"swap": sw, "therm": [l for l in th if l.strip()][-3:]}


def encode(src, ss, d, out, venc, hw, audio="aac"):
    a = ["ffmpeg", "-nostdin", "-v", "error", "-y"] + (["-hwaccel", "videotoolbox"] if hw else []) + \
        ["-ss", f"{ss:.4f}", "-i", src, "-t", f"{d:.4f}", "-map", "0:v:0", "-map", "0:a:0"]
    if audio == "pcm":                               # identical to cut_takes.py render()
        a += ["-af", f"aresample=48000,apad,atrim=0:{d:.4f},afade=t=in:st=0:d=0.015,afade=t=out:st={d - 0.015:.4f}:d=0.015"]
    a += venc + COMMON + (["-c:a", "pcm_s16le", "-ar", "48000", "-ac", "2"] if audio == "pcm" else ["-c:a", "aac", "-b:a", "256k"]) + [out]
    t0 = time.time()
    r = subprocess.run(a, capture_output=True, text=True)
    return time.time() - t0, (r.stderr.strip()[-300:] if r.returncode else None)


def _cmp(out, ref, off, frames=None, vmaf=True):
    """Compare out vs a LOSSLESS reference made by the same pipeline (same seek, same -r 30), so only encoding loss is
    measured. off > 0 drops `off` leading frames of the output, off < 0 drops reference frames."""
    lim = f":end_frame={frames}" if frames else ""
    fa = f"trim=start_frame={max(0, off)}{lim}"
    fb = f"trim=start_frame={max(0, -off)}{lim}"
    tail = ";[a1][b1]libvmaf=n_subsample=5:n_threads=8;[a2][b2]ssim" if vmaf else ";[a1][b1]ssim;[a2]nullsink;[b2]nullsink"
    fc = f"[0:v]{fa},setpts=PTS-STARTPTS,split[a1][a2];[1:v]{fb},setpts=PTS-STARTPTS,split[b1][b2]" + tail
    r = subprocess.run(["ffmpeg", "-nostdin", "-hide_banner", "-i", out, "-i", ref, "-lavfi", fc, "-f", "null", "-"],
                       capture_output=True, text=True).stderr
    vm = re.search(r"VMAF score: ([\d.]+)", r)
    ss_ = re.search(r"All:([\d.]+)", r)
    return (float(vm.group(1)) if vm else None), (float(ss_.group(1)) if ss_ else None)


def quality(out, ref):
    """Frame alignment from the first 30 frames (SSIM), then VMAF + SSIM over the whole sample."""
    best = max((-1, 0, 1), key=lambda o: _cmp(out, ref, o, frames=30, vmaf=False)[1] or 0)
    vm, s_ = _cmp(out, ref, best)
    return vm, s_, best


def main():
    a = sys.argv[1:]
    if len(a) < 2:
        sys.exit(__doc__)
    opt = lambda k, dflt: type(dflt)(a[a.index(k) + 1]) if k in a else dflt
    src, out = os.path.abspath(a[0]), os.path.abspath(a[1])
    at, dur, nseg, sd = opt("--at", 300.0), opt("--dur", 20.0), opt("--segs", 10), opt("--seg-dur", 3.4)
    only = opt("--only", "")
    names = [n for n in VARIANTS if not only or n in only.split(",")]
    keep = "--keep" in a
    os.makedirs(out, exist_ok=True)
    srcdur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", src],
                                  capture_output=True, text=True).stdout)
    rep = {"src": src, "at": at, "dur": dur, "segs": nseg, "seg_dur": sd, "before": sysstate(), "continuous": {}, "segments": {}}
    ref = os.path.join(out, "ref_lossless.mp4")
    _, err = encode(src, at, dur, ref, ["-c:v", "libx264", "-preset", "ultrafast", "-qp", "0"], False)
    if err:
        sys.exit("reference: " + err)
    for n in names:
        venc, hw = VARIANTS[n]
        f = os.path.join(out, f"c_{n}.mp4")
        t, err = encode(src, at, dur, f, venc, hw)
        if err:
            rep["continuous"][n] = {"error": err}; print(n, "ERROR", err); continue
        mb = os.path.getsize(f) / 1e6
        vm, ss_, off = quality(f, ref)
        rep["continuous"][n] = {"sec": round(t, 1), "x_realtime": round(dur / t, 2), "mb": round(mb, 1),
                                "mbit_s": round(mb * 8 / dur, 1), "vmaf": vm, "ssim": ss_, "frame_offset": off}
        print(n, rep["continuous"][n], flush=True)
        if not keep:
            os.remove(f)
    os.remove(ref)
    starts = [srcdur * (i + 0.5) / nseg for i in range(nseg)]
    for n in names:
        venc, hw = VARIANTS[n]
        tot, errs = 0.0, None
        for i, s0 in enumerate(starts):
            f = os.path.join(out, f"s_{n}_{i:02d}.mov")
            t, err = encode(src, s0, sd, f, venc, hw, audio="pcm")
            tot += t; errs = errs or err
            if not keep and os.path.exists(f):
                os.remove(f)
        rep["segments"][n] = {"error": errs} if errs else {"sec": round(tot, 1), "x_realtime": round(nseg * sd / tot, 2)}
        print("segments", n, rep["segments"][n], flush=True)
    rep["after"] = sysstate()
    json.dump(rep, open(os.path.join(out, "bench.json"), "w"), indent=1)
    base = rep["segments"].get("x264_slow_crf12", {}).get("sec")
    lines = ["| wariant | ciągły: czas | × realtime | MB | Mbit/s | VMAF | SSIM | segmenty: czas | vs dziś |",
             "|---|---|---|---|---|---|---|---|---|"]
    for n in names:
        c, s = rep["continuous"].get(n, {}), rep["segments"].get(n, {})
        rel = f"{base / s['sec']:.1f}× szybciej" if base and s.get("sec") else "—"
        lines.append(f"| {n} | {c.get('sec', 'ERR')} s | {c.get('x_realtime', '')} | {c.get('mb', '')} | {c.get('mbit_s', '')} | "
                     f"{c.get('vmaf', '')} | {c.get('ssim', '')} | {s.get('sec', 'ERR')} s | {rel} |")
    open(os.path.join(out, "bench.md"), "w").write("\n".join(lines) + f"\n\nprzed: {rep['before']}\npo: {rep['after']}\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
