---
name: konrad-studio
description: "Konrad's all-in-one video editor, thinking like a $20k/video editor: YouTube longform (cutting teleprompter takes, face/b-roll/card proportions, animation batches), VSLs 16:9, vertical ads and reels, captions, sound design, Iman-style music scoring and full hand-over with QA gates. Also reverse-engineers any reference edit (frame-level breakdown → clip catalogue → shot plan → kinetic engine: word-by-word motion-blur captions, blue/white cards, B&W vs colour, feed wall, photo collage, 2×2 flicker grid, giant city names) and keeps an effects toolbox for every video. Use for any request to edit, cut, animate or caption a video: „zmontuj”, „wytnij powtórki”, „zrób animacje”, „b-rolle”, „napisy”, „pod VSL / reklamę / rolkę / longform”, „zrób mi taki edit jak ten / odwzoruj / breakdown”, „jak ostatnio”, or when Konrad sends raw Teleprompter .MP4 files + a script."
---

# Konrad Studio: montaż w Apple style

Zapis całego warsztatu z filmu „Zbudowałem AI biznes w 3h”, VSL „Cyfrowy Autopilot” v2, reklam ANGLE i lekcji z referencji
(2 filmy-wzory i 6 skilli znajomego, 2026-10-03). **Cel każdego montażu:** wygląda jak od montażysty za 20 tys. $ za film,
czysty Apple style z warstwą premium, a każda animacja trzyma retencję. Twarz Konrada niesie przekaz, grafika go wspiera.

Konrad jest marketerem, nie montażystą. Pisz po polsku, krótko. Nie pytaj o kodeki, fps ani silniki, tylko o treść:
zatwierdzenie listy, niepewny fakt, preferencje filmu (napisy, muzyka i jej klimat, memy). Często odpowiada z telefonu, więc wysyłaj `_tel.mp4`.
**Nie ruszaj starych projektów bez prośby.** Błędy w nich tylko zgłaszaj.

## Najpierw przeczytaj (zawsze)

1. `references/myslenie-editora.md`: jak myśli montażysta. Retencja, kiedy animować, metafora, wejście przed słowem, autotesty.
2. `references/styl-apple.md`: wygląd, ruch, paleta, warstwa premium, biblioteka metafor, zakazy.
3. `references/feedback.md` (uwagi i fakty o marce) oraz `references/bledy.md` (błędy, których nie powtarzamy).
4. `references/biblioteka-efektow.md`: cała skrzynka efektów z oceną „kiedy”. Wybieraj z niej do każdego zdania.

Potem tylko to, czego wymaga zlecenie:

| Zlecenie | Czytaj |
|---|---|
| Surówka do pocięcia (powtórki, pauzy) | `references/ciecie.md` |
| Longform YT (gramatyka ujęć, timer, layout) | `references/formaty.md` § Longform |
| VSL 16:9 / reklama lub rolka 9:16 | `references/formaty.md` § VSL / § Pion |
| Budowa animacji | `references/silnik-tesseract.md` + `references/przyklady.md` |
| Napisy | `references/napisy.md` |
| Muzyka (styl Imana, cisze, drop na słowie) | `references/muzyka.md` |
| Przesiew longformu („za dużo animacji”) | `references/formaty.md` § Proporcje + `examples/longform_reedit_*.py` |
| Konrad przysyła film-wzór („zrób mi taki edit”, „odwzoruj”, breakdown) | `references/odwzorowanie-referencji.md` + `referencje.md` |
| Szybka rolka/reklama z napisami słowo po słowie, plansze, siatki | `scripts/kinetic.py` + `examples/kinetic_16x9_nathan_style.py` |
| **Każdy film:** jakie efekty do jakich zdań | `references/biblioteka-efektow.md` |
| **Każdy film, po grafice:** warstwa detali (SFX, tekst na twarzy, whipy, kursory, settle) | `references/detale-montazu.md` |
| Każde oddanie | `references/oddanie-qa.md` |

## Tryb automatyczny (od 2026-10-09): `ks.py` prowadzi projekt i pamięta wykonaną pracę

`$PY $K/ks.py PROJ init RAW1.MP4 RAW2.MP4` → `$PY $K/ks.py PROJ run` (powtarzaj po każdej decyzji) → `ks.py PROJ status`.
Kroki: preflight → asr → pack → [Ty: `takes.json`] → cut (dźwięk + audyt) → preview (+ `_tel`) → [Konrad: `ks.py PROJ approve cut`]
→ render (CUT.mp4) → words (`tr/words.json`) → [animacje: `anim/scenes.json`+`anim/out` albo `index.json`] → final (`FINAL.mp4`, `_tel`, `_bez-sfx`).
Krok bez zmian na wejściu jest pomijany; przerwany render wznawia się od gotowych kawałków. Czasy w `PROJ/runs.jsonl`.
Ręczne polecenia poniżej nadal działają (to te same narzędzia).

## Pipeline (jeden projekt = jeden folder, np. `~/Downloads/reelsygotowe/YT_<temat>/`)

`K=~/.claude/skills/konrad-studio/scripts` · `PY=/Library/Frameworks/Python.framework/Versions/3.13/bin/python3`
(ten Python ma Pillow, numpy, fontTools; `mlx_whisper` jest w tym samym `bin/`).

1. **Materiał.** Najpierw `$PY $K/preflight.py PROJ RAW1.MP4 RAW2.MP4 …` (sekundy: dźwięk mono/stereo, fps, VFR, miejsce
   na dysku, silniki ASR; exit 2 = bloker). Potem obejrzenie klatek (`$PY $K/check.py sheet RAW.MP4`): gdzie jest głowa,
   wolne ściany, jasność. Skrypt `.md` kopiuj do projektu.
2. **Cięcie** (gdy jest surówka), według `ciecie.md` — szybka ścieżka od 2026-10-09:
   - `$PY $K/asr.py RAW.MP4 PROJ/tr_<plik>` dla każdego pliku (Parakeet v3 + ratunek falstartów, ⚠ = do sprawdzenia;
     23 min surówki ≈ 2–3 min, drugi raz 0 s z cache) → `pack_takes.py` → wybór podejść → `takes.json`.
   - Iteracje BEZ renderu wideo: `cut_takes.py takes.json --audio CUT_audio.wav --audit` (sekundy; audyt tylko zmienionych
     łączeń) → `check.py pauses CUT_audio.wav` → poprawki w takes.json → znowu `--audio --audit`.
   - Do akceptacji Konrada: `--preview CUT_preview.mp4` (960 px, kilka minut) → `check.py tel`. Po OK jeden render
     `--render CUT.mp4` (koder sprzętowy, kawałki z cache; poprawka po akceptacji przelicza tylko zmienione kawałki).
   - **Nigdy** `rm -rf segs`/`cache` przy poprawkach — cache to cała oszczędność czasu.
   - Oddaj CUT do akceptacji (`_tel`) **przed** animacjami, bo animacje synchronizujesz do zmontowanego filmu.
3. **Transkrypcja CUT** do animacji i napisów, RAZ po akceptacji cięcia: `$PY $K/transcribe.py CUT.mp4 PROJ/tr`.
4. **Plan, czyli jedyna bramka akceptacji.**
   - Longform: najpierw gramatyka ujęć (każde zdanie A / A+ / A+K / B / C / D, `formaty.md`), potem lista animacji
     `| # | od | co mówisz | tryb | co pokazujemy (metafora) |`, ⭐ przy kluczowych.
   - Autotest z `myslenie-editora.md` (zdarzenie co ~5 s, różne metafory, prawdziwe dane).
   - Wyślij listę i **czekaj na OK**. Gdy prosi „kolejne 20”, poprzednia propozycja jest zatwierdzona.
5. **Budowa** (`apple.py`):
   - Jedna funkcja = jedna scena z własną metaforą, wejście tuż przed słowem (`w(t) - LEAD`).
   - Partie ~20 scen: `$PY PROJ/scenes_x.py [KLUCZE]`.
6. **QA** (nie oddawaj niesprawdzonego), według `oddanie-qa.md`:
   - `preview.py PROJ --auto 0.05 0.5 0.95` i **przeczytaj arkusz**,
   - po eksporcie `check.py motion` (pusta 1. klatka, bezruch > 0,6 s), `check.py alpha`, `check.py loud`,
   - poprawiaj do skutku.
7. **Eksport:** `$PY $K/export.py PROJ/scenes_x.py [KLUCZE]` zapisuje do `Animacje/`
   (`_MIX` + `_NAKLADKA` dla nakładek, `_BROLL` dla pełnych ekranów; czas wejścia w nazwie, dźwięk oryginału).
   Efekty dźwiękowe: `sfx.py cues.json SFX.wav --dur … [--mix FULL.mp4 OUT.mp4]`, oddawane jako osobna ścieżka.
7b. **Finał:** `$PY $K/assemble.py PROJ --scenes anim/scenes.json|--index index.json --sfx SFX.wav --settle 0.3 --out PROJ/FINAL.mp4 [--bez-sfx]`
   (składanie po odcinkach z cache: poprawiona animacja = przeliczone tylko jej klatki; ta sama jakość co dawne final*.py,
   x264 slow CRF 16; `--upto SEC` na szybki fragment). Nie pisz już własnego `final_vN.py` dla projektu.
   Styl face-first („Ciężka praca” v2): `--index index.json --reedit edit/reedit.json --zooms auto [--zoom 114] --audio comp`
   (zbliżenia 100↔114% na początkach zdań, karty bez zbliżenia, przycięte b-rolle, wyciszenia kart — plan identyczny z final_v2.py).
7c. **Video Review = dashboard montażu jak Frame.io** (`review/`): `$PY review/review.py PROJ` → http://127.0.0.1:8765 (lokalnie).
   Odpalaj go od razu po pierwszym podglądzie i zostaw w tle. Każdy nowy plik w PROJ (CUT_preview → cięcie, FINAL → finał)
   staje się sam kolejną wersją (v1, v2…; stare zostają jako twarde linki). Po restarcie sesji: odpal ponownie (port 8765).
   - Układ: **lewa kolumna** = lista animacji z `anim/scenes.json` (miniatura, czas, typ, co mówi, liczba uwag; klik = skok),
     **środek** = film (klik = start/pauza, szybkość 0,5–2×, pasek animacji pod osią), **prawa** = uwagi + pole komentarza.
   - Uwagi: Enter = uwaga w tym momencie; „◎ Zaznacz na kadrze” → klik w kadr = kropka z numerem w tym miejscu;
     „＋ Zdjęcie” / Cmd+V / przeciągnięcie = zdjęcie przy uwadze (wzór, screen). Każda uwaga sama zna numer animacji.
   - Przełączniki: „pokaż zaznaczenia” (kropki), „oryginał bez animacji” (ten sam moment z ostatniego cięcia).
   - Gdy Konrad pisze „wysłałem poprawki / poprawki z review”: `$PY review/review.py PROJ --notes` → lista z czasem, animacją,
     punktem na kadrze, tym co mówi, **screenshotem z kropką** (`review/shots/ID.jpg`) i **jego zdjęciami** (`review/attach/`).
     Obejrzyj każdy obrazek (Read) przed poprawką. „wytnij od X do Y” → `$PY $K/cut_span.py PROJ X Y …` (oś wersji, na której pisał).
     Po poprawce: przelicz (ks.py run / build + render.sh + assemble.py) i `--reply ID "co zrobione"`.
   - „ZATWIERDŹ CIĘCIE” robi też `ks.py PROJ approve cut`. Nic nie wykonuje się samo — poprawki robisz Ty.
7d. **Animacje longform (aktualny silnik, od 2026-10-10): HyperFrames, biały Apple v2** — `templates/hyperframes_apple_v2/`
   (README tam). Skopiuj do `PROJ/anim/`, pisz `buildN.py` partiami ~25 scen (wzór: `examples/longform_3modele/` — 78 scen
   + PLAN_ANIMACJI.md), `chk.sh` = szkic + arkusz, `sheet_batch.py` = arkusz partii dla Konrada, `render.sh` = finalna
   jakość, `sfx.py` = dźwięki z kodu scen, potem `assemble.py --scenes anim/scenes.json --sfx SFX.wav --settle 0.3 --zooms auto`.
   Partię pokaż też w Video Review: `assemble.py … --upto SEC --profile vt` (szybki podgląd).
7e. **Muzyka bez pracy Konrada:** 3 utwory z vidIQ (napięcie/środek/finał) + `examples/music_bed_longform.py`
   (drop na słowie, cisze na puentach, pod głosem ~−30 LUFS). Zasady: `references/muzyka.md`. Oddaj FINAL (z muzyką) + _bez-muzyki.
8. **Oddanie:**
   - `check.py tel FULL.mp4` i wysłanie przez SendUserFile,
   - raport po polsku: pliki, liczby scen, a na pierwszym miejscu rzeczy do sprawdzenia
     (dane przykładowe, audio ≠ ekran, niepewne łączenia).
9. **Retro i nauka (obowiązkowe):** co poszło źle, wpis do `bledy.md` (i poprawka w skrypcie),
   uwagi Konrada do `feedback.md`, udana nowa scena do `examples/`.

## Zasady twarde

- **Face-first.**
  - Domyślnie twarz albo karta lub tekst w wolnej ścianie obok niej.
  - Pełny ekran tylko dla pojęć, liczb i schematów. W reklamie 9:16 około 3.
  - **Longform: twarz ok. 50% · pełne b-rolle ok. 40% · karty ok. 10%.** B-roll trwa 3–8 s, nigdy nie ma ponad ok. 10 s bez twarzy.
    Policz procenty już w planie animacji. Pierwszy longform miał 84% b-rolli i Konrad powiedział „mojej twarzy nie ma”.
  - Nie zmniejszaj Konrada do okienka (wyjątek: PiP podczas nagrania ekranu).
- **Każda scena to inna metafora.** Powtórzenie tylko jako celowy callback.
- **Mało tekstu:**
  - tylko słowa, które padają, liczby albo UI,
  - zero etykiet nazywających scenę, pieczątek powtarzających słowo i szarych podtytułów.
- **Prawdziwe dane, prawdziwe ikony.**
  - Fact-check przed rysowaniem, przykładowe dane oznaczone.
  - Ludzi i marki pokazuj prawdziwymi ikonami (`fetch_icon.py`), nie rysuj ich.
- **Zero martwych klatek:** treść od klatki 0 (`check.py motion` to sprawdza).
- **Karty w 100% kryjące.** Brak glifów ©, ★, ⌘, ✓ w Geist i „—” w Studio Serif, więc rysuj je ścieżką.
- **Nie renderuj całego filmu, jeśli nie trzeba:** efekty jako klipy z czasem wejścia w nazwie. Pełny film na prośbę lub do kontroli.
- **Uczciwość:** nie słyszymy dźwięku. Kontrole są sygnałowe i tak to raportuj.
