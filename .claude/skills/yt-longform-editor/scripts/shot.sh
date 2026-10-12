#!/bin/bash
# Screenshot a website for browser-frame scenes (T5 browser / T6).
# usage: shot.sh <url> <out.png> [height=900 (one screen; taller only for pages without 100vh heroes)] [width=1440]
# Uses the headless Chrome that HyperFrames already installed.
set -e
URL="$1"; OUT="$2"; HGT="${3:-900}"; WID="${4:-1440}"
CHROME=$(ls -d "$HOME"/.cache/hyperframes/chrome/chrome-headless-shell/*/chrome-headless-shell-*/chrome-headless-shell 2>/dev/null | tail -1)
if [ -z "$CHROME" ]; then echo "headless chrome not found (run: npx hyperframes doctor)" >&2; exit 1; fi
"$CHROME" --headless --disable-gpu --hide-scrollbars --force-device-scale-factor=1 \
  --window-size="$WID,$HGT" --virtual-time-budget=12000 --screenshot="$OUT" "$URL" >/dev/null 2>&1
ls -la "$OUT"
