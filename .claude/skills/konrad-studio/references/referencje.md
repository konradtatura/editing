# Referencje: czego się nauczyliśmy i jak studiować nowe

## Jak analizować referencję, którą przysyła Konrad

1. `ffprobe` (wymiary, fps, długość).
2. **Sprawdź, czy to nie showreel 2×2.** Oba filmy z 2026-10-03 miały w każdej klatce 4 różne klipy naraz.
   - Najpierw zrób jedną pełną klatkę.
   - Jeśli to siatka, tnij na ćwiartki:
     `ffmpeg -i ref.mp4 -vf "crop=960:540:X:Y,fps=3,scale=320:-1,tile=6x6" -frames:v 1 q.jpg` dla X,Y ∈ {0, 960} × {0, 540}.
3. Arkusze 2–3 fps i **przeczytaj każdy**. Wypisz:
   - układ (gdzie twarz, gdzie grafika),
   - słownik scen (co się powtarza),
   - rytm (co ile s zmiana),
   - typografię, paletę, ruch kamery, przejścia, napisy.
4. Zapisz wnioski tutaj (sekcja niżej). **Nie kopiuj treści referencji**, bierz techniki i dopasuj je do stylu Konrada.

## Filmy przysłane 2026-10-03 (`kVCRbRhIauDwAXzJ.mp4`, `497EcrVyUQ7wk7Pj.mp4`)

Konrad: „naprawdę bardzo fajnie zmontowane… szczególnie te b-rolle, te animacje”. Oba to montaż „pół z AI”.

**Film A (rejestrator domen, granat + fiolet):**
- Okno przeglądarki: wpisuje się domena, pojawia się wynik „Available”, przycisk BUY.
- Kafel z ikoną (globus „Registrar”), z którego **wyrastają łuki** do etykiet Register, Renew, Ownership, jedna po drugiej na słowach.
- Nagłówek pisany słowo po słowie: słowa wchodzą z szarego do czarnego, jedno słowo w kolorze akcentu.
  Pod spodem przeglądarka w perspektywie 3D.
- **Wielkie rozmyte kształty 3D** (granatowe wstęgi, „swoosh”) w rogu kadru dają głębię ostrości.
- Pytanie z chipem „Priority” + okno marki (Cloudflare, Porkbun) wjeżdża z prawej, a w nim lista z kropkami odhaczana na słowach.
- Ciemne sceny: grafit z fioletową poświatą u góry, szklane karty cen $0 vs $30, pasek Google rozwija się i pisze.
- Logo (WIX) na rozmytym tle, przetarte kolorem. Prawdziwy screen strony przewija się w ramce.
- Na twarzy: linia wykresu z kropkami u dołu kadru + szklana etykieta. Podpis-tytuł w pigułce pisany na żywo, słowa kluczowe na fioletowo.
- Split: ciemny panel z listą świecących punktów po lewej, twarz po prawej.
- „4 things I'm looking at”: karty z numerem i ikoną 3D lądują przechylone na grubej granatowej wstędze.

**Film B (cold outreach, biel + barwinek #6E8BF5):**
- Tekst **na nagraniu obok głowy** (bez karty): lista „> B2B technology / > Software / > Infrastructure space” wpisywana po lewej.
  Tytuł „Cold Outreach / In 2026” rozbity po obu stronach głowy + niebieski łuk rysowany przez kadr.
- **Mieszanie fontów:** bezszeryfowy + **kursywa szeryfowa** na jednym słowie („Belief Change”, „a month”).
  Podwójny napis: wielka różowa kursywa pod białym bezszeryfowym („Rather than actually trying to / set them to a call”).
- **Kolaż:** rycina głowy z niebieskim mózgiem + łuk + kursywa. Zdjęcie wycięte (aktor) + łuki do niebieskich pigułek „Knowing / Getting closer”.
- Prawdziwe screeny (Google, Wikipedia, Reddit, słownik) z **ruchem kamery i rozmyciem ruchu**, częściowo rozmyte w głąb.
- Oś czasu z numerowanymi kołami (cyfry kursywą), przesuwa się poziomo, etykiety rozmyte poza ostrością.
- Arkusze kalkulacyjne w 3D, przechylone i ułożone w stos. Łuk prowadzi do „Send 30,000 contacts / a month”.
- Przejście: dym, rozpad na cząsteczki między twarzą a b-rollem (rzadko).

**Co z tego przejmujemy do stylu Konrada** (zapisane w `styl-apple.md` § Warstwa premium):
- łuki rysowane na słowach (`curve()`) zamiast prostych linii,
- głębia, czyli rozmyte kształty na pierwszym planie i delikatny najazd kamery (`push_in()`, `motion_blur()`),
- kursywa szeryfowa na JEDNYM słowie (`family="Studio Serif"`),
- prawdziwa strona + najazd + zakreślacz (`highlight()`),
- tekst na ścianie obok głowy, bez karty, w longformie 16:9,
- pisany tytuł-pigułka z kolorowym słowem jako otwarcie rozdziału,
- karty 3D „lądujące” z lekkim przechyleniem, prawdziwe ikony (`fetch_icon.py`), liczniki-klapki (`flap_keys()`).

**Tylko na prośbę:** split ekranu z panelem obok twarzy (Konrad odrzucił split w reklamach i VSL), dym i cząsteczki, ciemny motyw.

## Skille znajomego (6 szt., `drive-download-20261003…`), traktowane jak swipe file

| Skill | Co to | Co przejęliśmy |
|---|---|---|
| famous-youtube-editor | longform 16:9 (HTML/GSAP + Higgsfield) | gramatyka ujęć A–D, „coś nowego co ~5 s”, nie > 10 s w jednym trybie, punch-iny 100/115% na granicach zdań, martwa strefa pod PiP, karty jako okna aplikacji (nie goły tekst) |
| famous-reel-editor | reel 9:16 (pas czarny + karaoke) | tabela błędów: obcięte końcówki słów, ukryte powtórki w długich „słowach”, cache starych transkrypcji, dryf A/V przy łączeniu AAC, liczenie >1,2 s albo pop, kluczowy element wcześnie w zdaniu, „przed” widoczne od klatki 0 |
| albert-reel(-white/-white-screen) | warianty powyższego | zoom „punch-in” na nagraniach ekranu (0,5 s pełny widok → szybki najazd na to, co trzeba przeczytać), tekst czytany od lewej = fx 0 |
| albert-reel-dark | Apple UI, Pillow, bramki QA | bramki: brak ruchu > 0,6 s, brak pustej pierwszej klatki, pauzy z audio, TP < −1 dB; zero etykiet-pieczątek powtarzających słowo; bez szarych podtytułów; prawdziwe ikony zamiast rysowanych ludzi; obrys kraju z GeoJSON; licznik-klapki; memy 1–3 na „linie emocji”; wejście 0,1 s przed słowem; fact-check przed rysowaniem; retro po każdym projekcie |

**Nie przejmujemy:**
- ich silników (HTML/hyperframes, Pillow): zostajemy przy Tesseract,
- czarnego pasa i karaoke jednym słowem,
- zielono-pomarańczowych akcentów,
- pistoletów, kapelusza Claude'a i innych gagów pod tamtego twórcę,
- muzyki z ich assetów,
- **ich kluczy API** (pliki `.env` w paczce należą do znajomego i nie używamy ich).

## nathanazareth (2026-10-05): kinetyczna rolka/reklama 16:9, 69 s

Film znajomego Konrada, który odwzorowujemy za zgodą. Pełny breakdown cięcie po cięciu: `~/Documents/KonradStudio_Archiwum/referencje/REF_nathan/BREAKDOWN.md`.

**Formuła:** napisy słowo po słowie przez cały film (jedno wielkie słowo-bohater + drobne słowa nad i pod nim) i ujęcie średnio co 1,2 s.

**Proporcje:**
- twarz ok. 32%,
- kolorowe b-rolle „ja” ok. 44%,
- czarno-białe b-rolle „oni” ok. 9%,
- plansze ok. 14%: radialny gradient biel→jasnoniebieski z niebieskim tekstem ↔ nasycony niebieski z białym ↔ czarna.

**Efekty co 5–8 s:**
- otwarcie pasami kinowymi 2.39:1,
- ściana feedu w 3D,
- gigantyczna nazwa miasta półprzezroczyście nad nagraniem z drona,
- kolaż zdjęć z lat,
- siatka 2×2 budowana migotaniem i negatywem,
- czarny ekran „thinking”,
- sceptyk na tle ściany „guru”,
- akcja w ujęciu zgrana ze słowem (laptop zamyka się na „shut down”),
- tekst 3D na blacie,
- zamazanie słów białymi prostokątami przed słowem CTA.

**Muzyka:** przez cały film, basowa, ok. 4–5 dB pod głosem w pauzach. Uderzenia basu na zmianach sekcji.

**Uwaga:** to format reklamy/rolki, więc zasada 50/40/10 z longformu tu nie obowiązuje. Jest też wyjątkiem od zasady „mało tekstu”,
bo Konrad sam chce ten styl.

**Wykonanie (2026-10-05, „16–26”):** cały styl jest zrobiony jednym rendererem Python (PIL + numpy → ffmpeg), bez Tesseract:
`examples/kinetic_16x9_nathan_style.py`. Elementy i ich implementacja:
- **Napisy:** klasa Phrase (pre / hero / post) z odsłanianiem po czasie słowa ze Scribe, licznikiem-klapkami, przekreśleniem, zamazaniem i cytatem.
- **Ujęcia:** klipy z pionu przycinane do pasa 16:9 (parametr `band`), najazd przez `scale eval=frame` (crop nie zmienia w/h w czasie), gradacja bw / cine.
- **Sceny specjalne:** ściana feedu (perspektywa PIL), kolaż polaroidów, siatka 2×2 z negatywem, gigantyczny napis w trybie „screen”, ściana „guru” z wygenerowanych miniatur bez twarzy, tekst na blacie (perspektywa), pasy kinowe na otwarciu.
- **Font:** Helvetica Neue z systemu (index 1 Bold, 10 Medium).
- **Podgląd:** `--frames t1,t2,…` robi arkusz kontrolny bez renderu całości.
- **Animacja napisów (poprawka po uwadze Konrada):** nie „twarde wejście”, tylko wjazd od dołu ze smugą (`smear()`), skalą bohatera, dryfem bloku i wyjściem w górę. Cień: blur 22 × 0,85 plus ciasny blur 3 przesunięty o 4 px.

## „Premium” vs „tanio” (2026-10-09, 7 klipów w `~/Documents/KonradStudio_Archiwum/referencje/REF_premium/`, analiza w `ANALIZA.md`)

Konrad o animacjach w lfpdo (biały Apple style, Tesseract): „wyglądają tanio”. Wzorce premium:
- paleta marki z ciemnym tłem i poświatą;
- elementy 2–3× większe, jeden bohater na kadr;
- prawdziwe screeny i zdjęcia zamiast szarych pasków i emoji-clipartu;
- kamera zawsze w ruchu, sprężyny, przejścia przez rozmycie lub zoom, sceny przechodzą w siebie;
- mikro-interakcje (kursor, klik, licznik, skan).

**Zakaz:** drobne szare etykiety i placeholdery.
**Silnik do premium:** HyperFrames (HTML/GSAP, Chrome). Działa na tym Macu (`npx hyperframes` 0.8.143).

**Ale bez „AI slop” (2026-10-09, druga runda):** wersja ze szkłem, poświatą, kursywą szeryfową (Studio Serif), etykietami
w Geist Mono, polem gwiazd i pochyleniem 3D dostała „nie jest źle, ale wygląda jak AI slop”. Obowiązuje styl **Premium v3**:
- **jeden krój: Inter**, hierarchia tylko grubością i wielkością (Light 300 ↔ Bold/Black 800–900), domyślnie Inter Bold;
- **zakazane:** szeryf/kursywa, mono, WERSALIKI z rozstrzeleniem, poświata i text-shadow, glassmorphism, gradienty i plamy
  światła, cząsteczki/gwiazdy, pochylenie 3D, udawane okna z trzema kropkami, ogromne blade liczby w tle, emoji;
- płaska paleta A (granat #070b15, jeden akcent #3d7bff, czerwień tylko na stratę), jeden promień rogów (28 / pill);
- wejścia: słowa wysuwają się z maski od dołu; akcent = zamiana tego samego słowa z Light na Black;
- uczciwa wizualizacja danych (paski, siatki kropek, listy płatności, liczniki) zamiast dekoracji;
- karty obok twarzy: ciemna płaska karta na lewej ścianie, render MOV z alfą (ProRes 4444).
Gotowy zestaw: `templates/hyperframes_premium_v3/` (w tym skillu; kopia z LFPDO/premium/v3) (base.css, kit.js, page.py, build_cards.py, build_full.py,
chk.sh/sheet.sh/hi.sh), składanie: dziś `scripts/assemble.py` (dawny `LFPDO/final_v3.py` w `~/Documents/KonradStudio_Archiwum/projekty/LFPDO/`). Liczniki i rysowanie canvasu idą przez `K.count`/`K.frame`
(liczone z czasu playheadu, bezpieczne przy renderze wieloma workerami).
