#!/usr/bin/env python3
"""Remove spans given on the CUT timeline (Konrad's review notes: „od 2:27.36 do 2:27.92 wytnij”) from takes.json.

usage: cut_span.py PROJ FROM TO [FROM TO ...]     times in seconds or m:ss.xx, on the timeline of the current edl.json
Each span is mapped to source time through edl.json; the take holding it is split there: the first part ends exactly at
FROM, the second starts exactly at TO ({"exact_start": true}, so the onset search does not walk back over the cut).
A span covering a whole take drops it. takes.json is backed up to takes.before_span_<n>.json. Then: ks.py PROJ run.
"""
import json, os, shutil, sys


def secs(x):
    if ":" in x:
        m, s = x.split(":")
        return int(m) * 60 + float(s)
    return float(x)


def to_src(R, t):
    for r in R:
        d = r["n"] / 30
        if r["t"] - 1e-3 <= t <= r["t"] + d + 1e-3:
            return r["source"], r["ss"] + (t - r["t"])
    sys.exit(f"{t:.2f} s is outside the cut")


def main():
    a = sys.argv[1:]
    if len(a) < 3 or len(a) % 2 == 0:
        sys.exit(__doc__)
    P = a[0]
    R = json.load(open(os.path.join(P, "edl.json")))["ranges"]
    tp = os.path.join(P, "takes.json")
    T = json.load(open(tp))
    words = {k: json.load(open(os.path.join(P, v))) for k, v in T["transcripts"].items()}
    n = 1
    while os.path.exists(os.path.join(P, f"takes.before_span_{n}.json")):
        n += 1
    shutil.copy(tp, os.path.join(P, f"takes.before_span_{n}.json"))
    spans = [(secs(a[i]), secs(a[i + 1])) for i in range(1, len(a), 2)]
    for c0, c1 in spans:
        k0, s0 = to_src(R, c0)
        k1, s1 = to_src(R, c1)
        out, hit = [], False
        # ranges lying wholly inside the span on the cut timeline: the takes they come from are dropped entirely
        inner = [(r["source"], r["ss"], r["ss"] + r["n"] / 30) for r in R if r["t"] >= c0 - 1e-3 and r["t"] + r["n"] / 30 <= c1 + 1e-3]
        for tk in T["takes"]:
            key, st, lw = tk[0], tk[1], tk[2]
            end_guess = max(w["end"] for w in words[key] if abs(w["start"] - lw) < 0.006) if any(abs(w["start"] - lw) < 0.006 for w in words[key]) else lw
            opt = dict(tk[4]) if len(tk) > 4 else {}
            in0 = key == k0 and st - 0.3 <= s0 <= end_guess + 1.0
            in1 = key == k1 and st - 1.0 <= s1 <= end_guess + 0.3
            if not (in0 or in1) and any(k == key and st - 0.3 <= r0 and r1 <= end_guess + 0.5
                                              and end_guess - st <= r1 - r0 + 0.6 for k, r0, r1 in inner):
                hit = True; print(f"{c0:.2f}-{c1:.2f} cut → drop take {st:.2f}-{lw:.2f} {tk[3]!r}"); continue
            if not (in0 or in1):
                out.append(tk); continue
            hit = True
            if in0 and s0 >= end_guess + float(opt.get("hold", 0.1)):
                out.append(tk)                               # span starts after this take's tail: leave it alone
            elif in0 and s0 > st + 0.05:                     # keep the part before the span, ending exactly at FROM (no hold)
                e = round(s0, 3)
                if any(abs(w["start"] - e) < 0.006 for w in words[key]):
                    e += 0.007                               # not a word start → used as an explicit end
                first = [key, st, e, tk[3] + " (do cięcia)"]
                if opt.get("exact_start"):
                    first.append({"exact_start": True})
                out.append(first)
            if in1 and not in0 and s1 <= st + 0.02:
                out.append(tk)                               # span ends before this take starts: leave it alone
            elif in1 and s1 < end_guess - 0.05:              # keep the part after the span, starting exactly at TO
                o2 = {k: v for k, v in opt.items() if k != "exact_start"}
                o2["exact_start"] = True
                out.append([key, round(s1, 3), lw, tk[3], o2])
            print(f"{c0:.2f}-{c1:.2f} cut → {key} {s0:.2f}-{s1:.2f} in take {st:.2f}-{lw:.2f}")
        if not hit:
            sys.exit(f"no take found for {c0:.2f}-{c1:.2f}")
        T["takes"] = out
    json.dump(T, open(tp, "w"), ensure_ascii=False, indent=1)
    print(f"{len(spans)} span(s) cut; backup takes.before_span_{n}.json")


if __name__ == "__main__":
    main()
