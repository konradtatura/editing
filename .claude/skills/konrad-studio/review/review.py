#!/usr/bin/env python3
"""Konrad Studio — Video Review. Local page to watch a preview, pin notes to moments, send fixes to Claude Code.

usage:
  review.py PROJ [--port 8765]          start the review page for a project → http://127.0.0.1:8765  (local only)
  review.py PROJ --notes                print the open notes of the latest sent round (what Claude reads and fixes)
  review.py PROJ --reply ID "tekst"     mark a note as done with a short reply (shown to Konrad in the page)
Frame.io-style: a click on the picture pins a note to that spot (x/y kept); with anim/scenes.json the page shows an animation
strip, tags every note with its scene and offers „bez animacji” (latest cut at the same time). „WYŚLIJ” also saves
review/shots/ID.jpg — the frame with the numbered pin — and lists it in POPRAWKI.md (look at it before fixing).
Files (all in PROJ/review/):
  notes.json        every note, version and approval (the source of truth; written on every change)
  POPRAWKI.md       written by „WYŚLIJ POPRAWKI”: open notes of the version, with timecodes + what is said there
  versions/vN_*.mp4 each new preview, kept as a HARD LINK (no copy; the old render stays watchable after re-render)
Videos looked up in PROJ (first found per kind): cut = CUT_preview.mp4, CUT.mp4, then the _tel copies (phone copies are low bitrate);
final = FINAL.mp4, FINAL_tel.mp4. A changed file (new size/mtime) becomes the next version automatically.
„ZATWIERDŹ CIĘCIE” also runs `ks.py PROJ approve cut` when the project is run by ks.py. Nothing renders from here.
"""
import json, os, re, subprocess, sys, threading, time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

HERE = os.path.dirname(os.path.abspath(__file__))
KS = os.path.join(os.path.dirname(HERE), "scripts", "ks.py")
PY = "/Library/Frameworks/Python.framework/Versions/3.13/bin/python3"
CANDIDATES = {"cut": ["CUT_preview.mp4", "CUT.mp4", "CUT_preview_tel.mp4", "CUT_tel.mp4"],
              "final": ["FINAL.mp4", "FINAL_tel.mp4"]}
LOCK = threading.Lock()


def now():
    return time.strftime("%Y-%m-%d %H:%M:%S")


def tc(t):
    m, s = divmod(t, 60)
    return f"{int(m)}:{s:05.2f}"


class Review:
    def __init__(self, proj):
        self.proj = os.path.abspath(proj)
        self.dir = os.path.join(self.proj, "review")
        os.makedirs(os.path.join(self.dir, "versions"), exist_ok=True)
        self.path = os.path.join(self.dir, "notes.json")
        self.words = None

    def load(self):
        if os.path.exists(self.path):
            return json.load(open(self.path))
        return {"project": os.path.basename(self.proj), "versions": [], "notes": [], "approvals": {}, "sent": []}

    def save(self, d):
        tmp = self.path + ".part"
        json.dump(d, open(tmp, "w"), ensure_ascii=False, indent=1)
        os.replace(tmp, self.path)

    def scan(self, d):
        """Register a new version when the project's preview file changed (hard link keeps the old one viewable)."""
        changed = False
        for kind, names in CANDIDATES.items():
            src = next((os.path.join(self.proj, n) for n in names if os.path.exists(os.path.join(self.proj, n))), None)
            if not src:
                continue
            st = os.stat(src); sig = f"{os.path.basename(src)}|{st.st_size}|{int(st.st_mtime)}"
            if time.time() - st.st_mtime < 15:          # still being written by a render → register it once it is finished
                continue
            if any(v["sig"] == sig for v in d["versions"]):
                continue
            n = len(d["versions"]) + 1
            dst = os.path.join(self.dir, "versions", f"v{n}_{kind}.mp4")
            try:
                os.link(src, dst)                       # same disk: no copy, no extra space while the file is unchanged
            except OSError:
                os.symlink(src, dst)
            d["versions"].append({"id": f"v{n}", "kind": kind, "file": os.path.relpath(dst, self.proj),
                                  "source": os.path.basename(src), "sig": sig, "added": now()})
            changed = True
        return changed

    def scenes(self):
        """Animation scenes of the project (anim/scenes.json: {key: [in, out, "B"|"K"]}) — same timeline as CUT/FINAL."""
        p = os.path.join(self.proj, "anim", "scenes.json")
        try:
            sc = json.load(open(p))
        except Exception:
            return []
        out = sorted(({"key": k, "in": v[0], "out": v[1], "mode": v[2]} for k, v in sc.items()), key=lambda x: x["in"])
        self.said(0)                                  # load words once
        for s_ in out:
            ws = [w["word"].strip() for w in self.words if s_["in"] - 0.05 <= w["start"] < s_["out"]]
            s_["said"] = " ".join(ws)
        return out

    def thumb(self, vid, key):
        """Small frame of an animation (middle of the scene) from a version file → review/thumbs/VID_KEY.jpg (cached)."""
        d = self.load(); v = next((x for x in d["versions"] if x["id"] == vid), None)
        sc = next((s_ for s_ in self.scenes() if s_["key"] == key), None)
        if not v or not sc:
            return None
        td = os.path.join(self.dir, "thumbs"); os.makedirs(td, exist_ok=True)
        out = os.path.join(td, f"{vid}_{key}.jpg")
        if not os.path.exists(out):
            t = sc["in"] + min(1.6, (sc["out"] - sc["in"]) * 0.6)
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.2f}", "-i", os.path.join(self.proj, v["file"]), "-frames:v", "1",
                            "-vf", "scale=256:-2", "-q:v", "5", out], capture_output=True)
        return out if os.path.exists(out) else None

    def scene_at(self, t):
        return next((s["key"] for s in self.scenes() if s["in"] - 0.05 <= t < s["out"] + 0.05), None)

    def shot(self, d, n):
        """Frame of the note's version at its time, with the pin drawn on it → review/shots/ID.jpg (for Claude to look at)."""
        v = next((x for x in d["versions"] if x["id"] == n["version"]), None)
        if not v:
            return None
        sd = os.path.join(self.dir, "shots"); os.makedirs(sd, exist_ok=True)
        out = os.path.join(sd, f"{n['id']}.jpg")
        r = subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{n['t']:.3f}", "-i", os.path.join(self.proj, v["file"]),
                            "-frames:v", "1", "-vf", "scale=1280:-2", out], capture_output=True)
        if r.returncode or not os.path.exists(out):
            return None
        if n.get("x") is not None:
            try:
                from PIL import Image, ImageDraw
                im = Image.open(out).convert("RGB"); W_, H_ = im.size; dr = ImageDraw.Draw(im)
                x, y = n["x"] * W_, n["y"] * H_
                dr.ellipse([x - 22, y - 22, x + 22, y + 22], fill=(10, 132, 255), outline=(255, 255, 255), width=4)
                try:
                    from PIL import ImageFont
                    fnt = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 24)
                except Exception:
                    fnt = None
                dr.text((x, y), n.get("pin", "•"), fill=(255, 255, 255), font=fnt, anchor="mm")
                im.save(out, quality=88)
            except Exception:
                pass
        return os.path.relpath(out, self.proj)

    def said(self, t, span=2.5):
        """What is said around t (from tr/words.json of the cut — preview and final share the cut's timeline)."""
        if self.words is None:
            p = os.path.join(self.proj, "tr", "words.json")
            try:
                self.words = [w for s in json.load(open(p))["segments"] for w in s.get("words", [])]
            except Exception:
                self.words = []
        ws = [w["word"].strip() for w in self.words if t - span <= w["start"] <= t + span]
        return " ".join(ws)

    def write_poprawki(self, d, vid):
        v = next(x for x in d["versions"] if x["id"] == vid)
        rows = sorted([n for n in d["notes"] if n["version"] == vid and n["status"] == "open"], key=lambda n: n["t"])
        lines = [f"# Poprawki od Konrada — {d['project']}, wersja {vid} ({'cięcie' if v['kind'] == 'cut' else 'finał'}, plik {v['source']})",
                 f"Wysłane: {now()} · uwag: {len(rows)}",
                 "",
                 "Czasy są na osi czasu CIĘCIA (podgląd, CUT.mp4 i FINAL.mp4 mają tę samą oś). Wprowadź każdą uwagę istniejącymi",
                 "narzędziami (takes.json → ks.py run / cut_takes.py; animacje → sceny + assemble.py), resztę zostaw bez zmian.",
                 "Po każdej: `review.py PROJ --reply ID \"co zrobiłem\"`. Nowy podgląd pojawi się w Video Review sam jako kolejna wersja.",
                 ""]
        for k, n in enumerate(rows, 1):
            n["pin"] = str(k)
            ctx = self.said(n["t"])
            where = f" · animacja {n['scene']}" if n.get("scene") else ""
            spot = f" · punkt na kadrze: {n['x'] * 100:.0f}% od lewej, {n['y'] * 100:.0f}% od góry" if n.get("x") is not None else ""
            lines.append(f"- [{n['id']}] {tc(n['t'])} ({n['t']:.2f} s, klatka {n['frame']}){where}{spot}: {n['text']}")
            if ctx:
                lines.append(f"  mówisz tam: „{ctx}”")
            sh = self.shot(d, n)
            if sh:
                lines.append(f"  screenshot: {sh}")
            for im in n.get("images", []):
                lines.append(f"  zdjęcie od Konrada: review/attach/{im}  (obejrzyj — to wzór / pokazanie, o co chodzi)")
        open(os.path.join(self.dir, "POPRAWKI.md"), "w").write("\n".join(lines) + "\n")
        d["sent"].append({"version": vid, "at": now(), "count": len(rows), "ids": [n["id"] for n in rows]})
        for n in rows:
            n["sent"] = True
        return len(rows)


def handler_for(R):
    class H(BaseHTTPRequestHandler):
        def log_message(self, *a):
            pass

        def send_json(self, obj, code=200):
            b = json.dumps(obj, ensure_ascii=False).encode()
            self.send_response(code); self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(b))); self.send_header("Cache-Control", "no-store"); self.end_headers()
            self.wfile.write(b)

        def body(self):
            n = int(self.headers.get("Content-Length") or 0)
            return json.loads(self.rfile.read(n) or b"{}")

        def do_GET(self):
            if self.path in ("/", "/index.html"):
                b = open(os.path.join(HERE, "index.html"), "rb").read()
                self.send_response(200); self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(b))); self.end_headers(); self.wfile.write(b); return
            if self.path == "/api/state":
                with LOCK:
                    d = R.load()
                    if R.scan(d):
                        R.save(d)
                return self.send_json(dict(d, scenes=R.scenes()))
            m = re.match(r"^/attach/(a\d+\.(png|jpg|webp|gif|heic))$", self.path)
            if m:
                f = os.path.join(R.dir, "attach", m.group(1))
                if not os.path.exists(f):
                    return self.send_json({"error": "no file"}, 404)
                b = open(f, "rb").read(); ext = m.group(2)
                self.send_response(200); self.send_header("Content-Type", "image/" + ("jpeg" if ext == "jpg" else ext))
                self.send_header("Content-Length", str(len(b))); self.end_headers(); self.wfile.write(b); return
            m = re.match(r"^/thumb/(v\d+)/([A-Za-z0-9_]+)$", self.path)
            if m:
                f = R.thumb(m.group(1), m.group(2))
                if not f:
                    return self.send_json({"error": "no thumb"}, 404)
                b = open(f, "rb").read()
                self.send_response(200); self.send_header("Content-Type", "image/jpeg"); self.send_header("Content-Length", str(len(b)))
                self.send_header("Cache-Control", "max-age=3600"); self.end_headers(); self.wfile.write(b); return
            m = re.match(r"^/video/(v\d+)$", self.path)
            if m:
                d = R.load(); v = next((x for x in d["versions"] if x["id"] == m.group(1)), None)
                if not v:
                    return self.send_json({"error": "no such version"}, 404)
                return self.serve_file(os.path.join(R.proj, v["file"]))
            self.send_json({"error": "not found"}, 404)

        def serve_file(self, path):
            size = os.path.getsize(path); rng = self.headers.get("Range")
            start, end = 0, size - 1
            if rng and rng.startswith("bytes="):
                a, _, b = rng[6:].partition("-")
                start = int(a) if a else max(0, size - int(b)); end = int(b) if (a and b) else size - 1
                self.send_response(206); self.send_header("Content-Range", f"bytes {start}-{end}/{size}")
            else:
                self.send_response(200)
            self.send_header("Content-Type", "video/mp4"); self.send_header("Accept-Ranges", "bytes")
            self.send_header("Content-Length", str(end - start + 1)); self.end_headers()
            with open(path, "rb") as f:
                f.seek(start); left = end - start + 1
                try:
                    while left > 0:
                        chunk = f.read(min(1 << 20, left))
                        if not chunk:
                            break
                        self.wfile.write(chunk); left -= len(chunk)
                except (BrokenPipeError, ConnectionResetError):
                    pass

        def do_POST(self):
            if self.path == "/api/attach":            # a picture for a note: raw bytes → review/attach/aN.ext
                n = int(self.headers.get("Content-Length") or 0)
                if n <= 0 or n > 25 * 1024 * 1024:
                    return self.send_json({"error": "size"}, 400)
                ct = (self.headers.get("Content-Type") or "").lower()
                ext = {"image/png": "png", "image/jpeg": "jpg", "image/jpg": "jpg", "image/webp": "webp", "image/gif": "gif",
                       "image/heic": "heic"}.get(ct.split(";")[0].strip())
                if not ext:
                    return self.send_json({"error": "type"}, 400)
                data = self.rfile.read(n)
                ad = os.path.join(R.dir, "attach"); os.makedirs(ad, exist_ok=True)
                with LOCK:
                    k = 1 + max([int(re.sub(r"\D", "", f.split(".")[0]) or 0) for f in os.listdir(ad)] or [0])
                    f = f"a{k}.{ext}"
                    open(os.path.join(ad, f), "wb").write(data)
                return self.send_json({"ok": True, "file": f})
            b = self.body()
            with LOCK:
                d = R.load()
                if self.path == "/api/notes":
                    t = float(b["t"]); text = str(b["text"]).strip()
                    if not text:
                        return self.send_json({"error": "empty"}, 400)
                    nid = f"n{max([int(n['id'][1:]) for n in d['notes']] or [0]) + 1}"
                    note = {"id": nid, "version": b["version"], "t": round(t, 3), "frame": int(t * 30 + 1e-4),
                            "text": text, "status": "open", "created": now()}
                    if b.get("x") is not None and b.get("y") is not None:
                        note["x"], note["y"] = round(min(1, max(0, float(b["x"]))), 4), round(min(1, max(0, float(b["y"]))), 4)
                    imgs = [os.path.basename(str(x)) for x in (b.get("images") or []) if re.match(r"^a\d+\.(png|jpg|webp|gif|heic)$", os.path.basename(str(x)))]
                    if imgs:
                        note["images"] = imgs
                    sk = R.scene_at(t)
                    if sk:
                        note["scene"] = sk
                    d["notes"].append(note)
                elif re.match(r"^/api/notes/n\d+/delete$", self.path):
                    nid = self.path.split("/")[3]; d["notes"] = [n for n in d["notes"] if n["id"] != nid]
                elif self.path == "/api/send":
                    cnt = R.write_poprawki(d, b["version"]); R.save(d)
                    return self.send_json({"ok": True, "count": cnt, "file": os.path.join(R.dir, "POPRAWKI.md"), "state": dict(d, scenes=R.scenes())})
                elif self.path == "/api/approve":
                    kind = b["kind"]; msg = ""
                    d["approvals"][kind] = {"version": b["version"], "at": now()}
                    if kind == "cut" and os.path.exists(os.path.join(R.proj, "project.json")) and os.path.exists(KS):
                        r = subprocess.run([PY, KS, R.proj, "approve", "cut"], capture_output=True, text=True)
                        msg = (r.stdout or r.stderr).strip()[-200:]
                    R.save(d)
                    return self.send_json({"ok": True, "ks": msg, "state": dict(d, scenes=R.scenes())})
                else:
                    return self.send_json({"error": "not found"}, 404)
                R.save(d)
            self.send_json({"ok": True, "state": dict(d, scenes=R.scenes())})
    return H


def main():
    a = sys.argv[1:]
    if not a:
        sys.exit(__doc__)
    R = Review(a[0])
    if "--notes" in a:
        d = R.load()
        if not d["sent"]:
            sys.exit("Brak wysłanych poprawek (Konrad jeszcze nie kliknął „WYŚLIJ POPRAWKI”).")
        last = d["sent"][-1]
        print(open(os.path.join(R.dir, "POPRAWKI.md")).read().rstrip())
        still = [n for n in d["notes"] if n["id"] in last["ids"] and n["status"] == "open"]
        print(f"\n-- otwarte z tej rundy: {len(still)} z {last['count']}")
        return
    if "--reply" in a:
        i = a.index("--reply"); nid, text = a[i + 1], a[i + 2]
        with LOCK:
            d = R.load()
            for n in d["notes"]:
                if n["id"] == nid:
                    n["status"], n["reply"], n["done_at"] = "done", text, now()
            R.save(d)
        print(f"{nid}: oznaczona jako zrobiona")
        return
    port = int(a[a.index("--port") + 1]) if "--port" in a else 8765
    d = R.load(); R.scan(d); R.save(d)
    srv = ThreadingHTTPServer(("127.0.0.1", port), handler_for(R))   # local only — not reachable from the network
    print(f"Video Review: http://127.0.0.1:{port}  ({R.proj})", flush=True)
    srv.serve_forever()


if __name__ == "__main__":
    main()
