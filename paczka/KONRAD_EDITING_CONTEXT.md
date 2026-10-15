# Konrad: kontekst montażu reklam i rolek (dla Claude Code)

Wrzuć ten plik do projektu jako `CLAUDE.md` albo dołącz go jako kontekst. Zawiera cały warsztat z sesji 2026-10-12/15: proces, zasady Konrada, 9 stylów, komendy, błędy i audio. Kod silników leży w folderze `projekty/` w repo `konradtatura/editing` (albo w `silniki/` w `paczka/reklamy-studio.zip`). Odwołania do `references/*.md` poniżej to sekcje tego samego pliku.

---
name: reklamy-studio
description: "Konrad's paid-ad editing studio for vertical 9:16 Meta ads (Cyfrowy Autopilot and similar). Recreates any reference ad style he sends (breakdown → style engine → captions, zooms on cuts, plansze, b-roll, CTA), then runs QA loops, a Video Review artifact with timestamped notes, music + SFX from free-licensed libraries, and 1080p finals under 30 MB. Four ready styles: styl 1 (white + dark green, Inter, plansze), styl 2 (teal gradient hero words, warm cinematic, b-roll), styl 3 (navy + electric indigo, big stacked captions, proof cards), styl 4 (captions only: Poppins ExtraBold caps for AI-animation ads). Use for: „zmontuj reklamę / adsa”, „taki styl jak w tym filmie”, „odwzoruj ten edit”, „dodaj napisy w stylu oryginału”, „dałem feedback w review”, „muzyka i sfx do reklam”, or when Konrad uploads ads + a reference video."
---

## Reklamy Studio: montaż płatnych reklam w stylu z referencji

Zapis warsztatu z sesji 2026-10-12/13 (reklamy ad8, ad9, ads7, ads10, ads5, ads2, ad11 dla Cyfrowego Autopilota).
**Jak pracujemy:** Konrad wysyła film-wzór („taki styl”) i swoje surowe reklamy. Ja rozkładam wzór na czynniki,
buduję silnik stylu, montuję, sam sprawdzam każdą klatkę, wrzucam do Review, a on zostawia notatki z czasem.
Każda reklama ma inny kąt (angle) i trochę inny montaż.

Konrad jest marketerem, nie montażystą. Piszę po polsku, krótko, bez kodeków i fps. Pytam tylko o treść i gust.
Często jest na telefonie, więc wysyłam gotowe pliki (SendUserFile), a nie ścieżki.

### Najpierw przeczytaj
1. `references/zasady-konrada.md`: jego twarde wymagania i każdy feedback, który już dał. **Złamanie którejś = poprawka.**
2. `references/style-katalog.md`: 9 gotowych stylów (kolory, fonty, rozmiary, ruch, który adsy w jakim stylu).
3. `references/pipeline.md`: komendy krok po kroku (transkrypcja, cięcia, spec, render, kompozycja, QA, eksport, Review).
4. `references/bledy-i-lekcje.md`: błędy, które już raz wyszły. Sprawdź przed oddaniem.
5. `references/nowy-styl.md`: jak odtworzyć nowy styl z filmu-wzoru.
6. `references/audio.md`: muzyka i SFX (licencje, miks, ducking, -14 LUFS).

Kod silników leży w repo w `projekty/` (styl 1: `reklamy_CA/`, style 2–9: `styl2/` … `styl9/`, audio: `audio/`). Strona Video Review: `review/video-review.html`.
W paczce zip (`paczka/reklamy-studio.zip`) ten sam kod jest w `silniki/` obok tego pliku. Ścieżki `projekty/...` = `silniki/...`.

### Przebieg pracy (zawsze w tej kolejności)
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

### Zasady komunikacji
- Na „daj klatkę, powiem czy git”: renderuję JEDNĄ klatkę na trudnym tle i wysyłam obraz, zanim zrobię cały film.
- Gdy Konrad powie „nie rób X” (np. „nie ucinaj hooków, sam to zrobię”): przerywam od razu i usuwam to, co zrobiłem.
- Gdy feedback jest ogólny („gradient dalej niewidoczny”): szukam przyczyny w kodzie, nie tylko podkręcam wartości.
- Podsumowanie po robocie: co poprawione per film, krótko, po polsku.

## Zasady Konrada (z feedbacku, 2026-10-12/13)

Każdy punkt to uwaga, którą Konrad już raz zgłosił. Nie powtarzamy.

### Ogólne
- Wszystko po polsku (napisy, plansze, CTA). Rynek polski.
- Liczba e-booków w najlepszym dniu: **941** (nie 947). Cena Cyfrowego Autopilota: **17 zł**. „48 godzin”, „ponad 3 lata”.
- Powiadomienie o sprzedaży produktu klienta pokazuje **+79 zł** (nie 17 zł, bo 17 zł to cena CA).
- CTA: „Kliknij poniżej” albo „Kliknij przycisk poniżej”, przycisk **ze strzałką w dół na końcu**.
- Animacje nie za krótkie, nie za dużo i nie „AI-owe”. Mniej, ale dopracowane.
- Bez muzyki i SFX, dopóki nie powie inaczej. Od 2026-10-13: muzyka i SFX z darmowych bibliotek z licencją na reklamy (`audio.md`).

### Cięcia i zoomy (najczęstsze uwagi)
- Zoom zmienia się **tylko na cięciu** w jego nagraniu. Nigdy w środku ujęcia, nigdy kilka klatek po cięciu.
- Plansza startuje **dokładnie na klatce cięcia** (inaczej widać, jak tło zmienia się pod wejściem planszy).
- Znajdź każdą klatkę cięcia. Konrad podaje liczbę cięć, więc zawsze się zgadzam z jego liczbą (dodaję `extra_cuts`, jeśli detektor coś przeoczy).
- Ostatnie ujęcie z CTA: zoom 100%, żeby napis „Kliknij poniżej” nie wchodził na usta.

### Przejścia
- **Bez zanikania (opacity fade-out).** Plansza ucina się twardo na cięciu.
- Bez mignięcia twarzy między dwiema planszami. Plansze jedna po drugiej, twarde cięcie.

### Usta i twarz
- Nic nie może zasłaniać ust: ikonki, pigułki, karty „17 zł”, napisy. Przesuwaj niżej, pod brodę.
- Styl 3 / ads2: napisy na ok. 60% wysokości (capY 0.6), a listy (tracker, „bez…”) jeszcze niżej, żeby się nie zderzały.

### Napisy
- Wszystkie napisy w filmie na **jednej, stałej wysokości**. Nie przesuwaj ich per scena (nawet jeśli coś zasłaniają).
- Napisy muszą być czytelne na każdym tle: mocny cień. Ad11 (styl 4) przeszedł dopiero przy cieniu ok. 1,8× bazowego (+40%, potem +30%).
- Styl 3: napisy były za duże, zmniejszone o 25% (74/65/78 px).
- Niebieskie boxy obok siebie łączą się w jeden box (nie dwa nachodzące).
- Napis nie może wrócić po planszy, jeśli jego słowa padły już na planszy (np. „14 700 miesięcznie”).
- Słowo-akcent na planszy ma być widoczne odpowiednio długo (nie znikać od razu po wejściu, np. „cyfrowe”).

### Gradient (styl 2)
- Gradient dużych słów: **#9DC3F7 (góra) → #007A7C (dół), w każdej linii osobno**, z dużym ciemnym cieniem.
  Musi być wyraźnie widoczny na niebieskiej koszulce.

### B-rolle i materiały
- Jeśli Konrad wrzuca własne klipy (aislop1–3, aikicthen), wstawiam dokładnie je, nie stock.
- W kartach-reelach na planszach puszczam wideo (sekwencja klatek), nie zdjęcie.
- Stock z Pexels (klucz API w `scratchpad/.pexels.env`, nigdy w repo).

### Czego nie robić bez pytania
- Nie tnij hooków na osobne wersje, Konrad robi to sam. Pilnuj tylko, żeby żaden napis nie przechodził przez cięcie między hookami.
- Nie ruszaj zaakceptowanych reklam przy okazji innych poprawek.

## Katalog stylów

Każdy styl = breakdown wzoru + `build_specN.py` (treść i czasy) + strona HTML z warstwą (napisy, plansze) + kompozytor.
Wszystkie: 1080×1920, 30 fps, twarde cięcia, zoom tylko na cięciach, CTA z przyciskiem.

### Styl 1: biel + ciemna zieleń (ad8, ad9)
- Kod: `projekty/reklamy_CA/` (`build_spec.py`, `engine/overlay.html`, `engine/compose.py`, `engine/cut.py` do cięcia surowych dubli).
- Kolory: `#0E4D3A` (zieleń), `#1F7A5A` (akcent), `#0A3A2B`, `#0B2A20` (tekst), `#9CF0C8` (mięta), biel.
- Napisy: Inter Bold, biały z miękkim cieniem, 2–4 słowa, ok. 64% wysokości. Słowo-bohater większe, szeryfowa kursywa.
- Zoomy: 100% ↔ 112% naprzemiennie na cięciach.
- Plansze: biało-zielone, pełnoekranowe, 2–4 s: listy kroków, pigułki z ikonami (lucide), licznik (941), karta ceny, tarcza gwarancji.
- Koniec: zielony przycisk CTA. ad9 nagrane w lustrze, więc odbite w poziomie.

### Styl 2: kinowy, ciepły, turkus (ads7, ads10)
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

### Styl 3: granat + elektryczny indygo, dowody (ads5, ads2)
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

### Styl 4: same napisy (ad11, reklamy z animacji AI)
- Wzór: amerykańska reklama z animacjami 3D (Pixar-like), Konrad: „po prostu dodaj napisy w stylu oryginału”.
- Kod: `projekty/styl4/` (`build_spec4.py`, `engine/overlay4.html`), kompozycja zwykłym ffmpeg overlay.
- Font: **Poppins ExtraBold (800)**, WERSALIKI, biały, 64 px, 2–3 słowa (maks. ok. 17 znaków), twarde przełączanie, bez animacji.
- Cień (zaakceptowany): `0 0 5px .95, 0 2px 4px .6, 0 6px 18px .95, 0 12px 52px .82` (czarny).
- Akcent: żółty `#FFE600`, 96 px, 2 wyważone linie, rzadko (hook payoff, „produktach cyfrowych”, „wielokrotnie”, „w 48 godzin”, „17 zł”).
  Markup w skrypcie: `^słowo_słowo^`, `|` = wymuszony podział.
- Wysokość: wszystko na **jednej** wysokości (środek, capY 0.5), bez stref.
- Oba hooki zostają w filmie. Napisy przycięte do cięć scen na granicach hooków (10,733 s, 21,533 s), żeby Konrad mógł sam ciąć.

### Styl 5: „Nie mów / Mów” (viralowa rolka Konrada; nowa wersja „Jeśli chcesz / Musisz”)
- Kod: `projekty/styl5/` (`build_spec5.py`, `engine/overlay5.html`), kompozycja ffmpeg overlay. Bez napisów, bez zoomów.
- Dwie kolumny: nagłówki Inter 800, 78 px, czerwony `#FC0000` (lewa) i zielony `#00E000` (prawa), ciemny cień.
- Pod nimi rzędy słów (Inter 700, 40 px, biel z cieniem) zakryte kolorowymi paskami (60 px wysokości, co 70 px, radius 9).
- Pasek wyjeżdża w bok (lewy w lewo, prawy w prawo), liniowo ok. 2000 px/s (0,2–0,25 s), start 0,12 s przed pierwszym słowem frazy.
- Zmierzone na oryginale 720×1280: kolumny 333 px, paski 40 px co 46,5 px. Tabela zaczyna się tuż pod brodą: jeslito (twarz niżej) nagłówek 1180 / paski 1245;
  jeslito2 (bliższy kadr, zaakceptowany) nagłówek 1030 / paski 1095 (`build_spec5.py OUT tight`).

### Styl 6: „10/10” lista z emoji (format znajomego)
- Kod: `projekty/styl6/` (`build_spec6.py`, `engine/overlay6.html`), fonty `assets/fonts/fmt6.css` (Anton, Poppins 500/600), emoji Noto Color Emoji.
- Bez tytułu u góry (Konrad kazał usunąć białą pigułkę z tytułem). Emoji Apple jako PNG 64 px (`engine/emoji_apple/<kod>.png`, emoji-datasource-apple).
- Siatka 2×5: biała ramka 7 px, radius 22, linie 8 px (z sąsiednich obrysów), komórki półprzezroczyste, romby na skrzyżowaniach.
- Cyfry Poppins 600, 76 px, czarny obrys 3 px; kolory co 40° na kole barw: 2 `#FD0004`, 3 `#F9A901`, 4 `#ADFA01`, 5 `#03FC04`,
  6 `#00FCAC`, 7 `#03A8F8`, 8 `#0500FA`, 9 `#A700FE`, 10 `#FC00A7` (1 biały).
- Na pierwszym słowie punktu cyfra gaśnie w 3 klatki, a emoji pojawia się od razu w pełnym rozmiarze (dosunięte do cięcia, jeśli jest ≤0,3 s wcześniej).
- Napisy (wersja Konrada): Inter Bold 64 px, biel, letter-spacing -50 (-0.05em), czarny cień, zwykła wielkość liter, 2–3 słowa, twarde przełączanie, nad siatką.
- U Konrada: napisy na 1192 px, siatka od 1268 px (usta ok. 53% wysokości).

### Styl 7: „8 things you must keep PRIVATE” (format znajomego, „8 rzeczy”)
- Kod: `projekty/styl7/` (`build_spec7.py`, `engine/overlay7.html`), kompozycja ffmpeg overlay. Konrad dostarcza film już w czarnym kadrze (pasek obrazu w środku).
- Bez tytułu nad paskiem (Konrad kazał usunąć).
- Lista 1.–8. na obrazie (Poppins 500: cyfry 32 px, tekst 27 px, co 68 px, lekki cień; Konrad: o 30% mniejsza niż 1:1). Wszystkie numery od początku, tekst punktu pojawia się twardo na początku zdania.
- Lista po stronie bez twarzy (u Konrada po prawej, x 600). Teksty punktów od Konrada, pierwsza litera wielka (jak w oryginale).

### Styl 8: tierlista (format znajomego „AI SIDE HUSTLES TIER LIST”)
- Kod: `projekty/styl8/`. Kompozycja: ciemne tło na całym kadrze (ffmpeg), wideo Konrada w zaokrąglonym kadrze 1032×560 (radius 40, maska PNG) na x 24, y 1150, wyżej niż dół ekranu (opis i konto na IG zasłaniają dół). Napis w połowie między tacką a kamerką (pigułka top 1054). Face tracking w kadrze: `facecrop.py IN OUT 1032 560 0.53` (YuNet, wygładzanie 0.6 s + martwa strefa 3%).
- Góra (do 1212 px): ciemny panel `#29282D→#1D1C21`, biała pigułka z tytułem (Inter 900, czarne + niebieski gradient `#42BDFF→#0092FF`), rzędy S–F
  (etykiety `#FF8A7B #FFC079 #FFDA76 #FEF575 #B9F078 #73EA7B`, paski `#100F12`), tacka z kafelkami-ikonami (emoji Apple na białym kafelku).
- Łapka przenosi kafelek do rzędu (0,6 s, ease), ląduje na słowie z poziomem, obok pojawia się podpis. Tacka się dosuwa.
- Napisy: biała pigułka, Inter 800 40 px czarny, 2–3 słowa. Koniec: pole komentarza, wpisuje się słowo (np. „AI”), klik w „Post” → „Posted ✓”.

### Styl 9: LEGO AI (reklama znajomego „Walmart”, ailego12)
- Kod: `projekty/styl9/` (`build_spec9.py WORKDIR NAME`, `engine/overlay9.html`, `compose9.py`). Font `assets/fonts/montserrat.css`.
- Napisy: Montserrat 700, 70 px, biały, czarny obrys 3 px + cień `0 0 4px .9, 0 3px 8px 1, 0 6px 30px .7` (Konrad: +50–60% vs v1), 1–2 słowa, twarde przełączanie, jedna wysokość (capY 0.645).
  Krótkie kawałki (<0,3 s) łączą się z sąsiadem, „79 zł” zawsze razem. Napisy nie przechodzą przez cięcia hooków (`HOOK_CUTS`).
  `hideCaps`: wyłącza napisy tam, gdzie film ma już wtopiony tekst (u ailego12 scena 941).
- Efekty (tylko tam, gdzie film Konrada nie ma już grafiki): czerwona ramka rysowana wokół elementu UI (`box`, `#FF2B2B`, 0,35 s),
  deszcz pieniędzy (`rain`, emoji Noto, nie PNG), wybuch pieniędzy z punktu (`burst`), żółta 3D strzałka w dół przy CTA (`arrow`).
- Rozmycie wejścia 0,27 s na cięciach zmiany sekcji (`blurCuts`, w `compose9.py`, gblur).
- ailego12: deszcz przy „tysięcy złotych”, ramki na „link w bio” i „79 zł”, monety na „wielokrotnie”, wybuch na 941, strzałka na „Kliknij poniżej”.

### Wybór stylu do nowej reklamy
Konrad zwykle mówi, który styl. Jeśli nie: gadająca głowa + framework/kroki → styl 3; gadająca głowa, ciepło, b-rolle → styl 2;
prosty format z planszami → styl 1; animacja/lektor bez twarzy → styl 4 (same napisy) albo styl 9 (napisy + efekty jak w reklamie LEGO). Nowy wzór = nowy styl (`nowy-styl.md`).

## Pipeline: komendy krok po kroku

`W` = katalog roboczy (scratchpad). `P` = `projekty/` w repo. Media nigdy nie idą do repo, tylko kod.

### 0. Narzędzia (jednorazowo)
- Python: `faster-whisper`, `numpy`, `opencv-python`; ffmpeg; Node + `playwright` (Chromium).
- `render.mjs` ładuje playwright przez `createRequire` z globalnych node_modules (`PW_ROOT`, domyślnie `/opt/node22/lib/node_modules/`).
  Na komputerze Konrada: `npm i -g playwright && npx playwright install chromium`, potem `PW_ROOT=$(npm root -g)/`.
- Fonty są lokalnie w `P/reklamy_CA/engine/assets/fonts/` (Inter, Instrument Serif: `g.css`; Poppins: `poppins.css`). Ikony: `assets/icons/*.svg` (lucide).

### 1. Materiały z Drive
```bash
gdown --folder --json <URL_folderu>          # lista plików i ID (bez pobierania)
gdown -O ads2.mp4 <ID>                         # pobranie jednego pliku
```

### 2. Wzór
- Arkusz klatek: `ffmpeg -i REF.mp4 -vf "fps=1/2,scale=240:-1,drawtext=text='%{pts\:hms}':...,tile=8x4" ref_%02d.jpg`
- Animacja napisów: `ffmpeg -ss T -i REF.mp4 -t 1.2 -vf "fps=10,crop=...,tile=2x6"` (widać, czy słowa wchodzą, czy przełączają się twardo).
- Detal: crop w pełnej rozdzielczości, żeby odczytać font, cień i rozmiar.

### 3. Cięcia i transkrypcja
```bash
python3 P/reklamy_CA/engine/cuts.py ads2.mp4 > cuts.json      # czasy pierwszej klatki nowego ujęcia
python3 tools/tr.py ads2.mp4 tr_ads2 medium                    # -> tr_ads2.json (słowa z czasami) + .txt
```
Surowe duble (Teleprompter) tnie `P/reklamy_CA/engine/cut.py TAKES.json OUT.mp4` (flagi „x” = dokładny start, „y” = koniec nie później niż).

### 4. Spec
`python3 P/stylN/build_specN.py W ...` → `W/specN_<ad>.json`. W pliku builda:
- `FIX…` = tekst ze skryptu z markupem akcentów (nakładany na czasy whispera),
- `IT…` = lista plansz i elementów z czasami (t0/t1 na cięciach!),
- `make(..., extra_cuts=(...), capY=...)`.

### 5. Render warstwy i kompozycja
```bash
node P/reklamy_CA/engine/render.mjs SPEC.json FRAMES/ --page P/styl3/engine/overlay3.html --par 3
node ... --from 44.9 --to 62.1          # tylko zakres (po małej poprawce)
node ... --frames 13.3                   # jedna klatka do akceptacji
python3 P/styl2/engine/compose2.py SPEC.json FRAMES/ OUT.mp4        # styl 2 i 3
python3 P/reklamy_CA/engine/compose.py SPEC.json FRAMES/ OUT.mp4    # styl 1
ffmpeg -i src.mp4 -framerate 30 -i FRAMES/f_%05d.png -filter_complex "[0][1]overlay=format=auto:eof_action=pass,format=yuv420p" ...  # styl 4
```
Komunikaty „Broken pipe” przy kompozycji to normalne zamykanie dekoderów b-rolli.
Długie joby puszczaj w tle (`nohup bash job.sh > job.log &`) i czekaj na „ALLDONE”, nie odpalaj enkodowania na pliku, który się jeszcze komponuje.

### 6. QA
```bash
python3 P/styl2/engine/qa.py SPEC.json OUT.mp4 qa      # pary przed|po przy każdym cięciu i krawędzi elementu
ffmpeg -i OUT.mp4 -vf "fps=1,scale=216:384,drawtext=...,tile=10x4" sheet_%02d.jpg   # cały film co 1 s (gęściej: fps=2)
```
Oglądam każdy arkusz (Read obrazu). Checklistę mam w `bledy-i-lekcje.md`.

### 7. Eksport
Dwuprzebiegowo z wyliczonym bitrate: `vb = MB*8192/dur - 128` kb/s.
- Review: 720:1280, ok. 13,5–14 MB.
- FINAL: 1080:1920, 27–28,5 MB (limit 30 MB), audio AAC 128k, `-movflags +faststart`.

### 8. Review (artefakt Video Review)
- Upload: `Artifact` z `asset: true` (kilka plików naraz: `file_paths`).
- Baza: kolekcja `videos` (title, asset, url, order, ver, dur) → `update` z `if_version`; nowa reklama = `set`.
- Notatki: kolekcja `notes` (video, t, x, y, text, status). Czytam `query status == open`, poprawiam, odpowiadam
  (`reply`) i ustawiam `status: done` jednym `batch`.

### 9. Repo
Kod i specy (`build_spec*.py`, `engine/*`, `zones`, `cues`) commit + push na branch sesji. Media, klucze (Pexels) nigdy.

## Błędy i lekcje (sprawdź przed oddaniem)

### Checklista QA (każda reklama, każda wersja)
- [ ] Zoom zmienia się tylko na cięciu: para klatek przed/po każdym cięciu.
- [ ] Plansze zaczynają się i kończą na cięciu, twardo, bez fade i bez mignięcia twarzy.
- [ ] Nic nie zasłania ust (napisy, ikony, karty, listy). CTA na ujęciu 100%.
- [ ] Napisy na jednej wysokości. Nie zderzają się z trackerem, listami ani CTA.
- [ ] Żadna plansza nie startuje pusta: jest nagłówek albo pierwszy element od pierwszej klatki.
- [ ] Akcenty: boxy nie nachodzą na siebie, kursywa nie wchodzi w linię wyżej, słowo-akcent widoczne wystarczająco długo.
- [ ] Liczby i fakty: 941, 17 zł, +79 zł w powiadomieniu, 48 h. Bez zmyślonych wyników.
- [ ] Napis nie wraca po planszy z treścią, która na niej padła.
- [ ] Ostatnia klatka: CTA ze strzałką, nic ucięte.
- [ ] Rozmiar FINAL < 30 MB, długość = oryginał, dźwięk zsynchronizowany.

### Błędy techniczne, które już były
| Objaw | Przyczyna | Naprawa |
|---|---|---|
| Cień pod gradientem „nie działa” | `appear()` ustawia `element.style.filter` (blur→none) i kasuje CSS `filter: drop-shadow` | cień na osobnym elemencie-wrapperze (`.bs`) |
| Gradient „dziwny” przy 2 liniach | gradient na całym bloku, więc każda linia ma inny kolor | inline span + `box-decoration-break: clone` |
| Biała obwódka gradientu robi kreski w literach | `-webkit-text-stroke` przy ujemnym letter-spacing rysuje kontury nachodzących glifów | bez strokea, tylko cień |
| Stary zoom kilka klatek po cięciu | detektor nie złapał cięcia | `extra_cuts`, porównaj liczbę cięć z Konradem |
| Dwa niebieskie boxy nachodzą | każde słowo `h==1` osobnym spanem | sąsiednie słowa h=1 w jeden box |
| Napisy skaczą góra/dół | centrowanie bloku o zmiennej liczbie linii | stała górna krawędź (`top = capY*H`) |
| compose2: NoneType terminate | dekoder b-rolla zamknięty dwa razy | `bdec[k] = False` po terminate i `if not bdec[k]: continue` |
| Wideo w karcie nie gra | `<img>` w Playwright | sekwencja JPG 30 fps, `seek()` podmienia `src` i zwraca Promise z `decode()` |
| PNG bez alfy psuje kompozycję | screenshot bez `omitBackground` | traktuj jako nieprzezroczyste / zawsze `omitBackground: true` |
| cut.py OOM | jeden filter_complex na wszystkie segmenty | enkoduj segmenty osobno + concat |
| Fade audio w złym miejscu | `-ss` na wejściu przesuwa czasy filtrów | trim/atrim w filtrze |
| Enkod uszkodzony („moov atom not found”) | enkodowanie pliku, który się jeszcze komponował | czekaj na „wrote”/ALLDONE |
| Pętla czekania nie kończy się | `pgrep -f` łapie własną komendę | czekaj na plik wynikowy / marker w logu |
| Napis wisi na granicy hooków | blok napisów przechodzi przez cięcie sceny | przytnij t0/t1 bloków do cięć hooków |

### Lekcje z feedbacku
- Konrad patrzy na telefonie: czytelność > subtelność. Cienie mocniej, niż wydaje się potrzebne.
- „Dalej niewidoczne” zwykle oznacza bug, a nie za słabe wartości. Najpierw sprawdź, czy efekt w ogóle się renderuje (pojedyncza klatka, crop 1:1).
- Jedna klatka do akceptacji przed pełnym renderem oszczędza 20 minut.
- Po każdym przesunięciu jednego elementu sprawdź, w co teraz wchodzi (napisy niżej → zderzenie z trackerem).

## Nowy styl z filmu-wzoru

Konrad: „taki styl, tekst, zoomy, animacje (nie giga dużo, ale ważne)”. Cel: wierne odwzorowanie formuły, nie kopia 1:1 treści.

### 1. Obejrzyj jak montażysta
- Arkusz co 2 s całego wzoru + mikroskop pierwszych 10 s (hook) co 0,1 s.
- Policz: cięcia, średnia długość ujęcia, % czasu z twarzą vs plansze/b-roll, ile elementów na twarzy.
- Napisy: font (crop 1:1), wielkość względem szerokości kadru, wersaliki, kolor, cień/obrys, ile słów naraz,
  czy słowa wchodzą animacją czy przełączają się twardo, wysokość na ekranie, akcenty (kolor, kursywa, box).
- Plansze: tło, nagłówki, karty, ikony, liczniki, jak wchodzą i wychodzą.
- Kolor obrazu (gradacja), przejścia, dźwięk (muzyka cicho czy głośno, SFX gdzie).
- Psychologia: po co jest każdy element (autorytet, otwarta pętla, pattern interrupt, odwrócenie ryzyka).

### 2. Zapisz breakdown
`projekty/stylN/BREAKDOWN.md` z sekcjami: Formuła, Liczby, Napisy, Plansze, Elementy specjalne, Kolor, Dźwięk, Psychologia,
Przełożenie na Konrada (kolory i fonty pod markę, co od niego potrzeba).

### 3. Zbuduj silnik
- Skopiuj najbliższy styl (`overlayN.html` + `build_specN.py`) i zmień tylko to, co inne. Kontrakt strony: `window.init(spec)`,
  `window.seek(t)` (może zwrócić Promise), przezroczyste tło, 1080×1920.
- Fonty lokalnie (`assets/fonts`, pobierz woff2 z Google Fonts, podzbiory latin + latin-ext dla polskich znaków).
- Wyrenderuj 3–6 klatek na trudnych tłach i porównaj obok wzoru, zanim zrobisz cały film.

### 4. Pierwszy film
Pełny render → QA (2 przejścia) → Review → FINAL. Do opisu dla Konrada dodaj, co przełożyłeś ze wzoru i dlaczego.

### 5. Dopisz styl do `style-katalog.md` i zasady z feedbacku do `zasady-konrada.md`.

## Muzyka i SFX

Konrad nie ma Artlist ani Epidemic, więc muzykę i SFX biorę z darmowej biblioteki z licencją na reklamy.

### Źródło: Mixkit
- Licencja Mixkit Free: „commercial projects (YouTube videos, social media marketing, online ads…)”, bez podawania autora.
  Nie dotyczy TV, radia, gier ani nośników fizycznych. Każdy plik musi mieć „Free License” (`#musicFree` / SFX free), nie „Restricted”.
- Strony mixkit.co blokują curl (Cloudflare), więc listy pobieram headless Chromium (`playwright`), a pliki wprost z `assets.mixkit.co`:
  - muzyka: `https://assets.mixkit.co/music/<id>/<id>.mp3`
  - SFX: `https://assets.mixkit.co/active_storage/sfx/<id>/<id>-preview.mp3`
- Alternatywa tylko na FB/IG: Meta Sound Collection (licencja tylko w obrębie platform Mety).
- Pixabay i Freesound z serwera dają 403.

### Użyte pliki (ID)
- Muzyka: 140 „Cyberpunk City” (ad11, kosmos/tech, 1:40), 134 „Deep Techno Ambience”, 175 „Digital Clouds”, 184 „Vastness”.
- SFX: whoosh 1492 / 1490 / 1489, sweep 166, pop_whoosh 3005, pop_msg 2354, click_select 1109, click_tech 3124, coins 1993, coin_prize 1999.

### Miks: `projekty/audio/mix.py CUES.json IN.mp4 OUT.mp4`
- Muzyka: gain ok. -21 dB przy utworze -11 LUFS i głosie -18 LUFS (podkład ok. 14 LU pod głosem), sidechain ducking pod głos,
  fade-in 0,4 s, fade-out 2 s.
- SFX: `peak: true` ustawia najgłośniejszy moment dźwięku dokładnie na czasie cue (whoosh na cięciu).
- Wyjście: loudnorm -14 LUFS / -1,5 dBTP, AAC 128k, wideo kopiowane bez ponownego kodowania.
- Cue sheet per reklama: `projekty/audio/cues_<ad>.py`. Ad11: whoosh -17 dB na cięciach scen (najwyżej 1 na sekundę),
  pop -12 dB na żółtych akcentach, monety przy 941, powiadomienie przy „Automatycznie”, „ding” przy 17 zł, klik przy „Kliknij przycisk”.

### Zasady
- SFX oszczędnie: ma brzmieć dopracowanie, nie efekciarsko.
- Na serwerze nie da się odsłuchać, więc zawsze wysyłam próbkę do akceptacji klimatu i głośności, zanim zrobię wszystkie reklamy.
- Klimat per styl: styl 3 spokojny/premium, styl 2 ciepły i energiczny, styl 4 (animacje) elektroniczny/kosmiczny.

## Historia: co zostało zrobione (2026-10-12 → 15)

| Film | Styl | Najważniejsze decyzje Konrada |
|---|---|---|
| ad8 „Kawa / 48 h”, ad9 „ChatGPT nie zapłaci” | 1 (biel + zieleń) | 34 notatki: zoom tylko na cięciach, bez fade, nic na ustach, CTA na 100%, ad9 odbite (lustro) |
| ads7, ads10 | 2 (turkus, kinowy) | mocniejszy cień napisów, gradient #9DC3F7→#007A7C per linia (bug: appear() kasował cień), +79 zł w powiadomieniu |
| ads5, ads2 | 3 (granat + indygo) | napisy -25%, strzałka w CTA, klipy z Drive (aislop1-3, aikicthen) jako wideo w kartach, ads2 napisy na 60% wysokości |
| ad11 (animacja AI) | 4 (Poppins caps) | cień +40%, potem +30%; wszystkie napisy na jednej wysokości; oba hooki zostają (Konrad tnie sam); próbka muzyki Mixkit 140 + SFX |
| „Jeśli chcesz / Musisz” (jeslito, jeslito2) | 5 (Nie mów / Mów) | 1:1 z viralu; tabela tuż pod brodą |
| „10/10 nawyków” (1010) | 6 (siatka emoji) | emoji Apple, Inter Bold -50 z czarnym cieniem, bez tytułu |
| „8 rzeczy” | 7 (lista) | lista po prawej, -30%, bez tytułu |
| „Tierlista AI biznesów” | 8 (tierlista) | kamerka w zaokrąglonym kadrze wyżej (IG zasłania dół), napis w połowie między tacką a kamerką, face tracking |
| AI LEGO 12 „Postacie AI” (ailego12) | 9 (LEGO AI: napisy + efekty) | efekty z oryginału tylko tam, gdzie film nie ma grafiki; napisy wyłączone na scenie 941; cień napisów +50–60% (v2); muzyka i SFX później |

Narzędzia sesji: Video Review (artefakt z notatkami z czasem; od 2026-10-15 także wersje, tempo 0,5–2×, klatka po klatce, „Wyślij poprawki” i „Zatwierdź wersję”), Drive przez `gdown`, Pexels (klucz tylko lokalnie, nigdy w repo), Mixkit przez headless Chromium.

---

## Załącznik A: dokumenty projektowe (breakdowny wzorów, plany)


### `projekty/reklamy_CA/PLAN.md`

### Reklamy Cyfrowy Autopilot: ad8 i ad9 (plan do akceptacji)

Styl ze wzorów (3 reklamy referencyjne): twarz przez większość czasu, napisy 2–4 słowa, punch-in zoomy co zdanie,
krótkie pełnoekranowe plansze z ikonami/pigułkami/listami, SFX pod każdą zmianą, CTA-przycisk na końcu.
Kolory: biel `#FFFFFF` + ciemna zieleń `#0E4D3A` (akcent jaśniejszy `#1F7A5A`). Bez muzyki.

#### Wspólne dla obu
- Napisy: Inter Bold, biały z miękkim cieniem, 2–4 słowa, na wysokości klatki (ok. 64% wysokości), bez przerw.
  Słowo-bohater (liczby, puenty) większe, w kursywie szeryfowej. Na planszach tekst ciemnozielony.
- Zoomy: co zdanie 100% ↔ 112% (twarde punch-iny), po planszy settle 106→100%.
- Plansze: biało-zielone, 2–4 s każda, wejście/wyjście szybki zoom+blur + whoosh.
- SFX: whoosh (plansze), pop (pigułki/punkty listy), tick (licznik), bas (duża liczba / cena).
- Koniec: zielony przycisk pod napisami od CTA do końca.

#### ad8 (77 s)
| # | czas | słowa | co pokazujemy |
|---|---|---|---|
| 1 | 0,0–3,0 | „Za cenę jednej kawy… w 48 godzin” | PEŁNY: kubek kawy → okrąg 48 h wypełnia się na zielono |
| 2 | 9,6–13,8 | „prawdziwy produkt cyfrowy, strona sprzedażowa, wszystko” | PEŁNY: 3 pigułki wjeżdżają na słowo |
| 3 | 13,9–20,2 | „kolejny kurs… 10 godzin” | twarz + tekst „10 godzin” przekreślony |
| 4 | 20,3–23,0 | „Po pierwsze, pomysł” | PEŁNY: lista kroków, punkt 1 |
| 5 | 27,1–32,0 | „Po drugie… poradnik, planner, szablony, PDF” | PEŁNY: punkt 2 + 4 ikonki na słowo |
| 6 | 32,3–35,5 | „Po trzecie… strona sprzedażowa” | PEŁNY: punkt 3 (mini makieta strony) |
| 7 | 37,0–40,0 | „po czwarte… treści i reklamy” | PEŁNY: punkt 4, lista kompletna |
| 8 | 40,1–43,4 | „Pomysł, produkt, strona, marketing” | PEŁNY: 4 pigułki połączone linią z ikoną AI |
| 9 | 43,6–53,7 | „cały proces… coś, czego dzisiaj nie masz” | twarz, zoomy, bohaterowie „48 godzin”, „własny produkt” |
| 10 | 53,7–58,4 | „ponad 3 lata… 947 e-booków” | PEŁNY: licznik 0 → liczba „w jeden dzień” |
| 11 | 58,5–60,7 | „stworzyłem Cyfrowy Autopilot” | PEŁNY: nazwa produktu |
| 12 | 60,8–63,7 | „tylko za 17 zł” | twarz + duże „17 zł” obok kubka kawy |
| 13 | 63,8–68,7 | „gwarancja… zwracam 100%” | karta na klatce: tarcza „100% zwrotu · 48 h” |
| 14 | 68,8–koniec | „kliknij poniżej…” | przycisk CTA |

#### ad9 (67 s) – nagranie jest w lustrze (napis na koszulce od tyłu)
| # | czas | słowa | co pokazujemy |
|---|---|---|---|
| 1 | 0,0–2,1 | „…ChatGPT… ani złotówki” | PEŁNY: ikona ChatGPT + „0 zł” |
| 2 | 2,2–7,6 | „najlepsze prompty, narzędzia AI, 5–10 h dziennie” | PEŁNY: lista 3 pigułek na słowo |
| 3 | 7,7–11,6 | „…nadal nie masz biznesu” | twarz; bohater „nie masz biznesu” |
| 4 | 14,5–19,2 | „nie AI płaci… płacą ludzie… za rozwiązanie problemu” | PEŁNY: ikony ludzi + monety → „problem rozwiązany” |
| 5 | 19,3–22,4 | „planer budżetu” | PEŁNY: ikona planera |
| 6 | 22,5–25,2 | „proste przepisy” | twarz + karta na klatce z ikoną |
| 7 | 25,2–29,7 | „szablon CV” | PEŁNY: ikona CV (ten sam styl co #5, callback) |
| 8 | 31,7–37,8 | „AI pomoże… bez pisania od zera, bez twarzy” | twarz + 2 ptaszki obok głowy |
| 9 | 38,0–40,0 | „zbudowałem Cyfrowy Autopilot” | PEŁNY: nazwa produktu |
| 10 | 40,1–45,7 | „pomysł, stworzenie, strona sprzedażowa” | PEŁNY: lista buduje się na słowo |
| 11 | 45,8–49,5 | „jak zacząć sprzedawać” | twarz + karta, punkt 4 |
| 12 | 49,5–54,7 | „w 48 h od pustego ChatGPT do produktu” | PEŁNY: pusty czat → karta gotowego produktu |
| 13 | 54,9–60,3 | „17 zł… mniej niż kawa” | twarz + „17 zł” i kubek |
| 14 | 60,5–koniec | „kliknij przycisk poniżej…” | przycisk CTA |

#### Do sprawdzenia
- ad8 mówi „947 e-booków”, a fakt marki to **941**. Na ekranie daję 941.
- ad9 pierwsze zdanie ASR słabe („Trzeba GPT nie zapłacić ani złotówki”) – potwierdź brzmienie.
- ad9 w lustrze: proponuję odbić poziomo (koszulka czytelna).
- Tekst na przycisku CTA.


### `projekty/styl2/BREAKDOWN.md`

### Styl 2: breakdown wzoru (reklama „marketr.”, 51 s, 720×1280)

**Formuła:** kinowa reklama gadającej głowy. Ciepły, miękki obraz, dwa ujęcia kamery (szeroki ↔ bliski),
krótkie b-rolle przebitki, ciemne plansze z numerowanymi krokami i koralowym akcentem, karta marki na końcu.

#### Liczby
- 26 cięć w 51 s. W hooku (0–13 s) cięcie co ~0,7 s, potem co 2–9 s.
- B-rolle: ok. 6 przebitek po 0,5–1,5 s (dłonie na klawiaturze, odbicie ekranu w okularach, ekran laptopa, laptop z boku, dłonie przy stole).
- Plansze pełnoekranowe: 2 (kroki „1.” i „2.”), po 2–3 s. Karta marki na końcu: 3 s.
- Elementy na twarzy: wachlarz produktów (statics) wjeżdżający od lewej (ok. 2 s) i 3 szklane kafelki „1 2 3” (ok. 1,5 s).

#### Napisy
- Mały, czysty sans (DM Sans / Inter Medium, ok. 45 px przy 1080), biały z miękkim cieniem, na wysokości klatki.
- Słowa dopisują się po kolei w linii (każde wchodzi z lekkim rozmyciem i fade, ok. 4 klatki), 1–4 słowa w bloku.
- Akcent: wybrane słowa w kursywie szeryfowej w kolorze koralowym (np. „expensive way”, „know works”, „statics”).
- Hook: jedno słowo-bohater ogromne (np. „honest”) w koralowym gradiencie, nad nim małe „I'll be”.

#### Plansze
- Tło prawie czarne (#14110F), w rogach przycięte koła w brzoskwiniowo-koralowym gradiencie.
- Duża cyfra kroku „1.” / „2.” (gruba, biała) + tekst biały, końcówka w koralowej kursywie, budowane słowo po słowie.
- Na planszy kroku 1 obrócone w 3D karty produktu wjeżdżające z dołu.

#### Kolor i obraz
- Ciepła, lekko wyprana gradacja, jasne prześwietlone okno, ciemny stół (winieta u dołu), film look.
- Przejścia: twarde cięcia. Bez przesuwanych przejść i bez efektów „AI”.

#### Dźwięk
- Pod całością cichy podkład muzyczny (w przerwach mowy ok. −25 dB RMS, mowa ok. −17 dB).

#### Koniec
- Ciemna karta marki: logo, adres strony, jedno zdanie, koralowy przycisk z CTA.

#### Przełożenie na Konrada
- 1:1: napisy (mały sans + koralowy → u nas kolor do ustalenia), plansze z krokami na ciemnym tle, karta marki na końcu, twarde cięcia, punch-iny przez zmianę ujęcia.
- Potrzebne od Konrada: b-rolle (praca przy laptopie, dłonie, ekran, odbicie w okularach), zdjęcia produktu / ekranów do wachlarza, logo i kolor akcentu.


### `projekty/styl2/PLAN_ads7_ads10.md`

### Styl 2: plan montażu ads7 i ads10 (do akceptacji)

Wspólne: twarde cięcia (11 w ads7, 20 w ads10, zoom zmienia się tylko na nich: plan szeroki ↔ bliski),
ciepła „kinowa” gradacja, mały biały napis słowo po słowie na wysokości klatki, akcenty w kursywie teal/jasnoniebieskiej,
b-rolle z Pexels 0,8–1,5 s (napis leci dalej), ciemne plansze z numerowanymi krokami i teal kołami w rogach,
na końcu ciemna karta marki z przyciskiem. Bez SFX i muzyki (na razie).

#### ads7 (64,7 s)
| czas | słowa | co dajemy |
|---|---|---|
| 0,0–3,9 | „Zastanawiałeś się… skąd… biorą **pieniądze**” | hook: wielkie słowo „pieniądze” w teal gradiencie |
| 4,9–6,4 | „…za siedzenie przed komputerem” | b-roll: dłonie na klawiaturze |
| 6,6–10,3 | „…jeden z *najprostszych modeli*” | akcent teal |
| 13,3–14,7 | „poradnik z 30 szybkimi obiadami” | b-roll: szybkie gotowanie |
| 14,8–16,5 | „wystawia go za 49 zł” | wachlarz: okładka e-booka „30 szybkich obiadów” + cena 49 zł |
| 17,4–18,9 | „publikuje krótkie filmiki AI z przepisami” | b-roll: telefon, przewijanie rolek |
| 23,1–28,9 | „ogląda filmik → wchodzi na stronę → kupuje → 39 zł na konto” | szklane kafelki 1-2-3 + powiadomienie „+39 zł” |
| 32,7–35,0 | „nie musisz zamawiać towaru, pakować paczek” | 2 szybkie b-rolle: magazyn, pakowanie paczek |
| 37,7–39,9 | „na tym polega biznes na produktach cyfrowych” | PLANSZA: „Biznes na *produktach cyfrowych*” |
| 40,0–45,3 | „AI pomaga stworzyć produkt, stronę, filmiki” | PLANSZA: kroki 1. Produkt 2. Strona sprzedażowa 3. Filmiki |
| 46,9–48,5 | „…sklepu, e-commerce czy dropshippingu” | b-roll: tradycyjny sklep / paczki |
| 49,6–54,4 | „dlatego stworzyłem *Cyfrowy Autopilot*” | wachlarz kart produktu (makiety do podmiany na Twoje screeny) |
| 54,9–58,0 | „od pomysłu… produkt… strona… klienci” | szklane kafelki 1-2-3-4 |
| 59,2–60,6 | „zamiast dalej zastanawiać się…” | b-roll: ktoś przewija telefon |
| 61,5–64,7 | „kliknij poniżej” | przycisk teal pod napisem |
| 64,7–67,2 | – | karta marki (Cyfrowy Autopilot · jedno zdanie · przycisk) |

#### ads10 (95,6 s)
| czas | słowa | co dajemy |
|---|---|---|
| 0,0–5,1 | „…największą okazją w 2026 jest **sztuczna inteligencja**” | hook: wielkie „sztuczna inteligencja” w teal gradiencie |
| 8,7–10,0 | „większość ludzi nie rozumie” | b-roll: zagubiona osoba przy laptopie |
| 11,7–14,6 | „pytania do ChatGPT, śmieszne obrazki” | 2 b-rolle: pisanie w czacie, generowanie obrazków |
| 19,2–23,5 | „połączenie AI z produktami cyfrowymi” | PLANSZA: „AI + *produkty cyfrowe*” |
| 23,6–25,1 | „zaczynasz od kompletnego zera” | b-roll: pusty notes / pusta kartka |
| 28,2–31,4 | „AI znajduje pomysł z zapotrzebowaniem” | PLANSZA krok 1 |
| 32,2–34,5 | „analiza rynku i klientów” | PLANSZA krok 2 |
| 37,6–40,0 | „tworzy produkt cyfrowy” | PLANSZA krok 3 |
| 41,4–43,9 | „buduje stronę sprzedażową” | PLANSZA krok 4 |
| 44,4–46,1 | „filmiki, posty i reklamy” | b-roll: nagrywanie rolki telefonem |
| 50,7–52,3 | „coś, co możesz wystawić na sprzedaż” | powiadomienie o sprzedaży |
| 57,4–59,1 | „w najlepszym dniu 941 e-booków” | wielka liczba „941” w teal gradiencie |
| 62,3–64,0 | „kiedyś musiałeś się nauczyć / płacić innym” | b-roll: stara, ciężka praca biurowa |
| 70,5–73,3 | „stworzyłem Cyfrowy Autopilot” | wachlarz kart produktu |
| 77,5–80,1 | „bez doświadczenia i bez pokazywania twarzy” | 2 szklane kafelki z ptaszkiem |
| 83,0–83,9 | „za jedyne 17 zł” | wielkie „17 zł” |
| 84,9–91,8 | „dwie opcje…” | PLANSZE: „1. Dalej pytać AI…” / „2. *Stworzyć coś, za co ludzie zapłacą*” |
| 91,9–95,6 | „kliknij przycisk poniżej” | przycisk teal |
| 95,6–98,1 | – | karta marki |


### `projekty/styl3/BREAKDOWN.md`

### Styl 3: breakdown wzoru (reklama agencji, 72 s, 720×1280)

#### Formuła
Twarz w ciemnym studiu ↔ granatowe plansze z dowodami (screeny profili, siatki rolek, karty wyników) przeplatane co 2–4 s.
Narracja jest zbudowana jak framework („in 3 ways”): numerowana lista kroków zostaje na ekranie i rośnie razem z mową.

#### Liczby
- 25 cięć w 72 s (średnie ujęcie ok. 2,9 s). Ok. 45% czasu to plansze bez twarzy.
- Pod całością cicha muzyka (w przerwach ok. −30 dB RMS, mowa ok. −17 dB).

#### Napisy (najważniejszy element)
- Bardzo duże (ok. 90 px przy 1080), grube (Black), ciasny kerning, ułożone w pionowy stos: 1–2 słowa na linię, 2–4 linie.
- Każde słowo wchodzi z mocnego rozmycia (ok. 5 klatek) i lekkiego skalowania.
- Słowa-klucze w elektrycznie niebieskiej ramce (biały tekst na niebieskim prostokącie).
- Słowa „emocjonalne” w szeryfowej kursywie, pisane litera po literze (efekt maszyny do pisania).

#### Plansze
- Tło prawie czarne, granatowe, z ruchomymi rozmytymi plamami niebieskiego światła.
- Nagłówek: mały tekst z białą linią, która wysuwa się spod niego; albo duży biały tytuł budowany słowo po słowie nad kartą.
- Karty-dowody: screeny UI (profil, siatka rolek, wyniki) jako zaokrąglone karty.
- Wejście w planszę: krótki błysk/rozmycie (2–3 klatki), nie goły cut.

#### Elementy specjalne
- Lista-licznik: białe pigułki z niebieskim kwadratem z numerem (1 Testing, 2 Trust, 3 Retargeting). Zostaje na ekranie i przenosi się między planszami a twarzą.
- Drabinka 1–4 z paskami wypełnianymi na niebiesko (co wchodzi w usługę).
- Gwarancja: ikona + dwie linie („We guarantee 1M views / Or you don't pay”).
- CTA: mały niebieski prostokąt z tekstem wersalikami.

#### Psychologia
- Autorytet przez dowody: zamiast mówić „działa”, pokazuje screeny wyników.
- Otwarta pętla: „w 3 krokach” + lista, która się zapełnia, więc widz czeka na resztę.
- Zmiana obrazu co 2–3 s (pattern interrupt), żeby kciuk nie przewinął.
- Kontrast: niebieska ramka = „to zapamiętaj”, kursywa = emocja/ironia.
- Odwrócenie ryzyka (gwarancja) tuż przed CTA.

#### Przełożenie na Konrada (ads5, ads2)
- Kolory: granat #05071A, elektryczny indygo #3B3BFF (ramki, numery, poświaty), biel.
- Fonty: Inter Black (stos napisów), Instrument Serif italic (kursywa pisana literami).
- Lista-licznik dla 4 kroków Cyfrowego Autopilota (pomysł → produkt z AI → strona → sprzedaż).
- Karty-dowody tylko z prawdziwymi faktami (941 e-booków itd.) lub makiety produktu; zero zmyślonych wyników.
- Bez karty końcowej (jak we wzorze): koniec na twarzy z niebieskim CTA.

## Załącznik B: pełny kod silników

Każdy plik poniżej odtwarzasz 1:1 pod podaną ścieżką (względem katalogu repo). Binaria, których tu nie ma, trzeba pobrać:
- fonty woff2 → `projekty/reklamy_CA/engine/assets/fonts/` (Inter, Instrument Serif, Poppins 500/600/700/800, Anton, Montserrat 700/800 z Google Fonts, podzbiory latin + latin-ext; pliki CSS `g.css`, `poppins.css`, `fmt6.css`, `montserrat.css` są niżej),
- ikony lucide SVG → `projekty/reklamy_CA/engine/assets/icons/<nazwa>.svg` (lucide.dev),
- emoji Apple PNG 64 px → `projekty/styl6/engine/emoji_apple/` i `projekty/styl8/engine/emoji_apple/` z `https://cdn.jsdelivr.net/npm/emoji-datasource-apple@15.1.2/img/apple/64/<kod>.png`,
- model twarzy YuNet → `projekty/styl8/face_yunet.onnx` z `https://github.com/opencv/opencv_zoo/raw/main/models/face_detection_yunet/face_detection_yunet_2023mar.onnx`,
- muzyka i SFX z Mixkit (ID w sekcji „Muzyka i SFX”).


### `projekty/audio/cues_ad11.py`

````python
#!/usr/bin/env python3
"""Sound design cues for ad11.  usage: cues_ad11.py WORKDIR(ad11) AUDIODIR OUT.json"""
import json, os, sys
WD, AD, OUT = sys.argv[1:4]
S = lambda n: os.path.join(AD, "sfx", n + ".mp3")
cuts = json.load(open(os.path.join(WD, "cuts.json")))
spec = json.load(open(os.path.join(WD, "spec4_ad11.json")))

sfx, last = [], -9
whooshes = ["whoosh_fast", "sweep", "whoosh_trans"]
for i, c in enumerate(cuts):                      # soft whoosh on scene changes, never two within 1 s
    if c - last < 1.0: continue
    sfx.append(dict(t=c, f=S(whooshes[i % 3]), db=-17, peak=True)); last = c
for cp in spec["caps"]:                           # yellow emphasis words get a light pop
    if cp["em"] and "17" not in cp["html"]: sfx.append(dict(t=cp["t0"], f=S("pop_whoosh"), db=-12))
hit = lambda txt: next(cp["t0"] for cp in spec["caps"] if txt in cp["html"])
sfx += [dict(t=hit("941"), f=S("coins"), db=-11),                # 941 e-booków
        dict(t=hit("Automatycznie"), f=S("pop_msg"), db=-13),    # someone buys -> gets the product
        dict(t=hit("17 zł"), f=S("coin_prize"), db=-13),         # price reveal
        dict(t=hit("Kliknij przycisk"), f=S("click_select"), db=-9)]
json.dump(dict(music=os.path.join(AD, "music", "mk_140.mp3"), musicStart=0, musicDb=-21, fadeOut=2.0, sfx=sorted(sfx, key=lambda s: s["t"])),
          open(OUT, "w"), indent=1)
print(len(sfx), "sfx cues")
````


### `projekty/audio/mix.py`

````python
#!/usr/bin/env python3
"""Music + SFX mix for a finished ad.  usage: mix.py CUES.json IN.mp4 OUT.mp4
CUES = {"music": path, "musicStart": s, "musicDb": dB (gain before ducking), "fadeOut": s,
        "sfx": [{"t": s, "f": path, "db": dB, "peak": true}]}   peak=true aligns the loudest point of the sound to t.
Voice ducks the music (sidechain), everything is normalised to -14 LUFS / -1.5 dBTP for Meta."""
import json, subprocess, sys
import numpy as np

cues, src, out = json.load(open(sys.argv[1])), sys.argv[2], sys.argv[3]
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", src], capture_output=True, text=True).stdout)
_peaks = {}


def peak(f):  # seconds from file start to its loudest sample
    if f not in _peaks:
        a = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", f, "-ac", "1", "-ar", "8000", "-f", "s16le", "-"], capture_output=True).stdout, np.int16)
        _peaks[f] = float(np.argmax(np.abs(a.astype(np.int32)))) / 8000 if len(a) else 0.0
    return _peaks[f]


ins = ["-i", src, "-i", cues["music"]]
fc = [f"[0:a]aresample=48000,asplit=2[vo][sc]",
      f"[1:a]aresample=48000,atrim=start={cues.get('musicStart', 0)},asetpts=PTS-STARTPTS,atrim=0:{dur},volume={cues.get('musicDb', -18)}dB,"
      f"afade=t=in:d=0.4,afade=t=out:st={dur - cues.get('fadeOut', 1.5):.3f}:d={cues.get('fadeOut', 1.5)}[mu]",
      "[mu][sc]sidechaincompress=threshold=0.02:ratio=5:attack=15:release=350:makeup=1[duck]"]
mixin = ["[vo]", "[duck]"]
for k, s in enumerate(cues.get("sfx", [])):
    ins += ["-i", s["f"]]; t = max(0.0, s["t"] - (peak(s["f"]) if s.get("peak") else 0.0))
    fc.append(f"[{k + 2}:a]aresample=48000,volume={s.get('db', -10)}dB,adelay={int(t * 1000)}:all=1[s{k}]"); mixin.append(f"[s{k}]")
fc.append("".join(mixin) + f"amix=inputs={len(mixin)}:normalize=0:duration=first,loudnorm=I=-14:TP=-1.5:LRA=11[a]")
subprocess.run(["ffmpeg", "-v", "error", "-y", *ins, "-filter_complex", ";".join(fc), "-map", "0:v", "-map", "[a]",
                "-c:v", "copy", "-c:a", "aac", "-b:a", "128k", "-ar", "48000", "-movflags", "+faststart", out], check=True)
print("wrote", out)
````


### `projekty/reklamy_CA/build_spec.py`

````python
#!/usr/bin/env python3
"""Build render specs (captions + plansze + overlays + zooms) for ad8 / ad9.
usage: build_spec.py WORKDIR   (WORKDIR has ad8.mp4, ad9.mp4, tr8.json, tr9.json) -> writes spec_ad8.json, spec_ad9.json
"""
import difflib, json, os, re, subprocess, sys

WD = sys.argv[1]
WEAK = {"i", "w", "z", "na", "do", "od", "po", "a", "o", "że", "bo", "się", "to", "jak", "czy", "nie", "co", "za", "ci", "ten", "tego"}


def norm(t):
    return re.sub(r"[^\w]", "", t.lower())


def align(words, fixed):
    """fixed tokens (hero joined by _ and wrapped in *) get the time of the matching ASR word."""
    toks = []
    for raw in fixed.split():
        h = raw.startswith("*")
        clean = raw.strip("*")
        parts = clean.split("_")
        for k, p in enumerate(parts):
            toks.append({"d": p, "h": h, "join": k > 0})
    a = [norm(w["w"]) for w in words]
    b = [norm(t["d"]) for t in toks]
    times = [None] * len(toks)
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        if op == "equal":
            for k in range(i2 - i1): times[j1 + k] = words[i1 + k]["s"]
        elif op == "replace":
            s0, e0 = words[i1]["s"], words[i2 - 1]["e"]
            for j in range(j1, j2): times[j] = s0 + (e0 - s0) * (j - j1) / max(1, j2 - j1)
    for j in range(len(toks)):
        if times[j] is None:
            times[j] = next((times[k] for k in range(j - 1, -1, -1) if times[k] is not None), 0.0)
    for j, t in enumerate(toks): t["t"] = round(times[j], 3)
    # merge hero sub-tokens into one display unit
    units = []
    for t in toks:
        if t["join"] and units: units[-1]["d"] += " " + t["d"]
        else: units.append(dict(t))
    return units


def chunk(units, maxw=3, maxc=20):
    blocks, cur = [], []
    def flush():
        if cur: blocks.append(cur[:]); cur.clear()
    for i, u in enumerate(units):
        if u["h"]:
            # hero closes the block: keep at most 2 small words before it
            while len([x for x in cur if not x["h"]]) > 2:
                blocks.append([cur.pop(0)])
            cur.append(u); flush(); continue
        clen = sum(len(x["d"]) + 1 for x in cur) + len(u["d"])
        if cur and (len(cur) >= maxw or clen > maxc):
            # do not leave a weak word dangling at the end of a block
            last = cur[-1]["d"].lower().strip(",.?")
            if (last in WEAK or last.isdigit()) and len(cur) > 1:
                carry = cur.pop(); flush(); cur.append(carry)
            else: flush()
        cur.append(u)
        if u["d"].endswith((".", "?", "!")): flush()
    flush()
    out = []
    for b in blocks:
        out.append({"t0": b[0]["t"], "words": [{"d": w["d"], "t": w["t"], "h": w["h"]} for w in b]})
    return out


def dur(p):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p], capture_output=True, text=True).stdout)


def words_of(n):
    return [w for s in json.load(open(os.path.join(WD, f"tr{n}.json"))) for w in s["words"]]


def sentence_starts(n):
    return [round(s["start"], 2) for s in json.load(open(os.path.join(WD, f"tr{n}.json")))]


def cuts_of(n):
    out = subprocess.run([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), "engine", "cuts.py"),
                          os.path.join(WD, f"ad{n}.mp4")], capture_output=True, text=True).stdout
    return json.loads(out)


def snap_scenes(scenes, cuts):
    """plansza starts on the first frame of a shot and ends on a cut when one is near; back-to-back scenes hard-cut."""
    for s in scenes:
        c = [c for c in cuts if s["t0"] - 0.35 <= c <= s["t0"] + 0.6]
        if c: s["t0"] = c[0]
        c = [c for c in cuts if abs(c - s["t1"]) <= 0.6]
        if c: s["t1"] = min(c, key=lambda c: abs(c - s["t1"]))
    scenes.sort(key=lambda s: s["t0"])
    for a, b in zip(scenes, scenes[1:]):
        if b["t0"] - a["t1"] <= 0.4:
            b["t0"] = a["t1"]; b["noReveal"] = True
    return scenes


def shot_zooms(cuts, dur, scenes, cta_t0):
    """one zoom level per shot, switching only on real cuts; CTA shots stay at 100 %."""
    z, big = [], False
    for t in [0.0] + cuts:
        if any(s["t0"] - .05 <= t < s["t1"] - .05 for s in scenes): continue
        z.append([t, 1.0 if t >= cta_t0 - 0.5 else (1.10 if big else 1.0)]); big = not big
    # a shot that starts under a plansza gets its zoom from the plansza's end
    for s in scenes:
        inside = [c for c in cuts if s["t0"] - .05 <= c < s["t1"] - .05]
        if inside and not any(abs(zt - s["t1"]) < .05 for zt, _ in z):
            z.append([s["t1"], 1.0]); 
    return sorted(z)


def zooms_from(starts, scenes):
    z, big = [], False
    for t in starts:
        if any(s["t0"] - .05 <= t < s["t1"] for s in scenes): continue
        z.append([t, 1.12 if big else 1.0]); big = not big
    return z


WM_MONEY = [dict(icon="circle-dollar-sign", x=140, y=300, s=380, r=-12), dict(icon="circle-dollar-sign", x=930, y=1500, s=460, r=10),
            dict(icon="sparkles", x=900, y=260, s=300, r=8), dict(icon="file-text", x=180, y=1560, s=360, r=-6)]

# ------------------------------------------------------------------ AD 8
FIX8 = ("Za cenę takiej jednej kawy na mieście pokażę Ci, jak w *48_godzin* stworzyć z pomocą sztucznej inteligencji coś, "
        "co można *sprzedawać* przez internet. I nie, nie mówię tutaj o kolejnym pomyśle na biznes. Mówię o prawdziwym "
        "produkcie cyfrowym, własnej stronie sprzedażowej i wszystkim, czego potrzebujesz, żeby zacząć. I zanim pomyślisz, "
        "że to kolejny kurs, w którym przez *10_godzin* oglądasz, jak ktoś opowiada Ci o zarabianiu w internecie, to zobacz, "
        "co dokładnie zrobisz. Po pierwsze, wybierzesz pomysł na produkt cyfrowy, którego ludzie faktycznie potrzebują. "
        "Nie musisz go sam wymyślać. Sztuczna inteligencja pomoże Ci znaleźć odpowiedni *kierunek.* Po drugie, stworzysz ten "
        "produkt. Może to być poradnik, planner, zestaw szablonów, PDF albo coś zupełnie innego. Po trzecie, z pomocą AI "
        "przygotujesz własną stronę sprzedażową, na której ludzie będą mogli kupić, a po czwarte pokażę Ci, jak tworzyć treści "
        "i reklamy, które mogą przyciągać do niego klientów. Pomysł, produkt, strona, marketing i to wszystko z pomocą "
        "sztucznej inteligencji. Generalnie jest to cały proces krok po kroku i moim celem nie jest to, żebyś po 48 godzinach "
        "wiedział więcej o AI. Moim celem jest to, żebyś miał coś, czego *dzisiaj_nie_masz.* Własny produkt cyfrowy, który "
        "realnie ma szansę się *sprzedawać.* Ja sam sprzedaję produkty cyfrowe od ponad 3 lat, a w najlepszym dniu sprzedałem "
        "941 e-booków. I właśnie na tej podstawie stworzyłem Cyfrowy Autopilot. I dzisiaj dostęp do tego możesz dostać tylko "
        "za *17_zł.* I w dodatku daję Ci na to gwarancję. Jeżeli w 48 godzin nie zbudujesz wszystkiego, zwracam Ci 100% kwoty. "
        "Kliknij przycisk poniżej i zacznij działać już teraz, dosłownie za mniej niż kubek *kawy* na mieście. I zamiast "
        "kupować kolejną wiedzę o zarabianiu, zacznij w końcu tworzyć coś, co może się *sprzedać.*")

SC8 = [
    # 1: "nie kolejny pomysł na biznes" -> 3 real deliverables
    dict(type="discTile", t0=6.86, t1=13.86, cap=dict(mode="light", y=0.6, hideIn=[[9.36, 13.9]]), a=dict(
        tiles=[dict(icon="lightbulb", t=7.05, y=700, size=250, spark=True, t1=9.3, s1=.5)],
        strike=dict(t=8.9, y=690, t1=9.3),
        pills=[dict(text="Prawdziwy produkt cyfrowy", icon="book-open", t=9.7, y=640, cls="white"),
               dict(text="Własna strona sprzedażowa", icon="layout-template", t=11.16, y=790, cls="white"),
               dict(text="Wszystko, by zacząć", icon="rocket", t=12.22, y=940, cls="white")])),
    # 2: krok 1 – pomysł, AI pomaga znaleźć kierunek
    dict(type="orbit", t0=20.28, t1=27.08, cap=dict(mode="light", y=0.79), a=dict(
        wm=WM_MONEY, R=340, cy=760, center=dict(icon="lightbulb", t=20.6, size=200, spark=True),
        sats=[dict(icon="users", ang=-150, t=22.36, label="Ludzie tego potrzebują"),
              dict(icon="sparkles", ang=-30, t=24.76, label="AI pomaga"),
              dict(icon="compass", ang=90, t=26.32, label="Kierunek")])),
    # 3: krok 3+4 – strona sprzedażowa, zakup, treści i reklamy
    dict(type="phone", t0=32.2, t1=39.98, cap=dict(mode="dark", y=0.885), a=dict(
        cy=780, buildT=33.2, buyT=35.72, notifT1=36.9,
        ads=[dict(icon="clapperboard", x=175, y=560, t=37.5, rot=-8), dict(icon="megaphone", x=905, y=520, t=38.06, rot=7),
             dict(icon="video", x=905, y=1080, t=38.5, rot=-5)],
        people=[dict(x=170, y=1060, t=39.3), dict(x=250, y=1180, t=39.42)])),
    # 5: dowód – najlepszy dzień
    dict(type="discTile", t0=53.66, t1=58.42, cap=dict(mode="light", y=0.6, hideIn=[[56.3, 58.5]]), a=dict(
        slot=dict(x=540, y=1480, w=460, h=330, rot=-5, t=54.3),
        tiles=[dict(icon="trending-up", t=53.9, y=640, size=220, t1=56.2, s1=.6)],
        pills=[dict(text="Od ponad 3 lat", icon="clock", t=55.48, y=880, cls="white", t1=56.2)],
        counter=dict(t=56.84, d=1.0, to=941, y=640, fs=230, sub="e-booków w jeden dzień", subT=57.5))),
    # 6: gwarancja
    dict(type="hero", t0=63.72, t1=68.74, cap=dict(mode="light", y=0.84), a=dict(
        wm=WM_MONEY, icon="shield-check", iy=560, isize=270, it=63.95,
        items=[dict(kind="text", text="Gwarancja", fs=120, y=820, t=64.76),
               dict(kind="pill", text="48 godzin", icon="clock", y=990, t=65.78, cls="white"),
               dict(kind="text", text="100%", fs=150, y=1170, t=67.88, count=dict(t=67.88, d=.5, to=100, suf="%"))])),
]
OV8 = [
    dict(type="tile", t0=2.76, t1=6.6, a=dict(icon="clock", x=540, y=1410, size=150, badge="48 h", badgeT=2.9)),
    dict(type="pills", t0=28.8, t1=32.1, a=dict(items=[
        dict(text="Poradnik", icon="book-open", x=310, y=1480, t=28.88), dict(text="Planner", icon="calendar-check", x=770, y=1480, t=29.42),
        dict(text="Szablony", icon="files", x=310, y=1580, t=30.04), dict(text="PDF", icon="file-text", x=770, y=1580, t=30.66)])),
    dict(type="pills", t0=40.05, t1=43.5, cap=dict(mode="face", y=0.645, hideIn=[[40.0, 41.6]]), a=dict(items=[
        dict(text="Pomysł", icon="lightbulb", x=310, y=1480, t=40.12, cls="solid"), dict(text="Produkt", icon="package", x=770, y=1480, t=40.52, cls="solid"),
        dict(text="Strona", icon="layout-template", x=310, y=1580, t=40.96, cls="solid"), dict(text="Marketing", icon="megaphone", x=770, y=1580, t=41.34, cls="solid"),
        dict(text="+ AI", icon="sparkles", x=540, y=1680, t=42.58, cls="white")])),
    dict(type="brand", t0=59.6, t1=60.8, a=dict(y=1420)),
    dict(type="price", t0=62.8, t1=63.72, a=dict(text="17 zł", x=540, y=1610, w=480, h=230, fs=150)),
    dict(type="cta", t0=68.9, t1=99, a=dict(text="Kliknij poniżej", y=1420)),
]

# ------------------------------------------------------------------ AD 9
FIX9 = ("ChatGPT nie zapłaci Ci *ani_złotówki.* Możesz mieć najlepsze prompty na świecie, znać wszystkie narzędzia AI "
        "i codziennie spędzać po 5–10 godzin przed laptopem. Ale dopóki nie masz czegoś, za co ktoś jest gotowy zapłacić, "
        "to nadal *nie_masz_biznesu.* I właśnie tego nie rozumie większość ludzi próbujących zarabiać z AI. Bo finalnie to "
        "nie sztuczna inteligencja płaci pieniądze, płacą Ci *ludzie.* Za co? Za rozwiązywanie ich *problemu.* Pomyśl, ktoś "
        "potrzebuje planera budżetu, żeby uporządkować swoje wydatki. Ktoś inny szuka prostych przepisów, bo nie ma czasu na "
        "gotowanie. A jeszcze ktoś potrzebuje gotowego szablonu CV, żeby szybciej przygotować dokumenty do rekrutacji. "
        "To są rzeczy, za które ludzie mogą *zapłacić.* I teraz najlepsze, bo dzisiaj AI może pomóc takie rzeczy stworzyć. "
        "I to wszystko bez pisania wszystkiego od zera czy pokazywania swojej twarzy. Dokładnie dlatego zbudowałem Cyfrowy "
        "Autopilot. System, który pokazuje Ci, jak znaleźć pomysł na produkt cyfrowy, stworzyć go z pomocą sztucznej "
        "inteligencji i przygotować całą stronę sprzedażową. I oczywiście następnie pokazuje Ci, jak zacząć go sprzedawać "
        "przy pomocy sztucznej inteligencji. I to wszystko po to, żebyś w ciągu *48_godzin* mógł przejść od pustego czatu GPT "
        "do produktu gotowego na sprzedaż. I co jest najciekawsze, aktualnie możesz otrzymać dostęp za jedyne *17_zł.* Czyli "
        "dosłownie mniej niż jedna kawa na mieście. Kliknij przycisk poniżej pod tym filmem i przestań pisać do ChatGPT, jak "
        "zarabiać pieniądze, a zacznij używać go do stworzenia czegoś, za co ludzie mogą *zapłacić.*")

SC9 = [
    dict(type="checklist", t0=2.12, t1=7.62, cap=dict(mode="hide"), a=dict(cy=900, rowH=200, items=[
        dict(icon="wand-sparkles", text="Najlepsze prompty na świecie", t=2.6),
        dict(icon="wrench", text="Wszystkie narzędzia AI", t=4.28),
        dict(icon="laptop", text="5–10 godzin dziennie przed laptopem", t=5.44, fs=52)])),
    dict(type="discTile", t0=14.44, t1=19.22, cap=dict(mode="light", y=0.62), a=dict(
        tiles=[dict(icon="bot", t=14.65, y=640, size=230, t1=16.85, s1=.5),
               dict(icon="users", t=16.95, y=640, size=250, spark=True)],
        pills=[dict(text="0 zł", icon="x", t=16.12, y=880, cls="white", t1=16.85),
               dict(text="Płacą ludzie", icon="hand-coins", t=17.26, y=880, cls="white")])),
    dict(type="orbit", t0=19.22, t1=29.72, cap=dict(mode="light", y=0.8), a=dict(
        wm=WM_MONEY, R=340, cy=760, center=dict(icon="user", t=19.5, size=200),
        sats=[dict(icon="wallet", ang=-140, t=20.22, label="Planer budżetu"),
              dict(icon="chef-hat", ang=-40, t=23.18, label="Proste przepisy"),
              dict(icon="file-user", ang=90, t=26.36, label="Szablon CV")])),
    dict(type="checklist", t0=40.95, t1=49.46, cap=dict(mode="hide"), a=dict(cy=900, rowH=200, connector=True, items=[
        dict(icon="lightbulb", text="Pomysł na produkt cyfrowy", t=41.26),
        dict(icon="sparkles", text="Stworzenie go z AI", t=43.32),
        dict(icon="layout-template", text="Cała strona sprzedażowa", t=44.96),
        dict(icon="trending-up", text="Sprzedaż z pomocą AI", t=47.96)])),
]
OV9 = [
    dict(type="pills", t0=34.9, t1=37.95, a=dict(items=[
        dict(text="Bez pisania od zera", icon="pen-line", x=540, y=1420, t=35.18, cls="white"),
        dict(text="Bez pokazywania twarzy", icon="user", x=540, y=1530, t=36.76, cls="white")])),
    dict(type="brand", t0=39.0, t1=40.95, a=dict(y=1420)),
    dict(type="flow", t0=52.3, t1=54.85, a=dict(items=[
        dict(icon="message-square-dashed", x=290, y=1450, t=52.46, label="Pusty czat"),
        dict(x=540, y=1450, t=53.2), dict(icon="package", x=790, y=1450, t=53.52, label="Gotowy produkt", dark=True)])),
    dict(type="cta", t0=60.55, t1=99, a=dict(text="Kliknij poniżej", y=1420)),
]


def make(n, fixed, scenes, overlays, mirror, capY):
    src = os.path.join(WD, f"ad{n}.mp4")
    units = align(words_of(n), fixed)
    cuts = cuts_of(n); scenes = snap_scenes(scenes, cuts); d = round(dur(src), 3)
    cta = min([o["t0"] for o in overlays if o["type"] == "cta"] or [d])
    spec = dict(src=src, dur=d, fps=30, mirror=mirror, capY=capY, zoomCenter=[0.5, 0.34], cuts=cuts,
                caps=chunk(units), scenes=scenes, overlays=overlays,
                zooms=shot_zooms(cuts, d, scenes, cta))
    p = os.path.join(WD, f"spec_ad{n}.json")
    json.dump(spec, open(p, "w"), ensure_ascii=False, indent=1)
    print(p, len(spec["caps"]), "caption blocks")
    for b in spec["caps"]:
        print(f'  {b["t0"]:6.2f}  ' + " ".join(("*" + w["d"] + "*") if w["h"] else w["d"] for w in b["words"]))


make(8, FIX8, SC8, OV8, False, 0.645)
make(9, FIX9, SC9, OV9, True, 0.56)
````


### `projekty/reklamy_CA/run_all.sh`

````bash
#!/bin/bash
# full render: overlays -> compose. usage: run_all.sh WORKDIR [ads...]
set -e
D=$1; shift; H=$(cd "$(dirname "$0")" && pwd)
python3 $H/build_spec.py $D > /dev/null
for n in ${@:-8 9}; do
  rm -rf $D/frames$n
  node $H/engine/render.mjs $D/spec_ad$n.json $D/frames$n --par 3
  python3 $H/engine/compose.py $D/spec_ad$n.json $D/frames$n $D/AD${n}_EDIT.mp4
  ffmpeg -v error -y -i $D/AD${n}_EDIT.mp4 -vf scale=540:-2 -c:v libx264 -crf 28 -preset fast -c:a aac -b:a 96k -movflags +faststart $D/AD${n}_EDIT_tel.mp4
  echo "DONE ad$n"
done
````


### `projekty/reklamy_CA/engine/chunks.py`

````python
#!/usr/bin/env python3
"""Verbatim-ish chunk transcript for cutting raw takes.
Splits speech on silences (energy), transcribes every chunk separately (so Whisper can't merge retakes),
writes OUT.json [{i,s,e,text,words:[{w,s,e}]}] and prints one line per chunk.
usage: chunks.py VIDEO OUT.json [--model medium] [--gap 0.35]"""
import json, subprocess, sys
import numpy as np
from faster_whisper import WhisperModel
a = sys.argv[1:]; src, out = a[0], a[1]
model = a[a.index("--model") + 1] if "--model" in a else "medium"
GAP = float(a[a.index("--gap") + 1]) if "--gap" in a else 0.35
SR = 16000
pcm = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", src, "-ac", "1", "-ar", str(SR), "-f", "s16le", "-"],
                                   capture_output=True).stdout, np.int16).astype(np.float32) / 32768
hop = int(0.02 * SR)
rms = np.sqrt(np.convolve(pcm ** 2, np.ones(hop) / hop, "same")[::hop] + 1e-12)
db = 20 * np.log10(rms)
floor = np.percentile(db, 10); thr = max(floor + 12, -45)
speech = db > thr
segs, i, n = [], 0, len(speech)
while i < n:
    if speech[i]:
        j = i
        while j < n and speech[j]: j += 1
        segs.append([i * 0.02, j * 0.02]); i = j
    else: i += 1
merged = []
for s, e in segs:
    if merged and s - merged[-1][1] < GAP: merged[-1][1] = e
    else: merged.append([s, e])
merged = [m for m in merged if m[1] - m[0] > 0.18]
m = WhisperModel(model, device="cpu", compute_type="int8")
res = []
for k, (s, e) in enumerate(merged):
    s0, e0 = max(0, s - 0.15), min(len(pcm) / SR, e + 0.15)
    seg, _ = m.transcribe(pcm[int(s0 * SR):int(e0 * SR)], language="pl", word_timestamps=True,
                          condition_on_previous_text=False, vad_filter=False, beam_size=5)
    words, text = [], []
    for sg in seg:
        text.append(sg.text.strip())
        words += [{"w": w.word.strip(), "s": round(s0 + w.start, 3), "e": round(s0 + w.end, 3)} for w in sg.words]
    r = {"i": k, "s": round(s, 3), "e": round(e, 3), "text": " ".join(text), "words": words}
    res.append(r); print(f"[{k:3d}] {s:7.2f}-{e:7.2f}  {r['text']}", flush=True)
json.dump(res, open(out, "w"), ensure_ascii=False, indent=0)
print(f"thr {thr:.1f} dB, {len(res)} chunks")
````


### `projekty/reklamy_CA/engine/compose.py`

````python
#!/usr/bin/env python3
"""Footage (+zoom punch-ins, optional mirror) + overlay PNG frames -> final mp4 with the original audio.

usage: compose.py SPEC.json FRAMES_DIR OUT.mp4 [--from S --to S] [--preview]
Zoom: spec["zooms"] = [[t, scale], ...] hard punch at each t; after a plansza ends the face settles 1.07->1.0 in 0.35 s.
"""
import json, os, subprocess, sys
import numpy as np, cv2

a = sys.argv[1:]
spec = json.load(open(a[0])); fdir = a[1]; out = a[2]
opt = lambda k, d=None: a[a.index(k) + 1] if k in a else d
fps = spec.get("fps", 30); W, H = 1080, 1920
t_from = float(opt("--from", 0)); t_to = float(opt("--to", spec["dur"]))
f0, f1 = round(t_from * fps), round(t_to * fps)
zooms = sorted(spec.get("zooms", [])); settles = [s["t1"] for s in spec["scenes"]]
cx, cy = spec.get("zoomCenter", [0.5, 0.36])


def scale_at(t):
    s = 1.0
    for zt, zs in zooms:
        if zt <= t: s = zs
    return s


src = spec["src"]
vf = "hflip," if spec.get("mirror") else ""
dec = subprocess.Popen(["ffmpeg", "-v", "error", "-ss", str(t_from), "-i", src, "-t", str(t_to - t_from),
                        "-vf", f"{vf}scale={W}:{H},fps={fps}", "-f", "rawvideo", "-pix_fmt", "bgr24", "-"], stdout=subprocess.PIPE)
crf = "23" if "--preview" in a else "17"
enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", str(fps), "-i", "-",
                        "-ss", str(t_from), "-t", str(t_to - t_from), "-i", src, "-map", "0:v", "-map", "1:a",
                        "-c:v", "libx264", "-preset", "medium", "-crf", crf, "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
                        "-movflags", "+faststart", "-shortest", out], stdin=subprocess.PIPE)
fsz = W * H * 3
for f in range(f0, f1):
    buf = dec.stdout.read(fsz)
    if len(buf) < fsz: break
    fr = np.frombuffer(buf, np.uint8).reshape(H, W, 3)
    t = f / fps; s = scale_at(t)
    if s > 1.001:
        w, h = W / s, H / s
        x0 = min(max(cx * W - w / 2, 0), W - w); y0 = min(max(cy * H - h / 2, 0), H - h)
        M = np.float32([[s, 0, -x0 * s], [0, s, -y0 * s]])
        fr = cv2.warpAffine(fr, M, (W, H), flags=cv2.INTER_LINEAR)
    p = os.path.join(fdir, f"f_{f:05d}.png")
    ov = cv2.imread(p, cv2.IMREAD_UNCHANGED) if os.path.exists(p) else None
    if ov is not None:
        al = ov[:, :, 3:4].astype(np.float32) / 255.0 if ov.shape[2] == 4 else np.ones(ov.shape[:2] + (1,), np.float32)
        if al.max() > 0:
            fr = (ov[:, :, :3].astype(np.float32) * al + fr.astype(np.float32) * (1 - al)).astype(np.uint8)
    enc.stdin.write(np.ascontiguousarray(fr).tobytes())
enc.stdin.close(); enc.wait(); dec.terminate()
print("wrote", out)
````


### `projekty/reklamy_CA/engine/cut.py`

````python
#!/usr/bin/env python3
"""Cut raw takes into a tight edit.
usage: cut.py TAKES.json OUT.mp4 [--preview]
TAKES.json = {"src": "raw.mp4", "takes": [[s, e], ...]}   (s = start of first word, e = end of last word, seconds)
Edges are snapped to the audio envelope (30–60 ms before the first sound, 60 ms after the last),
silences > 0.28 s inside a take are shortened to 0.13 s. Writes OUT.mp4 and OUT.edl.json (src ranges in output order).
"""
import json, subprocess, sys
import numpy as np

a = sys.argv[1:]; cfg = json.load(open(a[0])); out = a[1]
src = cfg["src"]; SR = 16000; HOP = 0.01
pcm = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", src, "-ac", "1", "-ar", str(SR), "-f", "s16le", "-"],
                                   capture_output=True).stdout, np.int16).astype(np.float32) / 32768
h = int(HOP * SR)
db = 20 * np.log10(np.sqrt(np.convolve(pcm ** 2, np.ones(h) / h, "same")[::h] + 1e-12))
thr = max(np.percentile(db, 10) + 12, -45)
on = db > thr
idx = lambda t: int(round(t / HOP))


def snap(s, e):
    i0, i1 = idx(s - 0.25), idx(s + 0.12)
    st = next((i for i in range(max(0, i0), min(len(on), i1)) if on[i]), idx(s)) * HOP - 0.05
    j0, j1 = idx(e - 0.12), idx(e + 0.3)
    en = (max([i for i in range(max(0, j0), min(len(on), j1)) if on[i]] or [idx(e)]) + 1) * HOP + 0.06
    return max(0.0, st), en


ranges = []
for tk in cfg["takes"]:
    s, e = tk[0], tk[1]
    st, en = snap(s, e)
    if len(tk) > 2 and "x" in tk[2]: st = s - 0.02          # exact start, no snapping (word glued to a previous one)
    if len(tk) > 2 and "y" in tk[2]:                          # end no later than e (next take glued right after)
        en = (max([i for i in range(max(0, idx(e) - 40), min(len(on), idx(e) + 1)) if on[i]] or [idx(e)]) + 1) * HOP + 0.05
    # split on long internal silences
    cur = st; i = idx(st); end_i = idx(en); run0 = None
    while i < end_i:
        if not on[i]:
            if run0 is None: run0 = i
        else:
            if run0 is not None and (i - run0) * HOP > 0.28:
                ranges.append([cur, run0 * HOP + 0.065]); cur = i * HOP - 0.065
            run0 = None
        i += 1
    ranges.append([cur, en])
ranges = [[round(x, 3), round(y, 3)] for x, y in ranges if y - x > 0.08]

import os, tempfile
n = len(ranges); crf = "26" if "--preview" in a else "15"
tmp = tempfile.mkdtemp(prefix="cut_", dir=os.path.dirname(os.path.abspath(out)))
lst = []
for k, (s, e) in enumerate(ranges):
    d = e - s; seg = os.path.join(tmp, f"s{k:03d}.mkv")
    o0 = min(2, s)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{max(0, s - 2):.3f}", "-i", src,
                    "-vf", f"trim=start={o0:.3f}:duration={d:.3f},setpts=PTS-STARTPTS,scale=1080:1920,fps=30,setsar=1",
                    "-af", f"atrim=start={o0:.3f}:duration={d:.3f},asetpts=PTS-STARTPTS,afade=t=in:d=0.02,afade=t=out:st={max(0, d - 0.025):.3f}:d=0.025",
                    "-c:v", "libx264", "-preset", "medium", "-crf", crf, "-pix_fmt", "yuv420p", "-c:a", "pcm_s16le", "-ar", "48000", seg], check=True)
    lst.append(f"file '{seg}'")
open(os.path.join(tmp, "list.txt"), "w").write("\n".join(lst))
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", os.path.join(tmp, "list.txt"), "-c:v", "copy",
                "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", out], check=True)
t, edl = 0.0, []
for s, e in ranges:
    edl.append({"src": [s, e], "t": round(t, 3)}); t += e - s
json.dump({"src": src, "ranges": edl, "dur": round(t, 3)}, open(out + ".edl.json", "w"), indent=0)
print(f"{n} ranges, {t:.2f} s -> {out}")
````


### `projekty/reklamy_CA/engine/cuts.py`

````python
#!/usr/bin/env python3
"""Detect hard cuts (jump cuts) in footage: per-frame diff of a small grey thumbnail, peaks vs local median.
usage: cuts.py VIDEO [--mirror]  -> prints JSON list of cut times (s) = time of first frame of the new shot"""
import json, subprocess, sys
import numpy as np
src = sys.argv[1]; W, H = 64, 112
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", src, "-vf", f"scale={W}:{H},format=gray", "-f", "rawvideo", "-"], capture_output=True).stdout
fps = eval(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v", "-show_entries", "stream=r_frame_rate", "-of", "csv=p=0", src], capture_output=True, text=True).stdout.strip())
a = np.frombuffer(raw, np.uint8).reshape(-1, H, W).astype(np.float32)
d = np.abs(np.diff(a, axis=0)).mean(axis=(1, 2))
cuts = []
for i in range(len(d)):
    lo, hi = max(0, i - 8), min(len(d), i + 9)
    nb = np.concatenate([d[lo:i], d[i + 1:hi]])
    med = np.median(nb) if len(nb) else 0
    if d[i] > 9 and d[i] > 3.2 * med + 3 and d[i] == d[max(0, i - 2):i + 3].max():
        cuts.append(round((i + 1) / fps, 3))
print(json.dumps(cuts))
````


### `projekty/reklamy_CA/engine/overlay.html`

````html
<!doctype html>
<html><head><meta charset="utf-8">
<link rel="stylesheet" href="assets/fonts/g.css">
<style>
:root{--g:#0E4D3A;--g2:#1F7A5A;--g3:#0A3A2B;--mint:#9CF0C8;--ink:#0B2A20;}
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:1080px;height:1920px;background:transparent;overflow:hidden}
#stage{position:absolute;inset:0;font-family:Inter,sans-serif;-webkit-font-smoothing:antialiased}
.abs{position:absolute}
.scene{position:absolute;inset:0;overflow:hidden;will-change:transform}
.cam{position:absolute;inset:0;transform-origin:50% 46%}
/* backgrounds */
.bg-disc{background:radial-gradient(120% 80% at 50% 40%,#FFFFFF 0%,#EEF4F1 70%,#E3ECE8 100%)}
.bg-light{background:linear-gradient(180deg,#FFFFFF 0%,#F1F6F3 100%)}
.bg-green{background:radial-gradient(90% 60% at 30% 18%,#2A8A66 0%,#16624A 35%,#0E4D3A 65%,#08301F 100%)}
.grain{position:absolute;inset:0;opacity:.07;mix-blend-mode:overlay;pointer-events:none;
 background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='300' height='300'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2' stitchTiles='stitch'/></filter><rect width='300' height='300' filter='url(%23n)'/></svg>")}
.dots{position:absolute;inset:0;background-image:radial-gradient(rgba(14,77,58,.10) 2px,transparent 2.5px);background-size:44px 44px;
 -webkit-mask-image:radial-gradient(70% 55% at 50% 45%,#000 0%,transparent 100%)}
.disc{position:absolute;border-radius:50%;
 background:radial-gradient(circle at 34% 28%,#2B8F69 0%,#17684D 32%,#0E4D3A 62%,#09382A 100%);
 box-shadow:0 0 0 64px rgba(14,77,58,.10),0 0 0 140px rgba(14,77,58,.05),0 60px 140px rgba(8,48,31,.35),inset 0 8px 30px rgba(255,255,255,.18)}
.wm{position:absolute;color:#fff;opacity:.07}
.wm svg{width:100%;height:100%;stroke-width:1.6}
.sheen{position:absolute;inset:0;background:radial-gradient(60% 30% at 70% 0%,rgba(255,255,255,.16),transparent 70%)}
/* tiles */
.tile{position:absolute;display:flex;align-items:center;justify-content:center;border-radius:28%;
 background:linear-gradient(160deg,#FFFFFF 0%,#EEF4F1 100%);color:var(--g);
 box-shadow:0 2px 0 rgba(255,255,255,.9) inset,0 -6px 14px rgba(14,77,58,.08) inset,0 24px 50px rgba(6,40,28,.28),0 0 0 3px rgba(255,255,255,.55)}
.tile svg{width:52%;height:52%;stroke-width:1.9}
.tile.dark{background:linear-gradient(160deg,#25865F 0%,#0E4D3A 100%);color:#fff;box-shadow:0 2px 0 rgba(255,255,255,.25) inset,0 24px 50px rgba(6,40,28,.35)}
.ray{position:absolute;height:3px;border-radius:3px;background:linear-gradient(90deg,transparent,rgba(255,255,255,.95),transparent);transform-origin:50% 50%}
.ray.g{background:linear-gradient(90deg,transparent,rgba(31,122,90,.8),transparent)}
.star{position:absolute;color:#fff}
.star svg{width:100%;height:100%}
/* pills */
.pill{position:absolute;display:flex;align-items:center;gap:20px;white-space:nowrap;border-radius:999px;font-weight:700;letter-spacing:-.01em}
.pill svg{stroke-width:2.2;flex:none}
.pill.solid{background:linear-gradient(180deg,#22855F 0%,#0E4D3A 100%);color:#fff;
 box-shadow:inset 0 2px 0 rgba(255,255,255,.28),inset 0 -3px 8px rgba(0,0,0,.18),0 18px 40px rgba(8,48,31,.30),0 0 0 2px rgba(255,255,255,.08)}
.pill.white{background:linear-gradient(180deg,#FFFFFF,#F0F5F2);color:var(--g);
 box-shadow:inset 0 2px 0 #fff,0 18px 40px rgba(6,40,28,.22),0 0 0 2px rgba(14,77,58,.08)}
.pill.glass{background:linear-gradient(180deg,rgba(255,255,255,.26),rgba(255,255,255,.10));color:#fff;backdrop-filter:blur(14px);
 box-shadow:inset 0 1.5px 0 rgba(255,255,255,.45),0 18px 40px rgba(0,0,0,.25),0 0 0 1.5px rgba(255,255,255,.22)}
.chk{display:flex;align-items:center;justify-content:center;border-radius:50%;background:linear-gradient(180deg,#2FA375,#14674B);color:#fff;flex:none}
.chk svg{width:62%;height:62%;stroke-width:3.2}
/* card */
.card{position:absolute;border-radius:44px;background:linear-gradient(180deg,#FFFFFF,#F4F8F6);
 box-shadow:inset 0 2px 0 #fff,0 40px 90px rgba(6,40,28,.25),0 0 0 2px rgba(14,77,58,.07)}
.big{font-weight:900;letter-spacing:-.045em;line-height:.9;font-variant-numeric:tabular-nums}
.serif{font-family:'Instrument Serif',serif;font-style:italic;font-weight:400;letter-spacing:-.01em}
/* captions */
#caps{position:absolute;left:0;right:0;text-align:center;pointer-events:none}
#caps .ln{display:block;white-space:nowrap}
#caps .w{display:inline-block;margin:0 .13em}
.cap-face .w{font-weight:600;font-size:54px;color:#fff;letter-spacing:-.012em;
 text-shadow:0 2px 6px rgba(0,0,0,.55),0 0 26px rgba(0,0,0,.40)}
.cap-face .h{font-family:'Instrument Serif',serif;font-style:italic;font-weight:400;font-size:104px;line-height:.92;letter-spacing:-.01em;
 text-shadow:0 2px 8px rgba(0,0,0,.45),0 0 34px rgba(0,0,0,.35),0 0 60px rgba(156,240,200,.25)}
.cap-light .w{font-weight:800;font-size:60px;color:#fff;letter-spacing:-.02em;text-shadow:0 6px 22px rgba(0,0,0,.25)}
.cap-light .h{font-family:'Instrument Serif',serif;font-style:italic;font-weight:400;font-size:112px;line-height:.92}
.cap-dark .w{font-weight:800;font-size:60px;color:var(--ink);letter-spacing:-.02em}
.cap-dark .h{font-family:'Instrument Serif',serif;font-style:italic;font-weight:400;font-size:112px;line-height:.92;color:var(--g)}
/* phone */
.phone{position:absolute;border-radius:78px;background:#0C1311;padding:20px;box-shadow:0 50px 110px rgba(6,40,28,.35),inset 0 0 0 3px #2a3330}
.screen{position:absolute;inset:20px;border-radius:60px;background:#fff;overflow:hidden}
.blk{position:absolute;border-radius:16px;background:#E6EEEA}
.cta{position:absolute;display:flex;align-items:center;justify-content:center;gap:18px;border-radius:999px;font-weight:700;color:#fff;
 background:linear-gradient(180deg,#2A9A6F 0%,#16684C 55%,#0E4D3A 100%);
 box-shadow:inset 0 2px 0 rgba(255,255,255,.35),inset 0 -4px 10px rgba(0,0,0,.2),0 16px 40px rgba(0,0,0,.35),0 0 0 3px rgba(255,255,255,.18),0 0 40px rgba(46,170,120,.45)}
.notif{position:absolute;border-radius:34px;background:rgba(255,255,255,.96);display:flex;align-items:center;gap:22px;padding:22px 30px;
 box-shadow:0 26px 60px rgba(6,40,28,.28),0 0 0 2px rgba(14,77,58,.06);font-weight:600;color:var(--ink)}
.line{position:absolute;height:5px;border-radius:5px;background:rgba(255,255,255,.55);transform-origin:0 50%}
.line.g{background:rgba(14,77,58,.25)}
</style></head>
<body><div id="stage"></div>
<script>
const W=1080,H=1920;
const ICONS=window.ICONS||{};
const cl=(x,a=0,b=1)=>Math.min(b,Math.max(a,x));
const lerp=(a,b,p)=>a+(b-a)*p;
const E={out:t=>1-Math.pow(1-t,3),out5:t=>1-Math.pow(1-t,5),inout:t=>t<.5?4*t*t*t:1-Math.pow(-2*t+2,3)/2,
 back:t=>{const c1=1.5,c3=c1+1;return 1+c3*Math.pow(t-1,3)+c1*Math.pow(t-1,2)},in:t=>t*t*t};
const P=(t,t0,d)=>cl((t-t0)/d);
function svg(name){return ICONS[name]||''}
function el(tag,cls,parent,html){const e=document.createElement(tag);if(cls)e.className=cls;if(html!=null)e.innerHTML=html;(parent||document.getElementById('stage')).appendChild(e);return e}
function place(e,x,y,w,h){e.style.left=(x-(w||0)/2)+'px';e.style.top=(y-(h||0)/2)+'px';if(w)e.style.width=w+'px';if(h)e.style.height=h+'px'}
// generic appear/disappear: returns visible factor
function pop(e,t,t0,o={}){
 const d=o.d||.42, p=P(t,t0,d), pe=(o.ease||E.back)(p), pf=E.out(P(t,t0,d*.6));
 let op=pf, s=lerp(o.s0??.7,1,pe), y=lerp(o.y0??30,0,E.out(p)), b=lerp(o.b0??10,0,E.out(P(t,t0,d*.7)));
 if(o.t1!=null){const q=E.in(P(t,o.t1,o.d1||.28)); op*=1-q; s*=lerp(1,o.s1??.9,q); b+=q*(o.b1??10); y+=q*(o.y1??0)}
 const base=e.dataset.base||'';
 e.style.opacity=op; e.style.transform=`${base} translateY(${y}px) scale(${s*(o.k||1)})`; e.style.filter=b>.05?`blur(${b}px)`:'none';
 e.style.visibility=op<=0.001?'hidden':'visible'; return op}
function tile(parent,icon,x,y,size,dark){const e=el('div','tile'+(dark?' dark':''),parent,svg(icon));place(e,x,y,size,size);return e}
function pill(parent,cls,text,icon,x,y,fs,h){const e=el('div','pill '+cls,parent,(icon?svg(icon):'')+`<span>${text}</span>`);
 e.style.fontSize=fs+'px';e.style.height=h+'px';e.style.padding=`0 ${h*.5}px`;
 const s=e.querySelector('svg');if(s){s.style.width=fs*1.15+'px';s.style.height=fs*1.15+'px'}
 e.style.left='0px';e.style.top=(y-h/2)+'px';
 requestAnimationFrame(()=>{});const w=e.getBoundingClientRect().width;e.style.left=(x-w/2)+'px';return e}
function chk(parent,size){const e=el('div','chk',parent,svg('check'));e.style.width=e.style.height=size+'px';return e}
const STAR='<svg viewBox="0 0 100 100"><path fill="currentColor" d="M50 0 C53 32 68 47 100 50 C68 53 53 68 50 100 C47 68 32 53 0 50 C32 47 47 32 50 0Z"/></svg>';
function sparkle(parent,x,y,size,green){const g=el('div','abs',parent);g.style.left=x+'px';g.style.top=y+'px';
 const rays=[];for(let i=0;i<4;i++){const r=el('div','ray'+(green?' g':''),g);r.style.width=size*3+'px';r.style.left=(-size*1.5)+'px';r.style.top='-1.5px';r.dataset.rot=i*45+20;rays.push(r)}
 const s=el('div','star',g,STAR);s.style.width=s.style.height=size+'px';s.style.left=-size/2+'px';s.style.top=-size/2+'px';if(green)s.style.color='#1F7A5A';
 return {g,rays,s,update(t,t0){const p=E.out(P(t,t0,.6));const q=E.back(P(t,t0,.45));
  rays.forEach((r,i)=>{r.style.opacity=p*(.85-.15*i);r.style.transform=`rotate(${+r.dataset.rot+t*14}deg) scaleX(${p})`});
  s.style.opacity=P(t,t0,.2);s.style.transform=`scale(${q*(1+.06*Math.sin(t*5))}) rotate(${t*30}deg)`;g.style.visibility=t<t0?'hidden':'visible'}}}

/* ---------------- scene shell: circle reveal in, blur-zoom out ---------------- */
function shell(sc,kind){
 const root=el('div','scene bg-'+kind);const cam=el('div','cam',root);
 if(kind==='disc'||kind==='light')el('div','dots',cam);
 if(kind==='green'){el('div','sheen',root)}
 el('div','grain',root);
 sc.root=root;sc.cam=cam;return cam}
function shellUpdate(sc,t){
 const {t0,t1}=sc, r=sc.root;
 if(t<t0-0.001||t>=t1){r.style.display='none';return false}
 r.style.display='';
 const pin=sc.noReveal?1:E.out5(P(t,t0,.5)), rad=lerp(0,1500,pin);
 if(pin<1){const m=`radial-gradient(circle ${rad}px at 50% 46%, #000 ${Math.max(0,rad-90)}px, transparent ${rad}px)`;r.style.webkitMaskImage=m}
 else r.style.webkitMaskImage='none';
 const q=0; // hard cut out, on the cut of the footage
 r.style.opacity=1;r.style.filter='none';
 const life=P(t,t0,t1-t0);
 sc.cam.style.transform=`scale(${lerp(1.14,1,E.out5(P(t,t0,.7)))*lerp(1.0,0.965,life)*(1+q*.08)})`;
 return true}

/* ---------------- scene builders ---------------- */
const B={};
// disc with a center tile, optional strike, then pills
B.discTile=(sc)=>{const c=shell(sc,'disc');const a=sc.a;
 const disc=el('div','disc',c);place(disc,540,860,980,980);sc.disc=disc;
 sc.tiles=(a.tiles||[]).map(o=>({o,e:tile(c,o.icon,o.x??540,o.y??700,o.size??230),sp:o.spark?sparkle(c,(o.x??540)+(o.size??230)*.42,(o.y??700)-(o.size??230)*.42,70):null}));
 sc.pills=(a.pills||[]).map(o=>({o,e:pill(c,o.cls||'white',o.text,o.icon,o.x??540,o.y,o.fs||46,o.h||104)}));
 if(a.strike){sc.strike=el('div','abs',c);Object.assign(sc.strike.style,{height:'16px',borderRadius:'8px',background:'#fff',boxShadow:'0 6px 20px rgba(0,0,0,.3)',width:'360px',left:(540-180)+'px',top:'692px',transformOrigin:'50% 50%'})}
 if(a.counter){const k=el('div','abs big',c);Object.assign(k.style,{color:'#fff',fontSize:a.counter.fs+'px',width:'1080px',left:'0',textAlign:'center',top:a.counter.y+'px',textShadow:'0 12px 40px rgba(0,0,0,.25)'});sc.k=k;
  if(a.counter.sub){const s=el('div','abs',c);Object.assign(s.style,{color:'rgba(255,255,255,.9)',fontWeight:700,fontSize:'52px',width:'1080px',left:0,textAlign:'center',top:(a.counter.y+a.counter.fs*.95)+'px'});s.textContent=a.counter.sub;sc.ks=s}}
 if(a.slot){const s=el('div','card',c);place(s,a.slot.x,a.slot.y,a.slot.w,a.slot.h);s.dataset.base=`rotate(${a.slot.rot||0}deg)`;s.innerHTML=SLOT();sc.slot=s}
};
function SLOT(){let bars='';for(let i=0;i<9;i++){const h=30+Math.round(Math.abs(Math.sin(i*1.7))*60)+i*7;bars+=`<div style="position:absolute;bottom:40px;left:${40+i*42}px;width:28px;height:${h}px;border-radius:8px;background:linear-gradient(180deg,#2FA375,#0E4D3A)"></div>`}
 return `<div style="position:absolute;left:40px;top:34px;font-weight:700;color:#0B2A20;font-size:30px">Sprzedaż · dziś</div><div style="position:absolute;left:40px;top:76px;font-weight:900;color:#0E4D3A;font-size:58px;letter-spacing:-.03em">+16 000 zł</div>${bars}`}
B.discTile.u=(sc,t)=>{const a=sc.a;
 sc.tiles.forEach(({o,e,sp})=>{const op=pop(e,t,o.t,{s0:.4,t1:o.t1,s1:o.s1??.6});if(o.dimAt!=null){const q=E.out(P(t,o.dimAt,.35));e.style.opacity=op*(1-q*.55)} if(sp)sp.update(t,o.t+.15)});
 sc.pills.forEach(({o,e})=>pop(e,t,o.t,{s0:.75,y0:40,t1:o.t1}));
 if(sc.strike){const p=E.out(P(t,a.strike.t,.32));sc.strike.style.transform=`rotate(-35deg) scaleX(${p})`;sc.strike.style.top=((a.strike.y||700)-8)+'px';sc.strike.style.opacity=(p>0?1:0)*(a.strike.t1?1-P(t,a.strike.t1,.25):1)}
 if(sc.k){const c=a.counter;const p=E.inout(P(t,c.t,c.d||1.0));const v=Math.round(lerp(c.from||0,c.to,p));
  sc.k.textContent=(c.pre||'')+v.toLocaleString('pl-PL')+(c.suf||'');pop(sc.k,t,c.t-.1,{s0:.8,y0:20});sc.k.style.transform+=` scale(${1+.04*E.out(P(t,c.t+(c.d||1),.15))*(1-P(t,c.t+(c.d||1)+.15,.3))})`;if(sc.ks)pop(sc.ks,t,c.subT??c.t,{s0:.9,y0:20})}
 if(sc.slot)pop(sc.slot,t,a.slot.t,{s0:.85,y0:60});
};
// light background, vertical checklist card
B.checklist=(sc)=>{const c=shell(sc,sc.a.bg||'light');const a=sc.a;
 if(a.title){}
 const n=a.items.length, rowH=a.rowH||150, cardW=960, cardH=n*rowH+100, cx=540, cy=a.cy||820;
 const glow=el('div','abs',c);Object.assign(glow.style,{borderRadius:'50%',background:'radial-gradient(circle,rgba(31,122,90,.22),transparent 62%)'});place(glow,cx,cy,1500,1500);
 const card=el('div','card',c);place(card,cx,cy,cardW,cardH);sc.card=card;
 sc.rows=a.items.map((it,i)=>{const r=el('div','abs',card);Object.assign(r.style,{left:'60px',top:(50+i*rowH)+'px',height:rowH+'px',display:'flex',alignItems:'center',gap:'34px',width:(cardW-120)+'px'});
  const ic=el('div','tile',r,svg(it.icon));Object.assign(ic.style,{position:'relative',width:'128px',height:'128px',flex:'none'});
  const tx=el('div','',r,it.text);Object.assign(tx.style,{fontSize:(it.fs||58)+'px',fontWeight:750,color:'#0B2A20',letterSpacing:'-.02em',lineHeight:1.05,flex:'1'});
  const k=chk(r,80);if(a.noCheck)k.style.display='none';
  if(a.numbers){const nb=el('div','',ic,'');}
  if(i<n-1&&a.connector){const ln=el('div','abs',card);Object.assign(ln.style,{left:'121px',top:(50+i*rowH+rowH/2+64)+'px',width:'6px',height:(rowH-128)+'px',borderRadius:'3px',background:'linear-gradient(#2FA375,#0E4D3A)',transformOrigin:'50% 0'});it._ln=ln}
  return {it,r,ic,tx,k}});
};
B.checklist.u=(sc,t)=>{const a=sc.a;pop(sc.card,t,sc.t0+.12,{s0:.9,y0:80,ease:E.out5,d:.55});
 sc.rows.forEach(({it,r,ic,tx,k},i)=>{const op=pop(r,t,it.t,{s0:.96,y0:26,b0:8,ease:E.out,d:.4});pop(ic,t,it.t,{s0:.5,y0:0});pop(k,t,it.t+(it.kd??.35),{s0:.3,y0:0});
  if(it._ln){const p=E.inout(P(t,a.items[i+1].t-.35,.35));it._ln.style.transform=`scaleY(${p})`;it._ln.style.opacity=p>0?1:0}
  if(it.strike!=null){const q=E.out(P(t,it.strike,.3));tx.style.textDecoration=q>0?'line-through':'none';tx.style.textDecorationThickness='6px';tx.style.textDecorationColor='#C9372C';r.style.opacity=op*(1-q*.45)}})
};
// green bg orbit: center tile + satellites; highlight the latest
B.orbit=(sc)=>{const c=shell(sc,'green');const a=sc.a;
 sc.wm=(a.wm||[]).map((w,i)=>{const e=el('div','wm',c,svg(w.icon));place(e,w.x,w.y,w.s,w.s);e.dataset.r=w.r||0;return e});
 const ring=el('div','abs',c);Object.assign(ring.style,{border:'3px dashed rgba(255,255,255,.18)',borderRadius:'50%'});place(ring,540,a.cy||760,a.R*2,a.R*2);sc.ring=ring;
 sc.center=a.center?{o:a.center,e:tile(c,a.center.icon,540,a.cy||760,a.center.size||210)}:null;
 if(a.center&&a.center.spark)sc.csp=sparkle(c,540+80,(a.cy||760)-80,60);
 sc.sats=a.sats.map((s,i)=>{const ang=s.ang*Math.PI/180,x=540+Math.cos(ang)*a.R,y=(a.cy||760)+Math.sin(ang)*a.R;
  const ln=el('div','line',c);ln.style.left='540px';ln.style.top=(a.cy||760)+'px';ln.style.width=a.R+'px';ln.style.transform=`rotate(${s.ang}deg)`;
  const e=tile(c,s.icon,x,y,s.size||170);
  let lb=null;if(s.label){const up=Math.sin(ang)<-0.2;lb=pill(c,'white',s.label,null,Math.min(820,Math.max(260,x)),up?y-(s.size||170)/2-56:y+(s.size||170)/2+56,38,76)}
  return {s,e,ln,lb,x,y}});
};
B.orbit.u=(sc,t)=>{const a=sc.a;
 sc.wm.forEach((e,i)=>{e.style.transform=`translateY(${-t*8}px) rotate(${(+e.dataset.r)+t*2}deg)`});
 pop(sc.ring,t,sc.t0+.2,{s0:.6,y0:0,d:.8,ease:E.out});sc.ring.style.transform+=` rotate(${t*6}deg)`;
 if(sc.center)pop(sc.center.e,t,sc.center.o.t,{s0:.4});if(sc.csp)sc.csp.update(t,sc.center.o.t+.2);
 const last=sc.sats.reduce((m,x,i)=>t>=x.s.t?i:m,-1);
 sc.sats.forEach(({s,e,ln,lb},i)=>{const p=E.out(P(t,s.t-.15,.4));ln.style.transform=`rotate(${s.ang}deg) scaleX(${p})`;ln.style.opacity=p>0?1:0;
  const op=pop(e,t,s.t,{s0:.4});const hi=i===last?1:0;const k=lerp(1,hi?1.12:.86,E.out(P(t,s.t+.35,.4)));
  e.style.transform+=` scale(${i===last?1.0+.12*E.out(P(t,s.t,.5)):(t>=s.t?lerp(1.12,.86,E.out(P(t,sc.sats[Math.min(i+1,sc.sats.length-1)].s.t,.4))):1)})`;
  if(i<last)e.style.opacity=op*.75;
  if(lb)pop(lb,t,s.t+.18,{s0:.8,y0:20})})
};
// phone + sales page building + notifications + ads flying in
B.phone=(sc)=>{const c=shell(sc,'light');const a=sc.a;
 const ph=el('div','phone',c);place(ph,540,a.cy||800,560,1080);sc.ph=ph;const sc2=el('div','screen',ph);sc.scr=sc2;
 const mk=(x,y,w,h,bg)=>{const b=el('div','blk',sc2);Object.assign(b.style,{left:x+'px',top:y+'px',width:w+'px',height:h+'px'});if(bg)b.style.background=bg;return b};
 sc.blocks=[mk(30,90,460,300,'linear-gradient(135deg,#1F7A5A,#0E4D3A)'),mk(30,420,400,38),mk(30,474,300,38),mk(30,540,460,22,'#EEF3F0'),mk(30,574,420,22,'#EEF3F0'),mk(30,608,380,22,'#EEF3F0')];
 const prod=el('div','tile',sc.blocks[0],svg('book-open'));Object.assign(prod.style,{left:'150px',top:'70px',width:'160px',height:'160px'});
 const price=el('div','big',sc2,'17 zł');Object.assign(price.style,{position:'absolute',left:'30px',top:'660px',fontSize:'78px',color:'#0E4D3A'});sc.price=price;
 const btn=el('div','cta',sc2,'Kup teraz');Object.assign(btn.style,{left:'30px',top:'780px',width:'460px',height:'110px',fontSize:'40px'});sc.btn=btn;
 sc.notif=el('div','notif',c,`<div class="chk" style="width:64px;height:64px">${svg('check')}</div><div><div style="font-size:30px;font-weight:800">Nowe zamówienie</div><div style="font-size:26px;color:#4A6B5E">+17 zł · właśnie teraz</div></div>`);
 place(sc.notif,540,300,620,130);
 sc.ads=(a.ads||[]).map(o=>{const e=el('div','card',c,`<div style="position:absolute;inset:18px;border-radius:28px;background:linear-gradient(135deg,#2A8A66,#0E4D3A)"></div>`);place(e,o.x,o.y,o.w||230,o.h||300);e.dataset.base=`rotate(${o.rot||0}deg)`;
  const ic=el('div','tile',e,svg(o.icon));Object.assign(ic.style,{left:'50%',top:'50%',width:'110px',height:'110px',marginLeft:'-55px',marginTop:'-55px'});return {o,e}});
 sc.people=(a.people||[]).map(o=>{const e=el('div','chk',c,svg('user'));Object.assign(e.style,{width:'84px',height:'84px',position:'absolute'});place(e,o.x,o.y,84,84);return {o,e}});
};
B.phone.u=(sc,t)=>{const a=sc.a;pop(sc.ph,t,sc.t0+.1,{s0:.85,y0:120,ease:E.out5,d:.6});
 const sh=E.inout(P(t,a.shiftT??999,.6));sc.ph.style.transform+=` translateX(${-0*sh}px) scale(${1-.12*sh})`;
 sc.blocks.forEach((b,i)=>pop(b,t,a.buildT+i*.12,{s0:.9,y0:20,b0:4,ease:E.out,d:.35}));
 pop(sc.price,t,a.buildT+.8,{s0:.6,y0:10});pop(sc.btn,t,a.buildT+1.0,{s0:.6,y0:10});
 const pr=P(t,a.buyT,.18),pr2=P(t,a.buyT+.18,.2);sc.btn.style.transform+=` scale(${1-.08*pr+.08*pr2})`;
 pop(sc.notif,t,a.buyT+.2,{s0:.8,y0:-60,t1:a.notifT1});
 sc.ads.forEach(({o,e})=>pop(e,t,o.t,{s0:.5,y0:80}));
 sc.people.forEach(({o,e})=>{const p=E.out(P(t,o.t,.7));pop(e,t,o.t,{s0:.3,y0:0});e.style.transform+=` translate(${(540-o.x)*p*.0}px,0)`});
};
// green full: big icon + title + counter + pill (guarantee)
B.hero=(sc)=>{const c=shell(sc,'green');const a=sc.a;
 sc.wm=(a.wm||[]).map(w=>{const e=el('div','wm',c,svg(w.icon));place(e,w.x,w.y,w.s,w.s);e.dataset.r=w.r||0;return e});
 const glow=el('div','abs',c);Object.assign(glow.style,{width:'900px',height:'900px',borderRadius:'50%',background:'radial-gradient(circle,rgba(156,240,200,.28),transparent 60%)'});place(glow,540,a.iy||640,900,900);sc.glow=glow;
 sc.icon=tile(c,a.icon,540,a.iy||640,a.isize||260);sc.sp=sparkle(c,540+120,(a.iy||640)-120,80);
 sc.items=(a.items||[]).map(o=>{let e;if(o.kind==='pill')e=pill(c,o.cls||'white',o.text,o.icon,540,o.y,o.fs||46,o.h||104);
  else {e=el('div','abs '+(o.serif?'serif':'big'),c);Object.assign(e.style,{color:'#fff',fontSize:o.fs+'px',width:'1080px',left:0,textAlign:'center',top:(o.y-o.fs/2)+'px',textShadow:'0 12px 40px rgba(0,0,0,.25)'});e.textContent=o.text}
  return {o,e}});
};
B.hero.u=(sc,t)=>{const a=sc.a;sc.wm.forEach(e=>e.style.transform=`translateY(${-t*8}px) rotate(${(+e.dataset.r)+t*2}deg)`);
 pop(sc.icon,t,a.it??sc.t0+.15,{s0:.4});sc.sp.update(t,(a.it??sc.t0+.15)+.25);sc.glow.style.opacity=.6+.4*Math.sin(t*2.2);
 sc.items.forEach(({o,e})=>{pop(e,t,o.t,{s0:.75,y0:36});if(o.count){const p=E.inout(P(t,o.count.t,o.count.d||.6));e.textContent=Math.round(lerp(0,o.count.to,p))+(o.count.suf||'')}})
};

/* ---------------- face overlays ---------------- */
const O={};
O.tile=(ov)=>{const a=ov.a;ov.e=tile(null,a.icon,a.x,a.y,a.size||170,a.dark);ov.sp=a.spark?sparkle(document.getElementById('stage'),a.x+(a.size||170)*.42,a.y-(a.size||170)*.42,56):null;
 if(a.badge){ov.b=pill(null,'solid',a.badge,null,a.x,a.y+(a.size||170)/2+30,36,74)}};
O.tile.u=(ov,t)=>{const a=ov.a;pop(ov.e,t,ov.t0,{s0:.4,t1:ov.t1-.25});ov.e.style.transform+=` translateY(${Math.sin(t*2.4)*5}px) rotate(${Math.sin(t*1.7)*2}deg)`;
 if(ov.sp){ov.sp.update(t,ov.t0+.2);ov.sp.g.style.opacity=1-P(t,ov.t1-.25,.25)} if(ov.b)pop(ov.b,t,a.badgeT??ov.t0+.2,{s0:.7,y0:14,t1:ov.t1-.25})};
O.pills=(ov)=>{const a=ov.a;ov.ps=a.items.map(o=>({o,e:pill(null,o.cls||'white',o.text,o.icon,o.x,o.y,o.fs||40,o.h||86)}))};
O.pills.u=(ov,t)=>{ov.ps.forEach(({o,e})=>{pop(e,t,o.t,{s0:.7,y0:30,t1:ov.t1-.22});e.style.transform+=` translateY(${Math.sin(t*2+o.x)*3}px)`})};
O.price=(ov)=>{const a=ov.a;const c=el('div','card');place(c,a.x,a.y,a.w||520,a.h||250);ov.c=c;
 c.innerHTML=`<div class="big" style="position:absolute;left:0;right:0;top:${a.h?a.h*.16:40}px;text-align:center;color:#0E4D3A;font-size:${a.fs||150}px">${a.text}</div>`+(a.sub?`<div style="position:absolute;left:0;right:0;bottom:30px;text-align:center;color:#3F6B5B;font-weight:700;font-size:36px">${a.sub}</div>`:'');
 if(a.side){ov.s=tile(null,a.side,a.x+(a.w||520)/2+20,a.y-(a.h||250)/2+10,130);ov.sx=el('div','abs');Object.assign(ov.sx.style,{height:'10px',width:'170px',borderRadius:'6px',background:'#E0483A',boxShadow:'0 4px 14px rgba(0,0,0,.3)',transformOrigin:'0 50%'});ov.sx.style.left=(a.x+(a.w||520)/2+20-85)+'px';ov.sx.style.top=(a.y-(a.h||250)/2+5)+'px'}};
O.price.u=(ov,t)=>{const a=ov.a;pop(ov.c,t,ov.t0,{s0:.6,y0:40,t1:ov.t1-.25});ov.c.style.transform+=` rotate(${-2+Math.sin(t*1.6)}deg)`;
 if(ov.s){pop(ov.s,t,a.sideT,{s0:.4,t1:ov.t1-.25});const p=E.out(P(t,a.strikeT,.3));ov.sx.style.transform=`rotate(-30deg) scaleX(${p})`;ov.sx.style.opacity=(p>0?1:0)*(1-P(t,ov.t1-.25,.25))}};
O.cta=(ov)=>{const a=ov.a;const b=el('div','cta',null,`<span>${a.text}</span>${svg('arrow-down')}`);Object.assign(b.style,{fontSize:'44px',height:'118px'});
 b.querySelector('svg').style.cssText='width:46px;height:46px;stroke-width:2.6';place(b,a.x||540,a.y,a.w||560,118);ov.b=b};
O.cta.u=(ov,t)=>{pop(ov.b,t,ov.t0,{s0:.5,y0:30});const k=t>ov.t0+.6?1+.035*Math.max(0,Math.sin((t-ov.t0)*4.2)):1;ov.b.style.transform+=` scale(${k})`;
 const ar=ov.b.querySelector('svg');ar.style.transform=`translateY(${Math.max(0,Math.sin((t-ov.t0)*4.2))*8}px)`};
O.brand=(ov)=>{const a=ov.a;const b=el('div','pill glass',null,`<div class="tile dark" style="position:relative;width:76px;height:76px;border-radius:22px">${svg('sparkles')}</div><span>Cyfrowy Autopilot</span>`);
 Object.assign(b.style,{fontSize:'50px',height:'116px',padding:'0 44px 0 20px',fontWeight:800});b.style.background='linear-gradient(180deg,rgba(255,255,255,.95),rgba(240,246,243,.92))';b.style.color='#0E4D3A';
 b.style.left='0';b.style.top=(a.y-58)+'px';const w=b.getBoundingClientRect().width;b.style.left=(540-w/2)+'px';ov.b=b;ov.sp=sparkle(document.getElementById('stage'),540+w/2-30,a.y-60,50,true)};
O.brand.u=(ov,t)=>{pop(ov.b,t,ov.t0,{s0:.6,y0:30,t1:ov.t1-.25});ov.sp.update(t,ov.t0+.25);ov.sp.g.style.opacity=1-P(t,ov.t1-.25,.25)};
O.flow=(ov)=>{const a=ov.a;ov.items=a.items.map(o=>{let e;if(o.icon){e=tile(null,o.icon,o.x,o.y,o.size||150,o.dark)}else{e=el('div','abs');e.innerHTML=svg('arrow-right');e.style.color='#fff';e.style.filter='drop-shadow(0 4px 10px rgba(0,0,0,.4))';place(e,o.x,o.y,80,80);e.querySelector('svg').style.cssText='width:80px;height:80px;stroke-width:2.6'}
 let lb=null;if(o.label)lb=pill(null,'solid',o.label,null,o.x,o.y+(o.size||150)/2+34,32,66);return {o,e,lb}})};
O.flow.u=(ov,t)=>{ov.items.forEach(({o,e,lb})=>{pop(e,t,o.t,{s0:.5,t1:ov.t1-.25});if(lb)pop(lb,t,o.t+.15,{s0:.7,y0:10,t1:ov.t1-.25})})};

/* ---------------- captions ---------------- */
function buildCaps(spec){const box=el('div','',null);box.id='caps';return box}
function capState(spec,t){
 // scene override
 for(const s of spec.scenes){if(t>=s.t0&&t<s.t1){if(s.cap)return s.cap;return {mode:'hide'}}}
 for(const o of spec.overlays){if(o.cap&&t>=o.t0&&t<o.t1)return o.cap}
 return {mode:'face',y:spec.capY}}
let lastKey='';
function capsUpdate(spec,t){const box=document.getElementById('caps');const st=capState(spec,t);
 const blocks=spec.caps;let bi=-1;for(let i=0;i<blocks.length;i++){if(t>=blocks[i].t0-0.04)bi=i;else break}
 if(st.mode==='hide'||bi<0){box.style.visibility='hidden';return}
 const b=blocks[bi];if(st.hideIn&&st.hideIn.some(([a,z])=>t>=a&&t<z)){box.style.visibility='hidden';return}
 box.style.visibility='visible';const key=bi+'|'+st.mode;
 if(key!==lastKey){lastKey=key;box.className='cap-'+st.mode;box.innerHTML='';
  const lines=[[],[]];b.words.forEach(w=>lines[w.h&&b.words.some(x=>!x.h)?1:0].push(w));
  lines.filter(l=>l.length).forEach(l=>{const ln=el('span','ln',box);l.forEach(w=>{const s=el('span','w'+(w.h?' h':''),ln);s.textContent=w.d;s.dataset.t=w.t})})}
 box.style.top='0px';const hgt=box.getBoundingClientRect().height;box.style.top=((st.y??spec.capY)*H-hgt/2)+'px';
 box.querySelectorAll('.w').forEach(s=>{const p=P(t,+s.dataset.t-0.05,.16);const isH=s.classList.contains('h');
  s.style.opacity=E.out(p);s.style.transform=`translateY(${(1-E.out(p))*(isH?14:8)}px) scale(${isH?lerp(1.08,1,E.out(P(t,+s.dataset.t-.05,.35))):1})`;s.style.filter=p<1?`blur(${(1-p)*6}px)`:'none'})}

/* ---------------- main ---------------- */
let SPEC=null,SCN=[],OVS=[];
window.init=(spec)=>{SPEC=spec;
 SCN=spec.scenes.map(s=>{const sc={...s};B[s.type](sc);return sc});
 OVS=spec.overlays.map(o=>{const ov={...o};O[o.type](ov);return ov});
 buildCaps(spec);return true};
window.seek=(t)=>{
 SCN.forEach(sc=>{if(shellUpdate(sc,t))B[sc.type].u(sc,t)});
 OVS.forEach(ov=>{const on=t>=ov.t0-0.01&&t<ov.t1;const nodes=[ov.e,ov.b,ov.c,ov.s,ov.sx,ov.sp&&ov.sp.g,...(ov.ps||[]).map(x=>x.e),...(ov.items||[]).flatMap(x=>[x.e,x.lb])].filter(Boolean);
  nodes.forEach(n=>n.style.display=on?'':'none');if(on)O[ov.type].u(ov,t)});
 capsUpdate(SPEC,t);return true};
</script></body></html>
````


### `projekty/reklamy_CA/engine/render.mjs`

````javascript
// usage: node render.mjs SPEC.json OUTDIR [--from S] [--to S] [--frames 1,2,3 (seconds)] [--par 3]
// Renders the overlay layer (captions, plansze, overlays) as transparent 1080x1920 PNGs, one per frame.
import { createRequire } from 'module';
const req = createRequire(process.env.PW_ROOT || '/opt/node22/lib/node_modules/'); const { chromium } = req('playwright');
import fs from 'fs'; import path from 'path'; import { fileURLToPath } from 'url';
const here = path.dirname(fileURLToPath(import.meta.url));
const a = process.argv.slice(2);
const opt = (k, d) => { const i = a.indexOf(k); return i >= 0 ? a[i + 1] : d; };
const spec = JSON.parse(fs.readFileSync(a[0], 'utf8')); const out = a[1]; fs.mkdirSync(out, { recursive: true });
const fps = spec.fps || 30, N = Math.round(spec.dur * fps);
let frames;
if (opt('--frames')) frames = opt('--frames').split(',').map(s => Math.round(parseFloat(s) * fps));
else { const f0 = Math.round(parseFloat(opt('--from', 0)) * fps), f1 = Math.min(N, Math.round(parseFloat(opt('--to', spec.dur)) * fps)); frames = []; for (let i = f0; i < f1; i++) frames.push(i); }
const icons = {}; const idir = path.join(here, 'assets/icons');
for (const f of fs.readdirSync(idir)) icons[f.replace('.svg', '')] = fs.readFileSync(path.join(idir, f), 'utf8').replace(/<!--.*?-->/s, '').replace(/class="[^"]*"/, '').replace(/width="24"\s*height="24"/, '');
const par = parseInt(opt('--par', 3));
const browser = await chromium.launch({ executablePath: fs.existsSync('/opt/pw-browsers/chromium') ? undefined : undefined });
const t0 = Date.now(); let done = 0;
async function worker(k) {
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  page.on('pageerror', e => console.error('PAGEERR', e.message));
  await page.addInitScript(ic => { window.ICONS = ic; }, icons);
  await page.goto('file://' + (opt('--page') ? path.resolve(opt('--page')) : path.join(here, 'overlay.html')));
  await page.evaluate(async () => { await document.fonts.ready; });
  await page.evaluate(s => window.init(s), spec);
  await page.evaluate(async () => { await document.fonts.ready; });
  for (let j = k; j < frames.length; j += par) {
    const f = frames[j];
    await page.evaluate(t => window.seek(t), f / fps);
    await page.screenshot({ path: path.join(out, `f_${String(f).padStart(5, '0')}.png`), omitBackground: true });
    if (++done % 150 === 0) console.log(`${done}/${frames.length} ${((Date.now() - t0) / 1000).toFixed(0)}s`);
  }
  await page.close();
}
await Promise.all([...Array(par).keys()].map(worker));
await browser.close();
console.log(`rendered ${frames.length} frames in ${((Date.now() - t0) / 1000).toFixed(0)}s`);
````


### `projekty/reklamy_CA/engine/sheet.py`

````python
#!/usr/bin/env python3
"""Contact sheet: footage frame + overlay PNG for each rendered test frame. usage: sheet.py SPEC FRAMES_DIR OUT.jpg [cols]"""
import json, os, subprocess, sys, glob
import numpy as np, cv2
spec = json.load(open(sys.argv[1])); fd = sys.argv[2]; out = sys.argv[3]; cols = int(sys.argv[4]) if len(sys.argv) > 4 else 5
tiles = []
for p in sorted(glob.glob(os.path.join(fd, "f_*.png"))):
    f = int(os.path.basename(p)[2:7]); t = f / spec.get("fps", 30)
    vf = ("hflip," if spec.get("mirror") else "") + "scale=1080:1920"
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(t), "-i", spec["src"], "-frames:v", "1", "-vf", vf, "-f", "rawvideo", "-pix_fmt", "bgr24", "-"], capture_output=True).stdout
    fr = np.frombuffer(raw, np.uint8).reshape(1920, 1080, 3).astype(np.float32)
    ov = cv2.imread(p, cv2.IMREAD_UNCHANGED).astype(np.float32)
    al = ov[:, :, 3:4] / 255 if ov.shape[2] == 4 else np.ones_like(ov[:, :, :1])
    im = (ov[:, :, :3] * al + fr * (1 - al)).astype(np.uint8)
    im = cv2.resize(im, (360, 640), interpolation=cv2.INTER_AREA)
    cv2.putText(im, f"{t:.1f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, .9, (0, 0, 255), 2)
    tiles.append(im)
while len(tiles) % cols: tiles.append(np.zeros_like(tiles[0]))
rows = [np.hstack(tiles[i:i + cols]) for i in range(0, len(tiles), cols)]
cv2.imwrite(out, np.vstack(rows), [cv2.IMWRITE_JPEG_QUALITY, 85]); print(out)
````


### `projekty/reklamy_CA/engine/takes_from_words.py`

````python
#!/usr/bin/env python3
"""usage: takes_from_words.py CHUNKS.json SRC OUT_takes.json "s1-e1" "s2-e2" ...
each pair = start time of the first word and START time of the last word (as printed by chunks.py); end resolves to that word's end."""
import json, sys
ch = json.load(open(sys.argv[1])); words = [w for c in ch for w in c["words"]]
def find(t):
    return min(words, key=lambda w: abs(w["s"] - t))
takes = []
for p in sys.argv[4:]:
    s, e = map(float, p.split("-"))
    a, b = find(s), find(e)
    takes.append([a["s"], b["e"]]); print(f'{a["s"]:7.2f} {a["w"]!r:>16} .. {b["w"]!r:<16} {b["e"]:7.2f}')
json.dump({"src": sys.argv[2], "takes": takes}, open(sys.argv[3], "w"))
````


### `projekty/reklamy_CA/engine/assets/fonts/fmt6.css`

````css
@font-face {
  font-family: 'Anton';
  font-style: normal;
  font-weight: 400;
  font-display: swap;
  src: url(f6_1Ptgg87LROyAm3K9-C8QSw.woff2) format('woff2');
  unicode-range: U+0100-02BA, U+02BD-02C5, U+02C7-02CC, U+02CE-02D7, U+02DD-02FF, U+0304, U+0308, U+0329, U+1D00-1DBF, U+1E00-1E9F, U+1EF2-1EFF, U+2020, U+20A0-20AB, U+20AD-20C4, U+2113, U+2C60-2C7F, U+A720-A7FF;
}
@font-face {
  font-family: 'Anton';
  font-style: normal;
  font-weight: 400;
  font-display: swap;
  src: url(f6_1Ptgg87LROyAm3Kz-C8.woff2) format('woff2');
  unicode-range: U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD;
}
@font-face {
  font-family: 'Poppins';
  font-style: normal;
  font-weight: 500;
  font-display: swap;
  src: url(f6_pxiByp8kv8JHgFVrLGT9Z1JlFc-K.woff2) format('woff2');
  unicode-range: U+0100-02BA, U+02BD-02C5, U+02C7-02CC, U+02CE-02D7, U+02DD-02FF, U+0304, U+0308, U+0329, U+1D00-1DBF, U+1E00-1E9F, U+1EF2-1EFF, U+2020, U+20A0-20AB, U+20AD-20C4, U+2113, U+2C60-2C7F, U+A720-A7FF;
}
@font-face {
  font-family: 'Poppins';
  font-style: normal;
  font-weight: 500;
  font-display: swap;
  src: url(f6_pxiByp8kv8JHgFVrLGT9Z1xlFQ.woff2) format('woff2');
  unicode-range: U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD;
}
@font-face {
  font-family: 'Poppins';
  font-style: normal;
  font-weight: 600;
  font-display: swap;
  src: url(f6_pxiByp8kv8JHgFVrLEj6Z1JlFc-K.woff2) format('woff2');
  unicode-range: U+0100-02BA, U+02BD-02C5, U+02C7-02CC, U+02CE-02D7, U+02DD-02FF, U+0304, U+0308, U+0329, U+1D00-1DBF, U+1E00-1E9F, U+1EF2-1EFF, U+2020, U+20A0-20AB, U+20AD-20C4, U+2113, U+2C60-2C7F, U+A720-A7FF;
}
@font-face {
  font-family: 'Poppins';
  font-style: normal;
  font-weight: 600;
  font-display: swap;
  src: url(f6_pxiByp8kv8JHgFVrLEj6Z1xlFQ.woff2) format('woff2');
  unicode-range: U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD;
}
````


### `projekty/reklamy_CA/engine/assets/fonts/g.css`

````css
/* latin-ext */
@font-face {
  font-family: 'Instrument Serif';
  font-style: italic;
  font-weight: 400;
  font-display: swap;
  src: url(b721f6676b.woff2) format('woff2');
  unicode-range: U+0100-02BA, U+02BD-02C5, U+02C7-02CC, U+02CE-02D7, U+02DD-02FF, U+0304, U+0308, U+0329, U+1D00-1DBF, U+1E00-1E9F, U+1EF2-1EFF, U+2020, U+20A0-20AB, U+20AD-20C4, U+2113, U+2C60-2C7F, U+A720-A7FF;
}
/* latin */
@font-face {
  font-family: 'Instrument Serif';
  font-style: italic;
  font-weight: 400;
  font-display: swap;
  src: url(3dfbf70c14.woff2) format('woff2');
  unicode-range: U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD;
}
/* latin-ext */
@font-face {
  font-family: 'Instrument Serif';
  font-style: normal;
  font-weight: 400;
  font-display: swap;
  src: url(0f695a654c.woff2) format('woff2');
  unicode-range: U+0100-02BA, U+02BD-02C5, U+02C7-02CC, U+02CE-02D7, U+02DD-02FF, U+0304, U+0308, U+0329, U+1D00-1DBF, U+1E00-1E9F, U+1EF2-1EFF, U+2020, U+20A0-20AB, U+20AD-20C4, U+2113, U+2C60-2C7F, U+A720-A7FF;
}
/* latin */
@font-face {
  font-family: 'Instrument Serif';
  font-style: normal;
  font-weight: 400;
  font-display: swap;
  src: url(5884f5d073.woff2) format('woff2');
  unicode-range: U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD;
}
/* cyrillic-ext */
@font-face {
  font-family: 'Inter';
  font-style: normal;
  font-weight: 400;
  font-display: swap;
  src: url(390b907766.woff2) format('woff2');
  unicode-range: U+0460-052F, U+1C80-1C8A, U+20B4, U+2DE0-2DFF, U+A640-A69F, U+FE2E-FE2F;
}
/* cyrillic */
@font-face {
  font-family: 'Inter';
  font-style: normal;
  font-weight: 400;
  font-display: swap;
  src: url(d4047416a6.woff2) format('woff2');
  unicode-range: U+0301, U+0400-045F, U+0490-0491, U+04B0-04B1, U+2116;
}
/* greek-ext */
@font-face {
  font-family: 'Inter';
  font-style: normal;
  font-weight: 400;
  font-display: swap;
  src: url(a656acc858.woff2) format('woff2');
  unicode-range: U+1F00-1FFF;
}
/* greek */
@font-face {
  font-family: 'Inter';
  font-style: normal;
  font-weight: 400;
  font-display: swap;
  src: url(9f07a5502c.woff2) format('woff2');
  unicode-range: U+0370-0377, U+037A-037F, U+0384-038A, U+038C, U+038E-03A1, U+03A3-03FF;
}
/* vietnamese */
@font-face {
  font-family: 'Inter';
  font-style: normal;
  font-weight: 400;
  font-display: swap;
  src: url(0583c36d6d.woff2) format('woff2');
  unicode-range: U+0102-0103, U+0110-0111, U+0128-0129, U+0168-0169, U+01A0-01A1, U+01AF-01B0, U+0300-0301, U+0303-0304, U+0308-0309, U+0323, U+0329, U+1EA0-1EF9, U+20AB;
}
/* latin-ext */
@font-face {
  font-family: 'Inter';
  font-style: normal;
  font-weight: 400;
  font-display: swap;
  src: url(ba68014684.woff2) format('woff2');
  unicode-range: U+0100-02BA, U+02BD-02C5, U+02C7-02CC, U+02CE-02D7, U+02DD-02FF, U+0304, U+0308, U+0329, U+1D00-1DBF, U+1E00-1E9F, U+1EF2-1EFF, U+2020, U+20A0-20AB, U+20AD-20C4, U+2113, U+2C60-2C7F, U+A720-A7FF;
}
/* latin */
@font-face {
  font-family: 'Inter';
  font-style: normal;
  font-weight: 400;
  font-display: swap;
  src: url(1fab01e7b4.woff2) format('woff2');
  unicode-range: U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD;
}
/* cyrillic-ext */
@font-face {
  font-family: 'Inter';
  font-style: normal;
  font-weight: 500;
  font-display: swap;
  src: url(390b907766.woff2) format('woff2');
  unicode-range: U+0460-052F, U+1C80-1C8A, U+20B4, U+2DE0-2DFF, U+A640-A69F, U+FE2E-FE2F;
}
/* cyrillic */
@font-face {
  font-family: 'Inter';
  font-style: normal;
  font-weight: 500;
  font-display: swap;
  src: url(d4047416a6.woff2) format('woff2');
  unicode-range: U+0301, U+0400-045F, U+0490-0491, U+04B0-04B1, U+2116;
}
/* greek-ext */
@font-face {
  font-family: 'Inter';
  font-style: normal;
  font-weight: 500;
  font-display: swap;
  src: url(a656acc858.woff2) format('woff2');
  unicode-range: U+1F00-1FFF;
}
/* greek */
@font-face {
  font-family: 'Inter';
  font-style: normal;
  font-weight: 500;
  font-display: swap;
  src: url(9f07a5502c.woff2) format('woff2');
  unicode-range: U+0370-0377, U+037A-037F, U+0384-038A, U+038C, U+038E-03A1, U+03A3-03FF;
}
/* vietnamese */
@font-face {
  font-family: 'Inter';
  font-style: normal;
  font-weight: 500;
  font-display: swap;
  src: url(0583c36d6d.woff2) format('woff2');
  unicode-range: U+0102-0103, U+0110-0111, U+0128-0129, U+0168-0169, U+01A0-01A1, U+01AF-01B0, U+0300-0301, U+0303-0304, U+0308-0309, U+0323, U+0329, U+1EA0-1EF9, U+20AB;
}
/* latin-ext */
@font-face {
  font-family: 'Inter';
  font-style: normal;
  font-weight: 500;
  font-display: swap;
  src: url(ba68014684.woff2) format('woff2');
  unicode-range: U+0100-02BA, U+02BD-02C5, U+02C7-02CC, U+02CE-02D7, U+02DD-02FF, U+0304, U+0308, U+0329, U+1D00-1DBF, U+1E00-1E9F, U+1EF2-1EFF, U+2020, U+20A0-20AB, U+20AD-20C4, U+2113, U+2C60-2C7F, U+A720-A7FF;
}
/* latin */
@font-face {
  font-family: 'Inter';
  font-style: normal;
  font-weight: 500;
  font-display: swap;
  src: url(1fab01e7b4.woff2) format('woff2');
  unicode-range: U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD;
}
/* cyrillic-ext */
@font-face {
  font-family: 'Inter';
  font-style: normal;
  font-weight: 600;
  font-display: swap;
  src: url(390b907766.woff2) format('woff2');
  unicode-range: U+0460-052F, U+1C80-1C8A, U+20B4, U+2DE0-2DFF, U+A640-A69F, U+FE2E-FE2F;
}
/* cyrillic */
@font-face {
  font-family: 'Inter';
  font-style: normal;
  font-weight: 600;
  font-display: swap;
  src: url(d4047416a6.woff2) format('woff2');
  unicode-range: U+0301, U+0400-045F, U+0490-0491, U+04B0-04B1, U+2116;
}
/* greek-ext */
@font-face {
  font-family: 'Inter';
  font-style: normal;
  font-weight: 600;
  font-display: swap;
  src: url(a656acc858.woff2) format('woff2');
  unicode-range: U+1F00-1FFF;
}
/* greek */
@font-face {
  font-family: 'Inter';
  font-style: normal;
  font-weight: 600;
  font-display: swap;
  src: url(9f07a5502c.woff2) format('woff2');
  unicode-range: U+0370-0377, U+037A-037F, U+0384-038A, U+038C, U+038E-03A1, U+03A3-03FF;
}
/* vietnamese */
@font-face {
  font-family: 'Inter';
  font-style: normal;
  font-weight: 600;
  font-display: swap;
  src: url(0583c36d6d.woff2) format('woff2');
  unicode-range: U+0102-0103, U+0110-0111, U+0128-0129, U+0168-0169, U+01A0-01A1, U+01AF-01B0, U+0300-0301, U+0303-0304, U+0308-0309, U+0323, U+0329, U+1EA0-1EF9, U+20AB;
}
/* latin-ext */
@font-face {
  font-family: 'Inter';
  font-style: normal;
  font-weight: 600;
  font-display: swap;
  src: url(ba68014684.woff2) format('woff2');
  unicode-range: U+0100-02BA, U+02BD-02C5, U+02C7-02CC, U+02CE-02D7, U+02DD-02FF, U+0304, U+0308, U+0329, U+1D00-1DBF, U+1E00-1E9F, U+1EF2-1EFF, U+2020, U+20A0-20AB, U+20AD-20C4, U+2113, U+2C60-2C7F, U+A720-A7FF;
}
/* latin */
@font-face {
  font-family: 'Inter';
  font-style: normal;
  font-weight: 600;
  font-display: swap;
  src: url(1fab01e7b4.woff2) format('woff2');
  unicode-range: U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD;
}
/* cyrillic-ext */
@font-face {
  font-family: 'Inter';
  font-style: normal;
  font-weight: 700;
  font-display: swap;
  src: url(390b907766.woff2) format('woff2');
  unicode-range: U+0460-052F, U+1C80-1C8A, U+20B4, U+2DE0-2DFF, U+A640-A69F, U+FE2E-FE2F;
}
/* cyrillic */
@font-face {
  font-family: 'Inter';
  font-style: normal;
  font-weight: 700;
  font-display: swap;
  src: url(d4047416a6.woff2) format('woff2');
  unicode-range: U+0301, U+0400-045F, U+0490-0491, U+04B0-04B1, U+2116;
}
/* greek-ext */
@font-face {
  font-family: 'Inter';
  font-style: normal;
  font-weight: 700;
  font-display: swap;
  src: url(a656acc858.woff2) format('woff2');
  unicode-range: U+1F00-1FFF;
}
/* greek */
@font-face {
  font-family: 'Inter';
  font-style: normal;
  font-weight: 700;
  font-display: swap;
  src: url(9f07a5502c.woff2) format('woff2');
  unicode-range: U+0370-0377, U+037A-037F, U+0384-038A, U+038C, U+038E-03A1, U+03A3-03FF;
}
/* vietnamese */
@font-face {
  font-family: 'Inter';
  font-style: normal;
  font-weight: 700;
  font-display: swap;
  src: url(0583c36d6d.woff2) format('woff2');
  unicode-range: U+0102-0103, U+0110-0111, U+0128-0129, U+0168-0169, U+01A0-01A1, U+01AF-01B0, U+0300-0301, U+0303-0304, U+0308-0309, U+0323, U+0329, U+1EA0-1EF9, U+20AB;
}
/* latin-ext */
@font-face {
  font-family: 'Inter';
  font-style: normal;
  font-weight: 700;
  font-display: swap;
  src: url(ba68014684.woff2) format('woff2');
  unicode-range: U+0100-02BA, U+02BD-02C5, U+02C7-02CC, U+02CE-02D7, U+02DD-02FF, U+0304, U+0308, U+0329, U+1D00-1DBF, U+1E00-1E9F, U+1EF2-1EFF, U+2020, U+20A0-20AB, U+20AD-20C4, U+2113, U+2C60-2C7F, U+A720-A7FF;
}
/* latin */
@font-face {
  font-family: 'Inter';
  font-style: normal;
  font-weight: 700;
  font-display: swap;
  src: url(1fab01e7b4.woff2) format('woff2');
  unicode-range: U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD;
}
/* cyrillic-ext */
@font-face {
  font-family: 'Inter';
  font-style: normal;
  font-weight: 800;
  font-display: swap;
  src: url(390b907766.woff2) format('woff2');
  unicode-range: U+0460-052F, U+1C80-1C8A, U+20B4, U+2DE0-2DFF, U+A640-A69F, U+FE2E-FE2F;
}
/* cyrillic */
@font-face {
  font-family: 'Inter';
  font-style: normal;
  font-weight: 800;
  font-display: swap;
  src: url(d4047416a6.woff2) format('woff2');
  unicode-range: U+0301, U+0400-045F, U+0490-0491, U+04B0-04B1, U+2116;
}
/* greek-ext */
@font-face {
  font-family: 'Inter';
  font-style: normal;
  font-weight: 800;
  font-display: swap;
  src: url(a656acc858.woff2) format('woff2');
  unicode-range: U+1F00-1FFF;
}
/* greek */
@font-face {
  font-family: 'Inter';
  font-style: normal;
  font-weight: 800;
  font-display: swap;
  src: url(9f07a5502c.woff2) format('woff2');
  unicode-range: U+0370-0377, U+037A-037F, U+0384-038A, U+038C, U+038E-03A1, U+03A3-03FF;
}
/* vietnamese */
@font-face {
  font-family: 'Inter';
  font-style: normal;
  font-weight: 800;
  font-display: swap;
  src: url(0583c36d6d.woff2) format('woff2');
  unicode-range: U+0102-0103, U+0110-0111, U+0128-0129, U+0168-0169, U+01A0-01A1, U+01AF-01B0, U+0300-0301, U+0303-0304, U+0308-0309, U+0323, U+0329, U+1EA0-1EF9, U+20AB;
}
/* latin-ext */
@font-face {
  font-family: 'Inter';
  font-style: normal;
  font-weight: 800;
  font-display: swap;
  src: url(ba68014684.woff2) format('woff2');
  unicode-range: U+0100-02BA, U+02BD-02C5, U+02C7-02CC, U+02CE-02D7, U+02DD-02FF, U+0304, U+0308, U+0329, U+1D00-1DBF, U+1E00-1E9F, U+1EF2-1EFF, U+2020, U+20A0-20AB, U+20AD-20C4, U+2113, U+2C60-2C7F, U+A720-A7FF;
}
/* latin */
@font-face {
  font-family: 'Inter';
  font-style: normal;
  font-weight: 800;
  font-display: swap;
  src: url(1fab01e7b4.woff2) format('woff2');
  unicode-range: U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD;
}
/* cyrillic-ext */
@font-face {
  font-family: 'Inter';
  font-style: normal;
  font-weight: 900;
  font-display: swap;
  src: url(390b907766.woff2) format('woff2');
  unicode-range: U+0460-052F, U+1C80-1C8A, U+20B4, U+2DE0-2DFF, U+A640-A69F, U+FE2E-FE2F;
}
/* cyrillic */
@font-face {
  font-family: 'Inter';
  font-style: normal;
  font-weight: 900;
  font-display: swap;
  src: url(d4047416a6.woff2) format('woff2');
  unicode-range: U+0301, U+0400-045F, U+0490-0491, U+04B0-04B1, U+2116;
}
/* greek-ext */
@font-face {
  font-family: 'Inter';
  font-style: normal;
  font-weight: 900;
  font-display: swap;
  src: url(a656acc858.woff2) format('woff2');
  unicode-range: U+1F00-1FFF;
}
/* greek */
@font-face {
  font-family: 'Inter';
  font-style: normal;
  font-weight: 900;
  font-display: swap;
  src: url(9f07a5502c.woff2) format('woff2');
  unicode-range: U+0370-0377, U+037A-037F, U+0384-038A, U+038C, U+038E-03A1, U+03A3-03FF;
}
/* vietnamese */
@font-face {
  font-family: 'Inter';
  font-style: normal;
  font-weight: 900;
  font-display: swap;
  src: url(0583c36d6d.woff2) format('woff2');
  unicode-range: U+0102-0103, U+0110-0111, U+0128-0129, U+0168-0169, U+01A0-01A1, U+01AF-01B0, U+0300-0301, U+0303-0304, U+0308-0309, U+0323, U+0329, U+1EA0-1EF9, U+20AB;
}
/* latin-ext */
@font-face {
  font-family: 'Inter';
  font-style: normal;
  font-weight: 900;
  font-display: swap;
  src: url(ba68014684.woff2) format('woff2');
  unicode-range: U+0100-02BA, U+02BD-02C5, U+02C7-02CC, U+02CE-02D7, U+02DD-02FF, U+0304, U+0308, U+0329, U+1D00-1DBF, U+1E00-1E9F, U+1EF2-1EFF, U+2020, U+20A0-20AB, U+20AD-20C4, U+2113, U+2C60-2C7F, U+A720-A7FF;
}
/* latin */
@font-face {
  font-family: 'Inter';
  font-style: normal;
  font-weight: 900;
  font-display: swap;
  src: url(1fab01e7b4.woff2) format('woff2');
  unicode-range: U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD;
}
````


### `projekty/reklamy_CA/engine/assets/fonts/montserrat.css`

````css
@font-face {
  font-family: 'Montserrat';
  font-style: normal;
  font-weight: 700;
  font-display: swap;
  src: url(mont_JTUSjIg1_i6t8kCHKm459Wdhyzbi.woff2) format('woff2');
  unicode-range: U+0100-02BA, U+02BD-02C5, U+02C7-02CC, U+02CE-02D7, U+02DD-02FF, U+0304, U+0308, U+0329, U+1D00-1DBF, U+1E00-1E9F, U+1EF2-1EFF, U+2020, U+20A0-20AB, U+20AD-20C4, U+2113, U+2C60-2C7F, U+A720-A7FF;
}
@font-face {
  font-family: 'Montserrat';
  font-style: normal;
  font-weight: 700;
  font-display: swap;
  src: url(mont_JTUSjIg1_i6t8kCHKm459Wlhyw.woff2) format('woff2');
  unicode-range: U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD;
}
@font-face {
  font-family: 'Montserrat';
  font-style: normal;
  font-weight: 800;
  font-display: swap;
  src: url(mont_JTUSjIg1_i6t8kCHKm459Wdhyzbi.woff2) format('woff2');
  unicode-range: U+0100-02BA, U+02BD-02C5, U+02C7-02CC, U+02CE-02D7, U+02DD-02FF, U+0304, U+0308, U+0329, U+1D00-1DBF, U+1E00-1E9F, U+1EF2-1EFF, U+2020, U+20A0-20AB, U+20AD-20C4, U+2113, U+2C60-2C7F, U+A720-A7FF;
}
@font-face {
  font-family: 'Montserrat';
  font-style: normal;
  font-weight: 800;
  font-display: swap;
  src: url(mont_JTUSjIg1_i6t8kCHKm459Wlhyw.woff2) format('woff2');
  unicode-range: U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD;
}
````


### `projekty/reklamy_CA/engine/assets/fonts/poppins.css`

````css
@font-face {
  font-family: 'Poppins';
  font-style: normal;
  font-weight: 700;
  font-display: swap;
  src: url(pop_pxiByp8kv8JHgFVrLCz7Z1JlFc-K.woff2) format('woff2');
  unicode-range: U+0100-02BA, U+02BD-02C5, U+02C7-02CC, U+02CE-02D7, U+02DD-02FF, U+0304, U+0308, U+0329, U+1D00-1DBF, U+1E00-1E9F, U+1EF2-1EFF, U+2020, U+20A0-20AB, U+20AD-20C4, U+2113, U+2C60-2C7F, U+A720-A7FF;
}
@font-face {
  font-family: 'Poppins';
  font-style: normal;
  font-weight: 700;
  font-display: swap;
  src: url(pop_pxiByp8kv8JHgFVrLCz7Z1xlFQ.woff2) format('woff2');
  unicode-range: U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD;
}
@font-face {
  font-family: 'Poppins';
  font-style: normal;
  font-weight: 800;
  font-display: swap;
  src: url(pop_pxiByp8kv8JHgFVrLDD4Z1JlFc-K.woff2) format('woff2');
  unicode-range: U+0100-02BA, U+02BD-02C5, U+02C7-02CC, U+02CE-02D7, U+02DD-02FF, U+0304, U+0308, U+0329, U+1D00-1DBF, U+1E00-1E9F, U+1EF2-1EFF, U+2020, U+20A0-20AB, U+20AD-20C4, U+2113, U+2C60-2C7F, U+A720-A7FF;
}
@font-face {
  font-family: 'Poppins';
  font-style: normal;
  font-weight: 800;
  font-display: swap;
  src: url(pop_pxiByp8kv8JHgFVrLDD4Z1xlFQ.woff2) format('woff2');
  unicode-range: U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD;
}
````


### `projekty/styl2/build_spec2.py`

````python
#!/usr/bin/env python3
"""Style-2 render specs for add7fixed and ads10.
usage: build_spec2.py WORKDIR STOCKDIR  (WORKDIR: add7fixed.mp4, ads10.mp4, tr_a7f.json, tr_ads10.json) -> spec2_<name>.json"""
import difflib, json, os, re, subprocess, sys
WD, ST = sys.argv[1], sys.argv[2]
HERE = os.path.dirname(os.path.abspath(__file__))
WEAK = {"i", "w", "z", "na", "do", "od", "po", "a", "o", "że", "bo", "się", "to", "jak", "czy", "nie", "co", "za", "ci", "ten", "tego"}
GRADE = ("eq=contrast=0.95:saturation=0.86,colorbalance=rs=0.05:gs=0.01:bs=-0.04:rm=0.03:bm=-0.02:rh=0.02:bh=-0.03,"
         "curves=all='0/0.035 0.25/0.235 0.75/0.775 1/0.975',vignette=angle=PI/5")
norm = lambda t: re.sub(r"[^\w]", "", t.lower())


def align(words, fixed):
    toks = []
    for raw in fixed.split():
        h = raw.startswith("*"); parts = raw.strip("*").split("_")
        for k, p in enumerate(parts): toks.append({"d": p, "h": h, "join": k > 0})
    a = [norm(w["w"]) for w in words]; b = [norm(t["d"]) for t in toks]; times = [None] * len(toks)
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        if op == "equal":
            for k in range(i2 - i1): times[j1 + k] = words[i1 + k]["s"]
        elif op == "replace":
            s0, e0 = words[i1]["s"], words[i2 - 1]["e"]
            for j in range(j1, j2): times[j] = s0 + (e0 - s0) * (j - j1) / max(1, j2 - j1)
    for j in range(len(toks)):
        if times[j] is None: times[j] = next((times[k] for k in range(j - 1, -1, -1) if times[k] is not None), 0.0)
    for j, t in enumerate(toks): t["t"] = round(times[j], 3)
    return toks


def chunk(units, maxw=4, maxc=22):
    blocks, cur = [], []
    def flush():
        if cur: blocks.append(cur[:]); cur.clear()
    for u in units:
        clen = sum(len(x["d"]) + 1 for x in cur) + len(u["d"])
        if cur and not u["join"] and (len(cur) >= maxw or clen > maxc):
            carry = []
            while len(cur) > 1 and (cur[-1]["d"].lower().strip(",.?") in WEAK or cur[-1]["d"].isdigit()):
                carry.insert(0, cur.pop())
            flush(); cur.extend(carry)
        cur.append(u)
        if u["d"].endswith((".", "?", "!")): flush()
    flush()
    return [{"t0": b[0]["t"], "words": [{"d": w["d"], "t": w["t"], "h": w["h"]} for w in b]} for b in blocks]


def dur(p):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p], capture_output=True, text=True).stdout)


def cuts(p):
    return json.loads(subprocess.run([sys.executable, os.path.join(HERE, "..", "reklamy_CA", "engine", "cuts.py"), p], capture_output=True, text=True).stdout)


def W(text, t0, step=0.0):
    """plansza words: 'a *b* c' -> list with times (given explicitly as list) """
    return text


def pw(spec_words):
    """[(word, t, accent)] -> plansza words"""
    return [{"d": w, "t": t, "h": h} for w, t, h in spec_words]


def make(name, src, trname, fixed, items, brolls, capY, hide, end):
    srcp = os.path.join(WD, src); sd = round(dur(srcp), 3); cs = cuts(srcp)
    words = [w for s in json.load(open(os.path.join(WD, trname))) for w in s["words"]]
    caps = chunk(align(words, fixed))
    z, big = [], False
    for t in [0.0] + cs:
        z.append([t, 1.12 if big else 1.0]); big = not big
    for b in brolls: b["file"] = os.path.join(ST, b["file"] + ".mp4")
    total = round(sd + 2.5, 3)
    items = items + [dict(type="end", t0=sd, t1=total, hideCaps=True, **end)]
    spec = dict(src=srcp, srcDur=sd, dur=total, fps=30, capY=capY, capHide=hide, caps=caps, items=items, brolls=brolls,
                cuts=cs, zooms=z, zoomCenter=[0.5, 0.3], grade=GRADE)
    p = os.path.join(WD, f"spec2_{name}.json"); json.dump(spec, open(p, "w"), ensure_ascii=False, indent=1)
    print(p, len(caps), "caption blocks,", len(cs), "cuts")
    for b in caps: print(f'  {b["t0"]:6.2f}  ' + " ".join(("*" + w["d"] + "*") if w["h"] else w["d"] for w in b["words"]))


END = dict(brand="Cyfrowy Autopilot", tag="Od pomysłu do produktu cyfrowego z AI", button="Zobacz, jak zacząć")

# ------------------------------------------------------------------ ADS7 (add7fixed, 62.2 s)
FIX7 = ("Zastanawiałeś się kiedyś, skąd ci wszyscy ludzie w internecie właściwie biorą pieniądze? Bo przecież nie dostają ich "
        "tylko za siedzenie przed komputerem. Przez kolejne 40 sekund pokażę Ci jeden z *najprostszych_modeli,* który możesz "
        "zacząć już dzisiaj. Wyobraź sobie, że ktoś tworzy poradnik z 30 szybkimi obiadami dla zapracowanych osób. Wystawia go "
        "na sprzedaż za *49_zł,* a następnie publikuje krótkie filmiki AI z przepisami, które przyciągają zainteresowanych ludzi. "
        "Czyli ktoś ogląda filmik, wchodzi na stronę i jeśli poradnik rozwiązuje jego problem, to może go kupić. I *39_zł* trafia "
        "na konto. A produkt nadal może zostać sprzedany kolejnej i kolejnej osobie. Więc nie musisz zamawiać nowego towaru, nie "
        "musisz pakować paczek i nie musisz tworzyć produktu od nowa dla każdego możliwego klienta. I na tym polega właśnie biznes "
        "na produktach cyfrowych. I teraz wyobraź sobie, że AI pomaga Ci stworzyć cały taki produkt, napisać stronę sprzedażową i "
        "przygotować filmiki do jego promocji. Brzmi to znacznie prościej niż otwieranie tradycyjnego sklepu, e-commerce czy "
        "dropshippingu, prawda? I właśnie dlatego stworzyłem *Cyfrowy_Autopilot.* System, który pokazuje Ci, jak przygotować taki "
        "biznes z pomocą sztucznej inteligencji. Od pomysłu przez gotowy produkt, aż po stronę sprzedażową i plan zdobywania "
        "klientów. Więc zamiast dalej zastanawiać się, jak ludzie zarabiają w internecie, po prostu kliknij poniżej i zobacz, jak "
        "możesz zacząć budować *własny_produkt_cyfrowy.*")
IT7 = [
    dict(type="hero", t0=2.6, t1=3.767, y=0.55, small="właściwie biorą", big="pieniądze?", size=170, bigT=3.30, hideCaps=True),
    dict(type="fan", t0=14.7, t1=16.47, x=300, y=1660, dx=230, w=270, h=370, hideCaps=False, cards=[
        dict(title="30 szybkich obiadów", sub="dla zapracowanych", icon="chef-hat", price="49 zł", t=14.68),
        dict(title="Przepisy na 15 minut", sub="e-book PDF", icon="book-open", bg="linear-gradient(160deg,#E8F7FB,#BFE9F2)", t=14.80),
        dict(title="Lista zakupów", sub="na cały tydzień", icon="shopping-bag", bg="linear-gradient(160deg,#F7FCFD,#D6EFF5)", t=14.92)]),
    dict(type="tiles", t0=21.0, t1=26.8, y=1430, size=150, gap=110, items=[
        dict(icon="play", label="ogląda filmik", t=21.02), dict(icon="globe", label="wchodzi na stronę", t=21.78),
        dict(icon="shopping-cart", label="kupuje", t=24.70)]),
    dict(type="notif", t0=25.1, t1=26.8, y=330, title="Nowa płatność", sub="Poradnik: 30 szybkich obiadów", amount="+39 zł"),
    dict(type="plansza", t0=35.267, t1=37.75, hideCaps=True, y0=820, fs=74, rows=[dict(words=pw([
        ("I", 35.36, 0), ("na", 35.48, 0), ("tym", 35.54, 0), ("polega", 35.64, 0), ("właśnie", 35.94, 0), ("biznes", 36.24, 0),
        ("na", 36.48, 1), ("produktach", 36.64, 1), ("cyfrowych.", 37.0, 1)]))]),
    dict(type="plansza", t0=37.75, t1=42.9, hideCaps=True, y0=820, gap=230, fs=64, rows=[
        dict(y=520, fs=54, words=pw([("Wyobraź", 37.82, 0), ("sobie,", 38.10, 0), ("że", 38.38, 0), ("AI", 38.46, 1), ("pomaga", 38.70, 0),
                                     ("Ci", 38.94, 0), ("stworzyć:", 39.06, 0)])),
        dict(num=1, t=39.86, y=820, words=pw([("Produkt", 39.86, 0), ("cyfrowy", 40.0, 1)])),
        dict(num=2, t=40.64, y=1050, words=pw([("Strona", 40.64, 0), ("sprzedażowa", 40.8, 1)])),
        dict(num=3, t=41.68, y=1280, words=pw([("Filmiki", 41.68, 0), ("promocyjne", 41.9, 1)]))]),
    dict(type="fan", t0=48.1, t1=52.43, x=300, y=1660, dx=230, w=270, h=370, cards=[
        dict(title="Moduł 1: Pomysł", sub="AI znajduje niszę", icon="lightbulb", bg="linear-gradient(160deg,#0F2A31,#0B1A1E)", ink="#fff", ink2="#8fb4bc", t=48.14),
        dict(title="Moduł 2: Produkt", sub="e-book z AI", icon="book-open", bg="linear-gradient(160deg,#0F2A31,#0B1A1E)", ink="#fff", ink2="#8fb4bc", t=48.30),
        dict(title="Moduł 3: Sprzedaż", sub="strona + reklamy", icon="trending-up", bg="linear-gradient(160deg,#0F2A31,#0B1A1E)", ink="#fff", ink2="#8fb4bc", t=48.46)]),
    dict(type="tiles", t0=52.433, t1=55.933, y=1430, size=140, gap=60, items=[
        dict(num="1", label="pomysł", t=52.62), dict(num="2", label="produkt", t=53.58), dict(num="3", label="strona", t=54.24), dict(num="4", label="klienci", t=54.96)]),
    dict(type="cta", t0=59.06, t1=62.3, y=1400, text="Kliknij poniżej"),
]
BR7 = [dict(t0=4.36, t1=6.467, file="typing_0", ss=2.0), dict(t0=12.6, t1=14.66, file="cooking_2", ss=1.0),
       dict(t0=17.0, t1=18.95, file="scroll_2", ss=3.0), dict(t0=30.24, t1=31.42, file="warehouse_0", ss=1.5),
       dict(t0=31.42, t1=32.46, file="packing_0", ss=2.0), dict(t0=44.1, t1=46.3, file="store_1", ss=4.0),
       dict(t0=56.48, t1=58.3, file="thinking_0", ss=3.0)]

# ------------------------------------------------------------------ ADS10 (95.6 s)
FIX10 = ("Każdy wie, że największą okazją na zarabianie przez internet w 2026 roku jest sztuczna inteligencja i w 2027 będzie to "
         "jeszcze bardziej aktualne, ale większość ludzi kompletnie nie rozumie, jak ją wykorzystać. I nie chodzi mi tutaj o "
         "zadawanie pytań ChatGPT czy generowanie śmiesznych obrazków. Mówię o wykorzystaniu AI, żeby pomogło Ci wykonać pracę "
         "potrzebną do stworzenia *własnego_biznesu_online.* I tutaj moim zdaniem pojawia się jedna z największych okazji: "
         "połączenie AI z produktami cyfrowymi. Wyobraź sobie, że zaczynasz od kompletnego zera. Nie masz pomysłu na biznes, nie "
         "jesteś ekspertem ani nie jesteś znany, więc wykorzystujesz AI, żeby znaleźć pomysł na produkt, na który istnieje "
         "zapotrzebowanie. Następnie AI pomaga Ci przeanalizować rynek, sprawdzić, kim są Twoi potencjalni klienci i jakie problemy "
         "próbują rozwiązać. I na tej podstawie pomaga Ci stworzyć produkt cyfrowy, który odpowiada na konkretną potrzebę. Potem "
         "pomaga Ci zbudować stronę, na której możesz go sprzedawać, a na koniec przygotować filmiki, posty i reklamy, które mogą "
         "przyciągać do niego potencjalnych klientów. I nagle teraz, zamiast kolejnych 100 magicznych promptów, masz coś, co "
         "faktycznie możesz *wystawić_na_sprzedaż.* I teraz najlepsze, bo produkty cyfrowe istnieją od kilkunastu lat, sam "
         "sprzedaję od ponad trzech lat, a w najlepszym dniu sprzedałem 941 e-booków. Ale AI kompletnie zmieniło to, jak łatwo "
         "można dzisiaj zacząć. Kiedyś musiałeś nauczyć się wielu różnych umiejętności albo płacić innym, żeby wykonali tę pracę za "
         "Ciebie, a dzisiaj sztuczna inteligencja może Ci w tym wszystkim pomóc. I właśnie dlatego stworzyłem *Cyfrowy_Autopilot,* "
         "gotowy system, w którym pokazuję Ci krok po kroku, jak przejść od kompletnego zera do własnego produktu cyfrowego i "
         "strony gotowej do sprzedaży. I to wszystko bez szczególnego doświadczenia i bez pokazywania twarzy. Aktualnie możesz "
         "otrzymać dostęp do całego systemu za jedyne 17 złotych. Więc teraz masz dwie opcje. Możesz dalej pytać AI, jak zarabiać "
         "pieniądze przez internet, albo możesz w końcu wykorzystać je do stworzenia czegoś, za co inni ludzie mogą zapłacić. "
         "Więc kliknij przycisk poniżej i zacznij budować swój pierwszy produkt cyfrowy z AI jeszcze dzisiaj.")


def step(n, t0, t1, wl):
    return dict(type="plansza", t0=t0, t1=t1, hideCaps=True, y0=820, fs=70, numSize=230, textX=360,
                rows=[dict(num=n, t=t0 + .05, words=pw(wl))])


IT10 = [
    dict(type="hero", t0=4.0, t1=5.133, y=0.52, small="jest", big="sztuczna<br>inteligencja", size=140, bigT=4.20, hideCaps=True),
    dict(type="plansza", t0=20.40, t1=23.533, hideCaps=True, y0=760, fs=96, rows=[
        dict(y=600, fs=56, words=pw([("Jedna", 20.48, 0), ("z", 20.72, 0), ("największych", 20.84, 0), ("okazji:", 21.20, 1)])),
        dict(y=760, words=pw([("AI", 22.10, 0), ("+", 22.44, 0), ("produkty", 22.62, 1), ("cyfrowe", 22.80, 1)]))]),
    step(1, 28.16, 32.167, [("Pomysł,", 29.88, 0), ("na", 30.68, 0), ("który", 30.80, 0), ("jest", 31.0, 0), ("zapotrzebowanie", 31.40, 1)]),
    step(2, 32.167, 34.6, [("Analiza", 33.38, 0), ("rynku", 33.94, 1), ("i", 34.1, 1), ("klientów", 34.2, 1)]),
    step(3, 37.633, 41.433, [("Produkt", 39.12, 0), ("cyfrowy", 39.40, 1)]),
    step(4, 41.433, 43.9, [("Strona", 42.48, 0), ("sprzedażowa", 43.40, 1)]),
    dict(type="notif", t0=50.6, t1=52.733, y=330, title="Nowa sprzedaż", sub="Twój produkt cyfrowy", amount="+79 zł", icon="banknote"),
    dict(type="hero", t0=57.4, t1=59.067, y=0.50, small="w najlepszym dniu", big="941", size=280, bigT=57.82, sub="e-booków", subT=58.3, hideCaps=True),
    dict(type="fan", t0=70.1, t1=73.4, x=300, y=1660, dx=230, w=270, h=370, cards=[
        dict(title="Moduł 1: Pomysł", sub="AI znajduje niszę", icon="lightbulb", bg="linear-gradient(160deg,#0F2A31,#0B1A1E)", ink="#fff", ink2="#8fb4bc", t=70.12),
        dict(title="Moduł 2: Produkt", sub="e-book z AI", icon="book-open", bg="linear-gradient(160deg,#0F2A31,#0B1A1E)", ink="#fff", ink2="#8fb4bc", t=70.30),
        dict(title="Moduł 3: Sprzedaż", sub="strona + reklamy", icon="trending-up", bg="linear-gradient(160deg,#0F2A31,#0B1A1E)", ink="#fff", ink2="#8fb4bc", t=70.48)]),
    dict(type="tiles", t0=77.9, t1=80.433, y=1430, size=150, gap=330, items=[
        dict(icon="check", label="bez doświadczenia", t=78.0), dict(icon="check", label="bez pokazywania twarzy", t=79.42)]),
    dict(type="hero", t0=82.6, t1=83.833, y=0.52, small="za jedyne", big="17 zł", size=260, bigT=83.04, hideCaps=True),
    step(1, 84.9, 87.933, [("Dalej", 85.24, 0), ("pytać", 85.56, 0), ("AI,", 85.86, 0), ("jak", 86.32, 1), ("zarabiać", 86.44, 1)]),
    step(2, 87.933, 91.833, [("Stworzyć", 89.50, 0), ("coś,", 89.84, 0), ("za", 90.30, 1), ("co", 90.30, 1), ("ludzie", 90.76, 1), ("zapłacą", 90.92, 1)]),
    dict(type="cta", t0=92.10, t1=95.7, y=1400, text="Kliknij poniżej"),
]
BR10 = [dict(t0=8.48, t1=10.7, file="confused_1", ss=5.0), dict(t0=11.72, t1=13.2, file="aichat_0", ss=4.0),
        dict(t0=13.2, t1=14.633, file="aiimage_1", ss=2.0), dict(t0=24.28, t1=25.42, file="blank_0", ss=3.0),
        dict(t0=44.36, t1=46.1, file="filming_2", ss=2.0), dict(t0=62.32, t1=64.7, file="office_1", ss=4.0)]

make("ads7", "add7fixed.mp4", "tr_a7f.json", FIX7, IT7, BR7, 0.6, [], END)
make("ads10", "ads10.mp4", "tr_ads10.json", FIX10, IT10, BR10, 0.6, [], END)
````


### `projekty/styl2/run2.sh`

````bash
#!/bin/bash
# style-2 full render: run2.sh WORKDIR STOCKDIR [names...]
set -e
D=$1; S=$2; shift 2; H=$(cd "$(dirname "$0")" && pwd)
python3 $H/build_spec2.py $D $S > /dev/null
for n in ${@:-ads7 ads10}; do
  rm -rf $D/f2_$n
  node $H/../reklamy_CA/engine/render.mjs $D/spec2_$n.json $D/f2_$n --page $H/engine/overlay2.html --par 3
  python3 $H/engine/compose2.py $D/spec2_$n.json $D/f2_$n $D/${n}_STYL2.mp4
  ffmpeg -v error -y -i $D/${n}_STYL2.mp4 -vf scale=540:-2 -c:v libx264 -crf 28 -preset fast -c:a aac -b:a 96k -movflags +faststart $D/${n}_STYL2_tel.mp4
  echo "DONE $n"
done
````


### `projekty/styl2/stock_index.json`

````json
{
 "typing_0": {
  "id": 34771072,
  "url": "https://www.pexels.com/video/typing-in-dimly-lit-room-on-laptop-34771072/",
  "author": "Anh Nguyen",
  "dur": 12,
  "w": 1080,
  "h": 1920
 },
 "typing_1": {
  "id": 8480685,
  "url": "https://www.pexels.com/video/close-up-video-of-a-person-using-a-laptop-8480685/",
  "author": "ArtHouse Studio",
  "dur": 38,
  "w": 1080,
  "h": 1920
 },
 "typing_2": {
  "id": 34124550,
  "url": "https://www.pexels.com/video/hands-typing-fast-on-a-laptop-keyboard-34124550/",
  "author": "MELQUIZEDEQUE ALMEIDA",
  "dur": 15,
  "w": 1080,
  "h": 1920
 },
 "cooking_0": {
  "id": 8231548,
  "url": "https://www.pexels.com/video/a-person-cooking-eggs-8231548/",
  "author": "ArtHouse Studio",
  "dur": 9,
  "w": 1080,
  "h": 1920
 },
 "cooking_1": {
  "id": 3704774,
  "url": "https://www.pexels.com/video/flipping-a-pancake-from-the-pan-using-fork-3704774/",
  "author": "cottonbro studio",
  "dur": 28,
  "w": 1080,
  "h": 2048
 },
 "cooking_2": {
  "id": 10432188,
  "url": "https://www.pexels.com/video/a-person-cooking-seafood-10432188/",
  "author": "RDNE Stock project",
  "dur": 7,
  "w": 1080,
  "h": 1920
 },
 "scroll_0": {
  "id": 17512949,
  "url": "https://www.pexels.com/video/girl-using-her-phone-device-inside-of-a-hipster-coffee-shop-17512949/",
  "author": "Nathan J Hilton",
  "dur": 12,
  "w": 1080,
  "h": 1920
 },
 "scroll_1": {
  "id": 10374888,
  "url": "https://www.pexels.com/video/close-up-on-man-hand-scrolling-phone-gallery-10374888/",
  "author": "RDNE Stock project",
  "dur": 8,
  "w": 1080,
  "h": 1920
 },
 "scroll_2": {
  "id": 38410501,
  "url": "https://www.pexels.com/video/scrolling-through-social-media-on-smartphone-38410501/",
  "author": "Hamim Rony",
  "dur": 21,
  "w": 1080,
  "h": 1920
 },
 "warehouse_0": {
  "id": 6169086,
  "url": "https://www.pexels.com/video/packages-on-shelves-6169086/",
  "author": "Tima Miroshnichenko",
  "dur": 10,
  "w": 1080,
  "h": 1920
 },
 "warehouse_1": {
  "id": 6169102,
  "url": "https://www.pexels.com/video/brown-cardboard-courier-boxes-6169102/",
  "author": "Tima Miroshnichenko",
  "dur": 18,
  "w": 1080,
  "h": 1920
 },
 "warehouse_2": {
  "id": 7019176,
  "url": "https://www.pexels.com/video/woman-looking-at-camera-7019176/",
  "author": "cottonbro studio",
  "dur": 37,
  "w": 1080,
  "h": 2048
 },
 "packing_0": {
  "id": 6342201,
  "url": "https://www.pexels.com/video/woman-sealing-box-with-a-tape-6342201/",
  "author": "Liza Summer",
  "dur": 10,
  "w": 1080,
  "h": 1920
 },
 "packing_1": {
  "id": 7308367,
  "url": "https://www.pexels.com/video/a-man-taping-a-box-7308367/",
  "author": "RDNE Stock project",
  "dur": 7,
  "w": 1080,
  "h": 1920
 },
 "packing_2": {
  "id": 7205557,
  "url": "https://www.pexels.com/video/a-person-packing-a-box-7205557/",
  "author": "SHVETS production",
  "dur": 5,
  "w": 1080,
  "h": 1920
 },
 "store_0": {
  "id": 30703758,
  "url": "https://www.pexels.com/video/cosplay-character-shopping-for-instant-noodles-30703758/",
  "author": "TBD Tuy\u00ean",
  "dur": 14,
  "w": 1080,
  "h": 1920
 },
 "store_1": {
  "id": 6649434,
  "url": "https://www.pexels.com/video/crio-person-browsing-on-store-6649434/",
  "author": "cottonbro studio",
  "dur": 30,
  "w": 1080,
  "h": 2048
 },
 "store_2": {
  "id": 6025287,
  "url": "https://www.pexels.com/video/two-women-checking-the-mug-on-display-6025287/",
  "author": "Pavel Danilyuk",
  "dur": 14,
  "w": 1080,
  "h": 1920
 },
 "thinking_0": {
  "id": 6804127,
  "url": "https://www.pexels.com/video/man-sitting-on-an-office-chair-while-using-a-cellphone-6804127/",
  "author": "cottonbro studio",
  "dur": 21,
  "w": 1080,
  "h": 2048
 },
 "thinking_1": {
  "id": 7690126,
  "url": "https://www.pexels.com/video/man-celebrating-a-birthday-alone-7690126/",
  "author": "Polina Tankilevitch",
  "dur": 13,
  "w": 1080,
  "h": 1920
 },
 "thinking_2": {
  "id": 9460260,
  "url": "https://www.pexels.com/video/a-man-sitting-on-a-bench-with-his-phone-9460260/",
  "author": "Mike Jones",
  "dur": 10,
  "w": 1080,
  "h": 1920
 },
 "confused_0": {
  "id": 4874628,
  "url": "https://www.pexels.com/video/a-young-teenage-boy-using-a-laptop-4874628/",
  "author": "Antoni Shkraba",
  "dur": 13,
  "w": 1066,
  "h": 1920
 },
 "confused_1": {
  "id": 7597572,
  "url": "https://www.pexels.com/video/tired-man-working-at-home-7597572/",
  "author": "MART  PRODUCTION",
  "dur": 43,
  "w": 1080,
  "h": 2048
 },
 "confused_2": {
  "id": 6322165,
  "url": "https://www.pexels.com/video/man-using-laptop-6322165/",
  "author": "Tima Miroshnichenko",
  "dur": 11,
  "w": 1080,
  "h": 1920
 },
 "aichat_0": {
  "id": 7439142,
  "url": "https://www.pexels.com/video/people-talking-through-chat-7439142/",
  "author": "cottonbro studio",
  "dur": 34,
  "w": 1080,
  "h": 2048
 },
 "aichat_1": {
  "id": 10374892,
  "url": "https://www.pexels.com/video/close-up-on-man-hands-typing-on-laptop-10374892/",
  "author": "RDNE Stock project",
  "dur": 9,
  "w": 1080,
  "h": 1920
 },
 "aichat_2": {
  "id": 34124550,
  "url": "https://www.pexels.com/video/hands-typing-fast-on-a-laptop-keyboard-34124550/",
  "author": "MELQUIZEDEQUE ALMEIDA",
  "dur": 15,
  "w": 1080,
  "h": 1920
 },
 "aiimage_0": {
  "id": 18069831,
  "url": "https://www.pexels.com/video/an-artist-s-animation-of-artificial-intelligence-ai-this-video-depicts-agi-artificial-general-intelligence-s-potential-to-enrich-lives-it-was-created-by-xk-studio-as-part-of-the-visu-18069831/",
  "author": "Google DeepMind",
  "dur": 15,
  "w": 1080,
  "h": 1920
 },
 "aiimage_1": {
  "id": 25935017,
  "url": "https://www.pexels.com/video/an-artist-s-illustration-of-artificial-intelligence-ai-this-image-explores-how-ai-can-be-for-sustainability-efforts-it-was-created-by-dada-projects-as-part-of-the-visualising-ai-projec-25935017/",
  "author": "Google DeepMind",
  "dur": 16,
  "w": 1080,
  "h": 1920
 },
 "aiimage_2": {
  "id": 16456781,
  "url": "https://www.pexels.com/video/the-cover-of-the-book-the-art-of-the-modular-16456781/",
  "author": "Pachon in Motion",
  "dur": 16,
  "w": 1080,
  "h": 1920
 },
 "blank_0": {
  "id": 6185247,
  "url": "https://www.pexels.com/video/open-notebook-6185247/",
  "author": "KATRIN  BOLOVTSOVA",
  "dur": 19,
  "w": 1080,
  "h": 2048
 },
 "blank_1": {
  "id": 40101486,
  "url": "https://www.pexels.com/video/notebook-pages-fluttering-by-the-ocean-40101486/",
  "author": "Tanita Lupa",
  "dur": 5,
  "w": 1080,
  "h": 1920
 },
 "blank_2": {
  "id": 7744342,
  "url": "https://www.pexels.com/video/close-up-video-of-notebooks-7744342/",
  "author": "MART  PRODUCTION",
  "dur": 17,
  "w": 1080,
  "h": 2048
 },
 "filming_0": {
  "id": 6325290,
  "url": "https://www.pexels.com/video/a-man-talking-while-being-recorded-6325290/",
  "author": "Vanessa Garcia",
  "dur": 10,
  "w": 1080,
  "h": 1920
 },
 "filming_1": {
  "id": 13929670,
  "url": "https://www.pexels.com/video/woman-preparing-to-vlog-13929670/",
  "author": "Mizuno K",
  "dur": 10,
  "w": 1080,
  "h": 1920
 },
 "filming_2": {
  "id": 13929657,
  "url": "https://www.pexels.com/video/a-smartphone-on-a-tripod-filming-a-woman-putting-earrings-on-13929657/",
  "author": "Mizuno K",
  "dur": 10,
  "w": 1080,
  "h": 1920
 },
 "office_0": {
  "id": 9305619,
  "url": "https://www.pexels.com/video/a-tired-man-crumpling-a-piece-of-paper-9305619/",
  "author": "Monstera Production",
  "dur": 29,
  "w": 1080,
  "h": 2048
 },
 "office_1": {
  "id": 8468478,
  "url": "https://www.pexels.com/video/man-sitting-on-chair-tired-of-his-job-8468478/",
  "author": "cottonbro studio",
  "dur": 23,
  "w": 1080,
  "h": 2048
 },
 "office_2": {
  "id": 8731296,
  "url": "https://www.pexels.com/video/exhausted-man-working-at-the-office-8731296/",
  "author": "Mikhail Nilov",
  "dur": 15,
  "w": 1080,
  "h": 1920
 }
}
````


### `projekty/styl2/engine/compose2.py`

````python
#!/usr/bin/env python3
"""Style 2 compositor: graded footage (+per-shot zoom) with b-roll inserts, overlay PNGs on top, end card tail.
usage: compose2.py SPEC.json FRAMES_DIR OUT.mp4 [--preview]
spec: src, dur (total incl. end card), srcDur, cuts, zooms [[t,scale]], zoomCenter, brolls [{t0,t1,file,ss}], grade (ffmpeg filter)"""
import json, os, subprocess, sys
import numpy as np, cv2
a = sys.argv[1:]; spec = json.load(open(a[0])); fdir = a[1]; out = a[2]
W, H, fps = 1080, 1920, spec.get("fps", 30)
N = round(spec["dur"] * fps); NS = round(spec["srcDur"] * fps)
grade = spec.get("grade", "")
zooms = sorted(spec.get("zooms", [])); cx, cy = spec.get("zoomCenter", [0.5, 0.36])
def scale_at(t):
    s = 1.0
    for zt, zs in zooms:
        if zt <= t: s = zs
    return s
def dec(src, ss=0.0, vf=""):
    chain = f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={fps}" + ("," + vf if vf else "")
    return subprocess.Popen(["ffmpeg", "-v", "error", "-ss", f"{ss:.3f}", "-i", src, "-vf", chain, "-f", "rawvideo", "-pix_fmt", "bgr24", "-"], stdout=subprocess.PIPE)
main = dec(spec["src"], 0, grade)
brolls = sorted(spec.get("brolls", []), key=lambda b: b["t0"]); bdec = {}
crf = "23" if "--preview" in a else "17"
enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", str(fps), "-i", "-",
                        "-i", spec["src"], "-map", "0:v", "-map", "1:a", "-af", f"apad,atrim=0:{spec['dur']:.3f}",
                        "-c:v", "libx264", "-preset", "medium", "-crf", crf, "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
                        "-t", f"{spec['dur']:.3f}", "-movflags", "+faststart", out], stdin=subprocess.PIPE)
fsz = W * H * 3; last = np.zeros((H, W, 3), np.uint8)
for f in range(N):
    t = f / fps
    if f < NS:
        buf = main.stdout.read(fsz)
        fr = np.frombuffer(buf, np.uint8).reshape(H, W, 3) if len(buf) == fsz else last
        last = fr
        s = scale_at(t)
        if s > 1.001:
            w, h = W / s, H / s
            x0 = min(max(cx * W - w / 2, 0), W - w); y0 = min(max(cy * H - h / 2, 0), H - h)
            fr = cv2.warpAffine(fr, np.float32([[s, 0, -x0 * s], [0, s, -y0 * s]]), (W, H), flags=cv2.INTER_LINEAR)
    else:
        fr = np.zeros((H, W, 3), np.uint8)
    for k, b in enumerate(brolls):
        if b["t0"] <= t < b["t1"]:
            if k not in bdec: bdec[k] = dec(b["file"], b.get("ss", 0), grade)
            if not bdec[k]: continue
            bb = bdec[k].stdout.read(fsz)
            if len(bb) == fsz:
                fr = np.frombuffer(bb, np.uint8).reshape(H, W, 3)
                ks = 1.04 + 0.05 * (t - b["t0"]) / max(.1, b["t1"] - b["t0"])          # slow push-in on b-roll
                fr = cv2.warpAffine(fr, np.float32([[ks, 0, -(ks - 1) * W / 2], [0, ks, -(ks - 1) * H / 2]]), (W, H))
        elif t >= b["t1"] and bdec.get(k):
            bdec[k].terminate(); bdec[k] = False
    p = os.path.join(fdir, f"f_{f:05d}.png")
    ov = cv2.imread(p, cv2.IMREAD_UNCHANGED) if os.path.exists(p) else None
    if ov is not None:
        al = ov[:, :, 3:4].astype(np.float32) / 255.0 if ov.shape[2] == 4 else np.ones(ov.shape[:2] + (1,), np.float32)
        if al.max() > 0:
            fr = (ov[:, :, :3].astype(np.float32) * al + fr.astype(np.float32) * (1 - al)).astype(np.uint8)
    enc.stdin.write(np.ascontiguousarray(fr).tobytes())
enc.stdin.close(); enc.wait(); main.terminate()
print("wrote", out)
````


### `projekty/styl2/engine/overlay2.html`

````html
<!doctype html>
<html><head><meta charset="utf-8">
<link rel="stylesheet" href="../../reklamy_CA/engine/assets/fonts/g.css">
<style>
:root{--t1:#9EEBFF;--t2:#35C2DA;--t3:#0E8FA8;--bg:#0C1214;--ink:#0B1A1E}
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:1080px;height:1920px;background:transparent;overflow:hidden}
#stage{position:absolute;inset:0;font-family:Inter,sans-serif;-webkit-font-smoothing:antialiased}
.abs{position:absolute}
/* captions */
#caps{position:absolute;left:60px;right:60px;text-align:center;pointer-events:none}
#caps .w{display:inline-block;margin:0 .12em;font-weight:600;font-size:50px;color:#fff;letter-spacing:-.015em;
 text-shadow:0 1px 2px rgba(0,0,0,.85),0 3px 10px rgba(0,0,0,.75),0 0 30px rgba(0,0,0,.5)}
#caps .w.h{font-family:'Instrument Serif',serif;font-style:italic;font-weight:400;font-size:62px;color:var(--t1);letter-spacing:0;
 text-shadow:0 1px 2px rgba(0,0,0,.8),0 3px 12px rgba(0,0,0,.7),0 0 32px rgba(0,0,0,.45)}
#caps.dark .w{text-shadow:none}
/* hero word */
.hero{position:absolute;left:0;right:0;text-align:center}
.hero .sm{font-weight:600;font-size:46px;color:#fff;text-shadow:0 1px 2px rgba(0,0,0,.85),0 3px 10px rgba(0,0,0,.75),0 0 30px rgba(0,0,0,.5)}
.hero .bg{font-weight:900;letter-spacing:-.05em;line-height:.92}
/* shadow lives on .bs (appear() owns .bg's filter); gradient restarts on every line via box-decoration-break */
.hero .bs{filter:drop-shadow(0 0 2px rgba(0,0,0,.75)) drop-shadow(0 6px 10px rgba(0,0,0,.6)) drop-shadow(0 14px 44px rgba(0,0,0,.7))}
.hero .bt{background:linear-gradient(180deg,var(--g1,#9DC3F7) 8%,var(--g2,#007A7C) 92%);-webkit-box-decoration-break:clone;box-decoration-break:clone;
 -webkit-background-clip:text;background-clip:text;color:transparent}
/* plansza */
.pl{position:absolute;inset:0;background:var(--bg);overflow:hidden}
.pl .c{position:absolute;border-radius:50%;background:radial-gradient(circle at 30% 30%,#D8F8FF 0%,#8FE2F0 30%,#3FB9D0 62%,#14879F 100%);filter:saturate(.85)}
.pl .num{position:absolute;font-weight:900;color:#fff;letter-spacing:-.06em;line-height:.8}
.pl .txt{position:absolute;font-weight:700;color:#fff;letter-spacing:-.02em;line-height:1.08}
.pl .txt .h{font-family:'Instrument Serif',serif;font-style:italic;font-weight:400;color:var(--t1);letter-spacing:0;font-size:1.12em}
.pl .wd{display:inline-block;margin-right:.24em}
.pl .grain,.grain{position:absolute;inset:0;opacity:.06;mix-blend-mode:overlay;
 background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='300' height='300'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2' stitchTiles='stitch'/></filter><rect width='300' height='300' filter='url(%23n)'/></svg>")}
/* fan cards */
.fan{position:absolute;perspective:1600px}
.card{position:absolute;border-radius:22px;overflow:hidden;box-shadow:0 30px 60px rgba(0,0,0,.45),0 0 0 2px rgba(255,255,255,.35);transform-origin:50% 100%}
/* glass tile */
.gt{position:absolute;display:flex;align-items:center;justify-content:center;border-radius:30px;font-weight:900;color:#fff;
 background:linear-gradient(160deg,rgba(170,240,255,.85) 0%,rgba(53,194,218,.82) 45%,rgba(11,120,145,.88) 100%);
 box-shadow:inset 0 3px 0 rgba(255,255,255,.65),inset 0 -6px 14px rgba(0,50,70,.35),0 18px 40px rgba(0,40,55,.45),0 0 0 2px rgba(255,255,255,.35);
 text-shadow:0 3px 8px rgba(0,60,80,.5)}
.gt svg{width:52%;height:52%;stroke-width:2.6}
.gl{position:absolute;font-weight:700;color:#fff;font-size:30px;text-align:center;white-space:nowrap;text-shadow:0 2px 8px rgba(0,0,0,.6)}
/* notification */
.nt{position:absolute;display:flex;gap:22px;align-items:center;padding:24px 30px;border-radius:36px;background:rgba(245,250,252,.92);
 box-shadow:0 24px 60px rgba(0,0,0,.35);color:#0B1A1E}
.nt .ic{width:78px;height:78px;border-radius:20px;background:linear-gradient(160deg,#5FD3E6,#0E8FA8);display:flex;align-items:center;justify-content:center;color:#fff}
.nt .ic svg{width:44px;height:44px;stroke-width:2.4}
/* cta */
.cta{position:absolute;display:flex;align-items:center;justify-content:center;gap:16px;border-radius:999px;font-weight:700;color:#04252D;
 background:linear-gradient(180deg,#BDF3FF 0%,#5FD3E6 50%,#22B4CC 100%);
 box-shadow:inset 0 2px 0 rgba(255,255,255,.7),0 16px 40px rgba(0,0,0,.4),0 0 40px rgba(53,194,218,.45)}
.cta svg{width:40px;height:40px;stroke-width:2.8}
/* end card */
.end{position:absolute;inset:0;background:var(--bg)}
</style></head>
<body><div id="stage"></div>
<script>
const W=1080,H=1920;const ICONS=window.ICONS||{};
const cl=(x,a=0,b=1)=>Math.min(b,Math.max(a,x)),lerp=(a,b,p)=>a+(b-a)*p,P=(t,t0,d)=>cl((t-t0)/d);
const E={out:t=>1-Math.pow(1-t,3),out5:t=>1-Math.pow(1-t,5),back:t=>{const c1=1.4,c3=c1+1;return 1+c3*Math.pow(t-1,3)+c1*Math.pow(t-1,2)}};
const svg=n=>ICONS[n]||'';
function el(tag,cls,parent,html){const e=document.createElement(tag);if(cls)e.className=cls;if(html!=null)e.innerHTML=html;(parent||document.getElementById('stage')).appendChild(e);return e}
function vis(e,on){e.style.display=on?'':'none'}
function appear(e,t,t0,o={}){const d=o.d||.38,p=P(t,t0,d),pe=(o.ease||E.out)(p);
 e.style.opacity=E.out(P(t,t0,d*.6));e.style.filter=p<1?`blur(${(1-pe)*(o.b0??8)}px)`:'none';
 e.style.transform=`${e.dataset.base||''} translate(${(1-pe)*(o.x0||0)}px,${(1-pe)*(o.y0??20)}px) scale(${lerp(o.s0??.9,1,pe)})`;return p}
/* ---------- builders ---------- */
const B={};
B.hero=(o)=>{const r=el('div','hero');r.style.top=(o.y*H)+'px';o.e=r;
 o.sm=o.small?el('div','sm',r,o.small):null;const b=el('div','bg',r,`<div class="bs"><span class="bt">${o.big}</span></div>`);b.style.fontSize=o.size+'px';o.b=b;
 if(o.sub){o.s2=el('div','sm',r,o.sub)}};
B.hero.u=(o,t)=>{if(o.sm)appear(o.sm,t,o.t0,{d:.25,y0:10});appear(o.b,t,o.bigT,{d:.45,s0:1.18,y0:0,b0:14,ease:E.out5});
 o.b.style.transform+=` scale(${1+.03*P(t,o.bigT,o.t1-o.bigT)})`;if(o.s2)appear(o.s2,t,o.subT||o.bigT+.2,{d:.3,y0:10})};
B.plansza=(o)=>{const p=el('div','pl');o.e=p;
 const c1=el('div','c',p);Object.assign(c1.style,{width:'760px',height:'760px',right:'-330px',top:'-330px'});
 const c2=el('div','c',p);Object.assign(c2.style,{width:'680px',height:'680px',left:'-300px',bottom:'-300px'});o.cs=[c1,c2];
 el('div','grain',p);
 o.rows=o.rows.map((r,i)=>{const y=r.y??(o.y0+i*(o.gap||230));let n=null;
  if(r.num!=null){n=el('div','num',p,r.num+'.');Object.assign(n.style,{left:'90px',top:(y-10)+'px',fontSize:(o.numSize||190)+'px'})}
  const tx=el('div','txt',p);Object.assign(tx.style,{left:(r.num!=null?(o.textX||330):90)+'px',right:'80px',top:y+'px',fontSize:(r.fs||o.fs||60)+'px'});
  r.words.forEach(w=>{const s=el('span','wd'+(w.h?' h':''),tx,w.d);s.dataset.t=w.t});return {r,n,tx}})};
B.plansza.u=(o,t)=>{const life=P(t,o.t0,o.t1-o.t0);o.cs[0].style.transform=`translate(${-20*life}px,${20*life}px) scale(${1+.04*life})`;o.cs[1].style.transform=`translate(${20*life}px,${-20*life}px)`;
 o.rows.forEach(({r,n,tx})=>{if(n)appear(n,t,r.t,{d:.35,y0:30,s0:.8});tx.querySelectorAll('.wd').forEach(s=>appear(s,t,+s.dataset.t-.04,{d:.22,y0:10,s0:1,b0:6}))})};
function bookCard(c){return `<div style="position:absolute;inset:0;background:${c.bg||'linear-gradient(160deg,#F4FBFD,#DDF2F7)'}"></div>
 <div style="position:absolute;left:26px;right:26px;top:30px;font:800 ${c.fs||40}px Inter;letter-spacing:-.03em;line-height:1.02;color:${c.ink||'#0B1A1E'}">${c.title}</div>
 ${c.sub?`<div style="position:absolute;left:26px;right:26px;top:${c.subY||150}px;font:500 22px Inter;color:${c.ink2||'#44626a'}">${c.sub}</div>`:''}
 ${c.icon?`<div style="position:absolute;left:50%;bottom:${c.iconB||70}px;width:120px;height:120px;margin-left:-60px;border-radius:30px;background:linear-gradient(160deg,#5FD3E6,#0E8FA8);display:flex;align-items:center;justify-content:center;color:#fff">${svg(c.icon).replace('<svg','<svg style="width:66px;height:66px;stroke-width:2.2"')}</div>`:''}
 ${c.price?`<div style="position:absolute;right:20px;bottom:20px;padding:10px 20px;border-radius:999px;background:#0B1A1E;color:#9EEBFF;font:800 30px Inter">${c.price}</div>`:''}`}
B.fan=(o)=>{const f=el('div','fan');Object.assign(f.style,{left:0,top:0,width:W+'px',height:H+'px'});o.e=f;
 o.cards=o.cards.map((c,i)=>{const e=el('div','card',f,bookCard(c));const w=o.w||260,h=o.h||360;
  Object.assign(e.style,{width:w+'px',height:h+'px',left:(o.x+i*(o.dx||200)-w/2)+'px',top:(o.y-h)+'px'});
  e.dataset.base=`rotateY(${o.ry??-18}deg) rotateZ(${(i-(o.cards.length-1)/2)*(o.rz??5)}deg)`;return {c,e,i}})};
B.fan.u=(o,t)=>{o.cards.forEach(({c,e,i})=>{const t0=(c.t??o.t0)+i*(c.t!=null?0:.09);appear(e,t,t0,{d:.5,x0:-520,y0:60,s0:.9,b0:10,ease:E.out5});
 e.style.transform+=` translateY(${Math.sin(t*1.6+i)*5}px)`})};
B.tiles=(o)=>{const n=o.items.length,s=o.size||150,gap=o.gap||34,x0=540-((n*s+(n-1)*gap)/2)+s/2;
 o.items=o.items.map((it,i)=>{const e=el('div','gt',null,it.icon?svg(it.icon):it.num);const x=x0+i*(s+gap);
  Object.assign(e.style,{width:s+'px',height:s+'px',left:(x-s/2)+'px',top:(o.y-s/2)+'px',fontSize:(s*.55)+'px'});
  let lb=null;if(it.label){lb=el('div','gl',null,it.label);Object.assign(lb.style,{left:(x-200)+'px',width:'400px',top:(o.y+s/2+14)+'px'})}
  return {it,e,lb,i}})};
B.tiles.u=(o,t)=>{o.items.forEach(({it,e,lb,i})=>{appear(e,t,it.t,{d:.42,y0:40,s0:.6,b0:8,ease:E.back});e.style.transform+=` translateY(${Math.sin(t*2+i)*5}px) rotate(${Math.sin(t*1.3+i)*3}deg)`;if(lb)appear(lb,t,it.t+.1,{d:.3,y0:10})})};
B.notif=(o)=>{const e=el('div','nt',null,`<div class="ic">${svg(o.icon||'circle-dollar-sign')}</div><div><div style="font:700 30px Inter">${o.title}</div><div style="font:500 26px Inter;color:#46646c">${o.sub}</div></div>
 <div style="margin-left:auto;font:800 40px Inter;color:#0E8FA8">${o.amount||''}</div>`);Object.assign(e.style,{left:'90px',right:'90px',top:(o.y-70)+'px'});o.e=e};
B.notif.u=(o,t)=>{appear(o.e,t,o.t0,{d:.45,y0:-80,s0:.92,ease:E.out5})};
B.cta=(o)=>{const b=el('div','cta',null,`<span>${o.text}</span>${svg('arrow-down')}`);Object.assign(b.style,{fontSize:'42px',height:'112px',width:(o.w||560)+'px',left:(540-(o.w||560)/2)+'px',top:(o.y-56)+'px'});o.e=b};
B.cta.u=(o,t)=>{appear(o.e,t,o.t0,{d:.4,y0:30,s0:.7,ease:E.back});o.e.style.transform+=` scale(${t>o.t0+.6?1+.03*Math.max(0,Math.sin((t-o.t0)*4)):1})`};
B.end=(o)=>{const e=el('div','end');o.e=e;const c1=el('div','c',e);el('div','grain',e);
 Object.assign(c1.style,{position:'absolute',borderRadius:'50%',width:'900px',height:'900px',left:'90px',top:'480px',background:'radial-gradient(circle,rgba(53,194,218,.22),transparent 65%)'});
 e.insertAdjacentHTML('beforeend',`<div style="position:absolute;left:0;right:0;top:720px;text-align:center;font:800 92px Inter;letter-spacing:-.045em;color:#fff">${o.brand}<span style="color:#35C2DA">.</span></div>
 <div style="position:absolute;left:0;right:0;top:850px;text-align:center;font:500 34px Inter;color:#9fb6bb"><span style="display:inline-block;width:12px;height:12px;border-radius:50%;background:#35C2DA;margin-right:14px;vertical-align:middle"></span>${o.tag}</div>`);
 const b=el('div','cta',e,`<span>${o.button}</span>`);Object.assign(b.style,{fontSize:'40px',height:'104px',width:'520px',left:'280px',top:'1000px'});o.b=b};
B.end.u=(o,t)=>{appear(o.b,t,o.t0+.35,{d:.4,y0:20,s0:.85,ease:E.back})};
/* ---------- captions ---------- */
let lastKey='';
function caps(spec,t){const box=document.getElementById('caps');
 const hide=spec.items.some(o=>o.hideCaps&&t>=o.t0&&t<o.t1)||spec.capHide.some(([a,b])=>t>=a&&t<b);
 let bi=-1;for(let i=0;i<spec.caps.length;i++){if(t>=spec.caps[i].t0-.03)bi=i;else break}
 if(hide||bi<0){box.style.visibility='hidden';return}box.style.visibility='visible';
 const capY=(spec.items.find(o=>o.capY&&t>=o.t0&&t<o.t1)||{}).capY||spec.capY;
 const b=spec.caps[bi];if(lastKey!==bi){lastKey=bi;box.innerHTML='';b.words.forEach(w=>{const s=el('span','w'+(w.h?' h':''),box,w.d);s.dataset.t=w.t})}
 box.style.top='0px';const hh=box.getBoundingClientRect().height;box.style.top=(capY*H-hh/2)+'px';
 box.querySelectorAll('.w').forEach(s=>{const p=P(t,+s.dataset.t-.04,.14);s.style.opacity=E.out(p);s.style.filter=p<1?`blur(${(1-p)*7}px)`:'none'})}
/* ---------- main ---------- */
let SPEC=null;
window.init=(spec)=>{SPEC=spec;spec.items.forEach(o=>B[o.type](o));const c=el('div','');c.id='caps';return true};
window.seek=(t)=>{SPEC.items.forEach(o=>{const on=t>=o.t0-1e-3&&t<o.t1;const nodes=[o.e,...(o.type==='tiles'?o.items.flatMap(x=>[x.e,x.lb]):[])].filter(Boolean);
 nodes.forEach(n=>vis(n,on));if(on)B[o.type].u(o,t)});caps(SPEC,t);return true};
</script></body></html>
````


### `projekty/styl2/engine/pexels.py`

````python
#!/usr/bin/env python3
"""Fetch portrait stock clips from Pexels. Key from $PEXELS_API_KEY.
usage: pexels.py OUTDIR "name=query" ...   -> OUTDIR/<name>_<n>.mp4 (up to 3 per query) + OUTDIR/index.json"""
import json, os, sys, urllib.parse, urllib.request
key = os.environ["PEXELS_API_KEY"]; out = sys.argv[1]; os.makedirs(out, exist_ok=True)
idxp = os.path.join(out, "index.json"); idx = json.load(open(idxp)) if os.path.exists(idxp) else {}
def get(url):
    return json.load(urllib.request.urlopen(urllib.request.Request(url, headers={"Authorization": key, "User-Agent": "Mozilla/5.0"})))
for arg in sys.argv[2:]:
    name, q = arg.split("=", 1)
    d = get("https://api.pexels.com/videos/search?" + urllib.parse.urlencode({"query": q, "orientation": "portrait", "per_page": 8, "size": "medium"}))
    n = 0
    for v in d.get("videos", []):
        if v["duration"] < 3: continue
        fs = [f for f in v["video_files"] if (f.get("height") or 0) >= 1280 and (f.get("width") or 0) < (f.get("height") or 0)]
        if not fs: continue
        f = min(fs, key=lambda f: abs((f.get("height") or 0) - 1920))
        p = os.path.join(out, f"{name}_{n}.mp4")
        req = urllib.request.Request(f["link"], headers={"User-Agent": "Mozilla/5.0"})
        open(p, "wb").write(urllib.request.urlopen(req).read())
        idx[f"{name}_{n}"] = {"id": v["id"], "url": v["url"], "author": v["user"]["name"], "dur": v["duration"], "w": f["width"], "h": f["height"]}
        print(name, n, v["url"], v["duration"], f["width"], f["height"], flush=True)
        n += 1
        if n >= 3: break
json.dump(idx, open(idxp, "w"), indent=1)
````


### `projekty/styl2/engine/qa.py`

````python
#!/usr/bin/env python3
"""QA sheet from a FINAL video: frames just before/after every cut, b-roll edge and overlay start/end.
usage: qa.py SPEC.json FINAL.mp4 OUT_prefix   -> OUT_prefix_1.jpg, _2.jpg ... (pairs: before | after)"""
import json, subprocess, sys
import numpy as np, cv2
spec = json.load(open(sys.argv[1])); vid = sys.argv[2]; pre = sys.argv[3]
ev = [("cut", c) for c in spec.get("cuts", [])]
ev += [("broll+", b["t0"]) for b in spec.get("brolls", [])] + [("broll-", b["t1"]) for b in spec.get("brolls", [])]
ev += [(o["type"] + "+", o["t0"]) for o in spec.get("items", spec.get("scenes", []))] + [(o["type"] + "-", o["t1"]) for o in spec.get("items", spec.get("scenes", [])) if o["t1"] < spec["dur"]]
ev = sorted(ev, key=lambda x: x[1])
def frame(t):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{max(0, t):.3f}", "-i", vid, "-frames:v", "1", "-vf", "scale=180:320", "-f", "rawvideo", "-pix_fmt", "bgr24", "-"], capture_output=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(320, 180, 3).copy() if len(raw) == 180 * 320 * 3 else np.zeros((320, 180, 3), np.uint8)
tiles = []
for name, t in ev:
    a, b = frame(t - 0.067), frame(t + 0.034)
    pair = np.hstack([a, np.full((320, 4, 3), 255, np.uint8), b])
    cv2.putText(pair, f"{name} {t:.2f}", (4, 16), cv2.FONT_HERSHEY_SIMPLEX, .45, (0, 0, 255), 1)
    tiles.append(pair)
cols, rows = 6, 4
for k in range(0, len(tiles), cols * rows):
    ch = tiles[k:k + cols * rows]
    while len(ch) % cols: ch.append(np.zeros_like(tiles[0]))
    cv2.imwrite(f"{pre}_{k // (cols * rows) + 1}.jpg", np.vstack([np.hstack(ch[i:i + cols]) for i in range(0, len(ch), cols)]))
print(len(tiles), "events")
````


### `projekty/styl2/engine/sheet2.py`

````python
#!/usr/bin/env python3
"""Contact sheet for style-2 specs: graded footage/b-roll + zoom + overlay PNG at each rendered frame. usage: sheet2.py SPEC FRAMES OUT.jpg [cols]"""
import json, os, subprocess, sys, glob
import numpy as np, cv2
spec = json.load(open(sys.argv[1])); fd = sys.argv[2]; out = sys.argv[3]; cols = int(sys.argv[4]) if len(sys.argv) > 4 else 6
W, H = 1080, 1920
def grab(src, t, grade):
    vf = f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}" + ("," + grade if grade else "")
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", src, "-frames:v", "1", "-vf", vf, "-f", "rawvideo", "-pix_fmt", "bgr24", "-"], capture_output=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(H, W, 3).copy() if len(raw) == W * H * 3 else np.zeros((H, W, 3), np.uint8)
tiles = []
for p in sorted(glob.glob(os.path.join(fd, "f_*.png"))):
    f = int(os.path.basename(p)[2:7]); t = f / spec.get("fps", 30)
    b = next((b for b in spec.get("brolls", []) if b["t0"] <= t < b["t1"]), None)
    if b: fr = grab(b["file"], b.get("ss", 0) + t - b["t0"], spec["grade"])
    elif t < spec["srcDur"]:
        fr = grab(spec["src"], t, spec["grade"]); s = 1.0
        for zt, zs in spec["zooms"]:
            if zt <= t: s = zs
        if s > 1.001:
            cx, cy = spec["zoomCenter"]; w, h = W / s, H / s
            x0 = min(max(cx * W - w / 2, 0), W - w); y0 = min(max(cy * H - h / 2, 0), H - h)
            fr = cv2.warpAffine(fr, np.float32([[s, 0, -x0 * s], [0, s, -y0 * s]]), (W, H))
    else: fr = np.zeros((H, W, 3), np.uint8)
    ov = cv2.imread(p, cv2.IMREAD_UNCHANGED).astype(np.float32)
    al = ov[:, :, 3:4] / 255 if ov.shape[2] == 4 else np.ones_like(ov[:, :, :1])
    im = (ov[:, :, :3] * al + fr.astype(np.float32) * (1 - al)).astype(np.uint8)
    im = cv2.resize(im, (360, 640), interpolation=cv2.INTER_AREA)
    cv2.putText(im, f"{t:.1f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, .9, (0, 0, 255), 2); tiles.append(im)
while len(tiles) % cols: tiles.append(np.zeros_like(tiles[0]))
cv2.imwrite(out, np.vstack([np.hstack(tiles[i:i + cols]) for i in range(0, len(tiles), cols)]), [cv2.IMWRITE_JPEG_QUALITY, 85]); print(out)
````


### `projekty/styl3/build_spec3.py`

````python
#!/usr/bin/env python3
"""Style-3 render specs for ads5 and ads2.  usage: build_spec3.py WORKDIR STOCKDIR
Caption markup in FIX: *word* = blue box, ~word~ = serif italic typed; join multi-word with _."""
import difflib, json, os, re, subprocess, sys
WD, ST = sys.argv[1], sys.argv[2]
HERE = os.path.dirname(os.path.abspath(__file__))
WEAK = {"i", "w", "z", "na", "do", "od", "po", "a", "o", "że", "bo", "się", "to", "jak", "czy", "nie", "co", "za", "ci", "ten", "tego", "mi"}
GRADE = ("eq=contrast=1.06:saturation=0.9:brightness=-0.025,colorbalance=rs=-0.02:bs=0.03:bm=0.02,"
         "curves=all='0/0.02 0.5/0.47 1/0.95',vignette=angle=PI/4.5")
norm = lambda t: re.sub(r"[^\w]", "", t.lower())


def align(words, fixed):
    toks = []
    for raw in fixed.split():
        h = 1 if raw.startswith("*") else 2 if raw.startswith("~") else 0
        for k, p in enumerate(raw.strip("*~").split("_")): toks.append({"d": p, "h": h, "join": k > 0})
    a = [norm(w["w"]) for w in words]; b = [norm(t["d"]) for t in toks]; times = [None] * len(toks)
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        if op == "equal":
            for k in range(i2 - i1): times[j1 + k] = words[i1 + k]["s"]
        elif op == "replace":
            s0, e0 = words[i1]["s"], words[i2 - 1]["e"]
            for j in range(j1, j2): times[j] = s0 + (e0 - s0) * (j - j1) / max(1, j2 - j1)
    for j in range(len(toks)):
        if times[j] is None: times[j] = next((times[k] for k in range(j - 1, -1, -1) if times[k] is not None), 0.0)
    for j, t in enumerate(toks): t["t"] = round(times[j], 3)
    return toks


def chunk(units, maxw=4, maxc=20):
    blocks, cur = [], []
    def flush():
        if cur: blocks.append(cur[:]); cur.clear()
    for u in units:
        clen = sum(len(x["d"]) + 1 for x in cur) + len(u["d"])
        if cur and not u["join"] and (len(cur) >= maxw or clen > maxc):
            carry = []
            while len(cur) > 1 and (cur[-1]["d"].lower().strip(",.?") in WEAK or cur[-1]["d"].isdigit()): carry.insert(0, cur.pop())
            flush(); cur.extend(carry)
        cur.append(u)
        if u["d"].endswith((".", "?", "!")): flush()
    flush()
    return [{"t0": b[0]["t"], "words": [{"d": w["d"], "t": w["t"], "h": w["h"]} for w in b]} for b in blocks]


def dur(p): return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p], capture_output=True, text=True).stdout)
def cuts(p): return json.loads(subprocess.run([sys.executable, os.path.join(HERE, "..", "reklamy_CA", "engine", "cuts.py"), p], capture_output=True, text=True).stdout)
def pw(lst): return [{"d": w, "t": t, "h": h} for w, t, h in lst]
STILL = lambda n: os.path.join(ST, "stills", n + ".jpg")
def VID(n, vs=0.0):  # clip from Konrad's Drive, pre-extracted to a 30 fps JPG sequence in <WD>/../drive5/seq_<n>
    d = os.path.join(os.path.dirname(WD), "drive5", "seq_" + n); return dict(vid=d, vn=len(os.listdir(d)), vs=vs)


def make(name, src, trname, fixed, items, extra_cuts=(), capY=0.6, brolls=()):
    srcp = os.path.join(WD, src); sd = round(dur(srcp), 3); cs = sorted(set(cuts(srcp)) | set(extra_cuts))
    words = [w for s in json.load(open(os.path.join(WD, trname))) for w in s["words"]]
    caps = chunk(align(words, fixed))
    z, big = [], False
    for t in [0.0] + cs: z.append([t, 1.14 if big else 1.0]); big = not big
    spec = dict(src=srcp, srcDur=sd, dur=sd, fps=30, capY=capY, caps=caps, items=items, brolls=list(brolls),
                cuts=cs, zooms=z, zoomCenter=[0.5, 0.3], grade=GRADE)
    p = os.path.join(WD, f"spec3_{name}.json"); json.dump(spec, open(p, "w"), ensure_ascii=False, indent=1)
    print(p, len(caps), "caption blocks,", len(cs), "cuts")
    for b in caps: print(f'  {b["t0"]:6.2f}  ' + " ".join(("*" + w["d"] + "*") if w["h"] == 1 else ("~" + w["d"] + "~") if w["h"] == 2 else w["d"] for w in b["words"]))


PL = dict(type="plansza", hideCaps=True)

# ------------------------------------------------------------------ ADS5 (53.2 s, 10 cuts) – angle: "gdzie jest haczyk?"
FIX5 = ("Gdybym zobaczył reklamę, w której jakiś gość mówi, że pokaże mi, jak zbudować *biznes_AI* w *48_godzin* za *17_zł,* "
        "to pierwsze, co bym pomyślał: dobra, ale gdzie jest ~haczyk?~ I szczerze, wcale Cię nie dziwię, bo w internecie jest "
        "pełno ludzi, którzy obiecują Ci *miliony_złotych* za ~kilka_kliknięć.~ Ale ja nie sprzedaję Ci magicznego sposobu na "
        "zarabianie, sprzedaję Ci coś znacznie prostszego. *Prosty_proces,* który pozwala Ci w końcu stworzyć coś ~własnego.~ "
        "Zobacz, najpierw wybierasz sobie pomysł na Twój produkt cyfrowy, potem AI pomaga Ci stworzyć jego zawartość, następnie "
        "przygotowujesz stronę sprzedażową z AI, podpinasz płatność i masz coś, co możesz realnie zaoferować innym ludziom. I to "
        "wszystko możesz przygotować w *48_godzin,* wykonując instrukcje krok po kroku. I czy to oznacza, że w 48 godzin będziesz "
        "milionerem? ~Nie.~ Ale zamiast kolejny miesiąc zastanawiać się, jak zacząć zarabiać w internecie, możesz w końcu mieć "
        "*produkt,* który faktycznie da się ~sprzedawać.~ I właśnie dlatego stworzyłem Cyfrowy Autopilot. Cały proces pokazuję Ci "
        "za jedyne *17_zł,* więc nie musisz mi wierzyć ~na_słowo.~ Kliknij poniżej, zobacz dokładnie, co dostajesz, i zdecyduj, "
        "czy chcesz spróbować.")
IT5 = [
    dict(PL, t0=6.333, t1=9.067, uh=dict(y=640, bar=560, words=pw([("Pierwsza", 6.34, 0), ("myśl:", 7.12, 0)])),
         bh=[dict(y=860, fs=120, words=pw([("Dobra,", 7.80, 0), ("ale", 8.26, 0), ("gdzie", 8.34, 0), ("jest", 8.50, 0), ("haczyk?", 8.66, 2)]))]),
    dict(PL, t0=14.333, t1=18.067, bh=[dict(y=560, fs=74, words=pw([("Nie", 14.62, 0), ("sprzedaję", 14.70, 0)]))], rows=[
        dict(y=820, t=15.22, icon="x", bad=True, html='magiczny<br>sposób'),
        dict(y=1080, t=16.72, icon="check", html='coś <span class="s">znacznie</span><br>prostszego')]),
    dict(type="tracker", t0=20.6, t1=34.033, x=70, y=1250, gap=104, doneT=30.0, items=[
        dict(text="Pomysł na produkt", t=21.80), dict(text="Zawartość z AI", t=24.04),
        dict(text="Strona sprzedażowa", t=25.98), dict(text="Płatność", t=27.26)]),
    dict(PL, t0=30.133, t1=34.033, uh=dict(y=330, bar=640, words=pw([("Wszystko", 30.20, 0), ("to", 30.32, 0), ("przygotujesz", 30.96, 0), ("w", 31.28, 0)])),
         bh=[dict(y=440, fs=180, words=pw([("48", 31.50, 1), ("godzin", 31.96, 0)])),
             dict(y=900, fs=90, words=pw([("krok", 33.24, 2), ("po", 33.46, 2), ("kroku", 33.66, 2)]))]),
    dict(PL, t0=43.567, t1=48.2, bh=[dict(y=330, fs=80, words=pw([("Dlatego", 43.90, 0), ("stworzyłem", 44.22, 0)]))], cards=[
        dict(kind="brand", t=44.62, x=540, y=1060, w=860, h=760, title="Cyfrowy<br>Autopilot", sub="cały proces krok po kroku", subY=330,
             rows=["pomysł na produkt", "produkt z AI", "strona + płatność"], rowsY=420, price="17 zł")]),
    dict(type="cta", t0=49.92, t1=53.2, y=1480, text="Kliknij poniżej"),
]

# ------------------------------------------------------------------ ADS2 (71.1 s, 17 cuts) – angle: "AI slop zarabia"
FIX2 = ("~AI_slop.~ Na pewno widziałeś już te dziwne filmiki generowane przez sztuczną inteligencję, ale jest coś, czego większość "
        "z nich kompletnie nie rozumie. Niektórzy wykorzystują takie filmiki, żeby zarabiać *tysiące_złotych* miesięcznie. I nie, "
        "nie chodzi mi kompletnie o pieniądze z ~wyświetleń.~ Akurat tutaj chodzi o coś znacznie prostszego: AI *produkty_cyfrowe.* "
        "Na przykład taka postać AI codziennie pokazuje kobietom proste triki i sekrety w kuchni, a na profilu sprzedaje poradnik AI "
        "za 49 złotych. I teraz sobie policzmy: 10 sprzedaży dziennie to 490 złotych przychodu każdego dnia. A gdyby utrzymać takie "
        "tempo przez 30 dni, daje to 14 700 miesięcznie. I to wszystko z *jednego* prostego AI produktu ~cyfrowego.~ Oczywiście to "
        "tylko przykład, ale pokazuje, jak działa ten *model_biznesowy.* I najlepsze jest to, że dzisiaj nawet nie musisz "
        "samodzielnie tworzyć takiego produktu od zera, bo AI może pomóc Ci zrobić praktycznie ~wszystko.~ I właśnie dlatego "
        "stworzyłem Cyfrowy Autopilot. Gotowy system, który pomaga Ci znaleźć pomysł na produkt, którego ludzie już szukają. "
        "Następnie AI pomaga Ci stworzyć gotowy produkt cyfrowy i zbudować stronę, na której możesz go sprzedawać. A na koniec "
        "pokazuję Ci, jak stworzyć proste filmiki i reklamy z AI, które przyciągają potencjalnych klientów. Więc nie, spokojnie, "
        "nie musisz być ekspertem, nie musisz umieć programować ani nawet pokazywać swojej twarzy. Więc po prostu kliknij przycisk "
        "poniżej i pokażę Ci, jak możesz stworzyć swój pierwszy *produkt_cyfrowy* gotowy do sprzedaży. I zamiast dalej oglądać, "
        "jak inni wykorzystują AI do zarabiania, zacznij wykorzystywać je ~dla_siebie.~")
IT2 = [
    dict(PL, t0=0.8, t1=4.167, bh=[dict(y=300, fs=150, words=pw([("AI", 0.82, 0), ("slop", 0.9, 2)]))], reels=[
        dict(VID("aislop1"), x=250, y=1080, w=330, h=560, rot=-6, t=1.0),
        dict(VID("aislop2"), x=540, y=1020, w=330, h=560, rot=0, t=1.25),
        dict(VID("aislop3"), x=830, y=1080, w=330, h=560, rot=6, t=1.5)]),
    dict(PL, t0=12.367, t1=15.567, uh=dict(y=600, bar=820, words=pw([("Akurat", 12.48, 0), ("tutaj", 12.74, 0), ("chodzi", 13.04, 0), ("o", 13.26, 0), ("coś", 13.40, 0), ("prostszego:", 13.56, 0)])),
         bh=[dict(y=820, fs=130, words=pw([("AI", 14.30, 0), ("+", 14.42, 0), ("produkty", 14.54, 1), ("cyfrowe", 14.70, 2)]))]),
    dict(PL, t0=15.567, t1=22.5, uh=dict(y=110, bar=380, words=pw([("Na", 15.66, 0), ("przykład:", 15.78, 0)])), bh=[dict(y=230, fs=90, words=pw([("Postać", 16.26, 0), ("AI", 16.58, 1)])),
                                   dict(y=340, fs=90, words=pw([("triki", 18.60, 0), ("w", 19.34, 2), ("kuchni", 19.44, 2)]))],
         reels=[dict(VID("aikicthen"), x=330, y=1050, w=420, h=720, rot=-4, t=15.8)],
         cards=[dict(kind="product", t=20.44, x=770, y=1180, w=420, h=560, rot=5, img=STILL("cooking_1"), imgH=270,
                     title="Poradnik AI:<br>sekrety kuchni", sub="e-book PDF", price="49 zł")]),
    dict(PL, t0=22.5, t1=26.533, noFlash=True, uh=dict(y=420, bar=520, words=pw([("Teraz", 22.72, 0), ("sobie", 22.86, 0), ("policzmy:", 23.04, 0)])), eq=[
        dict(t=23.62, y=600, fs=120, html='10 <span style="font-size:.6em;opacity:.8">sprzedaży</span>'),
        dict(t=24.0, y=760, fs=120, html='× 49 zł'),
        dict(t=24.56, y=980, fs=190, color="#8F8FFF", pre="", suf=" zł", count=dict(t=24.56, d=.8, to=490)),
        dict(t=25.88, y=1210, fs=70, html='<span style="font-family:Instrument Serif;font-style:italic;font-weight:400">każdego dnia</span>')]),
    dict(PL, t0=26.533, t1=30.733, noFlash=True, eq=[
        dict(t=26.6, y=600, fs=110, html='490 zł'),
        dict(t=28.10, y=760, fs=120, html='× 30 dni'),
        dict(t=29.04, y=980, fs=180, color="#8F8FFF", suf=" zł", count=dict(t=29.04, d=1.0, to=14700)),
        dict(t=30.12, y=1210, fs=70, html='<span style="font-family:Instrument Serif;font-style:italic;font-weight:400">miesięcznie</span>')]),
    dict(PL, t0=42.833, t1=45.033, bh=[dict(y=300, fs=80, words=pw([("Dlatego", 43.32, 0), ("stworzyłem", 43.64, 0)]))], cards=[
        dict(kind="brand", t=44.04, x=540, y=1000, w=860, h=640, title="Cyfrowy<br>Autopilot", sub="gotowy system z AI", subY=330, price="17 zł")]),
    dict(type="tracker", t0=45.033, t1=57.5, x=70, y=1390, gap=104, doneT=56.9, items=[
        dict(text="Pomysł, którego szukają", t=46.72), dict(text="Produkt z AI", t=49.62),
        dict(text="Strona sprzedażowa", t=50.98), dict(text="Filmiki i reklamy z AI", t=54.74)]),
    dict(type="irows", t0=58.6, t1=61.933, rows=[
        dict(y=1390, t=58.66, icon="x", bad=True, html='bez bycia ekspertem'),
        dict(y=1520, t=59.58, icon="x", bad=True, html='bez programowania'),
        dict(y=1650, t=60.86, icon="x", bad=True, html='bez pokazywania twarzy')]),
    dict(type="cta", t0=62.48, t1=71.2, y=1500, text="Kliknij przycisk poniżej"),
]

make("ads5", "ads5.mp4", "tr_ads5.json", FIX5, IT5, capY=0.5)
make("ads2", "ads2.mp4", "tr_ads2.json", FIX2, IT2, extra_cuts=(4.167, 6.567), capY=0.6)
````


### `projekty/styl3/engine/overlay3.html`

````html
<!doctype html>
<html><head><meta charset="utf-8">
<link rel="stylesheet" href="../../reklamy_CA/engine/assets/fonts/g.css">
<style>
:root{--bg:#05071A;--blue:#3B3BFF;--blue2:#5B5BFF;--ink:#0B0D24}
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:1080px;height:1920px;background:transparent;overflow:hidden}
#stage{position:absolute;inset:0;font-family:Inter,sans-serif;-webkit-font-smoothing:antialiased}
.abs{position:absolute}
/* stacked captions */
#caps{position:absolute;left:40px;right:40px;text-align:center;pointer-events:none}
#caps .ln{display:block;line-height:.92;white-space:nowrap}
#caps .ln.sl{line-height:1.08;margin-top:.06em}
#caps .w{display:inline-block;margin:0 .1em;font-weight:900;font-size:74px;color:#fff;letter-spacing:-.055em;
 text-shadow:0 4px 14px rgba(0,0,0,.45),0 0 40px rgba(0,0,0,.25)}
#caps .w.box{background:var(--blue);padding:0 .14em .04em;border-radius:6px;font-size:65px;box-shadow:0 10px 30px rgba(20,20,120,.45);text-shadow:none}
#caps .w.ser{font-family:'Instrument Serif',serif;font-style:italic;font-weight:400;letter-spacing:-.01em;font-size:78px}
/* plansza */
.pl{position:absolute;inset:0;background:var(--bg);overflow:hidden}
.blob{position:absolute;border-radius:50%;filter:blur(90px)}
.grain{position:absolute;inset:0;opacity:.07;mix-blend-mode:overlay;
 background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='300' height='300'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2' stitchTiles='stitch'/></filter><rect width='300' height='300' filter='url(%23n)'/></svg>")}
.flash{position:absolute;inset:0;background:radial-gradient(circle at 50% 45%,rgba(220,225,255,.95),rgba(120,130,255,.5) 60%,rgba(5,7,26,0));pointer-events:none}
.uh{position:absolute;left:70px;right:70px;font-weight:700;font-size:44px;color:#fff;letter-spacing:-.02em}
.uh .bar{position:absolute;left:0;height:6px;border-radius:3px;background:#fff;transform-origin:0 50%}
.bh{position:absolute;left:40px;right:40px;text-align:center;font-weight:900;color:#fff;letter-spacing:-.055em;line-height:.95}
.bh .h{background:var(--blue);padding:0 .12em;border-radius:6px}
.bh .s{font-family:'Instrument Serif',serif;font-style:italic;font-weight:400;letter-spacing:-.01em}
.wd{display:inline-block;margin:0 .12em}
/* cards */
.card{position:absolute;border-radius:34px;overflow:hidden;background:#0D1130;box-shadow:0 30px 80px rgba(0,0,30,.6),0 0 0 2px rgba(91,91,255,.35)}
.reel{position:absolute;border-radius:28px;overflow:hidden;box-shadow:0 26px 60px rgba(0,0,0,.55),0 0 0 3px rgba(255,255,255,.85)}
.reel img{width:100%;height:100%;object-fit:cover;display:block}
/* tracker */
.tr{position:absolute;display:flex;align-items:center;gap:0;height:86px;border-radius:12px;background:#fff;overflow:hidden;box-shadow:0 14px 40px rgba(0,0,30,.45)}
.tr .n{width:86px;height:86px;background:var(--blue);color:#fff;font-weight:900;font-size:52px;display:flex;align-items:center;justify-content:center}
.tr .t{padding:0 34px;font-weight:700;font-size:44px;color:#0B0D24;letter-spacing:-.02em;white-space:nowrap}
.tr .ck{margin-right:26px;width:46px;height:46px;border-radius:50%;background:var(--blue);display:flex;align-items:center;justify-content:center;color:#fff}
.tr .ck svg{width:30px;height:30px;stroke-width:3.4}
/* icon rows */
.ir{position:absolute;display:flex;align-items:center;gap:30px}
.ir .ic{width:110px;height:110px;border-radius:30px;display:flex;align-items:center;justify-content:center;color:#fff;flex:none}
.ir .ic svg{width:62px;height:62px;stroke-width:2.8}
.ir .tx{font-weight:900;font-size:68px;color:#fff;letter-spacing:-.045em;line-height:.95;background:rgba(12,16,26,.62);padding:14px 26px 18px;border-radius:22px}
.ir .tx .s{font-family:'Instrument Serif',serif;font-style:italic;font-weight:400;letter-spacing:-.01em}
/* equation */
.eq{position:absolute;left:0;right:0;text-align:center;color:#fff;font-weight:900;letter-spacing:-.05em}
/* cta */
.cta{position:absolute;padding:20px 34px;background:var(--blue);color:#fff;font-weight:800;font-size:40px;letter-spacing:.02em;text-transform:uppercase;border-radius:8px;box-shadow:0 14px 40px rgba(20,20,120,.5);white-space:nowrap;display:flex;align-items:center;gap:14px}
.cta svg{width:44px;height:44px;stroke-width:3;flex:none}
</style></head>
<body><div id="stage"></div>
<script>
const W=1080,H=1920;const ICONS=window.ICONS||{};
const cl=(x,a=0,b=1)=>Math.min(b,Math.max(a,x)),lerp=(a,b,p)=>a+(b-a)*p,P=(t,t0,d)=>cl((t-t0)/d);
const E={out:t=>1-Math.pow(1-t,3),out5:t=>1-Math.pow(1-t,5),back:t=>{const c1=1.3,c3=c1+1;return 1+c3*Math.pow(t-1,3)+c1*Math.pow(t-1,2)}};
const svg=n=>ICONS[n]||'';
function el(tag,cls,parent,html){const e=document.createElement(tag);if(cls)e.className=cls;if(html!=null)e.innerHTML=html;(parent||document.getElementById('stage')).appendChild(e);return e}
function blurIn(e,t,t0,o={}){const d=o.d||.2,p=P(t,t0,d),pe=E.out(p);e.style.opacity=E.out(P(t,t0,d*.7));
 e.style.filter=p<1?`blur(${(1-pe)*(o.b0??16)}px)`:'none';e.style.transform=`${e.dataset.base||''} translate(${(1-pe)*(o.x0||0)}px,${(1-pe)*(o.y0??0)}px) scale(${lerp(o.s0??1.12,1,pe)})`;return p}
function typeIn(e,t,t0,dur){const s=e.dataset.full;const n=Math.round(s.length*P(t,t0,dur));e.textContent=s.slice(0,Math.max(0,n))||'​';e.style.opacity=t>=t0?1:0}
/* ---------- plansza with blobs + flash ---------- */
function plBase(o){const p=el('div','pl');o.e=p;o.blobs=[[200,300,620,'#2B2BFF'],[880,1300,700,'#1A1ACC'],[500,1700,520,'#3B3BFF']].map(([x,y,s,c],i)=>{const b=el('div','blob',p);Object.assign(b.style,{left:(x-s/2)+'px',top:(y-s/2)+'px',width:s+'px',height:s+'px',background:c,opacity:.55});return b});
 el('div','grain',p);o.fl=el('div','flash',p);return p}
function plUpd(o,t){const l=t-o.t0;o.blobs.forEach((b,i)=>{b.style.transform=`translate(${Math.sin(l*.6+i*2)*80}px,${Math.cos(l*.5+i)*60}px) scale(${1+.1*Math.sin(l*.7+i)})`});
 o.fl.style.opacity=o.noFlash?0:1-E.out(P(t,o.t0,.16))}
const B={};
B.plansza=(o)=>{const p=plBase(o);
 if(o.uh){const u=el('div','uh',p);u.style.top=o.uh.y+'px';o.uhw=o.uh.words.map(w=>{const s=el('span','wd',u,w.d);s.dataset.t=w.t;return s});const bar=el('div','bar',u);bar.style.top='62px';bar.style.width=(o.uh.bar||620)+'px';o.bar=bar}
 o.bhs=(o.bh||[]).map(b=>{const d=el('div','bh',p);Object.assign(d.style,{top:b.y+'px',fontSize:(b.fs||100)+'px'});
  const ws=b.words.map(w=>{const s=el('span','wd'+(w.h==1?' h':w.h==2?' s':''),d,w.d);s.dataset.t=w.t;if(w.h==2){s.dataset.full=w.d}return s});return {b,ws}});
 o.reels=(o.reels||[]).map(r=>{const e=el('div','reel',p,`<img src="${r.vid?r.vid+'/0001.jpg':r.img}">`);Object.assign(e.style,{left:(r.x-r.w/2)+'px',top:(r.y-r.h/2)+'px',width:r.w+'px',height:r.h+'px'});e.dataset.base=`rotate(${r.rot||0}deg)`;return {r,e}});
 o.cards=(o.cards||[]).map(c=>{const e=el('div','card',p,cardHTML(c));Object.assign(e.style,{left:(c.x-c.w/2)+'px',top:(c.y-c.h/2)+'px',width:c.w+'px',height:c.h+'px'});e.dataset.base=`rotate(${c.rot||0}deg)`;return {c,e}});
 o.irs=(o.rows||[]).map(r=>{const e=el('div','ir',p,`<div class="ic" style="background:${r.bad?'#E0483A':'var(--blue)'}">${svg(r.icon)}</div><div class="tx">${r.html}</div>`);Object.assign(e.style,{left:(r.x||110)+'px',top:r.y+'px'});return {r,e}});
 o.eqs=(o.eq||[]).map(q=>{const e=el('div','eq',p);Object.assign(e.style,{top:q.y+'px',fontSize:q.fs+'px'});e.style.color=q.color||'#fff';return {q,e}})};
B.plansza.u=(o,t)=>{plUpd(o,t);
 if(o.uhw){o.uhw.forEach(s=>blurIn(s,t,+s.dataset.t-.03,{d:.18,b0:10,s0:1}));o.bar.style.transform=`scaleX(${E.out(P(t,o.uh.words[0].t,.6))})`}
 o.bhs.forEach(({b,ws})=>ws.forEach(s=>{if(s.dataset.full!=null)typeIn(s,t,+s.dataset.t,.32);else blurIn(s,t,+s.dataset.t-.03,{d:.2})}));
 o.reels.forEach(({r,e})=>{blurIn(e,t,r.t,{d:.4,y0:80,s0:.85,b0:12});if(r.vid){const i=1+Math.min(r.vn-1,Math.max(0,Math.floor((t-r.t+(r.vs||0))*30+1e-6)));const im=e.firstChild,src=r.vid+'/'+String(i).padStart(4,'0')+'.jpg';if(!im.src.endsWith(src)){im.src=src;PEND.push(im.decode().catch(()=>{}))}}e.style.transform+=` translateY(${Math.sin(t*1.4+r.x)*6}px)`});
 o.cards.forEach(({c,e})=>{blurIn(e,t,c.t,{d:.45,y0:90,s0:.88,b0:12});e.style.transform+=` translateY(${Math.sin(t*1.2)*5}px)`});
 o.irs.forEach(({r,e})=>blurIn(e,t,r.t,{d:.3,x0:-60,s0:1,b0:12}));
 o.eqs.forEach(({q,e})=>{blurIn(e,t,q.t,{d:.25});if(q.count){const p=E.out(P(t,q.count.t,q.count.d||.7));e.textContent=(q.pre||'')+Math.round(lerp(q.count.from||0,q.count.to,p)).toLocaleString('pl-PL')+(q.suf||'')}else e.innerHTML=q.html})};
function cardHTML(c){if(c.kind==='brand')return `<div style="position:absolute;inset:0;background:radial-gradient(120% 80% at 20% 0%,#2A2AA8 0%,#0D1130 60%)"></div>
 <div style="position:absolute;left:40px;top:40px;width:96px;height:96px;border-radius:26px;background:var(--blue);display:flex;align-items:center;justify-content:center;color:#fff">${svg('sparkles').replace('<svg','<svg style="width:56px;height:56px;stroke-width:2.2"')}</div>
 <div style="position:absolute;left:40px;right:40px;top:170px;font:900 70px Inter;letter-spacing:-.05em;color:#fff;line-height:.95">${c.title}</div>
 <div style="position:absolute;left:40px;right:40px;top:${c.subY||330}px;font:500 34px Inter;color:#AEB3E8">${c.sub||''}</div>
 ${(c.rows||[]).map((r,i)=>`<div style="position:absolute;left:40px;right:40px;top:${(c.rowsY||420)+i*74}px;display:flex;align-items:center;gap:18px;font:700 34px Inter;color:#fff"><span style="width:40px;height:40px;border-radius:50%;background:var(--blue);display:flex;align-items:center;justify-content:center">${svg('check').replace('<svg','<svg style="width:26px;height:26px;stroke-width:3.4"')}</span>${r}</div>`).join('')}
 ${c.price?`<div style="position:absolute;right:40px;bottom:40px;padding:14px 30px;border-radius:12px;background:#fff;color:#0B0D24;font:900 54px Inter;letter-spacing:-.04em">${c.price}</div>`:''}`;
 if(c.kind==='product')return `<div style="position:absolute;inset:0;background:linear-gradient(160deg,#F4F5FF,#D9DCFF)"></div>
 ${c.img?`<img src="${c.img}" style="position:absolute;left:0;right:0;top:0;width:100%;height:${c.imgH||300}px;object-fit:cover">`:''}
 <div style="position:absolute;left:30px;right:30px;top:${(c.imgH||300)+26}px;font:900 50px Inter;letter-spacing:-.045em;color:#0B0D24;line-height:.98">${c.title}</div>
 <div style="position:absolute;left:30px;top:${(c.imgH||300)+150}px;font:500 28px Inter;color:#4A4F80">${c.sub||''}</div>
 ${c.price?`<div style="position:absolute;right:26px;bottom:26px;padding:12px 26px;border-radius:12px;background:var(--blue);color:#fff;font:900 46px Inter;letter-spacing:-.03em">${c.price}</div>`:''}`;
 return ''}
B.tracker=(o)=>{o.items=o.items.map((it,i)=>{const e=el('div','tr',null,`<div class="n">${i+1}</div><div class="t">${it.text}</div><div class="ck">${svg('check')}</div>`);
  e.style.left=(o.x||70)+'px';e.style.top=(o.y+i*(o.gap||112))+'px';return {it,e}})};
B.tracker.u=(o,t)=>{o.items.forEach(({it,e},i)=>{blurIn(e,t,it.t,{d:.32,x0:-80,s0:1,b0:12});const ck=e.querySelector('.ck');const done=(o.items[i+1]&&t>=o.items[i+1].it.t)||(o.doneT&&t>=o.doneT);
  ck.style.opacity=done?1:0;ck.style.transform=`scale(${done?1:.4})`})};
B.irows=(o)=>{o.rs=o.rows.map(r=>{const e=el('div','ir',null,`<div class="ic" style="background:${r.bad?'#E0483A':'var(--blue)'}">${svg(r.icon)}</div><div class="tx" style="font-size:${r.fs||58}px;text-shadow:0 4px 14px rgba(0,0,0,.5)">${r.html}</div>`);Object.assign(e.style,{left:(r.x||90)+'px',top:r.y+'px'});return {r,e}})};
B.irows.u=(o,t)=>{o.rs.forEach(({r,e})=>blurIn(e,t,r.t,{d:.3,x0:-60,s0:1,b0:12}))};
B.cta=(o)=>{const e=el('div','cta',null,`<span>${o.text}</span>${svg('arrow-down')}`);e.style.top=(o.y-40)+'px';e.style.left='0';o.e=e;requestAnimationFrame(()=>{});const w=e.getBoundingClientRect().width;e.style.left=(540-w/2)+'px'};
B.cta.u=(o,t)=>{blurIn(o.e,t,o.t0,{d:.25,s0:1.2});o.e.style.transform+=` scale(${t>o.t0+.5?1+.025*Math.max(0,Math.sin((t-o.t0)*4)):1})`};
/* ---------- captions ---------- */
let lastKey=null;
function lines(words){const out=[];let cur=[],len=0;
 words.forEach(w=>{const L=w.d.length;if(cur.length&&(len+L>11||w.h==1&&!cur.every(x=>x.h==1)||cur.some(x=>x.h==1)&&w.h!=1||w.h==2&&cur.some(x=>x.h!=2))){out.push(cur);cur=[];len=0}cur.push(w);len+=L+1});
 if(cur.length)out.push(cur);return out}
function caps(spec,t){const box=document.getElementById('caps');
 let bi=-1;for(let i=0;i<spec.caps.length;i++){if(t>=spec.caps[i].t0-.03)bi=i;else break}
 const hide=spec.items.some(o=>o.hideCaps&&(t>=o.t0&&t<o.t1||bi>=0&&t>=o.t1&&spec.caps[bi].t0>=o.t0-.3&&spec.caps[bi].words.every(w=>w.t<o.t1)));
 if(hide||bi<0){box.style.visibility='hidden';return}box.style.visibility='visible';
 const ov=spec.items.find(o=>o.capY&&t>=o.t0&&t<o.t1);const capY=ov?ov.capY:spec.capY;
 const b=spec.caps[bi];if(lastKey!==bi){lastKey=bi;box.innerHTML='';
  lines(b.words).forEach(l=>{const ln=el('span','ln'+(l.some(w=>w.h==2)?' sl':''),box);let grp=null;
   l.forEach(w=>{if(w.h==1&&grp){grp.textContent+=' '+w.d;return}
    const s=el('span','w'+(w.h==1?' box':w.h==2?' ser':''),ln,w.d);s.dataset.t=w.t;if(w.h==2)s.dataset.full=w.d;grp=w.h==1?s:null})})}
 box.style.top=(capY*H)+'px';
 box.querySelectorAll('.w').forEach(s=>{if(s.dataset.full!=null){typeIn(s,t,+s.dataset.t,.3)}else blurIn(s,t,+s.dataset.t-.04,{d:.17,b0:18,s0:1.15})})}
/* ---------- main ---------- */
let SPEC=null,PEND=[];
window.init=(spec)=>{SPEC=spec;spec.items.forEach(o=>B[o.type](o));const c=el('div','');c.id='caps';return true};
window.seek=(t)=>{SPEC.items.forEach(o=>{const on=t>=o.t0-1e-3&&t<o.t1;const nodes=[o.e,...(o.items||[]).map(x=>x.e),...(o.rs||[]).map(x=>x.e)].filter(Boolean);
 nodes.forEach(n=>n.style.display=on?'':'none');if(on)B[o.type].u(o,t)});caps(SPEC,t);const pd=PEND;PEND=[];return pd.length?Promise.all(pd).then(()=>true):true};
</script></body></html>
````


### `projekty/styl4/build_spec4.py`

````python
#!/usr/bin/env python3
"""Style-4 caption spec (ad11).  usage: build_spec4.py WORKDIR
Script text is aligned onto whisper word times. Markup: ^word^ = yellow emphasis chunk (join words with _), | = force chunk break."""
import difflib, json, os, re, subprocess, sys
WD = sys.argv[1]
norm = lambda t: re.sub(r"[^\w]", "", t.lower())
WEAK = {"i", "w", "z", "na", "do", "od", "po", "a", "o", "że", "bo", "się", "to", "jak", "czy", "nie", "co", "za", "ci", "ten", "go", "im", "aż", "ani", "jest"}

SCRIPT = ("Jest biznes, w którym możesz sprzedać ten sam produkt setki razy… | I nie wysłać ^ani_jednej_paczki.^ "
          "A dzięki AI jego zbudowanie stało się znacznie prostsze niż kiedykolwiek wcześniej. "
          "Jest jeden sekretny model zarabiania przez internet, który istniał na długo przed ChatGPT. "
          "Ale AI właśnie sprawiło, że nawet zwykli ludzie mogą zacząć go budować bez bycia ekspertami. "
          "Mowa o ^produktach_cyfrowych.^ E-bookach, planerach i szablonach, za które ludzie płacą, bo pomagają im rozwiązywać "
          "konkretne problemy. Kiedyś stworzenie takiego biznesu wymagało wielu różnych umiejętności. Ale dzisiaj AI może wykonać "
          "znaczną część tej pracy. AI pomaga Ci znaleźć pomysł na produkt, sprawdzić, czego szukają potencjalni klienci, stworzyć "
          "produkt i przygotować stronę sprzedażową. Następnie pomaga tworzyć filmiki, które przyciągają zainteresowanych na Twoją "
          "stronę. Ktoś kupuje? Automatycznie otrzymuje produkt. Bez magazynu. Bez wysyłania paczek. A ten sam produkt możesz "
          "sprzedawać ^wielokrotnie.^ Konrad, twórca Cyfrowego Autopilota, sprzedaje produkty cyfrowe od ponad trzech lat. W swoim "
          "najlepszym dniu sprzedał aż | 941_e-booków i przez to wylądował na billboardach na Times Square jako jedyny Polak. Na "
          "podstawie swojego doświadczenia stworzył system, który pokazuje zwykłym ludziom, jak wykorzystać AI do zbudowania "
          "własnego biznesu cyfrowego. Od pomysłu do produktu i strony gotowej do sprzedaży w ^48_godzin.^ I nie, nie jest on "
          "kolejnym guru, który sprzedaje kurs za 5_000_zł. Aktualnie jest promocja i dostęp do całego systemu kosztuje jedyne "
          "^17_zł.^ Kliknij przycisk poniżej i zobacz, jak zacząć budować swój pierwszy biznes cyfrowy z AI.")


def align(words, text):
    toks = []
    for raw in text.split():
        if raw == "|": toks[-1]["brk"] = True; continue
        em = raw.startswith("^")
        parts = raw.strip("^").split("_")
        for k, p in enumerate(parts): toks.append({"d": p, "em": em, "join": k > 0, "brk": False})
    a = [norm(w["w"]) for w in words]; b = [norm(t["d"]) for t in toks]; T = [None] * len(toks); E = [None] * len(toks)
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        if op == "equal":
            for k in range(i2 - i1): T[j1 + k], E[j1 + k] = words[i1 + k]["s"], words[i1 + k]["e"]
        elif op == "replace":
            s0, e0 = words[i1]["s"], words[i2 - 1]["e"]; n = j2 - j1
            for j in range(j1, j2): T[j] = s0 + (e0 - s0) * (j - j1) / n; E[j] = s0 + (e0 - s0) * (j - j1 + 1) / n
    for j in range(len(toks)):
        if T[j] is None:
            T[j] = next((E[k] for k in range(j - 1, -1, -1) if E[k] is not None), 0.0); E[j] = T[j] + .2
        toks[j]["t"], toks[j]["e"] = round(T[j], 3), round(E[j], 3)
    return toks


def chunk(toks, maxw=3, maxc=17):
    out, cur = [], []
    def flush():
        if cur: out.append(cur[:]); cur.clear()
    for u in toks:
        if cur and not u["join"]:
            clen = sum(len(x["d"]) + 1 for x in cur) + len(u["d"])
            if u["em"] != cur[-1]["em"] or len(cur) >= maxw or clen > maxc:
                carry = []
                if not cur[-1]["em"]:  # a dangling weak word moves on to the next chunk (also into a yellow one)
                    while len(cur) > 1 and cur[-1]["d"][-1].isalnum() and cur[-1]["d"].lower() in WEAK: carry.insert(0, cur.pop())
                flush(); cur.extend(carry)
        cur.append(u)
        if u["brk"] or u["d"].endswith((".", "?", "!", "…")) or (u["d"].endswith(",") and len(cur) >= 2): flush()
    flush()
    return out


words = [w for s in json.load(open(os.path.join(WD, "tr_ad11.json"))) for w in s["words"]]
src = os.path.join(WD, "ad11.mp4")
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", src], capture_output=True, text=True).stdout)
ch = chunk(align(words, SCRIPT))
caps = []
for i, c in enumerate(ch):
    t0 = c[0]["t"] - 0.05; end = c[-1]["e"] + 0.35
    nxt = ch[i + 1][0]["t"] - 0.05 if i + 1 < len(ch) else dur
    t1 = nxt if nxt - c[-1]["e"] < 0.7 else min(nxt, end)
    txt = " ".join(w["d"] for w in c).rstrip(",.…")
    if any(w["em"] for w in c) and len(txt) > 12:  # two balanced lines
        sp = [m.start() for m in re.finditer(" ", txt)]; k = min(sp, key=lambda i: abs(i - len(txt) / 2)); txt = txt[:k] + "<br>" + txt[k + 1:]
    caps.append(dict(t0=round(max(0, t0), 3), t1=round(t1, 3), html=txt, em=any(w["em"] for w in c)))
# hook variants are cut at these scene cuts, so no caption may straddle them
for c in (10.733, 21.533):
    for cp in caps:
        if cp["t0"] < c < cp["t1"]:
            if c - cp["t0"] > cp["t1"] - c: cp["t1"] = c
            else: cp["t0"] = c
# where the animation has a big card in the frame centre, the caption drops lower
ZONES = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "zones_ad11.json")))
spec = dict(dur=round(dur, 3), fps=30, capY=0.5, zones=ZONES, caps=caps)
json.dump(spec, open(os.path.join(WD, "spec4_ad11.json"), "w"), ensure_ascii=False, indent=1)
for c in caps: print(f'{c["t0"]:6.2f}-{c["t1"]:6.2f} {"*" if c["em"] else " "} {c["html"]}')
````


### `projekty/styl4/zones_ad11.json`

````json
[]
````


### `projekty/styl4/engine/overlay4.html`

````html
<!doctype html><html><head><meta charset="utf-8">
<!-- Style 4: plain caption layer after Konrad's reference (Poppins ExtraBold caps, 2-3 words, hard cuts, rare yellow emphasis) -->
<link rel="stylesheet" href="../../reklamy_CA/engine/assets/fonts/poppins.css">
<style>
html,body{margin:0;background:transparent}
#stage{position:relative;width:1080px;height:1920px;overflow:hidden}
#cap{position:absolute;left:50px;right:50px;text-align:center;transform:translateY(-50%);font-family:'Poppins',sans-serif;font-weight:800;
 text-transform:uppercase;color:#fff;letter-spacing:-.005em;line-height:1.08;
 text-shadow:0 0 5px rgba(0,0,0,.95),0 2px 4px rgba(0,0,0,.6),0 6px 18px rgba(0,0,0,.95),0 12px 52px rgba(0,0,0,.82)}
#cap.n{font-size:64px}
#cap.em{font-size:96px;color:#FFE600;line-height:1.02}
</style></head><body><div id="stage"><div id="cap"></div></div>
<script>
let SPEC=null,last=-2;const H=1920;
window.init=(s)=>{SPEC=s;return true};
window.seek=(t)=>{const c=document.getElementById('cap');
 const i=SPEC.caps.findIndex(b=>t>=b.t0-1e-3&&t<b.t1);
 if(i!==last){last=i;if(i<0){c.style.visibility='hidden'}else{const b=SPEC.caps[i];c.className=b.em?'em':'n';c.innerHTML=b.html;c.style.visibility='visible'}}
 if(i>=0){const ov=(SPEC.zones||[]).find(z=>t>=z.t0&&t<z.t1);c.style.top=((ov?ov.capY:SPEC.capY)*H)+'px'}
 return true};
</script></body></html>
````


### `projekty/styl5/build_spec5.py`

````python
#!/usr/bin/env python3
"""Style 5 ("Nie mów / Mów" reveal) spec.  usage: build_spec5.py OUT.json [tight]   (tight = jeslito2, closer framing: table right under the chin)
Each bar slides out LEAD s before the first word of its row is said (measured on the original: 0.1-0.2 s)."""
import json, sys
LEAD = 0.12
RED, GREEN = "#FC0000", "#00E000"
# (text on screen, time of the first spoken word of that phrase)  -- ad "jeslito" (16.1 s)
LEFT = [("więcej wolności", 0.66), ("zarabiać więcej", 2.84), ("osiągnąć sukces", 5.48), ("zbudować majątek", 8.40), ("rozwijać się", 11.16)]
RIGHT = [("zarabiać pieniądze", 1.62), ("rozwiązywać problemy", 4.20), ("podejmować ryzyko", 6.44), ("cierpliwość", 9.58), ("wyjść ze strefy komfortu", 11.96)]
# 1080x1920. Original (720x1280): columns 333 px wide, bars 60 px high every 70 px, header 78 px; table lower here so it stays under the mouth.
layout = dict(colX=[70, 560], colW=450, hdY=1180, barY=1245, barH=60, pitch=70, fs=40, exitDur=0.71)
if len(sys.argv) > 2 and sys.argv[2] == "tight": layout.update(hdY=1030, barY=1095)
spec = dict(dur=16.133, fps=30, layout=layout, cols=[
    dict(head="Jeśli chcesz", color=RED, rows=[dict(text=t, t=round(s - LEAD, 3)) for t, s in LEFT]),
    dict(head="Musisz", color=GREEN, rows=[dict(text=t, t=round(s - LEAD, 3)) for t, s in RIGHT])])
json.dump(spec, open(sys.argv[1], "w"), ensure_ascii=False, indent=1)
````


### `projekty/styl5/engine/overlay5.html`

````html
<!doctype html><html><head><meta charset="utf-8">
<!-- Style 5: "Nie mów / Mów" two-column reveal (Konrad's viral reel). Coloured bars cover the words and slide out sideways,
     left bar to the left, right bar to the right, linearly in 0.2 s, just before each word is said. Nothing else on screen. -->
<link rel="stylesheet" href="../../reklamy_CA/engine/assets/fonts/g.css">
<style>
html,body{margin:0;background:transparent}
#stage{position:relative;width:1080px;height:1920px;overflow:hidden;font-family:'Inter',sans-serif}
.hd{position:absolute;font-weight:800;font-size:78px;letter-spacing:-.045em;line-height:1;text-align:center;white-space:nowrap;
 text-shadow:0 3px 6px rgba(0,0,0,.55),0 0 18px rgba(0,0,0,.35)}
.tx{position:absolute;font-weight:700;color:#fff;letter-spacing:-.03em;text-align:center;white-space:nowrap;
 text-shadow:0 2px 5px rgba(0,0,0,.6),0 0 14px rgba(0,0,0,.35)}
.bar{position:absolute;border-radius:9px}
</style></head><body><div id="stage"></div>
<script>
let SPEC=null;const st=()=>document.getElementById('stage');
function el(cls,css,html){const e=document.createElement('div');e.className=cls;Object.assign(e.style,css);if(html!=null)e.innerHTML=html;st().appendChild(e);return e}
window.init=(s)=>{SPEC=s;const L=s.layout;
 s.cols.forEach((c,ci)=>{const x0=L.colX[ci],w=L.colW;
  el('hd',{left:(x0+w/2)+'px',top:(L.hdY-39)+'px',transform:'translateX(-50%)',color:c.color},c.head);
  c.rows.forEach((r,ri)=>{const y=L.barY+ri*L.pitch;
   const t=el('tx',{left:x0+'px',width:w+'px',top:y+'px',height:L.barH+'px',lineHeight:L.barH+'px',fontSize:L.fs+'px'},r.text);
   r.tx=t;
   r.bar=el('bar',{left:x0+'px',width:w+'px',top:y+'px',height:L.barH+'px',background:c.color})})});
 // rows keep the original size; only a row that does not fit its column shrinks
 s.cols.flatMap(c=>c.rows).forEach(r=>{let f=L.fs;while(r.tx.scrollWidth>L.colW-12&&f>26){f-=1;r.tx.style.fontSize=f+'px'}});
 return true};
window.seek=(t)=>{const L=SPEC.layout;
 SPEC.cols.forEach((c,ci)=>c.rows.forEach(r=>{const p=Math.max(0,(t-r.t)/L.exitDur);   // linear slide, like the original
  const dx=p<=0?0:p*(1080+L.colW)*(ci?1:-1);r.bar.style.transform=`translateX(${dx}px)`;r.bar.style.visibility=p>=1?'hidden':'visible'}));
 return true};
</script></body></html>
````


### `projekty/styl6/build_spec6.py`

````python
#!/usr/bin/env python3
"""Style 6 ("10/10" list) spec.  usage: build_spec6.py WORKDIR NAME   (reads WORKDIR/NAME.mp4 + WORKDIR/tr_NAME.json)
Script text is aligned onto whisper word times; captions = 2-3 words, hard cuts. Each emoji swaps in on the first word
of its point (snapped back to a camera cut when one is within 0.3 s before)."""
import difflib, json, os, re, subprocess, sys
WD, NAME = sys.argv[1], sys.argv[2]
HERE = os.path.dirname(os.path.abspath(__file__))
norm = lambda t: re.sub(r"[^\w]", "", t.lower())
WEAK = {"i", "w", "z", "na", "do", "a", "o", "że", "się", "to", "nie", "co", "ale", "ten", "niż"}

TITLE = ""  # Konrad: no title pill
SCRIPT = ("10 na 10 prostych nawyków, których nikt Cię nie uczy, a zmienią Twoje życie. "
          "Ustawiaj budzik na godzinę, o której masz iść spać, a nie wstawać. Przestań oglądać wiadomości. "
          "Naucz się mówić nie częściej niż tak. Przestań obserwować ludzi na Instagramie, z którymi nawet nie przywitałbyś się na ulicy. "
          "Pamiętaj, że możesz odpuścić jeden dzień, ale nigdy dwa dni z rzędu. Inwestuj w siebie. "
          "Otaczaj się ludźmi, którzy osiągnęli więcej niż Ty. Czytaj codziennie minimum 10 stron książki. "
          "Zawsze zakładaj dobre intencje. Rób codziennie coś, czego się boisz. Zaobserwuj ten profil.")
# point -> (emoji, first word of the point in SCRIPT order)  -- same emoji as the original where the habit matches
POINTS = [("⏰", "Ustawiaj"), ("📺", "Przestań"), ("🚫", "Naucz"), ("📱", "Przestań"), ("💪", "Pamiętaj"),
          ("📈", "Inwestuj"), ("🤝", "Otaczaj"), ("📖", "Czytaj"), ("💡", "Zawsze"), ("😨", "Rób")]
APPLE = os.path.join(HERE, "engine", "emoji_apple")  # Apple emoji PNGs (emoji-datasource-apple, 64 px), file = codepoint
apple = lambda e: os.path.join(APPLE, "-".join(f"{ord(ch):x}" for ch in e if ord(ch) != 0xFE0F) + ".png")
COLORS = ["#FFFFFF", "#FD0004", "#F9A901", "#ADFA01", "#03FC04", "#00FCAC", "#03A8F8", "#0500FA", "#A700FE", "#FC00A7"]


def align(words, text):
    toks = [{"d": w} for w in text.split()]
    a = [norm(w["w"]) for w in words]; b = [norm(t["d"]) for t in toks]; T = [None] * len(toks); E = [None] * len(toks)
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        if op == "equal":
            for k in range(i2 - i1): T[j1 + k], E[j1 + k] = words[i1 + k]["s"], words[i1 + k]["e"]
        elif op == "replace":
            s0, e0 = words[i1]["s"], words[i2 - 1]["e"]; n = j2 - j1
            for j in range(j1, j2): T[j] = s0 + (e0 - s0) * (j - j1) / n; E[j] = s0 + (e0 - s0) * (j - j1 + 1) / n
    for j in range(len(toks)):
        if T[j] is None: T[j] = next((E[k] for k in range(j - 1, -1, -1) if E[k] is not None), 0.0); E[j] = T[j] + .2
        toks[j]["t"], toks[j]["e"] = round(T[j], 3), round(E[j], 3)
    return toks


def chunk(toks, maxw=3, maxc=16):
    out, cur = [], []
    for u in toks:
        if cur and (len(cur) >= maxw or sum(len(x["d"]) + 1 for x in cur) + len(u["d"]) > maxc):
            carry = []
            while len(cur) > 1 and cur[-1]["d"][-1].isalnum() and cur[-1]["d"].lower() in WEAK: carry.insert(0, cur.pop())
            out.append(cur); cur = carry
        cur.append(u)
        if u["d"][-1] in ".?!" or (u["d"][-1] == "," and len(cur) >= 2): out.append(cur); cur = []
    if cur: out.append(cur)
    return out


src = os.path.join(WD, NAME + ".mp4")
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", src], capture_output=True, text=True).stdout)
cuts = json.loads(subprocess.run([sys.executable, os.path.join(HERE, "..", "reklamy_CA", "engine", "cuts.py"), src], capture_output=True, text=True).stdout)
words = [w for s in json.load(open(os.path.join(WD, "tr_" + NAME + ".json"))) for w in s["words"]]
toks = align(words, SCRIPT)
ch = chunk(toks)
caps = []
for i, c in enumerate(ch):
    nxt = ch[i + 1][0]["t"] - 0.03 if i + 1 < len(ch) else dur
    t1 = nxt if nxt - c[-1]["e"] < 0.7 else min(nxt, c[-1]["e"] + 0.35)
    caps.append(dict(t0=round(max(0, c[0]["t"] - 0.03), 3), t1=round(t1, 3), text=" ".join(w["d"] for w in c).rstrip(",.")))
# swap times: k-th occurrence of each point's first word, after the hook sentence
items, pos = [], next(i for i, t in enumerate(toks) if t["d"].rstrip(".,").lower() == "ustawiaj")
for k, (emo, first) in enumerate(POINTS):
    j = next(i for i in range(pos, len(toks)) if toks[i]["d"].rstrip(".,") == first); pos = j + 1
    t = toks[j]["t"] - 0.05; c = [x for x in cuts if 0 <= t - x <= 0.3]
    img = apple(emo); items.append(dict(emoji=emo, img=img if os.path.exists(img) else None, color=COLORS[k], t=round(c[-1] if c else t, 3)))
# 1080x1920. Original (720x1280): title pill y 215-325, grid 534x164 at y 756, caption centre y 706. Here 6-7% lower (mouth sits lower).
layout = dict(titleY=318, titleFs=50, gridY=1268, cellW=148, cellH=111, capY=1192)
json.dump(dict(dur=round(dur, 3), fps=30, title=TITLE, layout=layout, items=items, caps=caps),
          open(os.path.join(WD, f"spec6_{NAME}.json"), "w"), ensure_ascii=False, indent=1)
for it in items: print(f'{it["t"]:6.2f} {it["emoji"]}')
for c in caps: print(f'{c["t0"]:6.2f}-{c["t1"]:6.2f} {c["text"]}')
````


### `projekty/styl6/engine/overlay6.html`

````html
<!doctype html><html><head><meta charset="utf-8">
<!-- Style 6: "10/10" list format (friend's reel). White title pill on top, 2x5 grid of coloured numbers that turn into emoji
     when the point is said (number fades in 3 frames, emoji appears at full size), Anton caps captions above the grid. -->
<link rel="stylesheet" href="../../reklamy_CA/engine/assets/fonts/fmt6.css">
<link rel="stylesheet" href="../../reklamy_CA/engine/assets/fonts/g.css">
<style>
html,body{margin:0;background:transparent}
#stage{position:relative;width:1080px;height:1920px;overflow:hidden}
#title{position:absolute;left:50%;transform:translateX(-50%);background:#fff;border-radius:16px;padding:18px 34px 20px;
 font-family:'Poppins',sans-serif;font-weight:500;color:#111;text-align:center;line-height:1.18;white-space:nowrap;
 box-shadow:0 6px 24px rgba(0,0,0,.18)}
#grid{position:absolute;left:50%;transform:translateX(-50%);display:grid;border:7px solid #fff;border-radius:22px;background:transparent;gap:8px;overflow:hidden;
 box-shadow:0 6px 26px rgba(0,0,0,.28)}
.cell{position:relative;border-radius:12px;background:rgba(232,238,250,.2);box-shadow:0 0 0 4px #fff}  /* neighbouring outlines form the 8 px white lines */
#gridwrap{position:absolute;inset:0}
.cell .n,.cell .e{position:absolute;inset:0;display:flex;align-items:center;justify-content:center}
.cell .n{font-family:'Poppins',sans-serif;font-weight:600;font-size:76px;letter-spacing:-.03em;-webkit-text-stroke:3px #000;paint-order:stroke fill;
 text-shadow:0 4px 8px rgba(0,0,0,.55)}
.cell .e{font-family:'Noto Color Emoji';font-size:76px;line-height:1}
.cell .e img{width:68px;height:68px;image-rendering:auto}  /* Apple emoji PNG (64 px source) */
.dia{position:absolute;width:14px;height:14px;background:#fff;transform:translate(-50%,-50%) rotate(45deg)}
#cap{position:absolute;left:40px;right:40px;text-align:center;transform:translateY(-50%);font-family:'Inter',sans-serif;font-weight:700;font-size:64px;
 color:#fff;letter-spacing:-.05em;line-height:1.05;
 text-shadow:0 0 4px rgba(0,0,0,.85),0 3px 8px rgba(0,0,0,.75),0 8px 26px rgba(0,0,0,.5)}
</style></head><body><div id="stage"><div id="title"></div><div id="grid"></div><div id="cap"></div></div>
<script>
let SPEC=null,last=-2;const $=id=>document.getElementById(id);
window.init=(s)=>{SPEC=s;const L=s.layout;
 const ti=$('title');if(s.title){ti.innerHTML=s.title;Object.assign(ti.style,{top:L.titleY+'px',fontSize:L.titleFs+'px'})}else ti.style.display='none';
 const g=$('grid');Object.assign(g.style,{top:L.gridY+'px',gridTemplateColumns:`repeat(5,${L.cellW}px)`,gridTemplateRows:`repeat(2,${L.cellH}px)`});
 s.items.forEach((it,i)=>{const c=document.createElement('div');c.className='cell';
  c.innerHTML=`<div class="n" style="color:${it.color}">${i+1}</div><div class="e">${it.img?`<img src="${it.img}">`:it.emoji}</div>`;g.appendChild(c);it.n=c.children[0];it.e=c.children[1]});
 // little white diamonds where the inner lines cross the border and each other (as in the original)
 const st=$('stage');const W=5*L.cellW+4*8,x0=540-W/2,y0=L.gridY+7;
 for(let k=1;k<5;k++)for(const y of [y0,y0+L.cellH+4,y0+2*L.cellH+8]){const d=document.createElement('div');d.className='dia';
  Object.assign(d.style,{left:(x0+k*(L.cellW+8)-4)+'px',top:y+'px'});st.appendChild(d)}
 return true};
window.seek=(t)=>{const fd=0.1;
 SPEC.items.forEach(it=>{const p=Math.min(1,Math.max(0,(t-it.t)/fd));it.n.style.opacity=1-p;it.n.style.transform=`scale(${1-.25*p})`;it.e.style.opacity=t>=it.t+0.033?1:0});
 const c=$('cap');const i=SPEC.caps.findIndex(b=>t>=b.t0-1e-3&&t<b.t1);
 if(i!==last){last=i;if(i<0)c.style.visibility='hidden';else{c.textContent=SPEC.caps[i].text;c.style.visibility='visible'}}
 c.style.top=(SPEC.layout.capY)+'px';return true};
</script></body></html>
````


### `projekty/styl7/build_spec7.py`

````python
#!/usr/bin/env python3
"""Style 7 ("8 rzeczy" numbered list) spec.  usage: build_spec7.py OUT.json
Video already cut and letterboxed by Konrad (band y 656-1263, picture x 0-871); list sits on the right of the band."""
import json, sys
TITLE = ""  # Konrad: no title
# (text from Konrad, start of the sentence in 8thingsprivate.mp4)
ITEMS = [("ile zarabiasz", 0.0), ("swoje plany", 1.16), ("problemy rodzinne", 2.54), ("problem w związku", 4.44),
         ("swoje słabości", 6.40), ("problemy finansowe", 8.02), ("trzymaj sekrety", 11.32), ("głupie błędy", 13.48)]
# original 720x1280 x1.5: title ~54 px above the band, numbers ~48 px, items ~39 px; pitch squeezed to fit Konrad's lower band
layout = dict(titleX=52, titleY=566, titleFs=54, listX=620, listY=700, pitch=68, numFs=32, fs=27)  # list ~30% smaller (Konrad)
json.dump(dict(dur=17.133, fps=30, title=TITLE, layout=layout, items=[dict(text=t[0].upper() + t[1:], t=s) for t, s in ITEMS]),
          open(sys.argv[1], "w"), ensure_ascii=False, indent=1)
````


### `projekty/styl7/engine/overlay7.html`

````html
<!doctype html><html><head><meta charset="utf-8">
<!-- Style 7: "8 things you must keep PRIVATE" (friend's reel). Black frame with the video band in the middle, white title above the band,
     numbered list on the band: all numbers visible from the start, each item's text appears (hard cut) when its sentence starts. -->
<link rel="stylesheet" href="../../reklamy_CA/engine/assets/fonts/fmt6.css">
<style>
html,body{margin:0;background:transparent}
#stage{position:relative;width:1080px;height:1920px;overflow:hidden;font-family:'Poppins',sans-serif;color:#fff}
#title{position:absolute;font-weight:500;white-space:nowrap;letter-spacing:-.005em}
.row{position:absolute;display:flex;align-items:baseline;white-space:nowrap;text-shadow:0 2px 6px rgba(0,0,0,.55)}
.row .n{font-weight:500;margin-right:.18em}
.row .t{font-weight:500}
</style></head><body><div id="stage"><div id="title"></div></div>
<script>
let SPEC=null;
window.init=(s)=>{SPEC=s;const L=s.layout,st=document.getElementById('stage'),ti=document.getElementById('title');
 ti.innerHTML=s.title;Object.assign(ti.style,{left:L.titleX+'px',top:L.titleY+'px',fontSize:L.titleFs+'px'});
 s.items.forEach((it,i)=>{const r=document.createElement('div');r.className='row';
  r.innerHTML=`<span class="n" style="font-size:${L.numFs}px">${i+1}.</span><span class="t" style="font-size:${L.fs}px">${it.text}</span>`;
  Object.assign(r.style,{left:L.listX+'px',top:(L.listY+i*L.pitch)+'px'});st.appendChild(r);it.t_el=r.children[1]});
 return true};
window.seek=(t)=>{SPEC.items.forEach(it=>it.t_el.style.visibility=t>=it.t-1e-3?'visible':'hidden');return true};
</script></body></html>
````


### `projekty/styl8/build_spec8.py`

````python
#!/usr/bin/env python3
"""Style 8 (tier list) spec.  usage: build_spec8.py WORKDIR NAME   (WORKDIR/NAME.mp4 + WORKDIR/tr_NAME.json)"""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "styl6"))
WD, NAME = sys.argv[1], sys.argv[2]
HERE = os.path.dirname(os.path.abspath(__file__)); EM = os.path.join(HERE, "engine", "emoji_apple")
import importlib.util, subprocess
spec6 = open(os.path.join(HERE, "..", "styl6", "build_spec6.py")).read()
import re, difflib
norm = lambda t: re.sub(r"[^\w]", "", t.lower())
WEAK = {"i", "w", "z", "na", "do", "a", "o", "że", "się", "to", "nie", "co", "ale", "ten", "niż", "go"}
exec(spec6[spec6.index("def align"):spec6.index("src = os.path.join")])          # reuse align() + chunk() from style 6
import re, difflib
norm = lambda t: re.sub(r"[^\w]", "", t.lower())
WEAK = {"i", "w", "z", "na", "do", "a", "o", "że", "się", "to", "nie", "co", "ale", "ten", "niż", "go", "na"}
SCRIPT = ("Dropshipping z AI: D. Większość ludzi, którzy go promują, zarabia więcej na sprzedawaniu Ci narzędzi niż na samym dropshippingu. "
          "Modelki AI: F. Chyba nie muszę komentować. AI YouTube Shorts: poziom C. Fajne pod wyświetlenia, ale YouTube przestał płacić za content AI. "
          "Budowanie stron: F. AI zastąpiło Cię 3 lata temu, a Twój lokalny dentysta nie potrzebuje kolejnej strony. "
          "Montowanie filmów: poziom B. Da się na tym zarobić, ale to po prostu drugi etat. Tworzenie AI agentów i automatyzacji: poziom A. "
          "Większość firm w Polsce tego nie ma, tylko musisz tłumaczyć 60-latkom, co to AI, i cały czas gonić klientów. "
          "Tworzenie prostych produktów cyfrowych z pomocą AI: poziom S. Możesz stworzyć produkt w 100% z AI, a później sprzedawać go wielokrotnie "
          "bez konieczności wykonywania całej pracy od nowa. Plus cały content AI wchodzi bardzo mocno w viral. Dlatego zamiast szukać kolejnego "
          "sposobu na szybkie pieniądze, zacznij budować coś, co realnie działa. A jeżeli chcesz dowiedzieć się, jak to zrobić, "
          "skomentuj „AI”, a wyślę Ci mój cały poradnik.")
# (label, emoji codepoint, tier, drop time = when the tier letter is said, tray order)
ITEMS = [("Dropshipping z AI", "1f4e6", "D", 0.80, 3), ("Modelki AI", "1f483", "F", 5.60, 0), ("AI YouTube Shorts", "1f3ac", "C", 8.30, 5),
         ("Strony WWW", "1f4bb", "F", 11.92, 1), ("Montaż filmów", "1f3a5", "B", 17.20, 6), ("AI agenci", "1f916", "A", 21.56, 2),
         ("Produkty cyfrowe", "1f4d8", "S", 28.98, 4)]
TIERS = [("S", "#FF8A7B"), ("A", "#FFC079"), ("B", "#FFDA76"), ("C", "#FEF575"), ("D", "#B9F078"), ("F", "#73EA7B")]
src = os.path.join(WD, NAME + ".mp4")
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", src], capture_output=True, text=True).stdout)
words = [w for s in json.load(open(os.path.join(WD, "tr_" + NAME + ".json"))) for w in s["words"]]
ch = chunk(align(words, SCRIPT), maxw=3, maxc=18)
caps = []
for i, c in enumerate(ch):
    nxt = ch[i + 1][0]["t"] - 0.03 if i + 1 < len(ch) else dur
    t1 = nxt if nxt - c[-1]["e"] < 0.7 else min(nxt, c[-1]["e"] + 0.35)
    caps.append(dict(t0=round(max(0, c[0]["t"] - 0.03), 3), t1=round(t1, 3), text=" ".join(w["d"] for w in c).rstrip(",.:")))
# original 720x1280 x1.5: panel to y 808, title pill y 115-172, rows 64 px every 72 px from y 198, labels x 47-113, bars x 122-672, tray ~y 640
layout = dict(panelH=0, titleY=150, titleFs=56, rowsY=282, rowH=96, pitch=108, labX=70, labW=99, barX=183, marginR=72,
              slot=84, nameFs=32, tray=72, trayGap=14, trayY=950, capY=1054, dragDur=0.6)
spec = dict(dur=round(dur, 3), fps=30, title="TIERLISTA <b>AI BIZNESÓW</b>", layout=layout, hand=os.path.join(EM, "1f446.png"),
            tiers=[dict(k=k, c=c) for k, c in TIERS], caps=caps,
            items=[dict(name=n, img=os.path.join(EM, e + ".png"), tier=tr, t=t, tray=o) for n, e, tr, t, o in ITEMS],
            ctaT=42.55, ctaType=42.72, ctaWord="AI", ctaPost=43.35)
json.dump(spec, open(os.path.join(WD, f"spec8_{NAME}.json"), "w"), ensure_ascii=False, indent=1)
for c in caps: print(f'{c["t0"]:6.2f} {c["text"]}')
````


### `projekty/styl8/facecrop.py`

````python
#!/usr/bin/env python3
"""Face-tracked crop for the rounded video card.  usage: facecrop.py IN.mp4 OUT.mp4 W H [face_y=0.42]
Scales the source to width W, detects the face every frame (OpenCV YuNet), smooths the centre (centred moving average,
dead-zone so small head moves don't wobble the frame) and crops a W x H window so the face sits at face_y of the card."""
import subprocess, sys
import numpy as np, cv2
src, out, W, H = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]); fy = float(sys.argv[5]) if len(sys.argv) > 5 else 0.42
cap = cv2.VideoCapture(src); fps = cap.get(cv2.CAP_PROP_FPS)
import os
det = None  # YuNet face detector (opencv_zoo), created on the first frame
frames, cy, cx = [], [], []
while True:
    ok, f = cap.read()
    if not ok: break
    f = cv2.resize(f, (W, int(round(f.shape[0] * W / f.shape[1] / 2)) * 2)); frames.append(f)
    g = cv2.resize(f, None, fx=.4, fy=.4)
    if det is None: det = cv2.FaceDetectorYN.create(os.path.join(os.path.dirname(os.path.abspath(__file__)), "face_yunet.onnx"), "", (g.shape[1], g.shape[0]), 0.6)
    _, d = det.detect(g)
    if d is not None and len(d): x, y, w, h = max(d[:, :4], key=lambda r: r[2] * r[3]); cy.append((y + h / 2) / .4); cx.append((x + w / 2) / .4)
    else: cy.append(np.nan); cx.append(np.nan)
FH = frames[0].shape[0]; cy = np.array(cy)
idx = np.arange(len(cy)); ok = ~np.isnan(cy)
cy = np.interp(idx, idx[ok], cy[ok]) if ok.any() else np.full(len(cy), FH * .4)
k = int(fps * 0.6) | 1; pad = np.pad(cy, k // 2, mode="edge"); cy = np.convolve(pad, np.ones(k) / k, mode="valid")   # smooth ~0.6 s
# dead-zone: follow only when the face drifts > 3% of the card
ys, cur = [], cy[0]
for v in cy:
    if abs(v - cur) > H * .03: cur += (v - cur) - np.sign(v - cur) * H * .03
    ys.append(cur)
top = np.clip(np.array(ys) - fy * H, 0, FH - H).astype(int)
p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", str(fps), "-i", "-",
                      "-i", src, "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-crf", "14", "-preset", "fast", "-c:a", "copy", out], stdin=subprocess.PIPE)
for f, t in zip(frames, top): p.stdin.write(f[t:t + H].tobytes())
p.stdin.close(); p.wait()
print("face found in", int(ok.sum()), "/", len(ok), "frames; crop top range", top.min(), "-", top.max())
````


### `projekty/styl8/engine/overlay8.html`

````html
<!doctype html><html><head><meta charset="utf-8">
<!-- Style 8: tier list (friend's reel "AI SIDE HUSTLES TIER LIST"). Top 1212 px = dark panel with title pill, S-F rows and a tray of
     icon tiles; a hand cursor drags each tile into its row as the tier is said, label appears next to it. White caption pill under the
     panel; speaker video sits under it (composited outside). Ends with a comment box typing the keyword and "Post". -->
<link rel="stylesheet" href="../../reklamy_CA/engine/assets/fonts/g.css">
<style>
html,body{margin:0;background:transparent}
#stage{position:relative;width:1080px;height:1920px;overflow:hidden;font-family:'Inter',sans-serif}
#panel{position:absolute;left:0;top:0;width:1080px;background:linear-gradient(180deg,#29282D,#1D1C21)}
#title{position:absolute;left:50%;transform:translateX(-50%);background:#fff;border-radius:14px;padding:10px 30px 12px;white-space:nowrap;
 font-weight:900;letter-spacing:-.045em;color:#0a0a0a;line-height:1}
#title b{font-weight:900;background:linear-gradient(180deg,#42BDFF,#0092FF);-webkit-background-clip:text;background-clip:text;color:transparent}
.lab{position:absolute;border-radius:14px;display:flex;align-items:center;justify-content:center;font-weight:900;color:#111;
 box-shadow:inset 0 -4px 0 rgba(0,0,0,.12)}
.bar{position:absolute;border-radius:14px;background:#100F12}
.tile{position:absolute;border-radius:20px;background:linear-gradient(180deg,#fff,#E9EAEE);box-shadow:0 4px 10px rgba(0,0,0,.35);
 display:flex;align-items:center;justify-content:center;transform-origin:center}
.tile img{width:70%;height:70%}
.name{position:absolute;color:#fff;font-weight:600;letter-spacing:-.02em;white-space:nowrap}
#cap{position:absolute;left:50%;transform:translateX(-50%);background:#fff;border-radius:12px;padding:8px 22px 10px;font-weight:800;
 font-size:40px;letter-spacing:-.035em;color:#0a0a0a;white-space:nowrap;line-height:1.05}
#hand{position:absolute;width:64px;height:64px;pointer-events:none}
#cbox{position:absolute;left:50%;transform:translateX(-50%);width:780px;height:84px;border-radius:42px;background:#fff;display:flex;align-items:center;
 box-shadow:0 6px 20px rgba(0,0,0,.35)}
#cbox .av{width:52px;height:52px;border-radius:50%;background:#D9DBE1;margin:0 18px 0 16px;display:flex;align-items:center;justify-content:center}
#cbox .tx{flex:1;font-weight:700;font-size:36px;color:#111;letter-spacing:-.02em}
#cbox .btn{margin-right:14px;height:58px;padding:0 30px;border-radius:29px;background:#1A8CFF;color:#fff;font-weight:700;font-size:30px;display:flex;align-items:center}
#cbox .btn.done{background:#EDEEF2;color:#555}
</style></head><body><div id="stage"><div id="panel"></div><div id="title"></div><div id="cap"></div><div id="cbox"></div>
<img id="hand"></div>
<script>
let SPEC=null,lastCap=-2;const $=id=>document.getElementById(id);
const E=t=>t<.5?4*t*t*t:1-Math.pow(-2*t+2,3)/2, cl=x=>Math.max(0,Math.min(1,x)), lerp=(a,b,p)=>a+(b-a)*p;
function el(cls,parent,html){const e=document.createElement('div');e.className=cls;if(html!=null)e.innerHTML=html;(parent||$('stage')).appendChild(e);return e}
window.init=(s)=>{SPEC=s;const L=s.layout;
 Object.assign($('panel').style,{height:L.panelH+'px'});
 const ti=$('title');ti.innerHTML=s.title;Object.assign(ti.style,{top:L.titleY+'px',fontSize:L.titleFs+'px'});
 L.rows=s.tiers.map((t,i)=>{const y=L.rowsY+i*L.pitch;
  const lb=el('lab');lb.textContent=t.k;Object.assign(lb.style,{left:L.labX+'px',top:y+'px',width:L.labW+'px',height:L.rowH+'px',fontSize:(L.rowH*.55)+'px',
   background:`linear-gradient(180deg,${t.c} 0%,${t.c} 60%,${t.c2||t.c} 100%)`});
  const b=el('bar');Object.assign(b.style,{left:L.barX+'px',top:y+'px',width:(1080-L.barX-L.marginR)+'px',height:L.rowH+'px'});
  return {k:t.k,y,x:L.barX+12}});
 // tiles start in the tray; slot positions are fixed per row in order of arrival
 const n=s.items.length;s.items.forEach((it,i)=>{const t=el('tile');t.innerHTML=`<img src="${it.img}">`;it.el=t;
  const nm=el('name');nm.textContent=it.name;nm.style.fontSize=L.nameFs+'px';nm.style.visibility='hidden';it.nm=nm;it.tray=i});
 s.items.slice().sort((a,b)=>a.t-b.t).forEach(it=>{const r=L.rows.find(r=>r.k===it.tier);it.sx=r.x;it.sy=r.y+(L.rowH-L.slot)/2;
  it.nm.style.left=(it.sx+L.slot+12)+'px';it.nm.style.top=(r.y+L.rowH/2-L.nameFs*.62)+'px';r.x+=L.slot+12+it.nm.getBoundingClientRect().width+28});
 $('hand').src=s.hand;
 const cb=$('cbox');cb.innerHTML=`<div class="av"><svg width="30" height="30" viewBox="0 0 24 24" fill="#8A8F9C"><circle cx="12" cy="8" r="4.5"/><path d="M3 21c0-5 4-7.5 9-7.5s9 2.5 9 7.5z"/></svg></div><div class="tx"></div><div class="btn">Post</div>`;
 cb.style.top=L.trayY+'px';
 return true};
function trayX(order,k,L){const w=L.tray,g=L.trayGap,W=order*w+(order-1)*g;return 540-W/2+k*(w+g)}
window.seek=(t)=>{const L=SPEC.layout,s=SPEC,items=s.items;let handPos=null,handOp=0;
 const pickT=it=>it.t-L.dragDur-0.15;
 // tray layout at time tt (tiles that have not been picked yet, re-centred); deterministic so frames can render in any order
 const inTray=tt=>items.filter(o=>tt<pickT(o)+0.15).sort((a,b)=>a.tray-b.tray);
 const trayPos=(it,tt)=>{const l=inTray(tt);const k=l.indexOf(it);return k<0?null:trayX(l.length,k,L)};
 const deps=items.map(o=>pickT(o)+0.15).filter(d=>d<=t);const lastDep=deps.length?Math.max(...deps):-9;
 items.forEach(it=>{
  const p0=pickT(it),p1=p0+0.15,p2=it.t;let x,y,sz,sc=1;
  const at=tt=>{const now=trayPos(it,tt);const ld=Math.max(-9,...items.map(o=>pickT(o)+0.15).filter(d=>d<=tt));
   if(tt-ld<0.25){const before=trayPos(it,ld-1e-3);if(before!=null&&now!=null)return lerp(before,now,E((tt-ld)/0.25))}return now};
  if(t<p1){x=at(t);y=L.trayY;sz=L.tray;
   if(t>=p0){sc=1+.14*E(cl((t-p0)/.12));handPos=[x+sz*.55,y+sz*.45];handOp=cl((t-p0)/.08)}}
  else{const fx=at(p1-1e-3),fy=L.trayY;
   if(t<p2){const p=E(cl((t-p1)/(p2-p1)));x=lerp(fx,it.sx,p);y=lerp(fy,it.sy,p);sz=lerp(L.tray,L.slot,p);sc=1.14-.14*p;
    handPos=[x+sz*.55,y+sz*.45];handOp=1}
   else{x=it.sx;y=it.sy;sz=L.slot;const q=cl((t-p2)/.12);sc=1+.06*Math.sin(q*Math.PI);
    if(t<p2+.35){handPos=[x+sz*.55,y+sz*.45];handOp=1-cl((t-p2-.15)/.2)}}}
  Object.assign(it.el.style,{left:x+'px',top:y+'px',width:sz+'px',height:sz+'px',transform:`scale(${sc})`,zIndex:t>=p0&&t<p2+.2?5:1});
  it.nm.style.visibility=t>=p2?'visible':'hidden';it.nm.style.opacity=cl((t-p2)/.12)});
 // comment box CTA
 const cb=$('cbox');if(t>=s.ctaT){cb.style.display='flex';const typed=s.ctaWord.slice(0,Math.max(0,Math.floor((t-s.ctaType)/.16)+1)*(t>=s.ctaType?1:0));
  cb.querySelector('.tx').textContent=typed+(t<s.ctaPost&&Math.floor(t*2.5)%2===0?'|':'');
  const btn=cb.querySelector('.btn');const posted=t>=s.ctaPost+.12;btn.className='btn'+(posted?' done':'');btn.textContent=posted?'Posted ✓':'Post';
  if(t>=s.ctaPost-.45&&t<s.ctaPost+.5){const bx=540+390-14-70,by=L.trayY+42;handPos=[lerp(540,bx,E(cl((t-s.ctaPost+.45)/.4))),by];handOp=1-cl((t-s.ctaPost-.3)/.2)}}
 else cb.style.display='none';
 const h=$('hand');if(handPos&&handOp>0){Object.assign(h.style,{left:handPos[0]+'px',top:handPos[1]+'px',opacity:handOp,display:'block'})}else h.style.display='none';
 // captions: hard cuts, white pill
 const c=$('cap');const i=s.caps.findIndex(b=>t>=b.t0-1e-3&&t<b.t1);
 if(i!==lastCap){lastCap=i;if(i<0)c.style.visibility='hidden';else{c.textContent=s.caps[i].text;c.style.visibility='visible'}}
 c.style.top=L.capY+'px';
 return true};
</script></body></html>
````


### `projekty/styl9/build_spec9.py`

````python
#!/usr/bin/env python3
"""Style 9 (LEGO AI ad) spec.  usage: build_spec9.py WORKDIR NAME   (WORKDIR/NAME.mp4 + WORKDIR/tr_NAME.json)
Captions from the script aligned onto whisper times (1-2 words, hard cuts), never crossing a hook boundary cut;
plus the original's extra layer (red boxes, money rain/burst, CTA arrow) and blur-in on a few section cuts (done in compose)."""
import difflib, json, os, re, subprocess, sys
WD, NAME = sys.argv[1], sys.argv[2]
HERE = os.path.dirname(os.path.abspath(__file__)); EM = os.path.join(HERE, "engine", "emoji_apple")
norm = lambda t: re.sub(r"[^\w]", "", t.lower())
WEAK = {"i", "w", "z", "na", "do", "a", "o", "że", "się", "to", "nie", "co", "ale", "ten", "niż", "go", "za", "tam", "bo", "od", "ci"}
s6 = open(os.path.join(HERE, "..", "styl6", "build_spec6.py")).read()
exec(s6[s6.index("def align"):s6.index("src = os.path.join")])      # align() + chunk() from style 6

SCRIPT = ("Otwórz TikToka. Zobaczysz tam dziesiątki postaci wygenerowanych przez sztuczną inteligencję. Ale najciekawsze jest to, "
          "że takie postacie są wykorzystywane do zarabiania tysięcy złotych miesięcznie. I nie, nie chodzi o pieniądze z wyświetleń. "
          "Otwórz TikToka i znajdź dowolną postać stworzoną przez AI. Teraz sprawdź jedną rzecz. Link w jej bio, bo właśnie tam może "
          "kryć się cały biznes, o którym większość ludzi nie ma pojęcia. Za takimi profilami często może stać coś znacznie ciekawszego "
          "niż same filmiki. Wyobraź sobie postać AI, która codziennie pokazuje proste przepisy kulinarne. A w swoim bio sprzedaje "
          "poradnik z przepisami za 79 złotych. Ktoś ogląda filmik, klika link i kupuje produkt. Bez magazynu. Bez wysyłania paczek. A ten "
          "sam produkt można sprzedawać wielokrotnie. I tutaj robi się naprawdę ciekawie. Bo AI może pomóc Ci nie tylko stworzyć taką "
          "postać. Może również znaleźć pomysł na produkt, przeanalizować rynek, stworzyć sam produkt, zbudować stronę sprzedażową "
          "i przygotować marketing. Czyli wykonać dużą część pracy, do której kiedyś potrzebowałeś kilku różnych umiejętności. "
          "Konrad, twórca Cyfrowego Autopilota, sprzedaje produkty cyfrowe od ponad 3 lat. W swoim najlepszym dniu sprzedał aż 941 "
          "e-booków. I na podstawie swojego doświadczenia stworzył system, który pokazuje, jak wykorzystać AI do budowania własnego "
          "biznesu cyfrowego. Od pomysłu do produktu i strony gotowej do sprzedaży w 48 godzin. Kliknij poniżej i zobacz, jak zacząć "
          "budować własny biznes cyfrowy z AI.")
HOOK_CUTS = (12.767, 23.133)        # hook 1 | hook 2 | body: no caption may straddle these (Konrad cuts the variants himself)
src = os.path.join(WD, NAME + ".mp4")
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", src], capture_output=True, text=True).stdout)
words = [w for s in json.load(open(os.path.join(WD, "tr_" + NAME + ".json"))) for w in s["words"]]
toks = align(words, SCRIPT)
for a, b in zip(toks, toks[1:]):                     # show "79 zł" although "79 złotych" is said
    if a["d"] == "79" and b["d"].startswith("złotych"): b["d"] = "zł" + b["d"][7:]
ch = chunk(toks, maxw=2, maxc=14)
merged = []                                          # no flash chunks: anything under 0.3 s joins its neighbour
for c in ch:
    if merged and (c[0]["t"] - merged[-1][0]["t"] < 0.3 or merged[-1][-1]["d"] == "79") and len(" ".join(w["d"] for w in merged[-1] + c)) <= 20 \
            and not merged[-1][-1]["d"].endswith((".", "?", "!")):
        merged[-1] = merged[-1] + c
    else: merged.append(c)
ch = merged
caps = []
for i, c in enumerate(ch):
    nxt = ch[i + 1][0]["t"] - 0.03 if i + 1 < len(ch) else dur
    t1 = nxt if nxt - c[-1]["e"] < 0.6 else min(nxt, c[-1]["e"] + 0.3)
    caps.append(dict(t0=round(max(0, c[0]["t"] - 0.03), 3), t1=round(t1, 3), text=" ".join(w["d"] for w in c).rstrip(",")))
for cut in HOOK_CUTS:
    for cp in caps:
        if cp["t0"] < cut < cp["t1"]:
            if cut - cp["t0"] > cp["t1"] - cut: cp["t1"] = cut
            else: cp["t0"] = cut
I = lambda c: os.path.join(EM, c + ".png")
MONEY, COINS = ["💵", "💵", "💸", "💵", "💰"], ["💰", "💵"]
FX = [dict(type="rain", t0=8.15, t1=10.43, emo=MONEY, n=26, spawn=1.3, seed=11),                 # "zarabiania tysięcy złotych miesięcznie"
      dict(type="box", t0=18.1, t1=18.66, x=350, y=1000, w=565, h=140, rot=3, r=34),              # "Link w jej bio"
      dict(type="box", t0=35.85, t1=37.36, x=595, y=1345, w=275, h=150, r=22),                     # "79 zł"
      dict(type="rain", t0=43.4, t1=44.75, emo=COINS, n=14, spawn=.8, seed=5),                   # "sprzedawać wielokrotnie"
      dict(type="burst", t0=68.84, t1=70.9, x=540, y=760, emo=MONEY, n=30, seed=9),              # "941"
      dict(type="arrow", t0=84.05, t1=dur, x=540, y=1560, size=170)]                              # CTA
BLUR_CUTS = [12.767, 23.133, 28.4, 62.067, 78.033]  # section changes: 0.2 s blur-in like the original
HIDE = [[66.7, 70.86]]                               # 941 scene already shows "e-booków w najlepszym dniu"
spec = dict(dur=round(dur, 3), fps=30, capY=0.645, caps=caps, fx=FX, blurCuts=BLUR_CUTS, hideCaps=HIDE)
json.dump(spec, open(os.path.join(WD, f"spec9_{NAME}.json"), "w"), ensure_ascii=False, indent=1)
for c in caps: print(f'{c["t0"]:6.2f} {c["text"]}')
````


### `projekty/styl9/compose9.py`

````python
#!/usr/bin/env python3
"""Style 9 compositor: source video + 0.2 s blur-in on spec["blurCuts"] + overlay PNG frames (+ original audio).
usage: compose9.py SPEC.json SRC.mp4 FRAMES_DIR OUT.mp4"""
import json, subprocess, sys
spec, src, frames, out = json.load(open(sys.argv[1])), sys.argv[2], sys.argv[3], sys.argv[4]
win = lambda a, b: "+".join(f"between(t,{c + a:.3f},{c + b:.3f})" for c in spec.get("blurCuts", [])) or "0"
vf = (f"[0:v]gblur=sigma=22:enable='{win(0, .1)}',gblur=sigma=9:enable='{win(.1, .2)}',gblur=sigma=3:enable='{win(.2, .27)}'[v];"
      f"[v][1]overlay=format=auto:eof_action=pass,format=yuv420p")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-framerate", str(spec.get("fps", 30)), "-i", f"{frames}/f_%05d.png",
                "-filter_complex", vf, "-map", "0:a", "-c:v", "libx264", "-crf", "16", "-preset", "medium", "-c:a", "aac", "-b:a", "192k", out], check=True)
print("wrote", out)
````


### `projekty/styl9/engine/overlay9.html`

````html
<!doctype html><html><head><meta charset="utf-8">
<!-- Style 9: LEGO AI ad (friend's "Walmart" reel). Montserrat Bold captions (1-3 words, hard cuts, ~64% height) plus the
     original's extra layer: red highlight box drawn around a UI element, money rain, money burst, bouncing yellow arrow. -->
<link rel="stylesheet" href="../../reklamy_CA/engine/assets/fonts/montserrat.css">
<style>
html,body{margin:0;background:transparent}
#stage{position:relative;width:1080px;height:1920px;overflow:hidden}
#cap{position:absolute;left:40px;right:40px;text-align:center;transform:translateY(-50%);font-family:'Montserrat',sans-serif;font-weight:700;
 font-size:70px;color:#fff;letter-spacing:-.01em;line-height:1.05;white-space:nowrap;
 -webkit-text-stroke:3px rgba(0,0,0,.95);paint-order:stroke fill;
 text-shadow:0 0 4px rgba(0,0,0,.9),0 3px 8px rgba(0,0,0,1),0 6px 30px rgba(0,0,0,.7)}  /* Konrad: cień +50-60% */
svg.fx{position:absolute;left:0;top:0;overflow:visible}
.p{position:absolute;will-change:transform}
</style></head><body><div id="stage"><div id="cap"></div></div>
<script>
let SPEC=null,last=-2;const $=id=>document.getElementById(id),NS='http://www.w3.org/2000/svg';
const cl=x=>Math.max(0,Math.min(1,x)),E=t=>1-Math.pow(1-t,3);
function rnd(seed){let s=seed>>>0||1;return()=>{s=(s*1664525+1013904223)>>>0;return s/4294967296}}
const B={};
// red rounded box drawn around a UI element (stroke animates on), optional rotation to follow a tilted phone
B.box=o=>{const s=document.createElementNS(NS,'svg');s.setAttribute('class','fx');s.setAttribute('width',1080);s.setAttribute('height',1920);
 const r=document.createElementNS(NS,'rect');Object.entries({x:o.x,y:o.y,width:o.w,height:o.h,rx:o.r||18,fill:'none',stroke:o.color||'#FF2B2B','stroke-width':o.sw||9,
  'stroke-linecap':'round',transform:`rotate(${o.rot||0} ${o.x+o.w/2} ${o.y+o.h/2})`}).forEach(([k,v])=>r.setAttribute(k,v));
 r.style.filter='drop-shadow(0 4px 10px rgba(0,0,0,.35))';s.appendChild(r);$('stage').appendChild(s);o.e=s;o.r=r;o.len=2*(o.w+o.h)};
B.box.u=(o,t)=>{const p=E(cl((t-o.t0)/(o.draw||.35)));o.r.setAttribute('stroke-dasharray',o.len);o.r.setAttribute('stroke-dashoffset',o.len*(1-p))};
// money rain: bills + coins fall from above the frame with spin and a touch of motion blur
B.rain=o=>{const R=rnd(o.seed||7),n=o.n||34;o.ps=[];for(let i=0;i<n;i++){const im=document.createElement('div');im.className='p';
 im.textContent=o.emo[i%o.emo.length];const sz=110+R()*90;Object.assign(im.style,{fontSize:sz+'px',lineHeight:1,fontFamily:'Noto Color Emoji'});$('stage').appendChild(im);
 o.ps.push({im,x:R()*1080,delay:R()*(o.spawn||1.2),v:900+R()*700,rot0:R()*360,vr:(R()-.5)*400,sway:20+R()*40,ph:R()*6,sz})}o.e=o.ps.map(p=>p.im)};
B.rain.u=(o,t)=>{const dt=t-o.t0;o.ps.forEach(p=>{const a=dt-p.delay;const y=-160+a*p.v;
 if(a<0||y>2000){p.im.style.display='none';return}p.im.style.display='block';
 p.im.style.transform=`translate(${p.x+Math.sin(a*3+p.ph)*p.sway-p.sz/2}px,${y}px) rotate(${p.rot0+a*p.vr}deg)`;p.im.style.filter=`blur(${Math.min(2.5,p.v/700)}px)`})};
// money burst: bills fly outward from a point, then fall
B.burst=o=>{const R=rnd(o.seed||3),n=o.n||26;o.ps=[];for(let i=0;i<n;i++){const im=document.createElement('div');im.className='p';im.textContent=o.emo[i%o.emo.length];
 const sz=110+R()*80;Object.assign(im.style,{fontSize:sz+'px',lineHeight:1,fontFamily:'Noto Color Emoji'});$('stage').appendChild(im);
 const ang=R()*Math.PI*2,sp=900+R()*1300;o.ps.push({im,vx:Math.cos(ang)*sp,vy:Math.sin(ang)*sp-600,rot0:R()*360,vr:(R()-.5)*700,sz})}o.e=o.ps.map(p=>p.im)};
B.burst.u=(o,t)=>{const a=t-o.t0;o.ps.forEach(p=>{const x=o.x+p.vx*a,y=o.y+p.vy*a+1400*a*a;
 if(a<0||y>2050){p.im.style.display='none';return}p.im.style.display='block';
 p.im.style.transform=`translate(${x-p.sz/2}px,${y-p.sz/2}px) rotate(${p.rot0+p.vr*a}deg) scale(${.4+.6*E(cl(a/.25))})`})};
// yellow 3D arrow pointing down, bouncing (CTA)
B.arrow=o=>{const d=document.createElement('div');d.className='p';
 d.innerHTML=`<svg width="${o.size||170}" height="${(o.size||170)*1.15}" viewBox="0 0 100 115"><defs><linearGradient id="ag" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#FFE45C"/><stop offset=".55" stop-color="#FFD21F"/><stop offset="1" stop-color="#E5A800"/></linearGradient></defs>
 <path d="M33 6h34v52h24L50 109 9 58h24z" fill="#B88400" transform="translate(4 5)"/><path d="M33 6h34v52h24L50 109 9 58h24z" fill="url(#ag)" stroke="#fff3" stroke-width="2"/></svg>`;
 d.style.filter='drop-shadow(0 8px 14px rgba(0,0,0,.45))';$('stage').appendChild(d);o.e=d};
B.arrow.u=(o,t)=>{const a=t-o.t0,s=o.size||170;const pop=E(cl(a/.25));const b=Math.abs(Math.sin(a*Math.PI*2.2))*26;
 o.e.style.transform=`translate(${o.x-s/2}px,${o.y-s*.575+b}px) scale(${.6+.4*pop})`;o.e.style.opacity=cl(a/.12)};
window.init=s=>{SPEC=s;s.fx.forEach(o=>B[o.type](o));return true};
window.seek=t=>{SPEC.fx.forEach(o=>{const on=t>=o.t0-1e-3&&t<o.t1;const els=Array.isArray(o.e)?o.e:[o.e];
  if(!on){els.forEach(e=>e.style.display='none');return}if(!Array.isArray(o.e))o.e.style.display='block';B[o.type].u(o,t)});
 const c=$('cap');const hid=(SPEC.hideCaps||[]).some(h=>t>=h[0]&&t<h[1]);const i=hid?-1:SPEC.caps.findIndex(b=>t>=b.t0-1e-3&&t<b.t1);
 if(i!==last){last=i;if(i<0)c.style.visibility='hidden';else{c.textContent=SPEC.caps[i].text;c.style.visibility='visible'}}
 c.style.top=(SPEC.capY*1920)+'px';return true};
</script></body></html>
````


### `review/video-review.html`

````html
<title>Video Review Studio</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter+Tight:wght@500;600;700&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@500&display=swap">
<style>
/* Layout: editor review desk — player left, notes rail right; stacks on phones. */
:root{
  --bg:#F3F6F4; --panel:#FFFFFF; --line:#DCE5E0; --fg:#0D2119; --muted:#5B7268;
  --accent:#0E4D3A; --accent-2:#1F7A5A; --accent-soft:#E2F0E9; --mark:#E0483A; --done:#7C8F86;
  --stage:#0A120F;
  --f-display:"Inter Tight",Inter,system-ui,sans-serif; --f-body:Inter,system-ui,sans-serif; --f-mono:"JetBrains Mono",ui-monospace,monospace;
}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){
  --bg:#0B1411; --panel:#111D18; --line:#22332B; --fg:#E6F0EB; --muted:#8FA59B;
  --accent:#4FC596; --accent-2:#79D8AE; --accent-soft:#16302A; --mark:#FF6B5C; --done:#5E7268; --stage:#050907; color-scheme:dark}}
:root[data-theme="dark"]{
  --bg:#0B1411; --panel:#111D18; --line:#22332B; --fg:#E6F0EB; --muted:#8FA59B;
  --accent:#4FC596; --accent-2:#79D8AE; --accent-soft:#16302A; --mark:#FF6B5C; --done:#5E7268; --stage:#050907; color-scheme:dark}
*{box-sizing:border-box}
html,body{background:var(--bg);color:var(--fg)}
body{font-family:var(--f-body);font-size:15px;line-height:1.45;padding-inline:16px;padding-block:20px 40px}
.wrap{max-width:1180px;margin:0 auto;display:flex;flex-direction:column;gap:16px}
header{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:12px}
h1{font-family:var(--f-display);font-weight:700;font-size:22px;letter-spacing:-.02em;margin:0}
.sub{color:var(--muted);font-size:13px}
.tabs{display:flex;gap:6px;overflow-x:auto;max-width:100%;padding-bottom:4px;scrollbar-width:thin}
.tab{flex:none;white-space:nowrap}
.tab .ok{color:var(--accent-2);margin-left:6px}
.tab{font:600 14px var(--f-display);border:1px solid var(--line);background:var(--panel);color:var(--fg);padding:8px 14px;border-radius:999px;cursor:pointer}
.tab[aria-selected="true"]{background:var(--accent);border-color:var(--accent);color:var(--bg)}
.tab .n{font-family:var(--f-mono);font-size:11px;margin-left:6px;opacity:.75}
.grid{display:grid;grid-template-columns:minmax(0,420px) minmax(0,1fr);gap:20px;align-items:start}
@media (max-width:820px){.grid{grid-template-columns:minmax(0,1fr)}}
.player{display:flex;flex-direction:column;gap:10px;min-width:0}
.stage{position:relative;background:var(--stage);border-radius:18px;overflow:hidden;aspect-ratio:9/16;max-width:100%;max-height:78vh;margin:0 auto;width:100%}
.stage video{position:absolute;inset:0;width:100%;height:100%;object-fit:contain;display:block}
.hit{position:absolute;inset:0;cursor:crosshair}
.dot{position:absolute;width:26px;height:26px;margin:-13px 0 0 -13px;border-radius:50%;border:3px solid #fff;background:var(--mark);box-shadow:0 2px 10px rgba(0,0,0,.5);pointer-events:none;
  display:flex;align-items:center;justify-content:center;font:700 11px var(--f-mono);color:#fff}
.dot.pending{animation:pulse 1s infinite}
@keyframes pulse{50%{transform:scale(1.25)}}
@media (prefers-reduced-motion:reduce){.dot.pending{animation:none}}
.empty-stage{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;color:#9fb3aa;text-align:center;padding:24px;font-size:14px}
.controls{display:flex;align-items:center;gap:10px}
.btn{font:600 14px var(--f-display);border:1px solid var(--line);background:var(--panel);color:var(--fg);border-radius:10px;padding:8px 12px;cursor:pointer;display:inline-flex;align-items:center;gap:6px}
.btn.primary{background:var(--accent);border-color:var(--accent);color:var(--bg)}
.btn:disabled{opacity:.45;cursor:default}
.btn:focus-visible,.tab:focus-visible,textarea:focus-visible,.note:focus-visible{outline:2px solid var(--accent-2);outline-offset:2px}
.time{font:500 13px var(--f-mono);color:var(--muted);font-variant-numeric:tabular-nums;min-width:96px}
.bar{position:relative;height:30px;flex:1;cursor:pointer;touch-action:none}
.bar .track{position:absolute;left:0;right:0;top:13px;height:4px;border-radius:4px;background:var(--line)}
.bar .fill{position:absolute;left:0;top:13px;height:4px;border-radius:4px;background:var(--accent)}
.bar .mk{position:absolute;top:6px;width:4px;height:18px;margin-left:-2px;border-radius:2px;background:var(--mark)}
.bar .mk.done{background:var(--done)}
.compose{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:12px;display:flex;flex-direction:column;gap:8px}
.compose .hint{font-size:13px;color:var(--muted)}
.compose .hint b{color:var(--fg);font-family:var(--f-mono);font-weight:500}
textarea{width:100%;min-height:72px;resize:vertical;font:inherit;color:var(--fg);background:var(--bg);border:1px solid var(--line);border-radius:10px;padding:10px}
.row{display:flex;gap:8px;flex-wrap:wrap;align-items:center}
.notes{background:var(--panel);border:1px solid var(--line);border-radius:18px;padding:16px;display:flex;flex-direction:column;gap:12px;min-width:0}
.notes h2{font:700 16px var(--f-display);margin:0;display:flex;justify-content:space-between;align-items:baseline;gap:8px}
.notes h2 span{font:500 12px var(--f-mono);color:var(--muted)}
.list{display:flex;flex-direction:column;gap:8px}
.note{display:grid;grid-template-columns:auto minmax(0,1fr);gap:4px 12px;padding:10px 12px;border-radius:12px;border:1px solid var(--line);background:var(--bg);cursor:pointer}
.note.active{border-color:var(--accent-2)}
.note .tc{font:500 13px var(--f-mono);color:var(--accent);font-variant-numeric:tabular-nums;padding-top:1px}
.note .txt{white-space:pre-wrap;overflow-wrap:anywhere}
.note .meta{grid-column:2;display:flex;flex-wrap:wrap;gap:8px;align-items:center;font-size:12px;color:var(--muted)}
.chip{font:600 11px var(--f-display);letter-spacing:.04em;text-transform:uppercase;border-radius:999px;padding:2px 8px;background:var(--accent-soft);color:var(--accent)}
.chip.open{background:color-mix(in srgb,var(--mark) 14%,transparent);color:var(--mark)}
.reply{grid-column:2;border-left:3px solid var(--accent-2);padding:4px 0 4px 10px;font-size:14px;color:var(--fg)}
.reply small{display:block;color:var(--muted);font-size:11px;text-transform:uppercase;letter-spacing:.05em;font-weight:600}
.note.done .txt{color:var(--muted);text-decoration:line-through}
.link{background:none;border:0;color:var(--muted);font:inherit;font-size:12px;cursor:pointer;padding:0;text-decoration:underline}
.blank{color:var(--muted);font-size:14px;padding:12px 4px}
.status{font-size:13px;color:var(--muted);min-height:18px}
.tools{display:flex;flex-wrap:wrap;gap:6px;align-items:center}
.seg{display:inline-flex;border:1px solid var(--line);border-radius:10px;overflow:hidden}
.seg button{font:600 13px var(--f-mono);background:var(--panel);color:var(--fg);border:0;padding:7px 10px;cursor:pointer}
.seg button+button{border-left:1px solid var(--line)}
.seg button.on{background:var(--accent);color:var(--bg)}
select.ver{font:600 13px var(--f-display);border:1px solid var(--line);background:var(--panel);color:var(--fg);border-radius:10px;padding:7px 10px}
.approve{display:flex;flex-wrap:wrap;gap:8px;align-items:center;background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:10px 12px}
.approve .st{font-size:13px;color:var(--muted);flex:1;min-width:160px}
.approve .st b{color:var(--accent)}
</style>

<div class="wrap">
  <header>
    <div>
      <h1>Video Review Studio</h1>
      <div class="sub">Zatrzymaj w miejscu, kliknij w kadr i wpisz uwagę. Claude czyta uwagi razem z czasem i odpisuje pod każdą.</div>
    </div>
    <div class="tabs" id="tabs" role="tablist" aria-label="Filmy"></div>
  </header>

  <div class="grid">
    <section class="player">
      <div class="stage" id="stage">
        <video id="vid" playsinline preload="metadata"></video>
        <div class="hit" id="hit" aria-label="Kliknij w kadr, żeby zaznaczyć miejsce uwagi"></div>
        <div class="empty-stage" id="emptyStage">Tu pojawi się film do przeglądu, gdy Claude go wgra.</div>
      </div>
      <div class="controls">
        <button class="btn" id="play" aria-label="Odtwórz">▶</button>
        <div class="bar" id="bar"><div class="track"></div><div class="fill" id="fill"></div><div id="marks"></div></div>
        <span class="time" id="time">0:00.0 / 0:00</span>
      </div>
      <div class="tools">
        <div class="seg" id="speed" aria-label="Prędkość"><button data-r="0.5">0.5×</button><button data-r="1" class="on">1×</button><button data-r="1.5">1.5×</button><button data-r="2">2×</button></div>
        <div class="seg"><button id="fb" aria-label="Klatka wstecz">◀ klatka</button><button id="ff" aria-label="Klatka dalej">klatka ▶</button></div>
        <select class="ver" id="ver" aria-label="Wersja filmu"></select>
      </div>
      <div class="approve">
        <div class="st" id="apSt">Ta wersja czeka na Twoją decyzję.</div>
        <button class="btn" id="send">Wyślij poprawki</button>
        <button class="btn primary" id="approveBtn">Zatwierdź wersję</button>
      </div>
      <div class="compose">
        <div class="hint" id="hint">Uwaga przy <b id="atTime">0:00.0</b>. Kliknięcie w kadr dodaje kropkę (opcjonalnie).</div>
        <textarea id="txt" placeholder="Np. animacja za krótka, przytrzymaj ją do końca zdania"></textarea>
        <div class="row">
          <button class="btn primary" id="save">Zapisz uwagę</button>
          <button class="btn" id="clearDot">Usuń kropkę</button>
          <span class="status" id="status"></span>
        </div>
      </div>
    </section>

    <section class="notes">
      <h2>Uwagi <span id="count">0 otwartych</span></h2>
      <div class="list" id="list"><div class="blank">Brak uwag do tego filmu. Pierwsza pojawi się tutaj po kliknięciu „Zapisz uwagę”.</div></div>
    </section>
  </div>
</div>

<script>
const $=id=>document.getElementById(id);
const vid=$('vid'), hit=$('hit'), stage=$('stage');
let db=null, me=null, users=null;
let videos=[], cur=null, notes=[], pending=null, activeId=null, unsubNotes=null, approvals={}, viewVer=null;
const fmt=t=>{t=Math.max(0,t||0);const m=Math.floor(t/60),s=t-m*60;return m+':'+(s<10?'0':'')+s.toFixed(1)};
const fmtShort=t=>{t=Math.max(0,t||0);const m=Math.floor(t/60),s=Math.floor(t-m*60);return m+':'+(s<10?'0':'')+s};

function renderTabs(){
  const tabs=$('tabs');tabs.innerHTML='';
  videos.forEach(v=>{const b=document.createElement('button');b.className='tab';b.setAttribute('role','tab');
    b.setAttribute('aria-selected',cur&&cur.id===v.id?'true':'false');b.textContent=v.title||v.id;
    if(v.ver){const n=document.createElement('span');n.className='n';n.textContent='v'+v.ver;b.appendChild(n)}
    const ap=approvals[v.id];if(ap&&ap.ver===v.ver){const k=document.createElement('span');k.className='ok';k.textContent='✓';k.title='Zatwierdzone';b.appendChild(k)}
    b.onclick=()=>select(v.id);tabs.appendChild(b)});
}
function select(id){
  cur=videos.find(v=>v.id===id)||null; renderTabs(); pending=null; activeId=null;
  $('emptyStage').hidden=!!cur;
  viewVer=null;loadSrc();renderVer();renderApprove();
  try{localStorage.setItem('vr-cur',id)}catch(e){}
  if(unsubNotes){unsubNotes();unsubNotes=null}
  notes=[];renderNotes();
  if(db&&cur){unsubNotes=db.collection('notes').where('video','==',cur.id).onSnapshot(s=>{
    notes=s.docs.map(d=>({id:d.id,...d.data()})).sort((a,b)=>a.t-b.t);renderNotes()},e=>status('Nie udało się wczytać uwag: '+e.message))}
}
function versionsOf(v){const list=(v.versions||[]).slice();if(!list.some(x=>x.ver===v.ver))list.push({ver:v.ver||1,url:v.url||('/_blob/'+v.asset)});return list.sort((a,b)=>b.ver-a.ver)}
function loadSrc(){if(!cur)return;const vs=versionsOf(cur);const pick=vs.find(x=>x.ver===viewVer)||vs[0];const src=pick.url;
  if(vid.getAttribute('src')!==src){const t=vid.currentTime;vid.src=src;vid.load();if(viewVer!=null)vid.addEventListener('loadedmetadata',()=>{vid.currentTime=t},{once:true});vid.playbackRate=rate}}
function renderVer(){const s=$('ver');s.innerHTML='';if(!cur)return;versionsOf(cur).forEach((x,i)=>{const o=document.createElement('option');o.value=x.ver;
  o.textContent='Wersja '+x.ver+(i===0?' (najnowsza)':'');if((viewVer??versionsOf(cur)[0].ver)===x.ver)o.selected=true;s.appendChild(o)});s.hidden=versionsOf(cur).length<2}
function renderApprove(){if(!cur)return;const ap=approvals[cur.id];const st=$('apSt');
  if(ap&&ap.ver===cur.ver){st.innerHTML='<b>Zatwierdzone</b> (wersja '+ap.ver+'). Claude robi z tej wersji FINAL.';$('approveBtn').textContent='Cofnij zatwierdzenie'}
  else{st.textContent=ap&&ap.sent===cur.ver?'Poprawki wysłane. Claude pracuje nad wersją '+(cur.ver+1)+'.':'Ta wersja czeka na Twoją decyzję.';$('approveBtn').textContent='Zatwierdź wersję'}}
function renderMarks(){
  const d=vid.duration||cur?.dur||0;const m=$('marks');m.innerHTML='';if(!d)return;
  notes.forEach(n=>{const k=document.createElement('div');k.className='mk'+(n.status==='done'?' done':'');k.style.left=(n.t/d*100)+'%';m.appendChild(k)});
}
function renderDots(){
  stage.querySelectorAll('.dot').forEach(e=>e.remove());
  const t=vid.currentTime;
  notes.forEach((n,i)=>{if(n.x==null)return;if(Math.abs(n.t-t)<0.6||n.id===activeId){const d=document.createElement('div');d.className='dot';d.style.left=(n.x*100)+'%';d.style.top=(n.y*100)+'%';d.textContent=i+1;stage.appendChild(d)}});
  if(pending&&pending.x!=null){const d=document.createElement('div');d.className='dot pending';d.style.left=(pending.x*100)+'%';d.style.top=(pending.y*100)+'%';stage.appendChild(d)}
}
async function renderNotes(){
  const list=$('list');list.innerHTML='';
  const open=notes.filter(n=>n.status!=='done').length;$('count').textContent=open+(open===1?' otwarta':' otwartych');
  if(!notes.length){list.innerHTML='<div class="blank">Brak uwag do tego filmu. Pierwsza pojawi się tutaj po kliknięciu „Zapisz uwagę”.</div>';renderMarks();renderDots();return}
  let profiles={};try{if(users){const ids=[...new Set(notes.map(n=>n.author).filter(Boolean))];profiles=await users.profiles(ids)}}catch(e){}
  notes.forEach((n,i)=>{
    const el=document.createElement('div');el.className='note'+(n.status==='done'?' done':'')+(n.id===activeId?' active':'');el.tabIndex=0;
    const tc=document.createElement('div');tc.className='tc';tc.textContent=(i+1)+'. '+fmt(n.t);
    const tx=document.createElement('div');tx.className='txt';tx.textContent=n.text||'';
    const meta=document.createElement('div');meta.className='meta';
    const chip=document.createElement('span');chip.className='chip '+(n.status==='done'?'':'open');chip.textContent=n.status==='done'?'poprawione':'do poprawy';meta.appendChild(chip);
    const who=document.createElement('span');who.textContent=(profiles[n.author]&&profiles[n.author].name)||'';if(who.textContent)meta.appendChild(who);
    if(n.version){const v=document.createElement('span');v.textContent='wersja '+n.version;meta.appendChild(v)}
    const tg=document.createElement('button');tg.className='link';tg.textContent=n.status==='done'?'Otwórz ponownie':'Oznacz jako poprawione';
    tg.onclick=async ev=>{ev.stopPropagation();try{await db.collection('notes').doc(n.id).update({status:n.status==='done'?'open':'done'})}catch(e){status('Nie zapisano: '+e.message)}};meta.appendChild(tg);
    const del=document.createElement('button');del.className='link';del.textContent='Usuń';
    del.onclick=async ev=>{ev.stopPropagation();if(del.dataset.sure){try{await db.collection('notes').doc(n.id).delete()}catch(e){status('Nie usunięto: '+e.message)}}else{del.dataset.sure=1;del.textContent='Na pewno usunąć?'}};meta.appendChild(del);
    el.append(tc,tx,meta);
    if(n.reply){const r=document.createElement('div');r.className='reply';r.innerHTML='<small>Claude</small>';r.appendChild(document.createTextNode(n.reply));el.appendChild(r)}
    const go=()=>{activeId=n.id;vid.pause();vid.currentTime=n.t;renderNotes()};
    el.onclick=go;el.onkeydown=e=>{if(e.key==='Enter')go()};
    list.appendChild(el)});
  renderMarks();renderDots();
}
function status(s){$('status').textContent=s}
function tick(){const d=vid.duration||0;$('time').textContent=fmt(vid.currentTime)+' / '+fmtShort(d);$('fill').style.width=(d?vid.currentTime/d*100:0)+'%';
  $('atTime').textContent=fmt(pending?pending.t:vid.currentTime);$('play').textContent=vid.paused?'▶':'❚❚';$('play').setAttribute('aria-label',vid.paused?'Odtwórz':'Pauza');renderDots()}
vid.addEventListener('timeupdate',tick);vid.addEventListener('play',tick);vid.addEventListener('pause',tick);vid.addEventListener('loadedmetadata',()=>{tick();renderMarks()});
(function loop(){if(!vid.paused)tick();requestAnimationFrame(loop)})();
$('play').onclick=()=>{vid.paused?vid.play():vid.pause()};
document.addEventListener('keydown',e=>{if(e.target.tagName==='TEXTAREA')return;if(e.code==='Space'){e.preventDefault();vid.paused?vid.play():vid.pause()}
  if(e.key==='ArrowLeft'){vid.currentTime=Math.max(0,vid.currentTime-(e.shiftKey?1:1/30))}if(e.key==='ArrowRight'){vid.currentTime+=e.shiftKey?1:1/30}});
const seekFrom=e=>{const r=$('bar').getBoundingClientRect();const p=Math.min(1,Math.max(0,(e.clientX-r.left)/r.width));if(vid.duration)vid.currentTime=p*vid.duration};
$('bar').addEventListener('pointerdown',e=>{seekFrom(e);$('bar').setPointerCapture(e.pointerId)});
$('bar').addEventListener('pointermove',e=>{if(e.buttons)seekFrom(e)});
function videoBox(){const r=stage.getBoundingClientRect();const vw=vid.videoWidth||9,vh=vid.videoHeight||16;const s=Math.min(r.width/vw,r.height/vh);const w=vw*s,h=vh*s;return {r,x:(r.width-w)/2,y:(r.height-h)/2,w,h}}
hit.addEventListener('click',e=>{if(!cur)return;vid.pause();const b=videoBox();const x=(e.clientX-b.r.left-b.x)/b.w,y=(e.clientY-b.r.top-b.y)/b.h;
  if(x<0||x>1||y<0||y>1)return;pending={t:vid.currentTime,x:+x.toFixed(4),y:+y.toFixed(4)};tick();$('txt').focus()});
$('clearDot').onclick=()=>{pending=null;tick()};
let rate=1;$('speed').querySelectorAll('button').forEach(b=>b.onclick=()=>{rate=+b.dataset.r;vid.playbackRate=rate;$('speed').querySelectorAll('button').forEach(x=>x.classList.toggle('on',x===b))});
$('fb').onclick=()=>{vid.pause();vid.currentTime=Math.max(0,vid.currentTime-1/30)};$('ff').onclick=()=>{vid.pause();vid.currentTime=vid.currentTime+1/30};
$('ver').onchange=()=>{viewVer=+$('ver').value;loadSrc()};
$('approveBtn').onclick=async()=>{if(!db||!cur)return;const ap=approvals[cur.id]||{};const on=!(ap.ver===cur.ver);
  try{await db.collection('approvals').doc(cur.id).set({...ap,ver:on?cur.ver:null,at:new Date().toISOString(),by:me||null});status(on?'Zatwierdzono wersję '+cur.ver+'.':'Cofnięto zatwierdzenie.')}catch(e){status('Nie zapisano: '+(e.message||e.code))}};
$('send').onclick=async()=>{if(!db||!cur)return;const open=notes.filter(n=>n.status!=='done').length;if(!open){status('Brak otwartych uwag do wysłania.');return}
  try{await db.collection('approvals').doc(cur.id).set({...(approvals[cur.id]||{}),sent:cur.ver,sentAt:new Date().toISOString(),openNotes:open});status('Wysłano '+open+' uwag. Napisz Claude’owi „poprawki z review”.')}catch(e){status('Nie zapisano: '+(e.message||e.code))}};
$('save').onclick=async()=>{const text=$('txt').value.trim();if(!text){status('Wpisz treść uwagi.');return}
  if(!db){status('Zapis niedostępny w tym widoku. Zaloguj się w claude.ai.');return}if(!cur)return;
  const n={video:cur.id,t:+(pending?pending.t:vid.currentTime).toFixed(2),x:pending?pending.x:null,y:pending?pending.y:null,text,status:'open',version:cur.ver||1,created:new Date().toISOString(),author:me||null};
  $('save').disabled=true;status('Zapisuję…');
  try{await db.collection('notes').add(n);$('txt').value='';pending=null;status('Zapisano przy '+fmt(n.t)+'.');tick()}catch(e){status('Nie zapisano: '+(e.message||e.code))}
  $('save').disabled=false};

(async()=>{
  db=await claude.use('db');
  if(!db){$('emptyStage').textContent='Zaloguj się w claude.ai, żeby zobaczyć filmy i dodawać uwagi.';return}
  try{users=await claude.use('user');if(users){me=await users.id()}}catch(e){}
  db.collection('videos').onSnapshot(s=>{
    videos=s.docs.map(d=>({id:d.id,...d.data()})).sort((a,b)=>(a.order||0)-(b.order||0));
    let want=null;try{want=localStorage.getItem('vr-cur')}catch(e){}
    const keep=cur&&videos.find(v=>v.id===cur.id);
    if(keep){const newer=keep.ver!==cur.ver;cur=keep;if(newer)viewVer=null;loadSrc();renderVer();renderApprove();renderTabs()}
    else if(videos.length)select((videos.find(v=>v.id===want)||videos[0]).id);
    else renderTabs();
  },e=>status('Nie udało się wczytać filmów: '+e.message));
  db.collection('approvals').onSnapshot(s=>{approvals={};s.docs.forEach(d=>approvals[d.id]=d.data());renderTabs();renderApprove()},()=>{});
})();
</script>
````
