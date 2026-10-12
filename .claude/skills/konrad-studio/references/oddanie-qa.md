# Oddanie i kontrola jakości

## Co dostaje Konrad (domyślnie)

```
PROJ/
  Animacje/
    S07_od-0-32-000_Najwieksza-zmiana_BROLL.mp4      pełny ekran, z dźwiękiem oryginału tego zakresu
    S12_od-0-55-850_Model_MIX.mp4                    karta nałożona na nagranie, z dźwiękiem
    S12_od-0-55-850_Model_NAKLADKA.mov               ta sama karta, ProRes 4444 z alfą (do jego montażu)
  NAZWA_FULL.mp4                                     cały film z animacjami (gdy prosi lub do kontroli)
  NAZWA_FULL_tel.mp4                                 kopia na telefon (< 30 MB, przez SendUserFile)
  LISTA_ANIMACJI.md                                  tabela: # | od | do | typ | co robi + „do sprawdzenia”
  scenes_*.py, projects/*.tsrct                      edytowalne źródła
```

- **Nazwa:** `KOD_od-M-SS-mmm_Etykieta_TYP`. Czas wejścia na osi filmu, żeby Konrad mógł położyć klip bez szukania.
- **Typy:** `_BROLL` (pełny ekran), `_MIX` + `_NAKLADKA` (nakładka), dodatkowo `.wav` dla efektów (tykanie, klik), jeśli są.
- Tylko efekty (pigułki timera, layout) oddawaj jako krótkie klipy. Pełny render, gdy o niego prosi.

## Kontrola przed oddaniem (nie oddawaj niesprawdzonego)

1. **Arkusze klatek scen** (`preview.py --auto 0.15 0.5 0.9`) i **przeczytaj każdy**. Szukaj:
   - pustych klatek na starcie lub końcu (biała pustka, sama karta bez treści),
   - tekstu na twarzy lub ustach i karty zasłaniającej oczy,
   - uciętego tekstu, nachodzących elementów, literówek, braku polskich znaków,
   - liczb innych niż w audio lub skrypcie i wymyślonych danych bez oznaczenia,
   - stylu, który odpłynął (za dużo tekstu, ozdobniki, ten sam szablon co poprzednia scena),
   - błędów glifów (kwadraciki, emoji zamiast ⌘ lub ✓).
2. **Bramki automatyczne** (wszystkie muszą przejść albo masz uzasadnienie):
   - `check.py motion Animacje/*.mp4`: brak `BLANK FIRST FRAME`, brak bezruchu > 0,6 s w środku sceny
     (końcowe przytrzymanie przed cięciem może być dłuższe),
   - `check.py alpha Animacje/*.mov` musi dać `yuva…`,
   - przy cięciu: `check.py pauses CUT.mp4` + `splice_audit.txt`,
   - z dźwiękiem: TP < −1 dBTP na finalnym MP4 (`check.py loud`).
2b. **Ciągłość:** `snap_gaps.py` przed eksportem, czyli zero klatek kamerki między animacjami, które idą po sobie.
3. **Głośność:** `check.py loud ŹRÓDŁO FULL.mp4 [klipy…]`, różnica ≤ ±0,5 dB (zwykle 0,0).
4. **Pełny film:** `check.py sheet FULL.mp4 --n 24` oraz `--times` w momentach wejść i wyjść animacji.
   Sprawdź, że cięcia są twarde i nie ma przeskoku dźwięku.
5. Poprawki wprowadzaj w pliku scen, buduj ponownie i eksportuj tylko zmienione klucze (`export.py scenes.py S07 S12 --full …`).

## Retro (obowiązkowe, po oddaniu lub po ostatniej rundzie poprawek)

1. Uczciwie, w 3–5 punktach: co poszło dobrze, co źle, ile rund, co trzeba było przewidzieć.
2. Każdy powtarzalny błąd trafia do `references/bledy.md`, a jeśli się da, poprawka idzie do skryptu.
3. Każda uwaga Konrada trafia do `references/feedback.md`, a nowa udana scena do `examples/`.

## Raport (po polsku, krótko)

- Gdzie są pliki: ścieżki jako linki i wysłana wersja `_tel`.
- Ile scen, ile pełnych ekranów, ile nakładek. Ewentualnie bardzo krótka lista najważniejszych.
- **Do sprawdzenia:**
  - przykładowe dane (nazwy, ceny, zadania),
  - różnice audio vs ekran (np. „w audio 947, na ekranie 941”),
  - niepewne słowa w napisach,
  - wątpliwe łączenia w cięciu.
- Bez technicznego żargonu (kodeki, fps).
