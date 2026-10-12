# Cięcie (E2)

Cel: film brzmi świetnie z zamkniętymi oczami. Zero ciszy, powtórzeń, falstartów i losowych ucięć. Skrypt jest orientacyjny — Konrad mówi swobodnie, dobre improwizacje zostają.

## Jak czytać takes_report.md
- **restart** — fraza zaczęta kilka razy („daj mi 3 minuty, daj mi 3 minuty, a pokażę…”) → zostaje ostatni start, który ma ciąg dalszy.
- **retake** — całe zdanie powtórzone później → zostaje najlepsze pełne podejście. Zwykle ostatnie, ale sprawdź: energię, przejęzyczenia, czy zdanie się kończy.
- **filler** — yyy/eee.
- **junk** — halucynacja rozpoznawania (to samo słowo 4+ razy).
- **asr-gap** — jedno „słowo” > 1,2 s = rozpoznawanie pominęło fragment (często całe podejście). Sprawdź okolicę w words_raw.json; jeśli trzeba, posłuchaj sensem po sąsiednich słowach i wytnij cały fragment.

## Zasady wyboru
1. Każda linia skryptu (albo myśl, jeśli improwizuje) występuje dokładnie raz.
2. Lepsze pełne podejście > sklejka z dwóch połówek. Sklejaj tylko na granicy zdania lub frazy.
3. Nie zaczynaj podejścia od spójnika, jeśli poprzednie zdanie zostało wycięte w połowie („…i to nawet” → zacznij od pełnej frazy).
4. Ostatnie zdanie przed cięciem musi się kończyć (słyszalna kropka).
5. Wątpliwość → zapisz w plan.md w sekcji „do sprawdzenia” (np. „2:00 ‘I-i dlatego’ — zostawiłem, bo inne podejście jest słabsze”).

## takes.json
```json
{"takes":[{"start":32.56,"end":43.04,"note":"Daj mi 3 minuty … żeby go sprzedawać."}],
 "pause_max":0.24, "pause_keep":0.14}
```
Czasy z words_raw.json (start pierwszego słowa, koniec ostatniego). `cutter.py build` sam dociąga krawędzie do głosu (wycina wdech przed podejściem, chroni miękkie spółgłoski), skraca pauzy > 0,24 s do 0,14 s, nie tnie w słowie. Kilka plików źródłowych: `"sources":{"A":"/abs/a.mp4","B":"/abs/b.mp4"}` i `"src":"B"` w podejściu (B wymaga osobnej transkrypcji `words_raw_B.json`).

## Kontrola po renderze
Przeczytaj `transcript_cut.md` od początku do końca. Szukaj: dwóch podobnych zdań obok siebie, urwanych słów, „i… i…”, zdań bez końca. Popraw takes.json → build → render.
