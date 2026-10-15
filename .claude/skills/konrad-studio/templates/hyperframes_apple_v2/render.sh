#!/bin/zsh
# render.sh KEY... — high quality: K → ProRes 4444 MOV (alpha), B → MP4
cd "${0:A:h}"
for k in "$@"; do
  m=$(python3 -c "import json;print(json.load(open('scenes.json'))['$k'][2])")
  fmt=mp4; [[ $m == K ]] && fmt=mov
  npx hyperframes render -c $k.html --quality high --format $fmt --output out/$k.$fmt --quiet >/dev/null 2>&1 && echo "$k ok" || echo "$k FAIL"
done
echo DONE
