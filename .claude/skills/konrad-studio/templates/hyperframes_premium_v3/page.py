"""Write one HyperFrames scene page (Premium v3) from css/body/js parts. Used by build_*.py."""
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def page(key, dur, body, js, css="", overlay=False):
    cls = ' class="ov"' if overlay else ""
    deco = "" if overlay else '\n      <div class="vign"></div>\n      <div class="grain"></div>'
    html = f"""<!doctype html>
<html lang="pl"{cls}>
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <link rel="stylesheet" href="base.css" />
    <style>{css}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{dur}" data-width="1920" data-height="1080">
{body}{deco}
    </div>
    <script src="kit.js"></script>
    <script>
      const tl = K.tl;
{js}
      K.done();
    </script>
  </body>
</html>
"""
    open(os.path.join(HERE, f"{key}.html"), "w").write(html)
