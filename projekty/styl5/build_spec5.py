#!/usr/bin/env python3
"""Style 5 ("Nie mów / Mów" reveal) spec.  usage: build_spec5.py OUT.json [tight]   (tight = jeslito2, closer framing: table right under the chin)
Each bar slides out LEAD s before the first word of its row is said (measured on the original: 0.1-0.2 s)."""
import json, sys
LEAD = 0.12
RED, GREEN = "#FC0000", "#00E000"
# (text on screen, time of the first spoken word of that phrase)  -- ad "jeslito" (16.1 s)
LEFT = [("więcej wolności", 0.66), ("zarabiać więcej", 2.84), ("osiągnąć sukces", 5.48), ("zbudować majątek", 8.40), ("rozwijać się", 11.16)]
RIGHT = [("zarabiać pieniądze", 1.62), ("rozwiązywać problemy", 4.20), ("podejmować ryzyko", 6.44), ("cierpliwość", 9.58), ("wyjść ze strefy komfortu", 11.96)]
# 1080x1920. Original (720x1280): columns 333 px wide, bars 60 px high every 70 px, header 78 px; table lower here so it stays under the mouth.
layout = dict(colX=[70, 560], colW=450, hdY=1180, barY=1245, barH=60, pitch=70, fs=40, exitDur=0.71)
if len(sys.argv) > 2 and sys.argv[2] == "tight": layout.update(hdY=1030, barY=1095)
spec = dict(dur=16.133, fps=30, layout=layout, cols=[
    dict(head="Jeśli chcesz", color=RED, rows=[dict(text=t, t=round(s - LEAD, 3)) for t, s in LEFT]),
    dict(head="Musisz", color=GREEN, rows=[dict(text=t, t=round(s - LEAD, 3)) for t, s in RIGHT])])
json.dump(spec, open(sys.argv[1], "w"), ensure_ascii=False, indent=1)
