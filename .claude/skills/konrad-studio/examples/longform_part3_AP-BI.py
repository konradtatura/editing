#!/usr/bin/env python3
"""Part 3, batch 2: AP–BI (18:24–26:31) on halfraw.mp4. Each its own Apple metaphor:
AP World Clock day/night → 24/7 · AQ description panel, first link tapped (a + b) · AR 3D cover turn + sheen ·
AS Maps place card (key lime pie) · AT balance card: 1 000 000 zł shakes → "kilka tysięcy" · AU Reminders swipe →
"Część 2?" · AV order bump checkout (a), post-purchase dashboard upsell (b), price ladder (c) · AW headline typography ·
AX 2025 → 2026 · AY store ⇄ payments connect · AZ Face ID owner vs buyer · BA live visitors: 0 · BB restaurant in a forest ·
BC organic vs paid split (a), budget dial (b), reach roulette vs volume grid (c) · BD cost → investment card flip ·
BE four ad angles dealt like cards · BF feed flies past your ad · BG funnel pipeline (overlay) · BH Focus mode ·
BI appearance light/dark + Night Shift when the red glasses go on.
Usage: scenes_ap.py AP AQ_a ...   (no args = all)."""
import sys, math, random
from scenes_af import adv
from scenes_af2 import check, spinner, fade
from scenes_gk import pop
from scenes_lu import card_bg, rise_group
from scenes_vo import new, overlay, arc, blur, scale_keys, pill_text, blob, OVERLAY as _OV
from ds import *

OVERLAY = set()
PURPLE = [0.69, 0.32, 0.87, 1]
TEAL = [0.35, 0.78, 0.86, 1]
DARK = [0.08, 0.08, 0.09, 1]


def zl(v):
    return f"{int(round(v)):,}".replace(",", " ") + " zł"


def ok_badge(sc, base, parent, cx, cy, t, d=36, color=A_GREEN):
    g = sc.group(base, "Ok", parent, cx, cy, cx, cy, op=0)
    sc.rect(base + 1, "Ok bg", g, cx - d / 2, cy - d / 2, d, d, color, r=d / 2)
    check(sc, base + 2, g, cx, cy + 1, d * 0.36, A_BG, max(2.5, d / 12))
    fade(sc, g, t, d_in=160)
    pop(sc, g, t, 420, 50)
    return g


def card_in(sc, g, t_in, t_out, dy=30, sc0=96):
    """Opacity + scale-in (group anchored at its centre) and fade-out."""
    sc.k(g, "opacity", [(0, f(0), LIN), (t_in, f(0), HOLD), (t_in + 260, f(100), SOFT), (t_out, f(100), HOLD), (t_out + 260, f(0), SOFT)])
    scale_keys(sc, g, [(0, f(sc0), LIN), (t_in, f(sc0), HOLD), (t_in + 700, f(100), OUT)])


# ================================================================== AP  World Clock → 24/7 (overlay)
def scene_AP():
    sc = new("AP_Strefy-czasowe", 1111.50, 1117.70)
    FX = overlay(sc)
    w = sc.word
    JA, POL, ZGR, DOBE = w(1111.84), w(1113.26), w(1115.40), w(1115.94)
    END = sc.t(1117.35)
    C = sc.group(110, "Card", FX, 1510, 275, 1510, 275, op=0)
    card_bg(sc, 111, C, 1180, 80, 660, 390, r=38, sh=(0.18, 60, 18))
    card_in(sc, C, JA - 150, END)

    def clock(base, cx, cy, dark, hour, city, time_txt, t_in):
        g = sc.group(base, city, C, cx, cy, cx, cy, op=0)
        face = [0.11, 0.11, 0.13, 1] if dark else A_BG
        ink = A_BG if dark else A_INK
        sc.rect(base + 1, "Face", g, cx - 90, cy - 90, 180, 180, face, r=90, stroke=(A_LINE, 2))
        for i in range(12):
            a_ = math.radians(i * 30 - 90)
            r0, r1 = (62, 80) if i % 3 == 0 else (70, 80)
            sc.path(base + 2 + i, "Tick", g, [(cx + r0 * math.cos(a_), cy + r0 * math.sin(a_)),
                                             (cx + r1 * math.cos(a_), cy + r1 * math.sin(a_))], 0, 0,
                    stroke=(a(ink, 0.8 if i % 3 == 0 else 0.35), 3 if i % 3 == 0 else 2), closed=False)
        hh = sc.rect(base + 20, "Hour", g, cx - 3.5, cy - 44, 7, 50, ink, r=3.5, ax=3.5, ay=44)
        mm = sc.rect(base + 21, "Min", g, cx - 2.5, cy - 66, 5, 72, ink, r=2.5, ax=2.5, ay=66)
        sc.rect(base + 22, "Pin", g, cx - 6, cy - 6, 12, 12, A_ORANGE, r=6)
        h0 = (hour % 12) * 30
        sc.k(hh, "rotation", [(0, f(h0), LIN), (ZGR, f(h0), HOLD), (ZGR + 1500, f(h0 + 60), INOUT)])
        sc.k(mm, "rotation", [(0, f(0), LIN), (ZGR, f(0), HOLD), (ZGR + 1500, f(720), INOUT)])
        sc.text(base + 23, "City", C, cx, cy + 142, city, 28, A_INK, just="center", op=0)
        tt = sc.text(base + 24, "Time", C, cx, cy + 176, time_txt, 22, A_GREY, style="Medium", family="Geist Mono", just="center", op=0)
        for lid in (g, base + 23, base + 24):
            sc.k(lid, "opacity", [(0, f(0), LIN), (t_in, f(0), HOLD), (t_in + 240, f(100), SOFT)])
        pop(sc, g, t_in, 550, 80)
        return tt
    tf_ = clock(120, 1350, 200, False, 16, "Floryda", "16:00", JA)
    tp_ = clock(150, 1670, 200, True, 22, "Polska", "22:00", POL)
    sc.k(tf_, "textContent", [(0, s("16:00"), LIN), (ZGR + 1500, s("18:00"), HOLD)])
    sc.k(tp_, "textContent", [(0, s("22:00"), LIN), (ZGR + 1500, s("00:00"), HOLD)])
    pg = sc.group(180, "247", C, 1510, 432, 1510, 432, op=0)
    sc.rect(181, "Pill", pg, 1390, 408, 240, 48, a(A_GREEN, 0.14), r=24)
    sc.rect(182, "Live", pg, 1412, 426, 12, 12, A_GREEN, r=6)
    sc.text(183, "Txt", pg, 1524, 441, "online 24 h / dobę", 22, [0.1, 0.5, 0.2, 1], just="center")
    fade(sc, pg, DOBE, d_in=200)
    pop(sc, pg, DOBE, 450, 70)
    return sc


# ================================================================== AQ  description panel: first link (overlay)
def link_scene(name, a0, a1, t_tap_s, t_in_s):
    sc = new(name, a0, a1)
    FX = overlay(sc)
    TAP, T0, END = sc.t(t_tap_s), sc.t(t_in_s), sc.t(a1) - 320
    P = sc.group(110, "Panel", FX, 960, 900, 960, 900, op=0)
    card_bg(sc, 111, P, 520, 770, 880, 260, r=34, sh=(0.2, 60, 18))
    sc.text(112, "Head", P, 560, 822, "Opis", 24, A_GREY)
    row = sc.rect(113, "Row", P, 548, 842, 824, 70, a(A_BLUE, 0.0), r=18)
    sc.rect(114, "Num", P, 566, 856, 42, 42, A_BLUE, r=12)
    sc.text(115, "Num t", P, 587, 886, "1", 24, A_BG, just="center")
    sc.text(116, "Link", P, 628, 888, "Darmowy kurs + cały system AI  →", 32, A_BLUE, tracking=-10)
    sc.rect(117, "L2", P, 566, 940, 560, 12, A_LINE, r=6)
    sc.rect(118, "L3", P, 566, 968, 420, 12, A_LINE, r=6)
    sc.k(row, "fillColor", [(0, col(a(A_BLUE, 0.0)), LIN), (TAP, col(a(A_BLUE, 0.0)), HOLD), (TAP + 120, col(a(A_BLUE, 0.12)), SOFT)])
    sc.k(P, "opacity", [(0, f(0), LIN), (T0, f(0), HOLD), (T0 + 220, f(100), SOFT), (END, f(100), HOLD), (END + 250, f(0), SOFT)])
    sc.k(P, "positionY", [(0, f(990), LIN), (T0, f(990), HOLD), (T0 + 600, f(900), OUT), (END, f(900), HOLD), (END + 300, f(950), SOFT)])
    # cursor glides to the link and taps
    CU = sc.group(130, "Cursor", P, 1300, 1000, 1000, 880, op=0)
    arrow = [(0, 0), (0, 34), (9, 26), (15, 40), (21, 37), (15, 24), (26, 24)]
    sc.path(131, "Cursor", CU, arrow, 1000, 880, fill=A_INK, stroke=(A_BG, 2.5))
    sc.k(CU, "opacity", [(0, f(0), LIN), (T0 + 200, f(0), HOLD), (T0 + 400, f(100), SOFT)])
    sc.kpos(CU, [(0, 1300, 1010, LIN), (T0 + 200, 1300, 1010, HOLD), (TAP - 60, 980, 872, APPLE)])
    scale_keys(sc, CU, [(0, f(100), LIN), (TAP - 60, f(100), HOLD), (TAP + 20, f(84), OUT), (TAP + 220, f(100), APPLE)])
    rp = sc.rect(140, "Ripple", P, 950, 842, 60, 60, [1, 1, 1, 0], r=30, stroke=(A_BLUE, 3), ax=30, ay=30, op=0)
    sc.k(rp, "opacity", [(0, f(0), LIN), (TAP, f(0), HOLD), (TAP + 60, f(100), SOFT), (TAP + 500, f(0), SOFT)])
    scale_keys(sc, rp, [(0, f(40), LIN), (TAP, f(40), HOLD), (TAP + 500, f(220), OUT)])
    return sc


def scene_AQ_a():
    return link_scene("AQ_a_Pierwszy-link", 1104.60, 1107.00, 1105.40, 1104.80)


def scene_AQ_b():
    return link_scene("AQ_b_Pierwszy-link", 1118.90, 1120.95, 1119.84, 1119.10)


# ================================================================== AR  cover turns in 3D + sheen (overlay)
def scene_AR():
    sc = new("AR_Okladka", 1158.70, 1162.10)
    FX = overlay(sc)
    w = sc.word
    O, BUM, PIEK = w(1159.40), w(1159.68), w(1159.94)
    END = sc.t(1161.80)
    CX, CY = 1450, 520
    SH = sc.rect(105, "Floor shadow", FX, CX - 170, CY + 250, 340, 40, [0, 0, 0, 0.25], r=20, op=0)
    blur(sc, SH, 7600, 22)
    fade(sc, SH, O - 100, END)
    BK = sc.group(110, "Book", FX, CX, CY, CX, CY, op=0)
    sc.rect(111, "Pages", BK, CX - 150 + 10, CY - 200 + 8, 300, 400, [0.93, 0.93, 0.95, 1], r=8)
    cov = sc.rect(112, "Cover", BK, CX - 150, CY - 200, 300, 400, A_BG, r=8, stroke=(A_LINE, 1.5))
    sc.shadow(cov, 0.18, 40, 14)
    sc.rect(113, "Spine", BK, CX - 150, CY - 200, 14, 400, [0.88, 0.90, 0.95, 1], r=4)
    sc.rect(114, "Circle", BK, CX - 80, CY - 150, 160, 160, A_BLUE, r=80)
    sc.text(115, "T1", BK, CX - 118, CY + 90, "Zacznij naukę", 32, A_INK, tracking=-15)
    sc.text(116, "T2", BK, CX - 118, CY + 128, "w 5 minut", 32, A_BLUE, tracking=-15)
    sc.text(117, "Sub", BK, CX - 118, CY + 170, "E-BOOK · 27 STRON", 14, A_GREY, style="Medium", family="Geist Mono", tracking=80)
    # sheen sweep clipped to the cover
    SG = sc.group(120, "Sheen", BK, 0, 0)
    sr = sc.rect(121, "Sheen bar", SG, CX - 400, CY - 260, 90, 520, [1, 1, 1, 0.75])
    sc.k(sr, "rotation", [(0, f(18), LIN)])
    blur(sc, sr, 7601, 18)
    sc.k(sr, "positionX", [(0, f(CX - 400), LIN), (BUM, f(CX - 400), HOLD), (BUM + 700, f(CX + 260), INOUT)])
    mt = sc.rect(122, "Sheen matte", BK, CX - 150, CY - 200, 300, 400, A_BG, r=8)
    sc.A.append({"type": "setFxLayerTrackMatte", "compositionId": "main", "layerId": SG, "matteLayerId": mt, "mode": "alpha"})
    sc.k(BK, "opacity", [(0, f(0), LIN), (O - 150, f(0), HOLD), (O + 80, f(100), SOFT), (END, f(100), HOLD), (END + 250, f(0), SOFT)])
    sc.k(BK, "rotationY", [(0, f(-80), LIN), (O - 150, f(-80), HOLD), (O + 800, f(-14), APPLE), (sc.dur, f(-6), LIN)])
    sc.k(BK, "rotation", [(0, f(-6), LIN), (O - 150, f(-6), HOLD), (O + 800, f(0), APPLE)])
    scale_keys(sc, BK, [(0, f(80), LIN), (O - 150, f(80), HOLD), (O + 800, f(100), APPLE)])
    ch = sc.group(130, "Chip", FX, CX, CY + 330, CX, CY + 330, op=0)
    pill_text(sc, 131, ch, CX + 16, CY + 330, "Okładka gotowa", 26, A_INK, A_BG, style="SemiBold")
    ok_badge(sc, 140, ch, CX - 104, CY + 330, PIEK + 250, d=28)
    card_in(sc, ch, PIEK + 100, END)
    return sc


# ================================================================== AS  Maps place card: key lime pie (overlay)
def scene_AS():
    sc = new("AS_Key-lime-pie", 1166.00, 1172.40)
    FX = overlay(sc)
    w = sc.word
    LIME, POL, FLO = w(1167.54), w(1170.20), w(1171.26)
    END = sc.t(1172.05)
    X0, Y0 = 80, 700
    C = sc.group(110, "Place", FX, X0 + 280, Y0 + 150, X0 + 280, Y0 + 150, op=0)
    card_bg(sc, 111, C, X0, Y0, 560, 300, r=36, sh=(0.2, 60, 18))
    # icon: slice of pie
    sc.rect(112, "Icon bg", C, X0 + 36, Y0 + 36, 96, 96, [0.86, 0.95, 0.72, 1], r=48)
    sc.path(113, "Slice", C, [(X0 + 58, Y0 + 106), (X0 + 110, Y0 + 106), (X0 + 94, Y0 + 58)], 0, 0, fill=[0.93, 0.95, 0.55, 1])
    sc.path(114, "Crust", C, [(X0 + 56, Y0 + 108), (X0 + 112, Y0 + 108)], 0, 0, stroke=([0.78, 0.58, 0.32, 1], 7), closed=False)
    sc.rect(115, "Cream", C, X0 + 88, Y0 + 52, 16, 12, A_BG, r=6)
    sc.text(116, "Title", C, X0 + 156, Y0 + 80, "Key Lime Pie", 38, A_INK, tracking=-15)
    sc.text(117, "Sub", C, X0 + 156, Y0 + 116, "Deser · Floryda", 24, A_GREY, style="Medium")
    for i in range(5):
        cx, cy = X0 + 52 + i * 34, Y0 + 180
        pts = [(cx + 13 * math.cos(math.radians(-90 + k * 36)) * (1 if k % 2 == 0 else 0.45),
                cy + 13 * math.sin(math.radians(-90 + k * 36)) * (1 if k % 2 == 0 else 0.45)) for k in range(10)]
        st = sc.path(120 + i, "Star", C, pts, 0, 0, fill=A_ORANGE, op=0)
        t = LIME + 400 + i * 90
        sc.k(st, "opacity", [(0, f(0), LIN), (t, f(0), HOLD), (t + 150, f(100), SOFT)])
    sc.text(126, "Score", C, X0 + 232, Y0 + 190, "5,0", 26, A_INK)
    bt = sc.group(130, "Btn", C, X0 + 280, Y0 + 246, X0 + 280, Y0 + 246, op=0)
    sc.rect(131, "Btn bg", bt, X0 + 36, Y0 + 220, 488, 54, A_GREEN, r=27)
    sc.text(132, "Btn t", bt, X0 + 280, Y0 + 256, "Konrad poleca", 26, A_BG, just="center")
    fade(sc, bt, POL - 60, d_in=160)
    pop(sc, bt, POL - 60, 450, 85)
    card_in(sc, C, LIME - 200, END)
    sc.k(C, "positionY", [(0, f(Y0 + 190), LIN), (LIME - 200, f(Y0 + 190), HOLD), (LIME + 500, f(Y0 + 150), OUT)])
    # map pin hopping above the card
    PN = sc.group(140, "Pin", FX, X0 + 470, Y0 - 20, X0 + 470, Y0 - 20, op=0)
    sc.rect(141, "Head", PN, X0 + 442, Y0 - 90, 56, 56, A_RED, r=28, stroke=(A_BG, 5))
    sc.rect(142, "Dot", PN, X0 + 461, Y0 - 71, 18, 18, A_BG, r=9)
    sc.path(143, "Stem", PN, [(X0 + 470, Y0 - 36), (X0 + 470, Y0 - 4)], 0, 0, stroke=(A_RED, 5), closed=False)
    sc.k(PN, "opacity", [(0, f(0), LIN), (FLO - 250, f(0), HOLD), (FLO - 100, f(100), SOFT), (END, f(100), HOLD), (END + 250, f(0), SOFT)])
    sc.k(PN, "positionY", [(0, f(Y0 - 140), LIN), (FLO - 250, f(Y0 - 140), HOLD), (FLO + 200, f(Y0 - 20), APPLE)])
    return sc


# ================================================================== AT  balance card: 1 000 000 zł shakes → "kilka tysięcy"
def scene_AT():
    sc = new("AT_Milion", 1199.60, 1209.00)
    sc.apple_bg()
    w = sc.word
    MIL, NIE, KILKA, CZYSTO, TAK = w(1201.14), w(1202.46), w(1205.62), w(1207.16), w(1208.02)
    CD = sc.group(110, "Card", None, 960, 540, 960, 540, op=0)
    crd = sc.rect(111, "Card", CD, 460, 300, 1000, 480, DARK, r=48)
    sc.shadow(crd, 0.3, 80, 30)
    for i, (x, y, d, c) in enumerate([(380, 180, 520, [0.25, 0.35, 0.95, 0.55]), (1080, 520, 460, [0.65, 0.25, 0.85, 0.45])]):
        g = sc.rect(112 + i, "Glow", CD, x, y, d, d, c, r=d / 2)
        blur(sc, g, 7610 + i, 120)
    mt = sc.rect(114, "Card matte", CD, 460, 300, 1000, 480, A_BG, r=48)
    for gid in (112, 113):
        sc.A.append({"type": "setFxLayerTrackMatte", "compositionId": "main", "layerId": gid, "matteLayerId": mt, "mode": "alpha"})
    lab = sc.text(115, "Label", CD, 540, 400, "Zysk miesięcznie", 34, [1, 1, 1, 0.6], style="Medium")
    sc.k(lab, "textContent", [(0, s("Zysk miesięcznie"), LIN), (CZYSTO, s("Miesięcznie, na czysto"), HOLD)])
    amt = sc.text(116, "Amount", CD, 540, 560, "0 zł", 130, A_BG, tracking=-50)
    sc.k(amt, "textContent", [(0, s("0 zł"), LIN)] + Scene.roll_keys(MIL - 100, MIL + 600, zl, 0, 1_000_000)[1:] +
         [(KILKA, s("kilka tysięcy zł"), HOLD)])
    sc.k(amt, "fillColor", [(0, col(A_BG), LIN), (NIE, col(A_BG), HOLD), (NIE + 120, col(A_RED), SOFT),
                            (KILKA - 1, col(A_RED), HOLD), (KILKA, col(A_GREEN), HOLD)])
    stw = adv("1 000 000 zł", 130, "SemiBold") * 1.0
    strike = sc.rect(117, "Strike", CD, 536, 514, 0.01, 8, A_RED, r=4)
    sc.k(strike, "rectSize", [(0, v2(0.01, 8), LIN), (NIE + 100, v2(0.01, 8), HOLD), (NIE + 500, v2(stw, 8), APPLE),
                              (KILKA - 200, v2(stw, 8), HOLD), (KILKA, v2(0.01, 8), SOFT)])
    sc.k(amt, "scaleX", [(0, f(100), LIN), (KILKA - 150, f(100), HOLD), (KILKA - 1, f(96), SOFT), (KILKA + 400, f(100), OUT)])
    sk = [(0, f(960), LIN), (NIE - 1, f(960), HOLD)]
    for n, dx in enumerate([-34, 28, -20, 12, -6, 0]):
        sk.append((NIE + (n + 1) * 65, f(960 + dx), SOFT))
    sc.k(CD, "positionX", sk)
    ok_badge(sc, 130, CD, 1380, 380, TAK, d=64)
    fade(sc, CD, 60, d_in=260)
    scale_keys(sc, CD, [(0, f(94), LIN), (60, f(94), HOLD), (800, f(100), OUT)])
    return sc


# ================================================================== AU  Reminders: upsells swiped to "Część 2" (overlay)
def scene_AU():
    sc = new("AU_Czesc-2", 1225.50, 1245.10)
    FX = overlay(sc)
    w = sc.word
    ZOST, CZT, UPS, REKL, KOL, KOM = w(1225.82), w(1226.26), w(1227.66), w(1235.20), w(1238.80), w(1243.84)
    END = sc.t(1244.75)
    X0, Y0, CW = 1240, 150, 600
    C = sc.group(110, "List", FX, X0 + CW / 2, 420, X0 + CW / 2, 420, op=0)
    card_bg(sc, 111, C, X0, Y0, CW, 560, r=36, sh=(0.2, 60, 18))
    sc.text(112, "Title", C, X0 + 40, Y0 + 70, "Do zrobienia", 38, A_INK, tracking=-15)
    tg = sc.group(113, "Time", C, X0 + CW - 110, Y0 + 58, X0 + CW - 110, Y0 + 58, op=0)
    pill_text(sc, 114, tg, X0 + CW - 110, Y0 + 58, "zostało 40 min", 22, A_ORANGE, a(A_ORANGE, 0.14), style="SemiBold")
    fade(sc, tg, CZT, d_in=160)
    pop(sc, tg, CZT, 420, 70)
    items = [("Pomysł", True), ("Produkt", True), ("Sklep", True), ("Upselle", False), ("Reklamy", False)]
    RY = [Y0 + 130 + i * 84 for i in range(5)]
    for i, (name, done) in enumerate(items):
        y = RY[i]
        if name == "Upselle":
            # swipe actions sit behind the row
            sc.rect(150, "Act 2", C, X0 + CW - 300, y, 150, 72, A_ORANGE, r=0)
            sc.text(151, "Act 2 t", C, X0 + CW - 225, y + 44, "Część 2", 22, A_BG, just="center")
            sc.rect(152, "Act del", C, X0 + CW - 150, y, 150, 72, A_RED, r=0)
            sc.text(153, "Act del t", C, X0 + CW - 75, y + 44, "Pomiń", 22, A_BG, just="center")
        g = sc.group(120 + i * 5, name, C, 0, 0)
        sc.rect(121 + i * 5, "Row bg", g, X0 + 1, y, CW - 2, 72, A_BG)
        if done:
            sc.rect(122 + i * 5, "Done", g, X0 + 40, y + 20, 32, 32, A_GREEN, r=16)
            check(sc, 123 + i * 5, g, X0 + 56, y + 37, 12, A_BG, 3)
            sc.text(124 + i * 5, "Txt", g, X0 + 92, y + 46, name, 30, A_GREY, style="Medium")
        else:
            circ = sc.rect(122 + i * 5, "Todo", g, X0 + 40, y + 20, 32, 32, [1, 1, 1, 0], r=16, stroke=(A_LINE, 3))
            sc.text(124 + i * 5, "Txt", g, X0 + 92, y + 46, name, 30, A_INK, style="Medium")
            if name == "Reklamy":
                sc.k(circ, "strokeColor", [(0, col(A_LINE), LIN), (REKL, col(A_LINE), HOLD), (REKL + 250, col(A_BLUE), SOFT)])
                sc.k(circ, "fillColor", [(0, col([1, 1, 1, 0]), LIN), (REKL, col([1, 1, 1, 0]), HOLD), (REKL + 250, col(a(A_BLUE, 0.15)), SOFT)])
                sc.k(g, "positionY", [(0, f(0), LIN), (REKL - 400, f(0), HOLD), (REKL, f(-84), APPLE)])
        if name == "Upselle":
            sc.k(g, "positionX", [(0, f(0), LIN), (UPS - 60, f(0), HOLD), (UPS + 500, f(-300), APPLE)])
            for lid in (g, 150, 151, 152, 153):
                sc.k(lid, "opacity", [(0, f(100), LIN), (REKL - 700, f(100), HOLD), (REKL - 400, f(0), SOFT)])
        if i < 4:
            sc.rect(145 + i, "Sep", C, X0 + 92, y + 76, CW - 132, 1.5, A_LINE)
    card_in(sc, C, ZOST - 150, END)
    # part 2 open loop
    P2 = sc.group(170, "Part 2", FX, X0 + CW / 2, 790, X0 + CW / 2, 790, op=0)
    card_bg(sc, 171, P2, X0, 740, CW, 100, r=30, sh=(0.18, 40, 14))
    sc.rect(172, "Icon", P2, X0 + 30, 764, 52, 52, A_ORANGE, r=14)
    sc.text(173, "Icon t", P2, X0 + 56, 800, "2", 28, A_BG, just="center")
    sc.text(174, "T", P2, X0 + 100, 784, "Upselle → część 2", 28, A_INK)
    sc.text(175, "S", P2, X0 + 100, 818, "30 dni z tym biznesem?", 22, A_GREY, style="Medium")
    card_in(sc, P2, KOL, END)
    cm = sc.group(180, "Comment", FX, X0 + CW / 2, 910, X0 + CW / 2, 910, op=0)
    pill_text(sc, 181, cm, X0 + CW / 2, 910, "Daj znać w komentarzu", 26, A_BG, A_BLUE, style="SemiBold")
    card_in(sc, cm, KOM - 100, END)
    scale_keys(sc, cm, [(0, f(80), LIN), (KOM - 100, f(80), HOLD), (KOM + 350, f(106), OUT), (KOM + 700, f(100), APPLE)]) if False else None
    return sc


# ================================================================== AV_a  order bump at checkout
def scene_AV_a():
    sc = new("AV_a_Order-bump", 1245.90, 1257.10)
    sc.apple_bg()
    w = sc.word
    DWA, OB, P19, P29, P39, P49 = w(1246.18), w(1246.94), w(1250.06), w(1250.84), w(1251.58), w(1252.20)
    ZWI, RAZU = w(1254.70), w(1256.28)
    ttl = sc.text(100, "Title", None, 960, 200, "Order bump", 88, A_INK, tracking=-40, just="center", op=0)
    sub = sc.text(101, "Sub", None, 960, 262, "dodatek jednym kliknięciem, przy zakupie", 32, A_GREY, style="Medium", just="center", op=0)
    fade(sc, ttl, OB - 100, d_in=240)
    fade(sc, sub, RAZU - 200, d_in=240)
    CO = sc.group(110, "Checkout", None, 960, 610, 960, 610, op=0)
    card_bg(sc, 111, CO, 560, 330, 800, 560, r=40, sh=(0.14, 70, 20))
    sc.text(112, "Head", CO, 610, 400, "Podsumowanie", 34, A_INK, tracking=-10)
    sc.rect(113, "Prod", CO, 610, 432, 64, 84, A_FILL, r=8)
    sc.rect(114, "Prod c", CO, 626, 448, 32, 32, A_BLUE, r=16)
    sc.text(115, "Prod t", CO, 700, 472, "E-book: Zacznij naukę w 5 minut", 28, A_INK, style="Medium")
    sc.text(116, "Prod s", CO, 700, 506, "PDF · dostęp od razu", 22, A_GREY, style="Medium")
    bx = sc.rect(120, "Bump", CO, 600, 548, 720, 150, a(A_ORANGE, 0.08), r=22, stroke=(A_ORANGE, 2.5))
    cb = sc.rect(121, "Check box", CO, 630, 598, 40, 40, A_BG, r=10, stroke=(A_ORANGE, 3))
    ck = check(sc, 122, CO, 650, 619, 15, A_BG, 3.5, op=0)
    sc.text(123, "Bump t", CO, 694, 610, "Tak, dodaj: Plan na sprawdziany", 28, A_INK)
    sc.text(124, "Bump s", CO, 694, 646, "Tylko teraz, przy tym zamówieniu", 22, A_GREY, style="Medium")
    pr = sc.text(125, "Bump price", CO, 1290, 610, "19 zł", 30, A_ORANGE, just="right")
    sc.k(pr, "textContent", [(0, s("19 zł"), LIN), (P29, s("29 zł"), HOLD), (P39, s("39 zł"), HOLD), (P49, s("49 zł"), HOLD)])
    scale_keys(sc, pr, [(0, f(100), LIN)] + sum([[(t - 1, f(100), HOLD), (t + 80, f(118), OUT), (t + 300, f(100), APPLE)]
                                                for t in (P19, P29, P39, P49)], []))
    sc.k(cb, "fillColor", [(0, col(A_BG), LIN), (ZWI, col(A_BG), HOLD), (ZWI + 150, col(A_ORANGE), SOFT)])
    fade(sc, ck, ZWI + 60, d_in=120)
    sc.rect(126, "Sep", CO, 610, 738, 700, 1.5, A_LINE)
    sc.text(127, "Tot", CO, 610, 800, "Wartość koszyka", 30, A_INK, style="Medium")
    up = sc.group(128, "Up", CO, 1250, 790, 1250, 790, op=0)
    pill_text(sc, 129, up, 1240, 790, "+49 zł", 30, [0.1, 0.5, 0.2, 1], a(A_GREEN, 0.16), style="SemiBold")
    fade(sc, up, ZWI + 250, d_in=160)
    pop(sc, up, ZWI + 250, 450, 60)
    sc.k(CO, "opacity", [(0, f(0), LIN), (OB + 300, f(0), HOLD), (OB + 560, f(100), SOFT)])
    sc.k(CO, "positionY", [(0, f(660), LIN), (OB + 300, f(660), HOLD), (OB + 1000, f(610), OUT)])
    for t in (P19,):
        fade(sc, 120, 0, d_in=1) if False else None
    sc.k(bx, "strokeColor", [(0, col(a(A_ORANGE, 0.3)), LIN), (P19 - 100, col(a(A_ORANGE, 0.3)), HOLD), (P19 + 200, col(A_ORANGE), SOFT)])
    return sc


# ================================================================== AV_b  after purchase: upsell inside the buyer dashboard
def scene_AV_b():
    sc = new("AV_b_Upsell", 1259.80, 1278.00)
    sc.apple_bg()
    w = sc.word
    DOST, DASH, DOD, UMIE, P129, SPR, PROD = (w(1260.50), w(1262.08), w(1263.44), w(1267.14), w(1269.62),
                                             w(1272.52), w(1276.54))
    WN = sc.group(110, "Window", None, 960, 560, 960, 560, op=0)
    card_bg(sc, 111, WN, 300, 200, 1320, 720, r=30, sh=(0.14, 80, 24))
    sc.rect(112, "Bar", WN, 300, 200, 1320, 64, A_FILL, r=30)
    sc.rect(113, "Bar sq", WN, 300, 234, 1320, 30, A_FILL)
    for i, c in enumerate([[1.0, 0.37, 0.34, 1], [1.0, 0.74, 0.18, 1], [0.16, 0.79, 0.25, 1]]):
        sc.rect(114 + i, "Light", WN, 330 + i * 26, 226, 14, 14, c, r=7)
    sc.text(117, "URL", WN, 960, 241, "Panel klienta", 22, A_GREY, style="Medium", just="center")
    sc.rect(118, "Side", WN, 300, 264, 280, 656, [0.975, 0.975, 0.98, 1])
    sc.text(119, "Hi", WN, 340, 330, "Cześć, Ania", 28, A_INK)
    for i, (t, on) in enumerate([("Moje produkty", True), ("Ustawienia", False)]):
        sc.rect(120 + i * 2, "Nav", WN, 320, 368 + i * 54, 240, 44, a(A_BLUE, 0.12) if on else [1, 1, 1, 0], r=10)
        sc.text(121 + i * 2, "Nav t", WN, 340, 398 + i * 54, t, 22, A_BLUE if on else A_GREY, style="Medium")
    sc.text(130, "H", WN, 640, 330, "Moje produkty", 40, A_INK, tracking=-15)
    # owned product
    sc.rect(131, "Own", WN, 640, 370, 920, 150, A_FILL, r=22)
    sc.rect(132, "Own cover", WN, 664, 390, 82, 110, A_BG, r=8, stroke=(A_LINE, 1.5))
    sc.rect(133, "Own c", WN, 684, 406, 42, 42, A_BLUE, r=21)
    sc.text(134, "Own t", WN, 770, 432, "Zacznij naukę w 5 minut", 30, A_INK)
    sc.text(135, "Own s", WN, 770, 470, "E-book · kupiony", 22, A_GREY, style="Medium")
    ob = sc.group(136, "Open", WN, 1460, 445, 1460, 445)
    pill_text(sc, 137, ob, 1460, 445, "Otwórz", 24, A_BG, A_BLUE, style="SemiBold")
    dn = sc.group(139, "Done", WN, 1300, 445, 1300, 445, op=0)
    pill_text(sc, 140, dn, 1300, 445, "Ukończone", 22, [0.1, 0.5, 0.2, 1], a(A_GREEN, 0.16), style="SemiBold")
    fade(sc, dn, UMIE, d_in=200)
    pop(sc, dn, UMIE, 420, 70)
    # recommendations
    rh = sc.text(150, "Rec h", WN, 640, 590, "Polecane dla Ciebie", 30, A_INK, op=0)
    fade(sc, rh, DOD - 100)

    def rec(base, x, t, title, price, t_price):
        g = sc.group(base, title, WN, x + 215, 740, x + 215, 740, op=0)
        sc.rect(base + 1, "Bg", g, x, 620, 430, 250, A_BG, r=24, stroke=(A_BLUE, 2.5))
        sc.rect(base + 2, "Cover", g, x + 26, 646, 82, 110, a(A_ORANGE, 0.18), r=8)
        sc.text(base + 3, "Tag", g, x + 130, 676, "NOWOŚĆ", 16, A_ORANGE, style="Medium", family="Geist Mono", tracking=100)
        sc.text(base + 4, "T", g, x + 130, 716, title, 26, A_INK)
        pt = sc.text(base + 5, "Price", g, x + 130, 830, price, 34, A_INK, op=0)
        bt = sc.group(base + 6, "Add", g, x + 340, 818, x + 340, 818, op=0)
        pill_text(sc, base + 7, bt, x + 340, 818, "Dodaj", 24, A_BG, A_BLUE, style="SemiBold")
        fade(sc, g, t - 60, d_in=240)
        pop(sc, g, t - 60, 650, 90)
        if t_price:
            fade(sc, pt, t_price - 60, d_in=160)
            fade(sc, bt, t_price + 150, d_in=160)
            scale_keys(sc, bt, [(0, f(100), LIN), (t_price + 600, f(100), HOLD), (t_price + 750, f(110), OUT), (t_price + 1000, f(100), APPLE)])
    rec(160, 640, DOD, "Plan na sprawdziany", "129 zł", P129)
    rec(180, 1100, PROD, "Produktywność na co dzień", "", None)
    fade(sc, WN, 60, d_in=260)
    scale_keys(sc, WN, [(0, f(95), LIN), (60, f(95), HOLD), (800, f(100), OUT)])
    return sc


# ================================================================== AV_c  price ladder: bumps vs upsells
def scene_AV_c():
    sc = new("AV_c_Ceny", 1281.90, 1290.00)
    sc.apple_bg()
    w = sc.word
    OB, UP = w(1282.16), w(1284.80)
    bumps = [(19, w(1283.20)), (29, w(1283.50)), (39, w(1284.08))]
    ups = [(129, w(1285.84)), (149, w(1286.72)), (490, w(1287.54)), (1000, w(1288.92))]
    BASE = 860
    hf = lambda v: 560 * math.sqrt(v / 1000)
    sc.rect(100, "Axis", None, 200, BASE, 1520, 2, A_LINE)

    def group_(base, x0, title, color, items, t_title):
        tl = sc.text(base, "Title", None, x0 + (len(items) * 150 - 40) / 2, BASE + 70, title, 34, A_INK, just="center", op=0)
        fade(sc, tl, t_title - 60, d_in=220)
        for i, (v, t) in enumerate(items):
            x = x0 + i * 150
            hgt = hf(v)
            b = sc.rect(base + 1 + i * 3, "Bar", None, x, BASE - hgt, 110, hgt, color, r=18, ax=55, ay=hgt)
            sc.k(b, "scaleY", [(0, f(0), LIN), (t - 60, f(0), HOLD), (t + 600, f(100), OUT)])
            lb = sc.text(base + 2 + i * 3, "Val", None, x + 55, BASE - hgt - 24, f"{v} zł", 32, A_INK, just="center", op=0)
            sc.k(lb, "opacity", [(0, f(0), LIN), (t + 150, f(0), HOLD), (t + 350, f(100), SOFT)])
            sc.k(lb, "positionY", [(0, f(BASE - 20), LIN), (t - 60, f(BASE - 20), HOLD), (t + 600, f(BASE - hgt - 24), OUT)])
    group_(110, 300, "Order bump", A_ORANGE, bumps, OB)
    group_(140, 900, "Upsell", A_BLUE, ups, UP)
    return sc


# ================================================================== AW  the headline, as typography
def scene_AW():
    sc = new("AW_Naglowek", 1302.90, 1306.40)
    sc.apple_bg()
    w = sc.word
    words1 = [w(1303.06), w(1303.24), w(1303.44), w(1303.56), w(1303.66)]
    words2 = [w(1303.96), w(1304.12), w(1304.32), w(1304.48), w(1304.62)]
    FAJ = w(1305.46)
    l1 = sc.text(110, "L1", None, 960, 520, "Zacznij naukę w 5 minut,", 132, A_INK, tracking=-55, just="center",
                 animators=[Scene.reveal_animator(1, 11, dy=36, blur=16), Scene.color_animator(2, 21, A_BLUE, 3, 5)])
    sc.reveal_words(l1, 11, words1, step=150)
    l2 = sc.text(111, "L2", None, 960, 640, "nawet jeśli od rana odkładasz", 64, A_GREY, style="Medium", tracking=-20,
                 just="center", animators=[Scene.reveal_animator(3, 31, dy=20, blur=10)])
    sc.reveal_words(l2, 31, words2, step=130)
    ch = sc.group(120, "Chip", None, 960, 330, 960, 330, op=0)
    pill_text(sc, 121, ch, 978, 330, "Mocny nagłówek", 28, A_INK, A_FILL, style="SemiBold")
    ok_badge(sc, 125, ch, 848, 330, FAJ + 200, d=30)
    fade(sc, ch, FAJ, d_in=200)
    pop(sc, ch, FAJ, 450, 80)
    return sc


# ================================================================== AX  2025 → 2026 (overlay)
def scene_AX():
    sc = new("AX_2026", 1314.60, 1318.10)
    FX = overlay(sc)
    w = sc.word
    T25, T26 = w(1315.12), w(1316.80)
    END = sc.t(1317.80)
    C = sc.group(110, "Card", FX, 960, 900, 960, 900, op=0)
    card_bg(sc, 111, C, 700, 830, 520, 140, r=32, sh=(0.2, 50, 16))
    sc.text(112, "K", C, 740, 880, "STOPKA", 16, A_GREY, style="Medium", family="Geist Mono", tracking=120)
    sc.text(113, "C", C, 740, 940, "©", 44, A_GREY, style="Medium")
    x_digits = 790
    sel = sc.rect(114, "Sel", C, x_digits + adv("202", 52, "SemiBold") * 1.0 - 2, 896, adv("5", 52, "SemiBold") + 6, 58, a(A_BLUE, 0.25), r=6, op=0)
    yr = sc.text(115, "Year", C, x_digits, 942, "2025", 52, A_INK, family="Geist Mono", style="Medium")
    sc.k(yr, "textContent", [(0, s("2025"), LIN), (T26, s("2026"), HOLD)])
    sc.k(sel, "opacity", [(0, f(0), LIN), (T25 + 200, f(0), HOLD), (T25 + 350, f(100), SOFT), (T26 - 1, f(100), HOLD), (T26, f(0), HOLD)])
    caret = sc.rect(116, "Caret", C, x_digits + adv("2026", 52, "SemiBold") * 1.06 + 4, 898, 3, 54, A_BLUE, r=1.5, op=0)
    ck, t, on = [(0, f(0), LIN), (T26, f(0), HOLD)], T26 + 1, True
    while t < END:
        ck.append((t, f(100 if on else 0), HOLD)); t += 450; on = not on
    sc.k(caret, "opacity", ck)
    ok_badge(sc, 120, C, 1160, 900, T26 + 350, d=44)
    card_in(sc, C, T25 - 250, END)
    return sc


# ================================================================== AY  store ⇄ payments (overlay)
def scene_AY():
    sc = new("AY_Platnosci", 1318.30, 1327.90)
    FX = overlay(sc)
    w = sc.word
    POD, DWA, NORM, POL = w(1319.00), w(1320.88), w(1323.16), w(1325.58)
    END = sc.t(1327.60)
    C = sc.group(110, "Card", FX, 960, 880, 960, 880, op=0)
    card_bg(sc, 111, C, 460, 770, 1000, 220, r=36, sh=(0.2, 60, 18))

    def node(base, cx, label, sub, color):
        sc.rect(base, "Node", C, cx - 44, 812, 88, 88, a(color, 0.14), r=44)
        sc.text(base + 1, "Label", C, cx, 944, label, 28, A_INK, just="center")
        sc.text(base + 2, "Sub", C, cx, 974, sub, 20, A_GREY, style="Medium", just="center")
    node(120, 600, "Sklep", "twojastrona.pl", A_BLUE)
    sc.path(124, "Awning", C, [(576, 842), (624, 842), (630, 858), (570, 858)], 0, 0, fill=A_BLUE)
    sc.rect(125, "Shop", C, 578, 858, 44, 26, [1, 1, 1, 0], stroke=(A_BLUE, 3), r=3)
    node(130, 1320, "Płatności", "Stripe", A_GREEN)
    sc.rect(134, "Card ic", C, 1294, 838, 52, 36, [1, 1, 1, 0], r=6, stroke=(A_GREEN, 3))
    sc.rect(135, "Card strip", C, 1294, 848, 52, 6, A_GREEN)
    ln = sc.rect(140, "Link", C, 668, 855, 0.01, 4, A_LINE, r=2)
    sc.k(ln, "rectSize", [(0, v2(0.01, 4), LIN), (POD, v2(0.01, 4), HOLD), (POD + 900, v2(584, 4), INOUT)])
    sc.k(ln, "fillColor", [(0, col(A_LINE), LIN), (POL, col(A_LINE), HOLD), (POL + 250, col(A_GREEN), SOFT)])
    for i in range(3):
        d = sc.rect(141 + i, "Packet", C, 668, 849, 16, 16, A_BLUE, r=8, op=0)
        t0 = POD + 900 + i * 450
        kk, t = [(0, f(668), LIN)], t0
        sc.k(d, "opacity", [(0, f(0), LIN), (t0, f(0), HOLD), (t0 + 100, f(100), SOFT), (POL, f(100), HOLD), (POL + 200, f(0), SOFT)])
        while t < POL:
            kk += [(t, f(668), HOLD), (t + 1300, f(1236), INOUT)]
            t += 1350
        sc.k(d, "positionX", kk)
    tg = sc.group(150, "2 min", C, 960, 810, 960, 810, op=0)
    pill_text(sc, 151, tg, 960, 810, "2 minuty", 24, A_INK, A_FILL, style="SemiBold")
    fade(sc, tg, DWA, d_in=160)
    pop(sc, tg, DWA, 420, 70)
    ng = sc.group(155, "Normal", C, 960, 900, 960, 900, op=0)
    pill_text(sc, 156, ng, 960, 900, "nowe konto: 10–15 min", 20, A_GREY, [1, 1, 1, 0])
    fade(sc, ng, NORM, d_in=200)
    pk = sc.group(160, "Connected", C, 960, 810, 960, 810, op=0)
    pill_text(sc, 161, pk, 960, 810, "Połączono", 24, A_BG, A_GREEN, style="SemiBold")
    fade(sc, pk, POL, d_in=160)
    pop(sc, pk, POL, 420, 70)
    sc.k(tg, "scaleX", [(0, f(100), LIN)])
    sc.k(150, "positionY", [(0, f(810), LIN), (POL - 200, f(810), HOLD), (POL + 100, f(780), SOFT)])
    card_in(sc, C, POD - 300, END)
    return sc


# ================================================================== AZ  Face ID: owner panel vs buyer reader (overlay)
def scene_AZ():
    sc = new("AZ_Face-ID", 1350.60, 1356.80)
    FX = overlay(sc)
    w = sc.word
    PAN, LOG, KAZ, CZY = w(1350.94), w(1352.48), w(1352.90), w(1356.08)
    END = sc.t(1356.45)
    X0, CW = 1250, 590
    C1 = sc.group(110, "Owner", FX, X0 + CW / 2, 300, X0 + CW / 2, 300, op=0)
    card_bg(sc, 111, C1, X0, 150, CW, 300, r=36, sh=(0.2, 60, 18))
    fx, fy = X0 + 110, 300
    FI = sc.group(112, "FaceID", C1, fx, fy, fx, fy)
    for i, (sx, sy) in enumerate([(-1, -1), (1, -1), (1, 1), (-1, 1)]):
        pts = [(fx + sx * 50, fy + sy * 20), (fx + sx * 50, fy + sy * 42), (fx + sx * 42, fy + sy * 50), (fx + sx * 20, fy + sy * 50)]
        sc.path(113 + i, "Corner", FI, pts, 0, 0, stroke=(A_BLUE, 5), closed=False)
    sc.rect(117, "Eye L", FI, fx - 20, fy - 18, 6, 14, A_BLUE, r=3)
    sc.rect(118, "Eye R", FI, fx + 14, fy - 18, 6, 14, A_BLUE, r=3)
    sc.path(119, "Nose", FI, [(fx + 2, fy - 16), (fx + 2, fy + 6), (fx - 6, fy + 6)], 0, 0, stroke=(A_BLUE, 4), closed=False)
    sc.path(120, "Smile", FI, arc(fx, fy + 6, 20, 30, 150, 12), 0, 0, stroke=(A_BLUE, 4), closed=False)
    scale_keys(sc, FI, [(0, f(100), LIN), (PAN + 200, f(100), HOLD), (PAN + 450, f(88), INOUT), (PAN + 700, f(100), INOUT),
                        (LOG - 150, f(100), HOLD), (LOG + 100, f(0), IN)])
    ok_badge(sc, 125, C1, fx, fy, LOG + 60, d=90)
    sc.text(130, "T", C1, X0 + 200, 284, "Panel właściciela", 34, A_INK, tracking=-10)
    sc.text(131, "S", C1, X0 + 200, 322, "sprzedaż · lejek · kody", 22, A_GREY, style="Medium")
    tg = sc.group(132, "Only you", C1, X0 + 250, 380, X0 + 250, 380, op=0)
    pill_text(sc, 133, tg, X0 + 262, 380, "tylko Ty", 22, A_BLUE, a(A_BLUE, 0.12), style="SemiBold")
    fade(sc, tg, LOG - 200, d_in=160)
    card_in(sc, C1, PAN - 250, END)
    C2 = sc.group(140, "Buyer", FX, X0 + CW / 2, 650, X0 + CW / 2, 650, op=0)
    card_bg(sc, 141, C2, X0, 500, CW, 300, r=36, sh=(0.2, 60, 18))
    lx, ly = X0 + 110, 660
    sc.rect(142, "Lock body", C2, lx - 34, ly - 14, 68, 54, A_GREEN, r=12)
    shk = sc.path(143, "Shackle", C2, arc(lx, ly - 14, 22, 180, 360, 16), 0, 0, stroke=(A_GREEN, 7), closed=False)
    sc.k(shk, "positionY", [(0, f(0), LIN), (KAZ + 500, f(0), HOLD), (KAZ + 800, f(-14), OUT)])
    sc.k(shk, "positionX", [(0, f(0), LIN), (KAZ + 800, f(0), HOLD), (KAZ + 1000, f(22), OUT)])
    sc.text(144, "T", C2, X0 + 200, 634, "Czytnik e-booka", 34, A_INK, tracking=-10)
    sc.text(145, "S", C2, X0 + 200, 672, "każdy, kto kupi", 22, A_GREY, style="Medium")
    rows = sc.group(146, "Lines", C2, 0, 0, op=0)
    for i, wd in enumerate([300, 250, 280]):
        sc.rect(147 + i, "L", rows, X0 + 200, 704 + i * 22, wd, 9, A_LINE, r=4.5)
    fade(sc, rows, CZY - 400, d_in=250)
    card_in(sc, C2, KAZ - 100, END)
    return sc


# ================================================================== BA  live analytics: 0 visitors
def scene_BA():
    sc = new("BA_Zero-odwiedzin", 1364.90, 1371.40)
    sc.apple_bg()
    w = sc.word
    PR, SK, PL, DZ, WART, ZERO, NIKT = w(1365.50), w(1366.04), w(1366.60), w(1367.42), w(1368.94), w(1369.68), w(1370.04)
    CH = sc.group(100, "Chips", None, 0, 0)
    for i, (t, txt) in enumerate([(PR, "Produkt"), (SK, "Sklep"), (PL, "Płatności")]):
        cx = 660 + i * 300
        g = sc.group(101 + i * 5, txt, CH, cx, 230, cx, 230, op=0)
        pill_text(sc, 102 + i * 5, g, cx + 20, 230, txt, 34, A_INK, A_BG, style="SemiBold", h=74)
        ok_badge(sc, 130 + i * 4, g, cx - adv(txt, 34, "SemiBold") / 2 - 12, 230, t + 150, d=34)
        fade(sc, g, t - 60, d_in=200)
        pop(sc, g, t - 60, 500, 80)
    sc.k(CH, "opacity", [(0, f(100), LIN), (WART, f(100), HOLD), (WART + 400, f(35), SOFT)])
    A_ = sc.group(150, "Analytics", None, 960, 620, 960, 620, op=0)
    card_bg(sc, 151, A_, 560, 360, 800, 520, r=44, sh=(0.14, 80, 24))
    sc.text(152, "Head", A_, 620, 440, "Teraz na stronie", 32, A_GREY)
    dot = sc.rect(153, "Live", A_, 1230, 418, 22, 22, A_GREY, r=11, ax=11, ay=11)
    kk, t, on = [(0, f(100), LIN)], WART, True
    while t < sc.dur:
        kk.append((t, f(160 if on else 100), INOUT)); t += 600; on = not on
    scale_keys(sc, dot, kk)
    sc.text(154, "Zero", A_, 620, 680, "0", 260, A_INK, tracking=-40)
    pts = [(620 + i * 30, 790 + (1.5 if i % 3 == 0 else 0)) for i in range(21)]
    line = sc.path(155, "Spark", A_, pts, 0, 0, stroke=(A_LINE, 5), closed=False, trim=0)
    sc.k(line, "trimEnd", [(0, f(0), LIN), (ZERO, f(0), HOLD), (ZERO + 900, f(100), INOUT)])
    sc.text(156, "Sub", A_, 620, 850, "odwiedzających dziś: 0", 26, A_GREY, style="Medium", op=0)
    fade(sc, 156, NIKT, d_in=240)
    sc.k(A_, "opacity", [(0, f(0), LIN), (WART - 100, f(0), HOLD), (WART + 200, f(100), SOFT)])
    sc.k(A_, "positionY", [(0, f(680), LIN), (WART - 100, f(680), HOLD), (WART + 700, f(620), OUT)])
    return sc


# ================================================================== BB  the best restaurant, in the middle of a forest
def scene_BB():
    sc = new("BB_Restauracja-w-lesie", 1376.30, 1382.15)
    sc.bg = [0.94, 0.96, 0.93, 1]
    w = sc.word
    NAJ, LAS, NIKT, RUCH, KLI = w(1377.16), w(1378.96), w(1379.76), w(1381.16), w(1381.70)
    HX, HY = 960, 560
    F = sc.group(100, "Forest", None, HX, HY, HX, HY)
    rng = random.Random(21)
    greens = [[0.36, 0.55, 0.40, 1], [0.44, 0.63, 0.45, 1], [0.30, 0.48, 0.36, 1], [0.52, 0.69, 0.50, 1]]
    trees = []
    for gx in range(-8, 40):
        for gy in range(-4, 22):
            x = -900 + gx * 95 + rng.uniform(-30, 30)
            y = -500 + gy * 95 + rng.uniform(-30, 30)
            if (x - HX) ** 2 / 1.6 + (y - HY) ** 2 < 170 ** 2:
                continue
            trees.append((y, x, rng.uniform(0.7, 1.15), rng.choice(greens)))
    trees.sort()
    lid = 1000
    for y, x, k, c in trees:
        hgt, wd = 90 * k, 60 * k
        sc.path(lid, "Tree", F, [(x, y - hgt), (x + wd / 2, y), (x - wd / 2, y)], 0, 0, fill=c)
        lid += 1
    # the restaurant
    sc.rect(110, "Ground", F, HX - 110, HY + 36, 220, 14, [0.82, 0.86, 0.80, 1], r=7)
    sc.rect(111, "House", F, HX - 70, HY - 30, 140, 70, [0.99, 0.97, 0.93, 1], r=6)
    sc.path(112, "Roof", F, [(HX - 88, HY - 28), (HX, HY - 86), (HX + 88, HY - 28)], 0, 0, fill=[0.80, 0.36, 0.30, 1])
    glow = sc.rect(113, "Glow", F, HX - 50, HY - 30, 100, 70, [1.0, 0.82, 0.35, 0.6], r=30)
    blur(sc, glow, 7620, 30)
    sc.rect(114, "Window", F, HX - 44, HY - 14, 34, 28, [1.0, 0.83, 0.38, 1], r=4)
    sc.rect(115, "Door", F, HX + 12, HY - 8, 28, 48, [0.55, 0.38, 0.28, 1], r=4)
    st = sc.group(116, "Stars", F, HX, HY - 130, HX, HY - 130, op=0)
    pill_text(sc, 117, st, HX, HY - 130, "★ 5,0  najlepsza na świecie", 22, A_INK, A_BG, style="SemiBold")
    fade(sc, st, NAJ, d_in=200)
    pop(sc, st, NAJ, 450, 70)
    scale_keys(sc, F, [(0, f(330), LIN), (LAS - 200, f(330), HOLD), (LAS + 1500, f(100), INOUT)])
    PC = sc.group(150, "Place card", None, 1500, 190, 1500, 190, op=0)
    card_bg(sc, 151, PC, 1240, 90, 520, 200, r=32, sh=(0.16, 50, 16))
    sc.text(152, "T", PC, 1280, 160, "Restauracja w lesie", 32, A_INK, tracking=-10)
    c1 = sc.text(153, "Ruch", PC, 1280, 214, "Ruch: 0 osób", 26, A_GREY, style="Medium", op=0)
    c2 = sc.text(154, "Kli", PC, 1280, 254, "Klienci: 0", 26, A_GREY, style="Medium", op=0)
    fade(sc, c1, RUCH - 100, d_in=160)
    fade(sc, c2, KLI - 100, d_in=160)
    card_in(sc, PC, NIKT - 100, sc.dur)
    return sc


# ================================================================== BC_a  two sources: organic vs paid
def scene_BC_a():
    sc = new("BC_a_Dwa-zrodla", 1382.30, 1386.10)
    sc.apple_bg()
    w = sc.word
    DWA, ORG, PLAT = w(1383.18), w(1384.06), w(1385.00)
    dv = sc.rect(100, "Divider", None, 959, 540, 2, 0.01, A_LINE, ax=1, ay=0)
    sc.k(dv, "rectSize", [(0, v2(2, 0.01), LIN), (DWA - 200, v2(2, 0.01), HOLD), (DWA + 500, v2(2, 520), OUT)])
    sc.k(dv, "positionY", [(0, f(540), LIN), (DWA - 200, f(540), HOLD), (DWA + 500, f(280), OUT)])

    def side(base, cx, t, title, sub, color, icon):
        g = sc.group(base, title, None, cx, 540, cx, 540, op=0)
        sc.rect(base + 1, "Icon bg", g, cx - 90, 280, 180, 180, a(color, 0.12), r=48)
        icon(g, cx, 370)
        sc.text(base + 2, "T", g, cx, 590, title, 84, A_INK, tracking=-40, just="center")
        sc.text(base + 3, "S", g, cx, 650, sub, 32, A_GREY, style="Medium", just="center")
        fade(sc, g, t - 80, d_in=240)
        pop(sc, g, t - 80, 650, 88)

    def ic_org(g, cx, cy):
        sc.rect(120, "Phone", g, cx - 36, cy - 62, 72, 124, [1, 1, 1, 0], r=16, stroke=(A_BLUE, 5))
        sc.path(121, "Play", g, [(cx - 10, cy - 18), (cx + 18, cy), (cx - 10, cy + 18)], 0, 0, fill=A_BLUE)

    def ic_paid(g, cx, cy):
        for i, r_ in enumerate([56, 36, 14]):
            sc.rect(130 + i, "Ring", g, cx - r_, cy - r_, 2 * r_, 2 * r_, A_GREEN if i == 2 else [1, 1, 1, 0], r=r_,
                    stroke=None if i == 2 else (A_GREEN, 5))
    side(110, 520, ORG, "Organiczne", "za darmo · Reels, TikTok, Shorts", A_BLUE, ic_org)
    side(140, 1400, PLAT, "Płatne", "za budżet · reklamy", A_GREEN, ic_paid)
    return sc


# ================================================================== BC_b  budget dial: 50 → 100 zł / day (overlay)
def scene_BC_b():
    sc = new("BC_b_Budzet", 1403.00, 1409.10)
    FX = overlay(sc)
    w = sc.word
    B50, B100, POL = w(1404.36), w(1404.90), w(1407.28)
    END = sc.t(1408.80)
    CX, CY = 1560, 330
    C = sc.group(110, "Dial card", FX, CX, CY + 20, CX, CY + 20, op=0)
    card_bg(sc, 111, C, CX - 260, 80, 520, 520, r=44, sh=(0.2, 60, 18))
    sc.text(112, "K", C, CX, 150, "Budżet dzienny", 28, A_GREY, just="center")
    R = 150
    trk = sc.path(113, "Track", C, arc(CX, CY + 40, R, 135, 405, 60), 0, 0, stroke=(A_LINE, 16), closed=False)
    val = sc.path(114, "Value", C, arc(CX, CY + 40, R, 135, 405, 60), 0, 0, stroke=(A_GREEN, 16), closed=False, trim=0)
    sc.k(val, "trimEnd", [(0, f(0), LIN), (B50 - 100, f(0), HOLD), (B50 + 400, f(35), OUT), (B100 - 50, f(35), HOLD), (B100 + 500, f(70), OUT)])
    KN = sc.group(115, "Knob", C, CX, CY + 40, CX, CY + 40)
    sc.rect(116, "Knob", KN, CX - 11, CY + 40 - R - 11, 22, 22, A_BG, r=11, stroke=(A_GREEN, 5))
    sc.k(KN, "rotation", [(0, f(-135), LIN), (B50 - 100, f(-135), HOLD), (B50 + 400, f(-135 + 270 * 0.35), OUT),
                          (B100 - 50, f(-135 + 270 * 0.35), HOLD), (B100 + 500, f(-135 + 270 * 0.70), OUT)])
    tx = sc.text(117, "Val", C, CX, CY + 60, "0 zł", 76, A_INK, tracking=-30, just="center")
    sc.k(tx, "textContent", [(0, s("0 zł"), LIN)] + Scene.roll_keys(B50 - 100, B50 + 400, zl, 0, 50)[1:] +
         Scene.roll_keys(B100 - 50, B100 + 500, zl, 50, 100)[1:])
    sc.text(118, "Per", C, CX, CY + 104, "dziennie", 26, A_GREY, style="Medium", just="center")
    rg = sc.group(120, "Rec", C, CX, 548, CX, 548, op=0)
    pill_text(sc, 121, rg, CX, 548, "polecam płatne reklamy", 24, [0.1, 0.5, 0.2, 1], a(A_GREEN, 0.14), style="SemiBold")
    fade(sc, rg, POL - 100, d_in=200)
    pop(sc, rg, POL - 100, 420, 80)
    card_in(sc, C, B50 - 700, END)
    return sc


# ================================================================== BD  cost → investment (card flip, overlay)
def scene_BD():
    sc = new("BD_Inwestycja", 1411.00, 1413.90)
    FX = overlay(sc)
    w = sc.word
    KOSZT, INW = w(1412.14), w(1412.62)
    END = sc.t(1413.60)
    CX, CY = 1500, 480
    FR = sc.group(110, "Front", FX, CX, CY, CX, CY, op=0)
    card_bg(sc, 111, FR, CX - 230, CY - 150, 460, 300, r=40, sh=(0.2, 60, 18))
    sc.text(112, "T", FR, CX, CY + 24, "Koszt", 84, A_INK, tracking=-35, just="center")
    sc.rect(113, "Minus", FR, CX - 30, CY + 70, 60, 8, A_RED, r=4)
    BKG = sc.group(120, "Back", FX, CX, CY, CX, CY, op=0)
    card_bg(sc, 121, BKG, CX - 230, CY - 150, 460, 300, r=40, fill=[0.93, 0.99, 0.94, 1], sh=(0.2, 60, 18))
    sc.text(122, "T", BKG, CX, CY + 10, "Inwestycja", 76, [0.1, 0.5, 0.2, 1], tracking=-35, just="center")
    sc.path(123, "Up", BKG, [(CX - 90, CY + 90), (CX - 30, CY + 60), (CX + 10, CY + 74), (CX + 90, CY + 40)], 0, 0,
            stroke=(A_GREEN, 6), closed=False)
    sc.k(FR, "opacity", [(0, f(0), LIN), (KOSZT - 250, f(0), HOLD), (KOSZT - 50, f(100), SOFT), (INW - 1, f(100), HOLD), (INW + 170, f(0), HOLD)])
    sc.k(FR, "rotationY", [(0, f(0), LIN), (INW - 1, f(0), HOLD), (INW + 170, f(90), IN)])
    pop(sc, FR, KOSZT - 250, 500, 85)
    sc.k(BKG, "opacity", [(0, f(0), LIN), (INW + 169, f(0), HOLD), (INW + 171, f(100), HOLD), (END, f(100), HOLD), (END + 250, f(0), SOFT)])
    sc.k(BKG, "rotationY", [(0, f(-90), LIN), (INW + 170, f(-90), HOLD), (INW + 520, f(0), OUT)])
    return sc


# ================================================================== BC_c  reach roulette vs posting volume
def scene_BC_c():
    sc = new("BC_c_Zasieg", 1419.20, 1428.90)
    sc.apple_bg()
    w = sc.word
    T100, T5, WPL, ILO, DARM = w(1421.18), w(1423.06), w(1425.34), w(1426.12), w(1428.14)
    L = sc.group(110, "Reach", None, 560, 540, 560, 540, op=0)
    card_bg(sc, 111, L, 200, 300, 720, 460, r=44, sh=(0.14, 70, 20))
    sc.text(112, "K", L, 260, 380, "Zasięg jednego filmu", 30, A_GREY)
    num = sc.text(113, "Num", L, 260, 540, "0", 140, A_INK, tracking=-50)
    rng = random.Random(5)
    ks = [(0, s("0"), LIN)] + Scene.roll_keys(T100 - 200, T100 + 500, lambda v: f"{int(v):,}".replace(",", " "), 0, 100000)[1:]
    ks += Scene.roll_keys(T5 - 100, T5 + 500, lambda v: f"{int(v):,}".replace(",", " "), 100000, 5000)[1:]
    t = WPL - 200
    while t < ILO - 150:
        ks.append((t, s(f"{rng.choice([3, 5, 12, 28, 47, 64, 91, 100, 7, 2])} {rng.randint(0, 9)}00".replace("0 0", "0 0")), HOLD))
        t += 90
    ks.append((ILO - 100, s("?"), HOLD))
    sc.k(num, "textContent", ks)
    sc.k(num, "fillColor", [(0, col(A_INK), LIN), (ILO - 101, col(A_INK), HOLD), (ILO - 100, col(A_GREY), HOLD)])
    wp = sc.group(114, "No control", L, 560, 660, 560, 660, op=0)
    pill_text(sc, 115, wp, 470, 660, "nie masz na to wpływu", 26, A_RED, a(A_RED, 0.1), style="SemiBold")
    fade(sc, wp, WPL - 60, d_in=180)
    fade(sc, L, 60, d_in=260)
    scale_keys(sc, L, [(0, f(95), LIN), (60, f(95), HOLD), (800, f(100), OUT)])
    # volume wins: posts fill a grid
    R = sc.group(130, "Volume", None, 0, 0, op=0)
    sc.text(131, "K", R, 1060, 330, "Wygrywa ilość", 44, A_INK, tracking=-20)
    cols = [A_BLUE, TEAL, A_ORANGE, PURPLE, A_GREEN, A_RED]
    n = 0
    for r_ in range(4):
        for c in range(6):
            x, y = 1060 + c * 106, 380 + r_ * 106
            tt = ILO + n * 55
            p = sc.rect(140 + n, "Post", R, x, y, 92, 92, a(cols[(n * 5) % 6], 0.8), r=16, ax=46, ay=46, op=0)
            sc.k(p, "opacity", [(0, f(0), LIN), (tt, f(0), HOLD), (tt + 120, f(100), SOFT)])
            scale_keys(sc, p, [(0, f(50), LIN), (tt, f(50), HOLD), (tt + 350, f(100), OUT)])
            n += 1
    cnt = sc.text(170, "Cnt", R, 1060, 860, "", 30, A_GREY, style="Medium", family="Geist Mono")
    sc.k(cnt, "textContent", [(0, s(""), LIN)] + [(ILO + i * 55, s(f"{i + 1} postów"), HOLD) for i in range(24)])
    dg = sc.group(171, "Free", R, 1560, 850, 1560, 850, op=0)
    pill_text(sc, 172, dg, 1560, 850, "za darmo", 26, [0.1, 0.5, 0.2, 1], a(A_GREEN, 0.14), style="SemiBold")
    fade(sc, dg, DARM - 60, d_in=160)
    pop(sc, dg, DARM - 60, 420, 70)
    fade(sc, R, ILO - 150, d_in=200)
    return sc


# ================================================================== BE  four ad angles, dealt like cards
def scene_BE():
    sc = new("BE_Cztery-kreacje", 1431.20, 1442.00)
    sc.apple_bg()
    w = sc.word
    KIL, KRE, ZOB = w(1431.52), w(1439.48), w(1441.22)
    deal = [w(1434.06), w(1435.30), w(1436.46), w(1437.70)]
    ads = [("Problem", "Znowu odkładasz naukę na jutro?", [0.99, 0.93, 0.92, 1], A_RED),
           ("Rezultat", "Siadasz i uczysz się. W 5 minut.", [0.92, 0.97, 0.93, 1], A_GREEN),
           ("Ciekawość", "Dlaczego nie umiesz zacząć? To nie lenistwo.", [0.93, 0.95, 1.0, 1], A_BLUE),
           ("Błąd", "Czekasz na motywację? To błąd.", [0.97, 0.94, 1.0, 1], PURPLE)]
    xs = [345, 755, 1165, 1575]
    for i, (ang, head, bg, acc) in enumerate(ads):
        cx, cy = xs[i], 500
        g = sc.group(110 + i * 20, ang, None, cx, cy, cx, cy, op=0)
        c = sc.rect(111 + i * 20, "Ad", g, cx - 180, cy - 180, 360, 360, bg, r=28)
        sc.shadow(c, 0.14, 40, 14)
        sc.text(112 + i * 20, "Spons", g, cx - 150, cy - 136, "Sponsorowane", 16, A_GREY, style="Medium")
        words = head.split(" ")
        lines, cur = [], ""
        for wd in words:
            if adv((cur + " " + wd).strip(), 36, "SemiBold") > 300:
                lines.append(cur); cur = wd
            else:
                cur = (cur + " " + wd).strip()
        lines.append(cur)
        for j, ln in enumerate(lines[:3]):
            sc.text(113 + i * 20 + j, "H", g, cx - 150, cy - 70 + j * 44, ln, 36, A_INK, tracking=-15)
        sc.rect(117 + i * 20, "Cover", g, cx + 72, cy + 40, 70, 94, A_BG, r=6, stroke=(A_LINE, 1.5))
        sc.rect(118 + i * 20, "Cover c", g, cx + 89, cy + 54, 36, 36, A_BLUE, r=18)
        sc.rect(119 + i * 20, "Btn", g, cx - 150, cy + 108, 190, 44, acc, r=22)
        sc.text(120 + i * 20, "Btn t", g, cx - 55, cy + 138, "Kup teraz", 20, A_BG, just="center")
        lab = sc.group(121 + i * 20, "Label", g, cx, cy + 240, cx, cy + 240, op=0)
        pill_text(sc, 122 + i * 20, lab, cx, cy + 240, ang, 30, acc, a(acc, 0.12), style="SemiBold")
        ctr = sc.group(124 + i * 20, "CTR", g, cx, cy + 310, cx, cy + 310, op=0)
        pill_text(sc, 125 + i * 20, ctr, cx, cy + 310, "CTR: ?", 24, A_GREY, A_FILL, style="SemiBold")
        t = deal[i]
        # deck in the centre, then dealt to its slot
        sc.k(g, "opacity", [(0, f(0), LIN), (KIL - 60 + i * 60, f(0), HOLD), (KIL + 180 + i * 60, f(100), SOFT)])
        sc.kpos(g, [(0, 960, 520 - i * 8, LIN), (t - 60, 960, 520 - i * 8, HOLD), (t + 650, cx, cy, APPLE)])
        sc.k(g, "rotation", [(0, f([-7, 4, -2, 6][i]), LIN), (t - 60, f([-7, 4, -2, 6][i]), HOLD), (t + 650, f(0), APPLE)])
        scale_keys(sc, g, [(0, f(88), LIN), (t - 60, f(88), HOLD), (t + 650, f(100), APPLE), (KRE + i * 70, f(100), HOLD),
                           (KRE + i * 70 + 150, f(104), OUT), (KRE + i * 70 + 450, f(100), APPLE)])
        fade(sc, lab, t + 300, d_in=180)
        fade(sc, ctr, ZOB + i * 110, d_in=160)
        pop(sc, ctr, ZOB + i * 110, 400, 70)
    return sc


# ================================================================== BF  the feed flies past your ad
def scene_BF():
    sc = new("BF_Scroll", 1466.60, 1474.40)
    sc.apple_bg()
    w = sc.word
    PROD, REK, OFE, OBCH = w(1466.96), w(1469.92), w(1471.38), w(1473.78)
    PX, PY, PW, PH = 810, 150, 340, 720
    fr = sc.rect(100, "Phone", None, PX - 14, PY - 14, PW + 28, PH + 28, A_INK, r=64)
    sc.shadow(fr, 0.2, 60, 20)
    FEED = sc.group(110, "Feed", None, 0, 0)
    sc.rect(111, "Screen bg", FEED, PX, PY, PW, PH, A_BG)
    SC_ = sc.group(112, "Scroll", FEED, 0, 0)
    cols = [A_BLUE, TEAL, A_ORANGE, PURPLE, A_GREEN, A_RED, [0.95, 0.75, 0.3, 1]]
    y, ad_y = PY + 20, None
    for i in range(34):
        is_ad = i == 22
        h_ = 300
        sc.rect(120 + i * 3, "Post", SC_, PX + 16, y, PW - 32, 240, A_FILL if is_ad else a(cols[i % 7], 0.55), r=18)
        if is_ad:
            ad_y = y
            sc.text(220, "Ad t1", SC_, PX + 36, y + 70, "E-book o nauce.", 28, A_INK)
            sc.text(221, "Ad t2", SC_, PX + 36, y + 110, "Kup teraz.", 28, A_GREY)
            sc.text(222, "Ad s", SC_, PX + 36, y + 36, "Sponsorowane", 14, A_GREY, style="Medium")
        sc.rect(121 + i * 3, "Line", SC_, PX + 16, y + 252, 180, 10, A_LINE, r=5)
        y += h_
    # scroll fast; the ad passes the middle right at "zdaniem, które nikogo nie obchodzi"
    mid = PY + PH / 2 - 120
    target = -(ad_y - mid)
    T_AD = w(1472.52)
    sc.k(SC_, "positionY", [(0, f(0), LIN), (T_AD, f(target), LIN), (sc.dur, f(target - 2400), IN)])
    mt = sc.rect(113, "Screen matte", None, PX, PY, PW, PH, A_BG, r=50)
    sc.A.append({"type": "setFxLayerTrackMatte", "compositionId": "main", "layerId": FEED, "matteLayerId": mt, "mode": "alpha"})
    sc.rect(114, "Island", None, 960 - 50, PY + 14, 100, 28, A_INK, r=14)
    # diagnosis on the left
    for i, (t, txt, good) in enumerate([(PROD, "Produkt", True), (REK, "Reklama", False)]):
        cy = 440 + i * 110
        g = sc.group(300 + i * 6, txt, None, 480, cy, 480, cy, op=0)
        pill_text(sc, 301 + i * 6, g, 500, cy, txt, 36, A_INK, A_BG, style="SemiBold", h=78)
        if good:
            ok_badge(sc, 303 + i * 6, g, 500 - adv(txt, 36, "SemiBold") / 2 - 14, cy, t + 150, d=36)
        else:
            xb = sc.group(303 + i * 6, "X", g, 500 - adv(txt, 36, "SemiBold") / 2 - 14, cy, 500 - adv(txt, 36, "SemiBold") / 2 - 14, cy, op=0)
            xx = 500 - adv(txt, 36, "SemiBold") / 2 - 14
            sc.rect(304 + i * 6, "X bg", xb, xx - 18, cy - 18, 36, 36, A_RED, r=18)
            sc.path(305 + i * 6, "X1", xb, [(xx - 7, cy - 7), (xx + 7, cy + 7)], 0, 0, stroke=(A_BG, 3.5), closed=False)
            sc.path(306 + i * 6, "X2", xb, [(xx + 7, cy - 7), (xx - 7, cy + 7)], 0, 0, stroke=(A_BG, 3.5), closed=False)
            fade(sc, xb, t + 150, d_in=160)
            pop(sc, xb, t + 150, 400, 50)
        fade(sc, g, t - 60, d_in=200)
        pop(sc, g, t - 60, 500, 85)
    sg = sc.group(320, "Attention", None, 1440, 540, 1440, 540, op=0)
    sc.text(321, "Big", sg, 1440, 540, "0,3 s", 120, A_INK, tracking=-50, just="center")
    sc.text(322, "Sub", sg, 1440, 600, "tyle dostaje Twoja reklama", 28, A_GREY, style="Medium", just="center")
    fade(sc, sg, OBCH - 400, d_in=200)
    pop(sc, sg, OBCH - 400, 500, 85)
    return sc


# ================================================================== BG  funnel pipeline (overlay, bottom band)
def scene_BG():
    sc = new("BG_Lejek", 1483.30, 1508.70)
    FX = overlay(sc)
    w = sc.word
    IMP, KLI, STR, SKON, ZBUD = w(1484.46), w(1485.56), w(1487.24), w(1489.34), w(1490.76)
    KUP, CHK, NIEP, ZAK, UPS, NIEM = w(1497.46), w(1499.78), w(1500.78), w(1503.10), w(1505.42), w(1507.46)
    END = sc.t(1508.40)
    B = sc.group(110, "Band", FX, 960, 905, 960, 905, op=0)
    card_bg(sc, 111, B, 110, 800, 1700, 210, r=40, sh=(0.2, 60, 18))
    card_in(sc, B, IMP - 300, END)
    names = ["Impresja", "Klik", "Strona", "Checkout", "Zakup", "Upsell"]
    ts = [IMP, KLI, STR, CHK, ZAK, UPS]
    xs = [255 + i * 282 for i in range(6)]
    Y = 880
    for i in range(5):
        ln = sc.rect(120 + i, "Arrow", B, xs[i] + 110, Y - 1.5, 0.01, 3, A_LINE, r=1.5)
        sc.k(ln, "rectSize", [(0, v2(0.01, 3), LIN), (ts[i + 1] - 300, v2(0.01, 3), HOLD), (ts[i + 1], v2(62, 3), OUT)])
    pills = []
    for i, (nm, t) in enumerate(zip(names, ts)):
        g = sc.group(130 + i * 6, nm, B, xs[i], Y, xs[i], Y, op=0)
        ghost = nm == "Upsell"
        bg = sc.rect(131 + i * 6, "Pill", g, xs[i] - 110, Y - 36, 220, 72, A_FILL if not ghost else [1, 1, 1, 0], r=36,
                     stroke=((A_LINE, 3) if ghost else ([1, 1, 1, 0], 3)))
        tx = sc.text(132 + i * 6, "T", g, xs[i], Y + 11, nm, 30, A_GREY if ghost else A_INK, just="center")
        fade(sc, g, t - 60, d_in=200)
        pop(sc, g, t - 60, 500, 85)
        pills.append((g, bg, tx))
    # the page must convert
    sc.k(pills[2][1], "strokeColor", [(0, col([1, 1, 1, 0]), LIN), (SKON - 60, col([1, 1, 1, 0]), HOLD), (SKON + 200, col(A_BLUE), SOFT)])
    sub = sc.text(160, "Page sub", B, xs[2], 960, "ta, którą zbudowaliśmy", 20, A_BLUE, style="Medium", just="center", op=0)
    fade(sc, sub, ZBUD - 60, d_in=200)
    # checkout not connected yet
    cg = sc.group(162, "Soon", B, xs[3], 960, xs[3], 960, op=0)
    pill_text(sc, 163, cg, xs[3], 960, "za chwilę podłączę", 20, A_ORANGE, a(A_ORANGE, 0.12), style="SemiBold")
    fade(sc, cg, NIEP - 60, d_in=180)
    # upsell: not today
    st = sc.rect(165, "Strike", B, xs[5] - 70, Y - 1.5, 0.01, 4, A_RED, r=2)
    sc.k(st, "rectSize", [(0, v2(0.01, 4), LIN), (NIEM - 60, v2(0.01, 4), HOLD), (NIEM + 350, v2(140, 4), APPLE)])
    ug = sc.group(166, "Not today", B, xs[5], 960, xs[5], 960, op=0)
    pill_text(sc, 167, ug, xs[5], 960, "nie tym razem", 20, A_RED, a(A_RED, 0.1), style="SemiBold")
    fade(sc, ug, NIEM, d_in=180)
    # traffic flowing through what exists, dropping off on the way
    rng = random.Random(9)
    lid = 400

    def wave(t0, t1, last_stage):
        nonlocal lid
        t = t0
        while t < t1:
            stop = min(last_stage, [0, 1, 1, 2, 2, 2, 3, 4, 4][rng.randint(0, 8)] if last_stage > 2 else rng.choice([0, 1, 1, 2, 2]))
            d = sc.rect(lid, "Visitor", B, xs[0] - 8, Y - 64, 16, 16, A_BLUE, r=8, op=0)
            keys, tt = [(0, xs[0] - 8, Y - 64, LIN), (t, xs[0] - 8, Y - 64, HOLD)], t
            for k in range(1, stop + 1):
                tt += 420
                keys.append((tt, xs[k] - 8, Y - 64, INOUT))
            keys.append((tt + 400, xs[stop] - 8 + 30, Y - 20, IN))
            sc.kpos(d, keys)
            sc.k(d, "opacity", [(0, f(0), LIN), (t, f(0), HOLD), (t + 120, f(100), SOFT), (tt + 150, f(100), HOLD), (tt + 400, f(0), SOFT)])
            lid += 1
            t += 260
    wave(STR + 400, KUP - 600, 2)
    wave(ZAK + 300, END - 1800, 4)
    return sc


# ================================================================== BH  Focus mode: 12 hours of copywriting (overlay)
def scene_BH():
    sc = new("BH_Skupienie", 1547.50, 1560.20)
    FX = overlay(sc)
    w = sc.word
    H12, USI, AIR, NIK, KOP, SKAL = w(1547.84), w(1549.72), w(1551.82), w(1553.24), w(1554.62), w(1556.92)
    END = sc.t(1559.90)
    X0, CW = 1200, 640
    C = sc.group(110, "Focus", FX, X0 + CW / 2, 330, X0 + CW / 2, 330, op=0)
    card_bg(sc, 111, C, X0, 90, CW, 480, r=40, fill=[0.12, 0.12, 0.16, 1], sh=(0.3, 60, 20))
    mx, my = X0 + 80, 170
    sc.rect(112, "Moon bg", C, mx - 36, my - 36, 72, 72, PURPLE, r=36)
    sc.rect(113, "Moon", C, mx - 18, my - 20, 36, 36, A_BG, r=18)
    sc.rect(114, "Moon cut", C, mx - 6, my - 28, 34, 34, PURPLE, r=17)
    sc.text(115, "T", C, X0 + 140, 162, "Skupienie", 38, A_BG, tracking=-15)
    sc.text(116, "S", C, X0 + 140, 198, "Pisanie reklamy", 24, [1, 1, 1, 0.6], style="Medium")
    tg = sc.group(117, "12h", C, X0 + CW - 110, 170, X0 + CW - 110, 170, op=0)
    pill_text(sc, 118, tg, X0 + CW - 110, 170, "12 godz.", 24, A_BG, a(PURPLE, 0.6), style="SemiBold")
    fade(sc, tg, H12, d_in=160)
    pop(sc, tg, H12, 400, 70)
    rows = [(AIR, "Słuchawki połączone"), (NIK, "Powiadomienia wyciszone"), (KOP, "Tylko Ty i copy")]
    for i, (t, txt) in enumerate(rows):
        y = 260 + i * 70
        g = sc.group(120 + i * 5, txt, C, 0, 0, op=0)
        sc.rect(121 + i * 5, "Row", g, X0 + 40, y, CW - 80, 56, [1, 1, 1, 0.08], r=16)
        sc.rect(122 + i * 5, "Dot", g, X0 + 64, y + 20, 16, 16, PURPLE, r=8)
        sc.text(123 + i * 5, "T", g, X0 + 98, y + 37, txt, 25, A_BG, style="Medium")
        sc.k(g, "opacity", [(0, f(0), LIN), (t - 60, f(0), HOLD), (t + 200, f(100), SOFT)])
        sc.k(g, "positionX", [(0, f(24), LIN), (t - 60, f(24), HOLD), (t + 500, f(0), OUT)])
    # headphones glyph on the first row
    hx, hy = X0 + CW - 90, 288
    ph = sc.path(140, "Band", C, arc(hx, hy + 6, 20, 180, 360, 16), 0, 0, stroke=(A_BG, 4), closed=False, op=0)
    e1 = sc.rect(141, "Cup L", C, hx - 25, hy + 2, 11, 20, A_BG, r=4, op=0)
    e2 = sc.rect(142, "Cup R", C, hx + 14, hy + 2, 11, 20, A_BG, r=4, op=0)
    for lid in (ph, e1, e2):
        fade(sc, lid, AIR + 150, d_in=200)
    # the payoff he's talking about
    sc.text(150, "Goal k", C, X0 + 40, 500, "Cel: skalowanie do", 22, [1, 1, 1, 0.55], style="Medium", op=0)
    gl = sc.text(151, "Goal", C, X0 + 40, 540, "kilkuset tys. zł / mies.", 32, A_GREEN, op=0)
    ch = sc.path(152, "Chart", C, [(X0 + 430, 540), (X0 + 480, 520), (X0 + 520, 528), (X0 + 560, 490), (X0 + 600, 470)],
                 0, 0, stroke=(A_GREEN, 5), closed=False, trim=0)
    for lid in (150, 151):
        fade(sc, lid, SKAL - 100, d_in=220)
    sc.k(ch, "trimEnd", [(0, f(0), LIN), (SKAL, f(0), HOLD), (SKAL + 1000, f(100), INOUT)])
    card_in(sc, C, USI - 1300, END)
    return sc


# ================================================================== BI  light vs dark ads + Night Shift on the red glasses (overlay)
def scene_BI():
    sc = new("BI_Tryb-nocny", 1573.40, 1590.60)
    FX = overlay(sc)
    w = sc.word
    CRE, CIEM, WIEC, JAS, ROZ = w(1573.54), w(1575.28), w(1580.74), w(1588.12), w(1589.60)
    GL = sc.t(1585.90)
    END = sc.t(1590.30)
    # warm Night Shift tint over the whole frame once the red glasses go on
    tint = sc.rect(105, "Night Shift", FX, 0, 0, W, H, [1.0, 0.55, 0.15, 0.13], op=0)
    sc.k(tint, "opacity", [(0, f(0), LIN), (GL - 100, f(0), HOLD), (GL + 500, f(100), SOFT), (END, f(100), HOLD), (END + 250, f(0), SOFT)])
    ng = sc.group(106, "Night pill", FX, 300, 110, 300, 110, op=0)
    pill_text(sc, 107, ng, 300, 110, "Tryb nocny: włączony", 26, A_BG, [0.2, 0.15, 0.1, 0.85], style="SemiBold")
    card_in(sc, ng, GL + 150, END)
    X0, CW = 1230, 610
    C = sc.group(110, "Appearance", FX, X0 + CW / 2, 480, X0 + CW / 2, 480, op=0)
    card_bg(sc, 111, C, X0, 190, CW, 580, r=40, sh=(0.2, 60, 18))
    sc.text(112, "T", C, X0 + 44, 256, "Wygląd reklamy", 34, A_INK, tracking=-10)
    sc.text(113, "S", C, X0 + 44, 292, "Creative diversity", 22, A_GREY, style="Medium")
    opts = [("Jasna", X0 + 60, A_BG, A_INK), ("Ciemna", X0 + 330, [0.1, 0.1, 0.12, 1], A_BG)]
    for i, (nm, x, bgc, ink) in enumerate(opts):
        ph = sc.rect(120 + i * 10, "Phone", C, x, 330, 220, 330, bgc, r=30, stroke=(A_LINE, 2))
        sc.rect(121 + i * 10, "L1", C, x + 26, 380, 150, 16, a(ink, 0.85), r=8)
        sc.rect(122 + i * 10, "L2", C, x + 26, 408, 110, 16, a(ink, 0.85), r=8)
        sc.rect(123 + i * 10, "Img", C, x + 26, 444, 168, 120, a(A_BLUE, 0.35), r=14)
        sc.rect(124 + i * 10, "Btn", C, x + 26, 584, 168, 36, A_BLUE, r=18)
        sc.text(125 + i * 10, "Name", C, x + 110, 708, nm, 26, A_INK, style="Medium", just="center")
    ring = sc.rect(140, "Select", C, X0 + 320, 320, 240, 350, [1, 1, 1, 0], r=38, stroke=(A_BLUE, 4), op=0)
    sc.k(ring, "opacity", [(0, f(0), LIN), (CIEM - 60, f(0), HOLD), (CIEM + 160, f(100), SOFT)])
    sc.k(ring, "positionX", [(0, f(X0 + 320), LIN), (JAS - 60, f(X0 + 320), HOLD), (JAS + 450, f(X0 + 50), APPLE),
                             (ROZ - 60, f(X0 + 50), HOLD), (ROZ + 450, f(X0 + 320), APPLE)])
    wg = sc.group(150, "Evening", C, X0 + 440, 752, X0 + 440, 752, op=0)
    pill_text(sc, 151, wg, X0 + 440, 752, "na wieczór", 20, PURPLE, a(PURPLE, 0.12), style="SemiBold")
    fade(sc, wg, WIEC - 60, d_in=160)
    pop(sc, wg, WIEC - 60, 400, 70)
    card_in(sc, C, CRE - 150, END)
    return sc


BUILD = {"AP": scene_AP, "AQ_a": scene_AQ_a, "AQ_b": scene_AQ_b, "AR": scene_AR, "AS": scene_AS, "AT": scene_AT,
         "AU": scene_AU, "AV_a": scene_AV_a, "AV_b": scene_AV_b, "AV_c": scene_AV_c, "AW": scene_AW, "AX": scene_AX,
         "AY": scene_AY, "AZ": scene_AZ, "BA": scene_BA, "BB": scene_BB, "BC_a": scene_BC_a, "BC_b": scene_BC_b,
         "BD": scene_BD, "BC_c": scene_BC_c, "BE": scene_BE, "BF": scene_BF, "BG": scene_BG, "BH": scene_BH, "BI": scene_BI}
OVERLAY.update({"AP", "AQ_a", "AQ_b", "AR", "AS", "AU", "AX", "AY", "AZ", "BC_b", "BD", "BG", "BH", "BI"})

if __name__ == "__main__":
    for key in (sys.argv[1:] or BUILD):
        try:
            BUILD[key]().build(key)
        except SystemExit as e:
            print(f"[{key}] FAILED: {e}")
