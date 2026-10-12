# Błędy, których nie powtarzamy

Każdy wiersz kosztował kiedyś poprawkę. Przeczytaj przed budową. Po projekcie dopisz nowe.

| Błąd | Zasada |
|---|---|
| Pusta biel na starcie sceny (ANGLE 4: A04 ~1 s pustki, A08 pusta 1. klatka; VSL S07/S08/S31) | Treść jest od klatki 0. `check.py motion` zgłasza `BLANK FIRST FRAME`. Przesuń in-point albo daj element, który już się rusza. |
| Mała etykieta nad treścią („Jedno pytanie”, chip „Priority”) | Etykieta, która tylko nazywa scenę, to bezużyteczny tekst. Wylatuje. |
| Pieczątka lub plakietka powtarzająca wypowiedziane słowo (GONE, DONE, NEW) | Animacja ma POKAZAĆ, że coś znikło (licznik spada, kafel pęka). Wyjątek: tekst, który byłby na prawdziwym ekranie (przycisk, status „Opłacone”). |
| Szary podtytuł pod każdym nagłówkiem karty | Jedna linia na wiersz. Liczba, pasek albo ikona niosą resztę. |
| Kadr stoi > 0,6 s | `check.py motion`. Dodaj coś, co żyje: kursor, pulsowanie, najazd, toczący się licznik, odblask. |
| Kluczowy element wchodzi na ostatnim słowie zdania | Bohater wchodzi wcześnie (na 1.–2. słowie albo 0,2 s po starcie sceny), a kolejne etapy są na kolejnych słowach. |
| Element „przed” w scenie przed/po czeka na swoje słowo | Stan „przed” jest od klatki 0, a na słowie dostaje tylko puknięcie. Zamiana jest sekwencyjna, bez przenikania. |
| Pusta połowa karty czeka na drugi wiersz | Karta zaczyna mała i ROŚNIE, gdy przychodzi wiersz. Samotny kafel stoi na środku i odsuwa się, gdy wchodzi partner. |
| Licznik od 0 do 91 000 w 0,9 s | Gdy beat < 1,2 s, pokaż od razu wynik (pop). Wielkie kwoty dostają licznik-klapki (`flap_keys`). |
| Proste linie łączące elementy | Łuki S rysowane na słowach (`curve`). |
| Rysowani ludzie i postacie | Prawdziwe ikony: Fluent 3D, App Store (`fetch_icon.py`), zdjęcia. Rysujemy tylko UI, wykresy i rekwizyty. |
| Wymyślone liczby lub nazwy podane jak fakt | Najpierw sprawdź fakty (strona, repo, nagranie). Przykładowe dane zaznacz w raporcie. Liczba z ekranu inna niż w audio? Pokaż poprawną i zgłoś. |
| Glif ©, ★, ⌘ lub ✓ w Geist, „—” w Studio Serif | Brak glifu = pustka albo emoji. Rysuj ścieżką albo użyj zwykłego myślnika. |
| Grupa kamery z pozycją (0,0) i kotwicą (960,540) | Wszystko ucieka w lewo w górę. Pozycja grupy musi być równa kotwicy: `group(id, …, 960, 540, 960, 540)`. |
| `lower()` liczone za wcześnie | Rozwiązane w `build()`. Obrazy (`image()`) są warstwami dokumentu, więc nie są dziećmi grup i trzeba je animować osobno. |
| Dwa klucze w t=0 (`push_in` od 0, `fade` + własne `opacity`) | `build()` przerywa. Jedna funkcja na właściwość warstwy, start od t > 0 albo bez klucza HOLD. |
| Łączenie segmentów z AAC (`concat -c copy`) | Każdy segment ma własny „priming”, więc dźwięk ucieka od obrazu. Segmenty idą z PCM (`cut_takes.py` tak robi), a AAC kodujemy raz na końcu. |
| Ufanie końcom słów z ASR | Pauzy mierz z audio (`check.py pauses`). Scribe i Whisper wydłużają ostatnie słowo przed pauzą. |
| Ukryta powtórka w jednym długim „słowie” (> 1,5 s, ⚠ w `pack_takes`) | Wytnij ±2 s i transkrybuj sam fragment. Po cięciu zrób `cut_takes.py … --audit` (transkrypcja każdego łączenia). |
| Stara transkrypcja z cache po ponownym cięciu | Usuń json przed transkrypcją. Słowo kończące się po końcu pliku = stary cache. |
| Pady na łączeniach tworzą nowe pauzy | Po cięciu zawsze `check.py pauses CUT.mp4` i skróć wszystko > ~200 ms, chyba że to celowa pauza ze skryptu. |
| Wycięta celowa pauza ze skryptu ([pauza]) | W `takes.json` daj `{"keep": true}` albo `{"hold": 0.5}`. |
| Zamknięcie renderu w połowie | Zabij też ffmpeg, usuń częściowy plik i dopiero wtedy renderuj od nowa. |
| Obietnica „odsłuchałem” | Nie słyszymy. Raportuj uczciwie, że kontrola była sygnałowa (pauzy, głośność, transkrypcja łączeń). |
| Poprawianie starych projektów bez prośby | Konrad: „nie montuj mi starych ads/vsl”. Błędy w starych rzeczach tylko zgłaszaj. |
| Sąsiednie zakresy z tego samego ujęcia nachodzą o ~20 ms (pad końca + pad startu) → zdublowany dźwięk | `cut_takes.py` scala stykające się/nachodzące zakresy (od 2026-10-03). Po zmianach sprawdź: brak zakresów < 0,4 s i brak nakładek. |
| `hold` na słowie, po którym od razu leci powtórka → mikro-kawałek 0,1 s | Pauzę dramatyczną dawaj tam, gdzie w nagraniu naprawdę jest cisza (często PRZED słowem-puentą, na końcu poprzedniego take'a). |
| Stały próg ciszy (−50 dB) przy cichszym nagraniu → pauzy 260–500 ms (oddechy −36…−45 dB) przechodzą nieskrócone | `cut_takes.py` liczy próg z zachowanego materiału (p15 + 10 dB, jak `check.py pauses`) i mierzy, gdzie słowo naprawdę kończy się w dźwięku (ASR wydłuża ostatnie słowo nad oddech). Wnętrza słów chronione, +80 ms ogona na miękkie głoski. |
| Wysoki próg na całym zakresie zjada ciche końcówki („tysię-”, „roś-”) | Nigdy nie tnij wnętrza słowa wysokim progiem: wewnątrz słów liczy się tylko prawdziwa cisza. Po zmianie progu sprawdź, czy żaden usunięty fragment nie nachodzi na słowo. |
| Pauzy 260–280 ms w audycie leżą wewnątrz słów (sz, cz, p) | To głoski, nie przerwy. Nie tnij. Audyt liczy cichą mowę jako pauzę. |
| Promień rogów obrazu w pikselach (`cornerRadius` 40) → zdjęcie jak pigułka | Silnik trzyma `cornerRadius` obrazu WZGLĘDNIE do krótszego boku; `image(r=px)` przelicza to od 2026-10-04. |
| Glif ↻ (i inne symbole) w Geist → `missing_fonts AppleColorEmoji` | Strzałki i pętle rysuj ścieżką (łuk + grot). |
| Kłódka z `ring(trim 50)` + obrót wygląda na otwartą | Rysuj pałąk jako półokrąg ścieżką (`padlock()` w scenes_yt.py, warto przenieść do apple.py). |
| Granatowy „blob głębi” w rogu wygląda jak tani pastelowy smug | Głębię dawaj ruchem kamery (`camera()` z najazdem na detal) i cieniem kart, nie rozmytą plamą. |
| Kilka scen naraz ustawia tę samą właściwość (np. `enter` + własne `opacity`) | `build()` przerywa. Jedna funkcja na właściwość albo własne klucze zamiast `enter`. |
| Bramka ruchu nie widzi cienkich linii, małych pierścieni ani rozmytego tekstu | To nie znaczy, że kadr stoi, ale przy > 2 s dodaj coś wyraźniejszego (najazd kamery, rosnący element, licznik). |
| Ikona 3D „zwrócona” w złą stronę (biegacz Fluent patrzy w LEWO) | Zanim ustawisz kierunek ruchu lub rekwizytu (marchewka, strzałka), obejrzyj PNG ikony. |
| `G(...)` ma domyślnie `op=0` — grupa bez `enter`/`fade` jest niewidoczna (tłum w S33a zniknął) | Grupy, które nie mają wejścia, twórz z `op=100`. |
| Klucze `textContent` liczone względem wejścia grupy | Czas klucza to zawsze czas SCENY (`w(t) - LEAD`), nie offset od rodzica. |
| Scena bez obrazów niepotrzebnie z `sc.lower(CAM)` → brak ruchu kamery | `lower()` tylko gdy są `image()`; inaczej kamera (`camera()`) daje najazd na detal. |
| Pusta połowa kadru przez kilka sekund (mapa wchodziła dopiero przy miastach) | Drugi element kompozycji jest od początku (szary), a na słowie tylko ożywa. |
| 1–15 klatek kamerki między dwiema animacjami (sceny zaczynają się 50–560 ms po końcu poprzedniej) | Konrad 2026-10-04: animacje mają iść jedna po drugiej. Po zbudowaniu wszystkich partii uruchom `snap_gaps.py PROJ scenes*.py` (zamyka luki < 1,2 s, wydłużając poprzednią scenę; `apple.Scene` czyta `snap.json`), potem przebuduj i wyeksportuj. Celowe wejścia twarzy ≥ 1,2 s zostają. |
| Pusty pierwszy kadr sceny (tło bez treści przez 1–3 klatki), bo `enter(t=40)` albo pisanie od pustego tekstu; po sklejeniu animacji błyska jak przerwa | `enter()` przy t ≤ 60 ms startuje już widoczne (55%). Pisanie otwierające scenę: `type_keys(0, tekst, start=len(pierwsze słowo))`. Bramka `check.py motion` → BLANK FIRST FRAME = do poprawki, nie „ok”. |
| Po złożeniu dalej 1–2 klatki kamerki na złączach, mimo snap.json | Klipy są kwantowane do klatek (kończą się do 1 klatki przed `out`), a `eof_action=pass` odsłania wtedy kamerkę. Każde wejście klipu przepuść przez `tpad=stop_mode=clone:stop_duration=0.5` (jest już w export.py --full i w final.py). Weryfikacja: porównaj klatki FINAL i CUT wokół każdego złącza; różnica ≈ 0 oznacza, że kamerka przebija. |
| Finał krótszy o ~0,4 s (ucięty ogon audio) | `loudnorm` połyka końcówkę. Rób `apad=pad_dur=1` przed loudnorm i `atrim=0:DUR` po nim. |
| Głos w finale wyprzedza obraz o 0,2–0,4 s od połowy filmu (w odtwarzaczu CUT wszystko gra, a po masteringu się rozjeżdża) | Część segmentów cięcia ma PCM o 1 klatkę krótszy niż obraz. Odtwarzacz wstawia tam ciszę według znaczników czasu, ale filtry audio sklejają próbki. Każdą obróbkę dźwięku z CUT zaczynaj od `aresample=async=1:first_pts=0` (cut_takes.py robi to teraz już przy enkodzie). Synchron sprawdzaj korelacją pełnych dekodów; samo `-ss` na AAC kłamie. |
| Przycięty b-roll w złożeniu pokazuje wcześniejszy moment animacji (spóźnia się o ułamek sekundy do sekundy) | Wejściowe `-ss` z `-itsoffset` i `setpts=PTS-STARTPTS` przesuwa klatki pre-rollu z wyszukiwania. Okno z klipu wycinaj filtrem `trim=start:end`, a potem `setpts=PTS-STARTPTS+IN/TB`. Weryfikuj porównaniem klatek FINAL i klipu na początku, w środku i na końcu każdego okna. |
| Scribe zwraca 401 `quota_exceeded` (2026-10-08: 95 kredytów z 10 000, a 12-minutowy film potrzebował 843) | Darmowy limit ElevenLabs się skończył. Do gotowego, już pociętego filmu użyj `transcribe.py` (Whisper lokalnie). Do cięcia surówki z powtórkami Scribe jest potrzebny, więc zgłoś to Konradowi (doładowanie lub kolejny miesiąc). |
| Film z kilkoma układami (kamerka / split z ekranem / PiP) i prośba „montuj tylko pełny ekran” | Wykryj układy automatycznie z cech klatek 4 kl/s: szew na x=960 (split), udział bieli > 0,8 (PiP na tablicy), ciemne piksele włosów w centrum (sama kamerka). Mediana z okna 7 klatek, scalanie odcinków < 1 s. Zapisz do `layout.json` i animuj tylko odcinki F. |
| Na karcie-nakładce brakuje ikon (żarówka, portfel, robot…) w złożonym filmie, choć w podglądzie są | `--fx-solo main:100` (eksport `_NAKLADKA.mov` z alfą) pomija obrazy dokumentu (`sc.image`). Karty z ikonami składaj z `_MIX.mp4` (to samo nagranie pod spodem) albo rysuj ikony ścieżkami. Sprawdzaj arkusz z GOTOWEGO filmu, nie tylko podgląd sceny. |
| Film Konrada ma −20 LUFS | YouTube nie podgłaśnia. Przy oddaniu mastering do −14 (`aresample=async=1` + loudnorm dwuprzebiegowy) i zgłoś to w raporcie. |
| Źródła z różnym układem audio (start mono 44,1 kHz, główny stereo 48 kHz) → po concat głos zamienia się w bełkot od pierwszego segmentu z drugiego pliku (2026-10-09) | `cut_takes.py` wymusza teraz `-ar 48000 -ac 2` na każdym segmencie. Przy kilku plikach zawsze sprawdź `ffprobe` audio każdego źródła i przeczytaj audyt łączeń. |
| Cięcie na siatce 1/30 s (`-ss` + `-r 30`), a klatki iPhone'a leżą ~15 ms obok siatki → 45 % kawałków zaczynało się zdublowaną klatką (mikro-zatrzymanie na łączeniu; YT_2026-09-10: 124/277) | `cut_takes.py` od 2026-10-09 zaczyna każdy zakres na prawdziwej klatce źródła (`ss`/`n` w edl.json), dźwięk z tego samego momentu. Nie wracaj do `-ss` na siatce. |
| Pełny render cięcia po każdej poprawce takes (9.10: 3 rendery = 3 h z 4 h 18 min) + `rm -rf segs` | Poprawki na `--audio --audit` (sekundy), `--preview` do akceptacji, `--render` raz; kawałki w `cache/segs/` — nigdy ich nie kasuj w trakcie projektu. |
| Audyt łączeń sklejony w jeden przebieg Whispera (test 2026-10-09) wymyślał powtórki („×3”) i gubił słowa | Audyt zawsze okno po oknie (model wczytany raz, cache per okno). Nie skracaj tego sklejaniem. |
| Parakeet na bardzo krótkim fragmencie (< 3 s) zgaduje język (cyrylica, „Yeah”) | Krótkie fragmenty (ratunek falstartów, audyt) → Whisper z `language="pl"`. Parakeet tylko na oknach ~45 s. |
| Długie okna Parakeeta (60 s) → szczyt pamięci ~12 GB, pierwszy przebieg padł po cichu przy równoległym renderze | `asr.py` tnie na ≤ 45 s przy ciszy (szczyt 2,8 GB). Zawsze sprawdzaj kod wyjścia, nie filtruj stderr do zera. |


| Znane ograniczenie (2026-10-10): assemble.py w trybie --reedit różni się od final_v2.py w 1 klatce na końcu wygaszanej karty (karta ~0 % krycia, 33 ms) | Niewidoczne; zaakceptowane przez Konrada. Nie poprawiać bez potrzeby. |
