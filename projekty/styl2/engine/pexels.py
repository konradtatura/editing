#!/usr/bin/env python3
"""Fetch portrait stock clips from Pexels. Key from $PEXELS_API_KEY.
usage: pexels.py OUTDIR "name=query" ...   -> OUTDIR/<name>_<n>.mp4 (up to 3 per query) + OUTDIR/index.json"""
import json, os, sys, urllib.parse, urllib.request
key = os.environ["PEXELS_API_KEY"]; out = sys.argv[1]; os.makedirs(out, exist_ok=True)
idxp = os.path.join(out, "index.json"); idx = json.load(open(idxp)) if os.path.exists(idxp) else {}
def get(url):
    return json.load(urllib.request.urlopen(urllib.request.Request(url, headers={"Authorization": key, "User-Agent": "Mozilla/5.0"})))
for arg in sys.argv[2:]:
    name, q = arg.split("=", 1)
    d = get("https://api.pexels.com/videos/search?" + urllib.parse.urlencode({"query": q, "orientation": "portrait", "per_page": 8, "size": "medium"}))
    n = 0
    for v in d.get("videos", []):
        if v["duration"] < 3: continue
        fs = [f for f in v["video_files"] if (f.get("height") or 0) >= 1280 and (f.get("width") or 0) < (f.get("height") or 0)]
        if not fs: continue
        f = min(fs, key=lambda f: abs((f.get("height") or 0) - 1920))
        p = os.path.join(out, f"{name}_{n}.mp4")
        req = urllib.request.Request(f["link"], headers={"User-Agent": "Mozilla/5.0"})
        open(p, "wb").write(urllib.request.urlopen(req).read())
        idx[f"{name}_{n}"] = {"id": v["id"], "url": v["url"], "author": v["user"]["name"], "dur": v["duration"], "w": f["width"], "h": f["height"]}
        print(name, n, v["url"], v["duration"], f["width"], f["height"], flush=True)
        n += 1
        if n >= 3: break
json.dump(idx, open(idxp, "w"), indent=1)
