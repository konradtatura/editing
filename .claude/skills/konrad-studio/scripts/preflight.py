#!/usr/bin/env python3
"""Preflight: check every source BEFORE transcription / cutting (seconds, ffprobe only — nothing is decoded or written
except PROJ/preflight.json). Catches what used to surface only after an hour of rendering.

usage: preflight.py PROJ SRC [SRC ...] [--out-mbps 25] [--copies 2] [--scribe]
  --out-mbps  bitrate of the intermediate CUT you plan to render (CRF 12 slow ≈ 25 Mbit/s)
  --copies    how many full-length copies the cut needs on disk at once (segments + CUT = 2)
  --scribe    also ask ElevenLabs how many Scribe credits are left (one small network request)
exit 0 = OK / warnings only, exit 2 = BLOCKER (fix before cutting).
Checks: video codec/size/fps, variable frame rate, rotation, HDR, audio present + layout, layout/fps/size differences
between sources (the 2026-10-09 garbled-audio case: mono 44.1 kHz + stereo 48 kHz), free disk vs estimate, swap,
available ASR engines.
"""
import glob, json, os, shutil, subprocess, sys, time

PY = "/Library/Frameworks/Python.framework/Versions/3.13/bin/python3"
SCRIBE_ENV = os.path.expanduser("~/Documents/Codex/video-use/.env")


def probe(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                        "format=duration,size:stream=index,codec_type,codec_name,width,height,r_frame_rate,avg_frame_rate,"
                        "pix_fmt,color_transfer,sample_rate,channels,channel_layout:stream_side_data=rotation:stream_tags=rotate",
                        "-of", "json", path], capture_output=True, text=True)
    if r.returncode:
        return None
    return json.loads(r.stdout)


def rate(s):
    try:
        n, d = s.split("/")
        return float(n) / float(d) if float(d) else 0.0
    except (ValueError, AttributeError):
        return 0.0


def check_source(path):
    issues, info = [], {"path": path}
    if not os.path.exists(path):
        return info, [("BLOCK", f"missing file {path}")]
    p = probe(path)
    if p is None:
        return info, [("BLOCK", f"ffprobe cannot read {path}")]
    fmt = p.get("format", {})
    info["duration"] = round(float(fmt.get("duration", 0)), 3)
    info["size_mb"] = round(int(fmt.get("size", 0)) / 1e6, 1)
    vs = [s for s in p["streams"] if s.get("codec_type") == "video"]
    au = [s for s in p["streams"] if s.get("codec_type") == "audio"]
    other = [s for s in p["streams"] if s.get("codec_type") not in ("video", "audio")]
    if not vs:
        issues.append(("BLOCK", "no video stream"))
    else:
        v = vs[0]
        r_, avg = rate(v.get("r_frame_rate")), rate(v.get("avg_frame_rate"))
        rot = 0
        for sd in v.get("side_data_list", []) or []:
            rot = int(sd.get("rotation", 0) or 0)
        rot = rot or int((v.get("tags") or {}).get("rotate", 0) or 0)
        info["video"] = {"codec": v.get("codec_name"), "w": v.get("width"), "h": v.get("height"), "fps": round(r_, 3),
                         "avg_fps": round(avg, 3), "pix_fmt": v.get("pix_fmt"), "transfer": v.get("color_transfer"),
                         "rotation": rot}
        if r_ and avg and abs(r_ - avg) / r_ > 0.005:
            issues.append(("WARN", f"variable frame rate (nominal {r_:.3f}, average {avg:.3f}) — the cut renders at 30 fps; "
                                   "check lip sync on the first preview"))
        if r_ and abs(r_ - 30) > 0.01:
            issues.append(("WARN", f"{r_:.3f} fps, the pipeline renders at 30 fps (cut_takes.FPS) — frames will be dropped/duplicated"))
        if rot:
            issues.append(("WARN", f"rotation {rot}° in metadata — check the contact sheet orientation"))
        if v.get("color_transfer") in ("smpte2084", "arib-std-b67"):
            issues.append(("WARN", f"HDR ({v.get('color_transfer')}) — the pipeline writes bt709 SDR; colours will shift"))
    if not au:
        issues.append(("BLOCK", "no audio stream"))
    else:
        a = au[0]
        info["audio"] = {"codec": a.get("codec_name"), "sample_rate": int(a.get("sample_rate", 0)),
                         "channels": a.get("channels"), "layout": a.get("channel_layout")}
        if len(au) > 1:
            issues.append(("WARN", f"{len(au)} audio streams — the cut uses only the first (0:a:0)"))
    if other:
        info["other_streams"] = [s.get("codec_type") for s in other]          # iPhone adds a data/timecode track: harmless
    return info, issues


def swap():
    r = subprocess.run(["sysctl", "-n", "vm.swapusage"], capture_output=True, text=True).stdout.split()
    try:
        tot, used = float(r[2].rstrip("M")), float(r[5].rstrip("M"))
        return tot, used
    except (IndexError, ValueError):
        return 0.0, 0.0


def asr_engines():
    eng = {}
    mlx = subprocess.run([PY, "-c", "import mlx_whisper"], capture_output=True).returncode == 0
    model = bool(glob.glob(os.path.expanduser("~/.cache/huggingface/hub/models--mlx-community--whisper-large-v3-turbo")))
    eng["mlx_whisper"] = "ok" if mlx and model else ("no model cached (first run downloads it)" if mlx else "missing")
    pk = glob.glob(os.path.expanduser("~/.cache/hyperframes/**/*parakeet*"), recursive=True) + \
        glob.glob(os.path.expanduser("~/.cache/huggingface/hub/*parakeet*"))
    eng["parakeet"] = "ok" if pk else "not installed"
    eng["scribe_key"] = "present" if os.path.exists(SCRIBE_ENV) else "missing"
    return eng


def scribe_credits():
    key = None
    for line in open(SCRIBE_ENV):
        if line.upper().startswith("ELEVEN") and "KEY" in line.split("=")[0].upper():
            key = line.split("=", 1)[1].strip().strip('"').strip("'")
            break
    if not key:
        return None
    r = subprocess.run(["curl", "-s", "-m", "10", "-H", f"xi-api-key: {key}", "https://api.elevenlabs.io/v1/user/subscription"],
                       capture_output=True, text=True)
    try:
        d = json.loads(r.stdout)
        return int(d["character_limit"]) - int(d["character_count"])
    except (ValueError, KeyError, TypeError):
        return None


def main():
    a = sys.argv[1:]
    opt = lambda k, dflt: float(a[a.index(k) + 1]) if k in a else dflt
    mbps, copies = opt("--out-mbps", 25.0), opt("--copies", 2.0)
    want_scribe = "--scribe" in a
    for k in ("--out-mbps", "--copies"):
        if k in a:
            i = a.index(k); del a[i:i + 2]
    a = [x for x in a if x != "--scribe"]
    if len(a) < 2:
        sys.exit(__doc__)
    t0 = time.time()
    proj, srcs = os.path.abspath(a[0]), [os.path.abspath(x) for x in a[1:]]
    os.makedirs(proj, exist_ok=True)
    report, problems = {"sources": [], "checks": {}}, []
    for s in srcs:
        info, iss = check_source(s)
        report["sources"].append(info)
        problems += [(lvl, f"{os.path.basename(s)}: {msg}") for lvl, msg in iss]

    ok = [x for x in report["sources"] if "audio" in x and "video" in x]
    if len(ok) > 1:
        lay = {(x["audio"]["sample_rate"], x["audio"]["channels"]) for x in ok}
        if len(lay) > 1:
            desc = ", ".join(f"{os.path.basename(x['path'])}={x['audio']['sample_rate']} Hz/{x['audio']['channels']} ch" for x in ok)
            problems.append(("WARN", f"sources have different audio layouts ({desc}). cut_takes.py converts every segment "
                                     "to 48 kHz stereo — read the splice audit of the first joins between files"))
        if len({(x["video"]["w"], x["video"]["h"]) for x in ok}) > 1:
            problems.append(("WARN", "sources have different resolutions — framing will jump between files"))
        if len({x["video"]["fps"] for x in ok}) > 1:
            problems.append(("WARN", "sources have different frame rates"))

    total = sum(x.get("duration", 0) for x in report["sources"])
    need_gb = total * mbps / 8 / 1000 * copies + 2.0           # + 2 GB margin for transcripts, scenes, temp files
    free_gb = shutil.disk_usage(proj).free / 1e9
    report["checks"]["disk"] = {"free_gb": round(free_gb, 1), "estimated_need_gb": round(need_gb, 1),
                                "source_minutes": round(total / 60, 1)}
    # the estimate assumes the cut is as long as ALL sources (retakes included) — a ceiling, not the real need:
    # block only when even 40 % of it (or 3 GB) does not fit, warn below the full estimate
    if free_gb < max(3.0, 0.4 * need_gb):
        problems.append(("BLOCK", f"free disk {free_gb:.1f} GB — too little even for a cut of ~40 % of the sources "
                                  f"(full estimate {need_gb:.1f} GB = {total / 60:.1f} min × {mbps:g} Mbit/s × {copies:g} copies + 2 GB)"))
    elif free_gb < need_gb:
        problems.append(("WARN", f"free disk {free_gb:.1f} GB < ceiling estimate {need_gb:.1f} GB — fine for a cut much shorter "
                                 "than the raw files; free space before long renders"))
    elif free_gb < 2 * need_gb:
        problems.append(("WARN", f"free disk {free_gb:.1f} GB is tight (estimated need {need_gb:.1f} GB)"))

    tot, used = swap()
    report["checks"]["swap_mb"] = {"total": tot, "used": used}
    if tot and used / tot > 0.7:
        problems.append(("WARN", f"swap {used:.0f}/{tot:.0f} MB used — close heavy apps (browsers) before long renders"))

    eng = asr_engines()
    scribe_ok = False
    if want_scribe and eng["scribe_key"] == "present":
        c = scribe_credits()
        need = total / 60 * 70                                   # bledy.md: 12 min ≈ 843 credits
        eng["scribe"] = "credits unknown (key lacks user_read permission or no network)" if c is None else (f"ok ({c} credits)" if c >= need else f"quota too low ({c} left, ~{need:.0f} needed)")
        scribe_ok = c is not None and c >= need
    report["checks"]["asr"] = eng
    if eng["parakeet"] != "ok" and eng["mlx_whisper"] != "ok" and not scribe_ok:
        problems.append(("BLOCK", "no transcription engine available"))
    elif eng["parakeet"] != "ok" and not scribe_ok:
        problems.append(("WARN", "no verbatim engine (Parakeet not installed, Scribe "
                                 + (eng.get("scribe") or "not checked — add --scribe") + ") — raw takes will use the slower Whisper fallback"))

    report["problems"] = [{"level": l, "msg": m} for l, m in problems]
    report["seconds"] = round(time.time() - t0, 2)
    json.dump(report, open(os.path.join(proj, "preflight.json"), "w"), indent=1, ensure_ascii=False)

    for x in report["sources"]:
        v, au = x.get("video", {}), x.get("audio", {})
        print(f"{os.path.basename(x['path'])}: {x.get('duration', 0) / 60:.1f} min, {v.get('codec')} {v.get('w')}x{v.get('h')} "
              f"{v.get('fps')} fps, audio {au.get('codec')} {au.get('sample_rate')} Hz {au.get('channels')} ch")
    d = report["checks"]["disk"]
    print(f"disk: {d['free_gb']} GB free, ~{d['estimated_need_gb']} GB needed · ASR: {eng}")
    for l, m in problems:
        print(f"{l}: {m}")
    blocks = sum(1 for l, _ in problems if l == "BLOCK")
    print(f"-- {blocks} blocker(s), {len(problems) - blocks} warning(s), {report['seconds']} s → {proj}/preflight.json")
    sys.exit(2 if blocks else 0)


if __name__ == "__main__":
    main()
