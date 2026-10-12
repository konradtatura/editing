# QA

Nie oddajesz niczego, czego nie obejrzałeś. Automatyczny check łapie liczby i formaty, Ty łapiesz resztę na contact sheetach (4 klatki: 0,3 s / ~1,2 s / środek / koniec).

## Automat (`qa.py check`)
- czas pliku = czas z planu (±0,12 s)
- .mov ma kanał alfa
- MIX/BROLL mają audio oryginału
- brak czarnych klatek > 0,3 s

## Oko (każdy sheet)
1. Tekst lub karta nie wchodzi na twarz/włosy w ŻADNEJ z 4 klatek (Konrad się rusza). Kolizja → `zone`, `y` albo krótsza fraza.
2. Tekst nie jest ucięty, nie wychodzi poza kadr, nie ma literówek, polskie znaki są poprawne.
3. Liczby = transkrypt.
4. Pierwsza klatka nie jest pusta dłużej niż 0,2 s (pełne ekrany), ostatnia klatka pokazuje rozwiązany stan (hold).
5. Kontrast: tekst czytelny na tle (jasna ściana → ciemny tekst).
6. Spójność: kolor akcentu, fonty, promienie te same co w reszcie filmu.
7. Split/PiP: okno z Konradem pokazuje twarz (nie ramię/ścianę), na końcu wraca do pełnego kadru.

## Final (`qa.py final` + sheet ~10 punktów)
- długość FINAL = rough cut (sync)
- -14 LUFS ±1, true peak ≤ -1 dB
- punch-iny nie ucinają głowy, animacje są w dobrych miejscach względem mowy

Max 3 poprawki na animację; jeśli dalej źle — wymień typ (np. T2 → T1) i zapisz powód w raporcie.
