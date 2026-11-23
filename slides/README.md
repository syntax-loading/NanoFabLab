# IH2659 / FIH3608 — LAB3 "Gate Formation" — process-flow deck

A single self-contained HTML slide deck that walks the whole LAB3 process, one
continuous camera take, 19 beats, ~15 min at 1× speed.

```
labs/
├── slides/
│   ├── lab3_process_flow.html   ← the deck (single file, no dependencies)
│   ├── SCRIPT.md                ← the speaking script, page by page (read this to present)
│   ├── QnA.md                   ← the Q&A cheatsheet (read this after the talk)
│   ├── README.md                ← this file
│   ├── .gitignore
│   ├── .env                     ← API key for the TTS timing pass (never committed)
│   └── _shot/
│       ├── mk_sheet.sh          ← renders all 19 beats + stitches a contact sheet
│       ├── tts_time.py          ← reads each page aloud via qwen3-tts, measures it
│       ├── timing_table.py      ← rebuilds the timing table at the end of SCRIPT.md
│       └── contact_sheet.png    ← the current preview (generated)
├── assets/wafer_pattern/        ← wafer_pattern.js, the top-view pattern source
└── HT26 Lab 3/                  ← raw measurement files + the original micrographs
```

## Viewing it

Open `lab3_process_flow.html` in a browser. Nothing is fetched: the CSS, the SVG
geometry, the JS state machine and every photograph are inlined (base64), so the
file can be mailed or opened from a USB stick.

Navigation: `←` / `→` step, `space` play the run, `1 2 4 6` speed, `T` tilt,
click left/right half of the slide. `#13` in the URL jumps straight to page 13.

## URL hooks (for review and QA)

| parameter | effect |
|---|---|
| `?instant=1` | kills all transitions and animations → every page shows its base/final state |
| `?notr=1` | kills transitions only, keeps keyframes (use with `at=`) |
| `?at=<ms>` | parks every CSS animation at that page time (the only way to hold a mid-animation frame; CSS transitions do not advance in headless virtual time) |
| `?et=<ms>` | freezes the JS-driven timelines (coating, ellipsometry, the PEB acid profile) at that time |
| `?play=1` | autoplays from page 1 |
| `?qa=1` | appends an overflow report to `document.title`: any text block that spills its box or leaves the 1600×900 stage |
| `#<n>` | jump to page n |

Example still of the main etch at 4 s: `lab3_process_flow.html?notr=1&at=4000#16`

## The 19 beats

| # | kicker | title | what is on screen |
|---|---|---|---|
| 1 | Opening | Gate Formation | title, wafer turning |
| 2 | Step 01 | Where we start | the SOI stack, cross-section |
| 3 | Step 02 | PECVD SiO₂ hard mask | PECVD, 37 nm growth |
| 4 | PECVD | (continuation) | the same run on the bare-Si monitor |
| 5 | Step 03 | Ellipsometry | 5-point measurement, Ψ/Δ, 37.02 nm |
| 6 | Step 04 | Surface prep | VPO: pump down → HMDS → reaction → purge |
| 7 | Step 04 | Spin coating & edge bead | dynamic dispense → spin-off → rim rinse → backside |
| 8 | Step 04 | Soft bake | 95 °C, solvent leaving, film densifies |
| 9 | Step 05 | Stepper exposure | 9×7 field flash sweep, resist darkens with depth ripple |
| 10 | Step 05 | Post-exposure bake | two phases: no heat (acid ripple) → 110 °C (profile flattens) |
| 11 | Step 06 | Development | TMAH, the pattern opens |
| 12 | Checkpoint | Inspection ① | micrograph, measured pitch 8.16 / 8.08 µm |
| 13 | Step 07 | Hard-mask etch | CH₃F/CF₄ opens the oxide, undercuts |
| 14 | Step 08 | Resist strip | O₂ ash, resist eaten from every side; 20× micrograph of the opened hard mask |
| 15 | Step 09 | Main etch · breakthrough | 12 s, no O₂, shallow narrow bite |
| 16 | Step 10 | Main etch · with oxygen | 20 s, sidewall inhibitor, the trench goes down |
| 17 | Step 11 | Second ellipsometry | monitor wafer again: 37.02 → 33.06 nm |
| 18 | Checkpoint | Inspection ④ · the result | final micrograph, gates + cap |
| 19 | Summary | What the numbers say | the derived numbers, hand-off to LAB4 |

## Where the copy lives (for the copy editor)

Everything a copy editor needs is in the `STEPS` array, roughly the block that
starts with

```js
/* -------- step data -------- */
```

and it is the only place to touch. Each entry has

| field | meaning |
|---|---|
| `no:` | kicker text, e.g. `"Step 07"` / `"Checkpoint"` |
| `h1:` | the big title |
| `h2:` | the subtitle line |
| `params:` | the little key/value table, `P("Key","Value")` |
| `note:` | the paragraph under it; supports inline HTML (`<b>`, `&mdash;`) |

Keep the entries in order, keep the count at 19. The beat index is just
`array index`, so **inserting or deleting an entry shifts every later page** and
also needs: the `CAM` array, the `data-beat="…"` CSS rules, any `idx === n`
checks, `COAT_QA` / `coatFns` keys, `wpStateFor()` thresholds and the
`for i in $(seq 0 18)` bound in `_shot/mk_sheet.sh` to be renumbered.

Editing rules that matter for correctness:

- **Numbers are measured, not invented.** 37.02 / 33.06 nm, s² = 0.014 / 0.76,
  3.96 nm loss (10.7 %), 8.16 / 8.08 µm pitch all come from the files in
  `HT26 Lab 3/`. If you reword, keep the digits.
- The etch times (12 s breakthrough + 20 s main) and the PECVD 37 nm are the
  process values used throughout; a sentence that contradicts them is a bug.
- Claims already trimmed for accuracy: the edge bead is **not** justified by
  contact printing (the tool is a Nikon NSR projection stepper) — it is a
  particle / hotplate / backside-flatness problem. Keep it that way.
- The dispense is **dynamic** (confirmed). Do not write a static-dispense
  recipe or a specific dispense rpm unless it comes from the process sheet.

## The numbers behind the deck

| quantity | value | source |
|---|---|---|
| hard mask before | 36.905 / 37.035 / 37.009 / 36.937 / 37.213 nm | `HT26 Lab 3/SI WAFEFR.txt` |
| mean, sample variance | **37.0198 nm, s² = 0.0144 nm²** | derived (n = 5, N−1) |
| hard mask after | 33.820 / 33.089 / 31.575 / 33.254 / 33.541 nm | `HT26 Lab 3/HARDMASK 12 S bt 20 S mAIN.txt` |
| mean, sample variance | **33.0558 nm, s² = 0.7631 nm²** | derived (n = 5, N−1) |
| loss | 3.964 nm = 10.7 % of the film | derived |
| SiO₂ etch rate in Cl₂/HBr/O₂ | 0.198 nm/s | 3.96 nm over 20 s |
| selectivity | ≈ 25–40 : 1 | 100 nm a-Si / 3.96 nm oxide |
| over-etch window | ≈ 11 s for a 30 % oxide loss | 7.5 nm × 0.3 / 0.198 |

## Embedded photographs

All four are base64 inside the HTML (search for `data:image/jpeg;base64`). The
originals are in `HT26 Lab 3/`:

| page | plate | original file |
|---|---|---|
| 2 | the "where we start" band | `Before process Captured Digital Sight 10 - EPI50X EPI BF 2.jpg` (cropped to a 7:1 band, rotated 0.405° to level) |
| 12 | Inspection ① | `after expose_ gate measuringCaptured Digital Sight 10 - EPI150X EPI BF.jpg` |
| 14 | opened hard mask, bottom-right corner | `hard mask Captured Digital Sight 10 - EPI20X EPI BF.jpg` (crop 2544,1644 → 3616,2312 = 92 × 57 µm across the array boundary, autocontrast, 900 × 563) |
| 18 | Inspection ④ | `End of process Captured Digital Sight 10 - EPI150X EPI BF.jpg` |

To swap one: crop to the plate's aspect (1.38 : 1, or 1.60 : 1 for page 14), re-encode
as JPEG, replace the base64 string — the plate CSS does the rounding, the shadow and the caption chip.

## Rendering the contact sheet

`_shot/mk_sheet.sh` renders all 19 pages with headless Chrome, then `_shot/mk_sheet.py`
stitches them into `contact_sheet.png` (it points at a Playwright `chrome-headless-shell`
install; adjust `CHROME=` at the top if yours lives elsewhere). Pages 7, 14–17
and the coating pages are captured mid-animation with `?notr=1&at=…`, the rest
with `?instant=1`.

## The speaking script

`SCRIPT.md` is the narration, one section per page, in the same order as the deck.
It is written to be read out loud, not to be browsed:

* plain paragraphs = the words to say;
* `> ` lines = notes for the speaker (why this page exists, what to cut if it runs
  long, extra detail for questions) - never spoken;
* `[顿]` = a half-second pause, not spoken;
* `▶ 按 →` = the only cue that needs timing: press the right arrow here.

Each heading carries the page's time budget (`— ~45 s`). Those numbers are the
author's marks and are not to be edited by anyone else. The table at the end
(`## 时间标记`) lists, per page, the mark, the measured length, and the difference.

## Measuring the script

The timing pass sends one page of narration to a text-to-speech model, saves the
audio and reads the duration out of the WAV:

```
python _shot/tts_time.py --list       # parse only: 19 pages, ~1.5k words
python _shot/tts_time.py              # measure every page (cached in _shot/tts/)
python _shot/tts_time.py 3 5 12       # just these pages
python _shot/tts_time.py --redo       # ignore the cache
python _shot/timing_table.py          # rebuild the table at the end of SCRIPT.md
```

Keys live in `slides/.env` (git-ignored): `DASHSCOPE_API_KEY`, `MODEL`
(`qwen3-tts-flash` - it reads the text verbatim; the omni models answer back
instead of reading, and `qwen3.8-omni-flash` rejects the audio modality outright),
`VOICE`, `LANGUAGE`. Output: `_shot/tts/pNN.wav` plus `tts/timing.json`.

TTS averages ~145 wpm; a human reading the same text is closer to 110-120, so the
measured column is a floor, and useful mainly for comparing pages with each other.

## The video

`lab3_video.mp4` is the deck with its narration: 9:36, 1920x1080, 30 fps, plus
`lab3_video.srt` as a sidecar. It is not edited — it is *recorded*, one page at a
time, so any single page can be re-recorded without touching the rest.

```
python _shot/build_timeline.py                    # -> _shot/timeline.json + narration.wav
python _shot/build_video.py --work D:/tmp/vid     # record, encode, mux  (~18 min)
python _shot/make_srt.py                          # sidecar subtitles
python _shot/qa_video.py --sheet D:/tmp/qa.png    # lengths, per-page frames, levels
```

Three decisions carry the whole thing:

* **One page = one clip.** `rec.mjs` loads page *N-1*, waits for it to settle,
  starts a CDP screencast and only then presses ArrowRight, so the 1.7 s `#camera`
  fly-in is *inside* the clip. Loading `#N` directly would fly in from the centre
  of the field instead of from the previous page. Clips are independent: a bad
  page costs one page. `--jobs 2` has hung the screencast before; keep it at 1.
* **Audio and video sit on the same frame grid.** `build_timeline.py` rounds each
  segment *up* to a whole frame and pads the leftover with silence, so clip *k*
  and audio segment *k* are identical in length by construction. `assemble.py`
  cuts each clip with `-frames:v`, never `-t` — `-t` lands one frame over about
  half the time, and eighteen of those is eighteen frames of drift against the voice.
* **The page turn is the lead-in.** A segment is `[2.0 s turn][voice][pad]`, so the
  voice starts once the camera has arrived.

Capture details worth knowing: a 1600x900 CSS viewport at device scale 1.2 gives
exactly 1920x1080 of vector-sharp output (no upscaling of the stage). Chrome
rounds the device width up by one pixel, so the stage is pinned to the viewport
origin (`--pin`) and the spare column is cropped at encode. A 1-px nearly
transparent tick animation is injected because `Page.startScreencast` only emits
frames when the page changes something — page 1 was recording its first 5.9 s and
then going quiet. Frame pacing is taken from the per-frame timestamps rather than
assumed, so a slow frame does not shift the voice.

The voice is the TTS wavs from the timing pass, joined with silence. To use a
human recording, drop your own files into `_shot/tts/pNN.wav` and re-run
`build_timeline.py` — nothing downstream knows where the voice came from.

Page 19 (Summary) is deliberately absent: the ending is meant to be a different
one, a fast pass back over the whole flow, and that is still to be assembled.
Two consequences of cutting it, both cosmetic: the footer of the last page reads
`18 / 19`, and the summary page's own content never appears. Both disappear the
day the new ending is built as a real 19th page rather than as a montage.

## The PDF

`lab3_process_flow.pdf` is 19 pages, 16:9 (1600x900 CSS px = 1200x675 pt), one
page per beat, with every animation left at its **end** state — the frame that
is on screen the moment before the arrow is pressed. It is the handout version:
nothing moves, nothing is half-revealed.

```
node _shot/mk_pdf.mjs        # 19 pages, ~5 min, -> lab3_process_flow.pdf
```

Four things carry it:

* **Why not `--print-to-pdf`.** The deck animates. `?instant=1` kills the CSS
  keyframes, and the keyframes are what carry the "before -> after" work, so a
  page printed that way is the *before* state. Headless virtual time does not
  advance the compositor clock either, so `--virtual-time-budget` leaves a page
  half revealed (this is why the contact sheet has to park animations with
  `?at=`). The only honest route is to let each beat run for its own dwell time
  and print afterwards; the `d` values in `CAM[]` are copied into `DWELL` in the
  script, and that is where the five minutes go.
* **Reload per page.** Every page is a fresh navigation to `?shot=N#N` — the
  throwaway query exists only because `#1 -> #16` is a same-document hash change
  and fires no load event. The stage is then pinned to the page origin
  (`left/top:0`, `margin:0`, no transform) so a window that is not exactly
  1600x900 cannot leak a `fit()` scale into the print layout, and the script
  checks `#cur`, `#t1` and `#note` before it prints.
* **The deck carries the page geometry** (`@page{size:1600px 900px;margin:0}`
  plus `#stage{transform:scale(1)!important}` in the `@media print` block), so a
  plain Ctrl+P also gives one 16:9 sheet per beat instead of paginating a 900 px
  stage across Letter.
* **The page box is corrected after the join.** Chrome answers "one 900 px page"
  with a 675.12 pt box while painting only 900.00 px, so each page rasterises
  with a white hairline along the bottom edge. `mk_pdf.mjs` rewrites
  `/MediaBox` and `/TrimBox` to 675.00 pt in place once `pdfunite` has joined the
  pages — same byte length, so the xref offsets stay valid and no PDF library is
  needed.

The PDF is committed (9.6 MB) because it is the thing that gets handed to a
reader; the per-page prints under `_shot/pdf/` are not.

## What the next sessions may want

* **Q&A cheatsheet** - `QnA.md`: 44 questions with a speakable English answer
  each, the numbers card, the six "we did not record that" sentences, a
  page-by-page index for interruptions, and a set of README-style traps
  (PEB is not a chemically amplified resist; 8.16 µm is pitch, not CD;
  the gate oxide was never verified directly). Facts come from
  `labs/LAB3_record_v2.md`, the `> ` notes in `SCRIPT.md`, and slide numbers
  in `md/slides/`.
* **Video** - the deck is deterministic: `?instant=1` for a settled frame,
  `?notr=1&at=<ms>` to park a mid-animation frame, `?et=<ms>` to freeze the JS
  timelines; `_shot/mk_sheet.sh` shows the exact query used per page. Per-page
  durations for an audio track are in `_shot/tts/timing.json`.

## Deliberate choices (please do not "fix" these)

- **The retained resist is one gate wide, not one island wide.** In the
  cross-section the gate stripe is 60 scene units on an ~8 um pitch, so the mask
  opening on either side of it covers the field; the island underneath stays
  wider than the gate on purpose (a gate crosses an island, it does not fill it).
- **The plasma is a background wash, not a shape.** It fills the whole cut with
  one continuous gradient so that a stripped mask or an etched trench simply
  shows gas; there is no outline to notice.
- **`shape-rendering="crispEdges"` on the etch card.** It removes 1-px
  anti-aliasing hairlines at the layer edges (they read as stray lines at 1×).
  The arcs therefore have a 1-px staircase at high zoom — intended trade.
- **The breakthrough bite is a quarter *ellipse*** (lateral 1.9 uu vs vertical
  5 uu ≈ 38 %), not a quarter circle: the spontaneous Cl reaction is much slower
  laterally than the ion-assisted vertical removal.
- **P15's resist-strip animation runs 6 s** (50 % faster than the first version)
  and the page is 6 s long to match.
- **The spin wind-down** integrates a constant deceleration in JS from the
  current angular speed and stops on a whole number of turns — that is what
  lands the primary flat facing down.
- **P18's cross-section is squeezed with `scaleX(.69)`** so the six layer labels
  fit inside the narrow card; `#xsWin` carries the same transform.
- **The standing cross-section shows the gate as a narrowed top-two-layer
  stripe** on `pat === "gates"` pages (not a dark block placed over the stack).
- **The PEB acid curve is redrawn per frame** with a decaying amplitude, so the
  same curve flattens instead of cross-fading into a second line.
