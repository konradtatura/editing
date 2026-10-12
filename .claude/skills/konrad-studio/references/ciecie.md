# Cięcie surówki (talking head, teleprompter, kilka podejść)

Cel: film ma brzmieć świetnie z zamkniętymi oczami. Bez powtórek, bez zawahań, ciasno, ale naturalnie.

## Proces

1. **Transkrypcja dosłowna każdego pliku źródłowego.**
   - Najpierw `$PY $K/preflight.py PROJ RAW…` (mieszany dźwięk, VFR, miejsce na dysku — sekundy zamiast godziny renderu).
   - Domyślnie `$PY $K/asr.py RAW.MP4 PROJ/tr_<nazwa>` (Parakeet v3 w `~/.venvs/parakeet` + polski Whisper na fragmentach
     z mową bez słów). Test 2026-10-09 na 23 min: 2:51 zamiast 33:16, więcej zachowanych powtórzeń (112 vs 94), zero
     „Dzięki za oglądanie”. ⚠ w transkrypcie = falstart/powtórka odzyskana w drugim przebiegu albo mowa bez słów — sprawdź.
     Wynik jest w cache (`~/.cache/konrad-studio/asr`); ponowne uruchomienie na tym samym pliku = 0 s. Nie kasuj transkryptów.
   - Scribe (ElevenLabs, klucz w `~/Documents/Codex/video-use/.env`) tylko gdy Konrad doładuje limit i chce porównania:
     `cd ~/Documents/Codex/video-use && .venv/bin/python helpers/transcribe.py RAW.MP4 --edit-dir PROJ/edit --language pl`.
   - Nigdy nie używaj cudzych kluczy z paczek skilli.
   - Whisper na całym pliku (`transcribe.py`) pomija powtórki i nadaje się tylko do gotowego cięcia.
   - Potem `$PY $K/pack_takes.py PROJ/edit/takes_packed.md tr1.json tr2.json --gap 0.35`, czyli wszystkie podejścia obok siebie.
     ⚠ oznacza „słowo” dłuższe niż 1,5 s, w którym może być ukryta powtórka.
   - Do wyboru co do słowa zrzuć `słowo@start` z jsona (przykład w `references/przyklady.md`).
   - Skrypt (`.md`) czytaj równolegle: [pauza] w skrypcie = pauza do zachowania.
2. **Wybierz podejścia (to robisz Ty, nie skrypt).**
   - **Źródłem prawdy jest NAGRANIE, nie skrypt** (Konrad, 2026-10-03: „skrypt to plus minus, ma mi pomóc mówić”).
     Treść filmu = to, co Konrad mówi w najlepszych podejściach, także improwizacje, dopowiedzenia i retoryczne
     powtórzenia („Ile z nich osiągnęło to, co chcieli? Ile osiągnęło sukces?”). Nie wycinaj niczego tylko dlatego,
     że nie ma tego w skrypcie, i nie dopisuj na ekranie rzeczy ze skryptu, których nie powiedział.
   - Wycinasz tylko: powtórzone podejścia, falstarty, jąkanie, urwane zdania, wtrącenia do siebie („tak, tak”, „okej”
     na restart) i zdania, które się rozsypały. Skrypt służy do orientacji (kolejność, [pauza], gdzie kończy się myśl).
   - Każde zdanie skryptu bierz z najlepszego **pełnego** podejścia, zwykle ostatniego, ale nie zawsze.
   - Zostaw dobre improwizacje spoza skryptu.
   - Dogrania z innego pliku (np. poprawiona końcówka) zastępują resztę starego ujęcia.
   - Zapisz `takes.json` (format w nagłówku `scripts/cut_takes.py`; wzór: `examples/vsl_cut_takes.py`).
3. **Uruchom** (od 2026-10-09 bez renderu wideo w pętli poprawek):
   - `$PY $K/cut_takes.py PROJ/takes.json --audio PROJ/CUT_audio.wav --audit` → dźwięk cięcia co do próbki (sekundy)
     + `splice_audit.txt`. Audyt przelicza tylko łączenia, których dźwięk się zmienił.
   - Poprawiasz `takes.json` i powtarzasz. Progi pauz są zamrożone w `edl_params.json` po pierwszym przebiegu
     (inaczej poprawka jednego ujęcia przesuwałaby cięcia w innych); `--refreeze` mierzy je od nowa.
   - Konrad ogląda `--preview PROJ/CUT_preview.mp4` (960 px). Po akceptacji: `--render PROJ/CUT.mp4` (profil `vt` =
     koder sprzętowy, VMAF 98,5; `--profile slow12` = stary wygląd CRF 12, 9× wolniej). Kawałki są w `cache/segs/`,
     więc późniejsza poprawka renderuje tylko zmienione kawałki.
   - Trzecia wartość może być STARTEM ostatniego słowa, wtedy skrypt sam bierze jego koniec.
   - Opcje take'a: `{"keep": true}` (bez skracania pauz w środku) i `{"hold": 0.5}` (zostaw 0,5 s ciszy po zdaniu, przed puentą).
   - Oś czasu w `edl.json`: każdy zakres zaczyna się na PRAWDZIWEJ klatce źródła (`ss`, `n` klatek, `t` w cięciu).
     Dźwięk jest wycinany z tego samego momentu, więc obraz i dźwięk są zgodne co do próbki (test: ≤ 0,04 ms).
   - Krawędzie są dociągane do obwiedni audio, wdech przed ujęciem jest wycinany, ciche głoski są chronione (próg −50 dB),
     każda cisza > 200 ms wewnątrz ujęcia jest skracana do ~140 ms.
   - `--legacy` = stary renderer (tylko do wycofania zmian).
4. **Kontrola.**
   - Przeczytaj `splice_audit.txt` i transkrypt (po akceptacji jedna transkrypcja CUT): żadnej powtórzonej frazy, uciętego zdania ani sierocego słowa („I-i dlatego”).
   - `check.py pauses CUT_audio.wav` to każda pauza z audio. Skróć > ~200 ms, chyba że celowa.
   - Zgłoś miejsca niepewne. Kontrola jest sygnałowa, nie odsłuch.
   - Wpisz decyzje do `PROJ/edit/project.md`.

## Zasady tempa (z poprawek Konrada; on zawsze skraca, nigdy nie wydłuża)

- **Cisza na granicy zdań i na łączeniu ujęć: ~100–150 ms.** Przecinek lub oddech wewnątrz zdania: ~80–120 ms.
  Dłużej (250–300 ms) zostaw tylko świadomie, np. po pytaniu retorycznym lub przed puentą.
- **Nie ufaj końcom słów z ASR.** Ostatnie słowo przed pauzą bywa wydłużone; mierz ciszę z obwiedni audio.
- **Oddechy i nieleksykalne dźwięki przed wejściem ujęcia** traktuj jak ciszę (ASR potrafi wdech zapisać jako „Wiesz”).
- **Zapas:** 30–60 ms przed rzeczywistym początkiem głoski, 30–80 ms po końcu. Fade audio 30 ms na każdej krawędzi.
- **Nie** przyspieszaj głosu, **nie** ucinaj głosek, **nie** usuwaj treści dla długości.
  Gdy masz wątpliwość, zapytaj albo zostaw i zgłoś.

## Jakość

- Tnij zawsze z **oryginału**: CRF 12, preset slow, źródłowa rozdzielczość i kolory bt709.
  Każdy zakres renderowany osobno: obraz H.264, dźwięk PCM. Łączenie concat (obraz kopiowany), jedno kodowanie AAC na końcu.
- Przy kolejnych poprawkach wracaj do źródła, nie kompresuj skompresowanego.
- Gdy Konrad przyśle własną poprawioną wersję cięć, to jest wzorzec czasu. Odtwórz go na surówce, jeśli ją masz.

## Pułapki z cudzych montaży (famous-reel-editor, albert-reel-dark)

- Liczby zapisane słowami („sto sześćdziesiąt”) scal przy napisach i animacjach w cyfry.
- Dwa podejścia zlane w jedno długie słowo: tnij w dołku obwiedni między nimi, nie po czasach ASR.
- Zdanie urwane w biegu („…bo jego produkt jest i pierwsza osoba…”): koniec ustaw w dołku 20–40 ms przed kolejną głoską.
- Każde cięcie od nowa: nowa transkrypcja, pauzy i audyt łączeń, bo stare czasy są nieważne.

## Typowe pułapki z VSL

- Audio mówi inną liczbę niż poprawna (177 vs 171 zł): nie tniesz tego, tylko zgłaszasz. Na ekranie pokazujesz poprawną.
- Jąkanie na łączeniu („I-i dlatego”): zgłoś albo popraw krawędź.
- Dogrywka w drugim pliku ma inny poziom głośności: sprawdź `check.py loud` na obu.
