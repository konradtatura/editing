#!/usr/bin/env python3
"""Music + SFX mix for a finished ad.  usage: mix.py CUES.json IN.mp4 OUT.mp4
CUES = {"music": path, "musicStart": s, "musicDb": dB (gain before ducking), "fadeOut": s,
        "sfx": [{"t": s, "f": path, "db": dB, "peak": true}]}   peak=true aligns the loudest point of the sound to t.
Voice ducks the music (sidechain), everything is normalised to -14 LUFS / -1.5 dBTP for Meta."""
import json, subprocess, sys
import numpy as np

cues, src, out = json.load(open(sys.argv[1])), sys.argv[2], sys.argv[3]
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", src], capture_output=True, text=True).stdout)
_peaks = {}


def peak(f):  # seconds from file start to its loudest sample
    if f not in _peaks:
        a = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", f, "-ac", "1", "-ar", "8000", "-f", "s16le", "-"], capture_output=True).stdout, np.int16)
        _peaks[f] = float(np.argmax(np.abs(a.astype(np.int32)))) / 8000 if len(a) else 0.0
    return _peaks[f]


ins = ["-i", src, "-i", cues["music"]]
fc = [f"[0:a]aresample=48000,asplit=2[vo][sc]",
      f"[1:a]aresample=48000,atrim=start={cues.get('musicStart', 0)},asetpts=PTS-STARTPTS,atrim=0:{dur},volume={cues.get('musicDb', -18)}dB,"
      f"afade=t=in:d=0.4,afade=t=out:st={dur - cues.get('fadeOut', 1.5):.3f}:d={cues.get('fadeOut', 1.5)}[mu]",
      "[mu][sc]sidechaincompress=threshold=0.02:ratio=5:attack=15:release=350:makeup=1[duck]"]
mixin = ["[vo]", "[duck]"]
for k, s in enumerate(cues.get("sfx", [])):
    ins += ["-i", s["f"]]; t = max(0.0, s["t"] - (peak(s["f"]) if s.get("peak") else 0.0))
    fc.append(f"[{k + 2}:a]aresample=48000,volume={s.get('db', -10)}dB,adelay={int(t * 1000)}:all=1[s{k}]"); mixin.append(f"[s{k}]")
fc.append("".join(mixin) + f"amix=inputs={len(mixin)}:normalize=0:duration=first,loudnorm=I=-14:TP=-1.5:LRA=11[a]")
subprocess.run(["ffmpeg", "-v", "error", "-y", *ins, "-filter_complex", ";".join(fc), "-map", "0:v", "-map", "[a]",
                "-c:v", "copy", "-c:a", "aac", "-b:a", "128k", "-ar", "48000", "-movflags", "+faststart", out], check=True)
print("wrote", out)
