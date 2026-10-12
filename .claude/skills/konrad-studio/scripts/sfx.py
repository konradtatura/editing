#!/usr/bin/env python3
"""Sound design layer: a cue sheet → one WAV (to hand over as a separate track) and optionally a mixed MP4.

usage: sfx.py CUES.json OUT.wav --dur SEC [--mix VIDEO.mp4 OUT.mp4]
CUES.json: [{"t": 12.40, "sfx": "click", "db": -26}, {"t": 15.02, "sfx": "pop", "db": -29}, ...]
  "sfx" = a name from assets/sfx (click, pop, tick, whoosh, swish) or a path to any wav.
  Times come from the word timestamps (the same `sc.word()` moments the animation lands on) — never hand-typed seconds.
Level guide (voice ≈ −16 LUFS): UI click/press −26…−28, pop on a landing −28…−31, tick on counters −30, whoosh on a
transition −27…−31 (sparingly), nothing louder than the voice. The mix uses alimiter level=false (otherwise it re-boosts
the whole mix) and checks true peak < −1 dBTP on the final file.
"""
import json, os, subprocess, sys
import numpy as np

SK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SR = 48000


def load(path):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, 2)


def main():
    a = sys.argv[1:]
    if len(a) < 2 or "--dur" not in a:
        sys.exit(__doc__)
    cues = json.load(open(a[0]))
    out = a[1]
    dur = float(a[a.index("--dur") + 1])
    buf = np.zeros((int(dur * SR) + SR, 2), np.float32)
    cache = {}
    for c in cues:
        name = c["sfx"]
        p = name if os.path.exists(name) else os.path.join(SK, "assets", "sfx", name + ".wav")
        if p not in cache:
            x = load(p)
            pk = np.abs(x).max() or 1
            cache[p] = x / pk                       # normalise to 0 dBFS peak, then apply the cue gain
        x = cache[p] * (10 ** (c.get("db", -28) / 20))
        i = int(c["t"] * SR)
        n = min(len(x), len(buf) - i)
        if n > 0:
            buf[i:i + n] += x[:n]
    buf = buf[:int(dur * SR)]
    pcm = (np.clip(buf, -1, 1) * 32767).astype("<i2")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "s16le", "-ar", str(SR), "-ac", "2", "-i", "-", out],
                   input=pcm.tobytes(), check=True)
    print(f"{out}: {len(cues)} cues, peak {20 * np.log10(np.abs(buf).max() + 1e-9):.1f} dBFS")
    if "--mix" in a:
        i = a.index("--mix"); video, mixed = a[i + 1], a[i + 2]
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", video, "-i", out, "-filter_complex",
                        "[0:a][1:a]amix=inputs=2:normalize=0:duration=first,alimiter=limit=0.84:level=false[a]",
                        "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart",
                        mixed], check=True)
        r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", mixed, "-af", "ebur128=peak=true", "-f", "null", "-"],
                           capture_output=True, text=True).stderr
        print("mixed", mixed, [l.strip() for l in r.splitlines() if l.strip().startswith(("I:", "Peak:"))][-2:])


if __name__ == "__main__":
    main()
