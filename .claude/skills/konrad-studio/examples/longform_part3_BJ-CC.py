#!/usr/bin/env python3
"""Part 3, batch 3: BJ–CC (26:38–32:15) on halfraw.mp4 — the finale + the results. Callbacks on purpose:
the intro's blurred result cards (#5) unblur in stages, the intro iOS timer (#8) rings and later turns into zł/h,
the BM spec sheet and the BG funnel come back filled with the real numbers, the AN receipt returns for the CTA.
BJ creative cell-division · BK bar that leaves the frame · BL 7×50 zł coins + the 10k screenshot · BM spec sheet ·
BN island countdown · BO timer alarm · BP overtime +0:05 → ready · BQ calendar 15→22 Sept · BR expectation ghost ·
BS_a revenue unblurs · BT ROAS equation + coin · BS_b profit unblurs · BU ring → 193 zł/h · BV result breaks the ghost ·
BW results sheet · BX funnel with real numbers (overlay) · BY 16 of 19 opened · BZ BLIK code · CA receipt + link ·
CB "Raczej nie." + footnote · CC best day.
Usage: scenes_bj.py BJ BK ...   (no args = all)."""
import sys, math, random
from fontTools.ttLib import TTFont
from scenes_af import adv
from scenes_af2 import check, spinner, fade
from scenes_gk import pop
from scenes_lu import card_bg, rise_group
from scenes_vo import new, overlay, arc, blur, scale_keys, pill_text, blob
from scenes_ap import zl, ok_badge, card_in, PURPLE, TEAL, DARK, link_scene
from ds import *

OVERLAY = set()
GOLD = [1.0, 0.78, 0.25, 1]
GOLD_D = [0.72, 0.50, 0.05, 1]
_mono = TTFont(os.path.join(ROOT, "Source/fonts/GeistMono-Medium.ttf"))


def madv(t, size):
    return sum(_mono["hmtx"][_mono.getBestCmap()[ord(c)]][0] for c in t) * size / _mono["head"].unitsPerEm


def zl2(v):
    s_ = f"{v:,.2f}".replace(",", " ").replace(".", ",")
    return s_ + " zł"


# ------------------------------------------------------------------ shared: the intro's three result columns (#5)
COLS = [("Przychód", 440), ("Sprzedaże", 960), ("Na czysto", 1480)]


def result_columns(sc, base, reveals, t_in=60, seed=7):
    """reveals = {col_index: (t_reveal, text, color)}; unrevealed columns keep scrambling behind a blur."""
    rng = random.Random(seed)
    gens = [lambda: zl(rng.randint(1000, 39999)), lambda: str(rng.randint(10, 999)),
            lambda: rng.choice(["+", "−"]) + zl(rng.randint(100, 9999))]
    for i, (label, cx) in enumerate(COLS):
        b = base + i * 10
        g = sc.group(b, label, None, cx, 520, cx, 520, op=0)
        sc.text(b + 1, "Label", g, cx, 420, label, 32, A_GREY, style="Medium", just="center")
        bl = sc.text(b + 2, "Blurred", g, cx, 560, gens[i](), 104, A_INK, tracking=-40, just="center")
        sc.A.append({"type": "addFxLayerEffect", "compositionId": "main", "layerId": bl, "effectId": 8100 + b,
                     "effect": {"type": "gaussianBlur", "blurriness": 75}})
        rv = reveals.get(i)
        stop = rv[0] if rv else sc.dur
        keys, tt = [(0, s(gens[i]()), LIN)], 90
        while tt < stop:
            keys.append((tt, s(gens[i]()), HOLD)); tt += 90
        sc.k(bl, "textContent", keys)
        fade(sc, g, t_in + i * 120, d_in=260)
        if rv:
            t, txt, colr = rv
            if t <= 1:
                sc.k(bl, "opacity", [(0, f(0), LIN)])
                sh = sc.text(b + 3, "Sharp", g, cx, 560, txt, 104, colr, tracking=-40, just="center")
            else:
                sc.k(bl, "opacity", [(0, f(100), LIN), (t - 1, f(100), HOLD), (t + 250, f(0), SOFT)])
                sh = sc.text(b + 3, "Sharp", g, cx, 560, txt, 104, colr, tracking=-40, just="center", op=0)
                sc.k(sh, "opacity", [(0, f(0), LIN), (t - 1, f(0), HOLD), (t + 200, f(100), SOFT)])
                scale_keys(sc, g, [(0, f(100), LIN), (t - 1, f(100), HOLD), (t + 120, f(108), OUT), (t + 600, f(100), APPLE)])


def island(sc, base, parent, t_in, t_out, width=360, height=64, top=18):
    """Black Dynamic-Island pill (same family as the timer pills). Returns (group, x0)."""
    x0 = 960 - width / 2
    g = sc.group(base, "Island", parent, 960, top + height / 2, 960, top + height / 2, op=0)
    isl = sc.rect(base + 1, "Pill", g, x0, top, width, height, [0.02, 0.02, 0.02, 1], r=height / 2)
    sc.shadow(isl, 0.25, 24, 6)
    sc.k(g, "opacity", [(0, f(0), LIN), (t_in, f(0), HOLD), (t_in + 200, f(100), SOFT), (t_out, f(100), HOLD), (t_out + 250, f(0), SOFT)])
    sc.k(g, "scaleX", [(0, f(40), LIN), (t_in, f(40), HOLD), (t_in + 500, f(100), APPLE)])
    sc.k(g, "scaleY", [(0, f(60), LIN), (t_in, f(60), HOLD), (t_in + 500, f(100), APPLE)])
    return g, x0, isl


# ================================================================== BJ  one creative divides into 64
def scene_BJ():
    sc = new("BJ_Warianty", 1598.70, 1604.25)
    sc.apple_bg()
    w = sc.word
    T = [60, w(1599.18), w(1599.90), w(1600.78), w(1602.44), w(1602.92), w(1603.22)]
    NS = [1, 2, 4, 8, 16, 32, 64]
    COLS_ = [1, 2, 2, 4, 4, 8, 16]
    ROWS_ = [1, 1, 2, 2, 4, 4, 4]
    LBL = ["1 kreacja", "2 warianty", "4 warianty", "8 wariantów", "16 wariantów", "32 warianty", "64 warianty"]
    cols = [[0.93, 0.95, 1.0, 1], [0.99, 0.93, 0.92, 1], [0.92, 0.97, 0.93, 1], [0.97, 0.94, 1.0, 1],
            [1.0, 0.96, 0.88, 1], [0.90, 0.97, 0.98, 1]]
    acc = [A_BLUE, A_RED, A_GREEN, PURPLE, A_ORANGE, TEAL]

    def layout(k):
        c, r = COLS_[k], ROWS_[k]
        size = min(300, 1560 / c - 18, 700 / r - 18)
        gap = size + 18
        x0 = 960 - (c - 1) * gap / 2
        y0 = 590 - (r - 1) * gap / 2
        return [(x0 + (i % c) * gap, y0 + (i // c) * gap) for i in range(c * r)], size
    lays = [layout(k) for k in range(7)]
    lid = 300
    for i in range(64):
        k0 = next(k for k in range(7) if i < NS[k])
        g = sc.group(lid, f"Ad {i}", None, 960, 590, 960, 590, op=0)
        sc.rect(lid + 1, "Bg", g, 810, 440, 300, 300, cols[i % 6], r=44)
        sc.rect(lid + 2, "Head", g, 846, 480, 180, 22, a(A_INK, 0.8), r=8)
        sc.rect(lid + 3, "Head2", g, 846, 512, 120, 22, a(A_INK, 0.8), r=8)
        if i % 3 != 1:          # with a face / without a face
            sc.rect(lid + 4, "Face", g, 990, 590, 80, 80, a(acc[i % 6], 0.55), r=40)
        else:
            sc.rect(lid + 4, "Book", g, 1000, 580, 60, 84, A_BG, r=6, stroke=(A_LINE, 2))
        sc.rect(lid + 5, "Btn", g, 846, 676, 130, 36, acc[i % 6], r=18)
        parent = i - NS[k0 - 1] if k0 else 0
        pk, sk_ = [], []
        t_first = T[k0]
        start_pos = lays[k0 - 1][0][parent] if k0 else lays[0][0][0]
        start_sc = (lays[k0 - 1][1] if k0 else lays[0][1]) / 300 * 100
        pk.append((0, start_pos[0], start_pos[1], LIN))
        sk_.append((0, f(start_sc), LIN))
        prev = start_pos, start_sc
        for k in range(k0, 7):
            pos, size = lays[k][0][i], lays[k][1] / 300 * 100
            t = T[k]
            if t - 1 > pk[-1][0]:
                pk.append((t - 1, prev[0][0], prev[0][1], HOLD))
                sk_.append((t - 1, f(prev[1]), HOLD))
            pk.append((t + 520, pos[0], pos[1], APPLE))
            sk_.append((t + 520, f(size), APPLE))
            prev = pos, size
        sc.kpos(g, pk)
        scale_keys(sc, g, sk_)
        sc.k(g, "opacity", [(0, f(0), LIN), (t_first - 1, f(0), HOLD), (t_first + 150, f(100), SOFT)])
        lid += 6
    lb = sc.text(200, "Count", None, 960, 190, LBL[0], 64, A_INK, tracking=-25, just="center", op=0)
    sc.k(lb, "textContent", [(0, s(LBL[0]), LIN)] + [(T[k], s(LBL[k]), HOLD) for k in range(1, 7)])
    fade(sc, lb, 80, d_in=240)
    scale_keys(sc, lb, [(0, f(100), LIN)] + sum([[(T[k] - 1, f(100), HOLD), (T[k] + 90, f(108), OUT), (T[k] + 360, f(100), APPLE)]
                                                for k in range(1, 7)], []))
    return sc


# ================================================================== BK  50 zł/day vs his high-ticket campaigns — the bar leaves the frame
def scene_BK():
    sc = new("BK_Skala", 1629.70, 1639.45)
    sc.apple_bg()
    w = sc.word
    WIEK, HIGH, KIL, DZIEN, SKALI = w(1629.72), w(1633.58), w(1635.14), w(1636.80), w(1638.60)
    BASE = 900
    WG = sc.group(100, "World", None, 960, 540, 960, 540)
    sc.rect(101, "Floor", WG, 300, BASE, 1320, 3, A_LINE)
    sm = sc.rect(102, "Small", WG, 460, BASE - 8, 200, 8, A_GREY, r=4, ax=100, ay=8)
    sc.k(sm, "scaleY", [(0, f(0), LIN), (WIEK - 100, f(0), HOLD), (WIEK + 500, f(100), OUT)])
    sl = sc.text(103, "Small lab", WG, 560, BASE - 40, "Ten test: 50 zł / dzień", 30, A_GREY, style="Medium", just="center", op=0)
    fade(sc, sl, WIEK, d_in=240)
    BH = 2600
    big = sc.rect(104, "Big", WG, 1200, BASE - BH, 220, BH, A_BLUE, r=24, ax=110, ay=BH)
    sc.k(big, "scaleY", [(0, f(0.4), LIN), (KIL - 200, f(0.4), HOLD), (DZIEN + 900, f(100), INOUT)])
    bl = sc.group(105, "Big label", WG, 1310, BASE - 60, 1310, BASE - 60, op=0)
    sc.text(106, "Big lab", bl, 1350, BASE - 50, "Moje kampanie high-ticket", 30, A_INK, style="Medium")
    sc.text(107, "Big lab2", bl, 1350, BASE - 14, "kilkanaście–kilkadziesiąt tys. zł / dzień", 26, A_BLUE, style="Medium")
    fade(sc, bl, HIGH - 100, d_in=240)
    sc.k(bl, "positionY", [(0, f(BASE - 60), LIN), (KIL - 200, f(BASE - 60), HOLD), (DZIEN + 900, f(BASE - BH - 20), INOUT)])
    # camera: follow the top of the bar, then pull back to show the scale
    S = 0.33
    P_end = 540 - ((BASE - BH / 2) - 540) * S
    sc.k(WG, "positionY", [(0, f(540), LIN), (KIL - 200, f(540), HOLD), (DZIEN + 900, f(540 + (BH - 700)), INOUT),
                           (SKALI - 1, f(540 + (BH - 700)), HOLD), (SKALI + 900, f(P_end), APPLE)])
    scale_keys(sc, WG, [(0, f(100), LIN), (SKALI - 1, f(100), HOLD), (SKALI + 900, f(S * 100), APPLE)])
    return sc


# ================================================================== BL  7 × 50 zł = 350 zł ... not 10 000 zł for a screenshot
def scene_BL():
    sc = new("BL_Budzet-tygodnia", 1648.20, 1657.55)
    sc.apple_bg()
    w = sc.word
    BUD, P50, T350, NIEZ, DZIES, FAJ, SHOT = w(1648.42), w(1649.28), w(1651.40), w(1652.46), w(1653.14), w(1656.40), w(1656.68)
    W1 = sc.group(100, "Week", None, 960, 540, 960, 540)
    hd = sc.text(101, "Head", W1, 960, 250, "Budżet: 50 zł dziennie", 60, A_INK, tracking=-25, just="center", op=0)
    fade(sc, hd, BUD, d_in=240)
    days = ["wt 15", "śr 16", "czw 17", "pt 18", "sob 19", "nd 20", "pn 21"]
    clicks = []
    for i, d in enumerate(days):
        x = 960 + (i - 3) * 190
        sc.rect(110 + i * 4, "Slot", W1, x - 70, 420, 140, 260, A_FILL, r=28)
        sc.text(111 + i * 4, "Day", W1, x, 730, d, 24, A_GREY, style="Medium", just="center")
        cg = sc.group(112 + i * 4, "Coin", W1, x, 600, x, 600, op=0)
        sc.rect(113 + i * 4, "Coin", cg, x - 50, 550, 100, 100, GOLD, r=50, stroke=(GOLD_D, 4))
        sc.text(140 + i, "50", cg, x, 614, "50", 36, GOLD_D, just="center")
        t = P50 + 150 + i * 190
        sc.k(cg, "opacity", [(0, f(0), LIN), (t, f(0), HOLD), (t + 80, f(100), SOFT)])
        sc.k(cg, "positionY", [(0, f(360), LIN), (t, f(360), HOLD), (t + 420, f(600), IN)])
        clicks.append(t + 420)
    tot = sc.text(150, "Total", W1, 960, 870, "0 zł", 80, A_INK, tracking=-30, just="center", op=0)
    tk = [(0, s("0 zł"), LIN)] + [(c, s(f"{(n + 1) * 50} zł"), HOLD) for n, c in enumerate(clicks)]
    sc.k(tot, "textContent", tk)
    fade(sc, tot, clicks[0] - 200, d_in=160)
    sc.k(tot, "fillColor", [(0, col(A_INK), LIN), (T350, col(A_INK), HOLD), (T350 + 200, col(A_GREEN), SOFT)])
    wk = sc.text(151, "Per week", W1, 960, 920, "maksymalnie na cały tydzień", 28, A_GREY, style="Medium", just="center", op=0)
    fade(sc, wk, T350 + 100, d_in=200)
    sc.k(W1, "opacity", [(0, f(100), LIN), (DZIES - 100, f(100), HOLD), (DZIES + 300, f(25), SOFT)])
    scale_keys(sc, W1, [(0, f(100), LIN), (DZIES - 100, f(100), HOLD), (DZIES + 600, f(92), APPLE)])
    # the 10k "for a screenshot" budget
    BG_ = sc.group(160, "10k", None, 960, 540, 960, 540, op=0)
    card_bg(sc, 161, BG_, 560, 380, 800, 320, r=44, sh=(0.18, 70, 20))
    sc.text(162, "K", BG_, 960, 460, "Budżet „pod screenshot”", 30, A_GREY, style="Medium", just="center")
    big = sc.text(163, "V", BG_, 960, 600, "10 000 zł", 130, A_INK, tracking=-50, just="center")
    stw = adv("10 000 zł", 130, "SemiBold") * 0.95
    st = sc.rect(164, "Strike", BG_, 960 - stw / 2, 560, 0.01, 10, A_RED, r=5)
    sc.k(st, "rectSize", [(0, v2(0.01, 10), LIN), (SHOT + 500, v2(0.01, 10), HOLD), (SHOT + 900, v2(stw, 10), APPLE)])
    card_in(sc, BG_, DZIES, sc.dur)
    flash = sc.rect(170, "Flash", None, 0, 0, W, H, A_BG, op=0)
    sc.k(flash, "opacity", [(0, f(0), LIN), (SHOT, f(0), HOLD), (SHOT + 40, f(90), LIN), (SHOT + 320, f(0), SOFT)])
    TH = sc.group(171, "Thumb", None, 250, 890, 250, 890, op=0)
    tb = sc.rect(172, "Thumb", TH, 130, 820, 240, 140, A_BG, r=16, stroke=(A_BG, 6))
    sc.shadow(tb, 0.25, 30, 10)
    sc.rect(173, "Thumb k", TH, 150, 850, 90, 10, A_LINE, r=5)
    sc.text(174, "Thumb v", TH, 150, 910, "+10 000 zł", 30, A_GREEN)
    sc.k(TH, "opacity", [(0, f(0), LIN), (SHOT + 120, f(0), HOLD), (SHOT + 250, f(100), SOFT)])
    scale_keys(sc, TH, [(0, f(250), LIN), (SHOT + 120, f(250), HOLD), (SHOT + 650, f(100), APPLE)])
    sc.kpos(TH, [(0, 960, 540, LIN), (SHOT + 120, 960, 540, HOLD), (SHOT + 650, 250, 890, APPLE)])
    sc.clicks = clicks
    return sc


# ================================================================== BM  the spec sheet (empty values — filled in BW)
def spec_sheet(sc, base, cells, title, t_title):
    """cells = [(abbr, desc, t_in, t_focus, value_keys or None)]; Apple 'tech specs' grid."""
    tl = sc.text(base, "Title", None, 160, 230, title, 64, A_INK, tracking=-30, op=0)
    fade(sc, tl, t_title, d_in=240)
    sc.rect(base + 1, "Rule", None, 160, 280, 1600, 2, A_LINE, op=0)
    fade(sc, base + 1, t_title + 100, d_in=300)
    n = len(cells)
    cw = 1600 / n
    focus_ts = [c[3] for c in cells]
    out = []
    for i, (abbr, desc, t_in, t_focus, vkeys) in enumerate(cells):
        x = 160 + i * cw
        g = sc.group(base + 10 + i * 10, abbr, None, x, 480, x, 480, op=0)
        if i:
            sc.rect(base + 11 + i * 10, "Sep", g, x - 1, 330, 2, 440, A_LINE)
        ab = sc.text(base + 12 + i * 10, "Abbr", g, x + 40, 450, abbr, 120, A_INK, tracking=-50)
        ds_ = sc.text(base + 13 + i * 10, "Desc", g, x + 44, 510, desc, 26, A_GREY, style="Medium", op=0)
        vl = sc.text(base + 14 + i * 10, "Value", g, x + 44, 680, "—", 60, A_LINE, tracking=-20)
        if vkeys:
            sc.k(vl, "textContent", vkeys[0])
            sc.k(vl, "fillColor", vkeys[1])
        fade(sc, g, t_in - 60, d_in=220)
        sc.k(g, "positionY", [(0, f(510), LIN), (t_in - 60, f(510), HOLD), (t_in + 550, f(480), OUT)])
        if t_focus:
            sc.k(ds_, "opacity", [(0, f(0), LIN), (t_focus - 60, f(0), HOLD), (t_focus + 200, f(100), SOFT)])
        else:
            sc.k(ds_, "opacity", [(0, f(0), LIN), (t_in, f(0), HOLD), (t_in + 200, f(100), SOFT)])
        # focus: the explained metric goes blue, the others step back
        ck = [(0, col(A_INK), LIN)]
        for j, ft in enumerate(focus_ts):
            if not ft or ft - 1 <= ck[-1][0]:
                continue
            ck += [(ft - 1, ck[-1][1], HOLD), (ft + 200, col(A_BLUE if j == i else a(A_INK, 0.35)), SOFT)]
        sc.k(ab, "fillColor", ck)
        out.append((g, vl, x))
    return out


def scene_BM():
    sc = new("BM_Liczby", 1662.60, 1674.30)
    sc.apple_bg()
    w = sc.word
    LIC, CTR, CPC, CAC = w(1663.52), w(1664.06), w(1664.58), w(1665.14)
    CTR2, CPC2, CAC2, NAJ, CPA = w(1665.84), w(1667.56), w(1669.12), w(1672.26), w(1673.08)
    cells = [("CTR", "ile osób klika w reklamę", CTR, CTR2, None), ("CPC", "koszt jednego kliknięcia", CPC, CPC2, None),
             ("CAC", "koszt pozyskania klienta", CAC, CAC2, None), ("CPA", "koszt jednego zakupu", NAJ + 300, CPA, None)]
    res = spec_sheet(sc, 100, cells, "Liczby, które śledzę", LIC - 100)
    g, vl, x = res[3]
    bd = sc.group(190, "Most important", None, x + 180, 330, x + 180, 330, op=0)
    pill_text(sc, 191, bd, x + 180, 330, "najważniejsze", 24, A_BG, A_BLUE, style="SemiBold")
    fade(sc, bd, CPA + 100, d_in=160)
    pop(sc, bd, CPA + 100, 450, 60)
    return sc


# ================================================================== BN  Dynamic Island countdown: the last minute (overlay)
def scene_BN():
    sc = new("BN_Ostatnia-minuta", 1694.30, 1705.00)
    FX = overlay(sc)
    w = sc.word
    ZOST = w(1694.54)
    END = sc.dur
    LAST5 = sc.t(1699.90)
    # red edge vignette for the final seconds
    for i, (x, y, ww, hh) in enumerate([(-300, -300, W + 600, 380), (-300, H - 80, W + 600, 380), (-300, -300, 380, H + 600),
                                        (W - 80, -300, 380, H + 600)]):
        v = sc.rect(105 + i, "Vignette", FX, x, y, ww, hh, [1.0, 0.15, 0.1, 0.55], op=0)
        blur(sc, v, 7700 + i, 140)
        kk = [(0, f(0), LIN), (LAST5 - 1, f(0), HOLD)]
        for n in range(5):
            t = LAST5 + n * 1000
            kk += [(t + 1, f(35 + n * 12), OUT), (t + 600, f(15 + n * 8), SOFT)]
        sc.k(v, "opacity", kk)
    PW, PH = 380, 66
    ISL, x0, pill = island(sc, 110, FX, ZOST - 200, END, PW, PH)
    FS = 34
    dig = sc.text(120, "Digits", ISL, x0 + 34, 18 + 45, "0:01:00", FS, A_RED, style="Medium", family="Geist Mono")
    fmt = lambda v: f"0:{int(v) // 60:02d}:{int(v) % 60:02d}"
    keys = [(0, s("0:01:00"), LIN)] + Scene.roll_keys(ZOST + 600, LAST5, fmt, 60, 5.4, fps=14, ease_pow=1.6)
    for n in range(1, 6):
        keys.append((LAST5 + n * 1000, s(fmt(5 - n)), HOLD))
    sc.k(dig, "textContent", keys)
    DX = x0 + 34 + madv("0:00:00", FS) + 28
    for i in range(4):
        colr = A_GREEN if i < 3 else [1, 1, 1, 0.9]
        d = sc.rect(130 + i, "Dot", ISL, DX + i * 26, 18 + PH / 2 - 8, 16, 16, colr, r=8)
        if i == 3:
            kk, t, on = [(0, f(100), LIN)], ZOST, False
            while t < END:
                kk.append((t, f(100 if on else 30), INOUT)); t += 400; on = not on
            sc.k(d, "opacity", kk)
    # heartbeat on each of the last five seconds
    hb = [(0, f(100), LIN), (LAST5 - 1, f(100), HOLD)]
    for n in range(5):
        t = LAST5 + n * 1000
        hb += [(t + 1, f(112 + n * 3), OUT), (t + 350, f(100), SOFT)]
    sc.k(110, "scaleX", [(0, f(40), LIN), (ZOST - 200, f(40), HOLD), (ZOST + 300, f(100), APPLE)] + hb[1:])
    sc.k(110, "scaleY", [(0, f(60), LIN), (ZOST - 200, f(60), HOLD), (ZOST + 300, f(100), APPLE)] + hb[1:])
    sc.clicks = [k[0] for k in keys[1:]][::2] + [LAST5 + n * 1000 for n in range(1, 6)]
    return sc


def island(sc, base, parent, t_in, t_out, width=360, height=64, top=18):   # noqa: F811 (scale handled by caller in BN)
    x0 = 960 - width / 2
    g = sc.group(base, "Island", parent, 960, top + height / 2, 960, top + height / 2, op=0)
    isl = sc.rect(base + 1, "Pill", g, x0, top, width, height, [0.02, 0.02, 0.02, 1], r=height / 2)
    sc.shadow(isl, 0.25, 24, 6)
    sc.k(g, "opacity", [(0, f(0), LIN), (t_in, f(0), HOLD), (t_in + 200, f(100), SOFT), (t_out, f(100), HOLD), (t_out + 250, f(0), SOFT)])
    return g, x0, isl


# ================================================================== BO  the intro timer (#8) rings: 0:00:00
def scene_BO():
    sc = new("BO_Alarm", 1704.80, 1708.15)
    sc.apple_bg()
    CX, CY, D = 960, 440, 680
    G = sc.group(600, "Timer", None, CX, 540, CX, 540)
    sc.ring(601, "Track", G, CX, CY, D, A_LINE, 14)
    ring = sc.ring(602, "Ring", G, CX, CY, D, A_RED, 14)
    sc.text(603, "Digits", G, CX, CY + 44, "0:00:00", 124, A_RED, style="Light", family="Geist Mono", tracking=-30, just="center")
    sc.text(604, "Label", G, CX, CY - 110, "Minutnik", 34, A_GREY, style="Medium", just="center")
    BY = CY + D / 2 + 96
    sc.rect(611, "Cancel bg", G, CX - 330 - 62, BY - 62, 124, 124, A_FILL, r=62)
    sc.text(612, "Cancel", G, CX - 330, BY + 10, "Powtórz", 24, A_GREY, style="Medium", just="center")
    sb = sc.group(615, "Stop", G, CX + 330, BY, CX + 330, BY)
    sc.rect(616, "Stop bg", sb, CX + 330 - 62, BY - 62, 124, 124, A_ORANGE, r=62)
    sc.text(617, "Stop", sb, CX + 330, BY + 10, "Stop", 28, A_BG, just="center")
    # ringing: the ring throbs, waves radiate
    kk, t, on = [(0, f(100), LIN)], 0, True
    while t < sc.dur:
        kk.append((t + 1, f(103 if on else 100), INOUT)); t += 300; on = not on
    scale_keys(sc, G, kk)
    for n in range(6):
        wv = sc.ring(620 + n, "Wave", None, CX, CY, D, A_RED, 6, op=0)
        t0 = n * 550
        sc.k(wv, "opacity", [(0, f(0), LIN), (t0, f(0), HOLD), (t0 + 60, f(60), SOFT), (t0 + 1100, f(0), SOFT)])
        scale_keys(sc, wv, [(0, f(100), LIN), (t0, f(100), HOLD), (t0 + 1100, f(145), OUT)])
    kk, t, on = [(0, f(100), LIN)], 0, True
    while t < sc.dur:
        kk.append((t + 1, f(108 if on else 100), INOUT)); t += 300; on = not on
    scale_keys(sc, sb, kk)
    sh = [(0, f(0), LIN)]
    t = 0
    while t < sc.dur:
        sh += [(t + 1, f(-2), SOFT), (t + 60, f(2), SOFT), (t + 120, f(0), SOFT)]
        t += 600
    sc.k(G, "rotation", sh)
    return sc


# ================================================================== BP  overtime +0:05 → every stage green (overlay)
def scene_BP():
    sc = new("BP_Gotowe", 1710.90, 1719.50)
    FX = overlay(sc)
    w = sc.word
    ZOST, SEK, RZUC, DZIA, GOT = w(1711.14), w(1712.08), w(1714.62), w(1717.08), w(1718.04)
    END = sc.t(1719.20)
    PW, PH = 400, 66
    ISL, x0, pill = island(sc, 110, FX, ZOST - 250, END, PW, PH)
    scale_keys(sc, ISL, [(0, f(60), LIN), (ZOST - 250, f(60), HOLD), (ZOST + 250, f(100), APPLE)])
    sc.k(pill, "rectSize", [(0, v2(PW, PH), LIN), (GOT - 60, v2(PW, PH), HOLD), (GOT + 450, v2(520, PH), APPLE)])
    sc.k(pill, "positionX", [(0, f(x0), LIN), (GOT - 60, f(x0), HOLD), (GOT + 450, f(960 - 260), APPLE)])
    dig = sc.text(120, "Digits", ISL, x0 + 34, 18 + 45, "+0:00", 34, A_RED, style="Medium", family="Geist Mono")
    sc.k(dig, "textContent", [(0, s("+0:00"), LIN)] + [(ZOST + 150 + n * 190, s(f"+0:0{n + 1}"), HOLD) for n in range(5)])
    sc.k(dig, "opacity", [(0, f(100), LIN), (GOT - 60, f(100), HOLD), (GOT + 120, f(0), SOFT)])
    ready = sc.text(121, "Ready", ISL, 960 - 260 + 34, 18 + 44, "Gotowe do sprzedaży", 28, A_BG, op=0)
    fade(sc, ready, GOT + 200, d_in=220)
    DX = x0 + 34 + madv("+0:00", 34) + 40
    names_t = [None, None, DZIA, GOT]
    for i in range(4):
        d = sc.rect(130 + i, "Dot", ISL, DX + i * 30, 18 + PH / 2 - 9, 18, 18, A_GREEN if i < 2 else [1, 1, 1, 0.3], r=9)
        if names_t[i]:
            t = names_t[i]
            sc.k(d, "fillColor", [(0, col([1, 1, 1, 0.3]), LIN), (t - 1, col([1, 1, 1, 0.3]), HOLD), (t + 200, col(A_GREEN), SOFT)])
        sc.k(d, "positionX", [(0, f(DX + i * 30), LIN), (GOT - 60, f(DX + i * 30), HOLD), (GOT + 450, f(960 + 90 + i * 30), APPLE)])
    # stage checklist under the island
    CL = sc.group(150, "Stages", FX, 960, 200, 960, 200, op=0)
    card_bg(sc, 151, CL, 640, 110, 640, 110, r=34, sh=(0.2, 50, 16))
    for i, (nm, t) in enumerate([("Pomysł", RZUC), ("Produkt", RZUC + 150), ("Sklep", DZIA), ("Ruch", GOT)]):
        x = 700 + i * 150
        dd = sc.rect(152 + i * 3, "Dot", CL, x, 152, 26, 26, A_LINE, r=13)
        sc.k(dd, "fillColor", [(0, col(A_LINE), LIN), (t - 1, col(A_LINE), HOLD), (t + 200, col(A_GREEN), SOFT)])
        ck = check(sc, 153 + i * 3, CL, x + 13, 166, 10, A_BG, 3, op=0)
        fade(sc, ck, t + 100, d_in=120)
        sc.text(154 + i * 3, "Name", CL, x + 36, 174, nm, 24, A_INK, style="Medium")
    card_in(sc, CL, RZUC - 250, END)
    return sc


# ================================================================== BQ  a week passes: 15 → 22 September
def scene_BQ():
    sc = new("BQ_Tydzien-pozniej", 1719.50, 1722.75)
    sc.apple_bg()
    w = sc.word
    TYD = w(1720.36)
    C = sc.group(100, "Calendar", None, 960, 560, 960, 560, op=0)
    card_bg(sc, 101, C, 510, 190, 900, 760, r=44, sh=(0.14, 80, 24))
    sc.text(102, "Month", C, 570, 280, "Wrzesień", 56, A_INK, tracking=-25)
    sc.text(103, "Year", C, 1350, 280, "2026", 40, A_RED, just="right")
    for i, d in enumerate(["pn", "wt", "śr", "cz", "pt", "sb", "nd"]):
        sc.text(104 + i, "Dow", C, 600 + i * 120, 350, d, 22, A_GREY, style="Medium", just="center")
    lid = 120
    for day in range(1, 31):
        idx = day + 0                 # 1 Sept 2026 = Tuesday → column 1
        col_, row = idx % 7, idx // 7
        x, y = 600 + col_ * 120, 420 + row * 100
        on = 15 <= day <= 22
        if on:
            t = 200 + (day - 15) * 140
            hl = sc.rect(lid, "Hl", C, x - 40, y - 42, 80, 80, A_BLUE, r=40, ax=40, ay=40, op=0)
            sc.k(hl, "opacity", [(0, f(0), LIN), (t, f(0), HOLD), (t + 120, f(100), SOFT)])
            scale_keys(sc, hl, [(0, f(40), LIN), (t, f(40), HOLD), (t + 350, f(100), OUT)])
            dt = sc.rect(lid + 1, "Ad dot", C, x - 4, y + 22, 8, 8, A_BG, r=4, op=0)
            fade(sc, dt, t + 150, d_in=100)
        tx = sc.text(lid + 2, "Day", C, x, y + 10, str(day), 30, A_INK, style="Medium", just="center")
        if on:
            sc.k(tx, "fillColor", [(0, col(A_INK), LIN), (t, col(A_INK), HOLD), (t + 120, col(A_BG), SOFT)])
        lid += 3
    fade(sc, C, 1, d_in=200)
    scale_keys(sc, C, [(0, f(96), LIN), (1, f(96), HOLD), (600, f(100), OUT)])
    lb = sc.group(200, "Label", None, 960, 110, 960, 110, op=0)
    sc.text(201, "L", lb, 960, 130, "7 dni później", 64, A_INK, tracking=-30, just="center")
    fade(sc, lb, 200 + 7 * 140, d_in=260)
    pop(sc, lb, 200 + 7 * 140, 550, 85)
    return sc


# ================================================================== BR  expectation: ~600 zł (ghost bars, overlay)
def scene_BR():
    sc = new("BR_Oczekiwanie", 1728.60, 1738.25)
    FX = overlay(sc)
    w = sc.word
    SPO, ROAS, P350, P600, P250 = w(1728.80), w(1731.00), w(1732.96), w(1734.94), w(1737.06)
    END = sc.t(1737.95)
    X0, CW = 1220, 620
    C = sc.group(110, "Expectation", FX, X0 + CW / 2, 330, X0 + CW / 2, 330, op=0)
    card_bg(sc, 111, C, X0, 110, CW, 470, r=40, sh=(0.2, 60, 18))
    sc.text(112, "K", C, X0 + 40, 172, "OCZEKIWANIE", 18, A_GREY, style="Medium", family="Geist Mono", tracking=140)
    rt = sc.text(113, "ROAS", C, X0 + 40, 240, "ROAS 1,5–2×", 50, A_INK, tracking=-20, op=0)
    fade(sc, rt, ROAS, d_in=200)
    rows = [("Reklamy", 350, P350, A_GREY, False), ("Przychód", 600, P600, A_BLUE, True), ("Zysk", 250, P250, A_GREEN, True)]
    for i, (nm, v, t, colr, ghost) in enumerate(rows):
        y = 300 + i * 90
        sc.text(120 + i * 5, "Name", C, X0 + 40, y + 30, nm, 26, A_INK, style="Medium", op=0)
        wd = v / 700 * 360
        bar = sc.rect(121 + i * 5, "Bar", C, X0 + 190, y + 6, wd, 34, a(colr, 0.12) if ghost else colr, r=10,
                      stroke=(colr, 2.5) if ghost else None, ax=0)
        sc.k(bar, "scaleX", [(0, f(0), LIN), (t - 60, f(0), HOLD), (t + 550, f(100), OUT)])
        vl = sc.text(122 + i * 5, "Val", C, X0 + 190 + wd + 14, y + 32, ("~" if ghost else "") + f"{v} zł", 26, colr, op=0)
        for lid in (120 + i * 5, 122 + i * 5):
            sc.k(lid, "opacity", [(0, f(0), LIN), (t, f(0), HOLD), (t + 250, f(100), SOFT)])
    card_in(sc, C, SPO, END)
    return sc


# ================================================================== BS_a  the intro's blurred results — revenue unblurs
def scene_BS_a():
    sc = new("BS_a_Przychod", 1760.80, 1769.90)
    sc.apple_bg()
    w = sc.word
    DATES, P931 = w(1763.10), w(1765.82)
    result_columns(sc, 1000, {0: (P931, "931 zł", A_INK)})
    dg = sc.group(1100, "Dates", None, 960, 250, 960, 250, op=0)
    pill_text(sc, 1101, dg, 960, 250, "15–22 września", 30, A_INK, A_FILL, style="SemiBold")
    fade(sc, dg, DATES - 60, d_in=200)
    pop(sc, dg, DATES - 60, 450, 80)
    return sc


# ================================================================== BT  ROAS: 931 ÷ 350 = 2,63×, then 1 zł → 2,66 zł
def scene_BT():
    sc = new("BT_ROAS", 1773.60, 1783.25)
    sc.apple_bg()
    w = sc.word
    P350, P931, R263, KAZ, R266, POW = w(1774.60), w(1776.04), w(1777.66), w(1779.70), w(1781.34), w(1782.78)
    EQ = sc.group(100, "Equation", None, 960, 500, 960, 500)
    items = [(470, "Przychód", "931 zł", A_GREEN, P931), (820, "", "÷", A_GREY, P931 + 150), (1080, "Reklamy", "350 zł", A_INK, P350),
             (1320, "", "=", A_GREY, R263 - 200), (1580, "ROAS", "0,00×", A_BLUE, R263)]
    for i, (x, lab, val, colr, t) in enumerate(items):
        g = sc.group(110 + i * 4, lab or val, EQ, x, 520, x, 520, op=0)
        if lab:
            sc.text(111 + i * 4, "Lab", g, x, 420, lab, 30, A_GREY, style="Medium", just="center")
        tx = sc.text(112 + i * 4, "Val", g, x, 560, val, 110 if lab else 90, colr, tracking=-40, just="center")
        if lab == "ROAS":
            sc.k(tx, "textContent", [(0, s("0,00×"), LIN)] + Scene.roll_keys(R263, R263 + 700, lambda v: f"{v:.2f}×".replace(".", ","), 0, 2.63)[1:])
        fade(sc, g, t - 60, d_in=220)
        pop(sc, g, t - 60, 550, 85)
    sc.k(EQ, "opacity", [(0, f(100), LIN), (KAZ - 100, f(100), HOLD), (KAZ + 400, f(30), SOFT)])
    scale_keys(sc, EQ, [(0, f(100), LIN), (KAZ - 100, f(100), HOLD), (KAZ + 600, f(62), APPLE)])
    sc.k(EQ, "positionY", [(0, f(500), LIN), (KAZ - 100, f(500), HOLD), (KAZ + 600, f(300), APPLE)])

    def coin(base, cx, cy, txt, d=180):
        g = sc.group(base, "Coin " + txt, None, cx, cy, cx, cy, op=0)
        sc.rect(base + 1, "Coin", g, cx - d / 2, cy - d / 2, d, d, GOLD, r=d / 2, stroke=(GOLD_D, 6))
        sc.text(base + 2, "Txt", g, cx, cy + d * 0.14, txt, d * 0.3, GOLD_D, just="center", tracking=-20)
        return g
    c1 = coin(200, 640, 700, "1 zł")
    fade(sc, c1, KAZ, d_in=200)
    pop(sc, c1, KAZ, 500, 70)
    ar = sc.path(210, "Arrow", None, [(790, 700), (1020, 700)], 0, 0, stroke=(A_GREY, 6), closed=False, trim=0)
    sc.k(ar, "trimEnd", [(0, f(0), LIN), (KAZ + 600, f(0), HOLD), (R266 - 100, f(100), OUT)])
    sc.path(211, "Head", None, [(1000, 682), (1022, 700), (1000, 718)], 0, 0, stroke=(A_GREY, 6), closed=False, op=0)
    fade(sc, 211, R266 - 150, d_in=100)
    for n in range(3):
        g = coin(220 + n * 5, 1180 + n * 40, 700 - n * 26, "", d=180)
        fade(sc, g, R266 + n * 110, d_in=150)
        sc.k(g, "positionY", [(0, f(560), LIN), (R266 + n * 110, f(560), HOLD), (R266 + n * 110 + 400, f(700 - n * 26), IN)])
    tv = sc.text(240, "Back", None, 1260, 890, "2,66 zł", 90, A_GREEN, tracking=-35, just="center", op=0)
    fade(sc, tv, R266 + 350, d_in=200)
    sc.text(241, "Back s", None, 1260, 940, "wraca z każdej złotówki", 28, A_GREY, style="Medium", just="center", op=0)
    fade(sc, 241, POW - 200, d_in=200)
    return sc


# ================================================================== BS_b  profit unblurs (sales stay hidden until the funnel)
def scene_BS_b():
    sc = new("BS_b_Na-czysto", 1784.60, 1789.30)
    sc.apple_bg()
    w = sc.word
    NA300, P581 = w(1785.20), w(1786.68)
    result_columns(sc, 1000, {0: (1, "931 zł", A_INK), 2: (P581, "+581 zł", A_GREEN)}, seed=11)
    sub = sc.text(1100, "Math", None, 1480, 640, "931 − 350", 32, A_GREY, style="Medium", family="Geist Mono", just="center", op=0)
    fade(sc, sub, P581 + 200, d_in=220)
    return sc


# ================================================================== BU  the intro timer ring → 193 zł per hour
def scene_BU():
    sc = new("BU_Na-godzine", 1789.10, 1792.75)
    sc.apple_bg()
    w = sc.word
    TRZY, P193 = w(1790.18), w(1790.98)
    CX, CY, D = 960, 470, 680
    G = sc.group(600, "Timer", None, CX, 540, CX, 540)
    sc.ring(601, "Track", G, CX, CY, D, A_LINE, 14)
    pr = sc.ring(602, "Progress", G, CX, CY, D, A_GREEN, 14, trim_end=0)
    sc.k(pr, "trimEnd", [(0, f(0), LIN), (TRZY - 400, f(0), HOLD), (P193 - 50, f(100), INOUT)])
    dg = sc.text(603, "Digits", G, CX, CY + 44, "3:00:00", 124, A_INK, style="Light", family="Geist Mono", tracking=-30, just="center")
    sc.k(dg, "opacity", [(0, f(100), LIN), (P193 - 150, f(100), HOLD), (P193 + 50, f(0), SOFT)])
    lb = sc.text(604, "Lab", G, CX, CY - 110, "3 godziny pracy", 34, A_GREY, style="Medium", just="center")
    sc.k(lb, "textContent", [(0, s("3 godziny pracy"), LIN), (P193, s("na godzinę"), HOLD)])
    vg = sc.group(610, "Value", G, CX, CY, CX, CY, op=0)
    sc.text(611, "V", vg, CX, CY + 50, "193 zł", 150, A_GREEN, tracking=-60, just="center")
    fade(sc, vg, P193, d_in=200)
    pop(sc, vg, P193, 550, 80)
    fade(sc, G, 40, d_in=200)
    return sc


# ================================================================== BV  expected 500–600 zł → the real 931 zł breaks through
def scene_BV():
    sc = new("BV_Ponad-oczekiwania", 1794.30, 1800.70)
    sc.apple_bg()
    w = sc.word
    SPO, P500, P600, P900, NIE = w(1794.38), w(1795.90), w(1797.12), w(1798.48), w(1799.52)
    BASE, K = 900, 0.62
    sc.rect(100, "Floor", None, 460, BASE, 1000, 3, A_LINE)
    # expectation (ghost)
    gh = sc.rect(101, "Ghost", None, 590, BASE - 600 * K, 240, 600 * K, a(A_GREY, 0.08), r=24, stroke=(A_GREY, 3), ax=120, ay=600 * K, op=0)
    band = sc.rect(102, "Band", None, 590, BASE - 600 * K, 240, 100 * K, a(A_GREY, 0.18), r=12, op=0)
    sc.k(gh, "opacity", [(0, f(0), LIN), (P500 - 100, f(0), HOLD), (P500 + 200, f(100), SOFT)])
    sc.k(gh, "scaleY", [(0, f(0), LIN), (P500 - 100, f(0), HOLD), (P600 + 300, f(100), OUT)])
    fade(sc, band, P600 + 200, d_in=250)
    gl = sc.text(103, "Ghost lab", None, 710, BASE - 600 * K - 30, "500–600 zł", 36, A_GREY, just="center", op=0)
    fade(sc, gl, P600, d_in=220)
    sc.text(104, "Ghost name", None, 710, BASE + 60, "Oczekiwanie", 32, A_GREY, style="Medium", just="center", op=0)
    fade(sc, 104, SPO, d_in=220)
    line = sc.rect(105, "Exp line", None, 460, BASE - 600 * K, 1000, 2, a(A_GREY, 0.5), op=0)
    fade(sc, line, P600 + 300, d_in=250)
    # reality
    rb = sc.rect(110, "Real", None, 1090, BASE - 931 * K, 240, 931 * K, A_GREEN, r=24, ax=120, ay=931 * K)
    sc.k(rb, "scaleY", [(0, f(0), LIN), (P900 - 200, f(0), HOLD), (P900 + 900, f(100), OUT)])
    rl = sc.text(111, "Real lab", None, 1210, BASE - 931 * K - 30, "931 zł", 48, A_GREEN, just="center", op=0)
    fade(sc, rl, P900 + 500, d_in=200)
    sc.text(112, "Real name", None, 1210, BASE + 60, "Wynik", 32, A_INK, style="Medium", just="center", op=0)
    fade(sc, 112, P900 - 200, d_in=200)
    bu = sc.group(113, "Over", None, 1210, BASE - 600 * K, 1210, BASE - 600 * K, op=0)
    pill_text(sc, 114, bu, 1400, BASE - 600 * K, "+55% ponad plan", 26, A_BG, A_GREEN, style="SemiBold")
    fade(sc, bu, NIE, d_in=160)
    pop(sc, bu, NIE, 420, 70)
    return sc


# ================================================================== BW  results sheet (the BM sheet, now with real values)
def scene_BW():
    sc = new("BW_Wyniki-liczby", 1817.10, 1827.00)
    sc.apple_bg()
    w = sc.word
    CONV, R537, WYS, CPM, NORM, CPC, R094 = w(1817.22), w(1818.16), w(1819.28), w(1820.64), w(1822.02), w(1823.30), w(1824.70)
    pct = lambda v: f"{v:.2f}%".replace(".", ",")
    cells = [("CR", "konwersja strony", CONV, CONV,
              ([(0, s("—"), LIN)] + Scene.roll_keys(R537 - 200, R537 + 600, pct, 0, 5.37)[0:], [(0, col(A_LINE), LIN), (R537 - 201, col(A_LINE), HOLD), (R537 - 200, col(A_INK), HOLD)])),
             ("CPM", "koszt 1000 wyświetleń", CPM, CPM,
              ([(0, s("—"), LIN), (NORM, s("w normie"), HOLD)], [(0, col(A_LINE), LIN), (NORM - 1, col(A_LINE), HOLD), (NORM, col(A_INK), HOLD)])),
             ("CPC", "koszt jednego kliknięcia", CPC, CPC,
              ([(0, s("—"), LIN)] + Scene.roll_keys(R094 - 150, R094 + 500, lambda v: f"{v:.2f} zł".replace(".", ","), 0, 0.94)[0:],
               [(0, col(A_LINE), LIN), (R094 - 151, col(A_LINE), HOLD), (R094 - 150, col(A_INK), HOLD)]))]
    res = spec_sheet(sc, 100, cells, "Liczby po tygodniu", 60)
    g, vl, x = res[0]
    bd = sc.group(190, "High", None, x + 200, 330, x + 200, 330, op=0)
    pill_text(sc, 191, bd, x + 200, 330, "bardzo wysoka", 24, A_BG, A_GREEN, style="SemiBold")
    fade(sc, bd, WYS, d_in=160)
    pop(sc, bd, WYS, 450, 60)
    return sc


# ================================================================== BX  the funnel, real numbers (overlay; callback to BG)
def scene_BX():
    sc = new("BX_Lejek-wyniki", 1827.00, 1848.60)
    FX = overlay(sc)
    w = sc.word
    stages = [("Wyświetlenia", 18200, w(1827.96), "18 200"), ("CTR", 2.04, w(1830.16), "2,04%"),
              ("Strona", 354, w(1832.84), "354"), ("Koszyk", 63, w(1836.58), "63"), ("Checkout", 44, w(1839.96), "44"),
              ("Płatność", 36, w(1841.70), "36"), ("Zakup", 19, w(1842.86), "19")]
    ZWI = w(1845.10)
    END = sc.t(1848.30)
    B = sc.group(110, "Band", FX, 960, 900, 960, 900, op=0)
    card_bg(sc, 111, B, 70, 770, 1780, 250, r=40, sh=(0.2, 60, 18))
    card_in(sc, B, stages[0][2] - 700, END)
    xs = [70 + 127 + i * 254 for i in range(7)]
    widths = [210, 170, 150, 110, 95, 88, 70]
    for i, (nm, v, t, txt) in enumerate(stages):
        g = sc.group(120 + i * 6, nm, B, xs[i], 900, xs[i], 900, op=0)
        sc.text(121 + i * 6, "Name", g, xs[i], 830, nm, 24, A_GREY, style="Medium", just="center")
        num = sc.text(122 + i * 6, "Num", g, xs[i], 900, txt, 56, A_GREEN if nm == "Zakup" else A_INK, tracking=-25, just="center")
        if nm not in ("CTR",):
            fmtn = (lambda vv: f"{int(vv):,}".replace(",", " "))
            sc.k(num, "textContent", [(0, s("0"), LIN)] + Scene.roll_keys(t, t + 600, fmtn, 0, v)[0:])
        bar = sc.rect(123 + i * 6, "Width", g, xs[i] - widths[i] / 2, 944, widths[i], 12, A_GREEN if nm == "Zakup" else A_BLUE, r=6)
        fade(sc, g, t - 60, d_in=200)
        pop(sc, g, t - 60, 500, 85)
        if i:
            ln = sc.rect(160 + i, "Link", B, xs[i - 1] + 105, 949, 0.01, 3, A_LINE, r=1.5)
            sc.k(ln, "rectSize", [(0, v2(0.01, 3), LIN), (t - 300, v2(0.01, 3), HOLD), (t, v2(44, 3), OUT)])
    # the leak between payment and purchase
    lk = sc.group(170, "Leak", B, (xs[5] + xs[6]) / 2, 800, (xs[5] + xs[6]) / 2, 800, op=0)
    pill_text(sc, 171, lk, (xs[5] + xs[6]) / 2, 800, "−47%", 24, A_BG, A_RED, style="SemiBold")
    fade(sc, lk, ZWI, d_in=160)
    pop(sc, lk, ZWI, 450, 60)
    hl = sc.rect(172, "Leak hl", B, xs[5] - 120, 790, 374, 220, [1, 1, 1, 0], r=30, stroke=(A_RED, 3), op=0)
    fade(sc, hl, ZWI, d_in=200)
    return sc


# ================================================================== BY  16 of 19 buyers opened the e-book (overlay)
def scene_BY():
    sc = new("BY_Otwarcia", 1851.60, 1855.50)
    FX = overlay(sc)
    w = sc.word
    P16, OTW, P3 = w(1851.70), w(1852.94), w(1854.06)
    END = sc.t(1855.20)
    X0, CW = 1240, 600
    C = sc.group(110, "Opens", FX, X0 + CW / 2, 330, X0 + CW / 2, 330, op=0)
    card_bg(sc, 111, C, X0, 120, CW, 420, r=40, sh=(0.2, 60, 18))
    hd = sc.text(112, "Head", C, X0 + 40, 196, "0 z 19", 60, A_INK, tracking=-25)
    sc.k(hd, "textContent", [(0, s("0 z 19"), LIN)] + [(P16 + n * 70, s(f"{n + 1} z 19"), HOLD) for n in range(16)])
    sc.text(113, "Sub", C, X0 + 40, 236, "kupujących otworzyło e-booka", 24, A_GREY, style="Medium")
    for i in range(19):
        c, r_ = i % 10, i // 10
        x, y = X0 + 44 + c * 52, 290 + r_ * 110
        bk = sc.rect(120 + i, "Book", C, x, y, 40, 56, A_LINE, r=6)
        if i < 16:
            t = P16 + i * 70
            sc.k(bk, "fillColor", [(0, col(A_LINE), LIN), (t, col(A_LINE), HOLD), (t + 150, col(A_BLUE), SOFT)])
        else:
            sc.k(bk, "fillColor", [(0, col(A_LINE), LIN), (P3, col(A_LINE), HOLD), (P3 + 200, col(a(A_ORANGE, 0.6)), SOFT)])
    ng = sc.group(150, "Not yet", C, X0 + 470, 500, X0 + 470, 500, op=0)
    pill_text(sc, 151, ng, X0 + 470, 500, "3 jeszcze nie", 22, A_ORANGE, a(A_ORANGE, 0.12), style="SemiBold")
    fade(sc, ng, P3 + 150, d_in=160)
    card_in(sc, C, P16 - 300, END)
    return sc


# ================================================================== BZ  BLIK code, payment accepted (overlay)
def scene_BZ():
    sc = new("BZ_BLIK", 1866.40, 1871.30)
    FX = overlay(sc)
    w = sc.word
    WIEK, BLIK, FAJ = w(1866.48), w(1867.98), w(1870.66)
    END = sc.t(1871.00)
    X0, CW = 1240, 600
    C = sc.group(110, "BLIK", FX, X0 + CW / 2, 360, X0 + CW / 2, 360, op=0)
    card_bg(sc, 111, C, X0, 160, CW, 400, r=40, sh=(0.2, 60, 18))
    sc.text(112, "K", C, X0 + 40, 226, "Kod BLIK", 32, A_INK, tracking=-10)
    sc.text(113, "S", C, X0 + 40, 262, "najczęstsza forma płatności", 22, A_GREY, style="Medium")
    code = "482913"
    for i, ch in enumerate(code):
        x = X0 + 40 + i * 88 + (20 if i > 2 else 0)
        sc.rect(120 + i * 3, "Box", C, x, 300, 72, 92, A_FILL, r=16)
        d = sc.text(121 + i * 3, "Digit", C, x + 36, 364, ch, 48, A_INK, style="Medium", family="Geist Mono", just="center", op=0)
        t = WIEK + 300 + i * 150
        fade(sc, d, t, d_in=80)
    okg = sc.group(150, "Paid", C, X0 + CW / 2, 470, X0 + CW / 2, 470, op=0)
    sc.rect(151, "Paid bg", okg, X0 + 40, 440, CW - 80, 64, a(A_GREEN, 0.14), r=32)
    check(sc, 152, okg, X0 + 90, 473, 14, A_GREEN, 4)
    sc.text(153, "Paid t", okg, X0 + 120, 482, "Płatność przyjęta", 28, [0.1, 0.5, 0.2, 1])
    fade(sc, okg, BLIK, d_in=180)
    pop(sc, okg, BLIK, 450, 85)
    card_in(sc, C, WIEK - 200, END)
    sc.clicks = [WIEK + 300 + i * 150 for i in range(6)]
    return sc


# ================================================================== CA  receipt reprise (callback to AN) + first link
def scene_CA_a():
    sc = new("CA_a_Za-darmo", 1889.80, 1896.35)
    sc.apple_bg()
    w = sc.word
    DARMO, BASE44, FUND = w(1890.04), w(1891.60), w(1894.84)
    R = sc.group(100, "Receipt", None, 960, 540, 960, 540, op=0)
    X0, X1, Y0, Y1 = 590, 1330, 110, 1000
    paper = sc.rect(101, "Paper", R, X0, Y0, X1 - X0, Y1 - Y0, A_BG, r=10)
    sc.shadow(paper, 0.14, 50, 18)
    teeth = [(X0, Y1 - 2)]
    for i in range(18):
        teeth += [(X0 + (i + 0.5) * (X1 - X0) / 18, Y1 + 18), (X0 + (i + 1) * (X1 - X0) / 18, Y1 - 2)]
    sc.path(102, "Teeth", R, teeth + [(X1, Y1 - 10), (X0, Y1 - 10)], 0, 0, fill=A_BG)
    sc.text(103, "Kicker", R, 960, 222, "PARAGON", 20, A_GREY, style="Medium", family="Geist Mono", just="center", tracking=200)
    sc.text(104, "Title", R, 960, 276, "Kurs + system AI", 40, A_INK, tracking=-15, just="center")
    for i, lab in enumerate(["Kurs", "Mentoring", "Rozmowy coachingowe", "System AI"]):
        y = 380 + i * 52
        sc.text(110 + i * 2, "L", R, X0 + 40, y, lab, 28, A_INK, style="Medium")
        sc.text(111 + i * 2, "R", R, X1 - 40, y, "w cenie", 26, A_GREY, style="Medium", just="right")
    sc.text(130, "L", R, X0 + 40, 650, "Wartość", 28, A_INK, style="Medium")
    sc.text(131, "R", R, X1 - 40, 650, "10 000,00 zł", 28, A_INK, style="Medium", just="right")
    sg = sc.group(140, "Sponsor", R, 0, 0, op=0)
    sc.text(141, "L", sg, X0 + 40, 706, "Sfinansowane przez Base44", 28, A_GREEN, style="Medium")
    sc.text(142, "R", sg, X1 - 40, 706, "−10 000,00 zł", 28, A_GREEN, style="Medium", just="right")
    fade(sc, sg, DARMO - 60, d_in=200)
    sc.text(150, "L", R, X0 + 40, 826, "Do zapłaty", 38, A_INK, tracking=-10)
    zlf = lambda v: f"{int(round(v)):,}".replace(",", " ") + ",00 zł"
    tot = sc.text(151, "R", R, X1 - 40, 826, zlf(10000), 38, A_INK, tracking=-10, just="right")
    sc.k(tot, "textContent", [(0, s(zlf(10000)), LIN)] + Scene.roll_keys(DARMO + 150, DARMO + 850, zlf, 10000, 0)[1:])
    sc.k(tot, "fillColor", [(0, col(A_INK), LIN), (DARMO + 650, col(A_INK), HOLD), (DARMO + 850, col(A_GREEN), SOFT)])
    STP = sc.group(160, "Stamp", R, 960, 925, 960, 925, op=0)
    sc.rect(161, "Box", STP, 820, 885, 280, 80, [1, 1, 1, 0], r=14, stroke=(A_GREEN, 5))
    sc.text(162, "T", STP, 960, 939, "OPŁACONE", 38, A_GREEN, just="center", tracking=80)
    sc.k(STP, "rotation", [(0, f(-9), LIN)])
    sc.k(STP, "opacity", [(0, f(0), LIN), (BASE44 - 60, f(0), HOLD), (BASE44 + 80, f(90), SOFT)])
    scale_keys(sc, STP, [(0, f(150), LIN), (BASE44 - 60, f(150), HOLD), (BASE44 + 200, f(100), IN)])
    fade(sc, R, 20, d_in=200)
    sc.k(R, "positionY", [(0, f(580), LIN), (20, f(580), HOLD), (700, f(540), OUT)])
    return sc


def scene_CA_b():
    return link_scene("CA_b_Pierwszy-link", 1904.50, 1906.55, 1905.12, 1904.65)


# ================================================================== CB  "Raczej nie." + honest footnote
def scene_CB_a():
    sc = new("CB_a_Raczej-nie", 1910.00, 1913.40)
    sc.apple_bg()
    w = sc.word
    Q = [w(1910.16), w(1910.30), w(1910.60), w(1910.80), w(1911.08), w(1911.18), w(1911.34)]
    SZ, RAC, NIE = w(1911.76), w(1912.16), w(1912.58)
    q = sc.text(100, "Q", None, 960, 360, "Czy zrobisz taki wynik w pierwszy tydzień?", 56, A_GREY, tracking=-20, just="center",
                animators=[Scene.reveal_animator(1, 11, dy=18, blur=8)])
    sc.reveal_words(q, 11, Q, step=130)
    sz = sc.text(101, "Sz", None, 960, 470, "Szczerze?", 40, A_GREY, style="Medium", just="center", op=0)
    fade(sc, sz, SZ - 60, d_in=180)
    big = sc.text(102, "Big", None, 960, 680, "Raczej nie.", 180, A_INK, tracking=-70, just="center",
                  animators=[Scene.reveal_animator(2, 21, dy=30, blur=14)])
    sc.reveal_words(big, 21, [RAC, NIE], step=170)
    return sc


def scene_CB_b():
    sc = new("CB_b_Przypis", 1919.60, 1923.35)
    FX = overlay(sc)
    w = sc.word
    GW = w(1919.94)
    END = sc.t(1923.05)
    txt = "¹ Wynik jednego testu, nie obietnica. Wyniki nie są gwarantowane."
    wd = adv(txt, 24, "Medium") + 60
    g = sc.group(110, "Footnote", FX, 80 + wd / 2, 1000, 80 + wd / 2, 1000, op=0)
    sc.rect(111, "Bg", g, 80, 972, wd, 56, [1, 1, 1, 0.92], r=28)
    sc.text(112, "T", g, 110, 1008, txt, 24, A_INK, style="Medium")
    sc.k(g, "opacity", [(0, f(0), LIN), (GW - 100, f(0), HOLD), (GW + 200, f(100), SOFT), (END, f(100), HOLD), (END + 250, f(0), SOFT)])
    sc.k(g, "positionY", [(0, f(1040), LIN), (GW - 100, f(1040), HOLD), (GW + 500, f(1000), OUT)])
    return sc


# ================================================================== CC  best day: 196 zł (overlay)
def scene_CC():
    sc = new("CC_Najlepszy-dzien", 1929.90, 1934.60)
    FX = overlay(sc)
    w = sc.word
    NAJ, P196 = w(1930.06), w(1931.78)
    END = sc.t(1934.30)
    X0, CW = 1240, 600
    C = sc.group(110, "Best day", FX, X0 + CW / 2, 350, X0 + CW / 2, 350, op=0)
    card_bg(sc, 111, C, X0, 130, CW, 440, r=40, sh=(0.2, 60, 18))
    sc.text(112, "K", C, X0 + 40, 196, "Najlepszy dzień", 30, A_GREY)
    v = sc.text(113, "V", C, X0 + 40, 280, "0 zł", 80, A_INK, tracking=-30)
    sc.k(v, "textContent", [(0, s("0 zł"), LIN)] + Scene.roll_keys(P196, P196 + 700, zl, 0, 196)[1:])
    rel = [0.5, 0.72, 1.0, 0.62, 0.68, 0.56, 0.66]
    for i, r_ in enumerate(rel):
        hgt = 200 * r_
        best = r_ == 1.0
        b = sc.rect(120 + i, "Bar", C, X0 + 50 + i * 76, 530 - hgt, 50, hgt, A_GREEN if best else A_LINE, r=10, ax=25, ay=hgt)
        t = NAJ + 200 + i * 80
        sc.k(b, "scaleY", [(0, f(0), LIN), (t, f(0), HOLD), (t + 500, f(100), OUT)])
        if best:
            sc.k(b, "fillColor", [(0, col(A_LINE), LIN), (P196 - 1, col(A_LINE), HOLD), (P196 + 200, col(A_GREEN), SOFT)])
    card_in(sc, C, NAJ - 200, END)
    return sc


BUILD = {"BJ": scene_BJ, "BK": scene_BK, "BL": scene_BL, "BM": scene_BM, "BN": scene_BN, "BO": scene_BO, "BP": scene_BP,
         "BQ": scene_BQ, "BR": scene_BR, "BS_a": scene_BS_a, "BT": scene_BT, "BS_b": scene_BS_b, "BU": scene_BU,
         "BV": scene_BV, "BW": scene_BW, "BX": scene_BX, "BY": scene_BY, "BZ": scene_BZ, "CA_a": scene_CA_a,
         "CA_b": scene_CA_b, "CB_a": scene_CB_a, "CB_b": scene_CB_b, "CC": scene_CC}
OVERLAY.update({"BN", "BP", "BR", "BX", "BY", "BZ", "CA_b", "CB_b", "CC"})

if __name__ == "__main__":
    for key in (sys.argv[1:] or BUILD):
        try:
            BUILD[key]().build(key)
        except SystemExit as e:
            print(f"[{key}] FAILED: {e}")
