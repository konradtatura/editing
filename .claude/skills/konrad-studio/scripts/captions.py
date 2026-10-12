#!/usr/bin/env python3
"""Konrad's captions: align a corrected text to whisper word times, chunk 2–5 words, render with NO gaps.

1) build:  captions.py build WORDS.json FIXED.txt OUT_caps.json [--maxw 5] [--maxc 24]
   WORDS.json = transcribe.py output of the FINAL edited video; FIXED.txt = the same speech, corrected by you
   (ASR typos fixed against the script / takes; keep the spoken words, only fix spelling & mishearings).
   Prints every block with start + duration — read it, fix FIXED.txt or splits, rebuild.
2) render: captions.py render VIDEO caps.json OUT.mp4 [--style box|reel] [--color white|yellow] [--y 0.91] [--size N] [--alpha OUT.mov]
   box  = 16:9 VSL/longform look: Inter Bold −50 tracking, ~38 px @1080p, white on black 50 % rounded box, y≈0.91.
   reel = 9:16 look: Inter Bold −50, ~48 px @1080 w, soft light shadow, no box, fixed under the chin (y 0.62–0.71).
   Every block shows until the next starts (first from frame 0, last to the end). Audio is copied untouched.
"""
import difflib, json, math, os, re, subprocess, sys

SK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT_P = os.path.join(SK, "assets", "fonts", "Inter-Bold.otf")
WEAK = {"i", "w", "z", "na", "do", "od", "po", "a", "ani", "o", "że", "bo", "się", "ten", "tego", "jak", "przez",
        "nie", "czy", "aż", "co", "u", "ze", "we", "the", "and", "to"}
UNITS = ("zł", "%", "dni", "godzin", "godzinach", "godziny", "lat", "minut", "minuty", "sprzedaże", "sprzedażach", "pomysłów", "osób", "tys")
KEEP_CASE = {"AI"}          # add brand names via --keep "Cyfrowy,Autopilot"


def norm(t):
    return re.sub(r"[^\w]", "", t.lower().replace("%", "procent"))


def build(words_json, fixed_txt, out, maxw=5, maxc=24, keep=()):
    keep = KEEP_CASE | set(keep)
    ww = [(w["word"].strip(), w["start"], w["end"]) for s in json.load(open(words_json))["segments"] for w in s.get("words", [])]
    fx = open(fixed_txt).read().split()
    a, b = [norm(w[0]) for w in ww], [norm(t) for t in fx]
    times = [None] * len(fx)
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        if op == "equal":
            for k in range(i2 - i1):
                times[j1 + k] = (ww[i1 + k][1], ww[i1 + k][2])
        elif op == "replace":
            s0, e0 = ww[i1][1], ww[i2 - 1][2]
            L, acc = sum(len(x) for x in fx[j1:j2]), 0
            for j in range(j1, j2):
                t0 = s0 + (e0 - s0) * acc / L; acc += len(fx[j])
                times[j] = (t0, s0 + (e0 - s0) * acc / L)
    for j in range(len(fx)):
        if times[j] is None:
            p = next((times[k][1] for k in range(j - 1, -1, -1) if times[k]), 0.0)
            n = next((times[k][0] for k in range(j + 1, len(fx)) if times[k]), p)
            times[j] = (p, max(p, n))
    for j in range(1, len(fx)):
        if times[j][0] < times[j - 1][0]:
            times[j] = (times[j - 1][0], max(times[j][1], times[j - 1][0]))

    def disp(t):
        t = re.sub(r"[.,:;!?„”\"…]", "", t)
        return t if (t in keep or t.isupper() and len(t) > 1) else t.lower()

    def clen(ix):
        return len(" ".join(disp(fx[i]) for i in ix))

    def cost(ix, is_end, whole):
        nw, ch = len(ix), clen(ix)
        if nw > maxw or (ch > maxc + 4 and nw > 1):
            return 1e9
        c = (ch - 15) ** 2 / 12
        if nw == 1 and whole > 1:
            c += 45
        if not is_end:
            if disp(fx[ix[-1]]).lower() in WEAK:
                c += 25
            if re.search(r"[,:;]$", fx[ix[-1]]):
                c -= 18
        c += 10 * sum(1 for i in ix[:-1] if re.search(r"[,:;]$", fx[i]))
        if times[ix[-1]][1] - times[ix[0]][0] < 0.45:
            c += 15
        return c

    phrases, cur = [], []
    for j, t in enumerate(fx):
        cur.append(j)
        gap = times[j + 1][0] - times[j][1] if j + 1 < len(fx) else 9
        if re.search(r"[.!?]$", t) or gap > 0.45:
            phrases.append(cur); cur = []
    if cur:
        phrases.append(cur)
    chunks = []
    for ph in phrases:
        n = len(ph); best = [0.0] + [1e18] * n; prev = [0] * (n + 1)
        for e in range(1, n + 1):
            for s in range(max(0, e - maxw), e):
                c = best[s] + cost(ph[s:e], e == n, n)
                if e < n and disp(fx[ph[e - 1]]).isdigit() and disp(fx[ph[e]]).lower() in UNITS:
                    c += 80
                if c < best[e]:
                    best[e], prev[e] = c, s
        cuts, e = [], n
        while e > 0:
            cuts.append((prev[e], e)); e = prev[e]
        chunks += [ph[s:e] for s, e in reversed(cuts)]
    caps = [{"start": round(times[ix[0]][0], 3), "text": " ".join(disp(fx[i]) for i in ix)} for ix in chunks]
    caps[0]["start"] = 0.0
    json.dump(caps, open(out, "w"), ensure_ascii=False, indent=0)
    lens = [len(c["text"].split()) for c in caps]
    print(len(caps), "blocks; words/block:", {k: lens.count(k) for k in sorted(set(lens))})
    for i, c in enumerate(caps):
        nxt = caps[i + 1]["start"] if i + 1 < len(caps) else c["start"] + 1.5
        print(f"{c['start']:8.2f} {nxt - c['start']:5.2f}  {c['text']}")


def render(video, caps_json, out, style="box", color="white", y=None, size=None, alpha=None):
    from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont
    pr = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-count_packets", "-show_entries",
                         "stream=width,height,r_frame_rate,nb_read_packets", "-of", "json", video], capture_output=True, text=True)
    st = json.loads(pr.stdout)["streams"][0]
    W, H, nfr = st["width"], st["height"], int(st["nb_read_packets"])
    num, den = map(int, st["r_frame_rate"].split("/")); fps = num / den
    unit = min(W, H) / 1080
    size = size or round((38 if style == "box" else 48) * unit)
    y = y or (0.911 if style == "box" else 0.66)
    font = ImageFont.truetype(FONT_P, size)
    track = -0.05 * size
    fill = (255, 255, 0) if color == "yellow" else (255, 255, 255)

    def advs(s):
        out_ = []
        for i, ch in enumerate(s):
            a_ = font.getlength(ch)
            if i + 1 < len(s):
                a_ += font.getlength(ch + s[i + 1]) - font.getlength(ch) - font.getlength(s[i + 1]) + track
            out_.append(a_)
        return out_

    def draw(d, x, yy, s, f_):
        for ch, a_ in zip(s, advs(s)):
            d.text((x, yy), ch, font=font, fill=f_); x += a_

    hb, xb = font.getbbox("H"), font.getbbox("x")
    yc = y * H
    ytop = yc - ((hb[1] + hb[3]) / 2 * 0.4 + (xb[1] + xb[3]) / 2 * 0.6)

    def png(s, path):
        tw = sum(advs(s)[:-1]) + font.getbbox(s[-1])[2]
        x0 = round((W - tw) / 2)
        im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        if style == "box":
            bh, pad = round(54 * unit), round(13 * unit)
            ImageDraw.Draw(im).rounded_rectangle((x0 - pad, yc - bh / 2, x0 + tw + pad, yc + bh / 2), round(8 * unit), fill=(0, 0, 0, 128))
        else:
            sh = Image.new("L", (W, H), 0); draw(ImageDraw.Draw(sh), x0, ytop + 2, s, 150)
            sh = sh.filter(ImageFilter.GaussianBlur(4))
            ti = Image.new("L", (W, H), 0); draw(ImageDraw.Draw(ti), x0, ytop + 1, s, 90)
            im.putalpha(ImageChops.lighter(sh, ti.filter(ImageFilter.GaussianBlur(1.2))))
        txt = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        draw(ImageDraw.Draw(txt), x0, ytop, s, fill + (255,))
        Image.alpha_composite(im, txt).save(path, compress_level=1)

    caps = json.load(open(caps_json))
    out = os.path.abspath(out)
    work = os.path.splitext(out)[0] + "_png"
    os.makedirs(work, exist_ok=True)
    starts = [0] + [max(1, round(c["start"] * fps)) for c in caps[1:]]
    for i in range(1, len(starts)):
        starts[i] = max(starts[i], starts[i - 1] + 1)
    lines = []
    for i, c in enumerate(caps):
        p = os.path.join(work, f"c{i:04d}.png"); png(c["text"], p)
        end = starts[i + 1] if i + 1 < len(caps) else nfr
        lines.append(f"file '{p}'\nduration {(end - starts[i]) / fps:.6f}\n")
    lines.append(f"file '{os.path.join(work, f'c{len(caps) - 1:04d}.png')}'\n")
    lst = os.path.join(work, "list.txt"); open(lst, "w").write("".join(lines))
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", video, "-f", "concat", "-safe", "0", "-i", lst, "-filter_complex",
                    f"[1:v]fps={fps},format=rgba[c];[0:v][c]overlay=0:0:eof_action=repeat:format=auto[v]",
                    "-map", "[v]", "-map", "0:a?", "-c:v", "libx264", "-preset", "slow", "-crf", "14", "-pix_fmt", "yuv420p",
                    "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", "-c:a", "copy",
                    "-frames:v", str(nfr), "-movflags", "+faststart", out], check=True)
    if alpha:
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-i", video, "-map", "0:v",
                        "-map", "1:a?", "-vf", f"fps={fps},format=yuva444p10le", "-c:v", "prores_ks", "-profile:v", "4444",
                        "-c:a", "aac", "-b:a", "256k", "-frames:v", str(nfr), alpha], check=True)
    print("done", out, alpha or "")


if __name__ == "__main__":
    a = sys.argv[1:]
    opt = lambda k, d=None: a[a.index(k) + 1] if k in a else d
    if a[:1] == ["build"]:
        build(a[1], a[2], a[3], int(opt("--maxw", 5)), int(opt("--maxc", 24)),
              [x for x in (opt("--keep", "") or "").split(",") if x])
    elif a[:1] == ["render"]:
        render(a[1], a[2], a[3], opt("--style", "box"), opt("--color", "white"),
               float(opt("--y")) if opt("--y") else None, int(opt("--size")) if opt("--size") else None, opt("--alpha"))
    else:
        sys.exit(__doc__)
