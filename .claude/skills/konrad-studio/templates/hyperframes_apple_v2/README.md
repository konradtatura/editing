# HyperFrames · biały Apple v2 (anti-AI-slop) — zestaw do animacji longform

Styl zatwierdzony przez Konrada („Skupienie”, „3 modele”, 2026-10): biel, tylko Inter (hierarchia grubością), jeden akcent
#0071e3, czerwony tylko na stratę, natywne UI iOS jako metafory, prawdziwe ikony aplikacji, zero poświat/szkła/emoji.
Wyjątek: biały tekst na ścianie obok głowy ma czarny miękki cień (WALL_CSS).

## Pliki
- `base.css` — tokeny, typografia, karty, telefon, przełączniki iOS, checkboxy.
- `kit.js` — `K.rise/sink/lift/count/type/draw/shake/stamp/strike/weight/toggle/click/tap/push/card/whip/frame`
  (wszystko liczone z czasu playheadu → bezpieczne przy renderze wieloma workerami).
- `page.py` — zapis strony sceny (1920×1080; overlay = MOV z alfą).
- `words.py` — `W("słowo", po_czasie)` = start słowa z `../tr/words.json` (transkrypcja CUT.mp4).
- `geo.py` — kontury krajów z `assets/*.geo.json` → ścieżka SVG + punkty (pinezki).
- `chk.sh KLUCZE…` — szkic + arkusz 5 klatek (karty na prawdziwym kadrze CUT) → `out/KLUCZ_sheet.png`.
- `render.sh KLUCZE…` — finalna jakość (B → MP4, K → ProRes 4444 MOV).
- `sheet_batch.py OUT.jpg KLUCZE…` — arkusz partii z podpisami (to wysyłasz Konradowi).
- `sfx.py` — dźwięki odczytane z kodu scen (wejścia, liczniki, kliknięcia, stemple) → `../SFX.wav`.

## Przebieg
1. `cp -R templates/hyperframes_apple_v2 PROJ/anim` (potrzebny `PROJ/tr/words.json`).
2. `buildN.py` wg `examples/longform_3modele/build1.py` (sc(key, a, b, "B"|"K", body, js, css); czasy ze słów).
3. `python3 buildN.py` → `./chk.sh …` → obejrzyj arkusze, popraw (pusta klatka na starcie, za małe elementy, nachodzenie).
4. `python3 sheet_batch.py ../PARTIA_N.jpg …` → wyślij; `./render.sh …` w tle.
5. Finał: `python3 sfx.py` → `assemble.py PROJ --scenes anim/scenes.json --sfx SFX.wav --settle 0.3 --zooms auto --out FINAL.mp4 --bez-sfx`.

## Pułapki (z praktyki)
- `K.rise` przepisuje innerHTML — licznik (`K.count`) nie może siedzieć w elemencie, który się „rise'uje” (scena padnie).
- Selektor `.x span {display:block}` psuje słowa po `K.rise` — stylizuj po id.
- Słowa, których Whisper nie złapał: czasy z `edl.json` + `words_raw.json` (mapowanie surówka → cięcie), wpisz na sztywno.
- Element nie może czekać pusty > 1 s: wszystko widoczne od startu, na słowie tylko „ożywa”.
