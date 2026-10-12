#!/bin/zsh
# render every scene in high quality: cards + wall callouts → ProRes 4444 MOV (alpha), full scenes → MP4
cd "${0:A:h}"
for s in L01 L04 L07 L09 L11b L14 L15 L19 L22 L25 L26b L30 L32 L32b L33 C01 C02 C03 C04 C05 C06 C07 C08 C09 C10 C11 C12 C13 C14; do [[ -f out/$s.mov ]] || ./hi.sh $s mov; done
for s in L02 L03 L06 L08 L10 L11 L12 L13 L16 L17 L18 L20 L21 L23 L24 L26 L27 L28 L29 L31; do [[ -f out/$s.mp4 ]] || ./hi.sh $s mp4; done
echo ALL DONE
