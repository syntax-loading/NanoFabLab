"""make_srt.py — sidecar subtitles for lab3_video.mp4.

    python _shot/make_srt.py                 # writes lab3_video.srt
    python _shot/make_srt.py --out x.srt

The text is already written (SCRIPT.md), and the spoken paragraphs are the only
lines that are actually read aloud; the "> " blocks are Chinese speaker notes and
never appear. Timing comes from two places, combined:

  * the page's own slot in timeline.json (start, lead, length), and
  * the energy envelope of that page's TTS wav, which tells us when the voice
    really starts and stops inside the slot -- the wavs carry a few hundred ms of
    silence at each end, and ignoring that would push every cue late.

Inside that window the cues are laid out by character count. TTS speaks at a very
even rate, so this lands within a few tenths of a second; it is a sidecar file,
not burned in, so small drift is harmless.
"""
import argparse, json, math, os, re, struct, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SLIDES = os.path.dirname(HERE)
SCRIPT = os.path.join(SLIDES, "SCRIPT.md")

PAUSE_S = 0.45          # a [顿] marker
MAX_LINE = 44           # subtitle line width
MAX_LINES = 2
MIN_CUE = 1.1


def wav_samples(path):
    b = open(path, "rb").read()
    i, rate, ch, sw, data = 12, 24000, 1, 2, None
    while i + 8 <= len(b):
        cid, sz = b[i:i + 4], struct.unpack("<I", b[i + 4:i + 8])[0]
        body = b[i + 8:i + 8 + sz]
        if cid == b"fmt ":
            _, ch, rate, _, _, bits = struct.unpack("<HHIIHH", body[:16])
            sw = bits // 8
        elif cid == b"data":
            data = body
            break
        i += 8 + sz + (sz & 1)
    n = len(data) // (ch * sw)
    return rate, list(struct.unpack("<%dh" % n, data[:n * 2]))


def speech_window(pcm, rate):
    """(start_s, end_s) of the voiced part, via a 20 ms RMS envelope."""
    win = int(rate * 0.02)
    rms = []
    for i in range(0, len(pcm) - win, win):
        s = 0
        for v in pcm[i:i + win]:
            s += v * v
        rms.append(math.sqrt(s / win))
    if not rms:
        return 0.0, len(pcm) / float(rate)
    peak = max(rms) or 1.0
    thr = max(60.0, 0.02 * peak)      # an absolute floor too: -54 dBFS-ish
    hot = [i for i, r in enumerate(rms) if r > thr]
    if not hot:
        return 0.0, len(pcm) / float(rate)
    pad = 0.06
    return max(0.0, hot[0] * 0.02 - pad), min(len(pcm) / float(rate), (hot[-1] + 1) * 0.02 + pad)


def spell_fix(t):
    # the script is plain ASCII English; only the dashes need normalising for srt
    return t.replace("&mdash;", "-").replace("&amp;", "&").replace("\u2014", "-")


def page_blocks(md):
    """{page_no: [spoken paragraphs]} from SCRIPT.md."""
    out, cur = {}, None
    for raw in md.splitlines():
        m = re.match(r"^## (\d+)\s*·", raw)
        if m:
            cur = int(m.group(1))
            out[cur] = []
            continue
        if raw.startswith("## "):
            cur = None
            continue
        if cur is None:
            continue
        s = raw.strip()
        if not s or s.startswith(">") or s.startswith("▶") or s.startswith("---") or s.startswith("|"):
            continue
        out[cur].append(s)
    return out


def paragraphs_to_text(lines):
    """join wrapped source lines into paragraphs, keeping missing blank lines from
    fusing two paragraphs: a line that ended a sentence closes the paragraph."""
    paras, buf = [], []
    for line in lines:
        buf.append(line)
        if re.search(r"[.!?][\"')\]]?$", line):
            paras.append(" ".join(buf))
            buf = []
    if buf:
        paras.append(" ".join(buf))
    return paras


def split_cues(paras):
    """[(text, pause_after)] — sentence packing, clause splitting, hard wraps."""
    units = []
    for p in paras:
        parts = re.split(r"(?<=[.!?])\s+(?=[A-Z0-9\"'])", p)
        for part in parts:
            part = part.strip()
            if not part:
                continue
            pause = False
            if "[顿]" in part:
                pause = True
                part = part.replace("[顿]", "").strip()
            units.append((part, pause))
    cues = []
    for text, pause in units:
        words = text.split()
        if len(text) <= MAX_LINE * MAX_LINES:
            cues.append((text, pause))
            continue
        # too long for one cue: break at a comma or semicolon near the middle
        chunks, cur = [], text
        while len(cur) > MAX_LINE * MAX_LINES:
            mid = len(cur) // 2
            best = -1
            for m in re.finditer(r"[,;:]\s", cur):
                if best < 0 or abs(m.end() - mid) < abs(best - mid):
                    best = m.end()
            if best < 0:
                best = cur.rfind(" ", 0, MAX_LINE * MAX_LINES)
            if best <= 0:
                best = MAX_LINE * MAX_LINES
            chunks.append(cur[:best].strip())
            cur = cur[best:].strip()
        if cur:
            chunks.append(cur)
        for i, ch in enumerate(chunks):
            cues.append((ch, pause and i == len(chunks) - 1))
    return cues


def wrap2(text):
    if len(text) <= MAX_LINE:
        return text
    mid = len(text) // 2
    best, bestd = -1, 1e9
    for m in re.finditer(r"\s", text):
        d = abs(m.start() - mid)
        if d < bestd:
            best, bestd = m.start(), d
    return text[:best] + "\n" + text[best + 1:]


def ts(t):
    ms = int(round(t * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return "%02d:%02d:%02d,%03d" % (h, m, s, ms)


def main():
    ap = argparse.ArgumentParser()
    global MAX_LINE
    ap.add_argument("--out", default=os.path.join(SLIDES, "lab3_video.srt"))
    ap.add_argument("--maxline", type=int, default=MAX_LINE)
    a = ap.parse_args()
    MAX_LINE = a.maxline

    tl = json.load(open(os.path.join(HERE, "timeline.json"), encoding="utf-8"))
    blocks = page_blocks(open(SCRIPT, encoding="utf-8").read())

    rows = []
    for r in tl["pages"]:
        pg = r["page"]
        paras = paragraphs_to_text(blocks.get(pg, []))
        if not paras:
            print("page %d: no script text" % pg, file=sys.stderr)
            continue
        rate, pcm = wav_samples(os.path.join(HERE, r["wav"]))
        s0, s1 = speech_window(pcm, rate)
        vs = r["start"] + r["lead"] + s0
        ve = r["start"] + r["lead"] + s1
        cues = split_cues(paras)
        rate_cps = sum(len(c[0]) for c in cues) / max(0.001, ve - vs)
        weights = [len(c[0]) + (PAUSE_S * rate_cps if c[1] else 0) for c in cues]
        total = sum(weights)
        t = vs
        for (text, pause), w in zip(cues, weights):
            d = (ve - vs) * w / total
            if d < MIN_CUE:
                d = MIN_CUE
            rows.append((t, min(t + d, ve + 0.2), text))
            t += d
        if t > ve + 0.05:
            print("page %d: cues overflow by %.2fs" % (pg, t - ve), file=sys.stderr)

    with open(a.out, "w", encoding="utf-8", newline="\n") as f:
        for i, (s, e, text) in enumerate(rows, 1):
            f.write("%d\n%s --> %s\n%s\n\n" % (i, ts(s), ts(e), wrap2(spell_fix(text))))
    print("wrote %s: %d cues, last ends %s" % (a.out, len(rows), ts(rows[-1][1])))


if __name__ == "__main__":
    main()
