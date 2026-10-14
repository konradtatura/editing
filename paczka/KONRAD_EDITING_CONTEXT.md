# Konrad: kontekst montażu reklam i rolek (dla Claude Code)

Wrzuć ten plik do projektu jako `CLAUDE.md` albo dołącz go jako kontekst. Zawiera cały warsztat z sesji 2026-10-12/14: proces, zasady Konrada, 8 stylów, komendy, błędy i audio. Kod silników leży w folderze `projekty/` w repo `konradtatura/editing` (albo w `silniki/` w `paczka/reklamy-studio.zip`). Odwołania do `references/*.md` poniżej to sekcje tego samego pliku.

## Reklamy Studio: montaż płatnych reklam w stylu z referencji

Zapis warsztatu z sesji 2026-10-12/13 (reklamy ad8, ad9, ads7, ads10, ads5, ads2, ad11 dla Cyfrowego Autopilota).
**Jak pracujemy:** Konrad wysyła film-wzór („taki styl”) i swoje surowe reklamy. Ja rozkładam wzór na czynniki,
buduję silnik stylu, montuję, sam sprawdzam każdą klatkę, wrzucam do Review, a on zostawia notatki z czasem.
Każda reklama ma inny kąt (angle) i trochę inny montaż.

Konrad jest marketerem, nie montażystą. Piszę po polsku, krótko, bez kodeków i fps. Pytam tylko o treść i gust.
Często jest na telefonie, więc wysyłam gotowe pliki (SendUserFile), a nie ścieżki.

### Najpierw przeczytaj
1. `references/zasady-konrada.md`: jego twarde wymagania i każdy feedback, który już dał. **Złamanie którejś = poprawka.**
2. `references/style-katalog.md`: 4 gotowe style (kolory, fonty, rozmiary, ruch, który adsy w jakim stylu).
3. `references/pipeline.md`: komendy krok po kroku (transkrypcja, cięcia, spec, render, kompozycja, QA, eksport, Review).
4. `references/bledy-i-lekcje.md`: błędy, które już raz wyszły. Sprawdź przed oddaniem.
5. `references/nowy-styl.md`: jak odtworzyć nowy styl z filmu-wzoru.
6. `references/audio.md`: muzyka i SFX (licencje, miks, ducking, -14 LUFS).

Kod silników leży w repo w `projekty/` (styl 1: `reklamy_CA/`, styl 2: `styl2/`, styl 3: `styl3/`, styl 4: `styl4/`, audio: `audio/`).
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

---

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

---

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

### Wybór stylu do nowej reklamy
Konrad zwykle mówi, który styl. Jeśli nie: gadająca głowa + framework/kroki → styl 3; gadająca głowa, ciepło, b-rolle → styl 2;
prosty format z planszami → styl 1; animacja/lektor bez twarzy → styl 4. Nowy wzór = nowy styl (`nowy-styl.md`).

---

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

---

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

---

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

---

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
