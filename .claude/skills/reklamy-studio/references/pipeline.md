# Pipeline: komendy krok po kroku

`W` = katalog roboczy (scratchpad). `P` = `projekty/` w repo. Media nigdy nie idą do repo, tylko kod.

## 0. Narzędzia (jednorazowo)
- Python: `faster-whisper`, `numpy`, `opencv-python`; ffmpeg; Node + `playwright` (Chromium).
- `render.mjs` ładuje playwright przez `createRequire` z globalnych node_modules (`PW_ROOT`, domyślnie `/opt/node22/lib/node_modules/`).
  Na komputerze Konrada: `npm i -g playwright && npx playwright install chromium`, potem `PW_ROOT=$(npm root -g)/`.
- Fonty są lokalnie w `P/reklamy_CA/engine/assets/fonts/` (Inter, Instrument Serif: `g.css`; Poppins: `poppins.css`). Ikony: `assets/icons/*.svg` (lucide).

## 1. Materiały z Drive
```bash
gdown --folder --json <URL_folderu>          # lista plików i ID (bez pobierania)
gdown -O ads2.mp4 <ID>                         # pobranie jednego pliku
```

## 2. Wzór
- Arkusz klatek: `ffmpeg -i REF.mp4 -vf "fps=1/2,scale=240:-1,drawtext=text='%{pts\:hms}':...,tile=8x4" ref_%02d.jpg`
- Animacja napisów: `ffmpeg -ss T -i REF.mp4 -t 1.2 -vf "fps=10,crop=...,tile=2x6"` (widać, czy słowa wchodzą, czy przełączają się twardo).
- Detal: crop w pełnej rozdzielczości, żeby odczytać font, cień i rozmiar.

## 3. Cięcia i transkrypcja
```bash
python3 P/reklamy_CA/engine/cuts.py ads2.mp4 > cuts.json      # czasy pierwszej klatki nowego ujęcia
python3 tools/tr.py ads2.mp4 tr_ads2 medium                    # -> tr_ads2.json (słowa z czasami) + .txt
```
Surowe duble (Teleprompter) tnie `P/reklamy_CA/engine/cut.py TAKES.json OUT.mp4` (flagi „x” = dokładny start, „y” = koniec nie później niż).

## 4. Spec
`python3 P/stylN/build_specN.py W ...` → `W/specN_<ad>.json`. W pliku builda:
- `FIX…` = tekst ze skryptu z markupem akcentów (nakładany na czasy whispera),
- `IT…` = lista plansz i elementów z czasami (t0/t1 na cięciach!),
- `make(..., extra_cuts=(...), capY=...)`.

## 5. Render warstwy i kompozycja
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

## 6. QA
```bash
python3 P/styl2/engine/qa.py SPEC.json OUT.mp4 qa      # pary przed|po przy każdym cięciu i krawędzi elementu
ffmpeg -i OUT.mp4 -vf "fps=1,scale=216:384,drawtext=...,tile=10x4" sheet_%02d.jpg   # cały film co 1 s (gęściej: fps=2)
```
Oglądam każdy arkusz (Read obrazu). Checklistę mam w `bledy-i-lekcje.md`.

## 7. Eksport
Dwuprzebiegowo z wyliczonym bitrate: `vb = MB*8192/dur - 128` kb/s.
- Review: 720:1280, ok. 13,5–14 MB.
- FINAL: 1080:1920, 27–28,5 MB (limit 30 MB), audio AAC 128k, `-movflags +faststart`.

## 8. Review (artefakt Video Review)
- Upload: `Artifact` z `asset: true` (kilka plików naraz: `file_paths`).
- Baza: kolekcja `videos` (title, asset, url, order, ver, dur) → `update` z `if_version`; nowa reklama = `set`.
- Notatki: kolekcja `notes` (video, t, x, y, text, status). Czytam `query status == open`, poprawiam, odpowiadam
  (`reply`) i ustawiam `status: done` jednym `batch`.

## 9. Repo
Kod i specy (`build_spec*.py`, `engine/*`, `zones`, `cues`) commit + push na branch sesji. Media, klucze (Pexels) nigdy.
