#!/usr/bin/env python3
"""Real icons instead of drawn ones (people and brands are never drawn by hand).

usage: fetch_icon.py app "Notion" OUT.png            official App Store icon (iTunes Search API, 512 px, no key)
       fetch_icon.py fluent "Office building" OUT.png Microsoft Fluent 3D emoji (objects; people: "Man technologist")
Import into a scene with `tsrct project import-asset --kind image` (see silnik-tesseract.md) or composite in ffmpeg.
For a country outline use real GeoJSON (e.g. github.com/johan/world.geo.json, countries/POL.geo.json) and draw it
as a path — a flag emoji alone is not enough.
"""
import json, sys, urllib.parse, urllib.request


def get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=30) as r:
        return r.read()


def main():
    if len(sys.argv) < 4:
        sys.exit(__doc__)
    kind, name, out = sys.argv[1:4]
    if kind == "app":
        q = urllib.parse.urlencode({"term": name, "entity": "software", "limit": 5, "country": "us"})
        res = json.loads(get("https://itunes.apple.com/search?" + q))["results"]
        if not res:
            sys.exit("no app found")
        hit = next((r for r in res if r["trackName"].lower().startswith(name.lower())), res[0])
        open(out, "wb").write(get(hit["artworkUrl512"]))
        print(out, "←", hit["trackName"])
    elif kind == "fluent":
        folder = name[0].upper() + name[1:].lower()
        snake = name.lower().replace(" ", "_")
        base = "https://raw.githubusercontent.com/microsoft/fluentui-emoji/main/assets/" + urllib.parse.quote(folder)
        for url in (f"{base}/3D/{snake}_3d.png", f"{base}/Default/3D/{snake}_3d_default.png"):
            try:
                open(out, "wb").write(get(url)); print(out, "←", url); return
            except Exception:
                pass
        sys.exit("not found — check the exact folder name on github.com/microsoft/fluentui-emoji/tree/main/assets")
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
