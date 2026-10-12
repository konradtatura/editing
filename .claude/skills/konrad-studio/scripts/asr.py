#!/usr/bin/env python3
"""Verbatim word transcript of a RAW recording for cutting takes — fast, cached, keeps every retake.

usage: asr.py SRC OUT_DIR [--lang pl] [--window 45] [--passes 2] [--no-cache] [--no-rescue]
Writes the same layout as yt-longform-editor/scripts/transcribe.py, so pack/takes/cut_takes work unchanged:
  OUT_DIR/00_input/audio16k.wav       mono 16 kHz
  OUT_DIR/01_cut/words_raw.json       [{"text","start","end"[,"rescued"]}]
  OUT_DIR/01_cut/transcript_raw.md    sentences with timecodes; ⚠ rows = voice the ASR left without words
  OUT_DIR/01_cut/asr_meta.json        engine, cache key, timings, flagged spots
Pipeline:
  1. Parakeet TDT 0.6b v3 (parakeet-mlx in ~/.venvs/parakeet, Apple GPU) on windows cut at silences (≤ --window s, no
     overlap merge). Measured 2026-10-09 on 23:13 of Konrad's Polish: 2:04 (old per-utterance Whisper: 33:16), more
     retakes kept (112 vs 94 repeated 4-grams), no "Dzięki za oglądanie" hallucinations.
  2. Rescue: every voiced utterance (between ≥0.25 s silences) that got NO word — typically a 1–4-word false start like
     „I to jest… I to jest dobra wiadomość” — is cut out, batched into one file and transcribed by Whisper large-v3-turbo
     forced to Polish (one pass, ~20 s). Rescued words carry "rescued": true; hallucinations/loops are dropped; every
     orphan is listed with ⚠ in transcript_raw.md so the take picker sees it even when nothing was recovered.
  3. Cache: ~/.cache/konrad-studio/asr/<key>.json, key = size + mtime + first/last 8 MB of SRC + engine/version/options.
     A second run on the same file costs only the 16 kHz extraction. Never delete transcripts by hand to "refresh".
Without ~/.venvs/parakeet it exits with code 3 (caller falls back to the old engine).
"""
import hashlib, json, os, re, subprocess, sys, time, wave
import numpy as np

VERSION = "asr-4"            # asr-4: smoothed voice-gap rescue; asr-3: 2 passes with shifted windows, fuller chunk wins; padded windows; mid-utterance gaps rescued
HERE = os.path.dirname(os.path.abspath(__file__))
PK_PY = os.path.expanduser("~/.venvs/parakeet/bin/python")
CACHE = os.environ.get("KS_ASR_CACHE") or os.path.expanduser("~/.cache/konrad-studio/asr")   # env override: clean timing tests
HALL = re.compile(r"dzi[eę]kuj[eę]|za ogl[aą]danie|napisy|subskryb", re.I)


def file_key(path, extra):
    st = os.stat(path)
    h = hashlib.sha1(f"{st.st_size}:{st.st_mtime_ns}:{extra}".encode())
    with open(path, "rb") as f:
        h.update(f.read(8 << 20))
        if st.st_size > 16 << 20:
            f.seek(-(8 << 20), 2); h.update(f.read())
    return h.hexdigest()


def envelope(x, sr):
    hop = sr // 100; n = len(x) // hop
    return 20 * np.log10(np.sqrt((x[:n * hop].reshape(n, hop) ** 2).mean(1)) + 1e-9)


def windows(db, max_s, first=None):
    """Cut points at the longest quiet run in the last 20 s before each max_s limit. `first` = shorter first window
    (second pass: every edge lands somewhere else, so a retake lost at an edge in one pass is mid-window in the other)."""
    quiet = db < np.percentile(db, 15) + 10
    n, cuts, s = len(db), [0], 0
    while n - s > (first or max_s) * 100:
        lim = first or max_s; first = None
        lo, hi = s + int(max(1, lim - 20) * 100), s + int(lim * 100)
        best, bl, i = hi, 0, lo
        while i < hi:
            if quiet[i]:
                j = i
                while j < hi and quiet[j]:
                    j += 1
                if j - i > bl:
                    bl, best = j - i, (i + j) // 2
                i = j
            else:
                i += 1
        cuts.append(best); s = best
    cuts.append(n)
    return [[cuts[k] / 100, cuts[k + 1] / 100] for k in range(len(cuts) - 1)]


def merge_passes(passes, db):
    """Per sentence-sized chunk (split at pauses ≥ 0.5 s) keep the pass that wrote MORE words: Parakeet drops a repeated
    take now and then depending on where a window starts — the fuller version is the one that kept the retake."""
    quiet = db < np.percentile(db, 15) + 10
    bounds, i, n = [0.0], 0, len(db)
    while i < n:
        if quiet[i]:
            j = i
            while j < n and quiet[j]:
                j += 1
            if j - i >= 50:
                bounds.append((i + j) / 200)
            i = j
        else:
            i += 1
    bounds.append(n / 100 + 1)
    out, chosen = [], [0] * len(passes)
    for c0, c1 in zip(bounds, bounds[1:]):
        cand = [[w for w in ws if c0 <= w["start"] < c1] for ws in passes]
        k = max(range(len(cand)), key=lambda q: (len(cand[q]), -q))
        chosen[k] += 1; out += cand[k]
    return sorted(out, key=lambda w: w["start"]), chosen


def utterances(db):
    sp = db > np.percentile(db, 15) + 10
    n, out, i = len(db), [], 0
    while i < n:
        if sp[i]:
            j, q = i, 0
            while j < n and q < 25:
                q = q + 1 if not sp[j] else 0; j += 1
            out.append((i / 100, (j - q) / 100)); i = j
        else:
            i += 1
    return [(a, b) for a, b in out if b - a >= 0.3]


def orphans(utt, words, db=None):
    """Voice the first pass left without words: (1) whole utterances with no word, (2) ≥ 0.5 s of clearly voiced
    audio inside an utterance not covered by any word (a retake swallowed in the middle of a sentence)."""
    st = np.array(sorted(w["start"] for w in words))
    res = []
    for a, b in utt:
        k = np.searchsorted(st, a - 0.05)
        if not (k < len(st) and st[k] <= b):
            res.append((a, b))
    if db is not None:
        cov = np.zeros(len(db), bool)
        for w in words:
            cov[max(0, int(w["start"] * 100) - 15):int(w["end"] * 100) + 15] = True
        voiced = db > np.percentile(db, 50) - 10
        gap = voiced & ~cov
        # voice flickers frame to frame: join uncovered bits closer than 0.15 s, keep stretches with ≥ 0.4 s of voice
        idx = np.nonzero(gap)[0]
        runs, cur = [], None
        for k in idx:
            if cur and k - cur[1] <= 15:
                cur[1] = k; cur[2] += 1
            else:
                if cur:
                    runs.append(cur)
                cur = [k, k, 1]
        if cur:
            runs.append(cur)
        for i0, i1, nv in runs:
            if nv >= 40 and not any(a <= i0 / 100 <= b for a, b in res):
                res.append((i0 / 100, (i1 + 1) / 100))
    return sorted(res)


def rescue(x, sr, orph, lang):
    """One Whisper pass over all orphan clips glued with 1.5 s of silence; words mapped back to source time."""
    if not orph:
        return [], []
    import mlx_whisper, mlx.core as mx
    mx.set_cache_limit(256 << 20); mx.set_memory_limit(3 << 30)   # see asr_parakeet_worker.py (swap blow-up 2026-10-09)
    gap, n_s = 1.5, len(x) / sr
    clips, parts, pos = [], [], 0.0
    for a, b in orph:
        a0, b0 = max(0, a - 0.2), min(n_s, b + 0.2)
        seg = x[int(a0 * sr):int(b0 * sr)]
        clips.append((pos, pos + len(seg) / sr, a0, a, b)); pos += len(seg) / sr + gap
        parts += [seg, np.zeros(int(gap * sr), np.float32)]
    r = mlx_whisper.transcribe(np.concatenate(parts), path_or_hf_repo="mlx-community/whisper-large-v3-turbo", language=lang,
                               word_timestamps=True, condition_on_previous_text=False, no_speech_threshold=0.6,
                               temperature=0.0, compression_ratio_threshold=None)
    bw = [wd for s in r.get("segments", []) if s.get("no_speech_prob", 0) < 0.6 for wd in s.get("words", [])]
    added, flags = [], []
    for c0, c1, a0, a, b in clips:
        got = [{"text": wd["word"].strip(), "start": round(wd["start"] - c0 + a0, 3),
                "end": round(min(wd["end"], c1) - c0 + a0, 3), "rescued": True} for wd in bw if c0 - 0.05 <= wd["start"] < c1]
        txt = " ".join(g["text"] for g in got)
        toks = [re.sub(r"\W", "", g["text"].lower()) for g in got]
        bad = HALL.search(txt) or (len(toks) > 3 and max(toks.count(t) for t in set(toks)) > 3) or len(got) > 4 * (b - a) + 3
        if bad:
            got = []
        got = [g for g in got if not any(abs(g["start"] - h["start"]) < 0.35 and g["text"].lower() == h["text"].lower()
                                         for h in added)]          # same spot found by two rules → keep one
        added += got
        flags.append({"start": round(a, 2), "dur": round(b - a, 2), "text": "" if bad else txt})
    return added, flags


def tc(t):
    return f"{int(t // 60):02d}:{t % 60:05.2f}"


def write_md(path, words, flags, src_label):
    rows, cur = [], []
    for i, w in enumerate(words):
        cur.append(w)
        nxt = words[i + 1] if i + 1 < len(words) else None
        if w["text"][-1:] in ".?!…" or nxt is None or nxt["start"] - w["end"] > 0.7:
            rows.append((cur[0]["start"], cur[-1]["end"], " ".join(("⚠" if x.get("rescued") else "") + x["text"] for x in cur)))
            cur = []
    rows += [(f["start"], f["start"] + f["dur"], f"⚠ mowa bez słów ({f['dur']:.1f} s) — nic nie rozpoznano, posłuchaj")
             for f in flags if not f["text"]]                       # rescued text is already inline as ⚠words
    rows.sort()
    md = [f"# Transkrypt surówki ({src_label})", "",
          "⚠ = fragment, który pierwsze rozpoznawanie pominęło (zwykle falstart / powtórka) — sprawdź przy wyborze podejść.", "",
          "| # | od | do | tekst |", "|---|---|---|---|"]
    md += [f"| {k} | {tc(a)} | {tc(b)} | {t} |" for k, (a, b, t) in enumerate(rows)]
    open(path, "w").write("\n".join(md) + "\n")


def main():
    a = sys.argv[1:]
    if len(a) < 2:
        sys.exit(__doc__)
    lang = a[a.index("--lang") + 1] if "--lang" in a else "pl"
    win = float(a[a.index("--window") + 1]) if "--window" in a else 45.0
    src, out = os.path.abspath(a[0]), os.path.abspath(a[1])
    if not os.path.exists(PK_PY):
        print("parakeet-mlx not installed (~/.venvs/parakeet)", file=sys.stderr); sys.exit(3)
    T = {}; t0 = time.time()
    os.makedirs(os.path.join(out, "00_input"), exist_ok=True); os.makedirs(os.path.join(out, "01_cut"), exist_ok=True)
    wav = os.path.join(out, "00_input", "audio16k.wav")
    if not os.path.exists(wav) or os.path.getmtime(wav) < os.path.getmtime(src):
        tmp = wav + ".part.wav"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-vn", "-ac", "1", "-ar", "16000", "-c:a", "pcm_s16le", tmp], check=True)
        os.replace(tmp, wav)
    T["extract_s"] = round(time.time() - t0, 1)
    key = file_key(src, f"{VERSION}|{lang}|{win}|{a[a.index('--passes') + 1] if '--passes' in a else 2}|{'norescue' if '--no-rescue' in a else 'rescue'}")
    cpath = os.path.join(CACHE, key + ".json")
    if os.path.exists(cpath) and "--no-cache" not in a:
        res = json.load(open(cpath)); res["timings"] = {"cache_hit": True, **T, "total_s": round(time.time() - t0, 1)}
    else:
        w = wave.open(wav); sr = w.getframerate()
        x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
        db = envelope(x, sr)
        npass = int(a[a.index("--passes") + 1]) if "--passes" in a else 2
        wins = [windows(db, win)] + ([windows(db, win, first=win / 2)] if npass > 1 else [])
        wp, op = os.path.join(out, "01_cut", ".windows.json"), os.path.join(out, "01_cut", ".parakeet.json")
        json.dump(wins, open(wp, "w"))
        t1 = time.time()
        r = subprocess.run([PK_PY, "-I", os.path.join(HERE, "asr_parakeet_worker.py"), wav, wp, op], capture_output=True, text=True)
        if r.returncode:
            sys.stderr.write(r.stderr[-2000:]); sys.exit(4)
        got = json.load(open(op))
        words, chosen = merge_passes(got, db) if len(wins) > 1 else (got[0] if got and isinstance(got[0], list) else got, [])
        T["parakeet_s"] = round(time.time() - t1, 1)
        T["chunks_from_pass"] = chosen
        flags = []
        if "--no-rescue" not in a:
            t1 = time.time()
            added, flags = rescue(x, sr, orphans(utterances(db), words, db), lang)
            words = sorted(words + added, key=lambda z: z["start"])
            T["rescue_s"] = round(time.time() - t1, 1)
        for p in (wp, op):
            os.remove(p)
        res = {"engine": "parakeet-tdt-0.6b-v3 + whisper rescue", "version": VERSION, "key": key, "src": src,
               "audio_s": round(len(x) / sr, 1), "windows": len(wins), "words": words, "flags": flags}
        os.makedirs(CACHE, exist_ok=True)
        json.dump(res, open(cpath + ".part", "w"), ensure_ascii=False); os.replace(cpath + ".part", cpath)
        res["timings"] = {"cache_hit": False, **T, "total_s": round(time.time() - t0, 1)}
    words, flags = res["words"], res["flags"]
    json.dump([{k: v for k, v in w.items()} for w in words], open(os.path.join(out, "01_cut", "words_raw.json"), "w"),
              ensure_ascii=False, indent=0)
    write_md(os.path.join(out, "01_cut", "transcript_raw.md"), words, flags, res["engine"])
    meta = {k: v for k, v in res.items() if k != "words"}
    json.dump(meta, open(os.path.join(out, "01_cut", "asr_meta.json"), "w"), ensure_ascii=False, indent=1)
    rescued = sum(1 for w in words if w.get("rescued"))
    print(f"{len(words)} words ({rescued} rescued), {len(flags)} ⚠ spots via {res['engine']} · {res['timings']}")


if __name__ == "__main__":
    main()
