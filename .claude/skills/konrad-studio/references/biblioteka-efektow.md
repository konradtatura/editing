# Biblioteka efektów: skrzynka montażysty Konrada

Wszystko, co już zrobiliśmy i co działa. **Przy każdym filmie** (longform, VSL, reklama, rolka, odwzorowanie) przejrzyj tę listę
i wybierz efekty do zdań, a nie do „ładnego wyglądu”. Każdy efekt ma powód narracyjny.
Dwa silniki:
- **Tesseract** (`apple.py`, sceny wektorowe Apple, nakładki z alfą),
- **kinetic** (`kinetic.py`, szybki montaż klatka po klatce: napisy, b-rolle, plansze).

## A. Tekst

| Efekt | Kiedy | Jak |
|---|---|---|
| **Napisy kinetyczne** (pre / BOHATER / post), słowo po słowie, wjazd ze smugą | szybkie rolki i reklamy w stylu „dokument o bogactwie”, gdy tekst niesie rytm | `kinetic.Phrase` |
| Bohater = liczba / pieniądze / słowo emocji | w każdej frazie jedno słowo, które widz ma zapamiętać | `hero=[(idx, "big")]` |
| Licznik-klapki | duża liczba, która „robi wrażenie” (130 000+) | `Phrase(flap=(start, lock))` / Tesseract `flap_keys` |
| Przekreślenie | „kiedyś za 10 000 zł → dziś za darmo” | `Phrase(strike=t)` |
| Zamazanie słów białymi paskami → słowo-klucz | napięcie przed CTA („napisz słowo … „KURS””) | `Phrase(redact=(t0, t1))` |
| Cytat sceptyka w „ ” | zarzut widza („kolejny guru…”) | `Phrase(quote=True)` |
| Chromowany bohater | ciemne b-rolle, luksus | `Phrase(chrome=True)` |
| Słowo leżące na powierzchni (3D) | rzecz „na stole” (system, plan, mentoring) | `desk_text(quad=…)` |
| Gigantyczne słowo nad nagraniem | miasto, kraj, jedno mocne słowo | `giant()` |
| Słowa wchodzące z blur + uniesieniem (Tesseract) | nagłówki w longformie, karty | `reveal_words` |
| Kursywa szeryfowa na jednym słowie | akcent w zdaniu Apple-style | `family="Studio Serif"` |
| Napisy ciągłe pod brodą / w boxie | reklamy 9:16, VSL | `captions.py` (`napisy.md`) |

## B. Kadr i ujęcia

| Efekt | Kiedy | Jak |
|---|---|---|
| Jump zoom 100 ↔ 112–114% na początkach zdań | długa gadająca głowa, żeby twarz nie stała | `final_v2.py` (longform), `run(face_crop=…)` |
| Wolny najazd w ujęciu (push-in) | każdy b-roll i twarz, życie w kadrze | `clip_vf(zoom=0.04)` / `push_in()` |
| Pion → poziomy pas 16:9 | klipy Konrada z telefonu w filmie poziomym | `clip_vf(band=0…1)` |
| Punch-in kadru poziomego (crop) | zbliżenie na twarz/laptop z szerokiego ujęcia | `clip_vf(crop=(scale, cx, cy))` |
| Timelapse godzin pracy | „cały system”, „miesiące pracy” | kind `lapse` (`a`, `b` sekundy źródła) |
| Akcja zgrana ze słowem | laptop zamyka się na „zamknąłem”, wstaje od biurka, odwraca się do kamery | szukaj momentu w długim klipie arkuszem 1 kl/s |
| Puste miejsce po człowieku | „zamknąłem / odszedłem / koniec” | ujęcie biurka po wyjściu |
| Pasy kinowe otwierające | pierwsza sekunda filmu | `letterbox()` |
| Animacje bez przerw (bez klatek kamerki między nimi) | sklejanie scen Tesseract | `snap_gaps.py` + `tpad` |

## C. Narracja kolorem i układem

| Efekt | Kiedy | Jak |
|---|---|---|
| **B&W = „oni / problem”, kolor = „ja / wynik”** | kontrast „ich życie vs moje”, „przed vs po” | `grade="bw"` / `"cine"` |
| Plansze jasne / niebieskie / czarne | oddech między b-rollami, lista „bez X, bez Y”, zdanie bez obrazu | kinds `light` / `blue` / `black` |
| Czarny ekran „wiem, co myślisz” | zwrot do widza, odpowiedź na zarzut | kind `black` |
| Siatka 2×2 budowana migotaniem | wiele miejsc naraz (podróże, PL + USA, wiele wyników) | `grid_cells` + `grid_frame` |
| Kolaż polaroidów | lata, historia, dowód („od 14. roku życia”) | `Collage(photos)` |
| Ściana feedu 3D (B&W) | „wyskoczyło Ci na feedzie”, „wszyscy to robią” | `FeedWall(tiles)` |
| Ściana „guru” z wymyślonych miniatur | sceptycyzm wobec branży, bez cudzych twarzy | `GuruWall(titles)` |
| Karta nad twarzą (Tesseract) | liczba lub UI, a twarz zostaje | `_NAKLADKA` / `cards_v2.py` (b-roll → karta) |
| Pełny b-roll Apple (Tesseract) | pojęcie, mechanizm, porównanie | `styl-apple.md` § Biblioteka metafor |
| Prawdziwa strona / mapa / ikona | dowód, miejsce, marka | `highlight()`, GeoJSON, `fetch_icon.py` |

## D. Proporcje (sprawdzone na reakcjach Konrada)

| Format | Twarz | B-roll pełny | Karty / plansze |
|---|---|---|---|
| Longform YT | ok. 50% | ok. 40% | ok. 10% |
| Kinetyczna rolka/reklama 16:9 (styl Nathana) | ok. 30% | ok. 45% (kolor + B&W) | ok. 25% plansze i animacje |
| Reklama 9:16 | twarz prawie cały czas, karty na klatce piersiowej | ok. 3 krótkie | reszta karty (`formaty.md`) |

Zawsze licz proporcje już w planie. Za dużo animacji w longformie to „mojej twarzy nie ma”.

## E. Dźwięk

| Efekt | Kiedy | Jak |
|---|---|---|
| Boom / uderzenie basu na zmianie sekcji | otwarcie, nowy rozdział, zwrot („nie.”), CTA | generowany numpy (`odwzorowanie-referencji.md` §5) |
| Whoosh na planszy, tick na liczniku, click na kaflu | mikro-sync z obrazem | `sfx.py` (assets/sfx) |
| Muzyka montowana: cisza na puencie, drop na słowie, ściszanie pod głosem | gdy Konrad chce muzykę | `muzyka.md` (vidIQ generuje) |
| Głos −14 LUFS, dekodowanie po znacznikach czasu | każde oddanie | `aresample=async=1` + loudnorm (`bledy.md`) |

## F. Jak wybierać (myślenie montażysty)

1. **Najpierw zdanie, potem efekt.** Co to zdanie ma zrobić w głowie widza: zaskoczyć, udowodnić, porównać, rozbawić, zmusić do działania?
2. Liczba → licznik albo bohater. Porównanie → B&W vs kolor, siatka, split. Dowód → prawdziwy kadr (billboard, wynik, zdjęcie).
   Zarzut → czarny ekran albo cytat. CTA → zamazanie → słowo-klucz.
3. **Złoto z materiału Konrada** (jego billboard, auto, praca nocą) bije każdy stock i animację. Szukaj go w katalogu.
4. Coś nowego co ~1–2 s w rolce, co ~5 s w longformie. Żaden efekt dwa razy pod rząd.
5. Autoironia i humor (Konrad jako „dzieciak z brokułem na głowie”) działają, ale zgłoś je do decyzji.
