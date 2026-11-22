"""assemble.py — turn one rec.mjs clip into a constant-frame-rate mp4.

    python _shot/assemble.py --clip D:/tmp/p0s --out D:/tmp/p0s.mp4
    python _shot/assemble.py --clip ... --audio narration.wav --ss 0 --t 30

rec.mjs records whatever the compositor hands over (here ~75 fps, but jittery),
so the clip is first given a *variable* timeline from the real frame timestamps
via ffmpeg's concat demuxer, and only then resampled to -r 30. that keeps the
motion in step with the wall clock instead of assuming capture was even.

1921 px wide? the device scale is 1.2 with a 1600 CSS viewport, and chrome
rounds the device width up by one; that leftover column is cropped here.
"""
import argparse, json, os, subprocess, sys, statistics

FFMPEG = os.environ.get("FFMPEG", r"E:\Program Files\ffmpeg\bin\ffmpeg.exe")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--clip", required=True)
    ap.add_argument("--out", default="")
    ap.add_argument("--w", type=int, default=1920)
    ap.add_argument("--h", type=int, default=1080)
    ap.add_argument("--fps", type=int, default=30)
    ap.add_argument("--crf", type=int, default=18)
    ap.add_argument("--preset", default="slow")
    ap.add_argument("--audio", default="")
    ap.add_argument("--ss", type=float, default=0.0, help="trim start (s)")
    ap.add_argument("--t", type=float, default=0.0, help="trim length (s), 0 = all")
    ap.add_argument("--exact", type=float, default=0.0,
                    help="force the clip to exactly this many seconds: hold the last "
                         "frame if capture came up short, cut if it ran long. the "
                         "timeline quantises each segment to a whole frame, so this "
                         "is what keeps 18 clips from drifting against the audio.")
    ap.add_argument("--vf", default="")
    a = ap.parse_args()

    cap = json.load(open(os.path.join(a.clip, "capture.json"), encoding="utf-8"))
    frames = cap["frames"]
    if not frames:
        sys.exit("no frames in " + a.clip)

    # per-frame duration from the next frame's timestamp; the last frame gets the
    # median, which only matters for the final 1/fps of the clip
    dts = [frames[i + 1]["ms"] - frames[i]["ms"] for i in range(len(frames) - 1)]
    tail = statistics.median(dts) if dts else 33
    dts.append(tail)

    lst = os.path.join(a.clip, "concat.txt")
    base = frames[0]["t"] - frames[0]["ms"]
    with open(lst, "w", encoding="utf-8") as f:
        for fr, dt in zip(frames, dts):
            f.write("file '%s'\n" % os.path.join(a.clip, fr["file"]).replace("\\", "/"))
            f.write("duration %.6f\n" % (max(1, dt) / 1000.0))
        f.write("file '%s'\n" % os.path.join(a.clip, frames[-1]["file"]).replace("\\", "/"))

    out = a.out or os.path.join(a.clip, "clip.mp4")
    vf = "crop=%d:%d:0:0" % (a.w, a.h)
    nframes = 0
    if a.exact:
        # hold the last frame for as long as we might be short, then let
        # -frames:v cut the clip to exactly the frame the timeline asked for.
        # -t alone is off by one frame half the time, which after 18 clips is 18
        # frames of audio drift.
        nframes = int(round(a.exact * a.fps))
        vf += ",tpad=stop_mode=clone:stop_duration=30"
    if a.vf:
        vf += "," + a.vf
    cmd = [FFMPEG, "-y", "-hide_banner", "-loglevel", "error",
           "-f", "concat", "-safe", "0", "-i", lst]
    if a.audio:
        cmd += ["-i", a.audio]
    cmd += ["-vf", vf, "-r", str(a.fps), "-fps_mode", "cfr",
            "-c:v", "libx264", "-preset", a.preset, "-crf", str(a.crf),
            "-pix_fmt", "yuv420p", "-profile:v", "high", "-movflags", "+faststart"]
    if a.audio:
        cmd += ["-c:a", "aac", "-b:a", "192k", "-shortest"]
    if a.ss:
        cmd += ["-ss", str(a.ss)]
    if a.exact:
        cmd += ["-frames:v", str(nframes)]
    elif a.t:
        cmd += ["-t", str(a.t)]
    cmd += [out]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        sys.stderr.write(r.stderr[-4000:])
        sys.exit("ffmpeg failed")
    dur = subprocess.run([FFMPEG.replace("ffmpeg.exe", "ffprobe.exe"), "-v", "error",
                          "-show_entries", "format=duration,size",
                          "-of", "csv=p=0", out], capture_output=True, text=True).stdout.strip()
    print("wrote %s  (duration,size = %s)" % (out, dur))


if __name__ == "__main__":
    main()
