#!/usr/bin/env python3
"""Close the camera flashes between back-to-back animations (Konrad 2026-10-04: "pół sekundy mojej kamerki między
animacjami — one powinny iść jedna po drugiej").

usage: snap_gaps.py PROJECT_DIR scenes_a.py [scenes_b.py ...] [--max 1.2]
Collects every scene (in, out) from the BUILD dicts, and for each gap shorter than --max seconds between consecutive
scenes extends the earlier scene's out-point to the next in-point. Writes PROJECT_DIR/snap.json {scene_name: new_out};
apple.Scene applies it automatically, so just rebuild + re-export afterwards. Gaps >= --max stay (intended face beats).
"""
import contextlib, importlib.util, io, json, os, sys


def main():
    a = sys.argv[1:]
    mx = float(a[a.index("--max") + 1]) if "--max" in a else 1.2
    if "--max" in a:
        i = a.index("--max"); del a[i:i + 2]
    if len(a) < 2:
        sys.exit(__doc__)
    root, files = os.path.abspath(a[0]), [os.path.abspath(p) for p in a[1:]]
    snap_p = os.path.join(root, "snap.json")
    if os.path.exists(snap_p):
        os.remove(snap_p)
    os.environ.setdefault("PROJECT", root)
    sys.path.insert(0, root)
    items = []
    for p in files:
        spec = importlib.util.spec_from_file_location(os.path.basename(p)[:-3], p)
        M = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = M
        spec.loader.exec_module(M)
        for k, fn in M.BUILD.items():
            with contextlib.redirect_stdout(io.StringIO()):
                sc = fn()
            items.append((sc.in_s, sc.out_s, sc.name))
    items = sorted(set(items))
    snap = {}
    for (a0, a1, n1), (b0, b1, n2) in zip(items, items[1:]):
        gap = b0 - a1
        if 0 < gap < mx:
            snap[n1] = round(b0, 3)
            print(f"closed {gap * 1000:4.0f} ms  {n1} → {n2}")
        elif gap >= mx:
            print(f"face   {gap:4.1f} s   {a1:.2f}–{b0:.2f}")
    json.dump(snap, open(snap_p, "w"), indent=1)
    print(len(snap), "scenes extended → rebuild and re-export them")


if __name__ == "__main__":
    main()
