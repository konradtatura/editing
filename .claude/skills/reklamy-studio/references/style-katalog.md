# Katalog stylów

Każdy styl = breakdown wzoru + `build_specN.py` (treść i czasy) + strona HTML z warstwą (napisy, plansze) + kompozytor.
Wszystkie: 1080×1920, 30 fps, twarde cięcia, zoom tylko na cięciach, CTA z przyciskiem.

## Styl 1: biel + ciemna zieleń (ad8, ad9)
- Kod: `projekty/reklamy_CA/` (`build_spec.py`, `engine/overlay.html`, `engine/compose.py`, `engine/cut.py` do cięcia surowych dubli).
- Kolory: `#0E4D3A` (zieleń), `#1F7A5A` (akcent), `#0A3A2B`, `#0B2A20` (tekst), `#9CF0C8` (mięta), biel.
- Napisy: Inter Bold, biały z miękkim cieniem, 2–4 słowa, ok. 64% wysokości. Słowo-bohater większe, szeryfowa kursywa.
- Zoomy: 100% ↔ 112% naprzemiennie na cięciach.
- Plansze: biało-zielone, pełnoekranowe, 2–4 s: listy kroków, pigułki z ikonami (lucide), licznik (941), karta ceny, tarcza gwarancji.
- Koniec: zielony przycisk CTA. ad9 nagrane w lustrze, więc odbite w poziomie.

## Styl 2: kinowy, ciepły, turkus (ads7, ads10)
- Wzór: reklama „marketr.” (`projekty/styl2/BREAKDOWN.md`).
- Kod: `projekty/styl2/` (`build_spec2.py`, `engine/overlay2.html`, `engine/compose2.py` = kompozytor dla stylów 2 i 3, `engine/pexels.py`, `engine/qa.py`).
- Kolory: tło planszy `#0C1214`, turkus `#9EEBFF / #35C2DA / #0E8FA8`, tekst `#0B1A1E`.
- Obraz: ciepła, lekko wyprana gradacja + winieta (GRADE w `build_spec2.py`).
- Napisy: mały czysty sans (Inter 600, 50 px), słowa dopisują się z rozmyciem. Akcent: Instrument Serif italic w turkusie.
  Cień mocny (Konrad: „ledwo widać”).
- Hero (jedno wielkie słowo, np. „sztuczna inteligencja”, „941”, „17 zł”): Inter 900, gradient **#9DC3F7 → #007A7C per linia**
  (`box-decoration-break: clone`), cień na osobnym wrapperze `.bs` (bo animacja `appear()` nadpisuje `filter`).
- Plansze: ciemne, numerowane kroki „1. 2. 3.”, przycięte koła w turkusowym gradiencie w rogach.
- B-rolle: krótkie przebitki 0,5–1,5 s (Pexels: dłonie na klawiaturze, ekran, laptop) z powolnym push-in.
- Pop-upy: powiadomienie „Nowa sprzedaż +79 zł”, karty e-booków (wachlarz).

## Styl 3: granat + elektryczny indygo, dowody (ads5, ads2)
- Wzór: reklama agencji (`projekty/styl3/BREAKDOWN.md`, z psychologią).
- Kod: `projekty/styl3/` (`build_spec3.py`, `engine/overlay3.html`), kompozycja przez `styl2/engine/compose2.py`.
- Kolory: tło `#05071A`, niebieski `#3B3BFF` / `#5B5BFF`, tekst `#0B0D24`, biel. Ruchome rozmyte plamy światła na planszach.
- Gradacja: chłodna, kontrastowa.
- Napisy: Inter Black, pionowy stos (1–2 słowa na linię), 74 px (po -25%). Słowa-klucze w niebieskim boxie (65 px),
  emocje w Instrument Serif italic pisanej literami (78 px). Wejście z mocnego rozmycia. Górna krawędź stała (capY).
  Markup w skrypcie: `*słowo*` = box, `~słowo~` = kursywa, `_` łączy słowa.
- Plansze (builder `plansza`): nagłówek z wysuwaną linią (`uh`), duże słowa (`bh`), karty-reels (zdjęcie albo **wideo**: `VID()`),
  karty produktu, rzędy z ikonami, równania z licznikiem (10 × 49 zł = 490 zł → 14 700 zł).
- Elementy na twarzy: tracker (lista 1–4 z checkami, zostaje na ekranie), `irows` (✕ bez bycia ekspertem…), CTA box ze strzałką.
- Napis, który padł na planszy, nie wraca po jej zejściu.

## Styl 4: same napisy (ad11, reklamy z animacji AI)
- Wzór: amerykańska reklama z animacjami 3D (Pixar-like), Konrad: „po prostu dodaj napisy w stylu oryginału”.
- Kod: `projekty/styl4/` (`build_spec4.py`, `engine/overlay4.html`), kompozycja zwykłym ffmpeg overlay.
- Font: **Poppins ExtraBold (800)**, WERSALIKI, biały, 64 px, 2–3 słowa (maks. ok. 17 znaków), twarde przełączanie, bez animacji.
- Cień (zaakceptowany): `0 0 5px .95, 0 2px 4px .6, 0 6px 18px .95, 0 12px 52px .82` (czarny).
- Akcent: żółty `#FFE600`, 96 px, 2 wyważone linie, rzadko (hook payoff, „produktach cyfrowych”, „wielokrotnie”, „w 48 godzin”, „17 zł”).
  Markup w skrypcie: `^słowo_słowo^`, `|` = wymuszony podział.
- Wysokość: wszystko na **jednej** wysokości (środek, capY 0.5), bez stref.
- Oba hooki zostają w filmie. Napisy przycięte do cięć scen na granicach hooków (10,733 s, 21,533 s), żeby Konrad mógł sam ciąć.

## Wybór stylu do nowej reklamy
Konrad zwykle mówi, który styl. Jeśli nie: gadająca głowa + framework/kroki → styl 3; gadająca głowa, ciepło, b-rolle → styl 2;
prosty format z planszami → styl 1; animacja/lektor bez twarzy → styl 4. Nowy wzór = nowy styl (`nowy-styl.md`).
