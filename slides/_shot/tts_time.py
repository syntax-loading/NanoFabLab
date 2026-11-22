"""Measure how long each page of SCRIPT.md takes to read aloud.

Sends one page of narration to a Qwen omni model on DashScope, saves the returned
audio, and reads the length out of the WAV header. The result is written back into
the 时间标记 table of SCRIPT.md (the 实测 column only) and into _shot/tts/timing.json.

  python _shot/tts_time.py              measure every page
  python _shot/tts_time.py 2 5 12       only these pages
  python _shot/tts_time.py --list       parse and print, no network
  python _shot/tts_time.py --redo       ignore cached audio and re-synthesise

Config comes from  labs/slides/.env  (DASHSCOPE_API_KEY, BASE_URL, MODEL, VOICE,
INSTRUCTIONS).  stdlib only, so no pip install is needed.
"""
import base64
import io
import json
import os
import re
import struct
import sys
import time
import urllib.error
import urllib.request
import wave

src0 = ""
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SCRIPT = os.path.join(ROOT, "SCRIPT.md")
ENV = os.path.join(ROOT, ".env")
OUT = os.path.join(HERE, "tts")

SUB = {"\u2080": "0", "\u2081": "1", "\u2082": "2", "\u2083": "3", "\u2084": "4",
       "\u2085": "5", "\u2086": "6", "\u2087": "7", "\u2088": "8", "\u2089": "9",
       "\u207a": " plus", "\u207b": " minus", "\u00b2": "2", "\u00b3": "3",
       "\u2074": "4", "\u2011": "-", "\u2013": "-", "\u2014": ", ", "\u00d7": " times "}


def load_env(path):
    cfg = {}
    if not os.path.exists(path):
        return cfg
    for raw in io.open(path, encoding="utf-8"):
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        k, v = k.strip(), v.strip()
        if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
            v = v[1:-1]
        cfg[k] = v
    return cfg


def pages():
    """[(number, title, narration_text)] in file order."""
    src = io.open(SCRIPT, encoding="utf-8").read()
    cut = src.find("## 时间标记")          # everything after the last page is a table
    if cut > 0:
        src = src[:src.rfind("---", 0, cut)]
    out = []
    for part in re.split(r"(?m)^(?=## \d\d · )", src)[1:]:
        head, body = part.split("\n", 1)
        num = re.match(r"## (\d\d) · (.*?)—", head)
        if not num:
            continue
        keep = []
        for ln in body.splitlines():
            s = ln.strip()
            if not s or s.startswith((">", "▶", "#", "---")):
                continue
            keep.append(s)
        text = " ".join(keep)
        text = text.replace("[顿]", " … ")
        for a, b in SUB.items():
            text = text.replace(a, b)
        text = re.sub(r"\s+", " ", text).strip()
        out.append((num.group(1), num.group(2).strip(), text))
    return out


def speak(text, cfg, timeout=180):
    """qwen3-tts-flash on the native multimodal endpoint: it reads the text verbatim
    and returns a URL to a wav, so nothing is paraphrased."""
    key = cfg.get("DASHSCOPE_API_KEY", "")
    if not key:
        raise SystemExit("DASHSCOPE_API_KEY is empty - fill it in " + ENV)
    url = cfg.get("TTS_URL",
                  "https://dashscope.aliyuncs.com/api/v1/services/aigc/"
                  "multimodal-generation/generation")
    body = {
        "model": cfg.get("MODEL", "qwen3-tts-flash"),
        "input": {
            "text": text,
            "voice": cfg.get("VOICE", "Cherry"),
            "language_type": cfg.get("LANGUAGE", "English"),
        },
    }
    req = urllib.request.Request(
        url, data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + key},
        method="POST")
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        obj = json.loads(resp.read().decode("utf-8"))
    out = (obj.get("output") or {}).get("audio") or {}
    if out.get("data"):
        return base64.b64decode(out["data"]), obj.get("output", {}).get("text", "")
    if not out.get("url"):
        raise RuntimeError("no audio url in the response: %s" % json.dumps(obj)[:300])
    with urllib.request.urlopen(out["url"], timeout=timeout) as resp:
        return resp.read(), obj.get("output", {}).get("text", "")


def _wav_info(data):
    """(rate, channels, width, data_offset) for a RIFF wav, else None."""
    if data[:4] != b"RIFF" or data[8:12] != b"WAVE":
        return None
    i, rate, ch, width = 12, 24000, 1, 2
    off = None
    while i + 8 <= len(data):
        cid = data[i:i + 4]
        size = struct.unpack("<I", data[i + 4:i + 8])[0]
        if cid == b"fmt ":
            ch, rate = struct.unpack("<H", data[i + 10:i + 12])[0], \
                       struct.unpack("<I", data[i + 12:i + 16])[0]
            width = struct.unpack("<H", data[i + 22:i + 24])[0] // 8
        elif cid == b"data":
            off = i + 8
            break
        i += 8 + size + (size & 1)
    if off is None:
        return None
    return rate, ch, width, off


def wav_seconds(data):
    info = _wav_info(data)
    if info:
        rate, ch, width, off = info
        # qwen3-tts writes a placeholder size field, so trust the file length
        return (len(data) - off) / float(rate * ch * width)
    return len(data) / 2.0 / 24000.0          # raw s16 mono PCM


def repair_wav(data):
    """rewrite the two size fields so ordinary players accept the file"""
    info = _wav_info(data)
    if not info:
        return data
    _, _, _, off = info
    body = len(data) - off
    out = bytearray(data)
    out[4:8] = struct.pack("<I", len(data) - 8)
    j = data.find(b"data") + 4
    out[j:j + 4] = struct.pack("<I", body)
    return bytes(out)


def main(argv):
    global src0
    src0 = io.open(SCRIPT, encoding="utf-8").read()
    cfg = load_env(ENV)
    items = pages()
    want = ["%02d" % int(a) for a in argv if re.fullmatch(r"\d{1,2}", a)]
    if want:
        items = [p for p in items if p[0] in want]
    if "--list" in argv:
        for num, title, text in items:
            print("%s  %-34s %4d words" % (num, title[:34], len(text.split())))
        print("total %d words" % sum(len(t.split()) for _, _, t in items))
        return 0

    os.makedirs(OUT, exist_ok=True)
    result = {}
    tpath = os.path.join(OUT, "timing.json")
    if os.path.exists(tpath):
        result = json.load(io.open(tpath, encoding="utf-8"))

    for num, title, text in items:
        wav = os.path.join(OUT, "p%s.wav" % num)
        if os.path.exists(wav) and "--redo" not in argv:
            sec = wav_seconds(open(wav, "rb").read())
            result[num] = {"title": title, "seconds": round(sec, 2), "words": len(text.split()),
                           "cached": True}
            print("p%s  %6.1f s  (cached)" % (num, sec))
            continue

        for attempt in range(3):
            try:
                t0 = time.time()
                audio, transcript = speak(text, cfg)
                break
            except (urllib.error.URLError, RuntimeError, TimeoutError) as e:
                if attempt == 2:
                    raise
                print("  retry p%s (%s)" % (num, e))
                time.sleep(2 + 3 * attempt)
        with open(wav, "wb") as f:
            f.write(repair_wav(audio))
        try:
            sec = wav_seconds(audio)
        except wave.Error:
            raise SystemExit("the model returned %s bytes that are not a WAV — set "
                             "audio format to wav in speak()" % len(audio))
        result[num] = {"title": title, "seconds": round(sec, 2), "words": len(text.split()),
                       "transcript": transcript, "wall": round(time.time() - t0, 1)}
        print("p%s  %6.1f s  %3d words  %.1f wpm" %
              (num, sec, len(text.split()), len(text.split()) / (sec / 60.0)))

    json.dump(result, io.open(tpath, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    total = sum(v["seconds"] for v in result.values())
    print("\ntotal %.1f s = %.1f min over %d pages" % (total, total / 60.0, len(result)))

    # comparison against the time budgets written in the headers
    heads = dict((m.group(1), int(m.group(2)))
                 for m in re.finditer(r"(?m)^## (\d\d) · [^\n]*—\s*~?(\d+)\s*s", src0))
    print("\n%-3s %-34s %5s %6s %6s" % ("pg", "title", "hdr", "tts", "diff"))
    for num in sorted(result):
        v = result[num]
        hdr = heads.get(num, 0)
        print("%-3s %-34s %5d %6.1f %+6.1f" % (num, v["title"][:34], hdr, v["seconds"],
                                              v["seconds"] - hdr))

    # the table at the end of SCRIPT.md is rebuilt by _shot/timing_table.py
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
