#!/bin/bash
# full render: overlays -> compose. usage: run_all.sh WORKDIR [ads...]
set -e
D=$1; shift; H=$(cd "$(dirname "$0")" && pwd)
python3 $H/build_spec.py $D > /dev/null
for n in ${@:-8 9}; do
  rm -rf $D/frames$n
  node $H/engine/render.mjs $D/spec_ad$n.json $D/frames$n --par 3
  python3 $H/engine/compose.py $D/spec_ad$n.json $D/frames$n $D/AD${n}_EDIT.mp4
  ffmpeg -v error -y -i $D/AD${n}_EDIT.mp4 -vf scale=540:-2 -c:v libx264 -crf 28 -preset fast -c:a aac -b:a 96k -movflags +faststart $D/AD${n}_EDIT_tel.mp4
  echo "DONE ad$n"
done
