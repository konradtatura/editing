#!/usr/bin/env python3
"""Rebuild paczka/KONRAD_EDITING_CONTEXT.md and paczka/reklamy-studio.zip from the repo (run from anywhere).
Context = skill + all references + history + design docs + full engine code, one file to drop into Claude.
Zip = the reklamy-studio skill folder with the engines under silniki/ (projekty/X -> silniki/X)."""
import os, re, zipfile
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SK = os.path.join(ROOT, ".claude", "skills", "reklamy-studio")
P = os.path.join(ROOT, "paczka")
REFS = ["zasady-konrada", "style-katalog", "pipeline", "bledy-i-lekcje", "nowy-styl", "audio"]
CODE_EXT = {".py": "python", ".html": "html", ".mjs": "javascript", ".js": "javascript", ".css": "css", ".sh": "bash", ".json": "json"}
SKIP_DIRS = {"icons", "emoji_apple", "__pycache__"}
read = lambda p: open(p, encoding="utf-8").read()
demote = lambda t, n: re.sub(r"^(#+) ", lambda m: "#" * min(6, len(m.group(1)) + n) + " ", t, flags=re.M)


def files(exts):
    out = []
    for base in ("projekty", "review"):
        for d, ds, fs in os.walk(os.path.join(ROOT, base)):
            ds[:] = sorted(x for x in ds if x not in SKIP_DIRS)
            out += [os.path.join(d, f) for f in sorted(fs) if os.path.splitext(f)[1] in exts]
    return out


rel = lambda p: os.path.relpath(p, ROOT)
HEAD = ("# Konrad: kontekst montażu reklam i rolek (dla Claude Code)\n\n"
        "Wrzuć ten plik do projektu jako `CLAUDE.md` albo dołącz go jako kontekst. Zawiera cały warsztat z sesji 2026-10-12/15: proces, "
        "zasady Konrada, 9 stylów, komendy, błędy i audio. Kod silników leży w folderze `projekty/` w repo `konradtatura/editing` "
        "(albo w `silniki/` w `paczka/reklamy-studio.zip`). Odwołania do `references/*.md` poniżej to sekcje tego samego pliku.\n")
parts = [HEAD, demote(read(os.path.join(SK, "SKILL.md")), 1)]
parts += [demote(read(os.path.join(SK, "references", r + ".md")), 1) for r in REFS]
parts.append(read(os.path.join(P, "HISTORIA.md")))
parts.append("---\n\n## Załącznik A: dokumenty projektowe (breakdowny wzorów, plany)\n")
parts += [f"\n### `{rel(f)}`\n\n" + demote(read(f), 2) for f in files({".md"})]
parts.append(read(os.path.join(P, "ZALACZNIK_B.md")))
parts += [f"\n### `{rel(f)}`\n\n````{CODE_EXT[os.path.splitext(f)[1]]}\n{read(f).rstrip()}\n````\n" for f in files(set(CODE_EXT))]
ctx = "\n".join(p.rstrip() + "\n" for p in parts)
open(os.path.join(P, "KONRAD_EDITING_CONTEXT.md"), "w", encoding="utf-8").write(ctx)

with zipfile.ZipFile(os.path.join(P, "reklamy-studio.zip"), "w", zipfile.ZIP_DEFLATED) as z:
    for d, ds, fs in os.walk(SK):
        for f in fs: z.write(os.path.join(d, f), os.path.join("reklamy-studio", os.path.relpath(os.path.join(d, f), SK)))
    z.write(os.path.join(P, "README.md"), "reklamy-studio/README.md")
    z.write(os.path.join(P, "KONRAD_EDITING_CONTEXT.md"), "reklamy-studio/KONRAD_EDITING_CONTEXT.md")
    for d, ds, fs in os.walk(os.path.join(ROOT, "projekty")):
        ds[:] = [x for x in ds if x != "__pycache__"]
        for f in fs: z.write(os.path.join(d, f), os.path.join("reklamy-studio", "silniki", os.path.relpath(os.path.join(d, f), os.path.join(ROOT, "projekty"))))
    z.write(os.path.join(ROOT, "review", "video-review.html"), "reklamy-studio/silniki/video-review.html")
print(f"context {len(ctx) // 1024} KB, zip {os.path.getsize(os.path.join(P, 'reklamy-studio.zip')) // 1024} KB")
