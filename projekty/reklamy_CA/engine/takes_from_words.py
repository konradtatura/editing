#!/usr/bin/env python3
"""usage: takes_from_words.py CHUNKS.json SRC OUT_takes.json "s1-e1" "s2-e2" ...
each pair = start time of the first word and START time of the last word (as printed by chunks.py); end resolves to that word's end."""
import json, sys
ch = json.load(open(sys.argv[1])); words = [w for c in ch for w in c["words"]]
def find(t):
    return min(words, key=lambda w: abs(w["s"] - t))
takes = []
for p in sys.argv[4:]:
    s, e = map(float, p.split("-"))
    a, b = find(s), find(e)
    takes.append([a["s"], b["e"]]); print(f'{a["s"]:7.2f} {a["w"]!r:>16} .. {b["w"]!r:<16} {b["e"]:7.2f}')
json.dump({"src": sys.argv[2], "takes": takes}, open(sys.argv[3], "w"))
