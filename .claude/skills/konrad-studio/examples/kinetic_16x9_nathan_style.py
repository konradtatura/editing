#!/usr/bin/env python3
"""„16–26” (2026-10-05): the full film built on scripts/kinetic.py — the reference for using the engine.
Konrad's verdict: „dojebane… kiedyś zapłaciłem za taki film 1000 zł”. Paths pointed to ~/Downloads/reelsygotowe/REF_nathan (media of the finished project may be gone; breakdown + photos kept in ~/Documents/KonradStudio_Archiwum/referencje/REF_nathan) — reference code, not runnable as is.
usage: kinetic_16x9_nathan_style.py [OUT.mp4] [--frames 1.0,5.2,...]   (frames → preview sheet)"""
import json, os, sys
import numpy as np
sys.path.insert(0, os.path.expanduser("~/.claude/skills/konrad-studio/scripts"))
import kinetic as K

REF = os.path.expanduser("~/Downloads/reelsygotowe/REF_nathan")
DL = os.path.expanduser("~/Downloads")
AROLL = os.path.join(REF, "..", "16-26.mp4")
D = 53.2
W, H = K.W, K.H
B = lambda n: os.path.join(REF, "brols", n)
WK1, WK2 = os.path.join(REF, "workd", "IMG_2926.MOV"), os.path.join(REF, "workd", "IMG_2937.MOV")
DUBAI, MIAMI = os.path.join(DL, "14629596_3840_2160_60fps.mp4"), os.path.join(DL, "6345016-hd_1920_1080_30fps.mp4")
PHOTOS = [os.path.join(REF, "photos", f) for f in ["IMG_9279.jpg", "IMG_4623.jpg", "IMG_4802.jpg", "IMG_4897.jpg",
          "IMG_6837.jpg", "IMG_6817_2.jpg", "9b1a7df8-a3bf-4c08-9a11-39dc1e3c9762.jpg"]]
FEED_TILES = [(B(f), t) for f, t in [("IMG_6553.MOV", 2), ("IMG_5845.MOV", 2), ("IMG_3475.MOV", 2),
    ("64CC6E8A-058C-45B6-A627-9B7A2BBB0B0F 3.MOV", 3), ("IMG_2129.MOV", 4), ("IMG_1928.MOV", 1), ("IMG_5587.MOV", 2),
    ("IMG_3590.MOV", 6), ("IMG_6554.MOV", 4), ("B7AE116A-05F1-4088-A9A4-4A5828722B12.MOV", 3), ("IMG_9863.MOV", 2),
    ("IMG_2793.MOV", 2), ("IMG_3439.MOV", 5), ("IMG_0434.MOV", 5), ("IMG_2008 2.MOV", 2), ("IMG_3992.mov", 2),
    ("IMG_7073.MOV", 3), ("IMG_1895.MOV", 2), ("d2ea8e92-22b9-45d8-bb76-82aa3529d253.MP4", 4), ("IMG_2552.MOV", 10),
    ("IMG_1025.MOV", 3), ("IMG_2500.MOV", 2)]]
DISPLAY = {3: "16", 5: "26", 6: "", 34: "Dubaj", 58: "14", 68: "130 000+", 69: "", 70: "", 77: "billboard",
           78: "Times", 79: "Square.", 83: "USA", 103: "sztuczną", 104: "inteligencją.", 121: "chcę.", 126: "10 000 zł",
           127: "", 128: "", 147: "130 000", 148: "", 149: "", 156: "0 zł.", 157: "", 172: "10 000 zł", 173: "", 174: "",
           184: "obserwuj", 188: "„KURS”", 192: "wyślę", 193: "ci", 48: "możliwe?", 12: "DLA", 13: "CIEBIE",
           183: "dostęp,", 109: "myślisz."}
K.setup(json.load(open(os.path.join(REF, "arol", "words.json"))), DISPLAY, {"Dubaju", "Miami.", "USA", "AI"})
ws = K.ws


def build():
    S = []   # (t0, t1, kind, params)
    def shot(t0, t1, kind, **k):
        S.append((t0, t1, kind, k))
    F = lambda t0, t1, z=False: shot(t0, t1, "face", zoom=z)
    shot(0.00, 2.22, "face", zoom=False, open=True)
    shot(2.22, 2.80, "light")
    shot(2.80, 3.24, "blue")
    feed = K.FeedWall(int((5.36 - 3.24) * K.FPS) + 2, FEED_TILES)
    shot(3.24, 5.36, "custom", fn=lambda t, i: feed.frame(i))
    shot(5.36, 7.12, "clip", src=B("IMG_6553.MOV"), ss=3.0, band=0.36, grade="bw", zoom=0.05)
    shot(7.12, 7.50, "clip", src=B("IMG_5845.MOV"), ss=1.0, band=0.45, grade="bw", zoom=0.04)
    shot(7.50, 7.86, "clip", src=B("IMG_3475.MOV"), ss=2.2, band=0.42, grade="bw", zoom=0.04)
    shot(7.86, 8.24, "clip", src=B("64CC6E8A-058C-45B6-A627-9B7A2BBB0B0F 3.MOV"), ss=3.2, band=0.5, grade="bw", zoom=0.04)
    shot(8.24, 8.80, "clip", src=DUBAI, ss=3.0, grade="night", zoom=0.05, giant=("Dubaj", 8.28))
    shot(8.80, 9.26, "clip", src=MIAMI, ss=1.0, grade="cine", zoom=0.05, giant=("Miami", 8.86))
    shot(9.26, 10.50, "clip", src=WK2, ss=480.0, grade="cine", zoom=0.04)
    shot(10.50, 11.74, "light")
    shot(11.74, 13.46, "clip", src=B("3c3d135a8662468fa96787374dcca667.MOV"), ss=1.2, band=0.52, grade="cine", zoom=0.05)
    collage = K.Collage(PHOTOS, 13.46, 15.78)
    shot(13.46, 15.78, "custom", fn=lambda t, i: collage.frame(t))
    F(15.78, 18.14, True)
    shot(18.14, 19.70, "clip", src=B("IMG_2550 2.MOV"), ss=6.6, band=0.06, grade="cine", zoom=0.04)
    shot(19.70, 20.62, "clip", src=B("IMG_2550 2.MOV"), ss=8.16, band=0.62, grade="cine", zoom=0.04)
    shot(20.62, 21.86, "clip", src=B("IMG_1025.MOV"), ss=1.0, band=0.02, grade="cine", zoom=0.05, giant=("USA", 21.42))
    cells = K.grid_cells([(B("IMG_9863.MOV"), 1.0, 0.45), (B("IMG_2008 2.MOV"), 0.6, 0.5),
                          (B("C1738 2.MOV"), 2.0, 0.5), (B("IMG_1025.MOV"), 3.0, 0.42)], int(round((23.98 - 21.86) * K.FPS)))
    shot(21.86, 23.98, "custom", fn=lambda t, i: K.grid_frame(cells, t, 21.86, i))
    shot(23.98, 25.50, "clip", src=WK1, ss=20.0, grade="night", zoom=0.04)
    shot(25.50, 27.56, "clip", src=WK1, ss=62.0, grade="night", crop=(1.45, 0.52, 0.48), zoom=0.04)
    shot(27.56, 28.56, "black")
    guru = K.GuruWall()
    shot(28.56, 30.46, "custom", fn=lambda t, i: guru.frame(t, int((t - 28.56) / 0.3)))
    F(30.46, 33.80, False)
    shot(33.80, 34.42, "clip", src=WK2, ss=626.0, grade="cine", zoom=0.03)
    shot(34.42, 36.10, "clip", src=WK1, ss=6.0, grade="night", zoom=0.05)
    shot(36.10, 36.62, "light")
    sys_t = ws(140) - 0.04
    shot(36.62, 37.80, "lapse", src=WK2, a=30, b=590,
         post=lambda fr, t: K.desk_text(fr.astype(np.float32), "system,", min(1, (t - sys_t) / 0.1)) if t >= sys_t else fr)
    F(37.80, 40.98, True)
    shot(40.98, 42.34, "clip", src=B("IMG_3590.MOV"), ss=8.0, band=0.42, grade="cine", zoom=0.05)
    shot(42.34, 43.34, "light")
    shot(43.34, 43.96, "blue")
    shot(43.96, 45.06, "light")
    F(45.06, 47.42, False)
    shot(47.42, 48.36, "clip", src=B("IMG_1928.MOV"), ss=0.3, band=0.5, grade="cine", zoom=0.05)
    shot(48.36, 50.20, "clip", src=WK1, ss=147.2, grade="night", zoom=0.04)
    F(50.20, D, True)

    VC = (1450, 470)        # caption block on the face (right of the head, on the headboard)
    P = [
        K.Phrase(0.0, 2.22, pre=[0, 1, 2], hero=[(3, "big"), (4, "small"), (5, "big")], post=[7], at=(1240, 470), maxw=640, hs=190),
        K.Phrase(2.22, 2.80, pre=[8, 9, 10, 11], style="light", at=(W / 2, 540), ss=74, align="center"),
        K.Phrase(2.80, 3.24, hero=[(12, "big"), (13, "big")], style="blue", at=(W / 2, 540), hs=110, align="center", maxw=1200),
        K.Phrase(3.24, 4.54, pre=[14, 15, 16, 17], hero=[(18, "big")], at=(W / 2 - 330, 520), hs=170, chrome=True),
        K.Phrase(4.54, 5.36, pre=[19, 20], hero=[(21, "big")], at=(W / 2 - 300, 540), hs=150, chrome=True),
        K.Phrase(5.36, 7.12, pre=[22, 23, 24, 25], hero=[(26, "big")], post=[27, 28], at=(140, 780), hs=150),
        K.Phrase(7.12, 8.24, pre=[29, 30, 31], hero=[(32, "big")], at=(W / 2 - 360, 540), hs=150),
        K.Phrase(9.26, 10.50, pre=[38, 39, 40, 41, 42], at=(170, 560), ss=48),
        K.Phrase(10.50, 11.74, pre=[43, 44, 45, 46, 47], hero=[(48, "big")], style="light", at=(W / 2 - 330, 560), hs=150, ss=46),
        K.Phrase(11.74, 13.46, pre=[49, 50, 51, 52, 53, 54], hero=[(55, "big")], at=(140, 640), hs=150),
        K.Phrase(13.46, 15.78, pre=[56, 57], hero=[(58, "big"), (59, "small", "lat")], post=[60, 61, 62, 63, 64, 65], style="light",
               at=(190, 520), hs=210, ss=46),
        K.Phrase(15.78, 18.14, pre=[66, 67], hero=[(68, "big")], post=[71, 72], at=(1180, 470), hs=170, maxw=700,
               flap=(ws(68), ws(70) + 0.25)),
        K.Phrase(18.14, 20.62, pre=[73, 74, 75, 76, 77], hero=[(78, "big"), (79, "big")], at=(W / 2 - 420, 600), hs=150, maxw=900),
        K.Phrase(20.62, 21.86, pre=[80, 81, 82], at=(W / 2, 860), ss=48, align="center"),
        K.Phrase(21.86, 23.06, pre=[84, 85, 86, 87, 88], hero=[(89, "big")], at=(W / 2 - 300, 540), hs=150),
        K.Phrase(23.06, 23.98, pre=[90, 91], hero=[(92, "big")], at=(W / 2 - 420, 540), hs=150, maxw=900),
        K.Phrase(23.98, 25.54, pre=[93, 94, 95], hero=[(96, "big"), (97, "big")], at=(980, 330), hs=120, maxw=860),
        K.Phrase(25.54, 27.56, pre=[98, 99, 100, 101, 102], hero=[(103, "big"), (104, "big")], at=(220, 820), hs=120, maxw=1450),
        K.Phrase(27.56, 28.56, pre=[105, 106, 107, 108], hero=[(109, "big")], style="black", at=(W / 2 - 230, 540), hs=150),
        K.Phrase(28.56, 29.24, pre=[110, 111], at=(W / 2, 930), ss=50, align="center", quote=True),
        K.Phrase(29.24, 30.46, pre=[112, 113, 114, 115, 116], at=(W / 2, 930), ss=50, align="center", quote=True),
        K.Phrase(30.46, 31.80, pre=[117, 118], hero=[(119, "big")], post=[120, 121], at=VC, hs=190),
        K.Phrase(31.80, 33.80, pre=[122, 123, 124, 125], hero=[(126, "big")], at=(1230, 470), hs=170, maxw=640),
        K.Phrase(33.80, 34.42, pre=[129, 130], hero=[(131, "big")], at=(1040, 520), hs=130),
        K.Phrase(34.42, 36.10, pre=[132, 133], hero=[(134, "big")], post=[135, 136], at=(240, 480), hs=150),
        K.Phrase(36.10, 36.62, hero=[(137, "big"), (138, "big")], style="light", at=(W / 2, 540), hs=120, align="center", maxw=1100),
        K.Phrase(36.62, 37.80, pre=[139], hero=[(141, "big")], at=(1330, 560), hs=130, maxw=540),
        K.Phrase(37.80, 40.98, pre=[142, 143, 144, 145, 146], hero=[(147, "big")], post=[150, 151], at=(1200, 470), hs=170, maxw=660),
        K.Phrase(40.98, 42.34, pre=[152, 153, 154, 155], hero=[(156, "big")], at=(W / 2 - 220, 300), hs=190),
        K.Phrase(42.34, 43.34, pre=[158, 159, 160], style="light", at=(W / 2, 540), ss=80, align="center"),
        K.Phrase(43.34, 43.96, pre=[161, 162], style="blue", at=(W / 2, 540), ss=84, align="center"),
        K.Phrase(43.96, 45.06, pre=[163, 164, 165], style="light", at=(W / 2, 540), ss=80, align="center"),
        K.Phrase(45.06, 47.42, pre=[166, 167, 168, 169, 170, 171], hero=[(172, "big")], at=(1200, 470), hs=170, maxw=660,
               strike=46.86),
        K.Phrase(47.42, 48.36, pre=[175, 176], hero=[(177, "big"), (178, "big")], at=(W / 2 - 330, 300), hs=150, maxw=800),
        K.Phrase(48.36, 49.50, pre=[179, 180, 181, 182], hero=[(183, "big")], at=(240, 760), hs=150),
        K.Phrase(49.50, 50.20, hero=[(184, "big")], post=[185], at=(240, 760), hs=150),
        K.Phrase(50.20, 51.46, pre=[186, 187], hero=[(188, "big")], post=[189, 190], at=(1230, 470), hs=170, maxw=640,
               redact=(50.60, 50.74)),
        K.Phrase(51.46, D, pre=[191, 192, 193, 194, 195, 196], hero=[(197, "big")], at=(1180, 470), hs=150, maxw=700),
    ]
    return S, P




if __name__ == "__main__":
    a = sys.argv[1:]
    fr = [float(x) for x in a[a.index("--frames") + 1].split(",")] if "--frames" in a else None
    out = next((x for x in a if x.endswith((".mp4", ".jpg", ".png"))), os.path.join(REF, "16-26_EDIT_video.mp4"))
    S, P = build()
    print(K.run(S, P, out, aroll=AROLL, dur=D, frames=fr))
