# Reklamy Studio: paczka do pobrania

`reklamy-studio.zip` to cały nasz warsztat montażu reklam w jednym pliku:
- `SKILL.md`: instrukcja dla Claude'a, jak montujemy (proces, zasady, Review, eksport),
- `references/`: 4 style, Twoje zasady z feedbacku, komendy, błędy i lekcje, jak odtworzyć nowy styl z filmu-wzoru, muzyka i SFX,
- `silniki/`: kod, który robi napisy, plansze, zoomy, kompozycję i miks dźwięku (style 1–4 + audio + strona Video Review).

## Jak pobrać z GitHuba
1. Otwórz repo `konradtatura/editing` na GitHubie, przełącz branch na `claude/admiring-hypatia-6xiaf6` (albo `main` po zmergowaniu).
2. Wejdź w folder `paczka`, kliknij `reklamy-studio.zip`, a potem przycisk **Download raw** (ikona ze strzałką w dół).

## Jak użyć
- **Claude.ai (Ustawienia → Capabilities → Skills):** wgraj `reklamy-studio.zip` jako nowy skill.
- **Claude Code na komputerze:** rozpakuj do `~/.claude/skills/` (wyjdzie `~/.claude/skills/reklamy-studio/SKILL.md`).
- **W tym repo** skill już jest w `.claude/skills/reklamy-studio/`, a kod w `projekty/`, więc każda nowa sesja go widzi.

Potem wystarczy napisać np. „zmontuj ads12 w stylu 3” albo „taki styl jak w tym filmie” i wrzucić film.
