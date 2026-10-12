#!/usr/bin/env python3
"""Scaffold + render animations from plan.json with the Studio Clean templates.

usage:
  anim.py scaffold <plan.json> <film_dir> [--only ID,ID]   # build HyperFrames projects in <film_dir>/04_anim/_src/<id>/
  anim.py render   <plan.json> <film_dir> [--only ID,ID] [--quality draft|standard|high] [--jobs 2]
  anim.py deliver  <plan.json> <film_dir> [--only ID,ID]   # NAKLADKA (.mov alpha) / MIX / BROLL with original audio

Item types and how they are rendered:
  overlay  (transparent, composited over the speaker): T1 T2 T3 T4
  full     (opaque full frame, may include the speaker clip): T5 T6 T7 T9 T10
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
TPL = SKILL / "templates"
ASSETS = SKILL / "assets"

TEMPLATE_FOR = {
    "T1": "T1_text_accent.html",
    "T2": "T2_card.html",
    "T3": "T3_stat.html",
    "T4": "T2_card.html",          # cards in space = T2 with layout "space"
    "T5": "T5_split.html",
    "T6": "T6_pip.html",
    "T7": "T7_fullscreen.html",
    "T9": "T9_chapter.html",
    "T10": "T10_device.html",
}
OVERLAY = {"T1", "T2", "T3", "T4"}
NEEDS_SPEAKER = {"T5", "T6"}


def sh(cmd: list[str], cwd: Path | None = None, quiet: bool = True) -> subprocess.CompletedProcess:
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if r.returncode != 0:
        sys.stderr.write(f"\n$ {' '.join(map(str, cmd))}\n{r.stdout[-2000:]}\n{r.stderr[-4000:]}\n")
        raise SystemExit(f"command failed ({r.returncode})")
    return r


def load_plan(p: Path) -> dict:
    plan = json.loads(p.read_text())
    plan.setdefault("film", {})
    plan["film"].setdefault("w", 1920)
    plan["film"].setdefault("h", 1080)
    plan["film"].setdefault("fps", 30)
    return plan


def item_name(it: dict) -> str:
    t = float(it["start"])
    tc = f"{int(t // 60):02d}m{t % 60:05.2f}s".replace(".", "_")
    return f"{it['id']}_{tc}_{it['type']}"


def pick(plan: dict, only: str | None) -> list[dict]:
    items = plan.get("items", [])
    if only:
        ids = set(only.split(","))
        items = [i for i in items if i["id"] in ids]
    return items


def image_size(p: Path) -> tuple[int, int]:
    """(width, height) of a PNG/JPEG without extra libraries (sips fallback on macOS)."""
    b = p.read_bytes()[:32]
    if b[:8] == b"\x89PNG\r\n\x1a\n":
        return int.from_bytes(b[16:20], "big"), int.from_bytes(b[20:24], "big")
    r = subprocess.run(["sips", "-g", "pixelWidth", "-g", "pixelHeight", str(p)], capture_output=True, text=True)
    nums = [int(x.split(":")[1]) for x in r.stdout.splitlines() if "pixel" in x]
    return (nums[0], nums[1]) if len(nums) == 2 else (1440, 900)


def free_zone(film: dict, params: dict, width_cap: int = 720) -> dict:
    """Rectangle for overlay text beside the speaker's HEAD (film.speakerBox = head bbox in px).
    side: params.zone = right | left | auto (default: the wider free side)."""
    W, H = film["w"], film["h"]
    x0, y0, x1, y1 = film.get("speakerBox") or [W * 0.38, H * 0.06, W * 0.62, H * 0.58]
    gap, safe = 56, 96
    right = W - safe - (x1 + gap)
    left = (x0 - gap) - safe
    side = params.get("zone", "auto")
    if side == "auto":
        side = "right" if right >= left else "left"
    y = params.get("y", int(max(safe + 40, y0 + (y1 - y0) * 0.22)))
    if side == "right":
        w = int(min(width_cap, right))
        return {"x": int(x1 + gap), "y": int(y), "w": w, "align": "left", "side": "right"}
    w = int(min(width_cap, left))
    return {"x": int(x0 - gap - w), "y": int(y), "w": w, "align": "right", "side": "left"}


def zone_luma(rough: Path, t: float, z: dict, h: int = 300) -> float:
    """Average luma (0-255) of the footage under the text zone at time t."""
    crop = f"crop={max(16, z['w'])}:{h}:{z['x']}:{z['y']}"
    r = subprocess.run(["ffmpeg", "-v", "info", "-ss", f"{t:.3f}", "-i", str(rough), "-frames:v", "1",
                        "-vf", f"{crop},signalstats,metadata=print:key=lavfi.signalstats.YAVG", "-f", "null", "-"],
                       capture_output=True, text=True)
    for line in r.stderr.splitlines()[::-1]:
        if "YAVG=" in line:
            return float(line.split("YAVG=")[1])
    return 100.0


def scaffold_one(plan: dict, it: dict, film_dir: Path) -> Path:
    f = plan["film"]
    typ = it["type"]
    tpl = TEMPLATE_FOR.get(typ)
    if not tpl or not (TPL / tpl).exists():
        raise SystemExit(f"[{it['id']}] no template for type {typ}")
    dur = round(float(it["end"]) - float(it["start"]), 3)
    proj = film_dir / "04_anim" / "_src" / item_name(it)
    if proj.exists():
        shutil.rmtree(proj)
    (proj / "fonts").mkdir(parents=True)
    for fnt in (ASSETS / "fonts").glob("*.ttf"):
        shutil.copy(fnt, proj / "fonts" / fnt.name)
    shutil.copy(ASSETS / "vendor" / "gsap.min.js", proj / "gsap.min.js")
    shutil.copy(TPL / "_base" / "studio.css", proj / "studio.css")
    shutil.copy(TPL / "_base" / "studio.js", proj / "studio.js")
    # local images referenced by params (screenshots, logos): copy next to index.html
    params = dict(it.get("params", {}))
    for key in ("image", "logo", "screenshot"):
        if params.get(key) and Path(params[key]).expanduser().exists():
            src = Path(params[key]).expanduser()
            dst = proj / ("img_" + key + src.suffix.lower())
            shutil.copy(src, dst)
            params[key] = dst.name
            if key in ("image", "screenshot"):
                w, h = image_size(src)
                params.setdefault("imageW", w)
                params.setdefault("imageH", h)
    for k, lst in (("images", params.get("images")),):
        if isinstance(lst, list):
            out = []
            for n, pth in enumerate(lst):
                src = Path(pth).expanduser()
                if src.exists():
                    dst = proj / f"img_{n}{src.suffix.lower()}"
                    shutil.copy(src, dst)
                    out.append(dst.name)
            params[k] = out
    # speaker clip for split / PiP: cut from the rough cut, video only (audio is muxed later from the source)
    if typ in NEEDS_SPEAKER:
        rough = film_dir / "01_cut" / "rough_cut.mp4"
        sh(["ffmpeg", "-v", "error", "-y", "-ss", f"{float(it['start']):.3f}", "-i", str(rough), "-t", f"{dur:.3f}",
            "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "16", "-pix_fmt", "yuv420p", str(proj / "speaker.mp4")])
    # overlay text beside the head: geometry + ink chosen from the actual footage
    if typ in OVERLAY and "_zone" not in params:
        params["_zone"] = free_zone(f, params, 720 if typ == "T1" else 640)
    if typ in OVERLAY and "ink" not in params and "_zone" in params:
        rough = film_dir / "01_cut" / "rough_cut.mp4"
        if rough.exists():
            luma = zone_luma(rough, float(it["start"]) + dur / 2, params["_zone"])
            params["ink"] = "dark" if luma > 150 else "light"
            params["_luma"] = round(luma, 1)
    data = {"film": f, "params": params, "id": it["id"], "type": typ, "duration": dur}
    html = (TPL / tpl).read_text()
    html = (html.replace("/*__DATA__*/{}", json.dumps(data, ensure_ascii=False))
                .replace("__DURATION__", f"{dur}")
                .replace("__W__", str(f["w"])).replace("__H__", str(f["h"])))
    (proj / "index.html").write_text(html)
    return proj


def render_one(plan: dict, it: dict, film_dir: Path, quality: str) -> Path:
    proj = film_dir / "04_anim" / "_src" / item_name(it)
    if not (proj / "index.html").exists():
        scaffold_one(plan, it, film_dir)
    fmt = "webm" if it["type"] in OVERLAY else "mp4"
    out = proj / f"render.{fmt}"
    cmd = ["npx", "hyperframes", "render", "--format", fmt, "--fps", str(plan["film"]["fps"]),
           "--quality", quality, "--output", str(out)]
    sh(cmd, cwd=proj)
    print(f"  rendered {proj.name} -> {out.name}")
    return out


def deliver_one(plan: dict, it: dict, film_dir: Path) -> list[Path]:
    f = plan["film"]
    proj = film_dir / "04_anim" / "_src" / item_name(it)
    outdir = film_dir / "04_anim"
    rough = film_dir / "01_cut" / "rough_cut.mp4"
    a, b = float(it["start"]), float(it["end"])
    dur = b - a
    name = item_name(it)
    made = []
    if it["type"] in OVERLAY:
        src = proj / "render.webm"
        nak = outdir / f"{name}_NAKLADKA.mov"
        # VP9 alpha must be decoded with libvpx-vp9 to keep the alpha plane
        sh(["ffmpeg", "-v", "error", "-y", "-c:v", "libvpx-vp9", "-i", str(src),
            "-c:v", "prores_ks", "-profile:v", "4444", "-pix_fmt", "yuva444p10le", "-an", str(nak)])
        mix = outdir / f"{name}_MIX.mp4"
        sh(["ffmpeg", "-v", "error", "-y", "-ss", f"{a:.3f}", "-t", f"{dur:.3f}", "-i", str(rough),
            "-c:v", "libvpx-vp9", "-i", str(src),
            "-filter_complex", "[0:v][1:v]overlay=0:0:format=auto:shortest=1[v]",
            "-map", "[v]", "-map", "0:a?", "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "256k", str(mix)])
        made += [nak, mix]
    else:
        src = proj / "render.mp4"
        broll = outdir / f"{name}_BROLL.mp4"
        sh(["ffmpeg", "-v", "error", "-y", "-i", str(src), "-ss", f"{a:.3f}", "-t", f"{dur:.3f}", "-i", str(rough),
            "-map", "0:v", "-map", "1:a?", "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "256k", "-shortest", str(broll)])
        made.append(broll)
    for m in made:
        print(f"  delivered {m.name}")
    return made


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["scaffold", "render", "deliver", "all"])
    ap.add_argument("plan")
    ap.add_argument("film_dir")
    ap.add_argument("--only")
    ap.add_argument("--quality", default="standard")
    ap.add_argument("--jobs", type=int, default=2)
    a = ap.parse_args()
    plan = load_plan(Path(a.plan))
    film = Path(a.film_dir).resolve()
    items = pick(plan, a.only)
    if a.cmd in ("scaffold", "all"):
        for it in items:
            p = scaffold_one(plan, it, film)
            print(f"  scaffolded {p.name}")
    if a.cmd in ("render", "all"):
        with ThreadPoolExecutor(max_workers=max(1, a.jobs)) as ex:
            list(ex.map(lambda it: render_one(plan, it, film, a.quality), items))
    if a.cmd in ("deliver", "all"):
        for it in items:
            deliver_one(plan, it, film)


if __name__ == "__main__":
    main()
