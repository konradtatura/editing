# Apple style: wygląd i ruch

Jedno zdanie: **wygląda jak ekran z iPhone'a albo slajd z keynote'u Apple, a nie jak „montaż z YouTube'a”.**

## Zasady

- **Jedna myśl na kadr.** Pokazujesz dokładnie to, co pada w tej sekundzie.
- **Pokazuj, nie pisz.** Zamiast napisu „dużo powiadomień” pokazujesz ekran blokady, na który spadają powiadomienia.
- **Biało, dużo powietrza, jeden bohater.**
- **Czysto, ale z charakterem:** pomysł ma być mocny, zabawny albo zaskakujący.

**Wzory:**
- interfejs iOS i macOS (powiadomienia, alerty, Dynamic Island, Kalendarz, Portfel, Mapy, Zegar, Czas przed ekranem, Spotlight, Finder, Skróty, AirDrop),
- apple.com: wielkie ciasne nagłówki, jedno słowo w kolorze, liczba jako bohater, „Tech Specs”,
- filmy z keynote'ów,
- premiery Linear, Stripe, Vercel i Arc.

**Unikaj jako wzoru:** lower thirds z YouTube'a, neonów, tęczowych gradientów, glitchy, emoji, sprężynujących napisów.
**Unikaj też pastelowych „blobów” jako treści.** Konrad nazwał to tanim wyglądem; poświaty w tle mają być ledwo widoczne.

## Tło

- Biel `#FFFFFF` plus dwie bardzo miękkie, rozmyte poświaty:
  - ciepła brzoskwiniowa z lewej u góry (`[1,0.90,0.85,0.30]`),
  - chłodna niebieskawa z prawej u dołu (`[0.90,0.93,1,0.22]`),
  - blur 320.
  - W kodzie: `sc.apple_bg()`, w pionie `vbg(sc)`.
- Wyjątkowo, dla kontrastu, ciemna scena „nocna” (ekran blokady o 2:00, licznik 941) albo jedna czarna plansza na materiał.

## Paleta (tylko te kolory; najwyżej jeden akcent na kadr)

| Token | Hex | Do czego |
|---|---|---|
| `A_INK` | #1D1D1F | tekst |
| `A_GREY` | #86868B | tekst drugiego planu, etykiety |
| `A_LINE` | #E5E5EA | linie, puste stany, wyłączony przełącznik |
| `A_FILL` | #F5F5F7 | pigułki, kafle |
| `A_BLUE` | #0071E3 | akcent, interakcja, „to jest ważne” |
| `A_GREEN` | #34C759 | sukces, zysk, ✓ |
| `A_RED` | #FF3B30 | błąd, strata, skreślenie |
| `A_ORANGE` | #FF9500 | uwaga, presja czasu |

## Typografia

- Nagłówki: Geist SemiBold, duże, ciasne (tracking od −20 do −50), jedno słowo akcentu na niebiesko (`color_animator`).
- Podpisy: Geist Medium, szare.
- Liczby, timery, metadane: Geist Mono, bo wyglądają jak z interfejsu.
- Na kadr maksymalnie kilka słów.
- Minimalne rozmiary, żeby było czytelne na telefonie:
  - 16:9: tekst ≥ 34 px, nagłówek 64–130 px,
  - 9:16: tekst ≥ 34 px przy szerokości 1080, nagłówek 58–110 px.

## Elementy

- **Białe karty:** 100% krycia, zaokrąglenie 28–48 px, bardzo miękki cień (alpha 0,14–0,22, blur 50–70, offset y 16–24).
- **Ikony:** cienka kreska w stylu SF Symbols, rysowane ścieżkami.
- **Bez ozdobników:** zero ramek, obrysów i dekoracyjnych etykiet.
- **Gotowe elementy w bibliotece:** przełącznik iOS (`toggle`), kursor macOS (`cursor`), ✓ (`check`, `ok_badge`),
  pigułka (`pill_text`), pierścień (`ring`), telefon (`phone()` w przykładzie VSL).

## Ruch

- **Wejście:** fade 200–300 ms i uniesienie o 20–60 px albo skala 92–96 → 100%, krzywa expo-out (`OUT`) lub Apple (`APPLE`), 500–700 ms.
- **Wyjście:** miękkie, 220–300 ms (`SOFT`), nigdy ucięte w połowie ruchu.
- **Bez sprężyn i overshootu.** Najwyżej delikatne „puknięcie” przy wciśnięciu.
- **Rzeczy żyją:** liczby się toczą (`roll_keys`), kursor jedzie i klika, wskaźnik pulsuje, powiadomienia się piętrzą.
- **Słowa pojawiają się na słowie** (`reveal_animator` i `reveal_words`: blur, opacity i uniesienie po słowie).
- **Detale z iOS:**
  - potrząśnięcie jak przy złym PIN-ie („nie”, „fałsz”),
  - przesunięcie wiersza w bok („odrzucam”),
  - rozwinięcie jak Dynamic Island,
  - matowe szkło jak blur („nie widzisz”).
- **Cięcia** między kamerą a pełnym ekranem są twarde, bez „wipe” i bez rozmytych przejść.

## Warstwa premium (z referencji 2026-10-03, zob. `referencje.md`)

To podnosi „czysty Apple” do poziomu filmów, które Konrad przysłał jako wzór. Używaj z wyczuciem, 1–2 rzeczy na scenę.
- **Łuki zamiast linii:** `curve()` rysuje S-krzywą na słowie od ikony do etykiet (pigułki A_INK z białym tekstem).
- **Głębia:**
  - delikatny najazd kamery na całą scenę (`push_in` 3–6%) albo szybki najazd na detal (0,6 s, do 140–160%),
  - `motion_blur()` na ruchomej grupie,
  - duży rozmyty kształt na pierwszym planie w rogu (blob z blurem 60–120, ciemniejszy od tła).
- **Jedno słowo kursywą szeryfową** (`family="Studio Serif"`, style Regular) obok bezszeryfowego nagłówka, np. „Ciężka praca / *nie* czyni Cię bogatym”.
  Najwyżej raz na scenę. W Studio Serif nie ma „—”.
- **Tekst na ścianie obok głowy** (16:9): biały lub ciemny, zależnie od tła, z miękkim cieniem, bez karty, pisany po słowie.
  Głowa zostaje czysta.
- **Pisany tytuł rozdziału:** pigułka, w której tekst pisze się na żywo (`type_keys`), jedno słowo w kolorze akcentu.
- **Prawdziwa strona:** okno Safari z prawdziwą stroną (`image()` ze screenem Konrada albo odtworzona),
  najazd, zakreślacz `highlight()` na słowie, kursor na końcu.
- **Karty 3D:** lekkie przechylenie (`rotationY` 8–15°) przy lądowaniu, numer w kółku, ikona Fluent 3D.
- **Prawdziwe ikony** (`fetch_icon.py app|fluent`) zamiast rysowanych. Kraje z GeoJSON.
- **Duże kwoty:** licznik-klapki `flap_keys` (cyfry kręcą się i blokują od lewej, ostatnia na słowie).

## Biblioteka metafor (sprawdzone; inspiracja, nie kopiuj 1:1)

| Myśl | Metafora |
|---|---|
| leży na dysku, nic nie robi | pusty pulpit Maca z jednym plikiem, kamera odjeżdża |
| zasypują cię wiadomości, nocą | ciemny ekran blokady, 2:00, spadają powiadomienia |
| nie widzi, co jest w środku | produkt za matowym szkłem |
| dzień klienta | widok dnia w Kalendarzu iOS |
| kopiuj-wklej | wielkie klawisze ⌘C ⌘V wciskane w rytm słów |
| scrolluję zamiast pracować | Czas przed ekranem, słupki rosną |
| czekam w kolejce | „Następne” jak w Apple Music |
| prawdziwy wybór | systemowy alert z dwoma przyciskami |
| za darmo, sponsor | paragon, suma zjeżdża do 0,00 zł, pieczątka OPŁACONE |
| podróż | karta pokładowa w Portfelu (Polska → USA) |
| nie ma ruchu | „Teraz na stronie: 0” |
| najlepsze, ale nikt nie wie | domek w środku lasu |
| ile to kosztuje | pokrętło budżetu, monety spadające w dni tygodnia |
| skala | słupek obok słupka, który wychodzi poza kadr |
| ukryty wynik | rozmyte, kręcące się cyfry, odsłaniane etapami |
| nie, fałsz | trzęsie się jak zły PIN i robi się czerwone |
| mało czasu | minutnik iOS, Dynamic Island z czerwonymi cyframi |
| masz biznes (pusty → pełny) | ekran główny iPhone'a: „?” → widżety Produkt, Strona, Sprzedaż → powiadomienie „+57 zł” |
| umiejętności, których nie masz | Ustawienia: przełączniki wyłączone, jeden produkt włącza wszystkie |
| AI jak lepszy Google | pasek wyszukiwania, w który wpisuje się banalna prośba |
| zamykasz i nic nie zostaje | czat zamyka się (⌘W), zostają liczniki Produkty 0 / Oferty 0 |
| 5 umiejętności → AI | Dock z 5 ikonami, które zlewają się w jedną |
| droga długa vs szybka | Mapy: szara trasa 6–12 miesięcy vs niebieska 48 h |
| premiera produktu | ikona aplikacji ląduje, nazwa obok (pełny ekran) |
| kurs vs jeden cel | playlista 248 lekcji skreślona, zostaje jeden checkbox |
| proces krok po kroku | pipeline jak w Skrótach: Prompt → Produkt → Strona → Marketing |
| „co mam teraz zrobić?” | pytanie zamienia się w przycisk „Następny krok →” |
| jeden produkt, wielu kupujących | AirDrop: kopie pliku lecą do ludzi |
| rachunek | Kalkulator iOS 57 × 3 = 171 |
| miesiąc przychodu | kalendarz 30 dni, każdy dzień +171, suma toczy się do 5 130 zł |
| utknąłeś | pasek postępu staje na 82%, kółko macOS, „Dokończę później” |
| wsparcie (kilka rzeczy) | przełącznik aplikacji z kartami: 1:1, live, czat, społeczność |
| pomoc coacha | wątek czatu: utknąłem → screenshot → „Zrób to tak” → Rozwiązane |
| bonus budżetu | przełącznik Reklamy włącza się, karta w Portfelu 800 zł |
| gwarancja | pieczęć „48 h Gwarancja”, warunki, „100% zwrotu” |
| dwie przyszłości | „Zapisane na później” przesuwa się w „Własny biznes” |
| CTA | przycisk, kursor klika, przycisk wciska się o kilka px |
| finał | „AI + Ty = coś swojego.” (wielki typ, jedno słowo na niebiesko) |
| wszyscy używają tak samo (9:16) | dymki czatu ze zwykłymi prośbami na karcie |
| konsument vs twórca | pytanie na pełnym ekranie, odpowiedź „nic”, pieczątka KONSUMENT |
| dla zwykłych ludzi | siatka kropek-ludzi zapalająca się |
| „zapytaj” | pole tekstowe: pisanie, kasowanie, przepisywanie (kasowanie 9 ms/znak) |

**Jak wymyślić nową metaforę:** zapytaj, gdzie na iPhonie albo Macu widz już widział tę sytuację. Tego elementu użyj.

## Tak / Nie

**Tak:** biel i powietrze, jeden bohater, natywne UI jako metafora, prawdziwe liczby i słowa z nagrania,
ruch na słowie, humor w detalu.

**Nie:**
- dużo tekstu, podpisy „dla ozdoby”, belki, chipy i etykiety bez treści, mono-metadane jako dekoracja,
- ten sam szablon scena po scenie,
- półprzezroczyste karty na twarzy,
- neony, gradienty, glitch, emoji, sprężyny,
- wymyślone dane podane jak fakty.
