# Studio Clean — wygląd i ruch

Struktura i rytm Imana Gadzhiego (2024–2025), wygląd Apple: dużo powietrza, jedna myśl na kadr, jeden akcent, płynny ruch z hamowaniem. Wszystko budowane w kodzie (bez generowanych ilustracji i postaci).

## Powierzchnia (film.surface)
- **light** — biel `#FFFFFF` / `#F5F5F7`, tekst `#1D1D1F`, szarość `#6E6E73`, białe karty z miękkim cieniem. Dla jasnych wnętrz (jak pokój Konrada).
- **dark** — `#0A0A0C`, tekst `#F5F5F7`, karty z ciemnego szkła (blur, 1 px jasna krawędź). Dla ciemnego, nastrojowego studia (klimat Imana).
- Tło pełnych ekranów: płaska powierzchnia + dwie ledwo widoczne poświaty (akcent w lewym górnym rogu).

## Kolor
- Jeden akcent na film, wzięty z nagrania (60% ciemny / 30% jasny / 10% akcent — zasada Imana). Domyślnie `#0A84FF`.
- Semantyczne tylko do danych: zysk `#30D158`/`#34C759`, strata `#FF453A`/`#FF3B30`, uwaga `#FF9F0A`.
- Max jeden akcent w kadrze.

## Typografia
- **Geist** (600 nagłówki, ciasno -0.03…-0.05em; 500 UI; 300 do stylu light→bold). **Geist Mono** do liczb porządkowych i oznaczeń rozdziałów.
- Skala 1080p: pełny ekran 120–140 px, liczby 150–260 px, akcent obok głowy 60–76 px, karty 48/30 px.
- Tekst na nagraniu: kolor dobierany automatycznie do jasności tła (ciemny na jasnej ścianie, biały z cieniem na ciemnym).

## Ruch (stałe w `templates/_base/studio.js`)
- Wejścia: `expo.out` 0,55–0,7 s; słowa po kolei co 0,07 s (podniesienie 16 px + fade + rozmycie 8→0 — sygnatura Imana).
- Karty: scale 0,94→1, podniesienie 26 px, rozmycie 10→0; elementy listy co 0,14 s albo na słowie.
- Wyjścia overlayów: 0,32 s (szybsze niż wejście), lekkie uniesienie i rozmycie.
- Ruchy układu (okno z Konradem, zoom strony): `expo.inOut` 0,75 s.
- Liczby się toczą (`power3.out` ~1,1–1,4 s), cyfry tabelaryczne.
- Bez sprężyn i podskoków na tekście. Pełne ekrany: twarde cięcie na wejściu i wyjściu.
- Każda grafika ma dźwięk (sound.md).

## Elementy
- Okno przeglądarki macOS (kropki, pasek URL, radius 18) dla stron i narzędzi — strony nigdy „gołe” na pełnym ekranie.
- Okno z Konradem: zaokrąglony portret (split) albo róg 16:9 (PiP), wraca płynnie do pełnego kadru.
- Ikony liniowe w stylu SF Symbols (lista w studio.js `S.icon`).

## Zakazy (z feedbacku Konrada i z researchu)
- Ozdobne etykiety mono, belki, chipy, napisy bez treści.
- Pastelowe bloby, neony, glitch, gradienty zmieniające barwę, emoji.
- Ten sam layout scena po scenie.
- Generowane ilustracje/postacie zamiast prostej grafiki w kodzie.
- Tekst na twarzy; przezroczyste karty na twarzy.
- Animacja, która nie ma informacji („bo fajnie wygląda”).
- Ucięcie animacji w połowie ruchu (zawsze hold ≥ 1 s przed wyjściem).
