#!/usr/bin/env python3
"""ks.py — runs a longform project end to end, remembers finished work, resumes after interruption.

usage:
  ks.py PROJ init RAW1.MP4 [RAW2.MP4 …] [--script skrypt.md]     new project (sources → project.json; nothing rendered)
  ks.py PROJ run [--until STAGE] [--force STAGE]                  do every stage whose inputs changed, stop at a gate
  ks.py PROJ approve cut                                           Konrad accepted the preview → full-quality cut allowed
  ks.py PROJ status                                                what is done, what is next, how long each stage took
Stages (in order; a stage is skipped when its inputs are unchanged and its outputs exist):
  preflight  sources probed (audio layout, fps, disk, ASR)                      → preflight.json      (exit 2 = blocker)
  asr        verbatim words of every source (Parakeet + rescue, cached)         → tr_<K>/01_cut/…
  pack       all takes side by side for choosing                                → edit/takes_packed.md
  [gate]     takes.json — written by the editor (agent) from takes_packed.md
  cut        cut sound + splice audit (no video; only changed joins re-run)     → CUT_audio.wav, splice_audit.txt
  preview    960 px cut for the phone (cached pieces)                           → CUT_preview.mp4, CUT_preview_tel.mp4
  [gate]     `ks.py PROJ approve cut` (Konrad's OK on the preview)
  render     full-quality cut, hardware encoder, cached pieces                  → CUT.mp4
  words      word times of the cut for animations / captions (once per cut)     → tr/words.json
  [gate]     animations rendered: anim/scenes.json + anim/out/* (HyperFrames) or index.json (Tesseract export.py)
  final      segment-based assembly, voice −14 LUFS + SFX.wav if present        → FINAL.mp4, FINAL_tel.mp4
Every stage's inputs fingerprint, outputs and duration go to project.json; every run to runs.jsonl. Interrupt anything
(Ctrl-C, crash, sleep): `run` again — finished stages are skipped and the heavy tools continue from their cached pieces.
"""
import hashlib, json, os, subprocess, sys, time

K = os.path.dirname(os.path.abspath(__file__))
PY = "/Library/Frameworks/Python.framework/Versions/3.13/bin/python3"
ORDER = ["preflight", "asr", "pack", "cut", "preview", "render", "words", "final"]
MBPS = {"preview": 4, "render": 25, "final": 12}       # written twice (cached pieces + joined file)


def disk_need(P, name):
    """GB of free disk a stage needs before it may start (swap shares the disk: keep 1.5 GB on top)."""
    edl = P.p("edl.json")
    dur = 0.0
    if os.path.exists(edl):
        rr = json.load(open(edl))["ranges"]
        dur = sum(r.get("n", round((r["end"] - r["start"]) * 30)) for r in rr) / 30
    if name in MBPS:
        return dur * MBPS[name] / 8 / 1000 * 2 + 1.5
    return {"asr": 2.5, "cut": 2.0, "words": 1.5}.get(name, 0.5)


def fp(paths, extra=""):
    """Fingerprint of input files (real file, size, mtime) + parameters."""
    h = hashlib.sha1(extra.encode())
    for p in paths:
        if os.path.exists(p):
            rp = os.path.realpath(p); st = os.stat(rp)
            if st.st_size < 5_000_000:              # decisions / timelines: by CONTENT (tools rewrite them unchanged)
                h.update(hashlib.sha1(open(rp, "rb").read()).digest())
            else:                                   # media: real file + size + mtime
                h.update(f"{os.path.basename(rp)}|{st.st_size}|{st.st_mtime_ns};".encode())
        else:
            h.update(f"missing:{p};".encode())
    return h.hexdigest()[:16]


class Project:
    def __init__(self, root):
        self.root = os.path.abspath(root)
        self.pj = os.path.join(self.root, "project.json")
        self.d = json.load(open(self.pj)) if os.path.exists(self.pj) else {}

    def save(self):
        json.dump(self.d, open(self.pj + ".part", "w"), indent=1, ensure_ascii=False)
        os.replace(self.pj + ".part", self.pj)

    def p(self, *a):
        return os.path.join(self.root, *a)

    def log(self, rec):
        with open(self.p("runs.jsonl"), "a") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")


def sh(cmd, logf):
    with open(logf, "a") as lf:
        lf.write(f"\n$ {' '.join(cmd)}\n"); lf.flush()
        r = subprocess.run(cmd, stdout=lf, stderr=subprocess.STDOUT)
    return r.returncode


def stage_specs(P):
    src = P.d["sources"]
    tk, scenes, index = P.p("takes.json"), P.p("anim", "scenes.json"), P.p("index.json")
    anim_inputs = []
    if os.path.exists(scenes):
        sc = json.load(open(scenes))
        anim_inputs = [scenes] + [P.p("anim", "out", f"{k}.{'mov' if v[2] == 'K' else 'mp4'}") for k, v in sc.items()]
    elif os.path.exists(index):
        anim_inputs = [index] + [it["file"] for it in json.load(open(index))]
    sfx = P.p("SFX.wav")
    return {
        "preflight": dict(inputs=list(src.values()), outputs=["preflight.json"],
                          cmds=[[PY, f"{K}/preflight.py", P.root, *src.values()]]),
        "asr": dict(inputs=list(src.values()), outputs=[f"tr_{k}/01_cut/words_raw.json" for k in src],
                    cmds=[[PY, f"{K}/asr.py", s, P.p(f"tr_{k}")] for k, s in src.items()]),
        "pack": dict(inputs=[P.p(f"tr_{k}/01_cut/words_raw.json") for k in src], outputs=["edit/takes_packed.md"],
                     cmds=[["mkdir", "-p", P.p("edit")],
                           [PY, f"{K}/pack_takes.py", P.p("edit", "takes_packed.md"),
                            *[P.p(f"tr_{k}/01_cut/words_raw.json") for k in src], "--gap", "0.35"]]),
        "cut": dict(gate=(os.path.exists(tk), "write takes.json (pick the takes from edit/takes_packed.md)"),
                    inputs=[tk] + list(src.values()), outputs=["CUT_audio.wav", "splice_audit.txt", "edl.json"],
                    cmds=[[PY, f"{K}/cut_takes.py", tk, "--audio", P.p("CUT_audio.wav"), "--audit"]]),
        "preview": dict(inputs=[P.p("edl.json")], outputs=["CUT_preview.mp4", "CUT_preview_tel.mp4"],
                        cmds=[[PY, f"{K}/cut_takes.py", tk, "--preview", P.p("CUT_preview.mp4")],
                              [PY, f"{K}/check.py", "tel", P.p("CUT_preview.mp4")]]),
        "render": dict(gate=(P.d.get("approved", {}).get("cut") == fp([P.p("edl.json")]),
                             "Konrad must approve the preview: ks.py PROJ approve cut (re-approve after every takes fix)"),
                       inputs=[P.p("edl.json")], outputs=["CUT.mp4"],
                       cmds=[[PY, f"{K}/cut_takes.py", tk, "--render", P.p("CUT.mp4")]]),
        "words": dict(inputs=[P.p("CUT.mp4")], outputs=["tr/words.json"],
                      cmds=[[PY, f"{K}/transcribe.py", P.p("CUT.mp4"), P.p("tr")]]),
        "final": dict(gate=(bool(anim_inputs), "render the animations (anim/scenes.json + anim/out, or index.json)"),
                      inputs=[P.p("CUT.mp4")] + anim_inputs + ([sfx] if os.path.exists(sfx) else []),
                      outputs=["FINAL.mp4", "FINAL_tel.mp4"],
                      cmds=[[PY, f"{K}/assemble.py", P.root] + (["--scenes", scenes] if os.path.exists(scenes) else ["--index", index])
                            + (["--sfx", sfx] if os.path.exists(sfx) else []) + ["--settle", str(P.d.get("settle", 0.3)),
                            "--out", P.p("FINAL.mp4")] + (["--bez-sfx"] if os.path.exists(sfx) else []),
                            [PY, f"{K}/check.py", "tel", P.p("FINAL.mp4")]]),
    }


def run(P, until=None, force=()):
    st = P.d.setdefault("stages", {})
    for name in ORDER:
        sp = stage_specs(P)[name]                  # re-evaluated per stage: earlier stages may have changed its inputs/gate
        if "gate" in sp and not sp["gate"][0]:
            print(f"⏸  {name}: waiting — {sp['gate'][1]}")
            P.save(); return
        key = fp(sp["inputs"], name)
        done = st.get(name, {})
        outs_ok = all(os.path.exists(P.p(o)) for o in sp["outputs"])
        if done.get("key") == key and outs_ok and name not in force:
            print(f"✓  {name}: up to date ({done.get('seconds', 0):.0f} s last time)")
        else:
            free = __import__("shutil").disk_usage(P.root).free / 1e9
            need = disk_need(P, name)
            if free < need:
                print(f"⏸  {name}: only {free:.1f} GB free on disk, this step needs ≥ {need:.0f} GB — free space "
                      "(PLAN_MIEJSCA_NA_DYSKU.md) or close apps (swap lives on the same disk), then run again")
                P.save(); return
            print(f"▶  {name} …", flush=True)
            t0 = time.time(); logf = P.p("logs", f"{name}.log"); os.makedirs(P.p("logs"), exist_ok=True)
            for c in sp["cmds"]:
                rc = sh(c, logf)
                if rc:
                    P.log({"stage": name, "status": "failed", "rc": rc, "seconds": round(time.time() - t0, 1), "at": time.ctime()})
                    st[name] = {"status": "failed", "rc": rc}; P.save()
                    print(f"✗  {name} failed (exit {rc}) — see {logf}; fix and run again (finished work is kept)")
                    sys.exit(rc if rc != 2 else 2)
            sec = round(time.time() - t0, 1)
            st[name] = {"key": key, "seconds": sec, "finished": time.ctime(), "status": "done"}
            P.log({"stage": name, "status": "done", "seconds": sec, "at": time.ctime()}); P.save()
            print(f"✓  {name}: done in {sec:.0f} s")
        if until == name:
            break
    P.save()


def main():
    a = sys.argv[1:]
    if len(a) < 2:
        sys.exit(__doc__)
    P = Project(a[0]); cmd = a[1]
    if cmd == "init":
        os.makedirs(P.root, exist_ok=True)
        raws = [os.path.abspath(x) for x in a[2:] if not x.startswith("--") and x.lower().endswith((".mp4", ".mov"))]
        P.d.setdefault("sources", {})
        for i, r in enumerate(raws):
            P.d["sources"][chr(ord("A") + len(P.d["sources"]))] = r
        if "--script" in a:
            P.d["script"] = os.path.abspath(a[a.index("--script") + 1])
        P.d.setdefault("created", time.ctime()); P.save()
        print(json.dumps(P.d["sources"], indent=1))
    elif cmd == "run":
        until = a[a.index("--until") + 1] if "--until" in a else None
        force = [a[i + 1] for i, x in enumerate(a) if x == "--force"]
        run(P, until, force)
    elif cmd == "approve" and len(a) > 2 and a[2] == "cut":
        P.d.setdefault("approved", {})["cut"] = fp([P.p("edl.json")]); P.save(); print("cut approved for the current edl.json")
    elif cmd == "status":
        specs = stage_specs(P); st = P.d.get("stages", {})
        for name in ORDER:
            s = st.get(name, {}); sp = specs[name]
            fresh = s.get("key") == fp(sp["inputs"], name) and all(os.path.exists(P.p(o)) for o in sp["outputs"])
            mark = "✓" if fresh else ("✗" if s.get("status") == "failed" else "·")
            gate = "" if sp.get("gate", (True,))[0] else f"  ⏸ {sp['gate'][1]}"
            print(f"{mark} {name:9s} {str(s.get('seconds', '')) + ' s' if s.get('seconds') else '':>9}{gate}")
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
