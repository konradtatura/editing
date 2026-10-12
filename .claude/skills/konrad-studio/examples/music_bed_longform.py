#!/usr/bin/env python3
"""Iman-style music bed for „3 modele”: 3 vidIQ tracks edited to the film (sections, loops, drops on words, silences on
punchlines), ducked under the voice, mixed into FINAL. Writes MUZYKA.wav (stem) and ../FINAL_muzyka.mp4."""
import json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__)); P = os.path.dirname(HERE)
DUR = 763.133
SR = 48000
# (track, film_start, film_end, [(track_in, track_out), ...] played back to back with 3 s crossfades)
SECTIONS = [
    ("A_napiecie.wav", 0.0, 217.6, [(0.26, 160.0), (22.16, 82.0)]),     # drop 22.16 → „Nazywam się Konrad” 21.90
    ("B_srodek.wav", 217.6, 513.6, [(0.0, 161.0), (24.0, 160.0)]),
    ("C_final.wav", 513.6, DUR, [(12.78, 168.0), (70.0, 165.0)]),       # drop 32.02 → „cztery elementy” 532.84
]
SILENCE = [(19.20, 21.86), (204.05, 205.60), (463.90, 465.45), (692.60, 694.30), (757.8, DUR)]
FADE_END = (755.0, 757.8)          # music leaves before the one black card
TARGET_LUFS = -22.0                # ~16 dB under the voice after gentle ducking (measured: ducked bed ≈ −30 LUFS)


def lufs(f):
    e = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", f, "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
    return float(e.rsplit("I:", 1)[1].split("LUFS")[0])


def section(track, a, b, parts, out):
    """Concatenate the track parts with 3 s crossfades, cut to the section length, fade the edges, normalize loudness."""
    src = os.path.join(HERE, track); n = len(parts)
    ins = sum([["-ss", f"{i:.3f}", "-to", f"{o:.3f}", "-i", src] for i, o in parts], [])
    f = "".join(f"[{k}:a]aresample={SR},aformat=channel_layouts=stereo[p{k}];" for k in range(n))
    last = "p0"
    for k in range(1, n):
        f += f"[{last}][p{k}]acrossfade=d=3:c1=tri:c2=tri[x{k}];"; last = f"x{k}"
    L = b - a
    f += f"[{last}]atrim=0:{L:.3f},afade=t=in:st=0:d=0.4,afade=t=out:st={L - 1.6:.3f}:d=1.6[o]"
    tmp = out + ".raw.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", *ins, "-filter_complex", f, "-map", "[o]", "-c:a", "pcm_s16le", tmp], check=True)
    g = TARGET_LUFS - lufs(tmp)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", tmp, "-af", f"volume={g:.2f}dB", "-c:a", "pcm_s16le", out], check=True)
    os.remove(tmp)
    return g


def main():
    secs = []
    for k, (t, a, b, parts) in enumerate(SECTIONS):
        o = os.path.join(HERE, f"sec{k}.wav"); g = section(t, a, b, parts, o); secs.append((o, a)); print(f"section {k}: {t} {a:.1f}-{b:.1f} gain {g:+.1f} dB")
    ins = sum([["-i", o] for o, _ in secs], [])
    f = "".join(f"[{k}:a]adelay={int(a * 1000)}:all=1[d{k}];" for k, (_, a) in enumerate(secs))
    f += "".join(f"[d{k}]" for k in range(len(secs))) + f"amix=inputs={len(secs)}:normalize=0:duration=longest,"
    f += "highpass=f=45,equalizer=f=2600:t=q:w=1.2:g=-5,"
    gate = "+".join(f"between(t,{a:.2f},{b:.2f})" for a, b in SILENCE)
    f += f"volume='if({gate},0,1)':eval=frame,afade=t=out:st={FADE_END[0]}:d={FADE_END[1] - FADE_END[0]},atrim=0:{DUR}[m]"
    stem = os.path.join(HERE, "MUZYKA.wav")
    subprocess.run(["ffmpeg", "-v", "error", "-y", *ins, "-filter_complex", f, "-map", "[m]", "-c:a", "pcm_s16le", stem], check=True)
    print("stem", stem)
    # mix into the finished film: music ducks under the voice/SFX track of FINAL, then a safety limiter
    for src, dst in [("FINAL_bez-muzyki.mp4", "FINAL.mp4")]:
        s, d = os.path.join(P, src), os.path.join(P, dst)
        part = d.replace(".mp4", ".part.mp4")
        fc = ("[0:a]aresample=48000,asplit=2[v][sc];[1:a]aresample=48000[m0];"
              "[m0][sc]sidechaincompress=threshold=0.06:ratio=3:attack=20:release=400:makeup=1[m];"
              "[v][m]amix=inputs=2:normalize=0:duration=first,alimiter=limit=0.89:level=false[a]")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", s, "-i", stem, "-filter_complex", fc, "-map", "0:v", "-map", "[a]",
                        "-c:v", "copy", "-c:a", "aac", "-b:a", "320k", "-movflags", "+faststart", part], check=True)
        os.replace(part, d)
        e = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", d, "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True).stderr
        tail = e.rsplit("Summary:", 1)[1]
        I = tail.split("I:")[1].split("LUFS")[0].strip(); pk = tail.split("Peak:")[1].split("dBFS")[0].strip()
        print(f"{dst}: {I} LUFS, true peak {pk} dBFS")


if __name__ == "__main__":
    main()
