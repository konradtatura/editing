#!/usr/bin/env python3
"""Style 7 ("8 rzeczy" numbered list) spec.  usage: build_spec7.py OUT.json
Video already cut and letterboxed by Konrad (band y 656-1263, picture x 0-871); list sits on the right of the band."""
import json, sys
TITLE = "8 rzeczy, które zachowaj dla SIEBIE"
# (text from Konrad, start of the sentence in 8thingsprivate.mp4)
ITEMS = [("ile zarabiasz", 0.0), ("swoje plany", 1.16), ("problemy rodzinne", 2.54), ("problem w związku", 4.44),
         ("swoje słabości", 6.40), ("problemy finansowe", 8.02), ("trzymaj sekrety", 11.32), ("głupie błędy", 13.48)]
# original 720x1280 x1.5: title ~54 px above the band, numbers ~48 px, items ~39 px; pitch squeezed to fit Konrad's lower band
layout = dict(titleX=52, titleY=566, titleFs=54, listX=600, listY=676, pitch=72, numFs=46, fs=38)
json.dump(dict(dur=17.133, fps=30, title=TITLE, layout=layout, items=[dict(text=t[0].upper() + t[1:], t=s) for t, s in ITEMS]),
          open(sys.argv[1], "w"), ensure_ascii=False, indent=1)
