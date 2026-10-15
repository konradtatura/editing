"""Word times of CUT.mp4 (tr/words.json) for syncing scenes: W("talent", after) → start (s) of the first word that
starts with the given text (case/punctuation-insensitive) at or after `after`."""
import json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
_W = [x for s in json.load(open(os.path.join(HERE, "..", "tr", "words.json")))["segments"] for x in s["words"]]
_norm = lambda s: re.sub(r"[^\wąćęłńóśźż0-9]", "", s.lower())


def W(text, after=0.0):
    parts = [_norm(p) for p in text.split()]
    for i, w in enumerate(_W):
        if w["start"] < after - 0.05:
            continue
        if all(i + j < len(_W) and _norm(_W[i + j]["word"]).startswith(p) for j, p in enumerate(parts)):
            return round(w["start"], 2)
    raise SystemExit(f"word not found: {text!r} after {after}")
