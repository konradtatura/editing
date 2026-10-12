#!/bin/zsh
# hi.sh SCENE [mov] — final render → out/SCENE.mp4|mov
cd "${0:A:h}"; s=$1; fmt=${2:-mp4}
npx hyperframes render -c $s.html --quality high --format $fmt --output out/$s.$fmt --quiet >/dev/null 2>&1 && echo "$s ok" || echo "$s FAIL"
