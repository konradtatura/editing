#!/bin/bash
# style-2 full render: run2.sh WORKDIR STOCKDIR [names...]
set -e
D=$1; S=$2; shift 2; H=$(cd "$(dirname "$0")" && pwd)
python3 $H/build_spec2.py $D $S > /dev/null
for n in ${@:-ads7 ads10}; do
  rm -rf $D/f2_$n
  node $H/../reklamy_CA/engine/render.mjs $D/spec2_$n.json $D/f2_$n --page $H/engine/overlay2.html --par 3
  python3 $H/engine/compose2.py $D/spec2_$n.json $D/f2_$n $D/${n}_STYL2.mp4
  ffmpeg -v error -y -i $D/${n}_STYL2.mp4 -vf scale=540:-2 -c:v libx264 -crf 28 -preset fast -c:a aac -b:a 96k -movflags +faststart $D/${n}_STYL2_tel.mp4
  echo "DONE $n"
done
