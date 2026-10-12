#!/usr/bin/env python3
"""Export built scenes as separate deliverables (+ optionally assemble the whole film).

usage: export.py SCENES.py [KEY ...] [--full OUT.mp4] [--no-export]
  SCENES.py must define: BUILD {key: fn -> Scene}, OVERLAY set, SRC (the film the scenes sit on) and call apple.init().
  Project dir = PROJECT env var or the folder of SCENES.py.
Writes PROJECT/Animacje/:
  overlay (card over footage):  KEY_od-M-SS-mmm_Label_MIX.mp4  (+ _NAKLADKA.mov = ProRes 4444 alpha, card only)
  full screen:                  KEY_od-M-SS-mmm_Label_BROLL.mp4
  every MP4 carries the original audio of its range. PROJECT/index.json lists in/out/file.
--full: overlays every exported MP4 on SRC at its in-point (hard cuts, audio from SRC) and checks loudness.
"""
import contextlib, importlib.util, io, json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)


def stamp(t):
    m, s_ = divmod(t, 60)
    return f"{int(m)}-{int(s_):02d}-{int(round((s_ % 1) * 1000)):03d}"


def lufs(path):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", path, "-map", "0:a", "-af", "ebur128", "-f", "null", "-"],
                       capture_output=True, text=True).stderr
    for line in reversed(r.splitlines()):
        if line.strip().startswith("I:"):
            return float(line.split()[1])
    return None


def main():
    a = sys.argv[1:]
    if not a:
        sys.exit(__doc__)
    path = os.path.abspath(a.pop(0))
    full = None
    if "--full" in a:
        i = a.index("--full"); full = os.path.abspath(a[i + 1]); del a[i:i + 2]
    skip = "--no-export" in a
    a = [x for x in a if x != "--no-export"]
    os.environ.setdefault("PROJECT", os.path.dirname(path))
    spec = importlib.util.spec_from_file_location("scenes", path)
    M = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(M)
    import apple
    run = lambda *x: subprocess.run([apple.TSRCT, *x], check=True, env=apple.ENV, capture_output=True, text=True)
    root = apple.ROOT
    out = os.path.join(root, "Animacje")
    os.makedirs(out, exist_ok=True)
    idx_p = os.path.join(root, "index.json")
    index = {it["key"]: it for it in (json.load(open(idx_p)) if os.path.exists(idx_p) else [])}
    for key in (a or sorted(M.BUILD)):
        with contextlib.redirect_stdout(io.StringIO()):
            sc = M.BUILD[key]()
        label = sc.name.split("_", 1)[1] if "_" in sc.name else sc.name
        base = os.path.join(out, f"{key}_od-{stamp(sc.in_s)}_{label}")
        proj = os.path.join(root, "projects", f"{sc.name}.tsrct")
        if not os.path.exists(proj):
            print(f"[{key}] not built (run the scenes file first)"); continue
        ov = key in getattr(M, "OVERLAY", set())
        mp4 = base + ("_MIX.mp4" if ov else "_BROLL.mp4")
        if not skip:
            run("export", "--project", proj, "--output", mp4)
            if ov:
                run("export", "--project", proj, "--output", base + "_NAKLADKA.mov", "--format", "prores", "--fx-solo", "main:100")
            print("exported", os.path.basename(base), "NAKLADKA" if ov else "BROLL", flush=True)
        index[key] = {"key": key, "in": sc.in_s, "out": sc.out_s, "file": mp4, "overlay": ov}
    items = sorted(index.values(), key=lambda x: x["in"])
    json.dump(items, open(idx_p, "w"), indent=1)
    if not full:
        return
    args = ["ffmpeg", "-v", "error", "-y", "-i", M.SRC]
    fc, last = [], "0:v"
    for n, it in enumerate(items, start=1):
        args += ["-itsoffset", f"{it['in']:.3f}", "-i", it["file"]]
        # tpad: clips are frame-quantised (end ≤1 frame early) — hold the last frame so back-to-back clips never show the camera
        fc.append(f"[{n}:v]tpad=stop_mode=clone:stop_duration=0.5[c{n}];[{last}][c{n}]overlay=enable='between(t,{it['in']:.3f},{it['out'] - 0.001:.3f})':eof_action=pass[v{n}]")
        last = f"v{n}"
    args += ["-filter_complex", ";".join(fc), "-map", f"[{last}]", "-map", "0:a", "-c:v", "libx264", "-preset", "medium",
             "-crf", "16", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart", full]
    subprocess.run(args, check=True)
    print(f"full → {full}   loudness src {lufs(M.SRC)} LUFS / full {lufs(full)} LUFS")


if __name__ == "__main__":
    main()
