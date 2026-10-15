#!/usr/bin/env python3
"""SFX layer for „3 modele”: cues read from the built scene pages (every kit call with a resolvable time gets its sound),
plus whoosh/swish on scene entries and card exits. Writes anim/sfx_cues.json and ../SFX.wav (levels: detale-montazu.md)."""
import json, os, re, subprocess
from page import HERE

MU = os.path.expanduser("~/.claude/skills/konrad-studio/assets/sfx_pixabay")  # copy of media-use sfx (portable)
DB = {"whoosh": -26, "m:whoosh-short": -29, "swish": -30, "pop": -29, "click": -26, "m:click-soft": -28, "tick": -35,
      "m:impact-bass-1": -27, "m:typing": -32, "m:notification": -30, "m:ping": -30, "m:error": -32}
KIND = {"stamp": "pop", "click": "click", "toggle": "m:click-soft", "shake": "m:error", "type": "m:typing", "tap": "click",
        "draw": "swish", "rise": "pop", "lift": "pop", "count": "tick", "weight": "pop", "strike": "swish"}
SC = json.load(open(os.path.join(HERE, "scenes.json")))
C = []


def num(expr, env):
    e = expr.strip()
    for k in sorted(env, key=len, reverse=True):
        e = re.sub(rf"\b{k}\b", str(env[k]), e)
    if not re.fullmatch(r"[0-9.+\-*/ ()]+", e):
        return None
    try:
        return float(eval(e))
    except Exception:
        return None


for key, (a, b, m) in SC.items():
    f = os.path.join(HERE, f"{key}.html")
    if not os.path.exists(f) or not os.path.exists(os.path.join(HERE, "out", f"{key}.{'mov' if m == 'K' else 'mp4'}")):
        continue
    js = open(f).read().split("const tl = K.tl;")[1]
    d = b - a
    env = {"DUR": d}
    for line in js.splitlines():
        for nm, ex in re.findall(r"(?:const|,)\s*(\w+)\s*=\s*([0-9.\-+ ]+?)(?=[,;])", line):
            v = num(ex, env)
            if v is not None:
                env[nm] = v
    C.append((a - 0.04, "m:whoosh-short") if m == "B" else (a + 0.02, "swish"))
    if m == "K":
        C.append((b - 0.3, "m:whoosh-short"))
    last = -9
    for call, arg in re.findall(r"K\.(\w+)\(\s*\"[^\"]*\"\s*,\s*([^,)]+)", js):
        if call not in KIND:
            continue
        if call == "count":          # K.count(sel, from, to, t, dur…) → time is the 4th argument
            continue
        t = num(arg, env)
        if t is None or t < 0.25 or t > d - 0.2:
            continue
        s = KIND[call]
        if s == "pop" and t - last < 0.4:
            continue
        if s == "pop":
            last = t
        C.append((a + t, s))
    for args in re.findall(r"K\.count\(\s*\"[^\"]*\"\s*,\s*[^,]+,\s*[^,]+,\s*([^,]+),\s*([^,]+),", js):
        t, du = num(args[0], env), num(args[1], env)
        if t is None or du is None or du < 0.25 or t < 0 or t > d:
            continue
        x = t
        while x < min(t + du, d - 0.1):
            C.append((a + x, "tick")); x += 0.12
        C.append((a + t + du, "m:ping"))

C.sort()
sheet = [{"t": round(t, 3), "sfx": (os.path.join(MU, s[2:] + ".mp3") if s.startswith("m:") else s), "db": DB[s]} for t, s in C]
json.dump(sheet, open(os.path.join(HERE, "sfx_cues.json"), "w"), indent=0)
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                            os.path.join(HERE, "..", "CUT.mp4")], capture_output=True, text=True).stdout)
subprocess.run(["/Library/Frameworks/Python.framework/Versions/3.13/bin/python3",
                os.path.expanduser("~/.claude/skills/konrad-studio/scripts/sfx.py"), os.path.join(HERE, "sfx_cues.json"),
                os.path.join(HERE, "..", "SFX.wav"), "--dur", str(dur)], check=True)
print(len(sheet), "cues")
