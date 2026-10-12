# Detale, które robią montaż „dojebany” (MMO / bizopp, 2026-10-09)

Skąd: analiza klatka po klatce + dźwięk (spektrogram) Imana Gadzhiego („10,000 hours of Claude”, wtDDjBOfTZo),
Kellana Henneberry'ego (V_t51u1tBJc) i 7 referencji Konrada (`~/Documents/KonradStudio_Archiwum/referencje/REF_premium/`, narzędzie `detail/strip.py` tamże:
filmstrip 4 kl./s + spektrogram pod spodem). Konrad o lfpdo v3: „niby nie jest złe, ale brakuje takich pierdółek,
detali, które realnie robią film”. Grafika była OK. Brakowało warstwy detali.

## Co mają wszyscy dobrzy (a my nie mieliśmy)

| # | Detal | Jak często | Jak u nas |
|---|---|---|---|
| 1 | **Dźwięk pod każdą zmianą obrazu**: whoosh na wejście/wyjście planszy, pop na tekst, klik na UI, tik na licznik, bas („impact”) na dużą liczbę, notification na sprzedaż, chime na „tak/3 z 3”, error na „nie” | 8–12/min (Iman: 2–3 warstwy na jedno zdarzenie: powietrze + klik + sub) | `sfx_cues.py` → `sfx.py`; poziomy niżej |
| 2 | **Muzyka pod całością**, ściszana pod trudniejsze zdania | ciągle | decyzja Konrada (dodaje sam / test muzyki) |
| 3 | **Tekst na twarzy bez ramki**: liczba albo 2–4 słowa obok głowy, prawie przy każdym zdaniu z liczbą (R7: „84%”, licznik 5→29 mln) | co 6–15 s na odcinkach z samą twarzą | „callouty” na ścianie (`build_callouts.py`) |
| 4 | **Przejścia** w planszę i z planszy: szybki zoom + rozmycie (0,3 s) + whoosh, nigdy goły cut | każda plansza | `K.whip(dur)` |
| 5 | **Po powrocie na twarz** lekki „settle” (106→100 % w 0,3 s) | po każdej planszy | `final_v4.py` |
| 6 | **Kursor i klik**: kursor wjeżdża, przycisk się wciska, licznik rusza; zawsze z klikiem w dźwięku | 3–4/min w scenach UI | `K.click()` |
| 7 | **Liczby się toczą** z tikiem, a lądują z basem | każda liczba | `K.count` + tick/impact |
| 8 | **Zakreślacz** pod jednym słowem, przekreślenie „starego” sposobu | 1–2/min | `.mk` + `K.mark`, `K.strike` |
| 9 | **Prawdziwe dowody**: screeny dashboardów, artykułów z podświetleniem, nagrania ekranu | 1–2/min | brak: potrzebne od Konrada |
| 10 | Twarz nie znika: na długich planszach mała zaokrąglona ramka z twarzą (Iman) | plansze > 8 s | do zrobienia, gdy layout planszy zostawia róg |

## Poziomy SFX (głos −14 LUFS, SFX peak-normalizowane, potem gain)
whoosh −25 · whoosh-short −28 · swish −29 · pop −27 · click −25 · click-soft −27 · tick −34 (co ≥ 0,15 s) ·
impact-bass −24/−25 · notification −29 · ping −29 · chime/error/sparkle/typing −31. Nic głośniej niż głos.
Biblioteki: `assets/sfx/*.wav` (click, pop, swish, tick, whoosh) + `~/.claude/skills/media-use/audio/assets/sfx/*.mp3`
(Pixabay: impact-bass-1/2, whoosh, whoosh-short, whoosh-cinematic, typing, notification, chime, ping, error, sparkle, …).

## Callouty na ścianie (Konrad przy białej ścianie)
Lewa strona kadru (x 100–740), pionowo przy głowie. Ciemny atrament #0b1020, Inter: linia lekka 64 px / 300,
linia mocna 100–132 px / 900, akcent #2a5be0, „nie” #e23447. Słowa wysuwają się z maski zsynchronizowane ze słowem,
pop na każdą linię, wyjście w górę 0,28 s (albo cięcie whipem, gdy zaraz wchodzi plansza). Bez ramki, bez cienia.
