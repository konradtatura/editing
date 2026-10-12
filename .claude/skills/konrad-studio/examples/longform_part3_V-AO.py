#!/usr/bin/env python3
"""Part 3 scenes V–AO (11:59–18:16) on the full edit halfraw.mp4 (same timeline as aw.mp4).
Each its own Apple metaphor:
V Finder desktop → MacBook · W black punch "Nie jesteś." · X stranger's journey (overlay) · Y 2:00 AM lock screen ·
Z frosted glass → Safari · AA landing-page anatomy (overlay) · AB two phones, particles → cart · AC Live Text scan (overlay) ·
AD browser vs download tiles (overlay) · AE Calendar: the customer's day · AF promise ↔ chapter links (overlay) ·
AG ⌘C ⌘V keycaps (a + b) · AH Screen Time · AI isometric store building (overlay) · AJ Up Next queue (overlay) ·
AK scale: 7 min vs · AL org chart → Ty + AI · AM iOS alert · AN receipt 10 000 → 0 zł · AO boarding pass (overlay).
Usage: scenes_vo.py V W ...   (no args = all).  Overlay scenes keep everything under root group 100 (alpha export)."""
import sys, math, random
from scenes_af import adv
from scenes_af2 import check, spinner, fade
from scenes_gk import pop
from scenes_lu import card_bg, rise_group
from ds import *

SRC = os.path.join(ROOT, "..", "halfraw.mp4")
WORDS = os.path.join(WORK, "transcript_half/from700.json")
OVERLAY = set()          # scene keys exported additionally as alpha MOV (fx-solo main:100)


def new(name, a, b):
    return Scene(name, a, b, words_json=WORDS, src=SRC, word_offset=700.0)


def overlay(sc):
    sc.layers.append(sc.footage())
    return sc.group(100, "FX", None, 0, 0)


def arc(cx, cy, r, a0, a1, n=36):
    return [(cx + r * math.cos(math.radians(a0 + (a1 - a0) * i / n)),
             cy + r * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]


def cmd_symbol(sc, base, parent, cx, cy, size, color, width):
    """Draw ⌘ (Geist has no glyph): 4 tangent lines + 4 three-quarter loops."""
    a, r = size * 0.17, size * 0.15
    ids = []
    for i, pts in enumerate([[(cx - a - r, cy - a), (cx + a + r, cy - a)], [(cx - a - r, cy + a), (cx + a + r, cy + a)],
                             [(cx - a, cy - a - r), (cx - a, cy + a + r)], [(cx + a, cy - a - r), (cx + a, cy + a + r)]]):
        ids.append(sc.path(base + i, "Cmd line", parent, pts, 0, 0, stroke=(color, width), closed=False))
    loops = [((cx - a - r, cy - a - r), 90, 360), ((cx + a + r, cy - a - r), 180, 450),
             ((cx + a + r, cy + a + r), 270, 540), ((cx - a - r, cy + a + r), 0, 270)]
    for i, ((lx, ly), a0, a1) in enumerate(loops):
        ids.append(sc.path(base + 4 + i, "Cmd loop", parent, arc(lx, ly, r, a0, a1), 0, 0, stroke=(color, width), closed=False))
    return ids


def blob(lid, x, y, d, c, blur=320, dur=None):
    return {"type": "Rect", "id": lid, "name": "Glow", "blendMode": "normal",
            "activeRange": {"start": 0, "duration": dur}, "transform": tf(x, y),
            "rect": {"size": [d, d], "fillColor": c, "roundness": d / 2},
            "effects": [{"id": 7000 + lid, "effect": {"type": "gaussianBlur", "blurriness": blur}}]}


def blur(sc, lid, eid, amount):
    sc.A.append({"type": "addFxLayerEffect", "compositionId": "main", "layerId": lid, "effectId": eid,
                 "effect": {"type": "gaussianBlur", "blurriness": amount}})


def scale_keys(sc, lid, keys):
    for p in ("scaleX", "scaleY"):
        sc.k(lid, p, keys)


def pill_text(sc, base, parent, cx, cy, text, size, fg, bg, pad=26, style="Medium", h=None):
    h = h or size + 26
    wd = adv(text, size, "SemiBold" if style == "SemiBold" else "Medium") + pad * 2
    sc.rect(base, "Pill", parent, cx - wd / 2, cy - h / 2, wd, h, bg, r=h / 2)
    sc.text(base + 1, "Pill text", parent, cx, cy + size * 0.36, text, size, fg, style=style, just="center")
    return wd


# ================================================================== V  Finder desktop: one PDF → MacBook
def scene_V():
    sc = new("V_PDF", 720.90, 724.35)
    sc.bg = A_BG
    w = sc.word
    AKT, PLIK, MAC = w(721.10), w(722.56), w(723.94)
    LAP = sc.group(100, "Laptop", None, 960, 540, 960, 540)
    # bezel + base sit just outside the frame until the zoom-out reveals them
    sc.rect(101, "Base", LAP, -240, 1098, 2400, 46, [0.80, 0.80, 0.82, 1], r=23)
    sc.rect(102, "Base notch", LAP, 810, 1098, 300, 14, [0.68, 0.68, 0.70, 1], r=7)
    sc.rect(103, "Bezel", LAP, -34, -34, 1988, 1148, [0.09, 0.09, 0.10, 1], r=72)
    DESK = sc.group(110, "Desktop", LAP, 0, 0)
    sc.rect(111, "Wallpaper", DESK, 0, 0, W, H, [0.93, 0.95, 0.99, 1])
    for i, (x, y, d, c) in enumerate([(-300, -400, 1300, [1.0, 0.86, 0.80, 0.55]), (1100, 350, 1300, [0.78, 0.86, 1.0, 0.6]),
                                      (400, 600, 900, [0.90, 0.84, 1.0, 0.45])]):
        g = sc.rect(112 + i, "Glow", DESK, x, y, d, d, c, r=d / 2)
        blur(sc, g, 7100 + i, 260)
    sc.rect(116, "Menu bar", DESK, 0, 0, W, 38, [1, 1, 1, 0.55])
    for i, (x, wd) in enumerate([(28, 18), (70, 64), (150, 44), (212, 52), (282, 40)]):
        sc.rect(117 + i, "Menu", DESK, x, 14, wd, 10, [0, 0, 0, 0.28 if i else 0.6], r=5)
    sc.text(123, "Clock", DESK, W - 28, 26, "wt. 14:32", 18, [0, 0, 0, 0.7], style="Medium", just="right")
    sc.rect(124, "Dock", DESK, 800, 986, 320, 78, [1, 1, 1, 0.5], r=24, stroke=([1, 1, 1, 0.8], 1.5))
    for i, c in enumerate([[0.30, 0.62, 1.0, 1], [0.86, 0.86, 0.88, 1], [0.86, 0.86, 0.88, 1], [0.93, 0.93, 0.95, 1]]):
        sc.rect(125 + i, "Dock icon", DESK, 818 + i * 74, 998, 56, 56, c, r=14)
    # the file
    ICON = sc.group(130, "PDF icon", DESK, 960, 470, 960, 470, op=0)
    page = sc.rect(131, "Page", ICON, 900, 390, 120, 156, A_BG, r=8, stroke=(A_LINE, 2))
    sc.shadow(page, 0.12, 20, 6)
    sc.path(132, "Fold", ICON, [(996, 390), (1020, 414), (996, 414)], 0, 0, fill=A_LINE)
    for i, wd in enumerate([72, 84, 60, 78]):
        sc.rect(133 + i, "Line", ICON, 916, 432 + i * 16, wd, 7, A_LINE, r=3.5)
    sc.rect(137, "Badge", ICON, 912, 500, 72, 30, A_RED, r=7)
    sc.text(138, "PDF", ICON, 948, 522, "PDF", 20, A_BG, just="center")
    lw = adv("Biznes.pdf", 22) + 26
    sc.rect(139, "Label bg", ICON, 960 - lw / 2, 562, lw, 34, A_BLUE, r=8)
    sc.text(140, "Label", ICON, 960, 586, "Biznes.pdf", 22, A_BG, style="Medium", just="center")
    sc.text(141, "Size", ICON, 960, 620, "2,4 MB", 18, A_GREY, style="Medium", just="center")
    fade(sc, ICON, AKT - 120, d_in=220)
    scale_keys(sc, ICON, [(0, f(200), LIN), (AKT - 120, f(200), HOLD), (AKT + 400, f(240), OUT),
                          (PLIK - 150, f(240), HOLD), (PLIK + 850, f(100), APPLE)])
    scale_keys(sc, LAP, [(0, f(100), LIN), (MAC - 250, f(100), HOLD), (MAC + 800, f(58), APPLE)])
    sc.k(LAP, "positionY", [(0, f(540), LIN), (MAC - 250, f(540), HOLD), (MAC + 800, f(500), APPLE)])
    return sc


# ================================================================== W  black punch
def scene_W():
    sc = new("W_Nie-jestes", 728.55, 730.62)
    sc.bg = [0, 0, 0, 1]
    w = sc.word
    SZ, NIE, JES, MASZ, PROD = w(728.70), w(729.10), w(729.36), w(729.90), w(730.18)
    q = sc.text(101, "Szczerze", None, 960, 560, "Szczerze?", 56, [1, 1, 1, 0.5], style="Medium", just="center", op=0)
    fade(sc, q, SZ - 60, NIE - 140, d_in=160, d_out=120)
    G = sc.group(110, "Big", None, 960, 540, 960, 540)
    big = sc.text(111, "Nie jestes", G, 960, 600, "Nie jesteś.", 176, A_BG, tracking=-45, just="center",
                  animators=[Scene.reveal_animator("wr1", "ws1", dy=30, blur=14)])
    sc.reveal_words(big, "ws1", [NIE, JES], step=160)
    sc.k(G, "positionY", [(0, f(540), LIN), (MASZ - 60, f(540), HOLD), (MASZ + 500, f(480), APPLE)])
    sub = sc.text(112, "Masz produkt", None, 960, 700, "Masz produkt.", 60, [1, 1, 1, 0.55], style="Medium",
                  tracking=-15, just="center", animators=[Scene.reveal_animator("wr2", "ws2", dy=18, blur=8)])
    sc.reveal_words(sub, "ws2", [MASZ, PROD], step=150)
    return sc


# ================================================================== X  stranger's journey (overlay)
def scene_X():
    sc = new("X_Droga-klienta", 731.30, 736.40)
    FX = overlay(sc)
    w = sc.word
    T = [w(732.92), w(733.86), w(734.36), w(734.98)]
    IN, OUT_ = sc.t(731.62), sc.t(736.02)
    CG = sc.group(110, "Card", FX, 960, 915, 960, 915, op=0)
    card_bg(sc, 111, CG, 400, 830, 1120, 170, r=46, fill=[1, 1, 1, 0.97], sh=(0.18, 60, 18))
    sc.rect(112, "Track", CG, 510, 893, 900, 4, A_LINE, r=2)
    prog = sc.rect(113, "Progress", CG, 510, 893, 0.01, 4, A_BLUE, r=2)
    xs = [510 + 300 * i for i in range(4)]
    pk = [(0, v2(0.01, 4), LIN)]
    for i, t in enumerate(T):
        pk += [(t - 380, v2(max(0.01, xs[i - 1] - 510) if i else 0.01, 4), HOLD), (t, v2(xs[i] - 510 or 0.01, 4), APPLE)]
    sc.k(prog, "rectSize", pk)
    labels = ["Zobaczy", "Zrozumie", "Zapłaci", "Dostanie"]
    for i, (x, t) in enumerate(zip(xs, T)):
        last = i == 3
        n = sc.rect(120 + i * 4, "Node", CG, x - 14, 881, 28, 28, A_LINE, r=14, ax=14, ay=14)
        sc.k(n, "fillColor", [(0, col(A_LINE), LIN), (t - 40, col(A_LINE), HOLD), (t + 160, col(A_GREEN if last else A_BLUE), SOFT)])
        scale_keys(sc, n, [(0, f(100), LIN), (t - 40, f(100), HOLD), (t + 140, f(135), OUT), (t + 520, f(100), APPLE)])
        lb = sc.text(121 + i * 4, "Label", CG, x, 962, labels[i], 30, A_GREY, style="Medium", just="center")
        sc.k(lb, "fillColor", [(0, col(A_GREY), LIN), (t - 40, col(A_GREY), HOLD), (t + 200, col(A_INK), SOFT)])
        if last:
            ck = check(sc, 123 + i * 4, CG, x, 895, 14, A_BG, 3, op=0)
            fade(sc, ck, t + 120, d_in=160)
    # the stranger travels along the line
    TR = sc.group(140, "Stranger", CG, 510, 895, 510, 895)
    sc.rect(141, "Halo", TR, 486, 871, 48, 48, a(A_BLUE, 0.16), r=24)
    sc.k(TR, "positionX", [(0, f(510), LIN)] + [(t - 380 if i else IN + 200, f(xs[i - 1] if i else 510), HOLD) for i, t in enumerate(T)][:1] +
         sum([[(t - 380, f(xs[i - 1]), HOLD), (t, f(xs[i]), APPLE)] for i, t in enumerate(T) if i], []))
    sc.k(CG, "opacity", [(0, f(0), LIN), (IN, f(0), HOLD), (IN + 260, f(100), SOFT), (OUT_, f(100), HOLD), (OUT_ + 300, f(0), SOFT)])
    sc.k(CG, "positionY", [(0, f(955), LIN), (IN, f(955), HOLD), (IN + 650, f(915), OUT), (OUT_, f(915), HOLD), (OUT_ + 300, f(940), SOFT)])
    return sc


# ================================================================== Y  2:00 AM lock screen, mails stacking
def scene_Y():
    sc = new("Y_Druga-w-nocy", 736.30, 739.95)
    sc.bg = [0.02, 0.025, 0.05, 1]
    sc.layers += [blob(20, -500, -700, 1600, [0.20, 0.25, 0.55, 0.55], dur=sc.dur),
                  blob(21, 900, 300, 1500, [0.35, 0.18, 0.45, 0.45], dur=sc.dur)]
    w = sc.word
    TN = [w(737.56), w(737.88), w(738.38), w(738.86)]
    MAIL = w(739.38)
    WH = A_BG
    # padlock
    sc.rect(101, "Lock body", None, 946, 118, 28, 22, [1, 1, 1, 0.85], r=6)
    sc.path(102, "Shackle", None, arc(960, 118, 9, 180, 360, 16), 0, 0, stroke=([1, 1, 1, 0.85], 3.5), closed=False)
    sc.text(103, "Date", None, 960, 214, "środa, 16 września", 32, [1, 1, 1, 0.8], style="Medium", just="center")
    clk = sc.text(104, "Clock", None, 960, 400, "2:00", 210, WH, tracking=-30, just="center")
    sc.k(clk, "textContent", [(0, s("2:00"), LIN), (MAIL + 200, s("2:01"), HOLD)])
    items = [("Ania K.", "Zapłaciłam 2 godziny temu. Gdzie jest PDF?"), ("Michał", "Nie dostałem maila z e-bookiem"),
             ("Ania K.", "Halo??"), ("Zamówienie #0147", "Nowy klient czeka na plik")]
    Y0, STEP = 519, 134
    for i, ((who, body), t) in enumerate(zip(items, TN)):
        g = sc.group(110 + i * 10, f"Notif {i}", None, 960, Y0, 960, Y0, op=0)
        card = sc.rect(111 + i * 10, "Card", g, 580, Y0 - 59, 760, 118, [0.30, 0.30, 0.34, 0.62], r=30)
        sc.rect(112 + i * 10, "Icon", g, 604, Y0 - 30, 60, 60, A_BLUE, r=14)
        sc.path(113 + i * 10, "Envelope", g, [(616, Y0 - 13), (652, Y0 - 13), (652, Y0 + 13), (616, Y0 + 13)], 0, 0,
                stroke=(WH, 3), closed=True)
        sc.path(114 + i * 10, "Flap", g, [(616, Y0 - 12), (634, Y0 + 2), (652, Y0 - 12)], 0, 0, stroke=(WH, 3), closed=False)
        sc.text(115 + i * 10, "Who", g, 686, Y0 - 8, who, 26, WH)
        sc.text(116 + i * 10, "When", g, 1312, Y0 - 8, "teraz", 22, [1, 1, 1, 0.55], style="Medium", just="right")
        sc.text(117 + i * 10, "Body", g, 686, Y0 + 30, body, 25, [1, 1, 1, 0.85], style="Medium")
        sc.k(g, "opacity", [(0, f(0), LIN), (t - 60, f(0), HOLD), (t + 160, f(100), SOFT)])
        scale_keys(sc, g, [(0, f(90), LIN), (t - 60, f(90), HOLD), (t + 480, f(100), APPLE)])
        pk, cur = [(0, f(Y0 - 40), LIN), (t - 60, f(Y0 - 40), HOLD), (t + 480, f(Y0), OUT)], Y0
        for j in range(i + 1, len(TN)):
            pk += [(TN[j] - 60, f(cur), HOLD), (TN[j] + 400, f(cur + STEP), APPLE)]
            cur += STEP
        sc.k(g, "positionY", pk)
    more = sc.group(160, "More", None, 960, 1040, 960, 1040, op=0)
    pill_text(sc, 161, more, 960, 1040, "+ 9 powiadomień", 22, WH, [0.30, 0.30, 0.34, 0.62])
    fade(sc, more, MAIL - 60, d_in=200)
    pop(sc, more, MAIL - 60, 420, 80)
    return sc


# ================================================================== Z  frosted glass → Safari window
def scene_Z():
    sc = new("Z_Za-szyba", 740.40, 748.15)
    sc.apple_bg()
    w = sc.word
    NW, ZOB, SWI, DEC, STR = w(741.36), w(743.78), w(744.50), w(746.14), w(747.40)
    # the product, unreadable behind glass
    BOOK = sc.group(110, "Product (blurred)", None, 0, 0)
    for i in range(2):
        sc.rect(111 + i, "Page", BOOK, 780 - i * 14 + 28, 300 + i * 10 + 10, 400, 540, [0.95, 0.95, 0.97, 1], r=14)
    cov = sc.rect(113, "Cover", BOOK, 760, 290, 400, 540, A_BG, r=14)
    sc.shadow(cov, 0.12, 40, 12)
    sc.rect(114, "Circle", BOOK, 840, 360, 240, 240, A_BLUE, r=120)
    sc.text(115, "T1", BOOK, 800, 690, "Zacznij naukę", 44, A_INK, tracking=-20)
    sc.text(116, "T2", BOOK, 800, 740, "w 5 minut", 44, A_BLUE, tracking=-20)
    sc.text(117, "Pages", BOOK, 800, 800, "27 stron", 20, A_GREY, style="Medium")
    for i, (x, y, t) in enumerate([(430, 330, "10 rozdziałów"), (1300, 420, "Plan nauki"), (470, 780, "Checklista"),
                                   (1330, 760, "Ćwiczenia")]):
        cg = sc.group(120 + i * 3, "Chip", BOOK, x, y, x, y, op=0)
        pill_text(sc, 121 + i * 3, cg, x, y, t, 30, A_INK, A_BG, style="SemiBold")
        fade(sc, cg, SWI - 250 + i * 110, d_in=220)
        pop(sc, cg, SWI - 250 + i * 110, 450, 70)
    blur(sc, BOOK, 7300, 26)
    # glass pane
    GX, GY, GW, GH = 340, 180, 1240, 720
    pane = sc.rect(130, "Glass", None, GX, GY, GW, GH, [1, 1, 1, 0.42], r=30, stroke=([1, 1, 1, 0.95], 2))
    sc.shadow(pane, 0.10, 60, 20)
    sc.k(pane, "fillColor", [(0, col([1, 1, 1, 0.42]), LIN), (DEC - 100, col([1, 1, 1, 0.42]), HOLD), (DEC + 350, col([1, 1, 1, 1]), SOFT)])
    sheen = sc.rect(131, "Sheen", None, GX + 60, GY + 40, 520, 18, [1, 1, 1, 0.7], r=9)
    fade(sc, sheen, 0, DEC - 100, d_in=1)
    qm = sc.text(132, "Question", None, 960, 600, "?", 220, [0.45, 0.45, 0.50, 0.55], just="center", op=0)
    fade(sc, qm, NW - 80, DEC - 150, d_in=250, d_out=200)
    pop(sc, qm, NW - 80, 500, 80) if False else None
    # Safari chrome + the page (the only thing the customer can see)
    WIN = sc.group(140, "Window", None, 0, 0, op=0)
    sc.rect(141, "Toolbar", WIN, GX, GY, GW, 70, A_FILL, r=30)
    sc.rect(142, "Toolbar sq", WIN, GX, GY + 36, GW, 34, A_FILL)
    sc.rect(143, "Toolbar line", WIN, GX, GY + 70, GW, 1.5, A_LINE)
    for i, c in enumerate([[1.0, 0.37, 0.34, 1], [1.0, 0.74, 0.18, 1], [0.16, 0.79, 0.25, 1]]):
        sc.rect(144 + i, "Light", WIN, GX + 28 + i * 26, GY + 28, 15, 15, c, r=7.5)
    sc.rect(147, "URL", WIN, 960 - 230, GY + 17, 460, 38, A_BG, r=10)
    sc.text(148, "URL text", WIN, 960, GY + 43, "twojastrona.pl", 20, A_GREY, style="Medium", just="center")
    fade(sc, WIN, DEC - 60, d_in=300)
    PG = sc.group(150, "Page", None, 0, 0)
    sc.text(151, "H1", PG, 960, 420, "Zacznij naukę w 5 minut", 64, A_INK, tracking=-30, just="center", op=0)
    sc.text(152, "Sub", PG, 960, 474, "nawet jeśli od rana odkładasz", 30, A_GREY, style="Medium", just="center", op=0)
    BT = sc.group(153, "Button", PG, 960, 570, 960, 570, op=0)
    sc.rect(154, "Btn", BT, 820, 536, 280, 68, A_BLUE, r=34)
    sc.text(155, "Btn txt", BT, 960, 580, "Kup teraz", 28, A_BG, just="center")
    for i in range(3):
        sc.rect(156 + i, "Benefit", PG, 600 + i * 250, 680, 220, 150, A_FILL, r=20, op=0)
    for i, lid in enumerate([151, 152, 153, 156, 157, 158]):
        t = DEC + 120 + i * 90
        sc.k(lid, "opacity", [(0, f(0), LIN), (t, f(0), HOLD), (t + 260, f(100), SOFT)])
    sc.k(PG, "positionY", [(0, f(24), LIN), (DEC + 100, f(24), HOLD), (DEC + 800, f(0), OUT)])
    scale_keys(sc, BT, [(0, f(100), LIN), (STR - 80, f(100), HOLD), (STR + 150, f(108), OUT), (STR + 500, f(100), APPLE)])
    return sc


# ================================================================== AA  landing-page anatomy (overlay)
def scene_AA():
    sc = new("AA_Anatomia-strony", 754.20, 777.00)
    FX = overlay(sc)
    w = sc.word
    IN, OUT_ = w(754.38), sc.t(776.75)
    CX0, CY0, CW, CH = 1380, 110, 420, 880
    L0 = CX0 + 36
    PG = sc.group(110, "Page card", FX, 0, 0, op=0)
    card_bg(sc, 111, PG, CX0, CY0, CW, CH, r=38, fill=[1, 1, 1, 0.98], sh=(0.18, 70, 20))
    names = ["Nagłówek", "Podnagłówek", "Zdjęcie produktu", "Nazwa", "Obietnica", "Benefity", "Cena", "Przycisk",
             "Dowody", "FAQ"]
    boxes = [(140, 98), (248, 40), (292, 166), (464, 42), (504, 58), (568, 92), (676, 50), (732, 76), (816, 78), (898, 72)]
    build = [w(755.88), w(758.64), w(760.80), w(761.94), w(762.32), w(762.86), w(763.38), w(763.70), w(764.82), w(775.88)]
    focus = [(w(766.86), 0), (w(767.68), 1), (w(770.32), 3), (w(770.74), 2), (w(771.82), 4), (w(772.52), 5),
             (w(773.16), 6), (w(773.58), 7), (w(775.22), 8), (w(775.88) + 250, 9)]

    def block(i):
        g = sc.group(200 + i * 20, names[i], PG, 0, 0, op=0)
        y0, bh = boxes[i]
        b = 201 + i * 20
        if i == 0:
            sc.text(b, "H1a", g, L0, y0 + 42, "Zacznij naukę", 38, A_INK, tracking=-20)
            sc.text(b + 1, "H1b", g, L0, y0 + 84, "w 5 minut", 38, A_BLUE, tracking=-20)
        elif i == 1:
            sc.text(b, "Sub", g, L0, y0 + 27, "nawet jeśli od rana odkładasz", 21, A_GREY, style="Medium")
        elif i == 2:
            sc.rect(b, "Img", g, L0, y0 + 4, 348, 156, A_FILL, r=18)
            sc.rect(b + 1, "Book", g, L0 + 139, y0 + 22, 70, 100, A_BG, r=6, stroke=(A_LINE, 1.5))
            sc.rect(b + 2, "Book circle", g, L0 + 154, y0 + 38, 40, 40, A_BLUE, r=20)
        elif i == 3:
            sc.rect(b, "Name", g, L0, y0 + 10, 230, 22, a(A_INK, 0.85), r=6)
        elif i == 4:
            sc.rect(b, "P1", g, L0, y0 + 10, 310, 14, a(A_BLUE, 0.55), r=7)
            sc.rect(b + 1, "P2", g, L0, y0 + 34, 220, 14, a(A_BLUE, 0.55), r=7)
        elif i == 5:
            for j in range(3):
                sc.rect(b + j * 2, "Dot", g, L0, y0 + 8 + j * 30, 18, 18, A_GREEN, r=9)
                sc.rect(b + j * 2 + 1, "Bar", g, L0 + 30, y0 + 12 + j * 30, [230, 190, 210][j], 10, A_LINE, r=5)
        elif i == 6:
            sc.rect(b, "Price", g, L0, y0 + 8, 116, 34, a(A_INK, 0.9), r=8)
            sc.rect(b + 1, "Old", g, L0 + 132, y0 + 20, 64, 12, A_LINE, r=6)
        elif i == 7:
            sc.rect(b, "Btn", g, L0, y0 + 8, 348, 60, A_BLUE, r=30)
            sc.text(b + 1, "Btn txt", g, L0 + 174, y0 + 47, "Kup teraz", 26, A_BG, just="center")
        elif i == 8:
            for j in range(5):
                cx, cy = L0 + 10 + j * 26, y0 + 18
                pts = [(cx + 10 * math.cos(math.radians(-90 + k * 36)) * (1 if k % 2 == 0 else 0.45),
                        cy + 10 * math.sin(math.radians(-90 + k * 36)) * (1 if k % 2 == 0 else 0.45)) for k in range(10)]
                sc.path(b + j, "Star", g, pts, 0, 0, fill=A_ORANGE)
            sc.rect(b + 5, "Q1", g, L0, y0 + 42, 300, 10, A_LINE, r=5)
            sc.rect(b + 6, "Q2", g, L0, y0 + 60, 210, 10, A_LINE, r=5)
        elif i == 9:
            for j in range(2):
                sc.rect(b + j * 3, "Sep", g, L0, y0 + j * 36, 348, 1.5, A_LINE)
                sc.rect(b + j * 3 + 1, "Q", g, L0, y0 + 14 + j * 36, 220, 10, a(A_INK, 0.6), r=5)
                sc.text(b + j * 3 + 2, "Plus", g, L0 + 348, y0 + 26 + j * 36, "+", 24, A_GREY, style="Medium", just="right")
        t = build[i]
        sc.k(g, "opacity", [(0, f(0), LIN), (t - 60, f(0), HOLD), (t + 200, f(100), SOFT)])
        sc.k(g, "positionY", [(0, f(-26), LIN), (t - 60, f(-26), HOLD), (t + 520, f(0), OUT)])
        # blueprint label on the left
        ly = y0 + bh / 2
        lb = sc.group(400 + i * 5, "Label " + names[i], FX, 0, 0, op=0)
        txt = sc.text(401 + i * 5, "Txt", lb, CX0 - 34, ly + 8, names[i], 23, A_INK, style="Medium", just="right")
        sc.rect(402 + i * 5, "Leader", lb, CX0 - 26, ly - 1, 30, 2, a(A_BLUE, 0.5), r=1)
        sc.rect(403 + i * 5, "Pin", lb, CX0 + 2, ly - 5, 10, 10, A_BLUE, r=5)
        sc.k(lb, "opacity", [(0, f(0), LIN), (t, f(0), HOLD), (t + 240, f(100), SOFT), (OUT_, f(100), HOLD), (OUT_ + 240, f(0), SOFT)])
        sc.k(lb, "positionX", [(0, f(20), LIN), (t, f(20), HOLD), (t + 500, f(0), OUT)])
        # label colour: ink on build → grey; blue while the visitor's eye is on it
        ck = [(0, col(A_INK), LIN), (t + 900, col(A_INK), HOLD), (t + 1200, col(A_GREY), SOFT)]
        for n, (ft, fi) in enumerate(focus):
            if fi == i:
                nxt = focus[n + 1][0] if n + 1 < len(focus) else OUT_
                if ft - 20 > ck[-1][0]:
                    ck += [(ft - 20, col(A_GREY), HOLD), (ft + 140, col(A_BLUE), SOFT)]
                    if nxt < OUT_:
                        ck += [(nxt - 20, col(A_BLUE), HOLD), (nxt + 160, col(A_GREY), SOFT)]
        sc.k(txt, "fillColor", ck)

    for i in range(10):
        block(i)
    # visitor's eye: focus frame travelling down the page
    fr = sc.rect(160, "Focus", PG, CX0 + 24, CY0 + 30, 372, 98, a(A_BLUE, 0.07), r=14, stroke=(A_BLUE, 3), op=0)
    ft0 = focus[0][0]
    sc.k(fr, "opacity", [(0, f(0), LIN), (ft0 - 100, f(0), HOLD), (ft0 + 120, f(100), SOFT)])
    pk, sk = [], []
    for n, (ft, fi) in enumerate(focus):
        y0, bh = boxes[fi]
        pk.append((ft - 60 if n else 0, CX0 + 24, y0 - 8, APPLE if n else LIN))
        sk.append((ft - 60 if n else 0, v2(372, bh + 16), APPLE if n else LIN))
        if n:
            pk.insert(-1, (focus[n - 1][0] + 400, pk[-2][1], pk[-2][2], HOLD)) if focus[n - 1][0] + 400 < ft - 60 else None
    # rebuild clean hold→move tracks
    pk2, sk2 = [(0, CX0 + 24, boxes[focus[0][1]][0] - 8, LIN)], [(0, v2(372, boxes[focus[0][1]][1] + 16), LIN)]
    for n in range(1, len(focus)):
        ft, fi = focus[n]
        y0, bh = boxes[fi]
        py, pb = boxes[focus[n - 1][1]]
        pk2 += [(ft - 380, CX0 + 24, py - 8, HOLD), (ft, CX0 + 24, y0 - 8, APPLE)]
        sk2 += [(ft - 380, v2(372, pb + 16), HOLD), (ft, v2(372, bh + 16), APPLE)]
    sc.kpos(fr, pk2)
    sc.k(fr, "rectSize", sk2)
    sc.k(PG, "opacity", [(0, f(0), LIN), (IN, f(0), HOLD), (IN + 300, f(100), SOFT), (OUT_, f(100), HOLD), (OUT_ + 260, f(0), SOFT)])
    sc.k(PG, "positionX", [(0, f(60), LIN), (IN, f(60), HOLD), (IN + 800, f(0), OUT)])
    return sc


# ================================================================== AB  two phones: traffic falls through vs into the cart
def scene_AB():
    sc = new("AB_Konwersja", 777.00, 784.85)
    sc.apple_bg()
    w = sc.word
    L_IN, R_IN, ZDOB = w(778.98), w(780.78), w(783.90)

    def phone(base, cx, t_in, title, tcol):
        g = sc.group(base, "Phone", None, cx, 530, cx, 530, op=0)
        fr = sc.rect(base + 1, "Frame", g, cx - 160, 200, 320, 640, A_BG, r=52, stroke=(A_LINE, 3))
        sc.shadow(fr, 0.10, 50, 16)
        sc.rect(base + 2, "Island", g, cx - 46, 218, 92, 26, A_INK, r=13)
        sc.rect(base + 3, "H1", g, cx - 116, 290, 232, 22, a(A_INK, 0.85), r=7)
        sc.rect(base + 4, "H2", g, cx - 86, 322, 172, 22, a(A_INK, 0.85), r=7)
        sc.rect(base + 5, "Img", g, cx - 116, 374, 232, 170, A_FILL, r=18)
        sc.rect(base + 6, "Btn", g, cx - 116, 568, 232, 50, A_BLUE, r=25)
        sc.text(base + 7, "Title", g, cx, 912, title, 34, tcol, just="center", tracking=-10)
        fade(sc, g, t_in - 60, d_in=240)
        pop(sc, g, t_in - 60, 650, 92)
        return g

    phone(110, 620, L_IN, "Jakaś strona", A_GREY)
    phone(130, 1300, R_IN, "Strona, która konwertuje", A_INK)
    # cart inside the right phone
    CART = sc.group(150, "Cart", None, 1300, 740, 1300, 740, op=0)
    sc.rect(151, "Cart bg", CART, 1260, 700, 80, 80, a(A_GREEN, 0.14), r=40)
    sc.path(152, "Bag", CART, [(1282, 724), (1318, 724), (1314, 760), (1286, 760)], 0, 0, stroke=(A_GREEN, 4))
    sc.path(153, "Handle", CART, arc(1300, 724, 10, 180, 360, 12), 0, 0, stroke=(A_GREEN, 4), closed=False)
    fade(sc, CART, R_IN + 300, d_in=200)
    # counters
    lc = sc.text(160, "L count", None, 620, 964, "Klienci: 0", 28, A_GREY, style="Medium", family="Geist Mono", just="center", op=0)
    rc = sc.text(161, "R count", None, 1300, 964, "Klienci: 0", 28, A_INK, style="Medium", family="Geist Mono", just="center", op=0)
    fade(sc, lc, L_IN + 300)
    fade(sc, rc, R_IN + 300)
    random.seed(4)
    lid = 300
    # left: visitors fall through the page and leave
    t = L_IN + 400
    while t < sc.dur - 700:
        ox = random.uniform(-90, 90)
        d = sc.rect(lid, "Visitor L", None, 620 + ox - 9, 120, 18, 18, A_BLUE, r=9, op=0)
        sc.k(d, "opacity", [(0, f(0), LIN), (t, f(0), HOLD), (t + 150, f(100), SOFT), (t + 900, f(100), HOLD), (t + 1300, f(0), SOFT)])
        sc.kpos(d, [(0, 620 + ox - 9, 120, LIN), (t, 620 + ox - 9, 120, HOLD), (t + 700, 620 + ox - 9, 560, IN),
                    (t + 1300, 620 + ox + (230 if ox > 0 else -230), 740, OUT)])
        lid += 1
        t += 330
    # right: visitors land in the cart
    t, hits = R_IN + 450, []
    while t < sc.dur - 900:
        ox = random.uniform(-90, 90)
        d = sc.rect(lid, "Visitor R", None, 1300 + ox - 9, 120, 18, 18, A_BLUE, r=9, op=0)
        sc.k(d, "opacity", [(0, f(0), LIN), (t, f(0), HOLD), (t + 150, f(100), SOFT), (t + 820, f(100), HOLD), (t + 900, f(0), SOFT)])
        sc.kpos(d, [(0, 1300 + ox - 9, 120, LIN), (t, 1300 + ox - 9, 120, HOLD), (t + 900, 1291, 731, IN)])
        hits.append(t + 900)
        lid += 1
        t += 300
    ck, bump = [(0, s("Klienci: 0"), LIN)], [(0, f(100), LIN)]
    for n, h in enumerate(hits):
        ck.append((h, s(f"Klienci: {n + 1}"), HOLD))
        bump += [(h - 1, f(100), HOLD), (h + 60, f(112), OUT), (h + 240, f(100), SOFT)]
    sc.k(rc, "textContent", ck)
    scale_keys(sc, CART, bump)
    sc.k(rc, "fillColor", [(0, col(A_INK), LIN), (ZDOB, col(A_INK), HOLD), (ZDOB + 200, col(A_GREEN), SOFT)])
    return sc


# ================================================================== AC  Live Text scan → product data (overlay)
def scene_AC():
    sc = new("AC_Czytanie-pliku", 796.10, 804.40)
    FX = overlay(sc)
    w = sc.word
    CZYT, POTRZ = w(797.16), w(799.82)
    FIELD_T = [w(801.32), w(801.80), w(802.54), w(803.12)]
    OUT_ = sc.t(804.05)
    DOC = sc.group(110, "Doc", FX, 470, 530, 470, 530, op=0)
    card_bg(sc, 111, DOC, 240, 190, 460, 680, r=26, sh=(0.18, 60, 18))
    sc.text(112, "Chapter", DOC, 280, 252, "Rozdział 1", 24, A_INK)
    rng = random.Random(3)
    KEY = {1: 0, 4: 1, 9: 2, 13: 3}
    lines = []
    for i in range(16):
        y = 290 + i * 34
        wd = rng.randint(290, 380)
        hl = sc.rect(130 + i * 2, "Sel", DOC, 274, y - 7, wd + 12, 26, a(A_BLUE, 0.16), r=6, op=0)
        sc.rect(131 + i * 2, "Line", DOC, 280, y, wd, 12, A_LINE, r=6)
        lines.append((y, wd, hl))
    sc.text(170, "Page no", DOC, 470, 848, "str. 1 / 27", 18, A_GREY, style="Medium", family="Geist Mono", just="center")
    scan0, scan1 = CZYT, POTRZ
    for i, (y, wd, hl) in enumerate(lines):
        t = int(scan0 + (y - 190) / 680 * (scan1 - scan0))
        on = i in KEY
        keys = [(0, f(0), LIN), (t, f(0), HOLD), (t + 120, f(100), SOFT)]
        if not on:
            keys += [(t + 700, f(100), HOLD), (t + 1100, f(0), SOFT)]
        sc.k(hl, "opacity", keys)
        if on:
            sc.k(hl, "fillColor", [(0, col(a(A_BLUE, 0.16)), LIN), (FIELD_T[KEY[i]] - 80, col(a(A_BLUE, 0.16)), HOLD),
                                   (FIELD_T[KEY[i]] + 120, col(a(A_ORANGE, 0.30)), SOFT)])
    SC = sc.group(180, "Scanner", DOC, 0, 190, 0, 190, op=0)
    gl = sc.rect(181, "Glow", SC, 250, 160, 440, 60, a(A_BLUE, 0.22), r=30)
    blur(sc, gl, 7400, 18)
    sc.rect(182, "Beam", SC, 244, 188, 452, 4, A_BLUE, r=2)
    sc.k(SC, "opacity", [(0, f(0), LIN), (scan0 - 120, f(0), HOLD), (scan0, f(100), SOFT), (scan1, f(100), HOLD), (scan1 + 200, f(0), SOFT)])
    sc.k(SC, "positionY", [(0, f(190), LIN), (scan0, f(190), HOLD), (scan1, f(870), INOUT)])
    fade(sc, DOC, sc.t(796.25), OUT_, d_in=260)
    pop(sc, DOC, sc.t(796.25), 600, 94)
    # data card
    DC = sc.group(200, "Data card", FX, 0, 0, op=0)
    card_bg(sc, 201, DC, 780, 280, 560, 500, r=30, sh=(0.18, 60, 18))
    sc.text(202, "Title", DC, 820, 340, "Dane produktu", 30, A_INK, tracking=-10)
    sc.rect(203, "AI", DC, 1236, 312, 64, 34, a(A_BLUE, 0.12), r=17)
    sc.text(204, "AI txt", DC, 1268, 336, "AI", 20, A_BLUE, just="center")
    keys_ = ["O czym", "Dla kogo", "Stron", "Obietnica"]
    vals = ["Produktywna nauka", "Uczniowie i studenci", "27", "Zacznij naukę w 5 minut"]
    for i in range(4):
        ry = 420 + i * 88
        sc.rect(210 + i * 6, "Sep", DC, 820, ry - 48, 480, 1.5, A_LINE)
        kl = sc.text(211 + i * 6, "Key", DC, 820, ry - 14, keys_[i], 20, A_GREY, style="Medium", op=0)
        t = FIELD_T[i]
        fade(sc, kl, t - 100, d_in=200)
        src_y = [l[0] for n, l in enumerate(lines) if n in KEY][i]
        g = sc.group(212 + i * 6, "Value", DC, 820, ry + 22, 820, ry + 22, op=0)
        sc.text(213 + i * 6, "Val", g, 820, ry + 22, vals[i], 30, A_INK, tracking=-10)
        sc.k(g, "opacity", [(0, f(0), LIN), (t - 60, f(0), HOLD), (t + 120, f(100), SOFT)])
        sc.kpos(g, [(0, 290, src_y + 12, LIN), (t - 60, 290, src_y + 12, HOLD), (t + 620, 820, ry + 22, APPLE)])
        scale_keys(sc, g, [(0, f(55), LIN), (t - 60, f(55), HOLD), (t + 620, f(100), APPLE)])
    fade(sc, DC, POTRZ - 200, OUT_, d_in=260)
    sc.k(DC, "positionX", [(0, f(40), LIN), (POTRZ - 200, f(40), HOLD), (POTRZ + 500, f(0), OUT)])
    return sc


# ================================================================== AD  browser vs download (overlay, top-right)
def scene_AD():
    sc = new("AD_Przegladarka", 818.20, 843.20)
    FX = overlay(sc)
    w = sc.word
    IN, T1, T2, SEL = w(818.74), w(820.78), w(821.66), w(824.48)
    LOG, EXC, POB, BACK, BEST = w(829.20), w(835.54), w(836.50), w(839.92), w(841.54)
    OUT_ = sc.t(842.85)
    P = sc.group(110, "Panel", FX, 1500, 260, 1500, 260, op=0)
    card_bg(sc, 111, P, 1160, 80, 680, 370, r=34, fill=[1, 1, 1, 0.97], sh=(0.18, 60, 18))
    sc.text(112, "Title", P, 1200, 140, "Jak klient dostaje e-booka?", 28, A_INK, tracking=-10)

    def tile(base, x, t_in, label, sub):
        g = sc.group(base, label, P, x + 145, 290, x + 145, 290, op=0)
        bg = sc.rect(base + 1, "Tile", g, x, 172, 290, 240, A_FILL, r=24, stroke=([1, 1, 1, 0], 3))
        sc.text(base + 2, "Label", g, x + 145, 344, label, 26, A_INK, just="center")
        sb = sc.text(base + 3, "Sub", g, x + 145, 380, sub, 20, A_GREY, style="Medium", just="center", op=0)
        fade(sc, g, t_in - 60, d_in=220)
        pop(sc, g, t_in - 60, 500, 90)
        return g, bg, sb

    g1, bg1, sb1 = tile(120, 1200, T1, "W przeglądarce", "loguje się i czyta")
    g2, bg2, sb2 = tile(140, 1510, T2, "Pobiera na dysk", "np. szablon Excela")
    # icons
    ix = 1345
    sc.rect(130, "Win", g1, ix - 56, 204, 112, 80, [1, 1, 1, 0], r=12, stroke=(A_INK, 3))
    sc.rect(131, "Win bar", g1, ix - 56, 224, 112, 3, A_INK)
    for i in range(3):
        sc.rect(132 + i, "Dot", g1, ix - 46 + i * 11, 211, 7, 7, A_INK, r=3.5)
    sc.rect(135, "Lock", g1, ix - 11, 250, 22, 18, A_INK, r=4)
    sc.path(136, "Shackle", g1, arc(ix, 250, 7, 180, 360, 12), 0, 0, stroke=(A_INK, 3), closed=False)
    jx = 1655
    sc.path(150, "Arrow", g2, [(jx, 204), (jx, 256)], 0, 0, stroke=(A_INK, 4), closed=False)
    sc.path(151, "Head", g2, [(jx - 18, 240), (jx, 258), (jx + 18, 240)], 0, 0, stroke=(A_INK, 4), closed=False)
    sc.path(152, "Tray", g2, [(jx - 40, 262), (jx - 40, 282), (jx + 40, 282), (jx + 40, 262)], 0, 0, stroke=(A_INK, 4), closed=False)
    # selection states
    sc.k(bg1, "strokeColor", [(0, col([1, 1, 1, 0]), LIN), (SEL - 60, col([1, 1, 1, 0]), HOLD), (SEL + 200, col(A_BLUE), SOFT)])
    sc.k(bg1, "fillColor", [(0, col(A_FILL), LIN), (SEL - 60, col(A_FILL), HOLD), (SEL + 200, col(a(A_BLUE, 0.06)), SOFT)])
    badge = sc.group(160, "Badge", g1, 1462, 200, 1462, 200, op=0)
    sc.rect(161, "Badge bg", badge, 1446, 184, 32, 32, A_BLUE, r=16)
    check(sc, 162, badge, 1462, 201, 12, A_BG, 3)
    fade(sc, badge, SEL + 60, d_in=160)
    pop(sc, badge, SEL + 60, 380, 50)
    sc.k(bg2, "strokeColor", [(0, col([1, 1, 1, 0]), LIN), (EXC - 60, col([1, 1, 1, 0]), HOLD), (EXC + 200, col(A_ORANGE), SOFT),
                              (BACK - 60, col(A_ORANGE), HOLD), (BACK + 250, col([1, 1, 1, 0]), SOFT)])
    sc.k(g2, "opacity", [(0, f(0), LIN), (T2 - 60, f(0), HOLD), (T2 + 160, f(100), SOFT), (SEL + 100, f(100), HOLD),
                         (SEL + 400, f(55), SOFT), (EXC - 100, f(55), HOLD), (EXC + 150, f(100), SOFT),
                         (BACK - 60, f(100), HOLD), (BACK + 300, f(55), SOFT)])
    fade(sc, sb1, LOG - 60)
    sc.k(sb1, "textContent", [(0, s("loguje się i czyta"), LIN), (BEST, s("najlepsze dla e-booków"), HOLD)])
    sc.k(sb1, "fillColor", [(0, col(A_GREY), LIN), (BEST, col(A_BLUE), HOLD)])
    fade(sc, sb2, EXC - 60)
    sc.k(P, "opacity", [(0, f(0), LIN), (IN, f(0), HOLD), (IN + 260, f(100), SOFT), (OUT_, f(100), HOLD), (OUT_ + 260, f(0), SOFT)])
    scale_keys(sc, P, [(0, f(94), LIN), (IN, f(94), HOLD), (IN + 650, f(100), OUT)])
    return sc


# ================================================================== AE  Calendar: the customer's day
def scene_AE():
    sc = new("AE_Dzien-klienta", 850.10, 857.75)
    sc.bg = A_BG
    w = sc.word
    KTO, DZIEN, OBJ = w(850.32), w(851.46), w(853.24)
    HH = 100
    yh = lambda h: 300 + (h - 7) * HH
    CAL = sc.group(110, "Calendar", None, 0, 0)
    for h in range(7, 25):
        sc.text(111 + (h - 7) * 2, "Hour", CAL, 212, yh(h) + 7, f"{h % 24:02d}:00", 20, A_GREY, style="Medium",
                family="Geist Mono", just="right")
        sc.rect(112 + (h - 7) * 2, "Line", CAL, 240, yh(h), 1540, 1.5, A_LINE)
    BLUEC, GREENC, ORANGEC, REDC, PURPLE, GREYC = A_BLUE, A_GREEN, A_ORANGE, A_RED, [0.69, 0.32, 0.87, 1], A_GREY
    ev = [(7.5, 8.0, "Budzik", "drzemka ×3", GREYC, 850.35),
          (8.0, 14.5, "Szkoła / uczelnia", "", BLUEC, 850.70),
          (16.0, 16.5, "Zaraz się pouczę", "", GREENC, 851.45),
          (16.5, 19.5, "Telefon", "TikTok · Instagram · YouTube", ORANGEC, 851.85),
          (21.5, 22.2, "Jutro sprawdzian", "stres rośnie", REDC, 852.40),
          (23.4, 24.0, "Jutro zacznę", "", PURPLE, 852.95)]
    for i, (h0, h1, title, sub, c, tt) in enumerate(ev):
        t = sc.t(tt)
        y0, hgt = yh(h0) + 3, max(58, (h1 - h0) * HH - 6)
        g = sc.group(160 + i * 6, title, CAL, 280, y0, 280, y0, op=0)
        sc.rect(161 + i * 6, "Bg", g, 280, y0, 1480, hgt, a(c, 0.13), r=12)
        sc.rect(162 + i * 6, "Bar", g, 280, y0, 7, hgt, c, r=3.5)
        dark = [c[0] * 0.62, c[1] * 0.62, c[2] * 0.62, 1]
        sc.text(163 + i * 6, "Title", g, 306, y0 + 38, title, 28, dark)
        if sub:
            sc.text(164 + i * 6, "Sub", g, 306 + adv(title, 28, "SemiBold") + 18, y0 + 38, sub, 24, a(dark, 0.7), style="Medium")
        sc.k(g, "opacity", [(0, f(0), LIN), (t, f(0), HOLD), (t + 220, f(100), SOFT)])
        sc.k(g, "positionX", [(0, f(310), LIN), (t, f(310), HOLD), (t + 550, f(280), OUT)])
    sc.k(CAL, "positionY", [(0, f(0), LIN), (DZIEN - 400, f(0), HOLD), (sc.t(853.35), f(-940), INOUT)])
    # problem tags on the three that matter
    for n, (i, tt) in enumerate([(2, OBJ + 350), (3, OBJ + 650), (5, OBJ + 950)]):
        h0 = ev[i][0]
        y = yh(h0) + 3 + 29
        g = sc.group(200 + n * 4, "Problem tag", CAL, 1660, y, 1660, y, op=0)
        pill_text(sc, 201 + n * 4, g, 1660, y, "Problem", 22, A_BG, A_RED, style="SemiBold")
        fade(sc, g, tt, d_in=160)
        pop(sc, g, tt, 420, 60)
    rep = sc.text(220, "Repeat", CAL, 306, yh(23.4) + 3 + 38 + 0, "", 24, a(PURPLE, 0.8), style="Medium")
    sc.k(rep, "textContent", [(0, s(""), LIN), (sc.t(855.3), s(""), HOLD)])
    rg = sc.group(221, "Repeat tag", CAL, 0, 0, op=0)
    sc.text(222, "Repeat txt", rg, 306 + adv("Jutro zacznę", 28, "SemiBold") + 18, yh(23.4) + 41,
            "powtarza się codziennie", 24, a([0.43, 0.2, 0.54, 1], 0.8), style="Medium")
    fade(sc, rg, sc.t(855.35), d_in=260)
    # fixed header on top
    sc.rect(230, "Header bg", None, 0, 0, W, 226, A_BG)
    sc.text(231, "Day", None, 160, 104, "WTOREK", 24, A_RED, tracking=40)
    hd = sc.text(232, "Title", None, 160, 176, "Dzień Twojego klienta", 60, A_INK, tracking=-25, op=0)
    fade(sc, hd, KTO - 60, d_in=240)
    sc.rect(233, "Header rule", None, 160, 224, 1600, 1.5, A_LINE)
    return sc


# ================================================================== AF  promises ↔ chapters (overlay)
def scene_AF():
    sc = new("AF_Obietnice", 885.40, 897.50)
    FX = overlay(sc)
    w = sc.word
    IN, CUDA, NIE, KOP, SRODEK = w(886.58), w(890.20), w(892.16), w(892.72), w(894.40)
    OUT_ = sc.t(897.10)
    CG = sc.group(110, "Card", FX, 960, 540, 960, 540, op=0)
    card_bg(sc, 111, CG, 360, 250, 1200, 580, r=40, fill=[1, 1, 1, 0.98], sh=(0.18, 70, 20))
    sc.text(112, "L head", CG, 420, 330, "Strona obiecuje", 26, A_GREY)
    sc.text(113, "R head", CG, 1080, 330, "Produkt zawiera", 26, A_GREY)
    rows = [400, 490, 580, 670]
    L = ["Start w 5 minut", "Plan na każdy dzień", "Same szóstki w tydzień", "Koniec z odkładaniem"]
    R = {0: "Rozdział 2 · Pierwsze 5 minut", 1: "Rozdział 4 · Plan nauki", 3: "Rozdział 7 · Odkładanie"}
    lines = []
    for i, y in enumerate(rows):
        bogus = i == 2
        t = CUDA if bogus else IN + 200 + i * 220
        g = sc.group(120 + i * 10, "Promise", CG, 630, y + 32, 630, y + 32, op=0)
        bg = sc.rect(121 + i * 10, "Bg", g, 420, y, 420, 64, A_FILL, r=32, stroke=([1, 1, 1, 0], 2.5))
        tx = sc.text(122 + i * 10, "Txt", g, 450, y + 42, L[i], 27, A_INK, style="Medium")
        if bogus:
            sc.k(bg, "strokeColor", [(0, col(A_ORANGE), LIN), (NIE - 200, col(A_ORANGE), HOLD), (NIE, col(A_RED), SOFT)])
            sc.k(tx, "fillColor", [(0, col(A_INK), LIN), (NIE - 200, col(A_INK), HOLD), (NIE, col(A_RED), SOFT)])
            sc.k(g, "opacity", [(0, f(0), LIN), (t - 60, f(0), HOLD), (t + 200, f(100), SOFT), (KOP + 100, f(100), HOLD), (KOP + 500, f(0), SOFT)])
            scale_keys(sc, g, [(0, f(85), LIN), (t - 60, f(85), HOLD), (t + 500, f(100), OUT), (KOP + 100, f(100), HOLD), (KOP + 500, f(88), SOFT)])
            sc.k(g, "positionY", [(0, f(y + 32), LIN), (KOP + 100, f(y + 32), HOLD), (KOP + 500, f(y + 60), IN)])
            # probe line reaching for a chapter that doesn't exist
            pr = sc.rect(125 + i * 10, "Probe", CG, 848, y + 31, 0.01, 3, A_RED, r=1.5, op=0)
            sc.k(pr, "rectSize", [(0, v2(0.01, 3), LIN), (t + 500, v2(0.01, 3), HOLD), (t + 1300, v2(120, 3), OUT)])
            sc.k(pr, "opacity", [(0, f(0), LIN), (t + 500, f(0), HOLD), (t + 560, f(100), SOFT), (KOP + 100, f(100), HOLD), (KOP + 400, f(0), SOFT)])
            mg = sc.group(126 + i * 10, "Missing", CG, 1290, y + 32, 1290, y + 32, op=0)
            sc.rect(127 + i * 10, "Missing bg", mg, 1080, y, 420, 64, [1, 1, 1, 0], r=32, stroke=(a(A_RED, 0.6), 2.5))
            sc.text(128 + i * 10, "Missing txt", mg, 1290, y + 42, "Brak w produkcie", 26, A_RED, style="Medium", just="center")
            sc.k(mg, "opacity", [(0, f(0), LIN), (NIE - 250, f(0), HOLD), (NIE, f(100), SOFT), (KOP + 100, f(100), HOLD), (KOP + 450, f(0), SOFT)])
            pop(sc, mg, NIE - 250, 450, 90)
            continue
        sc.k(g, "opacity", [(0, f(0), LIN), (t - 60, f(0), HOLD), (t + 200, f(100), SOFT)])
        sc.k(g, "positionX", [(0, f(600), LIN), (t - 60, f(600), HOLD), (t + 500, f(630), OUT)])
        rg = sc.group(123 + i * 10, "Chapter", CG, 1290, y + 32, 1290, y + 32, op=0)
        rbg = sc.rect(124 + i * 10, "Ch bg", rg, 1080, y, 420, 64, A_FILL, r=32)
        sc.text(125 + i * 10, "Ch txt", rg, 1110, y + 42, R[i], 25, A_INK, style="Medium")
        tr = t + 150
        sc.k(rg, "opacity", [(0, f(0), LIN), (tr - 60, f(0), HOLD), (tr + 200, f(100), SOFT)])
        sc.k(rg, "positionX", [(0, f(1320), LIN), (tr - 60, f(1320), HOLD), (tr + 500, f(1290), OUT)])
        ln = sc.rect(126 + i * 10, "Link", CG, 846, y + 31, 0.01, 3, A_LINE, r=1.5)
        sc.k(ln, "rectSize", [(0, v2(0.01, 3), LIN), (tr + 250, v2(0.01, 3), HOLD), (tr + 750, v2(228, 3), INOUT)])
        lines.append((ln, rbg))
        ckg = sc.group(127 + i * 10, "Ok", CG, 1470, y + 32, 1470, y + 32, op=0)
        sc.rect(128 + i * 10, "Ok bg", ckg, 1454, y + 16, 32, 32, A_GREEN, r=16)
        check(sc, 129 + i * 10, ckg, 1470, y + 33, 12, A_BG, 3)
    for n, (ln, rbg) in enumerate(lines):
        t = SRODEK + n * 180
        sc.k(ln, "fillColor", [(0, col(A_LINE), LIN), (t, col(A_LINE), HOLD), (t + 250, col(A_GREEN), SOFT)])
        sc.k(rbg, "fillColor", [(0, col(A_FILL), LIN), (t, col(A_FILL), HOLD), (t + 250, col(a(A_GREEN, 0.12)), SOFT)])
        ckg = [127, 137, 157][n]
        fade(sc, ckg, t + 100, d_in=160)
        pop(sc, ckg, t + 100, 380, 50)
    sc.k(CG, "opacity", [(0, f(0), LIN), (IN - 150, f(0), HOLD), (IN + 150, f(100), SOFT), (OUT_, f(100), HOLD), (OUT_ + 280, f(0), SOFT)])
    scale_keys(sc, CG, [(0, f(95), LIN), (IN - 150, f(95), HOLD), (IN + 600, f(100), OUT)])
    return sc


# ================================================================== AG  ⌘C ⌘V keycaps
def keycap(sc, base, parent, cx, cy, sz, presses, sym=None, word=None, letter=None):
    """Mac-style keycap. presses = [(t_down, t_up)]. Returns dict of text layer ids."""
    g = sc.group(base, "Key", parent, cx, cy, cx, cy)
    side = sc.rect(base + 1, "Side", g, cx - sz / 2, cy - sz / 2 + 12, sz, sz, [0.80, 0.80, 0.83, 1], r=sz * 0.14)
    sc.shadow(side, 0.14, 40, 16)
    TOP = sc.group(base + 2, "Top", g, 0, 0)
    face = sc.rect(base + 3, "Face", TOP, cx - sz / 2, cy - sz / 2, sz, sz, A_BG, r=sz * 0.14, stroke=(A_LINE, 2))
    out = {}
    if sym:
        out["sym"] = cmd_symbol(sc, base + 10, TOP, cx + sz * 0.26, cy - sz * 0.26, sz * 0.36, A_INK, sz * 0.022)
    if word:
        out["word"] = sc.text(base + 4, "Word", TOP, cx - sz * 0.38, cy + sz * 0.36, word, sz * 0.1, A_GREY, style="Medium")
    if letter:
        out["letter"] = sc.text(base + 5, "Letter", TOP, cx, cy + sz * 0.13, letter, sz * 0.36, A_INK, just="center")
    ky, fk = [(0, f(0), LIN)], [(0, col(A_BG), LIN)]
    for d, u in presses:
        ky += [(d - 1, f(0), HOLD), (d + 50, f(10), OUT), (u, f(10), HOLD), (u + 130, f(0), OUT)]
        fk += [(d - 1, col(A_BG), HOLD), (d + 50, col([0.94, 0.94, 0.96, 1]), SOFT), (u, col([0.94, 0.94, 0.96, 1]), HOLD),
               (u + 130, col(A_BG), SOFT)]
    sc.k(TOP, "positionY", ky)
    sc.k(face, "fillColor", fk)
    return g, out


def hud(sc, base, parent, cx, cy, events):
    """macOS-style HUD pill. events = [(t_in, t_out, text)]."""
    g = sc.group(base, "HUD", parent, cx, cy, cx, cy, op=0)
    sc.rect(base + 1, "HUD bg", g, cx - 150, cy - 34, 300, 68, [0.12, 0.12, 0.14, 0.86], r=34)
    tx = sc.text(base + 2, "HUD txt", g, cx, cy + 10, events[0][2], 28, A_BG, style="Medium", just="center")
    ok, tk = [(0, f(0), LIN)], [(0, s(events[0][2]), LIN)]
    for t0, t1, txt in events:
        ok += [(t0 - 1, f(0), HOLD), (t0 + 120, f(100), SOFT), (t1, f(100), HOLD), (t1 + 180, f(0), SOFT)]
        tk.append((t0, s(txt), HOLD))
    sc.k(g, "opacity", ok)
    sc.k(tx, "textContent", tk)
    return g


def scene_AG_a():
    sc = new("AG_a_Command", 917.80, 923.95)
    sc.apple_bg()
    w = sc.word
    CM1, C1, CM2, V1, WIN = w(918.70), w(919.10), w(919.44), w(919.60), w(920.28)
    CT1, C2, CT2, V2, BUM, SKL = w(921.42), w(921.68), w(921.96), w(922.12), w(922.98), w(923.32)
    KEYS = sc.group(100, "Keys", None, 960, 500, 960, 500, op=0)
    fade(sc, KEYS, 60, d_in=240)
    scale_keys(sc, KEYS, [(0, f(94), LIN), (60, f(94), HOLD), (700, f(100), OUT), (BUM - 60, f(100), HOLD), (BUM + 350, f(80), APPLE)])
    sc.k(KEYS, "opacity", [(0, f(0), LIN), (60, f(0), HOLD), (300, f(100), SOFT), (BUM - 60, f(100), HOLD), (BUM + 300, f(0), SOFT)])
    _, kl = keycap(sc, 200, KEYS, 770, 500, 320, [(CM1, V1 + 300), (CT1, V2 + 250)], sym=True, word="command")
    _, kr = keycap(sc, 300, KEYS, 1150, 500, 320, [(C1, C1 + 230), (V1, V1 + 250), (C2, C2 + 200), (V2, V2 + 230)], letter="C")
    sc.k(kr["letter"], "textContent", [(0, s("C"), LIN), (C1 + 330, s("V"), HOLD), (WIN, s("C"), HOLD), (C2 + 250, s("V"), HOLD)])
    sc.k(kl["word"], "textContent", [(0, s("command"), LIN), (WIN + 150, s("ctrl"), HOLD)])
    for lid in kl["sym"]:
        sc.k(lid, "opacity", [(0, f(100), LIN), (WIN, f(100), HOLD), (WIN + 250, f(0), SOFT)])
    wl = sc.text(150, "Win label", None, 960, 250, "Windows", 28, A_GREY, style="Medium", just="center", op=0)
    sc.k(wl, "opacity", [(0, f(0), LIN), (WIN, f(0), HOLD), (WIN + 250, f(100), SOFT), (BUM - 60, f(100), HOLD), (BUM + 200, f(0), SOFT)])
    hud(sc, 160, None, 960, 820, [(C1, C1 + 420, "Skopiowano"), (V1, V1 + 560, "Wklejono"), (C2, C2 + 380, "Skopiowano"),
                                  (V2, V2 + 520, "Wklejono")])
    # "bum, gotowy sklep"
    OK = sc.group(170, "Done", None, 960, 540, 960, 540, op=0)
    sc.rect(171, "Ok bg", OK, 900, 380, 120, 120, A_GREEN, r=60)
    check(sc, 172, OK, 960, 442, 46, A_BG, 9)
    sc.text(173, "Ok txt", OK, 960, 640, "Gotowy sklep", 84, A_INK, tracking=-35, just="center")
    fade(sc, OK, BUM + 80, d_in=220)
    pop(sc, OK, BUM + 80, 600, 80)
    sc.clicks = [CM1, C1, V1, CT1, C2, V2]
    return sc


def scene_AG_b():
    sc = new("AG_b_Copy-paste", 929.95, 933.35)
    sc.apple_bg()
    w = sc.word
    COPY = [w(930.04), w(930.56), w(931.02), w(931.52)]
    PASTE = [w(930.32), w(930.80), w(931.26), w(931.82)]
    END = w(932.10)
    KEYS = sc.group(100, "Keys", None, 960, 520, 960, 520)
    allp = sorted(COPY + PASTE)
    sk = [(0, f(100), LIN)]
    for n, t in enumerate(allp):
        sk += [(t - 1, f(100 + n * 1.6), HOLD), (t + 180, f(100 + (n + 1) * 1.6), OUT)]
    sk += [(END, f(100 + 8 * 1.6), HOLD), (END + 500, f(100), APPLE)]
    scale_keys(sc, KEYS, sk)
    keycap(sc, 200, KEYS, 560, 520, 290, [(COPY[0] - 150, END - 80)], sym=True, word="command")
    keycap(sc, 300, KEYS, 960, 520, 290, [(t, t + 170) for t in COPY], letter="C")
    keycap(sc, 400, KEYS, 1360, 520, 290, [(t, t + 170) for t in PASTE], letter="V")
    cnt = sc.text(150, "Counter", None, 960, 250, "", 64, A_INK, style="Medium", family="Geist Mono", just="center")
    ck = [(0, s(""), LIN)] + [(t, s(f"×{n + 1}"), HOLD) for n, t in enumerate(allp)]
    sc.k(cnt, "textContent", ck)
    cg = [(0, col(A_INK), LIN)]
    for n, t in enumerate(allp):
        cg += [(t - 1, col(A_INK), HOLD), (t + 30, col(A_BLUE), SOFT), (t + 200, col(A_INK), SOFT)]
    sc.k(cnt, "fillColor", cg)
    hud(sc, 160, None, 960, 850, [(PASTE[-1], sc.dur - 200, "Wklejono")])
    sc.clicks = allp + [COPY[0] - 150]
    return sc


# ================================================================== AH  Screen Time while the AI generates
def scene_AH():
    sc = new("AH_Czas-przed-ekranem", 935.50, 948.50)
    sc.apple_bg()
    w = sc.word
    CZEK, PROB, SKROL, SPRZ = w(938.56), w(943.46), w(944.34), w(946.46)
    PC = sc.group(110, "Progress card", None, 960, 540, 960, 540, op=0)
    card_bg(sc, 111, PC, 520, 400, 880, 280, r=36, sh=(0.14, 60, 18))
    spinner(sc, 112, PC, 590, 470, 36, A_GREY, 0, sc.dur, width=4)
    sc.text(113, "Title", PC, 630, 482, "Generowanie strony sprzedażowej", 34, A_INK, tracking=-10)
    sc.rect(114, "Track", PC, 570, 540, 780, 12, A_LINE, r=6)
    bar = sc.rect(115, "Fill", PC, 570, 540, 18, 12, A_BLUE, r=6)
    sc.k(bar, "rectSize", [(0, v2(18, 12), LIN), (sc.dur, v2(110, 12), LIN)])
    pct = sc.text(116, "Pct", PC, 1350, 612, "2%", 24, A_GREY, style="Medium", family="Geist Mono", just="right")
    sc.k(pct, "textContent", [(0, s("2%"), LIN)] + Scene.roll_keys(0, sc.dur, lambda v: f"{int(v)}%", 2, 14.9, fps=4, ease_pow=1)[1:])
    sc.text(117, "Eta", PC, 570, 612, "Pozostało: ok. 25 min", 24, A_GREY, style="Medium")
    fade(sc, PC, 40, d_in=260)
    scale_keys(sc, PC, [(0, f(96), LIN), (40, f(96), HOLD), (700, f(100), OUT), (PROB - 100, f(100), HOLD), (PROB + 700, f(72), APPLE)])
    sc.k(PC, "positionX", [(0, f(960), LIN), (PROB - 100, f(960), HOLD), (PROB + 700, f(560), APPLE)])
    # Screen Time
    ST = sc.group(130, "Screen Time", None, 0, 0, op=0)
    card_bg(sc, 131, ST, 1000, 220, 720, 640, r=40, sh=(0.16, 70, 20))
    sc.text(132, "Head", ST, 1050, 290, "Czas przed ekranem", 28, A_GREY)
    big = sc.text(133, "Big", ST, 1050, 380, "0 min", 72, A_INK, tracking=-30)

    def fmt(v):
        v = int(round(v))
        return f"{v} min" if v < 60 else f"{v // 60} godz. {v % 60} min"
    sc.k(big, "textContent", [(0, s("0 min"), LIN)] + Scene.roll_keys(SKROL, SKROL + 1700, fmt, 0, 252)[1:])
    heights = [0.2, 0.1, 0.35, 0.6, 0.9, 0.55, 0.75, 1.0, 0.85, 0.6, 0.95, 0.7]
    for i, hgt in enumerate(heights):
        x = 1050 + i * 52
        tot = 260 * hgt
        soc = tot * 0.78
        b1 = sc.rect(140 + i * 2, "Social", ST, x, 700 - soc, 34, soc, A_BLUE, r=6, ax=17, ay=soc)
        b2 = sc.rect(141 + i * 2, "Ent", ST, x, 700 - tot, 34, tot - soc - 3, [0.35, 0.78, 0.86, 1], r=6, ax=17, ay=tot - soc - 3 + soc + 3)
        t = SKROL + i * 70
        for bb in (b1, b2):
            sc.k(bb, "scaleY", [(0, f(0), LIN), (t, f(0), HOLD), (t + 700, f(100), OUT)])
    sc.rect(170, "Axis", ST, 1050, 702, 620, 1.5, A_LINE)
    sc.rect(171, "L1", ST, 1050, 756, 16, 16, A_BLUE, r=8)
    sc.text(172, "L1t", ST, 1078, 772, "Media społecznościowe   3 godz. 20 min", 22, A_INK, style="Medium")
    sc.rect(173, "L2", ST, 1050, 796, 16, 16, [0.35, 0.78, 0.86, 1], r=8)
    sc.text(174, "L2t", ST, 1078, 812, "Rozrywka   52 min", 22, A_INK, style="Medium")
    fade(sc, ST, PROB, d_in=280)
    sc.k(ST, "positionX", [(0, f(80), LIN), (PROB, f(80), HOLD), (PROB + 700, f(0), OUT)])
    # sticky note: the next product idea
    NT = sc.group(180, "Note", None, 1560, 200, 1560, 200, op=0)
    nb = sc.rect(181, "Note bg", NT, 1370, 110, 400, 190, [1.0, 0.90, 0.45, 1], r=16)
    sc.shadow(nb, 0.16, 30, 10)
    sc.text(182, "Note h", NT, 1400, 168, "Pomysł na e-booka #2", 28, [0.35, 0.28, 0.0, 1])
    sc.text(183, "Note b1", NT, 1400, 216, "Jak nie scrollować,", 26, [0.35, 0.28, 0.0, 0.8], style="Medium")
    sc.text(184, "Note b2", NT, 1400, 252, "kiedy AI generuje", 26, [0.35, 0.28, 0.0, 0.8], style="Medium")
    sc.k(NT, "rotation", [(0, f(-4), LIN)])
    fade(sc, NT, SPRZ - 60, d_in=200)
    pop(sc, NT, SPRZ - 60, 550, 70)
    return sc


# ================================================================== AI  isometric store, floor by floor (overlay)
def scene_AI():
    sc = new("AI_Budynek-sklepu", 955.50, 972.20)
    FX = overlay(sc)
    w = sc.word
    names = ["Fundament aplikacji", "Strona sprzedażowa", "Płatności i zamówienia", "Dostawa", "Panel kupującego",
             "Dokumenty", "Ochrona danych", "Kontrola przed startem"]
    T = [w(955.80), w(960.64), w(962.68), w(964.02), w(964.48), w(967.12), w(968.76), w(969.90)]
    SUPER = w(971.72)
    OUT_ = sc.t(971.95) + 150
    CX, Y0, HW, HH_, TH, STEP = 520, 860, 250, 125, 44, 54
    BGP = sc.group(105, "Backplate", FX, 0, 0, op=0)
    bp = sc.rect(106, "Plate", BGP, 150, 240, 1180, 830, [1, 1, 1, 0.96], r=44)
    sc.shadow(bp, 0.16, 70, 20)
    fade(sc, BGP, T[0] - 350, OUT_, d_in=300)
    for i in range(8):
        y = Y0 - i * STEP
        g = sc.group(110 + i * 10, f"Floor {i+1}", FX, CX, y, CX, y, op=0)
        top = [(CX, y - HH_), (CX + HW, y), (CX, y + HH_), (CX - HW, y)]
        left = [(CX - HW, y), (CX, y + HH_), (CX, y + HH_ + TH), (CX - HW, y + TH)]
        right = [(CX, y + HH_), (CX + HW, y), (CX + HW, y + TH), (CX, y + HH_ + TH)]
        sc.path(111 + i * 10, "Left", g, left, 0, 0, fill=[0.90, 0.90, 0.93, 1], stroke=([1, 1, 1, 1], 1.5))
        sc.path(112 + i * 10, "Right", g, right, 0, 0, fill=[0.84, 0.84, 0.88, 1], stroke=([1, 1, 1, 1], 1.5))
        tp = sc.path(113 + i * 10, "Top", g, top, 0, 0, fill=A_BG, stroke=(A_LINE, 2))
        t = T[i]
        sc.k(g, "opacity", [(0, f(0), LIN), (t - 60, f(0), HOLD), (t + 160, f(100), SOFT)])
        sc.k(g, "positionY", [(0, f(y - 170), LIN), (t - 60, f(y - 170), HOLD), (t + 520, f(y), OUT)])
        tint = [0.86, 0.93, 1.0, 1]
        sc.A.append({"type": "setFxPropertyKeyframes", "compositionId": "main",
                     "property": {"layerId": tp, "propertyType": "fillColor"}, "keyframes": []}) if False else None
        # label
        lg = sc.group(200 + i * 5, "Label", FX, 0, 0, op=0)
        sc.text(201 + i * 5, "Num", lg, 820, y + 10 + TH / 2, f"{i + 1:02d}", 22, A_BLUE, style="Medium", family="Geist Mono")
        sc.text(202 + i * 5, "Name", lg, 870, y + 10 + TH / 2, names[i], 30, A_INK, tracking=-10)
        sc.rect(203 + i * 5, "Leader", lg, CX + HW + 14, y + TH / 2 - 1, 790 - CX - HW - 14, 2, A_LINE, r=1)
        sc.k(lg, "opacity", [(0, f(0), LIN), (t + 100, f(0), HOLD), (t + 350, f(100), SOFT)])
        sc.k(lg, "positionX", [(0, f(24), LIN), (t + 100, f(24), HOLD), (t + 600, f(0), OUT)])
    # finished: check on the roof
    RF = sc.group(300, "Roof check", FX, CX, Y0 - 7 * STEP - 200, CX, Y0 - 7 * STEP - 200, op=0)
    ry = Y0 - 7 * STEP - 200
    sc.rect(301, "Ok bg", RF, CX - 40, ry - 40, 80, 80, A_GREEN, r=40)
    check(sc, 302, RF, CX, ry + 2, 30, A_BG, 7)
    fade(sc, RF, SUPER - 400, d_in=200)
    pop(sc, RF, SUPER - 400, 500, 60)
    sc.k(FX, "opacity", [(0, f(100), LIN), (OUT_, f(100), HOLD), (OUT_ + 250, f(0), SOFT)])
    return sc


# ================================================================== AJ  Up Next queue (overlay)
def scene_AJ():
    sc = new("AJ_Kolejka", 993.30, 1017.25)
    FX = overlay(sc)
    w = sc.word
    IN, PASTE, QUEUE, OBIAD, KOLEJKA = w(993.54), w(995.42), w(997.42), w(1013.78), w(1015.68)
    OUT_ = sc.t(1016.95)
    DONE1 = sc.t(1004.6)
    P = sc.group(110, "Panel", FX, 1560, 540, 1560, 540, op=0)
    card_bg(sc, 111, P, 1300, 110, 520, 860, r=36, fill=[1, 1, 1, 0.97], sh=(0.18, 70, 20))
    sc.text(112, "Head", P, 1340, 172, "Kolejka", 38, A_INK, tracking=-15)
    sub = sc.text(113, "Sub", P, 1340, 206, "8 promptów", 22, A_GREY, style="Medium", op=0)
    fade(sc, sub, QUEUE)
    # now generating
    NP = sc.group(120, "Now", P, 0, 0, op=0)
    sc.rect(121, "Art", NP, 1340, 236, 76, 76, A_BLUE, r=14)
    sc.text(122, "Art n", NP, 1378, 285, "1", 32, A_BG, just="center")
    art_n = 122
    ttl = sc.text(123, "Title", NP, 1434, 266, "Fundament aplikacji", 25, A_INK)
    sc.text(124, "Sub", NP, 1434, 298, "Generuje się…", 20, A_GREY, style="Medium")
    sc.rect(125, "Track", NP, 1340, 336, 440, 6, A_LINE, r=3)
    pf = sc.rect(126, "Fill", NP, 1340, 336, 0.01, 6, A_BLUE, r=3)
    sc.k(pf, "rectSize", [(0, v2(0.01, 6), LIN), (PASTE, v2(0.01, 6), HOLD), (DONE1, v2(440, 6), LIN),
                          (DONE1 + 300, v2(0.01, 6), HOLD), (sc.dur, v2(190, 6), LIN)])
    sc.k(ttl, "textContent", [(0, s("Fundament aplikacji"), LIN), (DONE1 + 300, s("Strona sprzedażowa"), HOLD)])
    sc.k(art_n, "textContent", [(0, s("1"), LIN), (DONE1 + 300, s("2"), HOLD)])
    for i in range(3):
        b = sc.rect(127 + i, "EQ", NP, 1740 + i * 13, 244, 8, 36, A_BLUE, r=4, ax=4, ay=36)
        rng = random.Random(i)
        kk, t = [(0, f(40), LIN)], PASTE
        while t < sc.dur:
            kk.append((t, f(rng.uniform(25, 100)), INOUT)); t += rng.randint(180, 260)
        sc.k(b, "scaleY", kk)
    fade(sc, NP, PASTE - 60, d_in=240)
    sc.rect(130, "Div", P, 1340, 364, 440, 1.5, A_LINE)
    sc.text(131, "Next", P, 1340, 402, "Następne", 22, A_GREY)
    # queued prompts
    Q = sc.group(140, "Queue", P, 0, 0)
    items = ["Strona sprzedażowa", "Płatności i zamówienia", "Dostawa", "Panel kupującego", "Dokumenty", "Ochrona danych",
             "Kontrola przed startem"]
    cols = [[0.35, 0.34, 0.84, 1], A_GREEN, A_ORANGE, [0.35, 0.78, 0.86, 1], A_GREY, A_RED, [0.69, 0.32, 0.87, 1]]
    for i, name in enumerate(items):
        y = 424 + i * 66
        t = QUEUE + i * 280
        g = sc.group(150 + i * 6, name, Q, 0, 0, op=0)
        sc.rect(151 + i * 6, "Art", g, 1340, y, 52, 52, cols[i], r=11)
        sc.text(152 + i * 6, "N", g, 1366, y + 35, str(i + 2), 24, A_BG, just="center")
        sc.text(153 + i * 6, "Title", g, 1408, y + 24, name, 22, A_INK)
        sc.text(154 + i * 6, "Sub", g, 1408, y + 48, "W kolejce", 18, A_GREY, style="Medium")
        ok = [(0, f(0), LIN), (t - 60, f(0), HOLD), (t + 180, f(100), SOFT)]
        if i == 0:
            ok += [(DONE1, f(100), HOLD), (DONE1 + 250, f(0), SOFT)]
        sc.k(g, "opacity", ok)
        sc.k(g, "positionX", [(0, f(30), LIN), (t - 60, f(30), HOLD), (t + 450, f(0), OUT)])
    sc.k(Q, "positionY", [(0, f(0), LIN), (DONE1 + 100, f(0), HOLD), (DONE1 + 600, f(-66), APPLE)])
    # …and lunch joins the queue
    y = 424 + 7 * 66
    g = sc.group(200, "Obiad", Q, 0, 0, op=0)
    sc.rect(201, "Art", g, 1340, y, 52, 52, A_ORANGE, r=11)
    for k in range(3):
        sc.rect(202 + k, "Tine", g, 1352 + k * 5, y + 11, 2.5, 12, A_BG, r=1.2)
    sc.rect(205, "Fork", g, 1355.5, y + 22, 4, 20, A_BG, r=2)
    sc.rect(206, "Knife", g, 1378, y + 11, 6, 31, A_BG, r=3)
    sc.text(207, "Title", g, 1408, y + 24, "Obiad", 22, A_INK)
    sc.text(208, "Sub", g, 1408, y + 48, "Ty · ok. 30 min", 18, A_ORANGE, style="Medium")
    sc.k(g, "opacity", [(0, f(0), LIN), (OBIAD - 60, f(0), HOLD), (OBIAD + 200, f(100), SOFT)])
    sc.k(g, "positionX", [(0, f(30), LIN), (OBIAD - 60, f(30), HOLD), (OBIAD + 500, f(0), OUT)])
    sc.k(P, "opacity", [(0, f(0), LIN), (IN, f(0), HOLD), (IN + 280, f(100), SOFT), (OUT_, f(100), HOLD), (OUT_ + 280, f(0), SOFT)])
    scale_keys(sc, P, [(0, f(95), LIN), (IN, f(95), HOLD), (IN + 700, f(100), OUT), (KOLEJKA, f(100), HOLD),
                       (KOLEJKA + 150, f(102), OUT), (KOLEJKA + 500, f(100), APPLE)])
    return sc


# ================================================================== AK  scale: "saved 7 minutes" vs …
def scene_AK():
    sc = new("AK_7-minut", 1021.40, 1028.60)
    sc.apple_bg()
    w = sc.word
    MAIL, OBR, OSZ, DLA = w(1023.42), w(1024.96), w(1026.08), w(1027.46)

    def tile(base, cx, t, label):
        g = sc.group(base, label, None, cx, 520, cx, 520, op=0)
        c = sc.rect(base + 1, "Tile", g, cx - 95, 425, 190, 190, A_BG, r=44)
        sc.shadow(c, 0.12, 40, 14)
        sc.text(base + 2, "Label", g, cx, 690, label, 30, A_GREY, style="Medium", just="center")
        fade(sc, g, t - 60, d_in=220)
        pop(sc, g, t - 60, 550, 80)
        sc.k(g, "positionX", [(0, f(cx), LIN), (OSZ - 60, f(cx), HOLD), (OSZ + 500, f(960), APPLE)])
        return g
    m = tile(110, 820, MAIL, "Mail")
    sc.path(120, "Env", m, [(770, 488), (870, 488), (870, 556), (770, 556)], 0, 0, stroke=(A_BLUE, 6))
    sc.path(121, "Flap", m, [(772, 490), (820, 528), (868, 490)], 0, 0, stroke=(A_BLUE, 6), closed=False)
    im = tile(130, 1100, OBR, "Obrazek")
    sc.path(140, "Frame", im, [(1050, 480), (1150, 480), (1150, 560), (1050, 560)], 0, 0, stroke=(A_ORANGE, 6))
    sc.path(141, "Hill", im, [(1052, 556), (1085, 516), (1108, 540), (1122, 526), (1148, 556)], 0, 0, stroke=(A_ORANGE, 5), closed=False)
    sc.rect(142, "Sun", im, 1118, 492, 16, 16, A_ORANGE, r=8)
    for g in (m, im):
        sc.k(g, "opacity", [(0, f(0), LIN), ((MAIL if g == m else OBR) - 60, f(0), HOLD), ((MAIL if g == m else OBR) + 160, f(100), SOFT),
                            (OSZ + 100, f(100), HOLD), (OSZ + 450, f(0), SOFT)])
        scale_keys(sc, g, [(0, f(80), LIN), ((MAIL if g == m else OBR) - 60, f(80), HOLD), ((MAIL if g == m else OBR) + 490, f(100), APPLE),
                           (OSZ - 60, f(100), HOLD), (OSZ + 500, f(12), APPLE)])
    # the saving: a tiny dot
    DOT = sc.group(150, "Dot", None, 960, 520, 960, 520, op=0)
    sc.rect(151, "Dot", DOT, 942, 502, 36, 36, A_BLUE, r=18)
    lab = sc.text(152, "Minus", DOT, 960, 640, "−7 min", 64, A_INK, tracking=-25, just="center")
    fade(sc, DOT, OSZ + 300, d_in=200)
    scale_keys(sc, DOT, [(0, f(100), LIN), (DLA - 60, f(100), HOLD), (DLA + 900, f(40), APPLE)])
    sc.k(lab, "opacity", [(0, f(100), LIN), (DLA - 60, f(100), HOLD), (DLA + 250, f(0), SOFT)])
    ring = sc.ring(160, "Big ring", None, 960, 540, 1500, A_LINE, 5, trim_end=0)
    sc.k(ring, "trimEnd", [(0, f(0), LIN), (DLA, f(0), HOLD), (sc.dur, f(100), INOUT)])
    return sc


# ================================================================== AL  org chart collapses into "Ty + AI"
def scene_AL():
    sc = new("AL_Zespol", 1028.60, 1036.40)
    sc.apple_bg()
    w = sc.word
    PROG, DES, PIEN, ZES, MOZE, BIZ, SAM = w(1029.62), w(1030.60), w(1031.42), w(1032.10), w(1033.96), w(1035.28), w(1035.66)
    # the big ring from AK shrinks into the top node
    NODE = sc.group(110, "Top node", None, 960, 540, 960, 540)
    ring = sc.ring(111, "Ring", NODE, 960, 540, 1500, A_LINE, 5)
    scale_keys(sc, NODE, [(0, f(100), LIN), (700, f(11), APPLE)])
    sc.k(NODE, "positionY", [(0, f(540), LIN), (700, f(230), APPLE)])
    sc.k(ring, "strokeWidth", [(0, f(5), LIN), (700, f(28), APPLE)]) if False else None
    nl = sc.text(112, "Node label", None, 960, 243, "Biznes", 30, A_INK, just="center", op=0)
    fade(sc, nl, 500, d_in=220)
    nodec = sc.rect(113, "Node fill", None, 960 - 82, 230 - 82, 164, 164, [1, 1, 1, 0], r=82, stroke=([1, 1, 1, 0], 4))
    sc.k(nodec, "strokeColor", [(0, col([1, 1, 1, 0]), LIN), (BIZ, col([1, 1, 1, 0]), HOLD), (BIZ + 250, col(A_GREEN), SOFT)])
    xs = [480, 720, 960, 1200, 1440]
    roles = ["Programista", "Designer", "Copywriter", "Marketing", "Project manager"]
    ts = [PROG, DES, ZES, sc.t(1032.50), sc.t(1032.98)]
    trunk = sc.rect(120, "Trunk", None, 958.5, 314, 3, 0.01, A_LINE)
    sc.k(trunk, "rectSize", [(0, v2(3, 0.01), LIN), (PROG - 300, v2(3, 0.01), HOLD), (PROG, v2(3, 106), OUT)])
    bar = sc.rect(121, "Bar", None, 960, 419, 0.01, 3, A_LINE, ax=0)
    sc.kpos(bar, [(0, 960, 419, LIN), (PROG - 100, 960, 419, HOLD), (PROG + 400, 480, 419, OUT)])
    sc.k(bar, "rectSize", [(0, v2(0.01, 3), LIN), (PROG - 100, v2(0.01, 3), HOLD), (PROG + 400, v2(963, 3), OUT)])
    for lid in (trunk, bar):
        sc.k(lid, "opacity", [(0, f(100), LIN), (MOZE, f(100), HOLD), (MOZE + 300, f(0), SOFT)])
    for i, (x, role, t) in enumerate(zip(xs, roles, ts)):
        g = sc.group(130 + i * 8, role, None, x, 560, x, 560, op=0)
        sc.rect(131 + i * 8, "Drop", g, x - 1.5, 420, 3, 80, A_LINE)
        sc.rect(132 + i * 8, "Av", g, x - 60, 500, 120, 120, A_FILL, r=60)
        sc.rect(133 + i * 8, "Head", g, x - 18, 526, 36, 36, A_GREY, r=18)
        sc.path(134 + i * 8, "Body", g, arc(x, 608, 32, 180, 360, 18), 0, 0, fill=A_GREY)
        sc.text(135 + i * 8, "Role", g, x, 670, role, 26, A_INK, style="Medium", just="center")
        sc.k(g, "opacity", [(0, f(0), LIN), (t - 60, f(0), HOLD), (t + 200, f(100), SOFT), (MOZE + 150, f(100), HOLD), (MOZE + 550, f(0), SOFT)])
        sc.k(g, "positionX", [(0, f(x), LIN), (MOZE, f(x), HOLD), (MOZE + 600, f(960), APPLE)])
        scale_keys(sc, g, [(0, f(80), LIN), (t - 60, f(80), HOLD), (t + 500, f(100), APPLE), (MOZE, f(100), HOLD), (MOZE + 600, f(60), APPLE)])
    # price of the team
    PR = sc.group(170, "Price", None, 960, 800, 960, 800, op=0)
    pw = pill_text(sc, 171, PR, 960, 800, "Koszt budowy: 5 000–10 000 zł", 32, A_INK, A_FILL)
    st = sc.rect(173, "Strike", PR, 960 - pw / 2 + 20, 799, 0.01, 4, A_RED, r=2)
    sc.k(st, "rectSize", [(0, v2(0.01, 4), LIN), (MOZE, v2(0.01, 4), HOLD), (MOZE + 400, v2(pw - 40, 4), APPLE)])
    sc.k(PR, "opacity", [(0, f(0), LIN), (PIEN - 60, f(0), HOLD), (PIEN + 200, f(100), SOFT), (MOZE + 600, f(100), HOLD), (MOZE + 900, f(0), SOFT)])
    pop(sc, PR, PIEN - 60, 500, 90)
    # one person + AI
    YOU = sc.group(180, "You", None, 960, 560, 960, 560, op=0)
    sc.rect(181, "Av", YOU, 900, 500, 120, 120, A_BLUE, r=60)
    sc.rect(182, "Head", YOU, 942, 526, 36, 36, A_BG, r=18)
    sc.path(183, "Body", YOU, arc(960, 608, 32, 180, 360, 18), 0, 0, fill=A_BG)
    sc.text(184, "Label", YOU, 960, 690, "Ty + AI", 44, A_INK, tracking=-15, just="center")
    fade(sc, YOU, MOZE + 450, d_in=220)
    scale_keys(sc, YOU, [(0, f(70), LIN), (MOZE + 450, f(70), HOLD), (MOZE + 1000, f(115), APPLE),
                         (SAM - 60, f(115), HOLD), (SAM + 150, f(125), OUT), (SAM + 500, f(115), APPLE)])
    ok = sc.group(190, "Node ok", None, 1030, 170, 1030, 170, op=0)
    sc.rect(191, "Ok bg", ok, 1012, 152, 36, 36, A_GREEN, r=18)
    check(sc, 192, ok, 1030, 171, 13, A_BG, 3)
    fade(sc, ok, BIZ + 100, d_in=160)
    pop(sc, ok, BIZ + 100, 400, 50)
    return sc


# ================================================================== AM  iOS alert: the real choice
def scene_AM():
    sc = new("AM_Wybor", 1053.80, 1065.35)
    sc.bg = [0.80, 0.80, 0.83, 1]
    rng = random.Random(8)
    cols = [A_BLUE, A_GREEN, A_ORANGE, A_RED, [0.69, 0.32, 0.87, 1], [0.35, 0.78, 0.86, 1]]
    for i in range(24):
        cx, cy = 360 + (i % 6) * 240, 150 + (i // 6) * 250
        sc.layers.insert(0, {"type": "Rect", "id": 20 + i, "name": "App", "blendMode": "normal",
                             "activeRange": {"start": 0, "duration": sc.dur}, "transform": tf(cx - 70, cy - 70),
                             "rect": {"size": [140, 140], "fillColor": a(rng.choice(cols), 0.55), "roundness": 32},
                             "effects": [{"id": 7500 + i, "effect": {"type": "gaussianBlur", "blurriness": 36}}]})
    sc.layers.insert(0, {"type": "Rect", "id": 60, "name": "Dim", "blendMode": "normal",
                         "activeRange": {"start": 0, "duration": sc.dur}, "transform": tf(),
                         "rect": {"size": [W, H], "fillColor": [0, 0, 0, 0.22]}})
    w = sc.word
    POCZ, WYB, AI2, NIEZ, OGR = w(1054.18), w(1060.24), w(1060.76), w(1061.88), w(1064.62)
    SHAKE = sc.t(1059.90)
    AL = sc.group(100, "Alert", None, 960, 530, 960, 530, op=0)
    box = sc.rect(101, "Box", AL, 650, 370, 620, 330, [0.97, 0.97, 0.98, 0.97], r=36)
    sc.shadow(box, 0.25, 60, 20)
    sc.text(102, "Title", AL, 960, 446, "Jak zaczynasz?", 38, A_INK, just="center")
    msg = sc.text(103, "Msg", AL, 960, 492, "Wybór, który masz w głowie", 26, A_GREY, style="Medium", just="center")
    sc.k(msg, "textContent", [(0, s("Wybór, który masz w głowie"), LIN), (WYB, s("Wybór, który masz naprawdę"), HOLD)])
    sc.rect(104, "Hair1", AL, 650, 540, 620, 1.5, A_LINE)
    sc.rect(105, "Hair2", AL, 650, 620, 620, 1.5, A_LINE)
    press = sc.rect(106, "Press", AL, 650, 541, 620, 79, [0, 0, 0, 0.07], op=0)
    b1 = sc.text(107, "Btn1", AL, 960, 592, "Zatrudnij seniora", 32, A_BLUE, style="Medium", just="center")
    b2 = sc.text(108, "Btn2", AL, 960, 672, "Użyj AI", 32, A_BLUE, style="Medium", just="center")
    sc.k(b1, "textContent", [(0, s("Zatrudnij seniora"), LIN), (WYB, s(""), HOLD), (AI2, s("Użyj AI"), HOLD)])
    sc.k(b1, "fillColor", [(0, col(A_BLUE), LIN), (SHAKE - 400, col(A_BLUE), HOLD), (SHAKE - 100, col(A_GREY), SOFT), (WYB, col(A_BLUE), HOLD)])
    sc.k(b2, "textContent", [(0, s("Użyj AI"), LIN), (WYB, s(""), HOLD), (NIEZ, s("Nie zaczynaj"), HOLD)])
    sc.k(b2, "fillColor", [(0, col(A_BLUE), LIN), (WYB, col(A_RED), HOLD)])
    sc.k(press, "opacity", [(0, f(0), LIN), (OGR, f(0), HOLD), (OGR + 80, f(100), SOFT), (OGR + 320, f(100), HOLD), (OGR + 450, f(0), SOFT)])
    sc.k(AL, "opacity", [(0, f(0), LIN), (POCZ - 100, f(0), HOLD), (POCZ + 120, f(100), SOFT), (OGR + 450, f(100), HOLD), (OGR + 700, f(0), SOFT)])
    scale_keys(sc, AL, [(0, f(118), LIN), (POCZ - 100, f(118), HOLD), (POCZ + 450, f(100), APPLE), (OGR + 450, f(100), HOLD), (OGR + 700, f(94), SOFT)])
    # passcode-style shake on the false choice, then a small pulse for the real one
    sk = [(0, f(960), LIN), (SHAKE - 1, f(960), HOLD)]
    for n, dx in enumerate([-26, 22, -16, 10, -5, 0]):
        sk.append((SHAKE + (n + 1) * 60, f(960 + dx), SOFT))
    sc.k(AL, "positionX", sk)
    return sc


# ================================================================== AN  receipt: 10 000 zł → 0,00 zł
def scene_AN():
    sc = new("AN_Paragon", 1081.20, 1087.75)
    sc.apple_bg()
    w = sc.word
    KURS, DZIES, SYS, WSZ, DARMO, PLAT = w(1081.66), w(1082.66), w(1083.88), w(1084.80), w(1085.42), w(1086.22)
    R = sc.group(100, "Receipt", None, 960, 540, 960, 540, op=0)
    X0, X1, Y0, Y1 = 690, 1230, 150, 900
    paper = sc.rect(101, "Paper", R, X0, Y0, X1 - X0, Y1 - Y0, A_BG, r=10)
    sc.shadow(paper, 0.14, 50, 18)
    teeth = [(X0, Y1 - 2)]
    n = 18
    for i in range(n):
        teeth += [(X0 + (i + 0.5) * (X1 - X0) / n, Y1 + 18), (X0 + (i + 1) * (X1 - X0) / n, Y1 - 2)]
    sc.path(102, "Teeth", R, teeth + [(X1, Y1 - 10), (X0, Y1 - 10)], 0, 0, fill=A_BG)
    sc.text(103, "Kicker", R, 960, 222, "PARAGON", 20, A_GREY, style="Medium", family="Geist Mono", just="center", tracking=200)
    sc.text(104, "Title", R, 960, 276, "Twój dostęp", 40, A_INK, tracking=-15, just="center")

    def dashes(lid, y):
        for i in range(24):
            sc.rect(lid + i, "Dash", R, X0 + 40 + i * 19.5, y, 10, 2, A_LINE)
    dashes(110, 318)
    rows = [("Kurs", KURS), ("Mentoring", sc.t(1081.95)), ("Rozmowy coachingowe", sc.t(1082.25)), ("System AI", SYS)]
    for i, (lab, t) in enumerate(rows):
        y = 380 + i * 52
        g = sc.group(140 + i * 3, lab, R, 0, 0, op=0)
        sc.text(141 + i * 3, "L", g, X0 + 40, y, lab, 28, A_INK, style="Medium")
        sc.text(142 + i * 3, "R", g, X1 - 40, y, "w cenie", 26, A_GREY, style="Medium", just="right")
        sc.k(g, "opacity", [(0, f(0), LIN), (t - 60, f(0), HOLD), (t + 180, f(100), SOFT)])
        sc.k(g, "positionY", [(0, f(-12), LIN), (t - 60, f(-12), HOLD), (t + 400, f(0), OUT)])
    dashes(160, 596)
    zl = lambda v: f"{int(round(v)):,}".replace(",", " ") + ",00 zł"
    wg = sc.group(190, "Value", R, 0, 0, op=0)
    sc.text(191, "L", wg, X0 + 40, 650, "Wartość", 28, A_INK, style="Medium")
    val = sc.text(192, "R", wg, X1 - 40, 650, zl(0), 28, A_INK, style="Medium", just="right")
    sc.k(val, "textContent", [(0, s(zl(0)), LIN)] + Scene.roll_keys(DZIES, DZIES + 600, zl, 0, 10000)[1:])
    fade(sc, wg, DZIES - 80, d_in=180)
    sg = sc.group(200, "Sponsor", R, 0, 0, op=0)
    sc.text(201, "L", sg, X0 + 40, 706, "Sfinansowane przez Base44", 28, A_GREEN, style="Medium")
    sc.text(202, "R", sg, X1 - 40, 706, "−10 000,00 zł", 28, A_GREEN, style="Medium", just="right")
    sc.k(sg, "opacity", [(0, f(0), LIN), (WSZ - 60, f(0), HOLD), (WSZ + 200, f(100), SOFT)])
    sc.k(sg, "positionX", [(0, f(-20), LIN), (WSZ - 60, f(-20), HOLD), (WSZ + 500, f(0), OUT)])
    dashes(210, 748)
    tg = sc.group(240, "Total", R, 0, 0, op=0)
    sc.text(241, "L", tg, X0 + 40, 826, "Do zapłaty", 38, A_INK, tracking=-10)
    tot = sc.text(242, "R", tg, X1 - 40, 826, zl(0), 38, A_INK, tracking=-10, just="right")
    sc.k(tot, "textContent", [(0, s(zl(0)), LIN)] + Scene.roll_keys(DZIES, DZIES + 600, zl, 0, 10000)[1:] +
         Scene.roll_keys(DARMO, DARMO + 700, zl, 10000, 0)[1:])
    sc.k(tot, "fillColor", [(0, col(A_INK), LIN), (DARMO + 500, col(A_INK), HOLD), (DARMO + 700, col(A_GREEN), SOFT)])
    fade(sc, tg, DZIES - 80, d_in=180)
    # stamp
    STP = sc.group(250, "Stamp", R, 1090, 470, 1090, 470, op=0)
    sc.rect(251, "Stamp box", STP, 950, 430, 280, 80, [1, 1, 1, 0], r=14, stroke=(A_GREEN, 5))
    sc.text(252, "Stamp txt", STP, 1090, 484, "OPŁACONE", 38, A_GREEN, just="center", tracking=80)
    sc.k(STP, "rotation", [(0, f(-9), LIN)])
    sc.k(STP, "opacity", [(0, f(0), LIN), (PLAT - 60, f(0), HOLD), (PLAT + 80, f(90), SOFT)])
    scale_keys(sc, STP, [(0, f(150), LIN), (PLAT - 60, f(150), HOLD), (PLAT + 200, f(100), IN)])
    fade(sc, R, 40, d_in=240)
    sc.k(R, "positionY", [(0, f(580), LIN), (40, f(580), HOLD), (800, f(540), OUT)])
    return sc


# ================================================================== AO  Wallet boarding pass → New York (overlay)
def scene_AO():
    sc = new("AO_Nowy-Jork", 1092.40, 1095.70)
    FX = overlay(sc)
    w = sc.word
    BYL, PODP, DEAL = w(1092.80), w(1093.78), w(1094.82)
    OUT_ = sc.t(1095.35)
    X0, Y0, PW, PH = 1180, 80, 660, 320
    P = sc.group(110, "Pass", FX, X0 + PW / 2, Y0 + PH / 2, X0 + PW / 2, Y0 + PH / 2, op=0)
    card_bg(sc, 111, P, X0, Y0, PW, PH, r=30, fill=[0.07, 0.09, 0.16, 1], sh=(0.3, 60, 20))
    WH = A_BG
    sc.text(112, "Kicker", P, X0 + 40, Y0 + 58, "KARTA POKŁADOWA", 18, [1, 1, 1, 0.55], style="Medium", family="Geist Mono", tracking=120)
    sc.text(113, "From", P, X0 + 40, Y0 + 148, "Floryda", 46, WH, tracking=-15)
    sc.text(114, "To", P, X0 + PW - 40, Y0 + 148, "Nowy Jork", 46, WH, tracking=-15, just="right")
    lx0, lx1 = X0 + 40 + adv("Floryda", 46, "SemiBold") + 26, X0 + PW - 40 - adv("Nowy Jork", 46, "SemiBold") - 26
    for i in range(int((lx1 - lx0) / 14)):
        sc.rect(120 + i, "Dash", P, lx0 + i * 14, Y0 + 132, 7, 3, [1, 1, 1, 0.35], r=1.5)
    PL = sc.group(160, "Plane", P, lx0, Y0 + 133, lx0, Y0 + 133)
    sc.path(161, "Plane", PL, [(lx0 + 14, Y0 + 133), (lx0 - 8, Y0 + 122), (lx0 - 4, Y0 + 133), (lx0 - 8, Y0 + 144)], 0, 0, fill=WH)
    sc.k(PL, "positionX", [(0, f(lx0), LIN), (BYL + 100, f(lx0), HOLD), (DEAL, f(lx1), INOUT)])
    for i in range(30):
        sc.rect(170 + i, "Perf", P, X0 + 30 + i * 20.5, Y0 + 196, 10, 2, [1, 1, 1, 0.25], r=1)
    sc.text(210, "Cel k", P, X0 + 40, Y0 + 244, "CEL", 16, [1, 1, 1, 0.5], style="Medium", family="Geist Mono", tracking=120)
    sc.text(211, "Cel", P, X0 + 40, Y0 + 284, "Podpisanie współpracy", 32, WH, tracking=-10)
    OK = sc.group(220, "Signed", P, X0 + PW - 110, Y0 + 262, X0 + PW - 110, Y0 + 262, op=0)
    sc.rect(221, "Ok bg", OK, X0 + PW - 190, Y0 + 240, 160, 44, A_GREEN, r=22)
    check(sc, 222, OK, X0 + PW - 164, Y0 + 262, 11, WH, 3)
    sc.text(223, "Ok txt", OK, X0 + PW - 146, Y0 + 270, "Podpisane", 20, WH)
    fade(sc, OK, DEAL - 60, d_in=160)
    pop(sc, OK, DEAL - 60, 420, 60)
    sc.k(P, "opacity", [(0, f(0), LIN), (BYL - 150, f(0), HOLD), (BYL + 100, f(100), SOFT), (OUT_, f(100), HOLD), (OUT_ + 250, f(0), SOFT)])
    sc.k(P, "positionX", [(0, f(X0 + PW / 2 + 120), LIN), (BYL - 150, f(X0 + PW / 2 + 120), HOLD), (BYL + 550, f(X0 + PW / 2), OUT),
                          (OUT_, f(X0 + PW / 2), HOLD), (OUT_ + 300, f(X0 + PW / 2 + 60), SOFT)])
    sc.k(P, "rotation", [(0, f(4), LIN), (BYL - 150, f(4), HOLD), (BYL + 600, f(0), OUT)])
    return sc


BUILD = {"V": scene_V, "W": scene_W, "X": scene_X, "Y": scene_Y, "Z": scene_Z, "AA": scene_AA, "AB": scene_AB,
         "AC": scene_AC, "AD": scene_AD, "AE": scene_AE, "AF": scene_AF, "AG_a": scene_AG_a, "AG_b": scene_AG_b,
         "AH": scene_AH, "AI": scene_AI, "AJ": scene_AJ, "AK": scene_AK, "AL": scene_AL, "AM": scene_AM,
         "AN": scene_AN, "AO": scene_AO}
OVERLAY.update({"X", "AA", "AC", "AD", "AF", "AI", "AJ", "AO"})

if __name__ == "__main__":
    import json
    for key in (sys.argv[1:] or BUILD):
        try:
            sc = BUILD[key]()
            sc.build(key)
            if hasattr(sc, "clicks"):
                json.dump([t / 1000 for t in sc.clicks], open(os.path.join(WORK, f"{key}_clicks.json"), "w"))
        except SystemExit as e:
            print(f"[{key}] FAILED: {e}")
