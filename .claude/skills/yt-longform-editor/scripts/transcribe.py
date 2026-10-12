#!/usr/bin/env python3
"""Word-level transcript of the raw recording (Polish by default).

usage:
  transcribe.py <raw.mp4> <film_dir> [--lang pl] [--import transcript.json] [--prompt-from skrypt.md]

Writes:
  <film_dir>/00_input/audio16k.wav      mono 16 kHz (also used by the cutter's audio envelope)
  <film_dir>/01_cut/words_raw.json      [{"text","start","end"}...]  (words only)
  <film_dir>/01_cut/transcript_raw.md   sentences with timecodes (for reading / picking takes)

Engines, in order: --import (…) → konrad-studio/scripts/asr.py (Parakeet v3 via parakeet-mlx on silence windows +
Polish Whisper rescue of skipped false starts, cached; 2026-10-09: 23 min in ~2–3 min) → --import (ElevenLabs Scribe JSON, Whisper JSON, or a plain word array) →
Parakeet TDT v3 via `npx hyperframes transcribe -e parakeet` (verbatim: keeps every retake, no invented
words, ~20x realtime — the right engine for cutting) → mlx-whisper large-v3-turbo per utterance (fallback;
Whisper tends to skip repeated attempts and invent words in silence, so the cut needs extra review).
"""
from __future__ import annotations

import argparse
import glob
import json
import subprocess
import sys
from pathlib import Path

KS_ASR = Path.home() / ".claude/skills/konrad-studio/scripts/asr.py"
MLX_PYS = sorted(glob.glob("/Library/Frameworks/Python.framework/Versions/*/bin/python3")) + \
    ["/opt/homebrew/bin/python3", "python3"]


def run(cmd, **kw):
    r = subprocess.run(cmd, capture_output=True, text=True, **kw)
    if r.returncode != 0:
        sys.stderr.write(r.stderr[-3000:])
        raise SystemExit(f"failed: {' '.join(map(str, cmd))[:200]}")
    return r


def normalize(obj) -> list[dict]:
    """Accept ElevenLabs Scribe, Whisper(-X/mlx) segments, or a flat word list."""
    if isinstance(obj, dict) and "words" in obj and isinstance(obj["words"], list):
        ws = obj["words"]
        if ws and "type" in ws[0]:          # ElevenLabs: word / spacing / audio_event
            ws = [w for w in ws if w.get("type") == "word"]
    elif isinstance(obj, dict) and "segments" in obj:
        ws = [w for s in obj["segments"] for w in s.get("words", [])]
    elif isinstance(obj, list):
        ws = obj
    else:
        raise SystemExit("unknown transcript format")
    out = []
    for w in ws:
        t = (w.get("text") or w.get("word") or "").strip()
        if not t or w.get("start") is None or w.get("end") is None:
            continue
        out.append({"text": t, "start": round(float(w["start"]), 3), "end": round(float(w["end"]), 3)})
    return out


def mlx_python() -> str | None:
    for p in MLX_PYS:
        r = subprocess.run([p, "-c", "import mlx_whisper"], capture_output=True)
        if r.returncode == 0:
            return p
    return None


def utterances(wav: Path, min_sil: float = 0.28, pad: float = 0.12, max_len: float = 14.0) -> list[tuple[float, float]]:
    """Split the recording at silences. Whisper skips repeated attempts inside one long window
    (it writes one 7-second word over four retakes) — transcribing each utterance on its own prevents that."""
    import wave
    import numpy as np
    w = wave.open(str(wav))
    x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
    hop = 160
    nfr = len(x) // hop
    db = 20 * np.log10(np.sqrt((x[: nfr * hop].reshape(nfr, hop) ** 2).mean(1)) + 1e-9)
    thr = np.percentile(db, 15) + 10
    speech = db > thr
    segs, i = [], 0
    while i < nfr:
        if speech[i]:
            j = i
            quiet = 0
            while j < nfr and quiet < int(min_sil * 100):
                quiet = quiet + 1 if not speech[j] else 0
                j += 1
            segs.append([max(0, i / 100 - pad), min(nfr / 100, (j - quiet) / 100 + pad)])
            i = j
        else:
            i += 1
    out = []
    for s, e in segs:
        if e - s < 0.25:
            continue
        while e - s > max_len:                     # very long run without a pause: split hard
            out.append((s, s + max_len)); s += max_len
        out.append((s, e))
    return out


def via_mlx(py: str, wav: Path, lang: str, prompt: str) -> list[dict]:
    clips = utterances(wav)
    code = (
        "import json,sys,wave,numpy as np,mlx_whisper\n"
        "w=wave.open(sys.argv[1]);x=np.frombuffer(w.readframes(w.getnframes()),np.int16).astype(np.float32)/32768\n"
        "clips=json.loads(sys.argv[4]);out=[]\n"
        "for s,e in clips:\n"
        "  a=x[int(s*16000):int(e*16000)]\n"
        "  r=mlx_whisper.transcribe(a,path_or_hf_repo='mlx-community/whisper-large-v3-turbo',language=sys.argv[2],"
        "word_timestamps=True,initial_prompt=(sys.argv[3] or None),condition_on_previous_text=False,no_speech_threshold=0.6)\n"
        "  for seg in r.get('segments',[]):\n"
        "    for wd in seg.get('words',[]):\n"
        "      out.append({'text':wd['word'],'start':wd['start']+s,'end':wd['end']+s})\n"
        "print(json.dumps(out,ensure_ascii=False))\n"
    )
    r = run([py, "-c", code, str(wav), lang, prompt[:400], json.dumps(clips)])
    return normalize(json.loads(r.stdout))


def via_parakeet(wav: Path, work: Path, lang: str) -> list[dict] | None:
    r = subprocess.run(["npx", "hyperframes", "transcribe", str(wav), "-d", str(work), "--json", "-e", "parakeet", "-l", lang],
                       capture_output=True, text=True)
    if r.returncode != 0 or '"engine":"parakeet"' not in r.stdout.replace(" ", ""):
        return None
    return normalize(json.loads((work / "transcript.json").read_text()))


def sentences(words: list[dict], gap: float = 0.7) -> list[dict]:
    out, cur = [], []
    for i, w in enumerate(words):
        cur.append(w)
        nxt = words[i + 1] if i + 1 < len(words) else None
        end_punct = w["text"][-1:] in ".?!…"
        long_gap = nxt is not None and nxt["start"] - w["end"] > gap
        if end_punct or long_gap or nxt is None:
            out.append({"start": cur[0]["start"], "end": cur[-1]["end"], "text": " ".join(x["text"] for x in cur),
                        "i0": i - len(cur) + 1, "i1": i})
            cur = []
    return out


def tc(t: float) -> str:
    return f"{int(t // 60):02d}:{t % 60:05.2f}"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("raw")
    ap.add_argument("film_dir")
    ap.add_argument("--lang", default="pl")
    ap.add_argument("--import", dest="imp")
    ap.add_argument("--prompt-from", help="script file: names/terms help the recogniser")
    ap.add_argument("--no-fast", action="store_true", help="skip konrad-studio asr.py (Parakeet-mlx + rescue)")
    a = ap.parse_args()
    film = Path(a.film_dir).resolve()
    (film / "00_input").mkdir(parents=True, exist_ok=True)
    (film / "01_cut").mkdir(parents=True, exist_ok=True)
    wav = film / "00_input" / "audio16k.wav"
    run(["ffmpeg", "-v", "error", "-y", "-i", a.raw, "-vn", "-ac", "1", "-ar", "16000", "-c:a", "pcm_s16le", str(wav)])
    prompt = Path(a.prompt_from).read_text()[:600] if a.prompt_from else ""
    if a.imp:
        words = normalize(json.loads(Path(a.imp).read_text()))
        src = f"import:{Path(a.imp).name}"
    elif KS_ASR.exists() and not a.no_fast:
        # 2026-10-09: Parakeet v3 (parakeet-mlx) + Polish Whisper rescue, cached — 23 min of raw in ~2–3 min, keeps retakes.
        # It writes the same files (words_raw.json, transcript_raw.md with ⚠ spots); exit code ≠ 0 → older engines below.
        py313 = "/Library/Frameworks/Python.framework/Versions/3.13/bin/python3"     # has numpy + mlx_whisper
        r = subprocess.run([py313 if Path(py313).exists() else sys.executable, str(KS_ASR), a.raw, str(film), "--lang", a.lang])
        if r.returncode == 0:
            return
        words = None
    if not a.imp and (not KS_ASR.exists() or a.no_fast or words is None):
        words = via_parakeet(wav, film / "01_cut", a.lang)
        src = "parakeet-tdt-0.6b-v3"
        if words is None:
            py = mlx_python()
            if not py:
                raise SystemExit("no ASR engine: run `npx hyperframes models install parakeet`")
            words, src = via_mlx(py, wav, a.lang, prompt), "mlx-whisper large-v3-turbo (fallback — review the cut carefully)"
    (film / "01_cut" / "words_raw.json").write_text(json.dumps(words, ensure_ascii=False, indent=0))
    sents = sentences(words)
    md = [f"# Transkrypt surówki ({src})", "", "| # | od | do | tekst |", "|---|---|---|---|"]
    md += [f"| {n} | {tc(s['start'])} | {tc(s['end'])} | {s['text']} |" for n, s in enumerate(sents)]
    (film / "01_cut" / "transcript_raw.md").write_text("\n".join(md) + "\n")
    print(f"{len(words)} words, {len(sents)} sentences via {src}")


if __name__ == "__main__":
    main()
