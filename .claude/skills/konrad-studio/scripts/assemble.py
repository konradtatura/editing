#!/usr/bin/env python3
"""Final assembly by SEGMENTS: fixing one animation re-renders only the frames it covers, not the whole film.

usage: assemble.py PROJ (--scenes anim/scenes.json | --index index.json [--reedit edit/reedit.json]) --out OUT.mp4
                   [--base CUT.mp4] [--sfx SFX.wav] [--settle 0.3] [--zooms auto [--zoom 114] [--words tr/cut.json]
                   [--joins edit/joins.json]] [--audio plain|comp] [--upto SEC] [--profile x264|vt] [--jobs 2]
                   [--bez-sfx] [--no-master] [--cache DIR]
  --scenes  HyperFrames projects: {"S01": [in, out, "K"|"B"]}, clips anim/out/S01.mov (K = card with alpha) / .mp4 (B)
  --index   Tesseract projects (export.py index.json): overlay → *_NAKLADKA.mov card (or the _MIX.mp4), else *_BROLL.mp4
  --settle  0.3 s ease-out zoom 105 → 100 % on the face right after every full-screen scene (as in „Skupienie”)
  --reedit  face-first re-edit (YT_Ciezka-praca v2): {"full": {key: [in, out]}, "card": {key: [in, out]}} windows over the
            index.json clips — b-roll trimmed to its window, cards from Animacje_v2/<key>_KARTA.mov or the NAKLADKA with
            0.22 s alpha fade-in / 0.26 s fade-out when the window cuts into the clip
  --zooms auto  Iman-style jump zooms on the face: every face stretch (outside full-screen b-roll) is split at sentence
            starts (≥ 2.2 s apart) or joins (≥ 5.5 s), alternate pieces are shown at --zoom % (default 114, eyes kept
            high: crop y = 35 %), never under a card — the same rule and picture as final_v2.py
  --audio   plain (default, „Skupienie”): voice −14 LUFS, then + SFX through a limiter
            comp  („Ciężka praca” v2): highpass + compressor, voice+SFX mixed THEN −14 LUFS
  --bez-sfx also writes OUT_bez-sfx.mp4 (same picture, voice only — stream copy, seconds)
How it works (same picture as the old one-pass final*.py; layers stack in order of their in-point like its overlay chain):
  1. Every layer becomes a frame window [ceil(in·30), floor((out−1 ms)·30)] on the base (CUT) — exactly the frames the old
     `overlay=enable='between(t,in,out−0.001)'` touched; clip frame j lands on base frame ⌊i − 30·in⌋ like setpts=+in.
  2. The film is split at every window edge; each piece = base frames + the layers active on it → one small ffmpeg job,
     cached in PROJ/cache/final/<profile>/<hash>.mp4 (hash = base, frames, layer files+offsets, settings).
  3. Pieces are concatenated without re-encoding; the voice (−14 LUFS, measured once on the base, cached) + SFX are mixed
     once and muxed — sound and picture share one timeline, so a fixed animation cannot shift the sync.
  Interrupted? Run it again: finished pieces are kept (written atomically), only missing ones are rendered.
  Timings of every run → PROJ/cache/final/runs.jsonl.
"""
import hashlib, json, math, os, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor

FPS = 30
ASM_V = "asm-2"          # bump when piece filters change → cached pieces re-render (sound has its own cache key)
PROFILES = {   # final picture encoders (one per film: pieces are concatenated without re-encoding)
    "x264": ["-c:v", "libx264", "-preset", "slow", "-crf", "16"],          # identical settings to the old final*.py
    "vt": ["-c:v", "h264_videotoolbox", "-b:v", "20M", "-profile:v", "high"],
}
SETTLE = "trunc(1920*(1.05-0.05*(1-pow(1-({T})/{D},3)))/2)*2"


def probe_dur(p):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p],
                                capture_output=True, text=True).stdout)


def stat_key(p):
    """Identity of a file for the cache: the real file behind links + size + modification time (a re-rendered animation
    gets a new mtime → its pieces re-render; moving/linking the project does not)."""
    rp = os.path.realpath(p); st = os.stat(rp)
    return f"{os.path.basename(rp)}|{st.st_size}|{st.st_mtime_ns}"


def f_in(a):
    return math.ceil(a * FPS - 1e-6)


def f_out(b):                                       # exclusive end frame
    return math.floor((b - 0.001) * FPS + 1e-6) + 1


def layers_from_scenes(proj, path, settle, base_dur):
    sc = json.load(open(path)); out_dir = os.path.join(os.path.dirname(path), "out")
    items = []
    for k, (a, b, m) in sc.items():
        f = os.path.join(out_dir, f"{k}.{'mov' if m == 'K' else 'mp4'}")
        if os.path.exists(f):
            items.append({"key": k, "kind": "card" if m == "K" else "broll", "a": a, "b": b, "file": f})
        else:
            print(f"⚠ {k}: {f} not rendered — skipped")
    return add_settles(sorted(items, key=lambda x: x["a"]), settle, base_dur)


def layers_from_index(proj, path, settle, base_dur):
    items = []
    for it in json.load(open(path)):
        f = it["file"]
        if it.get("overlay"):
            mov = f.replace("_MIX.mp4", "_NAKLADKA.mov")
            items.append({"key": it["key"], "kind": "card" if os.path.exists(mov) else "broll", "a": it["in"], "b": it["out"],
                          "file": mov if os.path.exists(mov) else f})
        else:
            items.append({"key": it["key"], "kind": "broll", "a": it["in"], "b": it["out"], "file": f})
    return add_settles(sorted(items, key=lambda x: x["a"]), settle, base_dur)


def layers_from_reedit(proj, reedit, index):
    """final_v2.py windows: b-roll trimmed to its window (clip offset = window in − clip in), cards converted to
    <key>_KARTA.mov (start at the window) or the original NAKLADKA trimmed with alpha fades."""
    R = json.load(open(reedit)); IDX = {i["key"]: i for i in json.load(open(index))}
    items = []
    for k, (a, b) in R["card"].items():
        conv = os.path.join(proj, "Animacje_v2", f"{k}_KARTA.mov")
        if os.path.exists(conv):
            items.append({"key": k, "kind": "card", "a": a, "b": b, "file": conv, "hold": False})
        else:
            it = IDX[k]
            items.append({"key": k, "kind": "card", "a": a, "b": b, "file": it["file"].replace("_MIX.mp4", "_NAKLADKA.mov"),
                          "clip_in": a - it["in"], "fade_in": 0.22 if a - it["in"] > 0.05 else 0,
                          "fade_out": 0.26 if it["out"] - b > 0.05 else 0, "hold": False})   # final_v2: cards not held
    for k, (a, b) in R["full"].items():
        it = IDX[k]
        items.append({"key": k, "kind": "broll", "a": a, "b": b, "file": it["file"], "clip_in": a - it["in"]})
    return sorted(items, key=lambda x: x["a"])


def plan_zooms(layers, D, sent, joins, scale, cy):
    """Exact port of final_v2.py's zoom plan: alternate 100 % / zoom over face stretches, cut at sentence starts and
    joins, cards always on the wide shot."""
    full = sorted((L["a"], L["b"]) for L in layers if L["kind"] == "broll")
    cards = sorted((L["a"], L["b"]) for L in layers if L["kind"] == "card")
    face, t = [], 0.0
    for a, b in full:
        if a - t > 0.05:
            face.append((t, a))
        t = b
    if D - t > 0.05:
        face.append((t, D))
    in_card = lambda x: any(a - 0.25 <= x <= b + 0.25 for a, b in cards)
    zoomed, level = [], 0
    for fs, fe in face:
        cands = sorted(set([round(x, 3) for x in sent if fs + 2.0 < x < fe - 1.6] + [round(x, 3) for x in joins if fs + 2.0 < x < fe - 1.6]))
        cuts, last = [fs], fs
        for p in cands:
            if in_card(p):
                continue
            if (p in sent and p - last >= 2.2) or p - last >= 5.5:
                cuts.append(p); last = p
        cuts.append(fe)
        for i in range(len(cuts) - 1):
            a, b = cuts[i], cuts[i + 1]
            if level and not any(ca < b and cb > a for ca, cb in cards):
                zoomed.append((a, b))
            level ^= 1
    return [{"key": f"zoom_{a:.2f}", "kind": "zoom", "a": a, "b": b, "scale": scale, "cy": cy} for a, b in zoomed]


def add_settles(items, settle, base_dur):
    ov = [x for x in items if x["kind"] in ("card", "broll")]
    for x, y in zip(ov, ov[1:]):
        if y["a"] < x["b"] - 0.01:
            sys.exit(f"{x['key']} overlaps {y['key']}")
    if not settle:
        return items
    st = []
    for i, it in enumerate(items):
        if it["kind"] != "broll":
            continue
        a, b = it["b"], it["b"] + settle
        if (i + 1 < len(items) and items[i + 1]["a"] < b + 0.01) or b > base_dur - 0.05:
            continue
        st.append({"key": "settle_" + it["key"], "kind": "settle", "a": a, "b": b, "dur": settle})
    return sorted(items + st, key=lambda x: x["a"])


def pieces(layers, nframes):
    for L in layers:
        L["f0"], L["f1"] = f_in(L["a"]), min(nframes, f_out(L["b"]))
    cuts = sorted({0, nframes} | {L["f0"] for L in layers if L["f0"] < nframes} | {L["f1"] for L in layers if L["f1"] <= nframes})
    out = []
    for s, e in zip(cuts, cuts[1:]):
        if e > s:
            out.append((s, e, [L for L in layers if L["f0"] <= s and e <= L["f1"]]))
    return out


def piece_cmd(base, s, e, act, venc, path):
    n = e - s
    cmd = ["ffmpeg", "-nostdin", "-v", "error", "-y", "-ss", f"{s / FPS - 0.001:.4f}", "-i", base]
    fc, last, k, idx = [], "0:v", 0, 0
    act = [L for L in act if L["kind"] in ("settle", "zoom")] + [L for L in act if L["kind"] not in ("settle", "zoom")]
    for L in act:
        if L["kind"] == "settle":                   # zoom on the base itself (time measured from the window start)
            T = f"t+{(s - L['f0']) / FPS:.6f}"
            fc.append(f"[{last}]scale=w='{SETTLE.format(T=T, D=L['dur'])}':h=-2:eval=frame,"
                      f"crop=1920:1080:(iw-1920)/2:(ih-1080)/2[z{k}]")
            last = f"z{k}"; k += 1
            continue
        if L["kind"] == "zoom":                     # static punch-in, eyes kept high (final_v2.py: 114 %, crop y 35 %)
            zw = int(round(1920 * L["scale"] / 2)) * 2
            fc.append(f"[{last}]scale={zw}:-2,crop=1920:1080:(iw-1920)/2:(ih-1080)*{L['cy']}[z{k}]")
            last = f"z{k}"; k += 1
            continue
        cmd += ["-i", L["file"]]; idx += 1
        # clip frames: the window starts at clip frame ceil(30·clip_in) (like trim=start=…); this piece starts j_rel
        # frames into the window (like setpts=+in under overlay); fades are timed on the WINDOW like the old graph
        c0 = math.ceil(FPS * L.get("clip_in", 0.0) - 1e-6)
        j_rel = math.floor(s - FPS * L["a"] + 1e-6)
        pre = "format=yuva444p10le," if L["kind"] == "card" else "scale=1920:1080,"
        fades = ""
        if L.get("fade_in"):
            fades += f",fade=t=in:st=0:d={L['fade_in']}:alpha=1"
        if L.get("fade_out"):
            fades += f",fade=t=out:st={L['b'] - L['a'] - L['fade_out']:.3f}:d={L['fade_out']}:alpha=1"
        hold = ",tpad=stop_mode=clone:stop_duration=0.5" if L.get("hold", True) else ""   # last frame held over a short clip
        fc.append(f"[{idx}:v]{pre}trim=start_frame={c0},setpts=PTS-STARTPTS{fades},trim=start_frame={j_rel},"
                  f"setpts=PTS-STARTPTS{hold}[c{k}]")
        fmt = ":format=auto" if L["kind"] == "card" else ""
        fc.append(f"[{last}][c{k}]overlay=eof_action=pass{fmt}[o{k}]")
        last = f"o{k}"; k += 1
    if fc:
        cmd += ["-filter_complex", ";".join(fc), "-map", f"[{last}]"]
    else:
        cmd += ["-map", "0:v"]
    cmd += ["-an", "-frames:v", str(n), "-r", str(FPS)] + venc + ["-pix_fmt", "yuv420p", path + ".part.mp4"]
    return cmd


def run_piece(job):
    cmd, path = job
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        raise RuntimeError(f"piece failed: {path}\n{r.stderr[-800:]}")
    os.replace(path + ".part.mp4", path)


PRE = {"plain": "aresample=async=1:first_pts=0",
       "comp": "aresample=async=1:first_pts=0,highpass=f=70,acompressor=threshold=-26dB:ratio=2.5:attack=8:release=120:makeup=1,"
               "aformat=channel_layouts=stereo"}


def master(cdir, inputs, fc_in, dur, tag):
    """−14 LUFS two-pass loudnorm of a filter chain over `inputs` (measured once) → cached 48 kHz PCM."""
    h = hashlib.sha1(json.dumps([[stat_key(p) for p in inputs], fc_in, dur, "I-14|TP-1.5|LRA11"]).encode()).hexdigest()[:16]
    out = os.path.join(cdir, f"{tag}_{h}.wav")
    if os.path.exists(out):
        return out
    ins = sum([["-i", p] for p in inputs], [])
    m = subprocess.run(["ffmpeg", "-hide_banner", "-nostats"] + ins + ["-filter_complex",
                        f"{fc_in},apad=pad_dur=1,loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"],
                       capture_output=True, text=True).stderr
    j = json.loads(m[m.rindex("{"):m.rindex("}") + 1])
    ln = (f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={j['input_i']}:measured_TP={j['input_tp']}:measured_LRA={j['input_lra']}:"
          f"measured_thresh={j['input_thresh']}:offset={j['target_offset']}:linear=true")
    subprocess.run(["ffmpeg", "-v", "error", "-y"] + ins + ["-filter_complex", f"{fc_in},apad=pad_dur=1,{ln},aresample=48000,atrim=0:{dur}",
                    "-c:a", "pcm_s24le", out + ".part.wav"], check=True)
    os.replace(out + ".part.wav", out)
    return out


def aac(src, dur, out, fc=None, extra=()):
    if not os.path.exists(out):
        cmd = ["ffmpeg", "-v", "error", "-y", "-i", src] + list(extra)
        cmd += (["-filter_complex", fc, "-map", "[a]"] if fc else ["-af", f"atrim=0:{dur:.4f}"])
        subprocess.run(cmd + ["-c:a", "aac", "-b:a", "320k", out + ".part.m4a"], check=True)
        os.replace(out + ".part.m4a", out)
    return out


def main():
    a = sys.argv[1:]
    if not a or a[0].startswith("-"):
        sys.exit(__doc__)
    opt = lambda k, d=None: a[a.index(k) + 1] if k in a else d
    proj = os.path.abspath(a[0])
    rel = lambda p: p if p is None or os.path.isabs(p) else os.path.join(proj, p)
    base = rel(opt("--base", "CUT.mp4")); out = os.path.abspath(opt("--out"))
    sfx = rel(opt("--sfx")); settle = float(opt("--settle", 0)); prof = opt("--profile", "x264")
    jobs = int(opt("--jobs", 2)); upto = float(opt("--upto", 1e9))     # 2 parallel x264 jobs: fastest on the M2 Air (3 = slower)
    venc = PROFILES[prof]
    T = {"start": time.strftime("%Y-%m-%d %H:%M:%S")}; t0 = time.time()
    base_dur = probe_dur(base)
    nframes = min(round(base_dur * FPS), round(upto * FPS))
    if "--scenes" in a:
        layers = layers_from_scenes(proj, rel(opt("--scenes")), settle, base_dur)
    elif "--index" in a and "--reedit" in a:
        layers = add_settles(layers_from_reedit(proj, rel(opt("--reedit")), rel(opt("--index"))), settle, base_dur)
    elif "--index" in a:
        layers = layers_from_index(proj, rel(opt("--index")), settle, base_dur)
    else:
        layers = []
    if opt("--zooms") == "auto":
        wj = rel(opt("--words", "tr/cut.json" if os.path.exists(rel("tr/cut.json")) else "tr/words.json"))
        jj = rel(opt("--joins", "edit/joins.json" if os.path.exists(rel("edit/joins.json")) else "joins.json"))
        ws = [w for sg in json.load(open(wj))["segments"] for w in sg["words"]]
        sent = [ws[i + 1]["start"] for i in range(len(ws) - 1) if ws[i]["word"].strip()[-1:] in ".?!"]
        layers = sorted(layers + plan_zooms(layers, base_dur, sent, json.load(open(jj)),
                                            float(opt("--zoom", 114)) / 100, float(opt("--zoom-y", 0.35))), key=lambda x: x["a"])
    layers = [L for L in layers if L["a"] < nframes / FPS]
    P = pieces(layers, nframes)
    cdir = os.path.abspath(opt("--cache", os.path.join(proj, "cache", "final"))); pdir = os.path.join(cdir, prof); os.makedirs(pdir, exist_ok=True)
    bstat = stat_key(base); files, todo = [], []
    for s, e, act in P:
        sig = [bstat, s, e, venc, ASM_V] + [[L["kind"], stat_key(L["file"]) if L.get("file") else L.get("dur"), L["a"], L["f0"],
                                             L.get("clip_in"), L.get("fade_in"), L.get("fade_out"), L.get("scale"), L.get("cy"), L.get("hold", True)]
                                            for L in act]
        h = hashlib.sha1(json.dumps(sig).encode()).hexdigest()[:20]
        f = os.path.join(pdir, h + ".mp4"); files.append(f)
        if not os.path.exists(f):
            todo.append((piece_cmd(base, s, e, act, venc, f), f))
    print(f"{len(layers)} layers → {len(P)} pieces; {len(todo)} to render, {len(P) - len(todo)} from cache", flush=True)
    t1 = time.time()
    with ThreadPoolExecutor(max_workers=max(1, jobs)) as ex:
        list(ex.map(run_piece, todo))
    T["pieces_s"] = round(time.time() - t1, 1)
    t1 = time.time()
    dur = nframes / FPS
    style = opt("--audio", "plain")
    if "--no-master" in a:
        voice, mixw = base, None
    else:
        voice = master(cdir, [base], f"[0:a]{PRE[style]}", base_dur, "voice")
        # comp („Ciężka praca” v2): voice+SFX mixed first, the mix normalised; plain: SFX added after, through a limiter
        mixw = master(cdir, [base, sfx], f"[0:a]{PRE[style]}[v];[v][1:a]amix=inputs=2:normalize=0:duration=first", base_dur,
                      "mix") if (sfx and style == "comp") else None
    T["voice_s"] = round(time.time() - t1, 1)
    lst = os.path.join(cdir, "concat_" + os.path.basename(out) + ".txt")
    open(lst, "w").write("".join(f"file '{f}'\n" for f in files))
    t1 = time.time()
    # sound is encoded ONCE per (voice, sfx, length, style) and cached as AAC; a picture fix only re-muxes (stream copy)
    akey = hashlib.sha1(json.dumps([stat_key(voice), stat_key(sfx) if sfx else None, nframes, style]).encode()).hexdigest()[:16]
    mix_a = os.path.join(cdir, f"mix_{akey}.m4a"); voice_a = os.path.join(cdir, f"voice_{akey}.m4a")
    if mixw:
        aac(mixw, dur, mix_a)
    elif sfx:
        aac(voice, dur, mix_a, fc=f"[0:a][1:a]amix=inputs=2:normalize=0:duration=first,alimiter=limit=0.89:level=false,"
                                  f"atrim=0:{dur:.4f}[a]", extra=["-i", sfx])
    else:
        aac(voice, dur, mix_a)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-i", mix_a, "-map", "0:v", "-map", "1:a",
                    "-c", "copy", "-movflags", "+faststart", out + ".part.mp4"], check=True)
    os.replace(out + ".part.mp4", out)
    if "--bez-sfx" in a and sfx:
        aac(voice, dur, voice_a)
        o2 = out.replace(".mp4", "_bez-sfx.mp4")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", out, "-i", voice_a, "-map", "0:v", "-map", "1:a", "-c", "copy",
                        "-movflags", "+faststart", o2], check=True)
    T["mux_s"] = round(time.time() - t1, 1)
    T.update({"total_s": round(time.time() - t0, 1), "pieces": len(P), "rendered": len(todo), "frames": nframes,
              "profile": prof, "out": out})
    with open(os.path.join(cdir, "runs.jsonl"), "a") as f:
        f.write(json.dumps(T) + "\n")
    print(f"→ {out}  ({dur:.1f} s)  {T}")


if __name__ == "__main__":
    main()
