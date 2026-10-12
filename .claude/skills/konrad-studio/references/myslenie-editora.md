# Jak myśli montażysta (uniwersalnie, dla każdego formatu)

Montaż ma pomagać oglądać, a nie być pokazem efektów. Zanim cokolwiek zbudujesz, przejdź przez cztery pytania.

## 1. Po co ta sekunda istnieje?

Każda animacja musi spełniać co najmniej jedną z trzech funkcji, inaczej wylatuje:
- **Wyjaśnia:** widz szybciej łapie liczbę, proces albo porównanie.
- **Budzi ciekawość:** otwarta pętla, ukryty wynik, „co dalej?”.
- **Bawi:** wizualny żart w detalu (Night Shift, gdy zakłada czerwone okulary; sernik limonkowy jako pinezka w Mapach).

Przy każdym zdaniu skryptu pytaj: czy twarz plus głos wystarczą? Jeśli tak, nie animuj. Konrad sprzedaje twarzą.

## 2. Kiedy animować (sygnały w transkrypcie)

Animuj, gdy pada:
- **Liczba lub wynik:** 941, 57 zł × 3, 5130 zł, 800 zł, 48 h, 100%.
- **Proces lub kroki:** „najpierw…, potem…, a później…”.
- **Porównanie, przeciwieństwo albo zmiana stanu:** kiedyś/dziś, kurs/jeden cel, e-book/biznes, koszt/inwestycja.
- **Nazwa rzeczy, którą widz może zobaczyć:** strona, prompt, reklama, kalendarz, koszyk.
- **Obietnica, gwarancja, oferta, CTA:** zawsze dostają najczystszy kadr.
- **Puenta albo pattern interrupt:** jedna czarna plansza na materiał („Nie jesteś.”).

Nie animuj:
- przejść, wtrąceń i ogólników („I teraz zobacz…”, „bo widzisz”),
- momentów emocji, gdzie twarz robi robotę.

## 3. Jak znaleźć metaforę (serce stylu)

1. **Gdzie widz już widział tę sytuację na iPhonie albo Macu?** Wybierz ten element UI. Przykłady:
   - zasypują cię wiadomości → ekran blokady o 2:00,
   - utknąłeś → pasek staje na 82% i kręci się kółko,
   - jeden plik sprzedany wielu ludziom → AirDrop,
   - koszt reklamy → karta w Portfelu,
   - wybór → systemowy alert z dwoma przyciskami.
2. Jeśli nie ma UI, sięgnij po **fizyczny obiekt w stylu Apple**: paragon, karta pokładowa, pieczęć, moneta, klawisz ⌘C, minutnik.
3. Jeśli to liczba, **liczba jest bohaterem**: wielka, toczy się, kontrastuje skalą (mały słupek obok słupka, który wychodzi poza kadr).
4. Sprawdź, czy ta metafora nie była już w tym filmie. Jeśli była, wymyśl inną albo zrób z niej **celowy callback**.
5. Dodaj jeden detal, który żyje: kursor klika, przełącznik się przestawia, licznik się toczy, coś się trzęsie jak przy złym PIN-ie.

## 4. Rytm, gęstość, czas

- **Synchronizacja co do słowa.** Każde wejście, zmiana liczby czy kliknięcie wypada na słowie z transkrypcji (`sc.word(t)` pilnuje ±0,05 s).
- **Coś się zmienia co 1–2 s.** Zasada z motion-video-kit: żaden kadr nie stoi bez ruchu dłużej niż ok. 0,6 s, chyba że to celowy oddech po puencie.
- **Scena trwa całe zdanie,** nie pół: wejście, beaty na słowach, przytrzymanie ≥ 1 s, miękkie wyjście.
  Sąsiednie beaty tej samej myśli łącz w jedną scenę, która się przekształca.
- **Bohater zajmuje 60–85% swojej strefy** (pełny ekran: kadru, karta: karty). Za mały element wygląda tanio.
- **Gęstość:**
  - longform: animacja co 20–40 s plus wszystkie liczby i kroki,
  - VSL: co 4–8 s, ale około 2/3 to karty obok twarzy,
  - reklama 9:16 (90 s): około 12 kart i 3 pełne ekrany,
  - rolka: 0–3 elementy.

## 5. Retencja: techniki, które zadziałały

- **Otwarte pętle:**
  - rozmyte wyniki w hooku, odsłaniane etapami na końcu (przychód, potem zysk, potem sprzedaże),
  - ukryty timer (rozmyte, kręcące się cyfry),
  - „Część 2?”.
- **Callbacki:** element z początku wraca z prawdziwymi danymi:
  - pusta karta wyników zostaje wypełniona,
  - lejek ze schematu wraca z liczbami,
  - minutnik z intro dzwoni na końcu,
  - paragon z CTA wraca skrócony.
- **Kontrast skali:** mały vs ogromny, „−7 min” jako kropka vs wielkie koło.
- **Pattern interrupt:** jedna czarna plansza, humor w detalu.
- **Szczerość buduje zaufanie:** przypis „¹ Wynik jednego testu, nie obietnica”.
- **Pierwsze 2 sekundy (krótka forma):** najmocniejszy wizual na start, czyli wynik, liczba albo zaskakujący UI.

## 5b. Zasady z najlepszych montaży (referencje 2026-10-03)

- **Wejście tuż przed słowem.** Element ma być już na ekranie, kiedy pada słowo: wejście 0,1 s przed słowem (`w(t) - LEAD`),
  a uderzenia i kliknięcia 0,05 s przed.
- **Bohater wcześnie.** Kluczowy element sceny wchodzi na początku zdania, a kolejne etapy na kolejnych słowach.
  Nigdy pół karty pustej przez 2 s.
- **Odsłona na słowie PRZED puentą.** Puenta jest już widoczna, gdy pada słowo-puenta, które dodaje tylko puknięcie.
- **Tajemnica do momentu nazwy.** Gdy pada nazwa produktu („Cyfrowy Autopilot”), wcześniej pokazuj „?” albo sylwetkę,
  a na nazwie zrób odsłonę. Potem używaj prawdziwego znaku.
- **Dosłowne obiekty dla dosłownych słów:**
  - „w telefonie” → telefon,
  - „na komputerze” → MacBook,
  - „szybciej” → wyścig albo licznik,
  - „kraj” → prawdziwy kontur z GeoJSON (Polska → USA),
  - „strona” → prawdziwa strona,
  - „kwota” → licznik.
- **Prawdziwa strona jako dowód:** okno przeglądarki z prawdziwą stroną (odtworzoną albo screen Konrada),
  najazd kamery na konkretny wiersz, zakreślacz na słowie, kursor na końcu zakreślacza.
- **Memy (propozycja, nie default):** 1–3 na film, tylko na „linie emocji” („jeśli jesteś jak ja…”, „i bum”).
  Nigdy na liczbach i dowodach. Zawsze zapytaj Konrada, czy chce memy w danym filmie.
- **Fact-check przed rysowaniem.** Nazwy, liczby i twierdzenia sprawdzasz, zanim narysujesz.
  Gdy nagranie mówi coś innego niż prawda, głos zostaje, ekran pokazuje prawdę, a w raporcie zgłaszasz to na pierwszym miejscu.

## 6. Autotest planu (przed wysłaniem listy)

- [ ] Każda pozycja ma funkcję (wyjaśnia, ciekawość, humor) i metaforę, a nie „tekst na ekranie”.
- [ ] Żadne dwie sąsiednie sceny nie mają tego samego układu.
- [ ] Twarz jest widoczna przez większość czasu; pełne ekrany tylko tam, gdzie zasłużone.
- [ ] Każda liczba pochodzi z nagrania, a przykładowe dane są oznaczone.
- [ ] ⭐ przy 3–6 scenach najważniejszych dla retencji (hook, wynik, oferta, gwarancja, CTA).
- [ ] Longform: wypisz zdarzenia chronologicznie (zmiana trybu, punch-in, nowa scena, element w scenie)
      i sprawdź, czy żadna przerwa nie przekracza ~5 s. Żaden tryb nie trwa ciągiem > 10 s.

## 7. Autotest każdej sceny (na arkuszu klatek)

1. Czy da się ją zrozumieć w 1 sekundę bez dźwięku?
2. Czy wygląda jak coś z iPhone'a albo apple.com, a nie jak „szablon z YouTube'a”?
3. Czy tekstu jest tak mało, jak się da?
4. Czy jest inna niż poprzednia scena?
5. Czy coś rusza się dokładnie na słowie?
6. **Test zamrożonej klatki:** czy każda klatka z połowy sceny wygląda jak dopracowany kadr, bez pustki, ucięć i nachodzenia?
7. **Krytyk:** obejrzyj arkusz jak Konrad. Co by powiedział? „Za dużo tekstu”, „tanie”, „powtarza się”, „zasłania twarz”?
   Popraw, zanim on to powie.
