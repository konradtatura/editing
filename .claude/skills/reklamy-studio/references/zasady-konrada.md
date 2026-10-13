# Zasady Konrada (z feedbacku, 2026-10-12/13)

Każdy punkt to uwaga, którą Konrad już raz zgłosił. Nie powtarzamy.

## Ogólne
- Wszystko po polsku (napisy, plansze, CTA). Rynek polski.
- Liczba e-booków w najlepszym dniu: **941** (nie 947). Cena Cyfrowego Autopilota: **17 zł**. „48 godzin”, „ponad 3 lata”.
- Powiadomienie o sprzedaży produktu klienta pokazuje **+79 zł** (nie 17 zł, bo 17 zł to cena CA).
- CTA: „Kliknij poniżej” albo „Kliknij przycisk poniżej”, przycisk **ze strzałką w dół na końcu**.
- Animacje nie za krótkie, nie za dużo i nie „AI-owe”. Mniej, ale dopracowane.
- Bez muzyki i SFX, dopóki nie powie inaczej. Od 2026-10-13: muzyka i SFX z darmowych bibliotek z licencją na reklamy (`audio.md`).

## Cięcia i zoomy (najczęstsze uwagi)
- Zoom zmienia się **tylko na cięciu** w jego nagraniu. Nigdy w środku ujęcia, nigdy kilka klatek po cięciu.
- Plansza startuje **dokładnie na klatce cięcia** (inaczej widać, jak tło zmienia się pod wejściem planszy).
- Znajdź każdą klatkę cięcia. Konrad podaje liczbę cięć, więc zawsze się zgadzam z jego liczbą (dodaję `extra_cuts`, jeśli detektor coś przeoczy).
- Ostatnie ujęcie z CTA: zoom 100%, żeby napis „Kliknij poniżej” nie wchodził na usta.

## Przejścia
- **Bez zanikania (opacity fade-out).** Plansza ucina się twardo na cięciu.
- Bez mignięcia twarzy między dwiema planszami. Plansze jedna po drugiej, twarde cięcie.

## Usta i twarz
- Nic nie może zasłaniać ust: ikonki, pigułki, karty „17 zł”, napisy. Przesuwaj niżej, pod brodę.
- Styl 3 / ads2: napisy na ok. 60% wysokości (capY 0.6), a listy (tracker, „bez…”) jeszcze niżej, żeby się nie zderzały.

## Napisy
- Wszystkie napisy w filmie na **jednej, stałej wysokości**. Nie przesuwaj ich per scena (nawet jeśli coś zasłaniają).
- Napisy muszą być czytelne na każdym tle: mocny cień. Ad11 (styl 4) przeszedł dopiero przy cieniu ok. 1,8× bazowego (+40%, potem +30%).
- Styl 3: napisy były za duże, zmniejszone o 25% (74/65/78 px).
- Niebieskie boxy obok siebie łączą się w jeden box (nie dwa nachodzące).
- Napis nie może wrócić po planszy, jeśli jego słowa padły już na planszy (np. „14 700 miesięcznie”).
- Słowo-akcent na planszy ma być widoczne odpowiednio długo (nie znikać od razu po wejściu, np. „cyfrowe”).

## Gradient (styl 2)
- Gradient dużych słów: **#9DC3F7 (góra) → #007A7C (dół), w każdej linii osobno**, z dużym ciemnym cieniem.
  Musi być wyraźnie widoczny na niebieskiej koszulce.

## B-rolle i materiały
- Jeśli Konrad wrzuca własne klipy (aislop1–3, aikicthen), wstawiam dokładnie je, nie stock.
- W kartach-reelach na planszach puszczam wideo (sekwencja klatek), nie zdjęcie.
- Stock z Pexels (klucz API w `scratchpad/.pexels.env`, nigdy w repo).

## Czego nie robić bez pytania
- Nie tnij hooków na osobne wersje, Konrad robi to sam. Pilnuj tylko, żeby żaden napis nie przechodził przez cięcie między hookami.
- Nie ruszaj zaakceptowanych reklam przy okazji innych poprawek.
