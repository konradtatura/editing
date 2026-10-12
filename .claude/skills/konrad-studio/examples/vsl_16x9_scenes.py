#!/usr/bin/env python3
"""VSL „Cyfrowy Autopilot” (VSL_cut.mp4, 3:08) — Apple-style animations, one metaphor per scene, synced to the word.
S01 Dynamic Island 3:00 → 48 h · S02 home screen of your business · S03 skill switches → Autopilot · S04 48 h ring → refund ·
S05 AI used as a search bar · S06 chat → ⌘W → nothing to sell · S07 „największa zmiana” · S08 the Dock of 5 skills ·
S09 the Dock collapses into AI · S10 „od 3+ lat” · S11 941 orders lock screen · S12 the model · S13 Maps: 6 months vs 48 h ·
S14 app icon launch · S15 course playlist → one goal · S16 system demo · S17 Shortcuts pipeline · S18 question → next step ·
S19 AirDrop: one file, many buyers · S20 iOS Calculator · S21 month calendar 5 130 zł · S22 not 300/500/1000 · S23 3 clients ·
S24 then vs now race · S25 AI ticks the list · S26 stuck: progress + beachball · S27 App Switcher of support ·
S28 problem → solved thread · S29 ads toggle + Wallet 800 zł · S30 e-book vs business · S31 the 48 h guarantee seal ·
S32 two futures (swipe) · S33 CTA button · S34 finale.
Usage: scenes_vsl.py S01 S02 ...   (no args = all)."""
import sys, os, random
sys.path.insert(0, os.path.expanduser("~/.claude/skills/konrad-studio/scripts"))
import apple
PROJECT = os.environ.get("PROJECT", os.path.dirname(os.path.abspath(__file__)))   # project folder (outputs)
apple.init(PROJECT, 1920, 1080)
from apple import *

SRC = os.path.join(PROJECT, "..", "VSL_cut.mp4")          # the CUT film the scenes sit on (original: VSL/VSL_cut.mp4)
WORDS = os.path.join(PROJECT, "tr", "vsl.json")           # whisper word-timestamps of SRC
OVERLAY = set()


def new(name, a_, b_):
    return Scene(name, a_, b_, WORDS, SRC)


def ovl(key):
    OVERLAY.add(key)


def phone(sc, base, parent, cx, cy, w_=400, h_=820, screen=A_BG, island=True):
    """iPhone outline centred at (cx, cy). Returns (x0, y0, w, h) of the screen."""
    x0, y0 = cx - w_ / 2, cy - h_ / 2
    fr = sc.rect(base, "Bezel", parent, x0 - 12, y0 - 12, w_ + 24, h_ + 24, A_INK, r=72)
    sc.shadow(fr, 0.22, 70, 26)
    sc.rect(base + 1, "Screen", parent, x0, y0, w_, h_, screen, r=60)
    if island:
        sc.rect(base + 2, "Island", parent, cx - 58, y0 + 18, 116, 34, A_INK, r=17)
    return x0, y0, w_, h_


# ================================================================== S01  Dynamic Island: 3:00 → 48 h (overlay)
def S01():
    sc = new("S01_Trzy-minuty", 0.00, 2.95)
    FX = overlay(sc)
    T48 = sc.word(1.80)
    END = sc.t(2.60)
    PW0, PW1, PH = 150, 330, 64
    g = sc.group(110, "Island", FX, 960, 50, 960, 50, op=0)
    pill = sc.rect(111, "Pill", g, 960 - PW0 / 2, 18, PW0, PH, [0.02, 0.02, 0.02, 1], r=PH / 2)
    sc.shadow(pill, 0.25, 24, 6)
    sc.k(pill, "rectSize", [(0, v2(PW0, PH), LIN), (40, v2(PW0, PH), HOLD), (520, v2(PW1, PH), APPLE)])
    sc.k(pill, "positionX", [(0, f(960 - PW0 / 2), LIN), (40, f(960 - PW0 / 2), HOLD), (520, f(960 - PW1 / 2), APPLE)])
    sc.k(g, "opacity", [(0, f(0), LIN), (1, f(0), HOLD), (160, f(100), SOFT), (END, f(100), HOLD), (END + 260, f(0), SOFT)])
    dg = sc.mono(120, "Digits", g, 960, 62, "3:00", 36, A_BG, just="center", op=0)
    fade(sc, dg, 300, d_in=200)
    keys = [(0, s("3:00"), LIN), (1000, s("2:59"), HOLD)]
    keys += Scene.roll_keys(T48 - 40, T48 + 520, lambda v: f"{int(v)}:00:00", 0, 48, ease_pow=2.4)
    sc.k(dg, "textContent", keys)
    sc.k(dg, "fillColor", [(0, col(A_BG), LIN), (T48 - 41, col(A_BG), HOLD), (T48 + 300, col([0.45, 0.72, 1.0, 1]), SOFT)])
    dot = sc.rect(121, "Live", g, 960 - PW1 / 2 + 26, 42, 16, 16, A_ORANGE, r=8, op=0)
    kk, t, on = [(0, f(0), LIN), (520, f(0), HOLD)], 521, True
    while t < sc.dur:
        kk.append((t, f(100 if on else 35), INOUT)); t += 450; on = not on
    sc.k(dot, "opacity", kk)
    return sc
ovl("S01")


# ================================================================== S02  the home screen of your future business
def S02():
    sc = new("S02_Ekran-biznesu", 3.10, 9.65)
    sc.apple_bg()
    w = sc.word
    NIE, PROD, STR, WSZ, SPR = w(3.56), w(5.90), w(7.10), w(7.58), w(9.06)
    P = sc.group(100, "Phone", None, 960, 540, 960, 540, op=0)
    x0, y0, pw, ph = phone(sc, 101, P, 960, 540, 420, 860, screen=[0.95, 0.96, 0.99, 1])
    for i, (x, y, d, c) in enumerate([(x0 - 120, y0 - 80, 420, [0.75, 0.84, 1.0, 0.8]), (x0 + 160, y0 + 520, 420, [1.0, 0.86, 0.80, 0.7])]):
        gl = sc.rect(104 + i, "Wallpaper glow", P, x, y, d, d, c, r=d / 2)
        sc.blur(gl, 7100 + i, 90)
    mt = sc.rect(107, "Screen matte", P, x0, y0, pw, ph, A_BG, r=60)
    sc.matte(104, mt); sc.matte(105, mt)
    sc.text(108, "Clock", P, x0 + 40, y0 + 50, "9:41", 22, A_INK)
    fade(sc, P, 1, d_in=220)
    scale_keys(sc, P, [(0, f(94), LIN), (1, f(94), HOLD), (700, f(100), OUT)])
    # empty state: a dashed "?" slot
    q = sc.group(110, "Empty", P, 960, y0 + 250, 960, y0 + 250, op=0)
    sc.rect(111, "Slot", q, x0 + 30, y0 + 110, pw - 60, 280, [1, 1, 1, 0.5], r=36, stroke=(a(A_GREY, 0.5), 3))
    sc.text(112, "Q", q, 960, y0 + 280, "?", 110, a(A_GREY, 0.8), just="center")
    sc.text(113, "Q lab", q, 960, y0 + 345, "brak pomysłu", 24, A_GREY, style="Medium", just="center")
    sc.k(q, "opacity", [(0, f(0), LIN), (NIE - 100, f(0), HOLD), (NIE + 150, f(100), SOFT), (PROD - 200, f(100), HOLD), (PROD, f(0), SOFT)])
    # widgets
    def widget(base, y, h_, t, title, sub, colr):
        g = sc.group(base, title, P, 960, y + h_ / 2, 960, y + h_ / 2, op=0)
        wd = sc.rect(base + 1, "W", g, x0 + 30, y, pw - 60, h_, A_BG, r=34)
        sc.shadow(wd, 0.10, 30, 10)
        sc.rect(base + 2, "Icon", g, x0 + 56, y + 26, 54, 54, colr, r=14)
        sc.text(base + 3, "T", g, x0 + 126, y + 52, title, 26, A_INK)
        sc.text(base + 4, "S", g, x0 + 126, y + 82, sub, 20, A_GREY, style="Medium")
        fade(sc, g, t - 60, d_in=200)
        pop(sc, g, t - 60, 600, 80)
        return g
    g1 = widget(120, y0 + 110, 280, PROD, "Twój produkt", "e-book · gotowy", A_BLUE)
    sc.rect(126, "Cover", g1, x0 + 56, y0 + 214, 120, 160, a(A_BLUE, 0.12), r=10)
    sc.rect(127, "Cover c", g1, x0 + 86, y0 + 244, 60, 60, A_BLUE, r=30)
    for i in range(3):
        sc.rect(128 + i, "Line", g1, x0 + 200, y0 + 236 + i * 34, [150, 120, 90][i], 12, A_LINE, r=6)
    g2 = widget(140, y0 + 410, 150, STR, "Twoja strona", "online", A_GREEN)
    g3 = widget(160, y0 + 580, 150, WSZ, "Sprzedaż", "płatności włączone", A_ORANGE)
    bt = sc.group(170, "Buy", g3, x0 + pw - 120, y0 + 655, x0 + pw - 120, y0 + 655, op=0)
    sc.rect(171, "Btn", bt, x0 + pw - 190, y0 + 633, 140, 44, A_BLUE, r=22)
    sc.text(172, "Btn t", bt, x0 + pw - 120, y0 + 663, "Kup teraz", 18, A_BG, just="center")
    fade(sc, bt, WSZ + 350, d_in=180)
    # first sale banner
    nb = sc.group(180, "Sale", P, 960, y0 + 60, 960, y0 + 60, op=0)
    card_bg(sc, 181, nb, x0 + 14, y0 + 16, pw - 28, 96, r=28, fill=[1, 1, 1, 0.98], sh=(0.18, 30, 10))
    sc.rect(182, "Icon", nb, x0 + 34, y0 + 36, 56, 56, A_GREEN, r=14)
    check(sc, 183, nb, x0 + 62, y0 + 64, 20, A_BG, 4)
    sc.text(184, "T", nb, x0 + 106, y0 + 60, "Nowa sprzedaż", 22, A_INK)
    sc.text(185, "S", nb, x0 + 106, y0 + 90, "+57 zł · e-book", 20, A_GREY, style="Medium")
    sc.k(nb, "opacity", [(0, f(0), LIN), (SPR - 200, f(0), HOLD), (SPR, f(100), SOFT)])
    sc.k(nb, "positionY", [(0, f(y0 - 40), LIN), (SPR - 200, f(y0 - 40), HOLD), (SPR + 300, f(y0 + 60), APPLE)])
    return sc


# ================================================================== S03  skills switched off → Autopilot switches them on (overlay)
def S03():
    sc = new("S03_Umiejetnosci", 9.70, 14.25)
    FX = overlay(sc)
    w = sc.word
    T_ = [w(10.72), w(11.48), w(12.18), w(13.04)]
    AI_ = w(13.76)
    END = sc.t(14.05)
    X0, Y0, CW = 70, 150, 600
    C = sc.group(110, "Settings", FX, X0 + CW / 2, 480, X0 + CW / 2, 480, op=0)
    card_bg(sc, 111, C, X0, Y0, CW, 640, r=40, sh=(0.18, 60, 18))
    sc.text(112, "Head", C, X0 + 40, Y0 + 66, "Twoje umiejętności", 34, A_INK)
    names = ["Pisanie e-booków", "Budowanie stron", "Tworzenie oferty", "Korzystanie z AI"]
    for i, (nm, t) in enumerate(zip(names, T_)):
        y = Y0 + 110 + i * 96
        g = sc.group(120 + i * 6, nm, C, 0, 0, op=0)
        sc.text(121 + i * 6, "N", g, X0 + 40, y + 46, nm, 28, A_INK, style="Medium")
        toggle(sc, 122 + i * 6, g, X0 + CW - 144, y + 10, AI_ + 250 + i * 90)
        sc.rect(124 + i * 6, "Sep", g, X0 + 40, y + 84, CW - 80, 1.5, A_LINE)
        fade(sc, g, t - 60, d_in=200)
        sc.k(g, "positionY", [(0, f(16), LIN), (t - 60, f(16), HOLD), (t + 450, f(0), OUT)])
    mg = sc.group(160, "Master", C, 0, 0, op=0)
    sc.rect(161, "Bg", mg, X0 + 24, Y0 + 500, CW - 48, 110, a(A_BLUE, 0.08), r=28)
    sc.text(162, "T", mg, X0 + 52, Y0 + 556, "Cyfrowy Autopilot", 30, A_BLUE)
    sc.text(163, "S", mg, X0 + 52, Y0 + 590, "robi to za Ciebie", 22, A_GREY, style="Medium")
    toggle(sc, 164, mg, X0 + CW - 152, Y0 + 525, AI_ + 120, on_color=A_BLUE)
    fade(sc, mg, AI_ - 200, d_in=200)
    card_in(sc, C, T_[0] - 300, END)
    return sc
ovl("S03")


# ================================================================== S04  48 h ring drains → 100% refund
def S04():
    sc = new("S04_Zwrot", 14.30, 20.65)
    sc.apple_bg()
    w = sc.word
    T48, NADAL, GOT, ODD, P100 = w(16.40), w(17.56), w(18.54), w(19.00), w(19.66)
    G = sc.group(100, "Timer", None, 960, 470, 960, 470, op=0)
    sc.ring(101, "Track", G, 960, 470, 520, A_LINE, 18)
    rg = sc.ring(102, "Ring", G, 960, 470, 520, A_BLUE, 18, trim_end=0)
    sc.k(rg, "trimEnd", [(0, f(0), LIN), (T48 - 200, f(0), HOLD), (T48 + 700, f(100), OUT), (NADAL, f(100), HOLD), (GOT + 300, f(0), INOUT)])
    sc.k(rg, "strokeColor", [(0, col(A_BLUE), LIN), (NADAL, col(A_BLUE), HOLD), (GOT, col(A_ORANGE), SOFT)])
    dg = sc.mono(103, "Digits", G, 960, 500, "00:00:00", 84, A_INK, just="center")
    hms = lambda v: f"{int(v) // 3600:02d}:{int(v) % 3600 // 60:02d}:{int(v) % 60:02d}"
    sc.k(dg, "textContent", [(0, s("00:00:00"), LIN)] + Scene.roll_keys(T48 - 200, T48 + 700, hms, 0, 48 * 3600)[1:] +
         Scene.roll_keys(NADAL, GOT + 300, hms, 48 * 3600, 0, ease_pow=1.3)[1:])
    sc.text(104, "Lab", G, 960, 600, "Twój proces", 28, A_GREY, style="Medium", just="center")
    fade(sc, G, 60, d_in=260)
    scale_keys(sc, G, [(0, f(96), LIN), (60, f(96), HOLD), (700, f(100), OUT), (ODD - 100, f(100), HOLD), (ODD + 600, f(62), APPLE)])
    sc.k(G, "positionY", [(0, f(470), LIN), (ODD - 100, f(470), HOLD), (ODD + 600, f(300), APPLE)])
    # refund sheet
    RS = sc.group(120, "Refund", None, 960, 820, 960, 820, op=0)
    card_bg(sc, 121, RS, 560, 660, 800, 320, r=44, sh=(0.16, 70, 22))
    sc.text(122, "K", RS, 620, 728, "Zwrot środków", 30, A_GREY, style="Medium")
    big = sc.text(123, "Big", RS, 620, 860, "0%", 130, A_GREEN, tracking=-50)
    sc.k(big, "textContent", [(0, s("0%"), LIN)] + Scene.roll_keys(P100, P100 + 700, lambda v: f"{int(v)}%", 0, 100)[1:])
    sc.text(124, "S", RS, 620 + adv("100%", 130, "SemiBold") * 0.93 + 22, 860, "kwoty", 44, A_INK, style="Medium")
    ok_badge(sc, 130, RS, 1290, 760, P100 + 750, d=70)
    sc.k(RS, "opacity", [(0, f(0), LIN), (ODD, f(0), HOLD), (ODD + 250, f(100), SOFT)])
    sc.k(RS, "positionY", [(0, f(1000), LIN), (ODD, f(1000), HOLD), (ODD + 700, f(820), APPLE)])
    return sc


# ================================================================== S05  AI used like a better search bar (overlay)
def S05():
    sc = new("S05_Wyszukiwarka", 20.70, 24.50)
    FX = overlay(sc)
    w = sc.word
    UZY, GOO = w(22.36), w(24.14)
    END = sc.t(24.30)
    C = sc.group(110, "Search", FX, 370, 300, 370, 300, op=0)
    sb = sc.rect(111, "Bar", C, 70, 250, 600, 96, A_BG, r=48)
    sc.shadow(sb, 0.18, 50, 16)
    sc.ring(112, "Lens", C, 128, 292, 30, A_GREY, 4)
    sc.path(113, "Handle", C, [(139, 303), (152, 316)], stroke=(A_GREY, 4), closed=False)
    q = "napisz maila do klienta"
    tx = sc.text(114, "Query", C, 176, 309, "", 30, A_INK, style="Medium")
    t0, t1 = UZY, UZY + 1500
    sc.k(tx, "textContent", [(0, s(""), LIN)] + [(t0 + (t1 - t0) * i / len(q), s(q[:i + 1]), HOLD) for i in range(len(q))])
    car = sc.rect(115, "Caret", C, 0, 272, 3, 44, A_BLUE, r=1.5)
    sc.k(car, "positionX", [(0, f(176), LIN)] + [(t0 + (t1 - t0) * i / len(q), f(176 + adv(q[:i + 1], 30) + 4), HOLD) for i in range(len(q))])
    kk, t, on = [(0, f(100), LIN)], t1 + 1, False
    while t < sc.dur:
        kk.append((t, f(100 if on else 0), HOLD)); t += 450; on = not on
    sc.k(car, "opacity", kk)
    lab = sc.group(120, "Label", C, 370, 200, 370, 200, op=0)
    pill_text(sc, 121, lab, 370, 200, "AI jak wyszukiwarka", 26, A_GREY, A_FILL, style="SemiBold")
    fade(sc, lab, GOO - 200, d_in=180)
    pop(sc, lab, GOO - 200, 420, 80)
    card_in(sc, C, sc.word(21.42) - 200, END)
    return sc
ovl("S05")


# ================================================================== S06  three prompts → ⌘W → nothing to sell
def S06():
    sc = new("S06_Zamykaja-karte", 24.30, 30.75)
    sc.apple_bg()
    w = sc.word
    M1, M2, M3, ZAM, P1, P2, P3 = w(24.56), w(25.44), w(26.08), w(27.20), w(28.04), w(28.72), w(29.34)
    WIN = sc.group(100, "Chat window", None, 960, 520, 960, 520, op=0)
    card_bg(sc, 101, WIN, 560, 200, 800, 640, r=28, sh=(0.16, 70, 22))
    sc.rect(102, "Bar", WIN, 560, 200, 800, 60, A_FILL, r=28)
    sc.rect(103, "Bar sq", WIN, 560, 230, 800, 30, A_FILL)
    lights = [[1.0, 0.37, 0.34, 1], [1.0, 0.74, 0.18, 1], [0.16, 0.79, 0.25, 1]]
    for i, c in enumerate(lights):
        sc.rect(104 + i, "Light", WIN, 588 + i * 26, 223, 14, 14, c, r=7)
    sc.text(107, "Title", WIN, 960, 238, "Nowy czat", 20, A_GREY, style="Medium", just="center")
    msgs = [(M1, "Napisz maila"), (M2, "Zrób obrazek"), (M3, "Daj 20 pomysłów")]
    for i, (t, m) in enumerate(msgs):
        y = 300 + i * 150
        wd = adv(m, 28) + 56
        g = sc.group(110 + i * 6, m, WIN, 1320 - wd / 2, y + 30, 1320 - wd / 2, y + 30, op=0)
        sc.rect(111 + i * 6, "Bub", g, 1320 - wd, y, wd, 60, A_BLUE, r=30)
        sc.text(112 + i * 6, "T", g, 1320 - wd + 28, y + 40, m, 28, A_BG, style="Medium")
        fade(sc, g, t - 60, d_in=160)
        pop(sc, g, t - 60, 420, 80)
        rp = sc.group(113 + i * 6, "Reply", WIN, 640, y + 105, 640, y + 105, op=0)
        sc.rect(114 + i * 6, "R", rp, 600, y + 80, 240 - i * 40, 50, A_FILL, r=25)
        for j in range(3):
            sc.rect(150 + i * 3 + j, "Dot", rp, 626 + j * 22, y + 98, 12, 12, A_GREY, r=6)
        fade(sc, rp, t + 300, d_in=160)
    # ⌘W: red light pressed, window shrinks away
    sc.k(104, "fillColor", [(0, col(lights[0]), LIN), (ZAM - 150, col(lights[0]), HOLD), (ZAM - 50, col([0.75, 0.2, 0.18, 1]), SOFT)])
    sc.k(WIN, "opacity", [(0, f(0), LIN), (40, f(0), HOLD), (300, f(100), SOFT), (ZAM, f(100), HOLD), (ZAM + 350, f(0), SOFT)])
    scale_keys(sc, WIN, [(0, f(96), LIN), (40, f(96), HOLD), (700, f(100), OUT), (ZAM, f(100), HOLD), (ZAM + 400, f(80), EIN)])
    # nothing to sell
    rows = [("Produkty", P1), ("Oferty", P2), ("Rzeczy do sprzedania", P3)]
    for i, (nm, t) in enumerate(rows):
        y = 380 + i * 130
        g = sc.group(170 + i * 4, nm, None, 960, y, 960, y, op=0)
        sc.rect(171 + i * 4, "Row", g, 560, y - 50, 800, 100, A_FILL, r=28)
        sc.text(172 + i * 4, "N", g, 610, y + 13, nm, 36, A_INK, style="Medium")
        sc.mono(173 + i * 4, "V", g, 1310, y + 18, "0", 56, A_GREY, just="right")
        fade(sc, g, t - 60, d_in=180)
        pop(sc, g, t - 60, 500, 90)
    return sc


# ================================================================== S07  „największa zmiana, jaką stworzyło AI”
def S07():
    sc = new("S07_Najwieksza-zmiana", 32.00, 34.30)
    sc.apple_bg()
    w = sc.word
    NAJ, ZM, AI_ = w(32.16), w(32.62), w(33.18)
    l1 = sc.text(100, "L1", None, 960, 520, "Największa zmiana", 150, A_INK, tracking=-60, just="center",
                 animators=[Scene.reveal_animator(1, 11, dy=36, blur_=18)])
    sc.reveal_words(l1, 11, [NAJ, ZM], step=200)
    l2 = sc.text(101, "L2", None, 960, 650, "jaką stworzyło AI", 64, A_GREY, style="Medium", tracking=-20, just="center",
                 animators=[Scene.reveal_animator(2, 21, dy=20, blur_=10), Scene.color_animator(3, 31, A_BLUE, 2, 3)])
    sc.reveal_words(l2, 21, [AI_ - 300, AI_ - 150, AI_], step=160)
    ln = sc.rect(102, "Line", None, 560, 760, 0.01, 3, A_LINE)
    sc.k(ln, "rectSize", [(0, v2(0.01, 3), LIN), (AI_, v2(0.01, 3), HOLD), (AI_ + 800, v2(800, 3), OUT)])
    dt = sc.rect(103, "Now", None, 952, 753, 16, 16, A_BLUE, r=8, op=0)
    fade(sc, dt, AI_ + 500, d_in=200)
    return sc


# ================================================================== S08  the Dock: five skills, months or hires
DOCK = [("Research", TEAL), ("Produkt", A_BLUE), ("Copywriting", A_ORANGE), ("Strona", A_GREEN), ("Marketing", A_RED)]
DX = [960 + (i - 2) * 190 for i in range(5)]
DY = 640


def dock_icon(sc, base, parent, i, cx, cy):
    nm, c = DOCK[i]
    g = sc.group(base, nm, parent, cx, cy, cx, cy, op=0)
    sc.rect(base + 1, "Icon", g, cx - 70, cy - 70, 140, 140, c, r=34)
    if i == 0:      # magnifier
        sc.ring(base + 2, "Lens", g, cx - 8, cy - 8, 52, A_BG, 8)
        sc.path(base + 3, "H", g, [(cx + 12, cy + 12), (cx + 32, cy + 32)], stroke=(A_BG, 9), closed=False)
    elif i == 1:    # book
        sc.rect(base + 2, "Book", g, cx - 34, cy - 42, 68, 84, A_BG, r=8)
        sc.rect(base + 3, "Spine", g, cx - 34, cy - 42, 12, 84, a(c, 0.4), r=4)
    elif i == 2:    # Aa
        sc.text(base + 2, "Aa", g, cx, cy + 26, "Aa", 72, A_BG, just="center")
    elif i == 3:    # browser
        sc.rect(base + 2, "Win", g, cx - 44, cy - 34, 88, 68, [1, 1, 1, 0], r=10, stroke=(A_BG, 6))
        sc.rect(base + 3, "Bar", g, cx - 44, cy - 18, 88, 5, A_BG)
    else:           # rising chart
        sc.path(base + 2, "Chart", g, [(cx - 40, cy + 26), (cx - 12, cy - 2), (cx + 8, cy + 12), (cx + 40, cy - 30)], stroke=(A_BG, 9), closed=False)
    lab = sc.text(base + 6, "Lab", g, cx, cy + 118, nm, 26, A_INK, style="Medium", just="center")
    return g


def dock_base(sc, base, parent):
    d = sc.rect(base, "Dock", parent, 960 - 520, DY - 100, 1040, 200, [1, 1, 1, 0.65], r=48, stroke=([1, 1, 1, 0.9], 2))
    sc.shadow(d, 0.10, 60, 20)
    return d


def S08():
    sc = new("S08_Dock-umiejetnosci", 38.15, 46.28)
    sc.apple_bg()
    w = sc.word
    LAT, ZEST = 120, w(38.40)
    T_ = [w(39.84), w(40.36), w(40.72), w(41.36), w(41.68)]
    MIES, LUDZ = w(43.28), w(44.74)
    yr = sc.group(100, "Year", None, 960, 210, 960, 210, op=0)
    pill_text(sc, 101, yr, 960, 210, "kilka lat temu", 30, A_GREY, A_FILL, style="SemiBold")
    fade(sc, yr, LAT - 100, d_in=200)
    hd = sc.text(106, "Head", None, 960, 330, "Cały zestaw umiejętności", 72, A_INK, tracking=-30, just="center", op=0)
    fade(sc, hd, ZEST - 100, d_in=240)
    D = sc.group(103, "Dock group", None, 960, DY, 960, DY, op=0)
    dock_base(sc, 104, D)
    fade(sc, D, T_[0] - 300, d_in=250)
    for i in range(5):
        g = dock_icon(sc, 110 + i * 10, D, i, DX[i], DY - 10)
        fade(sc, g, T_[i] - 60, d_in=160)
        scale_keys(sc, g, [(0, f(40), LIN), (T_[i] - 60, f(40), HOLD), (T_[i] + 180, f(118), OUT), (T_[i] + 520, f(100), APPLE)])
        # months: an install ring fills slowly around each icon
        rg = sc.ring(170 + i, "Install", D, DX[i], DY - 10, 176, a(DOCK[i][1], 0.8), 6, trim_end=0)
        sc.k(rg, "trimEnd", [(0, f(0), LIN), (MIES - 600 + i * 80, f(0), HOLD), (LUDZ - 200, f(55 + i * 6), LIN)])
        sc.k(rg, "opacity", [(0, f(100), LIN), (LUDZ, f(100), HOLD), (LUDZ + 300, f(0), SOFT)])
    mc = sc.group(180, "Months", None, 960, 900, 960, 900, op=0)
    pill_text(sc, 181, mc, 960, 900, "miesiące nauki", 30, A_ORANGE, a(A_ORANGE, 0.12), style="SemiBold")
    sc.k(mc, "opacity", [(0, f(0), LIN), (MIES - 600, f(0), HOLD), (MIES - 400, f(100), SOFT), (LUDZ - 300, f(100), HOLD), (LUDZ - 100, f(0), SOFT)])
    # …or people on the payroll
    for i in range(5):
        av = sc.group(190 + i * 4, "Person", None, DX[i], DY - 150, DX[i], DY - 150, op=0)
        sc.rect(191 + i * 4, "Av", av, DX[i] - 30, DY - 180, 60, 60, A_FILL, r=30, stroke=(A_BG, 4))
        sc.rect(192 + i * 4, "Head", av, DX[i] - 10, DY - 170, 20, 20, A_GREY, r=10)
        sc.path(193 + i * 4, "Body", av, arc(DX[i], DY - 128, 17, 180, 360, 14), fill=A_GREY)
        t = LUDZ - 300 + i * 90
        fade(sc, av, t, d_in=160)
        pop(sc, av, t, 420, 60)
    pc = sc.group(220, "Hire", None, 960, 900, 960, 900, op=0)
    pill_text(sc, 221, pc, 960, 900, "albo ludzie na fakturze", 30, A_RED, a(A_RED, 0.1), style="SemiBold")
    fade(sc, pc, LUDZ - 100, d_in=200)
    return sc


# ================================================================== S09  the Dock collapses into one AI icon
def S09():
    sc = new("S09_AI-zamiast-5", 46.28, 48.95)
    sc.apple_bg()
    w = sc.word
    DZIS, KOMP, MAT = w(46.46), w(47.16), w(48.22)
    D = sc.group(103, "Dock group", None, 960, DY, 960, DY)
    dock_base(sc, 104, D)
    sc.k(104, "opacity", [(0, f(100), LIN), (KOMP, f(100), HOLD), (KOMP + 300, f(0), SOFT)])
    for i in range(5):
        g = dock_icon(sc, 110 + i * 10, D, i, DX[i], DY - 10)
        sc.k(g, "opacity", [(0, f(100), LIN), (KOMP + 200 + abs(i - 2) * 40, f(100), HOLD), (KOMP + 450 + abs(i - 2) * 40, f(0), SOFT)])
        sc.k(g, "positionX", [(0, f(DX[i]), LIN), (KOMP - 100, f(DX[i]), HOLD), (KOMP + 450, f(960), APPLE)])
        scale_keys(sc, g, [(0, f(100), LIN), (KOMP - 100, f(100), HOLD), (KOMP + 450, f(70), APPLE)])
    AI = sc.group(170, "AI", None, 960, DY - 10, 960, DY - 10, op=0)
    ic = sc.rect(171, "Icon", AI, 960 - 110, DY - 120, 220, 220, A_BLUE, r=52)
    sc.shadow(ic, 0.25, 50, 18)
    sc.text(172, "AI", AI, 960, DY + 30, "AI", 110, A_BG, tracking=-30, just="center")
    fade(sc, AI, KOMP + 300, d_in=160)
    scale_keys(sc, AI, [(0, f(40), LIN), (KOMP + 300, f(40), HOLD), (KOMP + 700, f(112), OUT), (KOMP + 1000, f(100), APPLE)])
    yr = sc.group(100, "Year", None, 960, 210, 960, 210)
    sc.rect(101, "Pill", yr, 960 - 110, 180, 220, 60, A_FILL, r=30)
    y_t = sc.mono(102, "Y", yr, 960, 222, "kiedyś", 30, A_GREY, just="center")
    sc.k(y_t, "textContent", [(0, s("kiedyś"), LIN), (DZIS, s("dziś"), HOLD)])
    sc.k(y_t, "fillColor", [(0, col(A_GREY), LIN), (DZIS, col(A_BLUE), HOLD)])
    sub = sc.text(180, "Sub", None, 960, 900, "jedno narzędzie zamiast pięciu ról", 34, A_GREY, style="Medium", just="center", op=0)
    fade(sc, sub, MAT - 400, d_in=240)
    return sc


# ================================================================== S10  not from yesterday: 3+ years (overlay)
def S10():
    sc = new("S10_Od-3-lat", 49.00, 53.25)
    FX = overlay(sc)
    w = sc.word
    WCZ, LAT3 = w(51.00), w(52.72)
    END = sc.t(53.05)
    X0, Y0, CW = 70, 180, 560
    C = sc.group(110, "Years", FX, X0 + CW / 2, 420, X0 + CW / 2, 420, op=0)
    card_bg(sc, 111, C, X0, Y0, CW, 460, r=40, sh=(0.18, 60, 18))
    sc.text(112, "K", C, X0 + 40, Y0 + 66, "Sprzedaję produkty cyfrowe", 28, A_GREY, style="Medium")
    big = sc.text(113, "Big", C, X0 + 40, Y0 + 190, "0 lat", 92, A_INK, tracking=-40)
    sc.k(big, "textContent", [(0, s("od wczoraj?"), LIN), (LAT3 - 200, s("3+ lata"), HOLD)])
    sc.k(big, "fillColor", [(0, col(A_GREY), LIN), (LAT3 - 201, col(A_GREY), HOLD), (LAT3 - 200, col(A_INK), HOLD)])
    sc.k(big, "opacity", [(0, f(100), LIN)])
    for i, (yr, hh) in enumerate([("2022", 60), ("2023", 120), ("2024", 190), ("2025", 260)]):
        x = X0 + 50 + i * 120
        b = sc.rect(120 + i * 2, "Bar", C, x, Y0 + 420 - hh, 80, hh, A_BLUE if i == 3 else a(A_BLUE, 0.35), r=14, ax=40, ay=hh)
        t = LAT3 - 150 + i * 110
        sc.k(b, "scaleY", [(0, f(0), LIN), (t, f(0), HOLD), (t + 500, f(100), OUT)])
        sc.mono(121 + i * 2, "Yr", C, x + 40, Y0 + 452, yr, 20, A_GREY, just="center")
    card_in(sc, C, WCZ - 900, END)
    return sc
ovl("S10")


# ================================================================== S11  941 e-books in one day (dark lock screen)
def S11():
    sc = new("S11_941", 53.28, 55.85)
    sc.bg = [0.02, 0.025, 0.05, 1]
    sc.layers += [blob(20, -500, -700, 1600, [0.20, 0.25, 0.55, 0.55], dur=sc.dur), blob(21, 900, 300, 1500, [0.25, 0.18, 0.45, 0.45], dur=sc.dur)]
    w = sc.word
    N941, BUK = w(54.24), w(55.04)
    num = sc.text(100, "Num", None, 960, 330, "0", 210, A_BG, tracking=-80, just="center")
    sc.k(num, "textContent", [(0, s("0"), LIN)] + Scene.roll_keys(200, N941 + 650, lambda v: str(int(v)), 0, 941, ease_pow=1.8)[1:])
    sc.text(101, "Sub", None, 960, 410, "e-booków w jeden dzień", 40, [1, 1, 1, 0.7], style="Medium", just="center")
    # orders cascade, accelerating
    rng = random.Random(5)
    lid, t, gap = 200, 150, 260
    while t < sc.dur - 150 and lid < 260:
        g = sc.group(lid, "Order", None, 960, 600, 960, 600, op=0)
        sc.rect(lid + 1, "Card", g, 600, 545, 720, 110, [0.30, 0.30, 0.34, 0.62], r=30)
        sc.rect(lid + 2, "Icon", g, 624, 572, 56, 56, A_GREEN, r=14)
        sc.text(lid + 3, "T", g, 700, 595, "Nowe zamówienie", 26, A_BG)
        sc.text(lid + 4, "S", g, 700, 630, f"E-book · +{rng.choice([47, 57, 57, 67])} zł", 22, [1, 1, 1, 0.7], style="Medium")
        sc.k(g, "opacity", [(0, f(0), LIN), (t, f(0), HOLD), (t + 120, f(100), SOFT), (t + 900, f(100), HOLD), (t + 1200, f(0), SOFT)])
        sc.k(g, "positionY", [(0, f(560), LIN), (t, f(560), HOLD), (t + 350, f(600), OUT), (t + 1200, f(900), EIN)])
        scale_keys(sc, g, [(0, f(92), LIN), (t, f(92), HOLD), (t + 350, f(100), OUT), (t + 1200, f(90), SOFT)])
        lid += 5
        t += gap
        gap = max(70, int(gap * 0.82))
    return sc


# ================================================================== S12  the model hasn't changed (overlay)
def S12():
    sc = new("S12_Model", 55.85, 60.45)
    FX = overlay(sc)
    w = sc.word
    MOD, PLA, PROS, KONK = w(56.24), w(57.78), w(58.26), w(59.58)
    END = sc.t(60.25)
    X0, Y0, CW = 70, 170, 580
    C = sc.group(110, "Model", FX, X0 + CW / 2, 440, X0 + CW / 2, 440, op=0)
    card_bg(sc, 111, C, X0, Y0, CW, 540, r=40, sh=(0.18, 60, 18))
    sc.text(112, "K", C, X0 + 40, Y0 + 66, "Model się nie zmienił", 28, A_GREY, style="Medium")
    rows = [(PLA, "Ludzie płacą", A_GREEN), (PROS, "za prosty produkt", A_BLUE), (KONK, "na konkretny problem", A_RED)]
    for i, (t, nm, c) in enumerate(rows):
        y = Y0 + 110 + i * 140
        g = sc.group(120 + i * 6, nm, C, X0 + CW / 2, y + 45, X0 + CW / 2, y + 45, op=0)
        sc.rect(121 + i * 6, "Row", g, X0 + 30, y, CW - 60, 90, a(c, 0.08), r=26)
        sc.rect(122 + i * 6, "Dot", g, X0 + 60, y + 33, 24, 24, c, r=12)
        sc.text(123 + i * 6, "T", g, X0 + 104, y + 56, nm, 32, A_INK)
        fade(sc, g, t - 60, d_in=180)
        pop(sc, g, t - 60, 500, 90)
        if i < 2:
            ar = sc.path(124 + i * 6, "Arrow", C, [(X0 + 72, y + 96), (X0 + 72, y + 134)], stroke=(A_LINE, 4), closed=False, op=0)
            fade(sc, ar, max(t, rows[i + 1][0]) + 100, d_in=200)
    card_in(sc, C, MOD - 200, END)
    return sc
ovl("S12")


# ================================================================== S13  Maps: 6 months vs 48 hours to the first sale
def S13():
    sc = new("S13_Trasa", 60.50, 64.75)
    sc.bg = [0.957, 0.953, 0.937, 1]
    w = sc.word
    SZY, ZERA, ZAR = w(61.66), w(62.86), w(64.22)
    MAP = sc.group(100, "Map", None, 960, 540, 960, 540)
    sc.path(101, "Water", MAP, [(1400, 1080), (1920, 760), (1920, 1080)], fill=[0.72, 0.85, 0.97, 1])
    sc.rect(102, "Park", MAP, 220, 640, 360, 240, [0.80, 0.91, 0.77, 1], r=40)
    sc.rect(103, "Park2", MAP, 1240, 120, 300, 180, [0.80, 0.91, 0.77, 1], r=34)
    roads = [[(0, 820), (1920, 820)], [(0, 520), (1920, 520)], [(0, 260), (1920, 260)], [(420, 0), (420, 1080)],
             [(900, 0), (900, 1080)], [(1380, 0), (1380, 1080)], [(1700, 0), (1700, 1080)]]
    for i, pts in enumerate(roads):
        sc.path(104 + i, "Road", MAP, pts, stroke=(A_BG, 26), closed=False)
    scale_keys(sc, MAP, [(0, f(100), LIN), (sc.dur, f(106), LIN)])
    A_, B_ = (420, 820), (1380, 260)
    slow = [A_, (420, 520), (180, 520), (180, 260), (900, 260), (900, 820), (1700, 820), (1700, 520), (1380, 520), B_]
    fast = [A_, (900, 820), (900, 520), (1380, 520), B_]
    sr = sc.path(120, "Slow", MAP, slow, stroke=(a(A_GREY, 0.7), 12), closed=False, trim=0)
    sc.k(sr, "trimEnd", [(0, f(0), LIN), (150, f(0), HOLD), (SZY + 300, f(100), INOUT)])
    fr_c = sc.path(121, "Fast casing", MAP, fast, stroke=([0.0, 0.33, 0.75, 1], 20), closed=False, trim=0)
    fr = sc.path(122, "Fast", MAP, fast, stroke=(A_BLUE, 13), closed=False, trim=0)
    for lid in (fr_c, fr):
        sc.k(lid, "trimEnd", [(0, f(0), LIN), (ZERA - 100, f(0), HOLD), (ZERA + 1100, f(100), INOUT)])
    st = sc.group(130, "Start", MAP, A_[0], A_[1], A_[0], A_[1])
    sc.rect(131, "Dot", st, A_[0] - 22, A_[1] - 22, 44, 44, A_BLUE, r=22, stroke=(A_BG, 7))
    pin = sc.group(135, "Pin", MAP, B_[0], B_[1], B_[0], B_[1], op=0)
    sc.rect(136, "Head", pin, B_[0] - 30, B_[1] - 94, 60, 60, A_GREEN, r=30, stroke=(A_BG, 5))
    check(sc, 137, pin, B_[0], B_[1] - 63, 18, A_BG, 4)
    sc.path(138, "Stem", pin, [(B_[0], B_[1] - 34), (B_[0], B_[1])], stroke=(A_GREEN, 5), closed=False)
    sc.k(pin, "opacity", [(0, f(0), LIN), (100, f(0), HOLD), (300, f(100), SOFT)])
    sc.k(pin, "positionY", [(0, f(B_[1] - 120), LIN), (100, f(B_[1] - 120), HOLD), (500, f(B_[1]), APPLE),
                            (ZAR - 1, f(B_[1]), HOLD), (ZAR + 150, f(B_[1] - 26), OUT), (ZAR + 450, f(B_[1]), EIN)])

    def bubble(base, x, y, txt, colr, fg, t):
        wd = adv(txt, 30, "SemiBold") + 50
        g = sc.group(base, txt, MAP, x, y, x, y, op=0)
        b = sc.rect(base + 1, "B", g, x - wd / 2, y - 30, wd, 60, colr, r=30)
        sc.shadow(b, 0.14, 20, 6)
        sc.text(base + 2, "T", g, x, y + 11, txt, 30, fg, just="center")
        fade(sc, g, t, d_in=180)
        pop(sc, g, t, 450, 70)
        return g
    bubble(140, 180, 400, "6–12 miesięcy", A_BG, A_GREY, SZY - 200)
    bubble(145, 1140, 600, "48 h", A_BLUE, A_BG, ZERA + 900)
    lb = sc.group(150, "Dest", MAP, B_[0], B_[1] - 150, B_[0], B_[1] - 150, op=0)
    pill_text(sc, 151, lb, B_[0], B_[1] - 150, "pierwsza sprzedaż", 26, A_INK, A_BG, style="SemiBold")
    fade(sc, lb, ZAR - 300, d_in=200)
    lb2 = sc.group(155, "Start lab", MAP, A_[0], A_[1] + 70, A_[0], A_[1] + 70, op=0)
    pill_text(sc, 156, lb2, A_[0], A_[1] + 70, "zero", 26, A_INK, A_BG, style="SemiBold")
    fade(sc, lb2, 200, d_in=200)
    return sc


# ================================================================== S14  product launch: the app icon
def S14():
    sc = new("S14_Cyfrowy-Autopilot", 64.80, 67.05)
    sc.apple_bg()
    w = sc.word
    STW, NAME = w(65.52), w(66.06)
    IC = sc.group(100, "Icon", None, 960, 440, 960, 440, op=0)
    gl = sc.rect(101, "Glow", IC, 960 - 200, 440 - 200, 400, 400, a(A_BLUE, 0.35), r=200)
    sc.blur(gl, 7200, 80)
    sq = sc.rect(102, "Squircle", IC, 960 - 150, 440 - 150, 300, 300, A_BLUE, r=70)
    sc.shadow(sq, 0.28, 60, 24)
    sc.rect(103, "Top shade", IC, 960 - 150, 440 - 150, 300, 150, [1, 1, 1, 0.10], r=70)
    sc.path(104, "Glyph", IC, [(890, 500), (960, 360), (1030, 500), (960, 465)], fill=A_BG)
    SG = sc.group(110, "Sheen", IC, 0, 0)
    sh = sc.rect(111, "Sheen bar", SG, 700, 220, 70, 440, [1, 1, 1, 0.55])
    sc.k(sh, "rotation", [(0, f(20), LIN)])
    sc.blur(sh, 7201, 14)
    sc.k(sh, "positionX", [(0, f(700), LIN), (STW + 300, f(700), HOLD), (STW + 1000, f(1160), INOUT)])
    mt = sc.rect(112, "Matte", IC, 960 - 150, 440 - 150, 300, 300, A_BG, r=70)
    sc.matte(SG, mt)
    fade(sc, IC, STW - 300, d_in=200)
    scale_keys(sc, IC, [(0, f(30), LIN), (STW - 300, f(30), HOLD), (STW + 300, f(108), OUT), (STW + 650, f(100), APPLE)])
    nm = sc.text(120, "Name", None, 960, 760, "Cyfrowy Autopilot", 96, A_INK, tracking=-40, just="center",
                 animators=[Scene.reveal_animator(1, 11, dy=24, blur_=16)])
    sc.reveal_words(nm, 11, [NAME, NAME + 300], step=220)
    return sc


# ================================================================== S15  not a year-long course → one goal (overlay)
def S15():
    sc = new("S15_Jeden-cel", 67.05, 72.70)
    FX = overlay(sc)
    w = sc.word
    KURS, ROK, OGL, CEL, ZBUD, SPR = w(67.44), w(68.08), w(68.28), w(69.96), w(70.66), w(72.16)
    END = sc.t(72.45)
    X0, Y0, CW = 70, 170, 600
    C = sc.group(110, "Course", FX, X0 + CW / 2, 440, X0 + CW / 2, 440, op=0)
    card_bg(sc, 111, C, X0, Y0, CW, 540, r=40, sh=(0.18, 60, 18))
    PL = sc.group(120, "Playlist", C, 0, 0)
    sc.text(121, "K", PL, X0 + 40, Y0 + 66, "Kurs · 248 lekcji", 30, A_INK)
    for i in range(4):
        y = Y0 + 100 + i * 82
        sc.rect(122 + i * 4, "Thumb", PL, X0 + 40, y, 110, 64, A_FILL, r=10)
        sc.path(123 + i * 4, "Play", PL, [(X0 + 88, y + 20), (X0 + 108, y + 32), (X0 + 88, y + 44)], fill=A_GREY)
        sc.rect(124 + i * 4, "T", PL, X0 + 170, y + 14, [260, 220, 280, 200][i], 14, A_LINE, r=7)
        sc.rect(125 + i * 4, "S", PL, X0 + 170, y + 40, 120, 10, A_FILL, r=5)
    sc.text(140, "Prog", PL, X0 + 40, Y0 + 470, "12 miesięcy oglądania", 24, A_GREY, style="Medium")
    sc.rect(141, "Track", PL, X0 + 40, Y0 + 492, CW - 80, 8, A_LINE, r=4)
    sc.rect(142, "Fill", PL, X0 + 40, Y0 + 492, 18, 8, A_GREY, r=4)
    st = sc.rect(143, "Strike", PL, X0 + 30, Y0 + 270, 0.01, 6, A_RED, r=3)
    sc.k(st, "rectSize", [(0, v2(0.01, 6), LIN), (OGL, v2(0.01, 6), HOLD), (OGL + 400, v2(CW - 60, 6), APPLE)])
    sc.k(PL, "opacity", [(0, f(100), LIN), (CEL - 150, f(100), HOLD), (CEL + 150, f(0), SOFT)])
    GO = sc.group(150, "Goal", C, X0 + CW / 2, Y0 + 270, X0 + CW / 2, Y0 + 270, op=0)
    sc.text(151, "K", GO, X0 + 40, Y0 + 66, "Jeden cel", 30, A_BLUE)
    cb = sc.rect(152, "Box", GO, X0 + 40, Y0 + 210, 64, 64, [1, 1, 1, 0], r=32, stroke=(A_LINE, 4))
    sc.k(cb, "fillColor", [(0, col([1, 1, 1, 0]), LIN), (SPR, col([1, 1, 1, 0]), HOLD), (SPR + 200, col(A_BLUE), SOFT)])
    sc.k(cb, "strokeColor", [(0, col(A_LINE), LIN), (SPR, col(A_LINE), HOLD), (SPR + 200, col(A_BLUE), SOFT)])
    ck = check(sc, 153, GO, X0 + 72, Y0 + 243, 26, A_BG, 5, op=0)
    fade(sc, ck, SPR + 120, d_in=140)
    sc.text(154, "T1", GO, X0 + 130, Y0 + 238, "Zbudować coś,", 40, A_INK, tracking=-15)
    sc.text(155, "T2", GO, X0 + 130, Y0 + 288, "co możesz sprzedawać", 40, A_INK, tracking=-15)
    sc.k(GO, "opacity", [(0, f(0), LIN), (CEL, f(0), HOLD), (CEL + 250, f(100), SOFT)])
    pop(sc, GO, CEL, 550, 92)
    card_in(sc, C, KURS - 250, END)
    return sc
ovl("S15")


# ================================================================== S16  the system demo: market → 10 ideas → pick → direction
def S16():
    sc = new("S16_System", 72.70, 79.85)
    sc.apple_bg()
    w = sc.word
    RYN, DZIES, WYB, KIER, KOGO, CENA, SPRZ = w(73.14), w(74.48), w(75.78), w(76.46), w(77.36), w(78.68), w(79.12)
    WN = sc.group(100, "App", None, 960, 540, 960, 540, op=0)
    card_bg(sc, 101, WN, 200, 110, 1520, 860, r=30, sh=(0.14, 80, 24))
    sc.rect(102, "Bar", WN, 200, 110, 1520, 64, A_FILL, r=30)
    sc.rect(103, "Bar sq", WN, 200, 144, 1520, 30, A_FILL)
    for i, c in enumerate([[1.0, 0.37, 0.34, 1], [1.0, 0.74, 0.18, 1], [0.16, 0.79, 0.25, 1]]):
        sc.rect(104 + i, "Light", WN, 230 + i * 26, 136, 14, 14, c, r=7)
    sc.text(107, "Title", WN, 960, 152, "Cyfrowy Autopilot", 22, A_GREY, style="Medium", just="center")
    fade(sc, WN, 30, d_in=240)
    scale_keys(sc, WN, [(0, f(96), LIN), (30, f(96), HOLD), (700, f(100), OUT)])
    # step 1: markets
    sc.text(110, "Step1", WN, 260, 250, "1  Wybierz rynek", 30, A_INK)
    mk = ["Zdrowie", "Pieniądze", "Relacje", "Nauka", "Hobby"]
    for i, m in enumerate(mk):
        x = 260 + i * 200
        bg = sc.rect(111 + i * 2, "Chip", WN, x, 280, 180, 60, A_FILL, r=30)
        tx = sc.text(112 + i * 2, "T", WN, x + 90, 318, m, 24, A_INK, style="Medium", just="center")
        if m == "Nauka":
            sc.k(bg, "fillColor", [(0, col(A_FILL), LIN), (RYN + 450, col(A_FILL), HOLD), (RYN + 600, col(A_BLUE), SOFT)])
            sc.k(tx, "fillColor", [(0, col(A_INK), LIN), (RYN + 450, col(A_INK), HOLD), (RYN + 600, col(A_BG), SOFT)])
    # step 2: ten ideas cascade
    s2 = sc.text(130, "Step2", WN, 260, 420, "2  10 konkretnych pomysłów", 30, A_INK, op=0)
    fade(sc, s2, DZIES - 300, d_in=200)
    ideas = ["Plan nauki na sesję", "Start w 5 minut", "Notatki, które działają", "Matura bez stresu", "Fiszki z AI",
             "Nauka języka 15 min", "Koniec z odkładaniem", "Pamięć do egzaminu", "Szybkie czytanie", "Tydzień z planem"]
    for i, idea in enumerate(ideas):
        cx, cy = 260 + (i % 5) * 200, 450 + (i // 5) * 130
        g = sc.group(140 + i * 4, idea, WN, cx + 90, cy + 55, cx + 90, cy + 55, op=0)
        bg = sc.rect(141 + i * 4, "Card", g, cx, cy, 180, 110, A_BG, r=18, stroke=(A_LINE, 2))
        words_ = idea.split(" ")
        l1 = " ".join(words_[:2]); l2 = " ".join(words_[2:])
        sc.text(142 + i * 4, "L1", g, cx + 16, cy + 42, l1, 20, A_INK, style="SemiBold")
        sc.text(143 + i * 4, "L2", g, cx + 16, cy + 70, l2, 20, A_INK, style="SemiBold")
        t = DZIES + i * 70
        pop(sc, g, t, 400, 85)
        if i == 2:
            fade(sc, g, t, d_in=150)
            sc.k(bg, "strokeColor", [(0, col(A_LINE), LIN), (WYB + 300, col(A_LINE), HOLD), (WYB + 450, col(A_BLUE), SOFT)])
        else:
            sc.k(g, "opacity", [(0, f(0), LIN), (t, f(0), HOLD), (t + 150, f(100), SOFT), (WYB + 300, f(100), HOLD), (WYB + 600, f(35), SOFT)])
    # step 3: direction panel
    PN = sc.group(190, "Direction", WN, 1530, 600, 1530, 600, op=0)
    sc.rect(191, "Panel", PN, 1300, 230, 380, 700, a(A_BLUE, 0.06), r=24)
    sc.text(192, "H", PN, 1330, 290, "Kierunek", 32, A_BLUE)
    rows = [("Dla kogo", "uczniowie i studenci", KOGO), ("Cena", "57 zł", CENA), ("Jak sprzedawać", "reklamy + content", SPRZ)]
    for i, (k_, v_, t) in enumerate(rows):
        y = 360 + i * 150
        g = sc.group(193 + i * 4, k_, PN, 0, 0, op=0)
        sc.text(194 + i * 4, "K", g, 1330, y, k_, 22, A_GREY, style="Medium")
        sc.text(195 + i * 4, "V", g, 1330, y + 44, v_, 30, A_INK)
        fade(sc, g, t - 60, d_in=180)
        sc.k(g, "positionX", [(0, f(20), LIN), (t - 60, f(20), HOLD), (t + 450, f(0), OUT)])
    sc.k(PN, "opacity", [(0, f(0), LIN), (KIER - 100, f(0), HOLD), (KIER + 200, f(100), SOFT)])
    sc.k(PN, "positionX", [(0, f(1600), LIN), (KIER - 100, f(1600), HOLD), (KIER + 600, f(1530), OUT)])
    # cursor: market chip, then idea card
    CU = cursor(sc, 210, WN, 1000, 900)
    sc.k(CU, "opacity", [(0, f(0), LIN), (RYN - 300, f(0), HOLD), (RYN - 100, f(100), SOFT)])
    sc.kpos(CU, [(0, 1000, 900, LIN), (RYN - 300, 1000, 900, HOLD), (RYN + 350, 900, 318, APPLE),
                 (WYB - 200, 900, 318, HOLD), (WYB + 250, 640, 610, APPLE)])
    scale_keys(sc, CU, [(0, f(100), LIN), (RYN + 380, f(100), HOLD), (RYN + 450, f(84), OUT), (RYN + 650, f(100), APPLE),
                        (WYB + 260, f(100), HOLD), (WYB + 330, f(84), OUT), (WYB + 530, f(100), APPLE)])
    return sc


# ================================================================== S17  Shortcuts pipeline: prompt → product → page → marketing
def S17():
    sc = new("S17_Pipeline", 79.90, 84.55)
    sc.apple_bg()
    w = sc.word
    T_ = [w(80.58), w(81.80), w(82.60), w(83.86)]
    KLIK = w(83.00)
    blocks = [("Gotowy prompt", A_GREY, "kopiuj i wklej"), ("Produkt", A_BLUE, "tworzy się sam"),
              ("Strona", A_GREEN, "jednym kliknięciem"), ("Marketing", A_ORANGE, "reklamy i content")]
    for i, (nm, c, sub) in enumerate(blocks):
        y = 170 + i * 200
        g = sc.group(100 + i * 8, nm, None, 960, y + 70, 960, y + 70, op=0)
        sc.rect(101 + i * 8, "Block", g, 620, y, 680, 140, c, r=32)
        sc.rect(102 + i * 8, "Icon", g, 660, y + 35, 70, 70, [1, 1, 1, 0.25], r=18)
        sc.text(103 + i * 8, "N", g, 760, y + 68, nm, 40, A_BG, tracking=-10)
        sc.text(104 + i * 8, "S", g, 760, y + 106, sub, 24, [1, 1, 1, 0.8], style="Medium")
        t = T_[i]
        fade(sc, g, t - 80, d_in=180)
        sc.k(g, "positionY", [(0, f(y + 110), LIN), (t - 80, f(y + 110), HOLD), (t + 500, f(y + 70), OUT)])
        ck = ok_badge(sc, 105 + i * 8, g, 1250, y + 70, t + 450, d=48, color=[1, 1, 1, 0.35])
        if i < 3:
            ln = sc.rect(160 + i, "Link", None, 958, y + 142, 4, 0.01, A_LINE, r=2)
            sc.k(ln, "rectSize", [(0, v2(4, 0.01), LIN), (T_[i + 1] - 300, v2(4, 0.01), HOLD), (T_[i + 1] - 80, v2(4, 56), OUT)])
    CU = cursor(sc, 180, None, 1500, 900)
    sc.k(CU, "opacity", [(0, f(0), LIN), (KLIK - 700, f(0), HOLD), (KLIK - 500, f(100), SOFT), (KLIK + 900, f(100), HOLD), (KLIK + 1100, f(0), SOFT)])
    sc.kpos(CU, [(0, 1500, 900, LIN), (KLIK - 700, 1500, 900, HOLD), (KLIK - 60, 1180, 600, APPLE)])
    scale_keys(sc, CU, [(0, f(100), LIN), (KLIK - 40, f(100), HOLD), (KLIK + 30, f(84), OUT), (KLIK + 230, f(100), APPLE)])
    rp = sc.rect(185, "Ripple", None, 1150, 570, 60, 60, [1, 1, 1, 0], r=30, stroke=(A_BG, 4), ax=30, ay=30, op=0)
    sc.k(rp, "opacity", [(0, f(0), LIN), (KLIK, f(0), HOLD), (KLIK + 60, f(100), SOFT), (KLIK + 500, f(0), SOFT)])
    scale_keys(sc, rp, [(0, f(40), LIN), (KLIK, f(40), HOLD), (KLIK + 500, f(260), OUT)])
    return sc


# ================================================================== S18  „co mam teraz zrobić?” → Następny krok (overlay)
def S18():
    sc = new("S18_Nastepny-krok", 84.55, 91.70)
    FX = overlay(sc)
    w = sc.word
    PYT, ZROB, PRZ, KROK = w(85.04), w(86.18), w(87.10), w(88.14)
    T_ = [w(88.96), w(89.42), w(89.90), w(90.30)]
    END = sc.t(91.45)
    X0, Y0, CW = 70, 150, 600
    C = sc.group(110, "Steps", FX, X0 + CW / 2, 450, X0 + CW / 2, 450, op=0)
    card_bg(sc, 111, C, X0, Y0, CW, 620, r=40, sh=(0.18, 60, 18))
    fld = sc.rect(112, "Field", C, X0 + 30, Y0 + 40, CW - 60, 100, A_FILL, r=30)
    q = "Co ja mam teraz zrobić?"
    tx = sc.text(113, "Q", C, X0 + 60, Y0 + 102, "", 30, A_GREY, style="Medium")
    sc.k(tx, "textContent", [(0, s(""), LIN)] + [(PYT + (ZROB - PYT) * i / len(q), s(q[:i + 1]), HOLD) for i in range(len(q))])
    sc.k(tx, "opacity", [(0, f(100), LIN), (PRZ - 150, f(100), HOLD), (PRZ + 50, f(0), SOFT)])
    sc.k(fld, "fillColor", [(0, col(A_FILL), LIN), (PRZ - 100, col(A_FILL), HOLD), (PRZ + 200, col(A_BLUE), SOFT)])
    nx = sc.text(114, "Next", C, X0 + CW / 2, Y0 + 104, "Następny krok  →", 34, A_BG, just="center", op=0)
    fade(sc, nx, PRZ + 100, d_in=200)
    BT = sc.group(115, "Btn press", C, X0 + CW / 2, Y0 + 90, X0 + CW / 2, Y0 + 90)
    sc.k(112, "rectSize", [(0, v2(CW - 60, 100), LIN)])
    scale_keys(sc, C, [(0, f(96), LIN), (PYT - 300, f(96), HOLD), (PYT + 400, f(100), OUT), (KROK - 40, f(100), HOLD),
                       (KROK + 60, f(98.5), OUT), (KROK + 260, f(100), APPLE)])
    names = ["Produkt", "Strona", "Oferta", "Materiały do startu"]
    for i, (nm, t) in enumerate(zip(names, T_)):
        y = Y0 + 190 + i * 100
        g = sc.group(120 + i * 5, nm, C, 0, 0, op=0)
        sc.text(121 + i * 5, "N", g, X0 + 120, y + 50, nm, 32, A_INK, style="Medium")
        ok_badge(sc, 122 + i * 5, g, X0 + 72, y + 40, t, d=44)
        fade(sc, g, t - 60, d_in=160)
        sc.k(g, "positionX", [(0, f(20), LIN), (t - 60, f(20), HOLD), (t + 400, f(0), OUT)])
    sc.k(C, "opacity", [(0, f(0), LIN), (PYT - 300, f(0), HOLD), (PYT - 40, f(100), SOFT), (END, f(100), HOLD), (END + 250, f(0), SOFT)])
    return sc
ovl("S18")


# ================================================================== S19  AirDrop: one product, many buyers
def S19():
    sc = new("S19_AirDrop", 94.40, 101.25)
    sc.apple_bg()
    w = sc.word
    PROD, RAZ, NIE, SZT, SPRZ, OSOB, NOWA = w(94.62), w(95.92), w(96.48), w(97.82), w(98.92), w(99.76), w(100.80)
    CX, CY = 960, 520
    # the file
    FL = sc.group(100, "File", None, CX, CY, CX, CY, op=0)
    pg = sc.rect(101, "Page", FL, CX - 80, CY - 105, 160, 210, A_BG, r=14, stroke=(A_LINE, 2))
    sc.shadow(pg, 0.14, 30, 10)
    sc.rect(102, "Circle", FL, CX - 40, CY - 70, 80, 80, A_BLUE, r=40)
    for i in range(3):
        sc.rect(103 + i, "Line", FL, CX - 50, CY + 30 + i * 20, [100, 80, 90][i], 9, A_LINE, r=4.5)
    fade(sc, FL, PROD - 100, d_in=200)
    pop(sc, FL, PROD - 100, 600, 70)
    lb = sc.group(110, "Once", None, CX, CY + 170, CX, CY + 170, op=0)
    pill_text(sc, 111, lb, CX, CY + 170, "tworzysz raz", 28, A_BLUE, a(A_BLUE, 0.1), style="SemiBold")
    sc.k(lb, "opacity", [(0, f(0), LIN), (RAZ - 200, f(0), HOLD), (RAZ, f(100), SOFT), (SPRZ - 300, f(100), HOLD), (SPRZ - 100, f(0), SOFT)])
    # physical stock you don't need
    BX = sc.group(120, "Boxes", None, 0, 0, op=0)
    for i in range(6):
        x, y = 300 + (i % 3) * 110, 560 - (i // 3) * 95
        sc.rect(121 + i * 2, "Box", BX, x, y, 100, 85, [0.86, 0.72, 0.52, 1], r=8)
        sc.rect(122 + i * 2, "Tape", BX, x + 42, y, 16, 85, [0.75, 0.60, 0.40, 1])
    stk = sc.rect(135, "Strike", BX, 280, 545, 0.01, 8, A_RED, r=4)
    sc.k(stk, "rectSize", [(0, v2(0.01, 8), LIN), (SZT - 100, v2(0.01, 8), HOLD), (SZT + 300, v2(360, 8), APPLE)])
    sc.k(BX, "opacity", [(0, f(0), LIN), (NIE, f(0), HOLD), (NIE + 250, f(100), SOFT), (SPRZ - 300, f(100), HOLD), (SPRZ, f(0), SOFT)])
    # buyers around, copies fly out
    N = 8
    R = 330
    for i in range(N):
        ang = math.radians(-90 + i * 360 / N)
        ax_, ay_ = CX + R * 1.45 * math.cos(ang), CY + R * math.sin(ang)
        t_av = SPRZ - 200 + i * 60
        av = sc.group(140 + i * 6, "Buyer", None, ax_, ay_, ax_, ay_, op=0)
        sc.rect(141 + i * 6, "Av", av, ax_ - 44, ay_ - 44, 88, 88, A_FILL, r=44, stroke=(A_BG, 4))
        sc.rect(142 + i * 6, "Head", av, ax_ - 14, ay_ - 26, 28, 28, A_GREY, r=14)
        sc.path(143 + i * 6, "Body", av, arc(ax_, ay_ + 30, 24, 180, 360, 14), fill=A_GREY)
        fade(sc, av, t_av, d_in=160)
        pop(sc, av, t_av, 450, 60)
        t_cp = SPRZ + 250 + i * 190
        cp = sc.rect(144 + i * 6, "Copy", None, CX - 30, CY - 40, 60, 80, A_BG, r=8, stroke=(A_BLUE, 3), op=0)
        sc.k(cp, "opacity", [(0, f(0), LIN), (t_cp, f(0), HOLD), (t_cp + 80, f(100), SOFT), (t_cp + 600, f(100), HOLD), (t_cp + 750, f(0), SOFT)])
        sc.kpos(cp, [(0, CX - 30, CY - 40, LIN), (t_cp, CX - 30, CY - 40, HOLD), (t_cp + 600, ax_ - 30, ay_ - 40, APPLE)])
        ok_badge(sc, 200 + i * 4, None, ax_ + 34, ay_ - 34, t_cp + 600, d=34)
    cnt = sc.text(240, "Count", None, CX, 110, "", 44, A_INK, just="center")
    sc.k(cnt, "textContent", [(0, s(""), LIN)] + [(SPRZ + 850 + i * 190, s(f"Sprzedane: {i + 1}"), HOLD) for i in range(N)])
    nw = sc.group(245, "No rework", None, CX, CY + 170, CX, CY + 170, op=0)
    pill_text(sc, 246, nw, CX, CY + 170, "bez tworzenia od nowa", 28, A_GREEN, a(A_GREEN, 0.12), style="SemiBold")
    fade(sc, nw, NOWA - 300, d_in=200)
    return sc


# ================================================================== S20  iOS Calculator: 57 × 3
def S20():
    sc = new("S20_Kalkulator", 101.30, 107.25)
    sc.apple_bg()
    w = sc.word
    PROD, P57, P3, DZIEN, P170 = w(103.28), w(103.90), w(104.96), w(105.58), w(106.00)
    CAL = sc.group(100, "Calculator", None, 1240, 540, 1240, 540, op=0)
    body = sc.rect(101, "Body", CAL, 1020, 90, 440, 900, [0.04, 0.04, 0.05, 1], r=60)
    sc.shadow(body, 0.3, 70, 26)
    disp = sc.text(102, "Display", CAL, 1420, 380, "0", 110, A_BG, style="Regular", tracking=-30, just="right")
    seq = [(P57 - 60, "5"), (P57 + 120, "57"), (P3 + 200, "3"), (P170, "171")]
    sc.k(disp, "textContent", [(0, s("0"), LIN)] + [(t, s(v), HOLD) for t, v in seq])
    keys = [["C", "±", "%", "÷"], ["7", "8", "9", "×"], ["4", "5", "6", "−"], ["1", "2", "3", "+"], ["0", "", ",", "="]]
    press = {"5": P57 - 60, "7": P57 + 120, "×": P3 - 60, "3": P3 + 200, "=": P170 - 60}
    lid = 110
    for r_, row in enumerate(keys):
        for c_, k_ in enumerate(row):
            if r_ == 4 and c_ == 1:
                continue
            cx, cy = 1078 + c_ * 108, 470 + r_ * 108
            op_col = A_ORANGE if c_ == 3 else ([0.65, 0.65, 0.66, 1] if r_ == 0 else [0.2, 0.2, 0.21, 1])
            wd = 204 if (r_ == 4 and c_ == 0) else 92
            b = sc.rect(lid, "Key", CAL, cx - 46, cy - 46, wd, 92, op_col, r=46)
            sc.text(lid + 1, "K", CAL, cx + (wd - 92) / 2 - (56 if r_ == 4 and c_ == 0 else 0), cy + 14, k_, 40,
                    A_INK if r_ == 0 else A_BG, style="Medium", just="center")
            if k_ in press:
                t = press[k_]
                hi = [1, 1, 1, 1] if c_ == 3 else [0.45, 0.45, 0.46, 1]
                sc.k(b, "fillColor", [(0, col(op_col), LIN), (t, col(op_col), HOLD), (t + 60, col(hi), SOFT), (t + 300, col(op_col), SOFT)])
            lid += 2
    fade(sc, CAL, 60, d_in=260)
    sc.k(CAL, "positionY", [(0, f(580), LIN), (60, f(580), HOLD), (800, f(540), OUT)])
    # the story on the left
    L = [(PROD, "Produkt", "57 zł"), (P3, "Sprzedaży dziennie", "3"), (P170, "Dziennie", "171 zł")]
    for i, (t, k_, v_) in enumerate(L):
        y = 330 + i * 190
        g = sc.group(200 + i * 4, k_, None, 0, 0, op=0)
        sc.text(201 + i * 4, "K", g, 200, y, k_, 30, A_GREY, style="Medium")
        sc.text(202 + i * 4, "V", g, 200, y + 90, v_, 90, A_GREEN if i == 2 else A_INK, tracking=-35)
        fade(sc, g, t - 60, d_in=200)
        sc.k(g, "positionY", [(0, f(20), LIN), (t - 60, f(20), HOLD), (t + 500, f(0), OUT)])
    return sc


# ================================================================== S21  30 days → 5 130 zł
def S21():
    sc = new("S21_Miesiac", 107.25, 112.22)
    sc.apple_bg()
    w = sc.word
    DNI, P5130, TYL = w(107.80), w(109.06), w(110.82)
    sc.text(100, "Head", None, 260, 220, "30 dni", 60, A_INK, tracking=-25)
    tot = sc.text(101, "Total", None, 1660, 230, "0 zł", 100, A_INK, tracking=-40, just="right")
    sc.k(tot, "textContent", [(0, s("0 zł"), LIN)] + Scene.roll_keys(DNI, P5130 + 900, zl, 0, 5130, ease_pow=1.6)[1:])
    sc.k(tot, "fillColor", [(0, col(A_INK), LIN), (P5130 + 800, col(A_INK), HOLD), (P5130 + 1000, col(A_GREEN), SOFT)])
    for d in range(30):
        c_, r_ = d % 10, d // 10
        x, y = 260 + c_ * 142, 330 + r_ * 160
        t = DNI + d * 55
        g = sc.group(110 + d * 3, f"Day {d+1}", None, x + 64, y + 64, x + 64, y + 64)
        bx = sc.rect(111 + d * 3, "Day", g, x, y, 128, 128, A_FILL, r=24)
        sc.k(bx, "fillColor", [(0, col(A_FILL), LIN), (t, col(A_FILL), HOLD), (t + 200, col(a(A_GREEN, 0.16)), SOFT)])
        sc.mono(112 + d * 3, "N", g, x + 20, y + 40, str(d + 1), 22, A_GREY)
        pv = sc.mono(200 + d, "Plus", g, x + 64, y + 96, "+171", 22, DKGREEN, just="center", op=0)
        fade(sc, pv, t + 60, d_in=150)
        scale_keys(sc, g, [(0, f(100), LIN), (t, f(100), HOLD), (t + 120, f(106), OUT), (t + 360, f(100), APPLE)])
    tg = sc.group(240, "3/day", None, 960, 860, 960, 860, op=0)
    pill_text(sc, 241, tg, 960, 860, "tylko 3 sprzedaże dziennie", 34, A_BG, A_BLUE, style="SemiBold")
    fade(sc, tg, TYL - 100, d_in=200)
    pop(sc, tg, TYL - 100, 450, 80)
    return sc


# ================================================================== S22  not 300, not 500, not 1000
def S22():
    sc = new("S22_Nie-300", 112.20, 114.02)
    sc.apple_bg()
    w = sc.word
    T_ = [w(112.38), w(113.00), w(113.52)]
    for i, (n, t) in enumerate(zip(["300", "500", "1000"], T_)):
        x = 960 + (i - 1) * 520
        g = sc.group(100 + i * 4, n, None, x, 540, x, 540, op=0)
        sc.text(101 + i * 4, "N", g, x, 590, n, 190, A_INK, tracking=-70, just="center")
        sc.text(102 + i * 4, "S", g, x, 670, "klientów", 32, A_GREY, style="Medium", just="center")
        wd = adv(n, 190, "SemiBold")
        st = sc.rect(103 + i * 4, "Strike", g, x - wd / 2 - 10, 525, 0.01, 12, A_RED, r=6)
        sc.k(st, "rectSize", [(0, v2(0.01, 12), LIN), (t + 150, v2(0.01, 12), HOLD), (t + 450, v2(wd + 20, 12), APPLE)])
        sc.k(g, "opacity", [(0, f(0), LIN), (t - 60, f(0), HOLD), (t + 120, f(100), SOFT), (t + 600, f(100), HOLD), (t + 900, f(35), SOFT)])
        pop(sc, g, t - 60, 450, 80)
    return sc


# ================================================================== S23  three clients a day is enough (overlay)
def S23():
    sc = new("S23_Trzech-klientow", 115.90, 120.30)
    FX = overlay(sc)
    w = sc.word
    POT, MAT, INT = w(116.18), w(117.94), w(119.74)
    END = sc.t(120.05)
    X0, Y0, CW = 70, 200, 580
    C = sc.group(110, "Three", FX, X0 + CW / 2, 430, X0 + CW / 2, 430, op=0)
    card_bg(sc, 111, C, X0, Y0, CW, 460, r=40, sh=(0.18, 60, 18))
    sc.text(112, "K", C, X0 + 40, Y0 + 66, "Wystarczy", 28, A_GREY, style="Medium")
    for i in range(3):
        cx = X0 + 100 + i * 110
        av = sc.group(120 + i * 4, "Av", C, cx, Y0 + 160, cx, Y0 + 160, op=0)
        sc.rect(121 + i * 4, "C", av, cx - 46, Y0 + 114, 92, 92, a(A_BLUE, 0.12), r=46)
        sc.rect(122 + i * 4, "H", av, cx - 15, Y0 + 128, 30, 30, A_BLUE, r=15)
        sc.path(123 + i * 4, "B", av, arc(cx, Y0 + 192, 25, 180, 360, 14), fill=A_BLUE)
        t = POT + 200 + i * 120
        fade(sc, av, t, d_in=160)
        pop(sc, av, t, 450, 60)
    sc.text(140, "T", C, X0 + 40, Y0 + 290, "3 klientów dziennie", 40, A_INK, tracking=-15)
    ch = sc.path(141, "Chart", C, [(X0 + 40, Y0 + 420), (X0 + 160, Y0 + 400), (X0 + 280, Y0 + 380), (X0 + 400, Y0 + 340), (X0 + 530, Y0 + 300)],
                 stroke=(A_GREEN, 6), closed=False, trim=0)
    sc.k(ch, "trimEnd", [(0, f(0), LIN), (MAT, f(0), HOLD), (INT, f(100), INOUT)])
    vl = sc.text(142, "V", C, X0 + CW - 40, Y0 + 350, "5 130 zł / mies.", 26, DKGREEN, just="right", op=0)
    fade(sc, vl, INT - 200, d_in=200)
    card_in(sc, C, POT - 200, END)
    return sc
ovl("S23")


# ================================================================== S24  then vs now: the race
def S24():
    sc = new("S24_Przewaga", 120.70, 126.45)
    sc.apple_bg()
    w = sc.word
    JA, BOOM, DZIS, PRZ = w(121.12), w(122.88), w(124.14), w(124.66)
    lanes = [("Ja · przed boomem na AI", "wszystko ręcznie", A_GREY, JA, 0.42), ("Ty · dziś, z AI", "AI robi większość", A_BLUE, DZIS, 1.0)]
    for i, (nm, sub, c, t, frac) in enumerate(lanes):
        y = 340 + i * 260
        g = sc.group(100 + i * 8, nm, None, 0, 0, op=0)
        sc.text(101 + i * 8, "N", g, 260, y, nm, 40, A_INK, tracking=-10)
        sc.text(102 + i * 8, "S", g, 260, y + 44, sub, 26, A_GREY, style="Medium")
        sc.rect(103 + i * 8, "Track", g, 260, y + 80, 1400, 24, A_LINE, r=12)
        b = sc.rect(104 + i * 8, "Fill", g, 260, y + 80, 0.01, 24, c, r=12)
        if i == 0:
            sc.k(b, "rectSize", [(0, v2(0.01, 24), LIN), (t, v2(0.01, 24), HOLD), (sc.dur, v2(1400 * frac, 24), LIN)])
        else:
            sc.k(b, "rectSize", [(0, v2(0.01, 24), LIN), (t, v2(0.01, 24), HOLD), (PRZ + 900, v2(1400, 24), INOUT)])
        fade(sc, g, t - 100, d_in=220)
    pg = sc.group(130, "Edge", None, 1500, 760, 1500, 760, op=0)
    pill_text(sc, 131, pg, 1500, 760, "przewaga", 30, A_BG, A_BLUE, style="SemiBold")
    fade(sc, pg, PRZ + 600, d_in=160)
    pop(sc, pg, PRZ + 600, 420, 70)
    return sc


# ================================================================== S25  AI ticks the list by itself (overlay)
def S25():
    sc = new("S25_AI-robi", 126.25, 129.95)
    FX = overlay(sc)
    w = sc.word
    AI_, WYK = w(126.54), w(127.02)
    END = sc.t(129.75)
    X0, Y0, CW = 70, 190, 580
    C = sc.group(110, "Tasks", FX, X0 + CW / 2, 440, X0 + CW / 2, 440, op=0)
    card_bg(sc, 111, C, X0, Y0, CW, 500, r=40, sh=(0.18, 60, 18))
    sc.text(112, "K", C, X0 + 40, Y0 + 66, "Robi AI", 32, A_INK)
    chip = sc.group(113, "AI chip", C, X0 + CW - 90, Y0 + 56, X0 + CW - 90, Y0 + 56)
    pill_text(sc, 114, chip, X0 + CW - 90, Y0 + 56, "auto", 22, A_BLUE, a(A_BLUE, 0.12), style="SemiBold")
    tasks = ["Research rynku", "Struktura produktu", "Teksty na stronę", "Kreacje reklam"]
    for i, tk in enumerate(tasks):
        y = Y0 + 110 + i * 92
        t = WYK + 300 + i * 420
        cb = sc.rect(120 + i * 5, "Box", C, X0 + 40, y + 14, 44, 44, [1, 1, 1, 0], r=22, stroke=(A_LINE, 3))
        sc.k(cb, "fillColor", [(0, col([1, 1, 1, 0]), LIN), (t, col([1, 1, 1, 0]), HOLD), (t + 150, col(A_GREEN), SOFT)])
        sc.k(cb, "strokeColor", [(0, col(A_LINE), LIN), (t, col(A_LINE), HOLD), (t + 150, col(A_GREEN), SOFT)])
        ck = check(sc, 121 + i * 5, C, X0 + 62, y + 37, 18, A_BG, 3.5, op=0)
        fade(sc, ck, t + 80, d_in=100)
        tx = sc.text(122 + i * 5, "T", C, X0 + 108, y + 48, tk, 30, A_INK, style="Medium")
        sc.k(tx, "fillColor", [(0, col(A_INK), LIN), (t, col(A_INK), HOLD), (t + 200, col(A_GREY), SOFT)])
    card_in(sc, C, AI_ - 200, END)
    return sc
ovl("S25")


# ================================================================== S26  stuck: progress halts, the beachball spins, „później”
def S26():
    sc = new("S26_Utkniecie", 130.60, 135.45)
    sc.apple_bg()
    w = sc.word
    SYS, BEZ, UTK, MAL, ODL = w(131.86), w(132.06), w(133.04), w(133.84), w(134.52)
    sc.text(100, "Lab", None, 560, 420, "Twój produkt", 36, A_INK)
    pct = sc.mono(101, "Pct", None, 1360, 420, "0%", 36, A_GREY, just="right")
    sc.k(pct, "textContent", [(0, s("0%"), LIN)] + Scene.roll_keys(100, UTK, lambda v: f"{int(v)}%", 0, 82, ease_pow=1.4)[1:])
    sc.rect(102, "Track", None, 560, 460, 800, 22, A_LINE, r=11)
    bar = sc.rect(103, "Fill", None, 560, 460, 0.01, 22, A_BLUE, r=11)
    sc.k(bar, "rectSize", [(0, v2(0.01, 22), LIN), (100, v2(0.01, 22), HOLD), (UTK, v2(656, 22), OUT)])
    sc.k(bar, "fillColor", [(0, col(A_BLUE), LIN), (UTK, col(A_BLUE), HOLD), (UTK + 400, col(A_GREY), SOFT)])
    # macOS spinning wheel
    BB = sc.group(110, "Beachball", None, 960, 650, 960, 650, op=0)
    cols = [[1.0, 0.25, 0.25, 1], [1.0, 0.6, 0.0, 1], [1.0, 0.85, 0.1, 1], [0.2, 0.8, 0.3, 1], [0.15, 0.55, 1.0, 1], [0.6, 0.3, 0.9, 1]]
    for i, c in enumerate(cols):
        a0 = i * 60
        sc.path(111 + i, "Wedge", BB, [(960, 650)] + arc(960, 650, 60, a0, a0 + 60, 10), fill=c)
    sc.rect(118, "Shine", BB, 930, 605, 50, 26, [1, 1, 1, 0.45], r=13)
    sc.k(BB, "opacity", [(0, f(0), LIN), (UTK, f(0), HOLD), (UTK + 150, f(100), SOFT)])
    sc.k(BB, "rotation", [(0, f(0), LIN), (UTK, f(0), HOLD), (sc.dur, f((sc.dur - UTK) * 0.9), LIN)])
    # reminder: later
    RM = sc.group(120, "Later", None, 960, 860, 960, 860, op=0)
    card_bg(sc, 121, RM, 610, 805, 700, 110, r=30, sh=(0.16, 40, 14))
    sc.rect(122, "Icon", RM, 636, 832, 56, 56, A_ORANGE, r=14)
    sc.text(123, "T", RM, 712, 855, "Dokończę później", 28, A_INK)
    sc.text(124, "S", RM, 712, 890, "przypomnienie przesunięte", 22, A_GREY, style="Medium")
    fade(sc, RM, ODL - 60, d_in=200)
    sc.k(RM, "positionY", [(0, f(940), LIN), (ODL - 60, f(940), HOLD), (ODL + 450, f(860), OUT)])
    return sc


# ================================================================== S27  App Switcher: everything that keeps you moving
def S27():
    sc = new("S27_Wsparcie", 138.30, 145.50)
    sc.apple_bg()
    w = sc.word
    T_ = [w(138.72), w(140.36), w(141.66), w(142.62)]
    CWD, CH, GAP = 520, 700, 600
    STRIP = sc.group(100, "Switcher", None, 0, 0, op=0)
    cards = [("Rozmowa 1:1", "z ekspertem", A_GREEN), ("Live coaching", "co tydzień", A_RED), ("Czas z coachami", "pytasz, dostajesz odpowiedź", A_BLUE),
             ("Społeczność", "ludzie w tym samym procesie", PURPLE)]
    for i, (nm, sub, c) in enumerate(cards):
        cx = 960 + i * GAP
        g = sc.group(110 + i * 20, nm, STRIP, cx, 560, cx, 560)
        cd = sc.rect(111 + i * 20, "Card", g, cx - CWD / 2, 560 - CH / 2, CWD, CH, A_BG, r=46)
        sc.shadow(cd, 0.14, 60, 20)
        sc.rect(112 + i * 20, "App icon", g, cx - CWD / 2 + 20, 560 - CH / 2 - 80, 56, 56, c, r=14)
        sc.text(113 + i * 20, "App", g, cx - CWD / 2 + 90, 560 - CH / 2 - 42, nm, 28, A_INK)
        if i == 0:      # FaceTime tile
            sc.rect(300, "Video", g, cx - 220, 250, 440, 400, [0.12, 0.13, 0.16, 1], r=30)
            sc.rect(301, "Face", g, cx - 70, 340, 140, 140, a(A_GREEN, 0.5), r=70)
            sc.rect(302, "Self", g, cx + 90, 530, 110, 100, [0.3, 0.32, 0.36, 1], r=16)
            sc.rect(303, "End", g, cx - 34, 672, 68, 68, A_RED, r=34)
        elif i == 1:    # calendar week with a recurring event
            for d in range(7):
                sc.text(310 + d, "D", g, cx - 210 + d * 70, 300, "PWŚCPSN"[d], 22, A_GREY, style="Medium", just="center")
            for wk in range(3):
                sc.rect(320 + wk, "Ev", g, cx - 240 + 3 * 70, 340 + wk * 140, 60, 110, A_RED, r=12)
        elif i == 2:    # chat
            sc.rect(330, "Q", g, cx - 30, 300, 240, 70, A_BLUE, r=35)
            sc.rect(331, "A", g, cx - 220, 400, 300, 120, A_FILL, r=35)
            sc.rect(332, "Q2", g, cx - 10, 550, 220, 70, A_BLUE, r=35)
        else:           # community avatars
            for k_ in range(9):
                ax_, ay_ = cx - 160 + (k_ % 3) * 160, 330 + (k_ // 3) * 150
                sc.rect(340 + k_, "Av", g, ax_ - 50, ay_ - 50, 100, 100, a([A_BLUE, A_GREEN, A_ORANGE, PURPLE][k_ % 4], 0.35), r=50)
        sc.text(118 + i * 20, "T", g, cx, 560 + CH / 2 - 120, nm, 44, A_INK, tracking=-15, just="center")
        sc.text(119 + i * 20, "S", g, cx, 560 + CH / 2 - 70, sub, 26, A_GREY, style="Medium", just="center")
        # focus: centred card full, others smaller
        sk_ = [(0, f(100 if i == 0 else 86), LIN)]
        for j, t in enumerate(T_[1:], start=1):
            sk_ += [(t - 300, sk_[-1][1], HOLD), (t + 300, f(100 if i == j else 86), APPLE)]
        scale_keys(sc, g, sk_)
    pk = [(0, f(0), LIN)]
    for j, t in enumerate(T_[1:], start=1):
        pk += [(t - 300, f(-(j - 1) * GAP), HOLD), (t + 300, f(-j * GAP), APPLE)]
    sc.k(STRIP, "positionX", pk)
    fade(sc, STRIP, T_[0] - 300, d_in=250)
    return sc


# ================================================================== S28  problem → shown → direction → solved (overlay)
def S28():
    sc = new("S28_Problem", 145.45, 148.60)
    FX = overlay(sc)
    w = sc.word
    PRB, POK, KIER, RUSZ = w(145.88), w(146.42), w(147.44), w(147.92)
    END = sc.t(148.40)
    X0, Y0, CW = 70, 180, 580
    C = sc.group(110, "Thread", FX, X0 + CW / 2, 430, X0 + CW / 2, 430, op=0)
    card_bg(sc, 111, C, X0, Y0, CW, 500, r=40, sh=(0.18, 60, 18))
    sc.text(112, "K", C, X0 + 40, Y0 + 60, "Coach", 26, A_GREY, style="Medium")

    def bub(base, x, y, w_, h_, colr, txt, fg, t, right):
        g = sc.group(base, txt, C, x + w_ / 2, y + h_ / 2, x + w_ / 2, y + h_ / 2, op=0)
        sc.rect(base + 1, "B", g, x, y, w_, h_, colr, r=28)
        sc.text(base + 2, "T", g, x + 24, y + h_ / 2 + 10, txt, 26, fg, style="Medium")
        fade(sc, g, t - 60, d_in=160)
        pop(sc, g, t - 60, 420, 80)
        return g
    bub(120, X0 + CW - 40 - 380, Y0 + 90, 380, 60, A_BLUE, "Utknąłem na stronie", A_BG, PRB, True)
    sg = sc.group(125, "Screenshot", C, X0 + CW - 130, Y0 + 230, X0 + CW - 130, Y0 + 230, op=0)
    sc.rect(126, "Shot", sg, X0 + CW - 220, Y0 + 165, 180, 130, A_FILL, r=16, stroke=(A_BLUE, 3))
    for i in range(3):
        sc.rect(127 + i, "L", sg, X0 + CW - 200, Y0 + 190 + i * 30, [130, 100, 120][i], 12, A_LINE, r=6)
    fade(sc, sg, POK - 60, d_in=160)
    pop(sc, sg, POK - 60, 420, 80)
    bub(135, X0 + 40, Y0 + 320, 360, 60, A_FILL, "Zrób to tak  →", A_INK, KIER, False)
    sv = sc.group(140, "Solved", C, X0 + CW / 2, Y0 + 440, X0 + CW / 2, Y0 + 440, op=0)
    pill_text(sc, 141, sv, X0 + CW / 2, Y0 + 440, "Rozwiązane", 26, DKGREEN, a(A_GREEN, 0.14), style="SemiBold")
    fade(sc, sv, RUSZ, d_in=160)
    pop(sc, sv, RUSZ, 420, 70)
    card_in(sc, C, PRB - 250, END)
    return sc
ovl("S28")


# ================================================================== S29  ads switch on + Wallet: 800 zł bonus budget
def S29():
    sc = new("S29_800-zl", 148.60, 155.00)
    sc.apple_bg()
    w = sc.word
    GOT, WLA, ODB, BON, P800, KAMP = w(149.42), w(150.16), w(151.30), w(152.04), w(152.80), w(154.12)
    TG = sc.group(100, "Ads toggle", None, 960, 260, 960, 260, op=0)
    card_bg(sc, 101, TG, 620, 200, 680, 120, r=34, sh=(0.12, 40, 14))
    sc.text(102, "T", TG, 670, 272, "Reklamy", 36, A_INK)
    toggle(sc, 103, TG, 1170, 230, WLA)
    fade(sc, TG, GOT - 200, d_in=220)
    pop(sc, TG, GOT - 200, 550, 92)
    # wallet
    WL = sc.group(110, "Wallet", None, 960, 690, 960, 690, op=0)
    sc.rect(111, "Pocket back", WL, 620, 520, 680, 420, [0.12, 0.12, 0.14, 1], r=44)
    CD = sc.group(120, "Card", WL, 960, 690, 960, 690)
    cd = sc.rect(121, "Card", CD, 650, 560, 620, 380, A_BLUE, r=34)
    sc.shadow(cd, 0.3, 40, 14)
    sc.rect(122, "Shade", CD, 650, 560, 620, 190, [1, 1, 1, 0.08], r=34)
    sc.text(123, "K", CD, 690, 624, "Budżet reklamowy", 28, [1, 1, 1, 0.8], style="Medium")
    bal = sc.text(124, "Bal", CD, 690, 760, "0 zł", 110, A_BG, tracking=-40)
    sc.k(bal, "textContent", [(0, s("0 zł"), LIN)] + Scene.roll_keys(P800 - 100, P800 + 700, zl, 0, 800)[1:])
    sc.text(125, "S", CD, 690, 820, "na pierwszą kampanię", 26, [1, 1, 1, 0.75], style="Medium", op=0)
    fade(sc, 125, KAMP - 200, d_in=200)
    bg_ = sc.group(126, "Bonus", CD, 1170, 620, 1170, 620, op=0)
    pill_text(sc, 127, bg_, 1170, 620, "bonus", 24, A_BLUE, A_BG, style="SemiBold")
    fade(sc, bg_, BON - 60, d_in=160)
    pop(sc, bg_, BON - 60, 420, 60)
    sc.k(CD, "positionY", [(0, f(990), LIN), (ODB - 100, f(990), HOLD), (ODB + 650, f(690), APPLE)])
    sc.rect(130, "Pocket front", WL, 620, 860, 680, 80, [0.12, 0.12, 0.14, 1], r=20)
    fade(sc, WL, ODB - 300, d_in=220)
    return sc


# ================================================================== S30  „fajnie, mam e-booka” vs a business you can sell
def S30():
    sc = new("S30_Ebook-vs-biznes", 155.05, 161.65)
    sc.apple_bg()
    w = sc.word
    FAJ, EB, CHC, PROD, OF, STR, MOG = w(156.70), w(157.38), w(157.96), w(159.22), w(159.78), w(160.40), w(160.90)
    EBG = sc.group(100, "Ebook", None, 960, 520, 960, 520, op=0)
    pg = sc.rect(101, "Page", EBG, 880, 400, 160, 210, A_BG, r=14, stroke=(A_LINE, 2))
    sc.shadow(pg, 0.12, 30, 10)
    sc.rect(102, "C", EBG, 920, 430, 80, 80, A_GREY, r=40)
    sc.text(103, "L", EBG, 960, 680, "„fajnie, mam e-booka”", 40, A_GREY, style="Medium", just="center")
    sc.k(EBG, "opacity", [(0, f(0), LIN), (FAJ - 200, f(0), HOLD), (FAJ + 100, f(100), SOFT), (CHC + 200, f(100), HOLD), (CHC + 500, f(0), SOFT)])
    sc.k(EBG, "positionX", [(0, f(960), LIN), (CHC, f(960), HOLD), (CHC + 500, f(760), EIN)])
    BZ = sc.group(110, "Business", None, 960, 540, 960, 540, op=0)
    card_bg(sc, 111, BZ, 560, 180, 800, 720, r=44, sh=(0.14, 70, 22))
    sc.text(112, "H", BZ, 620, 270, "Twój biznes", 48, A_INK, tracking=-20)
    rows = [("Produkt", PROD), ("Oferta", OF), ("Strona", STR)]
    for i, (nm, t) in enumerate(rows):
        y = 330 + i * 110
        g = sc.group(120 + i * 6, nm, BZ, 0, 0, op=0)
        sc.rect(121 + i * 6, "Row", g, 600, y, 720, 90, A_FILL, r=24)
        sc.text(122 + i * 6, "N", g, 700, y + 58, nm, 34, A_INK, style="Medium")
        ok_badge(sc, 123 + i * 6, g, 650, y + 45, t + 50, d=46)
        fade(sc, g, t - 60, d_in=160)
        sc.k(g, "positionX", [(0, f(24), LIN), (t - 60, f(24), HOLD), (t + 400, f(0), OUT)])
    BT = sc.group(140, "Sell", BZ, 960, 740, 960, 740, op=0)
    sc.rect(141, "Btn", BT, 600, 700, 720, 90, A_GREEN, r=45)
    sc.text(142, "T", BT, 960, 758, "Zacznij sprzedawać", 36, A_BG, just="center")
    fade(sc, BT, MOG - 60, d_in=180)
    scale_keys(sc, BT, [(0, f(90), LIN), (MOG - 60, f(90), HOLD), (MOG + 400, f(100), APPLE), (MOG + 900, f(100), HOLD),
                        (MOG + 980, f(96), OUT), (MOG + 1200, f(100), APPLE)])
    sc.k(BZ, "opacity", [(0, f(0), LIN), (CHC + 200, f(0), HOLD), (CHC + 500, f(100), SOFT)])
    scale_keys(sc, BZ, [(0, f(95), LIN), (CHC + 200, f(95), HOLD), (CHC + 900, f(100), OUT)])
    return sc


# ================================================================== S31  the guarantee seal: launch in 48 h or 100% back
def S31():
    sc = new("S31_Gwarancja", 163.85, 173.30)
    sc.apple_bg()
    w = sc.word
    GW, H48, PRZ, PO48, PRD, STR, MAT, ODD, P100 = (w(164.08), w(164.86), w(165.90), w(167.44), w(169.32), w(169.90),
                                                    w(170.26), w(171.80), w(172.24))
    SL = sc.group(100, "Seal", None, 560, 470, 560, 470, op=0)
    pts = []
    for i in range(48):
        r_ = 210 if i % 2 == 0 else 192
        ang = math.radians(i * 7.5)
        pts.append((560 + r_ * math.cos(ang), 470 + r_ * math.sin(ang)))
    sc.path(101, "Scallop", SL, pts, fill=A_BLUE)
    sc.ring(102, "Inner", SL, 560, 470, 320, [1, 1, 1, 0.5], 3)
    sc.text(103, "48", SL, 560, 500, "48 h", 110, A_BG, tracking=-40, just="center")
    sc.text(104, "K", SL, 560, 560, "GWARANCJA", 22, [1, 1, 1, 0.85], style="Medium", family="Geist Mono", just="center")
    sc.k(SL, "opacity", [(0, f(0), LIN), (GW - 100, f(0), HOLD), (GW + 80, f(100), SOFT)])
    scale_keys(sc, SL, [(0, f(160), LIN), (GW - 100, f(160), HOLD), (GW + 300, f(100), EIN), (GW + 450, f(104), OUT), (GW + 700, f(100), APPLE)])
    sc.k(SL, "rotation", [(0, f(-25), LIN), (GW - 100, f(-25), HOLD), (GW + 700, f(0), APPLE), (sc.dur, f(6), LIN)])
    tl = sc.text(110, "Title", None, 900, 330, "Launch w 48 godzin", 68, A_INK, tracking=-30, op=0)
    fade(sc, tl, H48 - 100, d_in=240)
    sub = sc.text(111, "Sub", None, 900, 390, "przejdź cały proces", 32, A_GREY, style="Medium", op=0)
    fade(sc, sub, PRZ - 100, d_in=200)
    cond = sc.text(112, "If", None, 900, 500, "Jeśli po 48 h nie masz:", 30, A_GREY, style="Medium", op=0)
    fade(sc, cond, PO48, d_in=200)
    for i, (nm, t) in enumerate([("Produktu", PRD), ("Strony", STR), ("Materiałów do sprzedaży", MAT)]):
        y = 560 + i * 80
        g = sc.group(120 + i * 4, nm, None, 0, 0, op=0)
        sc.rect(121 + i * 4, "Box", g, 900, y, 44, 44, [1, 1, 1, 0], r=22, stroke=(A_LINE, 3))
        sc.text(122 + i * 4, "N", g, 966, y + 33, nm, 34, A_INK, style="Medium")
        fade(sc, g, t - 60, d_in=160)
        sc.k(g, "positionX", [(0, f(20), LIN), (t - 60, f(20), HOLD), (t + 400, f(0), OUT)])
    rf = sc.group(140, "Refund", None, 1180, 870, 1180, 870, op=0)
    rb = sc.rect(141, "Bg", rf, 900, 830, 560, 84, a(A_GREEN, 0.14), r=42)
    check(sc, 142, rf, 950, 872, 22, A_GREEN, 5)
    sc.text(143, "T", rf, 990, 884, "100% zwrotu kwoty", 36, DKGREEN)
    fade(sc, rf, P100 - 100, d_in=180)
    pop(sc, rf, P100 - 100, 500, 85)
    return sc


# ================================================================== S32  two futures: saved stuff vs a business (page swipe)
def S32():
    sc = new("S32_Dwie-przyszlosci", 173.30, 180.90)
    sc.apple_bg()
    w = sc.word
    P48, FIL, PROM, POM, ALBO, PROD, STR, OF, SPR = (w(173.50), w(175.68), w(176.16), w(176.60), w(177.10), w(177.72),
                                                    w(178.12), w(178.58), w(180.32))
    PAGES = sc.group(100, "Pages", None, 0, 0)
    # page 1: saved for later (grey, endless)
    sc.text(101, "K1", PAGES, 960, 190, "Za 48 godzin możesz mieć…", 40, A_GREY, style="Medium", just="center")
    x0 = 610
    card_bg(sc, 102, PAGES, x0, 250, 700, 700, r=44, sh=(0.10, 60, 18))
    sc.text(103, "H1", PAGES, x0 + 50, 330, "Zapisane na później", 40, A_GREY, tracking=-15)
    items = [("Kolejne filmy", FIL), ("Prompty", PROM), ("Pomysły", POM), ("Kolejne filmy", POM + 150), ("Prompty", POM + 250)]
    for i, (nm, t) in enumerate(items):
        y = 380 + i * 105
        g = sc.group(110 + i * 4, nm, PAGES, 0, 0, op=0)
        sc.rect(111 + i * 4, "Row", g, x0 + 40, y, 620, 85, A_FILL, r=22)
        sc.rect(112 + i * 4, "Ic", g, x0 + 64, y + 20, 45, 45, a(A_GREY, 0.4), r=10)
        sc.text(113 + i * 4, "T", g, x0 + 130, y + 54, nm, 30, A_GREY, style="Medium")
        fade(sc, g, t - 60, d_in=160)
    # page 2: a business (blue, sharp)
    X2 = 1920 + 610
    sc.text(140, "K2", PAGES, 1920 + 960, 190, "…albo", 40, A_BLUE, just="center")
    card_bg(sc, 141, PAGES, X2, 250, 700, 700, r=44, sh=(0.14, 60, 18))
    sc.text(142, "H2", PAGES, X2 + 50, 330, "Własny biznes", 44, A_INK, tracking=-15)
    for i, (nm, t, c) in enumerate([("Produkt", PROD, A_BLUE), ("Strona", STR, A_GREEN), ("Oferta", OF, A_ORANGE)]):
        y = 380 + i * 105
        g = sc.group(150 + i * 5, nm, PAGES, 0, 0, op=0)
        sc.rect(151 + i * 5, "Row", g, X2 + 40, y, 620, 85, a(c, 0.08), r=22)
        sc.rect(152 + i * 5, "Ic", g, X2 + 64, y + 20, 45, 45, c, r=10)
        sc.text(153 + i * 5, "T", g, X2 + 130, y + 54, nm, 30, A_INK)
        ok_badge(sc, 170 + i * 4, g, X2 + 620, y + 42, t + 150, d=40)
        fade(sc, g, t - 60, d_in=160)
    sale = sc.group(190, "Sale", PAGES, X2 + 350, 820, X2 + 350, 820, op=0)
    sc.rect(191, "Bg", sale, X2 + 40, 785, 620, 80, A_GREEN, r=40)
    sc.text(192, "T", sale, X2 + 350, 836, "Nowa sprzedaż  +57 zł", 30, A_BG, just="center")
    fade(sc, sale, SPR - 100, d_in=180)
    pop(sc, sale, SPR - 100, 500, 85)
    sc.k(PAGES, "positionX", [(0, f(0), LIN), (ALBO - 100, f(0), HOLD), (ALBO + 600, f(-1920), APPLE)])
    # page dots
    for i in range(2):
        d = sc.rect(195 + i, "Dot", None, 945 + i * 22, 1000, 12, 12, A_GREY, r=6)
        on, off = (A_INK, A_LINE)
        c0, c1 = (on, off) if i == 0 else (off, on)
        sc.k(d, "fillColor", [(0, col(c0), LIN), (ALBO + 200, col(c0), HOLD), (ALBO + 400, col(c1), SOFT)])
    return sc


# ================================================================== S33  CTA: the button under the video (overlay)
def S33():
    sc = new("S33_CTA", 180.60, 183.85)
    FX = overlay(sc)
    w = sc.word
    KLIK, DOL = w(181.08), w(182.42)
    END = sc.t(183.65)
    BT = sc.group(110, "CTA", FX, 960, 930, 960, 930, op=0)
    b = sc.rect(111, "Btn", BT, 560, 880, 800, 100, A_BLUE, r=50)
    sc.shadow(b, 0.3, 40, 14)
    sc.text(112, "T", BT, 920, 944, "Dołącz do Cyfrowego Autopilota", 34, A_BG, just="center")
    sc.path(113, "Arrow", BT, [(1290, 912), (1290, 948)], stroke=(A_BG, 5), closed=False)
    sc.path(114, "Head", BT, [(1276, 936), (1290, 950), (1304, 936)], stroke=(A_BG, 5), closed=False)
    sc.k(BT, "opacity", [(0, f(0), LIN), (KLIK - 300, f(0), HOLD), (KLIK - 60, f(100), SOFT), (END, f(100), HOLD), (END + 250, f(0), SOFT)])
    scale_keys(sc, BT, [(0, f(80), LIN), (KLIK - 300, f(80), HOLD), (KLIK + 200, f(100), APPLE), (KLIK + 600, f(100), HOLD),
                        (KLIK + 680, f(95), OUT), (KLIK + 900, f(100), APPLE), (DOL, f(100), HOLD), (DOL + 150, f(104), OUT), (DOL + 450, f(100), APPLE)])
    sc.k(113, "positionY", [(0, f(0), LIN)] + sum([[(KLIK + 400 + k_ * 500, f(0), HOLD), (KLIK + 650 + k_ * 500, f(8), INOUT)] for k_ in range(3)], []))
    CU = cursor(sc, 120, FX, 1500, 1060)
    sc.k(CU, "opacity", [(0, f(0), LIN), (KLIK, f(0), HOLD), (KLIK + 150, f(100), SOFT), (END, f(100), HOLD), (END + 200, f(0), SOFT)])
    sc.kpos(CU, [(0, 1500, 1060, LIN), (KLIK, 1500, 1060, HOLD), (KLIK + 600, 1180, 940, APPLE)])
    scale_keys(sc, CU, [(0, f(100), LIN), (KLIK + 620, f(100), HOLD), (KLIK + 680, f(84), OUT), (KLIK + 900, f(100), APPLE)])
    return sc
ovl("S33")


# ================================================================== S34  finale: AI alone changes nothing — you + AI builds something yours
def S34():
    sc = new("S34_Final", 183.84, 188.75)
    sc.apple_bg()
    w = sc.word
    AI_, NIC, ZM2, UZY, SWO = w(183.94), w(184.88), w(185.96), w(187.26), w(188.40)
    ai = sc.group(100, "AI", None, 960, 500, 960, 500, op=0)
    sc.text(101, "AI", ai, 960, 560, "AI", 220, A_GREY, tracking=-60, just="center")
    fade(sc, ai, AI_ - 60, d_in=200)
    sub = sc.text(102, "Sub", None, 960, 700, "samo w sobie niczego nie zmieni", 44, A_GREY, style="Medium", just="center", op=0)
    sc.k(sub, "opacity", [(0, f(0), LIN), (NIC - 300, f(0), HOLD), (NIC, f(100), SOFT), (ZM2, f(100), HOLD), (ZM2 + 250, f(0), SOFT)])
    sc.k(ai, "positionX", [(0, f(960), LIN), (ZM2 - 100, f(960), HOLD), (ZM2 + 500, f(400), APPLE)])
    scale_keys(sc, ai, [(0, f(85), LIN), (AI_ - 60, f(85), HOLD), (AI_ + 490, f(100), APPLE), (ZM2 - 100, f(100), HOLD), (ZM2 + 500, f(55), APPLE)])
    pl = sc.text(103, "Plus", None, 640, 540, "+  Ty", 96, A_INK, tracking=-30, just="center", op=0)
    fade(sc, pl, ZM2 + 300, d_in=220)
    eq = sc.text(104, "Eq", None, 900, 540, "=", 96, A_GREY, just="center", op=0)
    fade(sc, eq, UZY, d_in=200)
    res = sc.text(105, "Res", None, 980, 540, "coś swojego.", 110, A_BLUE, tracking=-40, op=0,
                  animators=[Scene.reveal_animator(1, 11, dy=24, blur_=16)])
    ZB = w(187.94)
    sc.reveal_words(res, 11, [ZB, SWO - 150], step=200)
    sc.k(res, "opacity", [(0, f(0), LIN), (ZB - 100, f(0), HOLD), (ZB, f(100), HOLD)])
    return sc


BUILD = {k: v for k, v in globals().items() if k.startswith("S") and k[1:].isdigit() and callable(v)}

if __name__ == "__main__":
    for key in (sys.argv[1:] or sorted(BUILD)):
        try:
            BUILD[key]().build()
        except SystemExit as e:
            print(f"[{key}] FAILED: {e}", flush=True)
        except Exception as e:
            print(f"[{key}] ERROR: {type(e).__name__}: {e}", flush=True)
