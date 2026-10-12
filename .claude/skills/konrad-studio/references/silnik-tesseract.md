# Silnik: Tesseract + `scripts/apple.py`

Animacje są edytowalnymi projektami Tesseract (`.tsrct`) generowanymi skryptem Pythona.
- CLI: `~/Library/Application Support/Tesseract/bin/tsrct` (stała `apple.TSRCT`).
  Uwaga: `tesseract` w PATH to OCR, nie to narzędzie.
- Ogólna dokumentacja schematu: skille `tesseract-motion` i `tesseract-video`.
  Tu jest tylko to, czego używamy i co sprawdziło się w praktyce.

## Szkielet pliku scen

```python
import sys, os
sys.path.insert(0, os.path.expanduser("~/.claude/skills/konrad-studio/scripts"))
import apple
HERE = os.path.dirname(os.path.abspath(__file__))
apple.init(HERE, 1920, 1080)          # 9:16 → apple.init(HERE, 1080, 1920); ZAWSZE przed `from apple import *`
from apple import *

SRC = os.path.join(HERE, "..", "film.mp4")          # film, na którym leżą sceny (zmontowany)
WORDS = os.path.join(HERE, "tr", "words.json")      # transcribe.py tego samego pliku
OVERLAY = set()                                     # klucze scen eksportowanych jako nakładki (alfa)

def new(name, a, b): return Scene(name, a, b, WORDS, SRC)

def S01():                       # jedna funkcja = jedna scena, nazwa "S01_Etykieta" trafia do nazwy pliku
    sc = new("S01_Wynik", 12.40, 17.80)          # in/out w sekundach filmu
    sc.apple_bg()                                # pełny ekran: biel + poświaty
    w = sc.word                                  # w(13.02) → czas lokalny (ms) słowa; assert ±0,05 s
    ...
    return sc
OVERLAY.add("S02")
def S02():
    sc = new("S02_Karta", 20.0, 26.5)
    FX = overlay(sc)                             # nagranie pod spodem + grupa 100 = wszystko, co idzie do alfy
    ...
BUILD = {k: v for k, v in globals().items() if k[:1] == "S" and k[1:].isdigit()}
if __name__ == "__main__":
    for k in sys.argv[1:] or sorted(BUILD): BUILD[k]().build()
```

Uruchomienie: `$PY scenes.py S01 S02`, potem `preview.py`, potem `export.py` (zob. SKILL.md).

## API `Scene` (czasy w ms lokalnych sceny; `sc.t(sek_filmu)`, `sc.word(sek_filmu)`)

| Metoda | Co robi |
|---|---|
| `group(lid, name, parent, x, y, ax, ay, op, sc)` | grupa (transform dla dzieci); anchor (ax, ay) = punkt skalowania |
| `rect(lid, name, parent, x, y, w, h, fill, r, stroke=(col, w), op)` | prostokąt (r = zaokrąglenie) |
| `text(lid, name, parent, x, y, txt, size, color, style, family, tracking, just, op, animators)` | tekst Geist; y = linia bazowa |
| `mono(...)` | tekst Geist Mono |
| `path(lid, name, parent, pts, x, y, fill, stroke, closed, trim)` | ścieżka z punktów (ikony, ✓, strzałki) |
| `ring(lid, name, parent, cx, cy, d, color, width, trim_end)` | pierścień (postęp: `trimEnd`) |
| `shadow(lid, alpha, blur, oy)` / `blur(lid, eid, amount)` / `matte(lid, matte_lid)` | efekty, maska (track matte) |
| `k(lid, prop, [(t, value, easing), ...])` | klatki kluczowe właściwości |
| `kpos(lid, [(t, x, y, easing)])` | pozycja |
| `kstyle(lid, itemId, prop, keys)` | animacja selektora animatora tekstu |
| `reveal_animator(aid, sel)` + `reveal_words(lid, sel, [czasy])` | słowa wchodzą po kolei (blur + uniesienie) |
| `color_animator(aid, sel, color, w0, w1)` | słowa w0..w1 w kolorze akcentu |
| `roll_keys(t0, t1, fmt, v0, v1)` | toczony licznik (klucze `textContent`, HOLD) |
| `apple_bg()` / `footage()` / `build()` | tło / nagranie pod sceną / zapis projektu z kontrolami |

**Właściwości do `k()`:** `opacity`, `scaleX`, `scaleY`, `positionX`, `positionY`, `rotation`, `rotationY`, `fillColor` (col),
`strokeColor`, `rectSize` (v2), `rectRoundness`, `trimEnd`, `textContent` (s, z `HOLD`).

**Wartości:** `f(x)`, `v2(x, y)`, `s("tekst")`, `col(A_BLUE)`.

**Easing:** `APPLE` (wejścia), `OUT` (expo-out), `SOFT` (fade), `INOUT`, `EIN` (przyspieszenie), `HOLD` (skok), `LIN`.

**Helpery modułu:**
- `fade(sc, lid, t_in, t_out)`, `pop(sc, lid, t)`, `scale_keys`,
- `card_bg(sc, lid, parent, x, y, w, h, r, sh)`, `card_in(sc, g, t_in, t_out)`,
- `pill_text(sc, base, ...)` (zajmuje id base i base+1), `ok_badge` (base..base+2),
- `check`, `cursor(sc, lid, parent, x, y)` (lid, lid+1), `toggle(sc, base, parent, x, y, t_on)` (base, base+1),
- `blob`, `arc`, `adv(text, size, style)` (szerokość tekstu Geist), `madv` (mono), `zl(v)` („5 130 zł”),
- `overlay(sc)`.

## Nowe narzędzia (2026-10-03)

| Funkcja | Do czego |
|---|---|
| `sc.image(lid, name, path, x, y, w, h, r, op)` | prawdziwy obraz (ikona, screen, zdjęcie). Warstwa dokumentu, więc nie jest dzieckiem grupy; animuj ją przez `k()` na jej `lid` |
| `sc.lower(gid)` | wyślij grupę lub kartę w tył (nad nagranie lub tło), żeby obrazy były na niej |
| `sc.motion_blur(lid)` | prawdziwe rozmycie ruchu (najazdy, karty w locie) |
| `curve(sc, lid, parent, (x0,y0), (x1,y1), t, dur, color, width)` | łuk S rysowany od t (`trimEnd`) |
| `highlight(sc, lid, parent, x, y, w, h, t)` | zakreślacz od lewej (twórz PRZED tekstem) |
| `push_in(sc, gid, t0, t1, s0, s1)` | najazd kamery na grupę; grupa musi mieć pozycję = kotwica (`group(id, n, None, 960, 540, 960, 540)`) |
| `type_keys(t0, text, cps)` | klucze `textContent` dla pisania z kursorem |
| `flap_keys(t0, t1, "130 000")` | licznik-klapki dla dużych kwot |
| `LEAD` = 100 ms | wejście przed słowem: `w(t) - LEAD` |
| font `Studio Serif` (style `Regular`) | kursywa szeryfowa (New York Italic przerobiony na statyczny); bez „—” |

## Pułapki (każda kosztowała poprawkę)

- **Fonty:** `fontFamily="Geist"` + `fontStyle="SemiBold"` (typograficzne nazwy). Inaczej renderer po cichu daje Regular.
  Regular musi być zaimportowany (biblioteka importuje z `assets/fonts`). Nie ma GeistMono-Light.
- **Brak glifów** ©, ★, ⌘, ✓ w Geist: dają `missing_fonts` albo AppleColorEmoji. Rysuj je ścieżkami.
- **Unikalne `layerId` w scenie.** `build()` przerywa przy duplikacie. Helpery zajmują kilka kolejnych id
  (np. `pill_text` = base, base+1), więc rezerwuj bloki id (110–119 karta, 120–129 wiersze…).
- **Klatki kluczowe:**
  - na tej samej ścieżce czasy muszą rosnąć i nie mogą się powtarzać (`build()` sprawdza),
  - typowy błąd to `fade()` i własne `opacity` na tej samej warstwie albo dwa klucze w t=0,
  - używaj jednej funkcji na właściwość warstwy.
- **ID animatorów to liczby całkowite:** `reveal_animator(1, 11)`.
- **Nie nazywaj zmiennej `IN`** (kiedyś przesłaniała easing). Easing wejścia to `EIN`.
- **Karty nad nagraniem:** `fill=A_BG` (100%). Półprzezroczyste przebijają.
- **Pisanie i kasowanie tekstu** (`textContent`) przy nakładających się fazach daje nieposortowane klucze.
  Kasuj szybciej (9 ms/znak) albo rozdziel fazy w czasie.
- **Puste otwarcie:** jeśli treść wchodzi po 0,5 s, przesuń in-point sceny. Nagranie (nakładka) albo poprzednia scena mają grać do tego czasu.
- **`sc.word(t)` rzuca assert,** gdy w ±0,05 s nie ma początku słowa. Sprawdź `words.txt` albo json i podaj dokładny czas.
- **Nakładki:** wszystko pod grupą 100 (`overlay(sc)`), eksport `--fx-solo main:100` daje alfę samej grafiki.
- **Sceny pionowe:** `apple.init(…, 1080, 1920)` przed `from apple import *`, bo inaczej W i H zostają 16:9.
- **Shader „light sweep” przez text matte** nie renderuje się w tsrct 0.2.0. Nie używaj.

## Podgląd i render

- `tsrct preview --project P --time SEK --output x.png`, opakowane w `preview.py` (arkusz).
- `tsrct export --project P --output x.mp4`: obraz z dźwiękiem oryginału (biblioteka importuje wycinek audio, a przy nakładce nagranie).
- `tsrct export … --format prores --fx-solo main:100 --output x.mov`: ProRes 4444 z alfą, bez dźwięku. Gdy Konrad potrzebuje audio do synchronizacji (np. pigułki timera), dograj wycinek przez ffmpeg: `-map 0:v -map 1:a -c:v copy`.
