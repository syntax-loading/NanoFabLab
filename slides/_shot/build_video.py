"""build_video.py — record, assemble and mux the whole narration video.

    python _shot/build_video.py --pages 12-13 --work D:/tmp/vid      # a slice, for testing
    python _shot/build_video.py --jobs 3 --work D:/tmp/vid           # all 18 pages
    python _shot/build_video.py --concat-only --work D:/tmp/vid      # just re-mux

Pipeline, per page: rec.mjs records that page's clip on its own chromium (so a
bad clip is re-recorded alone and pages can run in parallel), assemble.py cuts it
to exactly the frame count the timeline asked for, then every clip is
stream-concatenated and muxed with narration.wav.

The page turn lives *inside* the clip: rec loads the previous page, waits for it
to settle, starts the screencast and only then presses ArrowRight. That is the
only way to capture the 1.7 s #camera transform -- loading #N directly would fly
in from the centre of the field instead of from the previous page.
"""
import argparse, json, math, os, shutil, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
SLIDES = os.path.dirname(HERE)
FFMPEG = os.environ.get("FFMPEG", r"E:\Program Files\ffmpeg\bin\ffmpeg.exe")
FFPROBE = os.path.join(os.path.dirname(FFMPEG), "ffprobe.exe")
PY = sys.executable
NODE = os.environ.get("NODE", "node")


def sh(cmd, **kw):
    r = subprocess.run(cmd, capture_output=True, text=True, **kw)
    if r.returncode:
        sys.stderr.write(" ".join(cmd) + "\n" + r.stdout[-2000:] + r.stderr[-3000:] + "\n")
        raise SystemExit("command failed: " + cmd[0])
    return r.stdout


def dur_of(path):
    """(nb_frames, duration_s) of the first video stream, or (None, duration)."""
    js = json.loads(sh([FFPROBE, "-v", "error", "-select_streams", "v:0",
                        "-show_entries", "stream=nb_frames:format=duration",
                        "-of", "json", path]))
    nf = js.get("streams", [{}])[0].get("nb_frames")
    return (int(nf) if nf not in (None, "N/A") else None,
            float(js.get("format", {}).get("duration", 0)))


def one(tl, row, work, keep, fps, preset):
    pg, seg = row["page"], row["seg"]
    clip = os.path.join(work, "p%02d" % pg)
    out = os.path.join(work, "p%02d.mp4" % pg)
    ms = int(math.ceil(seg * 1000)) + 800
    hash_ = pg - 1 if pg > 1 else 1
    adv = pg if pg > 1 else -1
    cmd = [NODE, os.path.join(HERE, "rec.mjs"),
           "--hash", str(hash_), "--adv", str(adv),
           "--pre", "3000", "--dur", str(ms),
           "--fmt", "jpeg", "--win", "1920x1080", "--w", "1600", "--h", "900",
           "--dsf", "1.2", "--pin", "--out", clip]
    want = row["frames"]

    def attempt():
        sh(cmd)
        sh([PY, os.path.join(HERE, "assemble.py"), "--clip", clip, "--out", out,
            "--fps", str(fps), "--exact", "%.4f" % seg, "--preset", preset])
        return dur_of(out)

    t = time.time()
    nf, d = attempt()
    tries = 1
    while nf is not None and nf != want and tries < 3:
        tries += 1
        nf, d = attempt()
    rec_s = time.time() - t
    if not keep:
        shutil.rmtree(clip, ignore_errors=True)
    if nf is not None and nf != want:
        raise SystemExit("p%02d: %d frames, wanted %d -- capture came up short" % (pg, nf, want))
    return pg, out, rec_s, "%d frames / %.3fs" % (nf or -1, d)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", required=True)
    ap.add_argument("--pages", default="")
    ap.add_argument("--jobs", type=int, default=1)
    ap.add_argument("--keep", action="store_true", help="keep the captured frames")
    ap.add_argument("--preset", default="medium")
    ap.add_argument("--concat-only", action="store_true")
    ap.add_argument("--out", default=os.path.join(SLIDES, "lab3_video.mp4"))
    a = ap.parse_args()

    tl = json.load(open(os.path.join(HERE, "timeline.json"), encoding="utf-8"))
    rows = tl["pages"]
    if a.pages:
        lo, _, hi = a.pages.partition("-")
        sel = set(range(int(lo), int(hi or lo) + 1))
        rows = [r for r in rows if r["page"] in sel]
    os.makedirs(a.work, exist_ok=True)

    if not a.concat_only:
        print("recording %d page(s), %d at a time" % (len(rows), a.jobs))
        t0 = time.time()
        with ThreadPoolExecutor(max_workers=a.jobs) as ex:
            futs = [ex.submit(one, tl, r, a.work, a.keep, tl["fps"], a.preset) for r in rows]
            done = 0
            for f in futs:
                pg, out, rec_s, info = f.result()
                done += 1
                print("  [%2d/%2d] p%02d  rec %5.1fs  %s  (%s)" %
                      (done, len(rows), pg, rec_s, os.path.basename(out), info.strip()),
                      flush=True)
        print("record+assemble %.1f s" % (time.time() - t0))

    clips = [os.path.join(a.work, "p%02d.mp4" % r["page"]) for r in rows]
    missing = [c for c in clips if not os.path.exists(c)]
    if missing:
        sys.exit("missing clips: " + ", ".join(missing))
    lst = os.path.join(a.work, "body.txt")
    with open(lst, "w", encoding="utf-8") as f:
        for c in clips:
            f.write("file '%s'\n" % c.replace("\\", "/"))
    body = os.path.join(a.work, "body.mp4")
    sh([FFMPEG, "-y", "-hide_banner", "-loglevel", "error", "-f", "concat",
        "-safe", "0", "-i", lst, "-c", "copy", body])
    print("body:", dur_of(body)[1])

    if rows == tl["pages"]:
        wav = os.path.join(HERE, tl["audio"])
        sh([FFMPEG, "-y", "-hide_banner", "-loglevel", "error",
            "-i", body, "-i", wav,
            "-map", "0:v:0", "-map", "1:a:0",
            "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
            "-shortest", "-movflags", "+faststart", a.out])
        print("wrote", a.out, dur_of(a.out)[1])
    else:
        print("partial run: body only, no audio mux")


if __name__ == "__main__":
    main()
