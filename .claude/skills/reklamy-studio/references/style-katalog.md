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

## Styl 5: „Nie mów / Mów” (viralowa rolka Konrada; nowa wersja „Jeśli chcesz / Musisz”)
- Kod: `projekty/styl5/` (`build_spec5.py`, `engine/overlay5.html`), kompozycja ffmpeg overlay. Bez napisów, bez zoomów.
- Dwie kolumny: nagłówki Inter 800, 78 px, czerwony `#FC0000` (lewa) i zielony `#00E000` (prawa), ciemny cień.
- Pod nimi rzędy słów (Inter 700, 40 px, biel z cieniem) zakryte kolorowymi paskami (60 px wysokości, co 70 px, radius 9).
- Pasek wyjeżdża w bok (lewy w lewo, prawy w prawo), liniowo ok. 2000 px/s (0,2–0,25 s), start 0,12 s przed pierwszym słowem frazy.
- Zmierzone na oryginale 720×1280: kolumny 333 px, paski 40 px co 46,5 px. Tabela zaczyna się tuż pod brodą: jeslito (twarz niżej) nagłówek 1180 / paski 1245;
  jeslito2 (bliższy kadr, zaakceptowany) nagłówek 1030 / paski 1095 (`build_spec5.py OUT tight`).

## Styl 6: „10/10” lista z emoji (format znajomego)
- Kod: `projekty/styl6/` (`build_spec6.py`, `engine/overlay6.html`), fonty `assets/fonts/fmt6.css` (Anton, Poppins 500/600), emoji Noto Color Emoji.
- Bez tytułu u góry (Konrad kazał usunąć białą pigułkę z tytułem). Emoji Apple jako PNG 64 px (`engine/emoji_apple/<kod>.png`, emoji-datasource-apple).
- Siatka 2×5: biała ramka 7 px, radius 22, linie 8 px (z sąsiednich obrysów), komórki półprzezroczyste, romby na skrzyżowaniach.
- Cyfry Poppins 600, 76 px, czarny obrys 3 px; kolory co 40° na kole barw: 2 `#FD0004`, 3 `#F9A901`, 4 `#ADFA01`, 5 `#03FC04`,
  6 `#00FCAC`, 7 `#03A8F8`, 8 `#0500FA`, 9 `#A700FE`, 10 `#FC00A7` (1 biały).
- Na pierwszym słowie punktu cyfra gaśnie w 3 klatki, a emoji pojawia się od razu w pełnym rozmiarze (dosunięte do cięcia, jeśli jest ≤0,3 s wcześniej).
- Napisy (wersja Konrada): Inter Bold 64 px, biel, letter-spacing -50 (-0.05em), czarny cień, zwykła wielkość liter, 2–3 słowa, twarde przełączanie, nad siatką.
- U Konrada: napisy na 1192 px, siatka od 1268 px (usta ok. 53% wysokości).

## Styl 7: „8 things you must keep PRIVATE” (format znajomego, „8 rzeczy”)
- Kod: `projekty/styl7/` (`build_spec7.py`, `engine/overlay7.html`), kompozycja ffmpeg overlay. Konrad dostarcza film już w czarnym kadrze (pasek obrazu w środku).
- Bez tytułu nad paskiem (Konrad kazał usunąć).
- Lista 1.–8. na obrazie (Poppins 500: cyfry 32 px, tekst 27 px, co 68 px, lekki cień; Konrad: o 30% mniejsza niż 1:1). Wszystkie numery od początku, tekst punktu pojawia się twardo na początku zdania.
- Lista po stronie bez twarzy (u Konrada po prawej, x 600). Teksty punktów od Konrada, pierwsza litera wielka (jak w oryginale).

## Styl 8: tierlista (format znajomego „AI SIDE HUSTLES TIER LIST”)
- Kod: `projekty/styl8/` (`build_spec8.py`, `engine/overlay8.html`). Kompozycja: czarne tło, wideo Konrada wycięte 1080×708 (od y≈470) na dole od y 1212, warstwa na wierzchu.
- Góra (do 1212 px): ciemny panel `#29282D→#1D1C21`, biała pigułka z tytułem (Inter 900, czarne + niebieski gradient `#42BDFF→#0092FF`), rzędy S–F
  (etykiety `#FF8A7B #FFC079 #FFDA76 #FEF575 #B9F078 #73EA7B`, paski `#100F12`), tacka z kafelkami-ikonami (emoji Apple na białym kafelku).
- Łapka przenosi kafelek do rzędu (0,6 s, ease), ląduje na słowie z poziomem, obok pojawia się podpis. Tacka się dosuwa.
- Napisy: biała pigułka, Inter 800 40 px czarny, 2–3 słowa. Koniec: pole komentarza, wpisuje się słowo (np. „AI”), klik w „Post” → „Posted ✓”.

## Wybór stylu do nowej reklamy
Konrad zwykle mówi, który styl. Jeśli nie: gadająca głowa + framework/kroki → styl 3; gadająca głowa, ciepło, b-rolle → styl 2;
prosty format z planszami → styl 1; animacja/lektor bez twarzy → styl 4. Nowy wzór = nowy styl (`nowy-styl.md`).
