#!/bin/zsh
# chk.sh KEY... — draft render; B → 5 frames, K → 3 frames over the real CUT frames. Sheet → out/KEY_sheet.png
cd "${0:A:h}"; T=out/tmp; mkdir -p $T
for k in "$@"; do
  read a b m <<< "$(python3 -c "import json;v=json.load(open('scenes.json'))['$k'];print(v[0],v[1],v[2])")"
  fmt=mp4; [[ $m == K ]] && fmt=mov
  npx hyperframes render -c $k.html --quality draft --format $fmt --output out/${k}_draft.$fmt --quiet >/dev/null 2>&1 || { echo "FAIL $k"; continue; }
  d=$(python3 -c "print($b-$a)"); args=(); i=0
  for p in 0.1 0.3 0.5 0.7 0.92; do
    t=$(python3 -c "print(round($d*$p,2))")
    ffmpeg -v error -y -ss $t -i out/${k}_draft.$fmt -frames:v 1 $T/r$i.png
    if [[ $m == K ]]; then
      ffmpeg -v error -y -ss $(python3 -c "print($a+$t)") -i ../CUT.mp4 -i $T/r$i.png -filter_complex "[0:v][1:v]overlay,scale=480:-1" -frames:v 1 $T/c$i.png
    else
      ffmpeg -v error -y -i $T/r$i.png -vf scale=480:-1 $T/c$i.png
    fi
    args+=(-i $T/c$i.png); i=$((i+1))
  done
  ffmpeg -v error -y $args -filter_complex "hstack=5" out/${k}_sheet.png && echo "ok $k $m"
done
