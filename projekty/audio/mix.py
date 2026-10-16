#!/usr/bin/env python3
"""Music + SFX mix for a finished ad.  usage: mix.py CUES.json IN.mp4 OUT.mp4
CUES = {"music": path (optional: SFX-only mix without it), "musicStart": s, "musicDb": dB (gain before ducking), "fadeOut": s,
        "musicSegments": [[video_start, video_end, track_offset], ...] (restart the track per section, hard 20-30 ms joins on cuts),
        "duckThreshold": sidechain threshold (default 0.02; lower it for a quiet voice track),
        "sfx": [{"t": s, "f": path, "db": dB, "peak": true, "dur": s}]}
peak=true aligns the loudest point of the sound to t; dur trims the sound (with a 30 ms fade) so it never crosses a hook cut.
Voice ducks the music (sidechain). Measured static gain to -14 LUFS + limiter at -2.5 dBFS (≈ -1.5 dBTP after AAC) for Meta (no pumping on SFX)."""
import json, subprocess, sys
import numpy as np

cues, src, out = json.load(open(sys.argv[1])), sys.argv[2], sys.argv[3]
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", src], capture_output=True, text=True).stdout)
_peaks = {}
ST = "aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo"


def peak(f):  # seconds from file start to its loudest sample
    if f not in _peaks:
        a = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", f, "-ac", "1", "-ar", "8000", "-f", "s16le", "-"], capture_output=True).stdout, np.int16)
        _peaks[f] = float(np.argmax(np.abs(a.astype(np.int32)))) / 8000 if len(a) else 0.0
    return _peaks[f]


ins, mixin = ["-i", src], ["[vo]"]
fc = [f"[0:a]{ST},asplit=2[vo][sc]"]
if cues.get("music"):
    ins += ["-i", cues["music"]]
    segs = cues.get("musicSegments") or [[0, dur, cues.get("musicStart", 0)]]   # [video_start, video_end, track_offset]
    fc.append(f"[1:a]{ST},asplit={len(segs)}" + "".join(f"[m{i}]" for i in range(len(segs))))
    for i, (v0, v1, off) in enumerate(segs):
        v1 = min(v1, dur); fin = 0.4 if i == 0 else 0.02
        fc.append(f"[m{i}]atrim=start={off}:end={off + v1 - v0:.3f},asetpts=PTS-STARTPTS,afade=t=in:d={fin},"
                  f"afade=t=out:st={max(0, v1 - v0 - .03):.3f}:d=0.03,adelay={int(v0 * 1000)}:all=1[ms{i}]")
    fc += ["".join(f"[ms{i}]" for i in range(len(segs))) + f"amix=inputs={len(segs)}:normalize=0:duration=longest,atrim=0:{dur},"
           f"volume={cues.get('musicDb', -18)}dB,afade=t=out:st={dur - cues.get('fadeOut', 1.5):.3f}:d={cues.get('fadeOut', 1.5)}[mu]",
           f"[mu][sc]sidechaincompress=threshold={cues.get('duckThreshold', 0.02)}:ratio=5:attack=15:release=350:makeup=1[duck]"]
    mixin.append("[duck]")
else:
    fc.append("[sc]anullsink")
for s in cues.get("sfx", []):
    k = len(ins) // 2
    ins += ["-i", s["f"]]; t = max(0.0, s["t"] - (peak(s["f"]) if s.get("peak") else 0.0))
    trim = f",atrim=0:{s['dur']:.3f},afade=t=out:st={max(0, s['dur'] - .03):.3f}:d=0.03" if s.get("dur") else ""
    fc.append(f"[{k}:a]{ST}{trim},volume={s.get('db', -10)}dB,adelay={int(t * 1000)}:all=1[s{k}]"); mixin.append(f"[s{k}]")
fc.append("".join(mixin) + f"amix=inputs={len(mixin)}:normalize=0:duration=first[m]")
graph = ";".join(fc)
meas = subprocess.run(["ffmpeg", "-hide_banner", "-y", *ins, "-filter_complex", graph + ";[m]loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json[a]",
                       "-map", "[a]", "-f", "null", "-"], capture_output=True, text=True).stderr
m = json.loads(meas[meas.rindex("{"):meas.rindex("}") + 1])
enc = "aac_at" if "aac_at" in subprocess.run(["ffmpeg", "-hide_banner", "-encoders"], capture_output=True, text=True).stdout else "aac"
# ffmpeg 8.1 native aac overshoots limited material by up to +5 dB; Apple AudioToolbox (aac_at) keeps the ceiling
gain = -14 - float(m["input_i"])                     # static gain to -14 LUFS, then a brickwall limiter for the peaks
subprocess.run(["ffmpeg", "-v", "error", "-y", *ins, "-filter_complex", graph + f";[m]volume={gain:.2f}dB,alimiter=limit=-2.5dB:attack=2:release=60:level=0[a]", "-map", "0:v", "-map", "[a]",
                "-c:v", "copy", "-c:a", enc, "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", out], check=True)
print("wrote", out)
