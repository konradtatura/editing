#!/bin/bash
# Synthesises the default SFX kit into assets/sfx (no downloads). Subtle UI register, <= 1 s each.
# Replace any file with a better sample of the same name (e.g. from Artlist / Epidemic) and assemble.py picks it up.
set -e
D="$(cd "$(dirname "$0")/.." && pwd)/assets/sfx"
mkdir -p "$D"
F="ffmpeg -v error -y"
# soft whoosh: brown noise, band-limited, fast attack / smooth decay (cards and words entering)
$F -f lavfi -i "anoisesrc=d=0.5:c=brown:a=0.9" -af "highpass=f=180,lowpass=f=2600,afade=t=in:st=0:d=0.12,afade=t=out:st=0.14:d=0.34,volume=0.9" -ar 48000 "$D/whoosh.wav"
# airy swish for big moves (speaker shrink / grow, page zoom)
$F -f lavfi -i "anoisesrc=d=0.75:c=pink:a=0.8" -af "highpass=f=400,lowpass=f=6000,afade=t=in:st=0:d=0.32,afade=t=out:st=0.34:d=0.40,volume=0.7" -ar 48000 "$D/swish.wav"
# pop: two-tone sine, 100 ms (list items, icons, badges)
$F -f lavfi -i "sine=f=720:d=0.10" -f lavfi -i "sine=f=1440:d=0.08" -filter_complex "[0:a]volume=0.55,afade=t=in:st=0:d=0.002,afade=t=out:st=0.018:d=0.080[a];[1:a]volume=0.30,afade=t=in:st=0:d=0.001,afade=t=out:st=0.012:d=0.060[b];[a][b]amix=inputs=2:duration=first,highpass=f=300,lowpass=f=4000,volume=0.9" -ar 48000 "$D/pop.wav"
# tick: light high tick (numbers rolling, small accents)
$F -f lavfi -i "sine=f=2200:d=0.05" -af "afade=t=in:st=0:d=0.001,afade=t=out:st=0.006:d=0.04,highpass=f=900,volume=0.45" -ar 48000 "$D/tick.wav"
# click: UI click (cursor click, button press)
$F -f lavfi -i "anoisesrc=d=0.06:c=white:a=0.6" -f lavfi -i "sine=f=1500:d=0.05" -filter_complex "[0:a]highpass=f=2000,afade=t=out:st=0.005:d=0.04[n];[1:a]volume=0.4,afade=t=out:st=0.01:d=0.04[t];[n][t]amix=inputs=2:duration=longest,volume=0.9" -ar 48000 "$D/click.wav"
# hit: deep sub for chapter cards and big numbers
$F -f lavfi -i "sine=f=52:d=0.9" -f lavfi -i "sine=f=104:d=0.6" -filter_complex "[0:a]afade=t=in:st=0:d=0.004,afade=t=out:st=0.05:d=0.85,volume=0.9[a];[1:a]afade=t=in:st=0:d=0.004,afade=t=out:st=0.03:d=0.5,volume=0.35[b];[a][b]amix=inputs=2:duration=longest,volume=1.1" -ar 48000 "$D/hit.wav"
# riser: 1.2 s swell into a reveal
$F -f lavfi -i "anoisesrc=d=1.2:c=pink:a=0.7" -af "highpass=f=300,lowpass=f=5000,afade=t=in:st=0:d=1.05,afade=t=out:st=1.08:d=0.12,volume=0.6" -ar 48000 "$D/riser.wav"
ls "$D"
