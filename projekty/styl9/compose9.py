#!/usr/bin/env python3
"""Style 9 compositor: source video + 0.2 s blur-in on spec["blurCuts"] + overlay PNG frames (+ original audio).
usage: compose9.py SPEC.json SRC.mp4 FRAMES_DIR OUT.mp4"""
import json, subprocess, sys
spec, src, frames, out = json.load(open(sys.argv[1])), sys.argv[2], sys.argv[3], sys.argv[4]
win = lambda a, b: "+".join(f"between(t,{c + a:.3f},{c + b:.3f})" for c in spec.get("blurCuts", [])) or "0"
vf = (f"[0:v]gblur=sigma=22:enable='{win(0, .1)}',gblur=sigma=9:enable='{win(.1, .2)}',gblur=sigma=3:enable='{win(.2, .27)}'[v];"
      f"[v][1]overlay=format=auto:eof_action=pass,format=yuv420p")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-framerate", str(spec.get("fps", 30)), "-i", f"{frames}/f_%05d.png",
                "-filter_complex", vf, "-map", "0:a", "-c:v", "libx264", "-crf", "16", "-preset", "medium", "-c:a", "aac", "-b:a", "192k", out], check=True)
print("wrote", out)
