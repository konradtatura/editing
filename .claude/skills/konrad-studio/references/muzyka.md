# Muzyka (styl Imana)

Stan na 2026-10-04: Konrad zapytał o muzykę („muzyka robi w chuj, u Imana większość robi muzyka”). Test pod hook
„Ciężkiej pracy” była w `YT_Ciezka-praca/muzyka/` (projekt zakończony, film opublikowany; kod w ~/Documents/KonradStudio_Archiwum). Pierwszy longform był bez muzyki
(jego domyślne z 2026-10-03). **Przed każdym longformem zapytaj:** muzyka tak/nie, klimat filmowy (Iman) czy spokojny (lo-fi).

## Zasady (dlaczego u Imana działa)

1. **Muzyka jest montowana, nie podłożona.** Jeden track na cały film nic nie daje. Nowy rozdział to nowy track albo nowa sekcja tracku.
2. **Cisza na puencie.** Na kluczowym zdaniu muzyka urywa się do zera (0,4–1 s, krótki fade 30 ms), zostaje sam głos, potem wraca.
   Przykłady: „No właśnie.”, „I tu jest cały problem.”, „Wybór.”.
3. **Drop tracku ląduje na słowie.** Znajdź w tracku moment wejścia (największy skok głośności, patrz niżej) i przesuń track
   (`adelay`) tak, żeby uderzał w ważne słowo albo w wejście b-rolla.
4. **Cięcia na beatach.** Wejścia b-rolli i przybliżenia w miarę możliwości na mocnych uderzeniach tracku.
5. **Pod głosem, nie obok niego:**
   - track ok. −26 LUFS (12–14 dB pod głosem −14),
   - sidechain ściszający pod mową,
   - wycięcie ok. −5 dB przy 2,6 kHz (miejsce na głos), highpass 45 Hz.
6. **Mało melodii, dużo nastroju:** pulsujący bas, tykanie, rzadkie pianino, pady, narastanie. Bez wokali i wyraźnych melodii.

## Mapa muzyki = część planu animacji

Dla każdego rozdziału podaj emocję tracku, momenty ciszy (dokładne słowa) i punkt dropu.
Przykład z „Ciężkiej pracy”:
- hook: napięcie, cisza na „No właśnie.”, drop na „Nazywam się Konrad”,
- rutyna: monotonny loop,
- sufit: ciemniej, cisza na „I tu jest cały problem.”,
- dźwignia: jaśniej, nadzieja, uderzenie na ZASADZIE,
- test: tykający puls,
- dlaczego teraz: szansa, szczyt na „jest miejsce”,
- haczyk: pianino, najciszej w „dolinie”,
- wybór: filmowo, cisza przed „Wybór.”, ostatnie zdanie prawie bez muzyki.

## Skąd muzyka

| Źródło | Stan | Uwagi |
|---|---|---|
| **vidIQ** `vidiq_generate_music` (MCP) | działa | Royalty-free WAV, 10–180 s, 25 kredytów za track (saldo: `vidiq_balance`). Generowanie trwa 2–5 min (`vidiq_job_poll`). W prompcie bez negacji, dopisz „instrumental”. |
| ElevenLabs Music API | **nie działa** | Klucz Konrada jest na darmowym planie, więc API zwraca 402 `paid_plan_required`. |
| Epidemic Sound / Artlist | Konrad pobiera sam | Najbezpieczniejsze pod Content ID, często lepiej brzmi niż AI. |

Prompt, który dał dobry track do hooka: „Instrumental cinematic documentary underscore for a high-retention entrepreneur
YouTube video. Dark, tense, modern and premium. Pulsing low synth bass in steady eighth notes, soft ticking hi-hat like a clock,
sparse felt piano notes, airy atmospheric pads, subtle risers. 95 BPM, D minor. Starts minimal and builds tension steadily,
adding a deep sub pulse and wide cinematic strings in the second half. Calm, spacious arrangement that sits underneath a voice-over.”

## Technika

Gotowy łańcuch: `examples/music_hook_test.sh`. Składa się z: przesunięcia, EQ, głośności, ciszy przez `volume='if(between(t,a,b),0,1)'`,
fade'ów, `sidechaincompress` od głosu, `amix normalize=0` i limitera.
- **Punkt dropu:** RMS w oknach 100 ms, największy skok (np. +20 dB w 0,1 s). Kod jest w historii projektu; łatwo go odtworzyć numpy.
- **Kontrola:** `ebur128` całości (−14 LUFS, TP ≤ −1) oraz przebieg `showwavespic`.
- **Uczciwie:** nie słyszymy. Klimat i głośność ocenia Konrad, a my raportujemy tylko pomiary.
- **Oddanie:** wersja z muzyką, osobna ścieżka muzyki i wersja bez muzyki.

## Gotowy przepis na cały longform (2026-10-10, „3 modele”) — `examples/music_bed_longform.py`

Konrad: „chcę, żeby to się samo dopasowało, ja nic nie robię”. Domyślnie więc: **3 utwory z vidIQ** (napięcie / środek /
finał, po ~180 s, 75 kredytów), jeden na akt filmu. Skrypt: pętle z crossfade 3 s, drop utworu (największy skok RMS)
przesunięty na słowo (hook: „Nazywam się Konrad”, finał: „cztery elementy”), cisze na 3–4 puentach, muzyka znika przed
czarną planszą. Poziom: każdy odcinek −22 LUFS, potem łagodny sidechain od głosu (threshold 0.06, ratio 3) → pod mową
ok. −30 LUFS, czyli ~16 dB pod głosem. Uwaga: −27 LUFS + ratio 5 dało −42 LUFS pod mową = niesłyszalne.
Oddanie: FINAL.mp4 (z muzyką), FINAL_bez-muzyki.mp4, muzyka/MUZYKA.wav (osobna ścieżka).
