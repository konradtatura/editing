#!/usr/bin/env python3
"""Find restarts, repeated attempts, fillers and ASR junk in the raw transcript; propose a keep-list.

usage: takes.py <film_dir> [--script skrypt.md]

Reads 01_cut/words_raw.json, writes:
  01_cut/takes_report.md     what would be dropped and why (word level) + the resulting text
  01_cut/takes_suggest.json  {"takes":[{start,end,note}]} keep ranges → review, then save as 01_cut/takes.json

Detects (heuristics; Claude reviews every drop before cutting):
  restart   – a phrase restarted within a few words: "daj mi 3 minuty, daj mi 3 minuty, a pokażę…" → keep the last start
  retake    – a whole sentence said again later (similar text) → keep the last complete attempt
  filler    – yyy / eee / hmm
  junk      – ASR hallucination (same token 4+ times in a row)
"""
from __future__ import annotations

import argparse
import difflib
import json
import re
from pathlib import Path

FILLERS = {"yyy", "eee", "eem", "hmm", "mmm", "yy", "ee", "em", "eh", "uh", "um", "yyyy", "eeee"}
MAX_GAP_KEEP = 0.9      # merge kept words into one range when the gap between them is below this


NUM = {"zero": "0", "jeden": "1", "jedna": "1", "jedno": "1", "dwa": "2", "dwie": "2", "trzy": "3", "cztery": "4",
       "pięć": "5", "sześć": "6", "siedem": "7", "osiem": "8", "dziewięć": "9", "dziesięć": "10", "sto": "100",
       "dwadzieścia": "20", "trzydzieści": "30", "czterdzieści": "40", "pięćdziesiąt": "50", "tysiąc": "1000"}


def n(t: str) -> str:
    w = re.sub(r"[^\w%]", "", t.lower())
    return NUM.get(w, w)


def weq(a: str, b: str) -> bool:
    """Same word allowing ASR variants (pokaże/pokażę) and truncation (ma/maila)."""
    if a == b:
        return True
    if not a or not b:
        return False
    s, l = (a, b) if len(a) <= len(b) else (b, a)
    if len(s) >= 2 and l.startswith(s):
        return True
    if len(s) >= 4 and s[:4] == l[:4]:
        return True
    return difflib.SequenceMatcher(None, a, b).ratio() >= 0.8


def peq(x: list[str], y: list[str]) -> bool:
    return len(x) == len(y) and all(weq(a, b) for a, b in zip(x, y))


def find_restarts(ws: list[str]) -> list[tuple[int, int, str]]:
    """Return (i0, i1_exclusive, phrase) spans to drop: earlier starts of a phrase that is restarted
    within a short distance. Chains like A A A B → drop the first two A."""
    drops = []
    N = len(ws)
    i = 0
    while i < N:
        best = None
        for L in range(6, 1, -1):                      # phrase length 6..2 words
            if i + L > N:
                continue
            g = ws[i:i + L]
            # next occurrence of g starting within 1..L+4 words after this one
            for d in range(L, L + 5):
                j = i + d
                if j + L <= N and peq(ws[j:j + L], g):
                    best = (L, d)
                    break
            if best:
                break
        if best:
            L, d = best
            # extend the chain: keep jumping while the phrase repeats
            start, j = i, i + d
            while True:
                nxt = None
                for d2 in range(L, L + 5):
                    if j + d2 + L <= N and peq(ws[j + d2:j + d2 + L], ws[i:i + L]):
                        nxt = j + d2
                        break
                if nxt is None:
                    break
                j = nxt
            drops.append((start, j, " ".join(ws[i:i + L])))
            i = j
        else:
            i += 1
    return drops


def sentences(words, gap=0.55):
    out, cur = [], []
    for i, w in enumerate(words):
        cur.append(i)
        nxt = words[i + 1] if i + 1 < len(words) else None
        if w["text"][-1:] in ".?!…" or nxt is None or nxt["start"] - w["end"] > gap:
            out.append(cur)
            cur = []
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("film_dir")
    ap.add_argument("--script")
    a = ap.parse_args()
    film = Path(a.film_dir).resolve()
    words = json.loads((film / "01_cut" / "words_raw.json").read_text())
    ws = [n(w["text"]) for w in words]
    drop = [None] * len(words)            # reason per word

    # junk: same token 4+ times in a row (ASR hallucination on silence/noise)
    i = 0
    while i < len(ws):
        j = i
        while j + 1 < len(ws) and ws[j + 1] == ws[i]:
            j += 1
        if j - i + 1 >= 4:
            for k in range(i, j + 1):
                drop[k] = "junk"
        i = j + 1
    # a single "word" lasting > 1.2 s means the recogniser skipped speech there (often a whole retake)
    for k, w in enumerate(words):
        if w["end"] - w["start"] > 1.2:
            drop[k] = drop[k] or "asr-gap (rozpoznawanie pominęło fragment — sprawdź ręcznie)"
    for k, t in enumerate(ws):
        if t in FILLERS:
            drop[k] = drop[k] or "filler"
    for i0, i1, ph in find_restarts(ws):
        for k in range(i0, i1):
            drop[k] = drop[k] or f"restart „{ph}”"

    # retakes at sentence level: an earlier sentence whose kept text is very similar to a later one
    sents = sentences(words)
    def kept_text(s):
        return " ".join(ws[k] for k in s if not drop[k])
    for x in range(len(sents)):
        tx = kept_text(sents[x])
        if len(tx.split()) < 3:
            continue
        for y in range(x + 1, len(sents)):
            if words[sents[y][0]]['start'] - words[sents[x][-1]]['end'] > 45:
                break
            ty = kept_text(sents[y])
            if not ty:
                continue
            short, long_ = (tx, ty) if len(tx) <= len(ty) else (ty, tx)
            r = difflib.SequenceMatcher(None, tx, ty).ratio()
            prefix = difflib.SequenceMatcher(None, short, long_[: len(short)]).ratio() >= 0.85
            if r >= 0.72 or (prefix and len(tx) <= len(ty)):
                for k in sents[x]:
                    drop[k] = drop[k] or "retake (powtórzone później)"
                break

    # keep ranges
    keep, cur = [], None
    for k, w in enumerate(words):
        if drop[k]:
            if cur:
                keep.append(cur); cur = None
            continue
        if cur and w["start"] - words[cur["last"]]["end"] <= MAX_GAP_KEEP:
            cur["end"] = w["end"]; cur["last"] = k; cur["text"].append(w["text"])
        else:
            if cur:
                keep.append(cur)
            cur = {"start": w["start"], "end": w["end"], "last": k, "text": [w["text"]]}
    if cur:
        keep.append(cur)

    # report
    md = ["# Cięcie — propozycja", "",
          "Każde usunięcie ma powód. Sprawdź zwłaszcza „retake” (czy zostaje lepsze podejście) i „restart”.",
          "Zostawiony tekst na dole to to, co usłyszy widz.", "", "## Usunięcia", "",
          "| od | do | powód | tekst |", "|---|---|---|---|"]
    k = 0
    while k < len(words):
        if drop[k]:
            j = k
            while j + 1 < len(words) and drop[j + 1] == drop[k]:
                j += 1
            md.append(f"| {words[k]['start']:.2f} | {words[j]['end']:.2f} | {drop[k]} | {' '.join(w['text'] for w in words[k:j+1])} |")
            k = j + 1
        else:
            k += 1
    md += ["", "## Zostaje (zakresy do cięcia)", ""]
    md += [f"- `{c['start']:.2f}–{c['end']:.2f}` {' '.join(c['text'])}" for c in keep]
    kept_s = sum(c["end"] - c["start"] for c in keep)
    md += ["", f"Zostaje ok. {kept_s:.0f} s mowy z {words[-1]['end']:.0f} s nagrania."]
    (film / "01_cut" / "takes_report.md").write_text("\n".join(md) + "\n")
    sugg = [{"start": round(c["start"], 3), "end": round(c["end"], 3), "note": " ".join(c["text"])[:90]} for c in keep]
    (film / "01_cut" / "takes_suggest.json").write_text(json.dumps({"takes": sugg}, ensure_ascii=False, indent=1))
    nd = sum(1 for d in drop if d)
    print(f"{len(words)} words, {nd} dropped, {len(keep)} keep ranges, ~{kept_s:.0f}s speech → takes_report.md")


if __name__ == "__main__":
    main()
