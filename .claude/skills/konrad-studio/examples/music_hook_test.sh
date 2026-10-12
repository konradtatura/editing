#!/bin/zsh
# Test: Iman-style music under the hook (0:00–0:48) of FINAL_v2.
# Track build-up (20.2 s in the track) lands on „Nazywam się Konrad” (21.86) → delay 1.66 s. Music cut to silence on „No właśnie.” (13.40–14.05), ducked under the voice, EQ dip where the voice sits, fade into the chapter turn.
cd "$(dirname "$0")"
V=../YT_Ciezka-praca_FINAL_v2.mp4
M=hook_test.wav
END=48.4
ffmpeg -v error -y -t $END -i $V -i $M -filter_complex "
[1:a]aresample=48000,aformat=channel_layouts=stereo,atrim=0:$END,asetpts=PTS-STARTPTS,adelay=1660:all=1,
 highpass=f=45,equalizer=f=2600:t=q:w=1.2:g=-5,volume=-14dB,
 volume='if(between(t,13.40,14.05),0,1)':eval=frame,
 afade=t=in:st=1.66:d=0.05,afade=t=out:st=46.9:d=1.4[m0];
[0:a]asplit=2[v][sc];
[m0][sc]sidechaincompress=threshold=0.04:ratio=4:attack=25:release=350:makeup=1[m];
[v][m]amix=inputs=2:normalize=0:duration=first,alimiter=limit=0.84:level=false[a]" \
 -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 320k -movflags +faststart TEST_hook_muzyka.mp4
ffmpeg -hide_banner -nostats -i TEST_hook_muzyka.mp4 -af ebur128=peak=true -f null - 2>&1 | grep -E "I:|Peak:" | tail -2
