#!/usr/bin/env python3
"""lfpdo v4 detail pass — short phrases written straight on Konrad's wall (left of his head, dark ink, Inter weight
contrast) in the clean-face gaps of the full-camera stretches (premium/gaps.txt). Transparent MOV each.
Line = (text, classes, t) with t relative to the callout in-point (word timestamps from tr/words.json)."""
import json, os
from page import page, HERE

C = {
    "C01": (134.95, 137.55, [("Rodzice", "a", 0.05), ("ósmoklasistów", "b s", 1.3)]),
    "C02": (152.15, 155.9, [("Nie twórz potrzeby", "a", 0.05), ("sztucznie.", "b ng", 1.2)]),
    "C03": (158.7, 161.55, [("Pieniądze już", "a", 0.1), ("lecą.", "b mk", 1.35)]),
    "C04": (242.2, 247.0, [("Problem klienta", "a", 0.1), ("=", "b ac", 3.3), ("Twój produkt.", "b s", 3.95)]),
    "C05": (352.1, 354.85, [("Pytanie:", "a", 0.1), ("po co płacić?", "b s mk", 1.7)]),
    "C06": (403.2, 406.25, [("Nie płacą za wiedzę.", "a", 0.1), ("Płacą, żeby", "b s", 1.4), ("nie myśleć.", "b s ac", 1.9)]),
    "C07": (450.85, 454.0, [("Ludzie zawsze", "a", 0.05), ("porównują.", "b s", 0.5), ("Efekt zakotwiczenia", "a ac", 1.75)]),
    "C08": (462.65, 466.45, [("Ta sama cena,", "a", 0.1), ("inna", "b", 2.45), ("kotwica.", "b mk", 2.7)]),
    "C09": (499.1, 501.95, [("Pierwsze", "a", 0.1), ("10 minut:", "b s", 0.6), ("nic.", "b ng", 2.45)]),
    "C10": (529.55, 534.75, [("Zrozum te", "a", 0.1), ("4 rzeczy", "b mk", 0.95), ("i wiesz więcej niż większość.", "a", 2.4)]),
    "C11": (573.55, 577.85, [("Bajka?", "a st1", 0.4), ("Matematyka.", "b s ac", 3.35)]),
    "C12": (738.55, 741.35, [("Wszystko gotowe.", "a", 0.8), ("Nie musisz", "b s", 1.7), ("myśleć.", "b s mk", 2.3)]),
    "C13": (745.45, 748.0, [("Darmowy kurs =", "a", 0.05), ("no-brainer.", "b s ac", 1.3)]),
    "C14": (751.6, 754.6, [("Przestań robić produkty", "a", 0.1), ("dla nikogo.", "b s", 1.3)]),
}

BUTT = {"C05", "C07", "C09"}
for k, (a, b, lines) in C.items():
    dur = round(b - a, 3)
    body = '      <div class="co">' + "".join(
        f'<div><span class="{cls.replace("st1", "").replace("mk", "").strip()}{" mk" if "mk" in cls else ""}" id="l{i}">{tx}</span></div>'
        for i, (tx, cls, _) in enumerate(lines)) + "</div>"
    js = []
    for i, (tx, cls, t) in enumerate(lines):
        js.append(f'K.rise("#l{i}", {t}, {{ dur: 0.6, stagger: 0.05 }});')
        if "mk" in cls:
            js.append(f'K.mark("#l{i}", {t + 0.35});')
        if "st1" in cls:
            js.append(f'K.strike("#l{i}", {t + 0.75}, {{ dim: false }});')
    js.append(f'tl.to(".co", {{ y: -14, duration: {dur - 0.3}, ease: "none" }}, 0);')
    if k not in BUTT:     # callouts that butt straight into a full-screen scene are cut by its whip instead
        js.append(f'tl.to(".co", {{ opacity: 0, y: -40, duration: 0.28, ease: "power2.in" }}, {dur - 0.3});')
    page(k, dur, body, "      " + "\n      ".join(js), overlay=True)
json.dump({k: [a, b] for k, (a, b, _) in C.items()}, open(os.path.join(HERE, "callouts.json"), "w"), indent=1)
print(len(C), "callouts")
