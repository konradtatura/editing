# Dźwięk

Połowa „drogiego” wrażenia u Imana to dźwięk. Każda grafika ma swój dźwięk, cichy na tyle, żeby go czuć, a nie słyszeć.

## SFX (automatycznie w assemble.py)
Zestaw w `assets/sfx/` (generowany `scripts/make_sfx.sh`; każdy plik można podmienić lepszą próbką o tej samej nazwie):
whoosh (wejścia tekstu/kart), swish (okno z Konradem, zoom strony), pop (elementy list), tick (liczby), click (kursor), hit (karta rozdziału), riser (przed odsłoną).
Domyślne przypisanie per typ jest w `assemble.py:default_sfx`. Nadpisanie w planie: `"sfx":[{"t":0.4,"name":"pop","vol":0.4}]` albo `"sfx":false`.

## Muzyka
- Konrad dostarcza utwory (Artlist / Epidemic — dokumentalne, spokojne, „premium”). `film.music` = ścieżka. Bez pliku film idzie bez muzyki (nie syntetyzuj muzyki w kodzie).
- Pod głosem ok. -24 dB, ducking sidechain pod mową.
- `film.musicCuts` — muzyka znika na kluczowym zwrocie/problemie i wraca na rozwiązaniu (technika Imana). 1–3 razy na film.
- Wejście 1,5 s, wyjście 2,5 s.

## Głośność
Dwuprzebiegowo: kompresja głosu + limiter → loudnorm -14 LUFS, true peak ≤ -1,5 dB (standard YouTube). `qa.py final` sprawdza ±1 LUFS.
