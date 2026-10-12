# Przykłady (`examples/`): skąd brać wzorce kodu

To prawdziwe pliki scen z zaakceptowanych projektów. **Nie kopiuj scen 1:1 do nowego filmu,** bo każdy film potrzebuje
własnych metafor. Kopiuj **techniki**: jak zbudować telefon, toczony licznik, pisanie tekstu, kursor z kliknięciem, wejście karty.

| Plik | Format | Działa z obecnym `apple.py`? | Co w nim jest |
|---|---|---|---|
| `vsl_16x9_scenes.py` | VSL 16:9, 34 sceny | tak (`PROJECT=…`, SRC i WORDS w nagłówku) | najbogatszy katalog: `phone()`, Dynamic Island, widżety, powiadomienia, Ustawienia z przełącznikami, czat, Dock, Mapy, ikona aplikacji, playlista, Skróty, AirDrop, Kalkulator, Kalendarz, pasek postępu + kółko, przełącznik aplikacji, Portfel, pieczęć gwarancji, CTA z kursorem, finał typograficzny |
| `ad_9x16_scenes.py` | reklama 9:16, 15 scen | tak | `card()` na klatce piersiowej, `vbg()` pionowe tło, dymki czatu, segmented control, pytanie i pieczątka KONSUMENT, toggle + ×12, ikona klucza, ciemna karta z licznikiem 941, siatka kropek, pisanie i kasowanie tekstu, CTA |
| `longform_part3_V-AO.py` | longform 16:9 | **nie** (stara biblioteka `ds.py`; nazwy prawie te same co w `apple.py`) | pulpit Finder, czarna plansza, ekran blokady 2:00, matowe szkło → Safari, anatomia landingu, Live Text, Kalendarz dnia klienta, klawisze ⌘C ⌘V (`cmd_symbol`), Czas przed ekranem, sklep izometryczny, kolejka „Następne”, alert iOS, paragon → 0 zł, karta pokładowa |
| `longform_part3_AP-BI.py` | longform | nie (jw.) | Zegar światowy, okładka 3D z odblaskiem, pinezka w Mapach, saldo trzęsące się jak PIN, Przypomnienia „Część 2?”, order bump i upsell, Face ID, „Teraz na stronie: 0”, restauracja w lesie, pokrętło budżetu, karty kątów reklam, feed przelatujący obok reklamy, lejek, tryb skupienia, Night Shift |
| `longform_part3_BJ-CC.py` | longform, finał | nie (jw.) | callbacki: odsłanianie wyników etapami, słupek wychodzący poza kadr, monety 7×50 zł, karta specyfikacji, odliczanie i alarm, kalendarz, równanie ROAS, pierścień → zł/h, lejek z prawdziwymi liczbami, kod BLIK, paragon CTA, przypis szczerości |
| `longform_timer_pills.py` | longform, efekty | nie (jw.) | timer pill: `KNOTS` (czas filmu → czas challenge'u), tryby show, hidden, reveal, roll, skip, countdown, kropki etapów, generator tykania `.wav` |
| `vsl_cut_takes.py` | cięcie | wzorzec konfiguracji | lista TAKES z VSL (2 pliki źródłowe, dograna końcówka) → format `takes.json` dla `cut_takes.py` |
| `premium_helpers_demo.py` (+ .png) | 16:9 demo | tak | nowe pomocniki 2026-10-03: ikona na karcie (`image` + `lower`), łuki do pigułek, zakreślacz, kursywa szeryfowa, licznik-klapki, pisanie, najazd kamery |

**Zrzut słów do wyboru podejść** (Scribe json → `słowo@start`, `|` = pauza > 0,35 s):
```bash
$PY -c "import json,sys; ws=[w for w in json.load(open(sys.argv[1]))['words'] if w.get('type')=='word']; o=[];p=None
for w in ws:
    o+=(['|'] if p is not None and w['start']-p>0.35 else [])+[f\"{w['text']}@{w['start']:.2f}\"]; p=w['end']
print(' '.join(o))" edit/transcripts/RAW.json > edit/L1_words.txt
```

**Przenoszenie z longformu:** stara biblioteka różni się nazwami (`ds.py`, helpery z `scenes_af/af2/gk/lu`).
Odpowiedniki w `apple.py`: `adv`, `check`, `fade`, `pop`, `card_bg`, `Scene`, `blob`, `arc`, `cursor`, `toggle`.
`spinner` i `rise_group` przepisz z przykładu, jeśli są potrzebne. Easing `IN` z dawnej biblioteki to teraz `EIN`.
