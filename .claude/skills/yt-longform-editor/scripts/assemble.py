#!/usr/bin/env python3
"""Assemble the finished film: rough cut + punch-ins + every animation + SFX + music, loudness -14 LUFS.

usage: assemble.py <plan.json> <film_dir> [--preview]   # --preview: 960x540 fast encode for review

Reads 01_cut/rough_cut.mp4 and 04_anim/*_NAKLADKA.mov / *_BROLL.mp4 (from anim.py deliver).
Writes 05_audio/sfx.wav, 05_audio/mix.wav and 06_final/FINAL.mp4 (or FINAL_podglad.mp4).

plan.json keys used here:
  film.speakerBox            punch-in anchor (head centre)
  film.music                 optional path to a music bed (mp3/wav); looped, ducked under the voice
  film.musicVolume           dB below the voice (default -24)
  film.musicCuts             [[start, end], ...] music drops out (pivots / key statements)
  punch                      [{"start", "end", "scale": 1.12}]  static punch-ins on the talking head
  items[].sfx                false (no sound) or [{"t": rel_sec, "name": "pop", "vol": 0.4}] to override defaults
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import wave
from pathlib import Path

import numpy as np

SKILL = Path(__file__).resolve().parent.parent
SFX_DIR = SKILL / "assets" / "sfx"
SR = 48000
OVERLAY = {"T1", "T2", "T3", "T4"}


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        sys.stderr.write(r.stderr[-4000:])
        raise SystemExit(f"failed: {' '.join(map(str, cmd))[:300]}")
    return r


def dur(p: Path) -> float:
    return float(run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)]).stdout.strip())


def item_name(it: dict) -> str:
    t = float(it["start"])
    tc = f"{int(t // 60):02d}m{t % 60:05.2f}s".replace(".", "_")
    return f"{it['id']}_{tc}_{it['type']}"


def default_sfx(it: dict) -> list[dict]:
    """Every graphic gets a sound (Iman rule), quiet enough to feel, not hear."""
    t, p, d = it["type"], it.get("params", {}), float(it["end"]) - float(it["start"])
    ev = []
    if t == "T1":
        ev.append({"t": 0.03, "name": "whoosh", "vol": 0.30})
    elif t in ("T2", "T4"):
        for i, x in enumerate(p.get("items", [])):
            ev.append({"t": x.get("at", 0.08 + i * 0.5), "name": "pop", "vol": 0.40})
    elif t == "T3":
        ev += [{"t": 0.04, "name": "whoosh", "vol": 0.30}, {"t": 1.15, "name": "tick", "vol": 0.35}]
    elif t == "T5":
        ev += [{"t": 0.0, "name": "swish", "vol": 0.40}, {"t": max(0, d - 0.82), "name": "swish", "vol": 0.32}]
        for x in p.get("content", {}).get("items", []):
            if "at" in x:
                ev.append({"t": x["at"], "name": "pop", "vol": 0.38})
    elif t == "T6":
        ev += [{"t": 0.0, "name": "swish", "vol": 0.40}, {"t": max(0, d - 0.82), "name": "swish", "vol": 0.32}]
        if p.get("focus"):
            fa = p.get("focusAt", 1.0)
            ev += [{"t": fa, "name": "whoosh", "vol": 0.25}, {"t": fa + 1.75, "name": "click", "vol": 0.55}]
    elif t == "T7":
        ev.append({"t": 0.0, "name": "whoosh", "vol": 0.35})
        if p.get("variant") == "number":
            ev.append({"t": 1.5, "name": "tick", "vol": 0.35})
        if p.get("variant") == "compare":
            ev.append({"t": p.get("b", {}).get("at", 1.05), "name": "pop", "vol": 0.40})
    elif t == "T9":
        ev += [{"t": 0.0, "name": "hit", "vol": 0.55}, {"t": 0.02, "name": "whoosh", "vol": 0.28}]
    elif t == "T10":
        ev.append({"t": 0.05, "name": "whoosh", "vol": 0.30})
    return ev


def load_wav(path: Path) -> np.ndarray:
    tmp = path
    w = wave.open(str(tmp))
    if w.getframerate() != SR or w.getsampwidth() != 2:
        w.close()
        conv = path.with_suffix(".48k.wav")
        run(["ffmpeg", "-v", "error", "-y", "-i", str(path), "-ac", "1", "-ar", str(SR), "-c:a", "pcm_s16le", str(conv)])
        w = wave.open(str(conv))
    x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
    if w.getnchannels() == 2:
        x = x.reshape(-1, 2).mean(1)
    return x


def write_wav(path: Path, x: np.ndarray) -> None:
    x = np.clip(x, -1, 1)
    w = wave.open(str(path), "wb")
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((x * 32767).astype(np.int16).tobytes())
    w.close()


def build_sfx(plan: dict, total: float, out: Path) -> int:
    buf = np.zeros(int(total * SR) + SR, np.float32)
    cache, n = {}, 0
    for it in plan.get("items", []):
        evs = it.get("sfx")
        if evs is False:
            continue
        for e in (evs if isinstance(evs, list) else default_sfx(it)):
            name = e["name"]
            if name not in cache:
                f = SFX_DIR / f"{name}.wav"
                if not f.exists():
                    continue
                cache[name] = load_wav(f)
            s = cache[name] * float(e.get("vol", 0.4))
            i = int((float(it["start"]) + float(e.get("t", 0))) * SR)
            if 0 <= i < len(buf):
                j = min(len(buf), i + len(s))
                buf[i:j] += s[: j - i]
                n += 1
    write_wav(out, buf[: int(total * SR)])
    return n


def build_music(plan: dict, total: float, out: Path) -> bool:
    f = plan.get("film", {}).get("music")
    if not f or not Path(f).expanduser().exists():
        return False
    src = out.with_name("music_src.wav")
    run(["ffmpeg", "-v", "error", "-y", "-i", str(Path(f).expanduser()), "-ac", "1", "-ar", str(SR), "-c:a", "pcm_s16le", str(src)])
    m = load_wav(src)
    reps = int(np.ceil(total * SR / len(m)))
    m = np.tile(m, reps)[: int(total * SR)]
    g = np.ones_like(m)
    fade = int(0.35 * SR)
    for a, b in plan["film"].get("musicCuts", []):          # music drops out on pivots, comes back after
        ia, ib = int(a * SR), int(b * SR)
        g[ia:ib] = 0
        g[max(0, ia - fade):ia] = np.linspace(1, 0, ia - max(0, ia - fade))
        g[ib:min(len(g), ib + fade)] = np.linspace(0, 1, min(len(g), ib + fade) - ib)
    m = m * g * (10 ** (plan["film"].get("musicVolume", -24) / 20))
    m[: int(1.5 * SR)] *= np.linspace(0, 1, int(1.5 * SR))
    m[-int(2.5 * SR):] *= np.linspace(1, 0, int(2.5 * SR))
    write_wav(out, m)
    return True


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("plan")
    ap.add_argument("film_dir")
    ap.add_argument("--preview", action="store_true")
    a = ap.parse_args()
    plan = json.loads(Path(a.plan).read_text())
    film = Path(a.film_dir).resolve()
    f = plan.get("film", {})
    W, H = f.get("w", 1920), f.get("h", 1080)
    rough = film / "01_cut" / "rough_cut.mp4"
    total = dur(rough)
    (film / "05_audio").mkdir(exist_ok=True)
    (film / "06_final").mkdir(exist_ok=True)

    # ---- video graph
    inputs = ["-i", str(rough)]
    fc = []
    # punch-ins: split the talking head into segments, zoom the punched ones around the head
    box = f.get("speakerBox") or [W * 0.38, H * 0.06, W * 0.62, H * 0.58]
    cx, cy = (box[0] + box[2]) / 2, (box[1] + box[3]) / 2
    cuts = sorted({0.0, total} | {float(p["start"]) for p in plan.get("punch", [])} | {float(p["end"]) for p in plan.get("punch", [])})
    cuts = [c for c in cuts if 0 <= c <= total]
    segs = []
    for s, e in zip(cuts[:-1], cuts[1:]):
        if e - s < 0.02:
            continue
        z = next((float(p.get("scale", 1.12)) for p in plan.get("punch", []) if float(p["start"]) <= s + 1e-3 and e <= float(p["end"]) + 1e-3), 1.0)
        segs.append((s, e, z))
    for k, (s, e, z) in enumerate(segs):
        chain = f"[0:v]trim=start={s:.3f}:end={e:.3f},setpts=PTS-STARTPTS"
        if z > 1.001:
            sw, sh = int(W * z) // 2 * 2, int(H * z) // 2 * 2
            x = int(min(max(cx * z - W / 2, 0), sw - W)); y = int(min(max(cy * z - H / 2, 0), sh - H))
            chain += f",scale={sw}:{sh}:flags=lanczos,crop={W}:{H}:{x}:{y}"
        fc.append(chain + f"[s{k}]")
    fc.append("".join(f"[s{k}]" for k in range(len(segs))) + f"concat=n={len(segs)}:v=1:a=0,format=yuv420p[base]")
    last = "base"
    n_in = 1
    for it in sorted(plan.get("items", []), key=lambda x: float(x["start"])):
        name = item_name(it)
        st, en = float(it["start"]), float(it["end"])
        src = film / "04_anim" / (f"{name}_NAKLADKA.mov" if it["type"] in OVERLAY else f"{name}_BROLL.mp4")
        if not src.exists():
            print(f"  ! missing {src.name} — skipped")
            continue
        inputs += ["-itsoffset", f"{st:.3f}", "-i", str(src)]
        fc.append(f"[{n_in}:v]setpts=PTS[v{n_in}]")
        fc.append(f"[{last}][v{n_in}]overlay=0:0:eof_action=pass:enable='between(t,{st:.3f},{en - 0.001:.3f})'[o{n_in}]")
        last = f"o{n_in}"
        n_in += 1
    if a.preview:
        fc.append(f"[{last}]scale=960:540[vout]")
    else:
        fc.append(f"[{last}]null[vout]")

    # ---- audio: voice + sfx + ducked music, then two-pass loudness to -14 LUFS / -1.5 dBTP
    sfx = film / "05_audio" / "sfx.wav"
    n_sfx = build_sfx(plan, total, sfx)
    music = film / "05_audio" / "music.wav"
    has_music = build_music(plan, total, music)
    ain = ["-i", str(rough), "-i", str(sfx)] + (["-i", str(music)] if has_music else [])
    afc = [f"[0:a]aresample={SR},pan=mono|c0=c0,asplit=2[voice][vkey]", f"[1:a]aresample={SR}[sfx]"]
    if has_music:
        afc.append(f"[2:a]aresample={SR}[mus];[mus][vkey]sidechaincompress=threshold=0.04:ratio=6:attack=15:release=350[duck]")
        afc.append("[voice][sfx][duck]amix=inputs=3:normalize=0[mixed]")
    else:
        afc.append("[vkey]anullsink;[voice][sfx]amix=inputs=2:normalize=0[mixed]")
    mix_raw = film / "05_audio" / "mix_raw.wav"
    run(["ffmpeg", "-v", "error", "-y", *ain, "-filter_complex", ";".join(afc), "-map", "[mixed]", "-c:a", "pcm_s24le", "-ar", str(SR), str(mix_raw)])
    # broadcast-style voice dynamics: gentle compression + peak limiting, so -14 LUFS fits under -1.5 dBTP
    mix_dyn = film / "05_audio" / "mix_dyn.wav"
    run(["ffmpeg", "-v", "error", "-y", "-i", str(mix_raw), "-af",
         "acompressor=threshold=0.063:ratio=3:attack=8:release=140:knee=4,alimiter=limit=0.6:attack=4:release=60:level=disabled",
         "-c:a", "pcm_s24le", str(mix_dyn)])
    mix_raw = mix_dyn
    meas = run(["ffmpeg", "-v", "info", "-i", str(mix_raw), "-af", "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"]).stderr
    js = json.loads(meas[meas.rindex("{"): meas.rindex("}") + 1])
    ln = (f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={js['input_i']}:measured_TP={js['input_tp']}:measured_LRA={js['input_lra']}:"
          f"measured_thresh={js['input_thresh']}:offset={js['target_offset']}:linear=true")
    mix = film / "05_audio" / "mix.wav"
    # gentle limiter first so the linear gain is not blocked by a few speech peaks
    run(["ffmpeg", "-v", "error", "-y", "-i", str(mix_raw), "-af", f"{ln},aresample=48000",
         "-c:a", "pcm_s24le", str(mix)])

    graph = film / "06_final" / "_graph.txt"
    graph.write_text(";\n".join(fc))
    out = film / "06_final" / ("FINAL_podglad.mp4" if a.preview else "FINAL.mp4")
    venc = ["-c:v", "libx264", "-preset", "veryfast", "-crf", "26"] if a.preview else ["-c:v", "libx264", "-preset", "medium", "-crf", "17"]
    run(["ffmpeg", "-v", "error", "-y", *inputs, "-i", str(mix), "-filter_complex_script", str(graph), "-map", "[vout]", "-map", f"{n_in}:a",
         *venc, "-pix_fmt", "yuv420p", "-r", str(f.get("fps", 30)), "-c:a", "aac", "-b:a", "256k", "-ar", "48000",
         "-movflags", "+faststart", "-t", f"{total:.3f}", str(out)])
    print(f"{out.name}: {total:.1f}s, {len(segs)} segments ({sum(1 for s in segs if s[2] > 1)} punch-ins), "
          f"{n_in - 1} animations, {n_sfx} sfx, music: {'yes' if has_music else 'no'}")


if __name__ == "__main__":
    main()
