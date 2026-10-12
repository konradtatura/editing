"""Parakeet TDT 0.6b v3 worker — runs inside ~/.venvs/parakeet (parakeet-mlx). Called by asr.py, not by hand.
usage: asr_parakeet_worker.py WAV16K WINDOWS.json OUT.json
WINDOWS.json = [[start_s, end_s], ...] cut at silences by asr.py, or a list of such lists (several passes with shifted
window edges, model loaded once) → OUT.json is then a list of word lists. Each window is transcribed on its own (no overlap
merging: parakeet-mlx's own chunk merge can fuse a repeated take into one). Writes [{"text","start","end"}]."""
import json, os, sys, tempfile, wave
import numpy as np
import mlx.core as mx
from parakeet_mlx import from_pretrained

# 2026-10-09: on a busy 16 GB Mac an uncapped MLX buffer cache pushed swap from 7.5 to 14 GB (disk nearly full).
# Cap the allocator and drop the cache after every window; peak stays ~1–2 GB.
mx.set_cache_limit(256 << 20)
mx.set_memory_limit(3 << 30)
wav, win_p, out = sys.argv[1:4]
w = wave.open(wav); sr = w.getframerate()
x = np.frombuffer(w.readframes(w.getnframes()), np.int16)
model = from_pretrained("mlx-community/parakeet-tdt-0.6b-v3")
tmp = tempfile.mkdtemp()
PAD = 2.0          # context on both sides; words are kept only if they START inside the window's own [a, b)
total = len(x) / sr
spec = json.load(open(win_p))
passes = spec if spec and isinstance(spec[0][0], list) else [spec]       # one window list per pass
result = []
for windows_ in passes:
    words = []
    for a, b in windows_:
        a0, b0 = max(0.0, a - PAD), min(total, b + PAD)
        p = os.path.join(tmp, "w.wav")
        with wave.open(p, "wb") as o:
            o.setnchannels(1); o.setsampwidth(2); o.setframerate(sr); o.writeframes(x[int(a0 * sr):int(b0 * sr)].tobytes())
        got, cur = [], None
        for s in model.transcribe(p).sentences:
            for tk in s.tokens:
                if cur is None or tk.text.startswith(" "):
                    if cur and cur["text"]:
                        got.append(cur)
                    cur = {"text": tk.text.strip(), "start": round(tk.start + a0, 3), "end": round(tk.end + a0, 3)}
                else:
                    cur["text"] += tk.text; cur["end"] = round(tk.end + a0, 3)
        if cur and cur["text"]:
            got.append(cur)
        words += [w for w in got if a <= w["start"] < b]       # time-based hand-over: no text merging, no lost edge words
        mx.clear_cache()
        print(f"peak {mx.get_peak_memory() / 1e9:.2f} GB  window {a:.1f}-{b:.1f}: {len(words)} words", file=sys.stderr, flush=True)
    result.append(words)
json.dump(result if len(passes) > 1 else result[0], open(out, "w"), ensure_ascii=False)
