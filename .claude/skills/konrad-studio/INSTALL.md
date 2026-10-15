# Konrad Studio — instalacja na nowym Macu (Apple Silicon)

1. Rozpakuj skill do `~/.claude/skills/konrad-studio/` (albo `git clone` z prywatnego repo).
2. Narzędzia:
   ```bash
   brew install ffmpeg node
   ```
   Python 3.13 z python.org (skrypty używają `/Library/Frameworks/Python.framework/Versions/3.13/bin/python3`), potem:
   ```bash
   /Library/Frameworks/Python.framework/Versions/3.13/bin/python3 -m pip install pillow numpy fonttools mlx-whisper
   python3 -m venv ~/.venvs/parakeet && ~/.venvs/parakeet/bin/pip install parakeet-mlx
   ```
   HyperFrames (animacje): `npx --yes hyperframes@0.8.143 doctor` (pobiera się samo przy pierwszym renderze).
3. Czcionki Inter: `assets/fonts` i `templates/*/fonts` są w skillu (do Tesseracta zainstaluj Inter/Geist w systemie).
4. Efekty dźwiękowe są w skillu (`assets/sfx`, `assets/sfx_pixabay`). Opcjonalnie MCP vidIQ do muzyki.
5. Test: `python3 scripts/preflight.py /tmp/test some.mp4` i `python3 review/review.py PROJ` → http://127.0.0.1:8765.
Pamięć (styl, feedback) jest w `references/feedback.md` i `references/*.md` — przenosi się razem ze skillem.
