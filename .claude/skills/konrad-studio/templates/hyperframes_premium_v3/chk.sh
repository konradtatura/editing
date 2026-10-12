#!/bin/zsh
# chk.sh SCENE [mov] — lint, draft render, 6-frame contact sheet → out/SCENE_sheet.png (mov = alpha, shown over a wall-grey)
cd "${0:A:h}"; s=$1; fmt=${2:-mp4}; T=out/tmp; mkdir -p $T
cp $s.html index.html; npx hyperframes lint . 2>&1 | grep -iE "error|warn|✗" | head -12
npx hyperframes render -c $s.html --quality draft --format $fmt --output out/${s}_draft.$fmt --quiet >/dev/null 2>&1 || { echo RENDER FAIL; exit 1; }
./sheet.sh $s $fmt
