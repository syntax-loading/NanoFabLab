# IH2659 / FIH3608 — LAB3 "Gate Formation" — process-flow deck

A single self-contained HTML slide deck that walks the whole LAB3 process, one
continuous camera take, 19 beats, ~15 min at 1× speed.

```
labs/
├── slides/
│   ├── lab3_process_flow.html   ← the deck (single file, no dependencies)
│   ├── README.md                ← this file
│   ├── .gitignore
│   └── _shot/
│       ├── mk_sheet.sh          ← renders all 19 beats + stitches a contact sheet
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
| 14 | Step 08 | Resist strip | O₂ ash, resist eaten from every side |
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

All three are base64 inside the HTML (search for `data:image/jpeg;base64`). The
originals are in `HT26 Lab 3/`:

| page | plate | original file |
|---|---|---|
| 2 | the "where we start" band | `Before process Captured Digital Sight 10 - EPI50X EPI BF 2.jpg` (cropped to a 7:1 band, rotated 0.405° to level) |
| 12 | Inspection ① | `after expose_ gate measuringCaptured Digital Sight 10 - EPI150X EPI BF.jpg` |
| 18 | Inspection ④ | `End of process Captured Digital Sight 10 - EPI150X EPI BF.jpg` |

To swap one: crop to the plate's aspect (1.38 : 1), re-encode as JPEG, replace the
base64 string — the plate CSS does the rounding, the shadow and the caption chip.

## Rendering the contact sheet

`_shot/mk_sheet.sh` renders all 19 pages with headless Chrome and stitches them
into `contact_sheet.png` (it points at a Playwright `chrome-headless-shell`
install; adjust `CHROME=` at the top if yours lives elsewhere). Pages 7, 14–17
and the coating pages are captured mid-animation with `?notr=1&at=…`, the rest
with `?instant=1`.

## Deliberate choices (please do not "fix" these)

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
