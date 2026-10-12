#!/usr/bin/env python3
"""Cut raw talking-head recordings from a list of chosen takes → edl.json → (render) CUT.mp4.

usage: cut_takes.py takes.json [--audio OUT.wav] [--preview OUT.mp4] [--render OUT.mp4] [--audit]
                   [--profile slow12|fast|vt] [--jobs 2] [--refreeze] [--legacy]
  --audio    sound of the cut only (seconds, no video): use it for pauses / splice audit while iterating on takes
  --preview  low-res cut (960 px, hardware encoder) for watching on the phone — same timeline, same sound
  --render   full-quality cut (--profile; default vt = Apple hardware H.264 25 Mbit/s, VMAF 98.5; slow12 = old CRF 12 look)
  --audit    splice audit on the cut's sound (works with --audio alone); only joins whose sound changed are re-run
  --legacy   the pre-2026-10-10 renderer (segments with PCM, start on the 1/30 s grid) — rollback only
takes.json:
{
  "sources":     {"L": "/abs/raw_long.MP4", "S": "/abs/raw_short.MP4"},
  "transcripts": {"L": "tr/L.json", "S": "tr/S.json"},        # whisper json OR ElevenLabs Scribe json (words[] with type)
  "takes": [["L", 32.86, 42.56, "Daj mi trzy minuty … sprzedawać."], ...]   # source, first-word start, last-word START or end, note
}
optional 5th element per take: {"keep": true}  → do NOT tighten pauses inside (script says [pauza], rhetorical beat)
                                {"hold": 0.5}   → keep 0.5 s of real room tone after the last word (pause before a punchline)
If the 3rd value equals a word's START, the script uses that word's END automatically (you can copy times from pack_takes).
YOU choose the takes (best COMPLETE take of every line, usually the last; keep good improvisations). The script then:
- snaps each take's edges to the real audio (voiced onset, breath before the take excluded, 45 ms pre / 65 ms post pad),
- tightens every silence > 200 ms INSIDE a take to ~140 ms (Konrad always shortens these; never lengthens),
- writes edl.json next to takes.json with the exact timeline: every range starts on a REAL source frame ("ss", "n"
  frames, "t" = position in the cut) — iPhone frames sit ~15 ms off the 1/30 s grid; cutting on the grid duplicated the
  first frame of ~45 % of segments (micro-freeze at the join);
- video segments are cached by content (cache/segs/<profile>/<hash>.mov): after a takes.json fix only changed ranges
  are encoded; the sound is cut sample-exactly from the source (48 kHz stereo, 15 ms fades) and muxed once.
After rendering: transcribe the cut, read it end to end (no repeated phrase, no half sentence, no orphan word).
"""
import json, os, subprocess, sys, wave
import numpy as np

PRE, POST = 0.045, 0.065
PAUSE_DB = -50.0


def load_words(p):
    d = json.load(open(p))
    if isinstance(d, list):                          # asr.py / yt-longform-editor words_raw.json: [{text,start,end}]
        return [{"start": w["start"], "end": w["end"]} for w in d]
    if "segments" in d:
        return [{"start": w["start"], "end": w["end"]} for s in d["segments"] for w in s.get("words", [])]
    return [{"start": w["start"], "end": w["end"]} for w in d["words"] if w.get("type", "word") == "word"]


def snap_end(words, b):
    for w in words:
        if abs(w["start"] - b) < 0.006:
            return w["end"]
    return b


def main():
    a = sys.argv[1:]
    if not a:
        sys.exit(__doc__)
    cfg_p = os.path.abspath(a[0]); base = os.path.dirname(cfg_p)
    cfg = json.load(open(cfg_p))
    SRC = cfg["sources"]
    rel = lambda p: p if os.path.isabs(p) else os.path.join(base, p)
    ENV, WORDS = {}, {}
    for k, src in SRC.items():
        wav = os.path.join(base, f".{k}_16k.wav")
        if not os.path.exists(wav):
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-ac", "1", "-ar", "16000", wav], check=True)
        w = wave.open(wav)
        x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
        hop = 160; n = len(x) // hop
        db = 20 * np.log10(np.sqrt((x[:n * hop].reshape(n, hop) ** 2).mean(1)) + 1e-9)
        ENV[k] = (db, np.percentile(db, 15) + 10, np.percentile(db, 50) - 10)
        WORDS[k] = load_words(rel(cfg["transcripts"][k]))

    def loud(key, t, voiced=False):
        db, thr, hi = ENV[key]; i = int(t * 100)
        return 0 <= i < len(db) and db[i] > (hi if voiced else thr)

    def neighbours(key, a_, b_):
        ws = WORDS[key]
        return (max([w["end"] for w in ws if w["end"] <= a_ + 0.02] or [0]),
                min([w["start"] for w in ws if w["start"] >= b_ - 0.02] or [1e9]))

    def onset(key, a_, lo):
        db, thr, hi = ENV[key]
        i0, i1 = int(max(lo, a_ - 0.15) * 100), int((a_ + 0.08) * 100)
        m = i0 + int(np.argmin(db[i0:i1]))
        voiced_before = sum(1 for k in range(int(a_ * 100), m) if db[k] > hi + 6)
        t = a_
        if db[m] < hi and voiced_before < 4:
            t = m / 100
            while t < a_ + 0.2 and not loud(key, t, True):
                t += 0.01
            lo = max(lo, m / 100)
        if not loud(key, t, True):
            while t < a_ + 0.2 and not loud(key, t, True):
                t += 0.01
        else:
            while t - 0.01 > lo and loud(key, t - 0.01, True):
                t -= 0.01
        k = 0
        while k < 6 and t - 0.01 > lo and loud(key, t - 0.01):
            t -= 0.01; k += 1
        return t

    def offset(key, b_, hi):
        t = b_ - 0.05
        while t < min(hi, b_ + 0.25) and loud(key, t):
            t += 0.01
        return t

    # pause threshold measured on the KEPT material only (like check.py pauses on the finished cut):
    # p15 of the selected takes + 10 dB, per source. Raw-file stats are dragged down by long gaps between takes.
    keep_frames = {k: [] for k in SRC}
    for tk in cfg["takes"]:
        k_, a0, b0 = tk[0], tk[1], snap_end(WORDS[tk[0]], tk[2])
        keep_frames[k_].append(ENV[k_][0][int(a0 * 100):int(b0 * 100) + 1])
    Q_THR = {k: (np.percentile(np.concatenate(v), 15) + 10 if v else PAUSE_DB) for k, v in keep_frames.items()}
    # FROZEN after the first run (edl_params.json): Q_THR depends on ALL chosen takes, so re-measuring it after a small
    # takes.json fix would move pause cuts in every other take and invalidate every cached segment. --refreeze re-measures.
    par_p = os.path.join(base, "edl_params.json")
    par = json.load(open(par_p)) if os.path.exists(par_p) and "--refreeze" not in a else {}
    frozen = par.get("q_thr", {})
    Q_THR = {k: float(frozen.get(k, v)) for k, v in Q_THR.items()}
    json.dump({"q_thr": Q_THR, "note": "pause thresholds frozen after the first cut; delete or --refreeze to re-measure"},
              open(par_p, "w"), indent=1)
    log = [f"pause threshold {k}: {v:.1f} dB{' (frozen)' if k in frozen else ''}" for k, v in Q_THR.items()]
    ranges = []
    for tk in cfg["takes"]:
        key, a_, b_, note = tk[:4]
        opt = tk[4] if len(tk) > 4 else {}
        b_ = snap_end(WORDS[key], b_)
        prev_end, next_start = neighbours(key, a_, b_)
        s = max(onset(key, a_, prev_end + 0.03) - PRE, prev_end + 0.01)
        if opt.get("exact_start"):     # Konrad's review cut: start exactly at a_ (onset search would walk back over murmur)
            s = a_
        e = min(offset(key, b_, next_start - 0.03) + POST, next_start - 0.01)
        if opt.get("hold"):
            e = max(e, min(b_ + float(opt["hold"]), next_start - 0.02))
        db = ENV[key][0]
        i0, i1 = int(round(s * 100)), int(round(e * 100))
        inword = np.zeros(i1 - i0, bool)
        vthr = Q_THR[key] - 3          # "voiced" level: ASR stretches the last word over the following breath/silence
        for w_ in WORDS[key]:
            p0, p1 = int(w_["start"] * 100), int(w_["end"] * 100)
            if p1 < i0 or p0 >= i1:
                continue
            seg_w = db[p0:p1 + 1]
            loud_i = np.nonzero(seg_w > vthr)[0]
            if len(loud_i):            # real voiced span of the word + 80 ms tail / 50 ms head for soft consonants
                p0, p1 = max(p0, p0 + loud_i[0] - 5), min(p1, p0 + loud_i[-1] + 8)
            inword[max(0, p0 - i0):max(0, min(i1 - i0, p1 - i0))] = True
        # quiet = below this recording's own floor + 10 dB (same as check.py pauses), or breath-level between words
        # inside a word (ASR span): only real silence counts (raw floor + 10 dB) → soft endings (ś, ć, sz) are never eaten;
        # between words: the kept-material threshold, so breaths and room tone between sentences get tightened
        floor = max(PAUSE_DB, ENV[key][1])
        sp = [not (db[i] < floor or (db[i] < max(-40, Q_THR[key]) and not inword[i - i0])) for i in range(i0, i1)]
        seg = db[i0:i1]
        first = next((k for k in range(len(seg)) if seg[k] > -40), 0)
        while first > 0 and seg[first - 1] > PAUSE_DB:
            first -= 1
        last = next((k for k in range(len(seg) - 1, -1, -1) if seg[k] > -40), len(seg) - 1)
        while last < len(seg) - 1 and seg[last + 1] > PAUSE_DB:
            last += 1
        cur, keep_to, parts, k = max(0, first - 5) / 100 + s, min(len(sp), last + 8) / 100 + s, [], first
        if opt.get("hold"):
            keep_to = e
        while k <= last:
            if not sp[k]:
                j = k
                while j <= last and not sp[j]:
                    j += 1
                if (j - k) / 100 > 0.20 and not opt.get("keep") and s + k / 100 < b_ - 0.02:
                    parts.append((cur, s + k / 100 + 0.07)); cur = s + j / 100 - 0.07
                    log.append(f"  pause {(j - k) * 10} ms @ {key} {s + k / 100:.2f} → 140 ms")
                k = j
            else:
                k += 1
        parts.append((cur, keep_to))
        parts = clean_micro(parts, a_, tk[2], log, key)
        ranges += [{"source": key, "start": round(p[0], 3), "end": round(p[1], 3), "beat": note} for p in parts]
        log.append(f"{key} {s:7.2f}-{e:7.2f}  {note}")
    # merge ranges that touch or overlap in the same source (adjacent takes / tightened pauses) → no doubled audio
    merged = []
    for r in ranges:
        m = merged[-1] if merged else None
        if m and m["source"] == r["source"] and r["start"] <= m["end"] + 0.04 and r["start"] >= m["start"]:
            m["end"] = max(m["end"], r["end"])
        else:
            merged.append(dict(r))
    if len(merged) != len(ranges):
        log.append(f"merged {len(ranges) - len(merged)} touching/overlapping ranges")
    ranges = timeline(base, SRC, merged)
    edl = os.path.join(base, "edl.json")
    json.dump({"sources": SRC, "fps": FPS, "timeline": 2, "ranges": ranges}, open(edl, "w"), ensure_ascii=False, indent=1)
    print("\n".join(log))
    total = sum(r["n"] for r in ranges) / FPS
    for i, r in enumerate(ranges):                   # bledy.md: no range < 0.4 s — a 2-frame piece is a click / cut syllable
        if r["n"] < 6:
            print(f"⚠ range {i} is only {r['n']} frames ({r['n'] / FPS:.2f} s) at cut {r['t']:.2f} s — {r['beat'][:50]!r}: "
                  "listen; widen the take or drop the piece")
    print(f"{len(ranges)} ranges, runtime {total:.1f} s → {edl}")
    prof = a[a.index("--profile") + 1] if "--profile" in a else DEFAULT_PROFILE
    jobs = int(a[a.index("--jobs") + 1]) if "--jobs" in a else 2
    cut_wav = None
    if "--legacy" in a:
        if "--render" in a:
            out = os.path.abspath(a[a.index("--render") + 1])
            render_legacy(edl, out)
            if "--audit" in a:
                audit(edl, cut_audio(edl))
        return
    if "--audio" in a or "--audit" in a or "--preview" in a or "--render" in a:
        cut_wav = cut_audio(edl, os.path.abspath(a[a.index("--audio") + 1]) if "--audio" in a else None)
    if "--preview" in a:
        render(edl, os.path.abspath(a[a.index("--preview") + 1]), "preview", cut_wav, jobs)
    if "--render" in a:
        render(edl, os.path.abspath(a[a.index("--render") + 1]), prof, cut_wav, jobs)
    if "--audit" in a:
        audit(edl, cut_wav)


def clean_micro(parts, first_word, last_word_start, log, key, min_len=0.2, near=0.25):
    """Pieces shorter than 0.2 s left by pause tightening (2026-10-10: 28 of them in one film — clicks / cut syllables):
    before the first word or after the last word with a pause in between → a leftover breath or a word tail the ASR
    stretched → dropped; otherwise glued to the neighbour it is close to (the short pause stays, no cut inside a word)."""
    out = list(parts)
    changed = True
    while changed:
        changed = False
        for i, (p0, p1) in enumerate(out):
            if p1 - p0 >= min_len or len(out) == 1:
                continue
            gp = p0 - out[i - 1][1] if i > 0 else None
            gn = out[i + 1][0] - p1 if i + 1 < len(out) else None
            if (i == 0 and p1 <= first_word + 0.02) or (i == len(out) - 1 and p0 > last_word_start and (gp is None or gp > near)):
                log.append(f"  micro {key} {p0:.2f}-{p1:.2f} dropped (breath / stretched word tail)")
                del out[i]
            elif gn is not None and gn <= near and (gp is None or gn <= gp):
                log.append(f"  micro {key} {p0:.2f}-{p1:.2f} joined to next"); out[i:i + 2] = [(p0, out[i + 1][1])]
            elif gp is not None and gp <= near:
                log.append(f"  micro {key} {p0:.2f}-{p1:.2f} joined to previous"); out[i - 1:i + 1] = [(out[i - 1][0], p1)]
            else:
                continue
            changed = True
            break
    return out


FPS = 30
SR = 48000
RENDER_V = "seg-2"                                   # bump when the segment command changes → cache invalidates
COLOR = ["-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709"]
PROFILES = {   # video encoders for the cut segments (all segments of one cut use ONE profile → concat without re-encode)
    "slow12": {"args": ["-c:v", "libx264", "-preset", "slow", "-crf", "12"], "hw": False},            # original look
    "fast": {"args": ["-c:v", "libx264", "-preset", "veryfast", "-crf", "16"], "hw": False},
    "vt": {"args": ["-c:v", "h264_videotoolbox", "-b:v", "25M", "-profile:v", "high"], "hw": True},     # Apple media engine
    "preview": {"args": ["-c:v", "h264_videotoolbox", "-b:v", "4M", "-profile:v", "high", "-vf", "scale=960:-2"], "hw": True},
}
DEFAULT_PROFILE = "vt"         # 2026-10-09 benchmark: VMAF 98.5 vs 99.3 (slow12), 8.8× faster on cut segments


def _stat_key(path):
    st = os.stat(path)
    return f"{os.path.abspath(path)}|{st.st_size}|{st.st_mtime_ns}"


def src_pts(base, key, src):
    """Presentation times of every video frame of a source (cached next to takes.json)."""
    p = os.path.join(base, f".{key}_pts.json")
    sk = _stat_key(src)
    if os.path.exists(p):
        d = json.load(open(p))
        if d.get("stat") == sk:
            return d["pts"]
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "packet=pts_time",
                          "-of", "csv=p=0", src], capture_output=True, text=True, check=True).stdout
    pts = sorted(float(x.strip(", ")) for x in out.split() if x.strip(", ") not in ("", "N/A"))
    json.dump({"stat": sk, "pts": pts}, open(p, "w"))
    return pts


def timeline(base, SRC, ranges):
    """Snap every range to real source frames: ss = pts of the frame nearest to the range start, n = whole frames,
    t = position in the cut. Ranges of the same source never overlap after snapping."""
    import bisect
    pts = {k: src_pts(base, k, s) for k, s in SRC.items()}
    out, t, last_end = [], 0, {}
    for r in ranges:
        p = pts[r["source"]]
        n = max(1, round((r["end"] - r["start"]) * FPS))
        k = bisect.bisect_left(p, r["start"])
        k = min((j for j in (k - 1, k) if 0 <= j < len(p)), key=lambda j: abs(p[j] - r["start"]))
        le = last_end.get(r["source"])
        if le is not None and k < le <= k + n and r["start"] >= p[max(0, le - 1)] - 0.5:
            n -= le - k; k = le                       # would repeat frames/sound of the previous range of this source
        n = max(1, min(n, len(p) - k))
        last_end[r["source"]] = k + n
        out.append(dict(r, ss=round(p[k], 4), k=k, n=n, t=round(t / FPS, 4)))
        t += n
    return out


def src_audio(base, key, src):
    """Whole source sound decoded once to 48 kHz stereo int16 (memmap) + the time of its first sample."""
    raw, meta = os.path.join(base, f".{key}_48k.s16"), os.path.join(base, f".{key}_48k.json")
    sk = _stat_key(src)
    if not (os.path.exists(raw) and os.path.exists(meta) and json.load(open(meta)).get("stat") == sk):
        a0 = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "a:0", "-show_entries", "stream=start_time",
                             "-of", "csv=p=0", src], capture_output=True, text=True).stdout.strip().strip(",")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-map", "0:a:0", "-ac", "2", "-ar", str(SR),
                        "-f", "s16le", raw + ".part"], check=True)
        os.replace(raw + ".part", raw)
        json.dump({"stat": sk, "start": float(a0) if a0 not in ("", "N/A") else 0.0}, open(meta, "w"))
    m = json.load(open(meta))
    return np.memmap(raw, np.int16, "r").reshape(-1, 2), m["start"]


def cut_audio(edl_p, out=None):
    """The cut's sound, sample-exact on the frame timeline (1600 samples per frame), 15 ms fades at every edge.
    Same result the full render will carry. Returns the WAV path (default: <project>/cut_audio.wav)."""
    e = json.load(open(edl_p)); base = os.path.dirname(edl_p)
    out = out or os.path.join(base, "cut_audio.wav")
    spf, fade = SR // FPS, int(0.015 * SR)
    ramp = np.linspace(0, 1, fade, dtype=np.float32)[:, None]
    srcs, chunks = {}, []
    for r in e["ranges"]:
        if r["source"] not in srcs:
            srcs[r["source"]] = src_audio(base, r["source"], e["sources"][r["source"]])
        x, a0 = srcs[r["source"]]
        i0, ln = int(round((r["ss"] - a0) * SR)), r["n"] * spf
        seg = np.zeros((ln, 2), np.float32)
        lo, hi = max(0, i0), min(len(x), i0 + ln)
        if hi > lo:
            seg[lo - i0:hi - i0] = x[lo:hi]
        f = min(fade, ln // 2)
        seg[:f] *= ramp[:f]; seg[ln - f:] *= ramp[:f][::-1]
        chunks.append(seg)
    y = np.clip(np.concatenate(chunks), -32768, 32767).astype("<i2")
    import wave
    with wave.open(out + ".part", "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(y.tobytes())
    os.replace(out + ".part", out)
    print(f"audio → {out}  ({len(y) / SR:.2f} s)")
    return out


def _segment(src, r, prof, path):
    P = PROFILES[prof]
    cmd = ["ffmpeg", "-nostdin", "-v", "error", "-y"] + (["-hwaccel", "videotoolbox"] if P["hw"] else []) + \
          ["-ss", f"{r['ss'] - 0.001:.4f}", "-i", src, "-map", "0:v:0", "-an", "-frames:v", str(r["n"])] + P["args"] + \
          ["-pix_fmt", "yuv420p", "-r", str(FPS)] + COLOR + [path + ".part.mov"]
    subprocess.run(cmd, check=True)
    os.replace(path + ".part.mov", path)


def render(edl_p, out, prof, cut_wav, jobs=2):
    """Video segments from the ORIGINAL on real source frames, cached by content; concat without re-encoding; the
    sample-exact cut sound muxed once (one AAC encode). Only ranges whose source/frames/profile changed are encoded."""
    import hashlib, time
    from concurrent.futures import ThreadPoolExecutor
    e = json.load(open(edl_p)); base = os.path.dirname(edl_p)
    seg_dir = os.path.join(base, "cache", "segs", prof); os.makedirs(seg_dir, exist_ok=True)
    stat = {k: _stat_key(s) for k, s in e["sources"].items()}
    jobs_l, files = [], []
    for r in e["ranges"]:
        h = hashlib.sha1(json.dumps([stat[r["source"]], r["ss"], r["n"], PROFILES[prof], RENDER_V]).encode()).hexdigest()[:20]
        f = os.path.join(seg_dir, h + ".mov")
        files.append(f)
        if not os.path.exists(f):
            jobs_l.append((e["sources"][r["source"]], r, f))
    t0 = time.time()
    with ThreadPoolExecutor(max_workers=max(1, jobs)) as ex:
        list(ex.map(lambda j: _segment(j[0], j[1], prof, j[2]), jobs_l))
    t_enc = time.time() - t0
    lst = os.path.join(seg_dir, "concat_" + os.path.basename(out) + ".txt")
    open(lst, "w").write("".join(f"file '{f}'\n" for f in files))
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-i", cut_wav,
                    "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-shortest",
                    "-movflags", "+faststart", out + ".part.mp4"], check=True)
    os.replace(out + ".part.mp4", out)
    joins = [r["t"] for r in e["ranges"][1:]]
    json.dump(joins, open(os.path.join(base, "joins.json"), "w"))
    total = sum(r["n"] for r in e["ranges"]) / FPS
    print(f"rendered {out} [{prof}]  ({total:.1f} s, {len(joins)} joins; encoded {len(jobs_l)}/{len(files)} segments "
          f"in {t_enc:.0f} s, {len(files) - len(jobs_l)} from cache)")


def render_legacy(edl_p, out):
    """Pre-2026-10-10 renderer, kept for rollback: grid-aligned start (duplicates a first frame in ~45 % of segments)."""
    e = json.load(open(edl_p))
    seg_dir = os.path.join(os.path.dirname(edl_p), "segs"); os.makedirs(seg_dir, exist_ok=True)
    lines, joins, t = [], [], 0.0
    for i, r in enumerate(e["ranges"]):
        s0 = round(r["start"] * FPS) / FPS
        d = max(1, round((r["end"] - r["start"]) * FPS)) / FPS
        p = os.path.join(seg_dir, f"{i:03d}.mov")
        subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-ss", f"{s0:.4f}", "-i", e["sources"][r["source"]],
                        "-t", f"{d:.4f}", "-map", "0:v:0", "-map", "0:a:0",
                        "-af", f"aresample=48000,apad,atrim=0:{d:.4f},afade=t=in:st=0:d=0.015,afade=t=out:st={d - 0.015:.4f}:d=0.015",
                        "-c:v", "libx264", "-preset", "slow", "-crf", "12", "-pix_fmt", "yuv420p", "-r", str(FPS)] + COLOR +
                       ["-c:a", "pcm_s16le", "-ar", "48000", "-ac", "2", p], check=True)
        lines.append(f"file '{p}'\n")
        if i:
            joins.append(round(t, 3))
        t += d
    lst = os.path.join(seg_dir, "concat.txt"); open(lst, "w").write("".join(lines))
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c:v", "copy",
                    "-af", "aresample=async=1:first_pts=0", "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart", out], check=True)
    json.dump(joins, open(os.path.join(os.path.dirname(edl_p), "joins.json"), "w"))
    print(f"rendered (legacy) {out}  ({t:.1f} s, {len(joins)} joins → joins.json)")


def audit(edl_p, cut_wav):
    """Splice audit: transcribe ±1.6 s around every join of the cut's SOUND. Read it: each join must read as one clean
    sentence — no doubled words, no 'ma--', no swallowed word ends. Whisper per window (as before) but in ONE process
    (model loaded once); windows whose sound did not change come from cache/audit/."""
    import hashlib, time, wave
    base = os.path.dirname(edl_p)
    jf, f = [], 0                                    # joins in FRAMES (exact), from the timeline in edl.json
    for r in json.load(open(edl_p))["ranges"]:
        if f:
            jf.append(f)
        f += r["n"]
    cdir = os.path.join(base, "cache", "audit"); os.makedirs(cdir, exist_ok=True)
    w = wave.open(cut_wav); y = np.frombuffer(w.readframes(w.getnframes()), np.int16).reshape(-1, 2).astype(np.float32)
    mono = y.mean(1) / 32768
    wins, todo = [], []
    spf = SR // FPS
    for fj in jf:
        # window cut at 48 kHz on the frame grid (frame·1600 samples), THEN decimated → an unchanged join gives the
        # same samples (same cache key) even when everything before it moved
        j = fj / FPS
        a0 = max(0, fj * spf - int(1.6 * SR)); w48 = mono[a0:a0 + int(3.2 * SR)]
        seg = w48[: len(w48) // 3 * 3].reshape(-1, 3).mean(1).astype(np.float32)     # 48 → 16 kHz (box filter)
        h = hashlib.sha1(seg.tobytes()).hexdigest()[:20]
        wins.append((j, h)); p = os.path.join(cdir, h + ".txt")
        if not os.path.exists(p):
            todo.append((h, seg))
    t0 = time.time()
    if todo:
        import mlx_whisper
        # one window per call, exactly the CLI's decoding (incl. temperature fallback) — gluing windows into one pass
        # invented repeats and dropped words in the 2026-10-10 test; only the model load is shared now
        for h, seg in todo:
            r = mlx_whisper.transcribe(seg, path_or_hf_repo="mlx-community/whisper-large-v3-turbo", language="pl")
            open(os.path.join(cdir, h + ".txt"), "w").write(" ".join(s_["text"].strip() for s_ in r.get("segments", [])))
    rep = [f"{int(j // 60)}:{j % 60:05.2f}  {open(os.path.join(cdir, h + '.txt')).read()}" for j, h in wins]
    open(os.path.join(base, "splice_audit.txt"), "w").write("\n".join(rep) + "\n")
    print("\n".join(rep))
    print(f"-- audit: {len(todo)} new / {len(wins)} joins transcribed in {time.time() - t0:.0f} s")


if __name__ == "__main__":
    main()
