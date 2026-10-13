# Nowy styl z filmu-wzoru

Konrad: „taki styl, tekst, zoomy, animacje (nie giga dużo, ale ważne)”. Cel: wierne odwzorowanie formuły, nie kopia 1:1 treści.

## 1. Obejrzyj jak montażysta
- Arkusz co 2 s całego wzoru + mikroskop pierwszych 10 s (hook) co 0,1 s.
- Policz: cięcia, średnia długość ujęcia, % czasu z twarzą vs plansze/b-roll, ile elementów na twarzy.
- Napisy: font (crop 1:1), wielkość względem szerokości kadru, wersaliki, kolor, cień/obrys, ile słów naraz,
  czy słowa wchodzą animacją czy przełączają się twardo, wysokość na ekranie, akcenty (kolor, kursywa, box).
- Plansze: tło, nagłówki, karty, ikony, liczniki, jak wchodzą i wychodzą.
- Kolor obrazu (gradacja), przejścia, dźwięk (muzyka cicho czy głośno, SFX gdzie).
- Psychologia: po co jest każdy element (autorytet, otwarta pętla, pattern interrupt, odwrócenie ryzyka).

## 2. Zapisz breakdown
`projekty/stylN/BREAKDOWN.md` z sekcjami: Formuła, Liczby, Napisy, Plansze, Elementy specjalne, Kolor, Dźwięk, Psychologia,
Przełożenie na Konrada (kolory i fonty pod markę, co od niego potrzeba).

## 3. Zbuduj silnik
- Skopiuj najbliższy styl (`overlayN.html` + `build_specN.py`) i zmień tylko to, co inne. Kontrakt strony: `window.init(spec)`,
  `window.seek(t)` (może zwrócić Promise), przezroczyste tło, 1080×1920.
- Fonty lokalnie (`assets/fonts`, pobierz woff2 z Google Fonts, podzbiory latin + latin-ext dla polskich znaków).
- Wyrenderuj 3–6 klatek na trudnych tłach i porównaj obok wzoru, zanim zrobisz cały film.

## 4. Pierwszy film
Pełny render → QA (2 przejścia) → Review → FINAL. Do opisu dla Konrada dodaj, co przełożyłeś ze wzoru i dlaczego.

## 5. Dopisz styl do `style-katalog.md` i zasady z feedbacku do `zasady-konrada.md`.
