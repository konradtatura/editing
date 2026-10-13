# Muzyka i SFX

Konrad nie ma Artlist ani Epidemic, więc muzykę i SFX biorę z darmowej biblioteki z licencją na reklamy.

## Źródło: Mixkit
- Licencja Mixkit Free: „commercial projects (YouTube videos, social media marketing, online ads…)”, bez podawania autora.
  Nie dotyczy TV, radia, gier ani nośników fizycznych. Każdy plik musi mieć „Free License” (`#musicFree` / SFX free), nie „Restricted”.
- Strony mixkit.co blokują curl (Cloudflare), więc listy pobieram headless Chromium (`playwright`), a pliki wprost z `assets.mixkit.co`:
  - muzyka: `https://assets.mixkit.co/music/<id>/<id>.mp3`
  - SFX: `https://assets.mixkit.co/active_storage/sfx/<id>/<id>-preview.mp3`
- Alternatywa tylko na FB/IG: Meta Sound Collection (licencja tylko w obrębie platform Mety).
- Pixabay i Freesound z serwera dają 403.

## Użyte pliki (ID)
- Muzyka: 140 „Cyberpunk City” (ad11, kosmos/tech, 1:40), 134 „Deep Techno Ambience”, 175 „Digital Clouds”, 184 „Vastness”.
- SFX: whoosh 1492 / 1490 / 1489, sweep 166, pop_whoosh 3005, pop_msg 2354, click_select 1109, click_tech 3124, coins 1993, coin_prize 1999.

## Miks: `projekty/audio/mix.py CUES.json IN.mp4 OUT.mp4`
- Muzyka: gain ok. -21 dB przy utworze -11 LUFS i głosie -18 LUFS (podkład ok. 14 LU pod głosem), sidechain ducking pod głos,
  fade-in 0,4 s, fade-out 2 s.
- SFX: `peak: true` ustawia najgłośniejszy moment dźwięku dokładnie na czasie cue (whoosh na cięciu).
- Wyjście: loudnorm -14 LUFS / -1,5 dBTP, AAC 128k, wideo kopiowane bez ponownego kodowania.
- Cue sheet per reklama: `projekty/audio/cues_<ad>.py`. Ad11: whoosh -17 dB na cięciach scen (najwyżej 1 na sekundę),
  pop -12 dB na żółtych akcentach, monety przy 941, powiadomienie przy „Automatycznie”, „ding” przy 17 zł, klik przy „Kliknij przycisk”.

## Zasady
- SFX oszczędnie: ma brzmieć dopracowanie, nie efekciarsko.
- Na serwerze nie da się odsłuchać, więc zawsze wysyłam próbkę do akceptacji klimatu i głośności, zanim zrobię wszystkie reklamy.
- Klimat per styl: styl 3 spokojny/premium, styl 2 ciepły i energiczny, styl 4 (animacje) elektroniczny/kosmiczny.
