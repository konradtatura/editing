---
name: reklamy-studio
description: "Konrad's paid-ad editing studio for vertical 9:16 Meta ads (Cyfrowy Autopilot and similar). Recreates any reference ad style he sends (breakdown → style engine → captions, zooms on cuts, plansze, b-roll, CTA), then runs QA loops, a Video Review artifact with timestamped notes, music + SFX from free-licensed libraries, and 1080p finals under 30 MB. Four ready styles: styl 1 (white + dark green, Inter, plansze), styl 2 (teal gradient hero words, warm cinematic, b-roll), styl 3 (navy + electric indigo, big stacked captions, proof cards), styl 4 (captions only: Poppins ExtraBold caps for AI-animation ads). Use for: „zmontuj reklamę / adsa”, „taki styl jak w tym filmie”, „odwzoruj ten edit”, „dodaj napisy w stylu oryginału”, „dałem feedback w review”, „muzyka i sfx do reklam”, or when Konrad uploads ads + a reference video."
---

# Reklamy Studio: montaż płatnych reklam w stylu z referencji

Zapis warsztatu z sesji 2026-10-12/13 (reklamy ad8, ad9, ads7, ads10, ads5, ads2, ad11 dla Cyfrowego Autopilota).
**Jak pracujemy:** Konrad wysyła film-wzór („taki styl”) i swoje surowe reklamy. Ja rozkładam wzór na czynniki,
buduję silnik stylu, montuję, sam sprawdzam każdą klatkę, wrzucam do Review, a on zostawia notatki z czasem.
Każda reklama ma inny kąt (angle) i trochę inny montaż.

Konrad jest marketerem, nie montażystą. Piszę po polsku, krótko, bez kodeków i fps. Pytam tylko o treść i gust.
Często jest na telefonie, więc wysyłam gotowe pliki (SendUserFile), a nie ścieżki.

## Najpierw przeczytaj
1. `references/zasady-konrada.md`: jego twarde wymagania i każdy feedback, który już dał. **Złamanie którejś = poprawka.**
2. `references/style-katalog.md`: 9 gotowych stylów (kolory, fonty, rozmiary, ruch, który adsy w jakim stylu).
3. `references/pipeline.md`: komendy krok po kroku (transkrypcja, cięcia, spec, render, kompozycja, QA, eksport, Review).
4. `references/bledy-i-lekcje.md`: błędy, które już raz wyszły. Sprawdź przed oddaniem.
5. `references/nowy-styl.md`: jak odtworzyć nowy styl z filmu-wzoru.
6. `references/audio.md`: muzyka i SFX (licencje, miks, ducking, -14 LUFS).

Kod silników leży w repo w `projekty/` (styl 1: `reklamy_CA/`, style 2–9: `styl2/` … `styl9/`, audio: `audio/`). Strona Video Review: `review/video-review.html`.
W paczce zip (`paczka/reklamy-studio.zip`) ten sam kod jest w `silniki/` obok tego pliku. Ścieżki `projekty/...` = `silniki/...`.

## Przebieg pracy (zawsze w tej kolejności)
1. **Materiały.** Pliki z Drive (folder od Konrada) pobieram `gdown`. Wzór obejrzyj skillem `watch` albo arkuszami klatek.
2. **Breakdown wzoru** → `projekty/stylN/BREAKDOWN.md` (formuła, liczby, napisy, plansze, kolor, dźwięk, psychologia,
   przełożenie na Konrada). Kolory i fonty dobieram sam, jeśli Konrad tak powie.
3. **Cięcia.** Wykryj każde cięcie w jego nagraniu (`cuts.py`) i porównaj z liczbą, którą poda Konrad („ads10 ma 20 cięć”).
   Zoomy i plansze zmieniają się DOKŁADNIE na cięciach. To jego najczęstsza uwaga.
4. **Transkrypcja** faster-whisper medium (pl), potem tekst ze skryptu nakładany na czasy słów (difflib), żeby nie było literówek
   whispera („czas GPT” → „ChatGPT”).
5. **Plan** plansz i akcentów pod angle reklamy → `build_specN.py`. Fakty tylko prawdziwe (941 e-booków, 17 zł, 48 h, 3 lata).
6. **Render** warstwy (Playwright → przezroczyste PNG) + **kompozycja** (zoom per ujęcie, gradacja, b-rolle, oryginalny dźwięk).
7. **QA** (obowiązkowe, dwa przejścia): arkusz klatek co 0,5–1 s + pary przed/po każdym cięciu. Szukam: nachodzenia na usta,
   zderzeń napisów z planszami/listami, pustych plansz, starego zoomu po cięciu, skaczących napisów, ucinanych słów.
8. **Review**: kopia 720p (~14 MB) do artefaktu Video Review, `videos` w bazie (ver+1), odpowiedź na każdą notatkę i `status: done`.
9. **FINAL**: 1080p, dwuprzebiegowo, poniżej 30 MB, wysłany przez SendUserFile. Commit i push.

## Zasady komunikacji
- Na „daj klatkę, powiem czy git”: renderuję JEDNĄ klatkę na trudnym tle i wysyłam obraz, zanim zrobię cały film.
- Gdy Konrad powie „nie rób X” (np. „nie ucinaj hooków, sam to zrobię”): przerywam od razu i usuwam to, co zrobiłem.
- Gdy feedback jest ogólny („gradient dalej niewidoczny”): szukam przyczyny w kodzie, nie tylko podkręcam wartości.
- Podsumowanie po robocie: co poprawione per film, krótko, po polsku.
