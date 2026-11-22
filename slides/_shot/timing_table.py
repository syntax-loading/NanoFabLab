"""Rebuild the timing table at the end of SCRIPT.md.

Sources:
  * the per-page time budgets in the section headings  (author marks - never touched)
  * _shot/tts/timing.json                              (measured by tts_time.py)

  python _shot/timing_table.py           rebuild the table and print it
  python _shot/timing_table.py --print   print only
"""
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SCRIPT = os.path.join(ROOT, "SCRIPT.md")
JSON = os.path.join(HERE, "tts", "timing.json")


def read_pages():
    src = io.open(SCRIPT, encoding="utf-8").read()
    cut = src.find("## 时间标记")
    body = src[:src.rfind("---", 0, cut)] if cut > 0 else src
    pages = []
    for m in re.finditer(r"(?m)^## (\d\d) · ([^\n]*?)—\s*~?(\d+)\s*s", body):
        pages.append((m.group(1), m.group(2).strip(), int(m.group(3))))
    return src, cut, pages


def main(argv):
    src, cut, pages = read_pages()
    meas = {}
    if os.path.exists(JSON):
        meas = json.load(io.open(JSON, encoding="utf-8"))

    rows, tot_mark, tot_meas = [], 0, 0.0
    for num, title, mark in pages:
        m = meas.get(num)
        sec = m["seconds"] if m else None
        tot_mark += mark
        if sec:
            tot_meas += sec
        rows.append((num, title, mark, sec))

    lines = ["| 页 | 标题 | 标题标定 | omni 实测 | 差 |", "|---|---|---|---|---|"]
    for num, title, mark, sec in rows:
        if sec is None:
            lines.append("| %s | %s | %d s | — | — |" % (num, title, mark))
        else:
            lines.append("| %s | %s | %d s | %.1f s | %+.1f s |"
                         % (num, title, mark, sec, sec - mark))

    head = ["## 时间标记", "",
            "`标题标定` 是各节标题里的数（由作者填写，助手不改动）；`omni 实测` 是把该节正文交给",
            "Qwen omni 逐字朗读后的音频时长（`_shot/tts_time.py`，结果在同目录 `tts/timing.json`）。", ""]
    if tot_meas:
        head.append("合计：标定 **%d s ≈ %.1f 分钟**，omni 实测 **%.0f s ≈ %.1f 分钟**。"
                    % (tot_mark, tot_mark / 60.0, tot_meas, tot_meas / 60.0))
        head.append("")

    block = "\n".join(head + lines) + "\n"

    if "--print" not in argv:
        base = src[:src.rfind("---", 0, cut)].rstrip("\n") if cut > 0 else src.rstrip("\n")
        io.open(SCRIPT, "w", encoding="utf-8", newline="\n").write(
            base + "\n\n---\n\n" + block)
        print("SCRIPT.md: timing table rebuilt")
    print("\n".join(lines))
    print("marked %d s | measured %.1f s" % (tot_mark, tot_meas))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
