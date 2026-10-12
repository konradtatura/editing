#!/usr/bin/env python3
"""QA for delivered animations and the final film.

usage:
  qa.py sheets <film_dir> [--only ID,ID]   # contact sheet per animation -> qa/sheets/<name>.jpg (frames: 0.3s, 1.2s, mid, end-0.4s)
  qa.py check  <film_dir> <plan.json>      # automatic checks -> qa/report.md (+ exit 1 on errors)
  qa.py final  <film_dir>                  # loudness / duration / sync of 06_final/FINAL.mp4

Visual QA (Claude reads the sheets) looks for: text over the face, clipped text, empty frames,
wrong numbers, stiff/unfinished entries, style drift. Automatic QA covers what a script can measure.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path


def probe(p: Path) -> dict:
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                        "format=duration:stream=codec_type,codec_name,pix_fmt,width,height,r_frame_rate,nb_frames",
                        "-of", "json", str(p)], capture_output=True, text=True)
    return json.loads(r.stdout or "{}")


def dur(p: Path) -> float:
    try:
        return float(probe(p)["format"]["duration"])
    except Exception:
        return 0.0


def sheet(src: Path, out: Path, label: str) -> None:
    d = dur(src)
    ts = [min(0.3, d * 0.1), min(1.2, d * 0.35), d / 2, max(0, d - 0.4)]
    out.parent.mkdir(parents=True, exist_ok=True)
    tmp = []
    for i, t in enumerate(ts):
        f = out.parent / f".{out.stem}_{i}.jpg"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.3f}", "-i", str(src), "-frames:v", "1",
                        "-vf", "scale=640:-2,pad=iw+6:ih:0:0:color=black",
                        str(f)], capture_output=True)
        tmp.append(f)
    ins = sum([["-i", str(f)] for f in tmp], [])
    subprocess.run(["ffmpeg", "-v", "error", "-y", *ins, "-filter_complex",
                    f"hstack=inputs={len(tmp)}",
                    str(out)], capture_output=True)
    for f in tmp:
        f.unlink(missing_ok=True)


def cmd_sheets(film: Path, only: str | None) -> None:
    anim = film / "04_anim"
    files = sorted([p for p in anim.glob("*.mp4") if p.stem.endswith(("_MIX", "_BROLL"))])
    if only:
        ids = set(only.split(","))
        files = [p for p in files if p.name.split("_")[0] in ids]
    for p in files:
        out = film / "qa" / "sheets" / f"{p.stem}.jpg"
        sheet(p, out, p.stem.replace("'", ""))
        print(out)


def blackish(p: Path) -> float:
    r = subprocess.run(["ffmpeg", "-v", "info", "-i", str(p), "-vf", "blackdetect=d=0.25:pic_th=0.97", "-an", "-f", "null", "-"],
                       capture_output=True, text=True)
    return sum(float(m) for m in re.findall(r"black_duration:([\d.]+)", r.stderr))


def cmd_check(film: Path, plan_path: Path) -> int:
    plan = json.loads(plan_path.read_text())
    anim = film / "04_anim"
    rows, errors = [], 0
    for it in plan.get("items", []):
        exp = float(it["end"]) - float(it["start"])
        hits = sorted(anim.glob(f"{it['id']}_*"))
        hits = [h for h in hits if h.is_file()]
        if not hits:
            rows.append(f"| {it['id']} | {it['type']} | BRAK PLIKU | ✗ |"); errors += 1; continue
        for h in hits:
            pr = probe(h)
            vs = [s for s in pr.get("streams", []) if s.get("codec_type") == "video"]
            aus = [s for s in pr.get("streams", []) if s.get("codec_type") == "audio"]
            d = float(pr.get("format", {}).get("duration", 0))
            issues = []
            if abs(d - exp) > 0.12:
                issues.append(f"czas {d:.2f}s ≠ plan {exp:.2f}s")
            if h.suffix == ".mov":
                pf = vs[0].get("pix_fmt", "") if vs else ""
                if "yuva" not in pf and "argb" not in pf:
                    issues.append(f"brak alfy ({pf})")
            else:
                if not aus:
                    issues.append("brak audio oryginału")
                b = blackish(h)
                if b > 0.3:
                    issues.append(f"czarne klatki {b:.1f}s")
            ok = "✓" if not issues else "✗"
            errors += 1 if issues else 0
            rows.append(f"| {it['id']} | {it['type']} | {h.name} | {d:.2f}s | {'; '.join(issues) or 'ok'} | {ok} |")
    rep = film / "qa" / "report.md"
    rep.parent.mkdir(parents=True, exist_ok=True)
    rep.write_text("# QA animacji\n\n| id | typ | plik | czas | uwagi | |\n|---|---|---|---|---|---|\n" + "\n".join(rows) + "\n")
    print(rep.read_text())
    return 1 if errors else 0


def cmd_final(film: Path) -> int:
    fin = film / "06_final" / "FINAL.mp4"
    rough = film / "01_cut" / "rough_cut.mp4"
    r = subprocess.run(["ffmpeg", "-v", "info", "-i", str(fin), "-af", "ebur128=peak=true", "-f", "null", "-"],
                       capture_output=True, text=True)
    lufs = re.findall(r"I:\s+(-?[\d.]+) LUFS", r.stderr)
    peak = re.findall(r"Peak:\s+(-?[\d.]+) dBFS", r.stderr)
    out = [f"FINAL: {dur(fin):.2f}s | rough cut: {dur(rough):.2f}s",
           f"Loudness: {lufs[-1] if lufs else '?'} LUFS (cel -14) | true peak: {peak[-1] if peak else '?'} dBFS (cel ≤ -1)"]
    bad = 0
    if abs(dur(fin) - dur(rough)) > 0.2:
        out.append("✗ długość FINAL różni się od rough cut — sprawdź sync"); bad = 1
    if lufs and abs(float(lufs[-1]) + 14) > 1.0:
        out.append("✗ głośność poza -14 ±1 LUFS"); bad = 1
    print("\n".join(out))
    return bad


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["sheets", "check", "final"])
    ap.add_argument("film_dir")
    ap.add_argument("plan", nargs="?")
    ap.add_argument("--only")
    a = ap.parse_args()
    film = Path(a.film_dir).resolve()
    if a.cmd == "sheets":
        cmd_sheets(film, a.only)
    elif a.cmd == "check":
        sys.exit(cmd_check(film, Path(a.plan)))
    else:
        sys.exit(cmd_final(film))


if __name__ == "__main__":
    main()
