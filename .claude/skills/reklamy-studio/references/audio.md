# Muzyka i SFX

Konrad nie ma Artlist ani Epidemic, więc muzykę i SFX biorę z darmowej biblioteki z licencją na reklamy.

## Źródło: Mixkit
- Licencja Mixkit Free: „commercial projects (YouTube videos, social media marketing, online ads…)”, bez podawania autora.
  Nie dotyczy TV, radia, gier ani nośników fizycznych. Każdy plik musi mieć „Free License” (`#musicFree` / SFX free), nie „Restricted”.
- Strony mixkit.co blokują curl (Cloudflare), więc listy pobieram headless Chromium (`playwright`), a pliki wprost z `assets.mixkit.co`:
  - muzyka: `https://assets.mixkit.co/music/<id>/<id>.mp3`
  - SFX: `https://assets.mixkit.co/active_storage/sfx/<id>/<id>-preview.mp3`
- Alternatywa tylko na FB/IG: Meta Sound Collection (licencja tylko w obrębie platform Mety).
- Lokalnie (Mac) mixkit.co działa zwykłym curl; lista utworów jest w JSON-LD strony (`/free-stock-music/mood/playful/` itd.), pole `license` musi kończyć się `#musicFree`.
- Pixabay i Freesound z serwera dają 403.

## Źródło 2: Openverse (od ailego12, 2026-10-15)
- API: `https://api.openverse.org/v1/audio/?q=<fraza>&license=cc0&page_size=20` (bez klucza, curl; Python urllib na Macu ma problem z certyfikatami).
- Tylko **CC0**: w reklamie nie podpisujemy autorów, więc CC BY / BY-NC odpadają. Pliki to podglądy Freesound (`cdn.freesound.org/previews/...-hq.mp3`), lokalnie się pobierają.
- Nie da się odsłuchać, więc wybór po tytule + analizie (długość, położenie szczytu, szum tła). Każdy plik normalizuję do szczytu -1 dBFS.
- Lista użytych plików z linkami: `projekty/audio/sources_ad12.json`. Fajny motyw do filmów LEGO: „LEGO Click” / „LEGO Brick Fall” (CC0).

## Użyte pliki (ID)
- Muzyka: 322 „Life's a Movie” (ad14, filmowa, od 4,5 s; Konrad wybrał z 3 próbek, „Hip Hop 02” 738 mu nie siadł), 173 „Better Times are Coming” (ad12/ailego12, pozytywny synthpop, Konrad wybrał z 3 próbek), 140 „Cyberpunk City” (ad11, kosmos/tech, 1:40), 134 „Deep Techno Ambience”, 175 „Digital Clouds”, 184 „Vastness”.
- SFX: whoosh 1492 / 1490 / 1489, sweep 166, pop_whoosh 3005, pop_msg 2354, click_select 1109, click_tech 3124, coins 1993, coin_prize 1999.

## Miks: `projekty/audio/mix.py CUES.json IN.mp4 OUT.mp4`
- Muzyka: gain ok. -21 dB przy utworze -11 LUFS i głosie -18 LUFS (podkład ok. 14 LU pod głosem), sidechain ducking pod głos,
  fade-in 0,4 s, fade-out 2 s.
- SFX: `peak: true` ustawia najgłośniejszy moment dźwięku dokładnie na czasie cue (whoosh na cięciu).
- Wyjście: pomiar głośności, stały gain do -14 LUFS + limiter -2,5 dBFS, AAC 192k (koder Apple `aac_at`), wideo kopiowane bez ponownego kodowania.
- Bez `music` w CUES robi sam sound design (SFX only). `dur` przycina dźwięk, żeby nie przechodził przez cięcie hooka.
- Cue sheet per reklama: `projekty/audio/cues_<ad>.py`. Ad11: whoosh -17 dB na cięciach scen (najwyżej 1 na sekundę),
  pop -12 dB na żółtych akcentach, monety przy 941, powiadomienie przy „Automatycznie”, „ding” przy 17 zł, klik przy „Kliknij przycisk”.

- Ad12 (ailego12, styl 9, tylko SFX): `cues_ad12.py SFXDIR OUT.json`. Whoosh -23 dB na cięciach, szerszy swoosh -19 dB na zmianach sekcji (blur),
  ka-ching na 79 zł, klik na „klika link”, powiadomienie na „kupuje”, monety na „wielokrotnie”, odwrócony talerz + boom przed „Bo AI”,
  boom + pieniądze na 941, klocki LEGO na kroki 1-2-3 i rząd ikon, klik na „Kliknij”, pop na strzałkę CTA.
  Na cięciach hooków (12,767 / 23,133) dźwięk startuje na cięciu, nic sprzed cięcia nie wybrzmiewa za nie.
- Ad13 (film 13, styl 9, „gadający ziemniak”): `cues_ad13.py SFXDIR MUSIC OUT.json`. Ta sama paleta co ad12, poziomy przesunięte o różnicę
  głośności głosu (`VO_SHIFT`). Muzyka 173 w segmentach (`musicSegments`): hooki od 0, body od 0 na cięciu body (utwór krótszy niż film).
  Biblioteka SFX odtwarza się z `sources_ad12.json`: `fetch_sfx.py sources_ad12.json SFXDIR`.

## Zasady
- SFX oszczędnie: ma brzmieć dopracowanie, nie efekciarsko.
- Wybór muzyki w ciemno nie działa: zawsze 3 próbki po 30 s w różnych klimatach i Konrad wybiera. Nie powtarzaj tego samego utworu w kolejnej reklamie, chyba że poprosi.
- Na serwerze nie da się odsłuchać, więc zawsze wysyłam próbkę do akceptacji klimatu i głośności, zanim zrobię wszystkie reklamy.
- Klimat per styl: styl 3 spokojny/premium, styl 2 ciepły i energiczny, styl 4 (animacje) elektroniczny/kosmiczny.
