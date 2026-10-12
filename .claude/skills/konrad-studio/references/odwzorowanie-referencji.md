# Odwzorowanie referencji: „zrób mi taki edit jak ten”

Sprawdzone na „16–26” (2026-10-05, wzór: rolka nathanazareth). Konrad ocenił wynik: „10/10, dojebane, kiedyś zapłaciłem za taki
film 1000 zł”. Metoda działa dla każdego wzoru: rolki, reklamy, VSL czy fragmentu longformu.
**Najpierw rozłóż wzór do klatki, potem planuj, a na końcu buduj.** Nie zgaduj stylu z pamięci.

## 0. Zasady

- **Treści wzoru nie kopiujemy, tylko jego techniki.** Wyjątek: Konrad ma zgodę autora (jak przy Nathanie), ale i wtedy tekst i materiał są jego.
- **Prawa:**
  - cudzych relacji ani filmów (pobranych z IG/TikToka, np. StorySaver) nie używamy;
  - stock (Pexels, Pixabay) tylko po zgodzie Konrada na pobranie;
  - twarze innych twórców zastępujemy wymyślonymi miniaturami (`GuruWall`).
- **Kolejność bramek:** breakdown → katalog klipów → plan ujęć → **OK Konrada** → render → arkusz kontrolny → oddanie.

## 1. Breakdown wzoru (zapisz jako `PROJ/BREAKDOWN.md`)

1. `ffprobe`: wymiary, fps, długość. Pełna klatka: czy to nie siatka 2×2 (`referencje.md`)?
2. **Cięcia:** `ffprobe -f lavfi -i "movie=REF,select=gt(scene\,0.18)" -show_entries frame=pts_time`. Policz średnią długość ujęcia.
3. **Arkusze 3 kl/s** całego filmu (`fps=3,scale=320:-2,tile=6x6`, co 12 s) i **przeczytaj każdy**.
4. **Transkrypcja z czasami słów** (`transcribe.py … --lang en` przy angielskim, bo z domyślnym `pl` Whisper halucynuje).
   Potem tabela „cięcie → słowa”, która pokazuje, na którym słowie wypada każda zmiana ujęcia.
5. **Kluczowe momenty w 10 kl/s:** otwarcie, plansze, efekty, CTA.
6. **Animacje tekstu w 30 kl/s:** wycinek kadru z napisem (`crop=…,tile=6x6`) dla 3–4 słów.
   Szukaj: skąd słowo wjeżdża, ile klatek trwa wejście, czy jest smuga lub rozmycie, skala, dryf, wyjście.
   **Konrad to zauważa** („jego animacje tekstu są lepsze”), więc ten krok jest obowiązkowy.
7. **Typografia i kolor:** zbliżenie kadru z tekstem (krój, grubość, cień), paleta plansz, gradacja (B&W / kolor i po co).
8. **Audio:**
   - poziom w pauzach mowy vs mowa (czy jest muzyka i jak głośna),
   - udział basu < 150 Hz,
   - mocne uderzenia basu vs cięcia (czy zmiany sekcji są na beatach).
9. **Proporcje:** twarz / b-roll kolor / b-roll B&W / plansze, w sekundach i %.

**Format `BREAKDOWN.md`:**
formuła w 1 zdaniu · liczby · system napisów · plansze · kolor · efekty „wow” z czasami · dźwięk ·
oś czasu cięcie po cięciu · przełożenie na Konrada (co 1:1, co dopasować, czego potrzebujemy od niego, prawa).

## 2. Katalog klipów Konrada (`PROJ/KATALOG_klipow.md`)

- `ffprobe` wszystkich: obrót, wymiary, fps, długość, MB, data.
- **Pion** to standard u Konrada. Do 16:9 bierzemy poziomy pas (`band` 0…1):
  - 4K pion daje pas w pełnej jakości,
  - 1080 jest lekko miękkie,
  - 720p i mniej tylko jako kafel w siatce.
- Arkusz 6 klatek na klip z etykietą `B01…` (PIL, bo w tym ffmpeg nie ma `drawtext`). **Przeczytaj wszystkie.**
- **Długie klipy z pracą** (kilkanaście minut): arkusz co 30–36 s. Znajdź momenty-perełki: zamyślenie, puste biurko,
  odwrócenie do kamery, zamykanie laptopa. Wycinaj je co do sekundy (dodatkowy arkusz 1 kl/s wokół momentu).
- Szukaj **złota**, czyli kadrów, które same opowiadają historię (np. billboard KVNRADPROFIT na Nasdaq). One dostają kluczowe zdania.
- Oznacz, czego **nie** używamy i dlaczego (cudze relacje, słaba jakość).

## 3. Plan ujęć (`PROJ/PLAN_<nazwa>.md`), jedyna bramka akceptacji

Tabela `# | czas | słowa | ujęcie (ID + sekunda klipu + band) | napis (BOHATER) i efekt`.
- Czas cięcia = start pierwszego słowa nowej frazy minus ok. 0,04 s (słowa ze Scribe, dosłownie).
- Proporcje jak we wzorze. Policz i wpisz je w plan.
- „Oni / problem” idzie w B&W, „ja / wynik” w kolorze. Każde zdanie dostaje obraz, który je pokazuje.
- Na końcu pytania do Konrada: zdjęcia, zgoda na stock, format (pion/poziom), muzyka.

## 4. Budowa: `scripts/kinetic.py`

Wzorcowy film: `examples/kinetic_16x9_nathan_style.py`. Skopiuj go do projektu i podmień ścieżki, `DISPLAY`, `build()`.
- `K.setup(words, DISPLAY, KEEP_CASE)`:
  - słowa ze Scribe;
  - `DISPLAY` zamienia liczby słowne na cyfry („sto trzydzieści tysięcy” → „130 000+”, kolejne słowa → `""`),
    poprawia literówki mowy w napisie i wstawia cudzysłowy.
- `shots` to lista `(t0, t1, kind, params)`, `phrases` to lista `K.Phrase(...)`. Szczegóły w `biblioteka-efektow.md`.
- **Podgląd przed renderem:** `run(..., frames=[...])` robi arkusz. Przejrzyj **wszystkie** ujęcia, a po każdej poprawce te zmienione.
- Pełny render ~53 s trwa ok. 6–8 min. Puść w tle.

## 5. Dźwięk

- Głos z nagrania: `aresample=async=1:first_pts=0` → kompresja → `loudnorm` −14 LUFS, `apad`/`atrim` do długości.
  Synchron sprawdź korelacją (0 ms).
- **Muzyka:** pytaj. Konrad czasem woli dodać ją sam („skipnij muzykę, ja dodam na końcu”).
- **Efekty jako osobna ścieżka:**
  - boom (generowany numpy: sweep 90→40 Hz + szum) na zmianach sekcji,
  - whoosh na planszach,
  - tick przy liczniku,
  - click przy siatce.
- **Oddanie:** `_EDIT.mp4` (sam głos), `_z_efektami.mp4`, `_efekty.wav`, `_tel`.

## 6. Kontrola przed oddaniem

- Arkusz kluczowych momentów z gotowego pliku: otwarcie, siatka, CTA, ostatnia klatka.
- Długość wideo i audio się zgadza, −14 LUFS, TP ≤ −1.
- W raporcie wymień decyzje do sprawdzenia przez Konrada: autoironia, czyj klip, wymyślone tytuły.

## Pułapki (wszystkie już nas ugryzły)

| Objaw | Przyczyna / rozwiązanie |
|---|---|
| ffmpeg „Invalid argument” przy najeździe | `crop` nie zmienia w/h w czasie. Najazd robimy przez `scale=w='…*(1+z*t/d)':eval=frame` + stały `crop`. |
| `No such filter: ''` w zsh | `"$v[c]"` to indeks tablicy w zsh. Pisz `"${v}[c]"`. |
| Transkrypcja angielskiego to bełkot po polsku | `--lang en`. |
| Przycięty klip spóźnia się w złożeniu | wejściowe `-ss` + `setpts`. Wycinaj filtrem `trim` (`bledy.md`). |
| Moment z długiego klipu jest „prawie” dobry | sprawdź arkusz 1 kl/s wokół momentu. Puste biurko było 2 s później, niż pokazał arkusz co 6 s. |
| Słowa „po prostu się pojawiają”, a Konrad mówi, że animacje są słabe | `Phrase` ma już wjazd ze smugą, skalę bohatera, dryf i wyjście. Nie wyłączaj tego. |
| Tekst ginie na jasnym tle | cień `video`: szeroki blur 22 × 0,85 + ciasny 3 px. Na planszach jasnych cień słabszy. |
| Linia drobnych słów wychodzi poza kadr | `Phrase` sama zawija i dosuwa blok. Przy twarzy zostaw `maxw` ok. 560–700. |
