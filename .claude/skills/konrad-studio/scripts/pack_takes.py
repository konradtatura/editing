#!/usr/bin/env python3
"""Pack verbatim word transcripts into readable phrases so every take/retake is visible side by side.

usage: pack_takes.py OUT.md TRANSCRIPT.json [TRANSCRIPT2.json ...] [--gap 0.5]
Each transcript = asr.py words_raw.json (list), ElevenLabs Scribe json (words[] with type) or whisper json (segments[].words[]).
⚠word = recovered by asr.py's rescue pass (a false start / retake the first pass missed).
Output lines:  [start-end] KEY  text     (KEY = L1, L2… per file; a new line starts after a pause > --gap s)
Read the whole file next to the script, then write takes.json for cut_takes.py.
Long single "words" (> 1.5 s) are flagged ⚠ — Scribe sometimes hides a retake inside one long word.
"""
import json, os, sys


def words(p):
    d = json.load(open(p))
    if isinstance(d, list):                          # asr.py words_raw.json: [{text,start,end[,rescued]}]
        return [{"t": ("⚠" if w.get("rescued") else "") + w["text"].strip(), "s": w["start"], "e": w["end"]} for w in d]
    if "segments" in d:
        return [{"t": w["word"].strip(), "s": w["start"], "e": w["end"]} for s in d["segments"] for w in s.get("words", [])]
    return [{"t": w["text"].strip(), "s": w["start"], "e": w["end"]} for w in d["words"] if w.get("type", "word") == "word"]


def main():
    a = sys.argv[1:]
    gap = float(a[a.index("--gap") + 1]) if "--gap" in a else 0.5
    if "--gap" in a:
        i = a.index("--gap"); del a[i:i + 2]
    if len(a) < 2:
        sys.exit(__doc__)
    out, files = a[0], a[1:]
    lines = []
    for k, p in enumerate(files, 1):
        ws = words(p)
        lines.append(f"\n## L{k} = {os.path.basename(p)}  ({len(ws)} words, {ws[-1]['e'] if ws else 0:.1f} s)\n")
        cur = []
        for i, w in enumerate(ws):
            cur.append(w)
            nxt = ws[i + 1]["s"] if i + 1 < len(ws) else 1e9
            if nxt - w["e"] > gap or i == len(ws) - 1:
                txt = " ".join(x["t"] + (" ⚠" if x["e"] - x["s"] > 1.5 else "") for x in cur)
                lines.append(f"[{cur[0]['s']:7.2f}-{cur[-1]['e']:7.2f}] L{k}  {txt}")
                cur = []
    open(out, "w").write("\n".join(lines) + "\n")
    print(out, sum(1 for l in lines if l.startswith("[")), "phrases")


if __name__ == "__main__":
    main()
