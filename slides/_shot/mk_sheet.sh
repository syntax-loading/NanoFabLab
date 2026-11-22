#!/usr/bin/env bash
# Render every beat of lab3_process_flow.html and stitch a 2-column contact sheet.
# Beats 13–16 (0-based) are keyframe-animated process views: they are frozen at a
# chosen point with ?notr=1&at=<ms>. All other beats use ?instant=1.
set -e
CHROME="$LOCALAPPDATA/ms-playwright/chromium_headless_shell-1243/chrome-headless-shell-win64/chrome-headless-shell.exe"
PY="C:/Users/16329/.dsh/dsh-runtimes/dsh-primary-runtime/dependencies/python/python.exe"
ROOT="D:/documents/Visual Studio 2022/atKTH/NanoFab/labs/slides"
OUT="$ROOT/_shot/frames"
URL="file:///D:/documents/Visual%20Studio%202022/atKTH/NanoFab/labs/slides/lab3_process_flow.html"
mkdir -p "$OUT"
rm -f "$OUT"/b*.png
for i in $(seq 0 18); do
  n=$((i + 1))
  case $i in
     9) q="notr=1&at=7600" ;;
    10) q="notr=1&at=8500&et=8500" ;;
    13) q="notr=1&at=5500" ;;
    14) q="notr=1&at=4200" ;;
    15) q="notr=1&at=8800" ;;
    16) q="notr=1&at=9800" ;;
    *)  q="instant=1" ;;
  esac
  "$CHROME" --headless --no-sandbox --disable-gpu --hide-scrollbars \
    --force-device-scale-factor=1 --window-size=1600,900 --virtual-time-budget=2500 \
    --screenshot="$OUT/b$(printf %02d $i).png" \
    "$URL?$q#$n" \
    >/dev/null 2>&1
  echo "frame $i ok"
done
"$PY" "$ROOT/_shot/mk_sheet.py"
