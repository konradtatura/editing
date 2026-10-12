# Katalog animacji (T1–T10)

Czasy `at` / `focusAt` liczone w sekundach od startu animacji. Wszystkie teksty po polsku, krótko.

## T1 — akcent tekstowy obok głowy (overlay, .mov alfa)
```json
{"type":"T1","params":{"text":"Od zera do produktu w 48 godzin","accent":["48","godzin"],
  "style":"color|weight","zone":"auto|left|right","underline":false,"size":76,"maxLines":3}}
```
Pozycja i kolor tekstu liczone automatycznie z `speakerBox` i jasności tła. `style:"weight"` = light z pogrubionym akcentem.

## T2 — karty (overlay)
```json
{"type":"T2","params":{"layout":"stack","numbered":false,
  "items":[{"title":"Produkt cyfrowy","sub":"opcjonalnie","icon":"book","tone":"good|bad","logo":"/abs/logo.png","at":0.15}]}}
```
`stack` = kolumna obok głowy (2–4 karty). `T4` = to samo z `layout:"space"` (karty po obu stronach głowy, jak u Imana przy burzy opcji).

## T3 — liczba obok głowy (overlay)
```json
{"type":"T3","params":{"value":947,"unit":"e-booków","label":"sprzedanych w jeden dzień",
  "prefix":"","suffix":"","decimals":0,"accentNumber":true,"delta":"+38%","deltaTone":"good","variant":"bare|card"}}
```

## T5 — split screen (pełny kadr, zawiera Twoje wideo)
```json
{"type":"T5","params":{"side":"right",
  "content":{"kind":"steps|bullets|text|browser","title":"Jak to działa","accent":["działa"],
    "items":[{"title":"Wybierasz rynek","sub":"…","icon":"target","at":1.3}],
    "text":"(kind text)","url":"(kind browser)","scroll":0},
  "image":"/abs/screenshot.png (kind browser)"}}
```
Konrad zmniejsza się do zaokrąglonego okna (0,75 s), na końcu wraca do pełnego kadru. Min. 6 s.

## T6 — strona / narzędzie w przeglądarce + Ty w rogu (pełny kadr)
```json
{"type":"T6","params":{"url":"claude.ai","image":"/abs/shot.png","focus":[560,566,104,40],"focusAt":1.4,"zoom":1.6,
  "cursor":true,"speaker":true,"scroll":0}}
```
`focus` = prostokąt w pikselach zrzutu (1440 szer.), na który jest zoom + obwódka + klik kursora. Zrzut: `bash scripts/shot.sh <url> out.png` (1440×900). `speaker:false` = sama strona.

## T7 — pełny ekran
```json
{"type":"T7","params":{"variant":"statement","text":"AI zmieniło matematykę","accent":["matematykę"],"style":"color|weight","sub":"…","align":"left|center","eyebrow":"…"}}
{"type":"T7","params":{"variant":"number","value":171,"unit":"zł","label":"średnio dziennie","prefix":"","decimals":0,"accentNumber":false}}
{"type":"T7","params":{"variant":"compare","eyebrow":"Koszt startu","a":{"label":"Tradycyjnie","value":"12 000 zł","note":"…"},"b":{"label":"Z AI","value":"0 zł","note":"…","at":1.0},"winner":"b"}}
{"type":"T7","params":{"variant":"list","title":"Cały zestaw umiejętności","accent":["umiejętności"],"items":[{"title":"Research","sub":"…","icon":"(opcjonalnie)","at":1.9}]}}
```

## T9 — karta rozdziału (pełny kadr, zawsze ta sama)
```json
{"type":"T9","params":{"index":1,"title":"Gotowy prompt","accent":["prompt"],"label":"Rozdział"}}
```
Rozdziały brane z `film.device.chapters`. 2,5–3,5 s.

## T10 — mapa filmu (pełny kadr)
```json
{"type":"T10","params":{"mode":"agenda|progress|final","done":2,"title":"Plan na ten film","accent":["film"]}}
```

## Ikony (`icon`)
check, x, up, down, arrow, clock, money, user, bolt, chart, cart, mail, globe, lock, sparkle, file, book, play, star, target, rocket, brain, chat, code, calendar, gift
