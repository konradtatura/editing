"""Country outlines (GeoJSON in assets/) → SVG path fitted into a box; point projection for pins on the same box."""
import json, math, os

HERE = os.path.dirname(os.path.abspath(__file__))


def _polys(code, largest_only):
    g = json.load(open(os.path.join(HERE, "assets", f"{code}.geo.json")))["features"][0]["geometry"]
    polys = [g["coordinates"]] if g["type"] == "Polygon" else g["coordinates"]
    rings = [p[0] for p in polys]
    if largest_only:
        rings = [max(rings, key=len)]
    return rings


class Shape:
    def __init__(self, code, x, y, w, h, largest_only=True):
        self.rings = _polys(code, largest_only)
        lons = [p[0] for r in self.rings for p in r]; lats = [p[1] for r in self.rings for p in r]
        self.k = math.cos(math.radians((min(lats) + max(lats)) / 2))
        self.x0, self.x1 = min(lons) * self.k, max(lons) * self.k
        self.y0, self.y1 = min(lats), max(lats)
        sc = min(w / (self.x1 - self.x0), h / (self.y1 - self.y0))
        self.s = sc
        self.ox = x + (w - (self.x1 - self.x0) * sc) / 2
        self.oy = y + (h - (self.y1 - self.y0) * sc) / 2

    def pt(self, lon, lat):
        return round(self.ox + (lon * self.k - self.x0) * self.s, 1), round(self.oy + (self.y1 - lat) * self.s, 1)

    def path(self):
        out = []
        for r in self.rings:
            pts = [self.pt(*p[:2]) for p in r[::2]]
            out.append("M" + " L".join(f"{a},{b}" for a, b in pts) + " Z")
        return " ".join(out)
