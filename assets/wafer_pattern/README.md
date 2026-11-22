# WaferPattern — top-surface die pattern for the LAB3 wafer

Independent asset for the gate-formation deck (IH2659 NanoFabrication, LAB3).
It replaces the JS-faked pattern the deck used to draw into `#gPattern`
(rows of cream dashes) and `#gGates` (rose stripes) with a real tiled unit cell.

Plain ES5, one file, no build step, no imports, no external dependencies.
No `Math.random()`, no gradients, no filters — the same bytes on every load.

| file | what it is |
| --- | --- |
| `wafer_pattern.js` | the asset: exposes one global `WaferPattern` |
| `wafer_pattern.svg` | standalone render, 760 × 760, all three states labelled |
| `preview.html` | dark preview page, three states side by side (+ legend) |
| `preview_before.png`<br>`preview_resist.png`<br>`preview_gates.png` | 800 × 800 headless renders, one per state |
| `preview_all.png` | 900 × 900 headless render of the whole preview page |

---

## 1. Integration (copy-paste)

```html
<!-- once, after the wafer <svg> exists in the DOM -->
<script src="labs/assets/wafer_pattern/wafer_pattern.js"></script>
<script>
  var wp = WaferPattern.build({
    colors: { island:"#efe6c4", gate:"#e0738a", resist:"#f0a06a", field:"#223c62" },
    states: ["before","resist","gates"]      // <- the defaults, may be omitted
  });
  document.getElementById("gPattern").appendChild(wp);  // or waferSvg directly
  WaferPattern.show(wp, "before");                      // switch state
</script>
```

That is the whole contract. `build()` returns a `<g>` (`class="wp-root"`) that is
ready to append into the deck's existing `<svg viewBox="0 0 760 760">`; it does
**not** paint the disc, the rim or the flat — the host already does that, and
the asset only draws what is on top of the wafer.

Switching states later — one call, no DOM surgery:

```js
WaferPattern.show(wp, "resist");   // "before" | "resist" | "gates"
```

The deck should stop toggling `#gGates` opacity: gates now live inside the
state groups (`wp-resist` = resist-coloured, `wp-gates` = rose). Keep the deck's
own `#cResistBlanket` / `#cTint` overlays as they are — they sit above the
pattern and still work.

---

## 2. API

### `WaferPattern.build(opts) -> SVGGElement`

| option | default | meaning |
| --- | --- | --- |
| `colors.island` | `#efe6c4` | active-region silicon |
| `colors.gate` | `#e0738a` | gate stripe + contact land |
| `colors.resist` | `#f0a06a` | photoresist left on the gate areas |
| `colors.field` | `#223c62` | wafer base — informational only, `build()` never paints it |
| `colors.mark` | `rgba(255,255,255,.45)` | alignment-mark fine lines |
| `colors.markBacking` | `#101d30` | cleared window behind those lines |
| `states` | `["before","resist","gates"]` | which state groups to build |
| `show` | `states[0]` | which one is displayed initially |
| `scope` | `""` | id prefix, `"a"` → `wp-a-before`, … (needed for several instances in one document) |
| `opts.edges` | see source | hairline edge colours (island / gate / resist) |
| `opts.opacity` | `{island:0.94, gate:0.96}` | fill opacity |
| `opts.markBacking` | `true` | `false` drops the dark plate behind the mark lines |
| `opts.document` | `document` | for non-browser hosts (used by the generator) |

### `WaferPattern.show(root, state) -> Boolean`

Shows exactly one state group of a root returned by `build()` and hides the
others (`display` attribute, so it survives the deck's CSS transitions),
returns `false` for an unknown state.

### read-only data

`WaferPattern.states`, `.version`, `.geometry` (`cx, cy, r, flatY, cols, rows,
gridX0, gridY0, cellW, cellH, street, streetW, contentW, contentH, chordHalf`),
`.cell` (content-box ratios), `.mark` (incl. `vLanes` / `hLanes`),
`.colors`, `.discPath()`, `.cellBox` (`{w,h}` of a cell),
`.contentBox` (`{w,h}` of the drawn content — handy for zooming the P2 view).

---

## 3. Geometry (must match the host wafer SVG)

```
viewBox        0 0 760 760
disc centre    (380, 380)          r = 300
primary flat   chord y = 648
grid           9 columns × 7 rows, origin (80, 51.6)
cell           66.6667 × 85.2 uu      (aspect 0.782 — squashed from the old 142)
scribe lane    20 uu clear (10 uu inset on every cell edge)
content box    46.6667 × 65.2 uu      (54 % of the cell area, was 78 % in v1)
visible cells  57 of 63 grid positions (content-box vs disc test)
```

The disc silhouette (`wp-clip-disc`) is the circle with the flat segment cut
away: `M 245.182 648 A 300 300 0 1 1 514.818 648 Z`. Both state groups are
clipped to it, so anything outside the wafer is cut at the rim, exactly as
specified. (The deck's own flat line is drawn from x = 247.6 to 512.4; those
points sit ~2.4 uu inside the true chord ends — a host rounding detail, the
silhouette uses the exact circle–chord intersection.)

### Why no cell is cut by the flat

Rows are laid out **upwards from the flat**, with a row of cells one cellH tall
above it:

```
lane 7  y 638 … 658   centreline 648 === the primary flat
row  6  y 562.8 … 648         <- bottom die row: content stops at y = 638
row  5  y 477.6 … 562.8
…
row  0  y  51.6 … 136.8       <- top row, mostly clipped by the rim
```

because `gridY0 = flatY − rows·cellH = 648 − 7 × 85.2 = 51.6`. The flat
therefore lies on the **centreline of the last horizontal lane** (lane 7, the
bottom edge of the grid): the bottom row's content ends 10 uu above the chord,
so **nothing at all crosses y = 648** — the flat cannot cut a cell, and it is
squarely inside a lane. Vertically the grid is not re-centred (7 rows reach
y = 51.6, beyond the disc top at 80) — the rim simply clips the top row, which
leaves the same edge-exclusion ring a real wafer has and keeps the flat row
exact.

Columns are anchored the same way: `gridX0 = cx − r`, so 9 cells span exactly
the disc width and the outer column boundaries are tangent to the rim.

---

## 4. The unit cell

The drawing sits inside the content box; its ratios were measured off the two
reference PNGs (`labs/assets/pattern/unit_before.png` 111 × 243 and
`unit_after.png` 160 × 330), which agree to a few percent — the mean was used
where they differ.

```
                     fraction of contentW   after ref   before ref
  island column cx   0.219 / 0.710          0.219/0.709  0.225/0.739
  island width       0.395                  0.350        0.405
  gate stripe width  0.045                  0.044        —
  contact-land stub  0.150  beyond stripe   0.150        —
                     fraction of contentH
  short top island   0.058  at cy 0.0773    0.052        0.070
  tall bottom island 0.120  at cy 0.8803    0.112        0.128
  gate extent        0.028 … 0.962          0.024…0.964  —
  stub height        0.073                  0.073        —
  stub height (col1) 0.4364, (col2) 0.3167  staggered, see below
```

* **before lithography** — 4 active-region islands only: two short ones on the
  top row (NFET) and two taller ones on the bottom row (PFET), one island of
  each per column.
* **after lithography** — the same cell plus one gate stripe per column,
  centred on its island and crossing both islands (drawn on top, so the island
  reads as "gate over active region"). Each stripe carries a **contact land**:
  a rounded stub on one side, in the empty band between the N row and the P row.
* **developed, resist not stripped** (`resist`) — identical geometry, the gate
  areas keep the photoresist colour. After stripping they take the gate colour
  (`gates`). Only the fill/stroke colour differs; the cell symbol is built once
  per state in `<defs>` and placed with `<use>`.

The reference cell is 111 × 243 (0.46 : 1); this cell is 66.67 × 85.2
(0.78 : 1) — the drawing is stretched to the content box, which is the point of
the squash: a wider, shorter die with the same internal reading order.

**Interpretation notes** (the two references disagree slightly):

1. `unit_after.png` contains one cell of 160 × 330 (two columns), not two
   cells: the two stripes inside it carry their stubs at *different heights*
   (y ≈ 144 and y ≈ 105 of 330). That vertical stagger is reproduced exactly,
   which also keeps the tiled field from reading as a grid of identical blobs.
2. `unit_before.png` draws the same islands chunkier (island width 0.405 of the
   cell vs 0.350 in `unit_after.png`); the mean is used so the two states share
   one cell.
3. Both stubs point to +x, as in the reference.
4. The reference shows the bottom islands no wider than the top ones, so the
   "taller/**wider** PFET" wording is honoured by height only.

---

## 5. Alignment marks

Small dense-line blocks that live **in the scribe lanes**, on the crossings of
every second lane — sparse and regular, never on die content:

```
block        16 × 16 uu  (5 lines, pitch 3, length 12, stroke 1.0) — fits inside
             the 20 uu lane with 2 uu clearance on each side
vertical     x = 146.7, 280.0, 480.0, 613.3   (lane pairs 1&8, 3&6 — mirror
lanes        pairs about the wafer axis x = 380, so the lattice reads symmetric)
horizontal   y = 136.8, 307.2, 477.6          (lanes 1, 3, 5)
result       12 candidate crossings, 10 emitted: the two top-outer crossings
             (146.7 / 613.3, 136.8) fall outside the rim and are dropped
orientation  alternates lane row by lane row: y=136.8 vertical,
             y=307.2 horizontal, y=477.6 vertical
```

Each block sits on a 0.34-opacity cleared plate so the lines read over the
wafer base. `build({markBacking:false})` removes it.

---

## 6. Performance / node budget

| | before | resist | gates |
| --- | --- | --- | --- |
| `<use>` placements | 57 cells + 10 marks | same | same |
| drawn primitives | **288** | **516** | **516** |

The whole asset is **245 DOM elements** (201 `<use>`, 22 `<rect>`, 10 `<line>`,
40 in `<defs>`). Each unit cell exists once per state in `<defs>` and is placed
by `<use>`, so a state costs 57 references, not 57 subtrees — far inside the
1500-node budget while the deck animates 10 stacked 3D discs.

Line work is 0.9 (`island`/`gate` edges), 1.0 (mark lines) user units — no
hairlines, nothing below 0.6, so it survives the ~4× zoom onto a few cells.

---

## 7. Re-rendering the previews

```bash
CHROME="C:/Users/16329/AppData/Local/ms-playwright/chromium_headless_shell-1243/chrome-headless-shell-win64/chrome-headless-shell.exe"
BASE="file:///D:/documents/Visual%20Studio%202022/atKTH/NanoFab/labs/assets/wafer_pattern"

# all three states on one dark page (900 x 900)
"$CHROME" --headless --no-sandbox --disable-gpu --hide-scrollbars \
  --force-device-scale-factor=1 --window-size=900,900 --virtual-time-budget=2500 \
  --screenshot=preview_all.png "$BASE/preview.html"

# one state per 800 x 800 PNG (preview.html#before | #resist | #gates)
for st in before resist gates; do
  "$CHROME" --headless --no-sandbox --disable-gpu --hide-scrollbars \
    --force-device-scale-factor=1 --window-size=800,800 --virtual-time-budget=2500 \
    --screenshot="preview_$st.png" "$BASE/preview.html#$st"
done
```

`wafer_pattern.svg` is generated from `wafer_pattern.js` itself (so the two can
never drift) by a one-off Node script with a ~30-line fake DOM; it is not part
of the shipped asset and needs no build step to use.

---

## 8. Changelog

* **2.0.0** — cell squashed 142 → 85.2 uu (aspect 0.78), 20 uu scribe lanes all
  round, content shrunk to the content box, 9 × 7 grid, flat now on the
  bottom-lane centreline (nothing crosses it), alignment marks reduced 32 → 16
  uu and moved out of the die area onto lane crossings (hexagon layout dropped).
* **1.0.0** — first version: 9 × 4 cells of 66.67 × 142, content filling the
  cell, 7 hexagon + centre marks of 32 uu inside the die area.
