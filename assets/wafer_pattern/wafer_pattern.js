/*!
 * WaferPattern 2.0.0
 * Top-surface die pattern for the 200 mm wafer of the LAB3 gate-formation deck
 * (IH2659 NanoFabrication).  Plain ES5, no build step, no imports, no deps.
 * Exposes exactly one global: WaferPattern.
 *
 *   var g = WaferPattern.build({ colors:{...}, states:["before","resist","gates"] });
 *   document.getElementById("waferSvg").appendChild(g);   // or any <g> inside it
 *   WaferPattern.show(g, "gates");                        // before | resist | gates
 *
 * Host geometry it is written against: an <svg viewBox="0 0 760 760"> with the
 * disc at (380,380) r=300 and the primary flat as the chord y=648.
 *
 * v2: cell squashed to 66.67 x 85.2 (aspect 0.78), wide scribe lanes (20 uu
 * clear) around every cell, and small alignment marks moved into the lane
 * crossings.  The bottom lane centreline is the primary flat, so no cell is
 * ever cut by the flat.
 */
(function (root) {
  "use strict";

  var NS = "http://www.w3.org/2000/svg";
  var XLINK = "http://www.w3.org/1999/xlink";

  /* ------------------------------------------------------------------ *
   *  Geometry
   * ------------------------------------------------------------------ */

  /* Wafer body — must match the host wafer SVG (viewBox 0 0 760 760). */
  var GEO = {
    cx: 380,
    cy: 380,
    r: 300,
    flatY: 648,          /* primary flat: the chord y = 648                 */
    cols: 9,             /* 9 * 66.667 = 600 = 2r, tangent to the rim       */
    rows: 7,             /* 7 * 85.2 = 596.4, so the grid still covers y=80 */
    gridX0: 80,          /* = cx - r                                        */
    street: 10           /* scribe-lane half-width = inset of the content   */
  };
  GEO.cellW = (2 * GEO.r) / GEO.cols;              /*  66.6667           */
  GEO.cellH = 85.2;                                /*  was 142, now 3/5  */
  GEO.gridY0 = GEO.flatY - GEO.rows * GEO.cellH;   /*  51.6              */
  GEO.streetW = 2 * GEO.street;                    /*  20 uu clear lane  */
  GEO.contentW = GEO.cellW - 2 * GEO.street;       /*  46.6667           */
  GEO.contentH = GEO.cellH - 2 * GEO.street;       /*  65.2              */
  GEO.chordHalf = Math.sqrt(GEO.r * GEO.r -
                            (GEO.flatY - GEO.cy) * (GEO.flatY - GEO.cy));

  /* The cell grid is anchored so that one horizontal lane centreline lands
   * exactly on the primary flat (y = 648): gridY0 + rows*cellH === flatY.
   * The bottom die row's content therefore stops GEO.street above the flat
   * and nothing at all crosses the chord. */

  /* Unit cell, as fractions of the CONTENT box (cell minus the streets).
   * Proportions measured off labs/assets/pattern/unit_after.png (160x330)
   * and unit_before.png (111x243).  One cell = two island columns; each
   * column has a short island in the top (NFET) row and a tall island in the
   * bottom (PFET) row; a gate stripe is centred on each column and crosses
   * both islands. */
  var CELL = {
    /* fractions of contentW */
    colCx:    [0.219, 0.710],  /* island / gate column centres */
    islandW:  0.395,           /* active-region width          */
    gateW:    0.045,           /* gate stripe width            */
    bumpLen:  0.150,           /* contact-land stub, beyond the stripe */
    /* fractions of contentH */
    islTopCy: 0.0773, islTopH: 0.058,   /* short top islands   */
    islBotCy: 0.8803, islBotH: 0.120,   /* tall bottom islands */
    gateTop:  0.028, gateBot: 0.962,    /* gate stripe extent  */
    bumpCy:   [0.4364, 0.3167],         /* staggered: see note */
    bumpH:    0.073
  };

  /* Alignment marks: small dense-line blocks that sit inside the scribe
   * lanes, on the crossings of every second vertical and horizontal lane.
   * Sparse and regular; a block is emitted only where it fits entirely
   * inside the disc.  Orientation alternates by lane row (V, H, V, ...), so
   * the pattern of mark orientations reads deliberately. */
  var MARK = {
    size: 16,        /* block edge — must be < GEO.streetW            */
    pitch: 3,        /* line pitch inside a block                     */
    lines: 5,        /* lines per block                               */
    lineLen: 12,     /* line length                                   */
    stroke: 1.0,
    backingOpacity: 0.34,
    /* lane indices used for marks (lanes are numbered from gridX0/gridY0).
     * The vertical lanes come in mirror pairs about the wafer axis
     * (x = 380): 1 & 8, 3 & 6 — so the lattice reads symmetric. */
    vLanes: [1, 3, 6, 8],
    hLanes: [1, 3, 5]
  };

  var DEFAULT_COLORS = {
    island: "#efe6c4",                       /* active-region silicon  */
    gate:   "#e0738a",                       /* gate / poly stripe     */
    resist: "#f0a06a",                       /* photoresist            */
    field:  "#223c62",                       /* wafer base (not painted by build(); kept for reference) */
    mark:   "rgba(255,255,255,.45)",         /* alignment-mark lines   */
    markBacking: "#101d30"                   /* cleared window behind the mark lines */
  };
  var DEFAULT_EDGES = {
    island: "#c9bd93",
    gate:   "#b85974",
    resist: "#cf7f4f"
  };
  var STATES = ["before", "resist", "gates"];

  /* ------------------------------------------------------------------ *
   *  tiny helpers
   * ------------------------------------------------------------------ */

  function num(n) {
    return String(Math.round(n * 1000) / 1000);
  }

  function merge(base, over) {
    var out = {}, k;
    for (k in base) { if (base.hasOwnProperty(k)) out[k] = base[k]; }
    if (over) { for (k in over) { if (over.hasOwnProperty(k)) out[k] = over[k]; } }
    return out;
  }

  function wid(scope, name) {
    return "wp-" + scope + name;
  }

  function setHref(el, value) {
    el.setAttribute("href", value);
    try { el.setAttributeNS(XLINK, "xlink:href", value); } catch (e) { /* old IE */ }
  }

  function rect(el, x, y, w, h, rx, fill, stroke, sw, opacity) {
    if (w < 0.05 || h < 0.05) return;
    el.setAttribute("x", num(x));
    el.setAttribute("y", num(y));
    el.setAttribute("width", num(w));
    el.setAttribute("height", num(h));
    if (rx) el.setAttribute("rx", num(rx));
    el.setAttribute("fill", fill);
    if (stroke) {
      el.setAttribute("stroke", stroke);
      el.setAttribute("stroke-width", num(sw));
    }
    if (opacity !== undefined && opacity !== 1) el.setAttribute("opacity", num(opacity));
  }

  function mk(doc, tag) { return doc.createElementNS(NS, tag); }

  function rrect(doc, x, y, w, h, rx, fill, stroke, sw, opacity) {
    var r = mk(doc, "rect");
    rect(r, x, y, w, h, rx, fill, stroke, sw, opacity);
    return r;
  }

  /* Disc silhouette: the full circle minus the segment below the primary flat.
   * Start at the left end of the chord, sweep the long way (large-arc, sweep=1)
   * over the top of the disc to the right end, then close back along the chord. */
  function discPath() {
    var h = GEO.chordHalf;
    return "M " + num(GEO.cx - h) + " " + num(GEO.flatY) +
           " A " + num(GEO.r) + " " + num(GEO.r) + " 0 1 1 " +
           num(GEO.cx + h) + " " + num(GEO.flatY) + " Z";
  }

  /* ------------------------------------------------------------------ *
   *  <defs> content: one symbol per unit cell per state, plus marks
   * ------------------------------------------------------------------ */

  function cellSymbol(doc, id, state, colors, edges, opacity) {
    var s = GEO.street, CW = GEO.contentW, CH = GEO.contentH;
    var g = mk(doc, "g");
    g.setAttribute("id", id);

    /* --- active regions, drawn first (the gate stripes sit on top) --- */
    var islW = CELL.islandW * CW;
    var topH = CELL.islTopH * CH, botH = CELL.islBotH * CH;
    var i, cx;
    for (i = 0; i < 2; i++) {
      cx = s + CELL.colCx[i] * CW;
      /* top row: short island (NFET) */
      g.appendChild(rrect(doc,
        cx - islW / 2, s + CELL.islTopCy * CH - topH / 2, islW, topH, 1.6,
        colors.island, edges.island, 0.9, opacity.island));
      /* bottom row: taller island (PFET) */
      g.appendChild(rrect(doc,
        cx - islW / 2, s + CELL.islBotCy * CH - botH / 2, islW, botH, 2.0,
        colors.island, edges.island, 0.9, opacity.island));
    }

    if (state === "before") return g;

    /* --- gate stripes: one per column, crossing both islands.
     * "resist" = developed, resist still on; "gates" = resist stripped. --- */
    var fill = (state === "resist") ? colors.resist : colors.gate;
    var edge = (state === "resist") ? edges.resist : edges.gate;
    var gw = CELL.gateW * CW;
    var bumpLen = CELL.bumpLen * CW;
    var bumpH = CELL.bumpH * CH;
    var gateTop = s + CELL.gateTop * CH;
    var gateH = (CELL.gateBot - CELL.gateTop) * CH;

    for (i = 0; i < 2; i++) {
      cx = s + CELL.colCx[i] * CW;
      /* stripe, round-capped, reaching almost to the content-box edge */
      g.appendChild(rrect(doc,
        cx - gw / 2, gateTop, gw, gateH, gw / 2,
        fill, edge, 0.9, opacity.gate));
      /* contact-land stub on one side, between the N and P rows.
       * The two columns are staggered (see CELL.bumpCy) exactly as in
       * unit_after.png, which keeps the tiling from reading as a grid of
       * identical blobs. */
      g.appendChild(rrect(doc,
        cx - gw / 2, s + CELL.bumpCy[i] * CH - bumpH / 2,
        gw + bumpLen, bumpH, bumpH * 0.30,
        fill, edge, 0.9, opacity.gate));
    }
    return g;
  }

  function markSymbol(doc, id, vertical, colors, backing) {
    var g = mk(doc, "g");
    g.setAttribute("id", id);
    var s = MARK.size, half = s / 2, sp = MARK.pitch, nl = MARK.lines;
    var halfLen = MARK.lineLen / 2;

    if (backing) {
      var bg = mk(doc, "rect");
      rect(bg, -half, -half, s, s, 2, colors.markBacking, null, 0, MARK.backingOpacity);
      g.appendChild(bg);
    }
    for (var i = 0; i < nl; i++) {
      var p = (i - (nl - 1) / 2) * sp;
      var l = mk(doc, "line");
      if (vertical) {
        l.setAttribute("x1", num(p)); l.setAttribute("y1", num(-halfLen));
        l.setAttribute("x2", num(p)); l.setAttribute("y2", num(halfLen));
      } else {
        l.setAttribute("x1", num(-halfLen)); l.setAttribute("y1", num(p));
        l.setAttribute("x2", num(halfLen)); l.setAttribute("y2", num(p));
      }
      l.setAttribute("stroke", colors.mark);
      l.setAttribute("stroke-width", num(MARK.stroke));
      l.setAttribute("stroke-linecap", "butt");
      g.appendChild(l);
    }
    return g;
  }

  /* Mark positions: crossings of every second lane, kept only where the whole
   * block fits inside the disc.  Orientation alternates lane row by lane row. */
  function markList() {
    var out = [], half = MARK.size / 2, lim = GEO.r - 1;
    var a, b, x, y, dx, dy;
    for (a = 0; a < MARK.hLanes.length; a++) {
      for (b = 0; b < MARK.vLanes.length; b++) {
        x = GEO.gridX0 + MARK.vLanes[b] * GEO.cellW;
        y = GEO.gridY0 + MARK.hLanes[a] * GEO.cellH;
        dx = Math.max(Math.abs(x - GEO.cx) - half, 0);
        dy = Math.max(Math.abs(y - GEO.cy) - half, 0);
        if (dx * dx + dy * dy > lim * lim) continue;
        out.push({ x: x, y: y, v: (a % 2 === 0) });
      }
    }
    return out;
  }

  /* A cell is emitted only if its CONTENT box touches the disc (the streets
   * are empty, so a cell whose content is entirely outside the rim can be
   * dropped even though its grid box clips the circle). */
  function cellHitsDisc(x0, y0) {
    var xa = x0 + GEO.street, xb = x0 + GEO.cellW - GEO.street;
    var ya = y0 + GEO.street, yb = y0 + GEO.cellH - GEO.street;
    var dx = Math.max(GEO.cx - xb, 0, xa - GEO.cx);
    var dy = Math.max(GEO.cy - yb, 0, ya - GEO.cy);
    return dx * dx + dy * dy < GEO.r * GEO.r;
  }

  /* ------------------------------------------------------------------ *
   *  public API
   * ------------------------------------------------------------------ */

  function build(opts) {
    opts = opts || {};
    var doc = opts.document || document;
    var colors = merge(DEFAULT_COLORS, opts.colors);
    var edges = merge(DEFAULT_EDGES, opts.edges);
    var opacity = merge({ island: 0.94, gate: 0.96 }, opts.opacity);
    var states = (opts.states && opts.states.length) ? opts.states.slice() : STATES.slice();
    var scope = opts.scope ? String(opts.scope) + "-" : "";
    var visible = opts.show || states[0];
    var backing = (opts.markBacking === false) ? false : true;

    /* keep only states we know how to draw */
    var keep = [], i;
    for (i = 0; i < states.length; i++) {
      if (STATES.indexOf(states[i]) >= 0 && keep.indexOf(states[i]) < 0) keep.push(states[i]);
    }
    if (!keep.length) keep = STATES.slice();
    states = keep;
    if (states.indexOf(visible) < 0) visible = states[0];

    var g = mk(doc, "g");
    g.setAttribute("class", "wp-root");
    g.setAttribute("data-wp", "1");
    g.setAttribute("aria-label", "wafer surface pattern");

    /* ---- defs: clip + one cell symbol per state + two mark symbols ---- */
    var defs = mk(doc, "defs");

    var clip = mk(doc, "clipPath");
    clip.setAttribute("id", wid(scope, "clip-disc"));
    var sil = mk(doc, "path");
    sil.setAttribute("d", discPath());
    clip.appendChild(sil);
    defs.appendChild(clip);

    for (i = 0; i < states.length; i++) {
      defs.appendChild(cellSymbol(doc, wid(scope, "cell-" + states[i]),
                                  states[i], colors, edges, opacity));
    }
    defs.appendChild(markSymbol(doc, wid(scope, "mark-v"), true, colors, backing));
    defs.appendChild(markSymbol(doc, wid(scope, "mark-h"), false, colors, backing));
    g.appendChild(defs);

    /* ---- one group per state, all clipped to the disc silhouette ---- */
    var marks = markList(), c, m, u;
    for (i = 0; i < states.length; i++) {
      c = mk(doc, "g");
      c.setAttribute("id", wid(scope, states[i]));
      c.setAttribute("data-wp-state", states[i]);
      c.setAttribute("clip-path", "url(#" + wid(scope, "clip-disc") + ")");
      if (states[i] !== visible) c.setAttribute("display", "none");

      for (var row = 0; row < GEO.rows; row++) {
        for (var col = 0; col < GEO.cols; col++) {
          var x0 = GEO.gridX0 + col * GEO.cellW;
          var y0 = GEO.gridY0 + row * GEO.cellH;
          if (!cellHitsDisc(x0, y0)) continue;
          u = mk(doc, "use");
          setHref(u, "#" + wid(scope, "cell-" + states[i]));
          u.setAttribute("x", num(x0));
          u.setAttribute("y", num(y0));
          c.appendChild(u);
        }
      }
      for (m = 0; m < marks.length; m++) {
        u = mk(doc, "use");
        setHref(u, "#" + wid(scope, marks[m].v ? "mark-v" : "mark-h"));
        u.setAttribute("x", num(marks[m].x));
        u.setAttribute("y", num(marks[m].y));
        c.appendChild(u);
      }
      g.appendChild(c);
    }
    return g;
  }

  /* Show exactly one state group inside a root returned by build(). */
  function show(rootG, state) {
    if (!rootG || !rootG.childNodes) return false;
    var found = false, kids = rootG.childNodes;
    for (var i = 0; i < kids.length; i++) {
      var k = kids[i];
      if (!k.getAttribute) continue;
      var s = k.getAttribute("data-wp-state");
      if (!s) continue;
      if (s === state) {
        k.removeAttribute("display");
        if (k.style) k.style.opacity = "";
        found = true;
      } else {
        k.setAttribute("display", "none");
      }
    }
    return found;
  }

  var API = {
    version: "2.0.0",
    states: STATES.slice(),
    build: build,
    show: show,
    geometry: GEO,
    cell: CELL,
    mark: MARK,
    colors: DEFAULT_COLORS,
    discPath: discPath,
    /* world-space boxes the host can use for zooming */
    cellBox: { w: GEO.cellW, h: GEO.cellH },
    contentBox: { w: GEO.contentW, h: GEO.contentH }
  };

  root.WaferPattern = API;
}(typeof window !== "undefined" ? window
  : typeof global !== "undefined" ? global
  : this));
