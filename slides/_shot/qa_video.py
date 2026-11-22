"""qa_video.py — check the finished video against the timeline.

    python _shot/qa_video.py --video lab3_video.mp4 --sheet D:/tmp/qa_sheet.png

Three things are worth checking before calling a render done:

  1. lengths. the muxed file, the concatenated body and narration.wav must all be
     the same length; a frame-count mismatch means some clip was short.
  2. the right page is on screen when its voice starts. one frame is pulled from
     the middle of every page's narration and laid out as a contact sheet with
     the page number burned in, so the whole 9.5 minutes can be eyeballed at once.
  3. nothing is silent that should not be. per-page mean volume of the audio is
     read back from the muxed file, which catches a wrong wav or an empty slot.
"""
import argparse, json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SLIDES = os.path.dirname(HERE)
FFMPEG = os.environ.get("FFMPEG", r"E:\Program Files\ffmpeg\bin\ffmpeg.exe")
FFPROBE = os.path.join(os.path.dirname(FFMPEG), "ffprobe.exe")
PY = sys.executable


def probe(path):
    js = json.loads(subprocess.run(
        [FFPROBE, "-v", "error", "-show_entries",
         "stream=codec_type,codec_name,nb_frames,duration,width,height,sample_rate,channels:format=duration,size",
         "-of", "json", path], capture_output=True, text=True).stdout)
    return js


def volume(path, t0, dur):
    r = subprocess.run([FFMPEG, "-hide_banner", "-ss", "%.3f" % t0, "-t", "%.3f" % dur,
                        "-i", path, "-vn", "-af", "volumedetect", "-f", "null", "-"],
                       capture_output=True, text=True)
    for line in r.stderr.splitlines():
        if "mean_volume" in line:
            return float(line.split("mean_volume:")[1].split("dB")[0])
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--video", default=os.path.join(SLIDES, "lab3_video.mp4"))
    ap.add_argument("--sheet", default="")
    ap.add_argument("--frames", default="")
    a = ap.parse_args()

    tl = json.load(open(os.path.join(HERE, "timeline.json"), encoding="utf-8"))
    js = probe(a.video)
    streams = {s["codec_type"]: s for s in js["streams"]}
    v, au = streams.get("video"), streams.get("audio")
    fdur = float(js["format"]["duration"])
    print("video %s  %dx%d  %s fps-ish  %s frames  %.3fs" %
          (a.video, v["width"], v["height"], v.get("r_frame_rate", "?"),
           v.get("nb_frames"), float(v.get("duration") or 0)))
    print("audio %s %s Hz %sch  %.3fs" %
          (au["codec_name"], au["sample_rate"], au["channels"], float(au["duration"])))
    print("container %.3fs  %.1f MB" % (fdur, int(js["format"]["size"]) / 1e6))

    want = tl["total"]
    nframes = sum(p["frames"] for p in tl["pages"])
    ok = True
    if abs(fdur - want) > 0.05:
        print("FAIL duration %.3f != timeline %.3f" % (fdur, want))
        ok = False
    if v.get("nb_frames") and int(v["nb_frames"]) != nframes:
        print("FAIL frames %s != timeline %d" % (v["nb_frames"], nframes))
        ok = False
    if abs(float(v["duration"]) - float(au["duration"])) > 0.05:
        print("FAIL video %.3fs vs audio %.3fs" % (float(v["duration"]), float(au["duration"])))
        ok = False

    print("\npage  voice start   screen check")
    frames_dir = a.frames or os.path.join(os.path.dirname(a.video) or ".", "_qa_frames")
    os.makedirs(frames_dir, exist_ok=True)
    stamps = []
    for p in tl["pages"]:
        t = p["start"] + p["lead"] + p["voice"] * 0.5
        dst = os.path.join(frames_dir, "q%02d.png" % p["page"])
        subprocess.run([FFMPEG, "-y", "-v", "error", "-ss", "%.3f" % t, "-i", a.video,
                        "-frames:v", "1", "-vf", "scale=480:-1", dst], check=True)
        vol = volume(a.video, p["start"] + p["lead"], max(1.0, p["voice"] - 0.3))
        flag = ""
        if vol is None or vol < -50:
            flag = "  <-- suspiciously quiet (%.1f dB)" % (vol if vol is not None else 0)
            ok = False
        print("p%02d  %8.3fs  %s%s" % (p["page"], p["start"] + p["lead"],
                                       os.path.basename(dst), flag))
        stamps.append((p["page"], dst))

    if a.sheet:
        code = (
            "from PIL import Image, ImageDraw\n"
            "import json,sys\n"
            "stamps=json.load(open(sys.argv[1]))\n"
            "ims=[(p,Image.open(f)) for p,f in stamps]\n"
            "w,h=ims[0][1].size\n"
            "cols=6; rows=(len(ims)+cols-1)//cols\n"
            "sh=Image.new('RGB',(w*cols,h*rows),(8,10,14))\n"
            "d=ImageDraw.Draw(sh)\n"
            "for i,(p,im) in enumerate(ims):\n"
            "    x,y=(i%cols)*w,(i//cols)*h\n"
            "    sh.paste(im,(x,y)); d.text((x+8,y+6),'p%02d'%p,fill=(255,220,120))\n"
            "sh.save(sys.argv[2])\n")
        meta = os.path.join(frames_dir, "stamps.json")
        json.dump(stamps, open(meta, "w"))
        subprocess.run([PY, "-c", code, meta, a.sheet], check=True)
        print("\ncontact sheet:", a.sheet)
    print("\n", "OK" if ok else "PROBLEMS FOUND")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
