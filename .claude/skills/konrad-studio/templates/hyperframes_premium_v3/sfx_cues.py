#!/usr/bin/env python3
"""lfpdo v4 sound-design layer: per-scene cues (scene-relative s, synced to the tweens in build_*.py / L18/L21/L26.html)
→ one global cue sheet (film time) → sfx_lfpdo.wav (separate track) via konrad-studio/scripts/sfx.py.
Names: plain = konrad-studio/assets/sfx/*.wav (click, pop, swish, tick, whoosh); "m:" = media-use bundled Pixabay set."""
import json, os, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
LF = os.path.dirname(os.path.dirname(HERE))
MU = os.path.expanduser("~/.claude/skills/media-use/audio/assets/sfx")
DB = {"whoosh": -25, "m:whoosh": -25, "m:whoosh-short": -28, "swish": -29, "pop": -27, "click": -25, "m:click-soft": -27,
      "tick": -34, "m:impact-bass-1": -24, "m:impact-bass-2": -25, "m:typing": -31, "m:notification": -29, "m:chime": -31,
      "m:ping": -29, "m:error": -31, "m:sparkle": -31, "m:glitch-3": -31, "m:whoosh-cinematic": -27}


def ticks(t0, t1, step=0.11):
    step = max(step, 0.15)
    out, t = [], t0
    while t < t1:
        out.append((round(t, 3), "tick")); t += step
    return out


P = lambda *ts: [(t, "pop") for t in ts]
S = {
    "L01": P(1.35, 3.42) + [(3.3, "swish")],
    "L02": ticks(0.45, 3.1, 0.16) + P(4.38, 4.78, 5.18, 5.58),
    "L03": [(3.25, "m:impact-bass-1"), (2.2, "pop")],
    "L04": ticks(0.3, 1.3, 0.1) + [(1.5, "m:ping"), (2.4, "pop")],
    "L06": [(0.3, "m:whoosh-short"), (1.12, "m:ping")] + P(1.85, 2.4),
    "L07": P(1.1, 2.15) + [(1.85, "swish")],
    "L08": [(t, "m:click-soft") for t in (0.96, 2.06, 2.62, 3.08)] + [(3.65, "m:impact-bass-1"), (7.4, "pop"), (8.25, "pop"),
                                                                       (7.5, "m:whoosh-short")] + ticks(7.6, 9.7, 0.12),
    "L09": P(0.25) + [(1.2, "m:sparkle")] + [(t, "m:click-soft") for t in (1.7, 1.98, 2.26)],
    "L10": P(0.35, 1.0, 4.4) + [(3.1, "m:whoosh-short"), (3.6, "m:impact-bass-1"), (4.05, "m:whoosh-short")],
    "L11": P(3.0) + [(4.75, "m:whoosh-short"), (7.7, "m:impact-bass-1"), (8.0, "m:notification")],
    "L11b": P(0.6, 1.75),
    "L12": P(0.05, 0.45) + [(7.75, "m:whoosh-short"), (8.02, "click"), (8.2, "m:notification")] + ticks(8.2, 9.5, 0.13),
    "L13": [(1.15, "pop"), (3.3, "m:error"), (4.6, "m:whoosh-short")] + [(t, "m:click-soft") for t in (5.4, 7.3, 8.4)] + [(t + 0.15, "m:ping") for t in (5.4, 7.3, 8.4)],
    "L14": P(0.62, 4.1) + [(5.5, "m:chime")],
    "L15": [(t, "click") for t in (0.5, 0.72, 0.94, 5.45, 5.6)] + P(1.7) + [(3.0, "m:error"), (4.0, "m:error"), (5.65, "m:chime")],
    "L16": P(0.05, 0.3, 1.68, 2.16, 2.78, 3.26) + [(3.82, "m:sparkle")],
    "L17": P(0.6, 1.6, 2.95) + [(2.25, "m:whoosh-short")] + [(t, "m:notification") for t in (4.3, 4.85, 5.45)] + ticks(4.2, 6.2, 0.13),
    "L18": [(0.2, "click"), (0.22, "m:typing")] + ticks(0.8, 2.0, 0.1) + [(1.6, "m:whoosh-short"), (3.55, "m:impact-bass-1"),
                                                                       (4.72, "pop"), (5.5, "swish"), (6.62, "m:impact-bass-2")],
    "L19": P(0.4, 0.96, 1.68),
    "L20": [(0.08, "m:impact-bass-1")] + P(1.05, 1.62, 2.45),
    "L21": [(0.12, "pop"), (0.95, "m:whoosh-short"), (1.55, "m:whoosh-short"), (2.2, "m:error"), (3.15, "m:whoosh-short"),
            (4.75, "m:whoosh-short"), (6.9, "m:chime"), (7.38, "m:sparkle")] + ticks(4.8, 5.8, 0.11),
    "L22": [(0.12, "pop"), (0.98, "m:impact-bass-1"), (2.2, "m:whoosh-short"), (2.9, "swish"), (4.3, "m:whoosh-short"),
            (5.4, "pop"), (6.03, "click")],
    "L23": [(0.0, "m:whoosh-cinematic"), (4.55, "pop"), (5.0, "m:click-soft")],
    "L24": P(1.35, 2.3) + [(4.5, "click"), (5.75, "click"), (6.55, "m:notification")] + ticks(7.4, 9.6, 0.18),
    "L25": P(1.55, 2.88, 3.92, 6.1) + [(4.4, "swish"), (6.55, "m:impact-bass-1")],
    "L26": ticks(0.45, 1.6, 0.1) + [(1.84, "m:impact-bass-1")] + [(1.86 + i * 0.09, "pop") for i in range(6)] +
           [(4.3, "m:whoosh-short"), (5.75, "m:chime")] + ticks(4.35, 5.6, 0.11),
    "L26b": P(0.3, 4.3) + [(3.6, "m:impact-bass-1"), (6.55, "m:impact-bass-1")],
    "L27": P(0.1, 1.75) + ticks(4.45, 5.6, 0.1) + [(7.1, "m:impact-bass-1")] + [(7.15 + i * 0.13, "pop") for i in range(6)],
    "L28": [(0.0, "swish"), (0.95, "m:impact-bass-1")] + [(1.05 + i * 0.12, "pop") for i in range(6)] + ticks(2.0, 3.5, 0.1) + [(7.0, "m:sparkle")],
    "L29": [(0.85, "m:impact-bass-1")] + ticks(1.9, 6.0, 0.15) + P(6.05, 6.95, 7.45, 7.9, 9.55) + [(10.5, "m:error")],
    "L30": ticks(1.05, 1.9, 0.1) + [(1.95, "m:ping"), (5.6, "m:whoosh-short"), (5.85, "m:chime")] + ticks(5.6, 6.4, 0.1),
    "L31": P(1.2, 1.5, 3.85, 4.6, 5.5, 6.05) + [(2.7, "m:whoosh")],
    "L32": P(0.1, 3.7, 5.35, 6.6) + [(2.8, "m:sparkle"), (8.6, "m:chime")],
    "L32b": P(0.6, 1.85) + [(1.0, "m:whoosh-short")],
    "L33": [(0.3, "m:whoosh-short"), (0.95, "click"), (1.05, "m:notification")],
}

idx = {x["key"]: x for x in json.load(open(os.path.join(LF, "index.json")))}
for k, (a, b) in json.load(open(os.path.join(HERE, "timing.json"))).items():
    idx[k]["in"], idx[k]["out"] = a, b
cues = []
for k, lst in S.items():
    a, b, ov = idx[k]["in"], idx[k]["out"], idx[k]["overlay"]
    if ov:   # card slides in / out
        lst = lst + [(0.02, "swish"), (b - a - 0.34, "m:whoosh-short")]
    else:    # whip in / out of the full-screen scene
        lst = lst + [(-0.08, "m:whoosh"), (b - a - 0.18, "m:whoosh-short")]
    cues += [(a + t, n) for t, n in lst]
cues += [(49.0 - 0.08, "m:whoosh"), (52.6 - 0.18, "m:whoosh-short")]          # L05 billboard clip
# wall callouts: a pop on every line landing
CO = __import__("build_callouts").C
for k, (a, b, lines) in CO.items():
    cues += [(a + t + 0.05, "pop") for _, _, t in lines]
cues.sort()
sheet = [{"t": round(t, 3), "sfx": (os.path.join(MU, n[2:] + ".mp3") if n.startswith("m:") else n), "db": DB[n]} for t, n in cues]
json.dump(sheet, open(os.path.join(HERE, "sfx_cues.json"), "w"), indent=0)
dur = 758.75
subprocess.run(["/Library/Frameworks/Python.framework/Versions/3.13/bin/python3",
                os.path.expanduser("~/.claude/skills/konrad-studio/scripts/sfx.py"),
                os.path.join(HERE, "sfx_cues.json"), os.path.join(LF, "sfx_lfpdo.wav"), "--dur", str(dur)], check=True)
print(len(sheet), "cues,", round(len(sheet) / (dur / 60), 1), "per min overall")
