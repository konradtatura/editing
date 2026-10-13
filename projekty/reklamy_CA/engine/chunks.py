#!/usr/bin/env python3
"""Verbatim-ish chunk transcript for cutting raw takes.
Splits speech on silences (energy), transcribes every chunk separately (so Whisper can't merge retakes),
writes OUT.json [{i,s,e,text,words:[{w,s,e}]}] and prints one line per chunk.
usage: chunks.py VIDEO OUT.json [--model medium] [--gap 0.35]"""
import json, subprocess, sys
import numpy as np
from faster_whisper import WhisperModel
a = sys.argv[1:]; src, out = a[0], a[1]
model = a[a.index("--model") + 1] if "--model" in a else "medium"
GAP = float(a[a.index("--gap") + 1]) if "--gap" in a else 0.35
SR = 16000
pcm = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", src, "-ac", "1", "-ar", str(SR), "-f", "s16le", "-"],
                                   capture_output=True).stdout, np.int16).astype(np.float32) / 32768
hop = int(0.02 * SR)
rms = np.sqrt(np.convolve(pcm ** 2, np.ones(hop) / hop, "same")[::hop] + 1e-12)
db = 20 * np.log10(rms)
floor = np.percentile(db, 10); thr = max(floor + 12, -45)
speech = db > thr
segs, i, n = [], 0, len(speech)
while i < n:
    if speech[i]:
        j = i
        while j < n and speech[j]: j += 1
        segs.append([i * 0.02, j * 0.02]); i = j
    else: i += 1
merged = []
for s, e in segs:
    if merged and s - merged[-1][1] < GAP: merged[-1][1] = e
    else: merged.append([s, e])
merged = [m for m in merged if m[1] - m[0] > 0.18]
m = WhisperModel(model, device="cpu", compute_type="int8")
res = []
for k, (s, e) in enumerate(merged):
    s0, e0 = max(0, s - 0.15), min(len(pcm) / SR, e + 0.15)
    seg, _ = m.transcribe(pcm[int(s0 * SR):int(e0 * SR)], language="pl", word_timestamps=True,
                          condition_on_previous_text=False, vad_filter=False, beam_size=5)
    words, text = [], []
    for sg in seg:
        text.append(sg.text.strip())
        words += [{"w": w.word.strip(), "s": round(s0 + w.start, 3), "e": round(s0 + w.end, 3)} for w in sg.words]
    r = {"i": k, "s": round(s, 3), "e": round(e, 3), "text": " ".join(text), "words": words}
    res.append(r); print(f"[{k:3d}] {s:7.2f}-{e:7.2f}  {r['text']}", flush=True)
json.dump(res, open(out, "w"), ensure_ascii=False, indent=0)
print(f"thr {thr:.1f} dB, {len(res)} chunks")
