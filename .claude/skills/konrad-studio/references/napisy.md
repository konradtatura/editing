# Napisy

Skrypt: `scripts/captions.py` (build, potem render). Wejście: **gotowy, zmontowany** film (z animacjami, jeśli są).

## Proces

1. `$PY $K/transcribe.py FILM.mp4 PROJ/tr` daje `words.json` i `words.txt`.
2. Napisz `PROJ/fixed.txt`: ta sama wypowiedź, poprawiona.
   - Literówki i przesłyszenia ASR popraw według skryptu albo `takes_packed.md`.
     Przykłady z VSL: „Lexio AI” → „lekcje o AI”, „żynek” → „rynek”, „gotowy problem” → „gotowy prompt”,
     „utniesz” → „utkniesz”, „gwarancję lunch” → „gwarancję launchu”.
   - Słowa mają być te, które padają. Nie dopisuj i nie skracaj treści.
   - Liczby pisz cyframi (3, 48, 100%, 5130 zł). Interpunkcja pomaga dzielić bloki, na ekranie znika.
   - Gdy audio mówi błędną liczbę, a ekran pokazuje poprawną, w napisie daj poprawną i zgłoś to.
3. `$PY $K/captions.py build PROJ/tr/words.json PROJ/fixed.txt PROJ/caps.json --keep "Cyfrowy,Autopilot,TikToku"`
   - Wypisuje każdy blok z czasem. Przeczytaj całość: bez sierot typu „i”, „w”, „do” na końcu bloku,
     liczba nie jest oddzielona od jednostki, nowe zdanie zaczyna nowy blok.
4. `$PY $K/captions.py render FILM.mp4 PROJ/caps.json OUT_napisy.mp4 --style box|reel [--color yellow] [--alpha OUT.mov]`
5. Sprawdź `check.py sheet` w kilku miejscach: napis jest od pierwszej do ostatniej klatki, nie wchodzi na kartę animacji,
   nie ucina się na krawędzi. Wyślij `_tel.mp4`.

## Reguły dla obu stylów

- **2–5 słów na blok** (zależnie od długości), jedna linia, max ~24–28 znaków.
- **Zero przerw:** każdy blok trwa, aż wejdzie następny. Pierwszy od klatki 0, ostatni do końca filmu.
  Bez fade, podskoków i podświetleń słów.
- **Małe litery, bez kropek i przecinków.** Zostają akronimy (AI) i nazwy własne z `--keep`.
- Nowe zdanie zawsze w nowym bloku. Nie łącz końca zdania z początkiem kolejnego.

## Styl `box` (16:9: VSL, longform), zatwierdzony 2026-10-01

- Inter Bold, tracking −50 (−0,05 em), ~38 px przy 1080p, biały.
- Tło: czarny prostokąt 50% krycia dopasowany do tekstu (wys. 54 px, padding 13, promień 8).
- Wyśrodkowany, środek na ~91% wysokości kadru (y≈984). Leży też na pełnoekranowych animacjach.

## Styl `reel` (9:16 rolki), zatwierdzony 2026-09-26

- Inter Bold, tracking −50, ~48 px przy szerokości 1080. Miękki jasny cień, bez obrysu i bez tła.
- Stała pozycja przez cały film, pod brodą lub na brodzie: 0,62–0,71 wysokości od góry (dobierz do kadru z arkusza).
  Pozycja nie śledzi twarzy.
- Oddawaj **dwie wersje:** biały i żółty `#FFFF00` (dokładnie FFFF00).
- Zwykle 1–3 słowa (krótsze niż w box): użyj `--maxw 3 --maxc 18`.
- Starszy styl (Proxima Nova Semibold z obrysem, 2–3 słowa, skill `konrad-video-edit`) tylko na wyraźną prośbę.
