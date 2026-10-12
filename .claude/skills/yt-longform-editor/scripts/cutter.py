#!/usr/bin/env python3
"""Turn the approved keep-list (01_cut/takes.json) into a clean, listenable rough cut.

usage:
  cutter.py build  <film_dir>               # takes.json -> edl.json (edges snapped to the voice, pauses tightened)
  cutter.py render <film_dir> [--jobs 6]    # edl.json -> rough_cut.mp4 + words_cut.json + transcript_cut.md + cutmap.json

takes.json:
  {"sources": {"A": "/abs/raw.mp4"},          # optional; default A = 00_input/raw.* given at render
   "takes": [{"src": "A", "start": 32.86, "end": 42.56, "note": "..."}],
   "pause_max": 0.24, "pause_keep": 0.14}     # optional overrides

Rules (from the approved VSL cut): edges snap to the audio envelope (breaths before a take are cut,
soft consonants at the start are protected), silences > pause_max inside a take are shortened to
pause_keep, every segment gets 30 ms audio fades, nothing is cut inside a word.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import wave
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import numpy as np

PRE, POST = 0.045, 0.065
PAUSE_DB = -50.0
FADE = 0.03


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        sys.stderr.write(r.stderr[-3000:])
        raise SystemExit(f"failed: {' '.join(map(str, cmd))[:200]}")
    return r


class Src:
    def __init__(self, key: str, video: Path, wav: Path, words: list[dict]):
        self.key, self.video, self.words = key, video, words
        w = wave.open(str(wav))
        x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
        hop = w.getframerate() // 100            # 10 ms frames
        n = len(x) // hop
        self.db = 20 * np.log10(np.sqrt((x[: n * hop].reshape(n, hop) ** 2).mean(1)) + 1e-9)
        self.thr = np.percentile(self.db, 15) + 10    # "something is sounding"
        self.hi = np.percentile(self.db, 50) - 10     # "voiced"

    def lv(self, t):
        i = int(t * 100)
        return self.db[i] if 0 <= i < len(self.db) else -120

    def loud(self, t, voiced=False):
        return self.lv(t) > (self.hi + 8 if voiced else self.thr)

    def neighbours(self, a, b):
        pe = max([w["end"] for w in self.words if w["end"] <= a + 0.02] or [0])
        ns = min([w["start"] for w in self.words if w["start"] >= b - 0.02] or [1e9])
        return pe, ns

    def onset(self, a, lo):
        i0, i1 = int(max(lo, a - 0.15) * 100), int((a + 0.08) * 100)
        if i1 <= i0:
            return a
        m = i0 + int(np.argmin(self.db[i0:i1]))
        voiced_before = sum(1 for k in range(int(a * 100), m) if self.db[k] > self.hi + 6)
        if self.db[m] < self.hi and voiced_before < 4:
            t = m / 100
            while t < a + 0.2 and not self.loud(t, True):
                t += 0.01
            lo = max(lo, m / 100)
        else:
            t = a
        if not self.loud(t, True):
            while t < a + 0.2 and not self.loud(t, True):
                t += 0.01
        else:
            while t - 0.01 > lo and self.loud(t - 0.01, True):
                t -= 0.01
        k = 0
        while k < 6 and t - 0.01 > lo and self.loud(t - 0.01):    # soft consonant attack (<= 60 ms)
            t -= 0.01; k += 1
        return t

    def offset(self, b, hi):
        t = b - 0.05
        while t < min(hi, b + 0.25) and self.loud(t):
            t += 0.01
        return t


def build(film: Path) -> None:
    cfg = json.loads((film / "01_cut" / "takes.json").read_text())
    pmax, pkeep = cfg.get("pause_max", 0.24), cfg.get("pause_keep", 0.14)
    sources = cfg.get("sources") or {}
    raw = next((p for p in (film / "00_input").glob("raw.*")), None)
    if "A" not in sources:
        if not raw:
            raise SystemExit("put the recording at 00_input/raw.mp4 or list it in takes.json 'sources'")
        sources["A"] = str(raw)
    srcs: dict[str, Src] = {}
    for k, v in sources.items():
        wav = film / "00_input" / ("audio16k.wav" if k == "A" else f"audio16k_{k}.wav")
        wfile = film / "01_cut" / ("words_raw.json" if k == "A" else f"words_raw_{k}.json")
        if not wav.exists():
            run(["ffmpeg", "-v", "error", "-y", "-i", v, "-vn", "-ac", "1", "-ar", "16000", "-c:a", "pcm_s16le", str(wav)])
        srcs[k] = Src(k, Path(v), wav, json.loads(wfile.read_text()) if wfile.exists() else [])

    ranges, log = [], []
    for tk in cfg["takes"]:
        S = srcs[tk.get("src", "A")]
        a, b = float(tk["start"]), float(tk["end"])
        pe, ns = S.neighbours(a, b)
        # never start after the first word / end before the last word (protects soft consonants like "S", "f", "ch")
        s = max(min(S.onset(a, pe + 0.03) - PRE, a - 0.03), pe + 0.01)
        e = min(max(S.offset(b, ns - 0.03) + POST, b + 0.04), ns - 0.01)
        if e - s < 0.2:
            s, e = a - PRE, b + POST
        i0, i1 = int(round(s * 100)), int(round(e * 100))
        seg = S.db[i0:i1]
        inword = np.zeros(i1 - i0, bool)
        for w in S.words:
            a_, b_ = int(w["start"] * 100) - i0, int(w["end"] * 100) - i0
            if b_ >= 0 and a_ < i1 - i0:
                inword[max(0, a_):max(0, min(i1 - i0, b_))] = True
        sp = [not (seg[k] < PAUSE_DB or (seg[k] < -40 and not inword[k])) for k in range(len(seg))]
        first = next((k for k in range(len(seg)) if seg[k] > -40), 0)
        while first > 0 and seg[first - 1] > PAUSE_DB:
            first -= 1
        last = next((k for k in range(len(seg) - 1, -1, -1) if seg[k] > -40), len(seg) - 1)
        while last < len(seg) - 1 and seg[last + 1] > PAUSE_DB:
            last += 1
        keep_from = max(0, first - 5) / 100 + s
        keep_to = min(len(sp), last + 1 + 7) / 100 + s
        # the -40 dB trim must never eat into the first/last word of the take
        keep_from = max(s, min(keep_from, a - 0.03))
        keep_to = min(e, max(keep_to, b + 0.04))
        parts, cur, k = [], keep_from, first
        while k <= last:
            if not sp[k]:
                j = k
                while j <= last and not sp[j]:
                    j += 1
                gap = (j - k) / 100
                if gap > pmax:
                    half = pkeep / 2
                    parts.append((cur, s + k / 100 + half)); cur = s + j / 100 - half
                    log.append(f"   pauza {gap*1000:.0f} ms @ {S.key}{s + k/100:.2f} → {pkeep*1000:.0f} ms")
                k = j
            else:
                k += 1
        parts.append((cur, keep_to))
        for p0, p1 in parts:
            if p1 - p0 > 0.05:
                ranges.append({"source": S.key, "start": round(p0, 3), "end": round(p1, 3), "note": tk.get("note", "")})
        log.append(f"{S.key} {keep_from:8.2f}–{keep_to:8.2f}  {tk.get('note', '')[:70]}")
    total = sum(r["end"] - r["start"] for r in ranges)
    (film / "01_cut" / "edl.json").write_text(json.dumps({"sources": {k: str(v.video) for k, v in srcs.items()}, "ranges": ranges},
                                                          ensure_ascii=False, indent=1))
    print("\n".join(log))
    print(f"segments {len(ranges)}  runtime {total:.1f}s  → 01_cut/edl.json")


def render(film: Path, jobs: int) -> None:
    edl = json.loads((film / "01_cut" / "edl.json").read_text())
    segdir = film / "01_cut" / "_segs"
    segdir.mkdir(exist_ok=True)
    for f in segdir.glob("*.mp4"):
        f.unlink()

    def one(i_r):
        i, r = i_r
        d = r["end"] - r["start"]
        out = segdir / f"{i:04d}.mp4"
        run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-ss", f"{r['start']:.3f}", "-i", edl["sources"][r["source"]], "-t", f"{d:.3f}",
             "-map", "0:v:0", "-map", "0:a:0", "-af", f"afade=t=in:st=0:d={FADE},afade=t=out:st={max(0, d - FADE):.3f}:d={FADE}",
             "-c:v", "libx264", "-preset", "slow", "-crf", "14", "-pix_fmt", "yuv420p", "-r", "30",
             "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
             "-c:a", "aac", "-b:a", "256k", "-ar", "48000", str(out)])
        return out

    with ThreadPoolExecutor(max_workers=jobs) as ex:
        outs = list(ex.map(one, enumerate(edl["ranges"])))
    lst = segdir / "concat.txt"
    lst.write_text("".join(f"file '{o.name}'\n" for o in outs))
    rough = film / "01_cut" / "rough_cut.mp4"
    run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", "-movflags", "+faststart", str(rough)])

    # remap words onto the cut timeline (use the real segment durations to avoid drift)
    words = {}
    for k in edl["sources"]:
        wf = film / "01_cut" / ("words_raw.json" if k == "A" else f"words_raw_{k}.json")
        words[k] = json.loads(wf.read_text()) if wf.exists() else []
    cut_words, cutmap, t = [], [], 0.0
    for r, o in zip(edl["ranges"], outs):
        d = float(run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(o)]).stdout.strip())
        cutmap.append({"cut_start": round(t, 3), "cut_end": round(t + d, 3), "source": r["source"], "src_start": r["start"], "src_end": r["end"]})
        for w in words[r["source"]]:
            ov = min(w["end"], r["end"]) - max(w["start"], r["start"])
            if ov > 0 and ov >= 0.4 * max(0.01, w["end"] - w["start"]):
                cut_words.append({"text": w["text"], "start": round(max(0, w["start"] - r["start"]) + t, 3),
                                  "end": round(min(d, w["end"] - r["start"]) + t, 3)})
        t += d
    (film / "01_cut" / "words_cut.json").write_text(json.dumps(cut_words, ensure_ascii=False, indent=0))
    (film / "01_cut" / "cutmap.json").write_text(json.dumps(cutmap, indent=1))
    # readable transcript of the cut, one sentence per line with timecodes
    lines, cur = [], []
    for i, w in enumerate(cut_words):
        cur.append(w)
        nxt = cut_words[i + 1] if i + 1 < len(cut_words) else None
        if w["text"][-1:] in ".?!…" or nxt is None or nxt["start"] - w["end"] > 0.6:
            lines.append(f"| {cur[0]['start']:.2f} | {cur[-1]['end']:.2f} | {' '.join(x['text'] for x in cur)} |")
            cur = []
    (film / "01_cut" / "transcript_cut.md").write_text("# Transkrypt po cięciu\n\n| od | do | tekst |\n|---|---|---|\n" + "\n".join(lines) + "\n")
    print(f"rough cut {t:.1f}s, {len(outs)} segments → 01_cut/rough_cut.mp4 (+ words_cut.json, transcript_cut.md)")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["build", "render"])
    ap.add_argument("film_dir")
    ap.add_argument("--jobs", type=int, default=6)
    a = ap.parse_args()
    film = Path(a.film_dir).resolve()
    build(film) if a.cmd == "build" else render(film, a.jobs)


if __name__ == "__main__":
    main()
