#!/usr/bin/env python3
"""ANGLE 4 (angle4.mp4, 1080×1920, 1:31) — Apple-style, face-first: floating cards on the chest (y 1000–1560),
three full-screen key moments. Built on the VSL v2 library (apple.py) switched to vertical.
Usage: scenes_a4.py A01 A02 ...   (no args = all)."""
import sys, os, math, random
sys.path.insert(0, os.path.expanduser("~/.claude/skills/konrad-studio/scripts"))
import apple
HERE = os.environ.get("PROJECT", os.path.dirname(os.path.abspath(__file__)))      # project folder (outputs)
apple.init(HERE, 1080, 1920)
from apple import *

VW, VH = 1080, 1920
SRC = os.path.join(HERE, "..", "angle4.mp4")
WORDS = os.path.join(HERE, "tr", "a4.json")
OVERLAY = set()
X0, CW = 70, 940                     # card column
CY0, CH_ = 1030, 520                 # default card box (chest)


def new(name, a_, b_):
    sc = Scene(name, a_, b_, WORDS, SRC)
    return sc


def ovl(k):
    OVERLAY.add(k)


def vbg(sc):
    """Vertical studio white with two soft glows."""
    sc.bg = A_BG
    sc.layers += [blob(6, -500, -400, 1300, [1.0, 0.90, 0.85, 0.32], dur=sc.dur),
                  blob(7, 380, 1300, 1300, [0.90, 0.93, 1.0, 0.26], dur=sc.dur)]


def card(sc, base, FX, t_in, t_out, y0=CY0, h_=CH_):
    """White floating card on the chest; returns (group, y0)."""
    g = sc.group(base, "Card", FX, X0 + CW / 2, y0 + h_ / 2, X0 + CW / 2, y0 + h_ / 2, op=0)
    card_bg(sc, base + 1, g, X0, y0, CW, h_, r=48, sh=(0.22, 70, 22))
    sc.k(g, "opacity", [(0, f(0), LIN), (t_in, f(0), HOLD), (t_in + 260, f(100), SOFT), (t_out, f(100), HOLD), (t_out + 300, f(0), SOFT)])
    scale_keys(sc, g, [(0, f(92), LIN), (t_in, f(92), HOLD), (t_in + 700, f(100), OUT), (t_out, f(100), HOLD), (t_out + 300, f(96), SOFT)])
    sc.k(g, "positionY", [(0, f(y0 + h_ / 2 + 60), LIN), (t_in, f(y0 + h_ / 2 + 60), HOLD), (t_in + 700, f(y0 + h_ / 2), OUT)])
    return g


def head(sc, lid, g, y0, txt, t=None, color=A_GREY):
    h = sc.text(lid, "Head", g, X0 + 56, y0 + 84, txt, 34, color, style="Medium", op=0 if t else 100)
    if t:
        fade(sc, h, t - 60, d_in=200)
    return h


# ================================================================== A01  everyone uses AI the same way
def A01():
    sc = new("A01_Tak-samo", 0.00, 6.15)
    FX = overlay(sc)
    w = sc.word
    T_ = [w(2.72), w(3.40), w(4.26)]
    OSZ = w(5.54)
    END = sc.t(5.85)
    g = card(sc, 110, FX, sc.t(2.25), END)
    head(sc, 112, g, CY0, "Większość używa AI tak:")
    msgs = ["Napisz maila", "Zrób obrazek", "Odpowiedz na pytanie"]
    for i, (m, t) in enumerate(zip(msgs, T_)):
        y = CY0 + 130 + i * 110
        wd = adv(m, 38) + 64
        b = sc.group(120 + i * 4, m, g, X0 + CW - 50 - wd / 2, y + 40, X0 + CW - 50 - wd / 2, y + 40, op=0)
        sc.rect(121 + i * 4, "Bub", b, X0 + CW - 50 - wd, y, wd, 80, A_BLUE, r=40)
        sc.text(122 + i * 4, "T", b, X0 + CW - 50 - wd + 32, y + 53, m, 38, A_BG, style="Medium")
        fade(sc, b, t - 60, d_in=160)
        pop(sc, b, t - 60, 420, 80)
    ch = sc.group(140, "Saved", g, X0 + 200, CY0 + 465, X0 + 200, CY0 + 465, op=0)
    pill_text(sc, 141, ch, X0 + 200, CY0 + 465, "oszczędzone: 5 min", 32, DKGREEN, a(A_GREEN, 0.14), style="SemiBold")
    fade(sc, ch, OSZ - 60, d_in=160)
    pop(sc, ch, OSZ - 60, 420, 70)
    return sc
ovl("A01")


# ================================================================== A02  stop using → start building (segmented control)
def A02():
    sc = new("A02_Budowac", 6.15, 12.60)
    FX = overlay(sc)
    w = sc.word
    DEK, PRZ, ZACZ, BUD = w(8.80), w(9.38), w(10.94), w(12.00)
    END = sc.t(12.35)
    g = card(sc, 110, FX, sc.t(6.30), END)
    head(sc, 112, g, CY0, "Największa zmiana dekady", DEK - 300, A_INK)
    SX, SY, SW, SH = X0 + 50, CY0 + 200, CW - 100, 140
    sc.rect(113, "Seg", g, SX, SY, SW, SH, A_FILL, r=SH / 2)
    th = sc.rect(114, "Thumb", g, SX + 8, SY + 8, SW / 2 - 16, SH - 16, A_BG, r=(SH - 16) / 2)
    sc.shadow(th, 0.14, 16, 4)
    sc.k(th, "positionX", [(0, f(SX + 8), LIN), (ZACZ, f(SX + 8), HOLD), (ZACZ + 500, f(SX + SW / 2 + 8), APPLE)])
    sc.k(th, "fillColor", [(0, col(A_BG), LIN), (ZACZ, col(A_BG), HOLD), (ZACZ + 400, col(A_BLUE), SOFT)])
    l1 = sc.text(115, "Use", g, SX + SW / 4, SY + 86, "Używać", 46, A_INK, just="center")
    l2 = sc.text(116, "Build", g, SX + 3 * SW / 4, SY + 86, "Budować", 46, A_GREY, just="center")
    sc.k(l1, "fillColor", [(0, col(A_INK), LIN), (ZACZ, col(A_INK), HOLD), (ZACZ + 300, col(A_GREY), SOFT)])
    sc.k(l2, "fillColor", [(0, col(A_GREY), LIN), (ZACZ + 100, col(A_GREY), HOLD), (ZACZ + 400, col(A_BG), SOFT)])
    stp = sc.rect(117, "Strike", g, SX + SW / 4 - 90, SY + 70, 0.01, 6, A_RED, r=3)
    sc.k(stp, "rectSize", [(0, v2(0.01, 6), LIN), (PRZ, v2(0.01, 6), HOLD), (PRZ + 400, v2(180, 6), APPLE)])
    sub = sc.text(118, "Sub", g, X0 + CW / 2, CY0 + 450, "coś swojego, z pomocą AI", 34, A_BLUE, style="Medium", just="center", op=0)
    fade(sc, sub, BUD - 100, d_in=220)
    return sc
ovl("A02")


# ================================================================== A03  saved prompts pile up
def A03():
    sc = new("A03_Prompty", 12.60, 17.85)
    FX = overlay(sc)
    w = sc.word
    CZAT, ZAP, NIES = w(12.86), w(13.88), w(16.80)
    END = sc.t(17.60)
    g = card(sc, 110, FX, CZAT - 200, END)
    sc.rect(112, "Folder", g, X0 + 56, CY0 + 56, 70, 56, A_ORANGE, r=12)
    sc.text(113, "T", g, X0 + 150, CY0 + 98, "Zapisane prompty", 42, A_INK)
    cnt = sc.mono(114, "N", g, X0 + CW - 56, CY0 + 98, "0", 42, A_GREY, just="right")
    sc.k(cnt, "textContent", [(0, s("0"), LIN)] + Scene.roll_keys(ZAP, ZAP + 2600, lambda v: str(int(v)), 0, 127, ease_pow=1.4)[1:])
    rows = ["Prompt na maila sprzedażowego", "50 hooków do reelsów", "Mega prompt do biznesplanu"]
    for i, r_ in enumerate(rows):
        y = CY0 + 150 + i * 96
        t = ZAP + 150 + i * 380
        rg = sc.group(120 + i * 4, r_, g, 0, 0, op=0)
        sc.rect(121 + i * 4, "Row", rg, X0 + 40, y, CW - 80, 74, A_FILL, r=20)
        sc.text(122 + i * 4, "T", rg, X0 + 70, y + 49, r_, 32, A_INK, style="Medium")
        fade(sc, rg, t, d_in=160)
        sc.k(rg, "positionY", [(0, f(-20), LIN), (t, f(-20), HOLD), (t + 450, f(0), OUT)])
    ch = sc.group(140, "Wow", g, X0 + CW / 2, CY0 + 500, X0 + CW / 2, CY0 + 500, op=0)
    pill_text(sc, 141, ch, X0 + CW / 2, CY0 + 490, "AI potrafi niesamowite rzeczy…", 30, A_GREY, A_BG, style="SemiBold")
    fade(sc, ch, NIES - 100, d_in=200)
    return sc
ovl("A03")


# ================================================================== A04  FULL: the one question → „nic” → konsument
def A04():
    sc = new("A04_Pytanie", 17.85, 26.55)
    vbg(sc)
    w = sc.word
    JED, CO, NAL, SPR, NIC, KONS = w(18.62), w(19.42), w(20.82), w(22.22), w(24.26), w(25.94)
    k_ = sc.text(100, "K", None, 540, 520, "Jedno pytanie", 40, A_GREY, style="Medium", just="center", op=0)
    fade(sc, k_, JED - 100, d_in=220)
    lines = [("Co dzięki AI", CO), ("zbudowałeś,", w(20.04)), ("co jest twoje", NAL), ("i możesz sprzedać?", SPR)]
    for i, (ln, t) in enumerate(lines):
        tx = sc.text(101 + i, ln, None, 540, 680 + i * 110, ln, 92, A_INK if i < 3 else A_BLUE, tracking=-40, just="center", op=0)
        fade(sc, tx, t - 60, d_in=220)
        sc.k(tx, "positionY", [(0, f(710 + i * 110), LIN), (t - 60, f(710 + i * 110), HOLD), (t + 500, f(680 + i * 110), OUT)])
    fld = sc.group(110, "Field", None, 540, 1300, 540, 1300, op=0)
    sc.rect(111, "Box", fld, 140, 1240, 800, 120, A_FILL, r=36)
    an = sc.text(112, "Ans", fld, 190, 1320, "", 56, A_INK)
    sc.k(an, "textContent", [(0, s(""), LIN), (NIC, s("n"), HOLD), (NIC + 80, s("ni"), HOLD), (NIC + 160, s("nic"), HOLD)])
    car = sc.rect(113, "Caret", fld, 190, 1270, 4, 64, A_BLUE, r=2)
    sc.k(car, "positionX", [(0, f(190), LIN), (NIC + 160, f(190), HOLD), (NIC + 161, f(190 + adv("nic", 56) + 8), HOLD)])
    kk, t, on = [(0, f(100), LIN)], 300, False
    while t < sc.dur:
        kk.append((t, f(100 if on else 0), HOLD)); t += 450; on = not on
    sc.k(car, "opacity", kk)
    fade(sc, fld, SPR + 300, d_in=220)
    st = sc.group(120, "Stamp", None, 540, 1550, 540, 1550, op=0)
    sc.rect(121, "Box", st, 290, 1500, 500, 100, [1, 1, 1, 0], r=16, stroke=(A_RED, 6))
    sc.text(122, "T", st, 540, 1570, "KONSUMENT", 54, A_RED, just="center", tracking=60)
    sc.k(st, "rotation", [(0, f(-8), LIN)])
    sc.k(st, "opacity", [(0, f(0), LIN), (KONS - 60, f(0), HOLD), (KONS + 80, f(100), SOFT)])
    scale_keys(sc, st, [(0, f(150), LIN), (KONS - 60, f(150), HOLD), (KONS + 220, f(100), EIN)])
    return sc


# ================================================================== A05  two ways: faster same vs something new
def A05():
    sc = new("A05_Dwa-sposoby", 26.55, 37.65)
    FX = overlay(sc)
    w = sc.word
    DWA, SZYB, ALBO, PROD, OF, SPR = w(26.90), w(29.18), w(31.22), w(34.66), w(36.00), w(37.12)
    END = sc.t(37.40)
    y0, h_ = 1000, 580
    g = card(sc, 110, FX, DWA - 200, END, y0, h_)
    head(sc, 112, g, y0, "Dwa sposoby używania AI", None, A_INK)
    colw = (CW - 120) / 2
    L = sc.group(120, "Left", g, 0, 0, op=0)
    sc.rect(121, "Bg", L, X0 + 40, y0 + 130, colw, 400, A_FILL, r=32)
    sc.text(122, "T1", L, X0 + 40 + colw / 2, y0 + 230, "Szybciej", 40, A_GREY, just="center")
    sc.text(123, "T2", L, X0 + 40 + colw / 2, y0 + 280, "to samo", 40, A_GREY, just="center")
    sc.text(124, "S", L, X0 + 40 + colw / 2, y0 + 360, "maile, obrazki", 28, A_GREY, style="Medium", just="center")
    fade(sc, L, SZYB - 100, d_in=200)
    R = sc.group(130, "Right", g, 0, 0, op=0)
    rx = X0 + 80 + colw
    sc.rect(131, "Bg", R, rx, y0 + 130, colw, 400, a(A_BLUE, 0.08), r=32, stroke=(A_BLUE, 3))
    sc.text(132, "T1", R, rx + colw / 2, y0 + 210, "Coś nowego", 40, A_BLUE, just="center")
    for i, (txt, t) in enumerate([("produkt cyfrowy", PROD), ("oferta", OF), ("do sprzedania", SPR)]):
        c = sc.group(140 + i * 3, txt, R, rx + colw / 2, y0 + 290 + i * 76, rx + colw / 2, y0 + 290 + i * 76, op=0)
        pill_text(sc, 141 + i * 3, c, rx + colw / 2, y0 + 290 + i * 76, txt, 30, A_BG, A_BLUE, style="SemiBold")
        fade(sc, c, t - 60, d_in=160)
        pop(sc, c, t - 60, 420, 70)
    fade(sc, R, ALBO - 100, d_in=200)
    return sc
ovl("A05")


# ================================================================== A06  everything disappears when you close the tab
def A06():
    sc = new("A06_Znika", 37.60, 45.00)
    FX = overlay(sc)
    w = sc.word
    ZN = [w(40.96), w(42.62), w(43.48), w(44.10), w(44.66)]
    END = sc.t(44.85)
    y0, h_ = 1000, 580
    g = card(sc, 110, FX, sc.t(37.75), END, y0, h_)
    head(sc, 112, g, y0, "Po zamknięciu karty", None, A_INK)
    items = [("Odpowiedź z ChatGPT", A_GREEN), ("Odpowiedź z Claude", A_ORANGE), ("Obrazek", PURPLE), ("Prompt", A_BLUE), ("Mail", A_RED)]
    for i, (nm, c) in enumerate(items):
        y = y0 + 120 + i * 88
        t_in = sc.t(37.75) + 300 + i * 120
        r_ = sc.group(120 + i * 5, nm, g, X0 + CW / 2, y + 37, X0 + CW / 2, y + 37, op=0)
        sc.rect(121 + i * 5, "Row", r_, X0 + 40, y, CW - 80, 74, A_FILL, r=20)
        sc.rect(122 + i * 5, "Ic", r_, X0 + 64, y + 17, 40, 40, c, r=10)
        sc.text(123 + i * 5, "T", r_, X0 + 124, y + 49, nm, 32, A_INK, style="Medium")
        t = ZN[i]
        sc.k(r_, "opacity", [(0, f(0), LIN), (t_in, f(0), HOLD), (t_in + 200, f(100), SOFT), (t - 60, f(100), HOLD), (t + 300, f(0), SOFT)])
        scale_keys(sc, r_, [(0, f(100), LIN), (t - 60, f(100), HOLD), (t + 300, f(90), EIN)])
        sc.k(r_, "positionX", [(0, f(X0 + CW / 2), LIN), (t - 60, f(X0 + CW / 2), HOLD), (t + 300, f(X0 + CW / 2 + 60), EIN)])
    gone = sc.text(150, "Gone", g, X0 + CW / 2, y0 + 340, "nic nie zostaje", 44, A_GREY, style="Medium", just="center", op=0)
    fade(sc, gone, ZN[-1] + 250, d_in=220)
    return sc
ovl("A06")


# ================================================================== A07  the product stays — for sale, many times, yours
def A07():
    sc = new("A07_Zostaje", 45.00, 52.15)
    FX = overlay(sc)
    w = sc.word
    PROD, ZOST, WYST, WIEC, JED, TWOJ = w(45.18), w(47.12), w(47.98), w(49.70), w(50.20), w(51.70)
    END = sc.t(51.95)
    y0, h_ = 1000, 580
    g = card(sc, 110, FX, PROD - 150, END, y0, h_)
    sc.rect(112, "Cover", g, X0 + 56, y0 + 60, 200, 270, a(A_BLUE, 0.12), r=16)
    sc.rect(113, "Circle", g, X0 + 106, y0 + 110, 100, 100, A_BLUE, r=50)
    sc.text(114, "T", g, X0 + 290, y0 + 120, "Twój produkt", 48, A_INK, tracking=-15)
    sc.text(115, "S", g, X0 + 290, y0 + 168, "e-book · gotowy", 30, A_GREY, style="Medium")
    zg = sc.group(116, "Stays", g, X0 + 390, y0 + 240, X0 + 390, y0 + 240, op=0)
    pill_text(sc, 117, zg, X0 + 400, y0 + 240, "zostaje", 30, DKGREEN, a(A_GREEN, 0.14), style="SemiBold")
    fade(sc, zg, ZOST - 60, d_in=160)
    pop(sc, zg, ZOST - 60, 420, 70)
    sc.rect(120, "Sep", g, X0 + 56, y0 + 365, CW - 112, 2, A_LINE)
    sc.text(121, "Sale", g, X0 + 56, y0 + 440, "Na sprzedaż", 40, A_INK, style="Medium")
    toggle(sc, 122, g, X0 + CW - 160, y0 + 400, WYST)
    sc.text(124, "Sold k", g, X0 + 56, y0 + 530, "Sprzedane", 34, A_GREY, style="Medium")
    cnt = sc.mono(125, "Sold", g, X0 + CW - 56, y0 + 530, "×0", 44, A_INK, just="right")
    sc.k(cnt, "textContent", [(0, s("×0"), LIN)] + Scene.roll_keys(WIEC - 200, JED + 900, lambda v: f"×{int(v)}", 0, 12, ease_pow=1.3)[1:])
    tw = sc.group(130, "Yours", g, X0 + CW - 120, y0 + 90, X0 + CW - 120, y0 + 90, op=0)
    pill_text(sc, 131, tw, X0 + CW - 130, y0 + 90, "Twój", 32, A_BG, A_INK, style="SemiBold")
    fade(sc, tw, TWOJ - 60, d_in=160)
    pop(sc, tw, TWOJ - 60, 420, 60)
    return sc
ovl("A07")


# ================================================================== A08  FULL: launch — Cyfrowy Autopilot
def A08():
    sc = new("A08_Cyfrowy-Autopilot", 52.45, 54.25)
    vbg(sc)
    w = sc.word
    STW, CYF = w(52.86), w(53.42)
    IC = sc.group(100, "Icon", None, 540, 820, 540, 820, op=0)
    gl = sc.rect(101, "Glow", IC, 540 - 260, 820 - 260, 520, 520, a(A_BLUE, 0.35), r=260)
    sc.blur(gl, 7200, 90)
    sq = sc.rect(102, "Squircle", IC, 540 - 190, 820 - 190, 380, 380, A_BLUE, r=88)
    sc.shadow(sq, 0.28, 70, 26)
    sc.rect(103, "Shade", IC, 540 - 190, 820 - 190, 380, 190, [1, 1, 1, 0.10], r=88)
    sc.path(104, "Glyph", IC, [(452, 896), (540, 718), (628, 896), (540, 852)], fill=A_BG)
    fade(sc, IC, STW - 300, d_in=200)
    scale_keys(sc, IC, [(0, f(30), LIN), (STW - 300, f(30), HOLD), (STW + 300, f(108), OUT), (STW + 650, f(100), APPLE), (sc.dur, f(104), LIN)])
    nm = sc.text(110, "Name", None, 540, 1180, "Cyfrowy", 120, A_INK, tracking=-50, just="center",
                 animators=[Scene.reveal_animator(1, 11, dy=24, blur_=16)])
    sc.reveal_words(nm, 11, [CYF], step=220)
    nm2 = sc.text(111, "Name2", None, 540, 1310, "Autopilot", 120, A_BLUE, tracking=-50, just="center",
                  animators=[Scene.reveal_animator(2, 21, dy=24, blur_=16)])
    sc.reveal_words(nm2, 21, [CYF + 350], step=220)
    return sc


# ================================================================== A09  not more tricks — something you don't have yet
def A09():
    sc = new("A09_Nie-sztuczki", 54.25, 61.05)
    FX = overlay(sc)
    w = sc.word
    NIE, SZT, TYL, STW, MAS = w(54.24 + 0.24), w(55.72), w(57.40), w(59.08), w(60.76)
    END = sc.t(60.85)
    g = card(sc, 110, FX, sc.t(54.40), END)
    r1 = sc.group(120, "Tricks", g, 0, 0, op=0)
    sc.text(121, "K", r1, X0 + 56, CY0 + 90, "Nie po to, żeby:", 32, A_GREY, style="Medium")
    sc.text(122, "T", r1, X0 + 56, CY0 + 170, "uczyć się kolejnych sztuczek", 44, A_GREY, tracking=-15)
    stk = sc.rect(123, "Strike", r1, X0 + 50, CY0 + 152, 0.01, 6, A_RED, r=3)
    sc.k(stk, "rectSize", [(0, v2(0.01, 6), LIN), (TYL - 100, v2(0.01, 6), HOLD), (TYL + 400, v2(adv("uczyć się kolejnych sztuczek", 44, "SemiBold") + 16, 6), APPLE)])
    fade(sc, r1, SZT - 300, d_in=200)
    r2 = sc.group(130, "Build", g, X0 + CW / 2, CY0 + 360, X0 + CW / 2, CY0 + 360, op=0)
    sc.rect(131, "Bg", r2, X0 + 40, CY0 + 250, CW - 80, 220, a(A_BLUE, 0.08), r=32)
    sc.text(132, "K", r2, X0 + 80, CY0 + 315, "Tylko żeby stworzyć", 32, A_BLUE, style="Medium")
    sc.text(133, "T1", r2, X0 + 80, CY0 + 390, "coś, czego jeszcze", 54, A_INK, tracking=-20)
    sc.text(134, "T2", r2, X0 + 80, CY0 + 450, "nie masz", 54, A_BLUE, tracking=-20)
    fade(sc, r2, STW - 100, d_in=200)
    pop(sc, r2, STW - 100, 550, 92)
    return sc
ovl("A09")


# ================================================================== A10  product, page, offer → sell more than once
def A10():
    sc = new("A10_Wlasne", 61.00, 65.95)
    FX = overlay(sc)
    w = sc.word
    PROD, STR, OF, SPR, RAZ = w(61.40), w(62.66), w(63.32), w(64.60), w(65.56)
    END = sc.t(65.75)
    g = card(sc, 110, FX, sc.t(61.10), END)
    head(sc, 112, g, CY0, "Twoje, nie wypożyczone", None, A_INK)
    for i, (nm, t) in enumerate([("Własny produkt cyfrowy", PROD), ("Własna strona", STR), ("Własna oferta", OF)]):
        y = CY0 + 130 + i * 96
        r_ = sc.group(120 + i * 6, nm, g, 0, 0, op=0)
        sc.text(121 + i * 6, "T", r_, X0 + 130, y + 54, nm, 40, A_INK, style="Medium")
        ok_badge(sc, 122 + i * 6, r_, X0 + 80, y + 40, t, d=52)
        fade(sc, r_, t - 60, d_in=160)
        sc.k(r_, "positionX", [(0, f(24), LIN), (t - 60, f(24), HOLD), (t + 400, f(0), OUT)])
    ch = sc.group(150, "Many", g, X0 + CW / 2, CY0 + 460, X0 + CW / 2, CY0 + 460, op=0)
    pill_text(sc, 151, ch, X0 + CW / 2, CY0 + 460, "sprzedajesz więcej niż raz", 32, A_BG, A_BLUE, style="SemiBold")
    fade(sc, ch, SPR - 60, d_in=160)
    pop(sc, ch, SPR - 60, 420, 80)
    return sc
ovl("A10")


# ================================================================== A11  not another job — something of your own
def A11():
    sc = new("A11_Nie-praca", 65.95, 69.95)
    FX = overlay(sc)
    w = sc.word
    AI_, PRAC, MOZL, WLAS = w(66.10), w(67.40), w(68.16), w(69.36)
    END = sc.t(69.75)
    g = card(sc, 110, FX, AI_ - 100, END)
    L = sc.group(120, "Job", g, 0, 0)
    sc.text(121, "K", L, X0 + 56, CY0 + 90, "Kolejna praca", 36, A_GREY)
    for i, t in enumerate(["Odpisać na maile", "Zrobić grafiki", "Napisać posty"]):
        y = CY0 + 140 + i * 80
        sc.rect(122 + i * 3, "Box", L, X0 + 56, y + 10, 40, 40, [1, 1, 1, 0], r=20, stroke=(A_LINE, 3))
        sc.text(123 + i * 3, "T", L, X0 + 120, y + 42, t, 34, A_GREY, style="Medium")
    sc.k(L, "opacity", [(0, f(100), LIN), (PRAC, f(100), HOLD), (PRAC + 400, f(0), SOFT)])
    sc.k(L, "positionX", [(0, f(0), LIN), (PRAC, f(0), HOLD), (PRAC + 400, f(-80), EIN)])
    R = sc.group(140, "Own", g, X0 + CW / 2, CY0 + 260, X0 + CW / 2, CY0 + 260, op=0)
    sc.rect(141, "Key bg", R, X0 + CW / 2 - 70, CY0 + 90, 140, 140, A_BLUE, r=36)
    sc.ring(142, "Key ring", R, X0 + CW / 2 - 18, CY0 + 160, 44, A_BG, 8)
    sc.rect(143, "Key shaft", R, X0 + CW / 2 + 2, CY0 + 156, 50, 8, A_BG, r=4)
    sc.rect(144, "Key tooth", R, X0 + CW / 2 + 36, CY0 + 160, 8, 18, A_BG, r=2)
    sc.text(145, "T", R, X0 + CW / 2, CY0 + 330, "Możliwość zbudowania", 46, A_INK, tracking=-15, just="center")
    sc.text(146, "T2", R, X0 + CW / 2, CY0 + 400, "czegoś własnego", 58, A_BLUE, tracking=-20, just="center")
    fade(sc, R, MOZL - 100, d_in=200)
    pop(sc, R, MOZL - 100, 550, 88)
    return sc
ovl("A11")


# ================================================================== A12  3+ years, 941 e-books in one day
def A12():
    sc = new("A12_941", 69.90, 74.65)
    FX = overlay(sc)
    w = sc.word
    LAT, NAJ, N941 = w(71.70), w(72.32), w(73.22)
    END = sc.t(74.45)
    g = sc.group(110, "Card", FX, X0 + CW / 2, CY0 + CH_ / 2, X0 + CW / 2, CY0 + CH_ / 2, op=0)
    card_bg(sc, 111, g, X0, CY0, CW, CH_, r=48, fill=[0.06, 0.07, 0.12, 1], sh=(0.3, 70, 22))
    sc.k(g, "opacity", [(0, f(0), LIN), (sc.t(70.05), f(0), HOLD), (sc.t(70.05) + 260, f(100), SOFT), (END, f(100), HOLD), (END + 300, f(0), SOFT)])
    scale_keys(sc, g, [(0, f(92), LIN), (sc.t(70.05), f(92), HOLD), (sc.t(70.05) + 700, f(100), OUT)])
    sc.text(112, "K", g, X0 + 56, CY0 + 84, "Sprzedaję produkty cyfrowe od", 32, [1, 1, 1, 0.6], style="Medium")
    yr = sc.text(113, "Yr", g, X0 + 56, CY0 + 170, "", 64, A_BG, tracking=-20)
    sc.k(yr, "textContent", [(0, s(""), LIN), (LAT - 100, s("3+ lat"), HOLD)])
    sc.text(114, "K2", g, X0 + 56, CY0 + 270, "W najlepszym dniu", 32, [1, 1, 1, 0.6], style="Medium", op=0)
    fade(sc, 114, NAJ - 100, d_in=200)
    big = sc.text(115, "Big", g, X0 + 56, CY0 + 420, "0", 150, A_BG, tracking=-60)
    sc.k(big, "textContent", [(0, s("0"), LIN)] + Scene.roll_keys(N941 - 300, N941 + 800, lambda v: str(int(v)), 0, 941)[1:])
    sc.k(big, "opacity", [(0, f(0), LIN), (N941 - 301, f(0), HOLD), (N941 - 300, f(100), HOLD)])
    sc.text(116, "Unit", g, X0 + 420, CY0 + 420, "e-booków", 48, A_GREEN, op=0)
    fade(sc, 116, N941 + 600, d_in=200)
    return sc
ovl("A12")


# ================================================================== A13  FULL: never before available to so many ordinary people
def A13():
    sc = new("A13_Dla-wszystkich", 74.65, 81.90)
    vbg(sc)
    w = sc.word
    NAJ, NIG, ZBUD, TYLU = w(74.98), w(77.44), w(78.06), w(81.06)
    h1 = sc.text(100, "H1", None, 540, 300, "Największa zmiana AI", 72, A_INK, tracking=-30, just="center", op=0)
    fade(sc, h1, NAJ - 100, d_in=240)
    h2 = sc.text(101, "H2", None, 540, 400, "budowanie czegoś swojego", 54, A_BLUE, tracking=-20, just="center", op=0)
    fade(sc, h2, ZBUD - 100, d_in=240)
    h3 = sc.text(102, "H3", None, 540, 1700, "dostępne dla zwykłych ludzi", 50, A_INK, tracking=-15, just="center", op=0)
    fade(sc, h3, TYLU - 300, d_in=240)
    rng = random.Random(4)
    cols_, rows_ = 12, 16
    lid = 200
    early = set(rng.sample(range(cols_ * rows_), 4))
    for r_ in range(rows_):
        for c_ in range(cols_):
            i = r_ * cols_ + c_
            x, y = 540 - (cols_ - 1) * 38 + c_ * 76, 560 + r_ * 66
            d = sc.rect(lid, "Dot", None, x - 18, y - 18, 36, 36, A_LINE, r=18)
            t_on = NIG + 200 if i in early else TYLU - 600 + int(math.hypot(c_ - 5.5, r_ - 7.5) * 70)
            sc.k(d, "fillColor", [(0, col(A_LINE), LIN), (t_on, col(A_LINE), HOLD), (t_on + 250, col(A_BLUE if i not in early else A_ORANGE), SOFT)])
            lid += 1
    return sc


# ================================================================== A14  the question to ask next time
def A14():
    sc = new("A14_Zapytaj", 81.85, 88.00)
    FX = overlay(sc)
    w = sc.word
    OTW, PYT, TYL, ZAP, BUD = w(83.06), w(84.26), w(85.98), w(86.16), w(87.36)
    END = sc.t(87.80)
    g = card(sc, 110, FX, OTW - 200, END, CY0 + 60, 400)
    head(sc, 112, g, CY0 + 60, "Następnym razem zapytaj:", None, A_INK)
    sc.rect(113, "Field", g, X0 + 40, CY0 + 200, CW - 80, 130, A_FILL, r=40)
    q1, q2 = "Co możesz dla mnie zrobić?", "Co możemy razem zbudować?"
    tx = sc.text(114, "Q", g, X0 + 80, CY0 + 283, "", 42, A_GREY, style="Medium")
    keys = [(0, s(""), LIN)]
    t0, t1 = PYT, PYT + 1200
    for i in range(len(q1)):
        keys.append((t0 + (t1 - t0) * i / len(q1), s(q1[:i + 1]), HOLD))
    d0 = TYL
    for i in range(len(q1) - 1, -1, -1):
        keys.append((d0 + (len(q1) - 1 - i) * 9, s(q1[:i]), HOLD))
    t2 = ZAP + 100
    t3 = BUD + 200
    for i in range(len(q2)):
        keys.append((t2 + (t3 - t2) * i / len(q2), s(q2[:i + 1]), HOLD))
    sc.k(tx, "textContent", keys)
    sc.k(tx, "fillColor", [(0, col(A_GREY), LIN), (t2, col(A_GREY), HOLD), (t2 + 1, col(A_BLUE), HOLD)])
    snd = sc.group(120, "Send", g, X0 + CW - 110, CY0 + 265, X0 + CW - 110, CY0 + 265)
    sb = sc.rect(121, "Btn", snd, X0 + CW - 140, CY0 + 235, 60, 60, A_LINE, r=30)
    sc.path(122, "Arrow", snd, [(X0 + CW - 110, CY0 + 282), (X0 + CW - 110, CY0 + 250)], stroke=(A_BG, 5), closed=False)
    sc.path(123, "Head", snd, [(X0 + CW - 122, CY0 + 262), (X0 + CW - 110, CY0 + 250), (X0 + CW - 98, CY0 + 262)], stroke=(A_BG, 5), closed=False)
    sc.k(sb, "fillColor", [(0, col(A_LINE), LIN), (t3, col(A_LINE), HOLD), (t3 + 150, col(A_BLUE), SOFT)])
    return sc
ovl("A14")


# ================================================================== A15  CTA: tap below
def A15():
    sc = new("A15_CTA", 88.00, 91.23)
    FX = overlay(sc)
    w = sc.word
    KLIK, ZOB = w(88.24), w(89.50)
    BT = sc.group(110, "CTA", FX, 540, 1420, 540, 1420, op=0)
    b = sc.rect(111, "Btn", BT, 110, 1360, 860, 120, A_BLUE, r=60)
    sc.shadow(b, 0.3, 40, 14)
    sc.text(112, "T", BT, 500, 1436, "Zobacz, jak to działa", 46, A_BG, just="center")
    ar = sc.group(113, "Arrow", BT, 0, 0)
    sc.path(114, "Shaft", ar, [(860, 1396), (860, 1440)], stroke=(A_BG, 6), closed=False)
    sc.path(115, "Head", ar, [(842, 1424), (860, 1442), (878, 1424)], stroke=(A_BG, 6), closed=False)
    sc.k(ar, "positionY", [(0, f(0), LIN)] + sum([[(KLIK + 700 + k_ * 500, f(0), HOLD), (KLIK + 950 + k_ * 500, f(10), INOUT)] for k_ in range(4)], []))
    sc.k(BT, "opacity", [(0, f(0), LIN), (KLIK - 150, f(0), HOLD), (KLIK + 100, f(100), SOFT)])
    scale_keys(sc, BT, [(0, f(80), LIN), (KLIK - 150, f(80), HOLD), (KLIK + 350, f(100), APPLE), (KLIK + 700, f(100), HOLD),
                        (KLIK + 780, f(95), OUT), (KLIK + 1000, f(100), APPLE), (ZOB, f(100), HOLD), (ZOB + 150, f(104), OUT), (ZOB + 450, f(100), APPLE)])
    CU = cursor(sc, 120, FX, 900, 1700)
    sc.k(CU, "opacity", [(0, f(0), LIN), (KLIK + 100, f(0), HOLD), (KLIK + 250, f(100), SOFT)])
    sc.kpos(CU, [(0, 900, 1700, LIN), (KLIK + 100, 900, 1700, HOLD), (KLIK + 680, 640, 1450, APPLE)])
    scale_keys(sc, CU, [(0, f(140), LIN), (KLIK + 700, f(140), HOLD), (KLIK + 780, f(118), OUT), (KLIK + 1000, f(140), APPLE)])
    return sc
ovl("A15")


BUILD = {k: v for k, v in globals().items() if k.startswith("A") and k[1:].isdigit() and callable(v)}

if __name__ == "__main__":
    for key in (sys.argv[1:] or sorted(BUILD)):
        try:
            BUILD[key]().build()
        except SystemExit as e:
            print(f"[{key}] FAILED: {e}", flush=True)
        except Exception as e:
            print(f"[{key}] ERROR: {type(e).__name__}: {e}", flush=True)
