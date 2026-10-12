#!/bin/zsh
# cochk.sh KEY — draft MOV of a wall callout composited over the real lfpdo frames at that time → out/KEY_sheet.png
cd "${0:A:h}"; k=$1; T=out/tmp; mkdir -p $T
cp $k.html index.html
npx hyperframes render -c $k.html --quality draft --format mov --output out/${k}_draft.mov --quiet >/dev/null 2>&1 || { echo FAIL $k; exit 1; }
a=$(python3 -c "import json;print(json.load(open('callouts.json'))['$k'][0])")
d=$(ffprobe -v error -show_entries format=duration -of csv=p=0 out/${k}_draft.mov)
args=(); i=0
for p in 0.3 0.6 0.88; do
  t=$(python3 -c "print(round($d*$p,2))"); ta=$(python3 -c "print($a+$d*$p)")
  ffmpeg -v error -y -ss $t -i out/${k}_draft.mov -frames:v 1 $T/o$i.png
  ffmpeg -v error -y -ss $ta -i ../../../lfpdo.mp4 -i $T/o$i.png -filter_complex "[0:v][1:v]overlay,scale=640:-1" -frames:v 1 $T/c$i.png
  args+=(-i $T/c$i.png); i=$((i+1))
done
ffmpeg -v error -y $args -filter_complex "hstack=3" out/${k}_sheet.png && echo "ok $k"
