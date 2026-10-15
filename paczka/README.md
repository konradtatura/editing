# Paczka do pobrania: cały warsztat montażu Konrada

## Co tu jest
- `reklamy-studio.zip`: skill do reklam i rolek (proces, Twoje zasady z feedbacku, 9 stylów, komendy, błędy, muzyka i SFX)
  plus kod silników w `silniki/` (style 1–9, audio, face tracking, strona Video Review).
- `KONRAD_EDITING_CONTEXT.md`: to samo w jednym pliku tekstowym (zasady, style, historia, cały kod). Do wrzucenia do zwykłego czatu Claude.
- `build_paczka.py`: przebudowuje oba pliki z repo (`python3 paczka/build_paczka.py`).

Wszystkie skille są też w repo w `.claude/skills/` (m.in. `reklamy-studio`, `konrad-studio` z dashboardem Review i animacjami
HyperFrames, `yt-longform-editor`, `watch`, `hyperframes-*`). Claude Code otwarty w folderze repo widzi je sam.

## Najprościej: Claude Code na komputerze w folderze repo
```
git clone https://github.com/konradtatura/editing.git
cd editing
git checkout claude/admiring-hypatia-6xiaf6
claude
```
Plik `CLAUDE.md` i `.claude/skills/` wczytają się same. Aktualizacja później: `git pull`.

## Skille na stałe w każdym projekcie (Claude Code)
Skopiuj foldery skilli do `~/.claude/skills/`:
```
mkdir -p ~/.claude/skills && cp -R .claude/skills/* ~/.claude/skills/
```
Kod silników zostaje w repo (`projekty/`), więc do montażu i tak otwieraj Claude w folderze `editing`.

## Claude.ai / Claude Desktop (czat)
Ustawienia → Capabilities → Skills → wgraj `reklamy-studio.zip`. Do zwykłej rozmowy możesz też dołączyć `KONRAD_EDITING_CONTEXT.md`.
