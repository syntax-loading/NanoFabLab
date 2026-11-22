"""build_timeline.py — the single source of truth for the video timeline.

    python _shot/build_timeline.py                 # 18 pages, then write narration.wav
    python _shot/build_timeline.py --lead 2.2 --print-only

Every page of the deck is one narration segment:

    [ lead ][ voice ][ pad ]        <- one clip, exact whole number of frames
      ^ page turn happens here, inside the lead

The lead exists because a page turn is not instant: #camera animates its
transform over 1.7 s (2.4 s with .push). So the turn is commanded at the first
frame of the clip and the voice starts once the camera has arrived.

Segment length is quantised UP to a whole frame, and the leftover is silence, so
audio and video are the same length by construction -- never "close enough".

Outputs, both next to this file:
  timeline.json   per-page lead/voice/length/start + the totals
  narration.wav   24 kHz mono 16-bit, the concatenation of every segment
"""
import argparse, json, math, os, struct, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SLIDES = os.path.dirname(HERE)

# titles for the report only; the deck's own STEPS[] is authoritative for content
TITLES = {
    1: "Opening", 2: "Where we start", 3: "PECVD SiO2 hard mask", 4: "PECVD dual",
    5: "Ellipsometry", 6: "Surface prep (VPO)", 7: "Spin coating & edge bead",
    8: "Soft bake", 9: "Stepper exposure", 10: "Post-exposure bake",
    11: "Development", 12: "Inspection 1", 13: "Hard-mask etch", 14: "Resist strip",
    15: "Main etch / breakthrough", 16: "Main etch / with oxygen",
    17: "Second ellipsometry", 18: "Inspection 4 / the result", 19: "Summary",
}


def wav_info(path):
    """(sample_rate, channels, sampwidth, data_bytes, data) for a RIFF/WAVE file.

    reads the chunks by hand: the files come from a TTS endpoint that leaves a
    placeholder size in the header, so wave.open() cannot be trusted."""
    b = open(path, "rb").read()
    if b[:4] != b"RIFF" or b[8:12] != b"WAVE":
        sys.exit("not a wav: " + path)
    i, fmt, data = 12, None, None
    while i + 8 <= len(b):
        cid = b[i:i + 4]
        sz = struct.unpack("<I", b[i + 4:i + 8])[0]
        body = b[i + 8:i + 8 + sz] if sz < len(b) else b[i + 8:]
        if cid == b"fmt ":
            fmt = struct.unpack("<HHIIHH", body[:16])
        elif cid == b"data":
            data = body
            break
        i += 8 + sz + (sz & 1)
    if fmt is None or data is None:
        sys.exit("incomplete wav: " + path)
    _, ch, rate, _, _, bits = fmt
    return rate, ch, bits // 8, len(data), data


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pages", default="1-18")
    ap.add_argument("--fps", type=int, default=30)
    ap.add_argument("--lead", type=float, default=2.0, help="page-turn lead, seconds")
    ap.add_argument("--open", type=float, default=1.0, help="hold before page 1 speaks")
    ap.add_argument("--tts", default=os.path.join(HERE, "tts"))
    ap.add_argument("--print-only", action="store_true")
    a = ap.parse_args()

    lo, _, hi = a.pages.partition("-")
    pages = list(range(int(lo), int(hi or lo) + 1))

    rows, start = [], 0.0
    rate = ch = sw = None
    for k, pg in enumerate(pages):
        wav = os.path.join(a.tts, "p%02d.wav" % pg)
        if not os.path.exists(wav):
            sys.exit("missing " + wav)
        r, c, w, nbytes, data = wav_info(wav)
        if rate is None:
            rate, ch, sw = r, c, w
        elif (r, c, w) != (rate, ch, sw):
            sys.exit("wav formats differ at " + wav)
        voice = nbytes / float(rate * ch * sw)
        lead = a.open if k == 0 else a.lead
        frames = int(math.ceil((lead + voice) * a.fps - 1e-9))
        seg = frames / float(a.fps)
        rows.append({"page": pg, "title": TITLES.get(pg, ""), "wav": os.path.relpath(wav, HERE).replace("\\", "/"),
                     "voice": round(voice, 4), "lead": lead, "frames": frames,
                     "seg": round(seg, 4), "start": round(start, 4),
                     "silence": round(seg - lead - voice, 4)})
        start += seg

    total = start
    print("%-3s %-27s %7s %6s %6s %7s %8s" % ("pg", "title", "voice", "lead", "frames", "seg", "start"))
    for r in rows:
        print("%-3d %-27s %7.2f %6.2f %6d %7.3f %8.2f" %
              (r["page"], r["title"][:27], r["voice"], r["lead"], r["frames"], r["seg"], r["start"]))
    print("%-3s %-27s %7.2f %6s %6d %7.3f" % ("", "TOTAL", sum(r["voice"] for r in rows), "",
                                              sum(r["frames"] for r in rows), total))
    print("video %.3f s = %d frames = %s" % (total, sum(r["frames"] for r in rows),
                                             "%d:%05.2f" % divmod(total, 60)))
    if a.print_only:
        return

    # ---- narration.wav: silence + voice per segment, padded so each segment is
    # exactly frames/fps long. The pad lands after the voice, never inside it.
    frame_bytes = ch * sw
    zero = b"\x00" * frame_bytes
    out, cursor = [], 0
    for r in rows:
        n_lead = int(round(r["lead"] * rate))
        want = int(round(r["seg"] * rate))
        _, _, _, _, data = wav_info(os.path.join(HERE, r["wav"]))
        have = len(data) // frame_bytes
        body = zero * n_lead + data
        got = len(body) // frame_bytes
        if got > want:
            body = body[:want * frame_bytes]
        else:
            body += zero * (want - got)
        out.append(body)
        cursor += want
    pcm = b"".join(out)
    n = len(pcm) // frame_bytes
    hdr = b"RIFF" + struct.pack("<I", 36 + len(pcm)) + b"WAVEfmt " + \
        struct.pack("<IHHIIHH", 16, 1, ch, rate, rate * frame_bytes, frame_bytes, 8 * sw) + \
        b"data" + struct.pack("<I", len(pcm))
    dst = os.path.join(HERE, "narration.wav")
    with open(dst, "wb") as f:
        f.write(hdr + pcm)

    tl = {"fps": a.fps, "open": a.open, "lead": a.lead, "rate": rate, "channels": ch,
          "sampwidth": sw, "total": round(total, 4), "frames": sum(r["frames"] for r in rows),
          "audio": "narration.wav", "pages": rows}
    with open(os.path.join(HERE, "timeline.json"), "w", encoding="utf-8") as f:
        json.dump(tl, f, indent=1)
    print("wrote timeline.json and narration.wav (%.2f s, %.1f MB)" % (total, (36 + len(pcm)) / 1e6))


if __name__ == "__main__":
    main()
