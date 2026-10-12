# Planowanie animacji

## Zasada nadrzędna
Montaż wizualizuje to, co mówisz, i trzyma retencję. Nie jest filmem. Ludzie mają kupić Konrada, nie animację. Przeedytowany film męczy (szczególnie 25+) i gorzej konwertuje.

## 1. Najpierw struktura, potem efekty
Z `transcript_cut.md` wypisz mapę filmu: **hook** (pierwsze 60–90 s) → **obietnica** → **rozdziały** → **payoff / dowód** → **CTA**. Montaż wynika z tej mapy.

## 2. Urządzenie narracyjne (jedno na film)
Jeden element, który wraca i daje widzowi poczucie postępu (u Imana: dashboard poziomów, scorecard, notatnik z lekcjami).
Domyślnie: **mapa rozdziałów** (`film.device.chapters`) pokazana jako:
- T10 `agenda` po hooku (co będzie w filmie),
- T9 karta rozdziału przy każdym wejściu w rozdział (ten sam szablon, pasek postępu),
- T10 `final` przed CTA (wszystko odhaczone).
Film bez rozdziałów (np. krótkie intro, VSL) nie potrzebuje urządzenia.

## 3. Które zdania dostają animację (test zdania)
Animacja tylko, gdy zdanie: wprowadza tezę/pojęcie, ma **liczbę**, jest **dowodem**, zmienia **rozdział**, jest **obietnicą / open loopem**, wylicza **listę**, pokazuje **narzędzie / stronę**, albo następuje po długim, suchym fragmencie (odświeżenie uwagi). Wszystko inne niesie twarz, ewentualnie punch-in.

| Co mówisz | Typ |
|---|---|
| teza, kluczowe słowa, hasło | T1 akcent tekstowy |
| wyliczanka 2–4 rzeczy, narzędzia, opcje | T2 karty (stack) / T4 karty wokół głowy |
| liczba, wynik, kwota | T3 liczba obok głowy (lub T7 number przy kluczowej) |
| kroki procesu, tutorial, lista z tytułem | T5 split screen |
| konkretna strona / narzędzie / klik | T6 przeglądarka + Ty w rogu |
| zwrot narracji, mocna teza, porównanie A/B, lista bez twarzy | T7 pełny ekran |
| wejście w rozdział | T9 |
| agenda / postęp / finał | T10 |
| akcent bez grafiki, maskowanie cięcia | punch-in |

## 4. Budżet gęstości
- **Hook (pierwsze 60–90 s):** do 6–10 zdarzeń/min (zdarzenie = animacja lub punch-in).
- **Body:** 2–3 zaprojektowane animacje/min + punch-iny.
- **Twarz:** min. ~50% czasu filmu to sama twarz (z punch-inami). Pełne ekrany (T5–T10) łącznie ≤ ~25% czasu.
- **Nigdy** dwie pełnoekranowe sceny bezpośrednio po sobie — między nimi min. jedno zdanie twarzy (≥ 2 s).
- Przerwa twarzy między grafikami: albo animacje stykają się (< 0,3 s), albo przerwa ≥ 1,5 s. Przerwa 0,3–1,5 s wygląda jak mruganie — wydłuż poprzednią albo przesuń.
- Przy historii, emocjach, przekonywaniu: mniej grafik.

## 5. Timing
- Start animacji = moment, w którym pada słowo-klucz (z `words_cut.json`), nie początek zdania. Overlay może wejść 0,1–0,2 s przed słowem.
- Overlay (T1–T4): 2,5–6 s. Całe zdanie, nie pół.
- Elementy listy pojawiają się na słowie (`at` = sekundy od startu animacji).
- Pełny ekran: tyle, ile trwa myśl; twarde cięcie na początku i końcu (zero przejść).
- Split / PiP: min. 6 s (wejście i wyjście okna trwa po 0,75 s).

## 6. Punch-in
`plan.punch: [{start, end, scale}]` — statyczny zoom na całe zdanie, cięcie na granicy zdania. 1.12 dla akcentu, 1.15–1.18 dla puenty. Co drugie zdanie w długich fragmentach samej twarzy, zawsze tam, gdzie cięcie łączy dwa podejścia (maskuje jump cut). Nie pod overlayem, który stoi przy głowie (tekst wyjechałby za kadr), nie pod pełnym ekranem.

## 7. Teksty na ekranie
- 2–7 słów. Nie przepisuj zdania, wyciągnij esencję. Słowa Konrada, nie marketingowe ozdobniki.
- Jedno słowo-akcent (kolor) albo styl `weight` (light → bold).
- **Liczby tylko z transkryptu/skryptu.** Jeśli audio i skrypt/brief się różnią — oznacz w plan.md i zapytaj.
- Polskie znaki zawsze poprawne (e-booków, sprzedaż, 48 godzin).

## 8. Schemat plan.json
```json
{
  "film": {"w":1920,"h":1080,"fps":30,"surface":"light","accent":"#1F8A9A",
           "speakerBox":[740,30,1300,700],
           "device":{"kind":"map","chapters":["Rynek","Prompt","Produkt","Sprzedaż"]},
           "music":"/path/bed.mp3","musicVolume":-24,"musicCuts":[[120.5,126.0]]},
  "punch":[{"start":10.5,"end":14.8,"scale":1.12}],
  "items":[
    {"id":"01","type":"T1","start":2.10,"end":5.60,"why":"obietnica + liczba",
     "params":{"text":"Od zera do produktu w 48 godzin","accent":["48","godzin"]}}
  ]
}
```
`id` dwucyfrowe, rosnąco w czasie. `why` = jedno zdanie (wymusza test zdania). Parametry typów: `catalog.md`.

## 9. Self-check przed pokazaniem planu
1. Każda pozycja ma `why`, które przechodzi test zdania?
2. Hook gęsty, body spokojniejsze? Twarz ≥ 50%?
3. Żadne dwa pełne ekrany obok siebie? Żadnych przerw 0,3–1,5 s?
4. Ten sam layout nie powtarza się 3× z rzędu (zmieniaj T1/T2/T3/T5/T7)?
5. Liczby zgadzają się z transkryptem?
6. Urządzenie narracyjne pojawia się ≥ 3 razy (jeśli są rozdziały)?

Plan.md dla Konrada: krótko, po polsku, jedna linia na animację + na górze 2 zdania o kierunku (np. „jasna scena Apple, akcent turkusowy ze ściany, 14 animacji, 6 punch-inów”).
