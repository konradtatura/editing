#!/usr/bin/env python3
"""Word-level transcript of a video (mlx_whisper large-v3-turbo, Polish by default).

usage: transcribe.py VIDEO OUT_DIR [--lang pl] [--name words]
writes OUT_DIR/<name>.json  (whisper format: segments[].words[] with start/end/word)
       OUT_DIR/<name>.txt   (one segment per line: "MM:SS.ss  text"  — read this to plan)
Whisper loops at the very end of a file ("Zmieni coś dopiero." ×50) — those zero-length repeats are dropped.
Whisper is NOT verbatim: it skips restarts/retakes. For cutting raw takes prefer a verbatim transcript
(ElevenLabs Scribe JSON if Konrad sends one); for animating/captioning an already-cut film whisper is perfect.
"""
import json, os, subprocess, sys

PY = "/Library/Frameworks/Python.framework/Versions/3.13/bin"


def main():
    a = sys.argv[1:]
    if len(a) < 2:
        sys.exit(__doc__)
    video, out = a[0], a[1]
    lang = a[a.index("--lang") + 1] if "--lang" in a else "pl"
    name = a[a.index("--name") + 1] if "--name" in a else "words"
    os.makedirs(out, exist_ok=True)
    wav = os.path.join(out, name + ".wav")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", video, "-ac", "1", "-ar", "16000", wav], check=True)
    exe = os.path.join(PY, "mlx_whisper")
    if not os.path.exists(exe):
        exe = "mlx_whisper"
    subprocess.run([exe, wav, "--model", "mlx-community/whisper-large-v3-turbo", "--language", lang,
                    "--word-timestamps", "True", "--output-format", "json", "--output-dir", out,
                    "--output-name", name], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    p = os.path.join(out, name + ".json")
    r = json.load(open(p))
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", video],
                               capture_output=True, text=True).stdout)
    segs, seen_tail = [], set()
    for s in r["segments"]:
        txt = s["text"].strip()
        if s["end"] - s["start"] < 0.05 and s["start"] > dur - 3:      # end-of-file hallucination loop
            continue
        if s["start"] > dur - 3 and txt in seen_tail:
            continue
        seen_tail.add(txt)
        segs.append(s)
    r["segments"] = segs
    json.dump(r, open(p, "w"), ensure_ascii=False)
    with open(os.path.join(out, name + ".txt"), "w") as f:
        for s in segs:
            m, sec = divmod(s["start"], 60)
            f.write(f"{int(m):02d}:{sec:05.2f}  {s['text'].strip()}\n")
    os.remove(wav)
    print(f"{len(segs)} segments, {sum(len(s.get('words', [])) for s in segs)} words → {p}")


if __name__ == "__main__":
    main()
