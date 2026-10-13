# Błędy i lekcje (sprawdź przed oddaniem)

## Checklista QA (każda reklama, każda wersja)
- [ ] Zoom zmienia się tylko na cięciu: para klatek przed/po każdym cięciu.
- [ ] Plansze zaczynają się i kończą na cięciu, twardo, bez fade i bez mignięcia twarzy.
- [ ] Nic nie zasłania ust (napisy, ikony, karty, listy). CTA na ujęciu 100%.
- [ ] Napisy na jednej wysokości. Nie zderzają się z trackerem, listami ani CTA.
- [ ] Żadna plansza nie startuje pusta: jest nagłówek albo pierwszy element od pierwszej klatki.
- [ ] Akcenty: boxy nie nachodzą na siebie, kursywa nie wchodzi w linię wyżej, słowo-akcent widoczne wystarczająco długo.
- [ ] Liczby i fakty: 941, 17 zł, +79 zł w powiadomieniu, 48 h. Bez zmyślonych wyników.
- [ ] Napis nie wraca po planszy z treścią, która na niej padła.
- [ ] Ostatnia klatka: CTA ze strzałką, nic ucięte.
- [ ] Rozmiar FINAL < 30 MB, długość = oryginał, dźwięk zsynchronizowany.

## Błędy techniczne, które już były
| Objaw | Przyczyna | Naprawa |
|---|---|---|
| Cień pod gradientem „nie działa” | `appear()` ustawia `element.style.filter` (blur→none) i kasuje CSS `filter: drop-shadow` | cień na osobnym elemencie-wrapperze (`.bs`) |
| Gradient „dziwny” przy 2 liniach | gradient na całym bloku, więc każda linia ma inny kolor | inline span + `box-decoration-break: clone` |
| Biała obwódka gradientu robi kreski w literach | `-webkit-text-stroke` przy ujemnym letter-spacing rysuje kontury nachodzących glifów | bez strokea, tylko cień |
| Stary zoom kilka klatek po cięciu | detektor nie złapał cięcia | `extra_cuts`, porównaj liczbę cięć z Konradem |
| Dwa niebieskie boxy nachodzą | każde słowo `h==1` osobnym spanem | sąsiednie słowa h=1 w jeden box |
| Napisy skaczą góra/dół | centrowanie bloku o zmiennej liczbie linii | stała górna krawędź (`top = capY*H`) |
| compose2: NoneType terminate | dekoder b-rolla zamknięty dwa razy | `bdec[k] = False` po terminate i `if not bdec[k]: continue` |
| Wideo w karcie nie gra | `<img>` w Playwright | sekwencja JPG 30 fps, `seek()` podmienia `src` i zwraca Promise z `decode()` |
| PNG bez alfy psuje kompozycję | screenshot bez `omitBackground` | traktuj jako nieprzezroczyste / zawsze `omitBackground: true` |
| cut.py OOM | jeden filter_complex na wszystkie segmenty | enkoduj segmenty osobno + concat |
| Fade audio w złym miejscu | `-ss` na wejściu przesuwa czasy filtrów | trim/atrim w filtrze |
| Enkod uszkodzony („moov atom not found”) | enkodowanie pliku, który się jeszcze komponował | czekaj na „wrote”/ALLDONE |
| Pętla czekania nie kończy się | `pgrep -f` łapie własną komendę | czekaj na plik wynikowy / marker w logu |
| Napis wisi na granicy hooków | blok napisów przechodzi przez cięcie sceny | przytnij t0/t1 bloków do cięć hooków |

## Lekcje z feedbacku
- Konrad patrzy na telefonie: czytelność > subtelność. Cienie mocniej, niż wydaje się potrzebne.
- „Dalej niewidoczne” zwykle oznacza bug, a nie za słabe wartości. Najpierw sprawdź, czy efekt w ogóle się renderuje (pojedyncza klatka, crop 1:1).
- Jedna klatka do akceptacji przed pełnym renderem oszczędza 20 minut.
- Po każdym przesunięciu jednego elementu sprawdź, w co teraz wchodzi (napisy niżej → zderzenie z trackerem).
