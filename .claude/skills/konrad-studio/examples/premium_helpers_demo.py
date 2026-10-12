"""Demo of the 2026-10-03 premium helpers: image() icon on a lowered card, curve() connectors to pills, highlight(),
Studio Serif accent word, flap_keys() counter, type_keys() typing, push_in() + motion_blur() camera. Needs notion.png
(fetch_icon.py app "Notion" notion.png), tr/words.json and v6.mp4 in the project folder (any clip + its transcript)."""
import sys, os
sys.path.insert(0, os.path.expanduser("~/.claude/skills/konrad-studio/scripts"))
import apple
HERE = os.path.dirname(os.path.abspath(__file__)); apple.init(HERE, 1920, 1080)
from apple import *
def D():
    sc = Scene("P01_Premium", 0.0, 5.0, os.path.join(HERE, "tr", "words.json"), os.path.join(HERE, "v6.mp4"))
    sc.apple_bg()
    CAM = sc.group(100, "Camera", None, 960, 540, 960, 540)
    sc.lower(CAM)
    push_in(sc, CAM, 0, 5000, 100, 105)
    sc.image(50, "Notion", os.path.join(HERE, "notion.png"), 300, 420, 200, r=46)
    fade(sc, 50, 100)
    # tile card for icon
    t = sc.rect(101, "Tile", CAM, 280, 400, 240, 240, A_BG, r=56); sc.shadow(t, 0.14, 50, 16)
    labels = ["Produkt", "Zasięg", "Ludzie"]
    for i, lb in enumerate(labels):
        y = 330 + i * 140
        curve(sc, 110 + i, CAM, (520, 520), (980, y + 30), 600 + i * 450, color=A_LINE, width=4)
        g = sc.group(120 + i * 3, lb, CAM, 1000, y, 1000, y + 30, op=0)
        sc.rect(121 + i * 3, "Pill", g, 1000, y, 280, 60, A_INK, r=30)
        sc.text(122 + i * 3, "T", g, 1140, y + 40, lb, 30, A_BG, style="Medium", just="center")
        fade(sc, g, 900 + i * 450, d_in=200); pop(sc, g, 900 + i * 450, 420, 85)
    hl = highlight(sc, 140, CAM, 560, 860, 520, 64, 2600)
    sc.text(141, "Quote", CAM, 570, 905, "raz zrobione, sto razy sprzedane", 40, A_INK, style="Medium")
    ser = sc.text(142, "Serif", CAM, 1450, 160, "dźwignia", 90, A_BLUE, style="Regular", family="Studio Serif", just="center", op=0)
    fade(sc, ser, 300)
    num = sc.mono(143, "Flap", CAM, 1450, 300, "130 000", 70, A_INK, just="center")
    sc.k(num, "textContent", flap_keys(800, 2200, "130 000"))
    ty = sc.text(144, "Typed", CAM, 300, 760, "", 36, A_GREY, style="Medium")
    sc.k(ty, "textContent", type_keys(1500, "jak zarabiać, kiedy śpisz?"))
    sc.motion_blur(CAM)
    return sc
D().build()
