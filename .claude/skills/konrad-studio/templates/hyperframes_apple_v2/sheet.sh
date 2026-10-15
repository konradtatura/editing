#!/bin/zsh
# sheet.sh SCENE [mov] — 6-frame contact sheet of out/SCENE_draft.* (mov shown over a wall-grey)
cd "${0:A:h}"; s=$1; fmt=${2:-mp4}; T=out/tmp; mkdir -p $T
d=$(ffprobe -v error -show_entries format=duration -of csv=p=0 out/${s}_draft.$fmt)
args=(); i=0
for p in 0.06 0.22 0.4 0.58 0.76 0.9; do
  t=$(python3 -c "print(round($d*$p,2))")
  ffmpeg -v error -y -ss $t -i out/${s}_draft.$fmt -frames:v 1 $T/r$i.png
  if [[ $fmt == mov ]]; then
    ffmpeg -v error -y -f lavfi -i color=c=0xc9c2b8:s=1920x1080 -i $T/r$i.png -filter_complex "[0][1]overlay,crop=960:1080:0:0,scale=320:-1" -frames:v 1 $T/c$i.png
  else
    ffmpeg -v error -y -i $T/r$i.png -vf scale=640:-1 $T/c$i.png
  fi
  args+=(-i $T/c$i.png); i=$((i+1))
done
ffmpeg -v error -y $args -filter_complex "[0][1][2][3][4][5]hstack=6" out/${s}_sheet.png && echo "sheet ok $s $d"
