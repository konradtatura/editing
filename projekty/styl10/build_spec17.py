#!/usr/bin/env python3
"""Style 10 captions for AI song 1 (aisong1.mp4, 2:48, no SFX/music: it is a song).  usage: build_spec17.py WORKDIR NAME
Lyrics = faster-whisper (no VAD, condition_on_previous_text=False) corrected by hand; same caption treatment as the AI ads."""
import difflib, json, os, re, subprocess, sys
WD, NAME = sys.argv[1], sys.argv[2]
HERE = os.path.dirname(os.path.abspath(__file__))
norm = lambda t: re.sub(r"[^\w]", "", t.lower())
WEAK = set()
s6 = open(os.path.join(HERE, "..", "styl6", "build_spec6.py")).read()
exec(s6[s6.index("def align"):s6.index("src = os.path.join")])      # align() from style 6

SCRIPT = ("Chciałem po prostu dorobić do pensji, żeby pod koniec miesiąca nie drżeć. Wpisałem w Google, jak zarobić w sieci, i nagle zalał mnie złoty deszcz. "
          "Wyskoczył typ w wypożyczonym Lambo, krzyczy, że krypto to moja przyszłość. Wpłaciłem pięć stów, minęło pół godziny. "
          "Został mi screen i głęboka przykrość. Potem ankiety, trzy złote za wieczór. Klikam w kółko jak głupi przez noc. "
          "Koleżanka z liceum pisze na priv, że z jej szamponem odkryję swą moc. Dropshipping, paczka utknęła w Szanghaju. "
          "Klient mi grozi i sądem od rana. A na TikToku mówią: weź stań przed kamerą. No chyba kogoś tu boli głowa, proszę pana. "
          "Czy w tym świecie jest chociaż jeden normalny sposób? Gdzie nie muszę wysyłać paczek po nocy. Gdzie nie muszę świecić "
          "twarzą przed ludźmi. Gdzie nie muszę żebrać o lajki w niemocy. Zrób mały produkt cyfrowy z AI. Zero kartonów i zero "
          "wysyłek. Klient pobiera, Ty nie ruszasz palcem. I masz sto procent zysku na czysto. Żadnego wstydu, konto bez twarzy. "
          "Odpalam Autopilot, dwa dni i gotowe. Za siedemnaście ziko masz cały system. I wreszcie zarabiasz na swoje. Nie musisz "
          "pisać kodu, nie musisz być geniuszem. AI układa Ci gotowy produkt i stronę. Nawet na pierwszą reklamę dorzucają osiem "
          "stów, żebyś nie musiał ryzykować oszczędności znów. Zrób mały produkt cyfrowy z AI. Zero kartonów i zero wysyłek. "
          "Klient pobiera, Ty nie ruszasz palcem. I masz sto procent zysku na czysto. Żadnego wstydu, konto bez twarzy. "
          "Odpalam Autopilot, dwa dni i gotowe. Za siedemnaście ziko masz cały system. I wreszcie zarabiasz na swoje. "
          "Siedemnaście złotych, mniej niż duża kawa. Sto procent gwarancji zwrotu. Kliknij na dole i zobacz, jak to działa.")
BIG = {"pensji", "złoty", "deszcz", "lambo", "krypto", "pięć", "stów", "screen", "trzy", "złote", "szamponem", "dropshipping", "szanghaju",
       "sądem", "kamerą", "normalny", "paczek", "twarzą", "lajki", "produkt", "cyfrowy", "ai", "zero", "palcem", "sto", "procent", "zysku",
       "twarzy", "autopilot", "dwa", "dni", "siedemnaście", "ziko", "system", "swoje", "kodu", "geniuszem", "stronę", "osiem", "kawa",
       "gwarancji", "zwrotu", "kliknij", "działa", "gotowe"}
src = os.path.join(WD, NAME + ".mp4")
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", src], capture_output=True, text=True).stdout)
words = [dict(s=w.get("t", w.get("s")), e=w["e"], w=w["w"]) for s in json.load(open(os.path.join(WD, "tr_" + NAME + ".json"))) for w in s["words"]]
toks = align(words, SCRIPT)
for i in range(len(toks) - 2, -1, -1):              # "48 godzin" = one token
    if toks[i]["d"].isdigit() and toks[i + 1]["d"].startswith(("zł", "godzin")):
        toks[i]["d"] += " " + toks[i + 1]["d"]; toks[i]["e"] = toks[i + 1]["e"]; del toks[i + 1]
clean = lambda d: re.sub(r"[.,!?…:;]", "", d)
groups = []                                          # one word per caption; <0.12 s words glue onto the next
for k, u in enumerate(toks):
    nxt = toks[k + 1]["t"] if k + 1 < len(toks) else dur
    if groups and groups[-1]["glue"]:
        g = groups[-1]; g["w"].append(u); g["glue"] = False
    else:
        groups.append(dict(w=[u], glue=False))
    g = groups[-1]
    if nxt - g["w"][0]["t"] < 0.12 and not u["d"][-1] in ".?!" and len(clean(" ".join(x["d"] for x in g["w"]))) < 9: g["glue"] = True
caps = []
for i, g in enumerate(groups):
    t0 = g["w"][0]["t"] - 0.03; nxt = groups[i + 1]["w"][0]["t"] - 0.03 if i + 1 < len(groups) else dur
    end = g["w"][-1]["e"]; t1 = nxt if nxt - end < 0.6 else min(nxt, end + 0.3)
    text = clean(" ".join(x["d"] for x in g["w"]))
    caps.append(dict(t0=round(max(0, t0), 3), t1=round(t1, 3), text=text, big=any(norm(x["d"]) in {norm(b) for b in BIG} for x in g["w"])))
FX = [dict(type="arrow", t0=161.8, t1=dur, x=540, y=1790, size=130)]                   # "Kliknij na dole"
BLUR_CUTS = []
ZONES = [[143.1, 147.033, 0.885], [161.867, 999, 0.10]]   # 17 zł card on screen
spec = dict(dur=round(dur, 3), fps=30, capY=0.70, capSize=84, bigSize=112, capPunch=True, capZones=ZONES,
            caps=caps, fx=FX, blurCuts=BLUR_CUTS, hideCaps=[])
json.dump(spec, open(os.path.join(WD, f"spec10_{NAME}.json"), "w"), ensure_ascii=False, indent=1)
for c in caps: print(f'{c["t0"]:6.2f}-{c["t1"]:6.2f} {"*" if c["big"] else " "} {c["text"]}')
