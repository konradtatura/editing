#!/usr/bin/env python3
"""Rebuild the SFX folder from a sources list (Openverse CC0 links), peak-normalised to -1 dBFS mono 48 kHz WAV.
usage: fetch_sfx.py sources_ad12.json OUTDIR"""
import json, os, subprocess, sys
import numpy as np
src, out = json.load(open(sys.argv[1])), sys.argv[2]
os.makedirs(out, exist_ok=True)
for k, r in src.items():
    tmp = os.path.join(out, k + ".src")
    subprocess.run(["curl", "-s", "-L", "-o", tmp, r["file"]], check=True)
    a = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", tmp, "-ac", "1", "-ar", "48000", "-f", "s16le", "-"], capture_output=True).stdout, np.int16)
    pk = 20 * np.log10(np.abs(a.astype(int)).max() / 32768)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", tmp, "-ac", "1", "-ar", "48000", "-af", f"volume={-1 - pk:.2f}dB", os.path.join(out, k + ".wav")], check=True)
    os.remove(tmp)
print(len(src), "sfx in", out)
