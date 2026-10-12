#!/usr/bin/env python3
"""All timer pills (mini Dynamic Island) as SEPARATE short alpha clips — one file per pill, named with its in-point.
Each MOV carries the matching slice of Konrad's final-edit audio (for waveform sync); ticks go to a sibling WAV.
Pills 1–7 = the original set (2:44–11:58); 8–13 = the rest of the challenge up to the last minute.
Usage: pills_all.py [indices...]   (no args = all)."""
import sys, json, random, subprocess, wave
import numpy as np
from fontTools.ttLib import TTFont
from scenes_vo import new
from ds import *

FINAL = os.path.join(ROOT, "..", "0923 (2)-copy.mp4")
OUT = os.path.join(ROOT, "Czesc-3", "Pigulki")
TOTAL = 3 * 3600
# film seconds → challenge seconds elapsed (piecewise linear), consistent with everything Konrad says on camera
KNOTS = [(82.50, 0), (164.64, 90), (227.12, 240), (231.82, 360), (348.66, 660), (434.52, 900), (457.84, 960),
         (540.18, 1140), (571.94, 1260), (578.76, 1320), (652.46, 1440), (655.62, 2220), (670.28, 2340),
         (686.28, 2460), (698.24, 2520), (719.84, 2542),
         (904.46, 3420),                       # "jestem na minucie 57"
         (1181.38, 4440),                      # "której? 74"
         (1225.00, 4500), (1226.26, 8400),     # lunch → "zostało mi ostatnie 40 minut"
         (1357.76, 9600),                      # "ostatnie 20 minut"
         (1564.16, 9900),                      # "ostatnie 15 minut"
         (1676.28, 10440),                     # "ostatnie sześć minut"
         (1694.54, 10740),                     # "maksymalnie minuta"
         (1704.92, 10800)]                     # timer rings
DONE_AT = [457.84, 698.74, 1301.0]             # Pomysł, Produkt, Sklep completed


def elapsed(t):
    for (a0, e0), (a1, e1) in zip(KNOTS, KNOTS[1:]):
        if a0 <= t <= a1:
            return e0 + (e1 - e0) * (t - a0) / (a1 - a0)
    return KNOTS[-1][1] if t > KNOTS[-1][0] else 0


def hms(sec):
    sec = max(0, int(round(sec)))
    return f"{sec // 3600}:{sec % 3600 // 60:02d}:{sec % 60:02d}"


rem = lambda t: TOTAL - elapsed(t)
mono = TTFont(os.path.join(ROOT, "Source/fonts/GeistMono-Medium.ttf"))
madv = lambda t, size: sum(mono["hmtx"][mono.getBestCmap()[ord(c)]][0] for c in t) * size / mono["head"].unitsPerEm
FS = 30
DIG_W = madv("0:00:00", FS)
PW0, PH0 = 126, 38
PW1, PH1 = 36 + DIG_W + 26 + 4 * 16 + 3 * 10 + 30, 58
TOP = 18
X0 = 960 - PW1 / 2
WHITE, ORANGE, RED = A_BG, A_ORANGE, A_RED

# (film time, hold s, mode, extra, digit colour)
PILLS = [
    (164.64, 2.9, "show", None, WHITE),
    (227.12, 2.6, "show", None, WHITE),
    (348.66, 2.6, "show", None, WHITE),
    (540.18, 2.6, "show", None, WHITE),
    (578.76, 3.0, "hidden", None, WHITE),
    (656.04, 2.5, "roll", (652.46, 655.62), WHITE),
    (718.40, 3.2, "hidden", None, WHITE),                 # cliffhanger at the end of the product stage
    (904.46, 3.0, "show", None, WHITE),                   # 2:03:00
    (1180.02, 4.2, "reveal", 1181.38, WHITE),             # "której?" hidden → "74" 1:46:00
    (1225.00, 3.6, "skip", 1226.26, ORANGE),              # 1:45:00 → 0:40:00, turns orange
    (1357.76, 2.8, "show", None, ORANGE),                 # 0:20:00
    (1564.16, 2.8, "show", None, RED),                    # 0:15:00
    (1676.28, 17.9, "countdown", None, RED),              # 0:06:00 racing down to ~0:01:00 at "maksymalnie minuta"
]


def stamp(t):
    m, s_ = divmod(t, 60)
    return f"{int(m)}-{int(s_):02d}-{int(round((s_ % 1) * 1000)):03d}"


def build(idx):
    t_film, hold, mode, extra, dcol = PILLS[idx]
    a0 = t_film - 0.30
    a1 = t_film + hold + 0.80
    sc = new(f"PILL_{idx + 1:02d}", a0, a1)
    t = sc.t(t_film)
    IN0, IN1 = t + 60, t + 560
    OUT0 = t + int(hold * 1000)
    OUT1 = OUT0 + 420
    HUD = sc.group(100, "Timer pill", None, 0, 0)
    isl = sc.rect(101, "Island", HUD, 960 - PW0 / 2, TOP, PW0, PH0, [0.02, 0.02, 0.02, 1], r=PH0 / 2, op=0)
    sc.shadow(isl, 0.22, 24, 6)
    sc.k(isl, "rectSize", [(0, v2(PW0, PH0), LIN), (IN0, v2(PW0, PH0), HOLD), (IN1, v2(PW1, PH1), APPLE),
                           (OUT0, v2(PW1, PH1), HOLD), (OUT1, v2(PW0, PH0), APPLE)])
    sc.k(isl, "positionX", [(0, f(960 - PW0 / 2), LIN), (IN0, f(960 - PW0 / 2), HOLD), (IN1, f(960 - PW1 / 2), APPLE),
                            (OUT0, f(960 - PW1 / 2), HOLD), (OUT1, f(960 - PW0 / 2), APPLE)])
    sc.k(isl, "rectRoundness", [(0, f(PH0 / 2), LIN), (IN0, f(PH0 / 2), HOLD), (IN1, f(PH1 / 2), APPLE),
                                (OUT0, f(PH1 / 2), HOLD), (OUT1, f(PH0 / 2), APPLE)])
    sc.k(isl, "opacity", [(0, f(0), LIN), (IN0 - 200, f(0), HOLD), (IN0, f(100), SOFT), (OUT1, f(100), HOLD), (OUT1 + 220, f(0), SOFT)])
    CT = sc.group(110, "Content", HUD, 0, 0, op=0)
    sc.k(CT, "opacity", [(0, f(0), LIN), (IN0 + 250, f(0), HOLD), (IN0 + 450, f(100), SOFT), (OUT0 - 60, f(100), HOLD), (OUT0 + 120, f(0), SOFT)])
    ticks = []
    land = IN0 + 450
    rng = random.Random(11 + idx)
    scramble = lambda: f"{rng.randint(0, 2)}:{rng.randint(0, 59):02d}:{rng.randint(0, 59):02d}"

    def tick_run(keys, base, start, end):
        k, tt = 1, start + 1000
        while tt < end - 100:
            keys.append((tt, s(hms(base - k)), HOLD)); ticks.append((tt, 0.75)); k += 1; tt += 1000

    def blurred(lid, end):
        bl = sc.text(lid, "Digits hidden", CT, X0 + 36, TOP + 40, scramble(), FS, dcol, style="Medium", family="Geist Mono")
        keys, tt, n = [(0, s(scramble()), LIN)], IN0 + 300, 0
        while tt < end:
            keys.append((tt, s(scramble()), HOLD)); tt += 70 if n < 20 else 110; n += 1
        sc.k(bl, "textContent", keys)
        sc.A.append({"type": "addFxLayerEffect", "compositionId": "main", "layerId": bl, "effectId": 7990,
                     "effect": {"type": "gaussianBlur", "blurriness": 30}})
        return bl

    if mode == "hidden":
        blurred(120, OUT0)
    elif mode == "reveal":
        t_rev = sc.t(extra)
        bl = blurred(120, t_rev + 200)
        sc.k(bl, "opacity", [(0, f(100), LIN), (t_rev - 1, f(100), HOLD), (t_rev + 200, f(0), SOFT)])
        dg = sc.text(121, "Digits", CT, X0 + 36, TOP + 40, hms(rem(extra)), FS, dcol, style="Medium", family="Geist Mono", op=0)
        sc.k(dg, "opacity", [(0, f(0), LIN), (t_rev - 1, f(0), HOLD), (t_rev + 200, f(100), SOFT)])
        keys = [(0, s(hms(rem(extra))), LIN)]
        ticks.append((t_rev, 1.0))
        tick_run(keys, rem(extra), t_rev, OUT0)
        sc.k(dg, "textContent", keys)
    else:
        dg = sc.text(121, "Digits", CT, X0 + 36, TOP + 40, hms(rem(t_film)), FS, dcol, style="Medium", family="Geist Mono")
        if mode == "show":
            keys = [(0, s(hms(rem(t_film))), LIN)]
            ticks.append((land, 1.0))
            tick_run(keys, rem(t_film), land, OUT0)
        elif mode == "roll":
            r0, r1 = rem(extra[0]), rem(extra[1])
            keys = [(0, s(hms(r0)), LIN)] + Scene.roll_keys(IN0 + 300, IN0 + 750, hms, r0, r1, ease_pow=2.2)[1:]
            ticks.append((IN0 + 750, 1.0))
            tick_run(keys, r1, IN0 + 750, OUT0)
        elif mode == "skip":
            t_sk = sc.t(extra)
            r0, r1 = rem(t_film), rem(extra)
            keys = [(0, s(hms(r0)), LIN)]
            ticks.append((land, 1.0))
            kk, tt = 1, land + 1000
            while tt < t_sk - 150:
                keys.append((tt, s(hms(r0 - kk)), HOLD)); ticks.append((tt, 0.75)); kk += 1; tt += 1000
            keys += Scene.roll_keys(t_sk, t_sk + 900, hms, r0 - kk + 1, r1, ease_pow=2.6)
            for q in range(0, 900, 60):
                ticks.append((t_sk + q, 0.35))
            ticks.append((t_sk + 900, 1.0))
            tick_run(keys, r1, t_sk + 900, OUT0)
            sc.k(dg, "fillColor", [(0, col(WHITE), LIN), (t_sk, col(WHITE), HOLD), (t_sk + 500, col(ORANGE), SOFT)])
        elif mode == "countdown":
            keys, tt, last = [(0, s(hms(rem(t_film))), LIN)], land, None
            while tt < OUT0:
                txt = hms(rem(t_film + (tt - t) / 1000))
                if txt != last:
                    keys.append((tt, s(txt), HOLD)); last = txt
                tt += 100
            for tt in range(land, OUT0, 250):
                ticks.append((tt, 0.55))
            sc.k(dg, "scaleX", [(0, f(100), LIN)])
        sc.k(dg, "textContent", keys)
    # progress dots: done = green, current = breathing white
    done = sum(t_film + 0.1 >= d for d in DONE_AT)
    DX = X0 + 36 + DIG_W + 26
    for i in range(4):
        c = A_GREEN if i < done else ([1, 1, 1, 0.9] if i == done else [1, 1, 1, 0.22])
        d = sc.rect(130 + i, f"Dot {i}", CT, DX + i * 26, TOP + PH1 / 2 - 8, 16, 16, c, r=8)
        if i == done:
            kk, tt, on = [(0, f(100), LIN)], IN0 + 500, False
            while tt < OUT0:
                kk.append((tt, f(100 if on else 35), INOUT)); tt += 500; on = not on
            sc.k(d, "opacity", kk)
    sc.ticks = ticks
    sc.stamp = stamp(a0)
    return sc


def tick_wav(path, ticks, dur_s):
    sr = 48000
    y = np.zeros(int(dur_s * sr) + sr // 5)
    rng = np.random.default_rng(3)
    for t_ms, amp in ticks:
        i = int(t_ms / 1000 * sr)
        n = int(0.06 * sr)
        tt = np.arange(n) / sr
        tone = np.sin(2 * np.pi * 1500 * tt) * 0.6 + np.sin(2 * np.pi * 1900 * tt) * 0.4
        env = np.exp(-tt * 70)
        click = rng.normal(0, 1, n) * np.exp(-tt * 400) * 0.5
        y[i:i + n] += (tone * env + click) * 0.13 * amp
    y = np.clip(y, -1, 1)
    st = (np.stack([y, y], 1) * 32767).astype(np.int16)
    with wave.open(path, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr); w.writeframes(st.tobytes())


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    idxs = [int(a) - 1 for a in sys.argv[1:]] or range(len(PILLS))
    run = lambda *a: subprocess.run([TSRCT, *a], check=True, env=ENV, capture_output=True, text=True)
    for i in idxs:
        sc = build(i)
        sc.build(f"PILL_{i + 1:02d}")
        base = os.path.join(OUT, f"PIGULKA-{i + 1:02d}_od-{sc.stamp}")
        proj = os.path.join(ROOT, f"{sc.name}.tsrct")
        tmp = base + "_noaudio.mov"
        run("export", "--project", proj, "--output", tmp, "--format", "prores", "--fx-solo", "main:100")
        dur = sc.dur / 1000
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", tmp, "-ss", f"{sc.in_s:.3f}", "-t", f"{dur:.3f}", "-i", FINAL,
                        "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "pcm_s16le", "-shortest", base + ".mov"], check=True)
        os.remove(tmp)
        tick_wav(base + "_tyk.wav", sc.ticks, dur)
        print("pill", i + 1, sc.stamp, f"{dur:.1f}s", flush=True)
