"""VSL cut: pick best takes (by ASR word times), snap edges to the audio envelope,
tighten pauses inside kept takes to ~140 ms, write edl.json (render ranges)."""
import json, wave
import numpy as np

SRC = {
    "L": "/Users/konradtatura/Downloads/Teleprompter-2026-30-09_17-25-34.MP4",
    "S": "/Users/konradtatura/Downloads/Teleprompter-2026-30-09_17-33-03.MP4",
}
WAV = {"L": "long16k.wav", "S": "short16k.wav"}
TX = {"L": "transcripts/Teleprompter-2026-30-09_17-25-34.json",
      "S": "transcripts/Teleprompter-2026-30-09_17-33-03.json"}

# (source, first word start, last word end, note)  — times from ASR (words_long.txt / short dump)
TAKES = [
    ("L", 32.86, 42.56, "Daj mi trzy minuty … żeby go sprzedawać."),
    ("L", 45.66, 50.16, "I to nawet jeśli nie umiesz … z AI."),
    ("L", 55.34, 61.52, "A w dodatku … sto procent kwoty."),
    ("L", 64.60, 68.26, "Bo widzisz, większość ludzi … Google'a."),
    ("L", 69.30, 75.46, "Napisz maila. Zrób obrazek … co mogą sprzedać."),
    ("L", 80.16, 83.56, "A to kompletnie mija się … stworzyło."),
    ("L", 85.46, 93.22, "Bo jeszcze kilka lat temu … marketing"),
    ("L", 103.50, 107.38, "I albo uczyłeś się tego miesiącami … za ciebie."),
    ("L", 117.80, 120.32, "A dzisiaj to AI kompletnie zmieniło tą matematykę"),
    ("L", 133.74, 140.50, "I wiem to … 941 e-booków,"),
    ("L", 150.02, 154.60, "Sam w sobie model się nie zmienił … problem."),
    ("L", 156.62, 160.74, "ale zmieniło się to … realnie ci zarabia."),
    ("L", 161.68, 166.34, "I właśnie dlatego stworzyliśmy Cyfrowy Autopilot … o AI."),
    ("L", 187.90, 191.04, "Tu masz jeden cel … sprzedawać."),
    ("L", 195.11, 202.48, "najpierw wybierasz rynek. System daje … jak to sprzedawać."),
    ("L", 203.64, 208.20, "Potem dostajesz gotowy prompt … marketing."),
    ("L", 209.74, 216.90, "Czyli zamiast pytać … do startu."),
    ("L", 220.12, 224.66, "I teraz zobacz, dlaczego … raz."),
    ("L", 225.86, 230.64, "Nie musisz kupować … od nowa."),
    ("L", 232.50, 238.52, "A teraz połóżmy to razem … 177 zł dziennie."),
    ("L", 245.34, 251.80, "W skali 30 dni … nie tysiącu,"),
    ("L", 257.54, 264.22, "I to właśnie pokazuje piękno … interesująco."),
    ("L", 270.44, 276.18, "I dlatego ja sam wszedłem … nie miałem."),
    ("L", 286.34, 290.60, "AI może wykonać … ręcznie. I teraz posłuchaj."),
    ("L", 297.88, 302.96, "Ale nawet najlepszy system … na później."),
    ("L", 304.16, 310.60, "I właśnie dlatego nie zostawiamy … z coachami"),
    ("L", 312.10, 314.92, "i zamkniętą społeczność … proces."),
    ("L", 316.36, 319.34, "Masz jakiś problem? … ruszasz dalej."),
    ("L", 345.56, 351.80, "A kiedy produkt jest gotowy … pierwsze kampanie."),
    ("L", 354.48, 357.14, "Bo nie chcemy doprowadzić cię tylko do: Fajnie, mam e-booka."),
    # --- re-recorded ending (short file) replaces the rest of the long take
    ("S", 16.00, 20.22, "Chcemy doprowadzić cię do: mam produkt … mogę zacząć to sprzedawać."),
    ("S", 21.52, 24.96, "I jesteśmy tego tak pewni … launch w 48 godzin."),
    ("S", 26.96, 34.20, "Przejdź przez cały proces … sto procent kwoty."),
    ("S", 36.20, 43.70, "za 48 godzin możesz nadal mieć … zacząć sprzedawać."),
    ("S", 46.56, 54.84, "więc kliknij przycisk pod tym wideo … czegoś swojego."),
]

PRE, POST = 0.045, 0.065        # pad around real onset/offset
PAUSE_MAX, PAUSE_KEEP = 0.24, 0.14
PAUSE_DB = -50.0   # absolute speech floor for pause measurement (source PAUSE_MAX, PAUSE_KEEP = 0.24, 0.14 output share levels)


def env(key):
    w = wave.open(WAV[key])
    x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
    hop = 160
    n = len(x) // hop
    db = 20 * np.log10(np.sqrt((x[:n * hop].reshape(n, hop) ** 2).mean(1)) + 1e-9)
    return db, np.percentile(db, 15) + 10, np.percentile(db, 50) - 10


ENV = {k: env(k) for k in SRC}
WORDS = {k: [w for w in json.load(open(TX[k]))["words"] if w.get("type") == "word"] for k in SRC}


def neighbours(key, a, b):
    ws = WORDS[key]
    prev_end = max([w["end"] for w in ws if w["end"] <= a + 0.02] or [0])
    next_start = min([w["start"] for w in ws if w["start"] >= b - 0.02] or [1e9])
    return prev_end, next_start


def speech(key, t):
    db, thr = ENV[key]
    i = int(t * 100)
    return 0 <= i < len(db) and db[i] > thr


def loud(key, t, extra=0.0):
    db, thr, hi = ENV[key]
    i = int(t * 100)
    lvl = hi if extra else thr
    return 0 <= i < len(db) and db[i] > lvl


def onset(key, a, lo):
    """start of the loud (voiced) run at the first word; breaths sit below thr+8 and are excluded"""
    db, thr, hi = ENV[key]
    i0, i1 = int(max(lo, a - 0.15) * 100), int((a + 0.08) * 100)
    m = i0 + int(np.argmin(db[i0:i1]))
    voiced_before = sum(1 for k in range(int(a * 100), m) if db[k] > hi + 6)
    if db[m] < hi and voiced_before < 4:
        t = m / 100          # word boundary dip found: speech starts after it
        while t < a + 0.2 and not loud(key, t, 8):
            t += 0.01
        lo = max(lo, m / 100)
    else:
        t = a
    if not loud(key, t, 8):
        while t < a + 0.2 and not loud(key, t, 8):
            t += 0.01
    else:
        while t - 0.01 > lo and loud(key, t - 0.01, 8):
            t -= 0.01
    # include the soft consonant attack just before the voiced run (above base threshold, max 60 ms)
    k = 0
    while k < 6 and t - 0.01 > lo and loud(key, t - 0.01):
        t -= 0.01; k += 1
    return t


def offset(key, b, hi):
    """end of speech after the last word: walk forward while above base threshold (word tail), max +0.25 s"""
    t = b - 0.05
    while t < min(hi, b + 0.25) and loud(key, t):
        t += 0.01
    return t


ranges = []
log = []
for key, a, b, note in TAKES:
    prev_end, next_start = neighbours(key, a, b)
    s = onset(key, a, prev_end + 0.03) - PRE
    e = offset(key, b, next_start - 0.03) + POST
    s = max(s, prev_end + 0.01)
    e = min(e, next_start - 0.01)
    # tighten every quiet run (edges included), measured like pause_audit (p15 + 10 dB, 10 ms frames)
    db, thr, _ = ENV[key]
    i0, i1 = int(round(s * 100)), int(round(e * 100))
    inword = np.zeros(i1 - i0, bool)
    for w_ in WORDS[key]:
        a_, b_ = int(w_["start"] * 100) - i0, int(w_["end"] * 100) - i0
        if b_ >= 0 and a_ < i1 - i0:
            inword[max(0, a_):max(0, min(i1 - i0, b_))] = True
    # quiet = true silence anywhere, or breath-level audio (< -40 dB) between words
    sp = [not (db[i] < PAUSE_DB or (db[i] < -40 and not inword[i - i0])) for i in range(i0, i1)]
    # smooth 1-frame blips
    seg = db[i0:i1]
    first = next((k for k in range(len(seg)) if seg[k] > -40), 0)
    while first > 0 and seg[first - 1] > PAUSE_DB:
        first -= 1
    last = next((k for k in range(len(seg) - 1, -1, -1) if seg[k] > -40), len(seg) - 1)
    while last < len(seg) - 1 and seg[last + 1] > PAUSE_DB:
        last += 1
    keep_from = max(0, first - 5) / 100 + s           # <= 50 ms lead-in
    keep_to = min(len(sp), last + 1 + 7) / 100 + s    # <= 70 ms tail
    parts, cur = [], keep_from
    k = first
    while k <= last:
        if not sp[k]:
            j = k
            while j <= last and not sp[j]:
                j += 1
            gap = (j - k) / 100
            if gap > 0.20:
                ca = s + k / 100 + 0.07
                cb = s + j / 100 - 0.07
                parts.append((cur, ca)); cur = cb
                log.append(f"  pause {gap*1000:.0f}ms @ {key}{s + k/100:.2f} -> 140ms")
            k = j
        else:
            k += 1
    parts.append((cur, keep_to))
    for p in parts:
        ranges.append({"source": key, "start": round(p[0], 3), "end": round(p[1], 3), "beat": note})
    log.append(f"{key} {keep_from:7.2f}-{keep_to:7.2f}  {note}")

total = sum(r["end"] - r["start"] for r in ranges)
json.dump({"sources": SRC, "ranges": ranges}, open("edl.json", "w"), ensure_ascii=False, indent=1)
print("\n".join(log))
print(f"segments {len(ranges)}  runtime {total:.1f}s")
