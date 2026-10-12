# Longform face-first re-edit, final assembly (YT_Ciezka-praca, 2026-10-04): reedit.json windows + jump zooms + SFX + timestamp-true audio.
#!/usr/bin/env python3
"""v2 (2026-10-04, „za dużo animacji, za mało mojej twarzy”): face-first assembly from edit/reedit.json.
  full  → b-roll windows (trimmed BROLL clips, hard cuts)
  card  → floating cards over the face (Animacje_v2/*_KARTA.mov for converted ones, NAKLADKA .mov for original overlays)
  face  → everything else, with Iman-style jump zooms (100 ↔ 114 %) on sentence starts / cut joins; cards force 100 %.
Audio: CUT voice decoded by timestamp, mastered to −14 LUFS; soft swish on b-roll entrances, soft pop on cards.
Writes YT_Ciezka-praca_FINAL_v2.mp4 (+ _bez-sfx) and edit/v2_plan.json (zoom plan + stats)."""
import json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SK = os.path.expanduser("~/.claude/skills/konrad-studio")
P = sys.executable
SRC = os.path.join(HERE, "YT_Ciezka-praca_CUT.mp4")
OUT = os.path.join(HERE, "YT_Ciezka-praca_FINAL_v2.mp4")
R = json.load(open(os.path.join(HERE, "edit", "reedit.json")))
D = R["D"]
IDX = {i["key"]: i for i in json.load(open(os.path.join(HERE, "index.json")))}
ZOOM = 114
run = lambda a: subprocess.run(a, check=True)

full = sorted((a, b, k) for k, (a, b) in R["full"].items())
cards = sorted((a, b, k) for k, (a, b) in R["card"].items())

# ---------------------------------------------------------------- face zoom plan
d = json.load(open(os.path.join(HERE, "tr", "cut.json")))
ws = [w for s in d["segments"] for w in s["words"]]
sent = [ws[i + 1]["start"] for i in range(len(ws) - 1) if ws[i]["word"].strip()[-1:] in ".?!"]
joins = json.load(open(os.path.join(HERE, "edit", "joins.json")))
face, t = [], 0.0
for a, b, _ in full:
    if a - t > 0.05:
        face.append((t, a))
    t = b
if D - t > 0.05:
    face.append((t, D))
in_card = lambda x: any(a - 0.25 <= x <= b + 0.25 for a, b, _ in cards)
zoomed, level = [], 0          # level toggles 0/1 across the whole film so returns from b-roll alternate framing
for s, e in face:
    cands = sorted(set([round(x, 3) for x in sent if s + 2.0 < x < e - 1.6] + [round(x, 3) for x in joins if s + 2.0 < x < e - 1.6]))
    cuts, last = [s], s
    for p in cands:
        if in_card(p):
            continue
        if (p in sent and p - last >= 2.2) or p - last >= 5.5:
            cuts.append(p); last = p
    cuts.append(e)
    for i in range(len(cuts) - 1):
        a, b = cuts[i], cuts[i + 1]
        if level and not any(ca < b and cb > a for ca, cb, _ in cards):
            zoomed.append((a, b))
        level ^= 1
# cards always on the wide shot
zoomed = [(a, b) for a, b in zoomed]

# ---------------------------------------------------------------- SFX: soft swish on b-roll entrances, soft pop on cards
cues = [{"t": round(max(0, a - 0.06), 3), "sfx": "swish", "db": -33} for a, b, _ in full] + \
       [{"t": round(a + 0.02, 3), "sfx": "pop", "db": -33} for a, b, _ in cards]
json.dump(cues, open(os.path.join(HERE, "edit", "v2_cues.json"), "w"), indent=1)
sfx = os.path.join(HERE, "edit", "v2_sfx.wav")
run([P, f"{SK}/scripts/sfx.py", os.path.join(HERE, "edit", "v2_cues.json"), sfx, "--dur", str(D)])

# ---------------------------------------------------------------- audio master (timestamp-true decode of the CUT)
pre = ("aresample=async=1:first_pts=0,highpass=f=70,acompressor=threshold=-26dB:ratio=2.5:attack=8:release=120:makeup=1,"
       "aformat=channel_layouts=stereo")
def master(inputs, fc_in, out):
    m = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", *inputs, "-filter_complex",
                        f"{fc_in},apad=pad_dur=1,loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"],
                       capture_output=True, text=True).stderr
    j = json.loads(m[m.rindex("{"):m.rindex("}") + 1])
    ln = (f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={j['input_i']}:measured_TP={j['input_tp']}:"
          f"measured_LRA={j['input_lra']}:measured_thresh={j['input_thresh']}:offset={j['target_offset']}:linear=true")
    run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", f"{fc_in},apad=pad_dur=1,{ln},aresample=48000,atrim=0:{D}",
         "-c:a", "pcm_s24le", out])
voice = os.path.join(HERE, "edit", "final_voice.wav")
mix = os.path.join(HERE, "edit", "v2_mix.wav")
if not os.path.exists(voice) or os.path.getmtime(voice) < os.path.getmtime(SRC):
    master(["-i", SRC], f"[0:a]{pre}", voice)
master(["-i", SRC, "-i", sfx], f"[0:a]{pre}[v];[v][1:a]amix=inputs=2:normalize=0:duration=first", mix)

# ---------------------------------------------------------------- picture
between = lambda iv: "+".join(f"between(t,{a:.3f},{b - 0.001:.3f})" for a, b in iv) or "0"
zw = int(round(1920 * ZOOM / 100 / 2)) * 2
fc = ["[0:v]split[b][z]", f"[z]scale={zw}:-2,crop=1920:1080:(iw-1920)/2:(ih-1080)*0.35[zz]",
      f"[b][zz]overlay=enable='{between(zoomed)}'[v0]"]
args = ["ffmpeg", "-v", "error", "-stats", "-y", "-i", SRC]
last, n = "v0", 0
for a, b, k in cards:                                   # cards over the face
    n += 1
    conv = os.path.join(HERE, "Animacje_v2", f"{k}_KARTA.mov")
    if os.path.exists(conv):
        args += ["-itsoffset", f"{a:.3f}", "-i", conv]
        fx = f"[{n}:v]format=yuva444p10le[c{n}]"
    else:
        it = IDX[k]
        mov = it["file"].replace("_MIX.mp4", "_NAKLADKA.mov")
        dd = b - a
        # trim (not input -ss): -ss + setpts re-based the seek pre-roll and made trimmed clips run late
        args += ["-i", mov]
        fades = []
        if a - it["in"] > 0.05:
            fades.append("fade=t=in:st=0:d=0.22:alpha=1")
        if it["out"] - b > 0.05:
            fades.append(f"fade=t=out:st={dd - 0.26:.3f}:d=0.26:alpha=1")
        fx = (f"[{n}:v]format=yuva444p10le,trim=start={a - it['in']:.3f}:end={b - it['in']:.3f},setpts=PTS-STARTPTS"
              + ("," + ",".join(fades) if fades else "") + f",setpts=PTS+{a:.3f}/TB[c{n}]")
    fc.append(fx)
    fc.append(f"[{last}][c{n}]overlay=enable='between(t,{a:.3f},{b - 0.001:.3f})':eof_action=pass:format=auto[v{n}]")
    last = f"v{n}"
for a, b, k in full:                                    # full-screen b-rolls on top, trimmed to their windows
    n += 1
    it = IDX[k]
    args += ["-i", it["file"]]
    fc.append(f"[{n}:v]trim=start={a - it['in']:.3f}:end={min(b - it['in'] + 0.3, it['out'] - it['in'] + 1):.3f},"
              f"setpts=PTS-STARTPTS+{a:.3f}/TB,tpad=stop_mode=clone:stop_duration=0.5[c{n}]")
    fc.append(f"[{last}][c{n}]overlay=enable='between(t,{a:.3f},{b - 0.001:.3f})':eof_action=pass[v{n}]")
    last = f"v{n}"
args += ["-i", mix, "-filter_complex", ";".join(fc), "-map", f"[{last}]", "-map", f"{n + 1}:a",
         "-c:v", "libx264", "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p", "-r", "30",
         "-c:a", "aac", "-b:a", "320k", "-shortest", "-movflags", "+faststart", OUT]
run(args)
run(["ffmpeg", "-v", "error", "-y", "-i", OUT, "-i", voice, "-map", "0:v", "-map", "1:a", "-c:v", "copy",
     "-c:a", "aac", "-b:a", "320k", "-shortest", "-movflags", "+faststart", OUT.replace("_FINAL_v2", "_FINAL_v2_bez-sfx")])
F = sum(b - a for a, b, _ in full); C = sum(b - a for a, b, _ in cards); Z = sum(b - a for a, b in zoomed)
json.dump({"zoomed": zoomed, "face": face, "stats": {"full": F, "card": C, "face": D - F - C, "zoomed": Z}},
          open(os.path.join(HERE, "edit", "v2_plan.json"), "w"), indent=1)
print(f"full {100*F/D:.0f}%  card {100*C/D:.0f}%  face {100*(D-F-C)/D:.0f}%  zoomed face {Z:.0f}s  → {OUT}")
