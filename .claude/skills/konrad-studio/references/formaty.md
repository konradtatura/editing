# Formaty: jak montować każdy typ materiału

Wspólne dla wszystkich: styl z `styl-apple.md`, sposób myślenia z `myslenie-editora.md`, oddanie według `oddanie-qa.md`.
Różni się: układ, gęstość, strefy i to, co dostaje Konrad.

---

## Longform YouTube (16:9, 20–40 min), wzór: „Zbudowałem AI biznes w 3h”

**Gramatyka ujęć: każde zdanie dostaje JEDEN tryb** (to jest montaż; z famous-youtube-editor, dopasowane do Konrada)

| Tryb | Kiedy | Jak |
|---|---|---|
| A: twarz na pełnym kadrze | mówi do widza: historia, opinia, żart, hook, CTA, emocja | czysta kamera. Przy ciągu > ~8 s **punch-in** 100% ↔ 112–115% na granicy zdań (udaje 2 kamery), oczy na tej samej wysokości |
| A+: twarz + tekst na ścianie | lista, tytuł rozdziału, liczba, którą wystarczy zobaczyć | tekst obok głowy bez karty (miękki cień), łuk albo strzałka, pisany na słowach |
| A+K: twarz + karta | konkret, który trzeba zobaczyć, a twarz ma zostać | biała karta w wolnej ścianie (nakładka z alfą) |
| B: pełny ekran | pojęcie, schemat, porównanie, liczby, krok po kroku | jedna metafora Apple, twarde cięcie. Karty jako UI (okno, panel, telefon), nie goły tekst |
| C: ekran + kamerka PiP | Konrad pokazuje coś na ekranie | `layout_pip.py`. Zoom „punch-in”: 0,5 s pełny widok → 0,35 s szybki najazd na to, co trzeba przeczytać; tekst czytany od lewej = ognisko przy lewej krawędzi |
| D: b-roll filmowy | konkretne czynności („siadam i buduję”) | nagrania Konrada albo AI b-roll tylko na jego prośbę; dopasowany kolorystycznie, 3–6 s |

**Proporcje w longformie (Konrad, 2026-10-04, po pierwszym filmie): twarz ok. 50% · pełne b-rolle ok. 40% · karty ok. 10%.**
„Głównie full b-rolle” znaczy, że b-roll, kiedy już jest, ma być pełnoekranowy. NIE znaczy, że większość filmu to b-roll.
Pierwsza wersja „Ciężkiej pracy” miała 84% b-rolli i 9% twarzy. Werdykt: „za dużo animacji, mojej twarzy nie ma w tym filmie”.
- B-roll wchodzi na puentę (liczby, porównanie, mapa, mechanizm) i trwa 3–8 s.
- Otucha, emocje i zwroty do widza zawsze na twarzy.
- Między b-rollami co najmniej 4 s twarzy; nigdy dłużej niż ok. 8–10 s bez twarzy.
- Twarz żyje dzięki przybliżeniom 100 ↔ 114% na początkach zdań i złączeniach.
- Planuj tę proporcję JUŻ na etapie listy animacji: policz procenty i pokaż je w planie.
- Gotowy wzorzec przesiewu (z zakończonego projektu YT_Ciezka-praca): `examples/longform_reedit_example.json` (okna full/card/drop), `examples/longform_reedit_cards.py` (b-roll → pływająca karta na lewej ścianie) i składanie przez `scripts/assemble.py --reedit … --zooms auto` (dawny `final_v2.py`, kopia w archiwum; składanie z przybliżeniami).

**Rytm:**
- Hook = A (pierwsze ujęcie to twarz) i CTA = A.
- Co ~5 s coś nowego: zmiana trybu, punch-in, nowa scena albo nowy element w scenie.
- Żaden tryb nie trwa ciągiem > 10 s. B nigdy minutami.
- Zmiany trybu wypadają na granicach słów.
- Dobry przebieg: A → B → A+ → A → C → A+K → A …, regularnie wracaj do twarzy.

**Typy scen**

| Typ | Kiedy | Jak |
|---|---|---|
| FULL (pełny b-roll) | liczby, abstrakcyjne pojęcia, puenty | białe tło, jedna metafora, twarde cięcie z kamery i z powrotem, zwykle 2–10 s |
| OVL (nakładka) | twarz lub ekran mają zostać | biała karta w wolnym miejscu kadru, eksport z alfą; może trwać do ~25 s, jeśli żyje |
| Czarna plansza | max 1 na film | czarne tło, wielki biały tekst, najmocniejszy pattern interrupt |
| Timer pill | challenge, presja czasu | mała czarna pigułka u góry (poniżej) |

**Tryb pracy**
- Konrad przysyła swój zmontowany film (często z już wstawionymi animacjami) plus skrypt.
- Dostaje listę do końca filmu, a potem buduje się **partiami po ~20 scen od góry** („zrób kolejne 20”).
- Długie sceny dziel na części a/b/c, jeśli metafora się zmienia.
- Klucze scen alfabetyczne, ciągnięte przez cały film (V, W, …, AO, AP, …), żeby Konrad łatwo je znajdował.

**Timer pill (Dynamic Island).** Kod: `examples/longform_timer_pills.py`.
- Nie stały pasek („nie trzyma urgency”) i nie pełnoekranowe wejścia („za grube”).
- Mała czarna pigułka na środku u góry (TOP 18 px):
  - zwinięta 126×38, rozwija się do ~58 px wysokości z cyframi Geist Mono 30 px i 4 kropkami etapów
    (zielona = zrobione, pulsująca biała = w toku),
  - pokazuje się 2,5–4 s tam, gdzie Konrad mówi czas na głos, potem znika.
- Mapowanie czasu filmu na czas challenge'u: odcinkowo liniowe `KNOTS` z tego, co pada na kamerze.
- Tryby:
  - `show`: tyka co sekundę,
  - `hidden`: rozmyte, kręcące się cyfry („wyrobi się?”),
  - `reveal`: ukryte, a na słowie odsłonięte,
  - `roll`: przewinięcie przy przeskoku,
  - `skip`: przeskok typu obiad, przewija się i zmienia kolor,
  - `countdown`: ostatnie minuty pędzą.
- Kolory: biały, pomarańczowy (< 40 min), czerwony (< 15 min). Koniec to alarm minutnika na pełnym ekranie.
- Tykanie oddawaj jako osobny `.wav` obok klipu.
- **Oddanie:** każda pigułka to osobny krótki klip z alfą (`--fx-solo main:100`) z wycinkiem audio z finalnego montażu,
  bo Konrad dopasowuje je po waveformie. **Nie renderuj całego filmu.**

**Layout ekran + kamerka.** Skrypt: `scripts/layout_pip.py`.
- Gdy jest nagranie ekranu: ekran na cały kadr plus zaokrąglona kamerka w prawym dolnym rogu:
  24% szerokości, margines 40 px, promień ~30 px po zmniejszeniu, miękki cień.
- Przejście: pełna kamera płynnie zmniejsza się do rogu (0,6 s, smoothstep), a ekran wychodzi spod spodu. Powrót odwrotnie.
- Anty-miganie: przerwy < 3 s scal, ekran pokazuj tylko, gdy trwa ≥ 4 s.
- Pełnoekranowe animacje tną ponad layoutem (`--avoid index.json`). Nakładki w czasie ekranu nie mogą wchodzić na kamerkę.
- Konrad eksportuje ekran dopasowany do osi filmu, czarny tam, gdzie ekranu nie ma.
  Gdy prosi „sama kamerka i ekran”, nie kombinuj z animacjami. Można zrobić render np. pierwszych 10 minut (`--until 600`).

**Pytania do Konrada przed pierwszym longformem danego typu** (raz, krótko):
- czy napisy na YouTube (Konrad 2026-10-03: domyślnie NIE),
- czy muzyka w tle i jaki klimat (2026-10-03: pierwszy longform bez; 2026-10-04 chce spróbować muzyki jak u Imana, patrz `muzyka.md`),
- czy ma nagrania ekranu lub b-roll do konkretnych fragmentów,
- czy zgoda na memy i AI b-roll.

**Wynik końcowy longformu = gotowy plik do wrzucenia na YouTube** (Konrad, 2026-10-03). Przebieg:
1. cięcie → akceptacja (`_tel`),
2. gramatyka ujęć + lista animacji → akceptacja,
3. budowa animacji (partie, QA),
4. **pełny montaż**: CUT + punch-iny + nakładki i pełne ekrany na swoich miejscach + layout ekranu, jeśli jest
   + delikatne SFX pod animacje,
5. **finalny master**: 1920×1080, 30 fps, H.264 CRF 16, AAC 320k, głośność −14 LUFS i TP ≤ −1 dBTP, `+faststart`;
   arkusz kontrolny całego filmu przeczytany,
6. w raporcie gotowe **rozdziały YouTube** (`0:00 …`) z prawdziwymi czasami z finalnego pliku.

Klipy w `Animacje/` zostają jako zapas do jego poprawek, ale domyślnym oddaniem jest pełny film.

**Retencja w longformie**
- Hook z rozmytymi wynikami, odsłanianymi etapami na końcu.
- Callbacki: karta wyników, lejek, minutnik, paragon.
- Pętla „Część 2?”.
- Przypis szczerości.

---

## VSL (16:9, ~3 min), wzór: `examples/vsl_16x9_scenes.py` (34 sceny, zaakceptowane: „dopierdolone”)

- Ten sam styl co longform, ale **gęściej**: co 4–8 s nowa myśl, czyli nowa scena.
- Podział w zaakceptowanej v2: 23 pełne ekrany i 11 nakładek. Pełne ekrany przeszły, bo:
  - każdy to inna, mocna metafora zsynchronizowana ze słowami,
  - między scenami wraca twarz.
- Wcześniejszą wersję z losowymi animacjami, które zasłaniały twarz przez ~80%, odrzucił.
  Gdy masz wątpliwość, daj kartę obok twarzy, nie pełny ekran.
- **Nakładki w 16:9:** biała karta w wolnej ścianie obok głowy. W v2 była to lewa kolumna x 70–670, y 150–800.
  Zawsze sprawdź na klatkach, gdzie jest głowa.
- **Struktura VSL i jak ją wizualizować:**
  - hook z obietnicą (timer 3:00 → 48 h),
  - problem (AI jak Google, czat zamknięty, liczniki 0),
  - zmiana (Dock → AI),
  - autorytet (941 na ekranie blokady),
  - produkt (premiera ikony),
  - mechanizm (demo systemu, pipeline Skróty),
  - ekonomia (Kalkulator, Kalendarz 30 dni),
  - wsparcie (przełącznik aplikacji),
  - bonus (Portfel 800 zł),
  - gwarancja (pieczęć 48 h),
  - dwie przyszłości,
  - CTA (przycisk z kursorem),
  - finał (wielki typ).
- **Start sceny:** nigdy pusta biel. Przesuń in-point tak, żeby treść była od pierwszej klatki, albo zostaw twarz dłużej.

---

## Pion 9:16 (reklamy 60–90 s, rolki), wzór: `examples/ad_9x16_scenes.py` (ANGLE 4: 12 kart + 3 pełne ekrany)

- **Face-first.**
  - Domyślnie karta na klatce piersiowej pod brodą: kolumna x 70–1010 (szer. 940), y ~1000–1560 (wys. do ~520),
    środek ~(540, 1290). Zaokrąglenie 48, cień (0,22, 70, 22).
  - Wejście: skala 92 → 100, uniesienie o 60 px, fade.
- **Pełny ekran tylko dla 3 kluczowych momentów** w ~90 s:
  - mocne pytanie lub zarzut,
  - premiera produktu,
  - „dla wszystkich”.
  - W rolkach 0–1.
- **Czytelność na telefonie:**
  - tekst ≥ 34 px, liczby 90–160 px,
  - jedna rzecz na karcie,
  - karta nie zasłania ust ani oczu.
- **Bezpieczne strefy:** nic ważnego w górnych ~12% i dolnych ~20% (UI TikToka i Reels) ani przy prawej krawędzi.
- **Pierwsze 2 s:** najmocniejszy wizual.
- **Koniec reklamy:** czysty kadr z ofertą (biel, nagłówek, jeden przycisk), jeśli Konrad nie ma własnego CTA na twarzy.
- **Napisy:** styl „reel” z `napisy.md`. Mają nie kolidować z kartami: karta wyżej albo napis nad kartą, sprawdź na arkuszu.
- **Oddanie:** `_MIX.mp4` dla kart, `_NAKLADKA.mov` i `_BROLL.mp4`, plus `NAZWA_FULL.mp4` i `_tel.mp4`.
- **Hooki (ANGLE 1–3):** kilka wersji początku (HOOK1–3) ze wspólnym body. Rób, gdy Konrad przyśle kilka hooków.

---

## Shortform bez animacji (rolki „mój styl”)

Cięcie według `ciecie.md` i napisy „reel” według `napisy.md`. Bez zoomów, grafik i przejść, chyba że poprosi.
Gdy prosi tylko o cięcie, oddaj same cięcia. Napisy rób na osobne zlecenie.
